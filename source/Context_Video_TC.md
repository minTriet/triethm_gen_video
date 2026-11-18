# CONTEXT VIDEO TRAINING – VẬN HÀNH HÀNG TC (TRUNG CHUYỂN) · bản nháp v1 để duyệt

> Video riêng, độc lập với video "Vận hành kho khô". Giữ nguyên mọi quyết định đã chốt:
> không giọng đọc, chỉ phụ đề (lời thoại bên dưới = phụ đề nguyên văn), nhịp đọc 1.3×,
> hiệu ứng âm thanh thưa (≥ 4 s), nhân vật model v2, kiểu đi nghiêng-nhún, cùng nhà kho, màu, font.
> Mã hàng, mã cửa hàng, số lượng là **ví dụ minh họa**.
> Dự kiến **khoảng 1 phút 45 giây – 2 phút**.

---

## Ý chính người xem phải nhớ
Hàng TC **không lưu kho**: nhập vào **không dùng LPN**, nhập thẳng số lượng, đưa vào **khu TC**,
rồi **chia ngay cho các cửa hàng theo số lượng trên DO** – giống cross dock.

## Khác gì so với hàng kho khô thường

| | Hàng kho khô thường | Hàng TC |
| --- | --- | --- |
| Nhận hàng | Dán + scan **LPN** cho từng pallet | **Không LPN**, nhập thẳng số lượng |
| Sau khi nhận | Cất lên kệ (Primary / Reserved) | Đưa vào **khu TC**, không cất lên kệ |
| Xuất hàng | Allocate → (châm hàng) → pick từ pick face | **Chia** hàng vừa nhập cho từng cửa hàng theo DO |
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
   - Bước 1 – Chọn phiếu ASN của xe hàng TC (ví dụ ASN-TC-0007)
   - Bước 2 – Scan mã hàng (ví dụ SKU 5001 – Nước suối thùng 24 chai)
   - Bước 3 – Nhập thẳng số lượng nhận (ví dụ 100 thùng)
   **Lời:** "Trên PDA, nhân viên chọn phiếu ASN của xe hàng TC," / "scan mã hàng," / "và nhập thẳng số lượng nhận, không cần LPN."
3. **Đưa vào khu TC.** Hàng được kéo vào một khu sàn có vạch kẻ, biển "KHU TC". Không có xe nâng, không cất lên kệ.
   **Lời:** "Hàng nhận xong được mang vào khu TC trong kho, không cất lên kệ."
4. **Ghi nhớ Phần 1:**
   - Hàng TC không dùng LPN
   - Nhập thẳng số lượng nhận
   - Để tại khu TC, không cất lên kệ

### Phần 2 – Xuất hàng TC: chia cho cửa hàng (~50s)
1. **DO của cửa hàng.** Các cửa hàng gửi DO có số lượng yêu cầu.
   Ví dụ SKU 5001: CH-0125 cần 30, CH-0311 cần 45, CH-0420 cần 25 → **tổng 100 = đúng số đã nhận**.
   **Lời:** "Các cửa hàng gửi DO với số lượng cần." / "Hệ thống dùng chính hàng TC vừa nhập để chia cho từng cửa hàng."
2. **Chia hàng** (badge Bước 1–3, picker áo vàng, 3 xe trolley dán mã cửa hàng xếp hàng ngang):
   - Bước 1 – Scan mã hàng TC tại khu TC
   - Bước 2 – PDA hiện cửa hàng và số lượng cần chia (ví dụ "CH-0125 · Chia: 30 thùng")
   - Bước 3 – Đặt đúng số lượng lên trolley của cửa hàng đó, rồi xác nhận
   Hình: đống 100 thùng ở khu TC giảm dần 100 → 70 → 25 → 0; mỗi trolley sáng ✔ khi đủ.
   **Lời:** "Nhân viên scan mã hàng tại khu TC," / "PDA hiện cửa hàng và số lượng cần chia," / "đặt đúng số lượng lên trolley của cửa hàng đó, rồi xác nhận." / "Lặp lại cho đến khi chia hết hàng."
3. **Khu TC trống.** Đống hàng về 0, trên PDA: "Đã chia hết · Tồn TC: 0".
   **Lời:** "Hàng TC nhập bao nhiêu thì chia hết bấy nhiêu, không để lại tồn kho."
4. **Sau khi chia** (một cảnh ngắn): trolley đi tiếp tới bước kiểm hàng và bàn giao vận tải, giống hàng thường.
   **Lời:** "Sau đó, hàng được kiểm và bàn giao cho vận tải như hàng thông thường."
5. **Ghi nhớ Phần 2:**
   - Chia hàng theo số lượng trên DO của từng cửa hàng
   - Scan mã hàng → xem cửa hàng + số lượng → đặt lên trolley → xác nhận
   - Chia hết, không lưu kho

### Kết (~8s)
Dải tổng kết: Nhận (không LPN) → Khu TC → Chia theo DO → Kiểm hàng → Bàn giao. Giảng viên giơ ngón cái.
**Lời:** "Đó là toàn bộ quy trình hàng TC. Chúc các bạn làm việc thật tốt!"

---

## Cần bạn xác nhận (mình đang giả định – sai thì sửa giúp)
1. **Batch / Lot / Ngày** khi nhận hàng TC: có phải nhập theo yêu cầu từng mã như hàng thường không? *(bản nháp: không nhắc tới)*
2. **Khu TC**: hàng để trên sàn ở một khu riêng, đúng không? Có scan vị trí khu TC không? *(bản nháp: không scan vị trí)*
3. **DO có trước hay sau khi nhận?** *(bản nháp: DO đã có sẵn, hàng về là chia ngay)*
4. **Chia vào đâu**: trolley theo mã cửa hàng như pick chẵn thùng? Có chia hàng lẻ vào Oricon không? *(bản nháp: chỉ trolley, chẵn thùng)*
5. **Nhận thiếu / dư so với tổng DO** thì xử lý thế nào? *(bản nháp: ví dụ khớp đúng 100 = 100, không nói trường hợp lệch)*
6. **Ai chia hàng**: picker (áo vàng) hay vai khác? *(bản nháp: picker)*
7. **Sau khi chia**: kiểm hàng + bàn giao giống hệt hàng thường? *(bản nháp: nhắc 1 câu, không dựng lại chi tiết)*
