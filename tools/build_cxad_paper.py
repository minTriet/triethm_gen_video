"""Video CXAD bản giấy: nhập / cất / lấy hàng bằng giấy, PDA chỉ ở chia hàng và xác nhận lên xe -> ./video-cxad-paper
Run: python3 tools/build_cxad_paper.py [limit_seconds]
Script source: source/Context_Video_CXAD_Paper_Full.md
Reuses the scenes of the approved CXAD video (tools/cxad_scenes.py) for Phần 2–4.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, stick, walk_js, pose_js, REST, pda_svg, icon
import stage as st
from stage import FY, INK
from build_full import Scene, chapter, ghinho, build_all
from parts import figure, svg_layer, desk_svg, pallet_build, carry_box, CARRY, SCAN, ic_forklift
import build_cxad_giay as bx
import cxad_scenes as c
from cxad_scenes import (lab_js, lab_off, press_js, show_js, hide_js, write_js, draw_js, walk_to, win, btn, pill, sheet,
                         paper, arrow_defs, arrow, dock_svg, zone_banner, ZRack, clipboard, office, HANDW, IC_DOC, IC_PEN)

OUT = os.path.join(os.path.dirname(__file__), "..", "video-cxad-paper")

STAGES = [("Nhập & cất hàng", "giay"), ("Lấy hàng gộp theo xe", "giay"), ("Chia hàng theo DO", "pda"), ("Kiểm & xác nhận lên xe", "pda")]


def tag_html(kind, size=26):
    if kind == "giay":
        return (f'<span style="display:inline-block;background:#FFF2E0;border:4px solid {C["orange"]};border-radius:12px;padding:4px 14px;'
                f'font-size:{size}px;font-weight:900;color:#C45A00;white-space:nowrap">GIẤY</span>')
    return (f'<span style="display:inline-block;background:#EAF1FC;border:4px solid {C["blue"]};border-radius:12px;padding:4px 14px;'
            f'font-size:{size}px;font-weight:900;color:{C["blue"]};white-space:nowrap">PDA</span>')


def tagged(scene, mapping):
    """Add a GIẤY / PDA chip right after the step badge text for the given step numbers."""
    orig = scene.build

    def build(T, D):
        body, css, js = orig(T, D)
        for n, kind in mapping.items():
            body = re.sub(rf'(<div class="t">Bước {n}: [^<]*</div>)', lambda m: m.group(1) + tag_html(kind), body)
        return body, css, js
    scene.build = build
    return scene


# ============================================================ MỞ ĐẦU / KẾT
def stage_chips(P, top):
    W, G, X0 = 360, 60, 120
    out = ""
    for i, (t, kind) in enumerate(STAGES):
        x = X0 + i * (W + G)
        out += (f'<div id="{P}-s{i}" class="abs" style="left:{x}px;top:{top}px;width:{W}px;height:190px;background:#fff;border:4px solid {INK};border-radius:22px;'
                f'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;opacity:0">'
                f'<div style="font-size:30px;font-weight:900;color:#C45A00">{i+1}</div><div style="font-size:34px;font-weight:900;text-align:center;line-height:1.15;padding:0 10px">{t}</div>'
                f'{tag_html(kind, 28)}<div id="{P}-k{i}" class="abs" style="right:-18px;top:-18px;opacity:0">{st.check(54)}</div></div>')
        if i < len(STAGES) - 1:
            out += f'<div id="{P}-a{i}" class="abs" style="left:{x+W}px;top:{top+62}px;width:{G}px;text-align:center;font-size:50px;font-weight:900;color:{C["blue"]};opacity:0">›</div>'
    return out


def chips_js(P, t0, step=0.4):
    js = ""
    for i in range(len(STAGES)):
        t = t0 + i * step
        js += f'tl.fromTo("#{P}-s{i}",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.8)"}},{t:.2f});\n'
        if i:
            js += f'tl.fromTo("#{P}-a{i-1}",{{opacity:0}},{{opacity:1,duration:0.2}},{t-0.1:.2f});\n'
    return js


def pa_intro():
    lines = ["Xin chào các bạn. Video này đi qua quy trình kho CXAD khi nhập và lấy hàng bằng giấy.",
             "PDA chỉ dùng ở hai bước: chia hàng và xác nhận hàng lên xe."]

    def build(T, D):
        P = "pa0"
        body = f"""
    <div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,{C['ground']} 0%,{C['ground']} 74%,{C['floor']} 74%,{C['floor']} 100%)"></div>
    <div id="{P}-title" class="abs" style="left:120px;top:80px"><div style="font-size:84px;font-weight:900;line-height:1.05">Quy trình vận hành kho CXAD</div>
      <div style="font-size:46px;font-weight:700;color:{C['blue']};margin-top:10px">Nhập và lấy hàng bằng giấy</div></div>
    {stage_chips(P, 400)}
    {svg_layer(f'<g transform="translate(1760,900)"><g id="{P}-man">{stick(P + "-man", "instructor", scale=1.9)}</g></g>')}"""
        js = f'tl.fromTo("#{P}-title",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:0.6,ease:"power3.out"}},0);\n'
        js += f'tl.fromTo("#{P}-man",{{x:420}},{{x:0,duration:1.4,ease:"power1.out"}},0.1);\n' + walk_js(P + "-man", 0.1, 1.5)
        js += pose_js(P + "-man", 1.6, {"armR": (-150, -24)}, dur=0.3, ease="power2.out")
        for k in range(4):
            js += f'tl.to("#{P}-man-foreR",{{rotation:{-50 if k % 2 == 0 else -5},svgOrigin:"0 0",duration:0.22,ease:"sine.inOut"}},{1.9 + k*0.22:.2f});\n'
        js += pose_js(P + "-man", 2.9, {"armR": REST["armR"]}, dur=0.3)
        js += chips_js(P, T[0] + 1.4)
        for i in (2, 3):
            js += f'tl.to("#{P}-s{i}",{{borderColor:"{C["blue"]}",scale:1.05,duration:0.25}},{T[1]+0.6 + (i-2)*0.4:.2f});\n'
        return body, "", js
    s = Scene("paintro", lines, build, lead=0.6, tail=1.0, min_hold={0: 5.6, 1: 3.6})
    s.sfx = [(("T", 0, 1.4), "whoosh-short.mp3", 0.25)]
    return s


def pa_end():
    lines = ["Nhập, cất và lấy hàng làm trên giấy, XLCT nhập lại vào WMS.",
             "Chia hàng và xác nhận lên xe dùng PDA. Chúc các bạn làm việc thật tốt!"]

    def build(T, D):
        P = "pae"
        man = svg_layer(f'<g transform="translate(960,{FY+40})"><g id="{P}-man">{stick(P + "-man", "instructor", 1.8)}</g></g>')
        body = f'<div class="abs" style="left:0;top:{FY}px;width:1920px;height:{1080-FY}px;background:{C["floor"]}"></div>' + stage_chips(P, 170) + man
        js = chips_js(P, 0.3, 0.35)
        for i in range(4):
            js += f'tl.fromTo("#{P}-k{i}",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.25,ease:"power3.out"}},{T[0 if i < 2 else 1] + 0.6 + (i % 2)*0.5:.2f});\n'
        js += pose_js(P + "-man", T[1] + 1.4, {"armR": (-100, -80)}, dur=0.35, ease="back.out(2)")
        return body, "", js
    s = Scene("paend", lines, build, lead=0.6, tail=2.6, min_hold={0: 4.0, 1: 4.4})
    s.sfx = [(("T", 1, 1.4), "chime.mp3", 0.22)]
    return s


# ============================================================ PHẦN 1 – Nhập & cất hàng bằng giấy (02A)
def pa_asn():
    lines = ["Khi có kế hoạch nhập, XLCT nhận file và xử lý cho đúng định dạng WMS.",
             "Sau đó nhập file vào WMS để tạo ASN."]

    def build(T, D):
        P = "pa1"
        body = svg_layer(st.floor() + office(P))
        body += sheet(f"{P}-sheet", 1000, 170, "Kế hoạch nhập (ASN).xlsx", ["Mã hàng", "Số lượng", "Date / Batch"],
                      [("SKU 1001", "30 thùng", "HSD 12/2026"), ("SKU 2001", "40 thùng", "B2405"), ("SKU 3001", "25 thùng", "HSD 03/2027")], cw=230)
        body += (f'<div id="{P}-okfmt" class="abs" style="left:1160px;top:500px;opacity:0"><div style="display:flex;align-items:center;gap:12px;background:#fff;border:5px solid {C["green"]};'
                 f'border-radius:18px;padding:10px 24px;font-size:36px;font-weight:900">{st.check(46)}Đúng định dạng WMS</div></div>')
        inner = (f'<div style="display:flex;align-items:center;gap:16px">{btn(P + "-imp", "Import file")}'
                 f'<div style="font-size:24px;font-weight:700;color:{C["muted"]}">Kế hoạch nhập (ASN).xlsx</div></div>'
                 f'<div id="{P}-asn" style="margin-top:18px;border:4px solid {C["green"]};background:#EDF9F1;border-radius:14px;padding:12px 16px;opacity:0">'
                 f'<div style="font-size:36px;font-weight:900">ASN-0001 ✔</div><div style="font-size:26px;font-weight:700">Xe 51C-123.45 · 3 pallet · 3 mã hàng</div></div>')
        body += win(f"{P}-wms", 1040, 170, 640, "WMS · Nhập hàng", inner)
        body += st.badge(f"{P}-b1", 1, "Nhận ASN") + st.badge(f"{P}-b2", 2, "Nhập vào WMS")
        js = st.badge_seq_js([f"{P}-b1", f"{P}-b2"], [T[0], T[1]], D - 0.4) + lab_js(f"{P}-xl", 0.3)
        js += st.appear_js(f"#{P}-sheet", T[0] + 0.2, 0.35, dy=20)
        for i, o in enumerate([30, -22, 12]):
            js += f'tl.fromTo("#{P}-sheet-r{i}",{{x:{o}}},{{x:0,duration:0.45,ease:"back.out(1.6)"}},{T[0]+1.8+i*0.25:.2f});\n'
        js += st.stamp_js(f"{P}-okfmt", T[0] + 2.9) + hide_js(f"#{P}-okfmt", T[1] - 0.1) + hide_js(f"#{P}-sheet", T[1])
        js += st.appear_js(f"#{P}-wms", T[1] + 0.1, 0.3) + press_js(f"#{P}-imp", T[1] + 0.7) + st.pop_js(f"#{P}-asn", T[1] + 1.1)
        return body, "", js
    s = Scene("paasn", lines, build, lead=0.5, tail=1.2, min_hold={0: 5.0, 1: 3.4})
    s.sfx = [(("T", 0, 2.9), "chime.mp3", 0.22)]
    return s


def tally_html(pid, x, y, w=940, filled=False):
    """Phiếu kiểm đếm (tally slip) on paper; handwritten cells {pid}-w0 / {pid}-w1."""
    cell = "display:inline-block;padding:10px 12px;font-size:28px;font-weight:700;box-sizing:border-box;border-right:2px solid #D5DBE4;vertical-align:middle"
    cols = [("Mã hàng", 220), ("SL phiếu", 170), ("SL thực nhận", 200), ("Date / Batch", 342)]
    op = "1" if filled else "0"
    hw = f"color:{HANDW};font-style:italic;font-weight:900;font-size:30px;display:inline-block;opacity:{op}"
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;background:#fff;border:4px solid {INK};border-radius:6px;overflow:hidden;opacity:0;box-shadow:0 10px 0 rgba(27,36,48,.10)">'
            f'<div style="background:#F4F6F9;border-bottom:4px solid {C["blue"]};padding:10px 16px;font-size:30px;font-weight:900">PHIẾU KIỂM ĐẾM · ASN-0001 · Pallet 1/3</div>'
            f'<div style="white-space:nowrap">' + "".join(f'<span style="{cell};width:{cw}px;font-weight:900">{t}</span>' for t, cw in cols) + '</div>'
            f'<div style="white-space:nowrap;border-top:2px solid #D5DBE4">'
            f'<span style="{cell};width:220px">SKU 2001</span><span style="{cell};width:170px">40 thùng</span>'
            f'<span style="{cell};width:200px"><span id="{pid}-w0" style="{hw}">40 thùng</span></span>'
            f'<span style="{cell};width:342px;border-right:none"><span id="{pid}-w1" style="{hw}">20/05/27 · B2405</span></span></div></div>')


def pa_print():
    lines = ["XLCT in phiếu kiểm đếm và nhãn chi tiết pallet,",
             "rồi giao cho nhân viên nhận hàng."]

    def build(T, D):
        P = "pa3"
        rc = figure(f"{P}-rc", "receiver", 2100, FY, scale=1.5, label=True, hand_r=clipboard(P + "-rc"))
        body = svg_layer(st.floor() + office(P, label=False) + rc)
        body += paper(f"{P}-p0", 505, 460, "Phiếu kiểm đếm", 300, 200)
        body += paper(f"{P}-p1", 505, 460, "Nhãn chi tiết pallet", 300, 200, edge=C["orange"], head=C["orange"])
        body += st.badge(f"{P}-b3", 3, "In chứng từ")
        js = st.badge_seq_js([f"{P}-b3"], [T[0]], D - 0.4)
        for i, (dx, dy) in enumerate([(520, -280), (880, -280)]):
            t = T[0] + 0.5 + i * 0.8
            js += f'tl.fromTo("#{P}-p{i}",{{opacity:0,x:0,y:0,scale:0.4}},{{opacity:1,x:{dx},y:{dy},scale:1,duration:0.6,ease:"power2.out",transformOrigin:"50% 100%"}},{t:.2f});\n'
        js += walk_to(f"{P}-rc", f"{P}-rc", 800 - 2100, T[1], 1.8) + lab_js(f"{P}-rc", T[1] + 1.2)
        for i in range(2):
            js += f'tl.to("#{P}-p{i}",{{x:{290 + i*10},y:{-60},scale:0.15,opacity:0,duration:0.6,ease:"power2.in",transformOrigin:"50% 50%"}},{T[1]+2.0+i*0.2:.2f});\n'
        return body, "", js
    s = Scene("paprint", lines, build, lead=0.5, tail=1.4, min_hold={0: 3.4, 1: 3.6})
    s.sfx = [(("T", 0, 0.5), "click-soft.mp3", 0.3)]
    return s


def pallet_label(lid, cx, by, hidden=True):
    op = ' opacity="0"' if hidden else ""
    return (f'<g id="{lid}"{op}><rect x="{cx-72}" y="{by-66}" width="70" height="42" rx="3" fill="#fff" stroke="{C["orange"]}" stroke-width="2.5"/>'
            f'<text x="{cx-37}" y="{by-49}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="11" fill="{INK}">PALLET 1/3</text>'
            f'<rect x="{cx-64}" y="{by-42}" width="54" height="4" fill="#B0B8C4"/><rect x="{cx-64}" y="{by-34}" width="40" height="4" fill="#B0B8C4"/></g>')


def pa_recv():
    lines = ["Xe hàng tới, nhân viên dỡ hàng, kiểm tra ngoại quan và đếm hàng.",
             "Xếp hàng lên pallet, dán nhãn chi tiết pallet,",
             "rồi ghi số lượng thực nhận và date hoặc batch lên phiếu kiểm đếm."]

    def build(T, D):
        P, PX, RX, TX = "pa4", 520, 700, 1080
        mag = (f'<g id="{P}-mag" opacity="0" transform="translate({TX+40},{FY-330})"><circle cx="0" cy="0" r="34" fill="#EAF6FF" stroke="{INK}" stroke-width="6"/>'
               f'<line x1="24" y1="24" x2="54" y2="54" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
               f'<path d="M-14,0 l9,10 l18,-20" fill="none" stroke="{C["green"]}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>')
        cnt = "".join(f'<g id="{P}-n{i}" opacity="0"><rect x="{PX-90}" y="{FY-250}" width="180" height="56" rx="28" fill="{INK}"/>'
                      f'<text x="{PX}" y="{FY-212}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="30" fill="#fff">Đếm: {v}</text></g>'
                      for i, v in enumerate(["10", "20", "30", "40 thùng"]))
        body = svg_layer(st.floor() + dock_svg()
                         + f'<g transform="translate(1960,{FY})"><g id="{P}-truck">{st.truck(P + "-tk", label="51C-123.45")}</g></g>'
                         + pallet_build(P + "-pal", PX, FY, sku="2001", lpn=False) + pallet_label(P + "-lab", PX, FY)
                         + figure(f"{P}-rc", "receiver", RX, scale=1.5, label=True, extra=carry_box(f"{P}-rc", 1.5)) + mag + cnt)
        body += tally_html(f"{P}-ts", 80, 160)
        body += st.badge(f"{P}-b4", 4, "Nhận hàng")
        js = st.badge_seq_js([f"{P}-b4"], [T[0]], D - 0.4)
        js += f'tl.fromTo("#{P}-truck",{{x:0}},{{x:-810,duration:1.6,ease:"power2.out"}},0.0);\n' + lab_js(f"{P}-rc", 0.5)
        t = T[0] + 0.2
        for trip in range(2):
            js += walk_to(f"{P}-rc", f"{P}-rc", TX - RX, t, 1.0)
            js += pose_js(f"{P}-rc", t + 1.0, CARRY, dur=0.25) + show_js(f"#{P}-rc-box", t + 1.1, 0.15)
            js += f'tl.fromTo("#{P}-mag",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)"}},{t+1.2:.2f});\n' + hide_js(f"#{P}-mag", t + 1.75)
            js += walk_to(f"{P}-rc", f"{P}-rc", 0, t + 1.9, 1.0) + hide_js(f"#{P}-rc-box", t + 2.95, 0.1)
            for k in (2 * trip, 2 * trip + 1):
                tk = t + 2.95 + 0.25 * (k % 2)
                js += st.pop_js(f"#{P}-pal-c{k}", tk, 0.3)
                if k:
                    js += hide_js(f"#{P}-n{k-1}", tk, 0.1)
                js += show_js(f"#{P}-n{k}", tk + 0.05, 0.1)
            js += pose_js(f"{P}-rc", t + 3.0, REST, dur=0.2)
            t += 3.4
        js += st.pop_js(f"#{P}-lab", max(T[1] + 0.6, t))
        js += hide_js(f"#{P}-n3", T[2] - 0.1)
        js += lab_off(f"{P}-rc", T[2] - 0.1)
        js += f'tl.fromTo("#{P}-ts",{{opacity:0,y:20,rotation:-2}},{{opacity:1,y:0,rotation:0,duration:0.4,ease:"power2.out"}},{T[2]:.2f});\n'
        js += write_js(f"#{P}-ts-w0", T[2] + 1.0, 0.8) + write_js(f"#{P}-ts-w1", T[2] + 2.2, 1.2)
        return body, "", js
    s = Scene("parecv", lines, build, lead=1.6, tail=1.6, min_hold={0: 4.6, 1: 3.6, 2: 5.0})
    s.sfx = [(("T", 0, 1.4), "click-soft.mp3", 0.25)]
    return s


def gnk_doc(P, x=1000, y=110):
    sig = ["Tài xế (bên giao)", "Nhân viên nhận hàng", "XLCT"]
    boxes = "".join(f'<div style="flex:1;text-align:center"><div style="font-size:22px;font-weight:700;color:{C["muted"]};height:56px">{s}</div>'
                    f'<svg width="200" height="70" viewBox="0 0 200 70"><path id="{P}-sg{i}" d="M20,48 C40,10 55,62 75,30 S110,12 120,44 S160,30 182,22" fill="none" stroke="{HANDW}" stroke-width="5" '
                    f'stroke-linecap="round" stroke-dasharray="320" stroke-dashoffset="320"/><line x1="10" y1="62" x2="190" y2="62" stroke="#B0B8C4" stroke-width="3"/></svg></div>'
                    for i, s in enumerate(sig))
    rows = [("SKU 1001 · Há cảo", "30 thùng"), ("SKU 2001 · Sữa chua", "40 thùng"), ("SKU 3001 · Bánh quy", "25 thùng")]
    rh = "".join(f'<div style="display:flex;justify-content:space-between;border-top:2px solid #E3E8EF;padding:8px 0;font-size:28px;font-weight:700"><span>{a}</span><b>{b}</b></div>' for a, b in rows)
    return (f'<div id="{P}-doc" class="abs" style="left:{x}px;top:{y}px;width:780px;background:#fff;border:5px solid {C["blue"]};border-radius:14px;padding:22px 30px;opacity:0;box-shadow:0 14px 0 rgba(27,36,48,.10)">'
            f'<div style="font-size:44px;font-weight:900;text-align:center">PHIẾU NHẬP KHO</div>'
            f'<div style="font-size:26px;font-weight:700;text-align:center;color:{C["muted"]};margin-bottom:10px">ASN-0001 · Xe 51C-123.45</div>{rh}'
            f'<div style="display:flex;margin-top:18px">{boxes}</div></div>')


def pa_done():
    lines = ["Nhân viên nộp phiếu kiểm đếm cho XLCT.",
             "XLCT nhập số lượng và date hoặc batch vào WMS, xác nhận đã nhận hàng xong,",
             "in phiếu nhập kho và chuyển các bên ký."]

    def build(T, D):
        P = "pa5"
        rc = figure(f"{P}-rc", "receiver", 820, FY, scale=1.5, label=True, hand_r=clipboard(P + "-rc"))
        body = svg_layer(st.floor() + office(P, label=False) + rc)
        body += tally_html(f"{P}-ts", 60, 160, filled=True)
        inner = (f'<div style="font-size:28px;font-weight:700;color:{C["muted"]}">ASN-0001 · SKU 2001 · Pallet 1/3</div>'
                 f'<div style="font-size:26px;font-weight:700;color:{C["muted"]};margin-top:12px">SL thực nhận</div>'
                 f'<div style="border:4px solid {C["orange"]};background:#FFF7EE;border-radius:14px;padding:8px 16px;font-size:34px;font-weight:900;min-height:60px"><span id="{P}-t0" style="display:inline-block;opacity:0">40 thùng</span></div>'
                 f'<div style="font-size:26px;font-weight:700;color:{C["muted"]};margin-top:12px">Date / Batch</div>'
                 f'<div style="border:4px solid {C["orange"]};background:#FFF7EE;border-radius:14px;padding:8px 16px;font-size:34px;font-weight:900;min-height:60px;margin-bottom:16px"><span id="{P}-t1" style="display:inline-block;opacity:0">20/05/2027 · B2405</span></div>'
                 f'{btn(P + "-go", "XÁC NHẬN ĐÃ NHẬN HÀNG")}')
        body += win(f"{P}-w", 1040, 430, 720, "WMS · Nhận hàng", inner)
        body += svg_layer(arrow_defs(P) + arrow(f"{P}-a", "M1000,300 C1040,340 1000,470 1036,520", P, width=7, dash=500))
        body += st.stamp(f"{P}-ok", "Đã nhận hàng xong", x=1080, y=300)
        body += gnk_doc(P)
        body += st.badge(f"{P}-b5", 5, "Hoàn tất nhận hàng")
        js = st.badge_seq_js([f"{P}-b5"], [T[0]], D - 0.4) + lab_js(f"{P}-rc", 0.3)
        js += f'tl.fromTo("#{P}-ts",{{opacity:0,x:700,y:400,scale:0.15}},{{opacity:1,x:0,y:0,scale:1,duration:0.7,ease:"power2.out",transformOrigin:"0% 0%"}},{T[0]+0.5:.2f});\n'
        js += lab_off(f"{P}-rc", T[1] - 0.2) + walk_to(f"{P}-rc", f"{P}-rc", 1300, T[1], 2.4)
        js += st.appear_js(f"#{P}-w", T[1] + 0.2) + draw_js(f"#{P}-a", T[1] + 0.6, 0.5)
        js += write_js(f"#{P}-t0", T[1] + 1.2, 0.6) + write_js(f"#{P}-t1", T[1] + 2.0, 0.9) + press_js(f"#{P}-go", T[1] + 3.2) + st.stamp_js(f"{P}-ok", T[1] + 3.4)
        for sel in (f"#{P}-w", f"#{P}-a", f"#{P}-ok", f"#{P}-ts"):
            js += hide_js(sel, T[2] - 0.2)
        js += f'tl.fromTo("#{P}-doc",{{opacity:0,x:-380,y:420,scale:0.2}},{{opacity:1,x:0,y:0,scale:1,duration:0.8,ease:"power2.out",transformOrigin:"0% 100%"}},{T[2]+0.1:.2f});\n'
        for i in range(3):
            js += f'tl.to("#{P}-sg{i}",{{strokeDashoffset:0,duration:0.6,ease:"none"}},{T[2]+1.3+i*0.8:.2f});\n'
        return body, "", js
    s = Scene("padone", lines, build, lead=0.4, tail=1.4, min_hold={0: 2.8, 1: 5.0, 2: 4.6})
    s.sfx = [(("T", 1, 3.4), "chime.mp3", 0.22)]
    return s


PUT_ROWS = [("Pallet 1 · SKU 2001", "CHILL-A01-02", "chill"), ("Pallet 2 · SKU 1001", "ĐÔNG-A02-03", "dong"), ("Pallet 3 · SKU 3001", "KHÔ-A01-02", "kho")]


def putslip_html(pid, x, y, w=760, filled=False):
    hw = f"color:{HANDW};font-style:italic;font-weight:900;font-size:32px;display:inline-block;opacity:{'1' if filled else '0'}"
    rows = "".join(f'<div style="display:flex;align-items:center;border-top:2px solid #D5DBE4;padding:10px 16px"><span style="flex:1;font-size:28px;font-weight:700">{a}</span>'
                   f'<span style="width:300px;border-bottom:3px dotted #B0B8C4"><span id="{pid}-w{i}" style="{hw}">{b}</span></span></div>'
                   for i, (a, b, _) in enumerate(PUT_ROWS))
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;background:#fff;border:4px solid {INK};border-radius:6px;overflow:hidden;opacity:0;box-shadow:0 10px 0 rgba(27,36,48,.10)">'
            f'<div style="background:#F4F6F9;border-bottom:4px solid {C["orange"]};padding:10px 16px;font-size:30px;font-weight:900">PHIẾU CẤT HÀNG · ASN-0001 · ghi vị trí</div>{rows}</div>')


def pa_put():
    lines = ["Tài xế xe nâng đưa từng pallet lên kệ đúng khu,",
             "và ghi lại vị trí của từng pallet lên phiếu."]

    def build(T, D):
        P = "pa6"
        R = ZRack(P + "r", 900, "chill", cols=3, levels=3, cw=260, lh=200)
        rack = R.svg(contents={(1, 0): "cartons", (2, 0): "cartons", (1, 1): "pallet", (2, 2): "pallet", (0, 0): "cartons"})
        FX = 330
        tx, tb = R.slot(0, 1)
        lift, drive = tb - (FY - 22), tx - 125 - FX
        back = drive - 170
        load = pallet_build(P + "-pal", 125, -22, sku="2001", shown=True, lpn=False)
        fl = f'<g transform="translate({FX},{FY})"><g id="{P}-fl">{st.forklift(P + "-fk", label=True, load=load)}</g></g>'
        placed = f'<g id="{P}-placed" opacity="0">{st.pallet(P + "-pp", tx, tb, sku="2001")}</g>'
        hl = f'<rect id="{P}-hl" x="{tx-R.cw/2+8}" y="{tb-R.lh+34}" width="{R.cw-16}" height="{R.lh-30}" rx="8" fill="none" stroke="{C["orange"]}" stroke-width="8" opacity="0"/>'
        body = svg_layer(st.floor() + rack + zone_banner(P + "-zb", "chill", 900, 120, 780) + placed + hl + fl)
        body += putslip_html(f"{P}-ps", 90, 160)
        body += st.badge(f"{P}-b6", 6, "Đưa hàng lên kệ")
        js = st.badge_seq_js([f"{P}-b6"], [T[0]], D - 0.4)
        js += f'tl.fromTo("#{P}-fk-drv-label",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},0.3);\n'
        t1 = T[0] + 0.4
        js += f'tl.to("#{P}-fl",{{x:{drive},duration:1.4,ease:"power2.inOut"}},{t1:.2f});\n'
        js += f'tl.to("#{P}-fk-forks",{{y:{lift},duration:1.0,ease:"power2.inOut"}},{t1+1.45:.2f});\n'
        js += f'tl.set("#{P}-placed",{{opacity:1}},{t1+2.5:.2f});\ntl.set("#{P}-pal",{{opacity:0}},{t1+2.5:.2f});\n'
        js += f'tl.to("#{P}-fk-forks",{{y:0,duration:0.8,ease:"power2.inOut"}},{t1+2.6:.2f});\n'
        js += f'tl.to("#{P}-fl",{{x:{back},duration:0.8,ease:"power2.inOut"}},{t1+2.6:.2f});\n'
        js += show_js(f"#{P}-hl", t1 + 2.6, 0.2)
        js += f'tl.fromTo("#{P}-ps",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power2.out"}},{T[1]:.2f});\n'
        for i in range(3):
            js += write_js(f"#{P}-ps-w{i}", T[1] + 0.6 + i * 1.2, 0.8)
        js += hide_js(f"#{P}-hl", T[1] + 1.6)
        return body, "", js
    s = Scene("paput", lines, build, lead=0.4, tail=1.4, min_hold={0: 4.4, 1: 4.6})
    return s


def pa_loc():
    lines = ["XLCT nhập vị trí của các pallet vào WMS để hoàn tất cất hàng."]

    def build(T, D):
        P = "pa7"
        body = svg_layer(st.floor() + office(P))
        body += putslip_html(f"{P}-ps", 60, 160, w=760, filled=True)
        rows = "".join(f'<div style="display:flex;align-items:center;gap:12px;border-top:2px solid #E3E8EF;padding:10px 0">'
                       f'<span style="flex:1;font-size:28px;font-weight:700">{a}</span>'
                       f'<span style="width:290px;border:4px solid {C["orange"]};background:#FFF7EE;border-radius:12px;padding:4px 12px;font-size:26px;white-space:nowrap;font-weight:900;min-height:48px">'
                       f'<span id="{P}-t{i}" style="display:inline-block;opacity:0">{b}</span></span><span id="{P}-k{i}" style="opacity:0">{st.check(44)}</span></div>'
                       for i, (a, b, _) in enumerate(PUT_ROWS))
        body += win(f"{P}-w", 1000, 170, 780, "WMS · Cất hàng (nhập vị trí)", rows)
        body += svg_layer(arrow_defs(P) + arrow(f"{P}-a", "M824,300 C900,300 930,320 996,330", P, width=7, dash=300))
        body += st.stamp(f"{P}-ok", "Đã cất hàng", x=1180, y=560)
        body += st.badge(f"{P}-b7", 7, "Cất hàng vào vị trí")
        js = st.badge_seq_js([f"{P}-b7"], [T[0]], D - 0.4) + lab_js(f"{P}-xl", 0.3)
        js += st.appear_js(f"#{P}-ps", 0.2) + st.appear_js(f"#{P}-w", T[0] + 0.3) + draw_js(f"#{P}-a", T[0] + 0.7, 0.4)
        for i in range(3):
            t = T[0] + 1.2 + i * 1.0
            js += write_js(f"#{P}-t{i}", t, 0.6) + st.pop_js(f"#{P}-k{i}", t + 0.7, 0.25)
        js += st.stamp_js(f"{P}-ok", T[0] + 4.4)
        return body, "", js
    s = Scene("paloc", lines, build, lead=0.4, tail=1.4, min_hold={0: 5.4})
    s.sfx = [(("T", 0, 4.4), "chime.mp3", 0.22)]
    return s


def pa_g1():
    return ghinho("g1", 1, [
        (IC_DOC, "XLCT in <b>phiếu kiểm đếm</b> và <b>nhãn chi tiết pallet</b>", "XLCT in phiếu kiểm đếm và nhãn chi tiết pallet"),
        (IC_PEN, "Kho đếm hàng, <b>ghi tay</b> số lượng, date / batch – không dùng PDA",
         "Kho đếm hàng, ghi tay số lượng, date batch, không dùng PDA"),
        (ic_forklift(), "Kho ghi vị trí cất hàng, <b>XLCT nhập lại vào WMS</b>", "Kho ghi vị trí cất hàng, XLCT nhập lại vào WMS"),
    ])


# ============================================================ cầu nối Phần 2 → 3
def pa_gate():
    lines = ["XLCT phải nhập xong số thực lấy thì mới chia hàng trên PDA được."]

    def build(T, D):
        P = "pag"
        left = win(f"{P}-w", 200, 260, 620, "WMS · MDO-0001",
                   f'<div style="font-size:32px;font-weight:900">Xác nhận lấy hàng</div>'
                   f'<div id="{P}-st0" style="font-size:30px;font-weight:700;color:{C["muted"]};margin-top:8px">Đang chờ XLCT nhập số thực lấy…</div>'
                   f'<div id="{P}-st1" style="font-size:32px;font-weight:900;color:{C["green"]};margin-top:8px;opacity:0">✔ Đã nhập đủ số thực lấy</div>', hidden=False)
        pda = (f'<div class="abs" style="left:1240px;top:180px;width:300px;height:520px;background:#2B3646;border:5px solid {INK};border-radius:40px">'
               f'<div style="position:absolute;left:18px;right:18px;top:46px;bottom:56px;background:#fff;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px">'
               f'<div style="font-size:30px;font-weight:900">Chia hàng</div>'
               f'<div style="position:relative;width:96px;height:96px"><div id="{P}-lock" class="abs" style="left:0;top:0">{icon("lock", 96)}</div>'
               f'<div id="{P}-open" class="abs" style="left:0;top:0;opacity:0">{icon("check", 96)}</div></div>'
               f'<div id="{P}-l0" style="font-size:26px;font-weight:700;color:{C["muted"]};text-align:center;padding:0 10px">Chưa chia được</div></div></div>')
        body = left + pda + svg_layer(arrow_defs(P) + arrow(f"{P}-a", "M840,440 L1220,440", P, width=9, dash=400))
        js = draw_js(f"#{P}-a", T[0] + 0.4, 0.5)
        js += hide_js(f"#{P}-st0", T[0] + 1.8) + show_js(f"#{P}-st1", T[0] + 1.9)
        js += hide_js(f"#{P}-lock", T[0] + 2.6) + f'tl.fromTo("#{P}-open",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.3,ease:"power3.out"}},{T[0]+2.7:.2f});\n'
        js += f'tl.set("#{P}-l0",{{innerHTML:"Sẵn sàng chia hàng",color:"{C["green"]}"}},{T[0]+2.7:.2f});\n'
        return body, "", js
    s = Scene("pagate", lines, build, lead=0.4, tail=1.2, min_hold={0: 4.4})
    s.sfx = [(("T", 0, 2.7), "ping.mp3", 0.25)]
    return s


def pa_pdastart():
    lines = ["Từ bước chia hàng, nhân viên bắt đầu dùng PDA."]

    def build(T, D):
        P = "pap"
        pk = figure(f"{P}-pk", "picker", 700, FY, scale=1.8, label=True, pose={"armR": (-60, -60)}, hand_r=pda_svg(P + "-pk"))
        body = svg_layer(st.floor() + pk)
        body += st.pda(f"{P}-pda", "Chia hàng", [("s1", '<div class="lbl">Chọn xe / Master DO</div><div class="row sel"><b>XE-01 · MDO-0001</b></div><div class="row">XE-02 · MDO-0002</div>')])
        body += pill(f"{P}-tag", 160, 200, "Bắt đầu dùng PDA", "#EAF1FC", txt=C["blue"], border=C["blue"], size=48)
        js = lab_js(f"{P}-pk", 0.3) + st.appear_js(f"#{P}-pda", T[0] + 0.2, 0.35, dy=30) + st.show_panel_js(f"{P}-pda", None, "s1", T[0] + 0.3)
        js += f'tl.fromTo("#{P}-tag",{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:0.35,ease:"power3.out"}},{T[0]+0.6:.2f});\n'
        return body, "", js
    s = Scene("papda", lines, build, lead=0.4, tail=1.0, min_hold={0: 3.4})
    s.sfx = [(("T", 0, 0.6), "ping.mp3", 0.25)]
    return s


def timeline():
    return [pa_intro(), bx.cx_map(),
            chapter(1, "Nhập hàng và cất hàng bằng giấy", lead=2.7), pa_asn(), pa_print(), tagged(pa_recv(), {4: "giay"}),
            pa_done(), tagged(pa_put(), {6: "giay"}), pa_loc(), pa_g1(),
            chapter(2, "Lấy hàng gộp theo xe bằng giấy", lead=2.7), c.cx_do(), c.cx_master(), c.cx_alloc(), c.cx_picklist(),
            tagged(c.cx_pick(), {6: "giay", 7: "giay"}), c.cx_confirm(), pa_gate(), c.cx_g2(),
            chapter(3, "Chia hàng theo đơn DO", lead=2.7), pa_pdastart(), c.cx_cells(), tagged(c.cx_sort(), {2: "pda"}), c.cx_diff(), c.cx_g3(),
            chapter(4, "Kiểm hàng và xác nhận lên xe", lead=2.7), tagged(c.cx_check(), {1: "pda"}), c.cx_hand(), c.cx_g4(),
            pa_end()]


TITLES = ["Mở đầu (nhãn GIẤY / PDA)", "Sơ đồ kho CXAD",
          "Bước 1–2 · Nhận ASN, nhập WMS", "Bước 3 · In phiếu kiểm đếm, nhãn chi tiết pallet", "Bước 4 · Nhận hàng, ghi tay phiếu kiểm đếm [GIẤY]",
          "Bước 5 · XLCT nhập số liệu, in & ký phiếu nhập kho", "Bước 6 · Đưa hàng lên kệ, ghi vị trí [GIẤY]", "Bước 7 · XLCT nhập vị trí", "Ghi nhớ Phần 1",
          "Bước 1–2 · Nhận kế hoạch xuất, import DO", "Bước 3 · Tạo Master DO", "Bước 4 · Phân bổ tồn kho", "Bước 5 · In Picklist",
          "Bước 6–7 · Lấy hàng bằng giấy, đưa về khu chia [GIẤY]", "Bước 8 · XLCT xác nhận lấy hàng", "Nhắc: nhập xong mới chia trên PDA", "Ghi nhớ Phần 2",
          "Bắt đầu dùng PDA", "Bước 1 · Chuẩn bị khu chia", "Bước 2 · Chia hàng [PDA] + Đã chia hết hàng?",
          "Có thiếu / thừa? · Bước 3 Xử lý chênh lệch (thủ công)", "Ghi nhớ Phần 3",
          "Bước 1–2 · Kiểm hàng [PDA], xử lý sai lệch (thủ công)", "Bước 3–5 · In giấy bàn giao, tài xế ký, hoàn tất", "Ghi nhớ Phần 4", "Kết"]
SB_TITLE = "Storyboard – Kho CXAD: nhập & lấy hàng bằng giấy, PDA chỉ ở chia hàng và xác nhận lên xe"
CHAPTERS = {"chap1": "Phần 1 – Nhập hàng và cất hàng bằng giấy", "chap2": "Phần 2 – Lấy hàng gộp theo xe bằng giấy",
            "chap3": "Phần 3 – Chia hàng theo đơn DO (PDA)", "chap4": "Phần 4 – Kiểm hàng và xác nhận lên xe (PDA)"}

if __name__ == "__main__":
    limit = float(sys.argv[1]) if len(sys.argv) > 1 else None
    os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
    placed, total, kept = build_all(limit, seq=timeline(), out=OUT)
    for s, start in placed:
        print(f"{start:7.2f}  {s.D:6.2f}  {s.cid}")
    print("TOTAL", total, "sfx", len(kept))
