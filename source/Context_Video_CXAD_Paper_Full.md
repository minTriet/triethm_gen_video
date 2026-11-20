# STORYBOARD VIDEO TRAINING – KHO CXAD: NHẬP & LẤY HÀNG BẰNG GIẤY, PDA CHỈ Ở CHIA HÀNG VÀ XUẤT XE · v1 (bản nháp để duyệt)

> Video mới, cùng phong cách với video CXAD vừa chốt (`video-cxad-giay/renders/quy-trinh-kho-cxad-full-v2.mp4`):
> không giọng đọc, chỉ phụ đề (lời thoại = phụ đề nguyên văn), nhịp đọc 1.3×, hiệu ứng âm thanh thưa,
> cùng nhân vật, sơ đồ kho 3 khu Đông / Chill / Khô, màu, font. Mã hàng, xe, DO, vị trí, số lượng là **ví dụ minh họa**.
> Dự kiến **khoảng 4 phút 45 giây – 5 phút**, 1 video liền, 4 phần.

## Nguồn trong Brain Vault (`minTriet/triethm_company_brain_vault`)
- `03-Resources/Wiki/WMS - Bộ quy trình To-Be chuẩn.md`: biến thể **1 General Paper**, mã **02A Nhập hàng mới - Giấy**
  (giấy tờ + XLCT nhập liệu thay cho kho, không quét).
- `03-Resources/Diagrams/WMS/To-Be/specs/VI/To_Be_1_General_Paper_VI.spec.json`, trang **02A** (7 bước).
- `03-Resources/SOP/SOP - CXAD Bộ quy trình kho.md`: **Phiên bản B – Lấy hàng hoàn toàn bằng giấy** (04K.1 giấy),
  04K.2 chia hàng 🔍, 04K.3 kiểm và bàn giao 🔍; CXAD bắt buộc **date / batch**, putaway **theo khu**.

## Khác gì so với video CXAD vừa chốt

| Chặng | Video vừa chốt | Bản mới |
| --- | --- | --- |
| Nhập hàng | Barcode LPN (02F): tạo phiếu nhập, quét LPN, quét mã hàng, nhập SL, date/batch **trên PDA** | **Giấy (02A)**: XLCT in **phiếu kiểm đếm** + **nhãn chi tiết pallet**; kho đếm và **ghi tay** SL, date/batch; **XLCT nhập vào WMS** |
| Cất hàng | Quét LPN → hệ thống gợi ý vị trí → quét vị trí | **Giấy**: kho đưa pallet lên kệ đúng khu, **ghi vị trí**; **XLCT nhập vị trí** vào WMS |
| Lấy hàng | Picklist giấy theo khu | **Giữ nguyên** (Picklist giấy) |
| Chia hàng theo DO | PDA | **PDA** – lần đầu tiên dùng PDA trong video |
| Kiểm & xác nhận lên xe | PDA | **PDA** |

Ý chính người xem phải nhớ: **Nhập, cất và lấy hàng làm trên giấy – XLCT nhập lại vào WMS. Chỉ khi chia hàng và xác nhận hàng lên xe mới dùng PDA.**

Mỗi bước có thêm **nhãn nhỏ "GIẤY" (cam) hoặc "PDA" (xanh)** cạnh badge để người xem thấy rõ chỗ nào dùng gì.

---

## Kịch bản (lời thoại = phụ đề)

### Mở đầu (~15s) — *sửa từ cảnh cũ*
- **Hình:** tiêu đề "Quy trình vận hành kho CXAD – Nhập và lấy hàng bằng giấy". Giảng viên vẫy tay. Dải 4 chặng, dưới mỗi chặng có nhãn:
  Nhập & cất hàng **[GIẤY]** → Lấy hàng gộp theo xe **[GIẤY]** → Chia hàng theo DO **[PDA]** → Kiểm & xác nhận lên xe **[PDA]**.
- **Lời:** "Xin chào các bạn. Video này đi qua quy trình kho CXAD khi nhập và lấy hàng bằng giấy." / "PDA chỉ dùng ở hai bước: chia hàng và xác nhận hàng lên xe."

### Sơ đồ kho (~10s) — *giữ nguyên*
**Lời:** "Kho có ba khu theo nhiệt độ: khu đông, khu chill và khu khô."

