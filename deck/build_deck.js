// Deck: Quy trình vận hành kho khô & hàng TC (built from source/*.md)
// Run: NODE_PATH=<dir with pptxgenjs, jszip> node deck/build_deck.js <skill_dir>
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = process.argv[2];
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));
const OUT = path.join(__dirname, "Quy_trinh_van_hanh_kho_kho_va_TC.pptx");

const THEME = {
  name: "Kho kho TC",
  headFontFace: "Calibri", bodyFontFace: "Calibri",
  colors: {
    dk1: "1B2430", lt1: "FFFFFF", dk2: "16478F", lt2: "F4F6F9",
    accent1: "1F5FBF", accent2: "F28C1E", accent3: "22A55A", accent4: "D93B3B",
    accent5: "BFD8F5", accent6: "6B7685", hlink: "1F5FBF", folHlink: "16478F",
  },
};
const HEX = THEME.colors;
const ROLE = { receiver: "2FAE5F", forklift: "F28C1E", planner: "1F5FBF", picker: "F4C430", checker: "8B5CF6", transport: "8C96A3" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "Quy trình vận hành kho khô và hàng TC";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const W = 13.333, M = 0.6;

// ---------------------------------------------------------------- layouts
pres.defineSlideMaster({
  title: "TITLE", background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.2, w: W - 2 * M, h: 1.6, fontSize: 44, bold: true, color: C.background1, valign: "bottom", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 3.95, w: W - 2 * M, h: 1.0, fontSize: 22, color: C.accent5, valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "SECTION", background: { color: C.accent1 },
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: M, y: 2.3, w: W - 2 * M, h: 0.6, fontSize: 20, bold: true, color: C.accent2 }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.9, w: W - 2 * M, h: 1.3, fontSize: 44, bold: true, color: C.background1, valign: "top", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 4.3, w: W - 2 * M, h: 0.9, fontSize: 20, color: C.accent5, valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "DARK", background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.55, w: W - 2 * M, h: 0.9, fontSize: 40, bold: true, color: C.background1, valign: "middle", margin: 0, align: "left" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT", background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.35, w: W - 2 * M, h: 0.8, fontSize: 34, bold: true, color: C.text1, valign: "middle", margin: 0, align: "left" }, text: "" } },
    { text: { text: "Vận hành kho khô & hàng TC", options: { x: M, y: 7.0, w: 6, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: W - M - 0.6, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: C.accent6, align: "right" },
});

// ---------------------------------------------------------------- helpers
let objN = 0;
const nm = (p) => `${p}-${++objN}`;
const T = (s, text, o) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, color: C.text1, fontSize: 14, valign: "top" }, o, { objectName: nm("txt") }));
const box = (s, o) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign({ rectRadius: 0.12, line: { color: C.accent5, width: 1 }, fill: { color: C.background1 } }, o, { objectName: nm("box") }));
const arrow = (s, x1, y1, x2, y2, color) => s.addShape(pres.shapes.LINE, {
  x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001,
  flipV: y2 < y1, line: { color: color || C.accent6, width: 2, endArrowType: "triangle" }, objectName: nm("arrow"),
});
const badge = (s, x, y, n, fill, txt) => {
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.5, h: 0.5, fill: { color: fill || C.accent2 }, line: { color: fill || C.accent2 }, objectName: nm("num") });
  T(s, String(n), { x, y, w: 0.5, h: 0.5, align: "center", valign: "middle", bold: true, fontSize: 16, color: txt || C.text1 });
};
// horizontal step flow: cards with number badge, arrows between
function stepRow(s, steps, x, y, w, h, opts = {}) {
  const gap = opts.gap ?? 0.35, n = steps.length, cw = (w - gap * (n - 1)) / n;
  steps.forEach((st, i) => {
    const cx = x + i * (cw + gap);
    box(s, { x: cx, y, w: cw, h, fill: { color: opts.fill || C.background2 }, line: { color: opts.line || C.accent5, width: 1 } });
    badge(s, cx + 0.15, y + 0.15, opts.start ? opts.start + i : i + 1, opts.badge, opts.badgeTxt);
    T(s, st[0], { x: cx + 0.15, y: y + 0.75, w: cw - 0.3, h: 0.7, bold: true, fontSize: opts.titleSize || 16 });
    if (st[1]) T(s, st[1], { x: cx + 0.15, y: y + 1.45, w: cw - 0.3, h: h - 1.55, fontSize: 14, color: C.text1 });
    if (i < n - 1) arrow(s, cx + cw + 0.05, y + h / 2, cx + cw + gap - 0.05, y + h / 2, C.accent1);
  });
}
// flow of short chips on one line
function chipFlow(s, items, x, y, w, h, colorFn) {
  const gap = 0.3, n = items.length, cw = (w - gap * (n - 1)) / n;
  items.forEach((t, i) => {
    const cx = x + i * (cw + gap), col = colorFn(i, t);
    box(s, { x: cx, y, w: cw, h, fill: { color: col.fill }, line: { color: col.line || col.fill, width: 1 } });
    T(s, t, { x: cx + 0.08, y, w: cw - 0.16, h, align: "center", valign: "middle", bold: true, fontSize: 14, color: col.text || C.text1 });
    if (i < n - 1) arrow(s, cx + cw + 0.03, y + h / 2, cx + cw + gap - 0.03, y + h / 2, C.accent6);
  });
}
function card(s, x, y, w, h, title, body, opts = {}) {
  box(s, { x, y, w, h, fill: { color: opts.fill || C.background2 }, line: { color: opts.line || C.accent5, width: opts.lineW || 1 } });
  T(s, title, { x: x + 0.25, y: y + 0.2, w: w - 0.5, h: 0.45, bold: true, fontSize: 17, color: opts.titleColor || C.text1 });
  if (body) T(s, body, { x: x + 0.25, y: y + 0.7, w: w - 0.5, h: h - 0.85, fontSize: 14 });
}
const bullets = (arr) => arr.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < arr.length - 1, paraSpaceAfter: 12 } }));
const content = (sec, title) => { const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: sec }); s.addText(title, { placeholder: "title" }); return s; };
const section = (sec, kicker, title, body) => {
  pres.addSection({ title: sec });
  const s = pres.addSlide({ masterName: "SECTION", sectionTitle: sec });
  s.addText(kicker, { placeholder: "kicker" }); s.addText(title, { placeholder: "title" }); if (body) s.addText(body, { placeholder: "body" });
  return s;
};

