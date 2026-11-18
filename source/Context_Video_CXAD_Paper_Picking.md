# CONTEXT VIDEO TRAINING – QUY TRÌNH TOÀN KHO CXAD (LẤY HÀNG BẰNG GIẤY) · v2 (đã xác nhận)

> Nguồn: `source/CXAD_Warehouse_Processes_Paper_Picking_VI.pdf`. Video dùng 4 quy trình: 02F, 04K.1, 04K.2, 04K.3
> (bỏ 01A – Tạo chủ hàng mới).
> Video riêng, độc lập với video "Vận hành kho khô" và video "Hàng TC". Giữ nguyên mọi quyết định đã chốt trước đây:
> không giọng đọc, chỉ phụ đề (lời thoại bên dưới = phụ đề nguyên văn), nhịp đọc 1.3×,
> hiệu ứng âm thanh thưa (≥ 4 s), nhân vật model v2, kiểu đi nghiêng-nhún, cùng màu, font Be Vietnam Pro.
> Mã hàng, mã xe, số DO, vị trí, số lượng là **ví dụ minh họa**.
> **1 video liền, khoảng 4 phút 15 giây – 4 phút 45 giây**, chia 4 chương, mỗi chương có thẻ chương và thẻ "Ghi nhớ".

---

## Ý chính người xem phải nhớ
Kho CXAD chạy theo một dòng liền mạch:
**Nhập hàng bằng LPN & cất hàng → Gộp đơn theo xe, lấy hàng bằng Picklist giấy theo khu
→ Chia hàng về từng DO → Kiểm hàng, bàn giao cho tài xế.**
Ba điểm khác với kho khô trước đây:
1. Kho có **3 khu nhiệt độ: Đông / Chill / Khô**, Picklist được **tách theo khu**.
2. Xuất hàng **gộp theo xe**: các DO đi cùng 1 xe gộp thành **1 Master DO**, lấy hàng tổng rồi mới **chia về từng DO**.
3. Lấy hàng **bằng giấy**: ghi số thực lấy lên Picklist, XLCT nhập lại vào WMS.

## Nhân vật

| Nhân vật | Làm các bước | Hình |
| --- | --- | --- |
| Xử lý chứng từ (XLCT) | 02F b1–2, b11 · 04K.1 b1–5, b8 · 04K.3 b5 | Áo xanh dương, ngồi bàn máy tính (= "Nhân viên điều phối" cũ) |
| Nhân viên nhận hàng | 02F b3–6, b10 | Áo xanh lá, PDA |
| Tài xế xe nâng | 02F b7–9 (putaway, di chuyển pallet bằng xe nâng) | Áo cam, xe nâng |
| Picker | 04K.1 b6–7 · 04K.2 b1–2 | Áo vàng, kẹp Picklist giấy / PDA, xe đẩy |
| Quản lý (kiêm quản lý kho) | 04K.2 b3 | Áo sơ mi trắng, cà vạt xanh đậm, mũ bảo hộ trắng |
| Checker | 04K.3 b1–3 | Áo tím, PDA, máy in ở khu kiểm hàng |
| Tài xế | 04K.3 b4 | Áo xám, cạnh xe tải |
| Giảng viên (mở / kết) | Mở đầu, Kết | Áo xanh dương, cà vạt cam (giữ như cũ) |

## Quy ước hình
- Mỗi bước có badge "Bước n" và 1 dòng chú thích (không thêm nhãn WMS / Thủ công / Quét PDA).
- Khi thao tác trên hệ thống: PDA lớn bên phải hoặc màn hình WMS, hiện đúng ô đang nhập.
- **Chứng từ** (Mã vạch LPN, Phiếu nhập kho, Picklist giấy, Giấy bàn giao) hiện thành tờ giấy bay ra góc phải khi được tạo.
- Điều kiện (hình thoi) → câu hỏi lớn có 2 nhánh "Có / Không".

