"""Generate the single merged training video (currently: the first ~30 s for approval).
Run: python3 tools/build_video.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import (C, FONT, ICON, ROLE, font_css, iso, rack_row, stick, walk_js, pose_js,
                 REST, icon, DEPTH)

OUT = os.path.join(os.path.dirname(__file__), "..", "video")
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)

PACE = 1.3          # reading text runs 1.3x faster than the base rule
GAP = 0.15          # silence between two captions


def hold(text):
    """Seconds a caption stays: (0.5 s + 0.3 s per word) / PACE, never under 1.5 s."""
    n = len(text.split())
    return round(max(1.5, (0.5 + 0.3 * n) / PACE), 2)


# ------------------------------------------------------------ script (verbatim)
# (start, text). End = start + hold(text).
CAPS = [
    (0.3, "Xin chào các bạn."),
    (None, "Trong loạt video này, chúng ta sẽ cùng tìm hiểu cách kho vận hành,"),
    (None, "từng bước một, thật đơn giản."),
    # --- Phần 1 (kho scene starts 9.6)
    (9.9, "Kho khô có nhiều dãy kệ."),
    (None, "Các tầng trên cao gọi là khu Reserved, dùng để lưu trữ hàng."),
    (None, "Tầng sát mặt đất gọi là khu Primary, hay pick face,"),
    (None, "là nơi nhân viên lấy hàng."),
    (22.3, "Điều quan trọng cần nhớ:"),
    (None, "mỗi vị trí pick face chỉ chứa một mã hàng duy nhất,"),
    (None, "và mã hàng đó luôn cố định tại vị trí ấy."),
]


def timed_caps():
    out, t = [], 0
    for start, text in CAPS:
        s = start if start is not None else round(t + GAP, 2)
        e = round(s + hold(text), 2)
        out.append((s, e, text))
        t = e
    return out


CAPTIONS = timed_caps()
CAP_START = {i + 1: c[0] for i, c in enumerate(CAPTIONS)}

# ------------------------------------------------------------ sections (abs s)
INTRO = (0.0, 8.4)   # runs under the chapter wipe-in
CHAP1 = (8.0, 9.6)
KHO = (9.2, 31.0)    # starts under the chapter wipe-out
TOTAL = KHO[1]

# Sparse sound: key moments only, >= 4 s apart, quiet.
SFX = [
    (8.0, "whoosh.mp3", 0.30),          # chapter card
    (20.6, "whoosh-short.mp3", 0.22),   # camera dives into the pick face
    (27.8, "chime.mp3", 0.28),          # lock confirmed
]
SFX_LEN = {"chime.mp3": 2.54, "whoosh-short.mp3": 0.57, "whoosh.mp3": 0.57}

BASE_CSS = """
#root{position:absolute;inset:0;overflow:hidden;background:%(ground)s;font-family:%(font)s;color:%(ink)s}
.abs{position:absolute}
""" % {"ground": C["ground"], "font": FONT, "ink": C["ink"]}


def scene(cid, body, css, js, duration):
    return f"""<template>
  <style>
{font_css()}
{BASE_CSS}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{duration}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


# ============================================================ INTRO
PARTS = ["Tổng quan kho", "Nhập hàng & Cất hàng", "Đơn hàng & Châm hàng", "Pick hàng", "Kiểm hàng & Bàn giao"]


