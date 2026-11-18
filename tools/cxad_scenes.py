"""Scenes for the CXAD video after Chương 1 Bước 2 (see build_cxad.py for intro, map, Bước 1–2)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, stick, walk_js, pose_js, REST, pda_svg, icon
import stage as st
from stage import FY, INK
from build_full import Scene, ghinho, ic_svg
from parts import figure, svg_layer, desk_svg, pallet_build, pda_popup, kv, swap_js, hand, carry_box, SCAN, CARRY
from parts import ic_pallet, ic_forklift, ic_truck, ic_check, doc_html
import build_cxad as bx
from build_cxad import ZONE, zone_icon, printer_svg

HANDW = "#2747C9"   # pen ink for handwriting on paper


# ============================================================ helpers
def lab_js(fid, t):
    return f'tl.fromTo("#{fid}-label",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t:.2f});\n'


def lab_off(fid, t):
    return f'tl.to("#{fid}-label",{{opacity:0,duration:0.2}},{t:.2f});\n'


def press_js(sel, t):
    return (f'tl.to("{sel}",{{scale:0.92,duration:0.1}},{t:.2f});\n'
            f'tl.to("{sel}",{{scale:1,duration:0.15}},{t+0.1:.2f});\n')


def show_js(sel, t, dur=0.3):
    return f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:{dur}}},{t:.2f});\n'


def hide_js(sel, t, dur=0.2):
    return f'tl.to("{sel}",{{opacity:0,duration:{dur}}},{t:.2f});\n'


def write_js(sel, t, dur=0.7):
    """Handwriting / typing reveal left to right."""
    return (f'tl.set("{sel}",{{opacity:1}},{t:.2f});\n'
            f'tl.fromTo("{sel}",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:{dur},ease:"none"}},{t:.2f});\n')


def draw_js(sel, t, dur=0.5):
    return (f'tl.set("{sel}",{{opacity:1}},{t:.2f});\n'
            f'tl.to("{sel}",{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut"}},{t:.2f});\n')


def walk_to(fid, mv, dx, t, dur):
    return f'tl.to("#{mv}",{{x:{dx},duration:{dur},ease:"none"}},{t:.2f});\n' + walk_js(fid, t, t + dur)


def win(wid, x, y, w, title, inner, color=None, hidden=True):
    op = "opacity:0;" if hidden else ""
    return (f'<div id="{wid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;background:#fff;border:4px solid {INK};border-radius:16px;overflow:hidden;{op}">'
            f'<div style="background:{color or C["blue"]};color:#fff;font-weight:900;font-size:28px;padding:10px 18px">{title}</div>'
            f'<div style="padding:18px 20px;position:relative">{inner}</div></div>')


def btn(bid, text, color=None, hidden=False):
    op = "opacity:0;" if hidden else ""
    return (f'<div id="{bid}" style="display:inline-block;background:{color or C["green"]};color:#fff;font-size:30px;font-weight:900;'
            f'border:4px solid {INK};border-radius:14px;padding:8px 26px;{op}">{text}</div>')


def pill(pid, x, y, text, color="#fff", txt=INK, border=INK, size=34):
    return (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;opacity:0"><span style="display:inline-block;background:{color};color:{txt};'
            f'border:4px solid {border};border-radius:16px;padding:8px 22px;font-size:{size}px;font-weight:900;white-space:nowrap">{text}</span></div>')


def sheet(sid, x, y, title, hdr, rows, cw=210, w=None):
    cell = f"display:inline-block;width:{cw}px;padding:10px 12px;border-right:2px solid #D5DBE4;font-size:28px;font-weight:700;box-sizing:border-box"
    w = w or cw * len(hdr)
    out = (f'<div id="{sid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;background:#fff;border:4px solid {INK};border-radius:16px;overflow:hidden;opacity:0">'
           f'<div style="background:#2FAE5F;color:#fff;font-weight:900;font-size:26px;padding:10px 16px">{title}</div>'
           f'<div style="background:#EEF2F6;white-space:nowrap">' + "".join(f'<span style="{cell};font-weight:900">{h}</span>' for h in hdr) + '</div>')
    for i, r in enumerate(rows):
        out += (f'<div style="white-space:nowrap;border-top:2px solid #E3E8EF;overflow:hidden"><div id="{sid}-r{i}" style="white-space:nowrap">'
                + "".join(f'<span style="{cell}">{v}</span>' for v in r) + '</div></div>')
    return out + '</div>'


def paper(did, x, y, title, w=220, h=150, edge=None, kind="lines", head=None):
    """Legend 'Chứng từ' shape (wavy bottom), hidden. kind: lines | barcode."""
    edge = edge or C["blue"]
    wave = f'M0,0 H{w} V{h-18} C{w*0.75},{h-42} {w*0.55},{h+6} {w*0.3},{h-10} C{w*0.18},{h-18} {w*0.08},{h-14} 0,{h-6} Z'
    if kind == "barcode":
        inner = "".join(f'<rect x="{18 + i*11}" y="{58 + r*26}" width="{3 if i % 3 else 6}" height="18" fill="{INK}"/>'
                        for r in range(3) for i in range(int((w - 36) / 11)))
    else:
        inner = "".join(f'<rect x="18" y="{60 + r*20}" width="{w-36 - (50 if r % 2 else 0)}" height="8" rx="4" fill="#D5DBE4"/>' for r in range(3))
    hd = f'<rect x="0" y="0" width="{w}" height="12" fill="{head}"/>' if head else ""
    return (f'<div id="{did}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;opacity:0">'
            f'<svg width="{w}" height="{h}" viewBox="-3 -3 {w+6} {h+6}" style="overflow:visible"><path d="{wave}" fill="#fff" stroke="{edge}" stroke-width="4"/>{hd}'
            f'<text x="{w/2}" y="40" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="24" fill="{INK}">{title}</text>{inner}</svg></div>')


def fly_corner_js(did, t, x0, y0, x1=1700, y1=24, scale=0.5):
    return f'tl.to("#{did}",{{x:{x1-x0},y:{y1-y0},scale:{scale},duration:0.6,ease:"power2.inOut",transformOrigin:"0% 0%"}},{t:.2f});\n'


def diamond(did, cx, cy, text, w=440, h=230, fs=34):
    lines = text.split("\n")
    y0 = cy - (len(lines) - 1) * fs * 0.6 + fs * 0.35
    tx = "".join(f'<text x="{cx}" y="{y0 + i*fs*1.2:.0f}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="{fs}" fill="{INK}">{l}</text>'
                 for i, l in enumerate(lines))
    return (f'<g id="{did}" opacity="0"><polygon points="{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}" fill="#fff" stroke="{C["blue"]}" stroke-width="5" stroke-linejoin="round"/>{tx}</g>')


def arrow_defs(p, color=None):
    color = color or C["blue"]
    return (f'<defs><marker id="{p}-ah" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 Z" fill="{color}"/></marker></defs>')


def arrow(aid, d, p, color=None, width=8, dash=900):
    return (f'<path id="{aid}" d="{d}" opacity="0" fill="none" stroke="{color or C["blue"]}" stroke-width="{width}" stroke-linecap="round" '
            f'stroke-dasharray="{dash}" stroke-dashoffset="{dash}" marker-end="url(#{p}-ah)"/>')


def dock_svg():
    return (f'<rect x="0" y="560" width="110" height="240" fill="#D5DBE4"/><text x="60" y="545" text-anchor="middle" font-family="{FONT}" '
            f'font-weight="900" font-size="26" fill="{C["muted"]}">DOCK</text>')


def zone_banner(bid, z, x, y, w):
    fill, edge, lab = ZONE[z]
    return (f'<g id="{bid}"><rect x="{x}" y="{y}" width="{w}" height="62" rx="14" fill="{fill}" stroke="{edge}" stroke-width="5"/>'
            f'<text x="{x + w/2}" y="{y + 44}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="36" fill="{INK}">KHU {lab}</text>'
            + zone_icon(z, x + 46, y + 31, 0.8) + '</g>')


class ZRack(st.Rack):
    """Rack in a temperature zone: zone tint instead of Reserved/Primary, short labels A01-02."""

    def __init__(self, prefix, x0, zone, **kw):
        super().__init__(prefix, x0, **kw)
        self.zone = zone

    def loc(self, c, k):
        return f"A{c+1:02d}-{k+1:02d}"

    def full(self, c, k):
        return f"{ZONE[self.zone][2]}-A{c+1:02d}-{k+1:02d}"

    def svg(self, contents=None, tags=None):
        fill, edge, _ = ZONE[self.zone]
        out = super().svg(contents, tags)
        out = out.replace(f'fill="{C["reserved"]}" opacity="0.45"', f'fill="{fill}" opacity="0.9"')
        out = out.replace('fill="#FFE3C4" opacity="0.8"', f'fill="{fill}" opacity="0.9"')
        out = out.replace(f'fill="{C["orange"]}" stroke="{INK}" stroke-width="2.5"', f'fill="{edge}" stroke="{INK}" stroke-width="2.5"')
        out = out.replace(f'fill="#8DBAF0" stroke="{INK}" stroke-width="2.5"', f'fill="{edge}" stroke="{INK}" stroke-width="2.5"')
        return out


def label_svg(fid, role, sc):
    from kit import ROLE
    txt = ROLE[role][1]
    w = 30 + len(txt) * 14.5
    return (f'<g transform="scale({sc})"><g id="{fid}-label"><rect x="{-w/2:.0f}" y="-214" width="{w:.0f}" height="44" rx="22" fill="{INK}"/>'
            f'<text x="0" y="-184" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="24" fill="#fff">{txt}</text>'
            f'<polygon points="-8,-171 8,-171 0,-161" fill="{INK}"/></g></g>')


def mirrored(fid, role, sc, pose=None, hand_r="", label=True):
    """Figure facing left that can still walk (mirror on a plain wrapper, label unmirrored)."""
    return (f'<g transform="scale(-1,1)">{stick(fid, role, sc, pose=pose, hand_r=hand_r)}</g>'
            + (label_svg(fid, role, sc) if label else ""))


def cups(gid, x, by, n, hidden=True):
    op = ' opacity="0"' if hidden else ""
    s = "".join(f'<path d="M{x + i*22},{by-26} h18 l-3,26 h-12 z" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                f'<rect x="{x + i*22 - 1}" y="{by-30}" width="20" height="6" rx="2" fill="#24A08C" stroke="{INK}" stroke-width="1.5"/>' for i in range(n))
    return f'<g id="{gid}"{op}>{s}</g>'


def clipboard(fid):
    """Clipboard with a paper Picklist, drawn in forearm space."""
    return (f'<g id="{fid}-clip" transform="translate(0,22)"><rect x="-17" y="-4" width="34" height="42" rx="3" fill="#C9965A" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="-13" y="2" width="26" height="32" fill="#fff"/><rect x="-7" y="-7" width="14" height="6" rx="2" fill="#5D7290"/>'
            f'<line x1="-9" y1="10" x2="9" y2="10" stroke="#B0B8C4" stroke-width="2"/><line x1="-9" y1="17" x2="9" y2="17" stroke="#B0B8C4" stroke-width="2"/>'
            f'<line x1="-9" y1="24" x2="4" y2="24" stroke="#B0B8C4" stroke-width="2"/></g>')


def cell_svg(cid, cx, code, w=240, load="", qty=None, sign_h=230):
    """Floor cell of one DO in khu chia: dashed floor patch + sign with DO number. Hidden load group {cid}-load."""
    q = (f'<rect x="{cx-58}" y="{FY-170}" width="116" height="42" rx="21" fill="{INK}"/>'
         f'<text x="{cx}" y="{FY-140}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="26" fill="#fff">{qty}</text>') if qty else ""
    return (f'<g id="{cid}"><rect x="{cx-w/2}" y="{FY-6}" width="{w}" height="22" rx="6" fill="#FFE9D2" stroke="{C["orange"]}" stroke-width="4" stroke-dasharray="12 8"/>'
            f'<rect id="{cid}-hl" x="{cx-w/2-8}" y="{FY-sign_h-60}" width="{w+16}" height="{sign_h+84}" rx="16" fill="none" stroke="{C["orange"]}" stroke-width="7" opacity="0"/>'
            f'<line x1="{cx+w/2-18}" y1="{FY}" x2="{cx+w/2-18}" y2="{FY-sign_h}" stroke="{INK}" stroke-width="6"/>'
            f'<g id="{cid}-sign"><rect x="{cx-w/2+10}" y="{FY-sign_h-50}" width="{w-20}" height="58" rx="10" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            f'<text x="{cx}" y="{FY-sign_h-10}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="32" fill="{INK}">{code}</text></g>'
            f'<g id="{cid}-load" opacity="0">{load}{q}</g></g>')


def ic(inner):
    return ic_svg(inner)


IC_PDA = ic(f'<rect x="18" y="4" width="28" height="56" rx="6" fill="#2B3646" stroke="{INK}" stroke-width="3"/><rect x="22" y="12" width="20" height="24" rx="2" fill="#7FD3FF"/>'
            f'<path d="M46 20 L60 14 M46 28 L60 28" stroke="#E53935" stroke-width="4" stroke-linecap="round"/>')
IC_DOC = ic(f'<path d="M12 6 H52 V50 C42 44 34 60 24 54 C18 51 14 53 12 54 Z" fill="#fff" stroke="{C["blue"]}" stroke-width="4"/>'
            f'<path d="M20 20h24M20 30h24M20 40h14" stroke="#B0B8C4" stroke-width="4" stroke-linecap="round"/>')
IC_PEN = ic(f'<rect x="10" y="8" width="34" height="46" rx="4" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M16 22h20M16 32h14" stroke="#B0B8C4" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M30 52 L54 20 L60 26 L36 58 L28 60 Z" fill="{C["orange"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
IC_CELLS = ic(f'<rect x="4" y="34" width="16" height="16" fill="#FFE9D2" stroke="{C["orange"]}" stroke-width="3"/><rect x="24" y="34" width="16" height="16" fill="#FFE9D2" stroke="{C["orange"]}" stroke-width="3"/>'
              f'<rect x="44" y="34" width="16" height="16" fill="#FFE9D2" stroke="{C["orange"]}" stroke-width="3"/><path d="M12 30V14M32 30V14M52 30V14" stroke="{INK}" stroke-width="3"/>'
              f'<rect x="4" y="8" width="16" height="8" fill="#fff" stroke="{INK}" stroke-width="2"/><rect x="24" y="8" width="16" height="8" fill="#fff" stroke="{INK}" stroke-width="2"/><rect x="44" y="8" width="16" height="8" fill="#fff" stroke="{INK}" stroke-width="2"/>')
IC_WARN = ic(f'<path d="M32 6 L60 56 H4 Z" fill="{C["orange"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M32 24v16" stroke="{INK}" stroke-width="6" stroke-linecap="round"/><circle cx="32" cy="48" r="3.5" fill="{INK}"/>')
IC_LOOP = ic(f'<path d="M50 30 A18 18 0 1 1 40 15" fill="none" stroke="{C["blue"]}" stroke-width="6" stroke-linecap="round"/><path d="M36 6 L46 15 L35 22" fill="none" stroke="{C["blue"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')


# ============================================================ CHƯƠNG 1 (tiếp)
def cx_dock():
    lines = ["Xe hàng tới, nhân viên nhận hàng tạo phiếu nhập trên PDA, nhập số xe và tên tài xế."]

    def build(T, D):
        P = "c13"
        body = svg_layer(st.floor() + dock_svg()
                         + f'<g transform="translate(1960,{FY})"><g id="{P}-truck">{st.truck(P + "-tk", label="51C-123.45")}</g></g>'
                         + figure(f"{P}-rc", "receiver", 330, scale=1.5, label=True, pose=SCAN, hand_r=pda_svg(P + "-rc")))
        p1 = (f'<div class="lbl">Phiếu ASN</div><div class="fld ok">ASN-0001</div>'
              f'<div class="lbl">Số xe</div><div class="fld"><span id="{P}-t1" style="opacity:0;display:inline-block">51C-123.45</span></div>'
              f'<div class="lbl">Tài xế</div><div class="fld"><span id="{P}-t2" style="opacity:0;display:inline-block">Trần Văn Bình</span></div>'
              f'<div id="{P}-go" class="go">TẠO PHIẾU NHẬP</div>')
        body += st.pda(f"{P}-pda", "Tạo phiếu nhập", [("s1", p1)])
        body += st.badge(f"{P}-b3", 3, "Tạo phiếu nhập") + st.stamp(f"{P}-ok", "Đã tạo phiếu nhập", x=560, y=170)
        js = f'tl.fromTo("#{P}-truck",{{x:0}},{{x:-1340,duration:1.6,ease:"power2.out"}},0.0);\n' + lab_js(f"{P}-rc", 0.5)
        js += st.badge_seq_js([f"{P}-b3"], [T[0]], D - 0.4)
        js += st.appear_js(f"#{P}-pda", T[0] + 0.1, 0.35, dy=30) + st.show_panel_js(f"{P}-pda", None, "s1", T[0] + 0.2)
        js += write_js(f"#{P}-t1", T[0] + 1.4) + write_js(f"#{P}-t2", T[0] + 2.8)
        js += press_js(f"#{P}-go", T[0] + 4.2) + st.stamp_js(f"{P}-ok", T[0] + 4.5)
        return body, "", js
    s = Scene("cxdock", lines, build, lead=1.4, tail=1.4, min_hold={0: 5.6})
    s.sfx = [(("T", 0, 4.5), "chime.mp3", 0.22)]
    return s


def cx_pallet():
    lines = ["Nhân viên mang pallet tới khu nhận hàng và dán LPN lên pallet.",
             "Kiểm tra ngoại quan từng thùng, rồi xếp hàng lên pallet."]

    def build(T, D):
        P, PX, RX, TX = "c14", 520, 700, 1080
        mag = (f'<g id="{P}-mag" opacity="0" transform="translate({TX+40},{FY-330})"><circle cx="0" cy="0" r="34" fill="#EAF6FF" stroke="{INK}" stroke-width="6"/>'
               f'<line x1="24" y1="24" x2="54" y2="54" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
               f'<path d="M-14,0 l9,10 l18,-20" fill="none" stroke="{C["green"]}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>')
        body = svg_layer(st.floor() + dock_svg()
                         + f'<g transform="translate(1150,{FY})">{st.truck(P + "-tk", label="51C-123.45")}</g>'
                         + f'<g id="{P}-palmv">{pallet_build(P + "-pal", PX, FY, sku="2001")}</g>'
                         + figure(f"{P}-rc", "receiver", RX, scale=1.5, extra=carry_box(f"{P}-rc", 1.5)) + mag)
        body += (f'<div id="{P}-zoom" class="abs" style="left:220px;top:180px;opacity:0"><div style="background:#fff;border:5px solid {INK};border-radius:22px;padding:20px 32px;box-shadow:0 12px 0 rgba(27,36,48,.12)">'
                 f'<div style="font-size:30px;font-weight:700;color:{C["muted"]}">Nhãn LPN đã in sẵn</div><div style="font-size:60px;font-weight:900;margin:4px 0 8px">LPN-000102</div>'
                 f'<svg width="360" height="66" viewBox="0 0 360 66">{"".join(f"<rect x={chr(34)}{6 + i*13}{chr(34)} y={chr(34)}4{chr(34)} width={chr(34)}{4 if i % 3 else 7}{chr(34)} height={chr(34)}58{chr(34)} fill={chr(34)}{INK}{chr(34)}/>" for i in range(27))}</svg></div></div>')
        body += st.badge(f"{P}-b4", 4, "Chuẩn bị pallet") + st.badge(f"{P}-b5", 5, "Chất hàng lên pallet")
        js = st.badge_seq_js([f"{P}-b4", f"{P}-b5"], [T[0], T[1]], D - 0.4)
        js += f'tl.fromTo("#{P}-palmv",{{x:-700}},{{x:0,duration:1.3,ease:"power2.out"}},{T[0]+0.2:.2f});\n'
        js += st.pop_js(f"#{P}-pal-lpn", T[0] + 1.9)
        js += f'tl.fromTo("#{P}-zoom",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.8)",transformOrigin:"50% 100%"}},{T[0]+2.1:.2f});\n'
        js += hide_js(f"#{P}-zoom", T[1] - 0.2)
        t = T[1] + 0.2
        for trip in range(2):
            js += walk_to(f"{P}-rc", f"{P}-rc", TX - RX, t, 1.0)
            js += pose_js(f"{P}-rc", t + 1.0, CARRY, dur=0.25)
            js += show_js(f"#{P}-rc-box", t + 1.1, 0.15)
            js += f'tl.fromTo("#{P}-mag",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(2)"}},{t+1.2:.2f});\n' + hide_js(f"#{P}-mag", t + 1.75)
            js += walk_to(f"{P}-rc", f"{P}-rc", 0, t + 1.9, 1.0)
            js += hide_js(f"#{P}-rc-box", t + 2.95, 0.1)
            for k in (2 * trip, 2 * trip + 1):
                js += st.pop_js(f"#{P}-pal-c{k}", t + 2.95 + 0.12 * (k % 2), 0.3)
            js += pose_js(f"{P}-rc", t + 3.0, REST, dur=0.2)
            t += 3.3
        return body, "", js
    s = Scene("cxpallet", lines, build, lead=0.4, tail=1.0, min_hold={0: 4.4, 1: 6.8})
    s.sfx = [(("T", 0, 1.9), "click-soft.mp3", 0.3)]
    return s


def cx_rpda():
    lines = ["Trên PDA: quét LPN, quét mã hàng,",
             "nhập số lượng, và nhập date hoặc batch."]

    def build(T, D):
        P, PX, RX, SC = "c16", 420, 760, 1.6
        a, b = SCAN["armR"]
        tip = hand(RX, FY, SC, a, b, flip=True, extra=56)
        body = svg_layer(st.floor() + pallet_build(P + "-pal", PX, FY, sku="2001", shown=True)
                         + figure(f"{P}-rc", "receiver", RX, scale=SC, flip=True, pose=SCAN, hand_r=pda_svg(P + "-rc"))
                         + st.laser(f"{P}-l1", tip[0], tip[1], PX - 39, FY - 45) + st.laser(f"{P}-l2", tip[0], tip[1], PX + 38, FY - 102))
        p1 = kv("Quét LPN", "LPN-000102 ✔", "Pallet đang nhận")
        p2 = kv("Quét mã hàng", "SKU 2001 ✔", "Sữa chua · 50 hũ/thùng")
        p3 = ('<div class="lbl">Số lượng nhận</div><div class="fld ok">40 thùng</div>'
              '<div class="keys">' + "".join(f"<div>{k}</div>" for k in "123456789") + '</div>')
        p4 = (f'<div class="lbl">Hạn sử dụng (date)</div><div class="fld ok">20/05/2027</div>'
              f'<div class="lbl">Batch</div><div class="fld ok">B2405</div><div id="{P}-go" class="go">XÁC NHẬN</div>')
        body += st.pda(f"{P}-pda", "Nhận hàng", [("s1", p1), ("s2", p2), ("s3", p3), ("s4", p4)])
        steps = ["Quét LPN", "Quét mã hàng", "Số lượng", "Date / Batch"]
        chips = "".join(f'<div id="{P}-k{i}" style="background:#fff;border:4px solid {INK};border-radius:14px;padding:6px 16px;font-size:28px;font-weight:900;opacity:0.3">{i+1}. {t}</div>'
                        for i, t in enumerate(steps))
        body += f'<div class="abs" style="left:80px;top:160px;display:flex;gap:12px">{chips}</div>'
        body += st.badge(f"{P}-b6", 6, "Nhận hàng")
        times = [T[0] + 0.2, T[0] + 2.1, T[1] + 0.1, T[1] + 2.4]
        js = st.badge_seq_js([f"{P}-b6"], [T[0]], D - 0.4)
        js += st.appear_js(f"#{P}-pda", T[0], 0.35, dy=30)
        prev = None
        for i, t in enumerate(times):
            js += st.show_panel_js(f"{P}-pda", prev, f"s{i+1}", t)
            js += f'tl.to("#{P}-k{i}",{{opacity:1,background:"#FFF2E0",duration:0.2}},{t:.2f});\n'
            if i:
                js += f'tl.to("#{P}-k{i-1}",{{background:"#EDF9F1",duration:0.2}},{t:.2f});\n'
            prev = f"s{i+1}"
        js += st.laser_js(f"{P}-l1", times[0] + 0.4) + st.laser_js(f"{P}-l2", times[1] + 0.3)
        js += press_js(f"#{P}-go", times[3] + 1.8) + f'tl.to("#{P}-k3",{{background:"#EDF9F1",duration:0.2}},{times[3]+1.9:.2f});\n'
        return body, "", js
    s = Scene("cxrpda", lines, build, lead=0.4, tail=1.0, min_hold={0: 4.4, 1: 5.0})
    s.sfx = [(("T", 0, 0.6), "ping.mp3", 0.25)]
    return s


def cx_put():
    lines = ["Để cất hàng, tài xế xe nâng quét LPN. Hệ thống gợi ý vị trí theo khu.",
             "Xe nâng mang pallet tới đúng vị trí.",
             "Quét mã vạch vị trí để xác nhận."]

    def build(T, D):
        P = "c17"
        R = ZRack(P + "r", 900, "chill", cols=3, levels=3, cw=260, lh=200)
        rack = R.svg(contents={(1, 0): "cartons", (2, 0): "cartons", (1, 1): "pallet", (2, 2): "pallet", (0, 0): "cartons"})
        FX = 330
        tx, tb = R.slot(0, 1)
        lift, drive = tb - (FY - 22), tx - 125 - FX
        back = drive - 170
        load = pallet_build(P + "-pal", 125, -22, sku="2001", shown=True)
        fl = f'<g transform="translate({FX},{FY})"><g id="{P}-fl">{st.forklift(P + "-fk", label=True, load=load)}</g></g>'
        placed = f'<g id="{P}-placed" opacity="0">{st.pallet(P + "-pp", tx, tb, lpn=True, sku="2001")}</g>'
        lab = R.label_xy(0, 1)
        las1 = st.laser(f"{P}-l1", FX - 10, FY - 175, FX + 125 - 39, FY - 22 - 45)
        las2 = st.laser(f"{P}-l2", FX + back - 10, FY - 175, lab[0] - 40, lab[1] + 4)
        arr = (f'<path id="{P}-arr" d="M{FX+125},{FY-200} C{FX+260},{FY-440} {tx-220},{tb-330} {tx},{tb-170}" fill="none" '
               f'stroke="{C["orange"]}" stroke-width="8" stroke-dasharray="1100" stroke-dashoffset="1100" stroke-linecap="round"/>'
               f'<rect id="{P}-hl" x="{tx-R.cw/2+8}" y="{tb-R.lh+34}" width="{R.cw-16}" height="{R.lh-30}" rx="8" fill="none" stroke="{C["orange"]}" stroke-width="8" opacity="0"/>')
        pop = pda_popup(f"{P}-pop", "Cất hàng (Putaway)", [
            ("q1", kv("Đã quét LPN", "LPN-000102 ✔", "SKU 2001 · hàng Chill")),
            ("q2", kv("Vị trí gợi ý", R.full(0, 1), "Theo quy tắc putaway của khu", "#C45A00")),
            ("q3", kv("Quét vị trí", f"{R.full(0, 1)} ✔", "Xác nhận đã cất")),
        ], 130, 160)
        body = svg_layer(st.floor() + rack + zone_banner(P + "-zb", "chill", 900, 120, 780) + placed + arr + fl + las1 + las2) \
            + pop + st.stamp(f"{P}-done", "Đã cất hàng", x=760, y=230)
        body += st.badge(f"{P}-b7", 7, "Putaway") + st.badge(f"{P}-b8", 8, "Di chuyển pallet") + st.badge(f"{P}-b9", 9, "Xác nhận vị trí")
        js = st.badge_seq_js([f"{P}-b7", f"{P}-b8", f"{P}-b9"], [T[0], T[1], T[2]], D - 0.4)
        js += f'tl.fromTo("#{P}-fk-drv-label",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},0.3);\n'
        js += st.appear_js(f"#{P}-pop", T[0] + 0.3, 0.3, dy=20)
        js += st.laser_js(f"{P}-l1", T[0] + 0.6)
        js += swap_js(f"{P}-pop", [(T[0] + 0.7, "q1"), (T[0] + 2.8, "q2"), (T[2] + 0.3, "q3")])
        js += f'tl.to("#{P}-arr",{{strokeDashoffset:0,duration:0.9,ease:"power2.inOut"}},{T[0]+3.0:.2f});\n'
        js += show_js(f"#{P}-hl", T[0] + 3.7)
        t1 = T[1]
        js += hide_js(f"#{P}-arr", t1, 0.3)
        js += f'tl.to("#{P}-fl",{{x:{drive},duration:1.4,ease:"power2.inOut"}},{t1:.2f});\n'
        js += f'tl.to("#{P}-fk-forks",{{y:{lift},duration:1.0,ease:"power2.inOut"}},{t1+1.45:.2f});\n'
        js += f'tl.set("#{P}-placed",{{opacity:1}},{t1+2.5:.2f});\ntl.set("#{P}-pal",{{opacity:0}},{t1+2.5:.2f});\n'
        js += f'tl.to("#{P}-fk-forks",{{y:0,duration:0.8,ease:"power2.inOut"}},{t1+2.6:.2f});\n'
        js += f'tl.to("#{P}-fl",{{x:{back},duration:0.8,ease:"power2.inOut"}},{t1+2.6:.2f});\n'
        js += hide_js(f"#{P}-hl", t1 + 2.6)
        js += st.laser_js(f"{P}-l2", T[2] + 0.2) + st.stamp_js(f"{P}-done", T[2] + 0.8)
        return body, "", js
    s = Scene("cxput", lines, build, lead=0.5, tail=1.4, min_hold={0: 5.2, 1: 3.6, 2: 2.8})
    s.sfx = [(("T", 0, 0.6), "ping.mp3", 0.25), (("T", 2, 0.8), "chime.mp3", 0.22)]
    return s


def cx_loop():
    lines = ["Còn pallet chưa nhận thì lặp lại từ bước chuẩn bị pallet."]

    def build(T, D):
        P = "c1l"
        dx, dy = 560, 400
        svg = (arrow_defs(P) + diamond(f"{P}-dm", dx, dy, "Còn pallet\nchưa nhận?", 460, 250)
               + arrow(f"{P}-yes", f"M{dx-230},{dy} C{dx-330},{dy} {dx-330},{dy-110} {dx-300},{dy-150}", P)
               + arrow(f"{P}-no", f"M{dx},{dy+125} L{dx},{dy+230}", P))
        body = svg_layer(svg)
        body += pill(f"{P}-yl", 150, 410, "Có", C["orange"]) + pill(f"{P}-nl", 590, 560, "Không", "#fff")
        body += (f'<div id="{P}-loopbox" class="abs" style="left:110px;top:150px;opacity:0"><div style="background:#fff;border:5px solid {C["orange"]};border-radius:20px;'
                 f'padding:12px 26px;font-size:38px;font-weight:900">Lặp lại Bước 4 → 9</div></div>')
        body += (f'<div id="{P}-next" class="abs" style="left:380px;top:650px;opacity:0"><div style="background:#fff;border:5px solid {C["green"]};border-radius:20px;'
                 f'padding:12px 26px;font-size:36px;font-weight:900">Bước 10: Hoàn tất nhận hàng</div></div>')
        rows = [("LPN-000102", "SKU 2001 · Sữa chua", "chill"), ("LPN-000101", "SKU 1001 · Há cảo", "dong"), ("LPN-000103", "SKU 3001 · Bánh quy", "kho")]
        rh = ""
        for i, (lpn, sku, z) in enumerate(rows):
            fill, edge, lab = ZONE[z]
            rh += (f'<div style="display:flex;align-items:center;gap:16px;border-top:3px solid #E3E8EF;padding:14px 0">'
                   f'<div style="flex:1"><div style="font-size:34px;font-weight:900">{lpn}</div><div style="font-size:26px;font-weight:700;color:{C["muted"]}">{sku}</div></div>'
                   f'<div style="background:{fill};border:4px solid {edge};border-radius:14px;padding:6px 16px;font-size:28px;font-weight:900">→ KHU {lab}</div>'
                   f'<div id="{P}-ok{i}" style="opacity:0">{st.check(52)}</div></div>')
        cnt = "".join(f'<span id="{P}-n{i}" class="abs" style="left:0;top:0;opacity:{1 if i == 0 else 0}">{i+1}/3 pallet</span>' for i in range(3))
        body += (f'<div class="abs" style="left:1000px;top:150px;width:820px;background:#fff;border:4px solid {INK};border-radius:22px;padding:20px 28px">'
                 f'<div style="display:flex;justify-content:space-between;align-items:center"><div style="font-size:38px;font-weight:900">ASN-0001</div>'
                 f'<div style="position:relative;width:200px;height:44px;font-size:34px;font-weight:900;color:{C["green"]}">{cnt}</div></div>{rh}</div>')
        js = f'tl.fromTo("#{P}-dm",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{T[0]:.2f});\n'
        js += st.pop_js(f"#{P}-ok0", 0.4)
        js += draw_js(f"#{P}-yes", T[0] + 0.9) + st.appear_js(f"#{P}-yl", T[0] + 1.0) + st.appear_js(f"#{P}-loopbox", T[0] + 1.3)
        for i, t in ((1, T[0] + 2.2), (2, T[0] + 3.4)):
            js += st.pop_js(f"#{P}-ok{i}", t) + hide_js(f"#{P}-n{i-1}", t, 0.1) + show_js(f"#{P}-n{i}", t + 0.1, 0.1)
        js += hide_js(f"#{P}-yl", T[0] + 4.2) + f'tl.to("#{P}-loopbox",{{opacity:0.35,duration:0.2}},{T[0]+4.2:.2f});\n'
        js += draw_js(f"#{P}-no", T[0] + 4.4) + st.appear_js(f"#{P}-nl", T[0] + 4.5) + st.appear_js(f"#{P}-next", T[0] + 4.8)
        return body, "", js
    s = Scene("cxloop", lines, build, lead=0.4, tail=1.6, min_hold={0: 5.8})
    s.sfx = [(("T", 0, 2.2), "ping.mp3", 0.2)]
    return s


def cx_done():
    lines = ["Nhận đủ pallet thì xác nhận hoàn tất nhận hàng.",
             "Cuối cùng, XLCT in phiếu nhập kho và chuyển các bên ký."]

    def build(T, D):
        P = "c1d"
        st1 = f'<g id="{P}-st1">{figure(P + "-rc", "receiver", 330, scale=1.5, pose=SCAN, hand_r=pda_svg(P + "-rc"))}</g>'
        st2 = (f'<g id="{P}-st2" opacity="0">{desk_svg(300)}{printer_svg(P + "-pr", 620)}'
               f'{figure(P + "-xl", "xlct", 300, FY - 40, scale=1.5, label=True, pose={"armL": (22, -70), "armR": (-22, 70)})}</g>')
        body = svg_layer(st.floor() + st1 + st2)
        p1 = (kv("Phiếu ASN", "ASN-0001", "Xe 51C-123.45")
              + f'<div style="margin-top:20px;font-size:26px;font-weight:700;color:{C["muted"]}">Đã nhận</div>'
              f'<div style="height:34px;border-radius:17px;background:#E3E8EF;overflow:hidden;margin:8px 0"><div style="width:100%;height:100%;background:{C["green"]}"></div></div>'
              f'<div style="font-size:40px;font-weight:900;color:{C["green"]}">3/3 pallet ✔</div>'
              f'<div id="{P}-go" class="go" style="margin-top:26px">HOÀN TẤT NHẬN HÀNG</div>')
        body += st.pda(f"{P}-pda", "Nhận hàng", [("s1", p1)])
        body += st.stamp(f"{P}-ok", "Đã nhận đủ hàng", x=560, y=200)
        sig = ["Tài xế (bên giao)", "Nhân viên nhận hàng", "XLCT"]
        boxes = "".join(f'<div style="flex:1;text-align:center"><div style="font-size:22px;font-weight:700;color:{C["muted"]};height:56px">{s}</div>'
                        f'<svg width="200" height="70" viewBox="0 0 200 70"><path id="{P}-sg{i}" d="M20,48 C40,10 55,62 75,30 S110,12 120,44 S160,30 182,22" fill="none" stroke="{HANDW}" stroke-width="5" '
                        f'stroke-linecap="round" stroke-dasharray="320" stroke-dashoffset="320"/><line x1="10" y1="62" x2="190" y2="62" stroke="#B0B8C4" stroke-width="3"/></svg></div>'
                        for i, s in enumerate(sig))
        rows = [("SKU 1001 · Há cảo", "30 thùng"), ("SKU 2001 · Sữa chua", "40 thùng"), ("SKU 3001 · Bánh quy", "25 thùng")]
        rh = "".join(f'<div style="display:flex;justify-content:space-between;border-top:2px solid #E3E8EF;padding:8px 0;font-size:28px;font-weight:700"><span>{a}</span><b>{b}</b></div>' for a, b in rows)
        body += (f'<div id="{P}-doc" class="abs" style="left:1000px;top:110px;width:780px;background:#fff;border:5px solid {C["blue"]};border-radius:14px;padding:22px 30px;opacity:0;box-shadow:0 14px 0 rgba(27,36,48,.10)">'
                 f'<div style="font-size:44px;font-weight:900;text-align:center">PHIẾU NHẬP KHO</div>'
                 f'<div style="font-size:26px;font-weight:700;text-align:center;color:{C["muted"]};margin-bottom:10px">ASN-0001 · Xe 51C-123.45</div>{rh}'
                 f'<div style="display:flex;margin-top:18px">{boxes}</div></div>')
        body += st.badge(f"{P}-b10", 10, "Hoàn tất nhận hàng") + st.badge(f"{P}-b11", 11, "In và ký")
        js = st.badge_seq_js([f"{P}-b10", f"{P}-b11"], [T[0], T[1]], D - 0.4)
        js += st.appear_js(f"#{P}-pda", T[0], 0.35, dy=30) + st.show_panel_js(f"{P}-pda", None, "s1", T[0] + 0.1)
        js += press_js(f"#{P}-go", T[0] + 1.6) + st.stamp_js(f"{P}-ok", T[0] + 1.9)
        js += hide_js(f"#{P}-pda", T[1] - 0.2) + hide_js(f"#{P}-ok", T[1] - 0.2) + hide_js(f"#{P}-st1", T[1] - 0.2)
        js += show_js(f"#{P}-st2", T[1], 0.3) + lab_js(f"{P}-xl", T[1] + 0.2)
        js += f'tl.fromTo("#{P}-doc",{{opacity:0,x:-380,y:420,scale:0.2}},{{opacity:1,x:0,y:0,scale:1,duration:0.8,ease:"power2.out",transformOrigin:"0% 100%"}},{T[1]+0.6:.2f});\n'
        for i in range(3):
            js += f'tl.to("#{P}-sg{i}",{{strokeDashoffset:0,duration:0.6,ease:"none"}},{T[1]+2.0+i*0.9:.2f});\n'
        return body, "", js
    s = Scene("cxdone", lines, build, lead=0.4, tail=1.4, min_hold={0: 3.4, 1: 5.6})
    s.sfx = [(("T", 0, 1.9), "chime.mp3", 0.22), (("T", 1, 0.6), "click-soft.mp3", 0.3)]
    return s


def cx_g1():
    return ghinho("g1", 1, [
        (ic_pallet(), "LPN in sẵn, <b>mỗi pallet dán 1 LPN</b>", "LPN in sẵn, mỗi pallet dán 1 LPN"),
        (IC_PDA, "Nhận hàng: quét LPN → quét mã hàng → nhập số lượng → nhập <b>date / batch</b>",
         "Nhận hàng: quét LPN, quét mã hàng, nhập số lượng, nhập date batch"),
        (ic_forklift(), "Putaway: quét LPN → xe nâng đưa tới <b>vị trí gợi ý</b> → quét vị trí xác nhận",
         "Putaway: quét LPN, xe nâng đưa tới vị trí gợi ý, quét vị trí xác nhận"),
    ])


# ============================================================ CHƯƠNG 2 – Lấy hàng gộp theo xe
def office(P, label=True):
    return (desk_svg(300) + printer_svg(P + "-pr", 620)
            + figure(P + "-xl", "xlct", 300, FY - 40, scale=1.5, label=label, pose={"armL": (22, -70), "armR": (-22, 70)}))


def do_card(cid, num, store, x=None, y=None, hidden=True):
    pos = f"position:absolute;left:{x}px;top:{y}px;" if x is not None else ""
    op = "opacity:0;" if hidden else ""
    return (f'<div id="{cid}" style="{pos}{op}width:330px;background:#fff;border:4px solid {INK};border-left:14px solid {C["blue"]};border-radius:14px;padding:8px 16px;margin-bottom:12px">'
            f'<div style="font-size:34px;font-weight:900">{num}</div><div style="font-size:26px;font-weight:700;color:{C["muted"]}">{store} · XE-01</div></div>')


DOS = [("DO-1001", "CH-0125"), ("DO-1002", "CH-0311"), ("DO-1003", "CH-0420")]


def cx_do():
    lines = ["Với hàng xuất, XLCT nhận file kế hoạch xuất DO và xử lý cho đúng định dạng WMS.",
             "Import file vào WMS để tạo các DO."]

    def build(T, D):
        P = "c21"
        body = svg_layer(st.floor() + office(P))
        body += sheet(f"{P}-sheet", 960, 170, "Kế hoạch xuất (DO).xlsx", ["Số DO", "Cửa hàng", "Giao bằng"],
                      [(d, s, "XE-01") for d, s in DOS], cw=260)
        body += (f'<div id="{P}-okfmt" class="abs" style="left:1120px;top:500px;opacity:0"><div style="display:flex;align-items:center;gap:12px;background:#fff;border:5px solid {C["green"]};'
                 f'border-radius:18px;padding:10px 24px;font-size:36px;font-weight:900">{st.check(46)}Đúng định dạng WMS</div></div>')
        inner = (f'<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px">{btn(P + "-imp", "Import file")}'
                 f'<div style="font-size:24px;font-weight:700;color:{C["muted"]}">Kế hoạch xuất (DO).xlsx</div></div>'
                 + "".join(do_card(f"{P}-d{i}", d, s) for i, (d, s) in enumerate(DOS)))
        body += win(f"{P}-wms", 1060, 140, 560, "WMS · Xuất hàng", inner)
        body += st.badge(f"{P}-b1", 1, "Nhận kế hoạch xuất") + st.badge(f"{P}-b2", 2, "Nhập vào WMS")
        js = st.badge_seq_js([f"{P}-b1", f"{P}-b2"], [T[0], T[1]], D - 0.4) + lab_js(f"{P}-xl", 0.3)
        js += st.appear_js(f"#{P}-sheet", T[0] + 0.2, 0.35, dy=20)
        for i, o in enumerate([30, -22, 12]):
            js += f'tl.fromTo("#{P}-sheet-r{i}",{{x:{o}}},{{x:0,duration:0.45,ease:"back.out(1.6)"}},{T[0]+1.8+i*0.25:.2f});\n'
        js += st.stamp_js(f"{P}-okfmt", T[0] + 2.9)
        js += hide_js(f"#{P}-okfmt", T[1] - 0.1) + hide_js(f"#{P}-sheet", T[1])
        js += st.appear_js(f"#{P}-wms", T[1] + 0.1, 0.3) + press_js(f"#{P}-imp", T[1] + 0.6)
        for i in range(3):
            js += st.appear_js(f"#{P}-d{i}", T[1] + 1.0 + i * 0.35, 0.3, dy=14)
        return body, "", js
    s = Scene("cxdo", lines, build, lead=0.5, tail=1.4, min_hold={0: 5.0, 1: 3.6})
    s.sfx = [(("T", 0, 2.9), "chime.mp3", 0.22)]
    return s


def cx_master():
    lines = ["Các DO giao cùng một xe được gom lại thành một lệnh xuất gộp.",
             "Một xe là một Master DO."]

    def build(T, D):
        P = "c23"
        X0, Y0 = 160, [230, 380, 530]
        FXX, FY0 = 960, 230
        frame = (f'<div id="{P}-fr" class="abs" style="left:{FXX}px;top:{FY0}px;width:760px;height:470px;background:#F7FAFF;border:6px dashed {C["blue"]};border-radius:26px;opacity:0">'
                 f'<div style="position:relative;height:84px;border-bottom:4px dashed {C["blue"]}">'
                 f'<div id="{P}-h1" class="abs" style="left:26px;top:14px;font-size:44px;font-weight:900">Xe XE-01</div>'
                 f'<div id="{P}-h2" class="abs" style="left:26px;top:14px;font-size:44px;font-weight:900;color:{C["blue"]};opacity:0">MDO-0001 · Xe XE-01</div>'
                 f'<svg class="abs" style="right:26px;top:16px" width="120" height="60" viewBox="0 -240 400 250">{st.truck(P + "-tk")}</svg></div></div>')
        body = frame + "".join(do_card(f"{P}-d{i}", d, s, X0, Y0[i]) for i, (d, s) in enumerate(DOS))
        body += (f'<div id="{P}-eq" class="abs" style="left:960px;top:96px;opacity:0"><div style="display:flex;align-items:center;gap:16px;background:{C["orange"]};border:5px solid {INK};'
                 f'border-radius:20px;padding:10px 28px;font-size:46px;font-weight:900">1 xe = 1 Master DO</div></div>')
        body += st.badge(f"{P}-b3", 3, "Tạo lệnh xuất gộp")
        js = st.badge_seq_js([f"{P}-b3"], [T[0]], D - 0.4)
        for i in range(3):
            js += st.appear_js(f"#{P}-d{i}", 0.2 + i * 0.2, 0.3, dy=14)
        js += f'tl.fromTo("#{P}-fr",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.6)"}},{T[0]+0.4:.2f});\n'
        for i in range(3):
            ty = FY0 + 104 + i * 112
            js += f'tl.to("#{P}-d{i}",{{x:{FXX + 40 - X0},y:{ty - Y0[i]},duration:0.7,ease:"power2.inOut"}},{T[0]+1.4+i*0.4:.2f});\n'
        js += hide_js(f"#{P}-h1", T[1] - 0.1) + show_js(f"#{P}-h2", T[1])
        js += f'tl.to("#{P}-fr",{{borderStyle:"solid",duration:0.01}},{T[1]:.2f});\n'
        js += f'tl.fromTo("#{P}-eq",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.35,ease:"power3.out"}},{T[1]+0.2:.2f});\n'
        return body, "", js
    s = Scene("cxmaster", lines, build, lead=0.5, tail=1.4, min_hold={0: 3.6, 1: 3.2})
    s.sfx = [(("T", 1, 0.2), "chime.mp3", 0.22)]
    return s


def cx_alloc():
    lines = ["Hệ thống chạy phân bổ để tìm tồn, theo FIFO hoặc FEFO."]

    def build(T, D):
        P = "c24"
        svg = arrow_defs(P, C["orange"])
        tgt = []
        for i, z in enumerate(("dong", "chill", "kho")):
            fill, edge, lab = ZONE[z]
            x = 780 + i * 370
            svg += (f'<rect x="{x}" y="200" width="330" height="360" rx="20" fill="{fill}" stroke="{edge}" stroke-width="5"/>'
                    f'<text x="{x+165}" y="250" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="34" fill="{INK}">KHU {lab}</text>'
                    + zone_icon(z, x + 290, 236, 0.7))
            for r in range(3):
                for c in range(3):
                    sx, sy = x + 30 + c * 95, 290 + r * 85
                    svg += f'<rect x="{sx}" y="{sy}" width="80" height="62" rx="8" fill="#fff" stroke="{edge}" stroke-width="3"/>'
            hx, hy = x + 30 + (i % 3) * 95, 290 + (2 - i) * 85
            svg += f'<rect id="{P}-hl{i}" x="{hx}" y="{hy}" width="80" height="62" rx="8" fill="{C["orange"]}" stroke="{INK}" stroke-width="4" opacity="0"/>'
            tgt.append((hx + 40, hy))
        for i, (tx, ty) in enumerate(tgt):
            svg += arrow(f"{P}-a{i}", f"M640,450 C{(640+tx)/2:.0f},{560 - i*40} {tx},{ty+180} {tx},{ty+70}", P, C["orange"], 7, 1200)
        body = svg_layer(svg)
        body += win(f"{P}-mdo", 110, 300, 540, "WMS · MDO-0001",
                    f'<div style="font-size:30px;font-weight:700;margin-bottom:18px">Xe XE-01 · 3 DO</div>{btn(P + "-go", "PHÂN BỔ", C["blue"])}', hidden=False)
        body += (f'<div id="{P}-rule" class="abs" style="left:780px;top:600px;opacity:0;display:flex;gap:18px">'
                 f'<div style="background:#fff;border:4px solid {INK};border-radius:16px;padding:10px 22px"><div style="font-size:36px;font-weight:900">FIFO</div><div style="font-size:26px;font-weight:700">Nhập trước, xuất trước</div></div>'
                 f'<div style="background:#fff;border:4px solid {INK};border-radius:16px;padding:10px 22px"><div style="font-size:36px;font-weight:900">FEFO</div><div style="font-size:26px;font-weight:700">Hết hạn trước, xuất trước</div></div></div>')
        body += st.badge(f"{P}-b4", 4, "Phân bổ tồn kho")
        js = st.badge_seq_js([f"{P}-b4"], [T[0]], D - 0.4)
        js += press_js(f"#{P}-go", T[0] + 0.8)
        for i in range(3):
            js += draw_js(f"#{P}-a{i}", T[0] + 1.1 + i * 0.3, 0.6) + st.pop_js(f"#{P}-hl{i}", T[0] + 1.6 + i * 0.3)
        js += st.appear_js(f"#{P}-rule", T[0] + 2.8)
        return body, "", js
    s = Scene("cxalloc", lines, build, lead=0.5, tail=1.8, min_hold={0: 5.0})
    s.sfx = [(("T", 0, 0.8), "click-soft.mp3", 0.3)]
    return s


def cx_picklist():
    lines = ["Khi in Picklist, có thể chọn một hoặc nhiều Master DO để lấy cùng lúc.",
             "Số lượng được gộp tổng theo mã hàng,",
             "và hiện theo thùng cộng lẻ: năm mươi lăm hũ, quy cách năm mươi, là một thùng năm hũ.",
             "Picklist được tách và in riêng cho từng khu: đông, chill và khô."]

    def build(T, D):
        P = "c25"
        body = svg_layer(st.floor() + office(P, label=False))
        box = "display:inline-flex;width:40px;height:40px;border:4px solid #1B2430;border-radius:8px;align-items:center;justify-content:center;font-size:30px;font-weight:900;color:#fff;margin-right:16px"
        mrow = lambda i, t, sub: (f'<div style="display:flex;align-items:center;border:3px solid #E3E8EF;border-radius:12px;padding:12px 16px;margin-bottom:12px">'
                                  f'<span id="{P}-cb{i}" style="{box};background:#fff"></span><div><div style="font-size:32px;font-weight:900">{t}</div>'
                                  f'<div style="font-size:24px;font-weight:700;color:{C["muted"]}">{sub}</div></div></div>')
        pA = (mrow(0, "MDO-0001 · XE-01", "3 DO") + mrow(1, "MDO-0002 · XE-02", "2 DO") + mrow(2, "MDO-0003 · XE-03", "4 DO")
              + f'<div style="font-size:26px;font-weight:700;color:{C["blue"]}">Chọn 1 hoặc nhiều Master DO lấy cùng lúc</div>')
        body += win(f"{P}-wa", 1000, 130, 720, "WMS · In Picklist", pA)
        drows = [("DO-1001", "20 hũ"), ("DO-1002", "30 hũ"), ("DO-1003", "5 hũ")]
        pB = (f'<div style="font-size:30px;font-weight:900;margin-bottom:8px">SKU 2001 · Sữa chua</div>'
              + "".join(f'<div id="{P}-q{i}" style="display:flex;justify-content:space-between;font-size:32px;font-weight:700;border-top:2px solid #E3E8EF;padding:10px 0;opacity:0">'
                        f'<span>{a}</span><b>{b}</b></div>' for i, (a, b) in enumerate(drows))
              + f'<div id="{P}-tot" style="display:flex;justify-content:space-between;font-size:40px;font-weight:900;border-top:5px solid {INK};padding:12px 0;opacity:0">'
                f'<span>Tổng</span><span style="color:#C45A00">55 hũ</span></div>')
        body += win(f"{P}-wb", 1000, 130, 720, "Gộp theo mã hàng", pB)
        carton = f'<svg width="120" height="96" viewBox="0 0 120 96"><rect x="6" y="6" width="108" height="84" rx="4" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="4"/><rect x="50" y="6" width="20" height="84" fill="#F3DDB5"/></svg>'
        cupsv = f'<svg width="140" height="60" viewBox="0 0 140 60">{cups(P + "-cc", 8, 56, 5, hidden=False).replace("<g ", "<g transform=" + chr(34) + "scale(1.2)" + chr(34) + " ")}</svg>'
        pC = (f'<div style="display:flex;align-items:center;gap:22px;justify-content:center">'
              f'<div id="{P}-e0" style="font-size:64px;font-weight:900;opacity:0">55 hũ</div><div id="{P}-e1" style="font-size:64px;font-weight:900;opacity:0">=</div>'
              f'<div id="{P}-e2" style="text-align:center;opacity:0">{carton}<div style="font-size:34px;font-weight:900">1 thùng</div></div>'
              f'<div id="{P}-e3" style="font-size:64px;font-weight:900;opacity:0">+</div>'
              f'<div id="{P}-e4" style="text-align:center;opacity:0">{cupsv}<div style="font-size:34px;font-weight:900;margin-top:30px">5 hũ</div></div></div>'
              f'<div id="{P}-e5" style="text-align:center;font-size:30px;font-weight:700;color:{C["muted"]};margin-top:18px;opacity:0">Quy cách: 50 hũ = 1 thùng</div>')
        body += win(f"{P}-wc", 960, 160, 800, "Hiện số thùng + lẻ", pC)
        papers = ""
        for i, z in enumerate(("dong", "chill", "kho")):
            fill, edge, lab = ZONE[z]
            papers += paper(f"{P}-p{i}", 520, 470, f"Picklist {lab}", 250, 180, edge, head=edge)
        body += papers
        body += pill(f"{P}-plab", 1020, 600, "Picklist giấy (theo khu)", "#fff", size=36)
        body += st.badge(f"{P}-b5", 5, "In Picklist")
        js = st.badge_seq_js([f"{P}-b5"], [T[0]], D - 0.4)
        js += st.appear_js(f"#{P}-wa", T[0] + 0.2, 0.3)
        for i in (0, 1):
            js += f'tl.to("#{P}-cb{i}",{{background:"{C["green"]}",duration:0.15}},{T[0]+1.4+i*0.7:.2f});\n'
            js += f'tl.set("#{P}-cb{i}",{{innerHTML:"✓"}},{T[0]+1.4+i*0.7:.2f});\n'
        js += hide_js(f"#{P}-wa", T[1] - 0.1) + st.appear_js(f"#{P}-wb", T[1], 0.3)
        for i in range(3):
            js += st.appear_js(f"#{P}-q{i}", T[1] + 0.5 + i * 0.4, 0.25, dy=10)
        js += st.pop_js(f"#{P}-tot", T[1] + 1.9)
        js += hide_js(f"#{P}-wb", T[2] - 0.1) + st.appear_js(f"#{P}-wc", T[2], 0.3)
        for i, dt in enumerate([0.5, 2.2, 2.6, 3.4, 3.8, 4.6]):
            js += st.pop_js(f"#{P}-e{i}", T[2] + dt, 0.3)
        js += hide_js(f"#{P}-wc", T[3] - 0.1)
        for i in range(3):
            t = T[3] + 0.4 + i * 0.6
            js += f'tl.fromTo("#{P}-p{i}",{{opacity:0,x:0,y:0,scale:0.4}},{{opacity:1,x:{440 + i*300},y:-200,scale:1,duration:0.6,ease:"power2.out",transformOrigin:"50% 100%"}},{t:.2f});\n'
        js += st.appear_js(f"#{P}-plab", T[3] + 2.4)
        return body, "", js
    s = Scene("cxpick5", lines, build, lead=0.5, tail=1.6, min_hold={0: 4.4, 1: 3.4, 2: 6.4, 3: 5.0})
    s.sfx = [(("T", 3, 0.4), "click-soft.mp3", 0.3)]
    return s


def picklist_html(pid, x, y, w=860, scale_rows=True):
    fill, edge, lab = ZONE["chill"]
    cols = [("Vị trí", 210), ("Mã hàng", 290), ("Cần lấy", 200), ("Thực lấy", 160)]
    cell = "display:inline-block;padding:8px 10px;font-size:26px;font-weight:700;box-sizing:border-box;border-right:2px solid #D5DBE4;vertical-align:middle"
    rows = [("CHILL-A02-01", "SKU 2001 Sữa chua", "1 thùng 5 hũ"), ("CHILL-A03-01", "SKU 2002 Sữa tươi", "2 thùng")]
    out = (f'<div id="{pid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;background:#fff;border:4px solid {INK};border-radius:6px;overflow:hidden;opacity:0;box-shadow:0 10px 0 rgba(27,36,48,.10)">'
           f'<div style="background:{fill};border-bottom:4px solid {edge};padding:10px 16px;font-size:30px;font-weight:900">PICKLIST – KHU {lab} · MDO-0001</div>'
           f'<div style="white-space:nowrap;background:#F4F6F9">' + "".join(f'<span style="{cell};width:{cw}px;font-weight:900">{c}</span>' for c, cw in cols) + '</div>')
    for i, r in enumerate(rows):
        out += (f'<div id="{pid}-row{i}" style="white-space:nowrap;border-top:2px solid #D5DBE4;position:relative">'
                + "".join(f'<span style="{cell};width:{cols[k][1]}px">{v}</span>' for k, v in enumerate(r))
                + f'<span style="{cell};width:{cols[3][1]}px;border-right:none"><span id="{pid}-w{i}" style="display:inline-block;opacity:0;color:{HANDW};font-style:italic;font-weight:900;font-size:30px">'
                + ("1 thùng 5" if i == 0 else "") + '</span></span>'
                + f'<div id="{pid}-hl{i}" class="abs" style="left:0;top:0;right:0;bottom:0;border:5px solid {C["orange"]};opacity:0"></div></div>')
    return out + '</div>'


def cx_pick():
    lines = ["Picker cầm Picklist của khu mình, đến đúng vị trí,",
             "lấy đúng số thùng và số lẻ, rồi ghi số lượng thực lấy lên Picklist.",
             "Lấy xong, đưa hàng về khu chia và nộp Picklist cho XLCT."]

    def build(T, D):
        P = "c26"
        R = ZRack(P + "r", 1000, "chill", cols=3, levels=3, cw=260, lh=200)
        rack = R.svg(contents={(c, 0): "cartons" for c in range(3)} | {(0, 1): "pallet", (1, 1): "pallet", (2, 2): "pallet"})
        sx, sb = R.slot(1, 0)
        X0, X1 = 240, sx - 230
        SC = 1.5
        pk = (f'<g transform="translate({X0},{FY})"><g id="{P}-mv">{st.trolley_behind(P + "-tr", "MDO-0001")}'
              + cups(P + "-cups", -126, -28, 3) + cups(P + "-cups2", -126, -28 - 0, 0)
              + f'<g transform="translate(36,0)">{stick(P + "-pk", "picker", SC, label=True, hand_r=clipboard(P + "-pk"))}</g></g></g>')
        sign = (f'<g id="{P}-sign" opacity="0"><rect x="1560" y="520" width="300" height="70" rx="14" fill="#FFF3E4" stroke="{C["orange"]}" stroke-width="5"/>'
                f'<text x="1710" y="567" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="34" fill="{INK}">→ KHU CHIA</text></g>')
        hl = f'<rect id="{P}-slot" x="{sx-R.cw/2+8}" y="{sb-R.lh+34}" width="{R.cw-16}" height="{R.lh-30}" rx="8" fill="none" stroke="{C["orange"]}" stroke-width="8" opacity="0"/>'
        qty = (f'<g id="{P}-qa" opacity="0"><rect x="{sx-110}" y="{sb-300}" width="220" height="64" rx="32" fill="{C["orange"]}" stroke="{INK}" stroke-width="4"/>'
               f'<text x="{sx}" y="{sb-256}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="34" fill="{INK}">1 thùng</text></g>'
               f'<g id="{P}-qb" opacity="0"><rect x="{sx-110}" y="{sb-300}" width="220" height="64" rx="32" fill="{C["orange"]}" stroke="{INK}" stroke-width="4"/>'
               f'<text x="{sx}" y="{sb-256}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="34" fill="{INK}">+ 5 hũ</text></g>')
        body = svg_layer(st.floor() + rack + zone_banner(P + "-zb", "chill", 1000, 120, 780) + hl + pk + qty)
        body += picklist_html(f"{P}-pl", 60, 170)
        body += pill(f"{P}-sub", 1380, 40, "Nộp Picklist cho XLCT ✔", "#fff", border=C["green"], size=32)
        body += st.badge(f"{P}-b6", 6, "Lấy hàng (giấy)") + st.badge(f"{P}-b7", 7, "Đưa về khu chia")
        js = st.badge_seq_js([f"{P}-b6", f"{P}-b7"], [T[0], T[2]], D - 0.4)
        js += lab_js(f"{P}-pk", 0.3)
        js += f'tl.fromTo("#{P}-pl",{{opacity:0,y:20,rotation:-2}},{{opacity:1,y:0,rotation:0,duration:0.4,ease:"power2.out"}},{T[0]+0.1:.2f});\n'
        js += show_js(f"#{P}-pl-hl0", T[0] + 0.8, 0.2)
        js += lab_off(f"{P}-pk", T[0] + 0.9)
        js += walk_to(f"{P}-pk", f"{P}-mv", X1 - X0, T[0] + 0.9, 2.2)
        js += show_js(f"#{P}-slot", T[0] + 2.8, 0.2)
        t = T[1]
        js += pose_js(f"{P}-pk", t + 0.1, {"armL": (110, -20)}, dur=0.3)
        js += st.pop_js(f"#{P}-qa", t + 0.4) + st.pop_js(f"#{P}-tr-k0", t + 0.8, 0.3) + hide_js(f"#{P}-qa", t + 1.4)
        js += st.pop_js(f"#{P}-qb", t + 1.5) + st.pop_js(f"#{P}-cups", t + 1.9, 0.3) + hide_js(f"#{P}-qb", t + 2.5)
        js += pose_js(f"{P}-pk", t + 2.6, REST, dur=0.3)
        js += write_js(f"#{P}-pl-w0", t + 3.0, 0.9) + hide_js(f"#{P}-slot", t + 3.0)
        js += hide_js(f"#{P}-pl-hl0", T[2] - 0.1)
        js += walk_to(f"{P}-pk", f"{P}-mv", 2200 - X0, T[2] + 0.4, 3.0)
        js += f'tl.to("#{P}-pl",{{x:1480,y:-100,scale:0.25,opacity:0,duration:0.7,ease:"power2.in",transformOrigin:"0% 0%"}},{T[2]+1.6:.2f});\n'
        js += st.appear_js(f"#{P}-sub", T[2] + 2.2)
        return body, "", js
    s = Scene("cxpick", lines, build, lead=0.5, tail=1.6, min_hold={0: 3.6, 1: 5.4, 2: 4.4})
    s.sfx = [(("T", 1, 0.8), "click-soft.mp3", 0.3), (("T", 2, 2.2), "chime.mp3", 0.2)]
    return s


def cx_confirm():
    lines = ["XLCT nhập số lượng thực lấy vào WMS để xác nhận."]

    def build(T, D):
        P = "c28"
        body = svg_layer(st.floor() + office(P, label=False))
        body += picklist_html(f"{P}-pl", 60, 170, w=860)
        inner = (f'<div style="font-size:28px;font-weight:700;color:{C["muted"]}">MDO-0001 · Khu Chill</div>'
                 f'<div style="font-size:34px;font-weight:900;margin:6px 0 4px">SKU 2001 · Sữa chua</div>'
                 f'<div style="font-size:28px;font-weight:700">Cần lấy: 1 thùng 5 hũ</div>'
                 f'<div style="font-size:26px;font-weight:700;color:{C["muted"]};margin-top:14px">Thực lấy</div>'
                 f'<div style="border:4px solid {C["orange"]};background:#FFF7EE;border-radius:14px;padding:10px 16px;font-size:36px;font-weight:900;min-height:64px;margin-bottom:16px">'
                 f'<span id="{P}-t" style="display:inline-block;opacity:0">1 thùng 5 hũ</span></div>{btn(P + "-go", "XÁC NHẬN")}')
        body += win(f"{P}-w", 1100, 160, 660, "WMS · Xác nhận lấy hàng", inner)
        body += st.stamp(f"{P}-ok", "Đã xác nhận lấy hàng", x=1130, y=640)
        body += svg_layer(arrow_defs(P) + arrow(f"{P}-a", "M924,330 C1000,340 1030,430 1100,470", P, width=7, dash=500))
        body += st.badge(f"{P}-b8", 8, "Xác nhận lấy hàng")
        js = st.badge_seq_js([f"{P}-b8"], [T[0]], D - 0.4)
        js = st.badge_seq_js([f"{P}-b8"], [T[0]], D - 0.4) + st.appear_js(f"#{P}-pl", 0.2)
        js += f'tl.set("#{P}-pl-w0",{{opacity:1}},0);\n' + show_js(f"#{P}-pl-hl0", T[0] + 0.3, 0.2)
        js += st.appear_js(f"#{P}-w", T[0] + 0.4) + draw_js(f"#{P}-a", T[0] + 1.0, 0.6)
        js += write_js(f"#{P}-t", T[0] + 1.6, 0.8) + press_js(f"#{P}-go", T[0] + 2.9) + st.stamp_js(f"{P}-ok", T[0] + 3.2)
        return body, "", js
    s = Scene("cxconfirm", lines, build, lead=0.5, tail=1.6, min_hold={0: 4.6})
    s.sfx = [(("T", 0, 3.2), "chime.mp3", 0.22)]
    return s


def cx_g2():
    return ghinho("g2", 2, [
        (ic_truck(), "<b>1 xe = 1 Master DO</b>, có thể lấy nhiều Master DO cùng lúc", "1 xe = 1 Master DO, có thể lấy nhiều Master DO cùng lúc"),
        (IC_DOC, "Picklist gộp theo mã hàng, hiện <b>thùng + lẻ</b>, tách theo khu Đông / Chill / Khô",
         "Picklist gộp theo mã hàng, hiện thùng và lẻ, tách theo khu"),
        (IC_PEN, "Ghi <b>số thực lấy</b> lên giấy, XLCT nhập lại vào WMS", "Ghi số thực lấy lên giấy, XLCT nhập lại vào WMS"),
    ])


# ============================================================ CHƯƠNG 3 – Chia hàng theo DO
def cx_cells():
    lines = ["Tại khu chia, mỗi DO của xe có một ô riêng, ghi số DO lên từng ô."]

    def build(T, D):
        P = "c31"
        xs = [700, 1080, 1460]
        cells = "".join(cell_svg(f"{P}-c{i}", x, d) for i, (x, (d, _)) in enumerate(zip(xs, DOS)))
        pk = (f'<g transform="translate(300,{FY})"><g id="{P}-mv">{st.trolley_behind(P + "-tr", "MDO-0001")}'
              f'<g transform="translate(36,0)">{stick(P + "-pk", "picker", 1.5)}</g></g></g>')
        head = (f'<g><rect x="560" y="150" width="1040" height="76" rx="18" fill="#FFF3E4" stroke="{C["orange"]}" stroke-width="5"/>'
                f'<text x="1080" y="202" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="38" fill="{INK}">KHU CHIA · XE-01 / MDO-0001</text></g>')
        body = svg_layer(st.floor() + head + cells + pk)
        body += st.badge(f"{P}-b1", 1, "Chuẩn bị khu chia")
        js = st.badge_seq_js([f"{P}-b1"], [T[0]], D - 0.4)
        js += "".join(f'tl.set("#{P}-c{i}-sign",{{opacity:0}},0);\n' for i in range(3))
        js += walk_to(f"{P}-pk", f"{P}-mv", 1300, T[0] + 0.2, 4.0)
        for i, x in enumerate(xs):
            js += st.pop_js(f"#{P}-c{i}-sign", T[0] + 0.2 + 4.0 * (x - 120 - 300) / 1300)
        return body, "", js
    s = Scene("cxcells", lines, build, lead=0.4, tail=1.2, min_hold={0: 5.0})
    return s


def cx_sort():
    lines = ["Trên PDA, chọn xe hoặc Master DO, rồi quét mã vạch hàng.",
             "Hệ thống chỉ DO và số lượng cần đặt, theo thùng và số lẻ.",
             "Đặt hàng vào đúng ô DO rồi xác nhận.",
             "Chưa chia hết thì quét tiếp."]

    def build(T, D):
        P = "c32"
        xs = [600, 880, 1160]
        loads = [cups("x", 0, 0, 0)] * 3
        qtys = ["20 hũ", "30 hũ", "5 hũ"]
        cells = ""
        for i, (x, (d, _)) in enumerate(zip(xs, DOS)):
            n = [4, 5, 2][i]
            ld = cups(f"{P}-cl{i}", x - n * 11, FY - 4, n, hidden=False)
            cells += cell_svg(f"{P}-c{i}", x, d, w=230, load=ld, qty=qtys[i])
        pile = (f'<g id="{P}-pile">' + st.carton(130, FY - 56, 74, 56) + cups(P + "-pc", 210, FY - 2, 5, hidden=False)
                + cups(P + "-pc2", 210, FY - 32, 4, hidden=False) + '</g>')
        cnt = "".join(f'<g id="{P}-n{i}" opacity="{1 if i == 0 else 0}"><rect x="120" y="{FY-150}" width="200" height="50" rx="25" fill="{INK}"/>'
                      f'<text x="220" y="{FY-115}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="28" fill="#fff">Còn {v}</text></g>'
                      for i, v in enumerate(["55 hũ", "25 hũ", "5 hũ", "0 hũ"]))
        RX, SC = 400, 1.5
        a, b = SCAN["armR"]
        tip = hand(RX, FY, SC, a, b, flip=True, extra=56)
        pk = (f'<g transform="translate({RX},{FY})"><g id="{P}-mv">{mirrored(P + "-pk", "picker", SC, pose=SCAN, hand_r=pda_svg(P + "-pk"))}</g></g>')
        las = st.laser(f"{P}-las", tip[0], tip[1], 250, FY - 30)
        dm = diamond(f"{P}-dm", 880, 200, "Đã chia hết hàng?", 520, 150, 32)
        body = svg_layer(st.floor() + cells + pile + cnt + pk + las + dm)
        body += pill(f"{P}-no", 1160, 170, "Không → quét tiếp", "#fff", border=C["orange"], size=30)
        body += pill(f"{P}-yes", 1160, 170, "Có ✔", C["green"], txt="#fff", size=30)
        p1 = ('<div class="lbl">Chọn xe / Master DO</div><div class="row sel"><b>XE-01 · MDO-0001</b></div><div class="row">XE-02 · MDO-0002</div>')
        p2 = kv("Quét mã vạch hàng", "SKU 2001 ✔", "Sữa chua")
        p3 = (kv("Đặt vào ô", "DO-1002", "", "#C45A00") + f'<div style="margin-top:18px">{kv("Số lượng", "30 hũ", "0 thùng + 30 hũ lẻ")}</div>')
        p4 = (kv("Đã đặt vào ô", "DO-1002 ✔", "30 hũ") + f'<div id="{P}-go" class="go">XÁC NHẬN</div>')
        body += st.pda(f"{P}-pda", "Chia hàng", [("s1", p1), ("s2", p2), ("s3", p3), ("s4", p4)])
        body += st.badge(f"{P}-b2", 2, "Chia hàng")
        js = st.badge_seq_js([f"{P}-b2"], [T[0]], D - 0.4) + lab_js(f"{P}-pk", 0.3)
        js += "".join(f'tl.set("#{P}-c{i}-load",{{opacity:0}},0);\n' for i in range(3))
        js += st.appear_js(f"#{P}-pda", T[0], 0.35, dy=30) + st.show_panel_js(f"{P}-pda", None, "s1", T[0] + 0.1)
        js += st.show_panel_js(f"{P}-pda", "s1", "s2", T[0] + 2.4) + st.laser_js(f"{P}-las", T[0] + 2.6)
        js += st.show_panel_js(f"{P}-pda", "s2", "s3", T[1]) + show_js(f"#{P}-c1-hl", T[1] + 0.4)
        js += lab_off(f"{P}-pk", T[2] - 0.2)
        js += walk_to(f"{P}-pk", f"{P}-mv", 880 - 130 - RX, T[2], 1.4)
        js += st.pop_js(f"#{P}-c1-load", T[2] + 1.5) + hide_js(f"#{P}-n0", T[2] + 1.5, 0.1) + show_js(f"#{P}-n1", T[2] + 1.6, 0.1)
        js += st.show_panel_js(f"{P}-pda", "s3", "s4", T[2] + 1.7) + press_js(f"#{P}-go", T[2] + 2.4) + hide_js(f"#{P}-c1-hl", T[2] + 2.4)
        js += f'tl.fromTo("#{P}-dm",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power2.out"}},{T[3]:.2f});\n'
        js += st.appear_js(f"#{P}-no", T[3] + 0.4)
        js += st.pop_js(f"#{P}-c0-load", T[3] + 1.2) + hide_js(f"#{P}-n1", T[3] + 1.2, 0.1) + show_js(f"#{P}-n2", T[3] + 1.3, 0.1)
        js += st.pop_js(f"#{P}-c2-load", T[3] + 2.0) + hide_js(f"#{P}-n2", T[3] + 2.0, 0.1) + show_js(f"#{P}-n3", T[3] + 2.1, 0.1)
        js += hide_js(f"#{P}-pile", T[3] + 2.1)
        js += hide_js(f"#{P}-no", T[3] + 2.6) + st.pop_js(f"#{P}-yes", T[3] + 2.7)
        return body, "", js
    s = Scene("cxsort", lines, build, lead=0.4, tail=1.6, min_hold={0: 4.2, 1: 3.6, 2: 3.4, 3: 4.2})
    s.sfx = [(("T", 0, 2.6), "ping.mp3", 0.25), (("T", 3, 2.7), "chime.mp3", 0.22)]
    return s


def cx_diff():
    lines = ["Chia xong, kiểm tra có thiếu hay thừa hàng không.",
             "Nếu có chênh lệch, quản lý kho xử lý thủ công, không có báo cáo trên WMS.",
             "Thiếu thì lấy bổ sung hoặc điều chỉnh DO.",
             "Thừa thì trả hàng về vị trí."]

    def build(T, D):
        P = "c33"
        dx, dy = 430, 380
        svg = (arrow_defs(P) + diamond(f"{P}-dm", dx, dy, "Có thiếu /\nthừa hàng?", 440, 250)
               + arrow(f"{P}-ano", f"M{dx},{dy+125} L{dx},{dy+225}", P)
               + arrow(f"{P}-ayes", f"M{dx+220},{dy} L{dx+330},{dy}", P))
        body = svg_layer(st.floor() + svg + figure(P + "-mg", "manager", 1740, scale=1.5, label=True, hand_r=clipboard(P + "-mg")))
        body += pill(f"{P}-lno", 460, 520, "Không", "#fff", size=30) + pill(f"{P}-lyes", 640, 300, "Có", C["orange"], size=30)
        body += pill(f"{P}-end", 300, 620, "Kết thúc ✔", C["green"], txt="#fff", size=34)
        red, ora = "#FDECEC", "#FFF2E0"
        inner = (f'<div style="font-size:26px;font-weight:700;color:{C["muted"]};margin-bottom:10px">Kiểm đếm tại khu chia · MDO-0001 · XE-01</div>'
                 f'<div style="border:4px solid {C["red"]};background:{red};border-radius:14px;padding:10px 16px;margin-bottom:10px">'
                 f'<div style="font-size:30px;font-weight:900">DO-1003 · SKU 1001 Há cảo</div><div style="font-size:30px;font-weight:900;color:{C["red"]}">Thiếu 2 gói</div>'
                 f'<div id="{P}-o1" style="display:flex;gap:12px;margin-top:8px;opacity:0"><span style="background:#fff;border:3px solid {INK};border-radius:12px;padding:4px 14px;font-size:26px;font-weight:900">Lấy bổ sung</span>'
                 f'<span style="font-size:26px;font-weight:900;padding-top:6px">hoặc</span><span style="background:#fff;border:3px solid {INK};border-radius:12px;padding:4px 14px;font-size:26px;font-weight:900">Điều chỉnh DO</span></div></div>'
                 f'<div style="border:4px solid {C["orange"]};background:{ora};border-radius:14px;padding:10px 16px">'
                 f'<div style="font-size:30px;font-weight:900">DO-1001 · SKU 3001 Bánh quy</div><div style="font-size:30px;font-weight:900;color:#C45A00">Thừa 1 hộp</div>'
                 f'<div id="{P}-o2" style="display:flex;gap:12px;margin-top:8px;opacity:0"><span style="background:#fff;border:3px solid {INK};border-radius:12px;padding:4px 14px;font-size:26px;font-weight:900">Trả về vị trí KHÔ-A02-01</span></div></div>')
        body += win(f"{P}-w", 780, 120, 760, "Xử lý thủ công tại khu chia", inner, color="#C45A00")
        body += (f'<div id="{P}-nowms" class="abs" style="left:800px;top:600px;opacity:0"><div style="display:flex;align-items:center;gap:16px;background:#fff;'
                 f'border:5px solid {C["red"]};border-radius:18px;padding:8px 22px">'
                 f'<svg width="96" height="56" viewBox="0 0 96 56"><rect x="4" y="4" width="88" height="48" rx="8" fill="#EAF1FC" stroke="{INK}" stroke-width="3"/>'
                 f'<text x="48" y="37" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="22" fill="{C["blue"]}">WMS</text>'
                 f'<line x1="4" y1="54" x2="92" y2="2" stroke="{C["red"]}" stroke-width="7" stroke-linecap="round"/></svg>'
                 f'<span style="font-size:34px;font-weight:900">Không có báo cáo trên WMS</span></div></div>')
        body += st.badge(f"{P}-b3", 3, "Xử lý chênh lệch")
        js = f'tl.fromTo("#{P}-dm",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{T[0]:.2f});\n'
        js += draw_js(f"#{P}-ano", T[0] + 1.0) + st.appear_js(f"#{P}-lno", T[0] + 1.1) + st.pop_js(f"#{P}-end", T[0] + 1.5)
        js += draw_js(f"#{P}-ayes", T[0] + 2.4) + st.appear_js(f"#{P}-lyes", T[0] + 2.5)
        js += "".join(f'tl.set("#{P}-mg",{{opacity:0}},0);\n' for _ in [0])
        js += st.badge_seq_js([f"{P}-b3"], [T[1]], D - 0.4)
        js += show_js(f"#{P}-mg", T[1]) + lab_js(f"{P}-mg", T[1] + 0.2)
        js += st.appear_js(f"#{P}-w", T[1] + 0.5, 0.35)
        js += f'tl.fromTo("#{P}-nowms",{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:0.35,ease:"power3.out"}},{T[1]+2.2:.2f});\n'
        js += st.appear_js(f"#{P}-o1", T[2] + 0.3) + st.appear_js(f"#{P}-o2", T[3] + 0.3)
        return body, "", js
    s = Scene("cxdiff", lines, build, lead=0.4, tail=1.6, min_hold={0: 4.0, 1: 5.0, 2: 3.4, 3: 3.0})
    return s


def cx_g3():
    return ghinho("g3", 3, [
        (IC_CELLS, "Mỗi DO <b>một ô riêng</b>, ghi số DO lên ô", "Mỗi DO một ô riêng, ghi số DO lên ô"),
        (IC_PDA, "Quét mã hàng → PDA chỉ <b>DO và số lượng</b> → đặt vào ô, xác nhận",
         "Quét mã hàng, PDA chỉ DO và số lượng, đặt vào ô, xác nhận"),
        (IC_WARN, "Thiếu / thừa: <b>quản lý kho</b> xử lý thủ công (không có báo cáo WMS)", "Thiếu thừa: quản lý kho xử lý thủ công, không có báo cáo WMS"),
    ])


# ============================================================ CHƯƠNG 4 – Kiểm & Bàn giao
def cx_check():
    lines = ["Checker chọn xe hoặc Master DO, quét mã hàng của từng DO,",
             "kiểm ngoại quan và số lượng theo thùng và số lẻ.",
             "Nếu không khớp với DO, chia lại hoặc bổ sung hàng, rồi kiểm lại."]

    def build(T, D):
        P = "c41"
        xs = [560, 860, 1160]
        qtys = ["20/20", "29/30", "5/5"]
        cells = ""
        for i, (x, (d, _)) in enumerate(zip(xs, DOS)):
            n = [4, 5, 2][i]
            cells += cell_svg(f"{P}-c{i}", x, d, w=230, load=cups(f"{P}-cl{i}", x - n * 11, FY - 4, n, hidden=False))
        extra = cups(P + "-add", xs[1] + 60, FY - 4, 1)
        X0, SC = 230, 1.5
        a, b = SCAN["armR"]
        ck = (f'<g transform="translate({X0},{FY})"><g id="{P}-mv">{stick(P + "-ck", "checker", SC, label=True, pose=SCAN, hand_r=pda_svg(P + "-ck"))}</g></g>')
        tip0 = hand(X0, FY, SC, a, b, extra=56)
        stops = [xs[0] - 170, xs[1] - 170]
        l1 = st.laser(f"{P}-l1", tip0[0] + stops[0] - X0, tip0[1], xs[0] - 10, FY - 20)
        l2 = st.laser(f"{P}-l2", tip0[0] + stops[1] - X0, tip0[1], xs[1] - 10, FY - 20)
        l3 = st.laser(f"{P}-l3", tip0[0] + stops[1] - X0, tip0[1], xs[1] + 20, FY - 20)
        body = svg_layer(st.floor() + cells + extra + ck + l1 + l2 + l3)
        p1 = ('<div class="lbl">Kiểm hàng · chọn xe</div><div class="row sel"><b>XE-01 · MDO-0001</b></div><div class="row">XE-02 · MDO-0002</div>')
        p2 = kv("DO-1001 · SKU 2001", "20/20 hũ ✔", "Ngoại quan: tốt", C["green"])
        p3 = kv("DO-1002 · SKU 2001", "29/30 hũ ✖", "Không khớp với DO", C["red"])
        p4 = kv("DO-1002 · SKU 2001", "30/30 hũ ✔", "Đã khớp", C["green"])
        body += st.pda(f"{P}-pda", "Kiểm hàng", [("s1", p1), ("s2", p2), ("s3", p3), ("s4", p4)])
        body += pill(f"{P}-q", 560, 170, "Khớp với DO? → Không", "#fff", border=C["red"], size=32)
        body += st.badge(f"{P}-b1", 1, "Kiểm hàng") + st.badge(f"{P}-b2", 2, "Xử lý sai lệch")
        js = st.badge_seq_js([f"{P}-b1", f"{P}-b2"], [T[0], T[2]], D - 0.4) + lab_js(f"{P}-ck", 0.3)
        js += "".join(f'tl.set("#{P}-c{i}-load",{{opacity:1}},0);\n' for i in range(3))
        js += st.appear_js(f"#{P}-pda", T[0], 0.35, dy=30) + st.show_panel_js(f"{P}-pda", None, "s1", T[0] + 0.1)
        js += lab_off(f"{P}-ck", T[0] + 1.4)
        js += walk_to(f"{P}-ck", f"{P}-mv", stops[0] - X0, T[0] + 1.4, 1.0)
        js += st.laser_js(f"{P}-l1", T[0] + 2.6) + st.show_panel_js(f"{P}-pda", "s1", "s2", T[0] + 2.7)
        js += walk_to(f"{P}-ck", f"{P}-mv", stops[1] - X0, T[1] + 0.2, 1.0)
        js += st.laser_js(f"{P}-l2", T[1] + 1.4) + st.show_panel_js(f"{P}-pda", "s2", "s3", T[1] + 1.5)
        js += st.appear_js(f"#{P}-q", T[1] + 1.8)
        js += hide_js(f"#{P}-q", T[2] + 1.0) + st.pop_js(f"#{P}-add", T[2] + 0.8)
        js += st.laser_js(f"{P}-l3", T[2] + 2.0) + st.show_panel_js(f"{P}-pda", "s3", "s4", T[2] + 2.1)
        return body, "", js
    s = Scene("cxcheck", lines, build, lead=0.4, tail=1.6, min_hold={0: 4.2, 1: 3.8, 2: 4.8})
    s.sfx = [(("T", 1, 1.5), "error.mp3", 0.2), (("T", 2, 2.1), "ping.mp3", 0.25)]
    return s


def cx_hand():
    lines = ["Khớp rồi thì checker in giấy bàn giao của xe, mỗi DO một giấy.",
             "Tài xế nhận hàng lên xe và ký giấy bàn giao.",
             "XLCT xác nhận hoàn tất Master DO và lưu lại giấy bàn giao đã ký."]

    def build(T, D):
        P = "c42"
        TRX = 1300
        goods = "".join(f'<g id="{P}-g{i}">{st.carton(760 + i*80, FY - 56, 74, 56)}</g>' for i in range(3))
        body = svg_layer(st.floor() + f'<g id="{P}-st1">' + printer_svg(P + "-pr", 300)
                         + figure(P + "-ck", "checker", 480, scale=1.5, label=True) + '</g>'
                         + f'<g id="{P}-st2" opacity="0">{desk_svg(300)}'
                         + figure(P + "-xl", "xlct", 300, FY - 40, scale=1.5, label=True, pose={"armL": (22, -70), "armR": (-22, 70)}) + '</g>'
                         + f'<g transform="translate({TRX},{FY})"><g id="{P}-tk">{st.truck(P + "-tkk", label="XE-01")}</g></g>'
                         + goods
                         + f'<g transform="translate(1180,{FY})"><g id="{P}-dr">{stick(P + "-dv", "driver", 1.5, label=True)}</g></g>')
        sig = ""
        for i, (d, _) in enumerate(DOS):
            body += paper(f"{P}-p{i}", 190, 470, f"Bàn giao {d}", 260, 180)
            sx = 560 + i * 300
            sig += (f'<path id="{P}-s{i}" d="M{sx+40},{288} C{sx+60},{258} {sx+75},{302} {sx+95},{276} S{sx+130},{262} {sx+140},{290} S{sx+180},{276} {sx+210},{268}" '
                    f'fill="none" stroke="{HANDW}" stroke-width="5" stroke-linecap="round" stroke-dasharray="320" stroke-dashoffset="320"/>')
        body += svg_layer(sig)
        inner = (f'<div style="font-size:34px;font-weight:900">MDO-0001 · XE-01</div><div style="font-size:26px;font-weight:700;color:{C["muted"]};margin:4px 0 14px">3 DO · 3 giấy bàn giao đã ký</div>'
                 f'{btn(P + "-go", "HOÀN TẤT")}')
        body += win(f"{P}-w", 560, 380, 560, "WMS · Xuất hàng", inner)
        body += st.stamp(f"{P}-ok", "Hoàn tất Master DO", x=600, y=650)
        body += pill(f"{P}-file", 1480, 40, "Lưu giấy bàn giao đã ký ✔", "#fff", border=C["green"], size=30)
        body += st.badge(f"{P}-b3", 3, "In giấy bàn giao") + st.badge(f"{P}-b4", 4, "Nhận hàng và ký") + st.badge(f"{P}-b5", 5, "Hoàn tất")
        js = st.badge_seq_js([f"{P}-b3", f"{P}-b4", f"{P}-b5"], [T[0], T[1], T[2]], D - 0.4)
        js += lab_js(f"{P}-ck", 0.3) + f'tl.set("#{P}-dr",{{opacity:0}},0);\n'
        for i in range(3):
            t = T[0] + 0.6 + i * 0.7
            js += (f'tl.fromTo("#{P}-p{i}",{{opacity:0,x:0,y:0,scale:0.4}},{{opacity:1,x:{370 + i*300},y:-290,scale:1,duration:0.6,ease:"power2.out",transformOrigin:"50% 100%"}},{t:.2f});\n')
        js += lab_off(f"{P}-ck", T[1] - 0.2)
        js += show_js(f"#{P}-dr", T[1]) + lab_js(f"{P}-dv", T[1] + 0.2)
        for i in range(3):
            t = T[1] + 0.6 + i * 0.4
            js += f'tl.to("#{P}-g{i}",{{x:{TRX + 20 - 760 - i*80},y:-60,opacity:0,duration:0.6,ease:"power2.in"}},{t:.2f});\n'
        for i in range(3):
            js += f'tl.to("#{P}-s{i}",{{strokeDashoffset:0,duration:0.5,ease:"none"}},{T[1]+2.0+i*0.6:.2f});\n'
        js += lab_off(f"{P}-dv", T[2] - 0.2) + hide_js(f"#{P}-st1", T[2] - 0.2) + show_js(f"#{P}-st2", T[2]) + lab_js(f"{P}-xl", T[2] + 0.2)
        js += st.appear_js(f"#{P}-w", T[2] + 0.1) + press_js(f"#{P}-go", T[2] + 1.2) + st.stamp_js(f"{P}-ok", T[2] + 1.4)
        for i in range(3):
            js += f'tl.to("#{P}-p{i}",{{x:{1500 - 190},y:{-430},scale:0.2,opacity:0,duration:0.6,ease:"power2.in",transformOrigin:"0% 0%"}},{T[2]+2.0+i*0.15:.2f});\n'
            js += f'tl.to("#{P}-s{i}",{{opacity:0,duration:0.3}},{T[2]+2.0:.2f});\n'
        js += st.appear_js(f"#{P}-file", T[2] + 2.6)
        js += f'tl.to("#{P}-tk",{{x:900,duration:1.6,ease:"power2.in"}},{T[2]+2.8:.2f});\n'
        js += hide_js(f"#{P}-dr", T[2] + 2.8)
        return body, "", js
    s = Scene("cxhand", lines, build, lead=0.4, tail=2.0, min_hold={0: 4.0, 1: 4.2, 2: 5.0})
    s.sfx = [(("T", 0, 0.6), "click-soft.mp3", 0.3), (("T", 2, 1.4), "chime.mp3", 0.22)]
    return s


def cx_g4():
    return ghinho("g4", 4, [
        (ic_check(), "Kiểm từng DO: <b>ngoại quan + số lượng</b> thùng và lẻ", "Kiểm từng DO: ngoại quan và số lượng thùng và lẻ"),
        (IC_LOOP, "Không khớp → <b>chia lại / bổ sung</b> rồi kiểm lại", "Không khớp, chia lại hoặc bổ sung rồi kiểm lại"),
        (IC_DOC, "Mỗi DO <b>một giấy bàn giao</b>, tài xế ký, XLCT lưu", "Mỗi DO một giấy bàn giao, tài xế ký, XLCT lưu"),
    ])


def cx_end():
    lines = ["Đó là toàn bộ quy trình kho CXAD, từ nhập hàng đến bàn giao hàng lên xe.",
             "Chúc các bạn làm việc thật tốt!"]
    steps = bx.STAGES

    def build(T, D):
        P = "cxe"
        W, G, X0 = 360, 60, 120
        chips = ""
        for i, t in enumerate(steps):
            x = X0 + i * (W + G)
            chips += (f'<div id="{P}-s{i}" class="abs" style="left:{x}px;top:200px;width:{W}px;height:150px;background:#fff;border:4px solid {INK};border-radius:22px;'
                      f'display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0">'
                      f'<div style="font-size:30px;font-weight:900;color:#C45A00">{i+1}</div><div style="font-size:34px;font-weight:900;text-align:center;line-height:1.15;padding:0 10px">{t}</div>'
                      f'<div id="{P}-k{i}" class="abs" style="right:-18px;top:-18px;opacity:0">{st.check(54)}</div></div>')
            if i < len(steps) - 1:
                chips += f'<div id="{P}-a{i}" class="abs" style="left:{x+W}px;top:242px;width:{G}px;text-align:center;font-size:50px;font-weight:900;color:{C["blue"]};opacity:0">›</div>'
        thumb = f'<circle cx="0" cy="25" r="8" fill="{INK}"/><line x1="0" y1="30" x2="0" y2="44" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
        man = svg_layer(f'<g transform="translate(960,{FY+40})"><g id="{P}-man">{stick(P + "-man", "instructor", 2.0, hand_r=thumb)}</g></g>')
        body = f'<div class="abs" style="left:0;top:{FY}px;width:1920px;height:{1080-FY}px;background:{C["floor"]}"></div>' + chips + man
        js = ""
        for i in range(len(steps)):
            js += f'tl.fromTo("#{P}-s{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{0.3 + i*0.35:.2f});\n'
            if i < len(steps) - 1:
                js += f'tl.fromTo("#{P}-a{i}",{{opacity:0}},{{opacity:1,duration:0.2}},{0.5 + i*0.35:.2f});\n'
            js += f'tl.fromTo("#{P}-k{i}",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.25,ease:"power3.out"}},{T[0] + 0.8 + i*0.45:.2f});\n'
        js += pose_js(f"{P}-man", T[1] + 0.2, {"armR": (-100, -80)}, dur=0.35, ease="back.out(2)")
        return body, "", js
    s = Scene("cxend", lines, build, lead=0.6, tail=2.6, min_hold={0: 4.6, 1: 2.4})
    s.sfx = [(("T", 1, 0.2), "chime.mp3", 0.22)]
    return s
