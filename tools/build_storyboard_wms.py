"""Storyboard (khung duyệt) cho video "Quy trình kho cơ bản với WMS".

Nguồn: source/Prompt_Video_Quy_trinh_co_ban_WMS.md (v1 nháp) — bám bộ To-Be chuẩn của vault:
02C Nhập hàng mới - Barcode mã hàng (bước 1–7) và 04C Xuất kho theo đơn - Barcode (bước 1–6).
Mỗi màn = 1 khung 1920×1080 vẽ bằng SVG (màu, font, nhân vật của skill nhan-vat-kho),
kèm ghi chú hình/chuyển động, phụ đề và ô duyệt. Không cần ảnh ngoài.

Chạy:  python3 tools/build_storyboard_wms.py design/storyboard-wms-co-ban.html
"""
import html
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from kit import C, stick, pda_svg  # noqa: E402
from model_sheet import carton_flat, desk as ms_desk, truck as ms_truck, trolley as ms_trolley  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "design/storyboard-wms-co-ban.html"

F = "'Be Vietnam Pro', system-ui, sans-serif"
INK, MUTED, BLUE, ORANGE, GREEN, RED = C["ink"], C["muted"], C["blue"], C["orange"], C["green"], C["red"]
PURPLE = "#8B5CF6"
WAVE = {"armR": (-140, -25)}
POINT_R = {"armR": (-95, -5)}
POINT_L = {"armL": (95, 5)}
RAISE = {"armR": (-70, -100)}
TYPE = {"armL": (22, -70), "armR": (-22, 70)}
SCAN = {"armR": (-60, -10)}
CARRY = {"armL": (34, -104), "armR": (-34, 104)}
PUSH = {"armR": (-88, 0)}
SIGN = {"armL": (-8, -118), "armR": (-40, -95)}

CARTON = '<g transform="translate(0,23) rotate(-70)"><g transform="translate(-30,-22)">' + carton_flat(0, 0, 60, 44) + '</g></g>'
PEN = f'<line x1="0" y1="22" x2="10" y2="44" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
PAPER = ('<g transform="translate(4,22) rotate(-62)"><rect x="-4" y="-22" width="34" height="44" rx="3" fill="#fff" '
         f'stroke="{INK}" stroke-width="2.5"/><rect x="2" y="-14" width="22" height="3" fill="{MUTED}"/>'
         f'<rect x="2" y="-6" width="18" height="3" fill="{MUTED}"/><path d="M4 10 q6 -8 10 0 t10 0" fill="none" stroke="{BLUE}" stroke-width="2.5"/></g>')


# ------------------------------------------------------------------ primitives
def esc(s):
    return html.escape(s, quote=True)


def T(x, y, s, size=40, w=700, fill=INK, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" '
            f'fill="{fill}" text-anchor="{anchor}" xml:space="preserve" {extra}>{esc(s)}</text>')


def rect(x, y, w, h, fill="#fff", r=16, stroke=None, sw=3, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st} {extra}/>'


def tw(s, size):
    return len(s) * size * (0.68 if s.isupper() else 0.56)


def pill(cx, cy, s, bg=INK, fg="#fff", size=26, pad=24):
    w = tw(s, size) + pad * 2
    return (rect(cx - w / 2, cy - size * 0.95, w, size * 1.9, bg, size * 0.95) +
            T(cx, cy + size * 0.36, s, size, 700, fg, "middle"))


CHIP = {"tay": ("THỦ CÔNG", ORANGE), "wms": ("WMS", BLUE), "pda": ("QUÉT PDA", PURPLE), "doc": ("CHỨNG TỪ", MUTED)}


def chip(x, cy, kind, size=24):
    s, col = CHIP[kind]
    w = tw(s, size) + 44
    return rect(x, cy - 22, w, 44, "#fff", 22, col, 3) + T(x + w / 2, cy + 9, s, size, 800, col, "middle"), w


def badge(n, s, chips=()):
    w = tw(f"Bước {n}: {s}", 30) + 60
    out = (f'<circle cx="92" cy="84" r="30" fill="{ORANGE}" stroke="{INK}" stroke-width="3"/>'
           + T(92, 95, str(n).split("–")[0], 30, 900, INK, "middle")
           + rect(138, 54, w, 60, "#fff", 12, INK, 3) + T(166, 95, f"Bước {n}: {s}", 30, 800))
    x = 138 + w + 24
    for k in chips:
        c, cw = chip(x, 84, k)
        out += c
        x += cw + 14
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


def arrow(x1, y1, x2, y2, col=BLUE, sw=6, dash=False):
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 22 * math.cos(a), y2 - 22 * math.sin(a)
    l, r = a + 2.6, a - 2.6
    da = ' stroke-dasharray="14 12"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{hx}" y2="{hy}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"{da}/>'
            f'<polygon points="{x2},{y2} {x2 + 24 * math.cos(l)},{y2 + 24 * math.sin(l)} '
            f'{x2 + 24 * math.cos(r)},{y2 + 24 * math.sin(r)}" fill="{col}"/>')


def person(fid, role, x, y=830, s=1.8, tag=None, tag_col=INK, **kw):
    out = f'<g transform="translate({x},{y})">{stick(fid, role, s, **kw)}</g>'
    if tag:
        out += pill(x, y - 214 * s + 40, tag, tag_col, "#fff", 24)
    return out


def prop(svg, x, y=830, s=1.8, flip=False):
    fl = f" scale({-s},{s})" if flip else f" scale({s})"
    return f'<g transform="translate({x},{y}){fl}">{svg}</g>'


def floor(y=830):
    return f'<rect x="0" y="{y}" width="1920" height="{1080 - y}" fill="{C["floor"]}"/>'


def subtitle(s):
    words = s.split()
    lines = [s]
    if len(s) > 58:
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