// ================================================================ 1. Title
pres.addSection({ title: "Mở đầu" });
let s = pres.addSlide({ masterName: "TITLE", sectionTitle: "Mở đầu" });
s.addText("Quy trình vận hành kho khô và hàng TC", { placeholder: "title" });
s.addText("Tài liệu giới thiệu cho nhân viên mới làm quen với WMS", { placeholder: "body" });
s.addNotes("Giới thiệu tổng quan hai luồng: hàng kho khô (có lưu kho) và hàng TC – trung chuyển (không lưu kho, giống cross dock).");

// ================================================================ 2. Overview
s = content("Mở đầu", "Hai luồng hàng trong kho");
T(s, "Hàng kho khô – có lưu kho", { x: M, y: 1.45, w: 6, h: 0.4, bold: true, fontSize: 18, color: C.accent1 });
chipFlow(s, ["Nhập hàng", "Cất hàng", "Gom tuyến & Allocate", "Châm hàng", "Pick", "Kiểm hàng", "Bàn giao"], M, 1.95, W - 2 * M, 0.85,
  () => ({ fill: C.background2, line: C.accent5 }));
T(s, "Hàng TC (trung chuyển) – không lưu kho, giống cross dock", { x: M, y: 3.2, w: 9, h: 0.4, bold: true, fontSize: 18, color: C.accent2 });
chipFlow(s, ["Nhận hàng (không LPN)", "Khu TC", "Chia theo DO", "Gom & Bàn giao"], M, 3.7, 7.6, 0.85,
  (i) => ({ fill: i === 1 || i === 2 ? C.accent2 : C.background2, line: i === 1 || i === 2 ? C.accent2 : C.accent5 }));
T(s, "Các vai trò trong quy trình", { x: M, y: 4.95, w: 6, h: 0.4, bold: true, fontSize: 18 });
const roles = [["Nhân viên nhận hàng", ROLE.receiver], ["Tài xế xe nâng", ROLE.forklift], ["Nhân viên điều phối", ROLE.planner],
  ["Picker", ROLE.picker], ["Checker", ROLE.checker], ["Đội vận tải", ROLE.transport]];