def build_intro():
    rack = rack_row("ir", 0, bays=4)
    chips = "".join(
        f'<div id="i-chip{i+1}" style="display:flex;align-items:center;gap:14px;margin-top:14px;opacity:0">'
        f'<span style="display:inline-flex;width:54px;height:54px;border-radius:14px;background:{C["blue"] if i else C["orange"]};color:{"#fff" if i else C["ink"]};'
        f'font-weight:900;font-size:30px;align-items:center;justify-content:center">{i+1}</span>'
        f'<span style="font-size:34px;font-weight:700">{p}</span></div>' for i, p in enumerate(PARTS))
    body = f"""
    <div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,{C['ground']} 0%,{C['ground']} 70%,{C['floor']} 70%,{C['floor']} 100%)"></div>
    <div id="i-rack" class="abs" style="left:920px;top:-60px;width:1040px;height:900px;opacity:0.28">
      <svg width="1040" height="900" viewBox="560 120 1040 900">{rack}</svg>
    </div>
    <div class="abs" style="left:150px;top:120px;width:900px">
      <div id="i-title" style="font-weight:900;font-size:104px;line-height:1.05;color:{C['ink']}">Vận hành<br>kho khô</div>
      <div id="i-bar" style="width:200px;height:10px;border-radius:5px;background:{C['orange']};margin:26px 0 20px 0"></div>
      {chips}
    </div>
    <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <g transform="translate(1440,880)"><g id="i-man">{stick("i-man", "instructor", scale=2.5)}</g></g>
    </svg>"""
    js = """
    tl.fromTo("#i-title",{opacity:1,x:-24},{opacity:1,x:0,duration:0.6,ease:"power3.out"},0.0);
    tl.fromTo("#i-bar",{scaleX:0},{scaleX:1,duration:0.5,ease:"power2.out",transformOrigin:"0% 50%"},0.3);
    tl.fromTo("#i-rack",{x:50},{x:0,duration:7.9,ease:"none"},0);
"""
    for i in range(5):
        js += f'    tl.fromTo("#i-chip{i+1}",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:0.35,ease:"power2.out"}},{0.6 + i*0.22:.2f});\n'
    js += '    tl.fromTo("#i-man",{x:460},{x:0,duration:1.5,ease:"power1.out"},0.1);\n'
    js += walk_js("i-man", 0.1, 1.6)
    js += pose_js("i-man", 1.7, {"armR": (-150, -24)}, dur=0.3, ease="power2.out")
    for k in range(4):  # wave: forearm only
        js += f'    tl.to("#i-man-foreR",{{rotation:{-50 if k % 2 == 0 else -5},svgOrigin:"0 0",duration:0.22,ease:"sine.inOut"}},{2.0 + k*0.22:.2f});\n'
    js += pose_js("i-man", 3.0, {"armR": REST["armR"]}, dur=0.35)
    js += pose_js("i-man", 4.6, {"armL": (128, -10)}, dur=0.35, ease="power2.out")  # points at the parts list
    js += pose_js("i-man", 7.2, {"armL": REST["armL"]}, dur=0.3)
    return scene("intro", body, "", js, round(INTRO[1] - INTRO[0], 2))


# ============================================================ CHAPTER CARD
def build_chapter(cid, num, title):
    body = f"""
    <div id="{cid}-bg" class="abs" style="left:0;top:0;width:1920px;height:1080px;background:{C['blue']}"></div>
    <div id="{cid}-txt" class="abs" style="left:150px;top:380px;width:1600px;color:#fff">
      <div style="font-size:40px;font-weight:700;color:#FFD08A;letter-spacing:.08em">PHẦN {num}</div>
      <div style="font-size:120px;font-weight:900;line-height:1.1;margin-top:10px">{title}</div>
    </div>"""
    d = CHAP1[1] - CHAP1[0]
    js = f"""
    tl.fromTo("#{cid}-bg",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.35,ease:"power3.out"}},0);
    tl.fromTo("#{cid}-txt",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.35,ease:"power3.out"}},0.2);
    tl.to("#{cid}-bg",{{clipPath:"inset(0 0 0 100%)",duration:0.35,ease:"power3.in"}},{d-0.35:.2f});
    tl.to("#{cid}-txt",{{opacity:0,x:40,duration:0.25,ease:"power2.in"}},{d-0.4:.2f});
"""
    return scene(cid, body, "#root{background:transparent}", js, round(d, 2))


# ============================================================ PART 1 – KHO
ROWS = [("r1", 0.0), ("r2", 5.0), ("r3", 10.0), ("r4", 15.0)]
PAD = 600   # extra world on the left, so walkers never leave the drawing
WORLD_W, WORLD_H = 1700 + PAD, 1350
USABLE_CY = 450


def frame(cx, cy, s, sx=960, sy=USABLE_CY):
    return {"x": round(sx - s * (cx + PAD), 1), "y": round(sy - s * cy, 1), "scale": s}


def to_screen(f, p):
    return (f["x"] + f["scale"] * (p[0] + PAD), f["y"] + f["scale"] * p[1])


def fr(f):
    return "{x:%s,y:%s,scale:%s}" % (f["x"], f["y"], f["scale"])


CARRY = {"armL": (34, -104), "armR": (-34, 104)}


