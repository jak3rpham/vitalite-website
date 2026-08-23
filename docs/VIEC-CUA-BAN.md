# VIỆC CỦA BẠN — bản tổng hợp

**Cập nhật:** 2026-08-22
**Đọc file này thay vì nhớ 12 file khác.** Mọi thứ khác chỉ là chi tiết của các mục dưới đây.

---

## Đang đứng ở đâu

Theme đã deploy và đang chạy trên `vitalite.io.vn`. Git đã sạch, đã push.
Còn lại là **nội dung và cấu hình**, không phải code.

---

# PHẦN 1 — Làm ngay, mỗi việc dưới 10 phút

## 1.1 Upload 3 file theme mới nhất

Từ:
```
E:\Vitalite website\repo\vitalite-website\vitalite-theme\vitalite-theme-2\
```

Ba file đã sửa từ lần upload trước:

| File trong repo | Chỗ tương ứng trên hosting |
|---|---|
| `style.css` | `public_html/wp-content/themes/vitalite-theme-2/style.css` |
| `template-parts/site-footer.php` | `…/vitalite-theme-2/template-parts/site-footer.php` |

Upload **đè lên file cùng tên**, đừng đè cả thư mục. Xong thì **xoá cache LiteSpeed**.

*Sửa gì:* thanh chuyển slide hero hết bị dải hồng và hết dày 18px · lưới sản phẩm hết lộ mảng
xám khi ít hàng · footer có thêm cột **Legal**.

## 1.2 Đổi template trang chủ

Trang chủ đang bị Elementor chiếm quyền nên **chỉ hiện 2 trong 6 section**.

`Trang` → `Tất cả trang` → rê chuột lên trang chủ → **`Sửa nhanh`** → ô **`Mẫu`** →
chọn **`Mẫu mặc định`** → `Cập nhật`.

🔴 **Đừng mở Elementor để làm việc này** — nó sẽ báo *"the content area was not found"* và
không cho đổi. Sửa nhanh không load Elementor nên không dính lỗi đó.

## 1.3 Cấu hình WordPress cơ bản

Tiêu đề site vẫn đang là `Vitalite – My WordPress Blog`.

| Vào đâu | Đặt gì |
|---|---|
| `Cài đặt → Chung` | Tiêu đề `VITALITÉ` (có dấu sắc) · tagline · múi giờ **Ho Chi Minh** |
| `Cài đặt → Đường dẫn tĩnh` | `/%postname%` |
| `Cài đặt → Đọc` | **BẬT** "Ngăn công cụ tìm kiếm" — tắt vào ngày launch |

---

# PHẦN 2 — Tạo trang, dán HTML

## File nằm ở đâu

```
E:\Vitalite website\deliverables\pages-html\
```

Mở `_preview-all.html` bằng trình duyệt để xem trước cả 10 trang. **File đó chỉ để xem**, đừng dán.

## Cách dán

1. `Trang → Thêm mới`
2. Đặt **tiêu đề** và **slug** đúng bảng dưới — theme dò page **theo slug**, sai slug là footer
   không hiện link
3. Sửa bằng Elementor → kéo widget **HTML** → dán **toàn bộ** file `.html`
4. `Xuất bản`

## 🔴 Ô cam = chưa được xuất bản

Trong trang có những **ô nền cam** ghi *"Chưa có dữ liệu"*. Đó là chỗ tôi cố ý để trống —
bịa phí ship hay điều khoản pháp lý là bịa ra một hợp đồng với khách.

**Còn ô cam thì đừng xuất bản trang đó.** Điền xong, xoá ô, rồi mới đăng.

## Bảng 10 trang

| Thứ tự làm | Slug | File | Ô cam | Đăng được chưa |
|---|---|---|---|---|
| 1 | `about` | `about.html` | 1 | ✅ **Đăng được ngay** — ô cam là một quyết định kinh doanh, không phải thiếu dữ liệu |
| 2 | `size-guide` | `size-guide.html` | 1 | ⚠️ Thiếu số đo hoodie |
| 3 | `faq` | `faq.html` | 1 | ⚠️ Thiếu chính sách restock |
| 4 | `returns` | `returns.html` | 3 | ⚠️ Xem phần 3 |
| 5 | `contact` | *chưa có HTML* | — | Nội dung ở `deliverables/content/PAGES-CONTENT.md` |
| 6 | `seller-information` | `seller-information.html` | 2 | 🔴 Bắt buộc theo luật · thiếu pháp nhân |
| 7 | `privacy` | `privacy.html` | 3 | 🔴 Bắt buộc theo luật |
| 8 | `terms` | `terms.html` | 2 | 🔴 Bắt buộc theo luật |
| 9 | `complaints` | `complaints.html` | 2 | 🔴 Bắt buộc theo luật |
| 10 | `payment` | `payment.html` | 3 | ⚠️ Chờ cổng thanh toán |
| 11 | `shipping` | `shipping.html` | 4 | 🔴 **Chặn launch** |

Footer tự nối link khi trang được xuất bản — không phải sửa code.

---

# PHẦN 3 — 11 câu hỏi chỉ bạn trả lời được

Đây là thứ đang chặn mọi việc còn lại. Trả lời xong, tôi viết nốt trong một lượt.

## 🔴 Chặn launch

