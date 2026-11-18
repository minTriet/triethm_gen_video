"""Parts 2–5 of the training video. Each partN() returns a list of Scene objects."""
import math
from kit import C, FONT, stick, walk_js, pose_js, REST, icon, pda_svg
import stage as st
from stage import FY, INK
from build_full import Scene, ghinho, ic_svg

CARRY = {"armL": (34, -104), "armR": (-34, 104)}
SCAN = {"armR": (-60, -10)}


def carry_box(fid, scale):
    """Carton held at chest (in figure coords, hidden). Id {fid}-box."""
    return (f'<g transform="scale({scale})"><g id="{fid}-box" opacity="0"><rect x="-30" y="-100" width="60" height="42" rx="3" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2.5"/>'
            f'<rect x="-6" y="-100" width="12" height="42" fill="#F3DDB5"/></g></g>')


def figure(fid, role, x, y=FY, scale=1.5, label=False, pose=None, hand_r="", flip=False, extra=""):
    return (f'<g transform="translate({x},{y})"><g id="{fid}">{stick(fid, role, scale, label=label, pose=pose, hand_r=hand_r, flip=flip)}{extra}</g></g>')


def hand(px, py, scale, a, b, flip=False, extra=0):
    hx, hy = st.hand_xy(px, py, scale, a, b, "R", extra)
    if flip:
        hx = px - (hx - px)
    return hx, hy


def title_card(tid, text, x=80, y=56):
    return (f'<div id="{tid}" class="abs" style="left:{x}px;top:{y}px;opacity:0"><div style="background:#fff;border:4px solid {INK};'
            f'border-radius:18px;padding:12px 28px;font-size:42px;font-weight:900">{text}</div></div>')


def svg_layer(inner, lid=""):
    i = f' id="{lid}"' if lid else ""
    return f'<svg{i} class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">{inner}</svg>'


def pallet_build(pid, cx, by, sku=None, shown=False, lpn=True):
    """Pallet with 4 cartons {pid}-c0..3 and LPN {pid}-lpn (hidden unless shown)."""
    o = 1 if shown else 0
    s = [f'<g id="{pid}"><rect x="{cx-80}" y="{by-18}" width="160" height="18" rx="2" fill="{C["pal_r"]}" stroke="{INK}" stroke-width="2.5"/>']
    for k in range(3):
        s.append(f'<rect x="{cx-72 + k*62}" y="{by-14}" width="20" height="14" fill="{C["pal_l"]}"/>')
    pos = [(cx - 76, by - 74), (cx, by - 74), (cx - 76, by - 130), (cx, by - 130)]
    for i, (x, y) in enumerate(pos):
        s.append(f'<g id="{pid}-c{i}" opacity="{o}">' + st.carton(x, y, 76, 56, label=(sku if i == 1 else None), fs=14) + "</g>")
    if not lpn:
        s.append("</g>")
        return "".join(s)
    s.append(f'<g id="{pid}-lpn" opacity="{o}"><rect x="{cx-72}" y="{by-64}" width="66" height="38" rx="3" fill="#fff" stroke="{INK}" stroke-width="2"/>'
             f'<text x="{cx-39}" y="{by-49}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="{st.LPN_FS}" fill="{INK}">LPN</text>'
             + st.barcode(cx - 66, by - 46, 54, 14) + '</g></g>')
    return "".join(s)


def pda_popup(pid, title, panels, x, y, w=560, h=150):
    inner = "".join(f'<div id="{pid}-{k}" class="abs" style="left:18px;top:14px;right:18px;opacity:0">{html}</div>' for k, html in panels)
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;opacity:0">'
            f'<div style="background:#2B3646;border:5px solid {INK};border-radius:30px;padding:14px"><div style="background:#fff;border-radius:14px;overflow:hidden">'
            f'<div style="background:{C["blue"]};color:#fff;font-weight:900;font-size:28px;padding:12px 18px">{title}</div>'
            f'<div style="position:relative;height:{h}px">{inner}</div></div></div></div>')


def kv(label, value, sub="", color=None):
    col = f"color:{color};" if color else ""
    return (f'<div style="font-size:24px;font-weight:700;color:{C["muted"]}">{label}</div>'
            f'<div style="font-size:40px;font-weight:900;{col}">{value}</div>'
            + (f'<div style="font-size:26px;font-weight:700">{sub}</div>' if sub else ""))


def swap_js(prefix, seq):
    """seq: list of (time, panel_key); shows one panel of {prefix}-{key} at a time."""
    s, prev = "", None
    for t, k in seq:
        if prev:
            s += f'tl.to("#{prefix}-{prev}",{{opacity:0,duration:0.15}},{t:.2f});\n'
        s += f'tl.fromTo("#{prefix}-{k}",{{opacity:0,x:20}},{{opacity:1,x:0,duration:0.22,ease:"power2.out"}},{t+0.08:.2f});\n'
        prev = k
    return s


# ============================================================ PART 2 – Nhập hàng & Cất hàng
def p2_dock():
    lines = ["Khi xe hàng về kho, nhân viên chất hàng lên pallet.",
             "Mỗi pallet được dán một mã LPN để định danh."]

    def build(T, D):
        PX = 330
        body = svg_layer(
            st.floor()
            + f'<rect x="0" y="560" width="110" height="240" fill="#D5DBE4"/><text x="60" y="545" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="26" fill="{C["muted"]}">DOCK</text>'
            + f'<g transform="translate(1960,{FY})"><g id="p2a-truck-mv">{st.truck("p2a-truck")}</g></g>'
            + pallet_build("p2a-pal", PX, FY, sku="1001")
            + figure("p2a-rc", "receiver", 640, scale=1.5, label=True, extra=carry_box("p2a-rc", 1.5))
        ) + f"""
    <div id="p2a-zoom" class="abs" style="left:540px;top:180px;opacity:0">
      <div style="background:#fff;border:5px solid {INK};border-radius:22px;padding:22px 34px;box-shadow:0 12px 0 rgba(27,36,48,.12)">
        <div style="font-size:30px;font-weight:700;color:{C['muted']}">Nhãn pallet</div>
        <div style="font-size:64px;font-weight:900;margin:4px 0 10px 0">LPN000123</div>
        <svg width="360" height="70" viewBox="0 0 360 70">{''.join(f'<rect x="{6 + i*13}" y="4" width="{4 if i % 3 else 7}" height="62" fill="{INK}"/>' for i in range(27))}</svg>
        <div style="font-size:30px;font-weight:700;margin-top:6px">LPN = mã định danh của pallet</div>
      </div>
    </div>
    {svg_layer(f'<path id="p2a-lead" d="M{PX-39},{FY-64} L{PX-39},{FY-200} L540,{FY-200}" fill="none" stroke="{INK}" stroke-width="4" stroke-dasharray="3 9" stroke-linecap="round" opacity="0"/>')}"""
        js = ('tl.fromTo("#p2a-truck-mv",{x:0},{x:-1340,duration:1.6,ease:"power2.out"},0.0);\n'
              'tl.fromTo("#p2a-rc-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},0.6);\n')
        t = 1.4
        for trip in range(2):
            js += pose_js("p2a-rc", t, CARRY, dur=0.25)
            js += (f'tl.fromTo("#p2a-rc-box",{{opacity:0}},{{opacity:1,duration:0.15}},{t+0.1:.2f});\n' if trip == 0
                   else f'tl.to("#p2a-rc-box",{{opacity:1,duration:0.15}},{t+0.1:.2f});\n')
            js += f'tl.to("#p2a-rc",{{x:-170,duration:1.0,ease:"none"}},{t+0.3:.2f});\n' + walk_js("p2a-rc", t + 0.3, t + 1.3)
            js += f'tl.to("#p2a-rc-box",{{opacity:0,duration:0.1}},{t+1.35:.2f});\n'
            for k in (2 * trip, 2 * trip + 1):
                js += st.pop_js(f"#p2a-pal-c{k}", t + 1.35 + 0.12 * (k % 2), 0.3)
            js += pose_js("p2a-rc", t + 1.45, REST, dur=0.2)
            if trip == 0:
                js += f'tl.to("#p2a-rc",{{x:0,duration:0.9,ease:"none"}},{t+1.7:.2f});\n' + walk_js("p2a-rc", t + 1.7, t + 2.6)
            t += 2.7
        js += st.pop_js("#p2a-pal-lpn", T[1] + 0.1, 0.35)
        js += f'tl.fromTo("#p2a-lead",{{opacity:0}},{{opacity:1,duration:0.3}},{T[1]+0.45:.2f});\n'
        js += f'tl.fromTo("#p2a-zoom",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.8)",transformOrigin:"0% 100%"}},{T[1]+0.5:.2f});\n'
        return body, "", js
    s = Scene("p2dock", lines, build, lead=0.4, tail=1.6, pre={1: 3.1})
    s.sfx = [(("T", 1, 0.1), "click-soft.mp3", 0.3)]
    return s