def build_kho():
    T0 = KHO[0]
    L = lambda abs_t: round(abs_t - T0, 2)        # abs -> local time
    y4 = 15.0
    yf = y4 + DEPTH
    F_START = frame(1180, 560, 0.66)
    F_ROW4 = frame(560, 950, 1.28, sx=900)
    slot_c = iso(5.0, y4 + 0.55, 0.55)
    F_SLOT = frame(slot_c[0], slot_c[1], 2.7, sx=860, sy=500)

    w = [f'<rect x="{-PAD}" y="0" width="{WORLD_W}" height="{WORLD_H}" fill="{C["ground"]}"/>']
    floor = [iso(-16, -3), iso(16, -3), iso(16, 26), iso(-16, 26)]
    w.append('<polygon points="%s" fill="%s"/>' % (" ".join(f"{a:.0f},{b:.0f}" for a, b in floor), C["floor"]))
    for k in range(-16, 17, 2):
        a, b = iso(k, -3), iso(k, 26)
        w.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{C["floor_line"]}" stroke-width="2"/>')
    for rid, y0 in ROWS:
        w.append(rack_row(rid, y0))
    p0 = iso(-6, 17.4)
    carton = (f'<g id="k-pk-carton" opacity="0"><rect x="-30" y="-100" width="60" height="42" rx="3" fill="{C["box_r"]}" stroke="#A97A44" stroke-width="2.5"/>'
              f'<rect x="-6" y="-100" width="12" height="42" fill="#F3DDB5"/></g>')
    w.append(f'<g transform="translate({p0[0]:.1f},{p0[1]:.1f})"><g id="k-pk">{stick("k-pk", "picker", 1.1, label=True)}'
             f'<g transform="scale(1.1)">{carton}</g></g></g>')

    def wlabel(lid, anchor, dx, dy, title, sub, col):
        x, y = anchor[0] + dx, anchor[1] + dy
        return (f'<g id="{lid}" opacity="0">'
                f'<line x1="{anchor[0]:.0f}" y1="{anchor[1]:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="{C["ink"]}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>'
                f'<circle cx="{anchor[0]:.0f}" cy="{anchor[1]:.0f}" r="7" fill="{C["ink"]}"/>'
                f'<g transform="translate({x:.0f},{y:.0f})"><g id="{lid}-card">'
                f'<rect x="0" y="-44" width="400" height="92" rx="16" fill="{col}" stroke="{C["ink"]}" stroke-width="3"/>'
                f'<text x="22" y="-6" font-family="{FONT}" font-weight="900" font-size="32" fill="{C["ink"]}">{title}</text>'
                f'<text x="22" y="32" font-family="{FONT}" font-weight="700" font-size="26" fill="{C["ink"]}">{sub}</text>'
                f'</g></g></g>')
    w.append(wlabel("k-lres", iso(12, yf, 2.9), 120, -70, "RESERVED", "Lưu kho – tầng trên cao", C["reserved"]))
    w.append(wlabel("k-lprim", iso(12, yf, 0.55), 120, 40, "PRIMARY", "Pick face – tầng mặt đất", C["orange"]))
    world = "\n".join(w)

    tag = to_screen(F_SLOT, iso(5.0, yf, 0.12))
    slot_right = to_screen(F_SLOT, iso(6.0, yf, 0.5))
    topright = to_screen(F_SLOT, iso(6.0, y4, 1.32))
    sil = [iso(4.0, yf, 0), iso(6.0, yf, 0), iso(6.0, y4, 0), iso(6.0, y4, 1.32), iso(4.0, y4, 1.32), iso(4.0, yf, 1.32)]
    hole = "M0,0H1920V1080H0Z M" + " L".join("%.0f,%.0f" % to_screen(F_SLOT, q) for q in sil) + "Z"
    face = [iso(4.0, yf, 0.05), iso(6.0, yf, 0.05), iso(6.0, yf, 1.3), iso(4.0, yf, 1.3)]
    slotpts = " ".join("%.0f,%.0f" % to_screen(F_SLOT, q) for q in face)
    minis = []
    for ox in (0.15, 1.05):
        minis.append(to_screen(F_SLOT, iso(4.0 + ox + 0.4, y4 + 0.95, 0.3)))
        minis.append(to_screen(F_SLOT, iso(4.0 + ox + 0.4, y4 + 0.9, 0.82)))
    mini = "".join(f'<div id="k-mini{j+1}" class="abs" style="left:{m[0]-62:.0f}px;top:{m[1]-24:.0f}px;width:124px;opacity:0"><div style="background:#fff;border:3px solid {C["ink"]};border-radius:10px;text-align:center;font-weight:900;font-size:30px">1001</div></div>' for j, m in enumerate(minis))

    body = f"""
    <div id="k-cam" class="abs" data-layout-allow-overflow style="left:0;top:0;width:{WORLD_W}px;height:{WORLD_H}px">
      <svg width="{WORLD_W}" height="{WORLD_H}" viewBox="{-PAD} 0 {WORLD_W} {WORLD_H}">{world}</svg>
    </div>
    <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080" data-layout-ignore>
      <path id="k-dim" d="{hole}" fill="{C['ground']}" fill-rule="evenodd" opacity="0"/>
      <polygon id="k-slotline" points="{slotpts}" fill="none" stroke="{C['orange']}" stroke-width="8" stroke-linejoin="round" stroke-dasharray="14 12" opacity="0"/>
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
    {mini}
    <div id="k-no" class="abs" style="left:{slot_right[0]-25:.0f}px;top:{slot_right[1]-90:.0f}px;opacity:0">{icon('cross', 110)}</div>
"""
    pk = lambda x: iso(x, 17.4)
    a0, a1, a2 = pk(-6), pk(5.0), pk(15.0)
    d1 = (a1[0] - a0[0], a1[1] - a0[1])
    d2 = (a2[0] - a0[0], a2[1] - a0[1])
    t_res, t_prim = L(12.2), L(15.6)
    t_walk, t_reach, t_take, t_off = L(15.8), L(18.7), L(19.2), L(19.6)
    t_zoom = L(20.6)
    t_mini, t_tag, t_head = L(24.1), L(24.6), L(24.8)
    t_lock, t_wrong = L(27.4), L(28.4)
    js = f"""
    tl.fromTo("#k-cam",{fr(F_START)},{{...{fr(F_ROW4)},duration:4.0,ease:"power2.inOut",transformOrigin:"0% 0%"}},0);
    tl.to("#k-cam",{{scale:{F_ROW4['scale']+0.03},x:{F_ROW4['x']-18},y:{F_ROW4['y']-30},duration:{t_zoom-4.0:.2f},ease:"none",transformOrigin:"0% 0%"}},4.0);
    tl.fromTo(".r4-res-band",{{opacity:0}},{{opacity:0.95,duration:0.4}},{t_res});
    tl.fromTo(".r4-res-hl",{{opacity:0}},{{opacity:0.9,duration:0.4}},{t_res});
    tl.fromTo("#k-lres",{{opacity:0}},{{opacity:1,duration:0.25}},{t_res+0.15:.2f});
    tl.fromTo("#k-lres-card",{{scale:0.4}},{{scale:1,duration:0.4,ease:"back.out(2)",transformOrigin:"0% 50%"}},{t_res+0.15:.2f});
    tl.fromTo(".r4-prim-band",{{opacity:0}},{{opacity:0.95,duration:0.4}},{t_prim});
    tl.fromTo(".r4-prim-hl",{{opacity:0}},{{opacity:1,duration:0.4}},{t_prim});
    tl.fromTo("#k-lprim",{{opacity:0}},{{opacity:1,duration:0.25}},{t_prim+0.15:.2f});
    tl.fromTo("#k-lprim-card",{{scale:0.4}},{{scale:1,duration:0.4,ease:"back.out(2)",transformOrigin:"0% 50%"}},{t_prim+0.15:.2f});
    tl.to(".r4-res-hl",{{opacity:0.35,duration:0.4}},{t_prim});
    // picker: sway-walk in, reach the pick face, take a carton, sway-walk out
    tl.fromTo("#k-pk",{{x:0,y:0,opacity:1}},{{x:{d1[0]:.1f},y:{d1[1]:.1f},duration:{t_reach-0.1-t_walk:.2f},ease:"none"}},{t_walk});
    tl.fromTo("#k-pk-label",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t_walk+0.1:.2f});
""" + walk_js("k-pk", t_walk, t_reach - 0.1) + pose_js("k-pk", t_reach, {"armR": (-140, -10)}, dur=0.3, ease="power2.out") \
      + pose_js("k-pk", t_take, CARRY, dur=0.3) + f"""
    tl.fromTo("#k-pk-carton",{{opacity:0}},{{opacity:1,duration:0.2}},{t_take+0.1:.2f});
    tl.to("#k-pk",{{x:{d2[0]:.1f},y:{d2[1]:.1f},duration:2.0,ease:"none"}},{t_off});
""" + walk_js("k-pk", t_off, t_off + 2.0) + f"""
    tl.to("#k-pk",{{opacity:0,duration:0.3}},{t_off+1.7:.2f});
    // dive into one pick face
    tl.to(["#k-lres","#k-lprim",".r4-res-band",".r4-prim-band"],{{opacity:0,duration:0.3}},{t_zoom-0.2:.2f});
    tl.to("#k-cam",{{...{fr(F_SLOT)},duration:1.8,ease:"power2.inOut",transformOrigin:"0% 0%"}},{t_zoom});
    tl.fromTo("#k-dim",{{opacity:0}},{{opacity:0.72,duration:0.5}},{t_zoom+1.8:.2f});
    tl.fromTo(["#k-mini1","#k-mini2","#k-mini3","#k-mini4"],{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.4)",stagger:0.3}},{t_mini});
    tl.fromTo("#k-tag",{{opacity:0,y:20,scale:0.6}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"back.out(2)"}},{t_tag});
    tl.fromTo("#k-head",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{t_head});
    tl.fromTo("#k-slotline",{{opacity:0,strokeDashoffset:0}},{{opacity:1,strokeDashoffset:-104,duration:2.4,ease:"none"}},{t_head+0.6:.2f});
    tl.fromTo("#k-lock",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{t_lock});
    tl.fromTo("#k-shackle",{{y:-9}},{{y:0,duration:0.16,ease:"power3.in"}},{t_lock+0.25:.2f});
    tl.fromTo("#k-ok",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:0,duration:0.28,ease:"power3.out"}},{t_lock+0.4:.2f});
    tl.fromTo("#k-wrong",{{opacity:0,x:900,rotation:8}},{{opacity:1,x:0,rotation:-4,duration:0.7,ease:"power2.in"}},{t_wrong});
    tl.fromTo("#k-no",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.28,ease:"back.out(3)"}},{t_wrong+0.75:.2f});
    tl.to("#k-wrong",{{x:700,y:-60,rotation:14,duration:0.8,ease:"power2.out"}},{t_wrong+0.85:.2f});
    tl.to("#k-wrong",{{opacity:0,duration:0.25}},{t_wrong+1.35:.2f});
"""
    return scene("kho", body, "", js, round(KHO[1] - KHO[0], 2))


