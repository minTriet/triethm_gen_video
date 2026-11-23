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
| Render bản đầy đủ | v1: video-cxad/renders/quy-trinh-kho-cxad-full-v1.mp4 · v2 (phụ đề quy đổi bằng số, nhãn LPN + mã vị trí to hơn): quy-trinh-kho-cxad-full-v2.mp4 · v3 (ô điều kiện khớp mũi tên): quy-trinh-kho-cxad-full-v3.mp4 · v4 (dựng lại từ nhánh chính sau khi gộp PR #1): quy-trinh-kho-cxad-full-v4.mp4 · v5 (model mới: bàn tay tròn, Quản lý kho mũ trắng, bỏ giơ ngón cái): quy-trinh-kho-cxad-full-v5.mp4 |

# Video quy trình toàn kho CXAD (lấy hàng bằng giấy)

Nguồn: source/Context_Video_CXAD_Paper_Picking.md (v2, đã xác nhận) · Nhân vật: design/cxad-cast.png
Generator: `python3 tools/build_cxad_giay.py` → thư mục `video-cxad-giay/`.

| Phần | Trạng thái |
| --- | --- |
| Mở đầu + sơ đồ kho 3 khu + Chương 1 Bước 1–2 | xong (bản 34s đã duyệt) |
| Chương 1 Bước 3–11, Chương 2–4, Kết (tools/cxad_scenes.py) | xong |
| Check + render bản đầy đủ | v1: quy-trinh-kho-cxad-full-v1.mp4 · v2 (bản chốt, xử lý chênh lệch / sai lệch thủ công): video-cxad-giay/renders/quy-trinh-kho-cxad-full-v2.mp4 |

# Video CXAD bản giấy (nhập / cất / lấy hàng bằng giấy, PDA chỉ ở chia hàng và xác nhận lên xe)

Nguồn: source/Context_Video_CXAD_Paper_Full.md · Storyboard: design/cxad-giay-storyboard.pdf
Generator: `python3 tools/build_cxad_paper.py` → `video-cxad-paper/` · Render: v1 quy-trinh-kho-cxad-giay-v1.mp4 · v2 (bàn tay tròn) video-cxad-paper/renders/quy-trinh-kho-cxad-giay-v2.mp4 (5:10, 1080p)

# Video "Hành trình tạo kỹ năng làm video"

Nguồn: `source/Prompt_Video_Hanh_trinh_tao_skill_video.md` (v2) · Storyboard đã duyệt: `design/storyboard-hanh-trinh.html`
Giọng đọc: skill `vieneu-tts`, giọng Hải Đăng, seed 7. Câu thoại + văn bản đọc: `source/vo_hanh_trinh.json`
("Claude" đọc là "Cờ lốt", "MP4" đọc là "em pê bốn"; các từ tiếng Anh khác để nguyên vì đọc đúng hơn phiên âm).
Generator: `python3 tools/build_hanhtrinh.py` → `video-hanhtrinh/` (thời lượng câu = độ dài clip giọng đọc + 0.3 s).
Render: `cd video-hanhtrinh && node ../.claude/skills/hyperframes/scripts/plugin-cli.mjs render -o renders/<tên>.mp4`

| Phần | Trạng thái |
| --- | --- |
| Mở đầu + thẻ chương Phần 1 + Bước 1 + HyperFrames là gì (màn 01–04) | xong · bản duyệt `hanh-trinh-30s-v1.mp4` (model cũ), `hanh-trinh-30s-v2.mp4` (model mới) |
| Màn 05–17 (Bước 2–12, thẻ chương 2–4, công thức, Ghi nhớ) – `tools/hanhtrinh_scenes.py` | xong |
| Check + render bản đầy đủ | v1: `video-hanhtrinh/renders/hanh-trinh-full-v1.mp4` (2:13, 1080p, có giọng đọc) |

Ghi chú giọng đọc: câu c10-1 đọc "ba mươi mốt giây" và tạo với seed 11 (các câu khác seed 7).

# Video "Quy trình kho cơ bản với WMS"

Nguồn: `source/Prompt_Video_Quy_trinh_co_ban_WMS.md` (v1 nháp) — bám To-Be chuẩn 02C + 04C (Barcode mã hàng) của vault.
Storyboard: `design/storyboard-wms-co-ban.html` (`python3 tools/build_storyboard_wms.py design/storyboard-wms-co-ban.html`), 18 màn, khoảng 2:11.

| Phần | Trạng thái |
| --- | --- |
| Storyboard v1 | chờ duyệt (màn 03: dải nhãn chuyển lên trên, tránh phụ đề) |
| Bản duyệt 47 s đầu (màn 01–06: mở đầu, toàn cảnh, 3 vai, thẻ chương 1, Bước 1–2) | `video-wms/renders/wms-co-ban-duyet-v1.mp4` (1080p, chỉ phụ đề), chờ duyệt |
| Màn 07–18 + render bản đầy đủ | chưa làm |

Generator: `python3 tools/build_wms.py` → `video-wms/` (hình dùng chung với storyboard: `tools/wms_kit.py`).
Render: `cd video-wms && node ../.claude/skills/hyperframes/scripts/plugin-cli.mjs render -o renders/<tên>.mp4`

# Video demo đề xuất cho khách hàng Công ty Nhiêu Lộc (kho lạnh, WMS)

Nguồn: `source/Nhieu_Loc_-_Bo_quy_trinh_kho.drawio` (01A, 01B, 02B, 03B, 03C, 03D, 04C, 05B) · Người xem: cấp quản lý Nhiêu Lộc (đi kèm proposal).
Bối cảnh: kho đông lạnh 2 khu (Khu A kệ, 1 vị trí = 1 pallet; Khu B chất chồng), thịt đông lạnh đồng ký / đa ký, xuất chẵn pallet và theo thùng.
Storyboard: `design/storyboard-nhieu-loc.html` (`python3 tools/build_storyboard_nhieuloc.py design/storyboard-nhieu-loc.html`), 30 màn, khoảng 4:18.

| Phần | Trạng thái |
| --- | --- |
| Storyboard v3 (logo TKSolution nền trong suốt, model XLCT mới; sửa theo góp ý: S14 chỉ gợi ý ô B-02 không tầng; S22 đồng ký/đa ký đều xuất chẵn pallet hoặc theo thùng, chọn lô FEFO mặc định hoặc theo HSD còn lại > %; S23 xe nâng được lấy pallet khác cùng lô; S24 lấy theo thùng có quét LPN; mã lô đổi sang năm 2026) | chờ duyệt — đã chốt: WMS tự tách (đủ 1 pallet → chẵn pallet, không đủ → theo thùng); WMS cho đổi LPN cùng lô khi lấy |
| Bản duyệt 30 s đầu (S01–S03: tiêu đề, 2 khu kho, hàng hoá) có giọng đọc | `video-nhieuloc/renders/nhieu-loc-30s-v1.mp4` (35 s, 1080p), chờ duyệt |
| S04–S30 (`tools/nhieuloc_scenes.py`) + render bản đầy đủ | v1: `video-nhieuloc/renders/nhieu-loc-full-v1.mp4` (5:04, 1080p, giọng đọc 58 câu) · v2 (WMS đọc tiếng Anh "đúp bơ diu em ét"): `video-nhieuloc/renders/nhieu-loc-full-v2.mp4` |

Generator: `python3 tools/build_nhieuloc.py` → `video-nhieuloc/` (hình dùng chung với storyboard: `tools/nhieuloc_kit.py`).
Giọng đọc: skill `vieneu-tts`, giọng Hải Đăng, seed 7; câu thoại + văn bản đọc trong `source/vo_nhieu_loc.json`
("WMS" đọc "đúp bơ diu em ét", "pallet" viết "pa-lét", "kg" đọc "ký", "Khu A/B" viết "Khu a/bê").
Render: `cd video-nhieuloc && node ../.claude/skills/hyperframes/scripts/plugin-cli.mjs render -o renders/<tên>.mp4`
