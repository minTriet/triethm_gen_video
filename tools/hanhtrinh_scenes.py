"""Cảnh màn 05–17 của video "Hành trình tạo kỹ năng làm video" (dùng trong tools/build_hanhtrinh.py).
Bố cục bám storyboard đã duyệt (design/storyboard-hanh-trinh.html); hình vẽ bằng SVG 1920×1080,
nhân vật lấy từ bộ mặc định (skill nhan-vat-kho, tools/kit.py).
"""
import math

import stage as st
from kit import C, stick, walk_js, pose_js, folder_svg, pda_svg, MANAGER_HOLD, REST
from model_sheet import forklift as fl_front, forklift_back as fl_back, trolley as ms_trolley, carton_flat
from parts import svg_layer
from build_hanhtrinh import (VScene, floor_bg, wave_js, pop, rise, esc,
                             INK, MUTED, BLUE, ORANGE, GREEN, ORANGE_D, GREEN_D)

F = "'Be Vietnam Pro'"
_clip = [0]


# ------------------------------------------------------------------ SVG primitives
def T(x, y, s, size=40, w=700, fill=INK, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{w}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def rect(x, y, w, h, fill="#fff", r=16, stroke=None, sw=3, extra=""):
    st_ = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st_} {extra}/>'


def G(gid, inner, hidden=True, extra=""):
    return f'<g id="{gid}"{" opacity=\"0\"" if hidden else ""} {extra}>{inner}</g>'


def pill(cx, cy, s, bg=INK, fg="#fff", size=28, pad=26):
    w = len(s) * size * (0.7 if s.isupper() else 0.58) + pad * 2
    return rect(cx - w / 2, cy - size * 0.95, w, size * 1.9, bg, size * 0.95) + T(cx, cy + size * 0.36, s, size, 700, fg, "middle")


def check(cx, cy, r=34):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GREEN}"/>'
            f'<path d="M{cx - r * .45} {cy + r * .03} l{r * .3} {r * .3} l{r * .55} {r * -.62}" fill="none" '
            f'stroke="#fff" stroke-width="{r * .22}" stroke-linecap="round" stroke-linejoin="round"/>')


def arrow(x1, y1, x2, y2, col=ORANGE_D, sw=7):
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 22 * math.cos(a), y2 - 22 * math.sin(a)
    l, r = a + 2.6, a - 2.6
    return (f'<line x1="{x1}" y1="{y1}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<polygon points="{x2},{y2} {x2 + 24 * math.cos(l):.1f},{y2 + 24 * math.sin(l):.1f} '
            f'{x2 + 24 * math.cos(r):.1f},{y2 + 24 * math.sin(r):.1f}" fill="{col}"/>')


def scr(src, x, y, w, label=None):
    """Ảnh thật trong khung màn hình bo góc 16:9."""
    _clip[0] += 1
    h = w * 9 / 16
    cid = f"hc{_clip[0]}"
    g = (f'<rect x="{x - 10}" y="{y - 10}" width="{w + 20}" height="{h + 20}" rx="18" fill="#2B3646"/>'
         f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/></clipPath>'
         f'<image href="{src}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>')
    if label:
        g += pill(x + w / 2, y + h + 46, label, INK, "#fff", 28)
    return g


def paper(x, y, w, h, title, lines, col=BLUE, faded=False):
    out = (rect(x + 10, y + 12, w, h, "#000", 14, extra='opacity="0.08"') + rect(x, y, w, h, "#fff", 14, INK, 3)
           + rect(x, y, w, 70, col, 14) + rect(x, y + 40, w, 30, col, 0) + T(x + 28, y + 48, title, 30, 800, "#fff"))
    yy = y + 120
    for ln in lines:
        s, c, wt = ln if isinstance(ln, tuple) else (ln, INK, 600)
        out += T(x + 28, yy, s, 29, wt, c)
        yy += 50
    return f'<g opacity="{0.6 if faded else 1}">{out}</g>'


def man(fid, role, x, y, s=1.8, **kw):
    return f'<g transform="translate({x},{y})">{stick(fid, role, s, **kw)}</g>'


# ------------------------------------------------------------------ JS helpers
def show(sel, t, dur=0.3):
    return f'tl.to("{sel}",{{opacity:1,duration:{dur}}},{t:.2f});\n'


def slide(sel, t, dx=-80, dur=0.5):
    return f'tl.fromTo("{sel}",{{opacity:0,x:{dx}}},{{opacity:1,x:0,duration:{dur},ease:"power3.out"}},{t:.2f});\n'