# ============================================================ CAPTIONS
def build_captions():
    html, js = [], []
    for i, (s, e, t) in enumerate(CAPTIONS):
        cid = f"cap{i+1}"
        html.append(f'    <div id="{cid}" class="clip cap" data-start="{s}" data-duration="{round(e-s,2)}" data-track-index="0"><span id="{cid}-t">{t}</span></div>')
        js.append(f'    tl.fromTo("#{cid}-t",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.18,ease:"power2.out"}},{s});')
        js.append(f'    tl.to("#{cid}-t",{{opacity:0,duration:0.12,ease:"power2.in"}},{round(e-0.12,2)});')
    css = f"""
#root{{background:transparent}}
.cap{{position:absolute;left:0;bottom:84px;width:1920px;text-align:center}}
.cap span{{display:inline-block;max-width:1500px;background:rgba(255,255,255,.94);color:{C['ink']};
  font-weight:700;font-size:54px;line-height:1.3;padding:12px 34px;border-radius:16px;
  box-shadow:0 4px 0 rgba(27,36,48,.10)}}
"""
    return scene("captions", "\n".join(html), css, "\n".join(js), TOTAL)


# ============================================================ ROOT
def host(cid, rng, track=0, kind="graphics", extra=""):
    return (f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
            f'data-start="{rng[0]}" data-duration="{round(rng[1]-rng[0],2)}" data-track-index="{track}" '
            f'data-track-kind="{kind}" data-width="1920" data-height="1080"{extra}></div>')


def build_index():
    sfx = [f'      <audio id="sfx{i+1}" class="clip" src="assets/sfx/{f}" data-start="{t}" data-duration="{SFX_LEN[f]}" data-track-index="3" data-volume="{v}"></audio>'
           for i, (t, f, v) in enumerate(SFX)]
    hosts = [host("intro", INTRO), host("chap1", CHAP1, track=2), host("kho", KHO),
             host("captions", (0, TOTAL), track=1, kind="captions", extra=' style="z-index:10"')]
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
      #chap1 {{ z-index:5; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
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
        "compositions/chap1.html": build_chapter("chap1", 1, "Tổng quan kho"),
        "compositions/kho.html": build_kho(),
        "compositions/captions.html": build_captions(),
    }
    for p, s in files.items():
        with open(os.path.join(OUT, p), "w", encoding="utf-8") as fh:
            fh.write(s)
    for s, e, t in CAPTIONS:
        print(f"{s:6.2f}-{e:6.2f}  {t}")
