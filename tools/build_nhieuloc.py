"""Video demo đề xuất cho Công ty Nhiêu Lộc (kho lạnh, WMS) -> ./video-nhieuloc
Run: python3 tools/build_nhieuloc.py
Storyboard đã duyệt: design/storyboard-nhieu-loc.html (cùng bộ hình tools/nhieuloc_kit.py).
Giọng đọc VieNeu-TTS (skill vieneu-tts, giọng Hải Đăng, seed 7): câu thoại + văn bản đọc trong
source/vo_nhieu_loc.json, clip trong video-nhieuloc/assets/vo/ (manifest.json).
Thời lượng mỗi câu = độ dài clip thật + đệm, không đoán theo số chữ.
Màn S01–S03 ở file này, S04–S30 trong tools/nhieuloc_scenes.py.
Phụ đề thu nhỏ (44 px, cách đáy 40 px) cho khớp vị trí phụ đề trong storyboard đã duyệt.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from nhieuloc_kit import *  # noqa: E402,F401,F403
from kit import walk_js, pose_js, REST  # noqa: E402
from build_full import build_all  # noqa: E402
from build_wms import G, fig, svg, rise, wave_js  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "video-nhieuloc")
GAP, PAD = 0.15, 0.3            # khoảng lặng giữa hai câu · đệm sau mỗi clip
VO_VOL = 1.0

LINES = {d["id"]: d for d in json.load(open(os.path.join(ROOT, "source", "vo_nhieu_loc.json"), encoding="utf-8"))}
MAN = {m["id"]: m for m in json.load(open(os.path.join(OUT, "assets", "vo", "manifest.json"), encoding="utf-8"))}
MARK = logo(1676, 1016, 210)    # logo TKSolution nhỏ ở góc dưới phải


class VScene:
    """Một cảnh có giọng đọc: mỗi câu giữ đúng độ dài clip + PAD."""

    def __init__(self, cid, vo_ids, build, lead=0.4, tail=1.0):
        self.cid, self.build, self.lead, self.tail = cid, build, lead, tail
        self.vo = list(vo_ids)
        self.lines = [LINES[v]["sub"] for v in self.vo]
        self.sfx = []
        t, self.T, self.E = lead, [], []
        for v in self.vo:
            d = MAN[v]["duration"] + PAD
            self.T.append(round(t, 2)); self.E.append(round(t + d, 2))
            t += d + GAP
        self.D = round(t - GAP + tail, 2)


def popc(sel, t, cx, cy, dur=0.4, s0=0.85):
    """Bật ra quanh tâm (cx, cy) trong toạ độ SVG; svgOrigin cố định nên không lệch vị trí sau khi bật."""
    return (f'tl.fromTo("{sel}",{{opacity:0,scale:{s0}}},{{opacity:1,scale:1,duration:{dur},ease:"back.out(1.8)",'
            f'svgOrigin:"{cx} {cy}"}},{t:.2f});\n')


def drop(sel, t, dy=-60, dur=0.4):
    return f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"bounce.out"}},{t:.2f});\n'


def slide_in(sel, t, dx, dur=0.9, ease="power2.out"):
    return f'tl.fromTo("{sel}",{{opacity:0,x:{dx}}},{{opacity:1,x:0,duration:{dur},ease:"{ease}"}},{t:.2f});\n'


def pulse(sel, t, n=3):
    return f'tl.to("{sel}",{{opacity:0.25,duration:0.3,yoyo:true,repeat:{n * 2 - 1},ease:"sine.inOut"}},{t:.2f});\n'


# ============================================================ S01 Tiêu đề
def s01():
    def build(TT, D):
        b = floor() + G("in-logo", logo(110, 40, 400))
        b += G("in-tag", pill(110 + (tw("ĐỀ XUẤT GIẢI PHÁP · BẢN DEMO", 26) + 48) / 2, 190, "ĐỀ XUẤT GIẢI PHÁP · BẢN DEMO", ORANGE, "#fff", 26))
        b += G("in-l1", T(110, 320, "Vận hành kho lạnh", 92, 900)) + G("in-l2", T(110, 430, "cho Nhiêu Lộc", 92, 900, BLUE))
        b += G("in-l3", T(110, 515, "Thịt đông lạnh · Kệ pallet + Chất chồng · WMS", 38, 700, MUTED))
        b += G("in-cold", cold_sign(110, 580))
        b += G("in-rack", rack_pallets(1180, 300, 3, 2, MAIN_RACK, {(0, 0), (1, 0), (2, 0), (0, 1), (2, 1)},
                                       cw=230, lh=260, qrs=True))
        b += fig("in-man", "instructor", 990, s=2.0)
        js = rise("#in-rack", 0.0, dy=30, dur=0.6) + rise("#in-logo", 0.1, dy=-16)
        js += f'tl.fromTo("#in-man-w",{{x:420}},{{x:0,duration:1.2,ease:"power1.out"}},0.2);\n' + walk_js("in-man", 0.2, 1.4)
        js += rise("#in-tag", 0.4, dy=-14) + rise("#in-l1", 0.55) + rise("#in-l2", 0.75)
        js += wave_js("in-man", TT[0])
        js += rise("#in-l3", TT[1]) + popc("#in-cold", TT[1] + 0.8, 225, 620)
        return svg(b), "", js
    s = VScene("s01", ["s01-1", "s01-2"], build, lead=1.4, tail=1.0)
    s.sfx = [(0.2, "whoosh.mp3", 0.15)]
    return s


# ============================================================ S02 Hai khu kho
LANES = [("B-01", 3), ("B-02", 2), ("B-03", 3), ("B-04", 1)]


def s02():
    def build(TT, D):
        b = floor() + G("z-h", T(960, 120, "Kho đông lạnh có 2 khu", 58, 900, INK, "middle")) + G("z-cold", cold_sign(1640, 60, 220))
        b += G("z-pa", rect(40, 170, 900, 610, "#fff", 24, BLUE, 4, 'opacity="0.55"') + pill(240, 212, "KHU A · CÓ DÃY KỆ", BLUE, "#fff", 24))
        b += G("z-pb", rect(980, 170, 900, 610, "#fff", 24, ORANGE, 4, 'opacity="0.55"') + pill(1180, 212, "KHU B · CHẤT CHỒNG", ORANGE, "#fff", 24))
        b += G("z-rack", rack_pallets(130, 296, 3, 2, MAIN_RACK, {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)}, cw=240, lh=230))
        b += G("z-hl", rect(130 + 2 * 240 + 6, 296 + 6, 228, 212, "none", 10, GREEN, 5, 'stroke-dasharray="14 9"'))
        b += G("z-ta", T(490, 270, "1 vị trí = 1 pallet", 28, 800, BLUE, "middle"))
        lw, ph, base, x0 = 215, 100, 726, 1000
        floor_marks = ""
        for i, (lab, n) in enumerate(LANES):
            xx = x0 + i * lw
            floor_marks += rect(xx + 8, base - 3, lw - 16, 8, "#FFD84D", 2, INK, 1.5)
            floor_marks += rect(xx + lw / 2 - 52, base + 18, 104, 34, "#FFE34D", 4, INK, 2) + T(xx + lw / 2, base + 44, lab, 22, 900, INK, "middle")
        b += G("z-fl", floor_marks)
        for k in range(3):
            tier = "".join(pallet(x0 + i * lw + (lw - 190) / 2, base - k * ph, rows=2) for i, (_, n) in enumerate(LANES) if n > k)
            b += G(f"z-t{k}", tier)
        b += G("z-tb", T(1430, 270, "1 ô sàn = nhiều pallet chồng lên nhau", 28, 800, ORANGE, "middle"))
        b += MARK
        js = rise("#z-h", 0.0) + popc("#z-cold", 0.3, 1750, 100)
        js += rise("#z-pa", TT[0] + 0.2) + rise("#z-pb", TT[0] + 0.5)
        js += rise("#z-rack", TT[1], dy=30, dur=0.5) + rise("#z-ta", TT[1] + 0.9, dy=12)
        js += f'tl.set("#z-hl",{{opacity:0}},0);\n' + f'tl.to("#z-hl",{{opacity:1,duration:0.2}},{TT[1] + 1.4:.2f});\n' + pulse("#z-hl", TT[1] + 1.6, 2)
        js += rise("#z-fl", TT[2], dy=10, dur=0.3)
        for k in range(3):
            js += drop(f"#z-t{k}", TT[2] + 0.4 + k * 0.6)
        js += rise("#z-tb", TT[2] + 2.3, dy=12)
        return svg(b), "", js
    s = VScene("s02", ["s02-1", "s02-2", "s02-3"], build, lead=0.6, tail=1.2)
    s.sfx = [(("T", 2, 0.5), "click-soft.mp3", 0.15)]
    return s


# ============================================================ S03 Hàng hoá & cách xuất
def s03():
    def build(TT, D):
        b = floor() + G("g-h", T(960, 120, "Hàng hoá và cách xuất", 58, 900, INK, "middle"))
        b += G("g-c1", box(80, 180, 860, 300, "Hàng đồng ký", ["Thùng nào cũng cùng số kg"], GREEN))
        b += G("g-c2", box(980, 180, 860, 300, "Hàng đa ký", ["Mỗi thùng một số kg khác nhau"], PURPLE))
        for k in range(3):
            b += G(f"g-a{k}", prop(carton_flat(0, 0, 60, 44, "20 kg"), 140 + k * 150, 330, 2.0))
        for k, kg in enumerate(["11,6 kg", "12,3 kg", "11,9 kg"]):
            b += G(f"g-b{k}", prop(carton_flat(0, 0, 60, 44, kg), 1040 + k * 150, 330, 2.0))
        b += G("g-c3", box(80, 510, 860, 300, "Xuất chẵn pallet", ["Lấy nguyên pallet bằng xe nâng"], BLUE))
        b += G("g-c4", box(980, 510, 860, 300, "Xuất theo thùng", ["Lấy lẻ số thùng theo đơn"], ORANGE))
        b += G("g-lift", lift("g-f", 640, 790, 1.5))
        b += G("g-tr", prop(ms_trolley(), 1480, 790, 1.5)) + G("g-pk", fig("g-p", "picker", 1440, 790, s=1.2, pose=PUSH), hidden=True)
        b += MARK
        js = rise("#g-h", 0.0)
        js += popc("#g-c1", TT[0] + 0.2, 510, 330) + popc("#g-c2", TT[0] + 0.5, 1410, 330)
        for k in range(3):
            js += drop(f"#g-a{k}", TT[1] + 0.2 + k * 0.2)
        mid = TT[1] + MAN["s03-2"]["duration"] * 0.5
        for k in range(3):
            js += drop(f"#g-b{k}", mid + k * 0.25)
        js += popc("#g-c3", TT[2] + 0.1, 510, 660) + popc("#g-c4", TT[2] + 0.4, 1410, 660)
        js += slide_in("#g-lift", TT[2] + 0.5, -260, 1.2)
        js += show_js("#g-pk", TT[2] + 0.8) + slide_in("#g-tr", TT[2] + 0.8, 260, 1.2) + slide_in("#g-p-w", TT[2] + 0.8, 260, 1.2)
        js += walk_js("g-p", TT[2] + 0.8, TT[2] + 2.0)
        return svg(b), "", js
    s = VScene("s03", ["s03-1", "s03-2", "s03-3"], build, lead=0.5, tail=1.4)
    s.sfx = [(("T", 1, 0.2), "click-soft.mp3", 0.12)]
    return s


def show_js(sel, t, dur=0.2):
    return f'tl.to("{sel}",{{opacity:1,duration:{dur}}},{t:.2f});\n'


MAIN_RACK = [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"], ["A-03-01", "A-03-02"]]


# ============================================================ assembly + giọng đọc
def timeline():
    import nhieuloc_scenes
    return [s01(), s02(), s03()] + nhieuloc_scenes.scenes()


def restyle_captions():
    p = os.path.join(OUT, "compositions", "captions.html")
    src = open(p, encoding="utf-8").read()
    for a, b in (("bottom:84px", "bottom:40px"), ("font-size:54px", "font-size:44px"), ("max-width:1500px", "max-width:1380px")):
        assert a in src, a
        src = src.replace(a, b)
    open(p, "w", encoding="utf-8").write(src)


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
    restyle_captions()
    for s, start in placed:
        print(f"{start:7.2f}  {s.D:6.2f}  {s.cid}")
    print("TOTAL", total, "sfx", len(kept), "vo", n)
