"""Approval sheet: XLCT seated at the computer, hands raised.  Run: python3 tools/model_xlct.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, ROLE, font_css, stick, TYPE
from model_sheet import desk, cell_html
from parts import desk_svg

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "design")
INK = C["ink"]
BLUE = ROLE["xlct"][0]
OLD = {"armL": (22, -70), "armR": (-22, 70)}


def sheet_desk(fid, pose, dy):
    return f'<g transform="translate(0,{dy})">{stick(fid, "xlct", 1.0, pose=pose)}</g>' + desk()


def video_desk(fid, pose):
    """Same layout as the videos (desk_svg + figure at FY-40, scale 1.5), drawn at 1/1.5."""
    return (f'<g transform="scale({1/1.5:.4f})">{desk_svg(0, 0)}'
            f'<g transform="translate(0,-40)">{stick(fid, "xlct", 1.5, pose=pose)}</g></g>')


R = TYPE["armR"]
CELLS = [
    ("Cũ – trên bảng model", "Tay khuất sau mặt bàn", sheet_desk("o1", OLD, 16), -40),
    ("Mới – trên bảng model", "Tay đặt lên bàn phím", sheet_desk("n1", TYPE, 0), -40),
    ("Cũ – trong video", "Tay sát bụng, thấp", video_desk("o2", OLD), -30),
    ("Mới – trong video", "Tay nâng lên ngang ngực", video_desk("n2", TYPE), -30),
]
TYPING = [("Gõ phím 1", {"armL": TYPE["armL"], "armR": (R[0], 110)}),
          ("Gõ phím 2", {"armL": TYPE["armL"], "armR": (R[0], 132)})]


def build():
    W, H = 450, 440
    cells = "".join(cell_html(60 + i * (W + 10), 128, W, H, t, BLUE if i % 2 else "#C9D3E0", n, svg, fx)
                    for i, (t, n, svg, fx) in enumerate(CELLS))
    typ = ""
    for j, (t, pose) in enumerate(TYPING):
        typ += (f'<div class="lu" style="left:{40 + j*420}px"><svg width="400" height="300" viewBox="-160 -230 400 260">'
                f'{video_desk("t" + str(j), pose)}</svg><div class="ln">{t}</div></div>')
    html = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>
{font_css('../tap-1-tong-quan/assets/fonts/')}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1920px;height:1080px;background:{C['ground']};font-family:{FONT};color:{INK};position:relative;overflow:hidden}}
h1{{position:absolute;left:60px;top:20px;font-size:44px;font-weight:900}}
h1 span{{color:{BLUE}}}
.sub{{position:absolute;left:62px;top:76px;font-size:23px;font-weight:500;color:{C['muted']}}}
.cell{{position:absolute;background:#fff;border:3px solid #E3E8EF;border-radius:22px;overflow:hidden}}
.cap{{position:absolute;left:24px;bottom:18px;right:20px;font-size:28px}}
.cap .note{{font-size:21px;font-weight:500;color:{C['muted']};margin-top:4px}}
.chip{{display:inline-block;width:22px;height:22px;border-radius:6px;border:2.5px solid {INK};margin-right:10px;vertical-align:-3px}}
.strip{{position:absolute;left:60px;top:600px;width:1800px;height:440px;background:#fff;border:3px solid #E3E8EF;border-radius:22px}}
.strip h2{{position:absolute;left:24px;top:16px;font-size:28px;font-weight:900}}
.strip h2 small{{font-size:21px;font-weight:500;color:{C['muted']}}}
.row{{position:absolute;left:20px;top:80px}}
.lu{{position:absolute;top:0;width:400px;text-align:center}}
.ln{{font-size:22px;font-weight:700;margin-top:6px}}
.note2{{position:absolute;left:900px;top:110px;width:860px;font-size:24px;line-height:1.5}}
</style></head><body>
<h1>Nhân viên XLCT <span>– ngồi máy tính, tay nâng cao hơn</span></h1>
<div class="sub">Tư thế gõ máy (TYPE) dùng chung cho XLCT / điều phối trong mọi video · bàn tay tròn giữ nguyên</div>
{cells}
<div class="strip"><h2>Động tác gõ phím <small>– tay phải nhấp lên xuống quanh tư thế mới</small></h2><div class="row">{typ}</div>
<div class="note2">Vai: <b>armL (40, −120)</b> · <b>armR (−40, 120)</b><br>(cũ: 22, −70 / −22, 70)<br>Bàn tay nâng khoảng 17 px theo model (~25 px trên video 1080p), ngang ngực, nằm trên mặt bàn, không còn sát bụng.</div></div>
</body></html>'''
    p = os.path.join(OUT, "model-xlct.html")
    open(p, "w", encoding="utf-8").write(html)
    return p


if __name__ == "__main__":
    print(build())
