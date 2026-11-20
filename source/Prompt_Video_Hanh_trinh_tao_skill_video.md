# PROMPT VIDEO / SLIDE – HÀNH TRÌNH TẠO "KỸ NĂNG LÀM VIDEO THEO Ý TÔI" · v2 (theo storyboard đã duyệt)

> Mục đích: kể lại **quá trình và cách thức** tôi đã biến Claude Code + HyperFrames thành một "kỹ năng" làm video training kho
> đúng ý mình, để người khác (đồng nghiệp, quản lý) hiểu và làm lại được.
> Nguồn sự thật: lịch sử commit của repo `triethm_gen_video` (17–18/11/2026), `OUTLINE.md`, `PROGRESS.md`, các file trong `source/`,
> skill `.claude/skills/nhan-vat-kho`, thư mục `design/`, `tools/`, `deck/`.
> Dùng được cho **2 đầu ra**: [B1] video HyperFrames (~3 phút) **hoặc** [B2] slide deck (~12 slide). Luôn dán **[A]** trước.

---

## [A] KHỐI BỐI CẢNH + PHONG CÁCH CHUNG (dán ở đầu)

```
Bạn là người dựng nội dung trong repo triethm_gen_video. Hãy kể lại HÀNH TRÌNH tôi đã tạo ra
"kỹ năng làm video theo ý tôi" – từ một prompt viết tay đến một quy trình lặp lại được,
có bộ nhân vật đóng gói thành skill riêng. Khán giả: đồng nghiệp không biết code, muốn tự làm
video training tương tự. Mục tiêu: rất dễ hiểu, thấy rõ TỪNG BƯỚC và VÌ SAO làm như vậy.

DỮ KIỆN THẬT (không bịa thêm số liệu; lấy đúng từ repo):
- Công cụ: Claude Code + 9 skill HyperFrames cài từ heygen-com/hyperframes (video = HTML/GSAP render ra MP4).
- Thời gian: 2 ngày (17–18/11/2026), 27 commit.
- Sản phẩm: 3 video training + 1 deck:
  • "Vận hành kho khô" – 5 phần gộp 1 video, 5:09, 1080p
  • "Vận hành hàng TC (trung chuyển)" – 2:12
  • "Quy trình toàn kho CXAD" – 4 phần, 5:20, qua 3 bản v1 → v2 → v3
  • Deck "Quy trình vận hành kho khô và TC" – 17 slide (.pptx)
- Tài sản dùng lại: bộ vẽ Python (tools/kit.py, stage.py…) ~5.000 dòng sinh ra các cảnh;
  bảng nhân vật model sheet v2 → v3; skill riêng "nhan-vat-kho" (8 vai người que mặc định).

CÁC MỐC CỦA HÀNH TRÌNH (theo đúng thứ tự commit):
 1. Chuẩn bị: cài skill HyperFrames vào repo.
 2. Viết prompt gốc: khối phong cách chung [A] + kịch bản từng tập [B], lời thoại viết sẵn.
 3. Claude lập OUTLINE để tôi duyệt TRƯỚC khi dựng: kế hoạch, thông số chung (màu, font Be Vietnam Pro,
    1920×1080, 30 fps), bảng vai – màu – đạo cụ, quy tắc hình ảnh (mỗi cảnh 1 ý, badge "Bước n",
    PDA phóng to, thẻ "Ghi nhớ").
 4. Chốt 3 quyết định: bỏ giọng đọc (lời thoại = phụ đề nguyên văn); mã hàng/vị trí/số lượng là minh họa; không logo.
 5. Dựng bộ vẽ dùng chung + Tập 1 bản nháp → xem → góp ý.
 6. Góp ý Tập 1 thành 4 luật mới: gộp 5 tập thành 1 video có thẻ chương; nhịp đọc nhanh 1.3×
    (giữ phụ đề = (0.5s + 0.3s × số chữ) ÷ 1.3); hiệu ứng âm thanh thưa, cách nhau ≥ 4 s;
    nhân vật v2 có vai, khuỷu tay, đầu gối, áo phản quang + mũ bảo hộ theo màu vai.
 7. Duyệt model sheet v2 và demo dáng đi (nghiêng trái/phải + nhún nhẹ).
 8. Duyệt 31 giây đầu → mới làm tiếp phần 1–5 → render bản đầy đủ 5:09.
 9. Video TC: viết "context" so sánh với video trước → xác nhận v2 → duyệt 36 s đầu → bản đầy đủ 2:12.
10. Deck 17 slide tóm tắt quy trình kho khô và TC.
11. Video CXAD: đưa bản vẽ quy trình (PDF drawio) → prompt v1 nháp → v2 đã xác nhận
    (bỏ quy trình 01A vì không phải việc của nhân viên kho; tách vai; chip WMS / PDA / Thủ công /
    Chứng từ / ô thoi Điều kiện lấy từ chú giải bản vẽ).
12. Cần thêm vai "Quản lý kho" → vẽ mẫu, duyệt → đóng gói TOÀN BỘ nhân vật thành skill "nhan-vat-kho"
    (model v3) để mọi video sau dùng lại, không vẽ lại.
13. Render CXAD v1 → sửa theo góp ý: v2 (phụ đề quy đổi bằng số, nhãn LPN + mã vị trí to hơn)
    → v3 (ô điều kiện khớp mũi tên rẽ nhánh).

"CÔNG THỨC" RÚT RA (đây là thông điệp chính):
  Nguồn (quy trình / bản vẽ) → Prompt hoặc Context (có bảng "khác gì video trước")
  → Outline để duyệt → Chốt quyết định thành văn bản → Model sheet nhân vật
  → Bản mẫu 30 giây → Làm đủ → Render → Sửa theo vòng v2, v3
  → Đóng gói cái dùng lại được (bộ vẽ, skill nhân vật) cho video sau.

BÀI HỌC (mỗi ý 1 câu):
  • Duyệt sớm bằng thứ nhỏ (outline, model sheet, 30 giây đầu) – sửa rẻ hơn sửa cả video.
  • Mọi góp ý biến thành LUẬT ghi trong file, video sau tự kế thừa.
  • Viết rõ "khác gì so với video trước" để không lẫn khái niệm giữa các quy trình.
  • Thứ dùng nhiều lần (nhân vật) thì đóng gói thành skill.
  • Mỗi lần sửa là một phiên bản có commit – luôn quay lại được.

PHONG CÁCH (giữ đúng bộ đã chốt của repo):
- Tiếng Việt. Không giọng đọc, chỉ phụ đề (lời bên dưới = phụ đề nguyên văn), nhịp đọc 1.3×.
- 1920×1080, 30 fps. Nền #F4F6F9. Xanh #1F5FBF chủ đạo, cam #F28C1E "quan trọng",
  xanh lá #22A55A "xong / đã duyệt", đỏ #D93B3B "bỏ / sửa". Font Be Vietnam Pro (900 / 600 / 700).
- Nhân vật: dùng skill nhan-vat-kho (model v3). "Tôi" = vai instructor (giảng viên, sơ mi xanh,
  cà vạt cam). "Claude" = KHÔNG vẽ thành người: là một khung chat / cửa sổ terminal bo góc
  có con trỏ nhấp nháy, gõ chữ ra.
- Mỗi mốc có badge "Bước n" + 1 dòng chú thích. Mốc được duyệt: dấu ✔ xanh "Đã duyệt".
  Mốc bị sửa: bản cũ gạch đỏ, bản mới trượt vào.
- Dùng HÌNH THẬT từ repo khi có: design/model-sheet-v2.png, design/model-sheet-v3.png,
  design/model-quan-ly.png, design/walk-demo.mp4, các khung hình chụp từ 3 video trong
  video/renders, video-tc/renders, video-cxad/renders. Đặt trong khung "màn hình" bo góc.
- Hiệu ứng âm thanh thưa (≥ 4 s): chỉ khi chuyển phần, ✔ duyệt, ✖ bỏ.
- Mỗi cảnh 1 ý, nhiều khoảng trắng, không thuật ngữ code (gọi "file HTML" là "trang dựng cảnh",
  "commit" là "lưu phiên bản").
```

