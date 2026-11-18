"""Training video: Vận hành hàng TC (trung chuyển / cross dock) -> ./video-tc
Run: python3 tools/build_tc.py [limit_seconds]
Script source: source/Context_Video_TC.md
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, stick, walk_js, pose_js, REST, pda_svg
import stage as st
from stage import FY, INK
from build_full import Scene, chapter, build_all
from parts import figure, pallet_build, svg_layer, kv, hand, SCAN, CARRY, carry_box

OUT = os.path.join(os.path.dirname(__file__), "..", "video-tc")


def chip(cid, text, color="#fff", txt=INK, w=None, inner=""):
    ws = f"width:{w}px;" if w else ""
    return (f'<div id="{cid}" style="display:inline-flex;align-items:center;justify-content:center;{ws}background:{color};color:{txt};'
            f'border:4px solid {INK};border-radius:16px;padding:12px 20px;font-size:32px;font-weight:900;opacity:0;position:relative">{text}{inner}</div>')


def arrow(aid):
    return f'<div id="{aid}" style="font-size:44px;font-weight:900;color:{C["blue"]};opacity:0;margin:0 10px">›</div>'


# ============================================================ MỞ ĐẦU
def tc_intro():
    lines = ["Hàng TC là hàng trung chuyển.",
             "Hàng nhập vào không lưu kho, mà được chia ngay cho các cửa hàng, giống như cross dock."]
    normal = ["Nhập hàng", "Cất lên kệ", "Lưu kho", "Pick", "Xuất"]
    tc = ["Nhập hàng", "Khu TC", "Chia cho cửa hàng", "Xuất"]

    def build(T, D):
        def row(rid, label, items, color, top):
            inner = ""
            for i, t in enumerate(items):
                if i:
                    inner += arrow(f"{rid}-a{i}")
                strike = (f'<div id="{rid}-x{i}" class="abs" style="left:-8px;right:-8px;top:50%;height:7px;margin-top:-3px;background:{C["red"]};'
                          f'border-radius:4px;transform-origin:0% 50%;opacity:0"></div>') if t in ("Cất lên kệ", "Lưu kho") else ""
                inner += chip(f"{rid}-c{i}", t, color=color if t in ("Khu TC", "Chia cho cửa hàng") else "#fff", inner=strike)
            return (f'<div class="abs" style="left:110px;top:{top}px">'
                    f'<div id="{rid}-lab" style="font-size:34px;font-weight:900;color:{C["muted"]};margin-bottom:12px;opacity:0">{label}</div>'
                    f'<div style="display:flex;align-items:center">{inner}</div></div>')
        body = f"""
    <div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,{C['ground']} 0%,{C['ground']} 74%,{C['floor']} 74%,{C['floor']} 100%)"></div>
    <div id="tc0-title" class="abs" style="left:110px;top:70px"><div style="font-size:92px;font-weight:900;line-height:1.05">Vận hành hàng TC</div>
      <div style="font-size:48px;font-weight:700;color:{C['blue']};margin-top:8px">(Trung chuyển – giống cross dock)</div></div>
    {row("tc0-n", "Hàng kho khô thường", normal, "#fff", 380)}
    {row("tc0-t", "Hàng TC", tc, C["orange"], 560)}
    {svg_layer(f'<g transform="translate(1690,880)"><g id="tc0-man">{stick("tc0-man", "instructor", scale=2.2)}</g></g>')}"""
        js = 'tl.fromTo("#tc0-title",{opacity:1,x:-24},{opacity:1,x:0,duration:0.6,ease:"power3.out"},0);\n'
        js += 'tl.fromTo("#tc0-man",{x:420},{x:0,duration:1.4,ease:"power1.out"},0.1);\n' + walk_js("tc0-man", 0.1, 1.5)
        js += pose_js("tc0-man", 1.6, {"armR": (-150, -24)}, dur=0.3, ease="power2.out")
        for k in range(4):
            js += f'tl.to("#tc0-man-foreR",{{rotation:{-50 if k % 2 == 0 else -5},svgOrigin:"0 0",duration:0.22,ease:"sine.inOut"}},{1.9 + k*0.22:.2f});\n'
        js += pose_js("tc0-man", 2.9, {"armR": REST["armR"]}, dur=0.3)
        js += f'tl.fromTo("#tc0-n-lab",{{opacity:0}},{{opacity:1,duration:0.3}},{T[0]+0.3:.2f});\n'
        for i in range(len(normal)):
            t = T[0] + 0.4 + i * 0.22
            js += f'tl.fromTo("#tc0-n-c{i}",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{t:.2f});\n'
            if i:
                js += f'tl.fromTo("#tc0-n-a{i}",{{opacity:0}},{{opacity:1,duration:0.2}},{t:.2f});\n'
        js += f'tl.fromTo("#tc0-t-lab",{{opacity:0}},{{opacity:1,duration:0.3}},{T[1]:.2f});\n'
        for i in range(len(tc)):
            t = T[1] + 0.1 + i * 0.25
            js += f'tl.fromTo("#tc0-t-c{i}",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{t:.2f});\n'
            if i:
                js += f'tl.fromTo("#tc0-t-a{i}",{{opacity:0}},{{opacity:1,duration:0.2}},{t:.2f});\n'
        for sid in ("tc0-n-x1", "tc0-n-x2"):
            js += f'tl.fromTo("#{sid}",{{opacity:1,scaleX:0}},{{opacity:1,scaleX:1,duration:0.35,ease:"power2.out"}},{T[1]+1.6:.2f});\n'
        js += pose_js("tc0-man", T[1] + 1.2, {"armL": (128, -10)}, dur=0.35, ease="power2.out")
        return body, "", js
    s = Scene("tcintro", lines, build, lead=0.4, tail=1.4, min_hold={1: 5.0})
    return s


# ============================================================ PHẦN 1 – NHẬN HÀNG TC
def no_lpn_card(cid, x, y):
    return (f'<div id="{cid}" class="abs" style="left:{x}px;top:{y}px;opacity:0"><div style="display:flex;align-items:center;gap:22px;background:#fff;'
            f'border:5px solid {C["red"]};border-radius:22px;padding:18px 30px;box-shadow:0 12px 0 rgba(27,36,48,.10)">'
            f'<svg width="120" height="80" viewBox="0 0 120 80"><rect x="6" y="6" width="108" height="68" rx="8" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            f'<text x="60" y="34" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="24" fill="{INK}">LPN</text>'
            + "".join(f'<rect x="{20 + i*9}" y="44" width="{3 if i % 3 else 5}" height="20" fill="{INK}"/>' for i in range(9))
            + f'<line x1="4" y1="76" x2="116" y2="4" stroke="{C["red"]}" stroke-width="9" stroke-linecap="round"/></svg>'
            f'<div style="font-size:48px;font-weight:900">Không dùng LPN</div></div></div>')


def tc_dock():
    lines = ["Khi xe hàng TC về kho, nhân viên dỡ hàng xuống.",
             "Hàng TC không dán LPN."]

    def build(T, D):
        PX = 330
        body = svg_layer(
            st.floor()
            + f'<rect x="0" y="560" width="110" height="240" fill="#D5DBE4"/><text x="60" y="545" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="26" fill="{C["muted"]}">DOCK</text>'
            + f'<g transform="translate(1960,{FY})"><g id="tc1-truck-mv">{st.truck("tc1-truck", label="HÀNG TC")}</g></g>'
            + pallet_build("tc1-pal", PX, FY, sku="5001", lpn=False)
            + figure("tc1-rc", "receiver", 640, scale=1.5, label=True, extra=carry_box("tc1-rc", 1.5))
        ) + no_lpn_card("tc1-nolpn", 560, 200)
        js = ('tl.fromTo("#tc1-truck-mv",{x:0},{x:-1340,duration:1.6,ease:"power2.out"},0.0);\n'
              'tl.fromTo("#tc1-rc-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},0.6);\n')
        t = 1.4
        for trip in range(2):
            js += pose_js("tc1-rc", t, CARRY, dur=0.25)
            js += (f'tl.fromTo("#tc1-rc-box",{{opacity:0}},{{opacity:1,duration:0.15}},{t+0.1:.2f});\n' if trip == 0
                   else f'tl.to("#tc1-rc-box",{{opacity:1,duration:0.15}},{t+0.1:.2f});\n')
            js += f'tl.to("#tc1-rc",{{x:-170,duration:1.0,ease:"none"}},{t+0.3:.2f});\n' + walk_js("tc1-rc", t + 0.3, t + 1.3)
            js += f'tl.to("#tc1-rc-box",{{opacity:0,duration:0.1}},{t+1.35:.2f});\n'
            for k in (2 * trip, 2 * trip + 1):
                js += st.pop_js(f"#tc1-pal-c{k}", t + 1.35 + 0.12 * (k % 2), 0.3)
            js += pose_js("tc1-rc", t + 1.45, REST, dur=0.2)
            if trip == 0:
                js += f'tl.to("#tc1-rc",{{x:0,duration:0.9,ease:"none"}},{t+1.7:.2f});\n' + walk_js("tc1-rc", t + 1.7, t + 2.6)
            t += 2.7
        js += f'tl.fromTo("#tc1-nolpn",{{opacity:0,scale:1.6,rotation:-4}},{{opacity:1,scale:1,rotation:0,duration:0.35,ease:"power3.out"}},{T[1]+0.1:.2f});\n'
        return body, "", js
    s = Scene("tcdock", lines, build, lead=0.4, tail=1.4, pre={1: 2.9}, min_hold={1: 2.6})
    s.sfx = [(("T", 1, 0.1), "click-soft.mp3", 0.3)]
    return s


def tc_pda():
    lines = ["Trên PDA, nhân viên chọn phiếu ASN của xe hàng TC,",
             "scan mã hàng,",
             "và nhập thẳng số lượng nhận, không cần LPN, không nhập batch, lot hay ngày.",
             "Chỉ nhận đủ hoặc thiếu so với phiếu, không nhận dư."]

    def build(T, D):
        PX, RX, SC = 360, 720, 1.6
        a, b = SCAN["armR"]
        tip = hand(RX, FY, SC, a, b, flip=True, extra=56)
        stage_svg = (st.floor() + pallet_build("tc2-pal", PX, FY, sku="5001", shown=True, lpn=False)
                     + figure("tc2-rc", "receiver", RX, scale=SC, flip=True, pose=SCAN, hand_r=pda_svg("tc2-rc"))
                     + st.laser("tc2-las", tip[0], tip[1], PX + 38, FY - 46))
        body = svg_layer(stage_svg)
        rows = [("ASN-TC-0007", "SKU 5001 · 100 thùng"), ("ASN-0012", "Hàng kho khô"), ("ASN-TC-0008", "SKU 5002 · 60 thùng")]
        p1 = '<div class="lbl">Chọn phiếu ASN (TC)</div>' + "".join(
            f'<div class="row" style="position:relative"><b>{a_}</b><br><span style="font-size:24px;color:{C["muted"]}">{b_}</span>'
            + (f'<div id="tc2-sel" style="position:absolute;left:-3px;top:-3px;right:-3px;bottom:-3px;border:4px solid {C["blue"]};border-radius:12px;background:rgba(31,95,191,.08);opacity:0"></div>' if i == 0 else "")
            + '</div>' for i, (a_, b_) in enumerate(rows))
        p2 = kv("Scan mã hàng", "SKU 5001 ✔", "Nước suối thùng 24 chai (ví dụ)")
        off = f'border:3px dashed #C9D3E0;border-radius:12px;padding:10px 14px;font-size:26px;font-weight:700;color:#A9B2BF;margin-top:12px'
        p3 = (f'<div class="lbl">Số lượng nhận (phiếu: 100)</div><div class="fld ok">100 thùng</div>'
              f'<div id="tc2-o1" style="{off};opacity:0">LPN: không dùng</div><div id="tc2-o2" style="{off};opacity:0">Batch / Lot / Ngày: không nhập</div>')
        p4 = (f'<div class="lbl">Số lượng nhận (phiếu: 100)</div>'
              f'<div style="position:relative;height:150px">'
              f'<div id="tc2-over" class="abs" style="left:0;right:0;top:0"><div class="fld" style="border-color:{C["red"]};background:#FDECEC">110 thùng</div>'
              f'<div style="font-size:30px;font-weight:900;color:{C["red"]}">✖ Không nhận dư</div></div>'
              f'<div id="tc2-okq" class="abs" style="left:0;right:0;top:0;opacity:0"><div class="fld ok">100 thùng</div>'
              f'<div style="font-size:30px;font-weight:900;color:{C["green"]}">✔ Nhận đủ</div></div></div>'
              f'<div style="font-size:28px;font-weight:700;margin-top:6px">Ít hơn 100 = nhận thiếu</div>')
        body += st.pda("tc2-pda", "Nhận hàng TC", [("s1", p1), ("s2", p2), ("s3", p3), ("s4", p4)])
        body += "".join(st.badge(f"tc2-b{i+1}", i + 1, t) for i, t in enumerate(["Chọn phiếu ASN (TC)", "Scan mã hàng", "Nhập thẳng số lượng"]))
        body += (f'<div id="tc2-rule" class="abs" style="left:80px;top:56px;opacity:0"><span style="display:inline-block;background:#fff;border:5px solid {C["red"]};'
                 f'border-radius:18px;padding:10px 26px;font-size:40px;font-weight:900">Chỉ nhận đủ hoặc thiếu – không nhận dư</span></div>')
        js = st.appear_js("#tc2-pda", T[0], 0.35, dy=30)
        js += st.badge_seq_js(["tc2-b1", "tc2-b2", "tc2-b3"], T[0:3], T[3])
        js += f'tl.to("#tc2-b3",{{opacity:0,duration:0.15}},{T[3]-0.12:.2f});\n'
        js += st.show_panel_js("tc2-pda", None, "s1", T[0] + 0.1)
        js += f'tl.fromTo("#tc2-sel",{{opacity:0}},{{opacity:1,duration:0.2}},{T[0]+1.3:.2f});\n'
        js += st.show_panel_js("tc2-pda", "s1", "s2", T[1])
        js += st.laser_js("tc2-las", T[1] + 0.4)
        js += st.show_panel_js("tc2-pda", "s2", "s3", T[2])
        js += f'tl.fromTo("#tc2-o1",{{opacity:0,x:20}},{{opacity:1,x:0,duration:0.3}},{T[2]+1.2:.2f});\n'
        js += f'tl.fromTo("#tc2-o2",{{opacity:0,x:20}},{{opacity:1,x:0,duration:0.3}},{T[2]+2.4:.2f});\n'
        js += st.show_panel_js("tc2-pda", "s3", "s4", T[3])
        js += f'tl.fromTo("#tc2-rule",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{T[3]+0.1:.2f});\n'
        js += f'tl.to("#tc2-over",{{opacity:0,duration:0.2}},{T[3]+1.8:.2f});\ntl.fromTo("#tc2-okq",{{opacity:0}},{{opacity:1,duration:0.2}},{T[3]+1.9:.2f});\n'
        return body, "", js
    s = Scene("tcpda", lines, build, lead=0.4, tail=1.4, min_hold={0: 3.0, 1: 2.4, 2: 4.0, 3: 3.6})
    s.sfx = [(("T", 1, 0.4), "ping.mp3", 0.25), (("T", 3, 0.3), "error.mp3", 0.2)]
    return s



# ------------------------------------------------------------ shared TC pieces
def tc_zone_floor(x0=620, x1=1360, label=True):
    lab = (f'<rect x="{x0}" y="{FY-74}" width="160" height="54" rx="12" fill="{C["orange"]}" stroke="{INK}" stroke-width="3"/>'
           f'<text x="{x0+80}" y="{FY-36}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="30" fill="{INK}">KHU TC</text>' if label else "")
    return (f'<rect x="{x0}" y="{FY+8}" width="{x1-x0}" height="78" rx="10" fill="#FFE9D2" stroke="{C["orange"]}" stroke-width="5" stroke-dasharray="18 12"/>' + lab)


def tc_spot(sid, cx, code, qty=None):
    """Floor spot of one store inside the TC zone: sign with store code + barcode only (no location code).
    Hidden groups: {sid}-load (cartons + qty pill), {sid}-ok (tick)."""
    load = (f'<g id="{sid}-load" opacity="0">'
            + "".join(st.carton(cx - 96 + i*64, FY - 56, 62, 56) for i in range(3))
            + "".join(st.carton(cx - 64 + i*64, FY - 112, 62, 56) for i in range(2))
            + st.carton(cx - 32, FY - 168, 62, 56)
            + (f'<rect x="{cx-70}" y="{FY-226}" width="140" height="44" rx="22" fill="{INK}"/>'
               f'<text x="{cx}" y="{FY-196}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="28" fill="#fff">{qty}</text>' if qty else "")
            + '</g>')
    return (f'<g id="{sid}"><rect x="{cx-112}" y="{FY-4}" width="224" height="18" rx="6" fill="#FFD2A1" stroke="{C["orange"]}" stroke-width="3"/>'
            f'<line x1="{cx+96}" y1="{FY}" x2="{cx+96}" y2="{FY-250}" stroke="{INK}" stroke-width="6"/>'
            f'<g id="{sid}-sign"><rect x="{cx+20}" y="{FY-330}" width="152" height="86" rx="10" fill="#fff" stroke="{INK}" stroke-width="3.5"/>'
            f'<text x="{cx+96}" y="{FY-298}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="28" fill="{INK}">{code}</text>'
            + st.barcode(cx + 46, FY - 286, 100, 30) + '</g>'
            + load
            + f'<g id="{sid}-ok" opacity="0" transform="translate({cx+150},{FY-330})">'
            f'<circle r="26" fill="{C["green"]}"/><path d="M-11 1l7 7 14-15" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g></g>')


# ============================================================ PHẦN 1 (tiếp)
def tc_tozone():
    lines = ["Hàng nhận xong được mang vào khu TC trong kho, không cất lên kệ."]

    def build(T, D):
        mv = (f'<g transform="translate(260,0)"><g id="tc3-mv">{pallet_build("tc3-pal", 0, FY, sku="5001", shown=True, lpn=False)}'
              f'<g transform="translate(150,{FY})">{stick("tc3-rc", "receiver", 1.5, pose={"armL": (40, -30)})}</g></g></g>')
        norack = (f'<g id="tc3-norack" opacity="0" transform="translate(1610,330)"><rect x="-150" y="-150" width="300" height="300" rx="26" fill="#fff" stroke="{INK}" stroke-width="4"/>'
                  f'<g transform="translate(-60,-120)">' + mini_rack_svg() + '</g>'
                  f'<line x1="-90" y1="-110" x2="90" y2="70" stroke="{C["red"]}" stroke-width="12" stroke-linecap="round"/>'
                  f'<text x="0" y="122" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="30" fill="{C["red"]}">Không cất lên kệ</text></g>')
        body = svg_layer(st.floor() + tc_zone_floor() + mv + norack)
        js = f'tl.to("#tc3-mv",{{x:620,duration:2.6,ease:"none"}},{T[0]+0.2:.2f});\n' + walk_js("tc3-rc", T[0] + 0.2, T[0] + 2.8)
        js += st.pop_js("#tc3-norack", T[0] + 1.6, 0.4)
        return body, "", js
    return Scene("tctozone", lines, build, lead=0.4, tail=1.2, min_hold={0: 4.0})


def mini_rack_svg():
    return (f'<rect x="0" y="0" width="120" height="40" rx="4" fill="{C["reserved"]}"/><rect x="0" y="44" width="120" height="40" rx="4" fill="{C["reserved"]}"/>'
            f'<rect x="0" y="88" width="120" height="40" rx="4" fill="{C["orange"]}"/>'
            f'<path d="M0 -6v140M120 -6v140M0 42h120M0 86h120M0 130h120" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')


def ic(inner):
    from build_full import ic_svg
    return ic_svg(inner)


def tc_ghinho1():
    from build_full import ghinho
    return ghinho("tg1", 1, [
        (ic(f'<rect x="8" y="14" width="48" height="36" rx="5" fill="#fff" stroke="{INK}" stroke-width="3"/><text x="32" y="38" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="14">LPN</text><line x1="6" y1="54" x2="58" y2="10" stroke="{C["red"]}" stroke-width="6" stroke-linecap="round"/>'),
         "Không dùng LPN, <b>không nhập batch / lot / ngày</b>", "Không dùng LPN, không nhập batch / lot / ngày"),
        (ic(f'<rect x="10" y="8" width="44" height="48" rx="6" fill="#fff" stroke="{INK}" stroke-width="3"/><text x="32" y="40" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="20" fill="{C["green"]}">≤100</text>'),
         "Nhập thẳng số lượng – <b>chỉ nhận đủ hoặc thiếu</b>, không nhận dư", "Nhập thẳng số lượng, chỉ nhận đủ hoặc thiếu, không nhận dư"),
        (ic(f'<rect x="4" y="30" width="56" height="26" rx="5" fill="#FFE9D2" stroke="{C["orange"]}" stroke-width="3" stroke-dasharray="6 4"/><text x="32" y="49" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="13" fill="#C45A00">KHU TC</text>'),
         "Để tại <b>khu TC</b>, không cất lên kệ", "Để tại khu TC, không cất lên kệ"),
    ])


# ============================================================ PHẦN 2 – CHIA HÀNG
STORES = [("CH-0125", 30), ("CH-0311", 45), ("CH-0420", 25)]


def tc_do():
    lines = ["DO của các cửa hàng đã có sẵn số lượng cần.",
             "Hệ thống dùng chính hàng TC vừa nhập để chia cho từng cửa hàng."]

    def build(T, D):
        src = svg_layer(st.floor() + pallet_build("tc4-pal", 360, FY, sku="5001", shown=True, lpn=False)
                        + f'<text x="360" y="{FY-170}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="34" fill="{INK}">Hàng TC vừa nhập</text>'
                        + f'<text x="360" y="{FY-220}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="44" fill="#C45A00">SKU 5001 · 100 thùng</text>'
                        + "".join(f'<path id="tc4-ar{i}" d="M560,{FY-110} C760,{FY-110} 820,{210 + i*170} 1010,{210 + i*170}" fill="none" stroke="{C["orange"]}" stroke-width="7" '
                                  f'stroke-linecap="round" stroke-dasharray="700" stroke-dashoffset="700"/>' for i in range(3)))
        cards = ""
        for i, (code, q) in enumerate(STORES):
            cards += (f'<div id="tc4-d{i}" class="abs" style="left:1030px;top:{150 + i*170}px;width:620px;opacity:0"><div style="display:flex;align-items:center;gap:20px;'
                      f'background:#fff;border:4px solid {INK};border-radius:20px;padding:16px 26px">'
                      f'<span style="background:{C["blue"]};color:#fff;border-radius:10px;padding:6px 14px;font-size:30px;font-weight:900">DO</span>'
                      f'<span style="font-size:40px;font-weight:900;flex:1">{code}</span><span style="font-size:40px;font-weight:900;color:#C45A00">cần {q}</span></div></div>')
        cards += (f'<div id="tc4-sum" class="abs" style="left:1030px;top:660px;width:620px;text-align:center;opacity:0"><span style="display:inline-block;background:{C["green"]};color:#fff;'
                  f'border:4px solid {INK};border-radius:18px;padding:10px 26px;font-size:36px;font-weight:900">Tổng DO 100 = Nhận 100 ✔</span></div>')
        js = ""
        for i in range(3):
            js += f'tl.fromTo("#tc4-d{i}",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.35,ease:"power3.out"}},{T[0]+0.2+i*0.35:.2f});\n'
            js += f'tl.to("#tc4-ar{i}",{{strokeDashoffset:0,duration:0.7,ease:"power2.inOut"}},{T[1]+0.2+i*0.25:.2f});\n'
        js += st.pop_js("#tc4-sum", T[1] + 1.4)
        return src + cards, "", js
    return Scene("tcdo", lines, build, lead=0.4, tail=1.4, min_hold={1: 3.8})


def tc_spots():
    lines = ["Trong khu TC, mỗi cửa hàng có một vị trí riêng, chỉ dán mã cửa hàng, không có mã vị trí."]

    def build(T, D):
        spots = "".join(tc_spot(f"tc5-s{i}", 520 + i*420, code) for i, (code, _) in enumerate(STORES))
        body = svg_layer(st.floor() + tc_zone_floor(300, 1620) + spots)
        body += (f'<div id="tc5-noloc" class="abs" style="left:80px;top:70px;opacity:0"><div style="display:flex;align-items:center;gap:18px;background:#fff;border:5px solid {C["red"]};'
                 f'border-radius:20px;padding:12px 26px;font-size:40px;font-weight:900">'
                 f'<span style="position:relative;border:3px solid {INK};border-radius:8px;padding:2px 12px;font-size:32px">A-01-01'
                 f'<span style="position:absolute;left:-6px;right:-6px;top:50%;height:6px;background:{C["red"]};border-radius:3px"></span></span>Không có mã vị trí – chỉ có mã cửa hàng</div></div>')
        js = ""
        for i in range(3):
            js += f'tl.fromTo("#tc5-s{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{T[0]+0.2+i*0.35:.2f});\n'
            js += f'tl.fromTo("#tc5-s{i}-sign",{{scale:1}},{{scale:1.12,duration:0.2,yoyo:true,repeat:1,transformOrigin:"50% 50%"}},{T[0]+1.8+i*0.3:.2f});\n'
        js += f'tl.fromTo("#tc5-noloc",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{T[0]+2.4:.2f});\n'
        return body, "", js
    return Scene("tcspots", lines, build, lead=0.4, tail=1.4, min_hold={0: 5.0})


def tc_sort():
    lines = ["Nhân viên scan mã hàng,",
             "PDA hiện cửa hàng và số lượng cần chia.",
             "Đến vị trí của cửa hàng đó, scan mã cửa hàng,",
             "đặt đúng số lượng rồi xác nhận.",
             "Lặp lại cho đến khi chia hết hàng."]
    SX = [700, 940, 1180]           # spot centres (PDA occupies x >= 1390)

    def build(T, D):
        SC = 1.4
        spots = "".join(tc_spot(f"tc6-s{i}", SX[i], code, qty=f"{q} thùng") for i, (code, q) in enumerate(STORES))
        PX0, PSPOT = 400, SX[0] - 130
        scan_up = {"armR": (-115, -15)}
        tip = hand(PSPOT, FY, SC, *scan_up["armR"], extra=56)
        sign = (SX[0] + 96, FY - 268)
        tip0 = hand(PX0, FY, SC, *SCAN["armR"], extra=56)
        pk = (f'<g transform="translate({PX0},{FY})"><g id="tc6-mv">{stick("tc6-pk", "picker", SC, label=True, hand_r=pda_svg("tc6-pk"))}'
              f'{carry_box("tc6-pk", SC)}</g></g>')
        counts = "".join(f'<text id="tc6-c{i}" x="200" y="{FY-190}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="40" fill="#C45A00" opacity="{1 if i == 0 else 0}">Còn: {n}</text>'
                         for i, n in enumerate((100, 70, 25, 0)))
        body = svg_layer(st.floor() + tc_zone_floor(560, 1340, label=False) + pallet_build("tc6-pal", 200, FY, sku="5001", shown=True, lpn=False)
                         + counts + spots + pk
                         + st.laser("tc6-las1", tip0[0], tip0[1], 238, FY - 46) + st.laser("tc6-las2", tip[0], tip[1], *sign))
        body += st.pda("tc6-pda", "Chia hàng TC", [
            ("s1", kv("Scan mã hàng", "SKU 5001 ✔", "Còn 100 thùng chưa chia")),
            ("s2", kv("Chia cho cửa hàng", "CH-0125", "") + kv("Số lượng", "30 thùng", "", "#C45A00")),
            ("s3", kv("Scan mã cửa hàng", "CH-0125 ✔", "Đúng vị trí của cửa hàng")),
            ("s4", kv("CH-0125", "Đã đặt 30 thùng", "") + '<div id="tc6-go" class="go">XÁC NHẬN</div>'),
            ("s5", kv("SKU 5001", "Đã chia hết ✔", "CH-0125: 30 · CH-0311: 45 · CH-0420: 25")),
        ])
        body += "".join(st.badge(f"tc6-b{i+1}", i + 1, t) for i, t in enumerate(
            ["Scan mã hàng", "Xem cửa hàng & số lượng", "Đến vị trí, scan mã cửa hàng", "Đặt đủ số lượng, xác nhận"]))
        js = 'tl.fromTo("#tc6-pk-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},0.2);\n'
        js += st.appear_js("#tc6-pda", 0.1, 0.35, dy=30)
        js += st.badge_seq_js([f"tc6-b{i+1}" for i in range(4)], T[0:4], T[4])
        js += f'tl.to("#tc6-b4",{{opacity:0,duration:0.15}},{T[4]-0.12:.2f});\n'
        js += st.show_panel_js("tc6-pda", None, "s1", T[0])
        js += pose_js("tc6-pk", T[0], SCAN, dur=0.25, ease="power2.out") + st.laser_js("tc6-las1", T[0] + 0.4)
        js += st.show_panel_js("tc6-pda", "s1", "s2", T[1])
        js += pose_js("tc6-pk", T[1] + 0.3, CARRY, dur=0.25)
        js += f'tl.fromTo("#tc6-pk-box",{{opacity:0}},{{opacity:1,duration:0.15}},{T[1]+0.4:.2f});\n'
        js += f'tl.to("#tc6-mv",{{x:{PSPOT-PX0},duration:1.3,ease:"none"}},{T[1]+0.7:.2f});\n' + walk_js("tc6-pk", T[1] + 0.7, T[1] + 2.0)
        js += st.show_panel_js("tc6-pda", "s2", "s3", T[2])
        js += pose_js("tc6-pk", T[2] + 0.1, {"armL": (34, -104), "armR": scan_up["armR"]}, dur=0.25, ease="power2.out")
        js += st.laser_js("tc6-las2", T[2] + 0.5)
        js += st.show_panel_js("tc6-pda", "s3", "s4", T[3])
        js += pose_js("tc6-pk", T[3], CARRY, dur=0.2)
        js += f'tl.to("#tc6-pk-box",{{opacity:0,duration:0.1}},{T[3]+0.3:.2f});\n'
        js += f'tl.fromTo("#tc6-s0-load",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.35,ease:"bounce.out"}},{T[3]+0.3:.2f});\n'
        js += f'tl.set("#tc6-c0",{{opacity:0}},{T[3]+0.4:.2f});\ntl.set("#tc6-c1",{{opacity:1}},{T[3]+0.4:.2f});\n'
        js += f'tl.to("#tc6-go",{{scale:0.94,duration:0.1}},{T[3]+1.0:.2f});\ntl.to("#tc6-go",{{scale:1,duration:0.15}},{T[3]+1.1:.2f});\n'
        js += st.pop_js("#tc6-s0-ok", T[3] + 1.2, 0.3)
        # repeat for the other two stores, faster
        t = T[4] + 0.1
        x_prev = PSPOT
        for i in (1, 2):
            js += f'tl.to("#tc6-pk-box",{{opacity:1,duration:0.1}},{t:.2f});\n'
            js += f'tl.to("#tc6-mv",{{x:{SX[i]-130-PX0},duration:0.9,ease:"none"}},{t+0.1:.2f});\n' + walk_js("tc6-pk", t + 0.1, t + 1.0)
            js += f'tl.to("#tc6-pk-box",{{opacity:0,duration:0.1}},{t+1.1:.2f});\n'
            js += f'tl.fromTo("#tc6-s{i}-load",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.35,ease:"bounce.out"}},{t+1.1:.2f});\n'
            js += f'tl.set("#tc6-c{i}",{{opacity:0}},{t+1.2:.2f});\ntl.set("#tc6-c{i+1}",{{opacity:1}},{t+1.2:.2f});\n'
            js += st.pop_js(f"#tc6-s{i}-ok", t + 1.3, 0.3)
            t += 1.6
        js += st.show_panel_js("tc6-pda", "s4", "s5", t)
        return body, "", js
    s = Scene("tcsort", lines, build, lead=0.5, tail=1.4, min_hold={0: 2.4, 1: 2.8, 2: 3.2, 3: 3.0, 4: 4.0})
    s.sfx = [(("T", 0, 0.4), "ping.mp3", 0.25), (("T", 3, 1.2), "chime.mp3", 0.22)]
    return s


def tc_zero():
    lines = ["Hàng TC nhập bao nhiêu thì chia hết bấy nhiêu, không để lại tồn kho."]

    def build(T, D):
        body = (f'<div id="tc7-eq" class="abs" style="left:0;top:250px;width:1920px;text-align:center;opacity:0">'
                f'<div style="display:inline-flex;align-items:center;gap:34px;font-size:84px;font-weight:900">'
                f'<span style="background:#fff;border:5px solid {INK};border-radius:24px;padding:18px 40px">Nhận 100</span><span>=</span>'
                f'<span style="background:#fff;border:5px solid {INK};border-radius:24px;padding:18px 40px">Chia 100</span></div></div>'
                f'<div id="tc7-zero" class="abs" style="left:0;top:520px;width:1920px;text-align:center;opacity:0">'
                f'<span style="display:inline-block;background:{C["green"]};color:#fff;border:5px solid {INK};border-radius:24px;padding:16px 44px;font-size:72px;font-weight:900">Tồn TC: 0</span></div>')
        js = st.appear_js("#tc7-eq", T[0] + 0.1, 0.4, dy=24) + st.pop_js("#tc7-zero", T[0] + 1.4, 0.4)
        return body, "", js
    return Scene("tczero", lines, build, lead=0.4, tail=1.2, min_hold={0: 3.8})


def tc_short():
    lines = ["Nếu nhận thiếu, hàng được phân bổ từ trên xuống.",
             "Các cửa hàng phía trên nhận đủ, cửa hàng phía dưới có thể không có hàng."]

    def build(T, D):
        rows = ""
        res = [(30, True), (45, True), (0, False)]
        for i, ((code, q), (got, ok)) in enumerate(zip(STORES, res)):
            col = C["green"] if ok else C["red"]
            rows += (f'<div id="tc8-r{i}" class="abs" style="left:400px;top:{330 + i*150}px;width:1260px;opacity:0"><div style="display:flex;align-items:center;gap:26px;'
                     f'background:#fff;border:4px solid {INK};border-radius:20px;padding:16px 28px;font-size:40px;font-weight:900">'
                     f'<span style="width:60px;color:{C["muted"]}">{i+1}</span><span style="width:220px">{code}</span>'
                     f'<span style="width:170px;color:{C["muted"]}">cần {q}</span>'
                     f'<span id="tc8-g{i}" style="flex:1;white-space:nowrap;color:{col};opacity:0">→ chia {got} {"✔ đủ" if ok else "✖ không có hàng"}</span></div></div>')
        head = (f'<div id="tc8-h" class="abs" style="left:0;top:120px;width:1920px;text-align:center;opacity:0"><span style="display:inline-block;background:#fff;'
                f'border:5px solid {C["orange"]};border-radius:20px;padding:12px 34px;font-size:50px;font-weight:900">Ví dụ: chỉ nhận <span style="color:{C["red"]}">75</span> / 100 thùng</span></div>')
        arr = svg_layer(f'<g id="tc8-arr" opacity="0"><line x1="330" y1="340" x2="330" y2="740" stroke="{C["orange"]}" stroke-width="12" stroke-linecap="round"/>'
                        f'<path d="M306,716 L330,756 L354,716" fill="none" stroke="{C["orange"]}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
                        f'<text x="300" y="560" text-anchor="end" font-family="{FONT}" font-weight="900" font-size="32" fill="#C45A00">Từ trên</text>'
                        f'<text x="300" y="600" text-anchor="end" font-family="{FONT}" font-weight="900" font-size="32" fill="#C45A00">xuống</text></g>')
        left = "".join(f'<div id="tc8-l{i}" class="abs" style="left:1560px;top:230px;width:300px;text-align:center;opacity:{1 if i == 0 else 0};font-size:36px;font-weight:900;color:#C45A00">Còn: {n}</div>'
                       for i, n in enumerate((75, 45, 0)))
        js = st.appear_js("#tc8-h", T[0]) + f'tl.fromTo("#tc8-arr",{{opacity:0}},{{opacity:1,duration:0.3}},{T[0]+0.4:.2f});\n'
        for i in range(3):
            js += f'tl.fromTo("#tc8-r{i}",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.3,ease:"power2.out"}},{T[0]+0.5+i*0.25:.2f});\n'
            tg = T[1] + 0.2 + i * 1.0
            js += f'tl.fromTo("#tc8-g{i}",{{opacity:0,x:-10}},{{opacity:1,x:0,duration:0.3}},{tg:.2f});\n'
            if i < 2:
                js += f'tl.set("#tc8-l{i}",{{opacity:0}},{tg:.2f});\ntl.set("#tc8-l{i+1}",{{opacity:1}},{tg:.2f});\n'
        return arr + head + rows + left, "", js
    return Scene("tcshort", lines, build, lead=0.4, tail=1.6, min_hold={1: 4.4})


def tc_handover():
    lines = ["Khi bàn giao, nhân viên gom hàng chẵn, hàng lẻ và hàng ở vị trí TC của từng cửa hàng,",
             "rồi bàn giao cho vận tải như bình thường."]

    def build(T, D):
        def lab(x, text):
            return (f'<rect x="{x-90}" y="{FY-420}" width="180" height="50" rx="14" fill="#fff" stroke="{INK}" stroke-width="3"/>'
                    f'<text x="{x}" y="{FY-385}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="28" fill="{INK}">{text}</text>')
        srcs = (f'<g id="tc9-a"><g transform="translate(150,{FY})">{st.trolley("tc9-tr", "CH-0125")}</g></g>' + lab(250, "Hàng chẵn")
                + f'<g id="tc9-b"><g transform="translate(560,{FY})">{st.oricon("tc9-or", "CH-0125")}</g></g>' + lab(560, "Hàng lẻ")
                + f'<g id="tc9-c">{tc_spot("tc9-sp", 860, "CH-0125")}</g>' + lab(860, "Vị trí TC"))
        trk = f'<g transform="translate(1180,{FY})">{st.truck("tc9-truck", label="CH-0125")}</g>'
        tp = f'<g transform="translate(1690,{FY})">{stick("tc9-tp", "transport", 1.5, label=True, pose={"armR": (-30, -80)}, hand_r=pda_svg("tc9-tp"))}</g>'
        arrows = "".join(f'<path id="tc9-ar{i}" d="M{x},{FY-430} C{x+120},{FY-560} 1150,{FY-560} 1300,{FY-250}" fill="none" stroke="{C["orange"]}" stroke-width="7" '
                         f'stroke-linecap="round" stroke-dasharray="1300" stroke-dashoffset="1300"/>' for i, x in enumerate((250, 560, 860)))
        body = svg_layer(st.floor() + srcs + trk + tp + arrows) + st.stamp("tc9-done", "Bàn giao CH-0125", x=1180, y=150)
        js = ""
        for k in range(4):
            js += f'tl.set("#tc9-tr-k{k}",{{opacity:1}},0);\n'
        js += 'tl.set("#tc9-sp-load",{opacity:1},0);\n'
        for i, g in enumerate(("a", "b", "c")):
            t = T[0] + 0.5 + i * 0.9
            js += f'tl.fromTo("#tc9-{g}",{{scale:1}},{{scale:1.06,duration:0.2,yoyo:true,repeat:1,transformOrigin:"50% 100%"}},{t:.2f});\n'
            js += f'tl.to("#tc9-ar{i}",{{strokeDashoffset:0,duration:0.8,ease:"power2.inOut"}},{t+0.1:.2f});\n'
        js += 'tl.fromTo("#tc9-tp-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},%.2f);\n' % T[1]
        js += st.stamp_js("tc9-done", T[1] + 0.8)
        return body, "", js
    s = Scene("tchand", lines, build, lead=0.4, tail=1.6, min_hold={0: 5.0, 1: 3.0})
    s.sfx = [(("T", 1, 0.8), "chime.mp3", 0.22)]
    return s


def tc_ghinho2():
    from build_full import ghinho
    return ghinho("tg2", 2, [
        (ic(f'<rect x="6" y="20" width="22" height="22" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2"/><path d="M30 31h12M38 24l8 7-8 7" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><rect x="48" y="14" width="12" height="34" rx="3" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'),
         "Chia theo DO: scan mã hàng → đến vị trí cửa hàng → <b>scan mã cửa hàng</b> → đặt hàng, xác nhận",
         "Chia theo DO: scan mã hàng, đến vị trí cửa hàng, scan mã cửa hàng, đặt hàng, xác nhận"),
        (ic(f'<path d="M32 8v40M20 36l12 14 12-14" fill="none" stroke="{C["orange"]}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'),
         "Nhận thiếu: <b>phân bổ từ trên xuống</b>", "Nhận thiếu: phân bổ từ trên xuống"),
        (ic(f'<rect x="4" y="18" width="36" height="26" rx="3" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M40 26h10l8 10v8H40z" fill="{C["blue"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><circle cx="14" cy="48" r="6" fill="{INK}"/><circle cx="48" cy="48" r="6" fill="{INK}"/>'),
         "Bàn giao: gom <b>hàng chẵn + hàng lẻ + vị trí TC</b>", "Bàn giao: gom hàng chẵn, hàng lẻ, vị trí TC"),
    ])


def tc_end():
    lines = ["Đó là toàn bộ quy trình hàng TC. Chúc các bạn làm việc thật tốt!"]
    steps = ["Nhận hàng (không LPN)", "Khu TC", "Chia theo DO", "Gom & Bàn giao"]

    def build(T, D):
        W, G, X0 = 360, 60, 120
        chips = ""
        for i, t in enumerate(steps):
            x = X0 + i * (W + G)
            chips += (f'<div id="tc10-s{i}" class="abs" style="left:{x}px;top:220px;width:{W}px;height:150px;background:#fff;border:4px solid {INK};border-radius:22px;'
                      f'display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0">'
                      f'<div style="font-size:30px;font-weight:900;color:#C45A00">{i+1}</div><div style="font-size:36px;font-weight:900;text-align:center;line-height:1.15">{t}</div></div>')
            if i < len(steps) - 1:
                chips += f'<div id="tc10-a{i}" class="abs" style="left:{x+W}px;top:262px;width:{G}px;text-align:center;font-size:50px;font-weight:900;color:{C["blue"]};opacity:0">›</div>'
        thumb = f'<circle cx="0" cy="25" r="8" fill="{INK}"/><line x1="0" y1="30" x2="0" y2="44" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        man = svg_layer(f'<g transform="translate(960,{FY+40})"><g id="tc10-man">{stick("tc10-man", "instructor", 2.0, hand_r=thumb)}</g></g>')
        body = f'<div class="abs" style="left:0;top:{FY}px;width:1920px;height:{1080-FY}px;background:{C["floor"]}"></div>' + chips + man
        js = ""
        for i in range(len(steps)):
            js += f'tl.fromTo("#tc10-s{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{0.3 + i*0.35:.2f});\n'
            if i < len(steps) - 1:
                js += f'tl.fromTo("#tc10-a{i}",{{opacity:0}},{{opacity:1,duration:0.2}},{0.5 + i*0.35:.2f});\n'
        js += pose_js("tc10-man", T[0] + 1.2, {"armR": (-100, -80)}, dur=0.35, ease="back.out(2)")
        return body, "", js
    s = Scene("tcend", lines, build, lead=0.6, tail=2.6, min_hold={0: 4.0})
    s.sfx = [(("T", 0, 1.2), "chime.mp3", 0.22)]
    return s


def timeline():
    return [tc_intro(), chapter(1, "Nhận hàng TC"), tc_dock(), tc_pda(), tc_tozone(), tc_ghinho1(),
            chapter(2, "Xuất hàng TC – chia cho cửa hàng", lead=2.7), tc_do(), tc_spots(), tc_sort(), tc_zero(), tc_short(), tc_handover(), tc_ghinho2(),
            tc_end()]

if __name__ == "__main__":
    limit = float(sys.argv[1]) if len(sys.argv) > 1 else None
    os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
    placed, total, kept = build_all(limit, seq=timeline(), out=OUT)
    for s, start in placed:
        print(f"{start:7.2f}  {s.D:6.2f}  {s.cid}")
    print("TOTAL", total, "sfx", len(kept))