def p2_pda():
    lines = ["Trên PDA, nhân viên thực hiện năm bước:",
             "chọn phiếu ASN của xe đang nhập,",
             "scan mã LPN,",
             "scan mã hàng trên pallet,",
             "nhập số thùng nhận,",
             "và nhập thông tin batch, lot, ngày."]

    def build(T, D):
        PX, RX, SC = 360, 720, 1.6
        a, b = SCAN["armR"]
        tip = hand(RX, FY, SC, a, b, flip=True, extra=56)
        lpn_t, sku_t = (PX - 39, FY - 45), (PX + 38, FY - 46)
        stage_svg = (st.floor() + pallet_build("p2b-pal", PX, FY, sku="1001", shown=True)
                     + figure("p2b-rc", "receiver", RX, scale=SC, flip=True, pose=SCAN, hand_r=pda_svg("p2b-rc"))
                     + st.laser("p2b-las1", tip[0], tip[1], *lpn_t) + st.laser("p2b-las2", tip[0], tip[1], *sku_t))
        rows = [("ASN-0001", "Xe 51C-123.45 (đang nhập)"), ("ASN-0002", "Xe 51D-678.90"), ("ASN-0003", "Xe 60C-246.80")]
        p1 = '<div class="lbl">Chọn phiếu ASN</div>' + "".join(
            f'<div class="row" style="position:relative"><b>{a_}</b><br><span style="font-size:24px;color:{C["muted"]}">{b_}</span>'
            + (f'<div id="p2b-sel" style="position:absolute;left:-3px;top:-3px;right:-3px;bottom:-3px;border:4px solid {C["blue"]};border-radius:12px;background:rgba(31,95,191,.08);opacity:0"></div>'
               f'<div id="p2b-tap" style="position:absolute;right:30px;top:20px;width:56px;height:56px;border-radius:50%;border:5px solid {C["orange"]};opacity:0"></div>' if i == 0 else "")
            + '</div>' for i, (a_, b_) in enumerate(rows))

        def scanfield(label, val, sub, n):
            return (f'<div class="lbl">{label}</div><div style="position:relative"><div class="fld"> </div>'
                    f'<div id="p2b-v{n}" class="fld ok" style="position:absolute;left:0;right:0;top:0;opacity:0">{val}</div></div>'
                    + (f'<div id="p2b-s{n}" style="font-size:26px;font-weight:700;color:{C["muted"]};opacity:0">{sub}</div>' if sub else ""))
        p2 = scanfield("Scan LPN", "LPN000123", "", 2)
        p3 = scanfield("Scan mã hàng", "SKU 1001", "Sữa hộp (ví dụ)", 3)
        p4 = (scanfield("Nhập số thùng", "40 thùng", "", 4)
              + '<div class="keys">' + "".join(f"<div>{k}</div>" for k in "123456789") + '<div>⌫</div><div>0</div><div>OK</div></div>')
        p5 = ('<div class="lbl">Batch</div><div class="fld ok" style="min-height:0;font-size:30px">B2411</div>'
              '<div class="lbl">Lot</div><div class="fld ok" style="min-height:0;font-size:30px">L07</div>'
              '<div class="lbl">Ngày (theo mã hàng)</div><div class="fld ok" style="min-height:0;font-size:30px">NSX 01/11/2026</div>')
        dev = st.pda("p2b-pda", "Nhận hàng", [("s1", p1), ("s2", p2), ("s3", p3), ("s4", p4), ("s5", p5)])
        badges = "".join(st.badge(f"p2b-b{i+1}", i + 1, t) for i, t in enumerate(
            ["Chọn phiếu ASN", "Scan LPN", "Scan mã hàng", "Nhập số thùng", "Batch / Lot / Ngày"]))
        body = svg_layer(stage_svg) + dev + badges
        js = st.appear_js("#p2b-pda", T[0] + 0.1, 0.35, dy=30)
        js += st.badge_seq_js([f"p2b-b{i+1}" for i in range(5)], T[1:6], D - 0.3)
        js += st.show_panel_js("p2b-pda", None, "s1", T[1])
        js += f'tl.fromTo("#p2b-tap",{{opacity:1,scale:0.4}},{{opacity:0,scale:1.6,duration:0.5,ease:"power2.out"}},{T[1]+0.7:.2f});\n'
        js += f'tl.fromTo("#p2b-sel",{{opacity:0}},{{opacity:1,duration:0.2}},{T[1]+0.8:.2f});\n'
        js += st.show_panel_js("p2b-pda", "s1", "s2", T[2])
        js += st.laser_js("p2b-las1", T[2] + 0.5)
        js += f'tl.fromTo("#p2b-v2",{{opacity:0}},{{opacity:1,duration:0.2}},{T[2]+0.65:.2f});\n'
        js += st.show_panel_js("p2b-pda", "s2", "s3", T[3])
        js += st.laser_js("p2b-las2", T[3] + 0.5)
        js += f'tl.fromTo("#p2b-v3",{{opacity:0}},{{opacity:1,duration:0.2}},{T[3]+0.65:.2f});\n'
        js += f'tl.fromTo("#p2b-s3",{{opacity:0}},{{opacity:1,duration:0.2}},{T[3]+0.75:.2f});\n'
        js += st.show_panel_js("p2b-pda", "s3", "s4", T[4])
        js += f'tl.fromTo("#p2b-v4",{{opacity:0}},{{opacity:1,duration:0.2}},{T[4]+0.9:.2f});\n'
        js += st.show_panel_js("p2b-pda", "s4", "s5", T[5])
        return body, "", js
    s = Scene("p2pda", lines, build, lead=0.4, tail=1.0, min_hold={1: 2.4, 2: 2.4, 3: 2.4, 4: 2.4, 5: 2.8})
    s.sfx = [(("T", 2, 0.5), "ping.mp3", 0.25)]
    return s


def date_card(cid, x, name, nsx, hsd, note, top=170, w=500):
    def fld(lbl, on, fid):
        if on:
            return (f'<div style="font-size:26px;font-weight:700;color:{C["muted"]};margin:10px 0 6px">{lbl}</div>'
                    f'<div id="{fid}" style="border:4px solid {C["orange"]};background:#FFF7EE;border-radius:12px;padding:10px 14px;font-size:30px;font-weight:900">__/__/____</div>')
        return (f'<div style="font-size:26px;font-weight:700;color:#A9B2BF;margin:10px 0 6px">{lbl}</div>'
                f'<div style="border:4px solid #D5DBE4;background:#F1F3F6;border-radius:12px;padding:10px 14px;font-size:30px;font-weight:900;color:#A9B2BF">không nhập</div>')
    return (f'<div id="{cid}" class="abs" style="left:{x}px;top:{top}px;width:{w}px;opacity:0">'
            f'<div style="background:#2B3646;border:5px solid {INK};border-radius:34px;padding:18px">'
            f'<div style="background:#fff;border-radius:16px;overflow:hidden">'
            f'<div style="background:{C["blue"]};color:#fff;font-weight:900;font-size:30px;padding:14px 20px">{name}</div>'
            f'<div style="padding:8px 20px 22px 20px">{fld("Ngày sản xuất (NSX)", nsx, cid + "-f1")}{fld("Hạn sử dụng (HSD)", hsd, cid + "-f2")}</div></div></div>'
            f'<div style="margin-top:16px;text-align:center;font-size:34px;font-weight:900">{note}</div></div>')


def p2_dates():
    lines = ["Lưu ý: mỗi mã hàng có yêu cầu nhập ngày khác nhau.",
             "Có mã chỉ nhập ngày sản xuất,",
             "có mã chỉ nhập hạn sử dụng,",
             "và có mã không được nhập ngày.",
             "PDA sẽ hiển thị đúng ô cần nhập."]

    def build(T, D):
        body = (title_card("p2c-title", "Nhập ngày theo từng mã hàng")
                + date_card("p2c-a", 120, "Mã hàng A", True, False, "Chỉ nhập NSX")
                + date_card("p2c-b", 710, "Mã hàng B", False, True, "Chỉ nhập HSD")
                + date_card("p2c-c", 1300, "Mã hàng C", False, False, "Không nhập ngày"))
        js = st.appear_js("#p2c-title", T[0])
        for i, k in enumerate("abc"):
            js += f'tl.fromTo("#p2c-{k}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},{T[i+1]+0.05:.2f});\n'
        js += f'tl.fromTo(["#p2c-a-f1","#p2c-b-f2"],{{boxShadow:"0 0 0 0px rgba(242,140,30,0)"}},{{boxShadow:"0 0 0 12px rgba(242,140,30,0.35)",duration:0.5,ease:"power2.out"}},{T[4]+0.2:.2f});\n'
        return body, "", js
    return Scene("p2dates", lines, build, lead=0.4, tail=1.2)


def p2_repeat():
    lines = ["Lặp lại cho đến khi nhận đủ toàn bộ phiếu ASN."]

    def build(T, D):
        steps = ["Scan LPN", "Scan mã hàng", "Nhập số thùng", "Batch / Lot / Ngày"]
        cx, cy, r = 560, 440, 265
        chips = ""
        for i, s_ in enumerate(steps):
            ang = math.radians(-90 + i * 90)
            x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
            chips += (f'<div class="abs" style="left:{x-160:.0f}px;top:{y-32:.0f}px;width:320px;text-align:center">'
                      f'<span style="display:inline-block;background:#fff;border:4px solid {INK};border-radius:16px;padding:8px 18px;font-size:30px;font-weight:900">{s_}</span></div>')
        ring = svg_layer(f'<g id="p2d-ring"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["blue"]}" stroke-width="10" stroke-dasharray="40 22"/></g>'
                         f'<text x="{cx}" y="{cy+16}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="46" fill="{INK}">Lặp lại</text>')
        counts = "".join(f'<div id="p2d-n{i}" class="abs" style="left:0;top:0;opacity:{1 if i == 0 else 0}">{n}/120 thùng</div>' for i, n in enumerate((0, 40, 80, 120)))
        prog = f"""
    <div class="abs" style="left:1080px;top:250px;width:720px;background:#fff;border:4px solid {INK};border-radius:24px;padding:28px 34px">
      <div style="font-size:30px;font-weight:700;color:{C['muted']}">Phiếu nhập (ví dụ)</div>
      <div style="font-size:52px;font-weight:900">ASN-0001</div>
      <div style="height:40px;border-radius:20px;background:#E3E8EF;margin:18px 0;overflow:hidden"><div id="p2d-bar" style="height:100%;width:100%;background:{C['green']};transform-origin:0% 50%"></div></div>
      <div style="position:relative;height:56px;font-size:42px;font-weight:900">{counts}</div>
    </div>
    {st.stamp("p2d-done", "Đã nhận đủ ASN", x=1130, y=600)}"""
        body = ring + chips + prog
        js = f'tl.fromTo("#p2d-ring",{{rotation:0}},{{rotation:360,duration:{D-0.4:.2f},ease:"none",svgOrigin:"{cx} {cy}"}},0.2);\n'
        fill = T[0] + 2.6
        js += f'tl.fromTo("#p2d-bar",{{scaleX:0}},{{scaleX:1,duration:{fill:.2f},ease:"power1.inOut"}},0.3);\n'
        for i in range(1, 4):
            tt = 0.3 + fill * i / 3
            js += f'tl.set("#p2d-n{i-1}",{{opacity:0}},{tt:.2f});\ntl.set("#p2d-n{i}",{{opacity:1}},{tt:.2f});\n'
        js += st.stamp_js("p2d-done", T[0] + 3.0)
        return body, "", js
    s = Scene("p2repeat", lines, build, lead=0.4, tail=1.2, min_hold={0: 3.6})
    s.sfx = [(("T", 0, 3.0), "chime.mp3", 0.25)]
    return s