---

## [B1] VIDEO HYPERFRAMES – "Tôi đã dạy Claude làm video theo ý mình như thế nào" (~3 phút 05 giây)

```
Một video liền, có thẻ chương giữa các phần. Lời = phụ đề nguyên văn.

MỞ ĐẦU (~12s)
- Hình: tiêu đề "Từ một prompt đến một kỹ năng làm video". Giảng viên vẫy tay. Bên phải hiện
  4 thumbnail (3 video + 1 deck) bay vào, kèm chip "2 ngày · 27 phiên bản".
- Lời: "Đây là ba video training và một bộ slide, làm trong hai ngày." /
       "Video này kể lại tôi đã làm thế nào, để bạn cũng làm được."

PHẦN 1 – Bắt đầu từ một prompt (~35s)
- Bước 1: thẻ "Cài 9 skill HyperFrames" – 9 ô nhỏ xếp vào một hộp đồ nghề.
  Lời: "Đầu tiên, tôi cài cho Claude bộ 9 skill dựng video HyperFrames."
- HYPERFRAMES LÀ GÌ? (~15s, không có badge "Bước n"): tiêu đề "Video = một trang web chạy theo thời gian".
  Trái: cửa sổ code gõ ra đoạn thật trong project (khung phụ đề có data-start / data-duration,
  một nhân vật SVG, một dòng GSAP tl.to("#picker", {x: 600})). Giữa: 3 vạch HTML (cảnh, chữ, nhân vật) /
  CSS (màu, font, bố cục) / GSAP (chuyển động) sáng lần lượt. Phải: trình duyệt chụp từng khung –
  3 khung phim picker dịch dần sang phải, "30 khung / giây" → ô MP4. Chữ "frontend" đổi màu cam ở câu cuối.
  Lời: "HyperFrames dựng video bằng chính HTML, giống như làm một trang web." /
       "Cảnh là HTML và CSS, chuyển động viết bằng JavaScript." /
       "Trình duyệt chạy trang đó và chụp từng khung, 30 khung mỗi giây, rồi ghép thành MP4." /
       "Vì vậy cốt lõi là frontend: dựng được trang web thì dựng được video."
- Bước 2: tờ giấy "Prompt gốc" chia 2 khối: [A] Phong cách chung + [B] Kịch bản từng tập.
- Bước 3: khung Claude gõ ra "OUTLINE" – bảng màu, font, bảng vai. Giảng viên đóng dấu ✔.
- Lời: "Tôi bắt đầu bằng một prompt: phong cách chung và kịch bản từng tập." /
       "Claude không dựng ngay, mà lập outline để tôi duyệt trước."

PHẦN 2 – Xem bản nháp, biến góp ý thành luật (~40s)
- Bước 4: khung "Tập 1 – bản nháp" chạy vài giây (dùng tap-1-tong-quan/renders/tap-1-draft.mp4).
- Bước 5: 4 thẻ góp ý lật thành 4 "luật" có số:
  "5 tập → 1 video" · "Nhịp đọc 1.3×" · "Âm thanh cách nhau ≥ 4 giây" · "Nhân vật v2".
- Bước 6: model sheet v1 (người que đơn giản) trượt ra, model-sheet-v2.png trượt vào; cạnh đó
  demo dáng đi nghiêng – nhún (walk-demo.mp4). Dấu ✔ "Đã duyệt".
- Bước 7: thanh thời lượng: đoạn 0:31 sáng xanh "Duyệt 31 giây đầu", rồi kéo dài ra 5:09.
- Lời: "Xem Tập 1 xong, tôi góp ý bốn điểm." /
       "Mỗi góp ý được ghi thành luật, áp dụng cho mọi phần sau." /
       "Nhân vật được vẽ lại, duyệt trên một bảng mẫu, rồi mới đưa vào video." /
       "Duyệt 31 giây đầu trước, rồi mới làm đủ 5 phút."

PHẦN 3 – Video thứ hai nhanh hơn nhờ kế thừa (~30s)
- Bước 8: tờ "Context TC" với bảng 2 cột "Hàng kho khô | Hàng TC"; các luật cũ (1.3×, ≥ 4 s,
  nhân vật v2) bay từ góc trên xuống gắn vào tờ giấy. 36 giây đầu → bản đầy đủ 2:12.
- Bước 9: deck 17 slide xòe ra như quạt.
- Lời: "Video thứ hai không phải bắt đầu lại." /
       "Tôi chỉ viết phần khác so với video trước, mọi luật cũ tự áp dụng." /
       "Cùng nội dung đó, tôi tạo thêm một bộ slide 17 trang."

PHẦN 4 – Đóng gói thành kỹ năng (~40s)
- Bước 10: file PDF bản vẽ quy trình CXAD → prompt v1 (nháp, chữ xám) → v2 (✔ đã xác nhận).
  Hiện 5 chip lấy từ chú giải bản vẽ: WMS · PDA · Thủ công · Chứng từ · Điều kiện.
  Quy trình "01A" bị gạch: "Việc của quản lý – bỏ".
- Bước 11: 8 vai đứng thành hàng, mỗi vai một hành động tại chỗ, không trùng nhau: nhận hàng bê thùng ·
  xe nâng nâng càng có thùng · điều phối gõ máy tính · quản lý kho cầm hồ sơ và chỉ tay giao việc ·
  picker kéo trolley · checker scan PDA · vận tải ký giấy giao · giảng viên vẫy tay.
  "Quản lý kho" (model-quan-ly.png) bước vào sau cùng, nhãn "MỚI" → cả hàng được bọc vào một hộp
  có nhãn "Skill: nhan-vat-kho (model v3)".
- Bước 12: ba khung v1 → v2 → v3 xếp chồng; mỗi lần sửa có 1 dòng:
  "Phụ đề quy đổi bằng số, nhãn to hơn" · "Ô điều kiện khớp mũi tên".
- Lời: "Video thứ ba bắt đầu từ bản vẽ quy trình." /
       "Cần thêm vai quản lý kho, tôi đóng gói cả bộ nhân vật thành một skill riêng." /
       "Từ nay, mọi video kho mới đều dùng lại bộ này, không vẽ lại." /
       "Mỗi lần sửa là một phiên bản mới, luôn quay lại được."

TỔNG KẾT (~25s)
- Hình: "Công thức" chạy như băng chuyền, từng ô sáng lần lượt:
  Nguồn → Prompt / Context → Outline duyệt → Chốt luật → Model sheet → 30 giây mẫu → Làm đủ → Render → v2, v3 → Đóng gói
- Thẻ "Ghi nhớ" 3 ý:
  • Duyệt sớm bằng thứ nhỏ
  • Góp ý nào cũng thành luật ghi lại
  • Cái gì dùng lại thì đóng gói thành skill
- Giảng viên giơ ngón cái.
- Lời: "Đó là công thức của tôi." /
       "Duyệt sớm, ghi lại luật, và đóng gói những gì dùng lại." /
       "Bạn hãy thử với quy trình của mình."
```

