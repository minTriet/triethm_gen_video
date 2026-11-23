"""Màn S04–S30 của video Nhiêu Lộc (dựng theo storyboard design/storyboard-nhieu-loc.html).
Được tools/build_nhieuloc.py gọi trong timeline(); mỗi màn có giọng đọc (VScene), thẻ chương là Chap.
Toạ độ hình lấy đúng từ tools/build_storyboard_nhieuloc.py để khung video khớp khung đã duyệt.
"""
from nhieuloc_kit import *  # noqa: F401,F403
from kit import walk_js, pose_js, REST, C  # noqa: F401
from build_wms import G, fig, svg, rise, laser_js, wave_js  # noqa: F401
from build_nhieuloc import VScene, popc, drop, slide_in, pulse, show_js, MARK, MAIN_RACK  # noqa: F401


# ------------------------------------------------------------------ helpers
def badge_g(code, title, chips=()):
    return G("bdg", code_badge(code, title, chips))


def badge_js():
    return rise("#bdg", 0.1, dy=-16, dur=0.35)


def type_js(fid, t0, t1):
    """Gõ phím (model XLCT mới: tay cao) – cẳng tay phải nhấp lên xuống quanh tư thế TYPE."""
    s, t, k = "", t0, 0
    while t < t1:
        s += f'tl.to("#{fid}-foreR",{{rotation:{108 if k % 2 else 124},svgOrigin:"0 0",duration:0.18,ease:"sine.inOut"}},{t:.2f});\n'
        t += 0.2
        k += 1
    return s


def sign_js(fid, t, n=3):
    return f'tl.to("#{fid}-foreR",{{rotation:-80,svgOrigin:"0 0",duration:0.3,yoyo:true,repeat:{n}}},{t:.2f});\n'


def move(sel, t, dx, dur=1.2, dy=0, ease="power1.inOut"):
    return f'tl.to("{sel}",{{x:{dx},y:{dy},duration:{dur},ease:"{ease}"}},{t:.2f});\n'


def fade(sel, t, dur=0.3):
    return f'tl.to("{sel}",{{opacity:0,duration:{dur}}},{t:.2f});\n'


def xdesk(fid, x, s=1.6, tag=False):
    return prop(ms_desk(), x + 50, 830, s) + person(fid, "xlct", x, s=s, pose=TYPE,
                                                    tag="Xử lý chứng từ" if tag else None, tag_col=BLUE)


def S(cid, vo, build, lead=0.5, tail=1.2, sfx=()):
    s = VScene(cid, vo, build, lead=lead, tail=tail)
    s.sfx = list(sfx)
    return s


# ------------------------------------------------------------------ thẻ chương
CH = [("Thiết lập chủ hàng, giá bán", "01A · 01B"), ("Nhập hàng, cất hàng", "02B"),
      ("Khoá lô, chuyển pallet", "03B · 03C · 03D"), ("Xuất hàng theo kg", "04C"), ("Kiểm kê", "05B")]


class Chap:
    is_chapter = True

    def __init__(self, num, title):
        self.cid, self.num, self.title = f"chap{num}", num, title
        self.lines, self.T, self.E, self.vo = [], [], [], []
        self.D = 2.8
        self.sfx = [(0.0, "whoosh-short.mp3", 0.2)]

    def build(self, TT, D):
        cid, n = self.cid, self.num
        txt = T(120, 400, f"PHẦN {n}", 34, 700, "#BFD8F5", extra='letter-spacing="4"')
        for i, ln in enumerate(self.title):
            txt += T(120, 500 + i * 96, ln, 80, 900, "#fff")
        toc = ""
        for i, (s, code) in enumerate(CH):
            y, act = 260 + i * 140, i == n - 1
            toc += G(f"{cid}-i{i}", f'<circle cx="930" cy="{y}" r="38" fill="{BLUE if act else "#fff"}" stroke="{BLUE}" stroke-width="4"/>'
                     + T(930, y + 13, str(i + 1), 36, 900, "#fff" if act else BLUE, "middle")
                     + T(1000, y + 4, s, 40, 800 if act else 600, INK if act else MUTED)
                     + T(1000, y + 46, code, 26, 700, BLUE if act else "#A3ADBA"))
        body = (f'<div class="abs" style="left:0;top:0;width:1920px;height:1080px;background:{C["ground"]}"></div>'
                f'<div id="{cid}-bg" class="abs" style="left:0;top:0;width:760px;height:1080px;background:{BLUE}"></div>'
                f'<svg class="abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">'
                f'{G(cid + "-txt", txt)}{toc}{MARK}</svg>')
        js = f'tl.fromTo("#{cid}-bg",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.4,ease:"power3.out"}},0);\n'
        js += f'tl.fromTo("#{cid}-txt",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},0.2);\n'
        for i in range(len(CH)):
            js += f'tl.fromTo("#{cid}-i{i}",{{opacity:0,x:30}},{{opacity:1,x:0,duration:0.3,ease:"power3.out"}},{0.35 + i * 0.1:.2f});\n'
        js += f'tl.to("#{cid}-txt",{{opacity:0,x:40,duration:0.25,ease:"power2.in"}},{D - 0.4:.2f});\n'
        return body, "", js