def p2_putaway():
    lines = ["Tiếp theo là cất hàng.",
             "Tài xế xe nâng scan LPN.",
             "Hệ thống dựa vào mã hàng trên pallet",
             "và chỉ đến vị trí primary cố định của mã đó.",
             "Xe nâng đặt pallet phía trên hoặc gần vị trí này,",
             "rồi scan vị trí để xác nhận."]

    def build(T, D):
        R = st.Rack("p2r", 900, cols=3, levels=3, cw=260, lh=200, aisle="A")
        rack = R.svg(contents={(1, 0): "cartons", (2, 0): "cartons", (1, 1): "pallet", (2, 2): "pallet", (0, 0): "cartons"},
                     tags={(0, 0): "SKU 1001"})
        FX = 330
        tgt_x, tgt_beam = R.slot(0, 1)
        lift = tgt_beam - (FY - 22)
        drive = tgt_x - 125 - FX
        back = drive - 170
        load = pallet_build("p2e-pal", 125, -22, sku="1001", shown=True)
        fl = f'<g transform="translate({FX},{FY})"><g id="p2e-fl">{st.forklift("p2e-fk", label=True, load=load)}</g></g>'
        placed = f'<g id="p2e-placed" opacity="0">{st.pallet("p2e-pp", tgt_x, tgt_beam, lpn=True, sku="1001")}</g>'
        lab = R.label_xy(0, 1)
        prim = R.slot(0, 0)
        las_lpn = st.laser("p2e-las1", FX - 10, FY - 175, FX + 125 - 39, FY - 22 - 45)
        las_loc = st.laser("p2e-las2", FX + back - 10, FY - 175, lab[0] - 40, lab[1] + 4)
        arrow = (f'<path id="p2e-arrow" d="M{FX+125},{FY-200} C{FX+260},{FY-460} {prim[0]-220},{prim[1]-330} {prim[0]},{prim[1]-170}" fill="none" '
                 f'stroke="{C["orange"]}" stroke-width="8" stroke-dasharray="1100" stroke-dashoffset="1100" stroke-linecap="round"/>'
                 f'<rect id="p2e-hl" x="{prim[0]-R.cw/2+8}" y="{prim[1]-R.lh+34}" width="{R.cw-16}" height="{R.lh-30}" rx="8" fill="none" stroke="{C["orange"]}" stroke-width="8" opacity="0"/>')
        pop = pda_popup("p2e-pop", "Cất hàng (Putaway)", [
            ("q1", kv("Đã scan LPN", "LPN000123 ✔", "Mã hàng trên pallet: SKU 1001")),
            ("q2", kv("Vị trí đề xuất", f"{R.loc(0, 0)} (Primary)", "Vị trí cố định của SKU 1001", "#C45A00")),
            ("q3", kv("Scan vị trí", f"{R.loc(0, 1)} ✔", "Đặt phía trên vị trí primary")),
        ], 130, 140)
        body = svg_layer(st.floor() + rack + st.zone_labels(R, "p2r", 1700) + placed + arrow + fl + las_lpn + las_loc) \
            + pop + st.stamp("p2e-done", "Đã cất hàng", x=760, y=150)
        js = st.appear_js("#p2e-pop", T[1], 0.3, dy=20)
        js += 'tl.fromTo("#p2e-fk-drv-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},%.2f);\n' % max(0.1, T[0])
        js += st.laser_js("p2e-las1", T[1] + 0.4)
        js += swap_js("p2e-pop", [(T[1] + 0.45, "q1"), (T[3], "q2"), (T[5] + 0.3, "q3")])
        js += st.pop_js("#p2r-tag-c0-l0", T[2] + 0.2)
        js += f'tl.to("#p2e-arrow",{{strokeDashoffset:0,duration:0.9,ease:"power2.inOut"}},{T[3]+0.3:.2f});\n'
        js += f'tl.fromTo("#p2e-hl",{{opacity:0}},{{opacity:1,duration:0.3}},{T[3]+1.0:.2f});\n'
        t4 = T[4]
        js += f'tl.to("#p2e-arrow",{{opacity:0,duration:0.3}},{t4:.2f});\n'
        js += f'tl.to("#p2e-fl",{{x:{drive},duration:1.4,ease:"power2.inOut"}},{t4:.2f});\n'
        js += f'tl.to("#p2e-fk-forks",{{y:{lift},duration:1.0,ease:"power2.inOut"}},{t4+1.45:.2f});\n'
        js += f'tl.set("#p2e-placed",{{opacity:1}},{t4+2.5:.2f});\ntl.set("#p2e-pal",{{opacity:0}},{t4+2.5:.2f});\n'
        js += f'tl.to("#p2e-fk-forks",{{y:0,duration:0.8,ease:"power2.inOut"}},{t4+2.6:.2f});\n'
        js += f'tl.to("#p2e-fl",{{x:{back},duration:0.8,ease:"power2.inOut"}},{t4+2.6:.2f});\n'
        js += st.laser_js("p2e-las2", T[5] + 0.3)
        js += st.stamp_js("p2e-done", T[5] + 0.9)
        return body, "", js
    s = Scene("p2put", lines, build, lead=0.5, tail=1.4, min_hold={1: 2.0, 4: 3.6, 5: 2.6})
    s.sfx = [(("T", 5, 0.9), "chime.mp3", 0.25)]
    return s


def ic_pallet():
    return ic_svg(f'<rect x="6" y="48" width="52" height="8" fill="{C["pal_r"]}" stroke="{INK}" stroke-width="2"/>'
                  f'<rect x="8" y="22" width="24" height="26" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2"/><rect x="32" y="22" width="24" height="26" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2"/>'
                  f'<rect x="10" y="30" width="18" height="12" fill="#fff" stroke="{INK}" stroke-width="1.5"/>')


def ic_calendar():
    return ic_svg(f'<rect x="8" y="12" width="48" height="44" rx="6" fill="#fff" stroke="{INK}" stroke-width="3"/><rect x="8" y="12" width="48" height="12" rx="4" fill="{C["orange"]}"/>'
                  f'<path d="M20 6v12M44 6v12" stroke="{INK}" stroke-width="3" stroke-linecap="round"/><path d="M20 38l7 7 14-14" fill="none" stroke="{C["green"]}" stroke-width="5" stroke-linecap="round"/>')


def ic_forklift():
    return ic_svg(f'<rect x="6" y="28" width="30" height="20" rx="4" fill="#5D7290" stroke="{INK}" stroke-width="2.5"/><rect x="38" y="8" width="5" height="44" fill="#8FA3BF" stroke="{INK}" stroke-width="1.5"/>'
                  f'<rect x="43" y="46" width="16" height="4" fill="#8FA3BF" stroke="{INK}" stroke-width="1.5"/><circle cx="14" cy="52" r="6" fill="{INK}"/><circle cx="32" cy="52" r="6" fill="{INK}"/>'
                  f'<path d="M10 28V12h22v16" fill="none" stroke="{INK}" stroke-width="3"/>')


def part2():
    return [p2_dock(), p2_pda(), p2_dates(), p2_repeat(), p2_putaway(),
            ghinho("g2", 2, [
                (ic_pallet(), "Mỗi pallet = <b>1 LPN</b>", "Mỗi pallet = 1 LPN"),
                (ic_calendar(), "Nhập ngày theo <b>đúng yêu cầu</b> từng mã hàng", "Nhập ngày theo đúng yêu cầu từng mã hàng"),
                (ic_forklift(), "Putaway: scan LPN → đi đến vị trí → <b>scan vị trí</b> xác nhận", "Putaway: scan LPN, đi đến vị trí, scan vị trí xác nhận"),
            ])]


# ============================================================ PART 3 – Đơn hàng, Allocate & Châm hàng
def store_svg(x, y, code):
    return (f'<g transform="translate({x},{y})"><rect x="-70" y="-60" width="140" height="96" fill="#fff" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M-82,-60 L82,-60 L72,-96 L-72,-96 Z" fill="{C["orange"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            + "".join(f'<rect x="{-72 + i*36}" y="-96" width="18" height="36" fill="#fff" opacity="0.7"/>' for i in range(4))
            + f'<rect x="-22" y="-20" width="44" height="56" fill="{C["blue"]}" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="-60" y="-44" width="30" height="26" fill="#BFD8F5" stroke="{INK}" stroke-width="2"/><rect x="30" y="-44" width="30" height="26" fill="#BFD8F5" stroke="{INK}" stroke-width="2"/>'
            f'<text x="0" y="74" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="26" fill="{INK}">{code}</text></g>')


def doc_html(did, x, y, label="DO", w=86, h=104, color=None):
    color = color or C["blue"]
    return (f'<div id="{did}" class="abs" style="left:{x-w/2:.0f}px;top:{y-h/2:.0f}px;width:{w}px;height:{h}px;opacity:0">'
            f'<div style="width:100%;height:100%;background:#fff;border:3px solid {INK};border-radius:8px;overflow:hidden">'
            f'<div style="background:{color};color:#fff;font-weight:900;font-size:24px;text-align:center;padding:4px 0">{label}</div>'
            f'<div style="margin:10px 10px 0;height:6px;background:#D5DBE4;border-radius:3px"></div><div style="margin:8px 10px 0;height:6px;width:60%;background:#D5DBE4;border-radius:3px"></div>'
            f'<div style="margin:8px 10px 0;height:6px;background:#D5DBE4;border-radius:3px"></div></div></div>')


def cloud_svg(cx, cy):
    return (f'<g id="p3a-cloud"><path d="M{cx-170},{cy+60} a70,70 0 0 1 20,-136 a95,95 0 0 1 170,-30 a80,80 0 0 1 130,56 a60,60 0 0 1 -10,110 Z" '
            f'fill="#EAF1FC" stroke="{C["blue"]}" stroke-width="7" stroke-linejoin="round"/>'
            f'<text x="{cx}" y="{cy+30}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="72" fill="{C["blue"]}">WMS</text></g>')


def p3_do():
    lines = ["Mỗi ngày, các cửa hàng tự động đặt hàng và gửi đơn DO lên hệ thống."]
    stores = [(220, 330, "CH-0125"), (440, 330, "CH-0311"), (660, 330, "CH-0420"),
              (220, 600, "CH-0533"), (440, 600, "CH-0647"), (660, 600, "CH-0702")]
    CX, CY = 1430, 430

    def build(T, D):
        body = svg_layer("".join(store_svg(x, y, c) for x, y, c in stores) + cloud_svg(CX, CY)
                         + f'<path d="M790,460 L1180,440" stroke="{C["blue"]}" stroke-width="5" stroke-dasharray="4 14" stroke-linecap="round" fill="none" opacity="0.5"/>')
        body += "".join(doc_html(f"p3a-d{i}", x, y - 30) for i, (x, y, _) in enumerate(stores))
        body += (f'<div id="p3a-clock" class="abs" style="left:80px;top:56px;opacity:0"><div style="display:flex;align-items:center;gap:16px;background:#fff;border:4px solid {INK};'
                 f'border-radius:18px;padding:10px 26px;font-size:40px;font-weight:900">'
                 f'<svg width="54" height="54" viewBox="0 0 64 64"><circle cx="32" cy="32" r="27" fill="#fff" stroke="{INK}" stroke-width="5"/><path d="M32 16v17l11 7" stroke="{C["orange"]}" stroke-width="6" stroke-linecap="round" fill="none"/></svg>'
                 f'Mỗi ngày – tự động</div></div>'
                 f'<div id="p3a-count" class="abs" style="left:{CX-120}px;top:{CY+110}px;width:240px;text-align:center;opacity:0">'
                 f'<span style="display:inline-block;background:{C["blue"]};color:#fff;border-radius:16px;padding:8px 24px;font-size:38px;font-weight:900">6 đơn DO</span></div>')
        js = st.appear_js("#p3a-clock", 0.2)
        for i, (x, y, _) in enumerate(stores):
            t = T[0] + 0.3 + i * 0.28
            js += (f'tl.fromTo("#p3a-d{i}",{{opacity:0,x:0,y:0,scale:0.6}},{{opacity:1,scale:1,duration:0.2}},{t:.2f});\n'
                   f'tl.to("#p3a-d{i}",{{x:{CX-x},y:{CY-(y-30)},scale:0.5,duration:0.9,ease:"power2.in"}},{t+0.2:.2f});\n'
                   f'tl.to("#p3a-d{i}",{{opacity:0,duration:0.1}},{t+1.1:.2f});\n')
        js += st.pop_js("#p3a-count", T[0] + 0.3 + 6 * 0.28 + 0.9)
        return body, "", js
    s = Scene("p3do", lines, build, lead=0.5, tail=1.2, min_hold={0: 4.0})
    return s


def desk_svg(x, y=FY):
    return (f'<g transform="translate({x},{y})">'
            f'<rect x="80" y="-178" width="96" height="66" rx="6" fill="#2B3646" stroke="{INK}" stroke-width="3"/><rect x="87" y="-171" width="82" height="52" rx="3" fill="#7FD3FF"/>'
            f'<rect x="122" y="-112" width="12" height="16" fill="#2B3646"/>'
            f'<rect x="-110" y="-98" width="320" height="18" rx="4" fill="#C9965A" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-90" y="-80" width="280" height="80" fill="#B98A55" stroke="{INK}" stroke-width="3"/></g>')


