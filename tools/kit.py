"""Shared drawing kit for the "Vận hành kho khô" training series.

Every episode's scene files are generated from these helpers so the warehouse,
the stick figures, the colours and the type stay identical across episodes.
Output is plain SVG/HTML markup; animation is written per scene with GSAP.
"""
import math

# ---------------------------------------------------------------- palette
C = {
    "ground": "#F4F6F9",
    "floor": "#E6EAF0",
    "floor_line": "#D5DBE4",
    "ink": "#1B2430",
    "muted": "#6B7685",
    "blue": "#1F5FBF",
    "blue_dark": "#16478F",
    "orange": "#F28C1E",
    "green": "#22A55A",
    "red": "#D93B3B",
    "reserved": "#BFD8F5",
    "white": "#FFFFFF",
    # rack metal
    "post_top": "#8FA3BF", "post_l": "#5D7290", "post_r": "#748AA8",
    "deck_top": "#C9D3E0", "deck_l": "#9AA9BD", "deck_r": "#AEBBCC",
    # cardboard
    "box_top": "#E8C08A", "box_l": "#C9965A", "box_r": "#D9A86C",
    # pallet wood
    "pal_top": "#C7A27A", "pal_l": "#9C7A55", "pal_r": "#B08B63",
}

ROLE = {  # vest colour + label for each role (series bible)
    "receiver": ("#2FAE5F", "Nhân viên nhận hàng"),
    "forklift": ("#F28C1E", "Tài xế xe nâng"),
    "planner": ("#1F5FBF", "Nhân viên điều phối"),
    "picker": ("#F4C430", "Picker"),
    "checker": ("#8B5CF6", "Checker"),
    "transport": ("#8C96A3", "Đội vận tải"),
    "instructor": ("#1F5FBF", "Giảng viên"),
    "manager": ("#16478F", "Quản lý kho"),
}

FONT = "'Be Vietnam Pro'"

VI_RANGE = ("U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,"
            "U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,"
            "U+1EA0-1EF9,U+20AB")
LATIN_RANGE = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,"
               "U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,"
               "U+2193,U+2212,U+2215,U+FEFF,U+FFFD")


def font_css(prefix='assets/fonts/'):
    out = []
    for w in (500, 700, 900):
        for subset, rng in (("vietnamese", VI_RANGE), ("latin", LATIN_RANGE)):
            out.append(
                "@font-face{font-family:'Be Vietnam Pro';font-style:normal;"
                f"font-weight:{w};font-display:block;"
                f"src:url('{prefix}be-vietnam-pro-{subset}-{w}-normal.woff2') format('woff2');"
                f"unicode-range:{rng};}}")
    return "\n".join(out)


# ---------------------------------------------------------------- isometric
S = 60.0                 # px per world unit
COS = math.cos(math.radians(30)) * S
SIN = math.sin(math.radians(30)) * S
OX, OY = 940.0, 420.0    # world-svg origin offset


def iso(x, y, z=0.0):
    return (OX + (x - y) * COS, OY + (x + y) * SIN - z * S)


def _pts(points):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in points)


def poly(points, fill, extra=""):
    return f'<polygon points="{_pts(points)}" fill="{fill}" {extra}/>'


def cuboid(x, y, z, w, d, h, top, left, right, extra="", stroke=None):
    """Three visible faces of a box: top, the +y face (left) and the +x face (right)."""
    st = f' stroke="{stroke}" stroke-width="1.2" stroke-linejoin="round"' if stroke else ""
    t = [iso(x, y, z + h), iso(x + w, y, z + h), iso(x + w, y + d, z + h), iso(x, y + d, z + h)]
    l = [iso(x, y + d, z), iso(x + w, y + d, z), iso(x + w, y + d, z + h), iso(x, y + d, z + h)]
    r = [iso(x + w, y, z), iso(x + w, y + d, z), iso(x + w, y + d, z + h), iso(x + w, y, z + h)]
    return (f'<g {extra}>' + poly(l, left, st) + poly(r, right, st) + poly(t, top, st) + "</g>")