## Sơ đồ kho dùng trong video (cần dựng mới)
Nhìn từ trên xuống, từ trái sang phải: **Dock nhận hàng → 3 khu kệ: ĐÔNG (xanh băng, có hơi lạnh) · CHILL (xanh ngọc) · KHÔ (be)
→ Khu chia (các ô sàn ghi số DO) → Khu kiểm hàng (có máy in) → Dock xuất, xe tải.** Văn phòng XLCT ở góc trên.

## Dữ liệu minh họa dùng xuyên suốt
- Mã hàng: **SKU 1001** Há cảo (Đông, 20 gói/thùng) · **SKU 2001** Sữa chua (Chill, 50 hũ/thùng) · **SKU 3001** Bánh quy (Khô, 24 hộp/thùng)
- Nhập: **ASN-0001**, xe **51C-123.45**, 3 pallet, **LPN-000101 → LPN-000103**; ví dụ LPN-000102: SKU 2001 · 40 thùng · HSD 20/05/2027 · Batch B2405; vị trí gợi ý **CHILL-A01-02**
- Xuất: xe **XE-01** chở 3 DO: **DO-1001, DO-1002, DO-1003** → gộp thành **MDO-0001**
- Ví dụ thùng + pcs (đúng ví dụ trong file gốc): SKU 2001 – DO-1001 cần 20, DO-1002 cần 30, DO-1003 cần 5 → **tổng 55 hũ = 1 thùng 5 hũ** (quy cách 50)

---

## Kịch bản (lời thoại = phụ đề)

### Mở đầu (~15s)
- **Hình:** tiêu đề "Quy trình vận hành kho CXAD – Lấy hàng bằng giấy". Giảng viên vẫy tay. Dải 4 chặng hiện lần lượt:
  Nhập hàng & Putaway → Lấy hàng gộp theo xe → Chia hàng theo DO → Kiểm & Bàn giao.
  Sau đó camera lướt qua sơ đồ kho, 3 khu Đông / Chill / Khô sáng lần lượt.
- **Lời:** "Xin chào các bạn. Video này đi qua toàn bộ quy trình của kho CXAD, từ lúc nhập hàng đến lúc giao hàng lên xe." / "Kho có ba khu theo nhiệt độ: khu đông, khu chill và khu khô."

### Chương 1 – Nhập hàng và Putaway bằng LPN (02F) (~80s)
1. **Bước 1 – Nhận ASN** · XLCT nhận file kế hoạch nhập, sửa cột cho đúng mẫu WMS (cột lệch → cột thẳng ✔).
   **Lời:** "Khi có kế hoạch nhập, XLCT nhận file và xử lý cho đúng định dạng WMS."
2. **Bước 2 – Nhập vào WMS** · Import file → ASN-0001 hiện ra. Máy in nhả tờ **Mã vạch LPN** (chứng từ bay ra góc phải), XLCT trao cho nhân viên nhận hàng.
   **Lời:** "Sau đó nhập file vào WMS để tạo ASN," / "rồi in sẵn mã vạch LPN, giao cho nhân viên kho."
3. **Bước 3 – Tạo phiếu nhập** · Xe 51C-123.45 lùi vào dock. Nhân viên nhận hàng (áo xanh lá) cầm PDA; PDA lớn bên phải: "Tạo phiếu nhập · Số xe: 51C-123.45 · Tài xế: …".
   **Lời:** "Xe hàng tới, nhân viên nhận hàng tạo phiếu nhập trên PDA, nhập số xe và tên tài xế."
4. **Bước 4 – Chuẩn bị pallet** · Kéo pallet trống ra khu nhận, dán nhãn LPN-000102 (pop).
   **Lời:** "Nhân viên mang pallet tới khu nhận hàng và dán LPN lên pallet."
