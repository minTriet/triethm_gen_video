"""Flat (side-view) stage components for parts 2–5 of the training video.
All functions return SVG/HTML strings. Coordinates are scene pixels (1920x1080)
unless a function says it draws around a local origin.
"""
import math
from kit import C, FONT, ROLE, stick, pda_svg

INK = C["ink"]
FY = 800                       # floor line
PDA_X, PDA_Y, PDA_W, PDA_H = 1390, 96, 430, 740


# ------------------------------------------------------------ basics
def floor(y=FY):
    return (f'<rect x="0" y="{y}" width="1920" height="{1080-y}" fill="{C["floor"]}"/>'
            f'<line x1="0" y1="{y}" x2="1920" y2="{y}" stroke="{C["floor_line"]}" stroke-width="4"/>')


def carton(x, y, w=74, h=56, label=None, cid=None, fs=15):
    i = f' id="{cid}"' if cid else ""
    s = (f'<g{i}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2.5"/>'
         f'<rect x="{x + w/2 - 7}" y="{y}" width="14" height="{h}" fill="#F3DDB5"/>')
    if label:
        lw = min(w - 10, 14 + len(label) * fs * 0.62)
        s += (f'<rect x="{x + w/2 - lw/2}" y="{y + h/2 - fs*0.75}" width="{lw}" height="{fs*1.5}" rx="3" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
              f'<text x="{x + w/2}" y="{y + h/2 + fs*0.36}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="{fs}" fill="{INK}">{label}</text>')
    return s + "</g>"


def barcode(x, y, w=40, h=20):
    n = 9
    bars = "".join(f'<rect x="{x + 3 + i*(w-6)/n:.1f}" y="{y+3}" width="{1.6 if i % 3 else 2.8}" height="{h-6}" fill="{INK}"/>' for i in range(n))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{INK}" stroke-width="1.2"/>' + bars


def pallet(pid, cx, by, lpn=None, sku=None, rows=2, extra_cls=""):
    """Pallet with cartons, bottom-centre at (cx, by). Ids: {pid}, {pid}-lpn."""
    s = [f'<g id="{pid}" {extra_cls}>']
    s.append(f'<rect x="{cx-80}" y="{by-18}" width="160" height="18" rx="2" fill="{C["pal_r"]}" stroke="{INK}" stroke-width="2.5"/>')
    for k in range(3):
        s.append(f'<rect x="{cx-72 + k*62}" y="{by-14}" width="20" height="14" fill="{C["pal_l"]}"/>')
    for r in range(rows):
        for c in range(2):
            s.append(carton(cx - 76 + c*76, by - 18 - 56*(r+1), 76, 56, label=sku if (r == 0 and c == 1 and sku) else None, fs=13))
    if lpn:
        s.append(f'<g id="{pid}-lpn"><rect x="{cx-72}" y="{by-62}" width="66" height="36" rx="3" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                 f'<text x="{cx-39}" y="{by-47}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="12" fill="{INK}">LPN</text>'
                 + barcode(cx - 66, by - 44, 54, 14) + '</g>')
    s.append("</g>")
    return "".join(s)


