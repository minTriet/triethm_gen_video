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
}

FONT = "'Be Vietnam Pro'"

VI_RANGE = ("U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,"
            "U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,"
            "U+1EA0-1EF9,U+20AB")
LATIN_RANGE = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,"
               "U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,"
               "U+2193,U+2212,U+2215,U+FEFF,U+FFFD")


def font_css():
    out = []
    for w in (500, 700, 900):
        for subset, rng in (("vietnamese", VI_RANGE), ("latin", LATIN_RANGE)):
            out.append(
                "@font-face{font-family:'Be Vietnam Pro';font-style:normal;"
                f"font-weight:{w};font-display:block;"
                f"src:url('assets/fonts/be-vietnam-pro-{subset}-{w}-normal.woff2') format('woff2');"
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


# ---------------------------------------------------------------- stick figure
def stick(fid, role="picker", scale=1.0, label=False, carry=False, face_left=False):
    """Stick figure with feet at (0,0). Ids for animation:
    {fid}-legL/-legR (rotate, origin top), {fid}-armL/-armR (origin top),
    {fid}-label, {fid}-box (carried carton, hidden unless carry)."""
    vest = ROLE[role][0]
    flip = ' transform="scale(-1,1)"' if face_left else ""
    k = scale
    sw = 6
    lab = ""
    if label:
        txt = ROLE[role][1]
        w = 26 + len(txt) * 15
        lab = (f'<g id="{fid}-label"><rect x="{-w/2:.0f}" y="-205" width="{w:.0f}" height="44" rx="22" '
               f'fill="{C["ink"]}"/><text x="0" y="-175" text-anchor="middle" font-family="{FONT}" '
               f'font-weight="700" font-size="24" fill="#fff">{txt}</text>'
               f'<polygon points="-8,-162 8,-162 0,-152" fill="{C["ink"]}"/></g>')
    box = (f'<g id="{fid}-box" opacity="{1 if carry else 0}"><rect x="-4" y="-92" width="44" height="34" rx="3" '
           f'fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2"/><rect x="14" y="-92" width="8" height="34" fill="#F3DDB5"/></g>')
    return f'''<g transform="scale({k})"><g{flip}>
  <ellipse cx="0" cy="2" rx="34" ry="7" fill="#000" opacity="0.10"/>
  <line id="{fid}-legL" x1="0" y1="-55" x2="-2" y2="0" stroke="{C["ink"]}" stroke-width="{sw}" stroke-linecap="round"/>
  <line id="{fid}-legR" x1="0" y1="-55" x2="2" y2="0" stroke="{C["ink"]}" stroke-width="{sw}" stroke-linecap="round"/>
  <line x1="0" y1="-55" x2="0" y2="-102" stroke="{C["ink"]}" stroke-width="{sw}" stroke-linecap="round"/>
  <path d="M-15,-100 Q0,-106 15,-100 L13,-60 Q0,-56 -13,-60 Z" fill="{vest}" stroke="{C["ink"]}" stroke-width="3"/>
  <line id="{fid}-armL" x1="0" y1="-96" x2="-3" y2="-52" stroke="{C["ink"]}" stroke-width="{sw}" stroke-linecap="round"/>
  {box}
  <line id="{fid}-armR" x1="0" y1="-96" x2="3" y2="-52" stroke="{C["ink"]}" stroke-width="{sw}" stroke-linecap="round"/>
  <circle cx="0" cy="-122" r="18" fill="#fff" stroke="{C["ink"]}" stroke-width="{sw}"/>
  <circle cx="7" cy="-125" r="2.6" fill="{C["ink"]}"/><circle cx="-5" cy="-125" r="2.6" fill="{C["ink"]}"/>
  <path d="M-4,-115 Q2,-110 8,-115" fill="none" stroke="{C["ink"]}" stroke-width="2.4" stroke-linecap="round"/>
  {lab}
</g></g>'''


def walk_js(fid, t0, t1, step=0.32, amp=24):
    """GSAP lines for a walk cycle between t0 and t1 (finite repeats)."""
    n = max(1, int(round((t1 - t0) / step)))
    return (f'tl.fromTo("#{fid}-legL",{{rotation:{amp}}},{{rotation:-{amp},duration:{step},ease:"sine.inOut",repeat:{n-1},yoyo:true,transformOrigin:"50% 0%"}},{t0});\n'
            f'tl.fromTo("#{fid}-legR",{{rotation:-{amp}}},{{rotation:{amp},duration:{step},ease:"sine.inOut",repeat:{n-1},yoyo:true,transformOrigin:"50% 0%"}},{t0});\n'
            f'tl.fromTo("#{fid}-armL",{{rotation:-{amp*0.8}}},{{rotation:{amp*0.8},duration:{step},ease:"sine.inOut",repeat:{n-1},yoyo:true,transformOrigin:"50% 0%"}},{t0});\n'
            f'tl.to(["#{fid}-legL","#{fid}-legR","#{fid}-armL"],{{rotation:0,duration:0.15,transformOrigin:"50% 0%"}},{t0 + n*step:.2f});\n')


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