5. **Bước 5 – Chất hàng lên pallet** · Xoay thùng kiểm ngoại quan (kính lúp ✔), xếp thùng lên pallet.
   **Lời:** "Kiểm tra ngoại quan từng thùng, rồi xếp hàng lên pallet."
6. **Bước 6 – Nhận hàng** · PDA lần lượt: Scan LPN → Scan mã hàng (SKU 2001) → Nhập số lượng (40 thùng) → Nhập date / batch (HSD 20/05/2027 · B2405).
   **Lời:** "Trên PDA: quét LPN, quét mã hàng," / "nhập số lượng, và nhập date hoặc batch."
7. **Bước 7 – Putaway** · Tài xế xe nâng (áo cam) quét LPN → PDA hiện "Vị trí gợi ý: CHILL-A01-02".
   **Lời:** "Để cất hàng, tài xế xe nâng quét LPN. Hệ thống gợi ý vị trí theo khu."
8. **Bước 8 – Di chuyển pallet** · Mũi tên tự vẽ từ dock vào khu CHILL, xe nâng chở pallet tới kệ A01-02 và nâng lên ô.
   **Lời:** "Xe nâng mang pallet tới đúng vị trí."
9. **Bước 9 – Xác nhận vị trí** · Quét mã vị trí → dấu ✔ xanh "Đã cất".
   **Lời:** "Quét mã vạch vị trí để xác nhận."
10. **Còn pallet chưa nhận?** · Hình thoi; nhánh "Có" là mũi tên vòng về Bước 4, tua nhanh 2 pallet còn lại (LPN-000101 vào khu ĐÔNG, LPN-000103 vào khu KHÔ). Nhánh "Không" đi tiếp.
    **Lời:** "Còn pallet chưa nhận thì lặp lại từ bước chuẩn bị pallet."
11. **Bước 10 – Hoàn tất nhận hàng** · Nhân viên nhận hàng xác nhận trên PDA; thanh tiến độ ASN 3/3 pallet ✔.
    **Lời:** "Nhận đủ pallet thì xác nhận hoàn tất nhận hàng."
12. **Bước 11 – In và ký** · XLCT in **Phiếu nhập kho** (chứng từ bay ra), 3 chữ ký lần lượt hiện lên.
    **Lời:** "Cuối cùng, XLCT in phiếu nhập kho và chuyển các bên ký."
13. **Ghi nhớ Chương 1:**
    - LPN được in sẵn, mỗi pallet dán 1 LPN
    - Nhận hàng: quét LPN → quét mã hàng → nhập số lượng → nhập date / batch
    - Putaway: quét LPN → xe nâng đưa tới vị trí gợi ý → quét vị trí xác nhận

### Chương 2 – Lấy hàng gộp theo xe bằng giấy (04K.1) (~70s)
1. **Bước 1 – Nhận kế hoạch xuất** · File kế hoạch xuất (DO), XLCT sửa cho đúng định dạng.
   **Lời:** "Với hàng xuất, XLCT nhận file kế hoạch xuất DO và xử lý cho đúng định dạng WMS."
2. **Bước 2 – Nhập vào WMS** · Import → 3 thẻ DO-1001, DO-1002, DO-1003 hiện ra.
   **Lời:** "Import file vào WMS để tạo các DO."
3. **Bước 3 – Tạo lệnh xuất gộp** · 3 thẻ DO trượt vào chung một khung có icon xe XE-01 → khung đổi tên **MDO-0001**. Nhãn lớn "1 xe = 1 Master DO".
   **Lời:** "Các DO giao cùng một xe được gom lại thành một lệnh xuất gộp." / "Một xe là một Master DO."
4. **Bước 4 – Phân bổ tồn kho** · Bấm "Phân bổ", mũi tên từ MDO chạy tới các vị trí trong 3 khu; nhãn "FIFO · FEFO".
   **Lời:** "Hệ thống chạy phân bổ để tìm tồn, theo FIFO hoặc FEFO."
