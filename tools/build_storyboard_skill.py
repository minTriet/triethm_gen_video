"""Storyboard (khung duyệt) cho video "Hành trình tạo kỹ năng làm video".

Nguồn kịch bản: source/Prompt_Video_Hanh_trinh_tao_skill_video.md, mục [B1].
Mỗi màn = 1 khung 1920×1080 vẽ bằng SVG (cùng màu, font, nhân vật với các video kho),
kèm ghi chú hình/chuyển động, phụ đề và ô duyệt.

Chạy:  python3 tools/build_storyboard_skill.py <thư-mục-ảnh> <file-ra.html>
Thư mục ảnh chứa các .jpg trích từ renders/ và design/ (xem IMAGES bên dưới).
"""
import base64
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from kit import C, ROLE, stick, pda_svg, folder_svg, MANAGER_HOLD  # noqa: E402

IMG_DIR, OUT = sys.argv[1], sys.argv[2]
IMAGES = ["kho", "tc", "cxad", "t1draft", "ms2", "ql", "walk", "cx_v1", "cx_v2", "cx_v2b", "cx_v3",
          "deck-01", "deck-02", "deck-03", "deck-04", "deck-05"]
IMG = {}
for k in IMAGES:
    with open(os.path.join(IMG_DIR, k + ".jpg"), "rb") as f:
        IMG[k] = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

F = "'Be Vietnam Pro', system-ui, sans-serif"
MONOF = "ui-monospace, Menlo, Consolas, monospace"
INK, MUTED, BLUE, ORANGE, GREEN, RED = C["ink"], C["muted"], C["blue"], C["orange"], C["green"], C["red"]
WAVE = {"armR": (-140, -25)}
POINT_R = {"armR": (-95, -5)}
POINT_L = {"armL": (95, 5)}
THUMB = {"armR": (-70, -100)}
TYPE = {"armL": (22, -70), "armR": (-22, 70)}


# ------------------------------------------------------------------ primitives
def esc(s):
    return html.escape(s, quote=True)


def T(x, y, s, size=40, w=700, fill=INK, anchor="start", extra="", fam=None):
    return (f'<text x="{x}" y="{y}" font-family="{fam or F}" font-size="{size}" font-weight="{w}" '
            f'fill="{fill}" text-anchor="{anchor}" xml:space="preserve" {extra}>{esc(s)}</text>')


def rect(x, y, w, h, fill="#fff", r=16, stroke=None, sw=3, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st} {extra}/>'


def img(key, x, y, w, h, extra=""):
    return (f'<image href="{IMG[key]}" x="{x}" y="{y}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMidYMid slice" {extra}/>')


def screen(key, x, y, w, label=None, tilt=0):
    """Ảnh thật đặt trong khung 'màn hình' bo góc (16:9)."""
    h = w * 9 / 16
    cid = f"clip{abs(hash((key, x, y, w))) % 10**8}"
    g = (f'<g transform="rotate({tilt} {x + w / 2} {y + h / 2})">'
         f'<rect x="{x - 10}" y="{y - 10}" width="{w + 20}" height="{h + 20}" rx="18" fill="#2B3646"/>'
         f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/></clipPath>'
         f'<g clip-path="url(#{cid})">{img(key, x, y, w, h)}</g>')
    if label:
        g += pill(x + w / 2, y + h + 46, label, INK, "#fff", 28)
    return g + "</g>"


def pill(cx, cy, s, bg=INK, fg="#fff", size=26, pad=24):
    w = len(s) * size * (0.7 if s.isupper() else 0.58) + pad * 2
    return (rect(cx - w / 2, cy - size * 0.95, w, size * 1.9, bg, size * 0.95) +
            T(cx, cy + size * 0.36, s, size, 700, fg, "middle"))


def badge(n, s, chip=None):
    w = len(s) * 30 * 0.63 + 120
    out = (f'<circle cx="92" cy="84" r="30" fill="{ORANGE}" stroke="{INK}" stroke-width="3"/>'
           + T(92, 95, str(n), 30, 900, INK, "middle")
           + rect(138, 54, w, 60, "#fff", 12, INK, 3) + T(166, 95, f"Bước {n}: {s}", 30, 800))
    if chip:
        out += pill(138 + w + 30 + len(chip) * 9, 84, chip, "#fff", BLUE, 24)
    return out


def check(cx, cy, r=34):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GREEN}"/>'
            f'<path d="M{cx - r * .45} {cy + r * .03} l{r * .3} {r * .3} l{r * .55} {r * -.62}" fill="none" '
            f'stroke="#fff" stroke-width="{r * .22}" stroke-linecap="round" stroke-linejoin="round"/>')


def cross(cx, cy, r=34):
    d = r * .32
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{RED}"/>'
            f'<path d="M{cx - d} {cy - d} L{cx + d} {cy + d} M{cx + d} {cy - d} L{cx - d} {cy + d}" '
            f'stroke="#fff" stroke-width="{r * .22}" stroke-linecap="round"/>')


def stamp(cx, cy, s, col=GREEN, rot=-8):
    w = len(s) * 24 + 60
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            + rect(cx - w / 2, cy - 44, w, 88, "none", 12, col, 7)
            + T(cx, cy + 15, s, 42, 900, col, "middle", 'letter-spacing="3"') + '</g>')


def arrow(x1, y1, x2, y2, col=BLUE, sw=6, dash=False):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 22 * math.cos(a), y2 - 22 * math.sin(a)
    l, r = a + 2.6, a - 2.6
    da = ' stroke-dasharray="14 12"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{hx}" y2="{hy}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"{da}/>'
            f'<polygon points="{x2},{y2} {x2 + 24 * math.cos(l)},{y2 + 24 * math.sin(l)} '
            f'{x2 + 24 * math.cos(r)},{y2 + 24 * math.sin(r)}" fill="{col}"/>')


def person(fid, role, x, y, s=1.6, **kw):
    return f'<g transform="translate({x},{y})">{stick(fid, role, s, **kw)}</g>'