def p3_routes():
    lines = ["Nhân viên kho gom các DO theo tuyến đường.",
             "Mỗi tuyến được đánh số từ một đến n,",
             "đúng theo thứ tự xuất hàng của tuyến đó."]
    lanes = [(1, 250), (2, 450), (3, 650)]
    LX = 1120

    def build(T, D):
        planner = f'<g transform="translate(250,{FY - 40})">{stick("p3b-pl", "planner", 1.5, label=True, pose={"armL": (22, -70), "armR": (-22, 70)})}</g>'
        lane_svg = ""
        for n, y in lanes:
            lab = "Tuyến n" if n == 3 else f"Tuyến {n}"
            lane_svg += (f'<g><rect x="{LX}" y="{y-70}" width="620" height="140" rx="20" fill="#fff" stroke="{INK}" stroke-width="3.5"/>'
                         f'<g id="p3b-ln{n}" opacity="0"><rect x="{LX+14}" y="{y-56}" width="150" height="112" rx="14" fill="{C["blue"]}"/>'
                         f'<text x="{LX+89}" y="{y+14}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="34" fill="#fff">{lab}</text></g>'
                         f'<g transform="translate({LX+560},{y+40}) scale(0.28)">{st.truck("p3b-tk" + str(n))}</g></g>')
        order = (f'<g id="p3b-order" opacity="0"><line x1="1790" y1="200" x2="1790" y2="700" stroke="{C["orange"]}" stroke-width="8" stroke-linecap="round"/>'
                 f'<path d="M1772,680 L1790,712 L1808,680" fill="none" stroke="{C["orange"]}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></g>')
        body = svg_layer(st.floor() + desk_svg(250) + planner + lane_svg + order)
        body += (f'<div id="p3b-o1" class="abs" style="left:1600px;top:120px;width:300px;text-align:right;opacity:0;font-size:30px;font-weight:900;color:#C45A00">Xuất trước</div>'
                 f'<div id="p3b-o2" class="abs" style="left:1600px;top:722px;width:300px;text-align:right;opacity:0;font-size:30px;font-weight:900;color:#C45A00">Xuất sau</div>')
        docs, js = "", ""
        k = 0
        for n, y in lanes:
            for j in range(3):
                sx, sy = 560 + (k % 3) * 120 + (k // 3) * 30, 300 + (k // 3) * 150
                docs += doc_html(f"p3b-d{k}", sx, sy, w=80, h=96)
                tx, ty = LX + 220 + j * 100, y
                t = T[0] + 0.2 + k * 0.18
                js += (f'tl.fromTo("#p3b-d{k}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.2}},{0.2 + k*0.05:.2f});\n'
                       f'tl.to("#p3b-d{k}",{{x:{tx-sx},y:{ty-sy},scale:0.8,duration:0.6,ease:"power2.inOut"}},{t:.2f});\n')
                k += 1
        body += docs
        js += 'tl.fromTo("#p3b-pl-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},0.3);\n'
        for i, (n, y) in enumerate(lanes):
            js += st.pop_js(f"#p3b-ln{n}", T[1] + 0.2 + i * 0.35)
        js += f'tl.fromTo("#p3b-order",{{opacity:0}},{{opacity:1,duration:0.3}},{T[2]+0.1:.2f});\n'
        js += st.appear_js("#p3b-o1", T[2] + 0.2) + st.appear_js("#p3b-o2", T[2] + 0.5)
        return body, "", js
    return Scene("p3routes", lines, build, lead=0.6, tail=1.2, min_hold={0: 2.8})


def cursor_svg(cid):
    return (f'<g id="{cid}" opacity="0"><path d="M0,0 L0,46 L12,34 L22,56 L32,51 L22,30 L38,30 Z" fill="#fff" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/></g>')


def p3_alloc():
    lines = ["Sau đó, nhân viên bấm Allocate để hệ thống phân bổ tồn kho.",
             "Hệ thống chỉ lấy hàng ở vị trí primary."]

    def build(T, D):
        R = st.Rack("p3c", 860, cols=3, levels=3, cw=280, lh=200)
        rack = R.svg(contents={(c, k): ("cartons" if k == 0 else "pallet") for c in range(3) for k in range(3)})
        top = R.beam_y(2) - R.lh + 20
        dim = (f'<g id="p3c-dim" opacity="0"><rect x="{R.x0-10}" y="{top}" width="{R.cols*R.cw+20}" height="{R.beam_y(0)-top-4}" fill="{C["ground"]}" opacity="0.75"/>'
               f'<g transform="translate({R.x0 + R.cols*R.cw/2},{(top + R.beam_y(0))/2})"><rect x="-210" y="-40" width="420" height="80" rx="18" fill="#fff" stroke="{C["red"]}" stroke-width="5"/>'
               f'<text x="0" y="14" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="38" fill="{C["red"]}">Reserved: không pick</text></g></g>')
        arrows = ""
        for c in range(3):
            x, y = R.slot(c, 0)
            arrows += (f'<path id="p3c-a{c}" d="M560,330 C700,{330 + c*20} {x-80},{y-240} {x},{y-130}" fill="none" stroke="{C["orange"]}" stroke-width="7" '
                       f'stroke-linecap="round" stroke-dasharray="900" stroke-dashoffset="900"/>')
        body = svg_layer(st.floor() + rack + st.zone_labels(R, "p3c", 1700) + dim + arrows)
        body += (f'<div class="abs" style="left:120px;top:150px;width:460px;background:#fff;border:4px solid {INK};border-radius:22px;padding:24px 28px">'
                 f'<div style="font-size:28px;font-weight:700;color:{C["muted"]}">Tuyến 1 · 3 đơn DO</div>'
                 f'<div style="font-size:40px;font-weight:900;margin:6px 0 18px">Phân bổ tồn kho</div>'
                 f'<div id="p3c-btn" style="background:{C["blue"]};color:#fff;font-size:44px;font-weight:900;text-align:center;border-radius:16px;padding:16px 0;border:4px solid {INK}">ALLOCATE</div></div>'
                 + svg_layer(f'<g transform="translate(420,600)">{cursor_svg("p3c-cur")}</g>'))
        js = (f'tl.fromTo("#p3c-cur",{{opacity:0,x:0,y:0}},{{opacity:1,duration:0.2}},{T[0]+0.2:.2f});\n'
              f'tl.to("#p3c-cur",{{x:-40,y:-210,duration:0.8,ease:"power2.inOut"}},{T[0]+0.4:.2f});\n'
              f'tl.to("#p3c-btn",{{scale:0.92,duration:0.1,ease:"power2.in"}},{T[0]+1.3:.2f});\n'
              f'tl.to("#p3c-btn",{{scale:1,backgroundColor:"{C["green"]}",duration:0.2,ease:"power2.out"}},{T[0]+1.4:.2f});\n'
              f'tl.to("#p3c-cur",{{opacity:0,duration:0.3}},{T[0]+2.0:.2f});\n')
        js += f'tl.fromTo("#p3c-dim",{{opacity:0}},{{opacity:1,duration:0.4}},{T[1]:.2f});\n'
        for c in range(3):
            js += f'tl.to("#p3c-a{c}",{{strokeDashoffset:0,duration:0.7,ease:"power2.inOut"}},{T[0]+1.8 + c*0.2:.2f});\n'
        return body, "", js
    s = Scene("p3alloc", lines, build, lead=0.4, tail=1.4, min_hold={0: 3.4})
    s.sfx = [(("T", 0, 1.3), "click-soft.mp3", 0.3)]
    return s


def gauge_html(gid, x, y, loc="A-01-01", sku="SKU 1001"):
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:520px;background:#fff;border:4px solid {INK};border-radius:22px;padding:22px 28px">'
            f'<div style="font-size:28px;font-weight:700;color:{C["muted"]}">{loc} · {sku}</div>'
            f'<div style="font-size:38px;font-weight:900;margin:4px 0 14px">Cần 10 thùng</div>'
            f'<div style="height:40px;border-radius:20px;background:#E3E8EF;overflow:hidden;position:relative">'
            f'<div id="{gid}-red" style="position:absolute;left:0;top:0;bottom:0;width:40%;background:{C["red"]}"></div>'
            f'<div id="{gid}-grn" style="position:absolute;left:0;top:0;bottom:0;width:100%;background:{C["green"]};transform-origin:0% 50%;opacity:0"></div></div>'
            f'<div style="position:relative;height:54px;margin-top:10px;font-size:40px;font-weight:900">'
            f'<div id="{gid}-t1" class="abs" style="left:0;top:0;color:{C["red"]}">Có 4 thùng – thiếu</div>'
            f'<div id="{gid}-t2" class="abs" style="left:0;top:0;color:{C["green"]};opacity:0">Đủ hàng ✔</div></div></div>')


def p3_short():
    lines = ["Nếu tồn tại vị trí primary không đủ,",
             "hệ thống sẽ tạo lệnh châm hàng, đưa hàng từ khu reserved xuống."]

    def build(T, D):
        R = st.Rack("p3d", 260, cols=1, levels=3, cw=380, lh=210)
        rack = R.svg(contents={(0, 2): "pallet", (0, 1): "pallet"})
        x, by = R.slot(0, 0)
        low = "".join(st.carton(x - 150 + i*76, by - 56, 72, 56) for i in range(2))
        res = R.slot(0, 2)
        arrow = (f'<path id="p3d-arr" d="M{res[0]+220},{res[1]-80} C{res[0]+330},{res[1]+40} {x+330},{by-200} {x+200},{by-60}" fill="none" stroke="{C["orange"]}" '
                 f'stroke-width="8" stroke-linecap="round" stroke-dasharray="800" stroke-dashoffset="800"/>')
        warn = (f'<g id="p3d-warn" opacity="0" transform="translate({x+120},{by-150})"><path d="M0,-44 L44,34 L-44,34 Z" fill="#FFD23F" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<rect x="-4" y="-16" width="8" height="28" rx="3" fill="{INK}"/><circle cx="0" cy="22" r="5" fill="{INK}"/></g>')
        body = svg_layer(st.floor() + rack + f'<g id="p3d-low">{low}</g>' + arrow + warn)
        body += gauge_html("p3d-g", 1080, 150)
        body += (f'<div id="p3d-task" class="abs" style="left:1080px;top:470px;width:560px;opacity:0">'
                 f'<div style="background:#fff;border:5px solid {C["orange"]};border-radius:22px;padding:22px 28px">'
                 f'<div style="font-size:40px;font-weight:900;color:#C45A00">Lệnh châm hàng</div>'
                 f'<div style="font-size:32px;font-weight:700;margin-top:10px">Từ: <b>{R.loc(0, 2)}</b> (Reserved)</div>'
                 f'<div style="font-size:32px;font-weight:700">Đến: <b>{R.loc(0, 0)}</b> (Primary)</div></div></div>')
        js = st.pop_js("#p3d-warn", T[0] + 0.6)
        js += st.pop_js("#p3d-task", T[1] + 0.3, 0.4)
        js += f'tl.to("#p3d-arr",{{strokeDashoffset:0,duration:0.9,ease:"power2.inOut"}},{T[1]+0.6:.2f});\n'
        return body, "", js
    s = Scene("p3short", lines, build, lead=0.4, tail=1.4)
    s.sfx = [(("T", 0, 0.6), "notification.mp3", 0.25)]
    return s


