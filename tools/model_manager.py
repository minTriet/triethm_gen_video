"""Model sheet for the new 'Quản lý kho' role (CXAD video).  Run: python3 tools/model_manager.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, ROLE, font_css, stick, folder_svg, MANAGER_HOLD, TYPE
from model_sheet import desk, cell_html

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "design")
INK = C["ink"]
NAVY = ROLE["manager"][0]


def report_desk():
    """Desk with a WMS discrepancy report on screen."""
    return (desk()
            + f'<rect x="86" y="-122" width="62" height="40" rx="3" fill="#fff"/>'
            f'<text x="117" y="-111" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="8" fill="{INK}">THIẾU / THỪA</text>'
            f'<rect x="92" y="-105" width="22" height="6" fill="{C["red"]}"/><rect x="118" y="-105" width="24" height="6" fill="#E3E8EF"/>'
            f'<rect x="92" y="-96" width="22" height="6" fill="{C["orange"]}"/><rect x="118" y="-96" width="24" height="6" fill="#E3E8EF"/>')


def task_cards():
    return (f'<g transform="translate(70,-170)">'
            f'<rect x="0" y="0" width="190" height="44" rx="10" fill="#fff" stroke="{C["red"]}" stroke-width="3"/>'
            f'<text x="95" y="28" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="17" fill="{INK}">Thiếu → lấy bổ sung</text>'
            f'<rect x="0" y="56" width="190" height="44" rx="10" fill="#fff" stroke="{C["orange"]}" stroke-width="3"/>'
            f'<text x="95" y="84" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="17" fill="{INK}">Thừa → trả về vị trí</text></g>')


CELLS = [
    ("Đứng chuẩn", "Mũ bảo hộ trắng · sơ mi trắng · cà vạt xanh đậm",
     stick("q1", "manager", 1.0), 0),
    ("Cầm bìa hồ sơ", "Dấu hiệu nhận ra vai quản lý",
     stick("q2", "manager", 1.0, pose=MANAGER_HOLD, hand_l=folder_svg()), 0),
    ("Xem báo cáo trên WMS", "Bước 3 – Xử lý chênh lệch (04K.2)",
     stick("q3", "manager", 1.0, pose=TYPE)
     + report_desk(), -40),
    ("Chỉ tay giao việc", "Hướng dẫn xử lý thiếu / thừa",
     stick("q4", "manager", 1.0, pose={"armR": (-128, 10)}) + task_cards(), -100),
]

LINEUP = [("planner", "Nhân viên XLCT"), ("manager", "Quản lý kho"), ("instructor", "Giảng viên"),
          ("receiver", "Nhận hàng"), ("forklift", "Xe nâng"), ("picker", "Picker"),
          ("checker", "Checker"), ("transport", "Tài xế")]


def build():
    W, H = 450, 440
    cells = ""
    for i, (t, note, svg, fx) in enumerate(CELLS):
        cells += cell_html(60 + i * (W + 10), 128, W, H, t, NAVY, note, svg, fx)
    line = ""
    for j, (role, name) in enumerate(LINEUP):
        hl = "outline:4px solid " + NAVY + ";" if role == "manager" else ""
        line += (f'<div class="lu" style="left:{j*220}px;{hl}"><svg width="200" height="230" viewBox="-100 -200 200 230">'
                 f'<line x1="-90" y1="4" x2="90" y2="4" stroke="{C["floor_line"]}" stroke-width="3"/>'
                 f'{stick("l"+str(j), role, 1.1)}</svg><div class="ln">{name}</div></div>')
    html = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>
{font_css('../tap-1-tong-quan/assets/fonts/')}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1920px;height:1080px;background:{C['ground']};font-family:{FONT};color:{INK};position:relative;overflow:hidden}}
h1{{position:absolute;left:60px;top:20px;font-size:44px;font-weight:900}}
h1 span{{color:{NAVY}}}
.sub{{position:absolute;left:62px;top:76px;font-size:23px;font-weight:500;color:{C['muted']}}}
.cell{{position:absolute;background:#fff;border:3px solid #E3E8EF;border-radius:22px;overflow:hidden}}
.cap{{position:absolute;left:24px;bottom:18px;right:20px;font-size:28px}}
.cap .note{{font-size:21px;font-weight:500;color:{C['muted']};margin-top:4px}}
.chip{{display:inline-block;width:22px;height:22px;border-radius:6px;border:2.5px solid {INK};margin-right:10px;vertical-align:-3px}}
.strip{{position:absolute;left:60px;top:600px;width:1800px;height:440px;background:#fff;border:3px solid #E3E8EF;border-radius:22px}}
.strip h2{{position:absolute;left:24px;top:16px;font-size:28px;font-weight:900}}
.strip h2 small{{font-size:21px;font-weight:500;color:{C['muted']}}}
.row{{position:absolute;left:20px;top:80px}}
.lu{{position:absolute;top:0;width:200px;height:320px;border-radius:16px;text-align:center}}
.ln{{font-size:22px;font-weight:700;margin-top:6px}}
</style></head><body>
<h1>Model nhân vật mới <span>– Quản lý kho</span></h1>
<div class="sub">Gộp "Quản lý" và "Quản lý kho" thành một vai · cùng bộ nét v2 (đầu tròn, mắt chấm, thân nét đen)</div>
{cells}
<div class="strip"><h2>Đứng cạnh các vai khác <small>– kiểm tra dễ phân biệt</small></h2><div class="row">{line}</div></div>
</body></html>'''
    p = os.path.join(OUT, "model-quan-ly.html")
    open(p, "w", encoding="utf-8").write(html)
    return p


if __name__ == "__main__":
    print(build())