def gpop(sel, t, s0=0.6, dur=0.4):
    """Bật một nhóm SVG ra quanh tâm của nó (svgOrigin tuyệt đối, không làm lệch vị trí)."""
    return ('(function(){const e=document.querySelector("%s");const b=e.getBBox();'
            'const o=(b.x+b.width/2)+" "+(b.y+b.height/2);'
            'tl.fromTo(e,{opacity:0,scale:%s,svgOrigin:o},{opacity:1,scale:1,svgOrigin:o,duration:%s,ease:"back.out(1.8)"},%.2f);})();\n'
            % (sel, s0, dur, t))


def badge(bid, n, text):
    return st.badge(bid, n, text)


def badge_js(bid, D):
    return (f'tl.fromTo("#{bid}",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.25,ease:"power2.out"}},0.1);\n'
            f'tl.fromTo("#{bid}-ok",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.2,ease:"power3.out"}},{D - 0.8:.2f});\n')


def swing(sel, a, b, t0, t1, period=0.45):
    """Lặp một động tác tại chỗ (xoay khớp) từ t0 đến t1, số lần hữu hạn."""
    n = max(1, int((t1 - t0) / period) - 1)
    return (f'tl.fromTo("{sel}",{{rotation:{a}}},{{rotation:{b},svgOrigin:"0 0",duration:{period},yoyo:true,repeat:{n},'
            f'ease:"sine.inOut"}},{t0:.2f});\n')


def bob(sel, prop, val, t0, t1, period=0.45):
    n = max(1, int((t1 - t0) / period) - 1)
    return f'tl.to("{sel}",{{{prop}:{val},duration:{period},yoyo:true,repeat:{n},ease:"sine.inOut"}},{t0:.2f});\n'


def scene(svg, html_top=""):
    return floor_bg() + svg_layer(svg) + html_top


# ================================================================== màn 05 · Bước 2 prompt gốc
def prompt():
    def build(T_, D):
        a = paper(200, 200, 640, 560, "[A] Phong cách chung",
                  ["16:9 · 1920×1080", "Người que, áo màu theo vai", ("Xanh · Cam · Xanh lá", BLUE, 800),
                   "Badge “Bước n”, PDA phóng to", "Cuối tập: thẻ “Ghi nhớ”", "Mỗi cảnh một ý"])
        b = paper(980, 200, 640, 560, "[B] Kịch bản từng tập",
                  [("Tập 1 – Tổng quan kho · 70s", INK, 800), "Cảnh 1 (0–8s): tiêu đề,", "giảng viên vẫy tay",
                   ("VO: “Xin chào các bạn…”", MUTED, 600), "Cảnh 2 (8–25s): bay qua kho", ("… Tập 2 → Tập 5", MUTED, 600)],
                  ORANGE_D)
        svg = (G("pr-a", a) + G("pr-plus", T(910, 500, "+", 110, 900, ORANGE_D, "middle")) + G("pr-b", b)
               + man("pr-man", "instructor", 1770, 830, 1.6, pose={"armL": (22, -70), "armR": (-22, 70)}))
        js = badge_js("pr-bd", D) + slide("#pr-a", T_[0] + 0.9, -100) + gpop("#pr-plus", T_[0] + 1.9)
        js += slide("#pr-b", T_[0] + 2.4, 100) + swing("#pr-man-foreR", 70, 50, 0.5, D - 0.5, 0.3)
        return scene(svg, badge("pr-bd", 2, "Viết prompt gốc")), "", js
    return VScene("prompt", ["c04-1"], build, lead=0.4, tail=2.6)


