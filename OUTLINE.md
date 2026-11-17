# Outline v1 – Series “Vận hành kho khô” (5 tập)

Nguồn: `Prompt_Video_Training_Kho_Kho.md`. Bạn đã viết sẵn kịch bản và lời thoại, nên mình **giữ nguyên kịch bản, lời thoại và thứ tự cảnh**. Outline này chỉ chốt cách dựng, để bạn duyệt trước khi mình làm cả 5 tập.

---

## 1. Kế hoạch xử lý

| Bước | Việc | Kết quả để duyệt |
| --- | --- | --- |
| 0 | **Duyệt outline này** (bạn đang ở đây) | Chốt phong cách, cấu trúc, cách làm giọng đọc |
| 1 | Đăng nhập HeyGen để có giọng đọc tiếng Việt và nhạc nền (xem §4) | – |
| 2 | Dựng **bộ nhân vật dùng chung**: 6 người que, kệ isometric, PDA, xe nâng, trolley, Oricon, xe tải, badge “Bước n”, thẻ “Ghi nhớ”, phụ đề | 1 khung hình mẫu mỗi thành phần |
| 3 | Làm trọn **Tập 1** (giọng đọc, nhạc, phụ đề, chuyển động), xem trước trong preview | Bạn xem Tập 1 và góp ý |
| 4 | Sửa theo góp ý, render MP4 Tập 1 | `tap-1.mp4` |
| 5 | Làm Tập 2 → 5 dùng lại bộ nhân vật, mỗi tập duyệt preview rồi mới render | `tap-2.mp4` … `tap-5.mp4` |

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
| Thời lượng | Tập 1 khoảng 70s · Tập 2–4 khoảng 90s · Tập 5 khoảng 80s. **Giọng đọc quyết định nhịp**: mỗi cảnh dài đúng bằng câu thoại của nó, nên mốc giây trong file gốc chỉ là ước lượng (lệch ±5s). |
| Nền | Xám rất nhạt `#F4F6F9`, sàn kho `#E6EAF0` |
| Màu chính | Xanh doanh nghiệp `#1F5FBF` · Cam “quan trọng” `#F28C1E` · Xanh lá “xong” `#22A55A` · Đỏ “thiếu/lỗi” `#D93B3B` |
| Reserved / Primary | Tầng trên xanh nhạt `#BFD8F5` (nhãn “RESERVED – Lưu kho”) · tầng sát đất cam `#F28C1E` (nhãn “PRIMARY – Pick face”) |
| Font | **Be Vietnam Pro** (thiết kế cho tiếng Việt, đủ dấu), đóng file vào `shared/fonts/` để render ở đâu cũng giống nhau. Tiêu đề 900, nội dung 600, phụ đề 700. |
| Phụ đề | Tiếng Việt, cỡ 56px, tối đa 2 dòng, nền dải trắng 90%, đáy khung (trong vùng an toàn 80%), hiện theo từng cụm câu khớp giọng đọc |
| Giọng đọc | Nam, trầm ấm, chậm khoảng 0.8× (chậm hơn bình thường 20%), nghỉ 0.4–0.6s giữa câu |
| Nhạc nền | Lo-fi/acoustic nhẹ, âm lượng khoảng 0.14 dưới giọng, fade in/out 1.5s |
| Hiệu ứng âm thanh | “beep” khi scan, “pop” nhẹ khi item xuất hiện, “stamp” khi đóng dấu ✔, tiếng xe nâng/xe tải rất nhỏ |

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

## 4. Cần bạn quyết định

1. **Giọng đọc tiếng Việt (bắt buộc chọn):**
   - **(a) HeyGen voice, khuyến nghị.** Cần đăng nhập HeyGen (miễn phí). Gói Free có 3 phút Voice Turbo mỗi tháng, mà cả series khoảng **7 phút thoại**: đủ cho Tập 1–2, các tập sau cần gói trả phí hoặc chờ tháng sau. Đăng nhập cũng mở luôn thư viện nhạc nền và hiệu ứng âm thanh miễn phí.
   - **(b) Bạn tự thu âm** lời thoại (file .m4a/.wav, mỗi cảnh 1 file). Miễn phí, giọng đúng ý nhất. Mình sẽ tự tách thời gian từng chữ để khớp phụ đề.
   - Giọng đọc offline miễn phí (Kokoro) **không có tiếng Việt**, nên không dùng được.
2. **Mã ví dụ** (SKU 1001, A-01-01, CH-0125, số thùng…): giữ làm minh họa hay bạn gửi dữ liệu thật?
3. **Logo hoặc tên công ty** ở cuối tập: có cần không? (Mặc định là không.)

> Nếu chọn (a): gõ vào ô chat: `! cd /home/user/triethm_gen_video && node .claude/skills/hyperframes/scripts/plugin-cli.mjs auth login`, làm xong thì báo mình.

**Bạn duyệt outline Tập 1 + thông số chung**, hoặc ghi chỉnh sửa. Sau đó mình bắt đầu Bước 2.