def p3_repl():
    lines = ["Tài xế xe nâng xem lệnh,",
             "đến đúng vị trí reserved và scan LPN.",
             "Sau đó mang hàng xuống primary,",
             "và scan vị trí pick face để xác nhận đã châm."]

    def build(T, D):
        R = st.Rack("p3e", 760, cols=2, levels=3, cw=300, lh=200)
        rack = R.svg(contents={(1, 0): "cartons", (1, 1): "pallet", (1, 2): "pallet"})
        sx, sb = R.slot(0, 2)
        px, pb = R.slot(0, 0)
        FX0 = 230
        fx = sx - 125                          # forks centred on column 0
        res_pal = f'<g id="p3e-respal">{st.pallet("p3e-rp", sx, sb, lpn=True, sku="1001")}</g>'
        low = f'<g id="p3e-low">' + "".join(st.carton(px - 112 + i*76, pb - 56, 72, 56) for i in range(2)) + "</g>"
        full = (f'<g id="p3e-full" opacity="0">' + "".join(st.carton(px - 112 + i*76, pb - 56, 72, 56) for i in range(3))
                + "".join(st.carton(px - 74 + i*76, pb - 112, 72, 56) for i in range(2)) + "</g>")
        load = f'<g id="p3e-load" opacity="0">{st.pallet("p3e-lp", 125, -22, lpn=True, sku="1001")}</g>'
        fl = f'<g transform="translate({FX0},{FY})"><g id="p3e-fl">{st.forklift("p3e-fk", label=True, load=load)}</g></g>'
        lift_top = sb - (FY - 22)
        las1 = st.laser("p3e-las1", fx - 10, FY - 175 + lift_top * 0, sx - 39, sb - 45)
        lab = R.label_xy(0, 0)
        las2 = st.laser("p3e-las2", fx - 10, FY - 175, lab[0] - 40, lab[1] + 4)
        body = svg_layer(st.floor() + rack + st.zone_labels(R, "p3e", 1690) + res_pal + low + full + fl + las1 + las2)
        body += pda_popup("p3e-pop", "Lệnh châm hàng", [
            ("q1", kv("Lấy từ (Reserved)", R.loc(0, 2), f"Đưa xuống: {R.loc(0, 0)} (Primary)", "#C45A00")),
            ("q2", kv("Đã scan LPN", "LPN000456 ✔", "SKU 1001")),
            ("q3", kv("Scan vị trí pick face", f"{R.loc(0, 0)} ✔", "Đã châm hàng")),
        ], 120, 200, w=520)
        body += "".join(st.badge(f"p3e-b{i+1}", i + 1, t) for i, t in enumerate(
            ["Xem lệnh trên PDA", "Đến Reserved, scan LPN", "Mang hàng xuống Primary", "Scan vị trí pick face"]))
        body += gauge_html("p3e-g", 1340, 140)
        js = st.badge_seq_js([f"p3e-b{i+1}" for i in range(4)], T, D - 0.3)
        js += st.appear_js("#p3e-pop", T[0] + 0.1)
        js += swap_js("p3e-pop", [(T[0] + 0.2, "q1"), (T[1] + 2.0, "q2"), (T[3] + 0.9, "q3")])
        js += 'tl.fromTo("#p3e-fk-drv-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},0.3);\n'
        js += f'tl.to("#p3e-fl",{{x:{fx-FX0},duration:1.2,ease:"power2.inOut"}},{T[1]:.2f});\n'
        js += f'tl.to("#p3e-fk-forks",{{y:{lift_top},duration:0.9,ease:"power2.inOut"}},{T[1]+1.0:.2f});\n'
        js += f'tl.set("#p3e-las1",{{y:0}},0);\n' + st.laser_js("p3e-las1", T[1] + 1.95)
        t2 = T[2]
        js += f'tl.set("#p3e-respal",{{opacity:0}},{t2+0.1:.2f});\ntl.set("#p3e-load",{{opacity:1}},{t2+0.1:.2f});\n'
        js += f'tl.to("#p3e-fk-forks",{{y:0,duration:1.1,ease:"power2.inOut"}},{t2+0.2:.2f});\n'
        js += f'tl.to("#p3e-low",{{opacity:0,duration:0.2}},{t2+1.5:.2f});\n'
        js += f'tl.fromTo("#p3e-full",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.4,ease:"bounce.out"}},{t2+1.5:.2f});\n'
        js += f'tl.to("#p3e-load",{{opacity:0,duration:0.3}},{t2+1.5:.2f});\n'
        js += st.laser_js("p3e-las2", T[3] + 0.4)
        js += (f'tl.to("#p3e-g-red",{{opacity:0,duration:0.2}},{T[3]+0.9:.2f});\n'
               f'tl.fromTo("#p3e-g-grn",{{opacity:0,scaleX:0.4}},{{opacity:1,scaleX:1,duration:0.6,ease:"power2.out"}},{T[3]+0.9:.2f});\n'
               f'tl.to("#p3e-g-t1",{{opacity:0,duration:0.15}},{T[3]+1.1:.2f});\ntl.to("#p3e-g-t2",{{opacity:1,duration:0.2}},{T[3]+1.2:.2f});\n')
        return body, "", js
    s = Scene("p3repl", lines, build, lead=0.4, tail=1.6, min_hold={0: 2.4, 1: 3.0, 2: 2.6, 3: 3.2})
    s.sfx = [(("T", 1, 1.95), "ping.mp3", 0.25), (("T", 3, 1.0), "chime.mp3", 0.25)]
    return s


def ic_route():
    return ic_svg(f'<rect x="6" y="8" width="52" height="12" rx="4" fill="{C["blue"]}"/><rect x="6" y="26" width="52" height="12" rx="4" fill="{C["blue"]}" opacity="0.7"/>'
                  f'<rect x="6" y="44" width="52" height="12" rx="4" fill="{C["blue"]}" opacity="0.45"/><text x="14" y="18" font-family="{FONT}" font-weight="900" font-size="10" fill="#fff">1</text>')


def ic_down():
    return ic_svg(f'<rect x="10" y="6" width="44" height="16" rx="3" fill="{C["reserved"]}" stroke="{INK}" stroke-width="2"/><rect x="10" y="44" width="44" height="16" rx="3" fill="{C["orange"]}" stroke="{INK}" stroke-width="2"/>'
                  f'<path d="M32 24v16M24 32l8 9 8-9" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')


def part3():
    from kit import mini_rack
    return [p3_do(), p3_routes(), p3_alloc(), p3_short(), p3_repl(),
            ghinho("g3", 3, [
                (ic_route(), "Gom DO theo tuyến, <b>số tuyến = thứ tự xuất</b>", "Gom DO theo tuyến, số tuyến = thứ tự xuất"),
                (mini_rack("prim"), "Allocate <b>chỉ lấy hàng ở Primary</b>", "Allocate chỉ lấy hàng ở Primary"),
                (ic_down(), "Thiếu tồn → <b>châm hàng</b> từ Reserved", "Thiếu tồn, châm hàng từ Reserved"),
            ])]
# ============================================================ PART 4 – Pick hàng chẵn & lẻ
def p4_intro():
    lines = ["Pick hàng gồm hai phần: pick hàng chẵn thùng và pick hàng lẻ."]

    def build(T, D):
        def panel(pid, x, title, art):
            return (f'<div id="{pid}" class="abs" style="left:{x}px;top:120px;width:780px;height:640px;background:#fff;border:4px solid {INK};border-radius:30px;opacity:0">'
                    f'<div style="text-align:center;font-size:58px;font-weight:900;margin-top:40px">{title}</div>'
                    f'<svg class="abs" style="left:0;top:160px" width="780" height="440" viewBox="0 0 780 440">{art}</svg></div>')
        tro = f'<g transform="translate(300,400) scale(1.6)">{st.trolley("p4a-tr", "CH-0125")}</g>'
        ori = f'<g transform="translate(390,380) scale(1.9)">{st.oricon("p4a-or", "CH-0125")}</g>'
        body = panel("p4a-l", 120, "Hàng chẵn thùng", tro) + panel("p4a-r", 1020, "Hàng lẻ", ori)
        js = (f'tl.fromTo("#p4a-l",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},{T[0]+0.2:.2f});\n'
              f'tl.fromTo("#p4a-r",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},{T[0]+1.6:.2f});\n')
        for i in range(6):
            js += f'tl.set("#p4a-tr-k{i}",{{opacity:1}},0);\n'
        return body, "", js
    return Scene("p4intro", lines, build, lead=0.4, tail=1.0, min_hold={0: 3.8})