# ------------------------------------------------------------------ warehouse props
def wms_win(x, y, w, title, headers, rows, cols, hl=None, status=None):
    """Cửa sổ WMS: thanh tiêu đề xanh + bảng. cols = độ rộng cột (tổng = w - 40)."""
    h = 150 + 64 * len(rows) + (70 if status else 0)
    out = (rect(x + 8, y + 10, w, h, "#000", 18, extra='opacity="0.08"') + rect(x, y, w, h, "#fff", 18, INK, 3)
           + rect(x, y, w, 64, BLUE, 18) + rect(x, y + 40, w, 24, BLUE, 0)
           + rect(x + 20, y + 14, 92, 36, "#fff", 8) + T(x + 66, y + 41, "WMS", 24, 900, BLUE, "middle")
           + T(x + 130, y + 43, title, 28, 800, "#fff"))
    yy, xx = y + 112, x + 20
    for hd, cw in zip(headers, cols):
        out += T(xx + 10, yy, hd, 22, 800, MUTED)
        xx += cw
    out += f'<line x1="{x + 20}" y1="{yy + 16}" x2="{x + w - 20}" y2="{yy + 16}" stroke="{C["floor_line"]}" stroke-width="3"/>'
    for i, row in enumerate(rows):
        ry = yy + 30 + i * 64
        if hl is not None and i in (hl if isinstance(hl, (list, tuple)) else [hl]):
            out += rect(x + 14, ry, w - 28, 56, "#FFF1DF", 10, ORANGE, 2)
        xx = x + 20
        for cell, cw in zip(row, cols):
            col = GREEN if cell.endswith("✔") else RED if cell.endswith("✖") else INK
            out += T(xx + 10, ry + 38, cell, 26, 700, col)
            xx += cw
    if status:
        sy = yy + 30 + len(rows) * 64 + 14
        out += pill(x + 30 + tw(status, 24) / 2 + 24, sy + 22, status, GREEN, "#fff", 24)
    return out


def pda_big(x, y, title, fields, button=None, w=430):
    """PDA phóng to: fields = [(nhãn, giá trị, trạng thái 'ok'|'err'|'hl'|None)]."""
    h = 200 + 104 * len(fields) + (90 if button else 0)
    out = (rect(x + 10, y + 12, w, h, "#000", 40, extra='opacity="0.10"') + rect(x, y, w, h, "#2B3646", 40, INK, 4)
           + rect(x + 24, y + 50, w - 48, h - 100, "#F4F8FC", 14)
           + rect(x + w / 2 - 40, y + 18, 80, 10, "#56657A", 5)
           + rect(x + 24, y + 50, w - 48, 70, PURPLE, 14) + rect(x + 24, y + 100, w - 48, 20, PURPLE, 0)
           + T(x + w / 2, y + 98, title, 28, 800, "#fff", "middle"))
    yy = y + 150
    for lab, val, st in fields:
        bc = {"ok": GREEN, "err": RED, "hl": ORANGE}.get(st, C["floor_line"])
        out += T(x + 48, yy, lab, 21, 700, MUTED)
        out += rect(x + 44, yy + 12, w - 88, 58, "#fff", 10, bc, 3)
        out += T(x + 62, yy + 52, val, 27, 800, RED if st == "err" else INK)
        if st == "ok":
            out += check(x + w - 78, yy + 41, 18)
        elif st == "err":
            out += cross(x + w - 78, yy + 41, 18)
        yy += 104
    if button:
        out += rect(x + 44, yy, w - 88, 64, GREEN, 14) + T(x + w / 2, yy + 42, button, 26, 800, "#fff", "middle")
    return out


def rack(x, y, cols, labels, stock, hl=None, cw=200, lh=150, levels=2):
    """Kệ nhìn thẳng: labels[c][l] = mã vị trí (l=0 là tầng dưới), stock = {(c,l): số thùng}."""
    h = lh * levels
    out, tags = "", ""
    for c in range(cols):
        for lv in range(levels):
            cx, cy = x + c * cw, y + h - (lv + 1) * lh
            key = (c, lv)
            if hl and key in hl:
                out += rect(cx + 6, cy + 6, cw - 12, lh - 18, "none", 10, hl[key], 5, 'stroke-dasharray="14 9"')
            n = stock.get(key, 0)
            for k in range(n):
                out += carton_flat(cx + 22 + k * 52, cy + lh - 70, 48, 52)
            tags += rect(cx + cw / 2 - 58, cy + lh - 14, 116, 30, "#FFE34D", 4, INK, 2)
            tags += T(cx + cw / 2, cy + lh + 8, labels[c][lv], 20, 900, INK, "middle")
    for c in range(cols + 1):
        out += rect(x + c * cw - 7, y - 20, 14, h + 20, "#5D7290", 3, INK, 2)
    for lv in range(levels + 1):
        out += rect(x - 7, y + h - lv * lh - 6, cols * cw + 14, 12, ORANGE if lv else "#5D7290", 3, INK, 2)
    return out + tags


def doc(x, y, w, title, lines, sign=True, col=BLUE):
    h = 120 + 46 * len(lines) + (120 if sign else 0)
    out = (rect(x + 10, y + 12, w, h, "#000", 10, extra='opacity="0.08"') + rect(x, y, w, h, "#fff", 10, INK, 3)
           + rect(x, y, w, 12, col, 6) + T(x + w / 2, y + 70, title, 32, 900, INK, "middle"))
    yy = y + 124
    for s in lines:
        out += T(x + 30, yy, s, 25, 600)
        yy += 46
    if sign:
        for i, who in enumerate(["Kho", "Tài xế"]):
            sx = x + 30 + i * (w - 60) / 2
            out += T(sx, yy + 30, who, 22, 700, MUTED)
            out += f'<line x1="{sx}" y1="{yy + 90}" x2="{sx + (w - 60) / 2 - 30}" y2="{yy + 90}" stroke="{INK}" stroke-width="2"/>'
            out += f'<path d="M{sx + 10} {yy + 80} q14 -26 26 0 t26 0 t26 -6" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    return out


