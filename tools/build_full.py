"""Build the full single training video into ./video.
Run: python3 tools/build_full.py
Every scene is timed from its captions (reading pace 1.3x). Chapter cards sit
between parts; sound effects are thinned to >= 4 s apart.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, ICON, font_css, iso, rack_row, stick, walk_js, pose_js, REST, icon, mini_rack, DEPTH
import stage as st

OUT = os.path.join(os.path.dirname(__file__), "..", "video")
PACE, GAP = 1.3, 0.15
SFX_MIN_GAP = 4.0
SFX_LEN = {"chime.mp3": 2.54, "whoosh-short.mp3": 0.57, "whoosh.mp3": 0.57, "click-soft.mp3": 0.36,
           "ping.mp3": 0.6, "error.mp3": 1.61, "notification.mp3": 1.0}


def hold(text):
    n = len(text.split())
    return round(max(1.5, (0.5 + 0.3 * n) / PACE), 2)


class Scene:
    def __init__(self, cid, lines, build, lead=0.4, tail=0.8, pre=None, min_hold=None, sfx=None):
        self.cid, self.lines, self.build = cid, lines, build
        self.lead, self.tail = lead, tail
        self.pre, self.min_hold = pre or {}, min_hold or {}
        self.sfx = sfx or []          # [(local t or ("T", i, offset)), file, vol]
        t, self.T, self.E = lead, [], []
        for i, text in enumerate(lines):
            t += self.pre.get(i, 0)
            h = max(hold(text), self.min_hold.get(i, 0))
            self.T.append(round(t, 2)); self.E.append(round(t + h, 2))
            t += h + GAP
        self.D = round((t - GAP if lines else t) + tail, 2)


BASE_CSS = """
#root{position:absolute;inset:0;overflow:hidden;background:%(g)s;font-family:%(f)s;color:%(i)s}
.abs{position:absolute}
""" % {"g": C["ground"], "f": FONT, "i": C["ink"]}


def scene_file(cid, body, css, js, duration):
    return f"""<template>
  <style>
{font_css()}
{BASE_CSS}
{st.PDA_CSS}
{st.BADGE_CSS}
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


# ============================================================ shared builders
PARTS = ["Tổng quan kho", "Nhập hàng & Cất hàng", "Đơn hàng, Phân bổ & Châm hàng", "Pick hàng chẵn & lẻ", "Kiểm hàng & Bàn giao"]


def chapter(num, title):
    cid = f"chap{num}"

    def build(T, D):
        body = f"""
    <div id="{cid}-bg" class="abs" style="left:0;top:0;width:1920px;height:1080px;background:{C['blue']}"></div>
    <div id="{cid}-txt" class="abs" style="left:150px;top:380px;width:1600px;color:#fff">
      <div style="font-size:40px;font-weight:700;color:#FFD08A;letter-spacing:.08em">PHẦN {num}</div>
      <div style="font-size:112px;font-weight:900;line-height:1.1;margin-top:10px">{title}</div>
    </div>"""
        js = f"""
    tl.fromTo("#{cid}-bg",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.35,ease:"power3.out"}},0);
    tl.fromTo("#{cid}-txt",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.35,ease:"power3.out"}},0.2);
    tl.to("#{cid}-bg",{{clipPath:"inset(0 0 0 100%)",duration:0.35,ease:"power3.in"}},{D-0.35:.2f});
    tl.to("#{cid}-txt",{{opacity:0,x:40,duration:0.25,ease:"power2.in"}},{D-0.4:.2f});
"""
        return body, "#root{background:transparent}", js
    s = Scene(cid, [], build, lead=2.2, tail=0)
    s.sfx = [(0.0, "whoosh.mp3", 0.28)]
    s.is_chapter = True
    return s


