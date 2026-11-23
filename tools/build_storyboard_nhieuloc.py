"""Storyboard video demo đề xuất cho khách hàng Công ty Nhiêu Lộc (kho thịt đông lạnh, WMS).

Nguồn: source/Nhieu_Loc_-_Bo_quy_trinh_kho.drawio — 01A, 01B, 02B, 03B, 03C, 03D, 04C, 05B.
Bối cảnh khách hàng: kho đông lạnh 2 khu (Khu A có kệ: 1 vị trí = 1 pallet; Khu B không kệ: pallet chất chồng),
hàng thịt đông lạnh đồng ký / đa ký, xuất chẵn pallet và xuất theo thùng.
Người xem: cấp quản lý của Nhiêu Lộc (video đi kèm proposal).

Chạy:  python3 tools/build_storyboard_nhieuloc.py design/storyboard-nhieu-loc.html
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from wms_kit import *  # noqa: E402,F401,F403
from wms_kit import esc, CHIP, frame as _frame  # noqa: E402
from kit import folder_svg, MANAGER_HOLD, TYPE  # noqa: E402,F811  (TYPE: model XLCT mới, tay gõ phím cao hơn)
import base64  # noqa: E402
import io  # noqa: E402
from PIL import Image  # noqa: E402
from model_sheet import forklift, forklift_back  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "design/storyboard-nhieu-loc.html"
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


# ------------------------------------------------------------------ screens
S = []


def hold(s):  # luật nhịp đọc của repo: (0.5 s + 0.3 s × số chữ) ÷ 1.3
    return (0.5 + 0.3 * len(s.split())) / 1.3


def screen_def(sid, part, title, svg, visual, subs, note=None, minimum=3.0):
    dur = max(minimum, sum(hold(x) for x in subs) + (1.0 if subs else 0))
    S.append(dict(id=sid, part=part, title=title, svg=svg, visual=visual, subs=subs, note=note, dur=dur))


def scr(sid, part, title, body, visual, subs, note=None, mark=True, **kw):
    screen_def(sid, part, title, frame(body, subs[0] if subs else None, mark), visual, subs, note, **kw)


P0, PE = "Mở đầu", "Kết"
P1, P2, P3, P4, P5 = ("Phần 1 – Thiết lập (01A, 01B)", "Phần 2 – Nhập hàng (02B)", "Phần 3 – Trong kho (03B, 03C, 03D)",
                      "Phần 4 – Xuất hàng theo kg (04C)", "Phần 5 – Kiểm kê (05B)")
CH = [("Thiết lập chủ hàng, giá bán", "01A · 01B"), ("Nhập hàng, cất hàng", "02B"),
      ("Khoá lô, chuyển pallet", "03B · 03C · 03D"), ("Xuất hàng theo kg", "04C"), ("Kiểm kê", "05B")]
MAIN_RACK = [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"], ["A-03-01", "A-03-02"]]

# S01 — Tiêu đề
b = floor()
b += logo(110, 40, 400, card=False)
b += pill(330, 190, "ĐỀ XUẤT GIẢI PHÁP · BẢN DEMO", ORANGE, "#fff", 26)
b += T(110, 320, "Vận hành kho lạnh", 92, 900) + T(110, 430, "cho Nhiêu Lộc", 92, 900, BLUE)
b += T(110, 515, "Thịt đông lạnh · Kệ pallet + Chất chồng · WMS", 38, 700, MUTED)
b += cold_sign(110, 580)
b += rack_pallets(1180, 300, 3, 2, MAIN_RACK, {(0, 0), (1, 0), (2, 0), (0, 1), (2, 1)}, cw=230, lh=260, qrs=True)
b += person("s01i", "instructor", 990, s=2.0, pose=WAVE)
scr("S01", P0, "Tiêu đề", b,
    ["Logo TKSolution hiện trước ở góc trên trái; badge cam “ĐỀ XUẤT GIẢI PHÁP · BẢN DEMO” bật nhẹ; hai dòng tiêu đề hiện lần lượt, “Nhiêu Lộc” màu xanh.",
     "Bảng nhiệt độ −18°C có bông tuyết xoay chậm; kệ pallet thịt đông lạnh bên phải.",
     "Giảng viên (áo đồng phục TK) bước vào và vẫy tay."],
    ["Kính chào Ban lãnh đạo Công ty Nhiêu Lộc.",
     "Video này trình bày cách kho sẽ vận hành hàng thịt đông lạnh của Nhiêu Lộc trên hệ thống WMS."], mark=False)

# S02 — Hai khu kho
b = floor()
b += T(960, 120, "Kho đông lạnh có 2 khu", 58, 900, INK, "middle") + cold_sign(1640, 60, 220)
b += rect(40, 180, 900, 640, "#fff", 24, BLUE, 4, 'opacity="0.55"') + rect(980, 180, 900, 640, "#fff", 24, ORANGE, 4, 'opacity="0.55"')
b += pill(250, 230, "KHU A · CÓ DÃY KỆ", BLUE, "#fff", 28) + pill(1200, 230, "KHU B · CHẤT CHỒNG", ORANGE, "#fff", 28)
b += rack_pallets(130, 330, 3, 2, MAIN_RACK, {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)}, hl={(2, 1): GREEN}, cw=240, lh=230)
b += T(490, 300, "1 vị trí = 1 pallet", 32, 800, BLUE, "middle")
b += stack_zone(1000, 800, [("B-01", 3), ("B-02", 2), ("B-03", 3), ("B-04", 1)], lw=215, ph=100)
b += T(1430, 300, "1 ô sàn = nhiều pallet chồng lên nhau", 32, 800, ORANGE, "middle")
scr("S02", P0, "Bối cảnh: 2 khu trong kho", b,
    ["Mặt bằng chia đôi. Bên trái Khu A: kệ 3 cột × 2 tầng, mỗi ô đặt đúng 1 pallet, 1 ô trống viền xanh nét đứt.",
     "Bên phải Khu B: không kệ, các ô sàn có vạch vàng B-01…B-04, pallet chồng 1–3 tầng hiện lên từng tầng.",
     "Hai câu chú thích “1 vị trí = 1 pallet” / “1 ô sàn = nhiều pallet” bật ra theo phụ đề."],
    ["Kho đông lạnh có hai khu.",
     "Khu A có dãy kệ: mỗi vị trí chứa đúng một pallet.",
     "Khu B không có kệ: pallet được chất chồng lên nhau trên từng ô sàn."],
    "Mã vị trí (A-01-01, B-01…) và số tầng chồng là minh họa; cần chốt theo mặt bằng thực tế.")

# S03 — Hàng hoá & cách xuất
b = floor()
b += T(960, 120, "Hàng hoá và cách xuất", 58, 900, INK, "middle")
b += box(80, 180, 860, 300, "Hàng đồng ký", ["Thùng nào cũng cùng số kg"], GREEN)
for k in range(3):
    b += prop(carton_flat(0, 0, 60, 44, "20 kg"), 140 + k * 150, 330, 2.0)
b += box(980, 180, 860, 300, "Hàng đa ký", ["Mỗi thùng một số kg khác nhau"], PURPLE)
for k, kg in enumerate(["11,6 kg", "12,3 kg", "11,9 kg"]):
    b += prop(carton_flat(0, 0, 60, 44, kg), 1040 + k * 150, 330, 2.0)
b += box(80, 510, 860, 300, "Xuất chẵn pallet", ["Lấy nguyên pallet bằng xe nâng"], BLUE)
b += lift("s03f", 640, 790, 1.5)
b += box(980, 510, 860, 300, "Xuất theo thùng", ["Lấy lẻ số thùng theo đơn"], ORANGE)
b += prop(ms_trolley(), 1480, 790, 1.5) + person("s03p", "picker", 1440, 790, s=1.2, pose=PUSH)
scr("S03", P0, "Hàng thịt đông lạnh: đồng ký / đa ký, xuất chẵn / lẻ", b,
    ["Bốn thẻ hiện theo từng câu phụ đề.",
     "Đồng ký: 3 thùng cùng nhãn “20 kg”. Đa ký: 3 thùng nhãn 11,6 / 12,3 / 11,9 kg, số kg nhảy lệch nhau.",
     "Xuất chẵn pallet: xe nâng chở nguyên pallet. Xuất theo thùng: nhân viên đẩy xe hàng vài thùng."],
    ["Hàng là thịt đông lạnh, gồm hàng đồng ký và hàng đa ký.",
     "Đồng ký: thùng nào cũng cùng số kg. Đa ký: mỗi thùng một số kg khác nhau.",
     "Khi xuất, Nhiêu Lộc có thể xuất chẵn pallet hoặc xuất lẻ theo thùng."],
    "Ví dụ kg/thùng là minh họa.")

# S04 — Bản đồ 9 quy trình + vai
b = floor()
b += T(960, 110, "Bộ quy trình kho Nhiêu Lộc", 56, 900, INK, "middle")
groups = [("Thiết lập", ["01A Chủ hàng mới", "01B Giá bán theo ngày"], BLUE),
          ("Nhập", ["02B Nhập hàng – LPN", "+ tem lô QR"], GREEN),
          ("Trong kho", ["03B Khoá / mở lô", "03C Chuyển pallet", "03D Pallet → pallet"], PURPLE),
          ("Xuất", ["04C Xuất theo đơn", "tính theo kg"], ORANGE),
          ("Kiểm kê", ["05B Kiểm kê", "bằng quét mã"], MUTED)]
for i, (g, items, col) in enumerate(groups):
    x = 70 + i * 362
    b += rect(x, 170, 330, 300, "#fff", 18, col, 4) + rect(x, 170, 330, 62, col, 18) + rect(x, 210, 330, 22, col, 0)
    b += T(x + 165, 213, g, 32, 900, "#fff", "middle")
    for k, s in enumerate(items):
        b += T(x + 26, 290 + k * 56, s, 26, 700 if s[:2].isdigit() else 600, INK if s[:2].isdigit() else MUTED)
    if i < 4:
        b += arrow(x + 334, 320, x + 358, 320, INK, 4)
b += prop(ms_desk(), 820, 830, 1.3)
b += person("s04m", "manager", 330, s=1.35, pose=MANAGER_HOLD, hand_l=folder_svg(), tag="Quản lý", tag_col="#16478F")
b += person("s04x", "xlct", 770, s=1.35, pose=TYPE, tag="Xử lý chứng từ", tag_col=BLUE)
b += person("s04k", "receiver", 1210, s=1.35, pose=SCAN, hand_r=pda_svg("s04k", laser=True, reach=60), tag="Nhân viên kho", tag_col=GREEN)
for row, keys in enumerate((("wms", "tay"), ("pda", "doc"))):
    x = 1420
    for k in keys:
        c, cw = chip(x, 640 + row * 70, k)
        b += c
        x += cw + 14
b += T(1420, 590, "Nhãn ở mỗi bước:", 28, 800)
scr("S04", P0, "Bản đồ 9 quy trình và 3 vai", b,
    ["5 nhóm quy trình hiện từ trái sang phải, nối bằng mũi tên (đi theo vòng đời hàng hoá).",
     "Ba vai đứng dưới: Quản lý (bìa hồ sơ), Xử lý chứng từ (máy tính), Nhân viên kho (quét mã bằng PDA).",
     "Góc phải: 4 nhãn sẽ gắn cạnh mỗi bước – WMS, Thủ công, Quét mã, Chứng từ (theo chú giải của bộ quy trình)."],
    ["Bộ quy trình gồm chín quy trình, chia thành năm nhóm.",
     "Ba vai tham gia: quản lý, nhân viên xử lý chứng từ và nhân viên kho.",
     "Nhãn cạnh mỗi bước cho biết bước đó làm trên WMS, làm tay hay quét mã."],
    "Chú giải drawio còn có “Thao tác trên ERP”, nhưng không bước nào dùng tới nên không đưa vào.")

# S05 — Thẻ chương 1
screen_def("S05", P1, "Thẻ chương Phần 1", frame(chapter5(1, ["Thiết lập", "dữ liệu"], CH, 0)),
           ["Nửa trái xanh, tên phần to màu trắng; mục lục 5 phần bên phải, mục 1 sáng.", "Tiếng whoosh, giữ 2–3 giây."],
           [], "Không có phụ đề trên thẻ chương.")

# S06 — 01A
b = floor() + code_badge("01A", "Tạo chủ hàng Nhiêu Lộc", ["wms"])
b += person("s06m", "manager", 100, s=1.6, pose=POINT_R, tag="Quản lý", tag_col="#16478F")
b += prop(ms_desk(), 350, 830, 1.6) + person("s06x", "xlct", 300, s=1.6, pose=TYPE)
b += wms_win(640, 160, 1220, "Mã hàng · Chủ hàng NHIÊU LỘC", ["Mã hàng", "Tên hàng", "Loại", "Kg/thùng", "Thùng/pallet"],
             [["NL-BC01", "Ba chỉ heo", "Đồng ký", "20", "40"], ["NL-DG02", "Đùi gà", "Đa ký", "12 (chuẩn)", "50"],
              ["NL-BO03", "Thăn bò", "Đồng ký", "10", "60"]], [190, 300, 210, 250, 230], hl=1)
b += rect(640, 640, 1220, 150, "#fff", 18, INK, 3) + T(670, 690, "Quy tắc:", 30, 800)
for i, (s, col) in enumerate([("Nhận hàng", GREEN), ("Cất hàng: khu đông lạnh", BLUE), ("Tìm tồn: FEFO", ORANGE)]):
    b += pill([900, 1250, 1640][i], 750, s, col, "#fff", 26)
scr("S06", P1, "01A Tạo chủ hàng mới và dữ liệu gốc", b,
    ["Quản lý chỉ tay giao việc, XLCT gõ máy; cửa sổ WMS hiện danh mục mã hàng của Nhiêu Lộc từng dòng.",
     "Dòng “Đùi gà · Đa ký · 12 (chuẩn)” viền cam: hàng đa ký chỉ có kg chuẩn để quy đổi.",
     "Ba chip quy tắc bật lần lượt: Nhận hàng, Cất hàng khu đông lạnh, Tìm tồn FEFO."],
    ["Đầu tiên, tạo chủ hàng Nhiêu Lộc và dữ liệu gốc trên WMS.",
     "Mỗi mã hàng có quy cách thùng, pallet, và là hàng đồng ký hay đa ký.",
     "Sau đó khai báo quy tắc nhận hàng, cất hàng và tìm tồn theo FEFO."],
    "Mã hàng, tên hàng, kg/thùng, thùng/pallet là minh họa. 01A còn có nhóm loại hàng, khách hàng / nơi giao, nhà cung cấp "
    "(nhắc bằng hình, không đọc hết).")

# S07 — 01B
b = floor() + code_badge("01B", "Khai báo giá bán theo ngày", ["tay", "wms"])
b += person("s07m", "manager", 170, s=1.7, pose=MANAGER_HOLD, hand_l=folder_svg(), tag="Quản lý", tag_col="#16478F")
b += doc(300, 190, 460, "BẢNG GIÁ BÁN", ["Áp dụng: 24/11", "Ba chỉ heo · 98.000 đ/kg", "Đùi gà · 62.000 đ/kg"], sign=False)
b += arrow(780, 330, 870, 330, ORANGE, 7)
b += wms_win(890, 180, 970, "Danh mục giá bán", ["Mã hàng", "Ngày áp dụng", "Đơn giá / kg"],
             [["NL-BC01", "24/11", "98.000 ✔"], ["NL-DG02", "24/11", "62.000 ✔"]], [260, 330, 340], status="Đã lưu")
b += prop(ms_desk(), 1300, 830, 1.5) + person("s07x", "xlct", 1250, s=1.5, pose=TYPE, tag="Xử lý chứng từ", tag_col=BLUE)
scr("S07", P1, "01B Khai báo giá bán theo ngày", b,
    ["Quản lý cầm bìa hồ sơ; tờ “Bảng giá bán” có dấu duyệt bay sang XLCT.",
     "XLCT nhập đơn giá/kg và ngày áp dụng; từng dòng hiện ✔, chip “Đã lưu” bật ra."],
    ["Giá bán của Nhiêu Lộc thay đổi theo ngày.",
     "Quản lý duyệt bảng giá theo kg, XLCT khai báo vào WMS kèm ngày áp dụng."],
    "Đơn giá minh họa.")

# S08 — Thẻ chương 2
screen_def("S08", P2, "Thẻ chương Phần 2", frame(chapter5(2, ["Nhập hàng", "và cất hàng"], CH, 1)),
           ["Cùng khung S05, mục 2 sáng."], [], "Không có phụ đề trên thẻ chương.")

# S09 — 02B B1–2
b = floor() + code_badge("02B · Bước 1–2", "Nhận ASN, nhập WMS, in LPN và tem lô", ["tay", "wms", "doc"])
b += prop(ms_desk(), 260, 830, 1.6) + person("s09x", "xlct", 210, s=1.6, pose=TYPE, tag="Xử lý chứng từ", tag_col=BLUE)
b += mail(560, 180, 520, "Nhiêu Lộc", "Kế hoạch nhập ngày 23/11", "KeHoachNhap_23-11.xlsx")
b += arrow(1095, 300, 1160, 300, ORANGE, 7)
b += wms_win(1170, 170, 690, "ASN-NL-0001 · Chờ hàng", ["Mã hàng", "SL dự kiến"],
             [["NL-BC01", "240 thùng"], ["NL-DG02", "100 thùng"]], [300, 350], status="Đã tạo ASN")
b += printer(620, 700)
b += lpn_tag(860, 580, "LPN-000123") + lpn_tag(860, 660, "LPN-000124") + T(945, 760, "Mã LPN cho pallet", 24, 700, MUTED, "middle")
for k in range(3):
    b += qr(1150 + k * 90, 590, 70)
b += T(1265, 700, "Tem lô QR cho thùng", 24, 700, MUTED, "middle")
b += T(1265, 740, "NL-BC01 · Lô 261120", 24, 800, INK, "middle")
scr("S09", P2, "02B Bước 1–2: ASN, in LPN + tem lô QR", b,
    ["Email từ Nhiêu Lộc bay vào; file Excel trượt vào cửa sổ WMS, tạo ASN-NL-0001 (chip “Đã tạo ASN”).",
     "Máy in nhả ra tem LPN (mã vạch, cho pallet) và tem lô QR (cho thùng); XLCT gom lại giao cho nhân viên kho."],
    ["Bước 1 và 2: Nhiêu Lộc gửi kế hoạch nhập, XLCT xử lý file và nhập vào WMS để tạo ASN.",
     "WMS in sẵn mã LPN cho pallet và tem lô QR cho từng lô hàng."])

# S10 — 02B B3–4
b = floor() + code_badge("02B · Bước 3–4", "Tạo phiếu nhập, dỡ và xếp hàng", ["wms", "tay"])
b += prop(ms_truck(), 20, 830, 1.8) + person("s10d", "driver", 650, s=1.6)
b += pallet(780, 830, lpn="LPN-000123", qrs=True)
b += person("s10k", "receiver", 1050, s=1.7, pose={"armR": (-150, 30)}, hand_r=qr(-8, 10, 26),
            tag="Nhân viên kho", tag_col=GREEN)
b += pda_big(1400, 150, "Tạo phiếu nhập", [("ASN", "ASN-NL-0001", None), ("Số xe", "51D-678.90", "hl"),
                                            ("Tài xế", "Hùng", None)], "Tạo phiếu")
b += rect(760, 180, 560, 200, "#fff", 16, INK, 3) + T(790, 230, "Bước 4 tại cửa nhập:", 28, 800)
for i, s in enumerate(["Kiểm tra ngoại quan", "Dán tem lô QR lên thùng", "Dán LPN lên pallet"]):
    b += check(806, 270 + i * 40, 14) + T(832, 280 + i * 40, s, 25, 600)
scr("S10", P2, "02B Bước 3–4: Tạo phiếu nhập, dỡ / xếp hàng", b,
    ["Xe tải lạnh lùi vào cửa nhập, tài xế bước xuống; PDA phóng to tạo phiếu nhập (số xe, tài xế).",
     "Bước 4: thùng được xếp lên pallet; nhân viên kho dán tem QR lên từng thùng (QR nhỏ bật trên thùng), dán LPN lên pallet.",
     "Thẻ checklist 3 dòng ✔ lần lượt."],
    ["Bước 3: xe đến, tạo phiếu nhập kho với số xe, tài xế.",
     "Bước 4: kiểm tra ngoại quan, xếp hàng lên pallet, dán tem lô lên thùng và dán LPN lên pallet."],
    "Số xe, tên tài xế minh họa. Với hàng đông lạnh có thể bổ sung đo nhiệt độ khi nhận – không có trong 02B, chỉ gợi ý.")

# S11 — 02B B5
b = floor() + code_badge("02B · Bước 5", "Nhận hàng", ["pda"])
b += pallet(420, 830, lpn="LPN-000123", qrs=True, rows=4)
b += person("s11k", "receiver", 200, s=1.9, pose=SCAN, hand_r=pda_svg("s11k", laser=True, reach=90))
b += pda_big(860, 130, "Nhận hàng · ASN-NL-0001", [("Quét LPN", "LPN-000123", "ok"),
                                                   ("Quét tem lô QR", "NL-BC01 · Lô 261120", "ok"),
                                                   ("Số lượng (thùng)", "40", "hl"), ("Pallet đã nhận", "6 / 6", "ok")],
             "Xác nhận hoàn tất", w=520)
b += box(1440, 220, 420, 260, "Tem lô QR cho biết", ["Mã hàng · Số lô", "Hạn sử dụng", "→ WMS xuất theo FEFO"], PURPLE, 28)
scr("S11", P2, "02B Bước 5: Nhận hàng (LPN + tem lô + số thùng)", b,
    ["Tia quét chạm LPN trên pallet (beep) → ô 1 ✔; chạm QR trên thùng (beep) → ô 2 ✔.",
     "Ô số lượng gõ 40 thùng; “Pallet đã nhận” chạy tới 6 / 6 ✔, nút “Xác nhận hoàn tất” sáng.",
     "Thẻ tím bên phải: tem lô mang số lô và hạn dùng → nền cho FEFO lúc xuất."],
    ["Bước 5: quét LPN, quét tem lô QR và nhập số thùng trên pallet.",
     "Nhận đủ các pallet thì xác nhận hoàn tất."],
    "Hạn sử dụng trên tem lô là giả định để giải thích FEFO (01A khai báo tìm tồn FEFO); cần xác nhận nội dung tem.")

# S12 — 02B B6
b = floor() + code_badge("02B · Bước 6", "In và ký phiếu nhập kho", ["wms", "doc"])
b += prop(ms_desk(), 280, 830, 1.6) + person("s12x", "xlct", 230, s=1.6, pose=TYPE)
b += printer(600, 600)
b += doc(830, 170, 540, "PHIẾU NHẬP KHO", ["ASN-NL-0001 · 23/11", "NL-BC01 · Ba chỉ heo · 240 thùng", "NL-DG02 · Đùi gà · 100 thùng"])
b += person("s12d", "driver", 1560, s=1.7, pose=SIGN, hand_l=PAPER, hand_r=PEN)
b += counter(830, 690, "Tồn kho NL-BC01", 0, 240)
scr("S12", P2, "02B Bước 6: In và ký phiếu nhập kho", b,
    ["Máy in đẩy “PHIẾU NHẬP KHO” lên giữa khung; hai chữ ký được vẽ ra, tài xế ký bên phải.",
     "Bộ đếm “Tồn kho NL-BC01: 0 → 240 thùng” nhảy số."],
    ["Bước 6: in phiếu nhập kho và chuyển các bên ký.",
     "Hàng của Nhiêu Lộc đã có trong tồn kho WMS, theo từng lô và từng pallet."])

# S13 — 02B B7 khu A
b = floor() + code_badge("02B · Bước 7", "Cất hàng – Khu A (kệ)", ["pda"])
b += rack_pallets(700, 300, 3, 2, MAIN_RACK, {(0, 0), (1, 0), (2, 0), (0, 1)}, hl={(1, 1): GREEN}, cw=230, lh=260)
b += pill(1045, 255, "WMS gợi ý A-02-02", GREEN, "#fff", 24)
b += lift("s13f", 230, 830, 1.9)
b += arrow(470, 600, 1020, 450, GREEN, 6, True)
b += pda_big(1430, 150, "Cất hàng", [("Quét LPN", "LPN-000123", "ok"), ("Vị trí gợi ý", "A-02-02", "hl"),
                                      ("Quét mã vị trí", "A-02-02", "ok")], "Xác nhận cất hàng")
scr("S13", P2, "02B Bước 7: Cất hàng vào kệ (1 vị trí = 1 pallet)", b,
    ["Xe nâng chở pallet LPN-000123; PDA: quét LPN ✔ → ô “Vị trí gợi ý A-02-02” sáng cam.",
     "Trên kệ, ô A-02-02 viền xanh nét đứt + chip “WMS gợi ý”; xe nâng đi theo mũi tên, nâng pallet vào ô.",
     "Quét mã vị trí (beep) ✔, viền nét đứt thành viền liền."],
    ["Bước 7: quét LPN, WMS gợi ý vị trí cất.",
     "Ở khu kệ, mỗi vị trí nhận đúng một pallet; quét mã vị trí để xác nhận cất hàng."])

# S14 — 02B B7 khu B
b = floor() + code_badge("02B · Bước 7", "Cất hàng – Khu B (chất chồng)", ["pda"])
b += stack_zone(560, 800, [("B-01", 3), ("B-02", 2), ("B-03", 1)], lw=250, ph=110, hl={1: GREEN})
b += pill(935, 330, "Cùng mã · cùng lô", GREEN, "#fff", 24)
b += lift("s14f", 210, 830, 1.9)
b += pda_big(1400, 150, "Cất hàng", [("Quét LPN", "LPN-000130", "ok"), ("Vị trí gợi ý", "B-02", "hl"),
                                      ("Quét mã vị trí", "B-02", "ok")], "Xác nhận cất hàng")
scr("S14", P2, "02B Bước 7: Cất hàng khu chất chồng", b,
    ["Ba ô sàn B-01…B-03 với 3 / 2 / 1 pallet chồng; ô B-02 có khung xanh nét đứt trên đỉnh chồng + chip “Cùng mã · cùng lô”. WMS chỉ gợi ý ô sàn B-02, không quản lý tầng.",
     "Xe nâng đặt pallet lên đỉnh chồng ở B-02; quét mã ô sàn ✔.",
     "Zoom nhẹ vào LPN trên từng pallet trong chồng: pallet nào cũng có mã riêng."],
    ["Ở khu chất chồng, WMS gợi ý ô sàn để chồng các pallet cùng mã hàng, cùng lô.",
     "Mỗi pallet vẫn có LPN riêng, nên luôn biết pallet nào đang nằm ở ô nào."],
    "Quy tắc “chồng cùng mã · cùng lô” và số tầng tối đa là ĐỀ XUẤT (drawio chỉ ghi “Quy tắc cất hàng – khu đông lạnh”). "
    "Lý do: pallet dưới cùng khó lấy, chồng cùng lô thì FEFO không bị chặn. Cần chốt với Nhiêu Lộc.")

# S15 — Thẻ chương 3
screen_def("S15", P3, "Thẻ chương Phần 3", frame(chapter5(3, ["Quản lý", "trong kho"], CH, 2)),
           ["Cùng khung S05, mục 3 sáng."], [], "Không có phụ đề trên thẻ chương.")

# S16 — 03B
b = floor() + code_badge("03B", "Khoá / mở khoá lô", ["wms"])
b += prop(ms_desk(), 260, 830, 1.6) + person("s16x", "xlct", 210, s=1.6, pose=TYPE, tag="Xử lý chứng từ", tag_col=BLUE)
b += wms_win(560, 170, 860, "Tồn kho theo lô · NL-BC01", ["Lô", "LPN", "Trạng thái"],
             [["Lô 261101", "LPN-000088", "Đã khoá ✖"], ["Lô 261120", "LPN-000123", "Sẵn sàng ✔"]], [250, 290, 280], hl=0)
b += pallet(1500, 830, lpn="LPN-000088", dim=True) + lock(1595, 560, 1.6)
b += box(560, 600, 860, 170, "Lô bị khoá", ["không được phân bổ xuất cho tới khi mở khoá"], RED, 30)
scr("S16", P3, "03B Khoá / mở khoá lô", b,
    ["XLCT tìm lô trên WMS; dòng “Lô 261101” đổi sang “Đã khoá” đỏ, ổ khoá đỏ sập xuống trên pallet (pallet mờ đi).",
     "Thẻ đỏ “Lô bị khoá …” hiện ra; cuối màn ổ khoá bật mở, pallet sáng lại để thể hiện mở khoá."],
    ["Khi cần giữ một lô lại, XLCT khoá lô hoặc LPN trên WMS.",
     "Lô bị khoá không được phân bổ xuất cho tới khi mở khoá."],
    "Lý do khoá (chờ kiểm tra chất lượng, khiếu nại…) không có trong 03B – chỉ minh họa. "
    "“Không được phân bổ” là cách hiểu thông thường của trạng thái khoá, cần xác nhận trên WMS.")

# S17 — 03C
b = floor() + code_badge("03C", "Chuyển vị trí pallet", ["pda"])
b += stack_zone(80, 800, [("B-01", 2)], lw=250, ph=110)
b += rack_pallets(1000, 300, 2, 2, [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"]], {(1, 0), (1, 1), (0, 1)},
                  hl={(0, 0): GREEN}, cw=230, lh=260)
b += lift("s17f", 560, 830, 1.8)
b += arrow(250, 500, 1080, 700, GREEN, 6, True)
b += pda_big(1500, 150, "Chuyển vị trí", [("Quét LPN (vị trí cũ B-01)", "LPN-000130", "ok"),
                                          ("Quét vị trí mới", "A-01-01", "ok")], "Xác nhận hoàn tất", w=380)
scr("S17", P3, "03C Chuyển vị trí pallet", b,
    ["Pallet trên cùng ở ô sàn B-01 được xe nâng nhấc ra, đi theo mũi tên xanh nét đứt tới ô kệ A-01-01.",
     "PDA: quét LPN ✔ → quét vị trí mới ✔ → “Xác nhận hoàn tất”."],
    ["Chuyển vị trí pallet: tới vị trí cũ, quét LPN, đưa pallet tới vị trí mới.",
     "Quét mã vị trí mới và xác nhận, WMS cập nhật vị trí ngay."],
    "Ví dụ chuyển từ khu chất chồng lên kệ (để chuẩn bị xuất lẻ) là minh họa; 03C áp dụng cho mọi vị trí.")

# S18 — 03D
b = floor() + code_badge("03D", "Chuyển hàng pallet → pallet", ["pda"])
b += pallet(140, 830, lpn="LPN-000123", rows=3, qrs=True)
b += pallet(760, 830, lpn="LPN-000245", rows=1, qrs=True)
b += person("s18k", "receiver", 560, s=1.8, pose=CARRY, hand_l=CARTON, tag="Nhân viên kho", tag_col=GREEN)
b += arrow(300, 400, 860, 400, ORANGE, 6, True)
b += pda_big(1240, 120, "Pallet → pallet", [("Quét LPN nguồn", "LPN-000123", "ok"), ("Quét tem lô QR", "NL-BC01 · Lô 261120", "ok"),
                                             ("Số thùng cần chuyển", "12", "hl"), ("Quét pallet mới", "LPN-000245", "ok")],
             "Xác nhận hoàn tất", w=560)
scr("S18", P3, "03D Chuyển hàng từ pallet sang pallet", b,
    ["Nhân viên kho bê từng thùng từ pallet LPN-000123 sang pallet mới LPN-000245, theo mũi tên cam.",
     "PDA điền lần lượt: LPN nguồn ✔, tem lô ✔, số thùng 12, pallet mới ✔."],
    ["Chuyển hàng giữa hai pallet: quét LPN nguồn, quét tem lô và nhập số thùng cần chuyển.",
     "Quét mã pallet mới và xác nhận; tồn theo lô trên từng pallet vẫn đúng."])

# S19 — Thẻ chương 4
screen_def("S19", P4, "Thẻ chương Phần 4", frame(chapter5(4, ["Xuất hàng", "theo kg"], CH, 3)),
           ["Cùng khung S05, mục 4 sáng."], [], "Không có phụ đề trên thẻ chương.")

# S20 — 04C B1–2
b = floor() + code_badge("04C · Bước 1–2", "Nhận đơn theo kg, nhập WMS", ["tay", "wms"])
b += prop(ms_desk(), 260, 830, 1.6) + person("s20x", "xlct", 210, s=1.6, pose=TYPE, tag="Xử lý chứng từ", tag_col=BLUE)
b += mail(560, 190, 540, "Nhiêu Lộc", "Đơn đặt hàng 24/11 (kg)", "DonHang_24-11.xlsx")
b += arrow(1115, 310, 1180, 310, ORANGE, 7)
b += wms_win(1190, 180, 670, "SO-NL-0001 · Đơn xuất", ["Mã hàng", "Tên hàng", "Kg đặt"],
             [["NL-BC01", "Ba chỉ heo", "800 kg"], ["NL-DG02", "Đùi gà", "250 kg"]], [200, 250, 180], status="Đã tạo đơn xuất")
b += pill(830, 560, "Đặt hàng tính bằng KG", ORANGE, "#fff", 30)
scr("S20", P4, "04C Bước 1–2: Đơn đặt hàng theo kg", b,
    ["Email đơn hàng từ Nhiêu Lộc bay vào, file trượt vào WMS: đơn SO-NL-0001 hai dòng, cột “Kg đặt” nhấn mạnh.",
     "Chip cam “Đặt hàng tính bằng KG” bật ra."],
    ["Bước 1 và 2: đơn đặt hàng tính theo kg, XLCT nhập vào WMS để tạo đơn xuất."])

# S21 — 04C điều kiện giá
b = floor() + code_badge("04C", "Kiểm tra giá bán", ["wms"])
b += diamond(700, 470, 700, 380, ["Đã có giá bán", "ngày phân bổ?"])
b += arrow(1055, 470, 1330, 470, GREEN, 7) + T(1190, 445, "Có", 32, 900, GREEN, "middle")
b += box(1340, 380, 520, 180, "Bước 3: Phân bổ tồn kho", ["Tiếp tục xuất hàng"], GREEN, 30)
b += arrow(700, 665, 700, 760, RED, 7) + T(735, 725, "Không", 32, 900, RED)
b += rect(450, 760, 500, 66, "#fff", 14, BLUE, 4) + T(700, 805, "Thực hiện 01B", 30, 800, BLUE, "middle")
b += person("s21i", "instructor", 1600, s=1.5, pose=POINT_L)
scr("S21", P4, "04C Điều kiện: đã có giá bán ngày phân bổ?", b,
    ["Ô điều kiện hình thoi vàng ở giữa; nhánh “Có” xanh sang phải tới Bước 3, nhánh “Không” đỏ đi xuống “Thực hiện 01B”.",
     "Giảng viên chỉ tay vào ô điều kiện."],
    ["Trước khi phân bổ, WMS kiểm tra đã có giá bán cho ngày phân bổ chưa.",
     "Chưa có thì khai báo giá theo quy trình 01B rồi mới tiếp tục."])

# S22 — 04C B3 phân bổ
b = floor() + code_badge("04C · Bước 3", "Phân bổ tồn kho", ["wms"])
b += box(60, 170, 880, 330, "Quy đổi kg → thùng", ["Ba chỉ heo (đồng ký): 800 kg ÷ 20 = 40 thùng",
                                                   "Đùi gà (đa ký): 250 kg ÷ 12 = 20,8 → 21 thùng",
                                                   "Làm tròn gần nhất, tối thiểu 1 thùng"], GREEN)
b += box(980, 170, 880, 330, "WMS tự tách (đồng ký và đa ký)", ["Đủ 1 pallet → xuất chẵn pallet",
                                                               "Không đủ 1 pallet → xuất theo thùng",
                                                               "Ba chỉ heo 40 thùng = 1 pallet", "Đùi gà 21 thùng (pallet 50)"], BLUE)
b += pill(1640, 346, "→ CHẴN PALLET", BLUE, "#fff", 20) + pill(1640, 391, "→ THEO THÙNG", ORANGE, "#fff", 20)
b += rect(60, 530, 1300, 270, "#fff", 18, ORANGE, 4) + T(90, 580, "Chọn lô (hôm nay 24/11/2026)", 30, 900, ORANGE)
b += rect(90, 600, 560, 180, "#FFF1DF", 14, ORANGE, 3) + T(112, 645, "Mặc định · FEFO", 27, 900, ORANGE)
b += T(112, 690, "Lô 260601 · HSD 01/06/2027", 25, 800) + T(112, 735, "hết hạn trước → chọn", 25, 700, ORANGE) + check(605, 640, 20)
b += rect(680, 600, 650, 180, "#F1ECFE", 14, PURPLE, 3) + T(702, 645, "Đơn chỉ định · HSD còn lại > 70%", 27, 900, PURPLE)
b += T(702, 690, "Lô 260601 · còn 52%", 25, 800, MUTED) + cross(1040, 682, 17)
b += T(702, 735, "Lô 261105 · còn 95%", 25, 800) + check(1040, 727, 17)
b += box(1400, 530, 460, 270, "Đơn giá", ["theo ngày phân bổ 24/11", "Ba chỉ heo 98.000 đ/kg", "Đùi gà 62.000 đ/kg"], BLUE, 30)
scr("S22", P4, "04C Bước 3: Quy đổi kg → thùng, chẵn pallet / theo thùng, chọn lô, lấy đơn giá", b,
    ["Thẻ quy đổi hiện phép tính từng dòng (số chạy): 800 ÷ 20 = 40; 250 ÷ 12 = 20,8 → 21.",
     "Thẻ xanh “WMS tự tách”: hai quy tắc hiện trước (đủ 1 pallet → chẵn pallet; không đủ → theo thùng), "
     "rồi chip CHẴN PALLET bật cạnh Ba chỉ heo, chip THEO THÙNG bật cạnh Đùi gà.",
     "Thẻ chọn lô: ô trái “Mặc định · FEFO” chọn lô hết hạn trước ✔; ô phải “Đơn chỉ định HSD còn lại > 70%”: "
     "lô 52% bị gạch ✖, lô 95% được chọn ✔. Thẻ đơn giá theo ngày phân bổ bên phải."],
    ["Bước 3: WMS quy đổi kg ra số thùng, làm tròn gần nhất, tối thiểu một thùng.",
     "WMS tự tách: đủ một pallet thì xuất chẵn pallet, không đủ một pallet thì xuất theo thùng, cho cả đồng ký và đa ký.",
     "Lô được chọn theo FEFO mặc định, hoặc theo hạn dùng còn lại tối thiểu mà đơn chỉ định, rồi lấy đơn giá của ngày phân bổ."],
    "Hạn dùng còn lại % = số ngày còn tới HSD ÷ tổng hạn dùng (ví dụ hạn dùng 12 tháng). "
    "Đã chốt với khách: WMS tự tách chẵn pallet / theo thùng theo số thùng/pallet. "
    "Các màn sau dùng lô theo FEFO mặc định. Số liệu, HSD minh họa.")

# S23 — 04C B4–5 chẵn pallet
b = floor() + code_badge("04C · Bước 4–5", "In phiếu lấy hàng · Lấy chẵn pallet", ["doc", "pda"])
b += doc(60, 160, 380, "PHIẾU LẤY HÀNG", ["SO-NL-0001", "B-02 · 1 pallet", "A-01-01 · 21 thùng"], sign=False)
b += stack_zone(520, 800, [("B-02", 3)], lw=250, ph=110)
b += rect(532, 464, 226, 116, "none", 10, GREEN, 5, 'stroke-dasharray="14 9"')
b += rect(532, 684, 226, 116, "none", 10, ORANGE, 5, 'stroke-dasharray="14 9"')
b += pill(645, 432, "Lấy LPN-000130 · cùng lô", GREEN, "#fff", 22)
b += lift("s23f", 1090, 830, 1.9, load=False, flip=True)
b += pda_big(1400, 120, "Lấy hàng · SO-NL-0001", [("Đi tới vị trí", "B-02", "hl"),
                                                   ("WMS gợi ý (dưới cùng, khó lấy)", "LPN-000128", None),
                                                   ("Quét LPN thực lấy", "LPN-000130", "ok"),
                                                   ("Cùng mã · cùng lô 261120?", "Hợp lệ · 40 thùng", "ok")],
             "→ Khu chờ xuất", w=470)
scr("S23", P4, "04C Bước 4–5: Lấy chẵn pallet, được đổi pallet cùng lô", b,
    ["Phiếu lấy hàng in ra (góc trái) và được giao cho nhân viên kho.",
     "Xe nâng tới ô B-02; WMS gợi ý LPN-000128 nằm dưới cùng (viền cam nét đứt, khó lấy).",
     "Tài xế xe nâng lấy pallet trên cùng LPN-000130 (viền xanh), quét LPN; WMS kiểm tra cùng mã, cùng lô → “Hợp lệ” ✔, "
     "ghi nhận nguyên pallet 40 thùng. Xe nâng nhấc pallet, quay đầu ra khu chờ xuất."],
    ["Bước 4: in phiếu lấy hàng, giao cho nhân viên kho.",
     "Bước 5, chẵn pallet: nếu pallet được gợi ý khó lấy, xe nâng lấy pallet khác cùng lô cho thuận tiện.",
     "Quét LPN thực lấy, WMS kiểm tra đúng mã, đúng lô rồi ghi nhận nguyên pallet."],
    "Đã chốt: WMS cho phép thay LPN khác cùng mã, cùng lô khi lấy chẵn pallet. "
    "04C gốc ghi quét vị trí → tem lô → số thùng; bước quét LPN nguyên pallet bổ sung theo góp ý.")

# S24 — 04C B5 theo thùng
b = floor() + code_badge("04C · Bước 5", "Lấy hàng theo thùng", ["pda"])
b += rack_pallets(120, 300, 2, 2, [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"]],
                  {(0, 0): {"rows": 2, "lpn": "LPN-000140"}, (1, 0): None, (0, 1): None, (1, 1): None}, hl={(0, 0): ORANGE}, cw=240, lh=260)
b += prop(ms_trolley(), 700, 830, 1.6) + person("s24p", "picker", 660, s=1.8, pose=SCAN,
                                                hand_r=pda_svg("s24p", laser=True, reach=80), tag="Nhân viên kho", tag_col="#B88C00")
b += pda_big(1220, 120, "Lấy hàng · SO-NL-0001", [("Đi tới vị trí", "A-01-01", "hl"), ("Quét vị trí", "A-01-01", "ok"),
                                                   ("Quét LPN (lấy từ pallet nào)", "LPN-000140", "ok"),
                                                   ("Quét tem lô QR", "NL-DG02 · Lô 260601", "ok"), ("Số lượng (thùng)", "21 / 21", "ok")],
             w=520)
b += pill(880, 230, "→ Khu chờ xuất", ORANGE, "#fff", 26)
scr("S24", P4, "04C Bước 5: Lấy hàng theo thùng", b,
    ["PDA hiện “Đi tới vị trí A-01-01”; nhân viên kéo xe hàng tới ô kệ viền cam.",
     "Quét vị trí ✔ → quét LPN trên pallet ✔ (WMS biết lấy từ pallet nào) → quét tem lô QR trên thùng ✔ → số thùng chạy tới 21 / 21 ✔; pallet trên kệ thấp xuống.",
     "Chip “→ Khu chờ xuất”, nhân viên kéo xe ra khỏi khung."],
    ["Bước 5, lẻ thùng: tới vị trí theo phiếu, quét vị trí, quét LPN, quét tem lô và nhập số thùng.",
     "Quét LPN để WMS biết thùng được lấy từ pallet nào.",
     "Lấy xong, đưa hàng ra khu chờ xuất."],
    "Bước quét LPN khi lấy theo thùng được bổ sung theo góp ý; 04C gốc chỉ ghi quét vị trí → tem lô → số thùng.")

# S25 — 04C B6–7 xác nhận ra kho
b = floor() + code_badge("04C · Bước 6–7", "Xác nhận ra kho", ["pda", "can"])
b += box(60, 170, 620, 330, "Đồng ký · Ba chỉ heo", ["Quét tem lô QR ✔", "Xác nhận 40 thùng", "Kg = 40 × 20 = 800 kg"], GREEN)
b += check(620, 230, 26)
b += scale_svg(720, 830, "11,8 kg") + prop(carton_flat(0, 0, 60, 44, "DG02"), 770, 696, 2.4)
b += person("s25c", "checker", 1110, s=1.8, pose=SCAN, hand_r=pda_svg("s25c", laser=True, reach=70), tag="Nhân viên kho", tag_col=PURPLE)
b += pda_big(1300, 110, "Ra kho · Đùi gà (đa ký)", [("Quét tem lô QR", "NL-DG02 · Lô 260601", "ok"),
                                                     ("Kg thùng 7 / 21", "11,8", "hl"), ("Tổng kg đã nhập", "82,9 kg", None)],
             "Xác nhận", w=560)
b += diamond(370, 690, 560, 220, ["Số thùng nhập kg", "= số thùng đã lấy?"])
scr("S25", P4, "04C Bước 6–7: Xác nhận ra kho – đồng ký / đa ký", b,
    ["Trái: thẻ đồng ký – quét tem lô, xác nhận 40 thùng, WMS tự tính 800 kg ✔.",
     "Giữa–phải: thùng đùi gà đặt lên cân, màn cân hiện 11,8 kg; nhân viên nhập vào PDA, bộ đếm thùng 7 / 21 tăng dần, tổng kg cộng dồn.",
     "Ô điều kiện “Số thùng nhập kg = số thùng đã lấy?”: Chưa → cân tiếp (mũi tên vòng), Đủ → Bước 8."],
    ["Bước 6 và 7: xác nhận ra kho.",
     "Hàng đồng ký: quét tem lô, xác nhận số thùng, WMS tự tính số kg.",
     "Hàng đa ký: nhập số kg từng thùng cho tới khi đủ số thùng đã lấy."],
    "04C ghi “nhập số kg cho từng thùng”; việc cân từng thùng là thao tác thủ công giả định (nhãn CÂN). Số kg minh họa.")

# S26 — 04C B8 hoàn tất
b = floor() + code_badge("04C · Bước 8", "Hoàn tất, in phiếu xuất kho / giao hàng", ["wms", "doc"])
b += doc(60, 160, 900, "PHIẾU XUẤT KHO / GIAO HÀNG", ["SO-NL-0001 · Ngày 24/11",
                                                     "Ba chỉ heo · 800 kg × 98.000 = 78.400.000 đ",
                                                     "Đùi gà · 248,6 kg × 62.000 = 15.413.200 đ",
                                                     "Tổng cộng: 93.813.200 đ"])
b += prop(ms_truck(), 1100, 830, 1.8) + pallet(1250, 690, cols=2, rows=2, cw=50, ch=38)
b += person("s26d", "driver", 1050, s=1.7, pose=SIGN, hand_l=PAPER, hand_r=PEN)
b += box(60, 700, 900, 110, "Thành tiền = kg thực xuất × đơn giá", (), BLUE, 30)
scr("S26", P4, "04C Bước 8: Tổng kg, thành tiền, ký phiếu", b,
    ["WMS cộng kg thực xuất theo mã hàng; phép nhân kg × đơn giá chạy số trên tờ phiếu, dòng tổng in đậm.",
     "Phiếu in ra, tài xế ký; hàng trượt lên xe lạnh, xe chạy ra khỏi khung."],
    ["Bước 8: WMS tổng hợp kg thực xuất và tính thành tiền bằng kg nhân đơn giá.",
     "In phiếu xuất kho, phiếu giao hàng để các bên ký."],
    "Đùi gà 21 thùng = 248,6 kg (tổng kg cân, minh họa). Xếp hàng lên xe chỉ là hình minh họa, không có trong 04C.")

# S27 — Thẻ chương 5
screen_def("S27", P5, "Thẻ chương Phần 5", frame(chapter5(5, ["Kiểm kê"], CH, 4)),
           ["Cùng khung S05, mục 5 sáng."], [], "Không có phụ đề trên thẻ chương.")

# S28 — 05B B1–2
b = floor() + code_badge("05B · Bước 1–2", "Tạo phiên kiểm kê, đếm hàng", ["wms", "pda"])
b += prop(ms_desk(), 200, 830, 1.4) + person("s28x", "xlct", 160, s=1.4, pose=TYPE, tag="Xử lý chứng từ", tag_col=BLUE)
b += stack_zone(520, 800, [("B-02", 3)], lw=250, ph=110)
b += person("s28k", "receiver", 860, s=1.8, pose=SCAN, hand_r=pda_svg("s28k", laser=True, reach=80), tag="Nhân viên kho", tag_col=GREEN)
b += pda_big(1220, 110, "Kiểm kê · KK-2411-01", [("Quét vị trí", "B-02", "ok"), ("Quét LPN", "LPN-000131", "ok"),
                                                 ("Quét tem lô QR", "NL-BC01 · Lô 261120", "ok"), ("Số lượng (thùng)", "38", "hl")],
             w=560)
scr("S28", P5, "05B Bước 1–2: Tạo phiên kiểm kê, đếm hàng", b,
    ["XLCT chọn điều kiện (khu, mã hàng…) và tạo phiên kiểm kê trên WMS.",
     "Nhân viên kho tới ô B-02, quét lần lượt vị trí, LPN, tem lô, nhập số thùng đếm được (38)."],
    ["Bước 1: XLCT chọn điều kiện và tạo phiên kiểm kê.",
     "Bước 2: nhân viên kho tới vị trí, quét vị trí, LPN, tem lô và nhập số thùng đếm được."])

# S29 — 05B B3–5
b = floor() + code_badge("05B · Bước 3–5", "Báo cáo chênh lệch, đếm lại, điều chỉnh", ["wms"])
b += wms_win(60, 170, 1000, "Báo cáo chênh lệch · KK-2411-01", ["Vị trí", "LPN", "Hệ thống", "Đếm", "Lệch"],
             [["B-02", "LPN-000131", "40", "38", "−2 ✖"], ["A-01-01", "LPN-000140", "50", "50", "0 ✔"]],
             [170, 280, 190, 150, 170], hl=0)
b += person("s29m", "manager", 260, s=1.5, pose=MANAGER_HOLD, hand_l=folder_svg(), tag="Quản lý kho", tag_col="#16478F")
b += diamond(1440, 360, 620, 260, ["Cần đếm lại", "vị trí chênh lệch?"])
b += arrow(1440, 495, 1440, 560, ORANGE, 7) + T(1470, 540, "Có", 30, 900, ORANGE)
b += box(1180, 565, 520, 110, "Đếm lần 2, lần 3", (), ORANGE, 30)
b += arrow(1135, 360, 1060, 600, GREEN, 7) + T(1050, 500, "Không", 30, 900, GREEN, "end")
b += box(560, 600, 480, 110, "Điều chỉnh tồn kho", (), GREEN, 30)
scr("S29", P5, "05B Bước 3–5: Chênh lệch → đếm lại hoặc điều chỉnh", b,
    ["WMS tự tạo báo cáo; dòng B-02 lệch −2 viền cam, dòng A-01-01 khớp ✔.",
     "Quản lý kho xem báo cáo; ô điều kiện: Có → “Đếm lần 2, lần 3” (vòng lại bước đếm), Không → “Điều chỉnh tồn kho”."],
    ["Bước 3: WMS tự tạo báo cáo chênh lệch.",
     "Quản lý kho quyết định đếm lại lần 2, lần 3, hay tiến hành điều chỉnh tồn kho."])

# S30 — Kết
b = floor()
b += T(90, 150, "Nhiêu Lộc nhận được gì?", 60, 900) + logo(1450, 60, 400, card=False)
ben = [("Tồn kho theo lô, hạn dùng", "Xuất đúng FEFO, khoá lô khi cần", GREEN),
       ("Biết từng pallet ở đâu", "Cả khu kệ lẫn khu chất chồng", BLUE),
       ("Xuất theo kg chính xác", "Chẵn pallet hay lẻ thùng, có thành tiền", ORANGE),
       ("Kiểm kê bằng quét mã", "Chênh lệch có báo cáo ngay", PURPLE)]
for i, (t, s, col) in enumerate(ben):
    x, y = 90 + (i % 2) * 740, 210 + (i // 2) * 290
    b += rect(x, y, 710, 250, "#fff", 22, col, 5) + check(x + 70, y + 80, 34)
    b += T(x + 130, y + 95, t, 36, 900) + T(x + 130, y + 150, s, 27, 600, MUTED)
b += person("s30i", "instructor", 1680, s=2.0, pose=RAISE)
scr("S30", PE, "Kết: 4 điểm chính cho Nhiêu Lộc", b,
    ["4 thẻ lợi ích bật lần lượt, mỗi thẻ ✔ xanh.",
     "Logo TKSolution ở góc trên phải. Giảng viên giơ tay chào kết; khung cuối giữ 2 giây."],
    ["Mọi pallet và mọi thùng của Nhiêu Lộc đều được quét và ghi nhận trên WMS.",
     "Biết hàng nào, lô nào, nằm ở đâu, và đã giao bao nhiêu kg.",
     "Xin cảm ơn Ban lãnh đạo đã theo dõi."], mark=False, minimum=4.0)


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
page = page.replace("<title>Storyboard Hành trình kỹ năng</title>", "<title>Storyboard Nhiêu Lộc</title>")
page = page.replace('<p class="kicker">Storyboard · bản 2</p>',
                    f'<img src="{LOGO_URI}" alt="TKSolution" style="height:44px;display:block;margin-bottom:12px">'
                    '<p class="kicker">Storyboard · bản 2 · Khách hàng Công ty Nhiêu Lộc</p>')
page = page.replace("<h1>Hành trình tạo kỹ năng làm video theo ý tôi</h1>",
                    "<h1>Vận hành kho lạnh cho Nhiêu Lộc – video demo đề xuất</h1>")
page = page.replace(
    "{{COUNT}} màn cho video khoảng 3 phút, dựng theo mục [B1] của prompt. Mỗi khung là ảnh tĩnh của khoảnh khắc chính, "
    "đúng màu, font và nhân vật của các video kho; ảnh trong khung màn hình là ảnh thật trích từ các bản render.",
    f"{{{{COUNT}}}} màn, khoảng {mmss(TOTAL)} (nhịp đọc phụ đề 1.3×), dành cho cấp quản lý của Nhiêu Lộc. "
    "Nội dung bám bộ quy trình <b>Nhiêu Lộc – Bộ quy trình kho</b>: 01A, 01B, 02B, 03B, 03C, 03D, 04C, 05B; "
    "bối cảnh kho đông lạnh 2 khu (kệ pallet và chất chồng), hàng đồng ký / đa ký, xuất chẵn pallet và theo thùng. "
    "Ô ghi chú vàng ở từng màn đánh dấu chỗ là minh họa hoặc đề xuất, chưa có trong quy trình gốc.")
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