# ============================================================ S04 Bản đồ quy trình
def s04():
    groups = [("Thiết lập", ["01A Chủ hàng mới", "01B Giá bán theo ngày"], BLUE),
              ("Nhập", ["02B Nhập hàng – LPN", "+ tem lô QR"], GREEN),
              ("Trong kho", ["03B Khoá / mở lô", "03C Chuyển pallet", "03D Pallet → pallet"], PURPLE),
              ("Xuất", ["04C Xuất theo đơn", "tính theo kg"], ORANGE),
              ("Kiểm kê", ["05B Kiểm kê", "bằng quét mã"], MUTED)]

    def build(TT, D):
        b = floor() + G("m-h", T(960, 110, "Bộ quy trình kho Nhiêu Lộc", 56, 900, INK, "middle"))
        for i, (g, items, col) in enumerate(groups):
            x = 70 + i * 362
            gg = rect(x, 170, 330, 300, "#fff", 18, col, 4) + rect(x, 170, 330, 62, col, 18) + rect(x, 210, 330, 22, col, 0)
            gg += T(x + 165, 213, g, 32, 900, "#fff", "middle")
            for k, s in enumerate(items):
                gg += T(x + 26, 290 + k * 56, s, 26, 700 if s[:2].isdigit() else 600, INK if s[:2].isdigit() else MUTED)
            if i < 4:
                gg += arrow(x + 334, 320, x + 358, 320, INK, 4)
            b += G(f"m-g{i}", gg)
        b += G("m-r0", person("s04m", "manager", 330, s=1.35, pose=MANAGER_HOLD, hand_l=folder_svg(), tag="Quản lý", tag_col="#16478F"))
        b += G("m-r1", prop(ms_desk(), 820, 830, 1.3) + person("s04x", "xlct", 770, s=1.35, pose=TYPE, tag="Xử lý chứng từ", tag_col=BLUE))
        b += G("m-r2", person("s04k", "receiver", 1210, s=1.35, pose=SCAN, hand_r=pda_svg("s04k", laser=True, reach=60),
                              tag="Nhân viên kho", tag_col=GREEN))
        lg = T(1420, 590, "Nhãn ở mỗi bước:", 28, 800)
        for row, keys in enumerate((("wms", "tay"), ("pda", "doc"))):
            x = 1420
            for k in keys:
                c, cw = chip(x, 640 + row * 70, k)
                lg += c
                x += cw + 14
        b += G("m-lg", lg) + MARK
        js = rise("#m-h", 0.0)
        for i in range(5):
            js += rise(f"#m-g{i}", TT[0] + 0.2 + i * 0.4, dy=30)
        for i in range(3):
            js += rise(f"#m-r{i}", TT[1] + 0.3 + i * 1.1, dy=30)
        js += type_js("s04x", TT[1] + 1.4, D - 0.3) + laser_js("s04k", TT[1] + 2.6, 3)
        js += rise("#m-lg", TT[2] + 0.4, dy=20)
        return svg(b), "", js
    return S("s04", ["s04-1", "s04-2", "s04-3"], build, sfx=[(("T", 2, 0.4), "click-soft.mp3", 0.12)])


# ============================================================ S06 01A
def s06():
    def build(TT, D):
        b = floor() + badge_g("01A", "Tạo chủ hàng Nhiêu Lộc", ["wms"])
        b += person("s06m", "manager", 100, s=1.6, pose=POINT_R, tag="Quản lý", tag_col="#16478F")
        b += prop(ms_desk(), 350, 830, 1.6) + person("s06x", "xlct", 300, s=1.6, pose=TYPE)
        b += G("a-win", wms_win(640, 160, 1220, "Mã hàng · Chủ hàng NHIÊU LỘC", ["Mã hàng", "Tên hàng", "Loại", "Kg/thùng", "Thùng/pallet"],
                                [["NL-BC01", "Ba chỉ heo", "Đồng ký", "20", "40"], ["NL-DG02", "Đùi gà", "Đa ký", "12 (chuẩn)", "50"],
                                 ["NL-BO03", "Thăn bò", "Đồng ký", "10", "60"]], [190, 300, 210, 250, 230]))
        b += G("a-hl", rect(654, 366, 1192, 56, "none", 10, ORANGE, 4))
        b += G("a-rule", rect(640, 640, 1220, 150, "#fff", 18, INK, 3) + T(670, 690, "Quy tắc:", 30, 800))
        for i, (s, col) in enumerate([("Nhận hàng", GREEN), ("Cất hàng: khu đông lạnh", BLUE), ("Tìm tồn: FEFO", ORANGE)]):
            b += G(f"a-p{i}", pill([900, 1250, 1640][i], 750, s, col, "#fff", 26))
        b += MARK
        js = badge_js() + type_js("s06x", 0.4, D - 0.3)
        js += rise("#a-win", TT[0] + 0.5, dy=30) + show_js("#a-hl", TT[1] + 1.0) + pulse("#a-hl", TT[1] + 1.2, 2)
        js += rise("#a-rule", TT[2] + 0.2)
        for i, cx in enumerate([900, 1250, 1640]):
            js += popc(f"#a-p{i}", TT[2] + 1.2 + i * 0.7, cx, 750)
        return svg(b), "", js
    return S("s06", ["s06-1", "s06-2", "s06-3"], build, sfx=[(("T", 0, 0.5), "notification.mp3", 0.12)])


# ============================================================ S07 01B
def s07():
    def build(TT, D):
        b = floor() + badge_g("01B", "Khai báo giá bán theo ngày", ["tay", "wms"])
        b += person("s07m", "manager", 170, s=1.7, pose=MANAGER_HOLD, hand_l=folder_svg(), tag="Quản lý", tag_col="#16478F")
        b += G("p-doc", doc(300, 190, 460, "BẢNG GIÁ BÁN", ["Áp dụng: 24/11", "Ba chỉ heo · 98.000 đ/kg", "Đùi gà · 62.000 đ/kg"], sign=False))
        b += G("p-ar", arrow(780, 330, 870, 330, ORANGE, 7))
        b += G("p-win", wms_win(890, 180, 970, "Danh mục giá bán", ["Mã hàng", "Ngày áp dụng", "Đơn giá / kg"],
                                [["NL-BC01", "24/11", "98.000 ✔"], ["NL-DG02", "24/11", "62.000 ✔"]], [260, 330, 340], status="Đã lưu"))
        b += prop(ms_desk(), 1300, 830, 1.5) + person("s07x", "xlct", 1250, s=1.5, pose=TYPE, tag="Xử lý chứng từ", tag_col=BLUE)
        b += MARK
        js = badge_js() + rise("#p-doc", TT[0] + 0.3, dy=30)
        js += rise("#p-ar", TT[1] + 0.3, dy=0) + rise("#p-win", TT[1] + 0.8, dy=30) + type_js("s07x", TT[1] + 0.5, D - 0.3)
        return svg(b), "", js
    return S("s07", ["s07-1", "s07-2"], build, sfx=[(("T", 1, 2.5), "chime.mp3", 0.12)])


