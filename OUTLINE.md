# Outline v2 – Series “Vận hành kho khô” (5 tập)

Nguồn: `Prompt_Video_Training_Kho_Kho.md`. Bạn đã viết sẵn kịch bản và lời thoại, nên mình **giữ nguyên kịch bản, lời thoại và thứ tự cảnh**. Outline này chỉ chốt cách dựng, để bạn duyệt trước khi mình làm cả 5 tập.

---

## 1. Kế hoạch xử lý

| Bước | Việc | Kết quả để duyệt |
| --- | --- | --- |
| 0 | **Duyệt outline này** (bạn đang ở đây) | Chốt phong cách, cấu trúc, cách làm giọng đọc |
| 1 | Dựng **bộ nhân vật dùng chung**: 6 người que, kệ isometric, PDA, xe nâng, trolley, Oricon, xe tải, badge “Bước n”, thẻ “Ghi nhớ”, phụ đề | 1 khung hình mẫu mỗi thành phần |
| 2 | Làm trọn **Tập 1** (phụ đề, hiệu ứng âm thanh, chuyển động), xem trước trong preview | Bạn xem Tập 1 và góp ý |
| 3 | Sửa theo góp ý, render MP4 Tập 1 | `tap-1.mp4` |
| 4 | Làm Tập 2 → 5 dùng lại bộ nhân vật, mỗi tập duyệt preview rồi mới render | `tap-2.mp4` … `tap-5.mp4` |

Video được dựng **trực tiếp trong repo** bằng HyperFrames: mỗi tập là các file HTML/GSAP, sửa được, có lịch sử commit. Đây không phải project trên app HeyGen.

### Cấu trúc thư mục
```
triethm_gen_video/
  OUTLINE.md · SPEC.md
  shared/            # nhân vật, kệ, PDA, badge, thẻ Ghi nhớ, style, font
  tap-1-tong-quan/   index.html + compositions/scene-*.html + assets/
  tap-2-nhap-hang/
  tap-3-don-hang-cham-hang/
  tap-4-pick-hang/
  tap-5-kiem-hang-ban-giao/
```

---

## 2. Thông số chung (áp dụng cho cả 5 tập)

| Hạng mục | Chốt |
| --- | --- |
| Khung hình | 1920×1080, 30 fps |
| Thời lượng | Tập 1 = 76s · Tập 2–4 khoảng 90s · Tập 5 khoảng 80s. **Không có giọng đọc**: mỗi câu phụ đề được giữ đủ lâu để đọc thong thả (khoảng 0.3s mỗi chữ + 0.5s), nên mốc giây có thể lệch vài giây so với file gốc. |
| Nền | Xám rất nhạt `#F4F6F9`, sàn kho `#E6EAF0` |
| Màu chính | Xanh doanh nghiệp `#1F5FBF` · Cam “quan trọng” `#F28C1E` · Xanh lá “xong” `#22A55A` · Đỏ “thiếu/lỗi” `#D93B3B` |
| Reserved / Primary | Tầng trên xanh nhạt `#BFD8F5` (nhãn “RESERVED – Lưu kho”) · tầng sát đất cam `#F28C1E` (nhãn “PRIMARY – Pick face”) |
| Font | **Be Vietnam Pro** (thiết kế cho tiếng Việt, đủ dấu), đóng file vào `shared/fonts/` để render ở đâu cũng giống nhau. Tiêu đề 900, nội dung 600, phụ đề 700. |
| Phụ đề | Tiếng Việt, cỡ 56px, tối đa 2 dòng, nền dải trắng 90%, đáy khung (trong vùng an toàn 80%), hiện theo từng cụm câu khớp giọng đọc |
| Giọng đọc | **Không dùng** (đã chốt). Lời thoại trong file gốc được dùng nguyên văn làm phụ đề. |
| Nhạc nền | Chưa có: thư viện nhạc miễn phí cần đăng nhập HeyGen. Có thể thêm sau mà không phải dựng lại hình. |
| Hiệu ứng âm thanh (đang dùng, bộ có sẵn) | “beep” khi scan, “pop” nhẹ khi item xuất hiện, “stamp” khi đóng dấu ✔, tiếng xe nâng/xe tải rất nhỏ |

### Nhân vật người que (vẽ SVG, chuyển động bằng GSAP)
Đầu tròn, thân nét đen 6px, hai chấm mắt và miệng cười. Mỗi vai có áo khoác hoặc mũ màu riêng, và **nhãn vai** hiện trên đầu ở lần xuất hiện đầu tiên.

| Vai | Màu | Đạo cụ |
| --- | --- | --- |
| Nhân viên nhận hàng | Xanh lá | thùng carton |
| Tài xế xe nâng | Cam | xe nâng phẳng |
| Nhân viên điều phối | Áo xanh dương | bàn và máy tính |
| Picker | Vàng | trolley hoặc Oricon |
| Checker | Tím | PDA |
| Đội vận tải | Xám | xe tải |
| Giảng viên (mở/kết tập) | Áo xanh dương, cà vạt cam | – |

Động tác dùng chung: đi bộ, giơ PDA scan (tia laser đỏ, vòng sóng “beep”), nhấc thùng, đẩy trolley, vẫy tay, giơ ngón cái.

### Quy tắc hình ảnh
- Mỗi cảnh **một ý**, nhiều khoảng trắng.
- Khi có thao tác trên hệ thống: **PDA phóng to** ở bên phải, hiện đúng ô đang nhập (“Scan LPN”, “Scan SKU”, “Nhập số lượng”…).
- Mỗi bước có badge lớn “Bước n” và 1 dòng chú thích. Bước xong thì đóng dấu ✔ xanh.
- Mũi tên tự vẽ dọc đường đi, vật thể bật nhẹ khi xuất hiện, camera zoom nhẹ vào hành động.
- Cuối mỗi tập: thẻ **“Ghi nhớ”** 3 ý, rồi tên tập sau.

