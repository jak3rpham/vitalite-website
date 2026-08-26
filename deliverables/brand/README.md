# BRAND — nguồn sự thật về màu, chữ, logo

**Tạo:** 2026-08-27

---

## Ba file, ba việc

| File | Là gì | Ai đọc |
|---|---|---|
| `tokens.css` | **Giá trị.** 45 token màu, chữ, khoảng cách | Máy: 3 script sinh trang đều đọc từ đây |
| `BRAND-GUIDELINE.md` | **Lý do.** Vì sao mỗi màu tồn tại, dùng vào đâu, cấm gì | Người |
| `guideline.html` | **Bảng xem.** Ô màu, thang chữ, lưới logo, tỷ lệ tương phản | Người, mở bằng trình duyệt |

`guideline.html` **sinh tự động** từ `tokens.css`. Không sửa tay.

---

## Sửa một màu thì làm gì

```bash
# 1. sửa deliverables/brand/tokens.css
# 2. sửa cùng giá trị đó trong repo/.../vitalite-theme-2/style.css  (production đọc file này)
# 3. sinh lại:
cd "E:\Vitalite website"; python docs/make-pages.py; python docs/make-woo-preview.py; python docs/make-guideline.py
```

🔴 **Bước 2 chưa tự động.** `tokens.css` và khối `:root` trong `style.css` hiện phải sửa tay
cả hai. Có script kiểm lệch, chạy trước khi commit:

```bash
python docs/check-tokens.py
```

---

## Vì sao có file này

Trước 27/08, mỗi fragment mang giá trị dự phòng riêng và chúng **đã lệch nhau ở 10 token**:

| Token | Theme | Fragment |
|---|---|---|
| `--vt-muted` | `#6E6E76` | `#6B6B70` |
| `--vt-tint` | `#F4F4F4` | `#F7F7F8` |
| `--vt-sale` | `#C2413A` | `#C2452D` |
| `--vt-on-dark-muted` | `.68` | `.62` |

Trên site thật thì theme thắng nên không ai thấy. Nhưng **bản xem trước hiện sai màu so với
production**, mà đó chính là bản mọi người dùng để duyệt. Duyệt một màu, deploy ra màu khác.

Cùng lúc, `#B45309`, `#FEF6E7`, `#166534` hardcode rải rác **42 chỗ**, không đổi một lần được.

---

## Ba lỗi tìm ra khi dựng bộ này

1. **`--vt-dim` trượt chuẩn tiếp cận.** `#9A9AA2` chỉ đạt **2,79:1** trên nền trắng, trượt cả
   chuẩn chữ lớn, mà nó đang dùng cho chú thích và số trang. Đổi thành `#75757F`, đạt 4,56.
2. **`--vt-ok` hụt AA đúng 0,01.** `#18857A` đạt 4,49, cần 4,5. Đổi thành `#188479`.
3. **Weight 700 dùng 48 chỗ nhưng chưa bao giờ được tải.** Google Fonts chỉ yêu cầu
   `400;500;600;800`. Trình duyệt tự bắt sang 600 hoặc 800 nên những chỗ đó sai độ đậm mà
   không ai biết. Đã thêm `700` vào `inc/enqueue.php` và cả ba bản xem trước.

---

## Cái bộ này KHÔNG phải

Đây **không phải guideline do brand cấp**. Brand chưa cấp bộ nào.

Mỗi mục trong `BRAND-GUIDELINE.md` gắn một trong ba nhãn:

- ✅ **ĐO ĐƯỢC** — từ file gốc hoặc kênh chính thức của brand
- 🔧 **QUYẾT ĐỊNH BUILD** — lựa chọn của bản dựng, đổi được
- 🔴 **CHƯA CÓ** — đang chặn việc gì đó

**Trộn ba nhãn này lại là cách bộ guideline biến thành bịa.** Đừng trộn.

Bốn thứ còn thiếu thật sự đổi được diện mạo site: **mã hex tím/xanh dương**, **file vector logo**,
**bản logo trắng**, **ảnh chụp sản phẩm thật từ 1600px**.