def carton(x, y, z, w=0.8, d=0.7, h=0.55, extra=""):
    g = cuboid(x, y, z, w, d, h, C["box_top"], C["box_l"], C["box_r"], stroke="#A97A44")
    # tape stripe on top
    a, b = iso(x + w / 2 - 0.06, y, z + h), iso(x + w / 2 + 0.06, y, z + h)
    c, e = iso(x + w / 2 + 0.06, y + d, z + h), iso(x + w / 2 - 0.06, y + d, z + h)
    return f'<g {extra}>' + g + poly([a, b, c, e], "#F3DDB5") + "</g>"


# ---------------------------------------------------------------- rack
LEVELS = (0.0, 1.35, 2.7)   # deck heights: ground = primary, upper two = reserved
TOP = 3.75                  # post height
BAY = 2.0                   # bay width (x)
DEPTH = 1.1                 # rack depth (y)


def rack_row(rid, y0, bays=6, x0=0.0, stock=None):
    """One rack row running along +x. Returns SVG markup.

    Classes for animation:
      .{rid}-prim-hl / .{rid}-res-hl   coloured deck overlays (opacity 0 at rest)
    Ids: {rid}-slot{b}-l{lvl} on every deck's load group.
    """
    stock = stock or {}
    parts = [f'<g id="{rid}">']
    y1 = y0 + DEPTH
    # floor footprint shadow
    parts.append(poly([iso(x0 - 0.1, y0 - 0.1), iso(x0 + bays * BAY + 0.1, y0 - 0.1),
                       iso(x0 + bays * BAY + 0.1, y1 + 0.1), iso(x0 - 0.1, y1 + 0.1)],
                      C["floor_line"]))
    pw = 0.14
    for b in range(bays + 1):          # back posts first
        bx = x0 + b * BAY - (pw if b == bays else 0)
        parts.append(cuboid(bx, y0, 0, pw, pw, TOP, C["post_top"], C["post_l"], C["post_r"]))
    for b in range(bays):
        bx = x0 + b * BAY
        for li, z in enumerate(LEVELS):
            hl = "prim" if li == 0 else "res"
            hlcol = C["orange"] if li == 0 else "#8DBAF0"
            dz = z + (0.12 if li == 0 else 0)
            parts.append(cuboid(bx, y0, dz, BAY, DEPTH, 0.1, C["deck_top"], C["deck_l"], C["deck_r"]))
            parts.append(cuboid(bx, y0, dz, BAY, DEPTH, 0.1, hlcol, hlcol, hlcol,
                                extra=f'class="{rid}-{hl}-hl" opacity="0"'))
            load = stock.get((b, li), "pallet" if li else "cartons")
            parts.append(f'<g id="{rid}-slot{b}-l{li}">')
            if load == "pallet":
                px, py = bx + 0.25, y0 + 0.08
                parts.append(cuboid(px, py, dz + 0.1, 1.5, 0.95, 0.16, C["pal_top"], C["pal_l"], C["pal_r"]))
                for (ox, oy) in ((0.0, 0.0), (0.75, 0.0)):
                    for k in range(2):
                        parts.append(carton(px + ox, py + 0.1 + oy * 0, dz + 0.26 + k * 0.5,
                                            0.72, 0.8, 0.5))
            elif load == "cartons":
                for k, ox in enumerate((0.15, 1.05)):
                    parts.append(carton(bx + ox, y0 + 0.2, dz + 0.1, 0.8, 0.75, 0.55))
                    parts.append(carton(bx + ox + 0.05, y0 + 0.25, dz + 0.65, 0.7, 0.65, 0.45))
            parts.append("</g>")
        # front posts of this bay's left edge
        parts.append(cuboid(bx, y1 - pw, 0, pw, pw, TOP, C["post_top"], C["post_l"], C["post_r"]))
    parts.append(cuboid(x0 + bays * BAY - pw, y1 - pw, 0, pw, pw, TOP, C["post_top"], C["post_l"], C["post_r"]))
    # band overlays (tint whole level band on the long face)
    def band(cls, z0, z1, col):
        pts = [iso(x0, y1, z0), iso(x0 + bays * BAY, y1, z0), iso(x0 + bays * BAY, y1, z1), iso(x0, y1, z1)]
        return poly(pts, col, f'class="{cls}" opacity="0" style="mix-blend-mode:multiply"')
    parts.append(band(f"{rid}-res-band", LEVELS[1], TOP, C["reserved"]))
    parts.append(band(f"{rid}-prim-band", 0, LEVELS[1], "#FFD2A1"))
    parts.append(band(f"{rid}-cat-band", 0, TOP, "#FFE9A8"))
    parts.append("</g>")
    return "\n".join(parts)