def ghinho(cid, num, bullets, lines=(), tail=1.4):
    """bullets: list of (icon_html, rich_html, plain_text)."""
    times, t = [], 0.7
    for _, _, plain in bullets:
        times.append(round(t, 2)); t += hold(plain) + 0.25
    lead = t if lines else t

    def build(T, D):
        rows = ""
        for i, (ic, rich, _) in enumerate(bullets):
            rows += (f'<div id="{cid}-row{i+1}" style="display:flex;align-items:center;gap:28px;min-height:118px;opacity:0">'
                     f'<div style="width:96px;display:flex;justify-content:center">{ic}</div><div style="font-size:42px;font-weight:700;flex:1;line-height:1.25">{rich}</div>'
                     f'<div id="{cid}-ok{i+1}" style="opacity:0">{icon("check", 56)}</div></div>')
        body = f"""
    <div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,{C['ground']} 0%,{C['ground']} 76%,{C['floor']} 76%,{C['floor']} 100%)"></div>
    <div id="{cid}-card" class="abs" data-hold style="left:130px;top:80px;width:1180px;background:#fff;border:4px solid {C['ink']};border-radius:30px;box-shadow:0 14px 0 rgba(27,36,48,.10);padding:36px 50px 30px 50px">
      <div style="display:flex;align-items:baseline;gap:22px"><div style="font-size:70px;font-weight:900">Ghi nhớ</div><div style="font-size:34px;font-weight:700;color:{C['muted']}">Phần {num}</div></div>
      <div id="{cid}-under" style="width:200px;height:10px;border-radius:5px;background:{C['orange']};margin:8px 0 18px 0"></div>
      {rows}
    </div>
    <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <g transform="translate(1620,880)"><g id="{cid}-man">{stick(cid + "-man", "instructor", scale=2.4)}</g></g>
    </svg>"""
        js = f"""
    tl.fromTo("#{cid}-card",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.45,ease:"power2.out"}},0.0);
    tl.fromTo("#{cid}-under",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out",transformOrigin:"0% 50%"}},0.25);
""" + pose_js(cid + "-man", 0.5, {"armL": (120, -10)}, dur=0.4, ease="power2.out")
        for i, t0 in enumerate(times):
            js += (f'    tl.fromTo("#{cid}-row{i+1}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:0.35,ease:"power2.out"}},{t0});\n'
                   f'    tl.fromTo("#{cid}-ok{i+1}",{{opacity:0,scale:2}},{{opacity:1,scale:1,duration:0.25,ease:"power3.out"}},{t0+0.15:.2f});\n')
        return body, "", js
    s = Scene(cid, list(lines), build, lead=lead, tail=tail)
    s.sfx = [(times[-1] + 0.15, "chime.mp3", 0.22)]
    return s


def mini_lock():
    return f"<div style='width:96px;height:96px;display:flex;align-items:center;justify-content:center'>{icon('lock', 88)}</div>"


def ic_svg(inner, vb="0 0 64 64", size=88):
    return f'<svg width="{size}" height="{size}" viewBox="{vb}">{inner}</svg>'