def p4_full():
    lines = ["Với hàng chẵn thùng, nhân viên làm từng đơn hàng,",
             "kéo theo xe trolley có dán mã cửa hàng.",
             "Vì mỗi vị trí chỉ có một mã hàng, picker chỉ cần hai bước:",
             "đi đến vị trí hiện trên PDA,",
             "và scan mã sản phẩm.",
             "Hệ thống tự hiểu đúng vị trí và báo số lượng cần lấy.",
             "Xác nhận, đặt hàng lên trolley,",
             "rồi làm tiếp cho đến hết đơn."]

    def build(T, D):
        R = st.Rack("p4b", 640, cols=3, levels=3, cw=230, lh=190)
        rack = R.svg(contents={(1, 0): "cartons", (2, 0): "cartons", (0, 1): "pallet", (1, 1): "pallet", (2, 2): "pallet"},
                     tags={(0, 0): "SKU 1001", (1, 0): "SKU 2010", (2, 0): "SKU 3002"})
        sx, sb = R.slot(0, 0)
        slot = (f'<g id="p4b-slot">' + "".join(st.carton(sx - 100 + i*68, sb - 56, 64, 56) for i in range(3))
                + "".join(st.carton(sx - 66 + i*68, sb - 112, 64, 56) for i in range(2)) + "</g>")
        X0, X1, X2 = 260, 600, 700        # picker x: start, at A-01-01, next location
        SC = 1.5
        a, b = SCAN["armR"]
        tip = hand(X1, FY, SC, a, b, extra=56)
        pk = (f'<g transform="translate({X0},{FY})"><g id="p4b-mv">{st.trolley_behind("p4b-tr", "CH-0125")}'
              f'<g transform="translate(36,0)">{stick("p4b-pk", "picker", SC, label=True, hand_r=pda_svg("p4b-pk"))}</g></g></g>')
        tip = (tip[0] + 36, tip[1])
        las = st.laser("p4b-las", tip[0], tip[1], sx - 10, sb - 30)
        path = f'<path id="p4b-path" d="M{X0+36},{FY+30} L{X1+36},{FY+30}" stroke="{C["orange"]}" stroke-width="6" stroke-dasharray="6 14" stroke-linecap="round" fill="none" opacity="0"/>'
        counts = "".join(f'<text id="p4b-n{i}" x="{X1-60}" y="{FY-330}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="96" fill="{C["orange"]}" opacity="0">{i+1}</text>' for i in range(5))
        body = svg_layer(st.floor() + rack + slot + path + pk + las + counts)
        p0 = (kv("Đơn hàng", "CH-0125", "Tuyến 1")
              + f'<div class="row" style="margin-top:14px">A-01-01 · SKU 1001 · <b>5 thùng</b></div><div class="row">A-03-01 · SKU 3002 · <b>2 thùng</b></div>')
        p1 = kv("Bước 1 – Đến vị trí", "A-01-01", "", "#C45A00")
        p2 = kv("Bước 2 – Scan mã sản phẩm", "SKU 1001 ✔", "Đúng vị trí A-01-01") + f'<div id="p4b-qty" style="margin-top:22px;opacity:0">{kv("Số lượng cần lấy", "Lấy: 5 thùng", "", "#C45A00")}</div>'
        p3 = kv("Số lượng cần lấy", "Lấy: 5 thùng", "", "#C45A00") + f'<div id="p4b-go" class="go">XÁC NHẬN</div>'
        p4 = kv("Đơn CH-0125", "Vị trí tiếp theo", "A-03-01 · SKU 3002 · 2 thùng")
        dev = st.pda("p4b-pda", "Pick chẵn thùng", [("s0", p0), ("s1", p1), ("s2", p2), ("s3", p3), ("s4", p4)])
        body += dev
        body += (f'<div id="p4b-two" class="abs" style="left:80px;top:56px;opacity:0"><div style="display:flex;gap:14px;align-items:center">'
                 f'<span style="background:{C["orange"]};border:4px solid {INK};border-radius:18px;padding:10px 24px;font-size:40px;font-weight:900">Chỉ 2 bước</span>'
                 f'<span style="background:{C["green"]};color:#fff;border:4px solid {INK};border-radius:18px;padding:10px 24px;font-size:36px;font-weight:900">Tiết kiệm thời gian</span></div></div>')
        body += st.badge("p4b-b1", 1, "Đi đến vị trí trên PDA") + st.badge("p4b-b2", 2, "Scan mã sản phẩm")
        ring = (f'<div id="p4b-done" class="abs" data-hold style="left:760px;top:150px;opacity:0"><div style="display:flex;align-items:center;gap:18px;background:#fff;border:5px solid {C["green"]};'
                f'border-radius:24px;padding:16px 30px"><svg width="90" height="90" viewBox="0 0 90 90"><circle cx="45" cy="45" r="36" fill="none" stroke="#E3E8EF" stroke-width="12"/>'
                f'<circle id="p4b-ring" cx="45" cy="45" r="36" fill="none" stroke="{C["green"]}" stroke-width="12" stroke-dasharray="226" stroke-dashoffset="226" transform="rotate(-90 45 45)" stroke-linecap="round"/></svg>'
                f'<span style="font-size:44px;font-weight:900">Đơn hàng hoàn tất ✔</span></div></div>')
        body += ring
        js = st.appear_js("#p4b-pda", T[0] + 0.1, 0.35, dy=30) + st.show_panel_js("p4b-pda", None, "s0", T[0] + 0.2)
        js += 'tl.fromTo("#p4b-pk-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},%.2f);\n' % (T[0] + 0.3)
        js += st.pop_js("#p4b-tr-code", T[1] + 0.2)
        js += f'tl.fromTo("#p4b-two",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{T[2]+0.3:.2f});\n'
        js += f'tl.to("#p4b-two",{{opacity:0,duration:0.2}},{T[3]-0.15:.2f});\n'
        js += st.badge_seq_js(["p4b-b1", "p4b-b2"], [T[3], T[4]], T[6] - 0.1)
        js += f'tl.to("#p4b-b2",{{opacity:0,duration:0.2}},{T[6]-0.1:.2f});\n'
        js += st.show_panel_js("p4b-pda", "s0", "s1", T[3])
        js += f'tl.fromTo("#p4b-path",{{opacity:0}},{{opacity:1,duration:0.2}},{T[3]+0.2:.2f});\n'
        js += f'tl.to("#p4b-mv",{{x:{X1-X0},duration:1.8,ease:"none"}},{T[3]+0.3:.2f});\n' + walk_js("p4b-pk", T[3] + 0.3, T[3] + 2.1)
        js += f'tl.to("#p4b-path",{{opacity:0,duration:0.2}},{T[3]+2.1:.2f});\n'
        js += pose_js("p4b-pk", T[4], SCAN, dur=0.25, ease="power2.out")
        js += st.show_panel_js("p4b-pda", "s1", "s2", T[4])
        js += st.laser_js("p4b-las", T[4] + 0.4)
        js += f'tl.fromTo("#p4b-qty",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{T[5]+0.3:.2f});\n'
        js += pose_js("p4b-pk", T[5], REST, dur=0.3)
        js += st.show_panel_js("p4b-pda", "s2", "s3", T[6])
        js += f'tl.to("#p4b-go",{{scale:0.94,duration:0.1}},{T[6]+0.3:.2f});\ntl.to("#p4b-go",{{scale:1,duration:0.15}},{T[6]+0.4:.2f});\n'
        for i in range(5):
            t = T[6] + 0.7 + i * 0.42
            js += st.pop_js(f"#p4b-tr-k{i}", t, 0.25)
            js += f'tl.fromTo("#p4b-n{i}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.15,transformOrigin:"50% 50%"}},{t:.2f});\ntl.to("#p4b-n{i}",{{opacity:0,duration:0.1}},{t+0.38:.2f});\n'
        js += f'tl.to("#p4b-slot",{{opacity:0.25,duration:2.0}},{T[6]+0.7:.2f});\n'
        js += st.show_panel_js("p4b-pda", "s3", "s4", T[7])
        js += f'tl.to("#p4b-mv",{{x:{X2-X0},duration:1.2,ease:"none"}},{T[7]+0.2:.2f});\n' + walk_js("p4b-pk", T[7] + 0.2, T[7] + 1.4)
        js += f'tl.fromTo("#p4b-done",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{T[7]+1.5:.2f});\n'
        js += f'tl.to("#p4b-ring",{{strokeDashoffset:0,duration:0.8,ease:"power2.out"}},{T[7]+1.6:.2f});\n'
        return body, "", js
    s = Scene("p4full", lines, build, lead=0.4, tail=1.6,
              min_hold={2: 3.4, 3: 2.6, 4: 2.2, 6: 3.2, 7: 3.0})
    s.sfx = [(("T", 4, 0.4), "ping.mp3", 0.25), (("T", 7, 1.6), "chime.mp3", 0.25)]
    return s


def p4_piece():
    lines = ["Với hàng lẻ, nhân viên mang theo thùng xanh gọi là Oricon, có dán mã cửa hàng.",
             "Đến vị trí hiển thị,",
             "scan mã hàng,",
             "nhập số lượng,",
             "rồi bỏ hàng vào Oricon."]

    def build(T, D):
        R = st.Rack("p4c", 760, cols=2, levels=3, cw=280, lh=190, aisle="B")
        rack = R.svg(contents={(1, 0): "cartons", (0, 1): "pallet", (1, 2): "pallet"})
        sx, sb = R.slot(0, 0)
        packs = "".join(f'<g><rect x="{sx-110 + i*46}" y="{sb-48}" width="40" height="48" rx="5" fill="#E5584F" stroke="{INK}" stroke-width="2.5"/>'
                        f'<rect x="{sx-104 + i*46}" y="{sb-36}" width="28" height="12" fill="#F2B233"/></g>' for i in range(5))
        X0, X1, SC = 230, 600, 1.5
        a, b = SCAN["armR"]
        tip = hand(X1, FY, SC, a, b, extra=56)
        ori_carry = f'<g id="p4c-oc" transform="translate(0,-52) scale(0.42)">{st.oricon("p4c-or1", "CH-0125")}</g>'
        pk = (f'<g transform="translate({X0},{FY})"><g id="p4c-mv">{stick("p4c-pk", "picker", SC, pose=CARRY, hand_r=pda_svg("p4c-pk"))}'
              f'<g transform="scale({SC})">{ori_carry}</g></g></g>')
        floor_ori = f'<g transform="translate({X1-120},{FY})"><g id="p4c-of" opacity="0">{st.oricon("p4c-or2", "CH-0125")}</g></g>'
        drops = "".join(f'<g id="p4c-it{i}" opacity="0"><rect x="{X1-150 + i*30}" y="{FY-150}" width="40" height="48" rx="5" fill="#E5584F" stroke="{INK}" stroke-width="2.5"/></g>' for i in range(3))
        las = st.laser("p4c-las", tip[0], tip[1], sx - 64, sb - 26)
        body = svg_layer(st.floor() + rack + packs + floor_ori + pk + drops + las)
        body += st.pda("p4c-pda", "Pick hàng lẻ", [
            ("s1", kv("Đến vị trí", R.loc(0, 0), "", "#C45A00")),
            ("s2", kv("Scan mã hàng", "SKU 2005 ✔", "Bánh quy (ví dụ)")),
            ("s3", kv("Nhập số lượng", "3 gói", "") + '<div class="keys">' + "".join(f"<div>{k}</div>" for k in "123456789") + '<div>⌫</div><div>0</div><div>OK</div></div>'),
            ("s4", kv("Bỏ vào Oricon", "CH-0125 ✔", "Đã lấy 3 gói")),
        ])
        body += "".join(st.badge(f"p4c-b{i+1}", i + 1, t) for i, t in enumerate(["Đến vị trí", "Scan mã hàng", "Nhập số lượng", "Bỏ vào Oricon"]))
        body += (f'<div id="p4c-name" class="abs" style="left:80px;top:56px;opacity:0"><span style="display:inline-block;background:#2F6FD6;color:#fff;border:4px solid {INK};'
                 f'border-radius:18px;padding:10px 26px;font-size:40px;font-weight:900">Oricon = thùng nhựa xanh, dán mã cửa hàng</span></div>')
        js = f'tl.fromTo("#p4c-name",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.3}},{T[0]+0.3:.2f});\ntl.to("#p4c-name",{{opacity:0,duration:0.2}},{T[1]-0.2:.2f});\n'
        js += f'tl.fromTo("#p4c-mv",{{x:-420}},{{x:0,duration:1.8,ease:"none"}},{T[0]+0.2:.2f});\n' + walk_js("p4c-pk", T[0] + 0.2, T[0] + 2.0)
        js += st.appear_js("#p4c-pda", T[1], 0.35, dy=30)
        js += st.badge_seq_js([f"p4c-b{i+1}" for i in range(4)], T[1:5], D - 0.3)
        js += st.show_panel_js("p4c-pda", None, "s1", T[1])
        js += f'tl.to("#p4c-mv",{{x:{X1-X0},duration:1.6,ease:"none"}},{T[1]+0.1:.2f});\n' + walk_js("p4c-pk", T[1] + 0.1, T[1] + 1.7)
        js += f'tl.set("#p4c-oc",{{opacity:0}},{T[1]+1.9:.2f});\ntl.fromTo("#p4c-of",{{opacity:0}},{{opacity:1,duration:0.15}},{T[1]+1.9:.2f});\n'
        js += pose_js("p4c-pk", T[1] + 1.9, REST, dur=0.25)
        js += pose_js("p4c-pk", T[2], SCAN, dur=0.25, ease="power2.out")
        js += st.show_panel_js("p4c-pda", "s1", "s2", T[2])
        js += st.laser_js("p4c-las", T[2] + 0.4)
        js += st.show_panel_js("p4c-pda", "s2", "s3", T[3])
        js += pose_js("p4c-pk", T[3] + 0.1, REST, dur=0.25)
        js += st.show_panel_js("p4c-pda", "s3", "s4", T[4] + 1.4)
        for i in range(3):
            js += f'tl.fromTo("#p4c-it{i}",{{opacity:0,y:0}},{{opacity:1,y:70,duration:0.45,ease:"bounce.out"}},{T[4]+0.2+i*0.3:.2f});\n'
        return body, "", js
    s = Scene("p4piece", lines, build, lead=0.4, tail=1.6, min_hold={1: 2.6, 2: 2.2, 3: 2.4, 4: 2.8})
    s.sfx = [(("T", 2, 0.4), "ping.mp3", 0.25)]
    return s


def ic_trolley():
    return ic_svg(f'<line x1="10" y1="10" x2="10" y2="50" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><rect x="10" y="46" width="46" height="6" fill="#8FA3BF" stroke="{INK}" stroke-width="2"/>'
                  f'<rect x="16" y="26" width="18" height="20" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2"/><rect x="36" y="26" width="18" height="20" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2"/>'
                  f'<circle cx="16" cy="56" r="4" fill="{INK}"/><circle cx="50" cy="56" r="4" fill="{INK}"/>')


def ic_oricon():
    return ic_svg(f'<path d="M8 20h48l-4 34H12z" fill="#2F6FD6" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><rect x="18" y="30" width="28" height="10" rx="2" fill="#fff"/>')


def ic_order():
    return ic_svg(f'<rect x="12" y="6" width="40" height="52" rx="6" fill="#fff" stroke="{INK}" stroke-width="3"/>'
                  f'<path d="M20 20l4 4 8-8M20 34l4 4 8-8M20 48l4 4 8-8" fill="none" stroke="{C["green"]}" stroke-width="4" stroke-linecap="round"/>')