# ---------------------------------------------------------------- stick figure v2
# Anatomy (scale 1, feet on y=0): head r19 at y-127, neck y-106, hip y-60,
# shoulders at x±12 y-98, upper arm 25 + forearm 23, thigh 30 + shin 29.
OUTFIT = {  # role -> (top, hat)
    "receiver": ("vest", True), "forklift": ("vest", True), "picker": ("vest", True),
    "checker": ("vest", True), "transport": ("vest", True),
    "planner": ("shirt", False), "instructor": ("shirt_tie", False),
    "manager": ("manager", "white"),   # white safety helmet
}
REST = {"armL": (16, -8), "armR": (-16, 8), "legL": (8, -2), "legR": (-8, 2)}


def _limb(fid, side, kind, ang, ang2, extra="", ball=False):
    """Two-segment limb. kind 'arm' or 'leg'. Rotations are SVG degrees (clockwise)."""
    ink = C["ink"]
    if kind == "arm":
        root = (-12 if side == "L" else 12, -98)
        a, b, end = 25, 23, f'<circle cx="0" cy="23" r="4.5" fill="{ink}"/>'
        if ball:   # round "Doraemon" hand: no fingers, for every model and every gesture
            end = f'<circle cx="0" cy="26" r="9" fill="#fff" stroke="{ink}" stroke-width="3.5"/>'
        seg2 = "fore"
    else:
        root = (-3 if side == "L" else 3, -60)
        a, b = 30, 29
        fx = -8 if side == "L" else 8
        end = f'<line x1="0" y1="29" x2="{fx}" y2="30" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
        seg2 = "shin"
    return (f'<g transform="translate({root[0]},{root[1]})"><g id="{fid}-{kind}{side}" transform="rotate({ang})">'
            f'<line x1="0" y1="0" x2="0" y2="{a}" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
            f'<g transform="translate(0,{a})"><g id="{fid}-{seg2}{side}" transform="rotate({ang2})">'
            f'<line x1="0" y1="0" x2="0" y2="{b}" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>{end}{extra}'
            f'</g></g></g></g>')


def folder_svg(col="#16478F"):
    """Document folder held in the left hand (forearm space, hand at y=23). Manager's prop."""
    ink = C["ink"]
    return (f'<g transform="translate(4,22) rotate(-62)">'
            f'<rect x="-4" y="-22" width="34" height="44" rx="3" fill="{col}" stroke="{ink}" stroke-width="2.5"/>'
            f'<rect x="2" y="-16" width="22" height="30" rx="1" fill="#fff"/>'
            f'<rect x="5" y="-11" width="15" height="3" fill="{C["muted"]}"/>'
            f'<rect x="5" y="-4" width="12" height="3" fill="{C["muted"]}"/>'
            f'<rect x="5" y="3" width="15" height="3" fill="{C["muted"]}"/></g>')


MANAGER_HOLD = {"armL": (-8, -118)}  # pose for holding folder_svg() in the left hand