# ============================================================ PART 1
def p1_intro():
    lines = ["Xin chào các bạn.",
             "Trong loạt video này, chúng ta sẽ cùng tìm hiểu cách kho vận hành,",
             "từng bước một, thật đơn giản."]

    def build(T, D):
        rack = rack_row("ir", 0, bays=4)
        chips = "".join(
            f'<div id="i-chip{i+1}" style="display:flex;align-items:center;gap:16px;margin-top:14px;opacity:0">'
            f'<span style="display:inline-flex;width:54px;height:54px;border-radius:14px;background:{C["blue"] if i else C["orange"]};color:{"#fff" if i else C["ink"]};'
            f'font-weight:900;font-size:30px;align-items:center;justify-content:center">{i+1}</span>'
            f'<span style="font-size:34px;font-weight:700">{p}</span></div>' for i, p in enumerate(PARTS))
        body = f"""
    <div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(180deg,{C['ground']} 0%,{C['ground']} 70%,{C['floor']} 70%,{C['floor']} 100%)"></div>
    <div id="i-rack" class="abs" style="left:920px;top:-60px;width:1040px;height:900px;opacity:0.28">
      <svg width="1040" height="900" viewBox="560 120 1040 900">{rack}</svg>
    </div>
    <div class="abs" style="left:150px;top:110px;width:900px">
      <div id="i-title" style="font-weight:900;font-size:104px;line-height:1.05">Vận hành<br>kho khô</div>
      <div id="i-bar" style="width:200px;height:10px;border-radius:5px;background:{C['orange']};margin:26px 0 20px 0"></div>
      {chips}
    </div>
    <svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <g transform="translate(1440,880)"><g id="i-man">{stick("i-man", "instructor", scale=2.5)}</g></g>
    </svg>"""
        js = f"""
    tl.fromTo("#i-title",{{opacity:1,x:-24}},{{opacity:1,x:0,duration:0.6,ease:"power3.out"}},0.0);
    tl.fromTo("#i-bar",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out",transformOrigin:"0% 50%"}},0.3);
    tl.fromTo("#i-rack",{{x:50}},{{x:0,duration:{D:.2f},ease:"none"}},0);
"""
        for i in range(5):
            js += f'    tl.fromTo("#i-chip{i+1}",{{opacity:0,x:-24}},{{opacity:1,x:0,duration:0.35,ease:"power2.out"}},{0.6 + i*0.22:.2f});\n'
        js += '    tl.fromTo("#i-man",{x:460},{x:0,duration:1.5,ease:"power1.out"},0.1);\n'
        js += walk_js("i-man", 0.1, 1.6)
        js += pose_js("i-man", 1.7, {"armR": (-150, -24)}, dur=0.3, ease="power2.out")
        for k in range(4):
            js += f'    tl.to("#i-man-foreR",{{rotation:{-50 if k % 2 == 0 else -5},svgOrigin:"0 0",duration:0.22,ease:"sine.inOut"}},{2.0 + k*0.22:.2f});\n'
        js += pose_js("i-man", 3.0, {"armR": REST["armR"]}, dur=0.35)
        js += pose_js("i-man", T[1] + 2.6, {"armL": (128, -10)}, dur=0.35, ease="power2.out")
        js += pose_js("i-man", D - 0.8, {"armL": REST["armL"]}, dur=0.3)
        return body, "", js
    return Scene("intro", lines, build, lead=0.3, tail=0.9)


ROWS = [("r1", 0.0, "bottle", "Dãy Nước uống"), ("r2", 5.0, "noodle", "Dãy Mì"),
        ("r3", 10.0, "snack", "Dãy Snack"), ("r4", 15.0, "milk", "Dãy Sữa")]
PAD = 600
WORLD_W, WORLD_H = 1700 + PAD, 1350
USABLE_CY = 450


def frame(cx, cy, s, sx=960, sy=USABLE_CY):
    return {"x": round(sx - s * (cx + PAD), 1), "y": round(sy - s * cy, 1), "scale": s}


def to_screen(f, p):
    return (f["x"] + f["scale"] * (p[0] + PAD), f["y"] + f["scale"] * p[1])


def fr(f):
    return "{x:%s,y:%s,scale:%s}" % (f["x"], f["y"], f["scale"])


CARRY = {"armL": (34, -104), "armR": (-34, 104)}


