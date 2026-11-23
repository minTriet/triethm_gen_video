"""Shared pieces for the CXAD full-warehouse video (tools/build_cxad.py).
Step-kind chips from the drawio legend, a WMS monitor, email, paper documents,
printer, decision diamond, zone racks and the zone panorama."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, stick, TYPE
import stage as st
from stage import FY, INK

ZONES = {  # name -> (fill tint, edge colour, label)
    "dong": ("#D6EEFB", "#2A7BBF", "ĐÔNG"),
    "chill": ("#CDF1EA", "#17806F", "CHILL"),
    "kho": ("#F4E7D0", "#9A6B37", "KHÔ"),
}
CHIA = ("#FFE9D2", C["orange"], "KHU CHIA HÀNG")
NAVY = "#16478F"
PAPER = "#FFFFFF"

EXTRA_CSS = f"""
.kchip{{display:inline-flex;align-items:center;gap:10px;border-radius:14px;padding:8px 16px;font-size:30px;font-weight:900;border:4px solid {INK};white-space:nowrap}}
.k-wms{{background:#fff;color:{C['blue']};border-color:{C['blue']}}}
.k-pda{{background:#2B3646;color:#fff}}
.k-tc{{background:{C['orange']};color:#fff;border-color:#C45A00}}
.wms{{position:absolute;background:#2B3646;border:5px solid {INK};border-radius:22px;box-shadow:0 18px 0 rgba(27,36,48,.12)}}
.wms .scr{{position:absolute;left:16px;top:16px;right:16px;bottom:16px;background:#fff;border-radius:10px;overflow:hidden}}
.wms .hdr{{background:{C['blue']};color:#fff;font-weight:900;font-size:28px;padding:12px 22px;display:flex;justify-content:space-between}}
.wms .hdr span{{opacity:.75;font-weight:700}}
.wms .pn{{position:absolute;left:0;right:0;top:58px;bottom:0;padding:20px 26px;opacity:0}}
.wms .lbl{{font-size:24px;font-weight:700;color:{C['muted']};margin-bottom:8px}}
.wms .row{{border:3px solid #E3E8EF;border-radius:10px;padding:10px 16px;font-size:26px;font-weight:700;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}}
.wms .row.sel{{border-color:{C['blue']};background:#EAF1FC}}
.wms .btnw{{display:inline-block;background:{C['blue']};color:#fff;font-weight:900;font-size:28px;border-radius:12px;padding:12px 26px}}
.wms .btng{{display:inline-block;background:{C['green']};color:#fff;font-weight:900;font-size:28px;border-radius:12px;padding:12px 26px}}
.wms .big{{font-size:44px;font-weight:900}}
.mail{{position:absolute;background:#fff;border:4px solid {INK};border-radius:20px;box-shadow:0 12px 0 rgba(27,36,48,.10);overflow:hidden}}
.mail .mh{{background:#EEF2F6;padding:12px 20px;font-size:26px;font-weight:900;display:flex;align-items:center;gap:12px}}
.mail .mr{{padding:16px 20px;font-size:26px;font-weight:700}}
.att{{display:inline-flex;align-items:center;gap:10px;margin-top:10px;border:3px solid {C['green']};background:#EDF9F1;border-radius:10px;padding:6px 14px;font-size:24px;font-weight:900}}
.doc{{position:absolute}}
.doc .dt{{position:absolute;left:0;right:0;top:16px;text-align:center;font-weight:900;color:{INK}}}
.pill{{display:inline-block;background:#fff;border:4px solid {INK};border-radius:18px;padding:10px 26px;font-size:40px;font-weight:900}}
"""
st.BADGE_CSS += EXTRA_CSS     # scene_file() inlines st.BADGE_CSS into every scene
st.LPN_FS = 17                # bigger "LPN" on pallet labels in this video


# ------------------------------------------------------------ step kind chips (drawio legend)
def _ic_monitor(col):
    return (f'<svg width="34" height="30" viewBox="0 0 34 30"><rect x="2" y="2" width="30" height="20" rx="3" fill="none" stroke="{col}" stroke-width="4"/>'
            f'<path d="M11 28h12M17 22v6" stroke="{col}" stroke-width="4" stroke-linecap="round"/></svg>')


def _ic_scanner():
    return ('<svg width="22" height="34" viewBox="0 0 22 34"><rect x="2" y="2" width="18" height="30" rx="4" fill="#7FD3FF" stroke="#fff" stroke-width="3"/>'
            '<rect x="6" y="7" width="10" height="9" rx="1" fill="#2B3646"/></svg>')


def _ic_hand():
    return ('<svg width="30" height="30" viewBox="0 0 30 30"><path d="M8 28V12a3 3 0 0 1 6 0v6V6a3 3 0 0 1 6 0v12V9a3 3 0 0 1 6 0v11c0 5-3 8-8 8z" '
            'fill="#fff" stroke="#fff" stroke-width="1" stroke-linejoin="round"/></svg>')


def kchip(kind):
    if kind == "WMS":
        return f'<span class="kchip k-wms">{_ic_monitor(C["blue"])}WMS</span>'
    if kind == "PDA":
        return f'<span class="kchip k-pda">{_ic_scanner()}PDA</span>'
    return f'<span class="kchip k-tc">{_ic_hand()}Thủ công</span>'


def cbadge(bid, n, text, kind):
    return (f'<div id="{bid}" class="badge"><div class="n">{n}</div><div class="t">Bước {n}: {text}</div>'
            f'{kchip(kind)}<div id="{bid}-ok" class="ok">{st.check(60)}</div></div>')


# ------------------------------------------------------------ WMS monitor
def wms(pid, title, panels, x=900, y=100, w=920, h=560, right="WMS"):
    inner = "".join(f'<div id="{pid}-{k}" class="pn">{html}</div>' for k, html in panels)
    return (f'<div id="{pid}" class="wms" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;opacity:0"><div class="scr">'
            f'<div class="hdr"><b>{title}</b><span>{right}</span></div>{inner}</div></div>')


def cursor(cid):
    return (f'<svg id="{cid}" class="abs" style="left:0;top:0;opacity:0" width="40" height="58" viewBox="0 0 40 58">'
            f'<path d="M2,2 L2,48 L14,36 L24,56 L33,51 L23,32 L39,32 Z" fill="#fff" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/></svg>')


def click_js(cid, x0, y0, x1, y1, t, target=None):
    s = (f'tl.fromTo("#{cid}",{{opacity:0,x:{x0},y:{y0}}},{{opacity:1,duration:0.15}},{t:.2f});\n'
         f'tl.to("#{cid}",{{x:{x1},y:{y1},duration:0.5,ease:"power2.inOut"}},{t+0.1:.2f});\n'
         f'tl.to("#{cid}",{{scale:0.85,duration:0.08}},{t+0.65:.2f});\ntl.to("#{cid}",{{scale:1,duration:0.1}},{t+0.73:.2f});\n')
    if target:
        s += (f'tl.to("{target}",{{scale:0.94,duration:0.08}},{t+0.65:.2f});\n'
              f'tl.to("{target}",{{scale:1,duration:0.12}},{t+0.73:.2f});\n')
    return s


# ------------------------------------------------------------ office (XLCT / manager at desk)
def desk(x, y=FY, screen="#7FD3FF"):
    return (f'<g transform="translate({x},{y})">'
            f'<rect x="80" y="-178" width="96" height="66" rx="6" fill="#2B3646" stroke="{INK}" stroke-width="3"/><rect x="87" y="-171" width="82" height="52" rx="3" fill="{screen}"/>'
            f'<rect x="122" y="-112" width="12" height="16" fill="#2B3646"/>'
            f'<rect x="-110" y="-98" width="320" height="18" rx="4" fill="#C9965A" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-90" y="-80" width="280" height="80" fill="#B98A55" stroke="{INK}" stroke-width="3"/></g>')


def office(fid, x=260, role="planner", label=True, scale=1.5):
    fig = f'<g transform="translate({x},{FY - 40})"><g id="{fid}">{stick(fid, role, scale, label=label, pose=TYPE)}</g></g>'
    return fig + desk(x)


def label_js(fid, t):
    return f'tl.fromTo("#{fid}-label",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t:.2f});\n'


def type_js(fid, t0, t1):
    s, t, k = "", t0, 0
    while t < t1:
        s += f'tl.to("#{fid}-foreR",{{rotation:{110 if k % 2 else 132},svgOrigin:"0 0",duration:0.18,ease:"sine.inOut"}},{t:.2f});\n'
        t += 0.2; k += 1
    return s


# ------------------------------------------------------------ email
def mail(mid, x, y, subject, fname, w=640):
    env = (f'<svg width="40" height="30" viewBox="0 0 40 30"><rect x="2" y="2" width="36" height="26" rx="4" fill="#fff" stroke="{INK}" stroke-width="3"/>'
           f'<path d="M3 4l17 13L37 4" fill="none" stroke="{INK}" stroke-width="3"/></svg>')
    clip = (f'<svg width="22" height="30" viewBox="0 0 22 30"><path d="M15 9v12a5 5 0 0 1-10 0V7a3.5 3.5 0 0 1 7 0v13" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></svg>')
    return (f'<div id="{mid}" class="mail" style="left:{x}px;top:{y}px;width:{w}px;opacity:0"><div class="mh">{env}Hộp thư · <span style="color:{C["red"]}">1 thư mới</span></div>'
            f'<div class="mr"><div>{subject}</div><div id="{mid}-att" class="att">{clip}{fname}</div></div></div>')


def sheet(sid, x, y, w=520):
    """Spreadsheet whose columns get re-ordered into the WMS template. Ids {sid}-c0..2, {sid}-ok."""
    cols = [("SKU", 0), ("Số lượng", 1), ("Ngày", 2)]
    cw = (w - 40) / 3
    heads = ""
    for name, i in cols:
        heads += (f'<div id="{sid}-c{i}" class="abs" style="left:{20 + i*cw:.0f}px;top:20px;width:{cw-8:.0f}px">'
                  f'<div style="background:{C["green"]};color:#fff;font-weight:900;font-size:22px;padding:6px 10px;border-radius:6px">{name}</div>'
                  + "".join(f'<div style="height:14px;margin-top:10px;border-radius:4px;background:#E3E8EF;width:{70 + (k*17 % 25)}%"></div>' for k in range(4))
                  + '</div>')
    return (f'<div id="{sid}" class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:230px;background:#fff;border:4px solid {INK};border-radius:16px;opacity:0">'
            f'{heads}<div id="{sid}-ok" class="abs" style="right:14px;bottom:12px;opacity:0;display:flex;align-items:center;gap:8px;font-size:24px;font-weight:900;color:{C["green"]}">'
            f'{st.check(36)}Đúng mẫu WMS</div></div>')


def sheet_fix_js(sid, t, w=520):
    """Columns start shuffled (Ngày, SKU, Số lượng) and slide into place."""
    cw = (w - 40) / 3
    start = {0: 1, 1: 2, 2: 0}     # col index -> shuffled slot
    s = ""
    for i, slot in start.items():
        s += f'tl.set("#{sid}-c{i}",{{x:{(slot - i) * cw:.0f}}},0);\n'
        s += f'tl.to("#{sid}-c{i}",{{x:0,duration:0.6,ease:"power2.inOut"}},{t + 0.15*i:.2f});\n'
    s += f'tl.fromTo("#{sid}-ok",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.25,ease:"power3.out"}},{t+0.9:.2f});\n'
    return s


# ------------------------------------------------------------ paper documents (chứng từ) & printer
def doc(did, x, y, title, w=230, h=290, fs=24, lines=4, extra="", rot=0):
    wave = f'M0,0 H{w} V{h-18} Q{w*0.75},{h-40} {w/2},{h-18} T0,{h-18} Z'
    ls = "".join(f'<rect x="24" y="{70 + k*34}" width="{w-48 - (k % 2)*40}" height="10" rx="4" fill="#D5DBE4"/>' for k in range(lines))
    return (f'<div id="{did}" class="doc" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;opacity:0;transform:rotate({rot}deg)">'
            f'<svg class="abs" style="left:0;top:0" width="{w}" height="{h}" viewBox="-3 -3 {w+6} {h+6}"><path d="{wave}" fill="{PAPER}" stroke="{C["blue"]}" stroke-width="3"/>{ls}</svg>'
            f'<div class="dt" style="font-size:{fs}px;padding:0 10px">{title}</div>{extra}</div>')


def printer(pid, x, y):
    return (f'<g id="{pid}" transform="translate({x},{y})">'
            f'<rect x="-120" y="-40" width="240" height="90" rx="14" fill="#5D7290" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="-90" y="-70" width="180" height="34" rx="6" fill="#8FA3BF" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="-96" y="0" width="192" height="12" rx="4" fill="{INK}"/>'
            f'<circle cx="92" cy="-12" r="7" fill="{C["green"]}"/></g>')


# ------------------------------------------------------------ decision diamond with two branches
def decision(did, q, cx, cy, left, right, w=600, h=210, spread=560, drop=230, fs=32):
    """left/right: (branch label, card html, card width). Cards are centred under the branch ends.
    Ids: {did}-q, {did}-aL/{did}-aR (paths), {did}-lL/{did}-lR (labels), {did}-cL/{did}-cR (cards)."""
    # shapes are drawn around (0,0) inside a translated group and scaled about svgOrigin "0 0"
    pts = f"0,{-h/2} {w/2},0 0,{h/2} {-w/2},0"
    svg = (f'<svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">'
           f'<g transform="translate({cx},{cy})"><g id="{did}-q" opacity="0"><polygon points="{pts}" fill="#fff" stroke="{C["blue"]}" stroke-width="6" stroke-linejoin="round"/>'
           f'<text x="0" y="{fs*0.36}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="{fs}" fill="{INK}">{q}</text></g></g>')
    html = ""
    for side, sx, (lab, card, cw) in (("L", -1, left), ("R", 1, right)):
        x0, x1 = cx + sx * w / 2, cx + sx * spread
        y1 = cy + drop
        svg += (f'<path id="{did}-a{side}" d="M{x0},{cy} H{x1} V{y1 - 8}" fill="none" stroke="{C["blue"]}" stroke-width="6" '
                f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="900" stroke-dashoffset="900"/>'
                f'<g transform="translate({(x0 + x1)/2},{cy - 38})"><g id="{did}-l{side}" opacity="0"><rect x="-70" y="-24" width="140" height="48" rx="24" fill="{C["blue"]}"/>'
                f'<text x="0" y="10" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="28" fill="#fff">{lab}</text></g></g>')
        html += f'<div id="{did}-c{side}" class="abs" style="left:{x1 - cw/2}px;top:{y1}px;width:{cw}px;opacity:0">{card}</div>'
    return svg + "</svg>" + html


def decision_js(did, t, tL, tR):
    # opacity only: a scale pop on these SVG groups lands offset in the render (diamond drifts off its arrows)
    s = f'tl.fromTo("#{did}-q",{{opacity:0}},{{opacity:1,duration:0.35,ease:"power2.out"}},{t:.2f});\n'
    for side, ts in (("L", tL), ("R", tR)):
        s += (f'tl.to("#{did}-a{side}",{{strokeDashoffset:0,duration:0.5,ease:"power2.inOut"}},{ts:.2f});\n'
              f'tl.fromTo("#{did}-l{side}",{{opacity:0}},{{opacity:1,duration:0.25,ease:"power2.out"}},{ts+0.15:.2f});\n'
              f'tl.fromTo("#{did}-c{side}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{ts+0.45:.2f});\n')
    return s


def card(text, color=None, sub="", fs=34):
    color = color or INK
    return (f'<div style="background:#fff;border:5px solid {color};border-radius:20px;padding:16px 22px;text-align:center;box-shadow:0 10px 0 rgba(27,36,48,.08)">'
            f'<div style="font-size:{fs}px;font-weight:900;line-height:1.2">{text}</div>'
            + (f'<div style="font-size:24px;font-weight:700;color:{C["muted"]};margin-top:6px">{sub}</div>' if sub else "") + '</div>')


# ------------------------------------------------------------ zone racks (no primary/reserved)
class ZRack:
    """Neutral elevation rack inside a temperature zone. Location code K-cc-ll."""

    def __init__(self, prefix, x0, zone="kho", cols=3, levels=3, cw=230, lh=190, code=None):
        self.p, self.x0, self.zone, self.cols, self.levels, self.cw, self.lh = prefix, x0, zone, cols, levels, cw, lh
        self.code = code or {"dong": "D", "chill": "C", "kho": "K"}[zone]

    def beam_y(self, k):
        return FY - 24 - k * self.lh

    def slot(self, c, k):
        return (self.x0 + c * self.cw + self.cw / 2, self.beam_y(k))

    def loc(self, c, k):
        return f"{self.code}-{c+1:02d}-{k+1:02d}"

    def label_xy(self, c, k):
        x, y = self.slot(c, k)
        return (x, y + 12)

    def svg(self, contents=(), labels=True, cartons=()):
        p, x0, W = self.p, self.x0, self.cols * self.cw
        tint, edge, _ = ZONES[self.zone]
        top = self.beam_y(self.levels - 1) - self.lh + 30
        s = [f'<g id="{p}">']
        for c in range(self.cols + 1):
            s.append(f'<rect x="{x0 + c*self.cw - 8}" y="{top - 10}" width="16" height="{FY - top + 10}" fill="{C["post_r"]}" stroke="{INK}" stroke-width="2.5"/>')
        for k in range(self.levels):
            s.append(f'<rect x="{x0 - 8}" y="{self.beam_y(k)}" width="{W + 16}" height="20" fill="{edge}" stroke="{INK}" stroke-width="2.5"/>')
        for (c, k) in contents:
            cx, by = self.slot(c, k)
            s.append(st.pallet(f"{p}-c{c}-l{k}", cx, by, lpn=True))
        for (c, k) in cartons:   # loose cartons for picking
            cx, by = self.slot(c, k)
            s.append(f'<g id="{p}-k{c}-l{k}">' + "".join(st.carton(cx - 98 + i*66, by - 56, 64, 56) for i in range(3))
                     + "".join(st.carton(cx - 65 + i*66, by - 112, 64, 56) for i in range(2)) + "</g>")
        if labels:
            for c in range(self.cols):
                for k in range(self.levels):
                    x, y = self.label_xy(c, k)
                    s.append(f'<g id="{p}-loc-c{c}-l{k}"><rect x="{x-68}" y="{y-13}" width="136" height="36" rx="5" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                             f'<text x="{x}" y="{y+14}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="25" fill="{INK}">{self.loc(c, k)}</text></g>')
        s.append("</g>")
        return "".join(s)


def zone_bg(zid, x0, w, zone, top=150, sign=True, fs=40):
    tint, edge, name = ZONES[zone] if zone in ZONES else CHIA
    s = f'<g id="{zid}"><rect x="{x0}" y="{top}" width="{w}" height="{FY - top}" fill="{tint}"/>'
    s += f'<rect x="{x0}" y="{FY + 6}" width="{w}" height="14" fill="{edge}" opacity="0.6"/>'
    if zone == "dong":
        s += "".join(f'<ellipse cx="{x0 + 60 + (i*137) % (w - 80)}" cy="{top + 80 + (i*61) % (FY - top - 120)}" rx="{70 + i*7 % 40}" ry="20" fill="#fff" opacity="0.45"/>' for i in range(7))
    if sign:
        sw = 34 + len(name) * fs * 0.66
        s += (f'<g id="{zid}-sign"><rect x="{x0 + w/2 - sw/2}" y="{top + 18}" width="{sw}" height="{fs*1.6}" rx="14" fill="{edge}" stroke="{INK}" stroke-width="3.5"/>'
              f'<text x="{x0 + w/2}" y="{top + 18 + fs*1.12}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="{fs}" fill="#fff">{name}</text></g>')
    return s + "</g>"


def chia_floor(x0, x1, sign=True, y=FY):
    tint, edge, name = CHIA
    s = f'<rect x="{x0}" y="{y+8}" width="{x1-x0}" height="78" rx="10" fill="{tint}" stroke="{edge}" stroke-width="5" stroke-dasharray="18 12"/>'
    if sign:
        s += (f'<g><line x1="{x0+30}" y1="{y}" x2="{x0+30}" y2="{y-210}" stroke="{INK}" stroke-width="6"/>'
              f'<rect x="{x0+30}" y="{y-262}" width="300" height="60" rx="12" fill="{edge}" stroke="{INK}" stroke-width="3.5"/>'
              f'<text x="{x0+180}" y="{y-221}" text-anchor="middle" font-family="{FONT}" font-weight="900" font-size="30" fill="#fff">{name}</text></g>')
    return s


def flip_fig(wid, fid, role, x, scale=1.5, label=False, pose=None, hand_r="", extra=""):
    """Figure facing LEFT that can walk. Move the wrapper {wid}; sway with walk_js(f"{wid}s", ...).
    (Swaying the flipped body itself makes GSAP read scale(-1,1) as a 180° turn.)"""
    from kit import stick as _stick
    return (f'<g transform="translate({x},{FY})"><g id="{wid}"><g id="{wid}s-body">'
            f'{_stick(fid, role, scale, label=label, pose=pose, hand_r=hand_r, flip=True)}{extra}</g></g></g>')


def cart(cid, label, n=6):
    """Hand cart pulled behind a walker (st.trolley_behind) labelled with the Master DO."""
    return st.trolley_behind(cid, label, slots=n)