# ============================================================ S09 02B B1–2
def s09():
    def build(TT, D):
        b = floor() + badge_g("02B · Bước 1–2", "Nhận ASN, nhập WMS, in LPN và tem lô", ["tay", "wms", "doc"])
        b += xdesk("s09x", 210, tag=True)
        b += G("n-mail", mail(560, 180, 520, "Nhiêu Lộc", "Kế hoạch nhập ngày 23/11", "KeHoachNhap_23-11.xlsx"))
        b += G("n-ar", arrow(1095, 300, 1160, 300, ORANGE, 7))
        b += G("n-win", wms_win(1170, 170, 690, "ASN-NL-0001 · Chờ hàng", ["Mã hàng", "SL dự kiến"],
                                [["NL-BC01", "240 thùng"], ["NL-DG02", "100 thùng"]], [300, 350], status="Đã tạo ASN"))
        b += G("n-pr", printer(620, 700))
        b += G("n-l0", lpn_tag(860, 580, "LPN-000123")) + G("n-l1", lpn_tag(860, 660, "LPN-000124"))
        b += G("n-lt", T(945, 760, "Mã LPN cho pallet", 24, 700, MUTED, "middle"))
        for k in range(3):
            b += G(f"n-q{k}", qr(1150 + k * 90, 590, 70))
        b += G("n-qt", T(1265, 700, "Tem lô QR cho thùng", 24, 700, MUTED, "middle") + T(1265, 740, "NL-BC01 · Lô 261120", 24, 800, INK, "middle"))
        b += MARK
        js = badge_js() + type_js("s09x", 0.4, D - 0.3)
        js += slide_in("#n-mail", TT[0] + 0.3, 200, 0.6) + rise("#n-ar", TT[0] + 2.0, dy=0) + rise("#n-win", TT[0] + 2.5, dy=30)
        js += rise("#n-pr", TT[1] + 0.2, dy=20)
        js += drop("#n-l0", TT[1] + 1.0) + drop("#n-l1", TT[1] + 1.3) + rise("#n-lt", TT[1] + 1.6, dy=10)
        for k in range(3):
            js += popc(f"#n-q{k}", TT[1] + 2.2 + k * 0.3, 1185 + k * 90, 625)
        js += rise("#n-qt", TT[1] + 3.0, dy=10)
        return svg(b), "", js
    return S("s09", ["s09-1", "s09-2"], build, sfx=[(("T", 0, 0.3), "notification.mp3", 0.12), (("T", 1, 1.0), "click-soft.mp3", 0.12)])


# ============================================================ S10 02B B3–4
def s10():
    def build(TT, D):
        b = floor() + badge_g("02B · Bước 3–4", "Tạo phiếu nhập, dỡ và xếp hàng", ["wms", "tay"])
        b += G("e-truck", prop(ms_truck(), 20, 830, 1.8), hidden=False) + G("e-drv", person("s10d", "driver", 650, s=1.6))
        b += G("e-pal", pallet(780, 830, lpn="LPN-000123", qrs=True))
        b += person("s10k", "receiver", 1050, s=1.7, pose={"armR": (-150, 30)}, hand_r=qr(-8, 10, 26), tag="Nhân viên kho", tag_col=GREEN)
        b += G("e-pda", pda_big(1400, 150, "Tạo phiếu nhập", [("ASN", "ASN-NL-0001", None), ("Số xe", "51D-678.90", "hl"),
                                                             ("Tài xế", "Hùng", None)], "Tạo phiếu"))
        b += G("e-chk", rect(760, 180, 560, 200, "#fff", 16, INK, 3) + T(790, 230, "Bước 4 tại cửa nhập:", 28, 800))
        for i, s in enumerate(["Kiểm tra ngoại quan", "Dán tem lô QR lên thùng", "Dán LPN lên pallet"]):
            b += G(f"e-c{i}", check(806, 270 + i * 40, 14) + T(832, 280 + i * 40, s, 25, 600))
        b += MARK
        js = badge_js() + slide_in("#e-truck", 0.0, -500, 1.2, "power2.out") + rise("#e-drv", 1.2, dy=20)
        js += rise("#e-pda", TT[0] + 0.5, dy=30)
        js += rise("#e-chk", TT[1] + 0.2) + rise("#e-pal", TT[1] + 1.4, dy=30)
        for i in range(3):
            js += rise(f"#e-c{i}", TT[1] + 1.0 + i * 1.4, dy=10)
        return svg(b), "", js
    return S("s10", ["s10-1", "s10-2"], build, lead=1.2)


# ============================================================ S11 02B B5
def s11():
    def build(TT, D):
        b = floor() + badge_g("02B · Bước 5", "Nhận hàng", ["pda"])
        b += pallet(420, 830, lpn="LPN-000123", qrs=True, rows=4)
        b += person("s11k", "receiver", 200, s=1.9, pose=SCAN, hand_r=pda_svg("s11k", laser=True, reach=90))
        b += G("r-pda", pda_big(860, 130, "Nhận hàng · ASN-NL-0001", [("Quét LPN", "LPN-000123", "ok"),
                                                                     ("Quét tem lô QR", "NL-BC01 · Lô 261120", "ok"),
                                                                     ("Số lượng (thùng)", "40", "hl"), ("Pallet đã nhận", "6 / 6", "ok")],
                                "Xác nhận hoàn tất", w=520))
        b += G("r-box", box(1440, 220, 420, 260, "Tem lô QR cho biết", ["Mã hàng · Số lô", "Hạn sử dụng", "→ WMS xuất theo FEFO"], PURPLE, 28))
        b += MARK
        js = badge_js() + rise("#r-pda", 0.3, dy=30) + laser_js("s11k", TT[0] + 0.6, 3) + rise("#r-box", TT[0] + 3.0, dy=20)
        return svg(b), "", js
    return S("s11", ["s11-1", "s11-2"], build, sfx=[(("T", 0, 0.6), "ping.mp3", 0.12)])