def p1_kho():
    lines = ["Kho khô có nhiều dãy kệ.",
             "Các tầng trên cao gọi là khu Reserved, dùng để lưu trữ hàng.",
             "Tầng sát mặt đất gọi là khu Primary, hay pick face,",
             "là nơi nhân viên lấy hàng.",
             "Điều quan trọng cần nhớ:",
             "mỗi vị trí pick face chỉ chứa một mã hàng duy nhất,",
             "và mã hàng đó luôn cố định tại vị trí ấy.",
             "Mỗi dãy kệ được dành riêng cho một ngành hàng:",
             "một dãy cho nước uống,", "một dãy cho mì,", "một dãy cho snack,", "và một dãy cho sữa."]

    def build(T, D):
        y4, yf = 15.0, 15.0 + DEPTH
        F_START = frame(1180, 560, 0.66)
        F_ROW4 = frame(560, 950, 1.28, sx=900)
        slot_c = iso(5.0, y4 + 0.55, 0.55)
        F_SLOT = frame(slot_c[0], slot_c[1], 2.7, sx=860, sy=500)
        F_WIDE = frame(840, 660, 0.76)
        w = [f'<rect x="{-PAD}" y="0" width="{WORLD_W}" height="{WORLD_H}" fill="{C["ground"]}"/>']
        fl = [iso(-16, -3), iso(16, -3), iso(16, 26), iso(-16, 26)]
        w.append('<polygon points="%s" fill="%s"/>' % (" ".join(f"{a:.0f},{b:.0f}" for a, b in fl), C["floor"]))
        for k in range(-16, 17, 2):
            a, b = iso(k, -3), iso(k, 26)
            w.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{C["floor_line"]}" stroke-width="2"/>')
        for rid, y0, _, _ in ROWS:
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
        for i, (rid, y0, ic, name) in enumerate(ROWS):
            p = iso(6, y0 + 0.55, 4.75)
            sw_, sh_ = 150 + int(len(name) * 27), 112
            w.append(f'<g transform="translate({p[0]-sw_/2:.0f},{p[1]-sh_:.0f})"><g id="k-sign{i+1}" opacity="0">'
                     f'<line x1="{sw_/2-90}" y1="{sh_}" x2="{sw_/2-90}" y2="{sh_+40}" stroke="{C["ink"]}" stroke-width="4"/>'
                     f'<line x1="{sw_/2+90}" y1="{sh_}" x2="{sw_/2+90}" y2="{sh_+40}" stroke="{C["ink"]}" stroke-width="4"/>'
                     f'<rect x="0" y="0" width="{sw_}" height="{sh_}" rx="18" fill="{C["blue"]}" stroke="{C["ink"]}" stroke-width="4"/>'
                     f'<rect x="14" y="14" width="84" height="84" rx="14" fill="#fff"/>'
                     f'<g transform="translate(24,24)">{icon(ic, 64)}</g>'
                     f'<text x="116" y="72" font-family="{FONT}" font-weight="900" font-size="44" fill="#fff">{name}</text></g></g>')
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
        a0, a1, a2 = iso(-6, 17.4), iso(5.0, 17.4), iso(15.0, 17.4)
        d1 = (a1[0] - a0[0], a1[1] - a0[1]); d2 = (a2[0] - a0[0], a2[1] - a0[1])
        t_res, t_prim = T[1] + 0.4, T[2] + 0.25
        t_walk, t_reach = T[2] + 0.45, T[3]
        t_take, t_off = T[3] + 0.5, T[3] + 0.9
        t_zoom = T[3] + 1.9
        t_mini, t_tag, t_head = T[5] + 0.1, T[5] + 0.6, T[5] + 0.8
        t_lock, t_wrong = T[6] + 0.1, T[6] + 1.1
        t_back = E6 = T[6] + 2.9
        js = f"""
    tl.fromTo("#k-cam",{fr(F_START)},{{...{fr(F_ROW4)},duration:4.0,ease:"power2.inOut",transformOrigin:"0% 0%"}},0);
    tl.to("#k-cam",{{scale:{F_ROW4['scale']+0.03},x:{F_ROW4['x']-18},y:{F_ROW4['y']-30},duration:{t_zoom-4.0:.2f},ease:"none",transformOrigin:"0% 0%"}},4.0);
    tl.fromTo(".r4-res-band",{{opacity:0}},{{opacity:0.95,duration:0.4}},{t_res:.2f});
    tl.fromTo(".r4-res-hl",{{opacity:0}},{{opacity:0.9,duration:0.4}},{t_res:.2f});
    tl.fromTo("#k-lres",{{opacity:0}},{{opacity:1,duration:0.25}},{t_res+0.15:.2f});
    tl.fromTo("#k-lres-card",{{scale:0.4}},{{scale:1,duration:0.4,ease:"back.out(2)",transformOrigin:"0% 50%"}},{t_res+0.15:.2f});
    tl.fromTo(".r4-prim-band",{{opacity:0}},{{opacity:0.95,duration:0.4}},{t_prim:.2f});
    tl.fromTo(".r4-prim-hl",{{opacity:0}},{{opacity:1,duration:0.4}},{t_prim:.2f});
    tl.fromTo("#k-lprim",{{opacity:0}},{{opacity:1,duration:0.25}},{t_prim+0.15:.2f});
    tl.fromTo("#k-lprim-card",{{scale:0.4}},{{scale:1,duration:0.4,ease:"back.out(2)",transformOrigin:"0% 50%"}},{t_prim+0.15:.2f});
    tl.to(".r4-res-hl",{{opacity:0.35,duration:0.4}},{t_prim:.2f});
    tl.fromTo("#k-pk",{{x:0,y:0,opacity:1}},{{x:{d1[0]:.1f},y:{d1[1]:.1f},duration:{t_reach-0.1-t_walk:.2f},ease:"none"}},{t_walk:.2f});
    tl.fromTo("#k-pk-label",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t_walk+0.1:.2f});
""" + walk_js("k-pk", t_walk, t_reach - 0.1) + pose_js("k-pk", t_reach, {"armR": (-140, -10)}, dur=0.3, ease="power2.out") \
            + pose_js("k-pk", t_take, CARRY, dur=0.3) + f"""
    tl.fromTo("#k-pk-carton",{{opacity:0}},{{opacity:1,duration:0.2}},{t_take+0.1:.2f});
    tl.to("#k-pk",{{x:{d2[0]:.1f},y:{d2[1]:.1f},duration:2.0,ease:"none"}},{t_off:.2f});
""" + walk_js("k-pk", t_off, t_off + 2.0) + f"""
    tl.to("#k-pk",{{opacity:0,duration:0.3}},{t_off+1.7:.2f});
    tl.to(["#k-lres","#k-lprim",".r4-res-band",".r4-prim-band"],{{opacity:0,duration:0.3}},{t_zoom-0.2:.2f});
    tl.to("#k-cam",{{...{fr(F_SLOT)},duration:1.8,ease:"power2.inOut",transformOrigin:"0% 0%"}},{t_zoom:.2f});
    tl.fromTo("#k-dim",{{opacity:0}},{{opacity:0.72,duration:0.5}},{t_zoom+1.8:.2f});
    tl.fromTo(["#k-mini1","#k-mini2","#k-mini3","#k-mini4"],{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.4)",stagger:0.3}},{t_mini:.2f});
    tl.fromTo("#k-tag",{{opacity:0,y:20,scale:0.6}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"back.out(2)"}},{t_tag:.2f});
    tl.fromTo("#k-head",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{t_head:.2f});
    tl.fromTo("#k-slotline",{{opacity:0,strokeDashoffset:0}},{{opacity:1,strokeDashoffset:-104,duration:2.4,ease:"none"}},{t_head+0.6:.2f});
    tl.fromTo("#k-lock",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{t_lock:.2f});
    tl.fromTo("#k-shackle",{{y:-9}},{{y:0,duration:0.16,ease:"power3.in"}},{t_lock+0.25:.2f});
    tl.fromTo("#k-ok",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:0,duration:0.28,ease:"power3.out"}},{t_lock+0.4:.2f});
    tl.fromTo("#k-wrong",{{opacity:0,x:900,rotation:8}},{{opacity:1,x:0,rotation:-4,duration:0.7,ease:"power2.in"}},{t_wrong:.2f});
    tl.fromTo("#k-no",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.28,ease:"back.out(3)"}},{t_wrong+0.75:.2f});
    tl.to("#k-wrong",{{x:700,y:-60,rotation:14,duration:0.8,ease:"power2.out"}},{t_wrong+0.85:.2f});
    tl.to("#k-wrong",{{opacity:0,duration:0.25}},{t_wrong+1.35:.2f});
    // pull back to the whole warehouse: one category per row
    tl.to(["#k-head","#k-tag","#k-lock","#k-ok","#k-no","#k-mini1","#k-mini2","#k-mini3","#k-mini4","#k-slotline","#k-dim"],{{opacity:0,duration:0.3}},{t_back:.2f});
    tl.to("#k-cam",{{...{fr(F_WIDE)},duration:1.8,ease:"power2.inOut",transformOrigin:"0% 0%"}},{t_back:.2f});
    tl.to([".r4-res-hl",".r4-prim-hl"],{{opacity:0,duration:0.4}},{t_back:.2f});
    tl.to("#k-cam",{{scale:{F_WIDE['scale']+0.02},x:{F_WIDE['x']-18},y:{F_WIDE['y']-14},duration:{D-t_back-1.8:.2f},ease:"none",transformOrigin:"0% 0%"}},{t_back+1.8:.2f});
"""
        for i in range(4):
            t = T[8 + i] + 0.15
            js += (f'    tl.fromTo("#k-sign{i+1}",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.8)"}},{t:.2f});\n'
                   f'    tl.fromTo(".r{i+1}-cat-band",{{opacity:0}},{{opacity:0.95,duration:0.4}},{t:.2f});\n')
        return body, "", js
    s = Scene("kho", lines, build, lead=0.7, tail=1.2, pre={4: 1.96, 7: 2.0})
    s.sfx = [(("T", 3, 1.9), "whoosh-short.mp3", 0.22), (("T", 6, 0.5), "chime.mp3", 0.25)]
    return s