def mail(x, y, w, sender, subject, fname):
    out = (rect(x + 8, y + 10, w, 250, "#000", 16, extra='opacity="0.08"') + rect(x, y, w, 250, "#fff", 16, INK, 3)
           + rect(x, y, w, 60, "#E3E8EF", 16) + rect(x, y + 40, w, 20, "#E3E8EF", 0)
           + T(x + 24, y + 40, "Email", 24, 800, MUTED)
           + T(x + 24, y + 108, "Từ: " + sender, 26, 700) + T(x + 24, y + 150, subject, 26, 600, MUTED))
    out += rect(x + 24, y + 176, w - 48, 52, "#E8F5EC", 10, GREEN, 2)
    out += rect(x + 38, y + 186, 32, 32, GREEN, 5) + T(x + 54, y + 210, "X", 20, 900, "#fff", "middle")
    out += T(x + 84, y + 211, fname, 24, 700, INK)
    return out


def sheet(x, y, w, headers, rows, cols, title=None):
    h = 64 + 52 * (len(rows) + 1)
    out = rect(x, y, w, h, "#fff", 10, INK, 3)
    if title:
        out += T(x, y - 18, title, 26, 800, GREEN)
    out += rect(x, y, w, 52, "#DDEFE3", 10) + rect(x, y + 30, w, 22, "#DDEFE3", 0)
    xx = x
    for hd, cw in zip(headers, cols):
        out += T(xx + 16, y + 36, hd, 22, 800, INK)
        xx += cw
    for i, row in enumerate(rows):
        ry = y + 52 + i * 52
        out += f'<line x1="{x}" y1="{ry}" x2="{x + w}" y2="{ry}" stroke="{C["floor_line"]}" stroke-width="2"/>'
        xx = x
        for cell, cw in zip(row, cols):
            out += T(xx + 16, ry + 36, cell, 24, 600)
            xx += cw
    return out


def printer(x, y):
    return (rect(x, y, 170, 90, "#5D7290", 12, INK, 3) + rect(x + 24, y - 30, 122, 34, "#fff", 4, INK, 2)
            + rect(x + 20, y + 54, 130, 12, INK, 4) + f'<circle cx="{x + 146}" cy="{y + 24}" r="7" fill="{GREEN}"/>')


def counter(x, y, label, a, b, col=GREEN):
    out = rect(x, y, 470, 130, "#fff", 18, col, 4) + T(x + 30, y + 46, label, 26, 700, MUTED)
    out += T(x + 30, y + 108, str(a), 52, 900, MUTED) + arrow(x + 120, y + 92, x + 220, y + 92, col, 6)
    out += T(x + 240, y + 108, str(b), 52, 900, col) + T(x + 240 + 34 * len(str(b)), y + 108, " thùng", 30, 700, col)
    return out


def chapter(n, title, items, on):
    b = rect(0, 0, 760, 1080, BLUE, 0)
    b += T(120, 420, f"PHẦN {n}", 34, 700, "#BFD8F5", extra='letter-spacing="4"')
    for i, ln in enumerate(title):
        b += T(120, 520 + i * 100, ln, 86, 900, "#fff")
    for i, s in enumerate(items):
        y = 380 + i * 150
        act = i == on
        b += f'<circle cx="930" cy="{y}" r="38" fill="{BLUE if act else "#fff"}" stroke="{BLUE}" stroke-width="4"/>'
        b += T(930, y + 13, str(i + 1), 36, 900, "#fff" if act else BLUE, "middle")
        b += T(1000, y + 14, s, 42, 800 if act else 600, INK if act else MUTED)
    return b


def remember(title, items, tail=None):
    b = floor()
    b += rect(200, 170, 1080, 600, "#fff", 22, INK, 3)
    b += T(260, 270, title, 64, 900) + rect(260, 295, 120, 8, ORANGE, 4)
    for i, s in enumerate(items):
        yy = 410 + i * 110
        b += check(300, yy - 14, 30) + T(350, yy, s, 40, 700)
    if tail:
        b += pill(740, 720, tail, BLUE, "#fff", 28)
    return b


# ------------------------------------------------------------------ screens
S = []


def hold(s):  # luật nhịp đọc của repo: (0.5 s + 0.3 s × số chữ) ÷ 1.3
    return (0.5 + 0.3 * len(s.split())) / 1.3


def screen_def(sid, part, title, svg, visual, subs, note=None, minimum=3.0):
    dur = max(minimum, sum(hold(x) for x in subs) + (1.0 if subs else 0))
    S.append(dict(id=sid, part=part, title=title, svg=svg, visual=visual, subs=subs, note=note, dur=dur))


P0, P1, P2, PE = "Mở đầu", "Phần 1 – Nhập hàng (02C)", "Phần 2 – Xuất hàng (04C)", "Tổng kết"

