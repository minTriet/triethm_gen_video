"""Bộ vẽ dùng chung cho video "Quy trình kho cơ bản với WMS": storyboard và video dùng cùng hình.

Mọi hàm trả về chuỗi SVG trong hệ toạ độ 1920×1080. Nhân vật lấy từ kit.py (skill nhan-vat-kho).
"""
import html
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from kit import C, stick, pda_svg  # noqa: E402,F401
from model_sheet import carton_flat, desk as ms_desk, truck as ms_truck, trolley as ms_trolley  # noqa: E402,F401


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