def part4():
    return [p4_intro(), p4_full(), p4_piece(),
            ghinho("g4", 4, [
                (ic_trolley(), "Chẵn thùng: trolley theo mã cửa hàng – <b>chỉ 2 bước</b>: đến vị trí, scan mã hàng",
                 "Chẵn thùng: trolley theo mã cửa hàng, chỉ 2 bước: đến vị trí, scan mã hàng"),
                (ic_oricon(), "Hàng lẻ: <b>Oricon</b> – scan, nhập số lượng, bỏ vào thùng", "Hàng lẻ: Oricon, scan, nhập số lượng, bỏ vào thùng"),
                (ic_order(), "Luôn <b>làm xong trọn từng đơn</b>", "Luôn làm xong trọn từng đơn"),
            ])]
# ============================================================ PART 5 – Kiểm hàng & Bàn giao
def p5_intro():
    lines = ["Trước khi ra kho, hàng được kiểm theo hai loại."]

    def build(T, D):
        def tile(tid, x, label, art):
            return (f'<div id="{tid}" class="abs" style="left:{x}px;top:300px;width:560px;height:420px;background:#fff;border:4px solid {INK};border-radius:30px;opacity:0">'
                    f'<svg class="abs" style="left:0;top:20px" width="560" height="300" viewBox="0 0 560 300">{art}</svg>'
                    f'<div class="abs" style="left:0;right:0;bottom:30px;text-align:center;font-size:46px;font-weight:900">{label}</div></div>')
        tro = f'<g transform="translate(150,270) scale(1.25)">{st.trolley("p5a-tr", "CH-0125")}</g>'
        ori = f'<g transform="translate(280,260) scale(1.5)">{st.oricon("p5a-or", "CH-0125")}</g>'
        body = (f'<div id="p5a-t" class="abs" style="left:0;top:120px;width:1920px;text-align:center;opacity:0"><span style="display:inline-block;background:#fff;border:4px solid {INK};border-radius:20px;padding:14px 36px;font-size:56px;font-weight:900">Kiểm hàng trước khi ra kho</span></div>'
                + tile("p5a-l", 320, "Hàng thùng · trolley", tro) + tile("p5a-r", 1040, "Hàng lẻ · Oricon", ori))
        js = st.appear_js("#p5a-t", 0.2)
        js += f'tl.fromTo("#p5a-l",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},{T[0]+0.5:.2f});\n'
        js += f'tl.fromTo("#p5a-r",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},{T[0]+1.0:.2f});\n'
        for i in range(6):
            js += f'tl.set("#p5a-tr-k{i}",{{opacity:1}},0);\n'
        return body, "", js
    return Scene("p5intro", lines, build, lead=0.4, tail=1.0, min_hold={0: 3.2})


def p5_carton():
    lines = ["Với hàng thùng, nhóm checker đi kiểm từng đơn trên xe trolley.",
             "Checker chọn đúng cửa hàng theo mã trên trolley,",
             "scan mã hàng,",
             "đếm và nhập số lượng để biết đã pick đủ hay chưa."]
    trolleys = [(330, "CH-0125", 5), (630, "CH-0311", 3), (930, "CH-0420", 4)]

    def build(T, D):
        X0, X1, SC = -120, 230, 1.5
        a, b = SCAN["armR"]
        tip = hand(X1, FY, SC, a, b, extra=56)
        tr = "".join(f'<g transform="translate({x},{FY})">{st.trolley(f"p5b-t{i}", code)}</g>' for i, (x, code, n) in enumerate(trolleys))
        ck = f'<g transform="translate({X0},{FY})"><g id="p5b-mv">{stick("p5b-ck", "checker", SC, label=True, hand_r=pda_svg("p5b-ck"))}</g></g>'
        las = st.laser("p5b-las", tip[0], tip[1], 330 + 98, FY - 112)
        hl = f'<rect id="p5b-hl" x="{330-64}" y="{FY-182}" width="128" height="50" rx="10" fill="none" stroke="{C["green"]}" stroke-width="6" opacity="0"/>'
        tags = (f'<g id="p5b-ok" opacity="0" transform="translate(430,{FY-250})"><rect x="-80" y="-30" width="160" height="56" rx="16" fill="{C["green"]}" stroke="{INK}" stroke-width="3"/>'
                f'<text x="0" y="10" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="32" fill="#fff">Đủ ✔</text></g>'
                f'<g id="p5b-bad" opacity="0" transform="translate(730,{FY-250})"><rect x="-120" y="-30" width="240" height="56" rx="16" fill="{C["red"]}" stroke="{INK}" stroke-width="3"/>'
                f'<text x="0" y="10" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="30" fill="#fff">Thiếu ✖ (ví dụ)</text></g>')
        body = svg_layer(st.floor() + tr + hl + ck + las + tags)
        rows = "".join(f'<div class="row" style="position:relative">{code}' + (f'<div id="p5b-sel" style="position:absolute;left:-3px;top:-3px;right:-3px;bottom:-3px;border:4px solid {C["green"]};border-radius:12px;background:rgba(34,165,90,.08);opacity:0"></div>' if i == 0 else "") + '</div>'
                       for i, (_, code, _) in enumerate(trolleys))
        body += st.pda("p5b-pda", "Kiểm hàng thùng", [
            ("s1", '<div class="lbl">Chọn cửa hàng</div>' + rows),
            ("s2", kv("CH-0125 · Scan mã hàng", "SKU 1001 ✔")),
            ("s3", kv("Nhập số lượng đếm được", "5 thùng") + f'<div id="p5b-res" style="margin-top:20px;opacity:0"><div class="go">Đủ ✔ (cần 5 – có 5)</div></div>'),
        ])
        body += "".join(st.badge(f"p5b-b{i+1}", i + 1, t) for i, t in enumerate(["Chọn đúng cửa hàng", "Scan mã hàng", "Đếm & nhập số lượng"]))
        js = 'tl.fromTo("#p5b-ck-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},%.2f);\n' % (T[0] + 0.3)
        for i, (_, _, n) in enumerate(trolleys):
            for k in range(n):
                js += f'tl.set("#p5b-t{i}-k{k}",{{opacity:1}},0);\n'
        js += f'tl.to("#p5b-mv",{{x:{X1-X0},duration:1.8,ease:"none"}},{T[0]+0.2:.2f});\n' + walk_js("p5b-ck", T[0] + 0.2, T[0] + 2.0)
        js += st.appear_js("#p5b-pda", T[0] + 0.5, 0.35, dy=30)
        js += st.badge_seq_js([f"p5b-b{i+1}" for i in range(3)], T[1:4], D - 0.3)
        js += st.show_panel_js("p5b-pda", None, "s1", T[1])
        js += f'tl.fromTo("#p5b-sel",{{opacity:0}},{{opacity:1,duration:0.2}},{T[1]+0.9:.2f});\n'
        js += f'tl.fromTo("#p5b-hl",{{opacity:0}},{{opacity:1,duration:0.2}},{T[1]+0.9:.2f});\n'
        js += st.show_panel_js("p5b-pda", "s1", "s2", T[2])
        js += pose_js("p5b-ck", T[2], SCAN, dur=0.25, ease="power2.out") + st.laser_js("p5b-las", T[2] + 0.4)
        js += st.show_panel_js("p5b-pda", "s2", "s3", T[3])
        js += pose_js("p5b-ck", T[3], REST, dur=0.25)
        js += f'tl.fromTo("#p5b-res",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{T[3]+1.0:.2f});\n'
        js += st.pop_js("#p5b-ok", T[3] + 1.1) + st.pop_js("#p5b-bad", T[3] + 1.8)
        return body, "", js
    s = Scene("p5carton", lines, build, lead=0.4, tail=1.6, min_hold={0: 3.4, 1: 3.0, 2: 2.2, 3: 3.8})
    s.sfx = [(("T", 2, 0.4), "ping.mp3", 0.25)]
    return s


def p5_piece():
    lines = ["Với hàng lẻ, picker mang Oricon ra khu đóng gói.",
             "Checker kiểm hàng bên trong,",
             "scan mã hàng, nhập số lượng,",
             "và niêm phong thùng sau khi kiểm xong."]

    def build(T, D):
        TX, TY = 700, 620        # table left, top
        table = (f'<rect x="{TX}" y="{TY}" width="480" height="22" rx="4" fill="#C9965A" stroke="{INK}" stroke-width="3"/>'
                 f'<rect x="{TX+20}" y="{TY+22}" width="16" height="{FY-TY-22}" fill="#A97A44" stroke="{INK}" stroke-width="2.5"/>'
                 f'<rect x="{TX+444}" y="{TY+22}" width="16" height="{FY-TY-22}" fill="#A97A44" stroke="{INK}" stroke-width="2.5"/>'
                 f'<g transform="translate({TX+240},{TY-330})"><rect x="-170" y="-34" width="340" height="68" rx="14" fill="{C["blue"]}" stroke="{INK}" stroke-width="3"/>'
                 f'<text x="0" y="13" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="36" fill="#fff">Khu đóng gói</text></g>')
        OX = TX + 230
        ori = f'<g transform="translate({OX},{TY})"><g id="p5c-ot" opacity="0">{st.oricon("p5c-or", "CH-0125")}</g></g>'
        lid = (f'<g id="p5c-lid" opacity="0"><rect x="{OX-92}" y="{TY-112}" width="184" height="16" rx="5" fill="#4C86E6" stroke="{INK}" stroke-width="3"/></g>'
               f'<rect id="p5c-tape" x="{OX-100}" y="{TY-80}" width="200" height="22" fill="#F2B233" stroke="{INK}" stroke-width="2" opacity="0"/>'
               f'<g id="p5c-seal" opacity="0" transform="translate({OX+40},{TY-60}) rotate(-10)"><rect x="-70" y="-24" width="140" height="48" rx="8" fill="{C["red"]}" stroke="{INK}" stroke-width="3"/>'
               f'<text x="0" y="11" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="30" fill="#fff">SEALED</text></g>')
        PX0, PX1, SC = -150, 560, 1.5
        carry_ori = f'<g id="p5c-oc" transform="translate(0,-52) scale(0.42)">{st.oricon("p5c-or1", "CH-0125")}</g>'
        pk = (f'<g transform="translate({PX0},{FY})"><g id="p5c-pmv">{stick("p5c-pk", "picker", SC, pose=CARRY)}'
              f'<g transform="scale({SC})">{carry_ori}</g></g></g>')
        CKX = 1290
        a, b = SCAN["armR"]
        tip = hand(CKX, FY, SC, a, b, flip=True, extra=56)
        ck = figure("p5c-ck", "checker", CKX, scale=SC, label=True, flip=True, hand_r=pda_svg("p5c-ck"))
        las = st.laser("p5c-las", tip[0], tip[1], OX + 30, TY - 70)
        body = svg_layer(st.floor() + table + ori + lid + pk + ck + las)
        body += st.pda("p5c-pda", "Kiểm hàng lẻ", [
            ("s1", kv("Oricon", "CH-0125", "Mở thùng, kiểm hàng bên trong")),
            ("s2", kv("Scan mã hàng", "SKU 2005 ✔") + '<div style="height:16px"></div>' + kv("Số lượng", "3 gói ✔", "Khớp với số đã pick")),
            ("s3", kv("Niêm phong", "Đã seal ✔", "Sẵn sàng bàn giao")),
        ])
        body += "".join(st.badge(f"p5c-b{i+1}", i + 1, t) for i, t in enumerate(["Scan mã hàng", "Nhập số lượng", "Niêm phong thùng"]))
        js = f'tl.to("#p5c-pmv",{{x:{PX1-PX0},duration:2.0,ease:"none"}},{T[0]+0.1:.2f});\n' + walk_js("p5c-pk", T[0] + 0.1, T[0] + 2.1)
        js += f'tl.set("#p5c-oc",{{opacity:0}},{T[0]+2.3:.2f});\ntl.fromTo("#p5c-ot",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.3,ease:"bounce.out"}},{T[0]+2.3:.2f});\n'
        js += pose_js("p5c-pk", T[0] + 2.3, REST, dur=0.25)
        js += f'tl.to("#p5c-pmv",{{x:{-PX0-300},duration:1.6,ease:"none"}},{T[1]+0.2:.2f});\n' + walk_js("p5c-pk", T[1] + 0.2, T[1] + 1.8)
        js += 'tl.fromTo("#p5c-ck-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},%.2f);\n' % (T[1])
        js += st.appear_js("#p5c-pda", T[1], 0.35, dy=30) + st.show_panel_js("p5c-pda", None, "s1", T[1] + 0.1)
        js += st.badge_seq_js(["p5c-b1", "p5c-b2", "p5c-b3"], [T[2], T[2] + 1.7, T[3]], D - 0.3)
        js += st.show_panel_js("p5c-pda", "s1", "s2", T[2])
        js += pose_js("p5c-ck", T[2], SCAN, dur=0.25, ease="power2.out") + st.laser_js("p5c-las", T[2] + 0.4)
        js += pose_js("p5c-ck", T[2] + 1.4, REST, dur=0.25)
        js += st.show_panel_js("p5c-pda", "s2", "s3", T[3] + 1.2)
        js += f'tl.fromTo("#p5c-lid",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{T[3]+0.1:.2f});\n'
        js += f'tl.fromTo("#p5c-tape",{{opacity:1,scaleX:0}},{{opacity:1,scaleX:1,duration:0.5,ease:"power2.inOut",transformOrigin:"0% 50%"}},{T[3]+0.45:.2f});\n'
        js += f'tl.fromTo("#p5c-seal",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:0.25,ease:"power3.out",transformOrigin:"50% 50%"}},{T[3]+1.0:.2f});\n'
        return body, "", js
    s = Scene("p5piece", lines, build, lead=0.4, tail=1.6, min_hold={0: 3.2, 1: 2.4, 2: 3.4, 3: 3.0})
    s.sfx = [(("T", 3, 1.0), "chime.mp3", 0.25)]
    return s