# ============================================================ S12 02B B6
def s12():
    def build(TT, D):
        b = floor() + badge_g("02B · Bước 6", "In và ký phiếu nhập kho", ["wms", "doc"])
        b += xdesk("s12x", 230) + printer(600, 600)
        b += G("i-doc", doc(830, 170, 540, "PHIẾU NHẬP KHO", ["ASN-NL-0001 · 23/11", "NL-BC01 · Ba chỉ heo · 240 thùng", "NL-DG02 · Đùi gà · 100 thùng"]))
        b += person("s12d", "driver", 1560, s=1.7, pose=SIGN, hand_l=PAPER, hand_r=PEN)
        b += G("i-cnt", counter(830, 690, "Tồn kho NL-BC01", 0, 240))
        b += MARK
        js = badge_js() + type_js("s12x", 0.4, TT[0] + 1.0) + rise("#i-doc", TT[0] + 0.3, dy=60, dur=0.6)
        js += sign_js("s12d", TT[0] + 1.8) + rise("#i-cnt", TT[1] + 0.3, dy=20)
        return svg(b), "", js
    return S("s12", ["s12-1", "s12-2"], build, sfx=[(("T", 1, 0.3), "chime.mp3", 0.12)])


# ============================================================ S13 02B B7 khu A
def s13():
    def build(TT, D):
        b = floor() + badge_g("02B · Bước 7", "Cất hàng – Khu A (kệ)", ["pda"])
        b += rack_pallets(700, 300, 3, 2, MAIN_RACK, {(0, 0), (1, 0), (2, 0), (0, 1)}, cw=230, lh=260)
        b += G("k-hl", rect(936, 306, 218, 242, "none", 10, GREEN, 5, 'stroke-dasharray="14 9"') + pill(1045, 255, "WMS gợi ý A-02-02", GREEN, "#fff", 24))
        b += G("k-put", pallet(950, 554))
        b += G("k-ar", arrow(470, 600, 1020, 450, GREEN, 6, True))
        b += G("k-mv", lift("s13f", 230, 830, 1.9, load=False)
               + f'<g id="k-load" transform="translate(230,830) scale(1.9)">{pallet(50, -22, cols=2, rows=2, cw=46, ch=36)}</g>', hidden=False)
        b += G("k-pda", pda_big(1430, 150, "Cất hàng", [("Quét LPN", "LPN-000123", "ok"), ("Vị trí gợi ý", "A-02-02", "hl"),
                                                       ("Quét mã vị trí", "A-02-02", "ok")], "Xác nhận cất hàng"))
        b += MARK
        js = badge_js() + rise("#k-pda", TT[0] + 0.2, dy=30) + show_js("#k-hl", TT[0] + 1.6) + pulse("#k-hl", TT[0] + 1.8, 2)
        js += show_js("#k-ar", TT[1] + 0.2) + move("#k-mv", TT[1] + 0.5, 260, 1.4)
        js += fade("#k-load", TT[1] + 2.2, 0.2) + drop("#k-put", TT[1] + 2.2, dy=-40) + fade("#k-ar", TT[1] + 2.2)
        return svg(b), "", js
    return S("s13", ["s13-1", "s13-2"], build, sfx=[(("T", 1, 2.3), "ping.mp3", 0.12)])


# ============================================================ S14 02B B7 khu B
def s14():
    def build(TT, D):
        b = floor() + badge_g("02B · Bước 7", "Cất hàng – Khu B (chất chồng)", ["pda"])
        b += stack_zone(560, 800, [("B-01", 3), ("B-02", 2), ("B-03", 1)], lw=250, ph=110)
        b += G("b-hl", rect(822, 574, 226, 114, "none", 10, GREEN, 5, 'stroke-dasharray="14 9"') + pill(935, 330, "Cùng mã · cùng lô", GREEN, "#fff", 24))
        b += G("b-put", pallet(840, 580, rows=2))
        b += lift("s14f", 210, 830, 1.9)
        b += G("b-pda", pda_big(1400, 150, "Cất hàng", [("Quét LPN", "LPN-000130", "ok"), ("Vị trí gợi ý", "B-02", "hl"),
                                                       ("Quét mã vị trí", "B-02", "ok")], "Xác nhận cất hàng"))
        b += MARK
        js = badge_js() + rise("#b-pda", 0.3, dy=30) + show_js("#b-hl", TT[0] + 1.5) + pulse("#b-hl", TT[0] + 1.7, 2)
        js += drop("#b-put", TT[0] + 4.0, dy=-50) + fade("#b-hl", TT[0] + 4.0)
        return svg(b), "", js
    return S("s14", ["s14-1", "s14-2"], build, sfx=[(("T", 0, 4.0), "ping.mp3", 0.12)])


# ============================================================ S16 03B
def s16():
    def build(TT, D):
        b = floor() + badge_g("03B", "Khoá / mở khoá lô", ["wms"])
        b += xdesk("s16x", 210, tag=True)
        b += G("l-win", wms_win(560, 170, 860, "Tồn kho theo lô · NL-BC01", ["Lô", "LPN", "Trạng thái"],
                                [["Lô 261101", "LPN-000088", "Đã khoá ✖"], ["Lô 261120", "LPN-000123", "Sẵn sàng ✔"]], [250, 290, 280], hl=0))
        b += pallet(1500, 830, lpn="LPN-000088", dim=True) + G("l-lock", lock(1595, 560, 1.6))
        b += G("l-box", box(560, 600, 860, 170, "Lô bị khoá", ["không được phân bổ xuất cho tới khi mở khoá"], RED, 30))
        b += MARK
        js = badge_js() + type_js("s16x", 0.4, TT[1]) + rise("#l-win", TT[0] + 0.3, dy=30)
        js += f'tl.fromTo("#l-lock",{{opacity:0,y:-80}},{{opacity:1,y:0,duration:0.5,ease:"bounce.out"}},{TT[0] + 2.0:.2f});\n'
        js += rise("#l-box", TT[1] + 0.3, dy=20)
        return svg(b), "", js
    return S("s16", ["s16-1", "s16-2"], build, sfx=[(("T", 0, 2.0), "error.mp3", 0.1)])


