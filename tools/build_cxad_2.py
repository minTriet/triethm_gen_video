"""Parts 2–4 and the ending of the CXAD video (imported by tools/build_cxad.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, stick, walk_js, pose_js, REST, pda_svg, folder_svg, MANAGER_HOLD
import stage as st
from stage import FY, INK
from build_full import Scene, chapter, ghinho, ic_svg
from parts import figure, svg_layer, kv, hand, SCAN, CARRY, carry_box, pda_popup, swap_js
import cxad_kit as K
from cxad_kit import cbadge, wms, decision, decision_js, card
import build_cxad as B

DOS = ["DO-1001", "DO-1002", "DO-1003"]


def sel_row(rid, text, right="", sel=False):
    return (f'<div id="{rid}" class="row{" sel" if sel else ""}" style="opacity:0"><span>{text}</span><span>{right}</span></div>')


def check_box(cid):
    return (f'<span style="display:inline-flex;width:34px;height:34px;border:3px solid {INK};border-radius:6px;align-items:center;justify-content:center;margin-right:12px;vertical-align:-6px">'
            f'<svg id="{cid}" width="26" height="26" viewBox="0 0 26 26" style="opacity:0"><path d="M4 13l6 6 12-13" fill="none" stroke="{C["green"]}" stroke-width="5" stroke-linecap="round"/></svg></span>')


def zone_tag(z, fs=30, extra=""):
    tint, edge, name = K.ZONES[z]
    return f'<span style="display:inline-block;background:{edge};color:#fff;border:3px solid {INK};border-radius:12px;padding:4px 16px;font-size:{fs}px;font-weight:900;{extra}">{name}</span>'


# ============================================================ PHẦN 2 – LẤY HÀNG GỘP THEO XE (04K.1)
def p2_doin():
    lines = ["Với hàng xuất, XLCT nhận file đơn hàng DO qua email và chỉnh đúng định dạng của WMS.",
             "Import file để tạo các DO."]

    def build(T, D):
        body = svg_layer(st.floor() + K.office("o2-pl", 260))
        body += K.mail("o2-mail", 560, 170, "Đơn hàng xuất – CXAD", "Don_hang_DO.xlsx")
        body += K.sheet("o2-sh", 560, 420)
        rows = "".join(sel_row(f"o2-r{i}", f"<b>DO-100{i+1}</b> · Nơi giao {i+1:02d}", f'<span style="color:{C["green"]}">✔</span>') for i in range(5))
        body += wms("o2-w", "Đơn hàng xuất · DO", [("p1", f'<div class="lbl">Các DO vừa tạo</div>{rows}')], x=980, y=130, w=840, h=520)
        body += cbadge("o2-b1", 1, "Nhận kế hoạch xuất", "TC") + cbadge("o2-b2", 2, "Import vào WMS", "WMS")
        js = K.label_js("o2-pl", 0.3) + st.badge_seq_js(["o2-b1", "o2-b2"], T, D - 0.2)
        js += st.appear_js("#o2-mail", T[0] + 0.3, 0.35, dy=20) + st.appear_js("#o2-sh", T[0] + 1.8, 0.35, dy=20)
        js += K.sheet_fix_js("o2-sh", T[0] + 2.8) + K.type_js("o2-pl", T[0] + 1.8, T[0] + 4.0)
        js += f'tl.to(["#o2-mail","#o2-sh"],{{opacity:0,duration:0.3}},{T[1]:.2f});\n'
        js += st.appear_js("#o2-w", T[1], 0.35, dy=20) + f'tl.set("#o2-w-p1",{{opacity:1}},{T[1]:.2f});\n'
        for i in range(5):
            js += st.pop_js(f"#o2-r{i}", T[1] + 0.4 + i * 0.3, 0.25)
        return body, "", js
    s = Scene("p2doin", lines, build, lead=0.5, tail=1.4, min_hold={0: 5.0, 1: 3.2})
    s.sfx = [(("T", 0, 0.3), "notification.mp3", 0.25)]
    return s


def do_card(cid, code, x, y, w=220):
    return (f'<div id="{cid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;opacity:0;background:#fff;border:4px solid {INK};border-radius:14px;'
            f'padding:10px 14px;font-size:28px;font-weight:900;box-shadow:0 6px 0 rgba(27,36,48,.08)">{code}</div>')


def p2_master():
    lines = ["XLCT gom các DO giao cùng một xe thành một Master DO.",
             "Một xe là một Master DO."]

    def build(T, D):
        WX, WY = 120, 150
        win = wms("m2-w", "Tạo Master DO", [("p1", "")], x=WX, y=WY, w=1680, h=600)
        truck_ic = (f'<svg width="120" height="64" viewBox="0 0 120 64"><rect x="2" y="6" width="74" height="42" rx="4" fill="#fff" stroke="{INK}" stroke-width="4"/>'
                    f'<path d="M76 18h22l16 16v14H76z" fill="{C["blue"]}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                    f'<circle cx="22" cy="54" r="9" fill="{INK}"/><circle cx="96" cy="54" r="9" fill="{INK}"/></svg>')
        lanes = ""
        for j, (name, mdo) in enumerate([("Xe 1", "MDO-01"), ("Xe 2", "MDO-02")]):
            y = WY + 100 + j * 250
            lanes += (f'<div id="m2-l{j}" class="abs" style="left:620px;top:{y}px;width:1140px;height:220px;border:4px dashed #C9D3E0;border-radius:20px;opacity:0">'
                      f'<div class="abs" style="left:20px;top:20px;display:flex;align-items:center;gap:14px">{truck_ic}<div style="font-size:40px;font-weight:900">{name}</div></div>'
                      f'<div id="m2-m{j}" class="abs" style="left:20px;top:130px;opacity:0;background:{C["blue"]};color:#fff;border-radius:14px;padding:8px 18px;font-size:32px;font-weight:900">Master DO: {mdo}</div></div>')
        cards = "".join(do_card(f"m2-d{i}", f"DO-100{i+1}", 200, WY + 100 + i * 96) for i in range(5))
        eq = (f'<div id="m2-eq" class="abs" style="left:190px;top:600px;opacity:0"><span class="pill" style="border-color:{C["orange"]}">1 xe = 1 Master DO</span></div>')
        body = B.bg_floor() + win + lanes + cards + eq + cbadge("m2-b3", 3, "Tạo Master DO", "WMS")
        js = st.badge_seq_js(["m2-b3"], [T[0]], D - 0.2)
        js += st.appear_js("#m2-w", 0.1, 0.35, dy=20)
        for j in range(2):
            js += st.appear_js(f"#m2-l{j}", 0.4 + j * 0.2, 0.3)
        for i in range(5):
            js += st.pop_js(f"#m2-d{i}", 0.6 + i * 0.1, 0.25)
        dest = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        for i, (lane, slot) in enumerate(dest):
            tx = 900 + slot * 260 - 200
            ty = WY + 100 + lane * 250 + 30 - (WY + 100 + i * 96)
            js += f'tl.to("#m2-d{i}",{{x:{tx},y:{ty},duration:0.7,ease:"power2.inOut"}},{T[0] + 0.4 + i*0.45:.2f});\n'
        js += st.pop_js("#m2-m0", T[1] + 0.1) + st.pop_js("#m2-m1", T[1] + 0.4)
        js += f'tl.fromTo("#m2-eq",{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:0.35,ease:"power3.out"}},{T[1]+0.8:.2f});\n'
        return body, "", js
    s = Scene("p2master", lines, build, lead=0.8, tail=1.6, min_hold={0: 3.6, 1: 3.0})
    s.sfx = [(("T", 1, 0.8), "click-soft.mp3", 0.3)]
    return s


def p2_alloc():
    lines = ["Bấm phân bổ tồn, hệ thống tự chọn hàng theo FIFO hoặc FEFO."]

    def build(T, D):
        lots = [("Lô A", "HSD 10/2026", "K-01-02"), ("Lô B", "HSD 03/2027", "K-02-03"), ("Lô C", "HSD 08/2027", "K-03-02")]
        rows = ""
        for i, (a, b, c) in enumerate(lots):
            rows += (f'<div id="al-r{i}" class="row" style="position:relative"><span><b>{a}</b> · {b}</span><span>{c}</span>'
                     + (f'<div id="al-sel" class="abs" style="left:-3px;top:-3px;right:-3px;bottom:-3px;border:5px solid {C["green"]};border-radius:10px;background:rgba(34,165,90,.10);opacity:0"></div>' if i == 0 else "")
                     + '</div>')
        p1 = (f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px"><div class="lbl" style="margin:0">Tồn kho SKU 2001 · MDO-01, MDO-02</div>'
              f'<div id="al-btn" class="btnw">PHÂN BỔ TỒN</div></div>{rows}'
              f'<div id="al-pick" style="opacity:0;margin-top:14px;font-size:30px;font-weight:900;color:{C["green"]}">✔ Lô A được chọn trước (hạn gần nhất)</div>')
        body = B.bg_floor() + wms("al-w", "Phân bổ tồn", [("p1", p1)], x=300, y=150, w=1100, h=520) + K.cursor("al-cur")
        body += (f'<div id="al-rule" class="abs" style="left:1440px;top:250px;width:420px;opacity:0;background:#fff;border:5px solid {C["orange"]};border-radius:20px;padding:18px 22px">'
                 f'<div style="font-size:38px;font-weight:900">FIFO</div><div style="font-size:26px;font-weight:700">Nhập trước, xuất trước</div>'
                 f'<div style="font-size:38px;font-weight:900;margin-top:14px">FEFO</div><div style="font-size:26px;font-weight:700">Hết hạn trước, xuất trước</div></div>')
        body += cbadge("al-b4", 4, "Phân bổ tồn", "WMS")
        js = st.badge_seq_js(["al-b4"], [T[0]], D - 0.2)
        js += st.appear_js("#al-w", 0.1, 0.35, dy=20) + 'tl.set("#al-w-p1",{opacity:1},0.1);\n'
        js += K.click_js("al-cur", 900, 600, 1240, 248, T[0] + 0.2, target="#al-btn")
        js += f'tl.to("#al-cur",{{opacity:0,duration:0.2}},{T[0]+1.4:.2f});\n'
        js += f'tl.fromTo("#al-sel",{{opacity:0}},{{opacity:1,duration:0.3}},{T[0]+1.3:.2f});\n'
        js += st.appear_js("#al-pick", T[0] + 1.6) + st.appear_js("#al-rule", T[0] + 2.4, 0.35)
        return body, "", js
    s = Scene("p2alloc", lines, build, lead=0.6, tail=1.8, min_hold={0: 5.0})
    s.sfx = [(("T", 0, 0.85), "click-soft.mp3", 0.3)]
    return s


def p2_list():
    lines = ["Khi tạo phiếu lấy hàng, có thể chọn một hoặc nhiều Master DO lấy cùng lúc.",
             "Hệ thống gộp tổng số lượng theo từng mã hàng,",
             "quy đổi ra thùng và pcs, ví dụ 55 pcs, quy cách 50, là 1 thùng 5 pcs,",
             "và tách phiếu theo khu: đông, chill, khô."]

    def build(T, D):
        q1 = (f'<div class="lbl">Chọn Master DO lấy cùng lúc</div>'
              f'<div id="pl-c0" class="row" style="justify-content:flex-start;font-size:32px">{check_box("pl-k0")}<b>MDO-01</b>&nbsp;· Xe 1 · 3 DO</div>'
              f'<div id="pl-c1" class="row" style="justify-content:flex-start;font-size:32px">{check_box("pl-k1")}<b>MDO-02</b>&nbsp;· Xe 2 · 2 DO</div>')
        q2 = (f'<div class="lbl">SKU 2001 · gộp theo mã hàng</div>'
              + "".join(f'<div id="pl-s{i}" class="row" style="width:520px">{d}<b>{n} pcs</b></div>' for i, (d, n) in enumerate([("DO-1001", 20), ("DO-1002", 15), ("DO-1004", 20)]))
              + f'<div id="pl-sum" class="abs" style="left:640px;top:110px;opacity:0;background:{C["blue"]};color:#fff;border-radius:18px;padding:18px 28px;font-size:44px;font-weight:900">Tổng: 55 pcs</div>')
        big_box = f'<svg width="120" height="100" viewBox="0 0 120 100"><rect x="4" y="10" width="112" height="86" rx="6" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="4"/><rect x="50" y="10" width="20" height="86" fill="#F3DDB5"/></svg>'
        packs = "".join(f'<svg id="pl-pk{i}" width="40" height="52" viewBox="0 0 40 52" style="opacity:0"><rect x="3" y="3" width="34" height="46" rx="6" fill="#E5584F" stroke="{INK}" stroke-width="3"/></svg>' for i in range(5))
        q3 = (f'<div style="display:flex;align-items:center;gap:26px;margin-top:20px">'
              f'<div class="big">55 pcs</div><div style="font-size:50px;font-weight:900;color:{C["blue"]}">→</div>'
              f'<div style="font-size:30px;font-weight:700;text-align:center">Quy cách<br><b style="font-size:38px">50 pcs / thùng</b></div><div style="font-size:50px;font-weight:900;color:{C["blue"]}">→</div>'
              f'<div id="pl-res" style="opacity:0;display:flex;align-items:flex-end;gap:10px">{big_box}<div style="font-size:44px;font-weight:900;margin:0 6px 24px">+</div>{packs}</div></div>'
              f'<div id="pl-res2" style="opacity:0;margin-top:26px;font-size:52px;font-weight:900;color:{C["green"]}">= 1 thùng 5 pcs</div>')
        q4 = (f'<div class="lbl">Phiếu lấy hàng · tách theo khu</div><div style="display:flex;gap:30px;margin-top:20px">'
              + "".join(f'<div id="pl-z{i}" style="opacity:0;width:300px;background:#fff;border:5px solid {K.ZONES[z][1]};border-radius:18px;padding:18px;text-align:center">'
                        f'{zone_tag(z, 34)}<div style="font-size:28px;font-weight:700;margin-top:14px">PL-000{i+1}</div>'
                        f'<div style="font-size:24px;font-weight:700;color:{C["muted"]}">{"Phiếu giấy" if z == "dong" else "Trên PDA"}</div></div>' for i, z in enumerate(["dong", "chill", "kho"]))
              + '</div>')
        body = B.bg_floor() + wms("pl-w", "Tạo phiếu lấy hàng", [("q1", q1), ("q2", q2), ("q3", q3), ("q4", q4)], x=180, y=150, w=1560, h=560)
        body += cbadge("pl-b5", 5, "Tạo phiếu lấy hàng", "WMS")
        js = st.badge_seq_js(["pl-b5"], [T[0]], D - 0.2) + st.appear_js("#pl-w", 0.1, 0.35, dy=20)
        js += st.show_panel_js("pl-w", None, "q1", T[0])
        js += st.pop_js("#pl-k0", T[0] + 1.2, 0.25) + st.pop_js("#pl-k1", T[0] + 1.8, 0.25)
        js += st.show_panel_js("pl-w", "q1", "q2", T[1])
        for i in range(3):
            js += f'tl.fromTo("#pl-s{i}",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.25}},{T[1]+0.3+i*0.25:.2f});\n'
            js += f'tl.to("#pl-s{i}",{{opacity:0.35,duration:0.4}},{T[1]+1.9:.2f});\n'
        js += f'tl.fromTo("#pl-sum",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{T[1]+1.9:.2f});\n'
        js += st.show_panel_js("pl-w", "q2", "q3", T[2])
        js += f'tl.fromTo("#pl-res",{{opacity:0}},{{opacity:1,duration:0.3}},{T[2]+2.4:.2f});\n'
        for i in range(5):
            js += st.pop_js(f"#pl-pk{i}", T[2] + 2.8 + i * 0.15, 0.2)
        js += st.appear_js("#pl-res2", T[2] + 3.8)
        js += st.show_panel_js("pl-w", "q3", "q4", T[3])
        for i in range(3):
            js += f'tl.fromTo("#pl-z{i}",{{opacity:0,x:{-330*i}}},{{opacity:1,x:0,duration:0.45,ease:"power2.out"}},{T[3]+0.6+i*0.15:.2f});\n'
        return body, "", js
    s = Scene("p2list", lines, build, lead=0.5, tail=1.8, min_hold={0: 4.0, 1: 3.6, 2: 6.4, 3: 3.6})
    s.sfx = [(("T", 3, 0.6), "whoosh-short.mp3", 0.25)]
    return s


def p2_branch():
    lines = ["Cách lấy hàng khác nhau theo khu."]

    def build(T, D):
        left = card(f'{zone_tag("chill", 26)} {zone_tag("kho", 26)}<div style="margin-top:12px">Lấy bằng <b>PDA</b></div>', C["blue"], "Bước 8", fs=34)
        right = card(f'{zone_tag("dong", 26)}<div style="margin-top:12px">Lấy bằng <b>phiếu giấy</b></div>', C["orange"], "Bước 6 → Bước 7", fs=34)
        body = B.bg_floor() + decision("br-d", "Khu hàng đông?", 960, 260, ("Không", left, 440), ("Có", right, 440), spread=520, drop=170, fs=38)
        js = decision_js("br-d", 0.2, T[0] + 0.3, T[0] + 1.2)
        return body, "", js
    s = Scene("p2branch", lines, build, lead=0.6, tail=2.2, min_hold={0: 3.0})
    return s


def p2_pda():
    lines = ["Hàng chill và khô lấy bằng PDA:",
             "picker chọn phiếu, đến vị trí và scan vị trí,",
             "scan mã hàng, rồi nhập tổng số lượng theo thùng và cái."]

    def build(T, D):
        R = K.ZRack("pp-r", 140, zone="chill", cols=3, levels=3, cw=250, lh=190)
        zone = K.zone_bg("pp-z", 80, 880, "chill", top=170, fs=34)
        rack = R.svg(contents=[(0, 1), (1, 2), (2, 1)], cartons=[(0, 0), (1, 0), (2, 0)])
        PX0, PX1, SC = 1180, 820, 1.5
        cx, _ = R.slot(1, 0)
        lab = R.label_xy(1, 0)
        a, b = SCAN["armR"]
        tip = hand(PX1, FY, SC, a, b, flip=True, extra=56)
        cart = f'<g transform="translate({PX0+40},{FY})"><g id="pp-cmv">{st.trolley("pp-cart", "MDO-01", slots=6)}</g></g>'
        pk = K.flip_fig("pp-mv", "pp-pk", "picker", PX0, SC, label=True, hand_r=pda_svg("pp-pk"))
        las = st.laser("pp-l1", tip[0], tip[1], lab[0], lab[1] + 4) + st.laser("pp-l2", tip[0], tip[1], cx + 30, FY - 90)
        body = svg_layer(st.floor() + zone + rack + cart + pk + las)
        p1 = ('<div class="lbl">Chọn phiếu lấy hàng</div>'
              + sel_row("pp-r0", "<b>PL-0002</b> · CHILL", "", True).replace('style="opacity:0"', "")
              + sel_row("pp-r1", "<b>PL-0003</b> · KHÔ").replace('style="opacity:0"', ""))
        p2 = kv("Đến vị trí, scan vị trí", f"{R.loc(1, 0)} ✔", "SKU 2001")
        p3 = kv("Scan mã hàng", "SKU 2001 ✔", "Cần lấy: 1 thùng 5 cái")
        p4 = (f'<div class="lbl">Nhập tổng số lượng</div><div style="display:flex;gap:12px"><div class="fld ok" style="flex:1">1 <span style="font-size:24px">thùng</span></div>'
              f'<div class="fld ok" style="flex:1">5 <span style="font-size:24px">cái</span></div></div><div class="go">XÁC NHẬN</div>')
        body += st.pda("pp-pda", "Lấy hàng · MDO-01", [("s1", p1), ("s2", p2), ("s3", p3), ("s4", p4)])
        body += cbadge("pp-b8", 8, "Lấy hàng chill / khô", "PDA")
        js = st.badge_seq_js(["pp-b8"], [T[0]], D - 0.2)
        js += K.label_js("pp-pk", 0.3)
        js += st.appear_js("#pp-pda", T[0], 0.35, dy=30) + st.show_panel_js("pp-pda", None, "s1", T[0] + 0.2)
        js += st.show_panel_js("pp-pda", "s1", "s2", T[1] + 0.2)
        js += pose_js("pp-pk", T[1], REST, dur=0.2)
        js += f'tl.to("#pp-mv",{{x:{PX1-PX0},duration:1.4,ease:"none"}},{T[1]:.2f});\n' + walk_js("pp-mvs", T[1], T[1] + 1.4)
        js += f'tl.to("#pp-cmv",{{x:{PX1-PX0},duration:1.4,ease:"none"}},{T[1]:.2f});\n'
        js += pose_js("pp-pk", T[1] + 1.5, SCAN, dur=0.25) + st.laser_js("pp-l1", T[1] + 1.8)
        js += st.show_panel_js("pp-pda", "s2", "s3", T[2])
        js += st.laser_js("pp-l2", T[2] + 0.3)
        js += st.show_panel_js("pp-pda", "s3", "s4", T[2] + 2.1)
        js += pose_js("pp-pk", T[2] + 2.4, REST, dur=0.2)
        js += f'tl.to("#pp-r-k1-l0",{{opacity:0.35,duration:0.3}},{T[2]+2.6:.2f});\n'
        js += st.pop_js("#pp-cart-k0", T[2] + 2.8) + st.pop_js("#pp-cart-k1", T[2] + 3.0)
        return body, "", js
    s = Scene("p2pda", lines, build, lead=0.5, tail=1.6, min_hold={0: 2.4, 1: 3.6, 2: 4.0})
    s.sfx = [(("T", 1, 1.8), "ping.mp3", 0.22)]
    return s


def paper_sheet(pid, x, y):
    hdr = "".join(f'<th style="padding:8px 10px;border-bottom:3px solid {INK};font-size:22px;text-align:left">{h}</th>' for h in ["Vị trí", "Mã hàng", "Cần lấy", "Thực lấy"])
    row = (f'<td style="padding:10px;font-size:26px;font-weight:900">D-01-01</td><td style="padding:10px;font-size:26px;font-weight:900">SKU 3005</td>'
           f'<td style="padding:10px;font-size:26px;font-weight:900">1 thùng 2 pcs</td>'
           f'<td style="padding:10px;position:relative;min-width:160px"><span id="{pid}-hw" style="opacity:0;font-family:\'Segoe Script\',cursive;font-style:italic;font-size:34px;font-weight:700;color:#1D4FA8">1 thùng 2</span></td>')
    return K.doc(pid, x, y, "PHIẾU LẤY HÀNG ĐÔNG", w=760, h=300, fs=30, lines=0,
                 extra=f'<table class="abs" style="left:24px;top:76px;border-collapse:collapse">{"<tr>"+hdr+"</tr><tr>"+row+"</tr>"}</table>'
                       f'<svg id="{pid}-pen" class="abs" style="left:560px;top:150px;opacity:0" width="60" height="60" viewBox="0 0 60 60"><path d="M10 50l8-2 32-32-6-6-32 32z" fill="{C["orange"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/></svg>')


def p2_paper():
    lines = ["Hàng đông lấy bằng phiếu giấy in sẵn.",
             "Đến vị trí theo phiếu, lấy đúng số thùng và pcs,",
             "rồi ghi số lượng thực lấy lên phiếu."]

    def build(T, D):
        R = K.ZRack("fp-r", 140, zone="dong", cols=3, levels=3, cw=250, lh=190)
        zone = K.zone_bg("fp-z", 80, 1760, "dong", top=170, fs=34)
        rack = R.svg(contents=[(0, 1), (2, 2), (1, 1)], cartons=[(0, 0), (1, 0), (2, 0)])
        PX0, PX1, SC = 1400, 430, 1.5
        paper = (f'<g transform="translate(14,12)"><rect x="-12" y="-4" width="26" height="32" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                 f'<rect x="-8" y="2" width="18" height="3" fill="#C9D3E0"/><rect x="-8" y="9" width="14" height="3" fill="#C9D3E0"/></g>')
        cart = f'<g transform="translate({PX0+40},{FY})"><g id="fp-cmv">{st.trolley("fp-cart", "MDO-01", slots=6)}</g></g>'
        pk = K.flip_fig("fp-mv", "fp-pk", "picker", PX0, SC, pose={"armR": (-60, -60)}, hand_r=paper)
        mist = "".join(f'<ellipse id="fp-m{i}" cx="{200 + i*300}" cy="{FY-30}" rx="200" ry="34" fill="#fff" opacity="0.5"/>' for i in range(5))
        body = svg_layer(st.floor() + zone + rack + cart + pk + mist)
        body += paper_sheet("fp-doc", 1060, 190)
        body += cbadge("fp-b6", 6, "Lấy hàng đông (giấy)", "TC")
        js = st.badge_seq_js(["fp-b6"], [T[0]], D - 0.2)
        for i in range(5):
            js += f'tl.fromTo("#fp-m{i}",{{x:0}},{{x:{60 if i % 2 else -60},duration:{D:.2f},ease:"sine.inOut"}},0);\n'
        js += f'tl.fromTo("#fp-doc",{{opacity:0,y:40,rotation:-3}},{{opacity:1,y:0,rotation:0,duration:0.5,ease:"power2.out"}},{T[0]+0.3:.2f});\n'
        js += f'tl.to("#fp-doc",{{opacity:0,duration:0.3}},{T[1]-0.1:.2f});\n'
        js += f'tl.to("#fp-mv",{{x:{PX1-PX0},duration:2.2,ease:"none"}},{T[1]:.2f});\n' + walk_js("fp-mvs", T[1], T[1] + 2.2)
        js += f'tl.to("#fp-cmv",{{x:{PX1-PX0},duration:2.2,ease:"none"}},{T[1]:.2f});\n'
        js += pose_js("fp-pk", T[1] + 2.3, CARRY, dur=0.25)
        js += f'tl.to("#fp-r-k0-l0",{{opacity:0.35,duration:0.3}},{T[1]+2.4:.2f});\n'
        js += st.pop_js("#fp-cart-k0", T[1] + 2.7) + st.pop_js("#fp-cart-k1", T[1] + 2.9)
        js += pose_js("fp-pk", T[1] + 3.0, {"armR": (-60, -60)}, dur=0.25)
        js += f'tl.to("#fp-doc",{{opacity:1,duration:0.3}},{T[2]:.2f});\n'
        js += f'tl.fromTo("#fp-doc-pen",{{opacity:0,x:-120}},{{opacity:1,x:60,duration:1.0,ease:"none"}},{T[2]+0.4:.2f});\n'
        js += f'tl.fromTo("#fp-doc-hw",{{opacity:0,clipPath:"inset(0 100% 0 0)"}},{{opacity:1,clipPath:"inset(0 0% 0 0)",duration:1.0,ease:"none"}},{T[2]+0.4:.2f});\n'
        js += f'tl.to("#fp-doc-pen",{{opacity:0,duration:0.2}},{T[2]+1.5:.2f});\n'
        return body, "", js
    s = Scene("p2paper", lines, build, lead=0.5, tail=1.6, min_hold={0: 3.2, 1: 4.0, 2: 3.2})
    return s


def p2_confirm():
    lines = ["Sau đó XLCT nhập số lượng thực lấy theo phiếu vào WMS."]

    def build(T, D):
        body = svg_layer(st.floor() + K.office("cf-pl", 260, label=False))
        body += paper_sheet("cf-doc", 120, 150).replace('style="opacity:0;font-family', 'style="opacity:1;font-family')
        p1 = (f'<div class="lbl">Xác nhận lấy hàng đông · PL-0001</div><div class="row"><span><b>SKU 3005</b> · D-01-01</span><span>Cần: 1 thùng 2 pcs</span></div>'
              f'<div class="lbl" style="margin-top:16px">SL thực lấy</div><div style="display:flex;gap:14px;align-items:center">'
              f'<div style="border:4px solid {C["orange"]};border-radius:12px;padding:10px 18px;font-size:36px;font-weight:900;min-width:280px;background:#FFF7EE"><span id="cf-typed" style="display:inline-block">1 thùng 2 pcs</span></div>'
              f'<div id="cf-ok" class="btng" style="opacity:0">✔ Đã xác nhận</div></div>')
        body += wms("cf-w", "Lấy hàng đông", [("p1", p1)], x=960, y=190, w=880, h=380)
        body += cbadge("cf-b7", 7, "Xác nhận lấy hàng đông", "WMS")
        js = st.badge_seq_js(["cf-b7"], [T[0]], D - 0.2)
        js += f'tl.fromTo("#cf-doc",{{opacity:0,x:-200,rotation:-8}},{{opacity:1,x:0,rotation:-3,duration:0.6,ease:"power2.out"}},0.2);\n'
        js += f'tl.to("#cf-doc",{{scale:0.62,x:-60,y:-40,duration:0.5,ease:"power2.inOut"}},{T[0]+1.3:.2f});\n'
        js += st.appear_js("#cf-w", T[0] + 1.4, 0.35, dy=20) + f'tl.set("#cf-w-p1",{{opacity:1}},{T[0]+1.4:.2f});\n'
        js += K.type_js("cf-pl", T[0] + 1.8, T[0] + 3.2)
        js += f'tl.fromTo("#cf-typed",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:1.2,ease:"steps(12)"}},{T[0]+1.8:.2f});\n'
        js += st.pop_js("#cf-ok", T[0] + 3.2)
        return body, "", js
    s = Scene("p2confirm", lines, build, lead=0.5, tail=1.8, min_hold={0: 5.0})
    s.sfx = [(("T", 0, 3.2), "chime.mp3", 0.22)]
    return s


def p2_tosort():
    lines = ["Hàng đã lấy ở cả ba khu được đưa về chung một khu chia hàng."]

    def build(T, D):
        zs = ""
        for i, z in enumerate(["dong", "chill", "kho"]):
            zs += K.zone_bg(f"ts-z{i}", 40 + i * 300, 280, z, top=200, fs=30)
        floor = st.floor() + zs + K.chia_floor(960, 1880)
        movers = ""
        for i in range(3):
            x0 = 230 + i * 300
            movers += (f'<g transform="translate({x0},{FY})"><g id="ts-g{i}">{st.trolley_behind(f"ts-c{i}", "MDO-01", slots=3)}'
                       f'<g transform="translate(40,0)">{stick(f"ts-p{i}", "picker", 1.3, pose={"armL": (40, -30)})}</g></g></g>')
        body = svg_layer(floor + movers) + cbadge("ts-b9", 9, "Đưa hàng về khu chia", "TC")
        js = st.badge_seq_js(["ts-b9"], [T[0]], D - 0.2)
        for i in range(3):
            for k in range(3):
                js += f'tl.set("#ts-c{i}-k{k}",{{opacity:1}},0);\n'
            dx = 1200 + i * 250 - (230 + i * 300)
            t0 = T[0] + 0.3 + (2 - i) * 0.5
            js += f'tl.to("#ts-g{i}",{{x:{dx},duration:2.4,ease:"power1.inOut"}},{t0:.2f});\n' + walk_js(f"ts-p{i}", t0, t0 + 2.4)
        return body, "", js
    s = Scene("p2tosort", lines, build, lead=0.5, tail=1.6, min_hold={0: 4.8})
    return s


def ic_truck():
    return ic_svg(f'<rect x="4" y="18" width="36" height="26" rx="3" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M40 26h10l8 10v8H40z" fill="{C["blue"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
                  f'<circle cx="14" cy="48" r="6" fill="{INK}"/><circle cx="48" cy="48" r="6" fill="{INK}"/>')


def ic_sum():
    return ic_svg(f'<rect x="6" y="14" width="52" height="40" rx="6" fill="#fff" stroke="{INK}" stroke-width="3"/><text x="32" y="42" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="18" fill="{C["blue"]}">1T 5</text>')


def ic_snow():
    return ic_svg(f'<g stroke="#4FA3E0" stroke-width="5" stroke-linecap="round"><path d="M32 8v48M11 20l42 24M11 44l42-24"/></g>')


def part2():
    g = ghinho("g2", 2, [
        (ic_truck(), "<b>1 xe = 1 Master DO</b>; có thể lấy gộp nhiều Master DO", "1 xe = 1 Master DO, có thể lấy gộp nhiều Master DO"),
        (ic_sum(), "Số lượng gộp theo mã hàng, tính <b>thùng + pcs</b>", "Số lượng gộp theo mã hàng, tính thùng + pcs"),
        (ic_snow(), "Đông: <b>phiếu giấy</b>, XLCT nhập lại WMS · Chill / khô: <b>PDA</b>", "Đông: phiếu giấy, XLCT nhập lại WMS. Chill / khô: PDA"),
    ])
    return [chapter(2, "Lấy hàng gộp theo xe"), p2_doin(), p2_master(), p2_alloc(), p2_list(), p2_branch(), p2_pda(), p2_paper(), p2_confirm(), p2_tosort(), g]


# ============================================================ PHẦN 3 – CHIA HÀNG THEO DO (04K.2)
SLOT_X = [640, 920, 1200]


def do_slot(sid, cx, code, load=False):
    ld = (f'<g id="{sid}-load" opacity="{1 if load else 0}">' + st.carton(cx - 70, FY - 56, 66, 56) + st.carton(cx + 0, FY - 56, 66, 56)
          + f'<rect x="{cx-30}" y="{FY-92}" width="26" height="36" rx="5" fill="#E5584F" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{cx}" y="{FY-92}" width="26" height="36" rx="5" fill="#E5584F" stroke="{INK}" stroke-width="2"/></g>')
    return (f'<g id="{sid}"><rect x="{cx-120}" y="{FY+10}" width="240" height="60" rx="8" fill="#FFE3C4" stroke="{C["orange"]}" stroke-width="4"/>'
            f'<line x1="{cx+100}" y1="{FY}" x2="{cx+100}" y2="{FY-200}" stroke="{INK}" stroke-width="6"/>'
            f'<g id="{sid}-sign"><rect x="{cx+20}" y="{FY-262}" width="160" height="64" rx="10" fill="#fff" stroke="{INK}" stroke-width="3.5"/>'
            f'<text x="{cx+100}" y="{FY-219}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="30" fill="{INK}">{code}</text></g>'
            + ld + f'<g transform="translate({cx-40},{FY-150})"><g id="{sid}-ok" opacity="0"><circle r="24" fill="{C["green"]}"/>'
            f'<path d="M-10 1l6 6 13-14" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g></g></g>')


def pile(pid, x):
    """Picked goods waiting at the sorting area: cart with cartons."""
    s = f'<g transform="translate({x},{FY})">{st.trolley(pid, "MDO-01", slots=6)}</g>'
    return s


def p3_slots():
    lines = ["Tại khu chia, mỗi DO của xe có một ô riêng, dán hoặc ghi số DO lên ô."]

    def build(T, D):
        slots = "".join(do_slot(f"sl-s{i}", x, DOS[i]) for i, x in enumerate(SLOT_X))
        pk = K.flip_fig("sl-mv", "sl-pk", "picker", 1560, 1.5, label=True)
        body = svg_layer(st.floor() + K.chia_floor(480, 1400, sign=False) + pile("sl-pile", 120) + slots + pk)
        body += (f'<div id="sl-ban" class="abs" style="left:480px;top:160px;opacity:0"><span class="pill" style="border-color:{C["orange"]}">KHU CHIA · Xe 1 · MDO-01</span></div>')
        body += cbadge("sl-b1", 1, "Chuẩn bị khu chia", "TC")
        js = st.badge_seq_js(["sl-b1"], [T[0]], D - 0.2) + K.label_js("sl-pk", 0.3)
        for k in range(6):
            js += f'tl.set("#sl-pile-k{k}",{{opacity:1}},0);\n'
        js += st.appear_js("#sl-ban", T[0] + 0.2)
        for i in range(3):
            js += f'tl.set("#sl-s{i}-sign",{{opacity:0}},0);\n'
        for i, x in enumerate(SLOT_X):
            t = T[0] + 0.6 + i * 1.3
            px = x + 260 - 1560
            js += f'tl.to("#sl-mv",{{x:{px},duration:0.8,ease:"none"}},{t:.2f});\n' + walk_js("sl-mvs", t, t + 0.8)
            js += f'tl.fromTo("#sl-s{i}-sign",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)",transformOrigin:"50% 50%"}},{t+0.9:.2f});\n'
        return body, "", js
    s = Scene("p3slots", lines, build, lead=0.5, tail=1.6, min_hold={0: 5.0})
    s.sfx = [(("T", 0, 1.5), "click-soft.mp3", 0.25)]
    return s


def p3_sort():
    lines = ["Trên PDA, chọn xe hoặc Master DO, rồi scan mã hàng.",
             "Hệ thống chỉ DO nào và số lượng bao nhiêu.",
             "Đặt hàng vào đúng ô DO và xác nhận.",
             "Lặp lại cho đến khi chia hết hàng."]

    def build(T, D):
        slots = "".join(do_slot(f"so-s{i}", x, DOS[i]) for i, x in enumerate(SLOT_X))
        PX0, SC = 470, 1.5
        a, b = SCAN["armR"]
        tip = hand(PX0, FY, SC, a, b, flip=True, extra=56)
        pk = K.flip_fig("so-mv", "so-pk", "picker", PX0, SC, pose=SCAN, hand_r=pda_svg("so-pk"), extra=carry_box("so-pk", SC))
        las = st.laser("so-l1", tip[0], tip[1], 260, FY - 70)
        body = svg_layer(st.floor() + K.chia_floor(480, 1340, sign=False) + pile("so-pile", 60) + slots + pk + las)
        p1 = '<div class="lbl">Chọn xe / Master DO</div>' + sel_row("so-r0", "<b>Xe 1</b> · MDO-01", "", True).replace('style="opacity:0"', "") + sel_row("so-r1", "<b>Xe 2</b> · MDO-02").replace('style="opacity:0"', "")
        p2 = kv("Scan mã hàng", "SKU 2001 ✔", "Mì ly (ví dụ)")
        p3 = (f'<div class="lbl">Chia vào</div><div class="fld" style="font-size:44px">DO-1002</div>'
              f'<div class="lbl">Số lượng</div><div class="fld" style="font-size:40px">1 thùng 5 pcs</div>')
        p4 = (f'<div class="lbl">DO-1002 · SKU 2001</div><div class="fld ok">1 thùng 5 pcs ✔</div><div class="go">XÁC NHẬN</div>'
              f'<div id="so-left" style="margin-top:22px;font-size:30px;font-weight:900">Đã chia hết hàng? <span style="color:{C["red"]}">Chưa</span></div>')
        p5 = f'<div class="big" style="color:{C["green"]};margin-top:40px">✔ Đã chia hết hàng</div><div style="font-size:28px;font-weight:700;margin-top:14px">MDO-01 · 3 DO</div>'
        body += st.pda("so-pda", "Chia hàng", [("s1", p1), ("s2", p2), ("s3", p3), ("s4", p4), ("s5", p5)])
        body += (f'<div id="so-ff" class="abs" style="left:1040px;top:180px;opacity:0;background:{INK};color:#fff;border-radius:14px;padding:6px 16px;'
                 f'font-size:28px;font-weight:900">▶▶ Lặp lại</div>')
        body += cbadge("so-b2", 2, "Chia hàng", "PDA")
        js = st.badge_seq_js(["so-b2"], [T[0]], D - 0.2)
        for k in range(6):
            js += f'tl.set("#so-pile-k{k}",{{opacity:1}},0);\n'
        js += st.appear_js("#so-pda", T[0], 0.35, dy=30) + st.show_panel_js("so-pda", None, "s1", T[0] + 0.1)
        js += st.show_panel_js("so-pda", "s1", "s2", T[0] + 1.9) + st.laser_js("so-l1", T[0] + 2.0)
        js += st.show_panel_js("so-pda", "s2", "s3", T[1])
        js += f'tl.to("#so-pile-k5",{{opacity:0,duration:0.15}},{T[1]+0.6:.2f});\n'
        js += pose_js("so-pk", T[1] + 0.5, CARRY, dur=0.25) + f'tl.to("#so-pk-box",{{opacity:1,duration:0.15}},{T[1]+0.6:.2f});\n'
        dest = SLOT_X[1] + 170 - PX0
        js += f'tl.to("#so-mv",{{x:{dest},duration:1.6,ease:"none"}},{T[1]+0.9:.2f});\n' + walk_js("so-mvs", T[1] + 0.9, T[1] + 2.5)
        js += f'tl.to("#so-pk-box",{{opacity:0,duration:0.1}},{T[2]+0.2:.2f});\n' + f'tl.to("#so-s1-load",{{opacity:1,duration:0.2}},{T[2]+0.2:.2f});\n'
        js += pose_js("so-pk", T[2] + 0.3, SCAN, dur=0.25)
        js += st.show_panel_js("so-pda", "s3", "s4", T[2] + 0.4) + st.pop_js("#so-s1-ok", T[2] + 1.0)
        js += f'tl.fromTo("#so-ff",{{opacity:0}},{{opacity:1,duration:0.2}},{T[3]:.2f});\n'
        js += f'tl.to("#so-mv",{{x:{SLOT_X[0] + 170 - PX0},duration:0.6,ease:"none"}},{T[3]+0.2:.2f});\n'
        js += f'tl.to("#so-s0-load",{{opacity:1,duration:0.2}},{T[3]+0.8:.2f});\n' + st.pop_js("#so-s0-ok", T[3] + 0.9)
        js += f'tl.to("#so-mv",{{x:{SLOT_X[2] + 170 - PX0},duration:0.9,ease:"none"}},{T[3]+1.2:.2f});\n'
        js += f'tl.to("#so-s2-load",{{opacity:1,duration:0.2}},{T[3]+2.1:.2f});\n' + st.pop_js("#so-s2-ok", T[3] + 2.2)
        for k in range(5):
            js += f'tl.to("#so-pile-k{k}",{{opacity:0,duration:0.15}},{T[3]+0.6+k*0.35:.2f});\n'
        js += st.show_panel_js("so-pda", "s4", "s5", T[3] + 2.4)
        return body, "", js
    s = Scene("p3sort", lines, build, lead=0.5, tail=1.8, min_hold={0: 3.6, 1: 3.0, 2: 3.0, 3: 3.4})
    s.sfx = [(("T", 0, 2.0), "ping.mp3", 0.22), (("T", 3, 2.4), "chime.mp3", 0.22)]
    return s


def report_screen():
    return (f'<div class="lbl">Báo cáo chênh lệch · MDO-01</div>'
            f'<div class="row"><span><b>SKU 2001</b> · DO-1003</span><span style="color:{C["red"]};font-weight:900">Thiếu 2 pcs</span></div>'
            f'<div class="row"><span><b>SKU 4010</b> · MDO-01</span><span style="color:#C45A00;font-weight:900">Thừa 1 thùng</span></div>')


def p3_diff():
    lines = ["Nếu có thiếu hoặc thừa, quản lý kho xem báo cáo chênh lệch trên WMS.",
             "Thiếu thì lấy bổ sung hoặc điều chỉnh DO.",
             "Thừa thì trả hàng về vị trí."]

    def build(T, D):
        dec = decision("df-d", "Có thiếu / thừa?", 960, 240,
                       ("Không", card(f'{st.check(44)}<div>Kết thúc</div>', C["green"], fs=34), 360),
                       ("Có", card("Quản lý kho xử lý", C["orange"], "Bước 3: Xử lý chênh lệch", fs=34), 440), spread=480, drop=170)
        mgr_sit = f'<g id="df-sit">{K.office("df-mg", 300, role="manager", label=True)}</g>'
        mgr_up = (f'<g id="df-up" opacity="0"><g transform="translate(560,{FY})">{stick("df-mu", "manager", 1.6, pose={"armR": (-128, 10), "armL": MANAGER_HOLD["armL"]}, hand_l=folder_svg())}</g></g>')
        stage = f'<div id="df-stage" class="abs" style="left:0;top:0;opacity:0">{svg_layer(st.floor() + K.desk(300) + mgr_sit + mgr_up)}</div>'
        body = B.bg_floor() + f'<div id="df-dec">{dec}</div>' + stage
        body += wms("df-w", "WMS · Báo cáo", [("p1", report_screen())], x=900, y=130, w=900, h=330)
        body += (f'<div id="df-c1" class="abs" style="left:900px;top:500px;width:900px;opacity:0">{card("Thiếu → lấy bổ sung hoặc điều chỉnh DO", C["red"], fs=36)}</div>'
                 f'<div id="df-c2" class="abs" style="left:900px;top:640px;width:900px;opacity:0">{card("Thừa → trả hàng về vị trí", C["orange"], fs=36)}</div>')
        body += cbadge("df-b3", 3, "Xử lý chênh lệch", "WMS")
        js = decision_js("df-d", 0.1, 0.6, 1.2)
        js += f'tl.to("#df-dec",{{opacity:0,duration:0.3}},{T[0]+1.4:.2f});\n'
        js += f'tl.to("#df-stage",{{opacity:1,duration:0.3}},{T[0]+1.3:.2f});\n'
        js += st.badge_seq_js(["df-b3"], [T[0] + 1.3], D - 0.2)
        js += K.label_js("df-mg", T[0] + 1.5)
        js += st.appear_js("#df-w", T[0] + 1.8, 0.35, dy=20) + f'tl.set("#df-w-p1",{{opacity:1}},{T[0]+1.8:.2f});\n'
        js += f'tl.to("#df-sit",{{opacity:0,duration:0.25}},{T[1]:.2f});\ntl.to("#df-up",{{opacity:1,duration:0.25}},{T[1]:.2f});\n'
        js += st.appear_js("#df-c1", T[1] + 0.3) + st.appear_js("#df-c2", T[2] + 0.2)
        return body, "", js
    s = Scene("p3diff", lines, build, lead=2.4, tail=1.8, min_hold={0: 5.0, 1: 3.4, 2: 3.0})
    return s


def ic_slots():
    return ic_svg(f'<rect x="4" y="34" width="16" height="22" fill="#FFE3C4" stroke="{C["orange"]}" stroke-width="3"/><rect x="24" y="34" width="16" height="22" fill="#FFE3C4" stroke="{C["orange"]}" stroke-width="3"/>'
                  f'<rect x="44" y="34" width="16" height="22" fill="#FFE3C4" stroke="{C["orange"]}" stroke-width="3"/><rect x="8" y="12" width="48" height="14" rx="3" fill="#fff" stroke="{INK}" stroke-width="2.5"/>')


def ic_scan():
    return ic_svg(f'<rect x="20" y="6" width="24" height="40" rx="5" fill="#2B3646" stroke="{INK}" stroke-width="2"/><rect x="24" y="11" width="16" height="16" fill="#7FD3FF"/>'
                  f'<line x1="32" y1="46" x2="32" y2="60" stroke="#E53935" stroke-width="4"/>')


def ic_manager():
    return ic_svg(f'<g transform="translate(32,62) scale(0.36)">{stick("icm", "manager", 1.0)}</g>', size=88)


def part3():
    g = ghinho("g3", 3, [
        (ic_slots(), "Mỗi DO <b>một ô riêng</b>", "Mỗi DO một ô riêng"),
        (ic_scan(), "Scan mã hàng → hệ thống chỉ <b>DO và số lượng</b> → đặt vào ô, xác nhận", "Scan mã hàng, hệ thống chỉ DO và số lượng, đặt vào ô, xác nhận"),
        (ic_manager(), "Chênh lệch do <b>quản lý kho</b> xử lý", "Chênh lệch do quản lý kho xử lý"),
    ])
    return [chapter(3, "Chia hàng theo DO"), p3_slots(), p3_sort(), p3_diff(), g]


# ============================================================ PHẦN 4 – KIỂM & BÀN GIAO (04K.3)
def p4_check():
    lines = ["Checker chọn xe hoặc Master DO,",
             "scan mã hàng của từng DO, kiểm ngoại quan và số lượng thùng, pcs.",
             "Nếu không khớp, chia lại hoặc bổ sung hàng cho DO, rồi kiểm lại."]

    def build(T, D):
        slots = "".join(do_slot(f"ck-s{i}", x - 380, DOS[i], load=True) for i, x in enumerate(SLOT_X))
        CX0, SC = 1100, 1.5
        a, b = SCAN["armR"]
        ck = K.flip_fig("ck-mv", "ck-ck", "checker", CX0, SC, label=True, pose=SCAN, hand_r=pda_svg("ck-ck"))
        tip = hand(CX0, FY, SC, a, b, flip=True, extra=56)
        lasers = ""
        for i, x in enumerate(SLOT_X):
            dx = (x - 380 + 210) - CX0
            lasers += st.laser(f"ck-l{i}", tip[0] + dx, tip[1], x - 380 + 30, FY - 40)
        stage = f'<div id="ck-stage" class="abs" style="left:0;top:0">{svg_layer(st.floor() + K.chia_floor(100, 1060, sign=False) + slots + ck + lasers)}</div>'
        p1 = '<div class="lbl">Chọn xe / Master DO</div>' + sel_row("ck-r0", "<b>Xe 1</b> · MDO-01", "", True).replace('style="opacity:0"', "")
        p2 = (kv("DO-1001 · scan mã hàng", "SKU 2001 ✔", "") + '<div class="lbl" style="margin-top:12px">Ngoại quan</div><div class="fld ok">Đạt ✔</div>'
              '<div class="lbl">Số lượng</div><div class="fld ok">1 thùng 5 pcs ✔</div>')
        body = stage + st.pda("ck-pda", "Kiểm hàng", [("s1", p1), ("s2", p2)])
        dec = decision("ck-d", "Khớp với DO?", 960, 250,
                       ("Không", B.loop_card("Bước 2: Chia lại / bổ sung hàng cho DO<br><span style='font-size:24px;color:#6B7685'>rồi kiểm lại</span>"), 600),
                       ("Có", card("Bước 3: In giấy bàn giao", C["green"], fs=34), 440), spread=540, drop=170)
        body += f'<div id="ck-dec" class="abs" style="left:0;top:0;width:1920px;height:1080px;opacity:0;background:{C["ground"]}">{dec}</div>'
        body += cbadge("ck-b1", 1, "Kiểm hàng", "PDA")
        js = st.badge_seq_js(["ck-b1"], [T[0]], T[2])
        js += f'tl.to("#ck-b1",{{opacity:0,duration:0.15}},{T[2]-0.1:.2f});\n'
        js += K.label_js("ck-ck", 0.3)
        js += st.appear_js("#ck-pda", T[0], 0.35, dy=30) + st.show_panel_js("ck-pda", None, "s1", T[0] + 0.1)
        js += st.show_panel_js("ck-pda", "s1", "s2", T[1])
        for i, x in enumerate(SLOT_X):
            t = T[1] + 0.1 + i * 1.3
            js += f'tl.to("#ck-mv",{{x:{(x - 380 + 210) - CX0},duration:0.6,ease:"none"}},{t:.2f});\n' + walk_js("ck-mvs", t, t + 0.6)
            js += st.laser_js(f"ck-l{i}", t + 0.7, 0.5) + st.pop_js(f"#ck-s{i}-ok", t + 1.0, 0.25)
        js += f'tl.to("#ck-pda",{{opacity:0,duration:0.2}},{T[2]-0.2:.2f});\n'
        js += f'tl.to("#ck-dec",{{opacity:1,duration:0.3}},{T[2]-0.2:.2f});\n'
        js += decision_js("ck-d", T[2], T[2] + 0.4, T[2] + 2.6)
        return body, "", js
    s = Scene("p4check", lines, build, lead=0.5, tail=1.8, min_hold={0: 2.6, 1: 4.6, 2: 5.0})
    s.sfx = [(("T", 1, 0.8), "ping.mp3", 0.22)]
    return s


def handover_doc(did, x, y, do, rot=0, signed=False):
    sig = (f'<svg class="abs" style="left:0;top:0" width="240" height="300" viewBox="0 0 240 300">{B.signature(did + "-sg", 40, 236, 150)}</svg>'
           f'<div class="abs" style="left:30px;top:252px;width:180px;text-align:center;font-size:18px;font-weight:700;color:{C["muted"]};border-top:2px solid #C9D3E0;padding-top:2px">Tài xế ký</div>')
    return K.doc(did, x, y, f"GIẤY BÀN GIAO<br><span style='color:{C['blue']}'>{do}</span>", w=240, h=300, fs=22, lines=2, rot=rot,
                 extra=sig)


def p4_print():
    lines = ["Khớp rồi, checker in giấy bàn giao của xe, mỗi DO một giấy."]

    def build(T, D):
        p1 = (f'<div class="lbl">Xe 1 · MDO-01 · 3 DO</div><div class="row"><span>Kiểm hàng</span><span style="color:{C["green"]};font-weight:900">✔ Khớp</span></div>'
              f'<div id="pr-btn" class="btnw" style="margin-top:10px">IN GIẤY BÀN GIAO</div>')
        ck = figure("pr-ck", "checker", 360, scale=1.5, label=True)
        body = svg_layer(st.floor() + ck + K.printer("pr-prt", 760, FY - 110) + f'<rect x="620" y="{FY-70}" width="280" height="70" fill="#B98A55" stroke="{INK}" stroke-width="3"/>')
        body += wms("pr-w", "Bàn giao", [("p1", p1)], x=1080, y=120, w=740, h=300) + K.cursor("pr-cur")
        body += "".join(handover_doc(f"pr-d{i}", 660, 420, do) for i, do in enumerate(DOS))
        body += cbadge("pr-b3", 3, "In giấy bàn giao", "WMS")
        js = st.badge_seq_js(["pr-b3"], [T[0]], D - 0.2) + K.label_js("pr-ck", 0.2)
        js += st.appear_js("#pr-w", 0.2, 0.35, dy=20) + 'tl.set("#pr-w-p1",{opacity:1},0.2);\n'
        js += K.click_js("pr-cur", 1500, 560, 1260, 312, T[0] + 0.3, target="#pr-btn")
        js += f'tl.to("#pr-cur",{{opacity:0,duration:0.2}},{T[0]+1.3:.2f});\n'
        for i in range(3):
            t = T[0] + 1.2 + i * 0.6
            js += (f'tl.fromTo("#pr-d{i}",{{opacity:0,y:120,scale:0.5}},{{opacity:1,y:-120,scale:0.8,duration:0.5,ease:"power2.out"}},{t:.2f});\n'
                   f'tl.to("#pr-d{i}",{{x:{400 + i*270},y:110,rotation:{(i-1)*4},scale:0.85,duration:0.6,ease:"power2.inOut"}},{t+0.5:.2f});\n')
        return body, "", js
    s = Scene("p4print", lines, build, lead=0.5, tail=2.0, min_hold={0: 4.4})
    s.sfx = [(("T", 0, 1.2), "click-soft.mp3", 0.3)]
    return s


def p4_sign():
    lines = ["Tài xế xe tải nhận hàng lên xe và ký giấy bàn giao.",
             "XLCT xác nhận hoàn tất Master DO và lưu giấy bàn giao đã ký."]

    def build(T, D):
        trk = f'<g transform="translate(1160,{FY})"><g id="sg-tk">{st.truck("sg-truck", label="Xe 1")}</g></g>'
        drv = figure("sg-dv", "transport", 980, scale=1.5, label=True, extra=carry_box("sg-dv", 1.5))
        goods = "".join(f'<g id="sg-g{i}">{st.carton(560 + i*80, FY-56, 74, 56)}</g>' for i in range(4))
        stage = f'<div id="sg-a" class="abs" style="left:0;top:0">{svg_layer(st.floor() + goods + drv)}</div>'
        docs = "".join(handover_doc(f"sg-d{i}", 120 + i * 270, 150, do, rot=(i-1)*3) for i, do in enumerate(DOS))
        office = f'<div id="sg-b" class="abs" style="left:0;top:0;opacity:0">{svg_layer(K.office("sg-pl", 260, label=False))}</div>'
        p1 = (f'<div class="lbl">Master DO</div><div class="row sel"><span><b>MDO-01</b> · Xe 1 · 3 DO</span><span>Đã ký 3/3</span></div>'
              f'<div id="sg-btn" class="btng" style="margin-top:12px">HOÀN TẤT MASTER DO</div>')
        folder = (f'<div id="sg-fold" class="abs" style="left:620px;top:470px;opacity:0;width:300px;height:200px;background:{K.NAVY};border:4px solid {INK};border-radius:14px;'
                  f'color:#fff;font-size:28px;font-weight:900;display:flex;align-items:center;justify-content:center;text-align:center">Hồ sơ<br>MDO-01</div>')
        body = svg_layer(st.floor() + trk) + stage + office + docs + folder
        body += wms("sg-w", "Xuất kho", [("p1", p1)], x=1000, y=130, w=820, h=300) + K.cursor("sg-cur")
        body += st.stamp("sg-done", "Đã xuất kho", x=1180, y=470)
        body += cbadge("sg-b4", 4, "Nhận hàng, ký", "TC") + cbadge("sg-b5", 5, "Hoàn tất xuất kho", "WMS")
        js = st.badge_seq_js(["sg-b4", "sg-b5"], T, D - 0.2)
        js += K.label_js("sg-dv", 0.3)
        js += 'tl.fromTo("#sg-tk",{x:900},{x:0,duration:1.2,ease:"power2.out"},0);\n'
        for i in range(2):
            t = T[0] + 0.2 + i * 1.4
            js += pose_js("sg-dv", t, CARRY, dur=0.2) + f'tl.to("#sg-g{3-i}",{{opacity:0,duration:0.1}},{t+0.1:.2f});\ntl.to("#sg-dv-box",{{opacity:1,duration:0.1}},{t+0.1:.2f});\n'
            js += f'tl.to("#sg-dv",{{x:200,duration:0.5,ease:"none"}},{t+0.3:.2f});\n' + walk_js("sg-dv", t + 0.3, t + 0.8)
            js += f'tl.to("#sg-dv-box",{{opacity:0,duration:0.1}},{t+0.85:.2f});\n' + pose_js("sg-dv", t + 0.85, REST, dur=0.2)
            js += f'tl.to("#sg-dv",{{x:0,duration:0.5,ease:"none"}},{t+0.9:.2f});\n' + walk_js("sg-dv", t + 0.9, t + 1.4)
        for i in range(3):
            js += f'tl.fromTo("#sg-d{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3}},{T[0]+2.8+i*0.2:.2f});\n'
            js += B.sig_js(f"sg-d{i}-sg", T[0] + 3.4 + i * 0.5, 0.45)
        js += f'tl.to("#sg-a",{{opacity:0,duration:0.3}},{T[1]-0.1:.2f});\ntl.to("#sg-b",{{opacity:1,duration:0.3}},{T[1]:.2f});\n'
        js += st.appear_js("#sg-w", T[1] + 0.1, 0.35, dy=20) + f'tl.set("#sg-w-p1",{{opacity:1}},{T[1]+0.1:.2f});\n'
        for i in range(3):
            js += f'tl.to("#sg-d{i}",{{x:{120 - i*270 + 500},y:330,scale:0.4,rotation:0,duration:0.5,ease:"power2.in"}},{T[1]+0.3+i*0.15:.2f});\n'
        js += f'tl.fromTo("#sg-fold",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{T[1]+0.2:.2f});\n'
        for i in range(3):
            js += f'tl.to("#sg-d{i}",{{opacity:0,duration:0.15}},{T[1]+0.8+i*0.15:.2f});\n'
        js += K.click_js("sg-cur", 1700, 600, 1180, 330, T[1] + 1.3, target="#sg-btn")
        js += f'tl.to("#sg-cur",{{opacity:0,duration:0.2}},{T[1]+2.2:.2f});\n'
        js += st.stamp_js("sg-done", T[1] + 2.2)
        js += f'tl.to("#sg-tk",{{x:900,duration:1.4,ease:"power2.in"}},{T[1]+2.8:.2f});\n'
        return body, "", js
    s = Scene("p4sign", lines, build, lead=0.6, tail=2.2, min_hold={0: 5.2, 1: 4.6})
    s.sfx = [(("T", 1, 2.2), "chime.mp3", 0.25)]
    return s


def ic_doc():
    return ic_svg(f'<path d="M10 6h44v46q-11-8-22 0t-22 0z" fill="#fff" stroke="{C["blue"]}" stroke-width="3"/><rect x="18" y="18" width="28" height="4" fill="#C9D3E0"/><rect x="18" y="28" width="22" height="4" fill="#C9D3E0"/>')


def ic_sign():
    return ic_svg(f'<path d="M6 44c6-14 10-14 9 0s8 6 12-4 8-8 10 2 10 2 14-6" fill="none" stroke="#1D4FA8" stroke-width="4" stroke-linecap="round"/><line x1="6" y1="54" x2="58" y2="54" stroke="{INK}" stroke-width="3"/>')


def part4():
    g = ghinho("g4", 4, [
        (B.ic_loop(), "Kiểm theo <b>từng DO</b> của xe; sai thì chia lại rồi kiểm lại", "Kiểm theo từng DO của xe, sai thì chia lại rồi kiểm lại"),
        (ic_doc(), "Mỗi DO <b>một giấy bàn giao</b>", "Mỗi DO một giấy bàn giao"),
        (ic_sign(), "Tài xế ký nhận → XLCT <b>hoàn tất Master DO</b>", "Tài xế ký nhận, XLCT hoàn tất Master DO"),
    ])
    return [chapter(4, "Kiểm & Bàn giao"), p4_check(), p4_print(), p4_sign(), g]


# ============================================================ KẾT
def ending():
    lines = ["Vậy là bạn đã nắm toàn bộ quy trình kho CXAD.",
             "Chúc các bạn làm việc thật tốt!"]
    subs = ["LPN · putaway ngay", "1 xe = 1 Master DO", "Mỗi DO một ô", "Tài xế ký nhận"]

    def build(T, D):
        strip = B.step_strip("en", 200, tick=True)
        strip += "".join(f'<div id="en-t{i}" class="abs" style="left:{110 + i*436}px;top:372px;width:380px;text-align:center;font-size:28px;font-weight:700;color:{C["muted"]};opacity:0">{t}</div>'
                         for i, t in enumerate(subs))
        man = svg_layer(f'<g transform="translate(960,{FY+40})"><g id="en-man">{stick("en-man", "instructor", 2.0)}</g></g>')
        body = B.bg_floor() + strip + man
        js = B.strip_js("en", 0.3, 0.35)
        for i in range(4):
            js += st.pop_js(f"#en-ok{i}", T[0] + 0.3 + i * 0.4, 0.25)
            js += st.appear_js(f"#en-t{i}", T[0] + 0.4 + i * 0.4)
        js += pose_js("en-man", T[1], {"armR": (-100, -80)}, dur=0.35, ease="back.out(2)")
        return body, "", js
    s = Scene("cxend", lines, build, lead=1.6, tail=2.6, min_hold={0: 3.6, 1: 2.8})
    s.sfx = [(("T", 1, 0.0), "chime.mp3", 0.22)]
    return [s]
