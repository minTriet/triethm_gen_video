# CONTEXT VIDEO TRAINING – QUY TRÌNH TOÀN KHO CXAD (LẤY HÀNG BẰNG GIẤY) · v1 (bản nháp để duyệt)

> Nguồn: `source/CXAD_Warehouse_Processes_Paper_Picking_VI.pdf` (5 quy trình: 01A, 02F, 04K.1, 04K.2, 04K.3).
> Video riêng, độc lập với video "Vận hành kho khô" và video "Hàng TC". Giữ nguyên mọi quyết định đã chốt trước đây:
> không giọng đọc, chỉ phụ đề (lời thoại bên dưới = phụ đề nguyên văn), nhịp đọc 1.3×,
> hiệu ứng âm thanh thưa (≥ 4 s), nhân vật model v2, kiểu đi nghiêng-nhún, cùng màu, font Be Vietnam Pro.
> Mã hàng, mã xe, số DO, vị trí, số lượng là **ví dụ minh họa**.
> Dự kiến **khoảng 4 phút 30 giây – 5 phút** (1 video liền, chia 5 chương, mỗi chương có thẻ chương và thẻ "Ghi nhớ").

---

## Ý chính người xem phải nhớ
Kho CXAD chạy theo một dòng liền mạch:
**Tạo chủ hàng & dữ liệu gốc → Nhập hàng bằng LPN & cất hàng → Gộp đơn theo xe, lấy hàng bằng Picklist giấy theo khu
→ Chia hàng về từng DO → Kiểm hàng, bàn giao cho tài xế.**
Ba điểm khác với kho khô trước đây:
1. Kho có **3 khu nhiệt độ: Đông / Chill / Khô**, Picklist được **tách theo khu**.
2. Xuất hàng **gộp theo xe**: các DO đi cùng 1 xe gộp thành **1 Master DO**, lấy hàng tổng rồi mới **chia về từng DO**.
3. Lấy hàng **bằng giấy**: ghi số thực lấy lên Picklist, XLCT nhập lại vào WMS.

## Vai trò (lane trong file gốc) và nhân vật

| Vai trong quy trình | Xuất hiện ở | Nhân vật (đề xuất) |
| --- | --- | --- |
| Quản lý | 01A | Áo sơ mi trắng, cà vạt xanh đậm |
| Xử lý chứng từ (XLCT) | 01A, 02F, 04K.1, 04K.3 | Áo xanh dương, ngồi bàn máy tính (= "Nhân viên điều phối" cũ) |
| Nhân viên kho | 02F, 04K.1, 04K.2 | Áo vàng, cầm PDA / kẹp Picklist giấy, đẩy xe pallet tay |
| Quản lý kho | 04K.2 | Áo xanh đậm, đội mũ bảo hộ trắng |
| Checker | 04K.3 | Áo tím, PDA |
| Tài xế | 04K.3 | Áo xám, cạnh xe tải |
| Giảng viên (mở / kết) | Mở đầu, Kết | Áo xanh dương, cà vạt cam (giữ như cũ) |

## Quy ước hình theo chú thích của file gốc
Mỗi bước có badge "Bước n" và **thêm 1 nhãn nhỏ cho biết bước đó làm ở đâu**, lấy đúng ký hiệu trong trang chú thích:
- **WMS** – khung trắng viền xanh (thao tác trên WMS)
- **Thủ công** – khung cam (thao tác tay, không qua hệ thống)
- **Quét PDA** – icon máy quét (scan barcode / QR)
- **Chứng từ** – hình tờ giấy lượn sóng (Mã vạch LPN, Phiếu nhập kho, Picklist giấy, Giấy bàn giao) bay ra góc phải khi được tạo
- Điều kiện (hình thoi) → hiện thành câu hỏi lớn có 2 nhánh "Có / Không".
- File có ký hiệu "Thao tác trên ERP" (xanh lá) và "Quy trình con" nhưng **không bước nào dùng**, nên video không đưa vào.

## Sơ đồ kho dùng trong video (cần dựng mới)
Nhìn từ trên xuống, từ trái sang phải: **Dock nhận hàng → 3 khu kệ: ĐÔNG (xanh băng, có hơi lạnh) · CHILL (xanh ngọc) · KHÔ (be)
→ Khu chia (các ô sàn ghi số DO) → Khu kiểm hàng → Dock xuất, xe tải.** Văn phòng XLCT ở góc trên.