roles.forEach(([r, col], i) => {
  const x = M + (i % 3) * 4.1, y = 5.45 + Math.floor(i / 3) * 0.65;
  s.addShape(pres.shapes.OVAL, { x, y: y + 0.08, w: 0.34, h: 0.34, fill: { color: col }, line: { color: HEX.dk1, width: 1 }, objectName: nm("role") });
  T(s, r, { x: x + 0.5, y, w: 3.4, h: 0.5, valign: "middle", fontSize: 15, bold: true });
});
s.addNotes("Màu chấm tròn = màu áo/mũ bảo hộ của từng vai trong video training.");

// ================================================================ A. Kho khô
section("Kho khô", "PHẦN A", "Vận hành kho khô", "Nhập hàng → Cất hàng → Đơn hàng & Allocate → Châm hàng → Pick → Kiểm hàng → Bàn giao");

// ---- A1 layout
s = content("Kho khô", "Sơ đồ kho: Reserved và Primary");
// rack diagram
const rx = M, ry = 1.5, rw = 5.2, lh = 1.15;
[["RESERVED – Lưu kho", C.accent5], ["RESERVED – Lưu kho", C.accent5], ["PRIMARY – Pick face", C.accent2]].forEach(([t, col], i) => {
  box(s, { x: rx, y: ry + i * (lh + 0.12), w: rw, h: lh, fill: { color: col }, line: { color: C.text1, width: 1.5 }, rectRadius: 0.06 });
  T(s, t, { x: rx + 0.25, y: ry + i * (lh + 0.12), w: rw - 0.5, h: lh, valign: "middle", bold: true, fontSize: 18 });
});
T(s, "Tầng trên cao", { x: rx, y: ry + 3 * (lh + 0.12) + 0.05, w: 2.5, h: 0.35, fontSize: 12, color: C.accent6 });
T(s, "Tầng sát mặt đất = nơi lấy hàng", { x: rx + 2.5, y: ry + 3 * (lh + 0.12) + 0.05, w: 2.7, h: 0.35, fontSize: 12, color: C.accent6, align: "right" });
card(s, 6.4, 1.5, 6.33, 1.2, "1 vị trí pick face = 1 mã hàng cố định", "Mỗi vị trí Primary chỉ chứa một mã hàng duy nhất, và mã đó luôn cố định tại vị trí ấy.", { fill: C.background1, line: C.accent2, lineW: 2 });
card(s, 6.4, 2.95, 6.33, 1.25, "Reserved = lưu trữ", "Các tầng trên dùng để lưu hàng; hàng được châm xuống Primary khi thiếu.");
T(s, "Mỗi dãy kệ dành cho một ngành hàng", { x: 6.4, y: 4.5, w: 6.3, h: 0.4, bold: true, fontSize: 17 });
["Nước uống", "Mì", "Snack", "Sữa"].forEach((t, i) => {
  box(s, { x: 6.4 + i * 1.6, y: 5.0, w: 1.45, h: 0.75, fill: { color: C.accent1 }, line: { color: C.accent1 } });
  T(s, "Dãy " + t, { x: 6.4 + i * 1.6, y: 5.0, w: 1.45, h: 0.75, align: "center", valign: "middle", bold: true, fontSize: 14, color: C.background1 });
});
s.addNotes("Allocate chỉ lấy hàng ở Primary. Reserved là nguồn để châm hàng.");

// ---- A2 receiving
s = content("Kho khô", "Nhập hàng: 5 bước trên PDA");
T(s, "Xe hàng về → nhân viên nhận hàng chất hàng lên pallet → mỗi pallet dán 1 mã LPN để định danh", { x: M, y: 1.3, w: W - 2 * M, h: 0.45, fontSize: 16, color: C.accent6 });
stepRow(s, [["Chọn phiếu ASN", "Phiếu của xe đang nhập"], ["Scan LPN", "Nhãn trên pallet"], ["Scan mã hàng", "Mã hàng trên pallet"],
  ["Nhập số thùng", "Số thùng thực nhận"], ["Batch / Lot / Ngày", "Theo yêu cầu của mã hàng"]], M, 1.95, W - 2 * M, 2.15);
