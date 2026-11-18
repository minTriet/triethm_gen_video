# CONTEXT VIDEO TRAINING – VẬN HÀNH HÀNG TC (TRUNG CHUYỂN) · v2 (đã xác nhận)

> Video riêng, độc lập với video "Vận hành kho khô". Giữ nguyên mọi quyết định đã chốt:
> không giọng đọc, chỉ phụ đề (lời thoại bên dưới = phụ đề nguyên văn), nhịp đọc 1.3×,
> hiệu ứng âm thanh thưa (≥ 4 s), nhân vật model v2, kiểu đi nghiêng-nhún, cùng nhà kho, màu, font.
> Mã hàng, mã cửa hàng, số lượng là **ví dụ minh họa**.
> Dự kiến **khoảng 2 phút – 2 phút 15 giây**.

---

## Ý chính người xem phải nhớ
Hàng TC **không lưu kho**: nhập vào **không dùng LPN**, nhập thẳng số lượng, đưa vào **khu TC**,
rồi **chia ngay cho các cửa hàng theo số lượng trên DO** – giống cross dock.

## Khác gì so với hàng kho khô thường

| | Hàng kho khô thường | Hàng TC |
| --- | --- | --- |
| Nhận hàng | Dán + scan **LPN** cho từng pallet | **Không LPN**, nhập thẳng số lượng |
| Sau khi nhận | Cất lên kệ (Primary / Reserved) | Đưa vào **khu TC**, không cất lên kệ |
| Xuất hàng | Allocate → (châm hàng) → pick từ pick face | **Chia** hàng vừa nhập vào vị trí TC của từng cửa hàng theo DO |
| Tồn kho | Có lưu kho | Không lưu kho – nhập bao nhiêu chia bấy nhiêu |

---

## Kịch bản (lời thoại = phụ đề)

### Mở đầu (~10s)
- **Hình:** tiêu đề "Vận hành hàng TC (Trung chuyển)". Giảng viên vẫy tay. Hai dải quy trình xếp chồng:
  - Hàng thường: Nhập hàng → Cất lên kệ → Lưu kho → Pick → Xuất
  - Hàng TC: Nhập hàng → Khu TC → Chia cho cửa hàng → Xuất (hai bước "Cất lên kệ, Lưu kho" bị gạch đi)
- **Lời:** "Hàng TC là hàng trung chuyển." / "Hàng nhập vào không lưu kho, mà được chia ngay cho các cửa hàng, giống như cross dock."

### Phần 1 – Nhận hàng TC (~40s)
1. **Xe về, dỡ hàng.** Xe tải lùi vào dock, nhân viên nhận hàng (áo xanh lá) dỡ thùng.
   Biểu tượng LPN bị gạch: "Không dùng LPN".
   **Lời:** "Khi xe hàng TC về kho, nhân viên dỡ hàng xuống." / "Hàng TC không dán LPN."
2. **Các bước trên PDA** (badge Bước 1–3, PDA lớn bên phải):
   - Bước 1 – Chọn phiếu ASN của xe hàng TC (ví dụ ASN-TC-0007, SKU 5001 · 100 thùng)
   - Bước 2 – Scan mã hàng (ví dụ SKU 5001 – Nước suối thùng 24 chai)
   - Bước 3 – Nhập thẳng số lượng nhận. **Không nhập batch / lot / ngày.**
   - Thử nhập 110 > 100 → PDA báo đỏ "Không nhận dư". Chỉ nhận **đủ** hoặc **thiếu**.
   **Lời:** "Trên PDA, nhân viên chọn phiếu ASN của xe hàng TC," / "scan mã hàng," / "và nhập thẳng số lượng nhận, không cần LPN, không nhập batch, lot hay ngày." / "Chỉ nhận đủ hoặc thiếu so với phiếu, không nhận dư."
3. **Đưa vào khu TC.** Hàng được kéo vào khu sàn có vạch kẻ, biển "KHU TC". Không xe nâng, không cất lên kệ.
   **Lời:** "Hàng nhận xong được mang vào khu TC trong kho, không cất lên kệ."
