# Tiến độ video training (gộp 1 video)

Nguồn: Prompt_Video_Training_Kho_Kho.md (đã chép vào `source/`) · Quyết định: OUTLINE.md §4–5 · Nhân vật: design/model-sheet-v2.png (đã duyệt)
Bản 30s đầu: đã duyệt (video/renders/video-30s-v1.mp4).

Generator: `python3 tools/build_full.py` → thư mục `video/`. Render: `cd video && node ../.claude/skills/hyperframes/scripts/plugin-cli.mjs render -o renders/<tên>.mp4`

| Phần | Trạng thái |
| --- | --- |
| Khung dựng (timeline theo phụ đề, chapter, Ghi nhớ, captions, sfx ≥4s) | xong |
| Phần 1 – Tổng quan kho | xong |
| Phần 2 – Nhập hàng & Cất hàng | xong (tools/parts.py) |
| Phần 3 – Đơn hàng, Allocate & Châm hàng | xong |
| Phần 4 – Pick chẵn & lẻ | xong |
| Phần 5 – Kiểm hàng & Bàn giao + Tổng kết | xong |
| Check + review + render bản đầy đủ | xong: video/renders/van-hanh-kho-kho-full-v1.mp4 (5:09, 1080p) |

## Đối chiếu với file gốc
Mọi cảnh, bước, nhãn và câu thoại (dùng nguyên văn làm phụ đề) của Tập 1–5 đều có trong video.
Khác biệt có chủ đích: gộp 1 video, thẻ chương thay màn mở/kết từng tập; không giọng đọc; nhịp đọc 1.3×;
sound effect thưa (≥ 4 s); mã hàng/vị trí/cửa hàng/số lượng là minh họa.

# Video quy trình toàn kho CXAD

Nguồn: `source/Prompt_Video_Quy_trinh_toan_kho_CXAD.md` (v2, đã xác nhận) · Nhân vật: skill `nhan-vat-kho` (model v3)
Generator: `python3 tools/build_cxad.py` (Phần 2–4 + kết trong `tools/build_cxad_2.py`, thành phần dùng chung `tools/cxad_kit.py`) → thư mục `video-cxad/`.
Render: `cd video-cxad && node ../.claude/skills/hyperframes/scripts/plugin-cli.mjs render -o renders/<tên>.mp4`

| Phần | Trạng thái |
| --- | --- |
| Mở đầu + 3 khu (đông / chill / khô) | xong |
| Phần 1 – Nhập & Putaway (02F, bước 1–11) | xong |
| Phần 2 – Lấy hàng gộp theo xe (04K.1, bước 1–9) | xong |
| Phần 3 – Chia hàng theo DO (04K.2, bước 1–3) | xong |
| Phần 4 – Kiểm & Bàn giao (04K.3, bước 1–5) + kết | xong |
| Check | qua (0 lỗi) |
| Render bản đầy đủ | v1: video-cxad/renders/quy-trinh-kho-cxad-full-v1.mp4 · v2 (phụ đề quy đổi bằng số, nhãn LPN + mã vị trí to hơn): quy-trinh-kho-cxad-full-v2.mp4 · v3 (ô điều kiện khớp mũi tên): quy-trinh-kho-cxad-full-v3.mp4 |

# Video "Hành trình tạo kỹ năng làm video"

Nguồn: `source/Prompt_Video_Hanh_trinh_tao_skill_video.md` (v2) · Storyboard đã duyệt: `design/storyboard-hanh-trinh.html`
Giọng đọc: skill `vieneu-tts`, giọng Hải Đăng, seed 7. Câu thoại + văn bản đọc: `source/vo_hanh_trinh_30s.json`
("Claude" đọc là "Cờ lốt", "MP4" đọc là "em pê bốn"; các từ tiếng Anh khác để nguyên vì đọc đúng hơn phiên âm).
Generator: `python3 tools/build_hanhtrinh.py` → `video-hanhtrinh/` (thời lượng câu = độ dài clip giọng đọc + 0.3 s).
Render: `cd video-hanhtrinh && node ../.claude/skills/hyperframes/scripts/plugin-cli.mjs render -o renders/<tên>.mp4`

| Phần | Trạng thái |
| --- | --- |
| Mở đầu + thẻ chương Phần 1 + Bước 1 + HyperFrames là gì (màn 01–04) | render để duyệt: `video-hanhtrinh/renders/hanh-trinh-30s-v1.mp4` (0:36) |
| Màn 05–17 | chờ duyệt bản 30 giây đầu |
