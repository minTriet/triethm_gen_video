---
name: nhan-vat-kho
description: Bộ nhân vật mặc định (người que model v3) cho mọi video training kho trong repo này - nhận hàng, xe nâng, điều phối/XLCT, quản lý kho, picker, checker, vận tải/tài xế xe tải, giảng viên. Dùng khi viết prompt, kịch bản hoặc dựng cảnh có người trong video kho, khi cần chọn vai, màu áo, đạo cụ hay tư thế.
---

# Bộ nhân vật mặc định – video training kho

Mọi video kho mới dùng bộ này, không vẽ lại nhân vật. Bảng duyệt: `design/model-sheet-v3.png`
(dựng lại bằng `python3 tools/model_sheet.py`, chụp `design/model-sheet.html` ở 1920×1080).
Code vẽ: `tools/kit.py` → `stick(fid, role, ...)`; màu và nhãn trong `ROLE`, kiểu áo trong `OUTFIT`.

## Vai

| `role` | Nhãn mặc định | Hình | Đạo cụ / tư thế quen thuộc |
| --- | --- | --- | --- |
| `receiver` | Nhân viên nhận hàng | Áo + mũ bảo hộ xanh lá `#2FAE5F` | Bê thùng, dán LPN, PDA |
| `forklift` | Tài xế xe nâng | Áo + mũ cam `#F28C1E` | Xe nâng ngồi lái (`forklift()` trong `tools/model_sheet.py`) |
| `planner` | Nhân viên điều phối (dùng cả cho **Nhân viên XLCT**) | Sơ mi xanh dương `#1F5FBF`, không mũ | Ngồi bàn máy tính (`desk()`) |
| `manager` | **Quản lý kho** (gộp cả "Quản lý") | Mũ bảo hộ trắng, sơ mi trắng, cà vạt + thẻ đeo xanh đậm `#16478F` | Bìa hồ sơ: `pose=MANAGER_HOLD, hand_l=folder_svg()`; xem báo cáo WMS; chỉ tay giao việc. Mẫu: `design/model-quan-ly.png` |
| `picker` | Picker | Áo + mũ vàng `#F4C430` | Kéo trolley, PDA, lấy hàng, chia hàng |
| `checker` | Checker | Áo + mũ tím `#8B5CF6` | Scan bằng PDA (`pda_svg(fid, laser=True)`) |
| `transport` | Đội vận tải (dùng cả cho **Tài xế xe tải**) | Áo + mũ xám `#8C96A3` | Đứng cạnh xe tải, ký giấy |
| `instructor` | Giảng viên | Sơ mi xanh, cà vạt cam | Vẫy tay mở đầu, giơ tay chào kết |

Đổi nhãn theo video (ví dụ "Nhân viên XLCT", "Tài xế xe tải") nhưng giữ nguyên `role` và màu.

## Quy tắc chung

- Nét v2: đầu tròn, mắt chấm, miệng cười, thân nét đen có vai, khuỷu tay, đầu gối.
- **Bàn tay tròn** (hình tròn trắng viền đen), không ngón tay, cho mọi vai và mọi động tác; không dùng cử chỉ bằng ngón tay (không giơ ngón cái).
- Vai làm việc ngoài kho đội mũ bảo hộ + áo có sọc phản quang; vai văn phòng (điều phối/XLCT, giảng viên) mặc sơ mi, không mũ; quản lý kho mặc sơ mi nhưng đội mũ bảo hộ trắng.
- Đi bộ = cả người nghiêng trái/phải + nhún nhẹ (`walk_js`), tay chân giữ tư thế.
- Nhãn tên trên đầu (`label=True`) chỉ hiện ở lần xuất hiện đầu tiên của vai.
- Thêm vai mới: thêm vào `ROLE` + `OUTFIT` trong `tools/kit.py`, thêm ô vào `tools/model_sheet.py`, dựng lại bảng, gửi người dùng duyệt rồi mới dùng trong video, và cập nhật bảng trên.
