# BẮT ĐẦU TỪ ĐÂY
**Cập nhật:** 2026-08-20

---

## Đọc hai file này, theo thứ tự

1. **`CLAUDE.md`** — cách làm việc, rule không được vi phạm, trạng thái dự án
2. **`docs/HANDOFF.md`** — 👈 **file chính.** Việc kế tiếp, cấu trúc theme, mọi quyết định đã chốt, fact brand, thứ đang chặn, bản đồ tài liệu

Mọi thứ khác đều được `HANDOFF.md` trỏ tới.

---

## Muốn xem giao diện ngay, không cần server

Mở `deliverables/preview/static-preview.html` — bấm đúp là chạy.

8 màn hình dựng bằng đúng `style.css` của theme và ảnh thật.
Hero 3 slide **chạy thật** trong đó. Rê chuột lên thẻ sản phẩm để thấy đổi mặt sau + nút chọn size.

---

## Việc kế tiếp — tóm tắt

```
1. Gỡ 96MB video master khỏi thư mục theme   ← 5 phút, BẮT BUỘC trước khi nén
2. Nén → upload cPanel song song → đổi theme → xem thử
3. Cấu hình WordPress cơ bản
4. Polylang                                   ← CHẶN việc nhập sản phẩm
5. Nhập 2 sản phẩm test → kiểm toàn bộ luồng
```

Chi tiết: `deliverables/setup/DEPLOY.md`

---

## Ba thứ đang chặn — cần user trả lời

1. 🔴 **Phí + hãng + thời gian ship quốc tế** — chặn multi-currency, shipping zone, trang Shipping, và thực tế chặn cả launch
2. 🔴 **Thông tin pháp nhân** (tên công ty, mã ĐKKD, địa chỉ) — bắt buộc theo pháp luật TMĐT VN
3. 🔴 **Số đo `THE MOMENTS BOXY HOODIE`** — chặn PDP hoodie

---

## Kiểm theme sau mỗi lần sửa

```bash
python docs/check-theme.py "E:/Vitalite website/repo/vitalite-website/vitalite-theme/vitalite-theme"
```