## Dữ liệu minh họa dùng xuyên suốt
- Chủ hàng: **CXAD – Bán lẻ**
- Mã hàng: **SKU 1001** Há cảo (Đông, 20 gói/thùng) · **SKU 2001** Sữa chua (Chill, 50 hũ/thùng) · **SKU 3001** Bánh quy (Khô, 24 hộp/thùng)
- Nhập: **ASN-0001**, xe **51C-123.45**, 3 pallet, **LPN-000101 → LPN-000103**; ví dụ LPN-000102: SKU 2001 · 40 thùng · HSD 20/05/2027 · Batch B2405; vị trí gợi ý **CHILL-A01-02**
- Xuất: xe **XE-01** chở 3 DO: **DO-1001, DO-1002, DO-1003** → gộp thành **MDO-0001**
- Ví dụ thùng + pcs (đúng ví dụ trong file gốc): SKU 2001 – DO-1001 cần 20, DO-1002 cần 30, DO-1003 cần 5 → **tổng 55 hũ = 1 thùng 5 hũ** (quy cách 50)

---

## Kịch bản (lời thoại = phụ đề)

### Mở đầu (~15s)
- **Hình:** tiêu đề "Quy trình vận hành kho CXAD – Lấy hàng bằng giấy". Giảng viên vẫy tay. Dải 5 chặng hiện lần lượt:
  Tạo chủ hàng → Nhập hàng & Putaway → Lấy hàng gộp theo xe → Chia hàng theo DO → Kiểm & Bàn giao.
  Sau đó camera lướt qua sơ đồ kho, 3 khu Đông / Chill / Khô sáng lần lượt.
- **Lời:** "Xin chào các bạn. Video này đi qua toàn bộ quy trình của kho CXAD, từ lúc tạo chủ hàng đến lúc giao hàng lên xe." / "Kho có ba khu theo nhiệt độ: khu đông, khu chill và khu khô."

### Chương 1 – Tạo chủ hàng mới (01A) (~30s)
1. **Bước 1 – Tạo chủ hàng mới** [WMS] · Quản lý ngồi máy tính, màn hình WMS có thẻ mới "CXAD – Bán lẻ" bật ra.
   **Lời:** "Đầu tiên, quản lý tạo chủ hàng bán lẻ mới trên WMS."
2. **Bước 2 – Tạo dữ liệu gốc** [WMS] · XLCT điền lần lượt 5 thẻ: Nhóm loại hàng · Loại hàng (Đông / Chill / Khô – 3 icon màu) · Mã hàng và quy cách thùng (ví dụ "SKU 2001 · 50 hũ/thùng") · Nơi giao hàng · Nhà cung cấp.
   **Lời:** "Sau đó, bộ phận xử lý chứng từ tạo dữ liệu gốc:" / "nhóm loại hàng, loại hàng đông, chill hay khô, mã hàng và quy cách thùng," / "nơi giao hàng và nhà cung cấp."
3. **Bước 3 – Khai báo quy tắc** [WMS] · 3 công tắc bật xanh: Quy tắc nhập hàng (bắt buộc date / batch) · Putaway theo khu · Tìm tồn (phân bổ).
   **Lời:** "Cuối cùng là khai báo quy tắc: nhập hàng bắt buộc date hoặc batch," / "putaway theo khu, và quy tắc tìm tồn để phân bổ."
4. **Ghi nhớ Chương 1:**
   - Quản lý tạo chủ hàng trên WMS
   - XLCT tạo dữ liệu gốc: loại hàng Đông / Chill / Khô, mã hàng, quy cách thùng
   - Khai báo quy tắc nhập, putaway theo khu, tìm tồn

### Chương 2 – Nhập hàng và Putaway bằng LPN (02F) (~80s)
1. **Bước 1 – Nhận ASN** [Thủ công] · XLCT nhận file kế hoạch nhập, sửa cột cho đúng mẫu WMS (cột lệch → cột thẳng ✔).
   **Lời:** "Khi có kế hoạch nhập, XLCT nhận file và xử lý cho đúng định dạng WMS."
2. **Bước 2 – Nhập vào WMS** [WMS] · Import file → ASN-0001 hiện ra. Máy in nhả tờ **Mã vạch LPN** (chứng từ bay ra góc phải), XLCT trao cho nhân viên kho.
   **Lời:** "Sau đó nhập file vào WMS để tạo ASN," / "rồi in sẵn mã vạch LPN, giao cho nhân viên kho."