### Phần 1 – Nhập hàng và cất hàng bằng giấy (02A) (~85s) — *làm mới*
1. **Bước 1 – Nhận ASN** [GIẤY · XLCT] · File kế hoạch nhập, sửa cột cho đúng mẫu WMS (dùng lại cảnh cũ).
   **Lời:** "Khi có kế hoạch nhập, XLCT nhận file và xử lý cho đúng định dạng WMS."
2. **Bước 2 – Nhập vào WMS** [XLCT] · Import → ASN-0001 hiện ra (dùng lại cảnh cũ, bỏ phần in LPN).
   **Lời:** "Sau đó nhập file vào WMS để tạo ASN."
3. **Bước 3 – In chứng từ** [XLCT] · Máy in nhả 2 chứng từ bay ra góc phải: **Phiếu kiểm đếm** (cột Mã hàng · SL phiếu · **SL thực nhận** · **Date / Batch** để trống) và **Nhãn chi tiết pallet** (3 nhãn). XLCT trao cho nhân viên nhận hàng.
   **Lời:** "XLCT in phiếu kiểm đếm và nhãn chi tiết pallet," / "rồi giao cho nhân viên nhận hàng."
4. **Bước 4 – Nhận hàng** [GIẤY · Nhân viên nhận hàng] · Xe 51C-123.45 lùi vào dock. Nhân viên dỡ thùng, kính lúp kiểm ngoại quan ✔, đếm (số đếm bật lên 1…40), xếp lên pallet, dán nhãn chi tiết pallet. Cận cảnh phiếu kiểm đếm: bút **ghi tay** "40 thùng" và "HSD 20/05/2027 · B2405". Nhân viên cầm bìa kẹp giấy, **không cầm PDA**.
   **Lời:** "Xe hàng tới, nhân viên dỡ hàng, kiểm tra ngoại quan và đếm hàng." / "Xếp hàng lên pallet, dán nhãn chi tiết pallet," / "rồi ghi số lượng thực nhận và date hoặc batch lên phiếu kiểm đếm."
5. **Bước 5 – Hoàn tất nhận hàng** [XLCT] · Nhân viên nộp phiếu kiểm đếm. XLCT gõ SL + date/batch từ tờ giấy vào WMS (mũi tên từ ô viết tay sang ô trên màn hình), bấm xác nhận → in **Phiếu nhập kho**, 3 chữ ký hiện lần lượt.
   **Lời:** "Nhân viên nộp phiếu kiểm đếm cho XLCT." / "XLCT nhập số lượng và date hoặc batch vào WMS, xác nhận đã nhận hàng xong," / "in phiếu nhập kho và chuyển các bên ký."
6. **Bước 6 – Đưa hàng lên kệ** [GIẤY · Tài xế xe nâng] · Banner KHU CHILL. Xe nâng đưa pallet lên ô trống A01-02. Tài xế **ghi vị trí** "CHILL-A01-02" lên phiếu cất hàng (bìa kẹp). Tua nhanh 2 pallet còn lại vào khu ĐÔNG và KHÔ, mỗi lần ghi vị trí.
   **Lời:** "Tài xế xe nâng đưa từng pallet lên kệ đúng khu," / "và ghi lại vị trí của từng pallet lên phiếu."
7. **Bước 7 – Cất hàng vào vị trí** [XLCT] · XLCT nhận phiếu, nhập vị trí cho 3 pallet vào WMS (3 dòng lần lượt ✔).
   **Lời:** "XLCT nhập vị trí của các pallet vào WMS để hoàn tất cất hàng."
8. **Ghi nhớ Phần 1:**
   - XLCT in **phiếu kiểm đếm** và **nhãn chi tiết pallet**
   - Kho đếm hàng, **ghi tay** số lượng, date / batch – không dùng PDA
   - Kho ghi vị trí cất hàng, **XLCT nhập lại vào WMS**

### Phần 2 – Lấy hàng gộp theo xe bằng giấy (04K.1 giấy) (~70s) — *giữ nguyên, chỉ thêm nhãn GIẤY*
Bước 1–8 như video vừa chốt: Nhận kế hoạch xuất → Import tạo DO → Tạo Master DO (1 xe = 1 Master DO) → Phân bổ tồn (FIFO / FEFO)
→ In Picklist (gộp theo mã hàng, thùng + lẻ: 55 hũ = 1 thùng 5 hũ, tách theo khu) → Lấy hàng bằng giấy, ghi SL thực lấy
→ Đưa về khu chia, nộp Picklist → XLCT nhập SL thực lấy vào WMS. Lời thoại giữ nguyên.
**Thêm 1 câu ở cuối Bước 8** (điểm vault ghi là cần lưu ý):
**Lời:** "XLCT phải nhập xong số thực lấy thì mới chia hàng trên PDA được."
**Ghi nhớ Phần 2:** giữ nguyên.