---

## [B2] SLIDE DECK – cùng nội dung (~12 slide, 16:9)

```
Tạo deck 16:9 theo phong cách [A]. Mỗi slide 1 ý, tiêu đề là một câu khẳng định, tối đa 4 dòng chữ,
luôn có hình (ảnh thật từ repo hoặc sơ đồ vẽ phẳng). Ghi chú người nói (speaker notes) = lời thoại ở [B1].

 1. Tiêu đề: "Từ một prompt đến một kỹ năng làm video" – 4 thumbnail sản phẩm, chip "2 ngày · 27 phiên bản".
 2. Kết quả: bảng 4 sản phẩm (tên · thời lượng / số slide · số phiên bản).
 3. Công cụ: Claude Code + 9 skill HyperFrames – "video là trang web được render thành MP4":
    HTML = cảnh, CSS = màu/font/bố cục, GSAP = chuyển động, trình duyệt chụp 30 khung/giây → MP4.
    Cốt lõi là frontend.
 4. Prompt gốc: sơ đồ 2 khối [A] Phong cách chung + [B] Kịch bản từng tập.
 5. Outline trước, dựng sau: ảnh chụp bảng thông số của OUTLINE.md.
 6. Góp ý thành luật: 4 luật sau Tập 1 (kèm công thức nhịp đọc 1.3×).
 7. Nhân vật được duyệt trên bảng mẫu: model-sheet-v2.png cạnh model-sheet-v3.png.
 8. Duyệt 30 giây trước, làm đủ sau: dòng thời gian 0:31 → 5:09 và 0:36 → 2:12.
 9. Video sau kế thừa video trước: bảng "Khác gì so với video trước" (trích Context TC / CXAD).
10. Đóng gói thành skill "nhan-vat-kho": 8 vai, màu, đạo cụ (bảng rút gọn từ SKILL.md).
11. Sửa theo phiên bản: CXAD v1 → v2 → v3, mỗi bản 1 dòng thay đổi + ảnh trước/sau.
12. Công thức + 5 bài học + lời mời "Thử với quy trình của bạn".
```

---

## Ghi chú khi dựng
- Không thêm số liệu ngoài phần "Dữ kiện thật"; nếu cần chi tiết, đọc lại `git log`, `PROGRESS.md`, `OUTLINE.md`.
- Storyboard đã duyệt: `design/storyboard-hanh-trinh.html` (dựng bằng `tools/build_storyboard_skill.py`).
- Gửi outline + 30 giây đầu (hoặc 3 slide đầu) để tôi duyệt trước khi làm đủ – đúng công thức của chính video này.
