"""Character model sheet for approval.  Run: python3 tools/model_sheet.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, ROLE, font_css, stick, pda_svg, SWAY, BOB

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "design")
os.makedirs(OUT, exist_ok=True)
INK = C["ink"]


def carton_flat(x, y, w=60, h=42, label=None):
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2.5"/>'
         f'<rect x="{x + w/2 - 6}" y="{y}" width="12" height="{h}" fill="#F3DDB5"/>')
    if label:
        s += (f'<rect x="{x+6}" y="{y+h/2-9}" width="{w-12}" height="18" rx="3" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
              f'<text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="12" fill="{INK}">{label}</text>')
    return s


def barcode(x, y):
    bars = "".join(f'<rect x="{x + i*3.2}" y="{y}" width="{1.6 if i % 3 else 2.4}" height="16" fill="{INK}"/>' for i in range(8))
    return f'<rect x="{x-4}" y="{y-3}" width="33" height="22" fill="#fff"/>' + bars


def forklift_back():
    return (f'<path d="M-52,-78 L-52,-175 L22,-175 L22,-78" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<rect x="38" y="-185" width="10" height="175" fill="#8FA3BF" stroke="{INK}" stroke-width="2.5"/>'
            f'<line x1="22" y1="-110" x2="-6" y2="-104" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')


def forklift():
    return (f'<g>'
            f'<rect x="-70" y="-78" width="105" height="58" rx="10" fill="#5D7290" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-82" y="-70" width="18" height="42" rx="4" fill="#3E4E66" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="48" y="-22" width="70" height="8" fill="#8FA3BF" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="-66" y="-30" width="32" height="10" fill="{C["orange"]}"/>'
            f'<circle cx="-42" cy="-12" r="16" fill="{INK}"/><circle cx="-42" cy="-12" r="6" fill="#8FA3BF"/>'
            f'<circle cx="16" cy="-12" r="16" fill="{INK}"/><circle cx="16" cy="-12" r="6" fill="#8FA3BF"/>'
            f'</g>')


def forklift_front():
    return f'<rect x="-70" y="-78" width="105" height="40" rx="0" fill="#5D7290"/><rect x="-70" y="-80" width="105" height="6" fill="{INK}" opacity="0.15"/>'


def desk():
    return (f'<rect x="80" y="-128" width="74" height="52" rx="6" fill="#2B3646" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="86" y="-122" width="62" height="40" rx="3" fill="#7FD3FF"/>'
            f'<rect x="92" y="-114" width="36" height="5" fill="#fff"/><rect x="92" y="-104" width="46" height="5" fill="#fff" opacity="0.7"/>'
            f'<rect x="112" y="-76" width="10" height="12" fill="#2B3646"/>'
            f'<rect x="-70" y="-66" width="240" height="14" rx="4" fill="#C9965A" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-60" y="-52" width="12" height="52" fill="#A97A44" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="148" y="-52" width="12" height="52" fill="#A97A44" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="-28" y="-72" width="56" height="7" rx="2" fill="#E3E8EF" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="-48" y="-52" width="196" height="40" fill="#B98A55" stroke="{INK}" stroke-width="2.5"/>')


def trolley():
    return (f'<line x1="56" y1="-96" x2="56" y2="-14" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<line x1="48" y1="-96" x2="64" y2="-96" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="52" y="-22" width="140" height="10" rx="3" fill="#8FA3BF" stroke="{INK}" stroke-width="3"/>'
            + carton_flat(70, -64, 56, 42) + carton_flat(130, -64, 56, 42) + carton_flat(100, -106, 56, 42)
            + f'<rect x="64" y="-14" width="58" height="0" />'
            f'<circle cx="70" cy="-4" r="8" fill="{INK}"/><circle cx="176" cy="-4" r="8" fill="{INK}"/>'
            f'<rect x="138" y="-30" width="0" height="0"/>'
            f'<g><rect x="96" y="-150" width="86" height="30" rx="6" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="139" y="-129" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="17" fill="{INK}">CH-0125</text>'
            f'<line x1="139" y1="-120" x2="139" y2="-106" stroke="{INK}" stroke-width="2"/></g>')


def truck():
    return (f'<rect x="60" y="-160" width="200" height="132" rx="6" fill="#F4F6F9" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="60" y="-160" width="200" height="16" fill="#8C96A3"/>'
            f'<path d="M260,-118 L300,-118 L322,-82 L322,-28 L260,-28 Z" fill="#1F5FBF" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M268,-110 L296,-110 L312,-84 L268,-84 Z" fill="#BFD8F5" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="104" cy="-22" r="18" fill="{INK}"/><circle cx="104" cy="-22" r="7" fill="#8FA3BF"/>'
            f'<circle cx="286" cy="-22" r="18" fill="{INK}"/><circle cx="286" cy="-22" r="7" fill="#8FA3BF"/>')


# ------------------------------------------------------------- cells
CELLS = []  # (title, colour, note, svg, figure_offset_x)

CELLS.append(("Nhân viên nhận hàng", ROLE["receiver"][0], "Áo + mũ xanh lá · bê thùng",
    stick("m1", "receiver", 1.0, pose={"armL": (34, -104), "armR": (-34, 104)})
    + carton_flat(-32, -100, 64, 44, "LPN"), 0))

CELLS.append(("Tài xế xe nâng", ROLE["forklift"][0], "Áo + mũ cam · lái xe nâng",
    forklift_back()
    + f'<g transform="translate(-22,-14)">{stick("m2", "forklift", 1.0, pose={"armR": (-70, -20), "armL": (10, -40)})}</g>'
    + forklift(), 0))

CELLS.append(("Nhân viên điều phối", ROLE["planner"][0], "Áo sơ mi xanh dương · ngồi máy tính",
    f'<g transform="translate(0,16)">{stick("m3", "planner", 1.0, pose={"armL": (22, -70), "armR": (-22, 70)})}</g>'
    + desk(), -40))

CELLS.append(("Picker", ROLE["picker"][0], "Áo + mũ vàng · kéo trolley",
    stick("m4", "picker", 1.0, pose={"armR": (-55, -25)}) + trolley(), -70))

CELLS.append(("Checker", ROLE["checker"][0], "Áo + mũ tím · scan bằng PDA",
    carton_flat(118, -72, 74, 72) + barcode(139, -52)
    + stick("m5", "checker", 1.0, pose={"armR": (-60, -10)}, hand_r=pda_svg("m5", laser=True, reach=82)), -60))

CELLS.append(("Đội vận tải", ROLE["transport"][0], "Áo + mũ xám · bàn giao tại xe tải",
    stick("m6", "transport", 1.0, pose={"armR": (-30, -80)}, hand_r=pda_svg("m6"))
    + f'<g transform="translate(30,0) scale(0.68)">{truck()}</g>', -95))

CELLS.append(("Giảng viên", ROLE["instructor"][0], "Sơ mi xanh, cà vạt cam · dẫn dắt",
    stick("m7", "instructor", 1.0, pose={"armR": (-150, -24)}), 0))

ACTIONS = [
    ("Nghiêng trái", f'<g transform="translate(0,-{BOB}) rotate(-{SWAY})">{stick("a1", "picker", 1.0)}</g><path d="M-30,-40 Q-44,-60 -30,-80" fill="none" stroke="#1F5FBF" stroke-width="3" stroke-linecap="round" opacity="0.6"/>'),
    ("Nghiêng phải", f'<g transform="translate(0,-{BOB}) rotate({SWAY})">{stick("a2", "picker", 1.0)}</g><path d="M30,-40 Q44,-60 30,-80" fill="none" stroke="#1F5FBF" stroke-width="3" stroke-linecap="round" opacity="0.6"/>'),
    ("Chỉ tay", stick("a3", "instructor", 1.0, pose={"armL": (128, -10)})),
    ("Nhấc thùng", stick("a4", "receiver", 1.0, pose={"armL": (150, 20), "armR": (-150, -20)})
        + carton_flat(-32, -202, 64, 44)),
]


def cell_html(x, y, w, h, title, col, note, svg, fx, scale=1.25):
    return f'''
  <div class="cell" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">
    <svg width="{w}" height="{h-96}" viewBox="0 0 {w} {h-96}">
      <line x1="20" y1="{h-120}" x2="{w-20}" y2="{h-120}" stroke="{C['floor_line']}" stroke-width="3"/>
      <g transform="translate({w/2 + fx*scale:.0f},{h-122}) scale({scale})">{svg}</g>
    </svg>
    <div class="cap"><span class="chip" style="background:{col}"></span><b>{title}</b><div class="note">{note}</div></div>
  </div>'''


def build():
    cells = ""
    W, H = 450, 420
    for i, (t, col, note, svg, fx) in enumerate(CELLS):
        r, c = divmod(i, 4)
        cells += cell_html(60 + c * (W + 10), 128 + r * (H + 20), W, H, t, col, note, svg, fx)
    # actions strip in the last cell slot
    act = ""
    for j, (t, svg) in enumerate(ACTIONS):
        act += (f'<div class="act" style="left:{j*110}px"><svg width="110" height="250" viewBox="-55 -240 110 260">{svg}</svg>'
                f'<div class="an">{t}</div></div>')
    cells += (f'<div class="cell" style="left:{60 + 3*(W+10)}px;top:{128 + H + 20}px;width:{W}px;height:{H}px">'
              f'<div style="position:absolute;left:5px;top:20px;width:440px;height:300px">{act}</div>'
              f'<div class="cap"><span class="chip" style="background:#C9D3E0"></span><b>Động tác</b><div class="note">đi = nghiêng trái/phải + nhún nhẹ</div></div></div>')
    html = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>
{font_css('../tap-1-tong-quan/assets/fonts/')}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1920px;height:1080px;background:{C['ground']};font-family:{FONT};color:{INK};position:relative;overflow:hidden}}
h1{{position:absolute;left:60px;top:20px;font-size:44px;font-weight:900}}
h1 span{{color:{C['blue']}}}
.sub{{position:absolute;left:62px;top:76px;font-size:23px;font-weight:500;color:{C['muted']}}}
.cell{{position:absolute;background:#fff;border:3px solid #E3E8EF;border-radius:22px;overflow:hidden}}
.cap{{position:absolute;left:24px;bottom:18px;right:20px;font-size:28px}}
.cap .note{{font-size:21px;font-weight:500;color:{C['muted']};margin-top:4px}}
.chip{{display:inline-block;width:22px;height:22px;border-radius:6px;border:2.5px solid {INK};margin-right:10px;vertical-align:-3px}}
.act{{position:absolute;top:0;width:110px;text-align:center}}
.an{{font-size:19px;font-weight:700;margin-top:2px}}
</style></head><body>
<h1>Model nhân vật <span>– bản duyệt v2</span></h1>
<div class="sub">Đầu tròn · mắt chấm · miệng cười · thân nét đen · áo bảo hộ có sọc phản quang + mũ bảo hộ theo màu vai</div>
{cells}
</body></html>'''
    p = os.path.join(OUT, "model-sheet.html")
    open(p, "w", encoding="utf-8").write(html)
    return p


if __name__ == "__main__":
    print(build())
