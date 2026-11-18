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

# Video quy trình toàn kho CXAD (lấy hàng bằng giấy)

Nguồn: source/Context_Video_CXAD_Paper_Picking.md (v2, đã xác nhận) · Nhân vật: design/cxad-cast.png
Generator: `python3 tools/build_cxad.py` → thư mục `video-cxad/`.

| Phần | Trạng thái |
| --- | --- |
| Mở đầu + sơ đồ kho 3 khu + Chương 1 Bước 1–2 | xong (bản 34s đã duyệt) |
| Chương 1 Bước 3–11, Chương 2–4, Kết (tools/cxad_scenes.py) | xong |
| Check + render bản đầy đủ | v1: quy-trinh-kho-cxad-full-v1.mp4 · v2 (bản chốt, xử lý chênh lệch / sai lệch thủ công): video-cxad/renders/quy-trinh-kho-cxad-full-v2.mp4 |

# Video CXAD bản giấy (nhập / cất / lấy hàng bằng giấy, PDA chỉ ở chia hàng và xác nhận lên xe)

Nguồn: source/Context_Video_CXAD_Paper_Full.md · Storyboard: design/cxad-giay-storyboard.pdf
Generator: `python3 tools/build_cxad_paper.py` → `video-cxad-paper/` · Render: v1 quy-trinh-kho-cxad-giay-v1.mp4 · v2 (bàn tay tròn) video-cxad-paper/renders/quy-trinh-kho-cxad-giay-v2.mp4 (5:10, 1080p)
