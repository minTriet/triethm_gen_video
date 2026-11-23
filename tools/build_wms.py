"""Video "Quy trình kho cơ bản với WMS" -> ./video-wms
Run: python3 tools/build_wms.py
Kịch bản: source/Prompt_Video_Quy_trinh_co_ban_WMS.md · storyboard design/storyboard-wms-co-ban.html.
Hình vẽ dùng chung với storyboard (tools/wms_kit.py), nên khung video khớp từng màn đã duyệt.
Không giọng đọc: mỗi câu phụ đề giữ theo nhịp đọc 1.3× (tools/build_full.py).
Bản hiện tại: 30 giây đầu (màn 01–06) để duyệt.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from wms_kit import *  # noqa: E402,F401,F403
from wms_kit import C, stick, pda_svg, ms_desk, carton_flat  # noqa: E402
from kit import walk_js, pose_js, REST  # noqa: E402
from build_full import Scene, build_all  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "video-wms")


# ------------------------------------------------------------------ helpers
def G(gid, inner, hidden=True):
    st_ = ' style="opacity:0"' if hidden else ""
    return f'<g id="{gid}"{st_}>{inner}</g>'


def fig(fid, role, x, y=830, s=1.8, tag=None, tag_col=INK, **kw):
    """Nhân vật: bọc ngoài cố định vị trí, nhóm {fid}-w để dịch chuyển, nhãn {fid}-tag."""
    out = f'<g transform="translate({x},{y})"><g id="{fid}-w">{stick(fid, role, s, **kw)}</g></g>'
    if tag:
        out += G(f"{fid}-tag", pill(x, y - 214 * s + 40, tag, tag_col, "#fff", 24))
    return out


def svg(inner):
    return (f'<svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">'
            f'<rect width="1920" height="1080" fill="{C["ground"]}"/>{inner}</svg>')


def pop(sel, t, dur=0.4, s0=0.6):
    return (f'tl.fromTo("{sel}",{{opacity:0,scale:{s0}}},{{opacity:1,scale:1,duration:{dur},ease:"back.out(1.8)",'
            f'transformOrigin:"50% 50%"}},{t:.2f});\n')


def rise(sel, t, dy=24, dur=0.45):
    return f'tl.fromTo("{sel}",{{opacity:0,y:{dy}}},{{opacity:1,y:0,duration:{dur},ease:"power3.out"}},{t:.2f});\n'


def slide(sel, t, dx, dur=0.5):
    return f'tl.fromTo("{sel}",{{opacity:0,x:{dx}}},{{opacity:1,x:0,duration:{dur},ease:"power3.out"}},{t:.2f});\n'


def show(sel, t, dur=0.25):
    return f'tl.to("{sel}",{{opacity:1,duration:{dur}}},{t:.2f});\n'


def draw_arrow(sel, t, dur=0.35):
    return f'tl.fromTo("{sel}",{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,duration:{dur},ease:"power2.out",transformOrigin:"0% 50%"}},{t:.2f});\n'


def type_js(fid, t0, t1):
    s, t, k = "", t0, 0
    while t < t1:
        s += f'tl.to("#{fid}-foreR",{{rotation:{60 if k % 2 else 82},svgOrigin:"0 0",duration:0.18,ease:"sine.inOut"}},{t:.2f});\n'
        t += 0.2
        k += 1
    return s


def wave_js(fid, t, n=4):
    js = pose_js(fid, t, {"armR": (-150, -24)}, dur=0.3, ease="power2.out")
    for k in range(n):
        js += f'tl.to("#{fid}-foreR",{{rotation:{-50 if k % 2 == 0 else -5},svgOrigin:"0 0",duration:0.22,ease:"sine.inOut"}},{t + 0.3 + k * 0.22:.2f});\n'
    return js + pose_js(fid, t + 0.3 + n * 0.22, {"armR": REST["armR"]}, dur=0.3)


def laser_js(fid, t, n=2):
    js = f'tl.set("#{fid}-laser",{{opacity:0}},0);\n'
    for k in range(n):
        js += f'tl.to("#{fid}-laser",{{opacity:1,duration:0.08}},{t + k * 0.6:.2f});\n'
        js += f'tl.to("#{fid}-laser",{{opacity:0,duration:0.15}},{t + k * 0.6 + 0.35:.2f});\n'
    return js


def badge_js(t=0.1):
    return f'tl.fromTo("#bdg",{{opacity:0,y:-16}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{t:.2f});\n'


# ============================================================ 01 Mở đầu
def intro():
    def build(T, D):
        title = (G("in-tag", pill(270, 200, "VIDEO TRAINING WMS", ORANGE, "#fff", 26))
                 + G("in-l1", T_(120, 330, "Quy trình kho", 96, 900))
                 + G("in-l2", T_(120, 445, "cơ bản với WMS", 96, 900, BLUE)))
        flow = (f'<text x="120" y="530" font-family="{F}" font-size="40" font-weight="700" fill="{MUTED}" xml:space="preserve">'
                '<tspan id="in-f1" fill-opacity="0">Nhập hàng</tspan><tspan id="in-f2" fill-opacity="0">  →  Cất hàng</tspan>'
                '<tspan id="in-f3" fill-opacity="0">  →  Xuất hàng</tspan></text>')
        r = G("in-rack", rack(1150, 300, 3, [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"], ["A-03-01", "A-03-02"]],
                              {(0, 0): 3, (1, 1): 2, (2, 0): 2, (0, 1): 1}, cw=200, lh=160))
        body = svg(floor() + title + flow + r + fig("in-man", "instructor", 950, s=2.0))
        js = rise("#in-rack", 0.0, dy=30, dur=0.6)
        js += f'tl.fromTo("#in-man-w",{{x:420}},{{x:0,duration:1.2,ease:"power1.out"}},0.2);\n' + walk_js("in-man", 0.2, 1.4)
        js += pop("#in-tag", 0.3) + rise("#in-l1", 0.45) + rise("#in-l2", 0.65)
        js += wave_js("in-man", T[0])
        for i, dt in enumerate([0.2, 1.4, 2.6]):
            js += f'tl.to("#in-f{i + 1}",{{attr:{{"fill-opacity":1}},duration:0.3}},{T[1] + dt:.2f});\n'
        return body, "", js
    s = Scene("intro", ["Xin chào các bạn.",
                        "Hôm nay chúng ta xem hàng đi qua kho như thế nào, và WMS giúp gì ở từng bước."],
              build, lead=1.4, tail=1.2)
    s.sfx = [(0.2, "whoosh.mp3", 0.15)]
    return s


def T_(*a, **k):
    return T(*a, **k)


# ============================================================ 02 Toàn cảnh
NODES = ["Nhận hàng", "Cất hàng", "Lưu kho", "Lấy hàng", "Kiểm hàng", "Giao hàng"]


def overview():
    def build(T, D):
        b = floor() + G("ov-h", T_(960, 130, "Hàng đi qua kho", 60, 900, INK, "middle"))
        for i, s in enumerate(NODES):
            x = 95 + i * 300
            col = GREEN if i < 2 else BLUE if i == 2 else ORANGE
            b += G(f"ov-l{i}", f'<line x1="{x + 125}" y1="512" x2="960" y2="380" stroke="{BLUE}" stroke-width="3" stroke-dasharray="8 8"/>')
            b += f'<g id="ov-n{i}" style="opacity:0.25">' + rect(x, 520, 250, 120, "#fff", 20, col, 5) + T_(x + 125, 594, s, 34, 800, INK, "middle") + "</g>"
            if i < 5:
                b += G(f"ov-a{i}", arrow(x + 256, 580, x + 294, 580, INK, 5), hidden=False)
        b += G("ov-box", carton_flat(0, 0, 60, 44), hidden=True).replace('<g id="ov-box"', '<g id="ov-box" transform="translate(190,430) scale(1.3)"', 1)
        b += G("ov-wms", rect(700, 220, 520, 160, BLUE, 26) + T_(960, 300, "WMS", 64, 900, "#fff", "middle")
               + T_(960, 350, "ghi nhận từng bước", 28, 700, "#BFD8F5", "middle"))
        b += G("ov-p1", pill(560, 720, "PHẦN 1 · NHẬP", GREEN, "#fff", 26)) + G("ov-p2", pill(1390, 720, "PHẦN 2 · XUẤT", ORANGE, "#fff", 26))
        body = svg(b)
        js = rise("#ov-h", 0.0)
        # câu 1: ô sáng lần lượt, thùng hàng chạy theo
        t0, step = T[0] + 0.1, 0.62
        js += show("#ov-box", t0, 0.2)
        for i in range(6):
            js += f'tl.to("#ov-n{i}",{{opacity:1,duration:0.25}},{t0 + i * step:.2f});\n'
            if i:
                js += f'tl.to("#ov-box",{{x:{190 + i * 300},duration:{step - 0.1:.2f},ease:"power1.inOut"}},{t0 + (i - 1) * step + 0.1:.2f});\n'
        js += f'tl.to("#ov-box",{{opacity:0,duration:0.3}},{t0 + 6 * step:.2f});\n'
        # câu 2: WMS + nét đứt nối xuống từng ô
        js += pop("#ov-wms", T[1], s0=0.7)
        for i in range(6):
            js += show(f"#ov-l{i}", T[1] + 0.4 + i * 0.15)
        # câu 3: WMS nhấp nhẹ, hai chip phần
        js += f'tl.to("#ov-wms",{{scale:1.06,transformOrigin:"50% 50%",duration:0.25,yoyo:true,repeat:1}},{T[2] + 0.2:.2f});\n'
        js += pop("#ov-p1", T[2] + 0.9) + pop("#ov-p2", T[2] + 1.2)
        return body, "", js
    s = Scene("overview", ["Hàng vào kho, được cất lên kệ, rồi được lấy ra giao cho khách.",
                           "Mỗi bước đều được ghi vào WMS.",
                           "Nhờ vậy lúc nào cũng biết: hàng gì, ở đâu, còn bao nhiêu."], build, lead=0.6, tail=1.0)
    s.sfx = [(("T", 1, 0.0), "ping.mp3", 0.12)]
    return s


# ============================================================ 03 Ba vai + nhãn bước
def roles():
    def build(T, D):
        b = floor() + G("ro-h", T_(960, 110, "Ai làm gì?", 60, 900, INK, "middle"))
        b += prop(ms_desk(), 300, 830, 1.8) + fig("ro-x", "xlct", 230, pose=TYPE, tag="Nhân viên XLCT", tag_col=BLUE)
        b += fig("ro-k", "receiver", 960, pose=SCAN, hand_r=pda_svg("ro-k", laser=True, reach=70), tag="Nhân viên kho", tag_col=GREEN)
        b += prop(ms_truck(), 1380, 830, 1.5) + fig("ro-d", "driver", 1330, pose=SIGN, hand_l=PAPER, hand_r=PEN, tag="Tài xế", tag_col=MUTED)
        for i, s in enumerate(["Nhận file, nhập WMS, in chứng từ", "Làm với hàng, quét bằng PDA", "Giao / nhận hàng, ký chứng từ"]):
            b += G(f"ro-d{i}", T_([330, 960, 1560][i], 395, s, 28, 700, MUTED, "middle"))
        x = 700
        lg = T_(330, 215, "Nhãn ở mỗi bước:", 30, 800)
        for k in ("tay", "wms", "pda", "doc"):
            c, cw = chip(x, 205, k, 26)
            lg += G(f"ro-c{k}", c)
            x += cw + 22
        b += G("ro-lg", lg)
        body = svg(b)
        js = rise("#ro-h", 0.0)
        for i, (fid, dt) in enumerate([("ro-x", 0.1), ("ro-k", 1.2), ("ro-d", 2.3)]):
            js += f'tl.fromTo("#{fid}-w",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power2.out"}},{T[0] + dt - 0.4 if i == 0 else T[0] + dt:.2f});\n'
            js += pop(f"#{fid}-tag", T[0] + dt + 0.1) + rise(f"#ro-d{i}", T[0] + dt + 0.2, dy=12)
        js += type_js("ro-x", T[0] + 0.3, D - 0.4) + laser_js("ro-k", T[0] + 1.5, 3)
        js += f'tl.to("#ro-d-foreR",{{rotation:-80,svgOrigin:"0 0",duration:0.3,yoyo:true,repeat:3}},{T[0] + 2.6:.2f});\n'
        js += show("#ro-lg", T[1])
        for i, k in enumerate(("tay", "wms", "pda", "doc")):
            js += f'tl.set("#ro-c{k}",{{opacity:0}},0);\n' + pop(f"#ro-c{k}", T[1] + 1.4 + i * 0.45)
        # ẩn bàn/xe tải tới khi vai xuất hiện
        return body, "", js
    s = Scene("roles", ["Có ba vai chính: nhân viên xử lý chứng từ, nhân viên kho và tài xế.",
                        "Nhãn cạnh mỗi bước cho biết bước đó làm tay, làm trên WMS hay quét bằng PDA."], build, lead=0.6, tail=1.2)
    return s


# ============================================================ Thẻ chương
CH_ITEMS = ["Nhập hàng và cất hàng", "Xuất hàng theo đơn"]
CH_TITLE = {1: ["Nhập hàng", "và cất hàng"], 2: ["Xuất hàng", "theo đơn"]}


class Chapter:
    is_chapter = True

    def __init__(self, num):
        self.cid, self.num = f"chap{num}", num
        self.lines, self.T, self.E = [], [], []
        self.D = 2.8
        self.sfx = [(0.0, "whoosh-short.mp3", 0.2)]

    def build(self, T, D):
        cid, n = self.cid, self.num
        toc = ""
        for i, s in enumerate(CH_ITEMS):
            on = i == n - 1
            y = 380 + i * 150
            toc += G(f"{cid}-i{i}", f'<circle cx="930" cy="{y}" r="38" fill="{BLUE if on else "#fff"}" stroke="{BLUE}" stroke-width="4"/>'
                     + T_(930, y + 13, str(i + 1), 36, 900, "#fff" if on else BLUE, "middle")
                     + T_(1000, y + 14, s, 42, 800 if on else 600, INK if on else MUTED))
        txt = T_(120, 420, f"PHẦN {n}", 34, 700, "#BFD8F5", extra='letter-spacing="4"')
        for i, ln in enumerate(CH_TITLE[n]):
            txt += T_(120, 520 + i * 100, ln, 86, 900, "#fff")
        body = (f'<div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:{C["ground"]}"></div>'
                f'<div id="{cid}-bg" class="abs" style="left:0;top:0;width:760px;height:1080px;background:{BLUE}"></div>'
                f'<svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">'
                f'{G(cid + "-txt", txt)}{toc}</svg>')
        js = f'tl.fromTo("#{cid}-bg",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.4,ease:"power3.out"}},0);\n'
        js += slide(f"#{cid}-txt", 0.2, -40, 0.4)
        for i in range(len(CH_ITEMS)):
            js += slide(f"#{cid}-i{i}", 0.35 + i * 0.12, 30, 0.3)
        js += f'tl.to("#{cid}-txt",{{opacity:0,x:40,duration:0.25,ease:"power2.in"}},{D - 0.4:.2f});\n'
        return body, "", js


# ============================================================ 05 Bước 1: Nhận ASN
def xlct_desk(fid, x=260, tag=False):
    return prop(ms_desk(), x + 70, 830, 1.8) + fig(fid, "xlct", x, pose=TYPE,
                                                   tag="Nhân viên XLCT" if tag else None, tag_col=BLUE)


def b1_asn():
    def build(T, D):
        b = floor() + G("bdg", badge(1, "Nhận ASN", ["tay"])) + xlct_desk("b1x", tag=True)
        b += G("b1-mail", mail(700, 190, 560, "Chủ hàng", "Kế hoạch nhập ngày 20/11", "KeHoachNhap_20-11.xlsx"))
        b += G("b1-ar", arrow(1280, 320, 1360, 320, ORANGE, 7))
        b += G("b1-sh", sheet(1380, 230, 470, ["Mã hàng", "Tên hàng", "SL"],
                              [["SKU 1001", "Nước suối", "50"], ["SKU 2001", "Mì ly", "40"]], [150, 220, 100], "Đúng mẫu WMS"))
        # ô đang sửa: viền đỏ → xanh
        b += G("b1-bad", rect(1752, 334, 90, 48, "none", 6, RED, 4))
        b += G("b1-good", rect(1752, 334, 90, 48, "none", 6, GREEN, 4))
        b += G("b1-ok", check(1820, 210, 26))
        body = svg(b)
        js = badge_js() + pop("#b1x-tag", 0.3) + type_js("b1x", 0.3, D - 0.3)
        js += slide("#b1-mail", T[0] + 0.3, 200) + draw_arrow("#b1-ar", T[0] + 1.6) + pop("#b1-sh", T[0] + 1.9, s0=0.85)
        js += show("#b1-bad", T[1] + 0.3, 0.15) + f'tl.to("#b1-bad",{{opacity:0.2,duration:0.2,yoyo:true,repeat:3}},{T[1] + 0.5:.2f});\n'
        js += f'tl.to("#b1-bad",{{opacity:0,duration:0.15}},{T[1] + 1.4:.2f});\n' + show("#b1-good", T[1] + 1.4, 0.15)
        js += f'tl.to("#b1-good",{{opacity:0,duration:0.3}},{T[1] + 2.4:.2f});\n' + pop("#b1-ok", T[1] + 2.3, s0=0.3)
        return body, "", js
    s = Scene("b1asn", ["Bước 1: chủ hàng gửi kế hoạch nhập, gọi là ASN.",
                        "Nhân viên XLCT kiểm tra file và sửa cho đúng mẫu của WMS."], build, lead=0.5, tail=1.0)
    s.sfx = [(("T", 0, 0.3), "notification.mp3", 0.12)]
    return s


# ============================================================ 06 Bước 2: Nhập vào WMS
def b2_import():
    def build(T, D):
        b = floor() + G("bdg", badge(2, "Nhập vào WMS", ["wms"])) + xlct_desk("b2x")
        b += G("b2-file", rect(700, 300, 150, 120, "#E8F5EC", 14, GREEN, 3) + T_(775, 375, ".xlsx", 30, 900, GREEN, "middle"))
        b += G("b2-ar", arrow(860, 360, 940, 360, ORANGE, 7))
        win = wms_win(960, 180, 880, "ASN-0001 · Chờ hàng đến", ["Mã hàng", "Tên hàng", "SL dự kiến", "Đã nhận"],
                      [["SKU 1001", "Nước suối 500ml", "50", "0"], ["SKU 2001", "Mì ly", "40", "0"]], [190, 290, 200, 160],
                      status="Đã tạo ASN")
        # dòng bảng và chip trạng thái hiện lần lượt: che bằng tấm trắng rồi gỡ ra
        for i in range(2):
            win += f'<rect id="b2-m{i}" x="976" y="{322 + i * 64}" width="848" height="60" fill="#fff"/>'
        win += '<rect id="b2-st" x="976" y="456" width="320" height="60" fill="#fff"/>'
        b += G("b2-win", win)
        b += G("b2-zero", rect(1652, 318, 110, 132, "none", 10, ORANGE, 4, 'stroke-dasharray="10 8"'))
        body = svg(b)
        js = badge_js() + type_js("b2x", 0.3, T[0] + 1.2)
        js += pop("#b2-file", 0.4) + draw_arrow("#b2-ar", T[0] + 0.5) + pop("#b2-win", T[0] + 0.8, s0=0.9)
        js += f'tl.to("#b2-file",{{x:260,opacity:0,scale:0.5,duration:0.5,ease:"power2.in"}},{T[0] + 1.0:.2f});\n'
        for i in range(2):
            js += f'tl.to("#b2-m{i}",{{opacity:0,duration:0.25}},{T[0] + 1.5 + i * 0.4:.2f});\n'
        js += f'tl.to("#b2-st",{{opacity:0,duration:0.2}},{T[0] + 2.4:.2f});\n'
        js += show("#b2-zero", T[1] + 0.6, 0.3)
        return body, "", js
    s = Scene("b2import", ["Bước 2: nhập file vào WMS. Hệ thống tạo ASN.",
                           "WMS biết trước hàng gì sắp đến và bao nhiêu."], build, lead=0.5, tail=1.2)
    s.sfx = [(("T", 0, 2.4), "chime.mp3", 0.15)]
    return s


def timeline():
    return [intro(), overview(), roles(), Chapter(1), b1_asn(), b2_import()]


if __name__ == "__main__":
    placed, total, kept = build_all(seq=timeline(), out=OUT)
    for s, start in placed:
        print(f"{start:7.2f}  {s.D:6.2f}  {s.cid}")
    print("TOTAL", total, "sfx", len(kept))
