# PROMPT VIDEO – QUY TRÌNH KHO CƠ BẢN VỚI WMS · v1 (nháp, chờ duyệt storyboard)

> Mục đích: video nhập môn cho nhân sự kho mới / khách hàng mới của WMS — thấy trọn vòng **nhập → cất → xuất**
> và WMS ghi nhận gì ở từng bước. Storyboard: `design/storyboard-wms-co-ban.html` (dựng bằng `tools/build_storyboard_wms.py`).

## Nguồn sự thật
Vault `triethm_company_brain_vault`, ghi chú **WMS - Bộ quy trình To-Be chuẩn**, spec tiếng Việt
`03-Resources/Diagrams/WMS/To-Be/specs/VI/To_Be_3_Barcode_Item_VI.spec.json`:
- **02C Nhập hàng mới - Barcode mã hàng**: 1 Nhận ASN (thủ công) · 2 Nhập vào WMS · 3 Tạo phiếu nhập (PDA) ·
  4 Dỡ/Xếp hàng (thủ công) · 5 Nhận hàng (quét mã + số lượng) · 6 In và ký → Phiếu nhập kho · 7 Cất hàng vào vị trí (quét).
- **04C Xuất kho theo đơn - Barcode**: 1 Nhận kế hoạch xuất (thủ công) · 2 Nhập vào WMS · 3 Phân bổ tồn kho (FIFO/FEFO) ·
  4 Lấy hàng (quét vị trí + hàng) · 5 Kiểm hàng (quét) · 6 Hoàn tất → Phiếu xuất kho.

Chọn biến thể **Barcode mã hàng (cấp 3)** vì là mức cơ bản nhất có dùng máy quét — không cần LPN hay QRCode.

## Phạm vi
- Có: 02C (7 bước) + 04C (6 bước), mở đầu, toàn cảnh, 3 vai, 2 thẻ chương, 2 thẻ Ghi nhớ, tổng kết.
- Không: 01A thiết lập chủ hàng, 03 nội bộ kho, 05 kiểm kê, 07 xe ra/vào, cách xử lý thiếu/thừa (chỉ minh họa WMS báo lệch).

## Vai (skill `nhan-vat-kho`)
Nhân viên XLCT = `xlct` · Nhân viên kho = `receiver` (nhập/cất), `picker` (lấy hàng), `checker` (kiểm hàng) — cùng nhãn
"Nhân viên kho" như lane chuẩn · Tài xế = `driver` · Giảng viên = `instructor`.

## Phong cách (giữ bộ đã chốt của repo)
Tiếng Việt, 1920×1080, 30 fps, Be Vietnam Pro, nền #F4F6F9, xanh #1F5FBF / cam #F28C1E / xanh lá #22A55A / đỏ #D93B3B.
Badge "Bước n" + nhãn loại bước lấy từ chú giải To-Be: THỦ CÔNG (cam) · WMS (xanh) · QUÉT PDA (tím) · CHỨNG TỪ (xám).
PDA phóng to khi quét. Phụ đề nhịp 1.3× → khoảng 2:11. Âm thanh thưa (≥ 4 s). Mã hàng, vị trí, số xe, số lượng là minh họa.

## Câu hỏi chờ chốt
1. Biến thể: Barcode mã hàng (02C + 04C) — hay Giấy (02A + 04A) / LPN (02B + 04C)?
2. Giọng đọc: chỉ phụ đề (như video kho khô) hay lồng tiếng VieNeu-TTS (như video Hành trình)?