# ================================================================== màn 06 · Bước 3 outline
def outline():
    lines = [("> Viết OUTLINE.md", "#7FD3FF"), ("## 1. Kế hoạch xử lý", "#FFFFFF"), ("## 2. Thông số chung", "#FFFFFF"),
             ("    Màu  #1F5FBF  #F28C1E  #22A55A", "#F2B233"), ("    Font Be Vietnam Pro · 30 fps", "#F2B233"),
             ("## 3. Outline Tập 1 (5 cảnh)", "#FFFFFF"), ("## 4. Câu hỏi cần chốt", "#FFFFFF")]

    def build(T_, D):
        x, y, w, h = 160, 190, 1060, 600
        term = (rect(x, y, w, h, "#1B2430", 18) + rect(x, y, w, 56, "#2B3646", 18) + rect(x, y + 30, w, 26, "#2B3646", 0)
                + "".join(f'<circle cx="{x + 34 + i * 30}" cy="{y + 28}" r="9" fill="{c}"/>' for i, c in enumerate(["#E5584F", "#F2B233", "#2FAE5F"]))
                + T(x + w / 2, y + 38, "Claude Code", 26, 700, "#AEBBCC", "middle"))
        txt = "".join(G(f"ol-l{i}", T(x + 36, y + 120 + i * 62, s, 32, 600, c, extra='xml:space="preserve"')) for i, (s, c) in enumerate(lines))
        cur = G("ol-cur", rect(x + 36, y + 120 + len(lines) * 62 - 34, 18, 40, "#7FD3FF", 2), hidden=False)
        stamp = (rect(1370, 270, 320, 100, "none", 14, GREEN_D, 8) + T(1530, 338, "ĐÃ DUYỆT", 48, 900, GREEN_D, "middle", 'letter-spacing="3"'))
        svg = (G("ol-term", term + txt + cur) + G("ol-stamp", stamp)
               + G("ol-mang", man("ol-man", "instructor", 1450, 830, 1.9), hidden=False))
        js = rise("#ol-term", 0.2, dy=30)
        for i in range(len(lines)):
            js += f'tl.fromTo("#ol-l{i}",{{opacity:0}},{{opacity:1,duration:0.1}},{0.6 + i * 0.32:.2f});\n'
            js += f'tl.set("#ol-cur",{{y:{-(len(lines) - 1 - i) * 62}}},{0.6 + i * 0.32:.2f});\n'
        for k in range(int(D / 0.5)):
            js += f'tl.set("#ol-cur",{{opacity:{k % 2}}},{0.5 + k * 0.5:.2f});\n'
        ts = T_[0] + 2.4
        js += pose_js("ol-man", ts - 0.3, {"armR": (-150, -20)}, dur=0.3, ease="power2.out")
        js += f'tl.fromTo("#ol-stamp",{{opacity:0,scale:1.8,rotation:-8,svgOrigin:"1530 320"}},{{opacity:1,scale:1,rotation:-8,svgOrigin:"1530 320",duration:0.3,ease:"power3.out"}},{ts:.2f});\n'
        return scene(svg, badge("ol-bd", 3, "Claude lập outline để duyệt")), "", badge_js("ol-bd", D) + js
    s = VScene("outline", ["c05-1"], build, lead=0.4, tail=2.2)
    s.sfx = [(("T", 0, 2.4), "chime.mp3", 0.12)]
    return s


