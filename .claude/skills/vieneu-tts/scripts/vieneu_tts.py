#!/usr/bin/env python3
"""Vietnamese text-to-speech with VieNeu-TTS (https://github.com/pnnbao97/VieNeu-TTS).

Install once:  pip install vieneu   (CPU, torch-free; GPU: pip install "vieneu[cuda]")
The first run downloads the model from huggingface.co (pnnbao-ump/VieNeu-TTS-v3-Turbo).

Examples
  # one clip
  python3 vieneu_tts.py "Xin chào các bạn." -o out/hello.wav
  # one clip per line of a text file (blank lines and lines starting with # are skipped)
  python3 vieneu_tts.py --lines script.txt -o out/vo/
  # JSON list: [{"id": "s01", "text": "...", "voice": "Mai Anh"}, ...]
  python3 vieneu_tts.py --json lines.json -o out/vo/ --format mp3
  # clone a voice from a 3-8 s reference clip
  python3 vieneu_tts.py "..." --ref-audio my_voice.wav -o out/clone.wav
  # list preset voices
  python3 vieneu_tts.py --list-voices

Batch modes write <id>.<ext> per line plus manifest.json with each clip's duration,
so a video timeline can be laid out from real speech lengths.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
import wave
from pathlib import Path


def slug(i, text):
    ascii_ = unicodedata.normalize("NFKD", text.lower().replace("đ", "d")).encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-z0-9]+", "-", ascii_)[:24].strip("-")
    return f"{i:03d}-{base}" if base else f"{i:03d}"


def wav_duration(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / float(w.getframerate())


def to_format(wav_path, fmt, speed):
    """Optional ffmpeg pass: change tempo and/or encode to mp3/m4a. Returns the final path."""
    if fmt == "wav" and speed == 1.0:
        return wav_path
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg is needed for --format other than wav or --speed != 1")
    out = wav_path.with_suffix("." + fmt)
    tmp = out if out != wav_path else wav_path.with_name(wav_path.stem + ".tmp.wav")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path)]
    if speed != 1.0:
        cmd += ["-filter:a", f"atempo={speed}"]
    if fmt == "mp3":
        cmd += ["-codec:a", "libmp3lame", "-q:a", "2"]
    elif fmt == "m4a":
        cmd += ["-codec:a", "aac", "-b:a", "192k"]
    subprocess.run(cmd + [str(tmp)], check=True)
    if tmp != out:  # wav with speed change
        tmp.replace(wav_path)
        return wav_path
    wav_path.unlink()
    return out


def load_items(args):
    if args.json:
        data = json.loads(Path(args.json).read_text(encoding="utf-8"))
        items = []
        for i, d in enumerate(data, 1):
            if isinstance(d, str):
                d = {"text": d}
            items.append({"id": d.get("id") or slug(i, d["text"]), **d})
        return items
    if args.lines:
        lines = [l.strip() for l in Path(args.lines).read_text(encoding="utf-8").splitlines()]
        lines = [l for l in lines if l and not l.startswith("#")]
        return [{"id": slug(i, t), "text": t} for i, t in enumerate(lines, 1)]
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("text", nargs="?", help="text to speak (single clip)")
    p.add_argument("--lines", help="text file, one clip per line")
    p.add_argument("--json", help='JSON list of {"id","text","voice"?,"ref_audio"?} or strings')
    p.add_argument("-o", "--out", default="tts-out", help="output file (single) or directory (batch)")
    p.add_argument("--voice", help="preset voice name (default: the model's own, Hải Đăng on v3turbo)")
    p.add_argument("--ref-audio", help="3-8 s reference clip to clone (overrides --voice)")
    p.add_argument("--no-denoise", action="store_true", help="skip denoising the reference clip")
    p.add_argument("--mode", default="v3turbo", choices=["v3turbo", "v3nano"],
                   help="v3turbo = 48 kHz, best quality (default); v3nano = 24 kHz, for weak CPUs")
    p.add_argument("--precision", default="fp32", choices=["fp32", "int8"],
                   help="CPU only; int8 is ~2x faster but needs a VNNI CPU")
    p.add_argument("--temperature", type=float, default=0.8)
    p.add_argument("--seed", type=int, help="fix randomness so re-runs sound the same")
    p.add_argument("--speed", type=float, default=1.0, help="tempo change via ffmpeg atempo (0.5-2.0)")
    p.add_argument("--format", default="wav", choices=["wav", "mp3", "m4a"])
    p.add_argument("--no-watermark", action="store_true", help="disable the built-in audio watermark")
    p.add_argument("--list-voices", action="store_true")
    args = p.parse_args()

    try:
        from vieneu import Vieneu
    except ImportError:
        sys.exit("vieneu is not installed: pip install vieneu   (GPU: pip install \"vieneu[cuda]\")")

    kw = {}
    if args.mode == "v3turbo":
        kw["precision"] = args.precision
    tts = Vieneu(mode=args.mode, **kw)

    if args.list_voices:
        for label, vid in tts.list_preset_voices():
            print(f"{vid}\t{label}")
        return

    items = load_items(args)
    single = items is None
    if single:
        if not args.text:
            p.error("give text, --lines or --json")
        items = [{"id": Path(args.out).stem, "text": args.text}]
        out_dir = Path(args.out).parent
    else:
        out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.seed is not None:
        import random
        import numpy as np
        random.seed(args.seed)
        np.random.seed(args.seed)
        try:
            import torch
            torch.manual_seed(args.seed)
        except ImportError:
            pass

    manifest = []
    for it in items:
        ref = it.get("ref_audio") or args.ref_audio
        infer_kw = dict(temperature=args.temperature, apply_watermark=not args.no_watermark)
        infer_kw["denoise"] = not args.no_denoise
        if args.seed is not None:
            infer_kw["seed"] = args.seed
        voice = it.get("voice") or args.voice
        if ref:
            infer_kw["ref_audio"] = ref
        elif voice:
            infer_kw["voice"] = voice
        audio = tts.infer(it["text"], **infer_kw)
        wav_path = (Path(args.out) if single else out_dir / f"{it['id']}.wav").with_suffix(".wav")
        tts.save(audio, str(wav_path))
        dur = wav_duration(wav_path)
        final = to_format(wav_path, args.format, args.speed)
        if args.speed != 1.0:
            dur /= args.speed
        manifest.append({"id": it["id"], "file": final.name, "duration": round(dur, 3),
                         "text": it["text"], "voice": "clone:" + Path(ref).name if ref else (voice or "default")})
        print(f"{final}  {dur:.2f}s", flush=True)

    if not single:
        (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"manifest: {out_dir / 'manifest.json'}  total {sum(m['duration'] for m in manifest):.1f}s")


if __name__ == "__main__":
    main()
