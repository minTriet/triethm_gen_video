"""Storyboard PDF for review. Run after snapshots exist: python3 tools/cxad_storyboard.py <frames_dir>"""
import os, sys, glob, html
sys.path.insert(0, os.path.dirname(__file__))
import build_cxad as b
from build_full import assemble
from kit import font_css

import importlib
FR = sys.argv[1]
MOD = importlib.import_module(sys.argv[2] if len(sys.argv) > 2 else "build_cxad")
NAME = sys.argv[3] if len(sys.argv) > 3 else "cxad-storyboard"
SUB = sys.argv[4] if len(sys.argv) > 4 else None
ROOT = os.path.join(os.path.dirname(__file__), "..")
TITLES = ["Mở đầu", "Sơ đồ kho CXAD",
          "Bước 1–2 · Nhận ASN, nhập WMS, in LPN", "Bước 3 · Tạo phiếu nhập", "Bước 4–5 · Chuẩn bị pallet, chất hàng",
          "Bước 6 · Nhận hàng trên PDA", "Bước 7–9 · Putaway bằng xe nâng", "Điều kiện · Còn pallet chưa nhận?",
          "Bước 10–11 · Hoàn tất nhận hàng, in & ký phiếu nhập kho", "Ghi nhớ Phần 1",
          "Bước 1–2 · Nhận kế hoạch xuất, import DO", "Bước 3 · Tạo lệnh xuất gộp (Master DO)", "Bước 4 · Phân bổ tồn kho",
          "Bước 5 · In Picklist", "Bước 6–7 · Lấy hàng bằng giấy, đưa về khu chia", "Bước 8 · Xác nhận lấy hàng", "Ghi nhớ Phần 2",
          "Bước 1 · Chuẩn bị khu chia", "Bước 2 · Chia hàng + điều kiện Đã chia hết hàng?",
          "Điều kiện Có thiếu / thừa? · Bước 3 Xử lý chênh lệch (thủ công)", "Ghi nhớ Phần 3",
          "Bước 1–2 · Kiểm hàng, xử lý sai lệch", "Bước 3–5 · In giấy bàn giao, tài xế ký, hoàn tất", "Ghi nhớ Phần 4", "Kết"]
TITLES = getattr(MOD, "TITLES", TITLES)
placed, total = assemble(MOD.timeline())
frames = sorted(glob.glob(os.path.join(FR, "frame-*.png")))
rows, k, n = "", 0, 0
for s, start in placed:
    if getattr(s, "is_chapter", False):
        title = getattr(MOD, "CHAPTERS", None) or {"chap1": "Phần 1 – Nhập hàng và Putaway bằng LPN", "chap2": "Phần 2 – Lấy hàng gộp theo xe bằng giấy",
                 "chap3": "Phần 3 – Chia hàng theo đơn DO", "chap4": "Phần 4 – Kiểm hàng và Bàn giao"}
        title = title[s.cid]
        rows += f'<h2>{title}</h2>'
        continue
    n += 1
    m, sec = divmod(int(start), 60)
    caps = "".join(f"<li>{html.escape(l)}</li>" for l in s.lines) or "<li><i>(không phụ đề)</i></li>"
    rows += (f'<div class="sc"><img src="file://{os.path.abspath(frames[k])}"><div class="tx"><div class="no">Cảnh {n} · {m}:{sec:02d} · {s.D:.0f}s</div>'
             f'<div class="ti">{TITLES[k]}</div><ul>{caps}</ul><div class="ok">☐ Chốt &nbsp;&nbsp; ☐ Sửa: ..............................</div></div></div>')
    k += 1
doc = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{font_css('file://' + os.path.abspath(os.path.join(ROOT, 'video-cxad/assets/fonts')) + '/')}
@page{{size:A4 landscape;margin:12mm}}body{{font-family:'Be Vietnam Pro';color:#1B2430;margin:0}}
h1{{font-size:26px;margin:0 0 4px}}.sub{{font-size:13px;color:#6B7685;margin-bottom:10px}}
h2{{font-size:18px;background:#1F5FBF;color:#fff;padding:6px 12px;border-radius:6px;margin:14px 0 8px;break-after:avoid}}
.sc{{display:flex;gap:14px;border:1.5px solid #D5DBE4;border-radius:8px;padding:8px;margin-bottom:8px;break-inside:avoid}}
.sc img{{width:330px;height:186px;border-radius:4px;border:1px solid #D5DBE4}}.tx{{flex:1;font-size:13px}}
.no{{color:#C45A00;font-weight:900}}.ti{{font-size:16px;font-weight:900;margin:2px 0 4px}}ul{{margin:0;padding-left:18px}}li{{margin-bottom:2px}}
.ok{{margin-top:8px;color:#6B7685}}</style></head><body>
<h1>{getattr(MOD, "SB_TITLE", "Storyboard – Video quy trình toàn kho CXAD")}</h1><div class="sub">{SUB or "Bản v3 (xử lý chênh lệch khi chia hàng và xử lý sai lệch khi kiểm hàng: thủ công)"} · tổng {int(total)//60}:{int(total)%60:02d} · {n} cảnh + 4 thẻ phần · ảnh chụp ở khoảng 80% mỗi cảnh · lời = phụ đề nguyên văn</div>
{rows}</body></html>"""
out = os.path.join(ROOT, "design", NAME + ".html")
open(out, "w", encoding="utf-8").write(doc)
print(out, n)
