"""Generate Tập 1 – Tổng quan kho khô.  Run: python3 tools/build_tap1.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, ICON, font_css, iso, rack_row, stick, walk_js, icon, mini_rack, BAY, DEPTH, TOP

OUT = os.path.join(os.path.dirname(__file__), "..", "tap-1-tong-quan")
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)

# ------------------------------------------------------------- timing (abs s)
INTRO = (0, 10)
KHO = (10, 64)
GHINHO = (64, 76)
TOTAL = 76

CAPTIONS = [  # (start, end, text) – the episode script, verbatim, split for reading
    (0.3, 2.6, "Xin chào các bạn."),
    (2.7, 7.2, "Trong loạt video này, chúng ta sẽ cùng tìm hiểu cách kho vận hành,"),
    (7.3, 9.9, "từng bước một, thật đơn giản."),
    (10.3, 13.0, "Kho khô có nhiều dãy kệ."),
    (13.1, 18.6, "Các tầng trên cao gọi là khu Reserved, dùng để lưu trữ hàng."),
    (18.7, 24.6, "Tầng sát mặt đất gọi là khu Primary, hay pick face,"),
    (24.7, 28.0, "là nơi nhân viên lấy hàng."),
    (28.6, 32.6, "Điều quan trọng cần nhớ:"),
    (32.7, 37.7, "mỗi vị trí pick face chỉ chứa một mã hàng duy nhất,"),
    (37.8, 42.6, "và mã hàng đó luôn cố định tại vị trí ấy."),
    (46.6, 50.6, "Mỗi dãy kệ được dành riêng cho một ngành hàng:"),
    (50.7, 53.4, "một dãy cho nước uống,"),
    (53.5, 55.9, "một dãy cho mì,"),
    (56.0, 58.4, "một dãy cho snack,"),
    (58.5, 61.5, "và một dãy cho sữa."),
    (70.5, 75.6, "Nắm được sơ đồ kho rồi, chúng ta sẽ đi tiếp đến bước nhập hàng."),
]

SFX = [  # (abs time, file, volume)
    (0.2, "whoosh.mp3", 0.35),
    (1.3, "pop.mp3", 0.5),
    (10.1, "whoosh-cinematic.mp3", 0.35),
    (13.6, "pop.mp3", 0.5),
    (19.2, "pop.mp3", 0.5),
    (25.9, "click-soft.mp3", 0.5),
    (28.0, "whoosh.mp3", 0.35),
    (33.4, "pop.mp3", 0.5),
    (38.6, "click.mp3", 0.6),
    (38.9, "chime.mp3", 0.4),
    (40.4, "whoosh-short.mp3", 0.4),
    (41.3, "error.mp3", 0.45),
    (44.0, "whoosh.mp3", 0.35),
    (50.9, "pop.mp3", 0.5),
    (53.7, "pop.mp3", 0.5),
    (56.2, "pop.mp3", 0.5),
    (58.8, "pop.mp3", 0.5),
    (64.9, "chime.mp3", 0.35),
    (66.7, "chime.mp3", 0.35),
    (68.5, "chime.mp3", 0.35),
    (70.4, "sparkle.mp3", 0.4),
]

SFX_LEN = {"chime.mp3": 2.54, "click-soft.mp3": 0.36, "click.mp3": 0.36, "error.mp3": 1.61,
           "pop.mp3": 0.72, "sparkle.mp3": 1.8, "whoosh-cinematic.mp3": 5.54,
           "whoosh-short.mp3": 0.57, "whoosh.mp3": 0.57}

BASE_CSS = """
#root{position:absolute;inset:0;overflow:hidden;background:%(ground)s;font-family:%(font)s;color:%(ink)s}
.abs{position:absolute}
""" % {"ground": C["ground"], "font": FONT, "ink": C["ink"]}


def scene(cid, w_html, css, js, duration):
    return f"""<template>
  <style>
{font_css()}
{BASE_CSS}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{duration}">
{w_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


# ============================================================ INTRO
def build_intro():
    rack = rack_row("ir", 0, bays=4)
    html = f"""
    <div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,{C['ground']} 0%,{C['ground']} 62%,{C['floor']} 62%,{C['floor']} 100%)"></div>
    <div id="i-rack" class="abs" style="left:880px;top:-40px;width:1040px;height:900px;opacity:0.32">
      <svg width="1040" height="900" viewBox="560 120 1040 900">{rack}</svg>
    </div>
    <div id="i-text" class="abs" style="left:150px;top:300px;width:900px">
      <div id="i-badge" style="display:inline-block;background:{C['orange']};color:{C['ink']};font-weight:900;font-size:34px;letter-spacing:.06em;padding:10px 26px;border-radius:999px">TẬP 1</div>
      <div id="i-title" style="font-weight:900;font-size:112px;line-height:1.05;margin-top:26px;color:{C['ink']}">Vận hành<br>kho khô</div>
      <div id="i-sub" style="font-weight:700;font-size:56px;margin-top:26px;color:{C['blue']}">Tổng quan kho</div>
      <div id="i-bar" style="width:220px;height:10px;border-radius:5px;background:{C['blue']};margin-top:30px"></div>
    </div>
    <svg id="i-man-svg" class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <g transform="translate(1450,840)"><g id="i-man">{stick("i-man", "instructor", scale=2.4)}</g></g>
    </svg>"""
    js = """
    tl.fromTo("#i-title",{opacity:1,x:-24},{opacity:1,x:0,duration:0.8,ease:"power3.out"},0.0);
    tl.fromTo("#i-badge",{scale:0,opacity:0},{scale:1,opacity:1,duration:0.45,ease:"back.out(2.2)"},1.2);
    tl.fromTo("#i-sub",{opacity:0,y:24},{opacity:1,y:0,duration:0.5,ease:"power2.out"},0.7);
    tl.fromTo("#i-bar",{scaleX:0},{scaleX:1,duration:0.6,ease:"power2.out",transformOrigin:"0% 50%"},1.0);
    tl.fromTo("#i-rack",{x:60},{x:0,duration:9.8,ease:"none"},0);
    tl.fromTo("#i-man",{x:420},{x:0,duration:1.6,ease:"power2.out"},0.1);
""" + walk_js("i-man", 0.1, 1.6) + """
    tl.fromTo("#i-man-armR",{rotation:0},{rotation:-150,duration:0.35,ease:"power2.out",transformOrigin:"50% 0%"},1.75);
    tl.to("#i-man-armR",{rotation:-118,duration:0.26,ease:"sine.inOut",repeat:7,yoyo:true,transformOrigin:"50% 0%"},2.1);
    tl.to("#i-man-armR",{rotation:0,duration:0.4,ease:"power2.inOut",transformOrigin:"50% 0%"},4.3);
    tl.to("#i-man-armL",{rotation:40,duration:0.5,ease:"power2.out",transformOrigin:"50% 0%"},5.0);
    tl.to("#i-man-armL",{rotation:0,duration:0.5,ease:"power2.inOut",transformOrigin:"50% 0%"},8.6);
"""
    return scene("intro", html, "", js, INTRO[1] - INTRO[0])


# ============================================================ KHO (one continuous take)
ROWS = [("r1", 0.0, "bottle", "Dãy Nước uống"), ("r2", 5.0, "noodle", "Dãy Mì"),
        ("r3", 10.0, "snack", "Dãy Snack"), ("r4", 15.0, "milk", "Dãy Sữa")]
WORLD_W, WORLD_H = 1700, 1350
USABLE_CY = 450  # vertical centre of the frame above the caption band


def frame(cx, cy, s, sx=960, sy=USABLE_CY):
    return {"x": round(sx - s * cx, 1), "y": round(sy - s * cy, 1), "scale": s}


def to_screen(f, p):
    return (f["x"] + f["scale"] * p[0], f["y"] + f["scale"] * p[1])


def build_kho():
    y4 = 15.0
    yf = y4 + DEPTH
    # ---- frames
    F_START = frame(1180, 560, 0.66)
    F_ROW4 = frame(560, 950, 1.28, sx=900)
    slot_c = iso(5.0, y4 + 0.55, 0.55)
    F_SLOT = frame(slot_c[0], slot_c[1], 2.7, sx=860, sy=500)
    F_WIDE = frame(840, 735, 0.82)

    # ---- world svg
    w = []
    w.append(f'<rect x="0" y="0" width="{WORLD_W}" height="{WORLD_H}" fill="{C["ground"]}"/>')
    floor = [iso(-6, -3), iso(16, -3), iso(16, 20), iso(-6, 20)]
    w.append('<polygon points="%s" fill="%s"/>' % (" ".join(f"{a:.0f},{b:.0f}" for a, b in floor), C["floor"]))
    for k in range(-6, 17, 2):  # floor grid lines
        a, b = iso(k, -3), iso(k, 20)
        w.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{C["floor_line"]}" stroke-width="2"/>')
    # aisle arrows painted on the floor in front of r4
    for rid, y0, _, _ in ROWS:
        w.append(rack_row(rid, y0))
        if rid == "r4":
            # picker walks in the aisle in front of r4: drawn after r4
            p0 = iso(-6, 17.4)
            w.append(f'<g transform="translate({p0[0]:.1f},{p0[1]:.1f})"><g id="k-pk">{stick("k-pk", "picker", 1.0, label=True)}</g></g>')
    # labels for reserved / primary on r4 (world space, sized for F_ROW4)
    a_res = iso(12, yf, 2.9)
    a_prim = iso(12, yf, 0.55)
    def wlabel(lid, anchor, dx, dy, title, sub, col, txtcol):
        x, y = anchor[0] + dx, anchor[1] + dy
        return (f'<g id="{lid}" opacity="0">'
                f'<line x1="{anchor[0]:.0f}" y1="{anchor[1]:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="{C["ink"]}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>'
                f'<circle cx="{anchor[0]:.0f}" cy="{anchor[1]:.0f}" r="7" fill="{C["ink"]}"/>'
                f'<g transform="translate({x:.0f},{y:.0f})"><g id="{lid}-card">'
                f'<rect x="0" y="-44" width="400" height="92" rx="16" fill="{col}" stroke="{C["ink"]}" stroke-width="3"/>'
                f'<text x="22" y="-6" font-family="{FONT}" font-weight="900" font-size="32" fill="{txtcol}">{title}</text>'
                f'<text x="22" y="32" font-family="{FONT}" font-weight="700" font-size="26" fill="{txtcol}">{sub}</text>'
                f'</g></g></g>')
    w.append(wlabel("k-lres", a_res, 120, -70, "RESERVED", "Lưu kho – tầng trên cao", C["reserved"], C["ink"]))
    w.append(wlabel("k-lprim", a_prim, 120, 40, "PRIMARY", "Pick face – tầng mặt đất", C["orange"], C["ink"]))
    # category signs (world space, sized for F_WIDE)
    for i, (rid, y0, ic, name) in enumerate(ROWS):
        p = iso(6, y0 + 0.55, 4.75)
        sw_, sh_ = 150 + int(len(name) * 27), 112
        w.append(f'<g transform="translate({p[0]-sw_/2:.0f},{p[1]-sh_:.0f})"><g id="k-sign{i+1}" opacity="0">'
                 f'<line x1="{sw_/2-110}" y1="{sh_}" x2="{sw_/2-110}" y2="{sh_+40}" stroke="{C["ink"]}" stroke-width="4"/>'
                 f'<line x1="{sw_/2+110}" y1="{sh_}" x2="{sw_/2+110}" y2="{sh_+40}" stroke="{C["ink"]}" stroke-width="4"/>'
                 f'<rect x="0" y="0" width="{sw_}" height="{sh_}" rx="18" fill="{C["blue"]}" stroke="{C["ink"]}" stroke-width="4"/>'
                 f'<rect x="14" y="14" width="84" height="84" rx="14" fill="#fff"/>'
                 f'<g transform="translate(24,24)">{icon(ic, 64)}</g>'
                 f'<text x="116" y="72" font-family="{FONT}" font-weight="900" font-size="44" fill="#fff">{name}</text>'
                 f'</g></g>')
    world = "\n".join(w)

    # ---- screen-space overlays for the slot close-up (camera holds on F_SLOT)
    tag = to_screen(F_SLOT, iso(5.0, yf, 0.12))
    lock = to_screen(F_SLOT, iso(6.0, yf, 0.9))
    slot_right = to_screen(F_SLOT, iso(6.0, yf, 0.5))
    minis = []
    for ox in (0.15, 1.05):
        minis.append(to_screen(F_SLOT, iso(4.0 + ox + 0.4, y4 + 0.95, 0.3)))
        minis.append(to_screen(F_SLOT, iso(4.0 + ox + 0.4, y4 + 0.9, 0.82)))
    MINI = "".join(f'<div id="k-mini{j+1}" class="abs" style="left:{m[0]-62:.0f}px;top:{m[1]-24:.0f}px;width:124px;opacity:0"><div style="background:#fff;border:3px solid #1B2430;border-radius:10px;text-align:center;font-weight:900;font-size:30px">1001</div></div>' for j, m in enumerate(minis))
    face = [iso(4.0, yf, 0.05), iso(6.0, yf, 0.05), iso(6.0, yf, 1.3), iso(4.0, yf, 1.3)]
    sil = [iso(4.0, yf, 0), iso(6.0, yf, 0), iso(6.0, y4, 0), iso(6.0, y4, 1.32), iso(4.0, y4, 1.32), iso(4.0, yf, 1.32)]
    HOLE = "M0,0H1920V1080H0Z M" + " L".join("%.0f,%.0f" % to_screen(F_SLOT, q) for q in sil) + "Z"
    topright = to_screen(F_SLOT, iso(6.0, y4, 1.32))
    SLOTPTS = " ".join("%.0f,%.0f" % to_screen(F_SLOT, q) for q in face)
    html = f"""
    <div id="k-cam" class="abs" data-layout-allow-overflow style="left:0;top:0;width:{WORLD_W}px;height:{WORLD_H}px">
      <svg width="{WORLD_W}" height="{WORLD_H}" viewBox="0 0 {WORLD_W} {WORLD_H}">{world}</svg>
    </div>
    <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080" data-layout-ignore>
      <path id="k-dim" d="{HOLE}" fill="{C['ground']}" fill-rule="evenodd" opacity="0"/>
      <polygon id="k-slotline" points="{SLOTPTS}" fill="none" stroke="{C['orange']}" stroke-width="8" stroke-linejoin="round" stroke-dasharray="14 12" opacity="0"/>
    </svg>
    <div id="k-head" class="abs" style="left:0;top:70px;width:1920px;text-align:center;opacity:0">
      <span style="display:inline-block;background:#fff;border:4px solid {C['ink']};border-radius:22px;padding:18px 40px;font-weight:900;font-size:60px;box-shadow:0 10px 0 rgba(27,36,48,.12)">1 vị trí = <span style="color:#C45A00">1 mã hàng</span> (cố định)</span>
    </div>
    <div id="k-tag" class="abs" style="left:{tag[0]-150:.0f}px;top:{tag[1]+46:.0f}px;width:300px;opacity:0">
      <div style="background:#fff;border:4px solid {C['ink']};border-radius:14px;padding:10px 0;text-align:center;font-weight:900;font-size:46px">SKU 1001</div>
    </div>
    <div id="k-lock" class="abs" style="left:{topright[0]-40:.0f}px;top:{topright[1]-170:.0f}px;width:150px;height:150px;opacity:0">
      <svg width="150" height="150" viewBox="0 0 64 64"><g id="k-shackle">{ICON['lock_shackle']}</g>{ICON['lock']}</svg>
    </div>
    <div id="k-ok" class="abs" style="left:{topright[0]+90:.0f}px;top:{topright[1]-200:.0f}px;opacity:0">{icon('check', 90)}</div>
    <div id="k-wrong" class="abs" data-layout-allow-overflow style="left:{slot_right[0]+80:.0f}px;top:{slot_right[1]-130:.0f}px;width:240px;height:190px;opacity:0">
      <div style="position:absolute;inset:0;background:{C['box_r']};border:4px solid #A97A44;border-radius:10px"></div>
      <div style="position:absolute;left:96px;top:0;width:48px;height:100%;background:#F3DDB5"></div>
      <div style="position:absolute;left:20px;top:58px;width:200px;background:#fff;border:3px solid {C['ink']};border-radius:10px;text-align:center;font-weight:900;font-size:38px;padding:6px 0">SKU 2002</div>
    </div>
    {MINI}
    <div id="k-no" class="abs" style="left:{slot_right[0]-25:.0f}px;top:{slot_right[1]-90:.0f}px;opacity:0">{icon('cross', 110)}</div>
"""
    def fr(f):
        return "{x:%s,y:%s,scale:%s}" % (f["x"], f["y"], f["scale"])
    pk = lambda x: iso(x, 17.4)
    p0, p1, p2 = pk(-6), pk(5.0), pk(15.0)
    d1 = (p1[0] - p0[0], p1[1] - p0[1])
    d2 = (p2[0] - p0[0], p2[1] - p0[1])
    js = f"""
    // camera: fly in, settle on row 4
    tl.fromTo("#k-cam",{fr(F_START)},{{...{fr(F_ROW4)},duration:6.0,ease:"power2.inOut",transformOrigin:"0% 0%"}},0);
    tl.to("#k-cam",{{scale:{F_ROW4['scale']+0.04},x:{F_ROW4['x']-22},y:{F_ROW4['y']-38},duration:11.8,ease:"none",transformOrigin:"0% 0%"}},6.0);
    // reserved
    tl.fromTo(".r4-res-band",{{opacity:0}},{{opacity:0.95,duration:0.5}},3.4);
    tl.fromTo(".r4-res-hl",{{opacity:0}},{{opacity:0.9,duration:0.5}},3.4);
    tl.fromTo("#k-lres",{{opacity:0}},{{opacity:1,duration:0.3}},3.6);
    tl.fromTo("#k-lres-card",{{scale:0.4}},{{scale:1,duration:0.5,ease:"back.out(2)",transformOrigin:"0% 50%"}},3.6);
    // primary
    tl.fromTo(".r4-prim-band",{{opacity:0}},{{opacity:0.95,duration:0.5}},9.0);
    tl.fromTo(".r4-prim-hl",{{opacity:0}},{{opacity:1,duration:0.5}},9.0);
    tl.fromTo("#k-lprim",{{opacity:0}},{{opacity:1,duration:0.3}},9.2);
    tl.fromTo("#k-lprim-card",{{scale:0.4}},{{scale:1,duration:0.5,ease:"back.out(2)",transformOrigin:"0% 50%"}},9.2);
    tl.to(".r4-res-hl",{{opacity:0.35,duration:0.5}},9.0);
    // picker takes a carton from the pick face
    tl.fromTo("#k-pk",{{x:0,y:0}},{{x:{d1[0]:.1f},y:{d1[1]:.1f},duration:2.4,ease:"power1.inOut"}},12.6);
    tl.fromTo("#k-pk-label",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.4,ease:"back.out(2)"}},12.8);
""" + walk_js("k-pk", 12.6, 15.0) + f"""
    tl.fromTo("#k-pk-armR",{{rotation:0}},{{rotation:-140,duration:0.45,ease:"power2.out",transformOrigin:"50% 0%"}},15.2);
    tl.to("#k-pk-armR",{{rotation:-70,duration:0.4,ease:"power2.inOut",transformOrigin:"50% 0%"}},15.9);
    tl.fromTo("#k-pk-box",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)",transformOrigin:"50% 50%"}},15.9);
    tl.to("#k-pk-armL",{{rotation:-70,duration:0.3,transformOrigin:"50% 0%"}},16.0);
    tl.fromTo("#k-pk",{{x:{d1[0]:.1f},y:{d1[1]:.1f}}},{{x:{d2[0]:.1f},y:{d2[1]:.1f},duration:2.6,ease:"power1.in",immediateRender:false}},16.5);
    tl.fromTo("#k-pk-legL",{{rotation:22}},{{rotation:-22,duration:0.32,repeat:7,yoyo:true,ease:"sine.inOut",transformOrigin:"50% 0%",immediateRender:false}},16.5);
    tl.fromTo("#k-pk-legR",{{rotation:-22}},{{rotation:22,duration:0.32,repeat:7,yoyo:true,ease:"sine.inOut",transformOrigin:"50% 0%",immediateRender:false}},16.5);
    tl.to("#k-pk",{{opacity:0,duration:0.3}},19.0);
    // ---- slot close-up
    tl.to(["#k-lres","#k-lprim",".r4-res-band",".r4-prim-band"],{{opacity:0,duration:0.4}},17.7);
    tl.to("#k-cam",{{...{fr(F_SLOT)},duration:2.5,ease:"power2.inOut",transformOrigin:"0% 0%"}},18.0);
    tl.fromTo("#k-tag",{{opacity:0,y:20,scale:0.6}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(2)"}},23.4);
    tl.fromTo("#k-head",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},23.7);
    tl.fromTo("#k-dim",{{opacity:0}},{{opacity:0.72,duration:0.6}},20.6);
    tl.to("#k-dim",{{opacity:0,duration:0.5}},33.5);
    tl.fromTo(["#k-mini1","#k-mini2","#k-mini3","#k-mini4"],{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)",stagger:0.45}},24.6);
    tl.to(["#k-mini1","#k-mini2","#k-mini3","#k-mini4"],{{opacity:0,duration:0.4}},33.5);
    tl.fromTo("#k-slotline",{{opacity:0,strokeDashoffset:0}},{{opacity:1,strokeDashoffset:-104,duration:2.6,ease:"none"}},25.5);
    tl.to("#k-slotline",{{opacity:0,duration:0.4}},33.5);
    tl.fromTo("#k-lock",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2)"}},28.2);
    tl.fromTo("#k-shackle",{{y:-9}},{{y:0,duration:0.18,ease:"power3.in"}},28.5);
    tl.fromTo("#k-ok",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:0,duration:0.3,ease:"power3.out"}},28.85);
    tl.fromTo("#k-wrong",{{opacity:0,x:900,rotation:8}},{{opacity:1,x:0,rotation:-4,duration:0.8,ease:"power2.in"}},30.4);
    tl.fromTo("#k-no",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(3)"}},31.25);
    tl.to("#k-wrong",{{x:700,y:-60,rotation:14,duration:0.9,ease:"power2.out"}},31.35);
    tl.to("#k-wrong",{{opacity:0,duration:0.3}},31.95);
    tl.to("#k-no",{{opacity:0,duration:0.3}},32.9);
    tl.to(["#k-head","#k-tag","#k-lock","#k-ok"],{{opacity:0,duration:0.4}},33.5);
    // ---- pull back: whole warehouse, category rows
    tl.to("#k-cam",{{...{fr(F_WIDE)},duration:2.6,ease:"power2.inOut",transformOrigin:"0% 0%"}},34.0);
    tl.to(".r4-res-hl",{{opacity:0,duration:0.6}},34.0);
    tl.to(".r4-prim-hl",{{opacity:0,duration:0.6}},34.0);
    tl.to("#k-cam",{{scale:{F_WIDE['scale']+0.03},x:{F_WIDE['x']-25},y:{F_WIDE['y']-22},duration:17.4,ease:"none",transformOrigin:"0% 0%"}},36.6);
"""
    for i, t in enumerate((40.9, 43.7, 46.2, 48.8)):
        js += (f'    tl.fromTo("#k-sign{i+1}",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:0.55,ease:"back.out(1.8)"}},{t});\n'
               f'    tl.fromTo(".r{i+1}-cat-band",{{opacity:0}},{{opacity:0.95,duration:0.5}},{t});\n')
    return scene("kho", html, "", js, KHO[1] - KHO[0])


# ============================================================ GHI NHO
def build_ghinho():
    rows = [
        (mini_rack("res"), "Trên cao = <b style='color:#3B7DD8'>Reserved</b> (lưu kho)"),
        (mini_rack("prim"), "Mặt đất = <b style='color:#C45A00'>Primary</b> (pick face)"),
        (f"<div style='width:96px;height:96px;display:flex;align-items:center;justify-content:center'>{icon('lock', 88)}</div>",
         "1 vị trí pick face = <b>1 mã hàng</b> cố định"),
    ]
    items = ""
    for i, (ic, txt) in enumerate(rows):
        items += (f'<div id="g-row{i+1}" style="display:flex;align-items:center;gap:30px;height:118px;opacity:0">'
                  f'{ic}<div style="font-size:42px;font-weight:700;flex:1;white-space:nowrap">{txt}</div>'
                  f'<div id="g-ok{i+1}" style="opacity:0">{icon("check", 58)}</div></div>')
    html = f"""
    <div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,{C['ground']} 0%,{C['ground']} 74%,{C['floor']} 74%,{C['floor']} 100%)"></div>
    <div id="g-card" class="abs" style="left:150px;top:96px;width:1090px;height:574px;background:#fff;border:4px solid {C['ink']};border-radius:30px;box-shadow:0 14px 0 rgba(27,36,48,.10)">
      <div style="padding:40px 56px 0 56px">
        <div style="font-size:72px;font-weight:900">Ghi nhớ</div>
        <div id="g-under" style="width:200px;height:10px;border-radius:5px;background:{C['orange']};margin:8px 0 26px 0"></div>
        {items}
      </div>
    </div>
    <div id="g-next" class="abs" style="left:150px;top:706px;width:1090px;height:96px;border-radius:48px;background:{C['blue']};color:#fff;display:flex;align-items:center;padding:0 40px;font-size:42px;font-weight:700;opacity:0">
      <span style="font-weight:900;color:#FFD08A;margin-right:22px">Tiếp theo ›</span> Tập 2: Nhập hàng &amp; Cất hàng
    </div>
    <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <g transform="translate(1610,840)"><g id="g-man">{stick("g-man", "instructor", scale=2.4)}</g></g>
    </svg>"""
    js = """
    tl.fromTo("#g-card",{opacity:0,y:30},{opacity:1,y:0,duration:0.5,ease:"power2.out"},0.0);
    tl.fromTo("#g-under",{scaleX:0},{scaleX:1,duration:0.5,ease:"power2.out",transformOrigin:"0% 50%"},0.3);
"""
    for i, t in enumerate((0.8, 2.6, 4.4)):
        js += (f'    tl.fromTo("#g-row{i+1}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.45,ease:"power2.out"}},{t});\n'
               f'    tl.fromTo("#g-ok{i+1}",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:0.28,ease:"power3.out"}},{t+0.1:.2f});\n')
    js += """
    tl.fromTo("#g-man-armL",{rotation:0},{rotation:120,duration:0.5,ease:"power2.out",transformOrigin:"50% 0%"},0.6);
    tl.to("#g-man-armL",{rotation:80,duration:0.5,ease:"power2.inOut",transformOrigin:"50% 0%"},6.2);
    tl.fromTo("#g-next",{opacity:0,x:-60},{opacity:1,x:0,duration:0.6,ease:"power3.out"},6.4);
    """
    return scene("ghinho", html, "", js, GHINHO[1] - GHINHO[0])


# ============================================================ CAPTIONS
def build_captions():
    html, js = [], []
    for i, (s, e, t) in enumerate(CAPTIONS):
        cid = f"cap{i+1}"
        html.append(f'    <div id="{cid}" class="clip cap" data-start="{s}" data-duration="{round(e-s,2)}" data-track-index="0"><span id="{cid}-t">{t}</span></div>')
        js.append(f'    tl.fromTo("#{cid}-t",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.2,ease:"power2.out"}},{s});')
        js.append(f'    tl.to("#{cid}-t",{{opacity:0,duration:0.15,ease:"power2.in"}},{round(e-0.15,2)});')
    css = f"""
#root{{background:transparent}}
.cap{{position:absolute;left:0;bottom:84px;width:1920px;text-align:center}}
.cap span{{display:inline-block;max-width:1500px;background:rgba(255,255,255,.94);color:{C['ink']};
  font-weight:700;font-size:54px;line-height:1.3;padding:12px 34px;border-radius:16px;
  box-shadow:0 4px 0 rgba(27,36,48,.10)}}
"""
    return scene("captions", "\n".join(html), css, "\n".join(js), TOTAL)


# ============================================================ ROOT
def build_index():
    sfx, lanes = [], []  # greedy lane packing: one lane unless clips overlap
    for i, (t, f, v) in enumerate(SFX):
        d = SFX_LEN[f]
        for li, end in enumerate(lanes):
            if end <= t:
                lanes[li] = t + d; lane = li; break
        else:
            lanes.append(t + d); lane = len(lanes) - 1
        sfx.append(f'      <audio id="sfx{i+1}" class="clip" src="assets/sfx/{f}" data-start="{t}" data-duration="{d}" data-track-index="{3+lane}" data-volume="{v}"></audio>')
    return f"""<!doctype html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
{font_css()}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1920px; height:1080px; overflow:hidden; background:{C['ground']}; }}
      #root {{ position:relative; width:1920px; height:1080px; font-family:{FONT}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <div id="intro" data-composition-id="intro" data-composition-src="compositions/intro.html" data-start="{INTRO[0]}" data-duration="{INTRO[1]-INTRO[0]}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <div id="kho" data-composition-id="kho" data-composition-src="compositions/kho.html" data-start="{KHO[0]}" data-duration="{KHO[1]-KHO[0]}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <div id="ghinho" data-composition-id="ghinho" data-composition-src="compositions/ghinho.html" data-start="{GHINHO[0]}" data-duration="{GHINHO[1]-GHINHO[0]}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:10"></div>
{chr(10).join(sfx)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


if __name__ == "__main__":
    files = {
        "index.html": build_index(),
        "compositions/intro.html": build_intro(),
        "compositions/kho.html": build_kho(),
        "compositions/ghinho.html": build_ghinho(),
        "compositions/captions.html": build_captions(),
    }
    for p, s in files.items():
        with open(os.path.join(OUT, p), "w", encoding="utf-8") as fh:
            fh.write(s)
        print("wrote", p, len(s))