def floor(y=800):
    return f'<rect x="0" y="{y}" width="1920" height="{1080 - y}" fill="{C["floor"]}"/>'


def paper(x, y, w, h, title, lines, col=BLUE, faded=False):
    op = ' opacity="0.55"' if faded else ""
    out = (f'<g{op}>' + rect(x + 10, y + 12, w, h, "#000", 14, extra='opacity="0.08"')
           + rect(x, y, w, h, "#fff", 14, INK, 3) + rect(x, y, w, 70, col, 14)
           + rect(x, y + 40, w, 30, col, 0) + T(x + 28, y + 48, title, 30, 800, "#fff"))
    yy = y + 118
    for ln in lines:
        if isinstance(ln, tuple):
            s, c, wt = ln
        else:
            s, c, wt = ln, INK, 600
        out += T(x + 28, yy, s, 27, wt, c)
        yy += 46
    return out + "</g>"


def terminal(x, y, w, h, lines):
    out = (rect(x, y, w, h, "#1B2430", 18) + rect(x, y, w, 56, "#2B3646", 18) + rect(x, y + 30, w, 26, "#2B3646", 0)
           + "".join(f'<circle cx="{x + 34 + i * 30}" cy="{y + 28}" r="9" fill="{c}"/>'
                     for i, c in enumerate(["#E5584F", "#F2B233", "#2FAE5F"]))
           + T(x + w / 2, y + 38, "Claude Code", 24, 700, "#AEBBCC", "middle"))
    yy = y + 112
    for s, c in lines:
        out += T(x + 36, yy, s, 30, 600, c)
        yy += 50
    out += rect(x + 36, yy - 34, 18, 38, "#7FD3FF", 2)
    return out


def subtitle(s):
    # dải phụ đề giống các video: nền trắng, chữ 700, đáy khung
    words = s.split()
    lines = [s]
    if len(s) > 58:  # chia 2 dòng cân nhau, không để một chữ lẻ ở dòng dưới
        best = min(range(1, len(words)), key=lambda k: abs(len(" ".join(words[:k])) - len(" ".join(words[k:]))))
        lines = [" ".join(words[:best]), " ".join(words[best:])]
    h = 34 + 62 * len(lines)
    w = max(len(ln) for ln in lines) * 24 + 90
    y0 = 1040 - h
    out = rect(960 - w / 2, y0, w, h, "#FFFFFF", 14, extra='opacity="0.94"')
    for i, ln in enumerate(lines):
        out += T(960, y0 + 64 + i * 62, ln, 44, 700, INK, "middle")
    return out


def frame(body, sub=None, bg=C["ground"]):
    s = subtitle(sub) if sub else ""
    return (f'<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg" role="img">'
            f'<rect width="1920" height="1080" fill="{bg}"/>{body}{s}</svg>')


# ------------------------------------------------------------------ screens
S = []


def screen_def(sid, part, time, title, svg, visual, subs, note=None):
    S.append(dict(id=sid, part=part, time=time, title=title, svg=svg, visual=visual, subs=subs, note=note))