# ------------------------------------------------------------ flat rack
class Rack:
    """Elevation view of a rack. Level 0 = PRIMARY (orange beam), upper = RESERVED (blue)."""

    def __init__(self, prefix, x0, cols=3, levels=3, cw=250, lh=200, fy=FY, aisle="A"):
        self.p, self.x0, self.cols, self.levels, self.cw, self.lh, self.fy = prefix, x0, cols, levels, cw, lh, fy
        self.aisle = aisle

    def beam_y(self, k):
        return self.fy - 24 - k * self.lh if k else self.fy - 24

    def slot(self, c, k):
        """(centre x, top of beam y) where a load stands."""
        return (self.x0 + c * self.cw + self.cw / 2, self.beam_y(k))

    def loc(self, c, k):
        return f"{self.aisle}-{c+1:02d}-{k+1:02d}"

    def label_xy(self, c, k):
        x, y = self.slot(c, k)
        return (x, y + 12)

    def svg(self, contents=None, tags=None):
        contents = contents or {}
        tags = tags or {}
        p, x0, W = self.p, self.x0, self.cols * self.cw
        top = self.beam_y(self.levels - 1) - self.lh + 30
        s = [f'<g id="{p}">']
        # zone tints
        s.append(f'<rect id="{p}-resbg" x="{x0}" y="{top}" width="{W}" height="{self.beam_y(0) - top - 4}" fill="{C["reserved"]}" opacity="0.45"/>')
        s.append(f'<rect id="{p}-primbg" x="{x0}" y="{self.beam_y(0) - self.lh + 30}" width="{W}" height="{self.lh - 30}" fill="#FFE3C4" opacity="0.8"/>')
        for c in range(self.cols + 1):
            s.append(f'<rect x="{x0 + c*self.cw - 8}" y="{top - 10}" width="16" height="{self.fy - top + 10}" fill="{C["post_r"]}" stroke="{INK}" stroke-width="2.5"/>')
        for k in range(self.levels):
            y = self.beam_y(k)
            col = C["orange"] if k == 0 else "#8DBAF0"
            s.append(f'<rect x="{x0 - 8}" y="{y}" width="{W + 16}" height="20" fill="{col}" stroke="{INK}" stroke-width="2.5"/>')
        for (c, k), what in contents.items():
            cx, by = self.slot(c, k)
            gid = f"{p}-c{c}-l{k}"
            if what == "pallet":
                s.append(pallet(gid, cx, by, lpn=True))
            elif what == "cartons":
                s.append(f'<g id="{gid}">' + "".join(carton(cx - 100 + i*68, by - 56, 64, 56) for i in range(3))
                         + "".join(carton(cx - 66 + i*68, by - 112, 64, 56) for i in range(2)) + "</g>")
        for c in range(self.cols):
            for k in range(self.levels):
                x, y = self.label_xy(c, k)
                s.append(f'<g id="{p}-loc-c{c}-l{k}"><rect x="{x-62}" y="{y-11}" width="124" height="30" rx="4" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                         f'<text x="{x}" y="{y+11}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="20" fill="{INK}">{self.loc(c, k)}</text></g>')
        for (c, k), t in tags.items():   # fixed SKU tag above a primary slot
            x, y = self.slot(c, k)
            s.append(f'<g id="{p}-tag-c{c}-l{k}"><rect x="{x-58}" y="{y-self.lh+40}" width="116" height="30" rx="15" fill="{INK}"/>'
                     f'<text x="{x}" y="{y-self.lh+62}" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="19" fill="#fff">{t}</text></g>')
        s.append("</g>")
        return "".join(s)


def zone_labels(rack, prefix, x):
    """RESERVED / PRIMARY side labels to the left of a rack."""
    yr = (rack.beam_y(rack.levels - 1) + rack.beam_y(1)) / 2 - 60
    yp = rack.beam_y(0) - 80
    return (f'<g id="{prefix}-zr"><rect x="{x}" y="{yr-26}" width="200" height="52" rx="12" fill="{C["reserved"]}" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="{x+100}" y="{yr+9}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="26" fill="{INK}">RESERVED</text></g>'
            f'<g id="{prefix}-zp"><rect x="{x}" y="{yp-26}" width="200" height="52" rx="12" fill="{C["orange"]}" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="{x+100}" y="{yp+9}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="26" fill="{INK}">PRIMARY</text></g>')


# ------------------------------------------------------------ vehicles & carriers
def forklift(fid, label=False, load=None):
    """Forklift facing right, origin = ground under the body centre. Forks group {fid}-forks
    (translate y to lift). load: svg drawn on the forks (bottom at y=-22)."""
    return (f'<g id="{fid}">'
            f'<path d="M-52,-78 L-52,-175 L22,-175 L22,-78" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
            f'<rect x="38" y="-200" width="12" height="190" fill="#8FA3BF" stroke="{INK}" stroke-width="2.5"/>'
            f'<g transform="translate(-22,-14)">{stick(fid + "-drv", "forklift", 1.0, label=label, pose={"armR": (-70, -20), "armL": (10, -40)})}</g>'
            f'<line x1="22" y1="-110" x2="-6" y2="-104" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<g id="{fid}-forks"><rect x="46" y="-70" width="10" height="56" fill="#5D7290" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="50" y="-22" width="150" height="8" fill="#8FA3BF" stroke="{INK}" stroke-width="2.5"/>'
            f'{load or ""}</g>'
            f'<rect x="-70" y="-78" width="105" height="58" rx="10" fill="#5D7290" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-82" y="-70" width="18" height="42" rx="4" fill="#3E4E66" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-66" y="-30" width="32" height="10" fill="{C["orange"]}"/>'
            f'<circle cx="-42" cy="-12" r="16" fill="{INK}"/><circle cx="-42" cy="-12" r="6" fill="#8FA3BF"/>'
            f'<circle cx="16" cy="-12" r="16" fill="{INK}"/><circle cx="16" cy="-12" r="6" fill="#8FA3BF"/></g>')


def truck(tid, label=None):
    """Box truck, rear (cargo doors) on the left. Origin = ground at rear bumper."""
    lab = ""
    if label:
        lab = f'<text x="160" y="-100" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="30" fill="{C["muted"]}">{label}</text>'
    return (f'<g id="{tid}"><rect x="0" y="-232" width="300" height="196" rx="8" fill="#FFFFFF" stroke="{INK}" stroke-width="3.5"/>'
            f'<rect x="0" y="-232" width="300" height="22" fill="#8C96A3"/>'
            f'<line x1="8" y1="-200" x2="8" y2="-44" stroke="{INK}" stroke-width="2" opacity="0.5"/>{lab}'
            f'<path d="M300,-170 L360,-170 L392,-118 L392,-36 L300,-36 Z" fill="{C["blue"]}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<path d="M312,-158 L354,-158 L376,-122 L312,-122 Z" fill="#BFD8F5" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="64" cy="-30" r="26" fill="{INK}"/><circle cx="64" cy="-30" r="10" fill="#8FA3BF"/>'
            f'<circle cx="340" cy="-30" r="26" fill="{INK}"/><circle cx="340" cy="-30" r="10" fill="#8FA3BF"/></g>')


def trolley(tid, code, slots=6):
    """Platform trolley, handle at local x=0, origin = ground at the handle.
    Carton slot ids {tid}-k{i} (hidden by default)."""
    s = [f'<g id="{tid}">',
         f'<line x1="0" y1="-120" x2="0" y2="-18" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>',
         f'<line x1="-10" y1="-120" x2="10" y2="-120" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>',
         f'<rect x="-4" y="-28" width="200" height="12" rx="3" fill="#8FA3BF" stroke="{INK}" stroke-width="3"/>',
         f'<circle cx="18" cy="-8" r="9" fill="{INK}"/><circle cx="176" cy="-8" r="9" fill="{INK}"/>']
    pos = [(8, -84), (68, -84), (128, -84), (8, -140), (68, -140), (128, -140)][:slots]
    for i, (x, y) in enumerate(pos):
        s.append(f'<g id="{tid}-k{i}" opacity="0">' + carton(x, y, 58, 56) + "</g>")
    s.append(f'<g id="{tid}-code"><rect x="-58" y="-176" width="116" height="38" rx="7" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
             f'<text x="0" y="-149" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="22" fill="{INK}">{code}</text>'
             f'<line x1="0" y1="-138" x2="0" y2="-122" stroke="{INK}" stroke-width="2.5"/></g>')
    s.append("</g>")
    return "".join(s)


def oricon(oid, code, w=170, h=100, title_color="#2F6FD6"):
    """Blue plastic tote, origin = bottom-centre. Item slot group {oid}-items."""
    return (f'<g id="{oid}"><g id="{oid}-items"></g>'
            f'<path d="M{-w/2},{-h} L{w/2},{-h} L{w/2-10},0 L{-w/2+10},0 Z" fill="#2F6FD6" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
            f'<rect x="{-w/2-4}" y="{-h-6}" width="{w+8}" height="12" rx="4" fill="#4C86E6" stroke="{INK}" stroke-width="3"/>'
            + "".join(f'<line x1="{-w/2+24 + i*((w-48)/4):.0f}" y1="{-h+16}" x2="{-w/2+24 + i*((w-48)/4):.0f}" y2="-12" stroke="#1D4FA8" stroke-width="3"/>' for i in range(5))
            + f'<rect x="-46" y="{-h/2-16}" width="92" height="30" rx="5" fill="#fff" stroke="{INK}" stroke-width="2"/>'
            f'<text x="0" y="{-h/2+6}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="18" fill="{INK}">{code}</text>'
            f'<text x="0" y="{-h-16}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="20" fill="{title_color}" stroke="#fff" stroke-width="5" paint-order="stroke">ORICON</text></g>')


# ------------------------------------------------------------ geometry helpers
def hand_xy(px, py, scale, a, b, side="R", extra=0.0):
    """Global position of a figure's hand (or a point `extra` px further along the forearm).
    Figure feet at (px, py). a = shoulder deg, b = elbow deg."""
    sx = 12 if side == "R" else -12
    ra, rab = math.radians(a), math.radians(a + b)
    x = sx + 25 * -math.sin(ra) + (23 + extra) * -math.sin(rab)
    y = -98 + 25 * math.cos(ra) + (23 + extra) * math.cos(rab)
    return (px + scale * x, py + scale * y)


def laser(lid, x1, y1, x2, y2):
    """Red scan line + target rings (opacity 0). Animate with laser_js."""
    return (f'<g id="{lid}" opacity="0"><line id="{lid}-l" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#E53935" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="16" fill="none" stroke="#E53935" stroke-width="4"/>'
            f'<circle id="{lid}-r" cx="{x2:.0f}" cy="{y2:.0f}" r="16" fill="none" stroke="#E53935" stroke-width="3"/></g>')


def laser_js(lid, t, dur=0.9):
    return (f'tl.fromTo("#{lid}",{{opacity:0}},{{opacity:1,duration:0.08}},{t:.2f});\n'
            f'tl.fromTo("#{lid}-r",{{scale:1,opacity:1}},{{scale:2.6,opacity:0,duration:0.5,ease:"power2.out",transformOrigin:"50% 50%"}},{t+0.08:.2f});\n'
            f'tl.to("#{lid}",{{opacity:0,duration:0.15}},{t+dur:.2f});\n')


# ------------------------------------------------------------ PDA (big, right side)
PDA_CSS = f"""
.pda{{position:absolute;left:{PDA_X}px;top:{PDA_Y}px;width:{PDA_W}px;height:{PDA_H}px;background:#2B3646;border:5px solid {INK};border-radius:46px;box-shadow:0 18px 0 rgba(27,36,48,.12)}}
.pda .scr{{position:absolute;left:22px;top:52px;right:22px;bottom:66px;background:#fff;border-radius:16px;overflow:hidden}}
.pda .cam{{position:absolute;left:50%;top:20px;width:60px;height:10px;margin-left:-30px;border-radius:5px;background:#4A5568}}
.pda .btn{{position:absolute;left:50%;bottom:16px;width:96px;height:32px;margin-left:-48px;border-radius:16px;background:#4A5568}}
.pda .hdr{{background:{C['blue']};color:#fff;font-weight:900;font-size:30px;padding:18px 22px}}
.pda .pn{{position:absolute;left:0;right:0;top:74px;bottom:0;padding:22px 22px;opacity:0}}
.pda .lbl{{font-size:26px;font-weight:700;color:{C['muted']};margin-bottom:8px}}
.pda .fld{{border:4px solid {C['orange']};border-radius:14px;padding:12px 16px;font-size:34px;font-weight:900;min-height:66px;margin-bottom:18px;background:#FFF7EE}}
.pda .fld.off{{border-color:#D5DBE4;background:#F1F3F6;color:#A9B2BF}}
.pda .fld.ok{{border-color:{C['green']};background:#EDF9F1}}
.pda .row{{border:3px solid #E3E8EF;border-radius:12px;padding:12px 16px;font-size:28px;font-weight:700;margin-bottom:12px}}
.pda .row.sel{{border-color:{C['blue']};background:#EAF1FC}}
.pda .big{{font-size:44px;font-weight:900}}
.pda .go{{margin-top:12px;background:{C['green']};color:#fff;font-weight:900;font-size:32px;text-align:center;border-radius:14px;padding:16px 0}}
.pda .keys{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:10px}}
.pda .keys div{{background:#EEF2F6;border-radius:10px;text-align:center;font-size:32px;font-weight:900;padding:12px 0}}
"""


def pda(pid, title, panels):
    """panels: list of (panel_id, inner_html). Panel ids are {pid}-{panel_id}."""
    inner = "".join(f'<div id="{pid}-{k}" class="pn">{h}</div>' for k, h in panels)
    return (f'<div id="{pid}" class="pda" style="opacity:0"><div class="cam"></div><div class="scr">'
            f'<div class="hdr" id="{pid}-hdr">{title}</div>{inner}</div><div class="btn"></div></div>')


def show_panel_js(pid, prev, nxt, t):
    s = ""
    if prev:
        s += f'tl.to("#{pid}-{prev}",{{opacity:0,duration:0.15}},{t:.2f});\n'
    s += f'tl.fromTo("#{pid}-{nxt}",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.25,ease:"power2.out"}},{t+0.1:.2f});\n'
    return s


# ------------------------------------------------------------ step badges
BADGE_CSS = f"""
.badge{{position:absolute;left:80px;top:56px;display:flex;align-items:center;gap:16px;opacity:0}}
.badge .n{{width:76px;height:76px;border-radius:50%;background:{C['orange']};border:4px solid {INK};font-size:30px;font-weight:900;display:flex;align-items:center;justify-content:center;line-height:1;text-align:center}}
.badge .t{{background:#fff;border:4px solid {INK};border-radius:18px;padding:10px 24px;font-size:40px;font-weight:900}}
.badge .ok{{opacity:0}}
"""


def badge(bid, n, text):
    return (f'<div id="{bid}" class="badge"><div class="n">{"Bước<br>" if False else ""}{n}</div>'
            f'<div class="t">Bước {n}: {text}</div><div id="{bid}-ok" class="ok">{check(60)}</div></div>')


def check(size=60):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="{C["green"]}"/>'
            f'<path d="M19 33l9 9 17-19" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def cross(size=60):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="{C["red"]}"/>'
            f'<path d="M22 22l20 20M42 22L22 42" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>')


