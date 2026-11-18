"""Training video: Quy trình toàn kho CXAD (lấy hàng bằng giấy) -> ./video-cxad
Run: python3 tools/build_cxad.py [limit_seconds]
Script source: source/Context_Video_CXAD_Paper_Picking.md (v2, đã xác nhận)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, stick, walk_js, pose_js, REST
import stage as st
from stage import FY, INK
from build_full import Scene, chapter, build_all
from parts import figure, svg_layer, desk_svg, CARRY

OUT = os.path.join(os.path.dirname(__file__), "..", "video-cxad")

ZONE = {  # name -> (fill, edge, label)
    "dong": ("#D6ECFF", "#3E8FD8", "ĐÔNG"),
    "chill": ("#D3F2EC", "#24A08C", "CHILL"),
    "kho": ("#F5E9D3", "#C9965A", "KHÔ"),
}
STAGES = ["Nhập hàng & Putaway", "Lấy hàng gộp theo xe", "Chia hàng theo DO", "Kiểm & Bàn giao"]


# ------------------------------------------------------------ shared pieces
def zone_icon(z, cx, cy, s=1.0):
    """Small pictogram per temperature zone, centred at (cx, cy)."""
    if z == "dong":   # snowflake
        arms = "".join(f'<g transform="rotate({a})"><line x1="0" y1="0" x2="0" y2="-26" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                       f'<path d="M-8,-20 L0,-13 L8,-20" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></g>'
                       for a in range(0, 360, 60))
        inner = arms
    elif z == "chill":  # thermometer
        inner = (f'<rect x="-8" y="-30" width="16" height="42" rx="8" fill="#fff" stroke="{INK}" stroke-width="4"/>'
                 f'<circle cx="0" cy="16" r="13" fill="#24A08C" stroke="{INK}" stroke-width="4"/>'
                 f'<rect x="-3" y="-8" width="6" height="22" fill="#24A08C"/>')
    else:  # carton
        inner = (f'<rect x="-26" y="-20" width="52" height="40" rx="3" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="3.5"/>'
                 f'<rect x="-6" y="-20" width="12" height="40" fill="#F3DDB5"/>')
    return f'<g transform="translate({cx},{cy}) scale({s})">{inner}</g>'


def doc_shape(did, x, y, title, w=230, h=150, sub="", barcode=False):
    """Document with wavy bottom (legend symbol 'Chứng từ'), top-left at (x, y), hidden."""
    wave = f'M0,0 H{w} V{h-18} C{w*0.75},{h-42} {w*0.55},{h+6} {w*0.3},{h-10} C{w*0.18},{h-18} {w*0.08},{h-14} 0,{h-6} Z'
    lines = ""
    if barcode:
        for r in range(3):
            yy = 58 + r * 26
            lines += "".join(f'<rect x="{18 + i*11}" y="{yy}" width="{3 if i % 3 else 6}" height="18" fill="{INK}"/>' for i in range(int((w-36)/11)))
    else:
        lines = "".join(f'<rect x="18" y="{58 + r*20}" width="{w-36 - (40 if r % 2 else 0)}" height="8" rx="4" fill="#D5DBE4"/>' for r in range(3))
    return (f'<div id="{did}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;opacity:0">'
            f'<svg width="{w}" height="{h}" viewBox="-3 -3 {w+6} {h+6}" style="overflow:visible"><path d="{wave}" fill="#fff" stroke="{C["blue"]}" stroke-width="4"/>'
            f'<text x="{w/2}" y="36" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="24" fill="{INK}">{title}</text>{lines}</svg>'
            + (f'<div style="position:absolute;left:0;right:0;top:{h+6}px;text-align:center;font-size:22px;font-weight:700;color:{C["muted"]}">{sub}</div>' if sub else "")
            + '</div>')


def doc_fly_js(did, t, dx, dy, scale=0.55, hold=1.4):
    """Document pops in, then flies to its corner slot (dx, dy relative) and stays small."""
    return (f'tl.fromTo("#{did}",{{opacity:0,scale:0.4}},{{opacity:1,scale:1.15,duration:0.35,ease:"back.out(2)",transformOrigin:"50% 50%"}},{t:.2f});\n'
            f'tl.to("#{did}",{{scale:1,duration:0.2}},{t+0.35:.2f});\n'
            f'tl.to("#{did}",{{x:{dx},y:{dy},scale:{scale},duration:0.6,ease:"power2.inOut",transformOrigin:"50% 50%"}},{t+hold:.2f});\n')


def printer_svg(pid, x, y=FY):
    """Desk printer standing on a small cabinet, origin = ground centre. Paper slot at y-150."""
    return (f'<g id="{pid}" transform="translate({x},{y})">'
            f'<rect x="-70" y="-110" width="140" height="110" fill="#B98A55" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-80" y="-188" width="160" height="78" rx="10" fill="#E3E8EF" stroke="{INK}" stroke-width="3.5"/>'
            f'<rect x="-56" y="-168" width="112" height="10" rx="4" fill="#2B3646"/>'
            f'<circle cx="56" cy="-130" r="6" fill="{C["green"]}"/></g>')


# ============================================================ MỞ ĐẦU
def cx_intro():
    lines = ["Xin chào các bạn. Video này đi qua toàn bộ quy trình của kho CXAD, từ lúc nhập hàng đến lúc giao hàng lên xe."]

    def build(T, D):
        W, G, X0 = 330, 52, 110
        chips = ""
        for i, t in enumerate(STAGES):
            x = X0 + i * (W + G)
            chips += (f'<div id="cx0-s{i}" class="abs" style="left:{x}px;top:470px;width:{W}px;height:150px;background:#fff;border:4px solid {INK};border-radius:22px;'
                      f'display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0">'
                      f'<div style="font-size:30px;font-weight:900;color:#C45A00">{i+1}</div><div style="font-size:34px;font-weight:900;text-align:center;line-height:1.15;padding:0 12px">{t}</div></div>')
            if i < len(STAGES) - 1:
                chips += f'<div id="cx0-a{i}" class="abs" style="left:{x+W}px;top:510px;width:{G}px;text-align:center;font-size:50px;font-weight:900;color:{C["blue"]};opacity:0">›</div>'
        body = f"""
    <div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,{C['ground']} 0%,{C['ground']} 74%,{C['floor']} 74%,{C['floor']} 100%)"></div>
    <div id="cx0-title" class="abs" style="left:110px;top:90px"><div style="font-size:88px;font-weight:900;line-height:1.05">Quy trình vận hành kho CXAD</div>
      <div style="font-size:48px;font-weight:700;color:{C['blue']};margin-top:10px">Lấy hàng bằng giấy (Paper Picking)</div></div>
    {chips}
    {svg_layer(f'<g transform="translate(1720,880)"><g id="cx0-man">{stick("cx0-man", "instructor", scale=2.1)}</g></g>')}"""
        js = 'tl.fromTo("#cx0-title",{opacity:0,x:-24},{opacity:1,x:0,duration:0.6,ease:"power3.out"},0);\n'
        js += 'tl.fromTo("#cx0-man",{x:420},{x:0,duration:1.4,ease:"power1.out"},0.1);\n' + walk_js("cx0-man", 0.1, 1.5)
        js += pose_js("cx0-man", 1.6, {"armR": (-150, -24)}, dur=0.3, ease="power2.out")
        for k in range(4):
            js += f'tl.to("#cx0-man-foreR",{{rotation:{-50 if k % 2 == 0 else -5},svgOrigin:"0 0",duration:0.22,ease:"sine.inOut"}},{1.9 + k*0.22:.2f});\n'
        js += pose_js("cx0-man", 2.9, {"armR": REST["armR"]}, dur=0.3)
        for i in range(len(STAGES)):
            t = T[0] + 1.6 + i * 0.45
            js += f'tl.fromTo("#cx0-s{i}",{{opacity:0,y:24}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.8)"}},{t:.2f});\n'
            if i:
                js += f'tl.fromTo("#cx0-a{i-1}",{{opacity:0}},{{opacity:1,duration:0.2}},{t-0.1:.2f});\n'
        return body, "", js
    s = Scene("cxintro", lines, build, lead=0.6, tail=1.0, min_hold={0: 6.0})
    s.sfx = [(("T", 0, 1.6), "whoosh-short.mp3", 0.25)]
    return s


# ============================================================ SƠ ĐỒ KHO
def rack_rows(x0, y0, w, h, n=3):
    gap = h / (n + 0.5)
    return "".join(f'<rect x="{x0+30}" y="{y0 + gap*(i+0.75) - 13:.0f}" width="{w-60}" height="26" rx="5" fill="#8FA3BF" stroke="{INK}" stroke-width="2.5"/>'
                   for i in range(n))


def area(aid, x, y, w, h, fill, edge, label, sub="", dashed=False, inner=""):
    dash = ' stroke-dasharray="16 10"' if dashed else ""
    return (f'<g id="{aid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="{edge}" stroke-width="5"{dash}/>{inner}'
            f'<text x="{x + w/2}" y="{y + 46}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="34" fill="{INK}">{label}</text>'
            + (f'<text x="{x + w/2}" y="{y + h - 18}" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="22" fill="{C["muted"]}">{sub}</text>' if sub else "")
            + '</g>')


def mini_truck(x, y, s=0.42, flip=False):
    f = f" scale(-1,1)" if flip else ""
    return f'<g transform="translate({x},{y}) scale({s}){f}">{st.truck("mt" + str(x))}</g>'


def map_svg(prefix):
    """Top-down plan of the CXAD warehouse. Zones {prefix}-dong/-chill/-kho with hidden glow {prefix}-g-<z>."""
    s = [f'<rect x="40" y="130" width="1840" height="700" rx="26" fill="#fff" stroke="{INK}" stroke-width="5"/>']
    # office
    s.append(area(f"{prefix}-office", 70, 160, 210, 300, "#EAF1FC", C["blue"], "XLCT", "Văn phòng",
                  inner=f'<rect x="110" y="250" width="130" height="70" rx="6" fill="#2B3646"/><rect x="118" y="258" width="114" height="54" rx="3" fill="#7FD3FF"/>'
                        f'<rect x="96" y="340" width="158" height="16" rx="4" fill="#C9965A" stroke="{INK}" stroke-width="2"/>'))
    zx, zw, zg = 320, 500, 40
    for i, z in enumerate(("dong", "chill", "kho")):
        fill, edge, lab = ZONE[z]
        x = zx + i * (zw + zg)
        inner = rack_rows(x, 200, zw, 220) + zone_icon(z, x + zw - 50, 192, 0.8)
        glow = f'<rect id="{prefix}-g-{z}" x="{x-8}" y="152" width="{zw+16}" height="286" rx="24" fill="none" stroke="{edge}" stroke-width="12" opacity="0"/>'
        s.append(area(f"{prefix}-{z}", x, 160, zw, 270, fill, edge, f"KHU {lab}", inner=inner) + glow)
    # bottom row
    s.append(area(f"{prefix}-dockin", 70, 540, 360, 260, "#EEF2F6", "#8FA3BF", "Dock nhận hàng", inner=mini_truck(120, 770)))
    cells = "".join(f'<rect x="{835 + k*100}" y="{630}" width="90" height="90" rx="8" fill="#fff" stroke="{C["orange"]}" stroke-width="4" stroke-dasharray="8 6"/>'
                    f'<text x="{880 + k*100}" y="{682}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="20" fill="{INK}">DO-100{k+1}</text>' for k in range(3))
    s.append(area(f"{prefix}-chia", 820, 540, 330, 260, "#FFF3E4", C["orange"], "Khu chia", inner=cells))
    s.append(area(f"{prefix}-kiem", 1230, 540, 260, 260, "#F1EAFE", "#8B5CF6", "Khu kiểm hàng",
                  inner=f'<g transform="translate(1360,780) scale(0.55)">{printer_svg(prefix + "-pr", 0, 0)}</g>'))
    s.append(area(f"{prefix}-dockout", 1570, 540, 280, 260, "#EEF2F6", "#8FA3BF", "Dock xuất", inner=mini_truck(1600, 770)))
    return "".join(s)


def cx_map():
    lines = ["Kho có ba khu theo nhiệt độ: khu đông, khu chill và khu khô."]

    def build(T, D):
        P = "cxm"
        arrows = [("M250,540 C250,470 400,470 470,440", (330, 478)),      # dock -> zones (putaway)
                  ("M985,438 L985,535", (1030, 488)),                       # zones -> khu chia (lấy hàng)
                  ("M1150,670 L1226,670", (1188, 625)),                     # chia -> kiểm
                  ("M1490,670 L1566,670", (1528, 625))]                     # kiểm -> dock xuất
        flow = ""
        for i, (d, (bx, by)) in enumerate(arrows):
            flow += (f'<path id="{P}-f{i}" d="{d}" opacity="0" fill="none" stroke="{C["orange"]}" stroke-width="10" stroke-linecap="round" '
                     f'stroke-dasharray="400" stroke-dashoffset="400" marker-end="url(#{P}-ah)"/>'
                     f'<g id="{P}-n{i}" opacity="0"><circle cx="{bx}" cy="{by}" r="22" fill="{C["orange"]}" stroke="{INK}" stroke-width="3"/>'
                     f'<text x="{bx}" y="{by+9}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="26" fill="{INK}">{i+1}</text></g>')
        flow = (f'<defs><marker id="{P}-ah" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 Z" fill="{C["orange"]}"/></marker></defs>') + flow
        body = svg_layer(map_svg(P) + flow)
        body += (f'<div id="{P}-title" class="abs" style="left:60px;top:40px;opacity:0"><span style="font-size:52px;font-weight:900">Sơ đồ kho CXAD</span></div>')
        zt = [T[0] + 1.6, T[0] + 2.6, T[0] + 3.5]
        js = st.appear_js(f"#{P}-title", 0.1)
        for z, t in zip(("dong", "chill", "kho"), zt):
            js += (f'tl.fromTo("#{P}-g-{z}",{{opacity:0}},{{opacity:1,duration:0.25}},{t:.2f});\n'
                   f'tl.fromTo("#{P}-{z}",{{scale:1}},{{scale:1.04,duration:0.2,yoyo:true,repeat:1,ease:"power2.out",transformOrigin:"50% 50%"}},{t:.2f});\n')
        for i in range(4):
            t = T[0] + 4.9 + i * 0.85
            js += (f'tl.set("#{P}-f{i}",{{opacity:1}},{t:.2f});\n'
                   f'tl.to("#{P}-f{i}",{{strokeDashoffset:0,duration:0.6,ease:"power2.inOut"}},{t:.2f});\n'
                   + st.pop_js(f"#{P}-n{i}", t + 0.35, 0.3))
        return body, "", js
    s = Scene("cxmap", lines, build, lead=0.6, tail=4.6, min_hold={0: 4.6})
    s.sfx = [(("T", 0, 1.6), "ping.mp3", 0.2)]
    return s


# ============================================================ CHƯƠNG 1 – Bước 1–2
def sheet_html(sid, x, y):
    """Spreadsheet of the inbound plan. Rows {sid}-r{i} start misaligned; animate x to 0."""
    hdr = ["Mã hàng", "Số lượng", "Date / Batch"]
    rows = [("SKU 1001", "30 thùng", "HSD 12/2026"), ("SKU 2001", "40 thùng", "B2405"), ("SKU 3001", "25 thùng", "HSD 03/2027")]
    cell = "display:inline-block;width:200px;padding:10px 12px;border-right:2px solid #D5DBE4;font-size:28px;font-weight:700"
    out = (f'<div id="{sid}" class="abs" style="left:{x}px;top:{y}px;width:640px;background:#fff;border:4px solid {INK};border-radius:16px;overflow:hidden;opacity:0">'
           f'<div style="background:#2FAE5F;color:#fff;font-weight:900;font-size:26px;padding:10px 16px">Kế hoạch nhập (ASN).xlsx</div>'
           f'<div style="background:#EEF2F6;white-space:nowrap">' + "".join(f'<span style="{cell};font-weight:900">{h}</span>' for h in hdr) + '</div>')
    for i, r in enumerate(rows):
        out += (f'<div style="white-space:nowrap;border-top:2px solid #E3E8EF;overflow:hidden"><div id="{sid}-r{i}" style="white-space:nowrap">'
                + "".join(f'<span style="{cell}">{v}</span>' for v in r) + '</div></div>')
    return out + '</div>'


def wms_window(wid, x, y):
    return (f'<div id="{wid}" class="abs" style="left:{x}px;top:{y}px;width:640px;background:#fff;border:4px solid {INK};border-radius:16px;overflow:hidden;opacity:0">'
            f'<div style="background:{C["blue"]};color:#fff;font-weight:900;font-size:26px;padding:10px 16px">WMS · Nhập hàng</div>'
            f'<div style="padding:18px 20px">'
            f'<div style="display:flex;align-items:center;gap:16px"><div id="{wid}-btn" style="background:{C["green"]};color:#fff;font-size:30px;font-weight:900;border:4px solid {INK};border-radius:14px;padding:8px 26px">Import file</div>'
            f'<div style="font-size:24px;font-weight:700;color:{C["muted"]}">Kế hoạch nhập (ASN).xlsx</div></div>'
            f'<div id="{wid}-asn" style="margin-top:18px;border:4px solid {C["green"]};background:#EDF9F1;border-radius:14px;padding:12px 16px;opacity:0">'
            f'<div style="font-size:36px;font-weight:900">ASN-0001 ✔</div><div style="font-size:24px;font-weight:700">Xe 51C-123.45 · 3 pallet · 3 mã hàng</div></div>'
            f'<div id="{wid}-print" style="margin-top:14px;display:inline-block;background:#fff;font-size:26px;font-weight:900;border:4px solid {INK};border-radius:14px;padding:8px 22px;opacity:0">In mã vạch LPN (3)</div>'
            f'</div></div>')


def cx_asn():
    lines = ["Khi có kế hoạch nhập, XLCT nhận file và xử lý cho đúng định dạng WMS.",
             "Sau đó nhập file vào WMS để tạo ASN,",
             "rồi in sẵn mã vạch LPN, giao cho nhân viên kho."]

    def build(T, D):
        P = "cx1"
        PL, PRX = 300, 620
        xl = figure(f"{P}-xl", "xlct", PL, FY - 40, scale=1.5, label=True, pose={"armL": (22, -70), "armR": (-22, 70)})
        rc = figure(f"{P}-rc", "receiver", 2100, FY, scale=1.5, label=True)
        body = svg_layer(st.floor() + desk_svg(PL) + printer_svg(f"{P}-printer", PRX) + xl + rc)
        body += sheet_html(f"{P}-sheet", 1020, 170) + wms_window(f"{P}-wms", 1020, 170)
        body += (f'<div id="{P}-okfmt" class="abs" style="left:1170px;top:500px;opacity:0"><div style="display:flex;align-items:center;gap:12px;background:#fff;border:5px solid {C["green"]};'
                 f'border-radius:18px;padding:10px 24px;font-size:36px;font-weight:900">{st.check(46)}Đúng định dạng WMS</div></div>')
        body += st.badge(f"{P}-b1", 1, "Nhận ASN") + st.badge(f"{P}-b2", 2, "Nhập vào WMS")
        # LPN label sheet: printed at the printer, then into the corner, then handed over
        body += doc_shape(f"{P}-lpn", PRX - 115, FY - 340, "Mã vạch LPN", barcode=True)
        offs = [26, -18, 8]
        js = st.badge_seq_js([f"{P}-b1", f"{P}-b2"], [T[0], T[1]], D - 0.6)
        js += 'tl.fromTo("#%s-xl-label",{opacity:0,y:10},{opacity:1,y:0,duration:0.3,ease:"back.out(2)"},0.3);\n' % P
        js += f'tl.fromTo("#{P}-sheet",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power2.out"}},{T[0]+0.2:.2f});\n'
        for i, o in enumerate(offs):
            js += f'tl.fromTo("#{P}-sheet-r{i}",{{x:{o}}},{{x:0,duration:0.45,ease:"back.out(1.6)"}},{T[0]+1.6 + i*0.25:.2f});\n'
        js += st.stamp_js(f"{P}-okfmt", T[0] + 2.6)
        js += f'tl.to("#{P}-okfmt",{{opacity:0,duration:0.2}},{T[1]-0.1:.2f});\n'
        js += f'tl.to("#{P}-sheet",{{opacity:0,x:-30,duration:0.25}},{T[1]:.2f});\n'
        js += f'tl.fromTo("#{P}-wms",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.3,ease:"power2.out"}},{T[1]+0.1:.2f});\n'
        js += f'tl.to("#{P}-wms-btn",{{scale:0.92,duration:0.1,yoyo:true,repeat:1}},{T[1]+0.7:.2f});\n'
        js += st.pop_js(f"#{P}-wms-asn", T[1] + 1.0)
        js += st.pop_js(f"#{P}-wms-print", T[2] + 0.1)
        js += f'tl.to("#{P}-wms-print",{{scale:0.92,duration:0.1,yoyo:true,repeat:1}},{T[2]+0.5:.2f});\n'
        # print: paper slides up out of the printer, then flies to the corner (document tray)
        js += doc_fly_js(f"{P}-lpn", T[2] + 0.7, 1660 - (PRX - 115), 30 - (FY - 340), hold=2.2)
        # receiver walks in, XLCT stands and hands over
        tw = T[2] + 0.6
        js += f'tl.to("#{P}-rc",{{x:{800 - 2100},duration:2.0,ease:"none"}},{tw:.2f});\n' + walk_js(f"{P}-rc", tw, tw + 2.0)
        js += f'tl.fromTo("#{P}-rc-label",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{tw+1.4:.2f});\n'
        js += f'tl.to("#{P}-xl-label",{{opacity:0,duration:0.2}},{tw+1.2:.2f});\n'
        th = tw + 2.2
        js += pose_js(f"{P}-xl", th, {"armR": (-100, -10)}, dur=0.3, ease="power2.out")
        js += pose_js(f"{P}-rc", th + 0.2, {"armL": (80, 10)}, dur=0.3, ease="power2.out")
        js += f'tl.fromTo("#{P}-hand",{{opacity:0,x:0,y:0}},{{opacity:1,duration:0.15}},{th+0.3:.2f});\n'
        js += f'tl.to("#{P}-hand",{{x:150,y:60,duration:0.6,ease:"power2.inOut"}},{th+0.4:.2f});\n'
        js += pose_js(f"{P}-xl", th + 1.2, {"armR": (-22, 70)}, dur=0.3)
        hand = (f'<g transform="translate({PRX - 32},{FY - 236})"><g id="{P}-hand" opacity="0"><rect x="0" y="0" width="64" height="44" rx="4" fill="#fff" stroke="{C["blue"]}" stroke-width="3"/>'
                + "".join(f'<rect x="{8 + i*7}" y="14" width="{2 if i % 3 else 4}" height="18" fill="{INK}"/>' for i in range(7)) + '</g></g>')
        body += svg_layer(hand)
        return body, "", js
    s = Scene("cxasn", lines, build, lead=0.5, tail=2.2, min_hold={0: 4.2, 1: 2.8, 2: 4.6})
    s.sfx = [(("T", 0, 2.6), "chime.mp3", 0.22), (("T", 2, 0.7), "click-soft.mp3", 0.3)]
    return s


def timeline():
    return [cx_intro(), cx_map(), chapter(1, "Nhập hàng và Putaway bằng LPN", lead=2.7), cx_asn()]


if __name__ == "__main__":
    limit = float(sys.argv[1]) if len(sys.argv) > 1 else None
    os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
    placed, total, kept = build_all(limit, seq=timeline(), out=OUT)
    for s, start in placed:
        print(f"{start:7.2f}  {s.D:6.2f}  {s.cid}")
    print("TOTAL", total, "sfx", len(kept))
