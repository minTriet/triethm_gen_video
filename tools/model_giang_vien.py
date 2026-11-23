"""Approval sheet: Giảng viên in the TK uniform polo.  Run: python3 tools/model_giang_vien.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, ROLE, font_css, stick, POLO
from model_sheet import cell_html

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "design")
INK = C["ink"]
GREEN = ROLE["instructor"][0]

CELLS = [
    ("Cận cảnh áo", "Cổ bẻ + tay raglan xanh lá · logo TK ngực trái",
     f'<g transform="translate(0,95) scale(1.75)">{stick("g0", "instructor", 1.0)}</g>'
     f'<rect x="-230" y="-1" width="460" height="140" fill="#fff"/>'
     f'<line x1="-205" y1="0" x2="205" y2="0" stroke="{C["floor_line"]}" stroke-width="3"/>', 0),
    ("Đứng chuẩn", "Thân đen than, bàn tay tròn giữ nguyên", stick("g1", "instructor", 1.0), 0),
    ("Vẫy tay mở đầu", "Giơ tay chào", stick("g2", "instructor", 1.0, pose={"armR": (-150, -24)}), 0),
    ("Chỉ tay giải thích", "Hướng dẫn trên bảng", stick("g3", "instructor", 1.0, pose={"armL": (128, -10)}), 0),
]
LINEUP = [("instructor", "Giảng viên"), ("planner", "Điều phối"), ("manager", "Quản lý kho"),
          ("receiver", "Nhận hàng"), ("forklift", "Xe nâng"), ("picker", "Picker"),
          ("checker", "Checker"), ("transport", "Vận tải")]
SW = [("Thân áo", POLO["body"]), ("Tay + cổ + viền túi", POLO["green"]), ("Chỉ thêu xanh neon", POLO["neon"]), ("Chỉ thêu nâu (TK)", POLO["brown"])]


def build():
    W, H = 450, 440
    cells = "".join(cell_html(60 + i * (W + 10), 128, W, H, t, GREEN, n, svg, fx) for i, (t, n, svg, fx) in enumerate(CELLS))
    line = "".join(f'<div class="lu" style="left:{j*150}px;{"outline:4px solid " + GREEN + ";" if r == "instructor" else ""}">'
                   f'<svg width="140" height="200" viewBox="-70 -175 140 185"><line x1="-60" y1="4" x2="60" y2="4" stroke="{C["floor_line"]}" stroke-width="3"/>'
                   f'{stick("l" + str(j), r, 1.0)}</svg><div class="ln">{name}</div></div>' for j, (r, name) in enumerate(LINEUP))
    sw = "".join(f'<div class="sw"><span style="background:{c}"></span>{t}<small>{c}</small></div>' for t, c in SW)
    html = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>
{font_css('../tap-1-tong-quan/assets/fonts/')}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1920px;height:1080px;background:{C['ground']};font-family:{FONT};color:{INK};position:relative;overflow:hidden}}
h1{{position:absolute;left:60px;top:20px;font-size:44px;font-weight:900}}
h1 span{{color:{GREEN}}}
.sub{{position:absolute;left:62px;top:76px;font-size:23px;font-weight:500;color:{C['muted']}}}
.cell{{position:absolute;background:#fff;border:3px solid #E3E8EF;border-radius:22px;overflow:hidden}}
.cap{{position:absolute;left:24px;bottom:18px;right:20px;font-size:28px}}
.cap .note{{font-size:20px;font-weight:500;color:{C['muted']};margin-top:4px}}
.chip{{display:inline-block;width:22px;height:22px;border-radius:6px;border:2.5px solid {INK};margin-right:10px;vertical-align:-3px}}
.box{{position:absolute;top:600px;height:440px;background:#fff;border:3px solid #E3E8EF;border-radius:22px}}
.box h2{{position:absolute;left:24px;top:16px;font-size:28px;font-weight:900}}
.box h2 small{{font-size:21px;font-weight:500;color:{C['muted']}}}
.lu{{position:absolute;top:0;width:140px;height:250px;border-radius:16px;text-align:center}}
.ln{{font-size:20px;font-weight:700}}
.sw{{font-size:22px;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:14px}}
.sw span{{width:48px;height:48px;border-radius:8px;border:2.5px solid {INK}}}
.sw small{{font-weight:500;color:{C['muted']};margin-left:auto}}
</style></head><body>
<h1>Giảng viên <span>– mặc áo đồng phục TK (polo raglan)</span></h1>
<div class="sub">Thân đen than · tay raglan + cổ bẻ xanh lá · nẹp V không nút · logo TK + túi viền xanh ngực trái · không mũ</div>
{cells}
<div class="box" style="left:60px;width:1250px"><h2>Đứng cạnh các vai khác <small>– kiểm tra dễ phân biệt</small></h2>
<div style="position:absolute;left:20px;top:90px">{line}</div></div>
<div class="box" style="left:1330px;width:530px"><h2>Bảng màu <small>– theo bản vẽ áo</small></h2>
<div style="position:absolute;left:30px;top:90px;right:30px">{sw}<div class="sw" style="font-size:18px;font-weight:500;color:{C['muted']}">Nhân vật luôn quay mặt trước nên chữ in sau lưng / tay áo không hiện.</div></div></div>
</body></html>'''
    p = os.path.join(OUT, "model-giang-vien.html")
    open(p, "w", encoding="utf-8").write(html)
    return p


if __name__ == "__main__":
    print(build())
