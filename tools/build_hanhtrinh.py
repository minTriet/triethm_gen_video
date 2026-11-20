"""Video "Hành trình tạo kỹ năng làm video" -> ./video-hanhtrinh
Run: python3 tools/build_hanhtrinh.py
Kịch bản: source/Prompt_Video_Hanh_trinh_tao_skill_video.md (v2) · storyboard design/storyboard-hanh-trinh.html (đã duyệt).
Có giọng đọc VieNeu-TTS (skill vieneu-tts, giọng Hải Đăng): câu thoại + văn bản đọc trong
source/vo_hanh_trinh_30s.json, clip trong video-hanhtrinh/assets/vo/ (manifest.json).
Thời lượng mỗi câu = độ dài clip thật + đệm, không đoán theo số chữ.
"""
import html as _h
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from kit import C, stick, walk_js, pose_js, REST  # noqa: E402
import stage as st  # noqa: E402
from build_full import build_all  # noqa: E402
from parts import svg_layer  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "video-hanhtrinh")
INK, MUTED, BLUE, ORANGE, GREEN = C["ink"], "#4F5A69", C["blue"], C["orange"], C["green"]
ORANGE_D, GREEN_D = "#C45A00", "#1A8048"   # bản đậm cho chữ trên nền sáng (đủ tương phản)
GAP, PAD = 0.15, 0.3            # khoảng lặng giữa hai câu · đệm sau mỗi clip
VO_VOL = 1.0

LINES = {d["id"]: d for d in json.load(open(os.path.join(ROOT, "source", "vo_hanh_trinh_30s.json"), encoding="utf-8"))}
MAN = {m["id"]: m for m in json.load(open(os.path.join(OUT, "assets", "vo", "manifest.json"), encoding="utf-8"))}


class VScene:
    """Một cảnh có giọng đọc: mỗi câu giữ đúng độ dài clip + PAD."""

    def __init__(self, cid, vo_ids, build, lead=0.4, tail=1.0, pre=None, caps=None):
        self.cid, self.build, self.lead, self.tail = cid, build, lead, tail
        self.vo = list(vo_ids)
        caps = caps or {}
        self.lines = [caps.get(v, LINES[v]["sub"]) for v in self.vo]
        self.sfx = []
        t, self.T, self.E = lead, [], []
        for i, v in enumerate(self.vo):
            t += (pre or {}).get(i, 0)
            d = MAN[v]["duration"] + PAD
            self.T.append(round(t, 2)); self.E.append(round(t + d, 2))
            t += d + GAP
        self.D = round((t - GAP if self.vo else t) + tail, 2)


def esc(s):
    return _h.escape(s, quote=False)


def floor_bg(y=830):
    return (f'<div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,'
            f'{C["ground"]} 0%,{C["ground"]} {y/10.8:.1f}%,{C["floor"]} {y/10.8:.1f}%,{C["floor"]} 100%)"></div>')


def wave_js(fid, t, n=4):
    js = pose_js(fid, t, {"armR": (-150, -24)}, dur=0.3, ease="power2.out")
    for k in range(n):
        js += f'tl.to("#{fid}-foreR",{{rotation:{-50 if k % 2 == 0 else -5},svgOrigin:"0 0",duration:0.22,ease:"sine.inOut"}},{t + 0.3 + k * 0.22:.2f});\n'
    return js


def screen_card(cid, src, x, y, w, label):
    h = round(w * 9 / 16)
    return (f'<div id="{cid}" class="abs" style="left:{x}px;top:{y}px;width:{w + 20}px;opacity:0">'
            f'<div style="background:#2B3646;border-radius:18px;padding:10px">'
            f'<img src="{src}" style="display:block;width:{w}px;height:{h}px;object-fit:cover;border-radius:8px"/></div>'
            f'<div style="text-align:center;margin-top:16px"><span style="display:inline-block;background:{INK};color:#fff;'
            f'font-size:28px;font-weight:700;border-radius:26px;padding:8px 26px">{label}</span></div></div>')


def pop(sel, t, dur=0.4, s0=0.6):
    return f'tl.fromTo("{sel}",{{opacity:0,scale:{s0}}},{{opacity:1,scale:1,duration:{dur},ease:"back.out(1.8)",transformOrigin:"50% 50%"}},{t:.2f});\n'


def rise(sel, t, dy=24, dur=0.45):
    return f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"power3.out"}},{t:.2f});\n'