4. **Ghi nhớ Phần 1:**
   - Hàng TC không dùng LPN, không nhập batch / lot / ngày
   - Nhập thẳng số lượng – chỉ nhận đủ hoặc thiếu, không nhận dư
   - Để tại khu TC, không cất lên kệ

### Phần 2 – Xuất hàng TC: chia cho cửa hàng (~60s)
1. **DO của cửa hàng.** DO đã có sẵn, hàng về là chia ngay.
   Ví dụ SKU 5001: CH-0125 cần 30, CH-0311 cần 45, CH-0420 cần 25 → tổng 100 = đúng số đã nhận.
   **Lời:** "DO của các cửa hàng đã có sẵn số lượng cần." / "Hệ thống dùng chính hàng TC vừa nhập để chia cho từng cửa hàng."
2. **Khu TC có vị trí riêng cho từng cửa hàng.** Mỗi vị trí chỉ dán **mã cửa hàng** để scan khi chia, **không có mã vị trí**.
   **Lời:** "Trong khu TC, mỗi cửa hàng có một vị trí riêng, chỉ dán mã cửa hàng, không có mã vị trí."
3. **Chia hàng** (badge Bước 1–4, picker áo vàng):
   - Bước 1 – Scan mã hàng TC
   - Bước 2 – PDA hiện cửa hàng và số lượng cần chia (ví dụ "CH-0125 · Chia: 30 thùng")
   - Bước 3 – Đến vị trí của cửa hàng đó, scan mã cửa hàng
   - Bước 4 – Đặt đúng số lượng, xác nhận
   Hình: đống hàng nguồn giảm 100 → 70 → 25 → 0; vị trí mỗi cửa hàng sáng ✔ khi đủ.
   **Lời:** "Nhân viên scan mã hàng," / "PDA hiện cửa hàng và số lượng cần chia." / "Đến vị trí của cửa hàng đó, scan mã cửa hàng," / "đặt đúng số lượng rồi xác nhận." / "Lặp lại cho đến khi chia hết hàng."
4. **Khi nhận thiếu – phân bổ từ trên xuống.** Ví dụ chỉ nhận 75 thùng: CH-0125 đủ 30, CH-0311 đủ 45, CH-0420 không có hàng.
   **Lời:** "Nếu nhận thiếu, hàng được phân bổ từ trên xuống." / "Các cửa hàng phía trên nhận đủ, cửa hàng phía dưới có thể không có hàng."
5. **Bàn giao.** Nhân viên gom hàng của một cửa hàng từ 3 nguồn: trolley hàng chẵn + Oricon hàng lẻ + vị trí TC của cửa hàng → bàn giao cho vận tải.
   **Lời:** "Khi bàn giao, nhân viên gom hàng chẵn, hàng lẻ và hàng ở vị trí TC của từng cửa hàng," / "rồi bàn giao cho vận tải như bình thường."
6. **Ghi nhớ Phần 2:**
   - Chia theo DO: scan mã hàng → đến vị trí cửa hàng → scan mã cửa hàng → đặt hàng, xác nhận
   - Nhận thiếu: phân bổ từ trên xuống
   - Bàn giao: gom hàng chẵn + hàng lẻ + vị trí TC

### Kết (~8s)
Dải tổng kết: Nhận (không LPN) → Khu TC → Chia theo DO → Gom & Bàn giao. Giảng viên giơ ngón cái.
**Lời:** "Đó là toàn bộ quy trình hàng TC. Chúc các bạn làm việc thật tốt!"

---

## Đã xác nhận
1. Không nhập batch / lot / ngày.
2. Khu TC: mỗi cửa hàng một vị trí, chỉ có mã cửa hàng để scan khi chia, không có mã vị trí.
3. DO có sẵn trước khi hàng về.
4. Chia vào vị trí riêng của cửa hàng; khi bàn giao gom hàng chẵn + hàng lẻ + vị trí TC.
5. Không nhận dư; chỉ đủ hoặc thiếu; thiếu thì phân bổ từ trên xuống, một số cửa hàng có thể không có hàng.
6. Người chia: picker.
7. Kiểm hàng và bàn giao như hàng thường.