# ================================================================== màn 07 · Bước 4 Tập 1 nháp
def draft():
    def build(T_, D):
        x, y, w = 200, 200, 1000
        h = round(w * 9 / 16)
        notes = ""
        for i in range(4):
            nx, ny = 1330 + (i % 2) * 240, 210 + (i // 2) * 140
            notes += G(f"dr-n{i}", f'<g transform="rotate({-4 + i * 3} {nx + 100} {ny + 50})">' + rect(nx, ny, 210, 104, "#FFE9A8", 6, INK, 2)
                       + T(nx + 105, ny + 64, f"Góp ý {i + 1}", 32, 800, INK, "middle") + "</g>")
        svg = (G("dr-scr", rect(x - 10, y - 10, w + 20, h + 20, "#2B3646", 18) + pill(x + w / 2, y + h + 46, "Tập 1 – bản nháp · 76 giây"))
               + notes + man("dr-man", "instructor", 1520, 830, 1.9, pose={"armL": (95, 5)}))
        vid = (f'<video id="dr-vid" class="clip" src="assets/video/t1draft.mp4" muted playsinline data-start="0.4" '
               f'data-duration="{min(8.9, D - 0.5):.2f}" data-track-index="0" style="position:absolute;left:{x}px;top:{y}px;'
               f'width:{w}px;height:{h}px;object-fit:cover;border-radius:8px"></video>')
        js = badge_js("dr-bd", D) + gpop("#dr-scr", 0.15, 0.9)
        for i in range(4):
            js += gpop(f"#dr-n{i}", T_[0] + 1.4 + i * 0.3, 0.4, 0.3)
        return scene(svg, vid + badge("dr-bd", 4, "Xem Tập 1 bản nháp")), "", js
    return VScene("draft", ["c07-1"], build, lead=0.5, tail=1.5, min_d=7.0)


# ================================================================== màn 08 · Bước 5 bốn luật
def rules():
    R = [("1", "5 tập → 1 video", "Có thẻ chương giữa các phần"), ("2", "Nhịp đọc 1.3×", "(0.5s + 0.3s × số chữ) ÷ 1.3"),
         ("3", "Âm thanh thưa", "Cách nhau ít nhất 4 giây"), ("4", "Nhân vật v2", "Có khớp, áo phản quang")]

    def build(T_, D):
        svg = ""
        for i, (n, t1, t2) in enumerate(R):
            x = 120 + i * 430
            cx, cy = x + 195, 450
            g = rect(x, 200, 390, 580, "#fff", 22, INK, 3) + rect(x, 200, 390, 84, BLUE, 22) + rect(x, 240, 390, 44, BLUE, 0)
            g += T(x + 30, 256, f"LUẬT {n}", 32, 900, "#fff", extra='letter-spacing="2"')
            if n == "1":
                for k in range(5):
                    g += rect(cx - 150 + k * 22, cy - 80 + k * 10, 120, 70, "#E3E8EF", 8, MUTED, 2)
                g += arrow(cx - 10, cy + 10, cx + 50, cy + 10) + rect(cx + 60, cy - 40, 110, 90, BLUE, 10, INK, 3)
            elif n == "2":
                g += T(cx, cy + 30, "1.3×", 120, 900, ORANGE_D, "middle")
            elif n == "3":
                g += (f'<path d="M{cx - 90} {cy - 30} h40 l50 -45 v150 l-50 -45 h-40 z" fill="{BLUE}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
                      + T(cx + 70, cy + 30, "≥4s", 64, 900, INK, "middle"))
            else:
                g += man(f"ru-p{i}", "picker", cx, cy + 110, 1.25)
            g += T(cx, 650, t1, 38, 900, INK, "middle") + T(cx, 712, t2, 26, 600, MUTED, "middle")
            svg += G(f"ru-c{i}", g)
        js = badge_js("ru-bd", D)
        for i in range(4):
            js += rise(f"#ru-c{i}", T_[0] + 0.2 + i * 0.5, dy=40)
        return scene(svg, badge("ru-bd", 5, "Góp ý thành luật")), "", js
    return VScene("rules", ["c08-1"], build, lead=0.4, tail=3.0)


# ================================================================== màn 09 · Bước 6 nhân vật v2
def models():
    def build(T_, D):
        L = math.hypot(420, 236)
        svg = (G("mo-v1", scr("assets/img/t1draft.jpg", 140, 260, 420, "v1 – người que đơn giản"), extra="")
               + f'<line id="mo-x" x1="140" y1="260" x2="560" y2="496" stroke="#D93B3B" stroke-width="10" stroke-linecap="round" '
                 f'stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}"/>'
               + G("mo-ar", arrow(600, 378, 700, 378)) + G("mo-v2", scr("assets/img/ms2.jpg", 760, 180, 760, "Model sheet v2"))
               + G("mo-ok", check(1505, 185, 38))
               + G("mo-walk", f'<g transform="translate(1730,720)"><g id="mo-w">{stick("mo-w", "picker", 1.7)}</g></g>'
                   + T(1730, 790, "nghiêng – nhún", 30, 800, ORANGE_D, "middle")))
        js = badge_js("mo-bd", D) + gpop("#mo-v1", 0.2, 0.9)
        js += f'tl.to("#mo-x",{{attr:{{"stroke-dashoffset":0}},duration:0.4,ease:"power2.out"}},{T_[0] + 0.4:.2f});\n'
        js += show("#mo-ar", T_[0] + 0.9) + gpop("#mo-v2", T_[0] + 1.2, 0.85) + gpop("#mo-ok", T_[0] + 2.8, 0.3, 0.3)
        js += show("#mo-walk", T_[0] + 1.8) + walk_js("mo-w", T_[0] + 1.9, D - 0.4)
        return scene(svg, badge("mo-bd", 6, "Duyệt bảng nhân vật")), "", js
    return VScene("models", ["c09-1"], build, lead=0.4, tail=2.6)


# ================================================================== màn 10 · Bước 7 duyệt 31 giây
def bar31():
    def build(T_, D):
        x0, x1, y, tot = 160, 1760, 600, 309
        xs = x0 + (x1 - x0) * 31 / tot
        ticks = ""
        for t, s in [(0, "Phần 1"), (60, "Phần 2"), (125, "Phần 3"), (185, "Phần 4"), (245, "Phần 5")]:
            xx = x0 + (x1 - x0) * t / tot
            ticks += G(f"b3-t{t}", f'<line x1="{xx}" y1="{y + 40}" x2="{xx}" y2="{y + 70}" stroke="{MUTED}" stroke-width="3"/>' + T(xx + 8, y + 104, s, 28, 700, MUTED))
        svg = (rect(x0, y - 30, x1 - x0, 60, "#E3E8EF", 30)
               + f'<rect id="b3-blue" x="{xs - 30}" y="{y - 30}" width="{x1 - xs + 30}" height="60" rx="30" fill="{BLUE}"/>'
               + f'<rect id="b3-green" x="{x0}" y="{y - 30}" width="{xs - x0}" height="60" rx="30" fill="{GREEN}"/>'
               + G("b3-lab", T(x0, y - 60, "0:31 – duyệt trước", 34, 800, GREEN_D) + check(x0 + 385, y - 72, 26))
               + ticks + G("b3-end", T(x1, y + 104, "5:09", 38, 900, BLUE, "end"))
               + G("b3-scr", scr("assets/img/kho.jpg", 1240, 150, 420, "Bản đầy đủ · 1080p")))
        js = badge_js("b3-bd", D)
        js += f'tl.fromTo("#b3-green",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.6,ease:"power2.out",transformOrigin:"0% 50%"}},{T_[0] + 0.2:.2f});\n'
        js += f'tl.fromTo("#b3-blue",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:1.6,ease:"power1.inOut",transformOrigin:"0% 50%"}},{T_[0] + 1.6:.2f});\n'
        js += rise("#b3-lab", T_[0] + 0.7, dy=10)
        for i, t in enumerate([0, 60, 125, 185, 245]):
            js += show(f"#b3-t{t}", T_[0] + 1.6 + i * 0.32, 0.2)
        js += show("#b3-end", T_[0] + 3.2) + gpop("#b3-scr", T_[0] + 3.3, 0.85)
        return scene(svg, badge("b3-bd", 7, "Duyệt 31 giây đầu, rồi làm đủ")), "", js
    return VScene("bar31", ["c10-1"], build, lead=0.4, tail=2.4, min_d=6.5)


# ================================================================== màn 11 · Bước 8 context TC
def context():
    rows = [("", "Hàng kho khô", "Hàng TC"), ("Nhận hàng", "Dán LPN", "Không LPN"), ("Sau nhận", "Cất lên kệ", "Khu TC"),
            ("Xuất", "Pick từ pick face", "Chia theo DO"), ("Tồn kho", "Có lưu kho", "Không lưu kho")]

    def build(T_, D):
        px, py = 160, 220
        g = rect(px, py, 900, 540, "#fff", 18, INK, 3) + rect(px, py, 900, 70, BLUE, 18) + rect(px, py + 40, 900, 30, BLUE, 0)
        g += T(px + 30, py + 48, "Context TC – Khác gì video trước", 32, 800, "#fff")
        rr = ""
        for i, (a, c1, c2) in enumerate(rows):
            yy = py + 135 + i * 80
            line = f'<line x1="{px + 20}" y1="{yy - 50}" x2="{px + 880}" y2="{yy - 50}" stroke="#E3E8EF" stroke-width="2"/>' if i else ""
            rr += G(f"cx-r{i}", line + T(px + 30, yy, a, 30, 800, MUTED) + T(px + 250, yy, c1, 30, 800 if i == 0 else 600, INK)
                    + T(px + 590, yy, c2, 30, 800, ORANGE_D if i else INK))
        chips = "".join(G(f"cx-k{i}", pill(1320, 260 + i * 84, s, GREEN_D, "#fff", 28)) for i, s in enumerate(["Nhịp 1.3×", "Âm thanh ≥ 4s", "Nhân vật v2"]))
        svg = G("cx-p", g) + rr + chips + G("cx-scr", scr("assets/img/tc.jpg", 1190, 530, 480, "36 giây đầu → 2:12"))
        js = badge_js("cx-bd", D) + rise("#cx-p", 0.2, dy=30)
        for i in range(len(rows)):
            js += show(f"#cx-r{i}", 0.6 + i * 0.35, 0.25)
        for i in range(3):
            js += f'tl.fromTo("#cx-k{i}",{{opacity:0,x:200}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},{T_[1] + 2.2 + i * 0.35:.2f});\n'
        js += gpop("#cx-scr", T_[1] + 3.6, 0.85)
        return scene(svg, badge("cx-bd", 8, "Video TC: chỉ viết phần khác")), "", js
    return VScene("context", ["c11-1", "c11-2"], build, lead=0.4, tail=2.0)


# ================================================================== màn 12 · Bước 9 deck
def deck():
    def build(T_, D):
        pages = ""
        for i in range(5):
            k = 5 - i
            pages += (f'<g id="dk-p{i}" opacity="0">' + rect(720, 290, 480, 270, "#2B3646", 12)
                      + f'<image href="assets/img/deckp-0{k}.jpg" x="730" y="300" width="460" height="250" preserveAspectRatio="xMidYMid slice"/></g>')
        svg = pages + G("dk-pill", pill(960, 790, "17 slide · .pptx", INK, "#fff", 36))
        js = badge_js("dk-bd", D)
        for i in range(5):
            ang = -24 + i * 12
            js += show(f"#dk-p{i}", T_[0] + 0.2, 0.2)
            js += f'tl.fromTo("#dk-p{i}",{{rotation:0,svgOrigin:"960 1050"}},{{rotation:{ang},svgOrigin:"960 1050",duration:0.8,ease:"back.out(1.4)"}},{T_[0] + 0.3 + i * 0.12:.2f});\n'
        js += gpop("#dk-pill", T_[0] + 2.2, 0.4)
        return scene(svg, badge("dk-bd", 9, "Thêm một bộ slide")), "", js
    return VScene("deck", ["c12-1"], build, lead=0.4, tail=2.2)


# ================================================================== màn 13 · Bước 10 PDF → prompt
def pdf():
    def build(T_, D):
        p = rect(160, 200, 300, 380, "#fff", 12, INK, 3) + rect(160, 200, 300, 80, "#C42F2F", 12) + rect(160, 240, 300, 40, "#C42F2F", 0)
        p += T(310, 258, "PDF", 44, 900, "#fff", "middle") + "".join(rect(200, 320 + k * 60, 220 - (k % 2) * 60, 26, "#E3E8EF", 6) for k in range(4))
        p += T(310, 632, "Bản vẽ quy trình", 30, 800, INK, "middle")
        chips = [("WMS", "#fff", BLUE, BLUE), ("PDA", "#2B3646", "#fff", INK), ("Thủ công", ORANGE_D, "#fff", ORANGE_D), ("Chứng từ", "#fff", INK, INK)]
        ch = ""
        for i, (s, bg, fg, bd) in enumerate(chips):
            cx = 260 + i * 260
            ch += G(f"pd-c{i}", rect(cx - 110, 690, 220, 76, bg, 14, bd, 3) + T(cx, 740, s, 32, 800, fg, "middle"))
        ch += G("pd-c4", f'<polygon points="1300,665 1420,728 1300,791 1180,728" fill="#fff" stroke="{BLUE}" stroke-width="4"/>' + T(1300, 739, "Điều kiện", 28, 800, BLUE, "middle"))
        ch += G("pd-c5", rect(1480, 690, 280, 76, "#fff", 14, "#C42F2F", 3) + T(1620, 740, "01A", 34, 900, "#C42F2F", "middle")
                + '<line id="pd-strike" x1="1500" y1="728" x2="1740" y2="728" stroke="#C42F2F" stroke-width="7"/>'
                + T(1620, 812, "Việc của quản lý – bỏ", 26, 700, "#C42F2F", "middle"))
        svg = (G("pd-pdf", p) + G("pd-a1", arrow(490, 390, 580, 390))
               + G("pd-v1", paper(610, 200, 420, 380, "Prompt v1 (nháp)", ["Đủ 5 quy trình", "Vai gộp chung"], "#6B7685", True))
               + G("pd-a2", arrow(1060, 390, 1150, 390))
               + G("pd-v2", paper(1180, 200, 560, 380, "Prompt v2", ["Bỏ 01A", "Tách 8 vai theo việc", "Chip theo chú giải bản vẽ"], BLUE))
               + G("pd-ok", check(1720, 205, 36)) + ch)
        js = badge_js("pd-bd", D) + gpop("#pd-pdf", T_[0] + 0.3, 0.8) + show("#pd-a1", T_[0] + 1.2) + slide("#pd-v1", T_[0] + 1.4, -40)
        js += show("#pd-a2", T_[0] + 2.2) + slide("#pd-v2", T_[0] + 2.4, -40) + gpop("#pd-ok", T_[0] + 3.0, 0.3, 0.3)
        for i in range(6):
            js += rise(f"#pd-c{i}", T_[0] + 3.4 + i * 0.25, dy=20, dur=0.3)
        js += f'tl.fromTo("#pd-strike",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.35,ease:"power2.out",transformOrigin:"0% 50%"}},{T_[0] + 5.0:.2f});\n'
        return scene(svg, badge("pd-bd", 10, "CXAD: từ bản vẽ đến prompt")), "", js
    return VScene("pdf", ["c13-1"], build, lead=0.4, tail=4.2)


# ================================================================== màn 14 · Bước 11 skill nhân vật
def cast():
    SC, FY = 1.3, 690
    CARTON = '<g transform="translate(0,23) rotate(-70)"><g transform="translate(-30,-22)">' + carton_flat(0, 0, 60, 44) + '</g></g>'
    PEN = f'<line x1="0" y1="22" x2="10" y2="44" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    PAPER = ('<g transform="translate(4,22) rotate(-62)"><rect x="-4" y="-22" width="34" height="44" rx="3" fill="#fff" '
             f'stroke="{INK}" stroke-width="2.5"/><rect x="2" y="-14" width="22" height="3" fill="{MUTED}"/>'
             f'<rect x="2" y="-6" width="18" height="3" fill="{MUTED}"/><path d="M4 10 q6 -8 10 0 t10 0" fill="none" stroke="{BLUE}" stroke-width="2.5"/></g>')
    LAPTOP = (f'<rect x="30" y="-64" width="90" height="10" rx="3" fill="#C9965A" stroke="{INK}" stroke-width="3"/>'
              f'<rect x="70" y="-54" width="10" height="54" fill="#A97A44" stroke="{INK}" stroke-width="2.5"/>'
              f'<path d="M44 -66 L96 -66 L108 -112 L56 -112 Z" fill="#2B3646" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
              f'<path d="M60 -106 L102 -106 L94 -74 L52 -74 Z" fill="#7FD3FF"/>')
    roster = [
        (190, "receiver", "Nhận hàng", "bê thùng", dict(pose={"armL": (34, -104), "armR": (-34, 104)}, hand_r=CARTON), ""),
        (410, "forklift", "Xe nâng", "lái, nâng càng", None, ""),
        (600, "planner", "Điều phối", "gõ máy tính", dict(pose={"armL": (-40, -35), "armR": (-50, -25)}), LAPTOP),
        (850, "manager", "Quản lý kho", "giao việc", dict(pose={**MANAGER_HOLD, "armR": (-95, -5)}, hand_l=folder_svg()), ""),
        (1020, "picker", "Picker", "kéo trolley", dict(pose={"armR": (-88, 0)}), ms_trolley()),
        (1370, "checker", "Checker", "scan PDA", dict(pose={"armR": (-60, -10)}, hand_r=pda_svg("cs-chk", laser=True, reach=70)), ""),
        (1530, "transport", "Vận tải", "ký giấy giao", dict(pose={"armL": (-8, -118), "armR": (-40, -95)}, hand_l=PAPER, hand_r=PEN), ""),
        (1690, "instructor", "Giảng viên", "vẫy tay", dict(), ""),
    ]

    def build(T_, D):
        svg = G("cs-box", rect(110, 190, 1700, 640, "none", 30, BLUE, 6, 'stroke-dasharray="22 14"') + pill(960, 190, "Skill: nhan-vat-kho · model v3", BLUE, "#fff", 34))
        for i, (x, r, lab, act, kw, front) in enumerate(roster):
            if r == "forklift":
                drv = f'<g transform="translate(-22,-14)">{stick("cs-fl", "forklift", 1.0, pose={"armR": (-70, -20), "armL": (10, -40)})}</g>'
                fig = fl_back() + drv + fl_front() + '<g id="cs-load"><g transform="translate(60,-62)">' + carton_flat(0, 0, 56, 42) + '</g></g>'
            else:
                fig = stick(f"cs{i}m", r, 1.0, **kw) + front
            hl = ""
            if r == "manager":
                hl = rect(x - 95, 270, 190, 545, "#FFF3E2", 20, ORANGE_D, 4) + pill(x, 300, "MỚI", ORANGE_D, "#fff", 26)
            svg += G(f"cs{i}", hl + f'<g transform="translate({x},{FY})"><g id="cs{i}a"><g transform="scale({SC})">{fig}</g></g></g>'
                     + T(x, FY + 62, lab, 28, 800, INK, "middle") + T(x, FY + 98, act, 24, 600, MUTED, "middle"))
        t_new = T_[0] + 1.3
        js = badge_js("cs-bd", D)
        k = 0
        for i in range(len(roster)):
            if roster[i][1] == "manager":
                continue
            js += rise(f"#cs{i}", 0.3 + k * 0.12, dy=30, dur=0.35); k += 1
        js += f'tl.fromTo("#cs3",{{opacity:0,x:260}},{{opacity:1,x:0,duration:1.0,ease:"power1.out"}},{t_new:.2f});\n'
        js += walk_js("cs3m", t_new, t_new + 1.0)
        js += show("#cs-box", T_[0] + 3.0, 0.4)
        a0, a1 = 1.2, D - 0.3
        js += bob("#cs0a", "y", -10, a0, a1)                      # bê thùng
        js += bob("#cs-load", "y", -26, a0, a1, 0.6)             # nâng càng
        js += swing("#cs2m-foreR", -25, -5, a0, a1, 0.25)        # gõ phím
        js += swing("#cs3m-foreR", -5, -30, t_new + 1.1, a1, 0.5)  # chỉ tay giao việc
        js += bob("#cs4a", "x", 14, a0, a1, 0.55)                # kéo trolley
        n = int((a1 - a0) / 0.5)
        js += f'tl.fromTo("#cs-chk-laser",{{opacity:1}},{{opacity:0.1,duration:0.25,yoyo:true,repeat:{n},ease:"steps(1)"}},{a0:.2f});\n'
        js += swing("#cs6m-foreR", -95, -75, a0, a1, 0.3)       # ký giấy
        for t in range(int(a0 * 10), int((a1 - 1.4) * 10), 22):
            js += wave_js("cs7m", t / 10, n=3)
        return scene(svg, badge("cs-bd", 11, "Đóng gói nhân vật thành skill")), "", js
    return VScene("cast", ["c14-1", "c14-2"], build, lead=0.4, tail=2.0)