def pda_svg(fid, laser=False, reach=80):
    """PDA held in the right hand (drawn in forearm space, hand at y=23)."""
    las = ""
    if laser:
        las = (f'<g id="{fid}-laser"><line x1="0" y1="30" x2="0" y2="{reach}" stroke="#E53935" stroke-width="3"/>'
               f'<circle cx="0" cy="{reach}" r="10" fill="none" stroke="#E53935" stroke-width="3"/>'
               f'<circle cx="0" cy="{reach}" r="20" fill="none" stroke="#E53935" stroke-width="2" opacity="0.5"/></g>')
    return (f'<g id="{fid}-pda" transform="translate(0,26)">{las}'
            f'<rect x="-11" y="-6" width="22" height="34" rx="4" fill="#2B3646" stroke="{C["ink"]}" stroke-width="2"/>'
            f'<rect x="-7" y="-2" width="14" height="16" rx="1.5" fill="#7FD3FF"/></g>')


def stick(fid, role="picker", scale=1.0, label=False, pose=None, hand_r="", hand_l="", flip=False):
    """Stick figure v2 with feet at (0,0).
    Animatable ids: {fid}-armL/-armR (shoulder), {fid}-foreL/-foreR (elbow),
    {fid}-legL/-legR (hip), {fid}-shinL/-shinR (knee), {fid}-label, {fid}-body.
    pose: dict like REST {limb: (deg, deg2)}; hand_r/hand_l: svg drawn in that forearm."""
    p = dict(REST); p.update(pose or {})
    ink, col = C["ink"], ROLE[role][0]
    top, hat = OUTFIT[role]
    # torso
    if top == "vest":
        body = (f'<line x1="0" y1="-106" x2="0" y2="-60" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
                f'<line x1="-12" y1="-98" x2="12" y2="-98" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M-15,-101 L-3,-104 L-3,-61 L-16,-63 Z" fill="{col}" stroke="{ink}" stroke-width="2.5" stroke-linejoin="round"/>'
                f'<path d="M15,-101 L3,-104 L3,-61 L16,-63 Z" fill="{col}" stroke="{ink}" stroke-width="2.5" stroke-linejoin="round"/>'
                f'<rect x="-15.5" y="-83" width="12.5" height="5" fill="#EEF2F6"/><rect x="3" y="-83" width="12.5" height="5" fill="#EEF2F6"/>'
                f'<rect x="-15.8" y="-72" width="12.8" height="5" fill="#EEF2F6"/><rect x="3" y="-72" width="12.8" height="5" fill="#EEF2F6"/>')
    else:
        tie = ""
        if top == "shirt_tie":
            tie = f'<path d="M0,-102 L-4,-97 L-2,-76 L0,-72 L2,-76 L4,-97 Z" fill="{C["orange"]}" stroke="{ink}" stroke-width="1.5"/>'
        shirt = col
        if top == "manager":  # white shirt, navy tie, ID badge on a navy lanyard
            shirt = "#FFFFFF"
            tie = (f'<path d="M0,-102 L-4.5,-97 L-2.5,-74 L0,-69 L2.5,-74 L4.5,-97 Z" fill="{col}" stroke="{ink}" stroke-width="1.5"/>'
                   f'<path d="M-8,-103 L-10,-86 M8,-103 L10,-86" stroke="{col}" stroke-width="2.2" fill="none"/>'
                   f'<rect x="-14" y="-87" width="9" height="12" rx="1.5" fill="{col}" stroke="{ink}" stroke-width="1.5"/>'
                   f'<rect x="-12.3" y="-84" width="5.6" height="2.4" fill="#fff"/>')
        body = (f'<path d="M-15,-100 Q0,-108 15,-100 L14,-61 Q0,-58 -14,-61 Z" fill="{shirt}" stroke="{ink}" stroke-width="3" stroke-linejoin="round"/>'
                f'<path d="M-7,-104 L0,-96 L7,-104" fill="#fff" stroke="{ink}" stroke-width="2" stroke-linejoin="round"/>{tie}')
    head = (f'<circle cx="0" cy="-127" r="19" fill="#fff" stroke="{ink}" stroke-width="5.5"/>'
            f'<circle cx="-6.5" cy="-129" r="2.8" fill="{ink}"/><circle cx="6.5" cy="-129" r="2.8" fill="{ink}"/>'
            f'<path d="M-6,-119 Q0,-114 6,-119" fill="none" stroke="{ink}" stroke-width="2.6" stroke-linecap="round"/>')
    if hat:
        hcol = "#FFFFFF" if hat == "white" else col
        head += (f'<path d="M-19,-133 Q-19,-152 0,-153 Q19,-152 19,-133 Z" fill="{hcol}" stroke="{ink}" stroke-width="3" stroke-linejoin="round"/>'
                 f'<path d="M-2,-152 L-2,-134 M2,-152 L2,-134" stroke="{ink}" stroke-width="1.5" opacity="0.35"/>'
                 f'<line x1="-24" y1="-133" x2="24" y2="-133" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>')
    lab = ""
    if label:
        txt = ROLE[role][1]
        w = 30 + len(txt) * 14.5
        lab = (f'<g id="{fid}-label"><rect x="{-w/2:.0f}" y="-214" width="{w:.0f}" height="44" rx="22" fill="{ink}"/>'
               f'<text x="0" y="-184" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="24" fill="#fff">{txt}</text>'
               f'<polygon points="-8,-171 8,-171 0,-161" fill="{ink}"/></g>')
    legs = _limb(fid, "L", "leg", *p["legL"]) + _limb(fid, "R", "leg", *p["legR"])
    ball = True   # every model uses round hands: no fingers anywhere
    arms_back = _limb(fid, "L", "arm", *p["armL"], extra=hand_l, ball=ball)
    arms_front = _limb(fid, "R", "arm", *p["armR"], extra=hand_r, ball=ball)
    fl = ' transform="scale(-1,1)"' if flip else ""
    return (f'<g transform="scale({scale})"><g id="{fid}-body"{fl}>'
            f'<ellipse cx="0" cy="3" rx="30" ry="6" fill="#000" opacity="0.10"/>'
            f'{legs}{body}{arms_back}{arms_front}{head}</g>{lab}</g>')