def p1_ghinho():
    return ghinho("g1", 1, [
        (mini_rack("res"), "Trên cao = <b style='color:#2F6FD6'>Reserved</b> (lưu kho)", "Trên cao = Reserved (lưu kho)"),
        (mini_rack("prim"), "Mặt đất = <b style='color:#C45A00'>Primary</b> (pick face)", "Mặt đất = Primary (pick face)"),
        (mini_lock(), "1 vị trí pick face = <b>1 mã hàng cố định</b>", "1 vị trí pick face = 1 mã hàng cố định"),
    ], lines=["Nắm được sơ đồ kho rồi, chúng ta sẽ đi tiếp đến bước nhập hàng."])


# ============================================================ assembly
def timeline():
    import parts
    seq = [p1_intro(), chapter(1, PARTS[0]), p1_kho(), p1_ghinho()]
    for n, scenes in ((2, parts.part2), (3, parts.part3), (4, parts.part4), (5, parts.part5)):
        built = scenes()
        if built:
            seq.append(chapter(n, PARTS[n - 1]))
            seq.extend(built)
    return seq


def assemble(seq, limit=None):
    """Lay scenes back to back; a chapter card overlaps 0.35 s into its neighbours."""
    OV = 0.35
    placed, t = [], 0.0
    for i, s in enumerate(seq):
        if getattr(s, "is_chapter", False):
            start = t - OV
            placed.append((s, round(start, 2)))
            t = start + s.D - OV
        else:
            placed.append((s, round(t, 2)))
            t = t + s.D
    total = round(t, 2)
    if limit:
        total = min(total, limit)
    return placed, total