# ============================================================ S17 03C
def s17():
    def build(TT, D):
        b = floor() + badge_g("03C", "Chuyển vị trí pallet", ["pda"])
        b += stack_zone(80, 800, [("B-01", 1)], lw=250, ph=110) + G("c-top", pallet(110, 690, rows=2), hidden=False)
        b += rack_pallets(1000, 300, 2, 2, [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"]], {(1, 0), (1, 1), (0, 1)},
                          hl={(0, 0): GREEN}, cw=230, lh=260)
        b += G("c-new", pallet(1020, 814))
        b += G("c-mv", lift("s17f", 560, 830, 1.8), hidden=False)
        b += G("c-ar", arrow(250, 500, 1080, 700, GREEN, 6, True))
        b += G("c-pda", pda_big(1500, 150, "Chuyển vị trí", [("Quét LPN (vị trí cũ B-01)", "LPN-000130", "ok"),
                                                            ("Quét vị trí mới", "A-01-01", "ok")], "Xác nhận hoàn tất", w=380))
        b += MARK
        js = badge_js() + rise("#c-pda", TT[0] + 0.3, dy=30) + show_js("#c-ar", TT[0] + 1.0)
        js += fade("#c-top", TT[0] + 2.5) + move("#c-mv", TT[0] + 2.6, 160, 1.2)
        js += drop("#c-new", TT[1] + 0.4, dy=-40) + fade("#c-ar", TT[1] + 0.4)
        return svg(b), "", js
    return S("s17", ["s17-1", "s17-2"], build, sfx=[(("T", 1, 0.4), "ping.mp3", 0.12)])


# ============================================================ S18 03D
def s18():
    def build(TT, D):
        b = floor() + badge_g("03D", "Chuyển hàng pallet → pallet", ["pda"])
        b += pallet(140, 830, lpn="LPN-000123", rows=2, qrs=True)
        b += G("d-src", "".join(carton_flat(148 + c * 58, 830 - 22 - 3 * 44, 54, 40) for c in range(3)), hidden=False)
        b += pallet(760, 830, lpn="LPN-000245", rows=1, qrs=True)
        b += G("d-dst", "".join(carton_flat(768 + c * 58, 830 - 22 - 2 * 44, 54, 40) for c in range(3)))
        b += person("s18k", "receiver", 560, s=1.8, pose=CARRY, hand_l=CARTON, tag="Nhân viên kho", tag_col=GREEN)
        b += G("d-ar", arrow(300, 400, 860, 400, ORANGE, 6, True))
        b += G("d-pda", pda_big(1240, 120, "Pallet → pallet", [("Quét LPN nguồn", "LPN-000123", "ok"), ("Quét tem lô QR", "NL-BC01 · Lô 261120", "ok"),
                                                               ("Số thùng cần chuyển", "12", "hl"), ("Quét pallet mới", "LPN-000245", "ok")],
                                "Xác nhận hoàn tất", w=560))
        b += MARK
        js = badge_js() + rise("#d-pda", TT[0] + 0.3, dy=30) + show_js("#d-ar", TT[0] + 1.0)
        js += fade("#d-src", TT[0] + 3.0) + drop("#d-dst", TT[0] + 3.6, dy=-50)
        return svg(b), "", js
    return S("s18", ["s18-1", "s18-2"], build)


# ============================================================ S20 04C B1–2
def s20():
    def build(TT, D):
        b = floor() + badge_g("04C · Bước 1–2", "Nhận đơn theo kg, nhập WMS", ["tay", "wms"])
        b += xdesk("s20x", 210, tag=True)
        b += G("o-mail", mail(560, 190, 540, "Nhiêu Lộc", "Đơn đặt hàng 24/11 (kg)", "DonHang_24-11.xlsx"))
        b += G("o-ar", arrow(1115, 310, 1180, 310, ORANGE, 7))
        b += G("o-win", wms_win(1190, 180, 670, "SO-NL-0001 · Đơn xuất", ["Mã hàng", "Tên hàng", "Kg đặt"],
                                [["NL-BC01", "Ba chỉ heo", "800 kg"], ["NL-DG02", "Đùi gà", "250 kg"]], [200, 250, 180], status="Đã tạo đơn xuất"))
        b += G("o-kg", pill(830, 560, "Đặt hàng tính bằng KG", ORANGE, "#fff", 30))
        b += MARK
        js = badge_js() + type_js("s20x", 0.4, D - 0.3) + slide_in("#o-mail", TT[0] + 0.3, 200, 0.6)
        js += rise("#o-ar", TT[0] + 1.6, dy=0) + rise("#o-win", TT[0] + 2.0, dy=30) + popc("#o-kg", TT[0] + 3.5, 830, 560)
        return svg(b), "", js
    return S("s20", ["s20-1"], build, tail=1.6, sfx=[(("T", 0, 0.3), "notification.mp3", 0.12)])


# ============================================================ S21 điều kiện giá
def s21():
    def build(TT, D):
        b = floor() + badge_g("04C", "Kiểm tra giá bán", ["wms"])
        b += G("q-dia", diamond(700, 470, 700, 380, ["Đã có giá bán", "ngày phân bổ?"]))
        b += G("q-yes", arrow(1055, 470, 1330, 470, GREEN, 7) + T(1190, 445, "Có", 32, 900, GREEN, "middle")
               + box(1340, 380, 520, 180, "Bước 3: Phân bổ tồn kho", ["Tiếp tục xuất hàng"], GREEN, 30))
        b += G("q-no", arrow(700, 665, 700, 760, RED, 7) + T(735, 725, "Không", 32, 900, RED)
               + rect(450, 760, 500, 66, "#fff", 14, BLUE, 4) + T(700, 805, "Thực hiện 01B", 30, 800, BLUE, "middle"))
        b += person("s21i", "instructor", 1600, s=1.5, pose=POINT_L) + MARK
        js = badge_js() + popc("#q-dia", TT[0] + 0.3, 700, 470) + rise("#q-yes", TT[0] + 2.5, dy=0)
        js += rise("#q-no", TT[1] + 0.3, dy=-20)
        return svg(b), "", js
    return S("s21", ["s21-1", "s21-2"], build)


# ============================================================ S22 phân bổ
def s22():
    def build(TT, D):
        b = floor() + badge_g("04C · Bước 3", "Phân bổ tồn kho", ["wms"])
        b += G("f-c1", box(60, 170, 880, 330, "Quy đổi kg → thùng", ["Ba chỉ heo (đồng ký): 800 kg ÷ 20 = 40 thùng",
                                                                     "Đùi gà (đa ký): 250 kg ÷ 12 = 20,8 → 21 thùng",
                                                                     "Làm tròn gần nhất, tối thiểu 1 thùng"], GREEN))
        b += G("f-c2", box(980, 170, 880, 330, "WMS tự tách (đồng ký và đa ký)", ["Đủ 1 pallet → xuất chẵn pallet",
                                                                                 "Không đủ 1 pallet → xuất theo thùng",
                                                                                 "Ba chỉ heo 40 thùng = 1 pallet", "Đùi gà 21 thùng (pallet 50)"], BLUE))
        b += G("f-k1", pill(1640, 346, "→ CHẴN PALLET", BLUE, "#fff", 20)) + G("f-k2", pill(1640, 391, "→ THEO THÙNG", ORANGE, "#fff", 20))
        b += G("f-lot", rect(60, 530, 1300, 270, "#fff", 18, ORANGE, 4) + T(90, 580, "Chọn lô (hôm nay 24/11/2026)", 30, 900, ORANGE))
        b += G("f-l1", rect(90, 600, 560, 180, "#FFF1DF", 14, ORANGE, 3) + T(112, 645, "Mặc định · FEFO", 27, 900, ORANGE)
               + T(112, 690, "Lô 260601 · HSD 01/06/2027", 25, 800) + T(112, 735, "hết hạn trước → chọn", 25, 700, ORANGE) + check(605, 640, 20))
        b += G("f-l2", rect(680, 600, 650, 180, "#F1ECFE", 14, PURPLE, 3) + T(702, 645, "Đơn chỉ định · HSD còn lại > 70%", 27, 900, PURPLE)
               + T(702, 690, "Lô 260601 · còn 52%", 25, 800, MUTED) + cross(1040, 682, 17) + T(702, 735, "Lô 261105 · còn 95%", 25, 800) + check(1040, 727, 17))
        b += G("f-pr", box(1400, 530, 460, 270, "Đơn giá", ["theo ngày phân bổ 24/11", "Ba chỉ heo 98.000 đ/kg", "Đùi gà 62.000 đ/kg"], BLUE, 30))
        b += MARK
        js = badge_js() + rise("#f-c1", TT[0] + 0.3, dy=30) + rise("#f-c2", TT[1] + 0.2, dy=30)
        js += popc("#f-k1", TT[1] + 3.0, 1640, 346) + popc("#f-k2", TT[1] + 4.0, 1640, 391)
        js += rise("#f-lot", TT[2] + 0.2) + rise("#f-l1", TT[2] + 1.0, dy=15) + rise("#f-l2", TT[2] + 3.0, dy=15) + rise("#f-pr", TT[2] + 5.5, dy=20)
        return svg(b), "", js
    return S("s22", ["s22-1", "s22-2", "s22-3"], build, tail=1.6)


# ============================================================ S23 chẵn pallet
def s23():
    def build(TT, D):
        b = floor() + badge_g("04C · Bước 4–5", "In phiếu lấy hàng · Lấy chẵn pallet", ["doc", "pda"])
        b += G("h-doc", doc(60, 160, 380, "PHIẾU LẤY HÀNG", ["SO-NL-0001", "B-02 · 1 pallet", "A-01-01 · 21 thùng"], sign=False))
        b += stack_zone(520, 800, [("B-02", 2)], lw=250, ph=110) + G("h-top", pallet(550, 580, rows=2), hidden=False)
        b += G("h-sug", rect(532, 684, 226, 116, "none", 10, ORANGE, 5, 'stroke-dasharray="14 9"'))
        b += G("h-pick", rect(532, 464, 226, 116, "none", 10, GREEN, 5, 'stroke-dasharray="14 9"') + pill(645, 432, "Lấy LPN-000130 · cùng lô", GREEN, "#fff", 22))
        b += G("h-lift", lift("s23f", 1090, 830, 1.9, load=False, flip=True))
        b += G("h-pda", pda_big(1400, 120, "Lấy hàng · SO-NL-0001", [("Đi tới vị trí", "B-02", "hl"),
                                                                    ("WMS gợi ý (dưới cùng, khó lấy)", "LPN-000128", None),
                                                                    ("Quét LPN thực lấy", "LPN-000130", "ok"),
                                                                    ("Cùng mã · cùng lô 261120?", "Hợp lệ · 40 thùng", "ok")],
                                "→ Khu chờ xuất", w=470))
        b += MARK
        js = badge_js() + rise("#h-doc", TT[0] + 0.3, dy=30)
        js += slide_in("#h-lift", TT[1] + 0.2, 300, 1.0) + rise("#h-pda", TT[1] + 0.5, dy=30)
        js += show_js("#h-sug", TT[1] + 1.5) + pulse("#h-sug", TT[1] + 1.7, 2) + show_js("#h-pick", TT[1] + 4.0)
        js += f'tl.to("#h-top",{{y:-40,x:300,opacity:0,duration:1.0,ease:"power1.in"}},{TT[2] + 2.5:.2f});\n' + fade("#h-pick", TT[2] + 2.5)
        return svg(b), "", js
    return S("s23", ["s23-1", "s23-2", "s23-3"], build, sfx=[(("T", 2, 0.5), "ping.mp3", 0.12)])


# ============================================================ S24 theo thùng
def s24():
    def build(TT, D):
        b = floor() + badge_g("04C · Bước 5", "Lấy hàng theo thùng", ["pda"])
        b += rack_pallets(120, 300, 2, 2, [["A-01-01", "A-01-02"], ["A-02-01", "A-02-02"]],
                          {(0, 0): {"rows": 2, "lpn": "LPN-000140"}, (1, 0): None, (0, 1): None, (1, 1): None}, hl={(0, 0): ORANGE}, cw=240, lh=260)
        b += G("u-tr", prop(ms_trolley(), 700, 830, 1.6), hidden=False)
        b += fig("u-p", "picker", 660, s=1.8, pose=SCAN, hand_r=pda_svg("u-p", laser=True, reach=80), tag="Nhân viên kho", tag_col="#B88C00")
        b += G("u-pda", pda_big(1220, 120, "Lấy hàng · SO-NL-0001", [("Đi tới vị trí", "A-01-01", "hl"), ("Quét vị trí", "A-01-01", "ok"),
                                                                    ("Quét LPN (lấy từ pallet nào)", "LPN-000140", "ok"),
                                                                    ("Quét tem lô QR", "NL-DG02 · Lô 260601", "ok"), ("Số lượng (thùng)", "21 / 21", "ok")],
                                w=520))
        b += G("u-out", pill(880, 230, "→ Khu chờ xuất", ORANGE, "#fff", 26))
        b += MARK
        js = badge_js() + show_js("#u-p-tag", 0.3) + rise("#u-pda", 0.3, dy=30) + laser_js("u-p", TT[0] + 1.5, 4)
        js += popc("#u-out", TT[2] + 0.2, 880, 230)
        js += move("#u-tr", TT[2] + 0.8, 900, 1.6, ease="power1.in") + move("#u-p-w", TT[2] + 0.8, 900, 1.6, ease="power1.in")
        js += fade("#u-p-tag", TT[2] + 0.8) + walk_js("u-p", TT[2] + 0.8, TT[2] + 2.4)
        return svg(b), "", js
    return S("s24", ["s24-1", "s24-2", "s24-3"], build, tail=1.4, sfx=[(("T", 0, 1.5), "ping.mp3", 0.12)])


# ============================================================ S25 xác nhận ra kho
def s25():
    def build(TT, D):
        b = floor() + badge_g("04C · Bước 6–7", "Xác nhận ra kho", ["pda", "can"])
        b += G("x-c1", box(60, 170, 620, 330, "Đồng ký · Ba chỉ heo", ["Quét tem lô QR ✔", "Xác nhận 40 thùng", "Kg = 40 × 20 = 800 kg"], GREEN)
               + check(620, 230, 26))
        b += scale_svg(720, 830, "11,8 kg") + G("x-ct", prop(carton_flat(0, 0, 60, 44, "DG02"), 770, 696, 2.4))
        b += person("s25c", "checker", 1110, s=1.8, pose=SCAN, hand_r=pda_svg("s25c", laser=True, reach=70), tag="Nhân viên kho", tag_col=PURPLE)
        b += G("x-pda", pda_big(1300, 110, "Ra kho · Đùi gà (đa ký)", [("Quét tem lô QR", "NL-DG02 · Lô 260601", "ok"),
                                                                      ("Kg thùng 7 / 21", "11,8", "hl"), ("Tổng kg đã nhập", "82,9 kg", None)],
                                "Xác nhận", w=560))
        b += G("x-dia", diamond(370, 690, 560, 220, ["Số thùng nhập kg", "= số thùng đã lấy?"]))
        b += MARK
        js = badge_js() + rise("#x-c1", TT[1] + 0.2, dy=30)
        js += drop("#x-ct", TT[2] + 0.2, dy=-80, dur=0.5) + rise("#x-pda", TT[2] + 0.6, dy=30) + laser_js("s25c", TT[2] + 1.2, 2)
        js += popc("#x-dia", TT[2] + 2.6, 370, 690)
        return svg(b), "", js
    return S("s25", ["s25-1", "s25-2", "s25-3"], build, tail=1.4)


# ============================================================ S26 hoàn tất
def s26():
    def build(TT, D):
        b = floor() + badge_g("04C · Bước 8", "Hoàn tất, in phiếu xuất kho / giao hàng", ["wms", "doc"])
        b += G("y-doc", doc(60, 160, 900, "PHIẾU XUẤT KHO / GIAO HÀNG", ["SO-NL-0001 · Ngày 24/11",
                                                                        "Ba chỉ heo · 800 kg × 98.000 = 78.400.000 đ",
                                                                        "Đùi gà · 248,6 kg × 62.000 = 15.413.200 đ",
                                                                        "Tổng cộng: 93.813.200 đ"]))
        b += prop(ms_truck(), 1100, 830, 1.8) + G("y-pal", pallet(1250, 690, cols=2, rows=2, cw=50, ch=38))
        b += person("s26d", "driver", 1050, s=1.7, pose=SIGN, hand_l=PAPER, hand_r=PEN)
        b += G("y-f", box(60, 700, 900, 110, "Thành tiền = kg thực xuất × đơn giá", (), BLUE, 30))
        b += MARK
        js = badge_js() + rise("#y-doc", TT[0] + 0.3, dy=30) + rise("#y-f", TT[0] + 2.5, dy=15)
        js += sign_js("s26d", TT[1] + 0.5) + drop("#y-pal", TT[1] + 1.5, dy=-40)
        return svg(b), "", js
    return S("s26", ["s26-1", "s26-2"], build, sfx=[(("T", 1, 1.5), "chime.mp3", 0.12)])


# ============================================================ S28 kiểm kê
def s28():
    def build(TT, D):
        b = floor() + badge_g("05B · Bước 1–2", "Tạo phiên kiểm kê, đếm hàng", ["wms", "pda"])
        b += prop(ms_desk(), 200, 830, 1.4) + person("s28x", "xlct", 160, s=1.4, pose=TYPE, tag="Xử lý chứng từ", tag_col=BLUE)
        b += stack_zone(520, 800, [("B-02", 3)], lw=250, ph=110)
        b += G("v-k", person("s28k", "receiver", 860, s=1.8, pose=SCAN, hand_r=pda_svg("s28k", laser=True, reach=80), tag="Nhân viên kho", tag_col=GREEN))
        b += G("v-pda", pda_big(1220, 110, "Kiểm kê · KK-2411-01", [("Quét vị trí", "B-02", "ok"), ("Quét LPN", "LPN-000131", "ok"),
                                                                   ("Quét tem lô QR", "NL-BC01 · Lô 261120", "ok"), ("Số lượng (thùng)", "38", "hl")],
                                w=560))
        b += MARK
        js = badge_js() + type_js("s28x", 0.4, TT[1])
        js += rise("#v-k", TT[1] + 0.1, dy=30) + rise("#v-pda", TT[1] + 0.5, dy=30) + laser_js("s28k", TT[1] + 1.2, 4)
        return svg(b), "", js
    return S("s28", ["s28-1", "s28-2"], build, sfx=[(("T", 1, 1.2), "ping.mp3", 0.12)])


# ============================================================ S29 chênh lệch
def s29():
    def build(TT, D):
        b = floor() + badge_g("05B · Bước 3–5", "Báo cáo chênh lệch, đếm lại, điều chỉnh", ["wms"])
        b += G("w-win", wms_win(60, 170, 1000, "Báo cáo chênh lệch · KK-2411-01", ["Vị trí", "LPN", "Hệ thống", "Đếm", "Lệch"],
                                [["B-02", "LPN-000131", "40", "38", "−2 ✖"], ["A-01-01", "LPN-000140", "50", "50", "0 ✔"]],
                                [170, 280, 190, 150, 170], hl=0))
        b += person("s29m", "manager", 260, s=1.5, pose=MANAGER_HOLD, hand_l=folder_svg(), tag="Quản lý kho", tag_col="#16478F")
        b += G("w-dia", diamond(1440, 360, 620, 260, ["Cần đếm lại", "vị trí chênh lệch?"]))
        b += G("w-yes", arrow(1440, 495, 1440, 560, ORANGE, 7) + T(1470, 540, "Có", 30, 900, ORANGE) + box(1180, 565, 520, 110, "Đếm lần 2, lần 3", (), ORANGE, 30))
        b += G("w-no", arrow(1135, 360, 1060, 600, GREEN, 7) + T(1050, 500, "Không", 30, 900, GREEN, "end") + box(560, 600, 480, 110, "Điều chỉnh tồn kho", (), GREEN, 30))
        b += MARK
        js = badge_js() + rise("#w-win", TT[0] + 0.3, dy=30)
        js += popc("#w-dia", TT[1] + 0.3, 1440, 360) + rise("#w-yes", TT[1] + 2.0, dy=-15) + rise("#w-no", TT[1] + 3.5, dy=-15)
        return svg(b), "", js
    return S("s29", ["s29-1", "s29-2"], build, sfx=[(("T", 0, 0.3), "notification.mp3", 0.12)])


# ============================================================ S30 kết
def s30():
    ben = [("Tồn kho theo lô, hạn dùng", "Xuất đúng FEFO, khoá lô khi cần", GREEN),
           ("Biết từng pallet ở đâu", "Cả khu kệ lẫn khu chất chồng", BLUE),
           ("Xuất theo kg chính xác", "Chẵn pallet hay lẻ thùng, có thành tiền", ORANGE),
           ("Kiểm kê bằng quét mã", "Chênh lệch có báo cáo ngay", PURPLE)]

    def build(TT, D):
        b = floor() + G("z-h", T(90, 150, "Nhiêu Lộc nhận được gì?", 60, 900)) + G("z-logo", logo(1450, 60, 400))
        for i, (t_, s, col) in enumerate(ben):
            x, y = 90 + (i % 2) * 740, 210 + (i // 2) * 290
            b += G(f"z-b{i}", rect(x, y, 710, 250, "#fff", 22, col, 5) + check(x + 70, y + 80, 34)
                   + T(x + 130, y + 95, t_, 36, 900) + T(x + 130, y + 150, s, 27, 600, MUTED))
        b += fig("z-i", "instructor", 1680, s=2.0)
        js = rise("#z-h", 0.0) + rise("#z-logo", 0.2, dy=-16)
        for i in range(4):
            js += rise(f"#z-b{i}", TT[0] + 0.3 + i * 0.9, dy=30)
        js += wave_js("z-i", TT[2])
        return svg(b), "", js
    return S("s30", ["s30-1", "s30-2", "s30-3"], build, tail=2.5, sfx=[(("T", 2, 0.0), "chime.mp3", 0.12)])


def scenes():
    return [s04(),
            Chap(1, ["Thiết lập", "dữ liệu"]), s06(), s07(),
            Chap(2, ["Nhập hàng", "và cất hàng"]), s09(), s10(), s11(), s12(), s13(), s14(),
            Chap(3, ["Quản lý", "trong kho"]), s16(), s17(), s18(),
            Chap(4, ["Xuất hàng", "theo kg"]), s20(), s21(), s22(), s23(), s24(), s25(), s26(),
            Chap(5, ["Kiểm kê"]), s28(), s29(), s30()]