---

## 3. Outline chi tiết – TẬP 1: Tổng quan kho khô (khoảng 70s)

| # | Thời gian (ước) | Hình ảnh và chuyển động | Lời thoại (giữ nguyên) |
| --- | --- | --- | --- |
| 1 | 0–8s | **Khung đầu (thumbnail):** tiêu đề “Vận hành kho khô – Tập 1: Tổng quan kho” ở bên trái, kệ kho isometric mờ phía sau. Giảng viên người que bước vào từ phải và vẫy tay. Tiêu đề hiện từng chữ, badge “Tập 1” màu cam bật nhẹ. | “Xin chào các bạn. Trong loạt video này, chúng ta sẽ cùng tìm hiểu cách kho vận hành, từng bước một, thật đơn giản.” |
| 2 | 8–25s | **Bay qua kho:** camera trượt chéo qua 4 dãy kệ isometric (không cắt cảnh). Dừng ở một kệ. Khi giọng nói “tầng trên cao”: các tầng trên sáng xanh nhạt và nhãn “RESERVED – Lưu kho” bật ra. Khi nói “tầng sát mặt đất”: tầng đáy sáng cam và nhãn “PRIMARY – Pick face” bật ra. Một picker vàng đi ngang và lấy 1 thùng ở tầng đáy. | “Kho khô có nhiều dãy kệ. Các tầng trên cao gọi là khu Reserved, dùng để lưu trữ hàng. Tầng sát mặt đất gọi là khu Primary, hay pick face, là nơi nhân viên lấy hàng.” |
| 3 | 25–42s | **Zoom vào 1 ô pick face** (camera đi tiếp từ cảnh 2, không cắt). Trong ô có 1 hộp sản phẩm và mã ví dụ “SKU 1001”. Ổ khóa đóng “cạch” và dấu ✔. Nhãn lớn: “1 vị trí = 1 mã hàng (cố định)”. Một mã hàng khác thử bay vào ô thì bị dấu ✖ đỏ đẩy ra. | “Điều quan trọng cần nhớ: mỗi vị trí pick face chỉ chứa một mã hàng duy nhất, và mã hàng đó luôn cố định tại vị trí ấy.” |
| 4 | 42–60s | **Camera kéo lại nhìn toàn kho từ trên xuống.** 4 dãy kệ lần lượt sáng lên đúng lúc được đọc tên, mỗi dãy có biển lớn trên đầu: “Dãy Nước uống” (chai) → “Dãy Mì” (ly mì) → “Dãy Snack” (gói snack) → “Dãy Sữa” (hộp sữa). Icon vẽ phẳng, không dùng emoji. | “Mỗi dãy kệ được dành riêng cho một ngành hàng: một dãy cho nước uống, một dãy cho mì, một dãy cho snack, và một dãy cho sữa.” |
| 5 | 60–70s | **Thẻ “Ghi nhớ”** (3 ý hiện lần lượt, mỗi ý kèm icon nhỏ lấy từ cảnh trước): • Trên cao = Reserved (lưu kho) • Mặt đất = Primary (pick face) • 1 vị trí pick face = 1 mã hàng cố định. Sau đó dải “Tiếp theo: Tập 2 – Nhập hàng & Cất hàng”, giảng viên chỉ tay về dải này. Giữ khung 2s. | “Nắm được sơ đồ kho rồi, chúng ta sẽ đi tiếp đến bước nhập hàng.” |

**Hình thức:** cảnh 2 → 3 → 4 là **một cú máy liền mạch trong cùng một nhà kho** (bay vào, zoom ô, kéo ra), để người mới luôn biết mình đang đứng ở đâu trong kho. Cảnh 1 và 5 là khung giảng viên. Tập 2–5 dùng lại đúng nhà kho này làm “sân nhà”.

---

## 4. Đã chốt

1. Giọng đọc: **bỏ**, chỉ giữ phụ đề.
2. Mã hàng, mã vị trí, mã cửa hàng, số lượng: **minh họa**.
3. Logo hoặc tên công ty: **không cần**.

---

## 5. Thay đổi theo góp ý Tập 1 (áp dụng cho bản tiếp theo)

1. **Gộp 5 tập thành MỘT video** (khoảng 5–6 phút). Giữa các phần có một thẻ chương ngắn ("Phần 2: Nhập hàng & Cất hàng") thay cho màn kết/mở của từng tập. Thẻ "Ghi nhớ" vẫn giữ ở cuối mỗi phần.
2. **Nhịp nhanh hơn 1.3×** ở những đoạn đọc chữ: thời gian giữ mỗi câu phụ đề = (0.5s + 0.3s × số chữ) ÷ 1.3. Chuyển động camera và các đoạn chỉ có hình cũng rút ngắn theo.
3. **Hiệu ứng âm thanh tiết chế:** chỉ dùng ở các khoảnh khắc chính (chuyển phần, xác nhận ✔, báo lỗi ✖, tiếng beep khi scan). Hai tiếng cách nhau ít nhất 4s, âm lượng nhỏ hơn bản trước. Bỏ hết tiếng pop khi nhãn hoặc biển xuất hiện.
4. **Nhân vật v2** theo `design/model-sheet-v2.png`: có vai, khuỷu tay, đầu gối; áo bảo hộ có sọc phản quang và mũ bảo hộ theo màu vai.