def badge_seq_js(ids, starts, end):
    """Show badge i from starts[i] until the next one; tick it just before switching."""
    s = ""
    for i, b in enumerate(ids):
        t0 = starts[i]
        t1 = starts[i + 1] if i + 1 < len(ids) else end
        s += f'tl.fromTo("#{b}",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.25,ease:"power2.out"}},{t0:.2f});\n'
        s += f'tl.fromTo("#{b}-ok",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.2,ease:"power3.out"}},{t1 - 0.45:.2f});\n'
        if i + 1 < len(ids):
            s += f'tl.to("#{b}",{{opacity:0,duration:0.15}},{t1 - 0.12:.2f});\n'
    return s


def stamp(sid, text, color=None, x=0, y=0):
    color = color or C["green"]
    return (f'<div id="{sid}" class="abs" style="left:{x}px;top:{y}px;opacity:0"><div style="display:flex;align-items:center;gap:14px;'
            f'background:#fff;border:5px solid {color};border-radius:20px;padding:12px 26px;font-size:44px;font-weight:900;color:{INK}">'
            f'{check(54) if color == C["green"] else cross(54)}{text}</div></div>')


def stamp_js(sid, t):
    return f'tl.fromTo("#{sid}",{{opacity:0,scale:1.8,rotation:-6}},{{opacity:1,scale:1,rotation:0,duration:0.3,ease:"power3.out"}},{t:.2f});\n'