T(s, "Yêu cầu nhập ngày khác nhau theo mã hàng – PDA chỉ hiện đúng ô cần nhập", { x: M, y: 4.4, w: W - 2 * M, h: 0.4, bold: true, fontSize: 17 });
[["Mã hàng A", "Chỉ nhập ngày sản xuất (NSX)"], ["Mã hàng B", "Chỉ nhập hạn sử dụng (HSD)"], ["Mã hàng C", "Không nhập ngày"]].forEach(([a, b], i) => {
  card(s, M + i * 4.1, 4.9, 3.85, 1.15, a, b);
});
box(s, { x: M, y: 6.25, w: W - 2 * M, h: 0.55, fill: { color: C.accent5 }, line: { color: C.accent5 } });
T(s, "Lặp lại các bước cho đến khi nhận đủ toàn bộ phiếu ASN", { x: M + 0.25, y: 6.25, w: W - 2 * M - 0.5, h: 0.55, valign: "middle", bold: true, fontSize: 15 });

// ---- A3 putaway
s = content("Kho khô", "Cất hàng (Putaway)");
stepRow(s, [["Scan LPN", "Tài xế xe nâng scan nhãn LPN của pallet"],
  ["Hệ thống chỉ vị trí", "Dựa vào mã hàng trên pallet, chỉ đến vị trí Primary cố định của mã đó"],
  ["Đặt pallet", "Xe nâng đặt pallet phía trên hoặc gần vị trí Primary này"],
  ["Scan vị trí xác nhận", "Scan mã vị trí → hệ thống ghi nhận \"Đã cất hàng\""]], M, 1.5, W - 2 * M, 2.9);
card(s, M, 4.8, 6.0, 1.6, "Vai trò", "Tài xế xe nâng (áo cam) thực hiện toàn bộ bước cất hàng.");
card(s, 6.73, 4.8, 6.0, 1.6, "Ví dụ", "PDA: \"Vị trí đề xuất: A-01-01 (Primary)\" → pallet đặt ở A-01-02 ngay phía trên → scan A-01-02 để xác nhận", { fill: C.background1, line: C.accent2, lineW: 2 });

// ---- A4 orders & allocate
s = content("Kho khô", "Đơn hàng, gom tuyến và Allocate");
stepRow(s, [["Cửa hàng gửi DO", "Mỗi ngày, các cửa hàng tự động đặt hàng và gửi DO lên hệ thống"],
  ["Gom DO theo tuyến", "Nhân viên điều phối gom DO theo tuyến đường, đánh số Tuyến 1 → n"],
  ["Bấm Allocate", "Hệ thống phân bổ tồn kho cho đơn"],
  ["Chỉ lấy ở Primary", "Allocate chỉ lấy hàng ở vị trí Primary, không pick ở Reserved"]], M, 1.5, W - 2 * M, 2.6);
card(s, M, 4.5, 6.0, 1.9, "Số tuyến = thứ tự xuất hàng", "Tuyến 1 xuất trước, Tuyến n xuất sau. Đánh số đúng theo thứ tự xuất hàng của tuyến.", { fill: C.background1, line: C.accent2, lineW: 2 });
card(s, 6.73, 4.5, 6.0, 1.9, "Nếu tồn Primary không đủ", "Hệ thống tạo lệnh châm hàng: đưa hàng từ Reserved xuống Primary.\nVí dụ: cần 10 thùng – có 4 thùng.");

// ---- A5 replenishment
s = content("Kho khô", "Châm hàng (Replenishment)");
T(s, "Kích hoạt khi tồn tại vị trí Primary không đủ cho đơn đã Allocate", { x: M, y: 1.3, w: W - 2 * M, h: 0.45, fontSize: 16, color: C.accent6 });
stepRow(s, [["Xem lệnh", "Tài xế xe nâng xem lệnh châm hàng trên PDA"],
  ["Đến Reserved, scan LPN", "Đến đúng vị trí Reserved trong lệnh, scan LPN pallet"],
  ["Mang xuống Primary", "Đưa hàng xuống vị trí pick face"],
  ["Scan vị trí pick face", "Xác nhận đã châm → vị trí đủ hàng"]], M, 1.95, W - 2 * M, 2.6);
