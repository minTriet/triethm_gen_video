# PROMPT VIDEO TRAINING – QUY TRÌNH TOÀN KHO CXAD · v2 (đã xác nhận)

> Nguồn: `source/CXAD_-_Bo_quy_trinh_kho.drawio.pdf`. Video dùng 4 quy trình: 02F, 04K.1, 04K.2, 04K.3
> (**bỏ 01A – Thiết lập chủ hàng**, vì đó là việc của quản lý, nhân viên kho không làm).
> Video riêng, độc lập với video "Vận hành kho khô" và video TC. **Một video liền**, có thẻ chương giữa các phần.
> **Giữ phong cách đã chốt:** không giọng đọc, chỉ phụ đề (lời bên dưới = phụ đề nguyên văn), nhịp đọc 1.3×,
> hiệu ứng âm thanh thưa (≥ 4 s), nhân vật người que model v2, kiểu đi nghiêng-nhún, cùng màu và font, 1920×1080, 30 fps.
> Mã ASN, DO, mã hàng, biển số xe, vị trí, số lượng là **ví dụ minh họa** (giữ nguyên như bên dưới).
> Thời lượng dự kiến: **khoảng 5 phút 30 giây – 6 phút**.

---

## 1. Ý chính người xem phải nhớ

1. Hàng CXAD đi qua **4 quy trình nối nhau**: Nhập & Putaway (02F) → Lấy hàng gộp theo xe (04K.1) → Chia hàng theo DO (04K.2) → Kiểm & Bàn giao (04K.3).
2. **Nhập hàng:** mỗi pallet một **LPN ID**. Nhận xong pallet nào thì **putaway ngay** pallet đó rồi mới nhận pallet tiếp theo.
3. **Xuất hàng:** gom DO theo xe (**1 xe = 1 Master DO**), **lấy gộp** tổng số lượng theo mã hàng, rồi **chia lại** vào ô của từng DO.
4. Kho có **3 khu: đông / chill / khô**. Hàng **đông lấy bằng phiếu giấy**, hàng **chill / khô lấy bằng PDA**. Hàng cả ba khu về **chung một khu chia**.
5. Số lượng luôn tính **thùng + pcs** (ví dụ 55 pcs, quy cách 50 = **1 thùng 5 pcs**).
6. Bàn giao: checker kiểm khớp DO, in **giấy bàn giao theo từng DO**, **tài xế xe tải ký nhận**.

## 2. Khác gì so với video kho khô đã làm

| | Video kho khô (đã làm) | Quy trình CXAD (video này) |
| --- | --- | --- |
| Kho | Kệ Primary / Reserved, 1 vị trí pick = 1 mã cố định | 3 khu nhiệt độ: **đông / chill / khô** |
| Putaway | Theo vị trí primary cố định của mã | **Hệ thống gợi ý vị trí** theo quy tắc putaway từng khu |
| Gom đơn | Gom DO theo tuyến 1…n | Gom DO giao cùng xe thành **Master DO** |
| Phân bổ | Allocate chỉ lấy Primary, thiếu thì châm hàng | **Phân bổ tồn theo FIFO / FEFO**, không có châm hàng |
| Lấy hàng | Pick từng đơn: trolley (chẵn) + Oricon (lẻ) | **Lấy gộp** nhiều Master DO, rồi **chia theo DO** |
| Kiểm & giao | Vận tải chỉ xác nhận trên hệ thống, không đếm lại | Checker kiểm, **in giấy bàn giao từng DO**, **tài xế ký** |

→ Video này **không dùng lại** các khái niệm Primary/Reserved, châm hàng, trolley/Oricon.

## 3. Quy ước hình ảnh lấy từ chú giải của bản vẽ

Mỗi bước có một chip nhỏ cạnh badge "Bước n", đúng màu của bản vẽ, để người xem biết bước đó làm ở đâu:

| Chip | Ý nghĩa | Hình |
| --- | --- | --- |
| `WMS` (viền xanh, nền trắng) | Thao tác trên WMS (máy tính) | Màn hình máy tính phóng to, trỏ chuột bấm |
| `PDA` (biểu tượng máy quét) | Quét barcode / QR | PDA phóng to, tia laser đỏ + vòng "bíp" |
| `Thủ công` (nền cam) | Thao tác bằng tay | Nhân vật làm động tác thật (lái xe nâng, chất hàng, ghi phiếu) |
| `Chứng từ` (tờ giấy lượn sóng) | Giấy tờ được in ra | Tờ giấy bay ra từ máy in, có tiêu đề |
| Ô thoi `Điều kiện` | Ngã rẽ Có / Không | Thẻ câu hỏi hình thoi, hai mũi tên rẽ nhánh tự vẽ ra |