def pop_js(sel, t, dur=0.35):
    return f'tl.fromTo("{sel}",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:{dur},ease:"back.out(2.2)",transformOrigin:"50% 50%"}},{t:.2f});\n'


def fade_js(sel, t, to=0, dur=0.3):
    return f'tl.to("{sel}",{{opacity:{to},duration:{dur}}},{t:.2f});\n'


def appear_js(sel, t, dur=0.3, dy=16):
    return f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"power2.out"}},{t:.2f});\n'


def trolley_behind(tid, code, slots=6):
    """Trolley pulled behind a walker: handle at local x=0, platform to the LEFT.
    Carton ids {tid}-k{i} (hidden)."""
    s = [f'<g id="{tid}">',
         f'<line x1="0" y1="-120" x2="0" y2="-18" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>',
         f'<line x1="-10" y1="-120" x2="10" y2="-120" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>',
         f'<rect x="-196" y="-28" width="200" height="12" rx="3" fill="#8FA3BF" stroke="{INK}" stroke-width="3"/>',
         f'<circle cx="-18" cy="-8" r="9" fill="{INK}"/><circle cx="-176" cy="-8" r="9" fill="{INK}"/>']
    pos = [(-188, -84), (-128, -84), (-68, -84), (-188, -140), (-128, -140), (-68, -140)][:slots]
    for i, (x, y) in enumerate(pos):
        s.append(f'<g id="{tid}-k{i}" opacity="0">' + carton(x, y, 58, 56) + "</g>")
    s.append(f'<g id="{tid}-code"><rect x="-158" y="-196" width="116" height="38" rx="7" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
             f'<text x="-100" y="-169" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="22" fill="{INK}">{code}</text>'
             f'<line x1="-100" y1="-158" x2="-100" y2="-142" stroke="{INK}" stroke-width="2.5"/></g>')
    s.append("</g>")
    return "".join(s)
