---
name: vieneu-tts
description: Đọc tiếng Việt thành giọng nói (text-to-speech) bằng VieNeu-TTS - chạy trên máy, miễn phí, 25 giọng có sẵn Bắc/Trung/Nam và clone giọng từ 3-8 s ghi âm. Dùng khi cần giọng đọc / lồng tiếng / voiceover / thuyết minh tiếng Việt cho video training kho hoặc bất kỳ video HyperFrames nào, khi người dùng nói "đọc", "lồng tiếng", "giọng đọc", "TTS", "text to speech".
---

# VieNeu-TTS – giọng đọc tiếng Việt

Nguồn: https://github.com/pnnbao97/VieNeu-TTS (Apache 2.0). Mô hình mặc định **v3 Turbo** (48 kHz,
CPU chạy ONNX không cần torch, GPU dùng PyTorch). Với tiếng Việt, dùng skill này thay cho
`npx hyperframes tts` (Kokoro) của `media-use`.

## Cài đặt (một lần)

```bash
pip install vieneu            # CPU, torch-free (Python ≥ 3.10)
pip install "vieneu[cuda]"    # GPU NVIDIA trên Linux
```

Lần chạy đầu tải model từ `huggingface.co` (`pnnbao-ump/VieNeu-TTS-v3-Turbo`,
`OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano`). Nếu mạng chặn huggingface.co (proxy 403), báo người dùng
cần mở host đó cho môi trường – đừng thay bằng giọng khác mà không hỏi.

## Cách dùng – script `scripts/vieneu_tts.py`

```bash
S=.claude/skills/vieneu-tts/scripts/vieneu_tts.py
python3 $S "Xin chào các bạn." -o vo/hello.wav                 # 1 câu
python3 $S --lines script.txt -o video-x/assets/vo/            # mỗi dòng 1 clip (# và dòng trống bị bỏ)
python3 $S --json lines.json -o video-x/assets/vo/ --format mp3
python3 $S "..." --ref-audio giong_mau.wav -o vo/clone.wav     # clone giọng
python3 $S --list-voices
```

`lines.json`: `[{"id": "c01-s02", "text": "...", "voice": "Mai Anh"}, "chuỗi thường cũng được"]`.
Chế độ hàng loạt ghi `<id>.<ext>` cho từng câu + `manifest.json` (`id, file, duration, text, voice`).
**Dựng timeline theo `duration` thật trong manifest**, không đoán độ dài câu.

Tùy chọn: `--voice`, `--ref-audio` (+ `--no-denoise` nếu file đã sạch), `--speed 1.1` (ffmpeg atempo,
giữ cao độ), `--format wav|mp3|m4a`, `--seed N` (chạy lại ra giống nhau), `--temperature` (mặc định 0.8;
thấp hơn = đều hơn), `--precision int8` (CPU nhanh ~2×, cần CPU có VNNI), `--mode v3nano` (24 kHz, cho CPU yếu –
tên giọng khác, xem `--list-voices`), `--no-watermark` (mặc định thư viện gắn watermark âm thanh).

Python trực tiếp khi cần:

```python
from vieneu import Vieneu
tts = Vieneu()                                   # v3 Turbo
audio = tts.infer("Văn bản...", voice="Mai Anh") # numpy float32 48 kHz; câu dài tự chia đoạn
tts.save(audio, "out.wav")
tts.infer("...", ref_audio="mau.wav")            # clone; tts.add_voice("Tên", "mau.wav"); tts.save_voices()
```

## Giọng có sẵn (v3 Turbo)

| Vùng | Nam | Nữ |
| --- | --- | --- |
| Bắc | **Hải Đăng** (mặc định, tự nhiên), Thiện Minh (kể chuyện), Minh Đức (tin tức), Adam bựa, Thiền Tâm Đức, Phạm Tuyên, Xuân Vĩnh, Thanh Bình, Quốc Tuấn | **Mai Anh** (tin tức), Trúc Ly, Ngọc Huyền, Ngọc Linh, Đoan Trang, Quỳnh Anh |
| Trung | Quang Sơn | Ngọc Trân |
| Nam | Minh Triết (tin tức), Thái Sơn, Đức Trí, Adam | Thùy Dung (tin tức), Thục Đoan, Mỹ Duyên, Kim Thanh |

Video training kho: mặc định **Hải Đăng** cho người dẫn/giảng viên, **Mai Anh** nếu cần giọng nữ.
Giữ một giọng cho cả video; hỏi người dùng trước khi đổi giọng hay vùng miền.

## Viết văn bản cho TTS

- Viết như nói: câu ngắn, dấu câu rõ (dấu phẩy = ngắt nhẹ, dấu chấm = ngắt dài, xuống đoạn = ngắt dài hơn).
- Mã/viết tắt đọc sai thì viết lại theo cách đọc trong văn bản cho TTS (phụ đề vẫn giữ nguyên):
  "WMS" → "đáp-bờ-liu em ét", "LPN" → "eo pê en", "PDA" → "pê đê a", "DO" → "đê ô", "02F" → "không hai ép".
  Nghe thử rồi mới sửa – bộ chuẩn hóa sea-g2p đã xử lý được nhiều số, ngày, đơn vị.
- Thẻ cảm xúc (thử nghiệm): `[cười]`, `[thở dài]`, `[hắng giọng]` – không dùng trong video training.

## Ghép vào video HyperFrames

1. Lấy câu thoại/phụ đề của từng cảnh → `lines.json` (id theo cảnh) → chạy script vào `<video>/assets/vo/`.
2. Đọc `manifest.json`; mỗi cảnh dài ít nhất `duration` + ~0.4 s đệm. Nếu generator đang tính thời lượng
   cảnh theo phụ đề (ví dụ `tools/build_*.py`), thay bằng `duration` của clip.
3. Mỗi clip là một `<audio id="vo-c01-s02" src="assets/vo/c01-s02.mp3">` đặt đúng giờ bắt đầu câu
   (luật `<audio>` trong skill `hyperframes`: có `id`, không `play()`/seek). Hạ nhạc nền khi có giọng
   (xem `media-use` → `references/audio.md`).
4. Nghe lại vài câu trước khi render cả video; câu nào đọc sai thì sửa văn bản TTS và chỉ chạy lại câu đó
   (`--json` với một phần tử, cùng `id`).