# ================================================================== màn 15 · Bước 12 phiên bản
def versions():
    def build(T_, D):
        svg = ""
        for row, (ka, kb, la, lb, cap) in enumerate([("cx_v1", "cx_v2", "v1", "v2", "Phụ đề quy đổi bằng số"),
                                                     ("cx_v2b", "cx_v3", "v2", "v3", "Ô điều kiện khớp mũi tên")]):
            y = 175 + row * 330
            svg += G(f"vs-a{row}", scr(f"assets/img/{ka}.jpg", 300, y, 370, la)) + G(f"vs-r{row}", arrow(700, y + 104, 790, y + 104))
            svg += G(f"vs-b{row}", scr(f"assets/img/{kb}.jpg", 820, y, 370, lb))
            svg += G(f"vs-t{row}", T(1260, y + 95, cap, 42, 900, BLUE) + T(1260, y + 147, f"v{row + 1} → v{row + 2}", 32, 700, MUTED))
        js = badge_js("vs-bd", D)
        for row in range(2):
            t = 0.3 + row * 1.6
            js += gpop(f"#vs-a{row}", t, 0.9) + show(f"#vs-r{row}", t + 0.4) + gpop(f"#vs-b{row}", t + 0.6, 0.9) + slide(f"#vs-t{row}", t + 0.9, -30)
        return scene(svg, badge("vs-bd", 12, "Sửa theo phiên bản")), "", js
    return VScene("versions", ["c15-1"], build, lead=0.4, tail=3.0, min_d=6.2)