### Phần 3 – Chia hàng theo đơn DO (04K.2) (~45s) — *giữ nguyên, thêm nhãn PDA và 1 câu mở*
- Mở phần: PDA lớn bật lên với nhãn **"Bắt đầu dùng PDA"**.
  **Lời:** "Từ bước chia hàng, nhân viên bắt đầu dùng PDA."
- Bước 1 Chuẩn bị khu chia · Bước 2 Chia hàng (PDA) · *Đã chia hết hàng?* · *Có thiếu / thừa?* · Bước 3 Xử lý chênh lệch (thủ công) — như video vừa chốt.
**Ghi nhớ Phần 3:** giữ nguyên.

### Phần 4 – Kiểm hàng và xác nhận lên xe (04K.3) (~50s) — *giữ nguyên, đổi tên phần, thêm nhãn PDA*
Bước 1 Kiểm hàng **[PDA]** (quét mã hàng từng DO, kiểm ngoại quan, SL) · *Khớp với DO?* · Bước 2 Xử lý sai lệch (thủ công)
· Bước 3 In giấy bàn giao · Bước 4 Tài xế nhận hàng và ký · Bước 5 XLCT hoàn tất Master DO, xe ra kho. Lời thoại giữ nguyên.
**Ghi nhớ Phần 4:** giữ nguyên.

### Kết (~10s) — *sửa*
Dải 4 chặng với nhãn GIẤY / PDA, từng chặng đóng dấu ✔. Giảng viên giơ ngón cái.
**Lời:** "Nhập, cất và lấy hàng làm trên giấy, XLCT nhập lại vào WMS." / "Chia hàng và xác nhận lên xe dùng PDA. Chúc các bạn làm việc thật tốt!"

---

## Dùng lại / làm mới (ước lượng công dựng)

| Phần | Cảnh |
| --- | --- |
| Mở đầu, Kết | Sửa (thêm nhãn GIẤY / PDA, đổi lời) |
| Phần 1 | **Làm mới** 5 cảnh (Bước 3, 4, 5, 6, 7) + Ghi nhớ mới; Bước 1–2 dùng lại |
| Phần 2, 3, 4 | Dùng lại, thêm nhãn GIẤY / PDA, thêm 2 câu (cuối Phần 2, mở Phần 3), đổi tên Phần 4 |

---

## Cần bạn xác nhận trước khi dựng
Mình đã điền sẵn lựa chọn đề xuất; bạn chỉ cần sửa những dòng không đúng.

1. **Nhập hàng theo 02A (giấy)**: dùng **nhãn chi tiết pallet** thay cho mã vạch LPN, không còn bước "Tạo phiếu nhập trên PDA". → Đề xuất: đúng.
2. **Thứ tự 02A**: XLCT **hoàn tất nhận hàng, in phiếu nhập kho** (Bước 5) **trước** khi đưa hàng lên kệ (Bước 6–7), đúng như sơ đồ chuẩn. → Đề xuất: giữ thứ tự này.
3. **Cất hàng bằng giấy**: không có vị trí gợi ý; tài xế xe nâng tự chọn **ô trống trong đúng khu**, ghi vị trí lên phiếu. → Đúng không, hay XLCT in sẵn vị trí gợi ý trên phiếu?
4. **Ai ghi phiếu kiểm đếm**: nhân viên nhận hàng; **ai cất hàng**: tài xế xe nâng (tách vai như video vừa chốt). → Đề xuất: đúng.
5. **"Xác nhận lên xe ra kho" bằng PDA** = bước Kiểm hàng của 04K.3 (Checker quét từng DO trước khi giao tài xế). → Đúng không, hay cần thêm bước quét xác nhận khi hàng lên xe / xe qua cổng (theo 07B)?
6. **Hai câu nhắc thêm** (cuối Phần 2 và mở Phần 3) lấy từ ghi chú rủi ro trong vault: giữ hay bỏ?
7. **Tên file video** mới: `video-cxad-paper/` → `quy-trinh-kho-cxad-giay-v1.mp4`.
