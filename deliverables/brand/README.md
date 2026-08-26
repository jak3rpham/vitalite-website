# BRAND — nguồn sự thật về màu, chữ, logo

**Tạo:** 2026-08-27

> 🔴 **Bản PDF v1 CHƯA ĐƯỢC DUYỆT.** User xem ngày 27/08 và trả lời *"chưa được đâu"*,
> nhưng bảo cứ đẩy lên git. Nó nằm trong repo để có mốc so sánh, **không phải để gửi brand**.
> Chưa có ghi chú cụ thể hỏng chỗ nào. Đừng gửi bản này đi khi chưa hỏi lại user.

---

## Ba file, ba việc

| File | Là gì | Ai đọc |
|---|---|---|
| `tokens.css` | **Giá trị.** 45 token màu, chữ, khoảng cách | Máy: 3 script sinh trang đều đọc từ đây |
| `BRAND-GUIDELINE.md` | **Lý do.** Vì sao mỗi màu tồn tại, dùng vào đâu, cấm gì | Người |
| `guideline.html` | **Bảng tra nội bộ.** Ô màu, thang chữ, lưới logo, tỷ lệ tương phản | Người, mở bằng trình duyệt |
| `VITALITE-Brand-Guideline.pdf` | **Bản trình bày cho brand.** 16 trang A4 ngang, hình là chính | Đưa cho brand |
| `guideline-print.html` | Nguồn của bản PDF trên | Máy |
| `assets/` | Ảnh cắt sẵn cho bản in, sinh tự động | Máy |

`guideline.html` và bản PDF đều **sinh tự động** từ `tokens.css`. Không sửa tay file nào trong số đó.

## Bản PDF cho brand

```bash
cd "E:\Vitalite website"; python docs/make-guideline-pdf.py
```

16 trang A4 ngang, 2,6 MB. Render bằng Chrome headless, script tự dò Chrome hoặc Edge.
Không có trình duyệt thì nó vẫn ghi `guideline-print.html` ra, mở rồi Ctrl+P > Save as PDF
cũng ra đúng bản đó.

Khác nhau giữa hai bản:

| | `guideline.html` | bản PDF |
|---|---|---|
| Cho ai | nội bộ, người dựng site | brand |
| Dạng | cuộn dọc, dày chữ, tra cứu | 16 trang, hình là chính |
| Giọng | thẳng, nêu cả lỗi kỹ thuật | trình bày, nêu cái brand cần quyết |

Ba ảnh trong `assets/` (`e-20`, `e-21`, `wordmark-trim`) **sinh lúc build** bằng Pillow,
cắt từ file logo gốc. Đừng sửa tay, chạy lại script là chúng bị ghi đè.

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
