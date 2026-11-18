"""Training video: Quy trình toàn kho CXAD -> ./video-cxad
Run: python3 tools/build_cxad.py [limit_seconds]
Script source: source/Prompt_Video_Quy_trinh_toan_kho_CXAD.md (v2, đã xác nhận)
Characters: skill nhan-vat-kho (model sheet v3).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, ROLE, stick, walk_js, pose_js, REST, pda_svg
import stage as st
from stage import FY, INK
from build_full import Scene, chapter, build_all, ghinho, ic_svg
from parts import figure, svg_layer, kv, hand, SCAN, CARRY, carry_box, pallet_build, pda_popup, swap_js
import cxad_kit as K
from cxad_kit import cbadge, wms, decision, decision_js, card

OUT = os.path.join(os.path.dirname(__file__), "..", "video-cxad")

# labels used in this video (same roles and colours as the default cast)
ROLE["planner"] = (ROLE["planner"][0], "Nhân viên XLCT")
ROLE["transport"] = (ROLE["transport"][0], "Tài xế xe tải")

STEPS = [("Nhập & Putaway", "02F"), ("Lấy hàng gộp theo xe", "04K.1"), ("Chia hàng theo DO", "04K.2"), ("Kiểm & Bàn giao", "04K.3")]


def bg_floor():
    return (f'<div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,{C["ground"]} 0%,'
            f'{C["ground"]} 74%,{C["floor"]} 74%,{C["floor"]} 100%)"></div>')


def step_strip(prefix, top, W=380, G=56, X0=110, tick=False):
    s = ""
    for i, (t, code) in enumerate(STEPS):
        x = X0 + i * (W + G)
        okv = (f'<div id="{prefix}-ok{i}" class="abs" style="right:-18px;top:-22px;opacity:0">{st.check(56)}</div>' if tick else "")
        s += (f'<div id="{prefix}-s{i}" class="abs" style="left:{x}px;top:{top}px;width:{W}px;height:150px;background:#fff;border:4px solid {INK};border-radius:22px;'
              f'display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0">'
              f'<div style="font-size:26px;font-weight:900;color:#C45A00">{i+1} · {code}</div>'
              f'<div style="font-size:36px;font-weight:900;text-align:center;line-height:1.15;padding:0 12px">{t}</div>{okv}</div>')
        if i < len(STEPS) - 1:
            s += (f'<div id="{prefix}-a{i}" class="abs" style="left:{x+W}px;top:{top+42}px;width:{G}px;text-align:center;font-size:50px;'
                  f'font-weight:900;color:{C["blue"]};opacity:0">›</div>')
    return s


def strip_js(prefix, t0, gap=0.3):
    js = ""
    for i in range(len(STEPS)):
        js += f'tl.fromTo("#{prefix}-s{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{t0 + i*gap:.2f});\n'
        if i < len(STEPS) - 1:
            js += f'tl.fromTo("#{prefix}-a{i}",{{opacity:0}},{{opacity:1,duration:0.2}},{t0 + 0.2 + i*gap:.2f});\n'
    return js


def wave_js(fid, t):
    js = pose_js(fid, t, {"armR": (-150, -24)}, dur=0.3, ease="power2.out")
    for k in range(4):
        js += f'tl.to("#{fid}-foreR",{{rotation:{-50 if k % 2 == 0 else -5},svgOrigin:"0 0",duration:0.22,ease:"sine.inOut"}},{t + 0.3 + k*0.22:.2f});\n'
    return js + pose_js(fid, t + 1.3, {"armR": REST["armR"]}, dur=0.3)


# ============================================================ MỞ ĐẦU
def cx_intro():
    lines = ["Xin chào các bạn.",
             "Video này đi qua toàn bộ quy trình kho của chủ hàng CXAD, từ lúc nhập hàng đến khi giao hàng lên xe."]

    def build(T, D):
        body = bg_floor() + f"""
    <div id="ci-title" class="abs" style="left:110px;top:90px"><div style="font-size:100px;font-weight:900;line-height:1.05">Quy trình vận hành kho</div>
      <div style="display:flex;align-items:center;gap:20px;margin-top:16px"><div id="ci-bar" style="width:160px;height:10px;border-radius:5px;background:{C['orange']}"></div>
      <div style="font-size:54px;font-weight:900;color:{C['blue']}">Chủ hàng CXAD</div></div></div>
    {step_strip("ci", 330)}
    {svg_layer(f'<g transform="translate(1720,{FY+60})"><g id="ci-man">{stick("ci-man", "instructor", scale=2.0)}</g></g>')}"""
        js = 'tl.fromTo("#ci-title",{opacity:1,x:-24},{opacity:1,x:0,duration:0.6,ease:"power3.out"},0);\n'
        js += 'tl.fromTo("#ci-bar",{scaleX:0},{scaleX:1,duration:0.5,ease:"power2.out",transformOrigin:"0% 50%"},0.3);\n'
        js += 'tl.fromTo("#ci-man",{x:300},{x:0,duration:1.2,ease:"power1.out"},0.1);\n' + walk_js("ci-man", 0.1, 1.3)
        js += wave_js("ci-man", 1.4)
        js += strip_js("ci", T[1] + 0.5, 0.45)
        return body, "", js
    s = Scene("cxintro", lines, build, lead=0.4, tail=1.2, min_hold={0: 3.0, 1: 6.0})
    s.sfx = [(0.4, "whoosh.mp3", 0.25)]
    return s


WORLD = [("chia", 300, 600), ("dong", 960, 600), ("chill", 1600, 600), ("kho", 2240, 640)]


def cx_zones():
    lines = ["Kho có ba khu: hàng đông, hàng chill và hàng khô."]

    def build(T, D):
        w = (f'<rect x="0" y="{FY}" width="3000" height="{1080-FY}" fill="{C["floor"]}"/>'
             f'<line x1="0" y1="{FY}" x2="3000" y2="{FY}" stroke="{C["floor_line"]}" stroke-width="4"/>'
             f'<rect x="0" y="520" width="200" height="{FY-520}" fill="#D5DBE4"/><text x="100" y="500" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="30" fill="{C["muted"]}">DOCK</text>')
        for z, x0, wd in WORLD:
            if z == "chia":
                w += f'<g id="cz-chia">{K.chia_floor(x0, x0 + wd)}</g>'
                continue
            w += K.zone_bg(f"cz-{z}", x0, wd, z)
            R = K.ZRack(f"cz-r{z}", x0 + 70, zone=z, cols=2, cw=230, lh=180)
            w += R.svg(contents=[(0, 1), (1, 2), (0, 2)], cartons=[(0, 0), (1, 0)], labels=False)
        body = svg_layer(f'<g id="cz-world">{w}</g>')
        pan = -(3000 - 1920)
        js = f'tl.fromTo("#cz-world",{{x:0}},{{x:{pan},duration:{D-0.6:.2f},ease:"sine.inOut"}},0.2);\n'
        hits = {"dong": T[0] + 0.9, "chill": T[0] + 2.0, "kho": T[0] + 3.1}
        for z, t in hits.items():
            js += f'tl.fromTo("#cz-{z}-sign",{{scale:0.5,opacity:0}},{{scale:1,opacity:1,duration:0.35,ease:"back.out(2.4)",transformOrigin:"50% 50%"}},{t:.2f});\n'
        return body, "", js
    s = Scene("cxzones", lines, build, lead=0.4, tail=1.2, min_hold={0: 5.0})
    return s


# ============================================================ PHẦN 1 – NHẬP HÀNG & PUTAWAY (02F)
def p1_asn():
    lines = ["Khi có kế hoạch nhập, nhân viên XLCT nhận file qua email và chỉnh đúng định dạng của WMS.",
             "XLCT import file để tạo ASN,",
             "in sẵn nhãn LPN ID và giao cho kho."]

    def build(T, D):
        PRX = 1180
        lab = (f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:150px;height:96px;background:#fff;border:3px solid {INK};border-radius:8px">'
               f'<div style="font-size:20px;font-weight:900">LPN ID</div><svg width="110" height="34" viewBox="0 0 110 34">'
               + "".join(f'<rect x="{6 + i*10}" y="2" width="{3 if i % 3 else 6}" height="30" fill="{INK}"/>' for i in range(10)) + '</svg></div>')
        stack = (f'<div id="a1-lpn" class="abs" data-layout-allow-overlap style="left:{PRX-75}px;top:{FY-210}px;opacity:0">'
                 f'<div style="position:absolute;left:10px;top:-10px">{lab}</div><div style="position:absolute;left:5px;top:-5px">{lab}</div><div style="position:relative">{lab}</div></div>')
        stage = (st.floor() + K.office("a1-pl", 260) + K.printer("a1-prt", PRX, FY - 110)
                 + f'<rect x="{PRX-140}" y="{FY-70}" width="280" height="70" fill="#B98A55" stroke="{INK}" stroke-width="3"/>'
                 + figure("a1-rc", "receiver", 1660, scale=1.5, label=True, flip=True))
        body = svg_layer(stage)
        body += K.mail("a1-mail", 560, 170, "Kế hoạch nhập hàng – CXAD", "Ke_hoach_nhap.xlsx")
        body += K.sheet("a1-sh", 560, 420)
        p1 = (f'<div class="lbl">Import file kế hoạch nhập</div><div style="height:26px;border-radius:13px;background:#E3E8EF;overflow:hidden">'
              f'<div id="a1-bar" style="height:100%;width:100%;background:{C["green"]};transform-origin:0 50%"></div></div>'
              f'<div class="lbl" style="margin-top:22px">Phiếu ASN đã tạo</div>'
              f'<div id="a1-asn" class="row sel" style="opacity:0"><span><b>ASN-CXAD-0001</b> · 5 pallet</span><span style="color:{C["green"]}">✔ Đã tạo</span></div>')
        body += wms("a1-w", "Nhập hàng · ASN", [("p1", p1)], x=980, y=150, w=840, h=330)
        body += stack
        body += cbadge("a1-b1", 1, "Nhận ASN", "TC") + cbadge("a1-b2", 2, "Import vào WMS", "WMS")
        js = K.label_js("a1-pl", 0.3)
        js += st.badge_seq_js(["a1-b1", "a1-b2"], [T[0], T[1]], D - 0.2)
        js += st.appear_js("#a1-mail", T[0] + 0.3, 0.35, dy=20)
        js += f'tl.fromTo("#a1-mail-att",{{scale:1}},{{scale:1.08,duration:0.2,yoyo:true,repeat:1}},{T[0]+1.4:.2f});\n'
        js += st.appear_js("#a1-sh", T[0] + 2.0, 0.35, dy=20)
        js += K.sheet_fix_js("a1-sh", T[0] + 3.0)
        js += K.type_js("a1-pl", T[0] + 2.0, T[0] + 4.2)
        js += st.appear_js("#a1-w", T[1], 0.35, dy=20) + f'tl.set("#a1-w-p1",{{opacity:1}},{T[1]:.2f});\n'
        js += f'tl.fromTo("#a1-bar",{{scaleX:0}},{{scaleX:1,duration:1.0,ease:"power1.inOut"}},{T[1]+0.3:.2f});\n'
        js += st.pop_js("#a1-asn", T[1] + 1.4)
        js += f'tl.to("#a1-mail",{{opacity:0,duration:0.3}},{T[1]:.2f});\n'
        js += f'tl.to("#a1-sh",{{opacity:0,duration:0.3}},{T[1]+0.1:.2f});\n'
        js += f'tl.fromTo("#a1-lpn",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.6,ease:"power2.out"}},{T[2]+0.2:.2f});\n'
        js += K.label_js("a1-rc", T[2] + 0.4)
        js += f'tl.to("#a1-lpn",{{x:340,y:-60,duration:0.9,ease:"power2.inOut"}},{T[2]+1.2:.2f});\n'
        js += pose_js("a1-rc", T[2] + 1.6, {"armR": (-70, -20)}, dur=0.3)
        return body, "", js
    s = Scene("p1asn", lines, build, lead=0.5, tail=1.2, min_hold={0: 5.2, 1: 2.8, 2: 3.4})
    s.sfx = [(("T", 0, 0.3), "notification.mp3", 0.25), (("T", 1, 1.4), "ping.mp3", 0.22)]
    return s


def lpn_zoom(zid, x, y):
    return (f'<div id="{zid}" class="abs" style="left:{x}px;top:{y}px;opacity:0"><div style="background:#fff;border:5px solid {INK};border-radius:20px;padding:16px 26px;'
            f'box-shadow:0 12px 0 rgba(27,36,48,.10);text-align:center"><div style="font-size:30px;font-weight:900">LPN ID</div>'
            f'<svg width="240" height="70" viewBox="0 0 240 70">' + "".join(f'<rect x="{8 + i*11}" y="4" width="{4 if i % 3 else 7}" height="62" fill="{INK}"/>' for i in range(21))
            + f'</svg><div style="font-size:26px;font-weight:700">LPN000123</div></div></div>')


def p1_dock():
    lines = ["Xe về, nhân viên nhận hàng tạo phiếu nhập theo ASN, nhập số xe và tên tài xế.",
             "Nhân viên mang pallet tới khu nhận hàng và dán nhãn LPN ID lên pallet.",
             "Kiểm tra ngoại quan hàng, rồi chất hàng lên pallet."]

    def build(T, D):
        PX = 330
        stage = (st.floor()
                 + f'<rect x="0" y="560" width="110" height="240" fill="#D5DBE4"/><text x="60" y="545" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="26" fill="{C["muted"]}">DOCK</text>'
                 + f'<g transform="translate(1960,{FY})"><g id="d1-truck-mv">{st.truck("d1-truck", label="51C-123.45")}</g></g>'
                 + f'<g id="d1-palmv">{pallet_build("d1-pal", PX, FY, sku="2001", lpn=True)}</g>'
                 + figure("d1-rc", "receiver", 640, scale=1.5, label=True, pose=SCAN, hand_r=pda_svg("d1-rc"), extra=carry_box("d1-rc", 1.5))
                 + f'<g transform="translate(800,{FY-200})"><g id="d1-mag" opacity="0"><circle r="46" fill="#EAF6FF" fill-opacity="0.6" stroke="{INK}" stroke-width="8"/>'
                   f'<line x1="32" y1="32" x2="74" y2="74" stroke="{INK}" stroke-width="12" stroke-linecap="round"/></g></g>'
                 + f'<g transform="translate(880,{FY-280})"><g id="d1-magok" opacity="0"><circle r="26" fill="{C["green"]}"/><path d="M-11 1l7 7 14-15" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/></g></g>')
        body = svg_layer(stage)
        body += pda_popup("d1-pop", "Tạo phiếu nhập", [
            ("q1", kv("Theo ASN", "ASN-CXAD-0001") + f'<div style="font-size:28px;font-weight:700;margin-top:8px">Số xe: <b>51C-123.45</b><br>Tài xế: <b>Nguyễn Văn A</b></div>'),
        ], 1180, 150, w=640, h=210)
        body += lpn_zoom("d1-zoom", 120, 200)
        body += "".join(cbadge(f"d1-b{n}", n, t, k) for n, t, k in [(3, "Tạo phiếu nhập", "PDA"), (4, "Chuẩn bị pallet", "TC"), (5, "Chất hàng lên pallet", "TC")])
        js = 'tl.fromTo("#d1-truck-mv",{x:0},{x:-1240,duration:1.6,ease:"power2.out"},0.0);\n'
        js += K.label_js("d1-rc", 0.6)
        js += st.badge_seq_js(["d1-b3", "d1-b4", "d1-b5"], T, D - 0.2)
        js += st.appear_js("#d1-pop", T[0] + 0.6, 0.3) + f'tl.set("#d1-pop-q1",{{opacity:1}},{T[0]+0.6:.2f});\n'
        js += f'tl.to("#d1-pop",{{opacity:0,duration:0.3}},{T[1]-0.1:.2f});\n'
        js += pose_js("d1-rc", T[1], REST, dur=0.3)
        js += f'tl.to("#d1-rc-pda",{{opacity:0,duration:0.2}},{T[1]:.2f});\n'
        js += f'tl.fromTo("#d1-palmv",{{x:-460}},{{x:0,duration:1.4,ease:"power2.out"}},{T[1]+0.2:.2f});\n'
        js += st.pop_js("#d1-pal-lpn", T[1] + 1.9) + st.appear_js("#d1-zoom", T[1] + 2.1, 0.35)
        js += f'tl.to("#d1-zoom",{{opacity:0,duration:0.3}},{T[2]-0.1:.2f});\n'
        js += f'tl.fromTo("#d1-mag",{{opacity:0,x:0}},{{opacity:1,duration:0.2}},{T[2]+0.1:.2f});\n'
        js += f'tl.to("#d1-mag",{{x:180,duration:1.2,ease:"sine.inOut"}},{T[2]+0.2:.2f});\n'
        js += f'tl.to("#d1-mag",{{opacity:0,duration:0.2}},{T[2]+1.5:.2f});\n' + st.pop_js("#d1-magok", T[2] + 1.4)
        js += f'tl.to("#d1-magok",{{opacity:0,duration:0.2}},{T[2]+2.2:.2f});\n'
        t = T[2] + 2.0
        for trip in range(2):
            js += pose_js("d1-rc", t, CARRY, dur=0.25)
            js += f'tl.to("#d1-rc-box",{{opacity:1,duration:0.15}},{t+0.1:.2f});\n'
            js += f'tl.to("#d1-rc",{{x:-170,duration:0.8,ease:"none"}},{t+0.3:.2f});\n' + walk_js("d1-rc", t + 0.3, t + 1.1)
            js += f'tl.to("#d1-rc-box",{{opacity:0,duration:0.1}},{t+1.15:.2f});\n'
            for k in (2 * trip, 2 * trip + 1):
                js += st.pop_js(f"#d1-pal-c{k}", t + 1.15 + 0.12 * (k % 2), 0.3)
            js += pose_js("d1-rc", t + 1.25, REST, dur=0.2)
            if trip == 0:
                js += f'tl.to("#d1-rc",{{x:0,duration:0.7,ease:"none"}},{t+1.5:.2f});\n' + walk_js("d1-rc", t + 1.5, t + 2.2)
            t += 2.3
        return body, "", js
    s = Scene("p1dock", lines, build, lead=1.2, tail=1.0, min_hold={0: 5.0, 1: 4.6, 2: 6.4})
    s.sfx = [(0.0, "whoosh.mp3", 0.2), (("T", 1, 1.9), "click-soft.mp3", 0.3)]
    return s


def p1_recv():
    lines = ["Trên PDA: scan LPN ID, scan mã hàng, nhập số lượng,",
             "và nhập date hoặc batch theo quy tắc của mã hàng đó."]

    def build(T, D):
        PX, RX, SC = 360, 720, 1.6
        a, b = SCAN["armR"]
        tip = hand(RX, FY, SC, a, b, flip=True, extra=56)
        stage = (st.floor() + pallet_build("r1-pal", PX, FY, sku="2001", shown=True, lpn=True)
                 + figure("r1-rc", "receiver", RX, scale=SC, flip=True, pose=SCAN, hand_r=pda_svg("r1-rc"))
                 + st.laser("r1-l1", tip[0], tip[1], PX - 39, FY - 45) + st.laser("r1-l2", tip[0], tip[1], PX + 38, FY - 46))
        fields = [("Scan LPN ID", "LPN000123"), ("Scan mã hàng", "SKU 2001"), ("Số lượng", "40 thùng"), ("Date / Batch", "HSD 05/2027")]
        rows = "".join(f'<div id="r1-f{i}" style="opacity:0"><div class="lbl">{l}</div><div class="fld ok" style="margin-bottom:12px">{v}</div></div>' for i, (l, v) in enumerate(fields))
        body = svg_layer(stage) + st.pda("r1-pda", "Nhận hàng", [("s1", rows)])
        body += (f'<div id="r1-rule" class="abs" style="left:880px;top:660px;width:470px;opacity:0;background:#fff;border:4px solid {C["orange"]};border-radius:16px;'
                 f'padding:12px 18px;font-size:28px;font-weight:700">Date hay batch: theo <b>quy tắc của mã hàng</b></div>')
        body += cbadge("r1-b6", 6, "Nhận hàng", "PDA")
        js = st.appear_js("#r1-pda", 0.2, 0.35, dy=30) + f'tl.set("#r1-pda-s1",{{opacity:1}},0.2);\n'
        js += st.badge_seq_js(["r1-b6"], [T[0]], D - 0.2)
        ts = [T[0] + 0.3, T[0] + 1.6, T[0] + 2.9, T[1] + 0.2]
        for i, t in enumerate(ts):
            js += f'tl.fromTo("#r1-f{i}",{{opacity:0,x:24}},{{opacity:1,x:0,duration:0.25,ease:"power2.out"}},{t+0.2:.2f});\n'
        js += st.laser_js("r1-l1", ts[0]) + st.laser_js("r1-l2", ts[1])
        js += st.appear_js("#r1-rule", ts[3] + 0.4)
        return body, "", js
    s = Scene("p1recv", lines, build, lead=0.5, tail=1.6, min_hold={0: 4.0, 1: 3.6})
    s.sfx = [(("T", 0, 0.3), "ping.mp3", 0.25)]
    return s


def p1_put():
    lines = ["Nhận xong, tài xế xe nâng scan lại LPN của pallet đó.",
             "Hệ thống gợi ý vị trí putaway theo khu của hàng.",
             "Xe nâng đưa pallet tới đúng vị trí được gợi ý.",
             "Scan mã vị trí để xác nhận hoàn tất putaway pallet."]

    def build(T, D):
        R = K.ZRack("pu-r", 940, zone="kho", cols=3, levels=3, cw=260, lh=200)
        zone = K.zone_bg("pu-z", 880, 1040, "kho", top=110, fs=34)
        rack = R.svg(contents=[(0, 1), (1, 2), (0, 2)], cartons=[(0, 0), (1, 0), (2, 0)])
        FX = 300
        tgt_x, tgt_beam = R.slot(2, 1)
        lift = tgt_beam - (FY - 22)
        drive = tgt_x - 125 - FX
        back = drive - 170
        load = pallet_build("pu-pal", 125, -22, sku="2001", shown=True)
        fl = f'<g transform="translate({FX},{FY})"><g id="pu-fl" data-layout-allow-overlap>{st.forklift("pu-fk", label=True, load=load)}</g></g>'
        placed = f'<g id="pu-placed" opacity="0">{st.pallet("pu-pp", tgt_x, tgt_beam, lpn=True, sku="2001")}</g>'
        lab = R.label_xy(2, 1)
        las_lpn = st.laser("pu-las1", FX - 10, FY - 175, FX + 125 - 39, FY - 22 - 45)
        las_loc = st.laser("pu-las2", FX + back - 10, FY - 175, lab[0] - 40, lab[1] + 4)
        arrow = (f'<path id="pu-arrow" d="M{FX+125},{FY-200} C{FX+300},{FY-520} {tgt_x-260},{tgt_beam-360} {tgt_x},{tgt_beam-150}" fill="none" '
                 f'stroke="{C["orange"]}" stroke-width="8" stroke-dasharray="14 12" stroke-linecap="round"/>'
                 f'<rect id="pu-hl" x="{tgt_x-R.cw/2+10}" y="{tgt_beam-R.lh+34}" width="{R.cw-20}" height="{R.lh-30}" rx="8" fill="none" stroke="{C["orange"]}" stroke-width="8" opacity="0"/>')
        pop = pda_popup("pu-pop", "Putaway", [
            ("q1", kv("Đã scan LPN", "LPN000123 ✔", "Pallet vừa nhận · SKU 2001")),
            ("q2", kv("Vị trí gợi ý", f"{R.loc(2, 1)} (Khu khô)", "Theo quy tắc putaway của khu", "#C45A00")),
            ("q3", kv("Scan vị trí", f"{R.loc(2, 1)} ✔", "Hoàn tất putaway pallet")),
        ], 110, 170, w=600)
        body = svg_layer(st.floor() + zone + rack + placed + arrow + fl + las_lpn + las_loc) + pop + st.stamp("pu-done", "Đã putaway", x=640, y=420)
        body += "".join(cbadge(f"pu-b{n}", n, t, k) for n, t, k in [(7, "Putaway", "PDA"), (8, "Di chuyển pallet", "TC"), (9, "Xác nhận vị trí", "PDA")])
        js = st.badge_seq_js(["pu-b7", "pu-b8", "pu-b9"], [T[0], T[2], T[3]], D - 0.2)
        js += K.label_js("pu-fk-drv", 0.2)
        js += st.appear_js("#pu-pop", T[0] + 0.4, 0.3, dy=20)
        js += st.laser_js("pu-las1", T[0] + 0.8)
        js += swap_js("pu-pop", [(T[0] + 0.9, "q1"), (T[1], "q2"), (T[3] + 0.4, "q3")])
        js += f'tl.fromTo("#pu-arrow",{{opacity:0}},{{opacity:1,duration:0.4}},{T[1]+0.4:.2f});\n'
        js += f'tl.fromTo("#pu-hl",{{opacity:0}},{{opacity:1,duration:0.3}},{T[1]+0.9:.2f});\n'
        js += f'tl.to("#pu-arrow",{{opacity:0,duration:0.3}},{T[2]:.2f});\n'
        js += f'tl.to("#pu-fl",{{x:{drive},duration:1.6,ease:"power2.inOut"}},{T[2]:.2f});\n'
        js += f'tl.to("#pu-fk-forks",{{y:{lift},duration:1.0,ease:"power2.inOut"}},{T[2]+1.65:.2f});\n'
        js += f'tl.set("#pu-placed",{{opacity:1}},{T[2]+2.7:.2f});\ntl.set("#pu-pal",{{opacity:0}},{T[2]+2.7:.2f});\n'
        js += f'tl.to("#pu-fk-forks",{{y:0,duration:0.8,ease:"power2.inOut"}},{T[2]+2.8:.2f});\n'
        js += f'tl.to("#pu-fl",{{x:{back},duration:0.8,ease:"power2.inOut"}},{T[2]+2.8:.2f});\n'
        js += f'tl.to("#pu-hl",{{opacity:0,duration:0.3}},{T[3]+1.2:.2f});\n'
        js += st.laser_js("pu-las2", T[3] + 0.3)
        js += st.stamp_js("pu-done", T[3] + 1.0)
        return body, "", js
    s = Scene("p1put", lines, build, lead=0.5, tail=1.4, min_hold={0: 3.0, 1: 3.0, 2: 4.0, 3: 3.0})
    s.sfx = [(("T", 0, 0.8), "ping.mp3", 0.22), (("T", 3, 1.0), "chime.mp3", 0.25)]
    return s


def loop_card(text):
    return (f'<div style="display:flex;align-items:center;gap:14px;background:#fff;border:5px solid {C["orange"]};border-radius:20px;padding:14px 22px;'
            f'box-shadow:0 10px 0 rgba(27,36,48,.08)"><svg width="54" height="54" viewBox="0 0 64 64"><path d="M50 30a18 18 0 1 1-6-13" fill="none" stroke="{C["orange"]}" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M46 6v14H32" fill="none" stroke="{C["orange"]}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            f'<div style="font-size:32px;font-weight:900;line-height:1.2">{text}</div></div>')


def p1_loop():
    lines = ["Còn pallet thì quay lại bước chuẩn bị pallet.",
             "Mỗi pallet: nhận xong là putaway ngay."]

    def build(T, D):
        dec = decision("lp-d", "Còn pallet chưa nhận?", 960, 210,
                       ("Có", loop_card("Quay lại Bước 4<br><span style='font-size:24px;color:#6B7685'>Chuẩn bị pallet tiếp theo</span>"), 520),
                       ("Không", card("Bước 10: Hoàn tất nhận hàng", sub="Sang bước tiếp theo"), 480), spread=500, drop=130)
        strip = ""
        for i in range(3):
            x = 260 + i * 480
            strip += (f'<div id="lp-p{i}" class="abs" style="left:{x}px;top:660px;width:420px;opacity:0;background:#fff;border:4px solid {INK};border-radius:20px;padding:14px 18px">'
                      f'<div style="font-size:30px;font-weight:900">Pallet {i+1}</div><div style="display:flex;gap:12px;margin-top:10px">'
                      f'<div id="lp-p{i}-a" style="opacity:0;display:flex;align-items:center;gap:8px;font-size:26px;font-weight:900">{st.check(36)}Nhận</div>'
                      f'<div style="font-size:30px;font-weight:900;color:{C["blue"]}">›</div>'
                      f'<div id="lp-p{i}-b" style="opacity:0;display:flex;align-items:center;gap:8px;font-size:26px;font-weight:900">{st.check(36)}Putaway</div></div></div>')
        tag = (f'<div id="lp-ff" class="abs" style="left:1640px;top:600px;opacity:0;background:{INK};color:#fff;border-radius:14px;padding:6px 16px;'
               f'font-size:28px;font-weight:900">▶▶ ×3</div>')
        body = bg_floor() + dec + strip + tag
        js = decision_js("lp-d", 0.2, T[0] + 0.2, T[0] + 1.6)
        js += f'tl.fromTo("#lp-ff",{{opacity:0}},{{opacity:1,duration:0.2}},{T[1]:.2f});\n'
        for i in range(3):
            t = T[1] + 0.1 + i * 0.9
            js += st.appear_js(f"#lp-p{i}", t, 0.25)
            js += st.pop_js(f"#lp-p{i}-a", t + 0.3, 0.25) + st.pop_js(f"#lp-p{i}-b", t + 0.6, 0.25)
        return body, "", js
    s = Scene("p1loop", lines, build, lead=0.6, tail=1.6, min_hold={0: 3.6, 1: 3.4})
    return s


def sig_js(pid, t, dur=0.5):
    return f'tl.fromTo("#{pid}",{{strokeDashoffset:300}},{{strokeDashoffset:0,duration:{dur},ease:"power1.inOut"}},{t:.2f});\n'


def signature(sid, x, y, w=150):
    return (f'<path id="{sid}" d="M{x},{y} c12,-26 22,-26 18,0 s16,18 26,-6 s14,-20 20,4 s20,10 30,-10 s10,16 {w-94},2" fill="none" stroke="#1D4FA8" stroke-width="4" '
            f'stroke-linecap="round" stroke-dasharray="300" stroke-dashoffset="300"/>')


def p1_close():
    lines = ["Hết pallet, nhân viên nhận hàng xác nhận hoàn tất phiếu nhập.",
             "XLCT in phiếu nhập kho và chuyển các bên ký xác nhận."]

    def build(T, D):
        rc = figure("cl-rc", "receiver", 300, scale=1.6, pose={"armR": (-30, -80)}, hand_r=pda_svg("cl-rc"))
        office = K.office("cl-pl", 1000, label=False) + K.printer("cl-prt", 1500, FY - 110) + f'<rect x="1360" y="{FY-70}" width="280" height="70" fill="#B98A55" stroke="{INK}" stroke-width="3"/>'
        body = svg_layer(st.floor() + rc + f'<g id="cl-off" opacity="0">{office}</g>')
        body += pda_popup("cl-pop", "Phiếu nhập · ASN-CXAD-0001", [
            ("q1", kv("Đã nhận", "5 / 5 pallet ✔", "") + f'<div id="cl-btn" style="margin-top:14px;background:{C["green"]};color:#fff;font-weight:900;font-size:30px;text-align:center;border-radius:14px;padding:12px 0">HOÀN TẤT PHIẾU NHẬP</div>'),
        ], 480, 170, w=620, h=230)
        body += st.stamp("cl-done", "Đã hoàn tất phiếu nhập", x=520, y=470)
        sigs = "".join(f'<div class="abs" style="left:{20 + i*130}px;top:300px;width:116px;text-align:center;font-size:18px;font-weight:700;color:{C["muted"]};border-top:2px solid #C9D3E0;padding-top:4px">{n}</div>'
                       for i, n in enumerate(["Bên giao", "Bên nhận", "Kho"]))
        sig_svg = '<svg class="abs" style="left:0;top:0" width="420" height="420" viewBox="0 0 420 420">' + "".join(signature(f"cl-sg{i}", 34 + i*130, 290, 110) for i in range(3)) + '</svg>'
        body += K.doc("cl-doc", 1390, 420, "PHIẾU NHẬP KHO", w=420, h=380, fs=30, lines=5, extra=sigs + sig_svg)
        body += cbadge("cl-b10", 10, "Hoàn tất nhận hàng", "PDA") + cbadge("cl-b11", 11, "In và ký", "WMS")
        js = st.badge_seq_js(["cl-b10", "cl-b11"], T, D - 0.2)
        js += st.appear_js("#cl-pop", T[0] + 0.2, 0.3) + f'tl.set("#cl-pop-q1",{{opacity:1}},{T[0]+0.2:.2f});\n'
        js += f'tl.to("#cl-btn",{{scale:0.94,duration:0.1}},{T[0]+1.8:.2f});\ntl.to("#cl-btn",{{scale:1,duration:0.15}},{T[0]+1.9:.2f});\n'
        js += st.stamp_js("cl-done", T[0] + 2.1)
        js += f'tl.to(["#cl-pop","#cl-done"],{{opacity:0,duration:0.3}},{T[1]-0.1:.2f});\n'
        js += f'tl.to("#cl-rc",{{opacity:0,duration:0.3}},{T[1]-0.1:.2f});\n'
        js += f'tl.to("#cl-off",{{opacity:1,duration:0.35}},{T[1]:.2f});\n' + K.type_js("cl-pl", T[1] + 0.3, T[1] + 1.2)
        js += f'tl.fromTo("#cl-doc",{{opacity:0,y:260,scale:0.5}},{{opacity:1,y:0,scale:1,duration:0.8,ease:"power2.out"}},{T[1]+1.0:.2f});\n'
        for i in range(3):
            js += sig_js(f"cl-sg{i}", T[1] + 2.2 + i * 0.6)
        return body, "", js
    s = Scene("p1close", lines, build, lead=0.5, tail=1.6, min_hold={0: 3.6, 1: 4.6})
    s.sfx = [(("T", 0, 2.1), "chime.mp3", 0.25)]
    return s


def ic_pallet():
    return ic_svg(f'<rect x="6" y="48" width="52" height="8" fill="{C["pal_r"]}" stroke="{INK}" stroke-width="2"/>'
                  f'<rect x="8" y="22" width="24" height="26" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2"/><rect x="32" y="22" width="24" height="26" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2"/>'
                  f'<rect x="10" y="30" width="18" height="12" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')


def ic_loop():
    return ic_svg(f'<path d="M50 30a18 18 0 1 1-6-13" fill="none" stroke="{C["orange"]}" stroke-width="7" stroke-linecap="round"/>'
                  f'<path d="M46 6v14H32" fill="none" stroke="{C["orange"]}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')


def ic_forklift():
    return ic_svg(f'<rect x="6" y="28" width="30" height="20" rx="4" fill="#5D7290" stroke="{INK}" stroke-width="2.5"/><rect x="38" y="8" width="5" height="44" fill="#8FA3BF" stroke="{INK}" stroke-width="1.5"/>'
                  f'<rect x="43" y="46" width="16" height="4" fill="#8FA3BF" stroke="{INK}" stroke-width="1.5"/><circle cx="14" cy="52" r="6" fill="{INK}"/><circle cx="32" cy="52" r="6" fill="{INK}"/>'
                  f'<path d="M10 28V12h22v16" fill="none" stroke="{INK}" stroke-width="3"/>')


def p1_ghinho():
    return ghinho("g1", 1, [
        (ic_pallet(), "Mỗi pallet = <b>1 LPN ID</b>, in sẵn từ văn phòng", "Mỗi pallet = 1 LPN ID, in sẵn từ văn phòng"),
        (ic_loop(), "Nhận xong pallet nào, <b>putaway ngay</b> pallet đó", "Nhận xong pallet nào, putaway ngay pallet đó"),
        (ic_forklift(), "Putaway: scan LPN → đến <b>vị trí gợi ý</b> → scan vị trí", "Putaway: scan LPN, đến vị trí gợi ý, scan vị trí"),
    ])


# ============================================================ timeline
def timeline():
    seq = [cx_intro(), cx_zones(),
           chapter(1, "Nhập hàng & Putaway"), p1_asn(), p1_dock(), p1_recv(), p1_put(), p1_loop(), p1_close(), p1_ghinho()]
    from build_cxad_2 import part2, part3, part4, ending
    return seq + part2() + part3() + part4() + ending()


if __name__ == "__main__":
    limit = float(sys.argv[1]) if len(sys.argv) > 1 else None
    os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
    placed, total, kept = build_all(limit, seq=timeline(), out=OUT)
    for s, start in placed:
        print(f"{start:7.2f}  {s.D:6.2f}  {s.cid}")
    print("TOTAL", total, "sfx", len(kept))