1. **Ship quốc tế:** hãng nào · ship tới nước nào · phí theo vùng · thời gian · **thuế nhập khẩu ai chịu**
2. **Ship trong nước:** hãng nào · phí nội thành · phí tỉnh · thời gian · có ngưỡng miễn phí ship không
3. **Pháp nhân:** tên công ty/hộ kinh doanh · mã số thuế · địa chỉ đăng ký *(lấy từ hồ sơ Shopee)*

## 🟡 Chặn nội dung

4. **COD** hay trả trước 100%?
5. **Đổi size do khách chọn nhầm** — giữ "khách chịu ship 2 chiều", hay hỗ trợ 1 chiều?
6. **Có hoàn tiền không**, hay chỉ đổi hàng?
7. **Địa chỉ nhận hàng đổi trả**
8. **Hotline nào còn dùng** — Facebook ghi `093 838 14 07`, bài 2023 ghi `037 963 2222`
9. **Số đo `THE MOMENTS BOXY HOODIE`** — dài, rộng, dài tay
10. **Cổng thanh toán** nào đã cấu hình thật trong WooCommerce
11. **Hàng hết có restock không**, hay mỗi drop là một lần duy nhất

### Một câu tôi phải nói thẳng về mục 1

Áo bán ~280.000₫ (~$11). Ship quốc tế thường $25–40 — **gấp 3 lần giá hàng**.

Website tồn tại là để bán cho khách quốc tế: IG 7.000 follower, bio ghi `Worldwide shipping`,
và Shopee.vn không phục vụ khách ngoài Việt Nam. Nếu phí ship giết chết chuyện đó thì đây là
**rủi ro mô hình kinh doanh**, không phải rủi ro kỹ thuật — và phải biết **trước** khi launch.

---

# PHẦN 4 — Sản phẩm

Sản phẩm test hiện tại đang **sai kiểu**. Nó là **Simple** và nằm ở category `Uncategorized`,
nên không có nút chọn size và không hiện bảng số đo. Không phải lỗi theme.

Nhập đúng thì phải:

| | |
|---|---|
| Loại sản phẩm | **Variable**, không phải Simple |
| Category slug | `t-shirts` · `outerwear` · `bottoms` — **slug tiếng Anh** |
| Attribute biến thể | `pa_size` (S/M/L, **Custom ordering**) · `pa_color` |
| Attribute thông số | `pa_fabric` · `pa_fit` · `pa_collection` · `pa_print` — **KHÔNG tick "used for variations"** |
| Ảnh chính | **MẶT TRƯỚC** |
| Ảnh gallery đầu tiên | **MẶT SAU** — rê chuột trên lưới sẽ đổi trước ↔ sau |

🔴 **Polylang đang bật.** Sản phẩm test chỉ gán tiếng Việt nên `/shop` (EN) rỗng, `/vi/shop` mới có hàng.
Nhập sản phẩm thật thì phải để ý gán ngôn ngữ.

🔴 **Nhập đúng 2 sản phẩm rồi dừng lại kiểm** — một áo thun, một áo khoác. Hai loại vì chúng đi
qua hai nhánh code khác nhau. Sửa cấu trúc lúc có 2 sản phẩm là 10 phút; lúc có 40 sản phẩm là
làm lại từ đầu.

---

# Bản đồ file — cần gì mở file nào

| Cần gì | Mở file nào |
|---|---|
| **Việc phải làm** | 📍 **file này** |
| Thứ tự dựng site đầy đủ | `docs/BUILD-ON-WORDPRESS.md` |
| HTML 10 trang + hướng dẫn dán | `deliverables/pages-html/` (có `README.md` riêng) |
| Xem trước 10 trang | `deliverables/pages-html/_preview-all.html` |
| Nội dung Contact / About / Collection dạng chữ | `deliverables/content/PAGES-CONTENT.md` |
| So sánh chính sách với 2 đối thủ | `deliverables/content/POLICIES.md` |
| Trạng thái kỹ thuật của theme | `docs/HANDOFF.md` |
| Fact brand đã xác minh | `reference/BRAND_FACTS_OBSERVED.md` |
| **Brand đã đổi chủ — đọc trước khi viết copy** | `reference/BRAND_ERA_SPLIT.md` |
| Deploy theme | `deliverables/setup/DEPLOY.md` |
| Cấu hình WooCommerce | `deliverables/woo/STRUCTURE-SETUP.md` |
| Polylang | `docs/I18N-SETUP.md` |

## Hai lệnh chạy sau mỗi lần tôi sửa theme

```bash
cd "E:\Vitalite website"; python docs/check-theme.py "repo/vitalite-website/vitalite-theme/vitalite-theme-2"
```

```bash
cd "E:\Vitalite website"; python docs/make-pot.py
```

⚠️ Terminal máy này là **Windows PowerShell 5.1** — `&&` không tồn tại, nối lệnh bằng `;`.

---

# Thứ tự tôi khuyên

```
Hôm nay   →  1.1 upload 3 file  →  1.2 đổi template trang chủ  →  1.3 cấu hình WP
             →  đăng trang ABOUT (đăng được ngay)

Kế tiếp   →  trả lời 11 câu ở phần 3
             →  tôi viết nốt các trang trong một lượt

Sau đó    →  nhập 2 sản phẩm test đúng chuẩn  →  kiểm  →  nhập phần còn lại

Cuối      →  dịch VI  →  tắt "Ngăn công cụ tìm kiếm"  →  launch
```