**Nhân vật – tách nhiều vai** (bản vẽ gộp chung làn "Nhân viên kho"; video tách theo việc để dễ nhìn):

| Vai | Hình | Làm các bước |
| --- | --- | --- |
| Nhân viên XLCT (xử lý chứng từ) | Sơ mi xanh dương, ngồi máy tính (dùng lại nhân vật "điều phối") | 02F: 1, 2, 11 · 04K.1: 1–5, 7 · 04K.3: 5 |
| Nhân viên nhận hàng | Áo + mũ xanh lá | 02F: 3, 4, 5, 6, 10 |
| Tài xế xe nâng | Áo + mũ cam, **xe nâng ngồi lái** | 02F: 7, 8, 9 (putaway) |
| Picker | Áo + mũ vàng | 04K.1: 6, 8, 9 (lấy hàng, đưa về khu chia) · 04K.2: 1, 2 (chia hàng) |
| Quản lý kho | **Model mới** `design/model-quan-ly.png`: sơ mi trắng, cà vạt + thẻ đeo xanh đậm, cầm bìa hồ sơ | 04K.2: 3 (xử lý chênh lệch) |
| Checker | Áo + mũ tím | 04K.3: 1, 2, 3 |
| Tài xế xe tải | Áo + mũ xám, đứng cạnh xe tải (dùng lại nhân vật "vận tải") | 04K.3: 4 (nhận hàng, ký) |
| Giảng viên | Như các video trước | Mở đầu và kết |

Nhãn tên trên đầu hiện ở lần xuất hiện đầu tiên của mỗi vai.

---

## 4. Kịch bản (lời = phụ đề)

### Mở đầu (~18s)
- **Hình:** tiêu đề "Quy trình vận hành kho – Chủ hàng CXAD". Giảng viên vẫy tay.
  Dải 4 ô hiện lần lượt, nối bằng mũi tên tự vẽ: **Nhập & Putaway → Lấy hàng gộp theo xe → Chia hàng theo DO → Kiểm & Bàn giao**. Mỗi ô có mã nhỏ bên dưới (02F, 04K.1, 04K.2, 04K.3).
  Sau đó lướt camera qua nhà kho có 3 khu được tô màu: **ĐÔNG** (xanh băng), **CHILL** (xanh ngọc), **KHÔ** (be), và một khu sàn trống có biển **KHU CHIA HÀNG** gần dock.
- **Lời:** "Xin chào các bạn." / "Video này đi qua toàn bộ quy trình kho của chủ hàng CXAD, từ lúc nhập hàng đến khi giao hàng lên xe." / "Kho có ba khu: hàng đông, hàng chill và hàng khô."

### Phần 1 – Nhập hàng & Putaway (LPN) · 02F (~100s)
Thẻ chương: "Phần 1 · Nhập hàng & Putaway". Chứng từ: **Nhãn LPN ID**, **Phiếu nhập kho**.
1. **Bước 1 – Nhận ASN** `Thủ công`. Hộp thư email hiện thư mới có đính kèm "Ke_hoach_nhap.xlsx", file bay vào máy XLCT, các cột được sửa cho đúng mẫu WMS (cột nhảy về đúng chỗ, ✔).
   **Lời:** "Khi có kế hoạch nhập, nhân viên XLCT nhận file qua email và chỉnh đúng định dạng của WMS."
2. **Bước 2 – Import vào WMS** `WMS`. Thanh tải lên chạy 100% → phiếu "ASN-CXAD-0001" hiện ra. Máy in nhả ra xấp **nhãn LPN ID** (chứng từ), XLCT đưa xấp nhãn cho nhân viên nhận hàng.
   **Lời:** "XLCT import file để tạo ASN," / "in sẵn nhãn LPN ID và giao cho kho."
3. **Bước 3 – Tạo phiếu nhập** `PDA`. Xe tải lùi vào dock. Nhân viên nhận hàng tạo phiếu nhập theo ASN, PDA hiện ô "Số xe: 51C-123.45", "Tài xế: Nguyễn Văn A".
   **Lời:** "Xe về, nhân viên nhận hàng tạo phiếu nhập theo ASN, nhập số xe và tên tài xế."
4. **Bước 4 – Chuẩn bị pallet** `Thủ công`. Nhân viên kéo pallet trống tới khu nhận hàng, dán nhãn LPN lên pallet (nhãn bật lên, phóng to thấy barcode "LPN ID").
   **Lời:** "Nhân viên mang pallet tới khu nhận hàng và dán nhãn LPN ID lên pallet."