box(s, { x: M, y: 4.95, w: W - 2 * M, h: 1.3, fill: { color: C.background2 }, line: { color: C.accent5 } });
chipFlow(s, ["Reserved A-01-03", "Xe nâng", "Primary A-01-01", "Đủ hàng"], M + 0.4, 5.2, W - 2 * M - 0.8, 0.8,
  (i) => i === 0 ? { fill: C.accent5 } : i === 2 ? { fill: C.accent2 } : i === 3 ? { fill: C.accent3, text: C.background1 } : { fill: C.background1, line: C.accent6 });

// ---- A6 picking
s = content("Kho khô", "Pick hàng: chẵn thùng và hàng lẻ");
const colW = (W - 2 * M - 0.4) / 2;
[[M, "Hàng chẵn thùng", "Kéo trolley dán mã cửa hàng, làm từng đơn",
  [["Đến vị trí", "Vị trí hiện trên PDA"], ["Scan mã sản phẩm", "PDA báo số lượng cần lấy → xác nhận → đặt lên trolley"]], "Chỉ 2 bước – tiết kiệm thời gian, vì mỗi vị trí chỉ có 1 mã hàng"],
 [M + colW + 0.4, "Hàng lẻ", "Mang thùng xanh Oricon dán mã cửa hàng",
  [["Đến vị trí", ""], ["Scan mã hàng", ""], ["Nhập số lượng", ""], ["Bỏ vào Oricon", ""]], null]].forEach(([x, t, sub, steps, note]) => {
  T(s, t, { x, y: 1.35, w: colW, h: 0.45, bold: true, fontSize: 20, color: C.accent1 });
  T(s, sub, { x, y: 1.8, w: colW, h: 0.4, fontSize: 15, color: C.accent6 });
  steps.forEach(([a, b], i) => {
    const y = 2.4 + i * (steps.length === 2 ? 1.25 : 0.82), h = steps.length === 2 ? 1.1 : 0.68;
    box(s, { x, y, w: colW, h, fill: { color: C.background2 }, line: { color: C.accent5 } });
    badge(s, x + 0.15, y + (h - 0.5) / 2, i + 1);
    T(s, a, { x: x + 0.8, y: y + (b ? 0.12 : 0), w: colW - 1, h: b ? 0.4 : h, valign: b ? "top" : "middle", bold: true, fontSize: 16 });
    if (b) T(s, b, { x: x + 0.8, y: y + 0.52, w: colW - 1, h: 0.5, fontSize: 14 });
  });
  if (note) { box(s, { x, y: 5.0, w: colW, h: 0.65, fill: { color: C.accent2 }, line: { color: C.accent2 } }); T(s, note, { x: x + 0.2, y: 5.0, w: colW - 0.4, h: 0.65, valign: "middle", bold: true, fontSize: 14 }); }
});
box(s, { x: M, y: 6.05, w: W - 2 * M, h: 0.6, fill: { color: C.accent5 }, line: { color: C.accent5 } });
T(s, "Luôn làm xong trọn từng đơn", { x: M + 0.25, y: 6.05, w: 8, h: 0.6, valign: "middle", bold: true, fontSize: 16 });

// ---- A7 checking
s = content("Kho khô", "Kiểm hàng trước khi ra kho");
[[M, "Hàng thùng – kiểm trên trolley", "Nhóm checker đi kiểm từng đơn",
  [["Chọn đúng cửa hàng", "Khớp với mã trên trolley"], ["Scan mã hàng", ""], ["Đếm và nhập số lượng", "Biết đã pick đủ hay chưa (Đủ / Thiếu)"]]],
 [M + colW + 0.4, "Hàng lẻ – kiểm tại khu đóng gói", "Picker mang Oricon ra khu đóng gói",
  [["Scan mã hàng", "Checker kiểm hàng bên trong"], ["Nhập số lượng", ""], ["Niêm phong thùng", "Seal sau khi kiểm xong"]]]].forEach(([x, t, sub, steps]) => {
  T(s, t, { x, y: 1.35, w: colW, h: 0.45, bold: true, fontSize: 20, color: C.accent1 });
  T(s, sub, { x, y: 1.8, w: colW, h: 0.4, fontSize: 15, color: C.accent6 });
  steps.forEach(([a, b], i) => {
    const y = 2.4 + i * 1.3, h = 1.12;
    box(s, { x, y, w: colW, h, fill: { color: C.background2 }, line: { color: C.accent5 } });
    badge(s, x + 0.15, y + 0.31, i + 1, ROLE.checker, C.background1);
    T(s, a, { x: x + 0.8, y: y + (b ? 0.15 : 0), w: colW - 1, h: b ? 0.4 : h, valign: b ? "top" : "middle", bold: true, fontSize: 16 });
    if (b) T(s, b, { x: x + 0.8, y: y + 0.57, w: colW - 1, h: 0.45, fontSize: 14 });
  });
});