5. **Bước 5 – In Picklist** · 4 ý hiện lần lượt:
   - Chọn 1 hoặc nhiều Master DO lấy cùng lúc
   - Gộp tổng theo mã hàng: SKU 2001 → 20 + 30 + 5 = 55 hũ
   - Hiện thùng + pcs: "55 hũ = **1 thùng 5 hũ**" (quy cách 50)
   - Tách theo khu: máy in nhả **3 tờ Picklist** viền xanh băng / xanh ngọc / be (chứng từ "Picklist giấy (theo khu)")
   **Lời:** "Khi in Picklist, có thể chọn một hoặc nhiều Master DO để lấy cùng lúc." / "Số lượng được gộp tổng theo mã hàng," / "và hiện theo thùng cộng lẻ: năm mươi lăm hũ, quy cách năm mươi, là một thùng năm hũ." / "Picklist được tách và in riêng cho từng khu: đông, chill và khô."
6. **Bước 6 – Lấy hàng bằng giấy** · Picker (áo vàng) cầm tờ Picklist CHILL, đi tới vị trí, lấy 1 thùng + 5 hũ, dùng bút ghi "1 thùng 5" vào cột thực lấy.
   **Lời:** "Picker cầm Picklist của khu mình, đến đúng vị trí," / "lấy đúng số thùng và số lẻ, rồi ghi số lượng thực lấy lên Picklist."
7. **Bước 7 – Đưa về khu chia** · Đẩy hàng về khu chia, nộp Picklist cho XLCT.
   **Lời:** "Lấy xong, đưa hàng về khu chia và nộp Picklist cho XLCT."
8. **Bước 8 – Xác nhận lấy hàng** · XLCT gõ số thực lấy từ tờ giấy vào WMS, dấu ✔.
   **Lời:** "XLCT nhập số lượng thực lấy vào WMS để xác nhận."
9. **Ghi nhớ Chương 2:**
   - 1 xe = 1 Master DO, có thể lấy nhiều Master DO cùng lúc
   - Picklist gộp theo mã hàng, hiện thùng + lẻ, tách theo khu Đông / Chill / Khô
   - Ghi số thực lấy lên giấy, XLCT nhập lại vào WMS

### Chương 3 – Chia hàng theo đơn DO (04K.2) (~50s)
1. **Bước 1 – Chuẩn bị khu chia** · Khu chia có 3 ô sàn, picker dán giấy ghi số DO-1001 / DO-1002 / DO-1003.
   **Lời:** "Tại khu chia, mỗi DO của xe có một ô riêng, ghi số DO lên từng ô."
2. **Bước 2 – Chia hàng** · PDA: chọn XE-01 / MDO-0001 → quét SKU 2001 → PDA hiện "DO-1002 · 30 hũ" → đặt vào ô DO-1002 → xác nhận ✔. Ô sáng lên theo từng lượt; đống hàng chung vơi dần.
   **Lời:** "Trên PDA, chọn xe hoặc Master DO, rồi quét mã vạch hàng." / "Hệ thống chỉ DO và số lượng cần đặt, theo thùng và số lẻ." / "Đặt hàng vào đúng ô DO rồi xác nhận."
3. **Đã chia hết hàng?** · Nhánh "Không" vòng về Bước 2. Nhánh "Có" đi tiếp.
   **Lời:** "Chưa chia hết thì quét tiếp."
4. **Có thiếu / thừa hàng?** · Nhánh "Không" → Kết thúc ✔. Nhánh "Có" → Quản lý.
   **Lời:** "Chia xong, kiểm tra có thiếu hay thừa hàng không."
5. **Bước 3 – Xử lý chênh lệch** · Quản lý kho xử lý **thủ công hoàn toàn** tại khu chia, **không có báo cáo trên WMS**. Ví dụ hai trường hợp:
   - Thiếu (đỏ): lấy bổ sung, hoặc điều chỉnh DO
   - Thừa (cam): trả hàng về vị trí
   **Lời:** "Nếu có chênh lệch, quản lý kho xử lý thủ công, không có báo cáo trên WMS." / "Thiếu thì lấy bổ sung hoặc điều chỉnh DO." / "Thừa thì trả hàng về vị trí."