3. **Bước 3 – Tạo phiếu nhập** [Quét PDA] · Xe 51C-123.45 lùi vào dock. PDA lớn bên phải: "Tạo phiếu nhập · Số xe: 51C-123.45 · Tài xế: …".
   **Lời:** "Xe hàng tới, nhân viên kho tạo phiếu nhập trên PDA, nhập số xe và tên tài xế."
4. **Bước 4 – Chuẩn bị pallet** [Thủ công] · Kéo pallet trống ra khu nhận, dán nhãn LPN-000102 (pop).
   **Lời:** "Nhân viên mang pallet tới khu nhận hàng và dán LPN lên pallet."
5. **Bước 5 – Chất hàng lên pallet** [Thủ công] · Xoay thùng kiểm ngoại quan (kính lúp ✔), xếp thùng lên pallet.
   **Lời:** "Kiểm tra ngoại quan từng thùng, rồi xếp hàng lên pallet."
6. **Bước 6 – Nhận hàng** [Quét PDA] · PDA lần lượt: Scan LPN → Scan mã hàng (SKU 2001) → Nhập số lượng (40 thùng) → Nhập date / batch (HSD 20/05/2027 · B2405).
   **Lời:** "Trên PDA: quét LPN, quét mã hàng," / "nhập số lượng, và nhập date hoặc batch."
7. **Bước 7 – Putaway** [Quét PDA] · Quét LPN → PDA hiện "Vị trí gợi ý: CHILL-A01-02".
   **Lời:** "Để cất hàng, quét lại LPN. Hệ thống gợi ý vị trí theo khu."
8. **Bước 8 – Di chuyển pallet** [Thủ công] · Mũi tên tự vẽ từ dock vào khu CHILL, pallet được đưa tới kệ A01-02.
   **Lời:** "Nhân viên mang pallet tới đúng vị trí."
9. **Bước 9 – Xác nhận vị trí** [Quét PDA] · Quét mã vị trí → dấu ✔ xanh "Đã cất".
   **Lời:** "Quét mã vạch vị trí để xác nhận."
10. **Còn pallet chưa nhận?** · Hình thoi; nhánh "Có" là mũi tên vòng về Bước 4, tua nhanh 2 pallet còn lại (LPN-000101 vào khu ĐÔNG, LPN-000103 vào khu KHÔ). Nhánh "Không" đi tiếp.
    **Lời:** "Còn pallet chưa nhận thì lặp lại từ bước chuẩn bị pallet."
11. **Bước 10 – Hoàn tất nhận hàng** [Quét PDA] · Thanh tiến độ ASN 3/3 pallet ✔.
    **Lời:** "Nhận đủ pallet thì xác nhận hoàn tất nhận hàng."
12. **Bước 11 – In và ký** [WMS] · XLCT in **Phiếu nhập kho** (chứng từ bay ra), 3 chữ ký lần lượt hiện lên.
    **Lời:** "Cuối cùng, XLCT in phiếu nhập kho và chuyển các bên ký."
13. **Ghi nhớ Chương 2:**
    - LPN được in sẵn, mỗi pallet dán 1 LPN
    - Nhận hàng: quét LPN → quét mã hàng → nhập số lượng → nhập date / batch
    - Putaway: quét LPN → đi tới vị trí gợi ý → quét vị trí xác nhận

### Chương 3 – Lấy hàng gộp theo xe bằng giấy (04K.1) (~70s)
1. **Bước 1 – Nhận kế hoạch xuất** [Thủ công] · File kế hoạch xuất (DO), XLCT sửa cho đúng định dạng.
   **Lời:** "Với hàng xuất, XLCT nhận file kế hoạch xuất DO và xử lý cho đúng định dạng WMS."
2. **Bước 2 – Nhập vào WMS** [WMS] · Import → 3 thẻ DO-1001, DO-1002, DO-1003 hiện ra.
   **Lời:** "Import file vào WMS để tạo các DO."
3. **Bước 3 – Tạo lệnh xuất gộp** [WMS] · 3 thẻ DO trượt vào chung một khung có icon xe XE-01 → khung đổi tên **MDO-0001**. Nhãn lớn "1 xe = 1 Master DO".
   **Lời:** "Các DO giao cùng một xe được gom lại thành một lệnh xuất gộp." / "Một xe là một Master DO."
4. **Bước 4 – Phân bổ tồn kho** [WMS] · Bấm "Phân bổ", mũi tên từ MDO chạy tới các vị trí trong 3 khu; nhãn "FIFO · FEFO".
   **Lời:** "Hệ thống chạy phân bổ để tìm tồn, theo FIFO hoặc FEFO."
