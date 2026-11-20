"""Cast sheet for the CXAD video. Run: python3 tools/cxad_cast.py -> design/cxad-cast.html (+ png via playwright)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import C, FONT, ROLE, font_css, stick

ROOT = os.path.join(os.path.dirname(__file__), "..")
CAST = [("xlct", "Xử lý chứng từ (XLCT)", "Nhận file, nhập WMS, in chứng từ", False),
        ("receiver", "Nhân viên nhận hàng", "Tạo phiếu nhập, nhận hàng", False),
        ("forklift", "Tài xế xe nâng", "Putaway bằng xe nâng", False),
        ("picker", "Picker", "Lấy hàng theo Picklist, chia hàng", False),
        ("manager", "Quản lý kho", "Xử lý thiếu / thừa", True),
        ("checker", "Checker", "Kiểm hàng, in giấy bàn giao", False),
        ("driver", "Tài xế", "Nhận hàng lên xe, ký bàn giao", True)]
cells = ""
for role, name, job, new in CAST:
    tag = (f'<div style="position:absolute;top:14px;right:14px;background:{C["orange"]};color:#1B2430;font-weight:900;font-size:20px;'
           f'border-radius:10px;padding:2px 10px">MỚI</div>') if new else ""
    cells += (f'<div style="position:relative;width:214px;background:#fff;border:3px solid #1B2430;border-radius:22px;padding:16px 10px 18px;text-align:center">{tag}'
              f'<svg width="200" height="300" viewBox="-110 -320 220 330">{stick(role, role, 2.0)}</svg>'
              f'<div style="font-size:24px;font-weight:900;line-height:1.2;min-height:58px">{name}</div>'
              f'<div style="font-size:19px;font-weight:700;color:{C["muted"]};margin-top:6px">{job}</div></div>')
html = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{font_css('../video-cxad-giay/assets/fonts/')}
body{{margin:0;width:1920px;height:1080px;background:{C['ground']};font-family:{FONT};color:#1B2430}}</style></head><body>
<div style="padding:60px 70px 0"><div style="font-size:60px;font-weight:900">Nhân vật – Video quy trình kho CXAD</div>
<div style="font-size:30px;font-weight:700;color:{C['blue']};margin-top:6px">Giữ kiểu người que model v2 · nhãn "MỚI" = nhân vật mới cho video này</div></div>
<div style="display:flex;gap:14px;padding:50px 70px;flex-wrap:nowrap">{cells}</div></body></html>"""
out = os.path.join(ROOT, "design", "cxad-cast.html")
open(out, "w", encoding="utf-8").write(html)
print(out)