// ---- A8 handover
s = content("Kho khô", "Bàn giao cho vận tải");
box(s, { x: M, y: 1.5, w: W - 2 * M, h: 1.3, fill: { color: C.text2 }, line: { color: C.text2 } });
T(s, "Khuya", { x: M + 0.4, y: 1.5, w: 3, h: 1.3, valign: "middle", bold: true, fontSize: 26, color: C.background1 });
arrow(s, M + 2.2, 2.15, W - M - 3.2, 2.15, C.accent5);
T(s, "Rạng sáng", { x: W - M - 3.0, y: 1.5, w: 2.7, h: 1.3, valign: "middle", align: "right", bold: true, fontSize: 26, color: C.accent2 });
[["Chỉ đội vận tải làm việc", "Bàn giao diễn ra từ khuya đến rạng sáng"],
 ["Xác nhận bàn giao trên hệ thống", "Đội vận tải bấm xác nhận → hàng \"Đã ra kho\""],
 ["Không kiểm đếm lại số lượng", "Số lượng đã được checker kiểm trước đó"]].forEach(([a, b], i) => {
  card(s, M + i * 4.1, 3.2, 3.85, 2.0, a, b, i === 2 ? { fill: C.background1, line: C.accent4, lineW: 2 } : {});
});
T(s, "Toàn bộ quy trình: Nhập hàng → Cất hàng → Gom tuyến & Allocate → Châm hàng → Pick → Kiểm hàng → Bàn giao", { x: M, y: 5.6, w: W - 2 * M, h: 0.5, fontSize: 15, color: C.accent6 });

// ================================================================ B. Hàng TC
section("Hàng TC", "PHẦN B", "Vận hành hàng TC (trung chuyển)", "Hàng nhập vào không lưu kho, mà được chia ngay cho các cửa hàng – giống cross dock");

// ---- B1 comparison
s = content("Hàng TC", "Hàng TC khác hàng kho khô thế nào");
s.addTable([
  [{ text: "", options: { fill: { color: C.background1 } } },
   { text: "Hàng kho khô thường", options: { bold: true, color: C.background1, fill: { color: C.accent1 } } },
   { text: "Hàng TC", options: { bold: true, color: C.text1, fill: { color: C.accent2 } } }],
  [{ text: "Nhận hàng", options: { bold: true } }, "Dán + scan LPN cho từng pallet; nhập batch / lot / ngày theo mã", "Không LPN, không batch / lot / ngày – nhập thẳng số lượng"],
  [{ text: "Sau khi nhận", options: { bold: true } }, "Cất lên kệ (Primary / Reserved)", "Đưa vào khu TC, không cất lên kệ"],
  [{ text: "Xuất hàng", options: { bold: true } }, "Allocate → châm hàng (nếu thiếu) → pick từ pick face", "Chia hàng vừa nhập vào vị trí TC của từng cửa hàng theo DO"],
  [{ text: "Tồn kho", options: { bold: true } }, "Có lưu kho", "Không lưu kho – nhập bao nhiêu chia bấy nhiêu"],
], { x: M, y: 1.5, w: W - 2 * M, colW: [2.2, 4.97, 4.96], fontSize: 15, color: C.text1, valign: "middle",
  border: { type: "solid", pt: 1, color: HEX.accent5 }, fill: { color: HEX.lt2 }, rowH: [0.6, 0.95, 0.8, 0.95, 0.8], margin: 0.12, objectName: nm("table") });