# S01 — Mở đầu
b = floor()
b += pill(270, 200, "VIDEO TRAINING WMS", ORANGE, "#fff", 26)
b += T(120, 330, "Quy trình kho", 96, 900) + T(120, 445, "cơ bản với WMS", 96, 900, BLUE)
b += T(120, 530, "Nhập hàng  →  Cất hàng  →  Xuất hàng", 40, 700, MUTED)
b += rack(1150, 300, 3, [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"], ["A-03-01", "A-03-02"]],
          {(0, 0): 3, (1, 1): 2, (2, 0): 2, (0, 1): 1}, cw=200, lh=160)
b += person("s01i", "instructor", 950, s=2.0, pose=WAVE)
screen_def("S01", P0, "Tiêu đề",
           frame(b, "Xin chào các bạn."),
           ["Tiêu đề hiện từng dòng, badge cam “VIDEO TRAINING WMS” bật nhẹ.",
            "Giảng viên bước vào giữa khung và vẫy tay; kệ kho bên phải là “sân nhà” của cả video.",
            "Dòng “Nhập hàng → Cất hàng → Xuất hàng” hiện từng cụm theo mũi tên."],
           ["Xin chào các bạn.",
            "Hôm nay chúng ta xem hàng đi qua kho như thế nào, và WMS giúp gì ở từng bước."])

# S02 — Toàn cảnh
b = floor()
b += T(960, 130, "Hàng đi qua kho", 60, 900, INK, "middle")
nodes = ["Nhận hàng", "Cất hàng", "Lưu kho", "Lấy hàng", "Kiểm hàng", "Giao hàng"]
for i, s in enumerate(nodes):
    x = 95 + i * 300
    col = GREEN if i < 2 else BLUE if i == 2 else ORANGE
    b += rect(x, 520, 250, 120, "#fff", 20, col, 5) + T(x + 125, 594, s, 34, 800, INK, "middle")
    b += f'<line x1="{x + 125}" y1="512" x2="960" y2="380" stroke="{BLUE}" stroke-width="3" stroke-dasharray="8 8"/>'
    if i < 5:
        b += arrow(x + 256, 580, x + 294, 580, INK, 5)
b += rect(700, 220, 520, 160, BLUE, 26) + T(960, 300, "WMS", 64, 900, "#fff", "middle")
b += T(960, 350, "ghi nhận từng bước", 28, 700, "#BFD8F5", "middle")
b += pill(560, 720, "PHẦN 1 · NHẬP", GREEN, "#fff", 26) + pill(1390, 720, "PHẦN 2 · XUẤT", ORANGE, "#fff", 26)
screen_def("S02", P0, "Toàn cảnh: hàng đi qua kho",
           frame(b, "Mỗi bước đều được ghi vào WMS."),
           ["6 ô nối nhau bằng mũi tên, sáng lần lượt từ trái sang phải; một thùng hàng nhỏ chạy theo dọc hàng ô.",
            "Khối WMS xanh ở trên, nét đứt nối xuống từng ô khi ô đó sáng: mỗi bước đều được ghi lại.",
            "Hai chip “Phần 1 · Nhập” (xanh lá) và “Phần 2 · Xuất” (cam) chia video làm hai nửa."],
           ["Hàng vào kho, được cất lên kệ, rồi được lấy ra giao cho khách.",
            "Mỗi bước đều được ghi vào WMS.",
            "Nhờ vậy lúc nào cũng biết: hàng gì, ở đâu, còn bao nhiêu."])

# S03 — Ba vai + nhãn bước
b = floor()
b += T(960, 120, "Ai làm gì?", 60, 900, INK, "middle")
b += prop(ms_desk(), 300, 830, 1.8) + person("s03x", "xlct", 230, s=1.8, pose=TYPE, tag="Nhân viên XLCT", tag_col=BLUE)
b += person("s03k", "receiver", 960, s=1.8, pose=SCAN, hand_r=pda_svg("s03k", laser=True, reach=70),
            tag="Nhân viên kho", tag_col=GREEN)
b += prop(ms_truck(), 1380, 830, 1.5) + person("s03d", "driver", 1330, s=1.8, pose=SIGN, hand_l=PAPER, hand_r=PEN,
                                                 tag="Tài xế", tag_col=MUTED)
for i, s in enumerate(["Nhận file, nhập WMS, in chứng từ", "Làm với hàng, quét bằng PDA", "Giao / nhận hàng, ký chứng từ"]):
    b += T([330, 960, 1560][i], 210, s, 28, 700, MUTED, "middle")
x = 640
b += T(370, 905, "Nhãn ở mỗi bước:", 30, 800)
for k in ("tay", "wms", "pda", "doc"):
    c, cw = chip(x, 895, k, 26)
    b += c
    x += cw + 22
screen_def("S03", P0, "Ba vai chính và nhãn bước",
           frame(b),
           ["3 vai xuất hiện lần lượt, mỗi vai làm đúng động tác của mình tại chỗ (gõ máy tính / quét PDA / ký giấy cạnh xe tải).",
            "Dải dưới: 4 nhãn sẽ gắn cạnh badge “Bước n” ở mọi bước — Thủ công (cam), WMS (xanh), Quét PDA (tím), "
            "Chứng từ (xám) — giống chú giải của bộ quy trình To-Be.",
            "Trong video, phụ đề đè lên dải nhãn; storyboard ẩn phụ đề để thấy dải nhãn."],
           ["Có ba vai chính: nhân viên xử lý chứng từ, nhân viên kho và tài xế.",
            "Nhãn cạnh mỗi bước cho biết bước đó làm tay, làm trên WMS hay quét bằng PDA."],
           "Phụ đề màn này đặt cao hơn (trên dải nhãn) khi dựng.")

# S04 — Thẻ chương 1
CH_ITEMS = ["Nhập hàng và cất hàng", "Xuất hàng theo đơn"]
screen_def("S04", P1, "Thẻ chương Phần 1",
           frame(chapter(1, ["Nhập hàng", "và cất hàng"], CH_ITEMS, 0)),
           ["Cùng kiểu thẻ chương của các video kho: nửa trái xanh, tên phần to màu trắng; bên phải mục lục 2 phần.",
            "Tiếng whoosh khi chuyển phần. Giữ khoảng 2–3 giây."],
           [], "Không có phụ đề trên thẻ chương.")

# S05 — Bước 1: Nhận ASN
b = floor() + badge(1, "Nhận ASN", ["tay"])
b += prop(ms_desk(), 330, 830, 1.8) + person("s05x", "xlct", 260, s=1.8, pose=TYPE, tag="Nhân viên XLCT", tag_col=BLUE)
b += mail(700, 190, 560, "Chủ hàng", "Kế hoạch nhập ngày 20/11", "KeHoachNhap_20-11.xlsx")
b += arrow(1280, 320, 1360, 320, ORANGE, 7)
b += sheet(1380, 230, 470, ["Mã hàng", "Tên hàng", "SL"], [["SKU 1001", "Nước suối", "50"], ["SKU 2001", "Mì ly", "40"]],
           [150, 220, 100], "Đúng mẫu WMS")
b += check(1820, 210, 26)
screen_def("S05", P1, "Bước 1: Nhận ASN (kế hoạch nhập)",
           frame(b, "Bước 1: chủ hàng gửi kế hoạch nhập, gọi là ASN."),
           ["Email từ chủ hàng bay vào, file Excel đính kèm mở ra thành bảng bên phải.",
            "XLCT gõ máy tính; vài ô trong bảng nhấp nháy rồi được sửa, dấu ✔ “Đúng mẫu WMS” bật ra.",
            "Badge “Bước 1” + nhãn THỦ CÔNG (việc ngoài hệ thống)."],
           ["Bước 1: chủ hàng gửi kế hoạch nhập, gọi là ASN.",
            "Nhân viên XLCT kiểm tra file và sửa cho đúng mẫu của WMS."])

# S06 — Bước 2: Nhập vào WMS
b = floor() + badge(2, "Nhập vào WMS", ["wms"])
b += prop(ms_desk(), 330, 830, 1.8) + person("s06x", "xlct", 260, s=1.8, pose=TYPE)
b += rect(700, 300, 150, 120, "#E8F5EC", 14, GREEN, 3) + T(775, 375, ".xlsx", 30, 900, GREEN, "middle")
b += arrow(860, 360, 940, 360, ORANGE, 7)
b += wms_win(960, 180, 880, "ASN-0001 · Chờ hàng đến", ["Mã hàng", "Tên hàng", "SL dự kiến", "Đã nhận"],
             [["SKU 1001", "Nước suối 500ml", "50", "0"], ["SKU 2001", "Mì ly", "40", "0"]], [190, 290, 200, 160],
             status="Đã tạo ASN")
screen_def("S06", P1, "Bước 2: Nhập vào WMS → tạo ASN",
           frame(b, "Bước 2: nhập file vào WMS. Hệ thống tạo ASN."),
           ["File .xlsx trượt vào cửa sổ WMS; bảng ASN-0001 hiện từng dòng.",
            "Cột “Đã nhận” = 0 để người xem thấy: WMS biết trước hàng gì, bao nhiêu, nhưng chưa có hàng.",
            "Chip xanh “Đã tạo ASN” bật ra (tiếng chime)."],
           ["Bước 2: nhập file vào WMS. Hệ thống tạo ASN.",
            "WMS biết trước hàng gì sắp đến và bao nhiêu."])

# S07 — Bước 3–4: Tạo phiếu nhập + Dỡ hàng
b = floor() + badge("3–4", "Tạo phiếu nhập, dỡ hàng", ["pda", "tay"])
b += prop(ms_truck(), 40, 830, 1.9)
b += person("s07d", "driver", 700, s=1.7)
for k in range(3):
    b += prop(carton_flat(0, 0, 60, 44), 820 + k * 116, 750, 1.8)
b += prop(carton_flat(0, 0, 60, 44), 878, 671, 1.8)
b += person("s07k", "receiver", 1290, s=1.8, pose=SCAN, hand_r=pda_svg("s07k", laser=True, reach=70),
            tag="Nhân viên kho", tag_col=GREEN)
b += pda_big(1420, 150, "Tạo phiếu nhập", [("ASN", "ASN-0001", None), ("Số xe", "51C-123.45", "hl"),
                                            ("Tài xế", "Minh", None)], "Tạo phiếu")
b += rect(760, 330, 440, 150, "#fff", 16, INK, 3) + T(786, 380, "Kiểm ngoại quan", 28, 800)
b += T(786, 430, "Không móp · không ướt", 26, 600, MUTED) + check(1150, 375, 24)
screen_def("S07", P1, "Bước 3–4: Tạo phiếu nhập, dỡ hàng",
           frame(b, "Bước 3: xe đến, nhân viên kho tạo phiếu nhập trên PDA."),
           ["Xe tải lùi vào cửa kho, tài xế bước xuống.",
            "PDA phóng to bên phải: chọn ASN-0001, nhập số xe và tên tài xế, bấm “Tạo phiếu”.",
            "Bước 4 (badge đổi sang “Bước 4” + nhãn THỦ CÔNG): thùng được dỡ xuống, thẻ “Kiểm ngoại quan” hiện ✔."],
           ["Bước 3: xe đến, nhân viên kho tạo phiếu nhập trên PDA.",
            "Bước 4: dỡ hàng xuống và kiểm tra bên ngoài thùng."],
           "Số xe, tên tài xế, mã hàng, số lượng đều là minh họa.")

# S08 — Bước 5: Nhận hàng
b = floor() + badge(5, "Nhận hàng", ["pda"])
for k in range(4):
    b += prop(carton_flat(0, 0, 60, 44, "1001"), 260 + (k % 2) * 116, 750 - (k // 2) * 80, 1.8)
b += person("s08k", "receiver", 640, s=1.9, pose=SCAN, hand_r=pda_svg("s08k", laser=True, reach=90))
b += pda_big(900, 140, "Nhận hàng · ASN-0001", [("Quét mã hàng", "SKU 1001", "ok"), ("Số lượng thực nhận", "50", "hl"),
                                                 ("Dự kiến / đã nhận", "50 / 50", "ok")], "Xác nhận hoàn tất")
b += rect(1420, 300, 420, 230, "#fff", 18, RED, 4) + T(1450, 360, "Nếu lệch số lượng?", 30, 800, RED)
b += T(1450, 410, "Dự kiến 40 · nhận 38", 27, 700, INK) + T(1450, 460, "→ WMS báo thiếu 2", 27, 700, RED)
screen_def("S08", P1, "Bước 5: Nhận hàng (quét mã + số lượng)",
           frame(b, "Bước 5: quét mã vạch trên thùng và nhập số lượng thực nhận."),
           ["Tia quét đỏ chạm thùng, tiếng beep; PDA phóng to điền “SKU 1001” với ✔.",
            "Ô số lượng nhập 50, dòng “Dự kiến / đã nhận” đổi thành 50 / 50 ✔, nút “Xác nhận hoàn tất” sáng.",
            "Thẻ đỏ bên phải: ví dụ mã SKU 2001 dự kiến 40 nhận 38 → WMS báo thiếu 2 ngay tại chỗ."],
           ["Bước 5: quét mã vạch trên thùng và nhập số lượng thực nhận.",
            "WMS so với ASN ngay tại chỗ. Nhận đủ thì xác nhận hoàn tất."],
           "Cách xử lý khi thiếu/thừa không có trong quy trình chuẩn 02C → chỉ minh họa việc WMS báo lệch, không dạy cách xử lý.")

# S09 — Bước 6: In và ký
b = floor() + badge(6, "In và ký phiếu nhập kho", ["wms", "doc"])
b += prop(ms_desk(), 330, 830, 1.8) + person("s09x", "xlct", 260, s=1.8, pose=TYPE)
b += printer(700, 560)
b += doc(930, 170, 520, "PHIẾU NHẬP KHO", ["ASN-0001 · 20/11", "SKU 1001 · Nước suối · 50", "SKU 2001 · Mì ly · 38"])
b += person("s09d", "driver", 1620, s=1.8, pose=SIGN, hand_l=PAPER, hand_r=PEN)
b += counter(1060, 700, "Tồn kho SKU 1001", 0, 50)
screen_def("S09", P1, "Bước 6: In và ký phiếu nhập kho",
           frame(b, "Bước 6: XLCT in phiếu nhập kho để các bên ký."),
           ["Máy in đẩy tờ “PHIẾU NHẬP KHO” lên giữa khung; hai chữ ký (Kho, Tài xế) được vẽ ra.",
            "Tài xế ký bên phải.",
            "Bộ đếm “Tồn kho SKU 1001: 0 → 50” nhảy số (tiếng stamp ✔)."],
           ["Bước 6: XLCT in phiếu nhập kho để các bên ký.",
            "Hàng đã có trong tồn kho của WMS."])

# S10 — Bước 7: Cất hàng
b = floor() + badge(7, "Cất hàng vào vị trí", ["pda"])
b += rack(620, 260, 3, [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"], ["A-03-01", "A-03-02"]],
          {(0, 0): 2, (2, 0): 3, (2, 1): 1}, hl={(0, 1): GREEN}, cw=210, lh=270)
b += pill(725, 205, "WMS gợi ý", GREEN, "#fff", 24)
b += prop(ms_trolley(), 260, 830, 1.6) + person("s10k", "receiver", 220, s=1.8, pose=PUSH)
b += arrow(560, 760, 680, 560, GREEN, 6, True)
b += pda_big(1340, 140, "Cất hàng", [("Quét mã hàng · SL", "SKU 1001 · 50", "ok"), ("Vị trí gợi ý", "A-01-02", "hl"),
                                      ("Quét mã vị trí", "A-01-02", "ok")], "Xác nhận")
screen_def("S10", P1, "Bước 7: Cất hàng (putaway)",
           frame(b, "Bước 7: quét hàng, WMS gợi ý vị trí cất."),
           ["PDA: quét hàng + số lượng → ô “Vị trí gợi ý A-01-02” sáng cam; trên kệ, ô A-01-02 viền xanh nét đứt + chip “WMS gợi ý”.",
            "Nhân viên đẩy xe hàng theo mũi tên nét đứt tới kệ, quét mã vị trí (beep), ô “Quét mã vị trí” ✔.",
            "Thùng trượt vào ô A-01-02, viền nét đứt chuyển thành viền liền xanh."],
           ["Bước 7: quét hàng, WMS gợi ý vị trí cất.",
            "Mang hàng tới đúng vị trí và quét mã vị trí để xác nhận.",
            "Từ giờ, hàng có địa chỉ trong kho."])

# S11 — Ghi nhớ phần 1
screen_def("S11", P1, "Ghi nhớ Phần 1",
           frame(remember("Ghi nhớ", ["Có ASN trước khi hàng đến", "Nhận hàng: quét mã + nhập số lượng",
                                      "Cất hàng xong phải quét vị trí"], "Tiếp theo: Xuất hàng theo đơn")),
           ["Thẻ “Ghi nhớ” giống các video kho trước; 3 ý hiện lần lượt, mỗi ý có ✔.",
            "Dải xanh “Tiếp theo: Xuất hàng theo đơn” bật ra cuối cùng."],
           ["Hàng đã nằm trên kệ. Giờ chúng ta xuất hàng."])

# S12 — Thẻ chương 2
screen_def("S12", P2, "Thẻ chương Phần 2",
           frame(chapter(2, ["Xuất hàng", "theo đơn"], CH_ITEMS, 1)),
           ["Cùng khung S04, mục 2 sáng lên."], [], "Không có phụ đề trên thẻ chương.")

# S13 — Bước 1–2: Kế hoạch xuất → WMS
b = floor() + badge("1–2", "Nhận kế hoạch xuất, nhập WMS", ["tay", "wms"])
b += prop(ms_desk(), 330, 830, 1.8) + person("s13x", "xlct", 260, s=1.8, pose=TYPE)
b += mail(690, 200, 520, "Chủ hàng", "Đơn giao Cửa hàng 05", "KeHoachXuat_21-11.xlsx")
b += arrow(1225, 330, 1290, 330, ORANGE, 7)
b += wms_win(1300, 180, 560, "DO-0001 · Cửa hàng 05", ["Mã hàng", "SL đặt"],
             [["SKU 1001", "20"], ["SKU 2001", "10"]], [280, 240], status="Đã tạo đơn xuất")
screen_def("S13", P2, "Bước 1–2: Nhận kế hoạch xuất, nhập WMS",
           frame(b, "Bước 1 và 2: chủ hàng gửi kế hoạch xuất, XLCT nhập vào WMS."),
           ["Giống Bước 1–2 của phần nhập (người xem nhận ra ngay): email → file → cửa sổ WMS.",
            "Badge “Bước 1–2” với 2 nhãn THỦ CÔNG + WMS; đơn xuất DO-0001 hiện 2 dòng."],
           ["Bước 1 và 2: chủ hàng gửi kế hoạch xuất, XLCT nhập vào WMS.",
            "Hệ thống tạo đơn xuất, biết cần giao hàng gì và bao nhiêu."])

# S14 — Bước 3: Phân bổ tồn
b = floor() + badge(3, "Phân bổ tồn kho", ["wms"])
b += rack(160, 300, 2, [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"]], {(0, 0): 3, (0, 1): 3},
          hl={(0, 0): ORANGE}, cw=260, lh=230)
b += rect(760, 230, 520, 120, "#fff", 18, ORANGE, 4) + T(790, 285, "Lô A-01-01 · nhập 10/11", 28, 800)
b += T(790, 330, "30 thùng → lấy 20", 28, 700, ORANGE) + check(1230, 290, 26)
b += rect(760, 380, 520, 120, "#fff", 18, C["floor_line"], 4) + T(790, 435, "Lô A-01-02 · nhập 20/11", 28, 800, MUTED)
b += T(790, 480, "50 thùng → để sau", 28, 700, MUTED)
b += rect(1340, 230, 500, 270, BLUE, 22)
b += T(1590, 310, "FIFO", 64, 900, "#fff", "middle") + T(1590, 360, "nhập trước – xuất trước", 28, 700, "#BFD8F5", "middle")
b += T(1590, 440, "FEFO: hết hạn trước –", 26, 700, "#fff", "middle") + T(1590, 476, "xuất trước", 26, 700, "#fff", "middle")
screen_def("S14", P2, "Bước 3: Phân bổ tồn kho (FIFO)",
           frame(b, "Bước 3: WMS chạy phân bổ tồn kho để chọn hàng cần lấy."),
           ["Kệ bên trái có 2 lô SKU 1001: lô cũ A-01-01 (nhập 10/11) và lô mới vừa cất ở A-01-02 (nhập 20/11, từ Phần 1).",
            "Hai thẻ lô xếp chồng; thẻ lô cũ viền cam + “lấy 20” ✔, thẻ lô mới mờ “để sau”.",
            "Khối FIFO xanh bên phải; dòng FEFO nhỏ cho hàng có hạn dùng."],
           ["Bước 3: WMS chạy phân bổ tồn kho để chọn hàng cần lấy.",
            "Theo FIFO, lô nhập trước được xuất trước, dù lô mới vừa được cất lên kệ."],
           "Lô cũ 10/11 là dữ liệu minh họa thêm để thấy FIFO; Phần 1 chỉ nhập lô 20/11.")

# S15 — Bước 4: Lấy hàng
b = floor() + badge(4, "Lấy hàng", ["pda"])
b += rack(160, 300, 2, [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"]], {(0, 0): 1, (0, 1): 3},
          hl={(0, 0): ORANGE}, cw=260, lh=230)
b += prop(ms_trolley(), 780, 830, 1.6) + person("s15p", "picker", 720, s=1.8, pose=SCAN,
                                                hand_r=pda_svg("s15p", laser=True, reach=80), tag="Nhân viên kho", tag_col="#B88C00")
b += pda_big(1340, 120, "Lấy hàng · DO-0001", [("Đi tới vị trí", "A-01-01", "hl"), ("Quét vị trí", "A-01-01", "ok"),
                                               ("Quét mã hàng", "SKU 1001", "ok"), ("Đã lấy", "20 / 20", "ok")])
b += pill(1555, 880, "→ Khu chờ xuất", ORANGE, "#fff", 26)
screen_def("S15", P2, "Bước 4: Lấy hàng",
           frame(b, "Bước 4: PDA chỉ vị trí cần đến."),
           ["PDA hiện “Đi tới vị trí A-01-01” (cam); nhân viên kéo xe hàng tới kệ.",
            "Quét vị trí (beep) ✔ → quét mã hàng ✔ → số lấy chạy 0 → 20 / 20 ✔; 2 thùng còn lại 1 trên kệ.",
            "Chip cam “→ Khu chờ xuất”; nhân viên kéo xe ra khỏi khung."],
           ["Bước 4: PDA chỉ vị trí cần đến.",
            "Quét vị trí, quét mã hàng, xác nhận số lượng đã lấy.",
            "Lấy xong, đưa hàng ra khu chờ xuất."])

# S16 — Bước 5: Kiểm hàng
b = floor() + badge(5, "Kiểm hàng", ["pda"])
b += rect(120, 640, 620, 190, "#FFE9D2", 16, ORANGE, 3, 'stroke-dasharray="14 10"')
b += T(430, 690, "KHU CHỜ XUẤT", 28, 900, ORANGE, "middle")
for k in range(4):
    b += prop(carton_flat(0, 0, 60, 44), 170 + k * 130, 742, 1.8)
b += person("s16c", "checker", 880, s=1.9, pose=SCAN, hand_r=pda_svg("s16c", laser=True, reach=90),
            tag="Nhân viên kho", tag_col=PURPLE)
b += pda_big(1060, 150, "Kiểm hàng · DO-0001", [("Quét mã hàng", "SKU 1001", "ok"), ("SL đã kiểm", "20 / 20", "ok")],
             "Xác nhận hoàn tất", w=400)
b += rect(1500, 220, 360, 300, "#fff", 18, RED, 4) + T(1530, 280, "Quét nhầm?", 32, 800, RED)
b += T(1530, 335, "SKU 1002", 30, 800) + T(1530, 385, "Không có trong đơn", 26, 700, RED) + cross(1790, 440, 34)
screen_def("S16", P2, "Bước 5: Kiểm hàng",
           frame(b, "Bước 5: quét lại mã hàng, đếm bằng mắt và xác nhận số lượng."),
           ["Hàng ở khu chờ xuất (nền cam nét đứt). Nhân viên kho quét từng thùng, số kiểm chạy tới 20 / 20 ✔.",
            "Thẻ đỏ bên phải: quét nhầm SKU 1002 → WMS báo “Không có trong đơn” ✖ (tiếng báo lỗi).",
            "Bấm “Xác nhận hoàn tất”."],
           ["Bước 5: quét lại mã hàng, đếm bằng mắt và xác nhận số lượng.",
            "Sai mã hay sai số lượng, WMS báo ngay trước khi hàng rời kho."])

# S17 — Bước 6: Hoàn tất
b = floor() + badge(6, "Hoàn tất, in phiếu xuất kho", ["wms", "doc"])
b += prop(ms_desk(), 280, 830, 1.6) + person("s17x", "xlct", 220, s=1.6, pose=TYPE)
b += doc(560, 170, 470, "PHIẾU XUẤT KHO", ["DO-0001 · Cửa hàng 05", "SKU 1001 · 20", "SKU 2001 · 10"])
b += prop(ms_truck(), 1150, 830, 1.8)
for k in range(3):
    b += prop(carton_flat(0, 0, 60, 44), 1290 + k * 116, 690, 1.8)
b += person("s17d", "driver", 1110, s=1.7, pose=SIGN, hand_l=PAPER, hand_r=PEN)
b += counter(560, 700, "Tồn kho SKU 1001", 80, 60, ORANGE)
screen_def("S17", P2, "Bước 6: Hoàn tất, in phiếu xuất kho",
           frame(b, "Bước 6: XLCT hoàn tất đơn và in phiếu xuất kho để các bên ký."),
           ["Tờ “PHIẾU XUẤT KHO” in ra, tài xế ký; thùng hàng trượt lên thùng xe.",
            "Bộ đếm “Tồn kho SKU 1001: 80 → 60” (30 lô cũ + 50 lô mới, xuất 20).",
            "Xe tải chạy ra khỏi khung (tiếng xe nhỏ)."],
           ["Bước 6: XLCT hoàn tất đơn và in phiếu xuất kho để các bên ký.",
            "Hàng rời kho, tồn kho trên WMS tự giảm."],
           "Bước xếp hàng lên xe không có trong 04C (chỉ là hình minh họa); kiểm soát xe ra/vào là quy trình 07B, không đưa vào video này.")

# S18 — Tổng kết
b = floor()
b += T(960, 110, "Tóm tắt", 60, 900, INK, "middle")
rows = [("NHẬP · 02C", GREEN, ["Nhận ASN", "Nhập WMS", "Tạo phiếu nhập", "Dỡ hàng", "Nhận hàng", "In & ký", "Cất hàng"]),
        ("XUẤT · 04C", ORANGE, ["Kế hoạch xuất", "Nhập WMS", "Phân bổ tồn", "Lấy hàng", "Kiểm hàng", "Hoàn tất"])]
for r, (lab, col, steps) in enumerate(rows):
    y = 190 + r * 170
    b += pill(150, y + 50, lab, col, "#fff", 24)
    for i, s in enumerate(steps):
        x = 280 + i * 230
        b += rect(x, y, 210, 100, "#fff", 14, col, 4) + T(x + 105, y + 40, str(i + 1), 24, 900, col, "middle")
        b += T(x + 105, y + 78, s, 23, 800, INK, "middle")
b += rect(280, 560, 1100, 230, "#fff", 22, INK, 3) + T(320, 625, "Ghi nhớ", 44, 900) + rect(320, 645, 90, 7, ORANGE, 4)
for i, s in enumerate(["Chứng từ đi trước, hàng đi sau", "Mọi thao tác với hàng đều quét PDA"]):
    b += check(340, 700 + i * 52 - 10, 20) + T(375, 700 + i * 52, s, 30, 700)
b += person("s18i", "instructor", 1620, s=2.0, pose=RAISE)
screen_def("S18", PE, "Tóm tắt 13 bước + Ghi nhớ",
           frame(b, "Quét đúng thì tồn kho đúng."),
           ["Hai hàng ô: 7 bước nhập (xanh lá) và 6 bước xuất (cam), sáng lần lượt như băng chuyền.",
            "Thẻ “Ghi nhớ” 2 ý; câu chốt “Quét đúng thì tồn kho đúng” là phụ đề cuối.",
            "Giảng viên giơ tay chào kết. Giữ khung cuối 2 giây."],
           ["Tóm lại: chứng từ đi trước, hàng đi sau, và mọi thao tác với hàng đều quét PDA.",
            "Quét đúng thì tồn kho đúng.", "Hẹn gặp lại ở các quy trình tiếp theo."], minimum=4.0)


# ------------------------------------------------------------------ timing + page
def mmss(t):
    return f"{int(t // 60)}:{int(round(t % 60)):02d}"


t = 0.0
for s in S:
    s["time"] = f"{mmss(t)}–{mmss(t + s['dur'])}"
    t += s["dur"]
TOTAL = t

with open(os.path.join(os.path.dirname(__file__), "storyboard_page.html"), encoding="utf-8") as f:
    page = f.read()
page = page.replace("<title>Storyboard Hành trình kỹ năng</title>", "<title>Storyboard WMS cơ bản</title>")
page = page.replace("Storyboard · bản 2", "Storyboard · bản 1")
page = page.replace("<h1>Hành trình tạo kỹ năng làm video theo ý tôi</h1>", "<h1>Quy trình kho cơ bản với WMS</h1>")
page = page.replace(
    "{{COUNT}} màn cho video khoảng 3 phút, dựng theo mục [B1] của prompt. Mỗi khung là ảnh tĩnh của khoảnh khắc chính, "
    "đúng màu, font và nhân vật của các video kho; ảnh trong khung màn hình là ảnh thật trích từ các bản render.",
    f"{{{{COUNT}}}} màn, khoảng {mmss(TOTAL)} (tính theo nhịp đọc phụ đề 1.3×). Nội dung bám bộ quy trình To-Be chuẩn: "
    "<b>02C Nhập hàng mới – Barcode mã hàng</b> (7 bước) và <b>04C Xuất kho theo đơn – Barcode</b> (6 bước). "
    "Mỗi khung là ảnh tĩnh của khoảnh khắc chính, đúng màu, font và bộ nhân vật của các video kho.")
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
print("wrote", OUT, len(page) // 1024, "KB,", len(S), "screens,", mmss(TOTAL))