def build_all(limit=None):
    seq = timeline()
    placed, total = assemble(seq, limit)
    os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)
    hosts, caps, sfx = [], [], []
    for s, start in placed:
        if start >= total:
            continue
        body, css, js = s.build(s.T, s.D)
        with open(os.path.join(OUT, "compositions", f"{s.cid}.html"), "w", encoding="utf-8") as fh:
            fh.write(scene_file(s.cid, body, css, js, s.D))
        dur = s.D + (0.35 if not getattr(s, "is_chapter", False) else 0)  # hold under the next chapter wipe
        dur = round(min(dur, total - start), 2)
        z = ' style="z-index:5"' if getattr(s, "is_chapter", False) else ""
        hosts.append(f'      <div id="{s.cid}" data-composition-id="{s.cid}" data-composition-src="compositions/{s.cid}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="{2 if z else 0}" data-track-kind="graphics" '
                     f'data-width="1920" data-height="1080"{z}></div>')
        for a, b, text in zip(s.T, s.E, s.lines):
            if start + a < total:
                caps.append((round(start + a, 2), round(min(start + b, total), 2), text))
        for when, f, v in s.sfx:
            lt = s.T[when[1]] + when[2] if isinstance(when, tuple) else when
            sfx.append((round(start + lt, 2), f, v))
    # thin the sound: keep a cue only if >= SFX_MIN_GAP after the previous kept one
    sfx.sort(); kept, last = [], -99
    for t, f, v in sfx:
        if t - last >= SFX_MIN_GAP and t + SFX_LEN[f] <= total:
            kept.append((t, f, v)); last = t
    # captions composition
    ch, cj = [], []
    for i, (a, b, text) in enumerate(caps):
        cid = f"cap{i+1}"
        ch.append(f'    <div id="{cid}" class="clip cap" data-start="{a}" data-duration="{round(b-a,2)}" data-track-index="0"><span id="{cid}-t">{text}</span></div>')
        cj.append(f'    tl.fromTo("#{cid}-t",{{opacity:0,y:8}},{{opacity:1,y:0,duration:0.18,ease:"power2.out"}},{a});')
        cj.append(f'    tl.to("#{cid}-t",{{opacity:0,duration:0.12,ease:"power2.in"}},{round(b-0.12,2)});')
    ccss = f"""
#root{{background:transparent}}
.cap{{position:absolute;left:0;bottom:84px;width:1920px;text-align:center}}
.cap span{{display:inline-block;max-width:1500px;background:rgba(255,255,255,.94);color:{C['ink']};
  font-weight:700;font-size:54px;line-height:1.3;padding:12px 34px;border-radius:16px;box-shadow:0 4px 0 rgba(27,36,48,.10)}}
"""
    with open(os.path.join(OUT, "compositions", "captions.html"), "w", encoding="utf-8") as fh:
        fh.write(scene_file("captions", "\n".join(ch), ccss, "\n".join(cj), total))
    hosts.append(f'      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" '
                 f'data-duration="{total}" data-track-index="1" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index:10"></div>')
    lanes, audio = [], []
    for i, (t, f, v) in enumerate(kept):
        d = SFX_LEN[f]
        for li, end in enumerate(lanes):
            if end <= t:
                lanes[li] = t + d; lane = li; break
        else:
            lanes.append(t + d); lane = len(lanes) - 1
        audio.append(f'      <audio id="sfx{i+1}" class="clip" src="assets/sfx/{f}" data-start="{t}" data-duration="{d}" data-track-index="{3+lane}" data-volume="{v}"></audio>')
    index = f"""<!doctype html>
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
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
{chr(10).join(audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index)
    # clean stale scene files
    keep = {f"{s.cid}.html" for s, st_ in placed if st_ < total} | {"captions.html"}
    for f in os.listdir(os.path.join(OUT, "compositions")):
        if f.endswith(".html") and f not in keep:
            os.remove(os.path.join(OUT, "compositions", f))
    return placed, total, kept


if __name__ == "__main__":
    limit = float(sys.argv[1]) if len(sys.argv) > 1 else None
    placed, total, kept = build_all(limit)
    for s, start in placed:
        print(f"{start:7.2f}  {s.D:6.2f}  {s.cid}")
    print("TOTAL", total, "sfx", len(kept))