# ============================================================ MỞ ĐẦU (storyboard màn 01)
def intro():
    def build(T, D):
        thumbs = [("kho", "Kho khô · 5:09"), ("tc", "Hàng TC · 2:12"), ("cxad", "CXAD · 5:20"), ("deck", "Deck · 17 slide")]
        cards = "".join(screen_card(f"in-t{i}", f"assets/img/{k}.jpg", 1060 + (i % 2) * 410, 140 + (i // 2) * 330, 350, lab)
                        for i, (k, lab) in enumerate(thumbs))
        body = floor_bg() + f"""
    <div id="in-tag" class="abs" style="left:120px;top:170px;opacity:0"><span style="display:inline-block;background:{ORANGE_D};color:#fff;
      font-size:28px;font-weight:900;letter-spacing:.08em;border-radius:24px;padding:8px 24px">HÀNH TRÌNH</span></div>
    <div class="abs" style="left:120px;top:250px;font-size:92px;font-weight:900;line-height:1.18">
      <div id="in-l1" style="opacity:0">Từ một prompt</div><div id="in-l2" style="opacity:0">đến một kỹ năng</div>
      <div id="in-l3" style="opacity:0;color:{BLUE}">làm video</div></div>
    <div id="in-chip" class="abs" style="left:120px;top:640px;opacity:0"><span style="display:inline-block;background:{GREEN};color:#fff;
      font-size:32px;font-weight:800;border-radius:30px;padding:10px 32px">2 ngày · 27 phiên bản</span></div>
    {cards}
    {svg_layer(f'<g transform="translate(860,830)"><g id="in-man">{stick("in-man", "instructor", scale=2.0)}</g></g>')}"""
        js = rise("#in-tag", 0.1) + rise("#in-l1", 0.25) + rise("#in-l2", 0.45) + rise("#in-l3", 0.65)
        js += 'tl.fromTo("#in-man",{x:-260},{x:0,duration:1.1,ease:"power1.out"},0.2);\n' + walk_js("in-man", 0.2, 1.3)
        js += wave_js("in-man", 1.4)
        js += pose_js("in-man", 2.75, {"armR": REST["armR"]}, dur=0.3)
        # "ba video" → 3 khung video, "một bộ slide" → deck, "hai ngày" → chip
        for i, t in enumerate([T[0] + 0.5, T[0] + 0.85, T[0] + 1.2, T[0] + 1.85]):
            js += pop(f"#in-t{i}", t)
        js += pop("#in-chip", T[0] + 2.6, s0=0.4)
        js += pose_js("in-man", T[1] + 0.2, {"armR": (-100, -40)}, dur=0.35)   # chỉ về phía khán giả
        return body, "", js
    s = VScene("intro", ["c01-1", "c01-2"], build, lead=0.6, tail=1.0)
    s.sfx = [(0.2, "whoosh.mp3", 0.15)]
    return s


# ============================================================ THẺ CHƯƠNG (storyboard màn 02)
CHAPTERS = ["Bắt đầu từ một prompt", "Xem nháp, góp ý thành luật", "Video sau kế thừa video trước", "Đóng gói thành kỹ năng"]


class Chapter:
    is_chapter = True

    def __init__(self, num):
        self.cid, self.num = f"chap{num}", num
        self.lines, self.T, self.E, self.vo = [], [], [], []
        self.D = 2.8
        self.sfx = [(0.0, "whoosh-short.mp3", 0.2)]

    def build(self, T, D):
        cid, n = self.cid, self.num
        toc = ""
        for i, s in enumerate(CHAPTERS):
            on = i == n - 1
            toc += (f'<div id="{cid}-i{i}" style="display:flex;align-items:center;gap:30px;margin-bottom:50px;opacity:0">'
                    f'<div style="width:76px;height:76px;border-radius:50%;border:4px solid {BLUE};background:{BLUE if on else "#fff"};'
                    f'color:{"#fff" if on else BLUE};font-size:36px;font-weight:900;display:flex;align-items:center;justify-content:center">{i + 1}</div>'
                    f'<div style="font-size:42px;font-weight:{800 if on else 600};color:{INK if on else MUTED}">{s}</div></div>')
        body = f"""
    <div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:{C['ground']}"></div>
    <div id="{cid}-bg" class="abs" style="left:0;top:0;width:760px;height:1080px;background:{BLUE}"></div>
    <div id="{cid}-txt" class="abs" data-layout-allow-overlap style="left:120px;top:420px;width:600px;color:#fff">
      <div style="font-size:34px;font-weight:700;color:#BFD8F5;letter-spacing:.12em">PHẦN {n}</div>
      <div style="font-size:84px;font-weight:900;line-height:1.15;margin-top:12px">{CHAPTERS[n - 1]}</div></div>
    <div class="abs" data-layout-allow-overlap style="left:900px;top:290px">{toc}</div>"""
        js = f'tl.fromTo("#{cid}-bg",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.4,ease:"power3.out"}},0);\n'
        js += f'tl.fromTo("#{cid}-txt",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},0.2);\n'
        for i in range(len(CHAPTERS)):
            js += f'tl.fromTo("#{cid}-i{i}",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.3,ease:"power2.out"}},{0.35 + i * 0.1:.2f});\n'
        js += f'tl.to("#{cid}-txt",{{opacity:0,x:40,duration:0.25,ease:"power2.in"}},{D - 0.4:.2f});\n'
        return body, "", js


# ============================================================ BƯỚC 1 (storyboard màn 03)
SKILLS = ["hyperframes", "hyperframes-cli", "hyperframes-registry", "media-use", "figma",
          "slideshow", "style-sampling", "reverse-any-video", "remotion-to-hyperframes"]


def skills():
    def build(T, D):
        bx, by = 760, 350
        tiles = ""
        for i, s in enumerate(SKILLS):
            x, y = bx + 30 + (i % 3) * 284, by + 100 + (i // 3) * 92
            fs = 20 if len(s) > 20 else 23 if len(s) > 14 else 26
            tiles += (f'<div id="sk-t{i}" class="abs" style="left:{x}px;top:{y}px;width:272px;height:72px;white-space:nowrap;letter-spacing:-0.3px;background:#fff;border:3px solid {INK};'
                      f'border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:{fs}px;font-weight:700;color:{BLUE};opacity:0">{s}</div>')
        body = floor_bg() + st.badge("sk-b", 1, "Cài bộ skill dựng video") + f"""
    <div id="sk-box" class="abs" style="left:{bx}px;top:{by - 50}px;width:900px;height:440px;opacity:0">
      <div class="abs" style="left:330px;top:0;width:240px;height:80px;border:10px solid {INK};border-bottom:none;border-radius:30px 30px 0 0"></div>
      <div class="abs" style="left:0;top:50px;width:900px;height:390px;background:{ORANGE};border:4px solid {INK};border-radius:24px"></div>
      <div class="abs" style="left:4px;top:54px;width:892px;height:66px;background:#D9781A;border-radius:20px 20px 0 0"></div></div>
    {tiles}
    <div id="sk-src" class="abs" style="left:{bx}px;top:{by + 420}px;width:900px;text-align:center;opacity:0"><span style="display:inline-block;
      background:{INK};color:#fff;font-size:28px;font-weight:700;border-radius:28px;padding:10px 30px">9 skill HyperFrames · heygen-com/hyperframes</span></div>
    {svg_layer(f'<g transform="translate(330,830)"><g id="sk-man">{stick("sk-man", "instructor", scale=1.9)}</g></g>')}"""
        js = f'tl.fromTo("#sk-b",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.25,ease:"power2.out"}},0.1);\n'
        js += pop("#sk-box", 0.25, s0=0.85)
        js += pose_js("sk-man", 0.5, {"armR": (-95, -5)}, dur=0.35)
        for i in range(len(SKILLS)):
            js += f'tl.fromTo("#sk-t{i}",{{opacity:0,y:-120}},{{opacity:1,y:0,duration:0.35,ease:"bounce.out"}},{T[0] + 0.6 + i * 0.2:.2f});\n'
        js += rise("#sk-src", T[0] + 2.7)
        js += f'tl.fromTo("#sk-b-ok",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.2,ease:"power3.out"}},{D - 0.8:.2f});\n'
        return body, "", js
    s = VScene("skills", ["c03-1"], build, lead=0.5, tail=1.6)
    s.sfx = [(("T", 0, 0.6), "click-soft.mp3", 0.15)]
    return s


# ============================================================ HYPERFRAMES LÀ GÌ (storyboard màn 04)
CODE = [('<div class="clip" data-start="0.3"', "html"), ('     data-duration="1.5">', "html"), ("  Xin chào các bạn.", "html"),
        ("</div>", "html"), ('<svg id="picker">…</svg>', "html"), ("", ""),
        ('tl.to("#picker", {', "gsap"), ("  x: 600, duration: 2", "gsap"), ("});", "gsap")]
CODE_COL = {"html": "#7FD3FF", "gsap": "#F2B233", "": "#fff"}


def hfexplain():
    def build(T, D):
        ex, ey, ew, eh = 120, 250, 720, 520
        code = "".join(
            f'<div id="hf-c{i}" class="cl cl-{k or "x"}" style="color:{CODE_COL[k]};opacity:0">{esc(s) or "&nbsp;"}</div>'
            for i, (s, k) in enumerate(CODE))
        bars = ""
        for i, (name, desc, col) in enumerate([("HTML", "cảnh, chữ, nhân vật", BLUE), ("CSS", "màu, font, bố cục", GREEN_D),
                                               ("GSAP", "chuyển động", ORANGE_D)]):
            bars += (f'<div id="hf-k{i}" class="abs" style="left:{ex + ew + 22}px;top:{ey + 90 + i * 140}px;opacity:0;display:flex;gap:16px">'
                     f'<div style="width:14px;height:76px;border-radius:4px;background:{col}"></div><div>'
                     f'<div style="font-size:34px;font-weight:900;color:{col}">{name}</div>'
                     f'<div style="font-size:26px;font-weight:600;color:{MUTED}">{desc}</div></div></div>')
        frames = ""
        for n in range(3):
            gy = 240 + n * 182
            fig = stick(f"hf-p{n}", "picker", 0.62)
            frames += (f'<div id="hf-f{n}" class="abs" style="left:1280px;top:{gy}px;width:330px;height:172px;background:#2B3646;border-radius:10px;opacity:0">'
                       f'<div class="abs" style="left:16px;top:14px;width:298px;height:144px;background:{C["ground"]};border-radius:4px;overflow:hidden">'
                       f'<div class="abs" style="left:0;top:106px;width:298px;height:38px;background:{C["floor"]}"></div>'
                       f'<svg class="abs" style="left:0;top:0" width="298" height="144" viewBox="0 0 298 144">'
                       f'<g transform="translate({44 + n * 95},126)">{fig}</g></svg></div>'
                       f'</div><div id="hf-n{n}" class="abs" style="left:1306px;top:{gy + 22}px;font-size:28px;font-weight:700;color:#fff;background:{INK};border-radius:10px;padding:0 12px;white-space:nowrap;opacity:0">khung {n * 15 + 1}</div>')
        body = floor_bg() + f"""
    <div id="hf-tag" class="abs" style="left:120px;top:60px;opacity:0"><span style="display:inline-block;background:{ORANGE_D};color:#fff;
      font-size:28px;font-weight:900;letter-spacing:.06em;border-radius:26px;padding:8px 26px">HYPERFRAMES LÀ GÌ?</span></div>
    <div id="hf-h" class="abs" style="left:120px;top:130px;font-size:56px;font-weight:900;opacity:0">Video = một trang web chạy theo thời gian</div>
    <div id="hf-ed" class="abs" style="left:{ex}px;top:{ey}px;width:{ew}px;height:{eh}px;background:#1B2430;border-radius:18px;opacity:0">
      <div style="height:52px;background:#2B3646;border-radius:18px 18px 0 0;padding:10px 30px;font-size:26px;font-weight:700;color:#AEBBCC">compositions/kho.html</div>
      <div style="padding:26px 34px">{code}</div></div>
    {bars}
    <div id="hf-ar1" class="abs" style="left:1150px;top:435px;width:126px;text-align:center;opacity:0">
      <div style="font-size:24px;font-weight:700;color:{MUTED};white-space:nowrap">trình duyệt</div>
      <div style="font-size:64px;font-weight:900;color:{ORANGE_D};line-height:1">→</div></div>
    {frames}
    <div id="hf-fps" class="abs" style="left:1280px;top:784px;width:330px;text-align:center;font-size:26px;font-weight:800;opacity:0">30 khung / giây</div>
    <div id="hf-ar2" class="abs" style="left:1712px;top:470px;font-size:64px;font-weight:900;color:{ORANGE_D};line-height:1;opacity:0">→</div>
    <div id="hf-mp4" class="abs" style="left:1785px;top:455px;width:110px;height:110px;border-radius:18px;background:{BLUE};color:#fff;
      font-size:32px;font-weight:900;display:flex;align-items:center;justify-content:center;opacity:0">MP4</div>
    <div id="hf-core" class="abs" style="left:1420px;top:34px;opacity:0"><span style="display:inline-block;background:#fff;border:5px solid {ORANGE};
      border-radius:20px;padding:10px 28px;font-size:40px;font-weight:900">Cốt lõi: <span style="color:#C45A00">frontend</span></span></div>"""
        css = (".cl{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:27px;font-weight:600;line-height:44px;white-space:pre}"
               ".cl.hi{background:rgba(255,255,255,.08)}")
        js = rise("#hf-tag", 0.0) + rise("#hf-h", 0.15) + rise("#hf-ed", 0.3, dy=30)
        for i in range(len(CODE)):   # code gõ ra từng dòng trong câu 1
            js += f'tl.fromTo("#hf-c{i}",{{opacity:0,x:-10}},{{opacity:1,x:0,duration:0.18}},{0.7 + i * 0.32:.2f});\n'
        # câu 2: HTML → CSS → GSAP sáng lần lượt, dòng code tương ứng được tô
        for i, dt in enumerate([0.1, 1.15, 2.2]):
            js += f'tl.to("#hf-k{i}",{{opacity:1,duration:0.25}},{T[1] + dt:.2f});\n'
            js += f'tl.fromTo("#hf-k{i}",{{x:-14}},{{x:0,duration:0.3,ease:"back.out(2)"}},{T[1] + dt:.2f});\n'
        js += f'tl.to(".cl-html",{{backgroundColor:"rgba(127,211,255,0.16)",duration:0.2}},{T[1] + 0.1:.2f});\n'
        js += f'tl.to(".cl-html",{{backgroundColor:"rgba(127,211,255,0)",duration:0.2}},{T[1] + 2.1:.2f});\n'
        js += f'tl.to(".cl-gsap",{{backgroundColor:"rgba(242,178,51,0.18)",duration:0.2}},{T[1] + 2.2:.2f});\n'
        # câu 3: trình duyệt chụp từng khung → MP4
        js += rise("#hf-ar1", T[2] + 0.1, dy=0)
        for n in range(3):
            js += pop(f"#hf-f{n}", T[2] + 0.7 + n * 0.55, s0=0.85) + rise(f"#hf-n{n}", T[2] + 0.8 + n * 0.55, dy=0)
        js += rise("#hf-fps", T[2] + 2.3, dy=10)
        js += rise("#hf-ar2", T[2] + 3.2, dy=0) + pop("#hf-mp4", T[2] + 3.5, s0=0.4)
        # câu 4: cốt lõi là frontend
        js += pop("#hf-core", T[3] + 0.9, s0=0.5)
        return body, css, js
    caps = {"c18-4": 'Vì vậy cốt lõi là <b style="color:#C45A00;font-weight:900">frontend</b>: dựng được trang web thì dựng được video.'}
    s = VScene("hfexplain", ["c18-1", "c18-2", "c18-3", "c18-4"], build, lead=0.4, tail=1.4, caps=caps)
    s.sfx = [(("T", 2, 3.5), "ping.mp3", 0.15)]
    return s


# ============================================================ assembly + giọng đọc
def timeline():
    return [intro(), Chapter(1), skills(), hfexplain()]


def add_voice(placed, total):
    idx = os.path.join(OUT, "index.html")
    src = open(idx, encoding="utf-8").read()
    tags = []
    for s, start in placed:
        for v, t in zip(getattr(s, "vo", []), s.T):
            m = MAN[v]
            a = round(start + t, 2)
            if a >= total:
                continue
            d = round(min(m["duration"], total - a), 2)
            tags.append(f'      <audio id="vo-{v}" class="clip" src="assets/vo/{m["file"]}" data-start="{a}" '
                        f'data-duration="{d}" data-track-index="8" data-volume="{VO_VOL}"></audio>')
    src = src.replace("    </div>\n    <script>", "\n".join(tags) + "\n    </div>\n    <script>", 1)
    open(idx, "w", encoding="utf-8").write(src)
    return len(tags)


if __name__ == "__main__":
    placed, total, kept = build_all(seq=timeline(), out=OUT)
    n = add_voice(placed, total)
    for s, start in placed:
        print(f"{start:7.2f}  {s.D:6.2f}  {s.cid}")
    print("TOTAL", total, "sfx", len(kept), "vo", n)