// ---- B2 receiving TC
s = content("Hàng TC", "Nhận hàng TC: 3 bước trên PDA");
T(s, "Xe hàng TC về kho → nhân viên nhận hàng dỡ hàng xuống (không dán LPN)", { x: M, y: 1.3, w: W - 2 * M, h: 0.45, fontSize: 16, color: C.accent6 });
stepRow(s, [["Chọn phiếu ASN (TC)", "Phiếu của xe hàng TC"], ["Scan mã hàng", ""], ["Nhập thẳng số lượng", "Số lượng thực nhận"]], M, 1.95, 8.2, 2.2);
card(s, 9.2, 1.95, 3.53, 2.2, "Sau khi nhận", "Mang vào khu TC trong kho, không cất lên kệ.", { fill: C.background1, line: C.accent2, lineW: 2 });
[["Không dùng LPN", C.accent4], ["Không nhập batch / lot / ngày", C.accent4], ["Chỉ nhận đủ hoặc thiếu – không nhận dư", C.accent4]].forEach(([t, col], i) => {
  box(s, { x: M + i * 4.1, y: 4.6, w: 3.85, h: 1.0, fill: { color: C.background1 }, line: { color: col, width: 2 } });
  T(s, t, { x: M + i * 4.1 + 0.2, y: 4.6, w: 3.45, h: 1.0, valign: "middle", align: "center", bold: true, fontSize: 16 });
});
T(s, "Ví dụ: phiếu 100 thùng → nhập 110 bị PDA báo \"Không nhận dư\"; nhập ít hơn 100 = nhận thiếu.", { x: M, y: 5.9, w: W - 2 * M, h: 0.45, fontSize: 15, color: C.accent6 });

// ---- B3 sorting
s = content("Hàng TC", "Xuất hàng TC: chia cho cửa hàng theo DO");
T(s, "DO của các cửa hàng đã có sẵn số lượng cần – hệ thống dùng chính hàng TC vừa nhập để chia", { x: M, y: 1.3, w: W - 2 * M, h: 0.45, fontSize: 16, color: C.accent6 });
stepRow(s, [["Scan mã hàng", "Tại khu TC"], ["Xem cửa hàng & số lượng", "PDA hiện cửa hàng và số lượng cần chia"],
  ["Scan mã cửa hàng", "Đến vị trí riêng của cửa hàng đó"], ["Đặt hàng, xác nhận", "Đặt đúng số lượng rồi xác nhận"]], M, 1.95, W - 2 * M, 2.15);
card(s, M, 4.45, 6.0, 1.95, "Khu TC", "Mỗi cửa hàng có một vị trí riêng.\nVị trí chỉ dán mã cửa hàng để scan khi chia – không có mã vị trí.", { fill: C.background1, line: C.accent2, lineW: 2 });
T(s, "Ví dụ: nhận 100 thùng SKU 5001", { x: 6.73, y: 4.45, w: 6, h: 0.4, bold: true, fontSize: 16 });
[["CH-0125", "30"], ["CH-0311", "45"], ["CH-0420", "25"], ["Tồn TC", "0"]].forEach(([a, b], i) => {
  const x = 6.73 + i * 1.52, last = i === 3;
  box(s, { x, y: 4.95, w: 1.38, h: 1.45, fill: { color: last ? C.accent3 : C.background2 }, line: { color: last ? C.accent3 : C.accent5 } });
  T(s, b, { x, y: 5.02, w: 1.38, h: 0.75, align: "center", valign: "middle", bold: true, fontSize: 30, color: last ? C.background1 : C.text1 });
  T(s, a, { x, y: 5.8, w: 1.38, h: 0.45, align: "center", fontSize: 14, bold: true, color: last ? C.background1 : C.text1 });
});

