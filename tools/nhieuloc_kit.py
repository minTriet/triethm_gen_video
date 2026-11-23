"""Bộ vẽ dùng chung cho storyboard và video demo Nhiêu Lộc (kho lạnh): logo TKSolution, pallet, kệ pallet,
khu chất chồng, xe nâng, bảng −18°C, cân, ổ khoá, ô điều kiện, badge mã quy trình, thẻ chương 5 phần.
Mọi hàm trả về chuỗi SVG trong hệ toạ độ 1920×1080.
"""
import base64
import io
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from wms_kit import *  # noqa: E402,F401,F403
from wms_kit import CHIP, frame as _frame  # noqa: E402
from kit import folder_svg, MANAGER_HOLD, TYPE  # noqa: E402,F401,F811  (TYPE: model XLCT mới, tay gõ phím cao hơn)
from model_sheet import forklift, forklift_back  # noqa: E402

CHIP["pda"] = ("QUÉT MÃ", PURPLE)
CHIP["can"] = ("CÂN", "#0E8C9A")
ICE, ICE_D = "#DCEFFB", "#2A86C9"
WOOD, WOOD_D = "#C9965A", "#A97A44"


# ------------------------------------------------------------------ logo TKSolution (design/logo-tksolution.png)
_buf = io.BytesIO()  # nền trong suốt: logo hoà vào màu nền khung
Image.open(os.path.join(os.path.dirname(__file__), "..", "design", "logo-tksolution-trong-suot.png")).quantize(
    64, method=Image.Quantize.FASTOCTREE).save(_buf, "PNG", optimize=True)
LOGO_URI = "data:image/png;base64," + base64.b64encode(_buf.getvalue()).decode()
LOGO_AR = 620 / 144


def logo(x, y, w, card=False):
    h = w / LOGO_AR
    bg = rect(x - 14, y - 10, w + 28, h + 20, "#fff", 12, extra='opacity="0.96"') if card else ""
    return bg + f'<image href="{LOGO_URI}" x="{x}" y="{y}" width="{w}" height="{h:.1f}"/>'


def frame(body, sub=None, mark=True):
    """Khung chuẩn + logo TKSolution nhỏ ở góc dưới phải."""
    return _frame(body + (logo(1676, 1016, 210) if mark else ""), sub)


# ------------------------------------------------------------------ props riêng cho kho lạnh
def qr(x, y, sz=40):
    m = sz / 7
    out = rect(x, y, sz, sz, "#fff", 2, INK, 1.5)
    for fx, fy in ((0, 0), (4, 0), (0, 4)):
        out += rect(x + fx * m + m * .3, y + fy * m + m * .3, m * 2.4, m * 2.4, INK, 1)
    for gx, gy in ((4, 4), (5, 5), (3, 3), (4, 6), (6, 4), (3, 5)):
        out += rect(x + gx * m + m * .15, y + gy * m + m * .15, m * .8, m * .8, INK, 0)
    return out


def lpn_tag(x, y, code, w=170, size=18):
    bars = "".join(rect(x + 12 + i * 6, y + 8, 2.5 if i % 3 else 4, 20, INK, 0) for i in range(int((w - 24) / 6)))
    return rect(x, y, w, 58, "#fff", 4, INK, 2) + bars + T(x + w / 2, y + 50, code, size, 900, INK, "middle")


def pallet(x, base, cols=3, rows=3, cw=58, ch=44, lpn=None, qrs=False, label=None, dim=False):
    """Pallet nhìn thẳng, đáy pallet ở y = base. Rộng cols*cw+16, cao rows*ch+22."""
    W = cols * cw + 16
    out = rect(x, base - 22, W, 22, WOOD, 3, INK, 2.5)
    for bx in (6, W / 2 - 13, W - 32):
        out += rect(x + bx, base - 12, 26, 12, WOOD_D, 1, INK, 1.5)
    for r in range(rows):
        for c in range(cols):
            cx, cy = x + 8 + c * cw, base - 22 - (r + 1) * ch
            out += carton_flat(cx, cy, cw - 4, ch - 4, label)
            if qrs:
                out += qr(cx + cw - 22, cy + 4, 14)
    if lpn:
        out += lpn_tag(x + W / 2 - 62, base - 22 - ch * 0.5 - 22, lpn, 124, 15)
    if dim:
        out = f'<g opacity="0.35">{out}</g>'
    return out


def rack_pallets(x, y, cols, levels, labels, filled, hl=None, cw=240, lh=210, **pk):
    """Kệ pallet: filled = {(c, l): dict tham số pallet} hoặc tập vị trí. Mỗi vị trí đúng 1 pallet."""
    h = lh * levels
    out = ""
    for key in filled:
        c, lv = key
        opt = dict(pk)
        if isinstance(filled, dict):
            opt.update(filled[key] or {})
        W = opt.get("cols", 3) * opt.get("cw", 58) + 16
        out += pallet(x + c * cw + (cw - W) / 2, y + h - lv * lh - 6, **opt)
    return out + rack(x, y, cols, labels, {}, hl, cw, lh, levels)