5. **Bước 5 – In Picklist** [WMS] · 4 ý hiện lần lượt:
   - Chọn 1 hoặc nhiều Master DO lấy cùng lúc
   - Gộp tổng theo mã hàng: SKU 2001 → 20 + 30 + 5 = 55 hũ
   - Hiện thùng + pcs: "55 hũ = **1 thùng 5 hũ**" (quy cách 50)
   - Tách theo khu: máy in nhả **3 tờ Picklist** viền xanh băng / xanh ngọc / be (chứng từ "Picklist giấy (theo khu)")
   **Lời:** "Khi in Picklist, có thể chọn một hoặc nhiều Master DO để lấy cùng lúc." / "Số lượng được gộp tổng theo mã hàng," / "và hiện theo thùng cộng lẻ: năm mươi lăm hũ, quy cách năm mươi, là một thùng năm hũ." / "Picklist được tách và in riêng cho từng khu: đông, chill và khô."
6. **Bước 6 – Lấy hàng bằng giấy** [Thủ công] · Nhân viên kho cầm tờ Picklist CHILL, đi tới vị trí, lấy 1 thùng + 5 hũ, dùng bút ghi "1 thùng 5" vào cột thực lấy.
   **Lời:** "Nhân viên kho cầm Picklist của khu mình, đến đúng vị trí," / "lấy đúng số thùng và số lẻ, rồi ghi số lượng thực lấy lên Picklist."
7. **Bước 7 – Đưa về khu chia** [Thủ công] · Đẩy hàng về khu chia, nộp Picklist cho XLCT.
   **Lời:** "Lấy xong, đưa hàng về khu chia và nộp Picklist cho XLCT."
8. **Bước 8 – Xác nhận lấy hàng** [WMS] · XLCT gõ số thực lấy từ tờ giấy vào WMS, dấu ✔.
   **Lời:** "XLCT nhập số lượng thực lấy vào WMS để xác nhận."
9. **Ghi nhớ Chương 3:**
   - 1 xe = 1 Master DO, có thể lấy nhiều Master DO cùng lúc
   - Picklist gộp theo mã hàng, hiện thùng + lẻ, tách theo khu Đông / Chill / Khô
   - Ghi số thực lấy lên giấy, XLCT nhập lại vào WMS

### Chương 4 – Chia hàng theo đơn DO (04K.2) (~50s)
1. **Bước 1 – Chuẩn bị khu chia** [Thủ công] · Khu chia có 3 ô sàn, nhân viên dán giấy ghi số DO-1001 / DO-1002 / DO-1003.
   **Lời:** "Tại khu chia, mỗi DO của xe có một ô riêng, ghi số DO lên từng ô."
2. **Bước 2 – Chia hàng** [Quét PDA] · PDA: chọn XE-01 / MDO-0001 → quét SKU 2001 → PDA hiện "DO-1002 · 30 hũ" → đặt vào ô DO-1002 → xác nhận ✔. Ô sáng lên theo từng lượt; đống hàng chung vơi dần.
   **Lời:** "Trên PDA, chọn xe hoặc Master DO, rồi quét mã vạch hàng." / "Hệ thống chỉ DO và số lượng cần đặt, theo thùng và số lẻ." / "Đặt hàng vào đúng ô DO rồi xác nhận."
3. **Đã chia hết hàng?** · Nhánh "Không" vòng về Bước 2. Nhánh "Có" đi tiếp.
   **Lời:** "Chưa chia hết thì quét tiếp."
4. **Có thiếu / thừa hàng?** · Nhánh "Không" → Kết thúc ✔. Nhánh "Có" → Quản lý kho.
   **Lời:** "Chia xong, kiểm tra có thiếu hay thừa hàng không."
5. **Bước 3 – Xử lý chênh lệch** [WMS] · Quản lý kho mở báo cáo thiếu / thừa trên WMS. Ví dụ hai cột:
   - Thiếu (đỏ): lấy bổ sung, hoặc điều chỉnh DO
   - Thừa (cam): trả hàng về vị trí
   **Lời:** "Nếu có chênh lệch, quản lý kho xem báo cáo thiếu thừa trên WMS." / "Thiếu thì lấy bổ sung hoặc điều chỉnh DO." / "Thừa thì trả hàng về vị trí."