# ================================================================== màn 16 · công thức
STEPS = ["Nguồn", "Prompt / Context", "Outline duyệt", "Chốt luật", "Bảng nhân vật",
         "30 giây mẫu", "Làm đủ", "Render", "Sửa v2, v3", "Đóng gói"]


def formula():
    def build(T_, D):
        svg = G("fo-h", T(960, 150, "Công thức", 76, 900, INK, "middle"))
        for i, s in enumerate(STEPS):
            row, col = divmod(i, 5)
            c = col if row == 0 else 4 - col
            x, y = 140 + c * 340, 250 + row * 260
            box = (rect(x, y, 290, 140, "#fff", 18, BLUE, 4) + f'<rect id="fo-f{i}" x="{x}" y="{y}" width="290" height="140" rx="18" fill="{BLUE}" opacity="0"/>'
                   + f'<text id="fo-n{i}" x="{x + 145}" y="{y + 52}" font-family="{F}" font-size="28" font-weight="900" fill="{MUTED}" text-anchor="middle">{i + 1:02d}</text>'
                   + f'<text id="fo-s{i}" x="{x + 145}" y="{y + 100}" font-family="{F}" font-size="31" font-weight="800" fill="{INK}" text-anchor="middle">{esc(s)}</text>')
            if i < 9:
                if row == 0 and col < 4:
                    box += arrow(x + 296, y + 70, x + 334, y + 70, ORANGE_D, 6)
                elif row == 0:
                    box += arrow(x + 145, y + 146, x + 145, y + 254, ORANGE_D, 6)
                else:
                    box += arrow(x - 6, y + 70, x - 44, y + 70, ORANGE_D, 6)
            svg += G(f"fo-b{i}", box)
        js = rise("#fo-h", 0.1)
        for i in range(10):
            js += rise(f"#fo-b{i}", 0.2 + i * 0.07, dy=16, dur=0.3)
        for i in range(10):
            t = T_[0] + 0.6 + i * 0.32
            js += f'tl.to("#fo-f{i}",{{opacity:1,duration:0.2}},{t:.2f});\n'
            js += f'tl.to(["#fo-n{i}","#fo-s{i}"],{{attr:{{fill:"#FFFFFF"}},duration:0.2}},{t:.2f});\n'
        return scene(svg), "", js
    return VScene("formula", ["c16-1"], build, lead=0.4, tail=3.8)