5. **Bước 5 – Chất hàng lên pallet** `Thủ công`. Kính lúp lướt qua thùng hàng (kiểm ngoại quan, ✔), rồi chất thùng lên pallet.
   **Lời:** "Kiểm tra ngoại quan hàng, rồi chất hàng lên pallet."
6. **Bước 6 – Nhận hàng** `PDA`. Bốn ô trên PDA được điền lần lượt: Scan LPN ID → Scan mã hàng → Nhập số lượng → Nhập date / batch.
   **Lời:** "Trên PDA: scan LPN ID, scan mã hàng, nhập số lượng, và nhập date hoặc batch theo quy tắc của mã hàng đó."
7. **Bước 7 – Putaway** `PDA`. Tài xế xe nâng (áo cam) lái **xe nâng ngồi lái** tới, xúc pallet, scan lại LPN → PDA hiện "Vị trí gợi ý: K-03-02 (Khu khô)".
   **Lời:** "Nhận xong, tài xế xe nâng scan lại LPN của pallet đó." / "Hệ thống gợi ý vị trí putaway theo khu của hàng."
8. **Bước 8 – Di chuyển pallet** `Thủ công`. Mũi tên chấm tự vẽ từ dock tới vị trí K-03-02 trong khu khô, xe nâng chạy theo mũi tên, nâng pallet lên đúng ô kệ.
   **Lời:** "Xe nâng đưa pallet tới đúng vị trí được gợi ý."
9. **Bước 9 – Xác nhận vị trí** `PDA`. Scan mã vị trí → dấu ✔ xanh "Đã putaway".
   **Lời:** "Scan mã vị trí để xác nhận hoàn tất putaway pallet."
10. **Ngã rẽ "Còn pallet chưa nhận?"** Thẻ thoi. Nhánh **Có**: mũi tên vòng nét đứt quay về Bước 4, hiện nhanh 2 pallet nữa (tua nhanh ×3). Nhánh **Không**: đi tiếp.
    **Lời:** "Còn pallet thì quay lại bước chuẩn bị pallet." / "Mỗi pallet: nhận xong là putaway ngay."
11. **Bước 10 – Hoàn tất nhận hàng** `PDA`. Nhân viên nhận hàng bấm "Hoàn tất phiếu nhập" → ✔.
    **Lời:** "Hết pallet, nhân viên nhận hàng xác nhận hoàn tất phiếu nhập."
12. **Bước 11 – In và ký** `WMS`. XLCT in **Phiếu nhập kho** (chứng từ), ba chữ ký hiện lên phiếu.
    **Lời:** "XLCT in phiếu nhập kho và chuyển các bên ký xác nhận."
13. **Ghi nhớ Phần 1:**
    - Mỗi pallet = 1 LPN ID, in sẵn từ văn phòng
    - Nhận xong pallet nào, putaway ngay pallet đó
    - Putaway: scan LPN → đến vị trí gợi ý → scan vị trí

### Phần 2 – Lấy hàng gộp theo xe (Master DO) · 04K.1 (~110s)
Thẻ chương: "Phần 2 · Lấy hàng gộp theo xe". Chứng từ: **Phiếu lấy hàng đông (giấy)**.
1. **Bước 1 – Nhận kế hoạch xuất** `Thủ công`. Email mới có đính kèm file đơn hàng DO, file bay vào máy XLCT, chỉnh đúng mẫu WMS.
   **Lời:** "Với hàng xuất, XLCT nhận file đơn hàng DO qua email và chỉnh đúng định dạng của WMS."
2. **Bước 2 – Import vào WMS** `WMS`. Từng thẻ DO bật ra: DO-1001, DO-1002, DO-1003, DO-1004, DO-1005.
   **Lời:** "Import file để tạo các DO."
3. **Bước 3 – Tạo Master DO** `WMS`. Các thẻ DO được kéo vào hai xe tải: Xe 1 ← DO-1001, 1002, 1003; Xe 2 ← DO-1004, 1005. Mỗi xe hiện nhãn "Master DO".
   **Lời:** "XLCT gom các DO giao cùng một xe thành một Master DO." / "Một xe là một Master DO."
4. **Bước 4 – Phân bổ tồn** `WMS`. Bấm "Phân bổ" → các mũi tên chạy tới lô hàng có ngày cũ / hạn gần trước, nhãn "FIFO / FEFO".
   **Lời:** "Bấm phân bổ tồn, hệ thống tự chọn hàng theo FIFO hoặc FEFO."