6. **Ghi nhớ Chương 3:**
   - Mỗi DO một ô riêng, ghi số DO lên ô
   - Quét mã hàng → PDA chỉ DO và số lượng → đặt vào ô, xác nhận
   - Thiếu / thừa: quản lý kho xử lý thủ công (không có báo cáo WMS)

### Chương 4 – Kiểm hàng và Bàn giao (04K.3) (~50s)
1. **Bước 1 – Kiểm hàng** · Checker chọn XE-01 / MDO-0001, quét mã hàng từng DO, kiểm ngoại quan và số lượng (thùng + lẻ).
   **Lời:** "Checker chọn xe hoặc Master DO, quét mã hàng của từng DO," / "kiểm ngoại quan và số lượng theo thùng và số lẻ."
2. **Khớp với DO?** · Ví dụ DO-1002 quét được 29 / cần 30 → nhánh "Không".
   **Bước 2 – Xử lý sai lệch** · Bổ sung 1 hũ vào ô DO-1002 → vòng lại Bước 1 → lần này khớp ✔.
   **Lời:** "Nếu không khớp với DO, chia lại hoặc bổ sung hàng, rồi kiểm lại."
3. **Bước 3 – In giấy bàn giao** · Khớp hết → Checker in **Giấy bàn giao** ở máy in khu kiểm hàng, 3 tờ, mỗi DO một tờ (chứng từ bay ra).
   **Lời:** "Khớp rồi thì checker in giấy bàn giao của xe, mỗi DO một giấy."
4. **Bước 4 – Nhận hàng và ký** · Tài xế đưa hàng lên XE-01, ký 3 tờ bàn giao.
   **Lời:** "Tài xế nhận hàng lên xe và ký giấy bàn giao."
5. **Bước 5 – Hoàn tất** · XLCT xác nhận hoàn tất MDO-0001 (dấu ✔ lớn), cất giấy bàn giao đã ký vào kẹp hồ sơ. Xe XE-01 chạy ra khỏi dock.
   **Lời:** "XLCT xác nhận hoàn tất Master DO và lưu lại giấy bàn giao đã ký."
6. **Ghi nhớ Chương 4:**
   - Kiểm từng DO: ngoại quan + số lượng thùng và lẻ
   - Không khớp → chia lại / bổ sung rồi kiểm lại
   - Mỗi DO một giấy bàn giao, tài xế ký, XLCT lưu

### Kết (~10s)
Dải tổng kết 4 chặng (giống mở đầu), từng chặng đóng dấu ✔. Giảng viên giơ ngón cái.
**Lời:** "Đó là toàn bộ quy trình kho CXAD, từ nhập hàng đến bàn giao hàng lên xe." / "Chúc các bạn làm việc thật tốt!"

---

## Đã xác nhận
1. 1 video liền.
2. Bỏ quy trình 01A – Tạo chủ hàng mới.
3. Tách nhân vật: nhân viên nhận hàng (xanh lá), tài xế xe nâng (cam), picker (vàng). Quản lý và quản lý kho là 1 nhân vật.
4. Di chuyển pallet khi putaway bằng xe nâng.
5. Checker in giấy bàn giao tại khu kiểm hàng.
6. Giữ dữ liệu minh họa (không đổi sang mã thật).
7. Giữ mã vị trí minh họa dạng "CHILL-A01-02".
8. Bỏ nhãn WMS / Thủ công / Quét PDA ở mỗi bước.
9. Xử lý chênh lệch khi chia hàng (04K.2 Bước 3) làm thủ công hoàn toàn, không có báo cáo trên WMS.