# ================================================================== màn 17 · ghi nhớ + kết
def ghinho():
    items = ["Duyệt sớm bằng thứ nhỏ", "Góp ý nào cũng thành luật ghi lại", "Cái gì dùng lại thì đóng gói thành skill"]

    def build(T_, D):
        card = rect(220, 190, 1000, 580, "#fff", 22, INK, 3) + T(280, 295, "Ghi nhớ", 66, 900) + rect(280, 322, 120, 8, ORANGE, 4)
        svg = G("gn-card", card)
        for i, s in enumerate(items):
            yy = 440 + i * 110
            svg += G(f"gn-i{i}", T(290, yy, s, 42, 700) + check(1150, yy - 14, 28))
        svg += f'<g transform="translate(1530,830)"><g id="gn-mw">{stick("gn-m", "instructor", 2.1)}</g></g>'
        js = rise("#gn-card", 0.1, dy=30)
        for i, dt in enumerate([0.1, 0.9, 1.7]):
            js += slide(f"#gn-i{i}", T_[0] + dt, -30, 0.35)
        js += f'tl.fromTo("#gn-mw",{{x:280}},{{x:0,duration:1.0,ease:"power1.out"}},0.2);\n' + walk_js("gn-m", 0.2, 1.2)
        js += wave_js("gn-m", T_[1] + 0.1, n=6)
        return scene(svg), "", js
    s = VScene("ghinho", ["c17-1", "c17-2"], build, lead=0.4, tail=2.6)
    s.sfx = [(("T", 1, 0.2), "chime.mp3", 0.1)]
    return s