6. **Ghi nhớ Chương 4:**
   - Mỗi DO một ô riêng, ghi số DO lên ô
   - Quét mã hàng → PDA chỉ DO và số lượng → đặt vào ô, xác nhận
   - Thiếu / thừa: quản lý kho xử lý theo báo cáo WMS

### Chương 5 – Kiểm hàng và Bàn giao (04K.3) (~50s)
1. **Bước 1 – Kiểm hàng** [Quét PDA] · Checker chọn XE-01 / MDO-0001, quét mã hàng từng DO, kiểm ngoại quan và số lượng (thùng + lẻ).
   **Lời:** "Checker chọn xe hoặc Master DO, quét mã hàng của từng DO," / "kiểm ngoại quan và số lượng theo thùng và số lẻ."
2. **Khớp với DO?** · Ví dụ DO-1002 quét được 29 / cần 30 → nhánh "Không".
   **Bước 2 – Xử lý sai lệch** [Thủ công] · Bổ sung 1 hũ vào ô DO-1002 → vòng lại Bước 1 → lần này khớp ✔.
   **Lời:** "Nếu không khớp với DO, chia lại hoặc bổ sung hàng, rồi kiểm lại."
3. **Bước 3 – In giấy bàn giao** [WMS] · Khớp hết → in **Giấy bàn giao**, 3 tờ, mỗi DO một tờ (chứng từ bay ra).
   **Lời:** "Khớp rồi thì in giấy bàn giao của xe, mỗi DO một giấy."
4. **Bước 4 – Nhận hàng và ký** [Thủ công] · Tài xế đưa hàng lên XE-01, ký 3 tờ bàn giao.
   **Lời:** "Tài xế nhận hàng lên xe và ký giấy bàn giao."
5. **Bước 5 – Hoàn tất** [WMS] · XLCT xác nhận hoàn tất MDO-0001 (dấu ✔ lớn), cất giấy bàn giao đã ký vào kẹp hồ sơ. Xe XE-01 chạy ra khỏi dock.
   **Lời:** "XLCT xác nhận hoàn tất Master DO và lưu lại giấy bàn giao đã ký."
6. **Ghi nhớ Chương 5:**
   - Kiểm từng DO: ngoại quan + số lượng thùng và lẻ
   - Không khớp → chia lại / bổ sung rồi kiểm lại
   - Mỗi DO một giấy bàn giao, tài xế ký, XLCT lưu

### Kết (~10s)
Dải tổng kết 5 chặng (giống mở đầu), từng chặng đóng dấu ✔. Giảng viên giơ ngón cái.
**Lời:** "Đó là toàn bộ quy trình kho CXAD, từ tạo chủ hàng đến bàn giao hàng lên xe." / "Chúc các bạn làm việc thật tốt!"

---

## Cần bạn xác nhận trước khi dựng
Mình đã điền sẵn lựa chọn đề xuất; bạn chỉ cần sửa những dòng không đúng.

1. **Một video liền ~4:30–5:00** chia 5 chương (như video kho khô), hay tách 5 video ngắn? → Đề xuất: 1 video liền.
2. **Chương 1 (Tạo chủ hàng)** là việc văn phòng, làm một lần: giữ ~30s hay rút còn ~10s? → Đề xuất: giữ ~30s.
3. **Màu nhân vật:** "Nhân viên kho" làm cả nhận hàng, lấy hàng, chia hàng → dùng **1 nhân vật áo vàng** xuyên suốt (thay vì tách receiver xanh lá / picker vàng như video cũ)? Quản lý và Quản lý kho là 2 nhân vật mới như bảng trên?
4. **Di chuyển pallet (02F bước 8):** dùng xe nâng tay (pallet jack) do nhân viên kho kéo, hay xe nâng có tài xế riêng? File gốc ghi nhân viên kho làm → Đề xuất: xe nâng tay.
5. **Bước 3 của 04K.3 (In giấy bàn giao)** nằm ở lane Checker: Checker tự in ở khu kiểm? → Đề xuất: đúng vậy, máy in ở khu kiểm hàng.
6. **Dữ liệu minh họa** (SKU 1001 / 2001 / 3001, xe 51C-123.45, MDO-0001, vị trí CHILL-A01-02…) có cần đổi sang mã / tên thật của CXAD không?
7. **Định dạng mã vị trí** của kho CXAD (ví dụ "CHILL-A01-02") – nếu có quy ước thật, gửi mình 1 ví dụ.
8. **Nhãn "WMS / Thủ công / Quét PDA"** ở góc mỗi bước theo đúng chú thích file gốc: giữ hay bỏ cho gọn?