5. **Bước 5 – Tạo phiếu lấy hàng** `WMS`, chia 4 nhịp:
   - Chọn 1 hoặc nhiều Master DO lấy cùng lúc (tick 2 xe).
   - Gộp tổng số lượng theo mã hàng: ba dòng "SKU 2001: 20 + 15 + 20 pcs" gộp lại thành "55 pcs".
   - Quy đổi: "55 pcs, quy cách 50 → **1 thùng 5 pcs**" (1 thùng to + 5 gói nhỏ bật ra).
   - Tách phiếu theo khu: một phiếu tách thành 3 thẻ màu **ĐÔNG / CHILL / KHÔ**.
   **Lời:** "Khi tạo phiếu lấy hàng, có thể chọn một hoặc nhiều Master DO lấy cùng lúc." / "Hệ thống gộp tổng số lượng theo từng mã hàng," / "quy đổi ra thùng và pcs, ví dụ năm mươi lăm pcs, quy cách năm mươi, là một thùng năm pcs," / "và tách phiếu theo khu: đông, chill, khô."
6. **Ngã rẽ "Khu hàng đông?"** Thẻ thoi, màn hình chia đôi: trái "KHÔNG → chill / khô · PDA", phải "CÓ → đông · phiếu giấy".
   **Lời:** "Cách lấy hàng khác nhau theo khu."
7. **Nhánh chill / khô – Bước 8: Lấy hàng bằng PDA** `PDA`. Picker (áo vàng) chọn phiếu lấy hàng trên PDA → đi tới vị trí, scan vị trí → scan mã hàng → nhập tổng số lượng "1 thùng + 5 cái".
   **Lời:** "Hàng chill và khô lấy bằng PDA:" / "picker chọn phiếu, đến vị trí và scan vị trí, scan mã hàng, rồi nhập tổng số lượng theo thùng và cái."
8. **Nhánh đông – Bước 6: Lấy hàng bằng phiếu giấy** `Thủ công`. Hơi lạnh mờ ở cửa khu đông. Picker cầm **Phiếu lấy hàng đông** (chứng từ), đi tới vị trí theo phiếu, lấy đúng số thùng + pcs, ghi số lượng thực lấy lên phiếu bằng bút.
   **Lời:** "Hàng đông lấy bằng phiếu giấy in sẵn." / "Đến vị trí theo phiếu, lấy đúng số thùng và pcs, rồi ghi số lượng thực lấy lên phiếu."
9. **Bước 7 – Xác nhận lấy hàng đông** `WMS`. Phiếu giấy được chuyển về XLCT, XLCT gõ số lượng thực lấy vào WMS → ✔.
   **Lời:** "Sau đó XLCT nhập số lượng thực lấy theo phiếu vào WMS."
10. **Bước 9 – Đưa hàng về khu chia** `Thủ công`. Hàng từ cả ba khu (đông, chill, khô) cùng chảy về **một** khu sàn có biển "KHU CHIA HÀNG".
    **Lời:** "Hàng đã lấy ở cả ba khu được đưa về chung một khu chia hàng."
11. **Ghi nhớ Phần 2:**
    - 1 xe = 1 Master DO; có thể lấy gộp nhiều Master DO
    - Số lượng gộp theo mã hàng, tính thùng + pcs
    - Đông: phiếu giấy, XLCT nhập lại WMS · Chill / khô: PDA

### Phần 3 – Chia hàng theo DO · 04K.2 (~65s)
Thẻ chương: "Phần 3 · Chia hàng theo DO".
1. **Bước 1 – Chuẩn bị khu chia** `Thủ công`. Khu chia hiện các ô vạch sơn trên sàn, picker dán số DO lên từng ô: "DO-1001", "DO-1002", "DO-1003".
   **Lời:** "Tại khu chia, mỗi DO của xe có một ô riêng, dán hoặc ghi số DO lên ô."
2. **Bước 2 – Chia hàng** `PDA`. Picker chọn "Xe 1 / Master DO" trên PDA → scan mã hàng → PDA hiện "DO-1002 · 1 thùng 5 pcs" → đặt hàng vào ô DO-1002, xác nhận ✔. Đống hàng gộp giảm dần.
   **Lời:** "Trên PDA, chọn xe hoặc Master DO, rồi scan mã hàng." / "Hệ thống chỉ DO nào và số lượng bao nhiêu." / "Đặt hàng vào đúng ô DO và xác nhận."
3. **Ngã rẽ "Đã chia hết hàng?"** Nhánh **Chưa**: mũi tên nét đứt quay lại Bước 2 (tua nhanh vài lượt). Nhánh **Rồi**: đi tiếp.
   **Lời:** "Lặp lại cho đến khi chia hết hàng."