def stack_zone(x, base, lanes, lw=230, ph=110, hl=None, **pk):
    """Khu chất chồng: lanes = [(mã ô, số pallet chồng)]; hl = {i: màu} viền chỗ pallet kế tiếp."""
    out = ""
    for i, (lab, n) in enumerate(lanes):
        xx = x + i * lw
        out += rect(xx + 8, base - 3, lw - 16, 8, "#FFD84D", 2, INK, 1.5)
        for k in range(n):
            out += pallet(xx + (lw - 190) / 2, base - k * ph, rows=2, **pk)
        if hl and i in hl:
            out += rect(xx + 12, base - (n + 1) * ph - 6, lw - 24, ph + 4, "none", 10, hl[i], 5, 'stroke-dasharray="14 9"')
        out += rect(xx + lw / 2 - 52, base + 18, 104, 34, "#FFE34D", 4, INK, 2) + T(xx + lw / 2, base + 44, lab, 22, 900, INK, "middle")
    return out


def lift(fid, x, base=830, s=1.8, load=True, flip=False):
    ld = pallet(50, -22, cols=2, rows=2, cw=46, ch=36) if load else ""
    fl = f"scale({-s},{s})" if flip else f"scale({s})"
    return (f'<g transform="translate({x},{base}) {fl}">{forklift_back()}'
            f'<g transform="translate(-22,-14)">{stick(fid, "forklift", 1.0, pose={"armR": (-70, -20), "armL": (10, -40)})}</g>'
            f'{forklift()}{ld}</g>')


def cold_sign(x, y, w=230):
    flake = "".join(f'<line x1="{x + 46}" y1="{y + 40}" x2="{x + 46 + 22 * __import__("math").cos(a)}" '
                    f'y2="{y + 40 + 22 * __import__("math").sin(a)}" stroke="{ICE_D}" stroke-width="5" stroke-linecap="round"/>'
                    for a in (0, 1.047, 2.094, 3.142, 4.189, 5.236))
    return rect(x, y, w, 80, ICE, 18, ICE_D, 4) + flake + T(x + 84, y + 54, "−18°C", 40, 900, ICE_D)


def scale_svg(x, base, reading):
    return (rect(x, base - 28, 250, 28, "#8FA3BF", 6, INK, 3) + rect(x + 222, base - 210, 16, 184, "#5D7290", 3, INK, 2)
            + rect(x + 160, base - 286, 170, 80, INK, 12) + rect(x + 172, base - 276, 146, 60, "#0F2A1E", 6)
            + T(x + 245, base - 232, reading, 34, 900, "#7CFFB2", "middle"))


def lock(cx, cy, s=1.0, col=RED):
    return (f'<path d="M{cx - 18 * s} {cy} v{-14 * s} a{18 * s} {18 * s} 0 0 1 {36 * s} 0 v{14 * s}" fill="none" '
            f'stroke="{col}" stroke-width="{7 * s}"/>' + rect(cx - 28 * s, cy, 56 * s, 44 * s, col, 8 * s)
            + f'<circle cx="{cx}" cy="{cy + 20 * s}" r="{6 * s}" fill="#fff"/>')


def diamond(cx, cy, w, h, lines, col=ORANGE):
    out = (f'<polygon points="{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}" '
           f'fill="#FFF4DC" stroke="{col}" stroke-width="5" stroke-linejoin="round"/>')
    for i, ln in enumerate(lines):
        out += T(cx, cy + 12 + (i - (len(lines) - 1) / 2) * 40, ln, 30, 800, INK, "middle")
    return out


def box(x, y, w, h, title, lines=(), col=BLUE, size=30):
    out = rect(x, y, w, h, "#fff", 18, col, 4) + T(x + 28, y + 52, title, size, 800, col)
    for i, s in enumerate(lines):
        out += T(x + 28, y + 100 + i * 42, s, 26, 600, INK)
    return out


def code_badge(code, title, chips=()):
    cw = tw(code, 30) + 40
    out = rect(48, 54, cw, 60, BLUE, 12) + T(48 + cw / 2, 95, code, 30, 900, "#fff", "middle")
    w = tw(title, 30) + 56
    out += rect(48 + cw + 14, 54, w, 60, "#fff", 12, INK, 3) + T(48 + cw + 40, 95, title, 30, 800)
    x = 48 + cw + 14 + w + 22
    for k in chips:
        c, ww = chip(x, 84, k)
        out += c
        x += ww + 14
    return out


def chapter5(n, title, items, on):
    b = rect(0, 0, 760, 1080, BLUE, 0)
    b += T(120, 400, f"PHẦN {n}", 34, 700, "#BFD8F5", extra='letter-spacing="4"')
    for i, ln in enumerate(title):
        b += T(120, 500 + i * 96, ln, 80, 900, "#fff")
    for i, (s, code) in enumerate(items):
        y = 260 + i * 140
        act = i == on
        b += f'<circle cx="930" cy="{y}" r="38" fill="{BLUE if act else "#fff"}" stroke="{BLUE}" stroke-width="4"/>'
        b += T(930, y + 13, str(i + 1), 36, 900, "#fff" if act else BLUE, "middle")
        b += T(1000, y + 4, s, 40, 800 if act else 600, INK if act else MUTED)
        b += T(1000, y + 46, code, 26, 700, BLUE if act else "#A3ADBA")
    return b
