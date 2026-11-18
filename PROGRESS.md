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
| Render bản đầy đủ | video-cxad/renders/quy-trinh-kho-cxad-full-v1.mp4 (5:20, 1080p) |