def p5_handover():
    lines = ["Cuối cùng là bàn giao cho vận tải.",
             "Việc bàn giao diễn ra từ khuya đến rạng sáng,",
             "chỉ có đội vận tải làm việc,",
             "nên đội vận tải chỉ xác nhận bàn giao trên hệ thống,",
             "không kiểm đếm lại số lượng."]

    def build(T, D):
        stars = "".join(f'<circle cx="{(i*397) % 1880 + 20}" cy="{(i*173) % 420 + 30}" r="{2 + i % 3}" fill="#fff"/>' for i in range(26))
        sky = (f'<div class="abs" style="left:0;top:0;width:1920px;height:{FY}px;background:linear-gradient(180deg,#0E1A33 0%,#23355C 100%)"></div>'
               f'<div id="p5d-dawn" class="abs" style="left:0;top:0;width:1920px;height:{FY}px;opacity:0;background:linear-gradient(180deg,#9CC3EE 0%,#F7C58B 70%,#F49E5C 100%)"></div>')
        celestial = (f'<g id="p5d-stars">{stars}</g>'
                     f'<g id="p5d-moon"><circle cx="1500" cy="150" r="60" fill="#F4F1DE"/><circle cx="1525" cy="135" r="56" fill="#23355C" id="p5d-moonmask"/></g>'
                     f'<g id="p5d-sun" opacity="0"><circle cx="300" cy="{FY-40}" r="90" fill="#FFD23F"/></g>')
        goods = (f'<g transform="translate(330,{FY})">{st.trolley("p5d-t1", "CH-0125")}</g>'
                 f'<g transform="translate(600,{FY})"><g transform="scale(0.8)">{st.oricon("p5d-o1", "CH-0125", title_color="#2F6FD6")}</g></g>'
                 f'<g transform="translate(600,{FY-84})"><g transform="scale(0.8)">{st.oricon("p5d-o2", "CH-0311", title_color="#2F6FD6")}</g></g>')
        trk = f'<g transform="translate(1060,{FY})">{st.truck("p5d-truck")}</g>'
        TX = 920
        tp = figure("p5d-tp", "transport", TX, scale=1.5, label=True, pose={"armR": (-30, -80)}, hand_r=pda_svg("p5d-tp"))
        nocount = (f'<g id="p5d-no" opacity="0" transform="translate(1660,240)"><rect x="-180" y="-110" width="360" height="220" rx="24" fill="#fff" stroke="{INK}" stroke-width="4"/>'
                   f'<rect x="-60" y="-80" width="120" height="120" rx="10" fill="#F1F3F6" stroke="{INK}" stroke-width="3"/>'
                   f'<text x="0" y="-12" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="40" fill="{INK}">1 2 3</text>'
                   f'<line x1="-80" y1="-90" x2="80" y2="50" stroke="{C["red"]}" stroke-width="12" stroke-linecap="round"/>'
                   f'<text x="0" y="90" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="28" fill="{C["red"]}">Không kiểm đếm lại</text></g>')
        body = sky + svg_layer(celestial + st.floor() + goods + trk + tp + nocount)
        body += (f'<div id="p5d-time" class="abs" style="left:80px;top:56px;opacity:0"><span style="display:inline-block;background:#fff;border:4px solid {INK};border-radius:18px;'
                 f'padding:10px 26px;font-size:40px;font-weight:900">Khuya → Rạng sáng</span></div>')
        body += pda_popup("p5d-pop", "Bàn giao vận tải", [
            ("q1", kv("Tuyến 1 · 3 cửa hàng", "Xác nhận bàn giao?", "") + f'<div id="p5d-btn" class="abs" style="left:0;right:0;top:120px;background:{C["green"]};color:#fff;font-weight:900;font-size:32px;text-align:center;border-radius:14px;padding:12px 0">XÁC NHẬN BÀN GIAO</div>'),
        ], 640, 150, w=600, h=200)
        body += st.stamp("p5d-done", "Đã ra kho", x=1270, y=420)
        js = (f'tl.fromTo("#p5d-time",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.3}},{T[1]:.2f});\n'
              f'tl.to("#p5d-dawn",{{opacity:1,duration:{T[3]-T[1]+1.0:.2f},ease:"sine.inOut"}},{T[1]+0.3:.2f});\n'
              f'tl.to("#p5d-stars",{{opacity:0,duration:2.0}},{T[1]+0.5:.2f});\n'
              f'tl.to("#p5d-moon",{{opacity:0,y:60,duration:2.0}},{T[1]+0.6:.2f});\n'
              f'tl.fromTo("#p5d-sun",{{opacity:0,y:80}},{{opacity:1,y:0,duration:2.4,ease:"power1.out"}},{T[2]:.2f});\n')
        js += 'tl.fromTo("#p5d-tp-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},%.2f);\n' % (T[2])
        for k in range(5):
            js += f'tl.set("#p5d-t1-k{k}",{{opacity:1}},0);\n'
        js += st.appear_js("#p5d-pop", T[3], 0.3) + f'tl.set("#p5d-pop-q1",{{opacity:1}},{T[3]:.2f});\n'
        js += f'tl.to("#p5d-btn",{{scale:0.94,duration:0.1}},{T[3]+1.3:.2f});\ntl.to("#p5d-btn",{{scale:1,duration:0.15}},{T[3]+1.4:.2f});\n'
        js += st.stamp_js("p5d-done", T[3] + 1.6)
        js += st.pop_js("#p5d-no", T[4] + 0.2, 0.4)
        return body, "", js
    s = Scene("p5hand", lines, build, lead=0.5, tail=1.8, min_hold={1: 3.0, 3: 3.2, 4: 2.6})
    s.sfx = [(("T", 3, 1.6), "chime.mp3", 0.25)]
    return s


def ic_truck():
    return ic_svg(f'<rect x="4" y="18" width="36" height="26" rx="3" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M40 26h10l8 10v8H40z" fill="{C["blue"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                  f'<circle cx="14" cy="48" r="6" fill="{INK}"/><circle cx="48" cy="48" r="6" fill="{INK}"/>')


def ic_check():
    return ic_svg(f'<rect x="10" y="6" width="44" height="52" rx="6" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M20 32l8 8 16-18" fill="none" stroke="{C["green"]}" stroke-width="6" stroke-linecap="round"/>')


def p5_recap():
    lines = ["Vậy là bạn đã nắm toàn bộ quy trình vận hành kho.",
             "Chúc các bạn làm việc thật tốt!"]
    from kit import mini_rack
    steps = [("Nhập hàng", ic_pallet), ("Cất hàng", ic_forklift), ("Gom tuyến & Allocate", ic_route),
             ("Châm hàng", ic_down), ("Pick", ic_trolley), ("Kiểm hàng", ic_check), ("Bàn giao", ic_truck)]

    def build(T, D):
        W, G, X0 = 222, 34, 80
        chips = ""
        for i, (name, fn) in enumerate(steps):
            x = X0 + i * (W + G)
            chips += (f'<div id="p5e-s{i}" class="abs" style="left:{x}px;top:170px;width:{W}px;height:250px;background:#fff;border:4px solid {INK};border-radius:22px;opacity:0;text-align:center">'
                      f'<div style="margin-top:14px;font-size:26px;font-weight:900;color:#C45A00">{i+1}</div>'
                      f'<div style="display:flex;justify-content:center;margin-top:4px">{fn()}</div>'
                      f'<div style="font-size:27px;font-weight:900;line-height:1.15;margin:8px 10px 0">{name}</div></div>')
            if i < len(steps) - 1:
                chips += f'<div id="p5e-a{i}" class="abs" style="left:{x+W+2}px;top:270px;width:{G-4}px;text-align:center;font-size:36px;font-weight:900;color:{C["blue"]};opacity:0">›</div>'
        thumb = f'<circle cx="0" cy="25" r="8" fill="{INK}"/><line x1="0" y1="30" x2="0" y2="44" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        man = svg_layer(f'<g transform="translate(960,{FY+40})"><g id="p5e-man">{stick("p5e-man", "instructor", 2.0, hand_r=thumb)}</g></g>')
        body = f'<div class="abs" style="left:0;top:{FY}px;width:1920px;height:{1080-FY}px;background:{C["floor"]}"></div>' + chips + man
        js = ""
        for i in range(len(steps)):
            js += f'tl.fromTo("#p5e-s{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{0.3 + i*0.3:.2f});\n'
            if i < len(steps) - 1:
                js += f'tl.fromTo("#p5e-a{i}",{{opacity:0}},{{opacity:1,duration:0.2}},{0.5 + i*0.3:.2f});\n'
        js += pose_js("p5e-man", T[1], {"armR": (-100, -80)}, dur=0.35, ease="back.out(2)")
        return body, "", js
    s = Scene("p5recap", lines, build, lead=0.6, tail=2.6, min_hold={0: 3.2, 1: 2.4})
    s.sfx = [(("T", 1, 0.3), "chime.mp3", 0.25)]
    return s


def part5():
    return [p5_intro(), p5_carton(), p5_piece(), p5_handover(), p5_recap()]
