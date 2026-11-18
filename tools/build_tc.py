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
            + pallet_build("tc1-pal", PX, FY, sku="5001")
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
        stage_svg = (st.floor() + pallet_build("tc2-pal", PX, FY, sku="5001", shown=True)
                     + figure("tc2-rc", "receiver", RX, scale=SC, flip=True, pose=SCAN, hand_r=pda_svg("tc2-rc"))
                     + st.laser("tc2-las", tip[0], tip[1], PX + 38, FY - 46))
        body = svg_layer(stage_svg) + '<style>#tc2-pal-lpn{display:none}</style>'
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


def timeline():
    return [tc_intro(), chapter(1, "Nhận hàng TC"), tc_dock(), tc_pda()]


if __name__ == "__main__":
    limit = float(sys.argv[1]) if len(sys.argv) > 1 else None
    os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
    placed, total, kept = build_all(limit, seq=timeline(), out=OUT)
    for s, start in placed:
        print(f"{start:7.2f}  {s.D:6.2f}  {s.cid}")
    print("TOTAL", total, "sfx", len(kept))