def pose_js(fid, t, pose, dur=0.4, ease="power2.inOut"):
    """Tween a figure to a pose dict {limb: (deg, deg2)} at time t."""
    seg2 = {"armL": "foreL", "armR": "foreR", "legL": "shinL", "legR": "shinR"}
    out = []
    for limb, (a, b) in pose.items():
        out.append(f'tl.to("#{fid}-{limb}",{{rotation:{a},svgOrigin:"0 0",duration:{dur},ease:"{ease}"}},{t});')
        out.append(f'tl.to("#{fid}-{seg2[limb]}",{{rotation:{b},svgOrigin:"0 0",duration:{dur},ease:"{ease}"}},{t});')
    return "\n".join(out) + "\n"


SWAY = 7      # degrees the whole body tips each step
BOB = 5       # px the body lifts mid-step


def walk_js(fid, t0, t1, step=0.32):
    """Walk = the whole figure tips left/right around its feet and bobs slightly.
    Limbs stay in their pose (no leg/arm swing). Move the figure's wrapper separately."""
    out = [f'tl.set("#{fid}-body",{{rotation:0,y:0,transformOrigin:"50% 100%"}},{t0});']
    t, k = t0, 0
    while t + step <= t1 + 1e-6:
        ang = SWAY if k % 2 == 0 else -SWAY
        out.append(f'tl.to("#{fid}-body",{{rotation:{ang},duration:{step/2:.3f},ease:"sine.out"}},{t:.3f});')
        out.append(f'tl.to("#{fid}-body",{{y:-{BOB},duration:{step/2:.3f},ease:"sine.out"}},{t:.3f});')
        out.append(f'tl.to("#{fid}-body",{{rotation:0,y:0,duration:{step/2:.3f},ease:"sine.in"}},{t+step/2:.3f});')
        t += step; k += 1
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- icons (64x64 viewBox)
ICON = {
    "bottle": '<path d="M27 6h10v8l5 8v34a4 4 0 0 1-4 4H26a4 4 0 0 1-4-4V22l5-8z" fill="#4FA3E0" stroke="#1B2430" stroke-width="3" stroke-linejoin="round"/><rect x="22" y="30" width="20" height="12" fill="#fff" stroke="#1B2430" stroke-width="2"/>',
    "noodle": '<path d="M12 22h40l-6 34a4 4 0 0 1-4 3H22a4 4 0 0 1-4-3z" fill="#F2B233" stroke="#1B2430" stroke-width="3" stroke-linejoin="round"/><path d="M10 22h44" stroke="#1B2430" stroke-width="4" stroke-linecap="round"/><path d="M22 18c2-6 6-6 8 0M32 18c2-6 6-6 8 0" fill="none" stroke="#1B2430" stroke-width="3"/><circle cx="32" cy="40" r="7" fill="#E5584F"/>',
    "snack": '<path d="M16 8h32l-3 6 3 6v28l-3 6 3 6H16l3-6-3-6V20l3-6z" fill="#E5584F" stroke="#1B2430" stroke-width="3" stroke-linejoin="round"/><circle cx="32" cy="34" r="9" fill="#F2B233" stroke="#1B2430" stroke-width="2"/>',
    "milk": '<path d="M20 22l6-12h12l6 12v34a3 3 0 0 1-3 3H23a3 3 0 0 1-3-3z" fill="#fff" stroke="#1B2430" stroke-width="3" stroke-linejoin="round"/><path d="M20 22h24" stroke="#1B2430" stroke-width="3"/><rect x="20" y="32" width="24" height="16" fill="#4FA3E0"/>',
    "lock": '<rect x="14" y="28" width="36" height="28" rx="5" fill="#F28C1E" stroke="#1B2430" stroke-width="3"/><circle cx="32" cy="41" r="4" fill="#1B2430"/><rect x="30.5" y="41" width="3" height="8" fill="#1B2430"/>',
    "lock_shackle": '<path d="M21 28V20a11 11 0 0 1 22 0v8" fill="none" stroke="#1B2430" stroke-width="5" stroke-linecap="round"/>',
    "check": '<circle cx="32" cy="32" r="28" fill="#22A55A"/><path d="M19 33l9 9 17-19" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
    "cross": '<circle cx="32" cy="32" r="28" fill="#D93B3B"/><path d="M22 22l20 20M42 22L22 42" stroke="#fff" stroke-width="7" stroke-linecap="round"/>',
}


def icon(name, size=64, extra=""):
    return f'<svg {extra} width="{size}" height="{size}" viewBox="0 0 64 64">{ICON[name]}</svg>'


def mini_rack(highlight):
    """Small flat rack pictogram for cards: highlight 'res' or 'prim'."""
    res = C["reserved"] if highlight == "res" else "#E3E8EF"
    prim = C["orange"] if highlight == "prim" else "#E3E8EF"
    return f'''<svg width="96" height="96" viewBox="0 0 96 96">
<rect x="10" y="8" width="76" height="26" rx="3" fill="{res}"/><rect x="10" y="36" width="76" height="26" rx="3" fill="{res}"/>
<rect x="10" y="64" width="76" height="26" rx="3" fill="{prim}"/>
<path d="M10 4v88M86 4v88M10 34h76M10 62h76M10 90h76" stroke="#1B2430" stroke-width="4" stroke-linecap="round"/></svg>'''