# S01 — Mở đầu
b = floor(830)
b += pill(250, 210, "HÀNH TRÌNH", ORANGE, "#fff", 26)
b += T(120, 340, "Từ một prompt", 92, 900) + T(120, 450, "đến một kỹ năng", 92, 900)
b += T(120, 560, "làm video", 92, 900, BLUE)
b += pill(330, 660, "2 ngày · 27 phiên bản", GREEN, "#fff", 30)
b += person("s01i", "instructor", 860, 830, 2.0, pose=WAVE)
for i, (k, lab) in enumerate([("kho", "Kho khô · 5:09"), ("tc", "Hàng TC · 2:12"),
                              ("cxad", "CXAD · 5:20"), ("deck-01", "Deck · 17 slide")]):
    x, y = 1080 + (i % 2) * 400, 150 + (i // 2) * 320
    b += screen(k, x, y, 350, lab)
screen_def("S01", "Mở đầu", "0:00–0:12", "Tiêu đề + 4 sản phẩm",
           frame(b, "Đây là ba video training và một bộ slide, làm trong hai ngày."),
           ["Tiêu đề hiện từng dòng, badge cam “HÀNH TRÌNH” bật nhẹ.",
            "Giảng viên bước vào từ giữa và vẫy tay.",
            "4 ảnh thật (3 video + trang bìa deck) bay vào lưới 2×2 bên phải, mỗi ảnh có nhãn thời lượng.",
            "Chip xanh “2 ngày · 27 phiên bản” bật ra cuối cùng."],
           ["Đây là ba video training và một bộ slide, làm trong hai ngày.",
            "Video này kể lại tôi đã làm thế nào, để bạn cũng làm được."])

# S02 — Thẻ chương
b = rect(0, 0, 760, 1080, BLUE, 0)
b += T(120, 470, "PHẦN 1", 34, 700, "#BFD8F5", extra='letter-spacing="4"')
b += T(120, 570, "Bắt đầu từ", 86, 900, "#fff") + T(120, 670, "một prompt", 86, 900, "#fff")
for i, (n, s) in enumerate([("1", "Bắt đầu từ một prompt"), ("2", "Xem nháp, góp ý thành luật"),
                            ("3", "Video sau kế thừa video trước"), ("4", "Đóng gói thành kỹ năng")]):
    y = 330 + i * 130
    on = i == 0
    b += f'<circle cx="930" cy="{y}" r="38" fill="{BLUE if on else "#fff"}" stroke="{BLUE}" stroke-width="4"/>'
    b += T(930, y + 13, n, 36, 900, "#fff" if on else BLUE, "middle")
    b += T(1000, y + 14, s, 42, 800 if on else 600, INK if on else MUTED)
screen_def("S02", "Thẻ chương", "0:12–0:15", "Thẻ chương (mẫu cho Phần 1–4)",
           frame(b),
           ["Cùng kiểu thẻ chương của các video kho: nửa trái xanh, tên phần to màu trắng.",
            "Bên phải là mục lục 4 phần, phần đang tới sáng lên. Tiếng whoosh khi chuyển phần.",
            "Dùng lại đúng khung này trước Phần 2, 3, 4 (mỗi lần khoảng 2–3 giây)."],
           [], "Không có phụ đề trên thẻ chương.")

# S03 — Bước 1: cài skill
b = floor(830) + badge(1, "Cài bộ skill dựng video")
b += person("s03i", "instructor", 300, 830, 1.9, pose=POINT_R)
bx, by = 760, 230
skills = ["hyperframes", "hyperframes-cli", "hyperframes-registry", "media-use", "figma",
          "slideshow", "style-sampling", "reverse-any-video", "remotion-to-hyperframes"]
b += rect(bx, by + 120, 900, 380, ORANGE, 24, INK, 4)
b += rect(bx + 330, by + 70, 240, 70, "none", 30, INK, 10)
b += rect(bx, by + 120, 900, 70, "#D9781A", 24)
for i, s in enumerate(skills):
    x, y = bx + 40 + (i % 3) * 280, by + 220 + (i // 3) * 92
    b += rect(x, y, 260, 72, "#fff", 12, INK, 3) + T(x + 130, y + 45, s, 17 if len(s) > 20 else 20 if len(s) > 14 else 24, 700, BLUE, "middle")
b += pill(bx + 450, by + 570, "9 skill HyperFrames · heygen-com/hyperframes", INK, "#fff", 28)
screen_def("S03", "Phần 1 – Bắt đầu từ một prompt", "0:15–0:21", "Bước 1: Cài 9 skill",
           frame(b, "Đầu tiên, tôi cài cho Claude bộ 9 skill dựng video HyperFrames."),
           ["Hộp đồ nghề màu cam mở ra; 9 thẻ tên skill lần lượt rơi vào, xếp 3×3.",
            "Giảng viên đứng trái, chỉ tay vào hộp.",
            "Dải dưới: nguồn cài đặt “heygen-com/hyperframes”."],
           ["Đầu tiên, tôi cài cho Claude bộ 9 skill dựng video HyperFrames."],
           "Câu phụ đề này là câu MỚI, chưa có trong prompt v1 (Bước 1 trong prompt chưa có lời).")

# S18 — Bản chất HyperFrames (màn mới, sau Bước 1)
b = floor(830)
b += pill(250, 84, "HYPERFRAMES LÀ GÌ?", ORANGE, "#fff", 28)
b += T(120, 190, "Video = một trang web chạy theo thời gian", 56, 900)
ex, ey, ew, eh = 120, 250, 760, 520
b += rect(ex, ey, ew, eh, "#1B2430", 18) + rect(ex, ey, ew, 52, "#2B3646", 18) + rect(ex, ey + 30, ew, 22, "#2B3646", 0)
b += T(ex + 30, ey + 36, "compositions/kho.html", 22, 700, "#AEBBCC")
MONO = 'font-family="ui-monospace, Menlo, monospace"'
code = [("<div class=\"clip\" data-start=\"0.3\"", "#7FD3FF"), ("     data-duration=\"1.5\">", "#7FD3FF"),
        ("  Xin chào các bạn.", "#FFFFFF"), ("</div>", "#7FD3FF"), ("<svg id=\"picker\">…</svg>", "#7FD3FF"), ("", "#fff"),
        ("tl.to(\"#picker\", {", "#F2B233"), ("  x: 600, duration: 2", "#F2B233"), ("});", "#F2B233")]
for n, (ln, c) in enumerate(code):
    b += T(ex + 34, ey + 104 + n * 44, ln, 26, 600, c, fam=MONOF)
tags = [(ey + 130, "HTML = cảnh, chữ, nhân vật", BLUE), (ey + 280, "CSS = màu, font, bố cục", GREEN),
        (ey + 410, "JavaScript (GSAP) = chuyển động", ORANGE)]
for yy, s_, col in tags:
    b += rect(ex + ew + 20, yy - 30, 14, 60, col, 4)
b += T(ex + ew + 50, ey + 140, "HTML", 30, 900, BLUE) + T(ex + ew + 50, ey + 176, "cảnh, chữ, nhân vật", 22, 600, MUTED)
b += T(ex + ew + 50, ey + 290, "CSS", 30, 900, GREEN) + T(ex + ew + 50, ey + 326, "màu, font, bố cục", 22, 600, MUTED)
b += T(ex + ew + 50, ey + 420, "GSAP", 30, 900, ORANGE) + T(ex + ew + 50, ey + 456, "chuyển động", 22, 600, MUTED)
b += arrow(1150, 510, 1250, 510, ORANGE, 8)
b += T(1200, 470, "trình duyệt", 22, 700, MUTED, "middle")
# dải phim: 4 khung, người que dịch dần sang phải
for n in range(3):
    gy = 250 + n * 190
    b += rect(1280, gy, 330, 172, "#2B3646", 10)
    b += rect(1296, gy + 14, 298, 144, C["ground"], 4) + rect(1296, gy + 120, 298, 38, C["floor"], 0)
    b += f'<g transform="translate({1340 + n * 95},{gy + 140}) scale(0.62)">{stick(f"s18p{n}", "picker", 1.0)}</g>'
    b += T(1625, gy + 95, f"khung {n * 15 + 1}", 22, 700, MUTED)
b += T(1445, 828, "30 khung / giây", 24, 800, INK, "middle")
b += arrow(1720, 510, 1790, 510, ORANGE, 8)
b += rect(1790, 455, 110, 110, BLUE, 18) + T(1845, 522, "MP4", 30, 900, "#fff", "middle")
screen_def("S18", "Phần 1 – Bắt đầu từ một prompt", "0:21–0:36", "Bản chất HyperFrames: cốt lõi là frontend",
           frame(b, "HyperFrames dựng video bằng chính HTML, giống như làm một trang web."),
           ["Màn mới, đặt ngay sau Bước 1. Không có badge “Bước n” vì đây là phần giải thích công cụ.",
            "Trái: cửa sổ code gõ ra từng dòng. Đoạn code lấy từ project thật: một khung phụ đề có "
            "data-start / data-duration, một nhân vật SVG, và một dòng GSAP cho nhân vật đi sang phải.",
            "Ba vạch màu HTML / CSS / GSAP sáng lần lượt, khớp với từng câu phụ đề.",
            "Phải: trình duyệt “chụp” từng khung. 3 khung phim cho thấy picker dịch dần sang phải, "
            "rồi gộp thành ô MP4.",
            "Câu cuối: chữ “frontend” đổi sang màu cam."],
           ["HyperFrames dựng video bằng chính HTML, giống như làm một trang web.",
            "Cảnh là HTML và CSS, chuyển động viết bằng JavaScript.",
            "Trình duyệt chạy trang đó và chụp từng khung, 30 khung mỗi giây, rồi ghép thành MP4.",
            "Vì vậy cốt lõi là frontend: dựng được trang web thì dựng được video."],
           "Màn mới theo yêu cầu. Màn này khoảng 15 giây, cả video thành khoảng 3:05.")

# S04 — Bước 2: Prompt gốc
b = floor(830) + badge(2, "Viết prompt gốc")
b += paper(200, 190, 640, 560, "[A] Phong cách chung",
           ["16:9 · 1920×1080", "Người que, áo màu theo vai", ("Xanh · Cam · Xanh lá", BLUE, 700),
            "Badge “Bước n”, PDA phóng to", "Cuối tập: thẻ “Ghi nhớ”", "Mỗi cảnh một ý"])
b += T(905, 480, "+", 110, 900, ORANGE, "middle")
b += paper(970, 190, 640, 560, "[B] Kịch bản từng tập",
           [("Tập 1 – Tổng quan kho · 70s", INK, 800), "Cảnh 1 (0–8s): tiêu đề,", "giảng viên vẫy tay",
            ("VO: “Xin chào các bạn…”", MUTED, 600), "Cảnh 2 (8–25s): bay qua kho", ("… Tập 2 → Tập 5", MUTED, 600)],
           ORANGE)
b += person("s04i", "instructor", 1760, 830, 1.6, pose=TYPE)
screen_def("S04", "Phần 1 – Bắt đầu từ một prompt", "0:36–0:43", "Bước 2: Prompt gốc [A] + [B]",
           frame(b, "Tôi bắt đầu bằng một prompt: phong cách chung và kịch bản từng tập."),
           ["Hai tờ giấy trượt vào từ hai bên: [A] Phong cách chung (xanh) và [B] Kịch bản từng tập (cam).",
            "Dấu “+” cam bật ra giữa hai tờ.",
            "Các dòng trong tờ được trích đúng từ file Prompt_Video_Training_Kho_Kho.md."],
           ["Tôi bắt đầu bằng một prompt: phong cách chung và kịch bản từng tập."])

# S05 — Bước 3: Outline
b = floor(830) + badge(3, "Claude lập outline để duyệt")
b += terminal(160, 180, 1060, 600, [
    ("> Viết OUTLINE.md", "#7FD3FF"), ("## 1. Kế hoạch xử lý", "#FFFFFF"), ("## 2. Thông số chung", "#FFFFFF"),
    ("   Màu  #1F5FBF  #F28C1E  #22A55A", "#F2B233"), ("   Font Be Vietnam Pro · 30 fps", "#F2B233"),
    ("## 3. Outline Tập 1 (5 cảnh)", "#FFFFFF"), ("## 4. Câu hỏi cần chốt", "#FFFFFF")])
b += person("s05i", "instructor", 1450, 830, 1.9, pose=THUMB)
b += stamp(1600, 330, "ĐÃ DUYỆT")
screen_def("S05", "Phần 1 – Bắt đầu từ một prompt", "0:43–0:50", "Bước 3: Outline trước, dựng sau",
           frame(b, "Claude không dựng ngay, mà lập outline để tôi duyệt trước."),
           ["“Claude” là cửa sổ terminal (không vẽ thành người). Chữ được gõ ra từng dòng, con trỏ xanh nhấp nháy.",
            "Nội dung gõ ra là các mục thật của OUTLINE.md.",
            "Giảng viên giơ ngón cái, dấu “ĐÃ DUYỆT” xanh đóng xuống (tiếng chime)."],
           ["Claude không dựng ngay, mà lập outline để tôi duyệt trước."])

# S07 — Bước 5: Tập 1 nháp
b = floor(830) + badge(4, "Xem Tập 1 bản nháp")
b += screen("t1draft", 200, 200, 1000, "Tập 1 – bản nháp · 76 giây")
b += person("s07i", "instructor", 1500, 830, 1.9, pose=POINT_L)
for i, s in enumerate(["Góp ý 1", "Góp ý 2", "Góp ý 3", "Góp ý 4"]):
    x, y = 1330 + (i % 2) * 230, 200 + (i // 2) * 130
    b += f'<g transform="rotate({-4 + i * 3} {x + 100} {y + 50})">' + rect(x, y, 200, 100, "#FFE9A8", 6, INK, 2) + T(x + 100, y + 62, s, 30, 800, INK, "middle") + "</g>"
screen_def("S07", "Phần 2 – Xem nháp, góp ý thành luật", "0:50–1:00", "Bước 4: Tập 1 bản nháp",
           frame(b, "Xem Tập 1 xong, tôi góp ý bốn điểm."),
           ["Mở đầu bằng thẻ chương “Phần 2” (khung S02).",
            "Khung màn hình phát vài giây đoạn thật của tap-1-draft.mp4.",
            "Giảng viên chỉ vào màn hình; 4 tờ giấy nhớ vàng “Góp ý 1–4” dán lên lần lượt."],
           ["Xem Tập 1 xong, tôi góp ý bốn điểm."])

# S08 — Bước 6: 4 luật
b = floor(830) + badge(5, "Góp ý thành luật")
rules = [("1", "5 tập → 1 video", "Có thẻ chương giữa các phần"),
         ("2", "Nhịp đọc 1.3×", "(0.5s + 0.3s × số chữ) ÷ 1.3"),
         ("3", "Âm thanh thưa", "Cách nhau ít nhất 4 giây"),
         ("4", "Nhân vật v2", "Có khớp, áo phản quang")]
for i, (n, t1, t2) in enumerate(rules):
    x = 120 + i * 430
    b += rect(x, 210, 390, 560, "#fff", 22, INK, 3)
    b += rect(x, 210, 390, 84, BLUE, 22) + rect(x, 250, 390, 44, BLUE, 0)
    b += T(x + 30, 266, f"LUẬT {n}", 32, 900, "#fff", extra='letter-spacing="2"')
    cx, cy = x + 195, 450
    if n == "1":
        for k in range(5):
            b += rect(cx - 150 + k * 22, cy - 80 + k * 10, 120, 70, "#E3E8EF", 8, MUTED, 2)
        b += arrow(cx - 10, cy + 10, cx + 50, cy + 10, ORANGE)
        b += rect(cx + 60, cy - 40, 110, 90, BLUE, 10, INK, 3)
    elif n == "2":
        b += T(cx, cy + 30, "1.3×", 120, 900, ORANGE, "middle")
    elif n == "3":
        b += (f'<path d="M{cx - 90} {cy - 30} h40 l50 -45 v150 l-50 -45 h-40 z" fill="{BLUE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
              + T(cx + 70, cy + 30, "≥4s", 64, 900, INK, "middle"))
    else:
        b += person(f"s08p{i}", "picker", cx, cy + 110, 1.25)
    b += T(cx, 640, t1, 38, 900, INK, "middle") + T(cx, 700, t2, 23, 600, MUTED, "middle")
screen_def("S08", "Phần 2 – Xem nháp, góp ý thành luật", "1:00–1:10", "Bước 5: 4 góp ý thành 4 luật",
           frame(b, "Mỗi góp ý được ghi thành luật, áp dụng cho mọi phần sau."),
           ["4 tờ giấy nhớ vàng ở màn trước bay vào và lật thành 4 thẻ “LUẬT” đầu xanh.",
            "Luật 2 hiện công thức nhịp đọc đúng như trong OUTLINE.md §5.",
            "Giữ 4 thẻ đứng yên đủ lâu để đọc."],
           ["Mỗi góp ý được ghi thành luật, áp dụng cho mọi phần sau."])

# S09 — Bước 7: model sheet
b = floor(830) + badge(6, "Duyệt bảng nhân vật")
b += screen("t1draft", 140, 250, 420, "v1 – người que đơn giản")
b += f'<line x1="140" y1="250" x2="560" y2="486" stroke="{RED}" stroke-width="10" stroke-linecap="round" opacity="0.85"/>'
b += arrow(600, 370, 700, 370, ORANGE, 8)
b += screen("ms2", 760, 170, 760, "Model sheet v2")
b += check(1500, 175, 38)
b += person("s09w", "picker", 1720, 700, 1.7, pose={"armR": (-30, 10)})
b += f'<g transform="rotate(7 1720 700)"></g>'
b += (f'<path d="M1640 470 q80 -50 160 0" fill="none" stroke="{ORANGE}" stroke-width="6" stroke-dasharray="10 10"/>'
      + T(1720, 760, "nghiêng – nhún", 28, 800, ORANGE, "middle"))
screen_def("S09", "Phần 2 – Xem nháp, góp ý thành luật", "1:10–1:20", "Bước 6: Nhân vật v2 + dáng đi",
           frame(b, "Nhân vật được vẽ lại, duyệt trên một bảng mẫu, rồi mới đưa vào video."),
           ["Trái: khung Tập 1 nháp (người que v1) bị gạch đỏ, trượt ra.",
            "Giữa: ảnh thật model-sheet-v2.png trượt vào, ✔ xanh “đã duyệt”.",
            "Phải: picker v2 đi theo kiểu nghiêng trái/phải + nhún nhẹ (lấy từ walk-demo.mp4)."],
           ["Nhân vật được vẽ lại, duyệt trên một bảng mẫu, rồi mới đưa vào video."])

# S10 — Bước 8: timeline
b = floor(830) + badge(7, "Duyệt 31 giây đầu, rồi làm đủ")
x0, x1, y = 160, 1760, 560
tot = 309
b += rect(x0, y - 30, x1 - x0, 60, "#E3E8EF", 30)
xs = x0 + (x1 - x0) * 31 / tot
b += rect(x0, y - 30, xs - x0, 60, GREEN, 30)
b += T(x0, y - 60, "0:31 – duyệt trước", 32, 800, GREEN) + check(x0 + 330, y - 72, 26)
parts = [(0, "Phần 1"), (60, "Phần 2"), (125, "Phần 3"), (185, "Phần 4"), (245, "Phần 5")]
for t, s in parts:
    xx = x0 + (x1 - x0) * t / tot
    b += f'<line x1="{xx}" y1="{y + 40}" x2="{xx}" y2="{y + 70}" stroke="{MUTED}" stroke-width="3"/>'
    b += T(xx + 8, y + 100, s, 26, 700, MUTED)
b += f'<rect x="{xs}" y="{y - 30}" width="{x1 - xs}" height="60" rx="30" fill="{BLUE}" opacity="0.85"/>'
b += T(x1, y + 100, "5:09", 34, 900, BLUE, "end")
b += screen("kho", 1240, 170, 420, "Bản đầy đủ · 1080p")
screen_def("S10", "Phần 2 – Xem nháp, góp ý thành luật", "1:20–1:30", "Bước 7: 0:31 → 5:09",
           frame(b, "Duyệt 31 giây đầu trước, rồi mới làm đủ 5 phút."),
           ["Thanh thời lượng: đoạn 0:31 tô xanh trước + ✔.",
            "Sau đó thanh xanh dương kéo dài tới 5:09, các mốc Phần 1–5 hiện dần.",
            "Góc phải: khung thật của video kho khô bản đầy đủ."],
           ["Duyệt 31 giây đầu trước, rồi mới làm đủ 5 phút."])

# S11 — Bước 9: Context TC
b = floor(830) + badge(8, "Video TC: chỉ viết phần khác")
px, py = 160, 230
b += rect(px, py, 900, 520, "#fff", 18, INK, 3) + rect(px, py, 900, 70, BLUE, 18) + rect(px, py + 40, 900, 30, BLUE, 0)
b += T(px + 30, py + 48, "Context TC – Khác gì video trước", 30, 800, "#fff")
rows = [("", "Hàng kho khô", "Hàng TC"), ("Nhận hàng", "Dán LPN", "Không LPN"),
        ("Sau nhận", "Cất lên kệ", "Khu TC"), ("Xuất", "Pick từ pick face", "Chia theo DO"),
        ("Tồn kho", "Có lưu kho", "Không lưu kho")]
for i, (a, c1, c2) in enumerate(rows):
    yy = py + 130 + i * 78
    wt = 800 if i == 0 else 600
    b += T(px + 30, yy, a, 28, 800, MUTED) + T(px + 260, yy, c1, 28, wt, INK) + T(px + 590, yy, c2, 28, wt if i else 800, ORANGE if i else INK)
    if i:
        b += f'<line x1="{px + 20}" y1="{yy - 50}" x2="{px + 880}" y2="{yy - 50}" stroke="#E3E8EF" stroke-width="2"/>'
for i, s in enumerate(["Nhịp 1.3×", "Âm thanh ≥ 4s", "Nhân vật v2"]):
    b += pill(1210 + i * 0 + 120, 250 + i * 80, s, GREEN, "#fff", 26)
    b += arrow(1140, 250 + i * 80, 1080, 260 + i * 40, GREEN, 4, True)
b += screen("tc", 1180, 520, 480, "36 giây đầu → 2:12")
screen_def("S11", "Phần 3 – Video sau kế thừa video trước", "1:30–1:48", "Bước 8: Context TC",
           frame(b, "Tôi chỉ viết phần khác so với video trước, mọi luật cũ tự áp dụng."),
           ["Mở đầu bằng thẻ chương “Phần 3”.",
            "Tờ “Context TC” với bảng so sánh 2 cột, lấy đúng từ source/Context_Video_TC.md.",
            "3 chip luật cũ (xanh lá) bay từ góc phải gắn vào tờ giấy.",
            "Góc dưới phải: khung thật của video TC, nhãn “36 giây đầu → 2:12”."],
           ["Video thứ hai không phải bắt đầu lại.",
            "Tôi chỉ viết phần khác so với video trước, mọi luật cũ tự áp dụng."])

# S12 — Bước 10: deck
b = floor(830) + badge(9, "Thêm một bộ slide")
for i, k in enumerate(["deck-05", "deck-04", "deck-03", "deck-02", "deck-01"]):
    ang = -24 + i * 12
    b += (f'<g transform="rotate({ang} 960 1050)">'
          + rect(720, 280, 480, 270, "#2B3646", 12) + img(k, 730, 290, 460, 250) + "</g>")
b += pill(960, 160, "17 slide · .pptx", INK, "#fff", 34)
screen_def("S12", "Phần 3 – Video sau kế thừa video trước", "1:48–2:00", "Bước 9: Deck 17 slide",
           frame(b, "Cùng nội dung đó, tôi tạo thêm một bộ slide 17 trang."),
           ["5 trang đầu thật của deck xòe ra như quạt từ một điểm dưới đáy.",
            "Nhãn “17 slide · .pptx” bật ra phía trên."],
           ["Cùng nội dung đó, tôi tạo thêm một bộ slide 17 trang."])

# S13 — Bước 11: PDF → prompt
b = floor(830) + badge(10, "CXAD: từ bản vẽ đến prompt")
b += rect(160, 200, 300, 380, "#fff", 12, INK, 3) + rect(160, 200, 300, 80, RED, 12) + rect(160, 240, 300, 40, RED, 0)
b += T(310, 258, "PDF", 44, 900, "#fff", "middle")
for k in range(4):
    b += rect(200, 320 + k * 60, 220 - (k % 2) * 60, 26, "#E3E8EF", 6)
b += T(310, 630, "Bản vẽ quy trình", 28, 800, INK, "middle")
b += arrow(490, 390, 580, 390, ORANGE, 8)
b += paper(610, 200, 420, 380, "Prompt v1 (nháp)", ["Đủ 5 quy trình", "Vai gộp chung"], MUTED, True)
b += arrow(1060, 390, 1150, 390, ORANGE, 8)
b += paper(1180, 200, 560, 380, "Prompt v2", ["Bỏ 01A", "Tách 8 vai theo việc", "Chip theo chú giải bản vẽ"], BLUE)
b += check(1720, 205, 36)
chips = [("WMS", "#fff", BLUE), ("PDA", "#fff", INK), ("Thủ công", ORANGE, "#fff"), ("Chứng từ", "#fff", INK)]
for i, (s, bg, fg) in enumerate(chips):
    cx = 260 + i * 260
    b += rect(cx - 110, 690, 220, 76, bg, 14, fg if bg == "#fff" else ORANGE, 3) + T(cx, 740, s, 32, 800, fg, "middle")
b += (f'<polygon points="1300,665 1420,728 1300,791 1180,728" fill="#fff" stroke="{BLUE}" stroke-width="4"/>'
      + T(1300, 740, "Điều kiện", 28, 800, BLUE, "middle"))
b += (rect(1480, 690, 280, 76, "#fff", 14, RED, 3) + T(1620, 740, "01A", 34, 900, RED, "middle")
      + f'<line x1="1500" y1="728" x2="1740" y2="728" stroke="{RED}" stroke-width="7"/>')
screen_def("S13", "Phần 4 – Đóng gói thành kỹ năng", "2:00–2:13", "Bước 10: PDF → Prompt v1 → v2",
           frame(b, "Video thứ ba bắt đầu từ bản vẽ quy trình."),
           ["Mở đầu bằng thẻ chương “Phần 4”.",
            "Dòng chảy trái → phải: PDF bản vẽ → Prompt v1 (xám, nháp) → Prompt v2 (xanh, ✔).",
            "Hàng dưới: 5 chip lấy từ chú giải bản vẽ (WMS, PDA, Thủ công, Chứng từ, ô thoi Điều kiện).",
            "Ô “01A” bị gạch đỏ, kèm nhãn nhỏ “Việc của quản lý – bỏ” khi xuất hiện."],
           ["Video thứ ba bắt đầu từ bản vẽ quy trình."])

# S14 — Bước 11: skill nhân vật, mỗi vai một hành động tại chỗ
from model_sheet import forklift as fl_front, forklift_back as fl_back, trolley as ms_trolley, carton_flat  # noqa: E402
b = floor(830) + badge(11, "Đóng gói nhân vật thành skill")
b += rect(110, 190, 1700, 640, "none", 30, BLUE, 6, 'stroke-dasharray="22 14"')
b += pill(960, 190, "Skill: nhan-vat-kho · model v3", BLUE, "#fff", 34)
SC, FY14 = 1.3, 690
CARTON = '<g transform="translate(0,23) rotate(-70)"><g transform="translate(-30,-22)">' + carton_flat(0, 0, 60, 44) + '</g></g>'
PEN = f'<line x1="0" y1="22" x2="10" y2="44" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
PAPER = ('<g transform="translate(4,22) rotate(-62)"><rect x="-4" y="-22" width="34" height="44" rx="3" fill="#fff" '
         f'stroke="{INK}" stroke-width="2.5"/><rect x="2" y="-14" width="22" height="3" fill="{MUTED}"/>'
         f'<rect x="2" y="-6" width="18" height="3" fill="{MUTED}"/><path d="M4 10 q6 -8 10 0 t10 0" fill="none" stroke="{BLUE}" stroke-width="2.5"/></g>')
LAPTOP = (f'<rect x="30" y="-64" width="90" height="10" rx="3" fill="#C9965A" stroke="{INK}" stroke-width="3"/>'
          f'<rect x="70" y="-54" width="10" height="54" fill="#A97A44" stroke="{INK}" stroke-width="2.5"/>'
          f'<path d="M44 -66 L96 -66 L108 -112 L56 -112 Z" fill="#2B3646" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
          f'<path d="M60 -106 L102 -106 L94 -74 L52 -74 Z" fill="#7FD3FF"/>')
cast = [
    (190, "receiver", "Nhận hàng", "bê thùng", dict(pose={"armL": (34, -104), "armR": (-34, 104)}, hand_r=CARTON), "", ""),
    (410, "forklift", "Xe nâng", "lái, nâng càng", None, fl_back(), fl_front()),
    (600, "planner", "Điều phối", "gõ máy tính", dict(pose={"armL": (-40, -35), "armR": (-50, -25)}), "", LAPTOP),
    (850, "manager", "Quản lý kho", "giao việc", dict(pose={**MANAGER_HOLD, **POINT_R}, hand_l=folder_svg()), "", ""),
    (1020, "picker", "Picker", "kéo trolley", dict(pose={"armR": (-88, 0)}), "", ms_trolley()),
    (1370, "checker", "Checker", "scan PDA", dict(pose={"armR": (-60, -10)}, hand_r=pda_svg("s14chk", laser=True, reach=70)), "", ""),
    (1530, "transport", "Vận tải", "ký giấy giao", dict(pose={"armL": (-8, -118), "armR": (-40, -95)}, hand_l=PAPER, hand_r=PEN), "", ""),
    (1690, "instructor", "Giảng viên", "vẫy tay", dict(pose=WAVE), "", ""),
]
for i, (x, r, lab, act, kw, back, front) in enumerate(cast):
    if r == "manager":
        b += rect(x - 95, 270, 190, 520, "#FFF3E2", 20, ORANGE, 4) + pill(x, 300, "MỚI", ORANGE, "#fff", 24)
    if r == "forklift":
        load = '<g transform="translate(60,-62)">' + carton_flat(0, 0, 56, 42) + '</g>'
        drv = f'<g transform="translate(-22,-14)">{stick("s14fl", "forklift", 1.0, pose={"armR": (-70, -20), "armL": (10, -40)})}</g>'
        fig = back + drv + front + load
    else:
        fig = stick(f"s14r{i}", r, 1.0, **kw) + front
    b += f'<g transform="translate({x},{FY14}) scale({SC})">{fig}</g>'
    b += T(x, FY14 + 62, lab, 26, 800, INK, "middle") + T(x, FY14 + 98, act, 22, 600, MUTED, "middle")
screen_def("S14", "Phần 4 – Đóng gói thành kỹ năng", "2:13–2:28", "Bước 11: Skill nhan-vat-kho",
           frame(b, "Cần thêm vai quản lý kho, tôi đóng gói cả bộ nhân vật thành một skill riêng."),
           ["8 vai đứng thành hàng, mỗi vai làm một hành động khác nhau ngay tại chỗ (lặp nhẹ, không đi lại):",
            "Nhận hàng bê thùng · Xe nâng nâng càng có thùng · Điều phối gõ máy tính · Quản lý kho cầm hồ sơ và chỉ tay · "
            "Picker kéo trolley · Checker scan PDA (tia laser đỏ) · Vận tải ký giấy giao · Giảng viên vẫy tay.",
            "“Quản lý kho” bước vào chỗ trống sau cùng, nhãn cam “MỚI”.",
            "Khung nét đứt xanh vẽ quanh cả hàng, rồi nhãn “Skill: nhan-vat-kho · model v3” đóng lên."],
           ["Cần thêm vai quản lý kho, tôi đóng gói cả bộ nhân vật thành một skill riêng.",
            "Từ nay, mọi video kho mới đều dùng lại bộ này, không vẽ lại."])

# S15 — Bước 13: v1→v2→v3
b = floor(830) + badge(12, "Sửa theo phiên bản")
for row, (ka, kb, la, lb, cap) in enumerate([("cx_v1", "cx_v2", "v1", "v2", "Phụ đề quy đổi bằng số"),
                                              ("cx_v2b", "cx_v3", "v2", "v3", "Ô điều kiện khớp mũi tên")]):
    y = 175 + row * 330
    b += screen(ka, 300, y, 370, la) + arrow(700, y + 104, 790, y + 104, ORANGE, 8) + screen(kb, 820, y, 370, lb)
    b += T(1260, y + 95, cap, 40, 900, BLUE) + T(1260, y + 145, "v" + str(row + 1) + " → v" + str(row + 2), 30, 700, MUTED)
screen_def("S15", "Phần 4 – Đóng gói thành kỹ năng", "2:28–2:40", "Bước 12: CXAD v1 → v2 → v3",
           frame(b, "Mỗi lần sửa là một phiên bản mới, luôn quay lại được."),
           ["Hai cặp trước/sau, ảnh thật từ 3 bản render CXAD:",
            "v1 → v2: phụ đề đổi từ chữ (“năm mươi lăm pcs”) sang số (“55 pcs”).",
            "v2 → v3: ô thoi “Khu hàng đông?” dời về đúng giữa hai mũi tên Có / Không.",
            "Khi chiếu, phóng to vùng thay đổi trong từng ảnh để người xem thấy rõ."],
           ["Mỗi lần sửa là một phiên bản mới, luôn quay lại được."],
           "Ảnh trong storyboard nhỏ; bản dựng thật sẽ phóng to vùng thay đổi.")

# S16 — Công thức
b = floor(830)
b += T(960, 150, "Công thức", 72, 900, INK, "middle")
steps = ["Nguồn", "Prompt / Context", "Outline duyệt", "Chốt luật", "Bảng nhân vật",
         "30 giây mẫu", "Làm đủ", "Render", "Sửa v2, v3", "Đóng gói"]
for i, s in enumerate(steps):
    row, col = divmod(i, 5)
    c = col if row == 0 else 4 - col
    x, y = 140 + c * 340, 260 + row * 260
    on = i < 6
    b += rect(x, y, 290, 140, BLUE if on else "#fff", 18, BLUE, 4)
    b += T(x + 145, y + 52, f"{i + 1:02d}", 28, 900, "#BFD8F5" if on else MUTED, "middle")
    b += T(x + 145, y + 100, s, 30, 800, "#fff" if on else INK, "middle")
    if i < 9:
        if row == 0 and col < 4:
            b += arrow(x + 296, y + 70, x + 334, y + 70, ORANGE, 6)
        elif row == 0 and col == 4:
            b += arrow(x + 145, y + 146, x + 145, y + 254, ORANGE, 6)
        else:
            b += arrow(x - 6, y + 70, x - 44, y + 70, ORANGE, 6)
screen_def("S16", "Tổng kết", "2:40–2:50", "Công thức 10 bước",
           frame(b, "Đó là công thức của tôi."),
           ["10 ô chạy như băng chuyền hình chữ S (5 trên, 5 dưới), sáng xanh lần lượt từ 01 đến 10.",
            "Storyboard đang chụp lúc ô 06 vừa sáng.",
            "Đánh số ở đây là thật vì đây là thứ tự làm."],
           ["Đó là công thức của tôi."])

# S17 — Ghi nhớ
b = floor(830)
b += rect(220, 200, 1000, 560, "#fff", 22, INK, 3)
b += T(280, 300, "Ghi nhớ", 64, 900) + rect(280, 325, 120, 8, ORANGE, 4)
for i, s in enumerate(["Duyệt sớm bằng thứ nhỏ", "Góp ý nào cũng thành luật ghi lại",
                       "Cái gì dùng lại thì đóng gói thành skill"]):
    yy = 440 + i * 105
    b += T(290, yy, s, 40, 700) + check(1150, yy - 14, 28)
b += person("s17i", "instructor", 1530, 830, 2.1, pose=THUMB)
screen_def("S17", "Tổng kết", "2:50–3:05", "Thẻ Ghi nhớ + kết",
           frame(b, "Duyệt sớm, ghi lại luật, và đóng gói những gì dùng lại."),
           ["Thẻ “Ghi nhớ” giống cuối mỗi phần của video kho; 3 ý hiện lần lượt, mỗi ý có ✔.",
            "Giảng viên giơ ngón cái. Giữ khung cuối 2 giây."],
           ["Đó là công thức của tôi.", "Duyệt sớm, ghi lại luật, và đóng gói những gì dùng lại.",
            "Bạn hãy thử với quy trình của mình."])

# ------------------------------------------------------------------ page
with open(os.path.join(os.path.dirname(__file__), "storyboard_page.html"), encoding="utf-8") as f:
    page = f.read()
cards = []
for idx, s in enumerate(S, 1):
    subs = "".join(f"<li>{esc(x)}</li>" for x in s["subs"]) or '<li class="none">Không có phụ đề</li>'
    vis = "".join(f"<li>{esc(x)}</li>" for x in s["visual"])
    note = f'<p class="note">{esc(s["note"])}</p>' if s["note"] else ""
    cards.append(f'''<article class="card" id="{s["id"]}" data-id="{s["id"]}">
<header class="card-head"><span class="sid">{idx:02d}</span><div><p class="eyebrow">{esc(s["part"])} · {s["time"]}</p>
<h2>{esc(s["title"])}</h2></div><span class="state" data-state>Chưa duyệt</span></header>
<div class="card-body"><div class="frame">{s["svg"]}</div>
<div class="side"><h3>Hình &amp; chuyển động</h3><ul>{vis}</ul><h3>Phụ đề</h3><ol class="subs">{subs}</ol>{note}
<div class="review"><div class="btns"><button type="button" class="ok" data-act="ok">Duyệt</button>
<button type="button" class="fix" data-act="fix">Cần sửa</button></div>
<label for="n-{s["id"]}">Ghi chú cho màn {idx:02d}</label>
<textarea id="n-{s["id"]}" rows="3" placeholder="Muốn đổi gì ở màn này?"></textarea>
<p class="saved" aria-live="polite"></p></div></div></div></article>''')
page = page.replace("{{CARDS}}", "\n".join(cards)).replace("{{COUNT}}", str(len(S)))
page = page.replace("{{IDS}}", json.dumps([s["id"] for s in S]))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print("wrote", OUT, len(page) // 1024, "KB,", len(S), "screens")