4. **Ngã rẽ "Có thiếu / thừa?"** Nhánh **Không** → Kết thúc ✔. Nhánh **Có** → Quản lý kho xuất hiện.
5. **Bước 3 – Xử lý chênh lệch** `WMS`. Quản lý kho (model mới, cầm bìa hồ sơ) ngồi xem báo cáo "THIẾU / THỪA" trên WMS, rồi đứng lên chỉ tay vào hai thẻ:
   - "Thiếu → lấy bổ sung hoặc điều chỉnh DO"
   - "Thừa → trả hàng về vị trí"
   **Lời:** "Nếu có thiếu hoặc thừa, quản lý kho xem báo cáo chênh lệch trên WMS." / "Thiếu thì lấy bổ sung hoặc điều chỉnh DO." / "Thừa thì trả hàng về vị trí."
6. **Ghi nhớ Phần 3:**
    - Mỗi DO một ô riêng
    - Scan mã hàng → hệ thống chỉ DO và số lượng → đặt vào ô, xác nhận
    - Chênh lệch do quản lý kho xử lý

### Phần 4 – Kiểm & Bàn giao hàng · 04K.3 (~60s)
Thẻ chương: "Phần 4 · Kiểm & Bàn giao". Chứng từ: **Giấy bàn giao (theo DO)**.
1. **Bước 1 – Kiểm hàng** `PDA`. Checker (áo tím) chọn xe / Master DO, đi qua từng ô, scan mã hàng từng DO, kính lúp kiểm ngoại quan, đếm số lượng thùng + pcs.
   **Lời:** "Checker chọn xe hoặc Master DO," / "scan mã hàng của từng DO, kiểm ngoại quan và số lượng thùng, pcs."
2. **Ngã rẽ "Khớp với DO?"** Nhánh **Không** → **Bước 2 – Xử lý sai lệch** `Thủ công`: chia lại / bổ sung hàng cho DO, mũi tên nét đứt quay về Bước 1 để kiểm lại. Nhánh **Có** → đi tiếp.
   **Lời:** "Nếu không khớp, chia lại hoặc bổ sung hàng cho DO, rồi kiểm lại."
3. **Bước 3 – In giấy bàn giao** `WMS`. Máy in nhả 3 tờ **Giấy bàn giao**, mỗi tờ ghi một số DO.
   **Lời:** "Khớp rồi, checker in giấy bàn giao của xe, mỗi DO một giấy."
4. **Bước 4 – Nhận hàng, ký** `Thủ công`. Tài xế xe tải (áo xám) nhận hàng lên xe, ký từng giấy bàn giao (nét ký tự vẽ).
   **Lời:** "Tài xế xe tải nhận hàng lên xe và ký giấy bàn giao."
5. **Bước 5 – Hoàn tất xuất kho** `WMS`. XLCT bấm "Hoàn tất Master DO" → ✔ xanh "Đã xuất kho", xấp giấy đã ký vào bìa lưu hồ sơ. Xe tải lăn bánh rời dock.
   **Lời:** "XLCT xác nhận hoàn tất Master DO và lưu giấy bàn giao đã ký."
6. **Ghi nhớ Phần 4:**
    - Kiểm theo từng DO của xe; sai thì chia lại rồi kiểm lại
    - Mỗi DO một giấy bàn giao
    - Tài xế ký nhận → XLCT hoàn tất Master DO

### Kết (~15s)
Dải tổng kết 4 ô như phần mở đầu, từng ô sáng ✔ lần lượt, dưới mỗi ô một dòng tóm tắt:
Nhập & Putaway (LPN) → Lấy gộp theo xe (Master DO) → Chia theo DO → Kiểm & Bàn giao (tài xế ký).
Giảng viên giơ ngón cái.
**Lời:** "Vậy là bạn đã nắm toàn bộ quy trình kho CXAD." / "Chúc các bạn làm việc thật tốt!"

---

## 5. Đã xác nhận
1. Bỏ quy trình 01A (Thiết lập chủ hàng mới).
2. Putaway bằng **xe nâng ngồi lái**.
3. Tách nhiều vai (nhận hàng, xe nâng, picker, checker, tài xế xe tải, XLCT) thay vì một vai "Nhân viên kho".
4. "Quản lý" và "Quản lý kho" là **một vai**; model mới ở `design/model-quan-ly.png` (chờ duyệt).
5. ASN và kế hoạch xuất được nhận qua **email**.
6. Hàng đông sau khi lấy bằng giấy đưa về **chung khu chia** với hàng chill / khô.
7. Giữ các ví dụ minh họa.
8. Làm **một video liền**, có thẻ chương.

Giả định của mình (nói nếu cần đổi): **picker** là người chia hàng ở 04K.2, giống video TC.