// ---- B4 short receipt + handover
s = content("Hàng TC", "Khi nhận thiếu và khi bàn giao");
T(s, "Nhận thiếu: phân bổ từ trên xuống", { x: M, y: 1.35, w: 6, h: 0.45, bold: true, fontSize: 20, color: C.accent1 });
T(s, "Ví dụ: chỉ nhận 75 / 100 thùng", { x: M, y: 1.8, w: 6, h: 0.4, fontSize: 15, color: C.accent6 });
s.addTable([
  [{ text: "Thứ tự", options: { bold: true } }, { text: "Cửa hàng", options: { bold: true } }, { text: "Cần", options: { bold: true } }, { text: "Được chia", options: { bold: true } }],
  ["1", "CH-0125", "30", { text: "30 – đủ", options: { color: C.accent3, bold: true } }],
  ["2", "CH-0311", "45", { text: "45 – đủ", options: { color: C.accent3, bold: true } }],
  ["3", "CH-0420", "25", { text: "0 – không có hàng", options: { color: C.accent4, bold: true } }],
], { x: M, y: 2.35, w: 6.0, colW: [1.0, 1.6, 1.0, 2.4], fontSize: 15, color: C.text1, valign: "middle", rowH: 0.62,
  border: { type: "solid", pt: 1, color: HEX.accent5 }, fill: { color: HEX.lt2 }, margin: 0.1, objectName: nm("table") });
T(s, "Cửa hàng phía trên nhận đủ; cửa hàng phía dưới có thể không có hàng.", { x: M, y: 5.0, w: 6, h: 0.7, fontSize: 15 });
T(s, "Bàn giao: gom từ 3 nguồn của từng cửa hàng", { x: 6.95, y: 1.35, w: 5.8, h: 0.45, bold: true, fontSize: 20, color: C.accent1 });
[["Hàng chẵn", "Trolley theo mã cửa hàng"], ["Hàng lẻ", "Oricon theo mã cửa hàng"], ["Vị trí TC", "Hàng TC đã chia cho cửa hàng"]].forEach(([a, b], i) => {
  const y = 2.0 + i * 1.05;
  box(s, { x: 6.95, y, w: 3.4, h: 0.9, fill: { color: C.background2 }, line: { color: C.accent5 } });
  T(s, a, { x: 7.15, y: y + 0.08, w: 3.0, h: 0.4, bold: true, fontSize: 16 });
  T(s, b, { x: 7.15, y: y + 0.46, w: 3.0, h: 0.4, fontSize: 13, color: C.accent6 });
  arrow(s, 10.4, y + 0.45, 11.0, 3.05, C.accent2);
});
box(s, { x: 11.05, y: 2.55, w: 1.68, h: 1.0, fill: { color: C.accent1 }, line: { color: C.accent1 } });
T(s, "Bàn giao vận tải", { x: 11.1, y: 2.55, w: 1.58, h: 1.0, align: "center", valign: "middle", bold: true, fontSize: 15, color: C.background1 });
T(s, "Kiểm hàng và bàn giao như hàng thông thường.", { x: 6.95, y: 5.3, w: 5.8, h: 0.5, fontSize: 15 });

// ================================================================ Ghi nhớ
pres.addSection({ title: "Ghi nhớ" });
s = pres.addSlide({ masterName: "DARK", sectionTitle: "Ghi nhớ" });
s.addText("Ghi nhớ", { placeholder: "title" });
[[M, "Kho khô", ["Trên cao = Reserved (lưu kho); mặt đất = Primary (pick face)", "1 vị trí pick face = 1 mã hàng cố định", "Mỗi pallet = 1 LPN; nhập ngày theo đúng yêu cầu từng mã", "Gom DO theo tuyến – số tuyến = thứ tự xuất", "Allocate chỉ lấy ở Primary; thiếu tồn → châm từ Reserved", "Pick chẵn thùng chỉ 2 bước; luôn làm xong trọn từng đơn"]],
 [6.85, "Hàng TC", ["Không LPN, không batch / lot / ngày", "Nhập thẳng số lượng – chỉ nhận đủ hoặc thiếu, không nhận dư", "Để tại khu TC, không cất lên kệ", "Chia theo DO: scan mã hàng → scan mã cửa hàng → đặt hàng, xác nhận", "Nhận thiếu: phân bổ từ trên xuống", "Bàn giao: gom hàng chẵn + hàng lẻ + vị trí TC"]]].forEach(([x, t, items]) => {
  box(s, { x, y: 1.75, w: 5.88, h: 4.9, fill: { color: C.background1 }, line: { color: C.background1 } });
  T(s, t, { x: x + 0.3, y: 1.95, w: 5.3, h: 0.5, bold: true, fontSize: 22, color: x === M ? C.accent1 : C.accent2 });
  T(s, bullets(items), { x: x + 0.3, y: 2.65, w: 5.3, h: 3.85, fontSize: 17 });
});

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log(OUT);
})();
