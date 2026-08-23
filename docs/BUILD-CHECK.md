# TỰ KIỂM — KẾT QUẢ
**Ngày:** 2026-08-20 · Chạy sau khi build xong, sửa, rồi chạy lại

---

## 0. Giới hạn của lần kiểm này — đọc trước

**Máy này không có PHP CLI, không có WordPress, không có server.**
Nghĩa là:

| Kiểm được | KHÔNG kiểm được |
|---|---|
| Cân bằng cú pháp `{}` `()` `[]` `<?php`/`?>` | `php -l` thật |
| Hàm gọi mà chưa định nghĩa | Hàm WordPress/Woo gọi sai tham số |
| `get_template_part()` trỏ file có thật không | Hook chạy đúng thứ tự không |
| Class CSS dùng mà thiếu rule | Trang hiển thị ra sao |
| Chuỗi bịa còn sót | Query có chạy đúng không |
| `echo` biến chưa escape | LCP thật là bao nhiêu |
| Text-domain nhất quán | Tương thích Elementor, Premmerce, Polylang |

**Kết luận: bản build này CHƯA ĐƯỢC CHẠY THỬ.** Phải xem thử trên hosting.
Quy trình upload an toàn (song song, lùi lại được trong 5 giây) ở `deliverables/setup/DEPLOY.md`.

---

## 1. Kết quả lần chạy cuối (2026-08-20, sau khi làm lại layout)

```
1. CÂN BẰNG CÚ PHÁP           25/25 file OK
2. HÀM vt_*                   24 định nghĩa · 0 gọi mà chưa có · 0 trùng · 0 thừa
3. get_template_part()        14/14 trỏ đúng file có thật
4. CLASS CSS                  0 class thiếu rule
5. CHUỖI BỊA                  sạch
6. ESCAPE                     0 dòng đáng ngờ
7. TEXT-DOMAIN                'vitalite' × 118, nhất quán

KẾT LUẬN: không phát hiện vấn đề
```

## 2. Lỗi ĐÃ TÌM RA và ĐÃ SỬA trong quá trình build

### 🔴 Nặng — lưới shop rỗng hoàn toàn
`woocommerce/archive-product.php`

Bản đầu dùng `if (wc_get_loop_prop('total'))` làm điều kiện vòng lặp.
Giá trị đó **do `woocommerce_product_loop_start()` đặt** — mà template này không gọi hàm đó
(nó in ra `<ul class="products">`, ta muốn `<div class="vt-grid">`).
→ `total` luôn bằng 0 → **vòng lặp không bao giờ chạy** → trang shop trắng trơn dù có sản phẩm.

Sửa: dùng `have_posts()`.

### 🔴 Nặng — nội dung trang con bị header che
`style.css`

Bản đầu đặt `padding-top` lên `#content` và `.site-main` — hai container của **Hello Elementor**.
Nhưng `header.php` mới in ra `<main class="vt-main">`, không phải `#content`.
→ Selector không khớp gì cả → mọi trang con, phần đầu nội dung **chui xuống dưới header dán**.

Sửa: thêm `.vt-main` vào selector, giữ hai cái cũ phòng khi có trang đi qua template cha.

### 🟡 Vừa — hai header chồng nhau
`inc/setup.php`

Trang Elementor cũ có thể vẫn đang chèn `[vt_header]` / `[vt_footer]`.
Giờ `header.php` và `footer.php` đã tự render → trang đó sẽ có **hai header**.

Sửa: thêm `vt_mark_rendered()`. Shortcode im lặng trả về rỗng nếu khối đã render rồi.

### 🟡 Vừa — trắng site nếu WooCommerce tắt
`template-parts/product-card.php`

Gọi `wc_get_product()` và `wc_product_class()` không kiểm tra tồn tại.
→ Woo tắt (khi debug, hoặc gỡ ra cài lại) là **fatal error, trắng toàn site**.

Sửa: `if (!function_exists('wc_get_product')) return;`

### 🟡 Vừa — cảnh báo PHP ở `og:url`
`inc/seo.php` — `$GLOBALS['wp']->request` rỗng ở một số route.
Sửa: `isset()` rồi mới dùng.

### 🟡 Vừa — `remove_action` có thể chạy quá sớm
`inc/woocommerce.php` — đổi `add_action('init', …)` sang ưu tiên `20`,
để chắc chắn chạy sau khi WooCommerce đăng ký xong hook mặc định.

### 🟡 Vòng làm lại layout (2026-08-20) — hai lỗi nữa

**Closure đặt tên `vt_*`.** `template-parts/hero.php` dùng `$vt_has()` / `$vt_url()` làm closure.
Trùng quy ước đặt tên của hàm thật trong theme → công cụ kiểm báo "hàm chưa định nghĩa",
và người đọc sau cũng sẽ nhầm. Đổi thành `$asset_exists()` / `$asset_url()`.

**Numbering section bị nhảy cóc.** Trang chủ đánh `01 · 02 · 03 · 05` — thiếu `04` vì
band iridescent không có eyebrow đánh số. Đã đổi section cuối thành `04`.

### 🔵 Nhẹ
- 6 chỗ `echo $var` trong thuộc tính `class` → bọc `esc_attr()`.
  *(Đều là ternary trả về chuỗi hằng, không phải input người dùng — không phải lỗ hổng,
  nhưng bọc lại thì reviewer không phải dừng lại kiểm tra.)*
- `menu_class => 'vt-mobile-list'` là code chết — `items_wrap` `%3$s` bỏ luôn thẻ `<ul>`.
- `vt_maybe_link()` mặc định gán class `vt-footer-link` không tồn tại trong CSS.
- Thêm rule còn thiếu: `.vt-main` `.vt-page-links` `.vt-size-guide` `.vt-grid.products`

---

## 3. Phát hiện khi đo — không phải lỗi code

### 🔴 Thư mục theme nặng 122MB

```
video/            115 MB   ← 96MB là master KHÔNG dùng
product-images/   5.4 MB   ← chỉ phục vụ lưới sản phẩm giả đã xoá
assets/           732 KB
code              ~110 KB
```

Nén cả thư mục để upload sẽ ra file zip ~120MB.
**Phải gỡ master ra trước khi deploy** — xem `DEPLOY.md` bước 0.
Và nhiều khả năng chúng cũng đang nằm trên production, ăn dung lượng hosting mà không phục vụ ai.

### 🟡 Ảnh đã tối ưu trong lúc build

| | Trước | Sau |
|---|---|---|
| `hero-poster` | 159 KB JPG | **38 KB** WebP |
| `cb-poster` | — | 81 KB WebP |
| `editorial-01` | — | 76 KB WebP, crop 4:5 từ ảnh model |
| `og-default` | — | 12 KB, nền đen + wordmark trắng |
| 18 mockup *(chưa đưa vào theme)* | 5.61 MB PNG | **359 KB** WebP |

---

## 4. Còn phải kiểm bằng tay — checklist sau khi upload

### Hiển thị
- [ ] Trang chủ: hero **3 slide tự đổi sau 7s**, thanh tiến trình chạy, bấm nhảy được
- [ ] Slide 03 (tone sáng): header tự đảo sang **chữ đen**, logo bỏ invert
- [ ] Header trong suốt trên hero → chuyển kính trắng khi cuộn qua
- [ ] Trang chủ trên **mobile thật**: video KHÔNG tải (đúng thiết kế), poster hiện
- [ ] Trang con (`/about`): nội dung KHÔNG bị header che ← lỗi vừa sửa
- [ ] `/shop`: lưới sản phẩm hiện ← lỗi vừa sửa
- [ ] Menu mobile: mở, đóng, phím Esc đóng, khoá cuộn nền
- [ ] Rê chuột lên thẻ sản phẩm: đổi sang ảnh mặt sau
- [ ] Giỏ hàng rỗng: badge số bị ẩn hoàn toàn
- [ ] Thêm hàng vào giỏ: badge hiện số, không cần tải lại trang

### Chức năng
- [ ] SEARCH ở header ra trang kết quả, không phải click chết
- [ ] Không còn 404 nào trong nav và footer
- [ ] `/cart` `/checkout` `/my-account` chạy đúng như trước
- [ ] Đặt một đơn test đi hết luồng
- [ ] Trang Elementor cũ (nếu còn) không bị **hai header**

### Kỹ thuật
- [ ] Console trình duyệt: 0 lỗi đỏ
- [ ] `wp-content/debug.log`: 0 PHP warning/notice
- [ ] PageSpeed Insights **tab Mobile**: LCP < 2.5s
- [ ] Xem source: `<title>` không còn "My WordPress Blog"
- [ ] Xem source: có JSON-LD `Organization` với `sameAs`
- [ ] Rich Results Test của Google: schema hợp lệ

### Hồi quy
- [ ] So sánh với ảnh chụp màn hình bản cũ — có gì mất mà đáng lẽ phải còn không?
- [ ] Premmerce filter vẫn chạy trên `/shop`
- [ ] Polylang (sau khi cài) không phá layout header

---

## 5. Điểm lệch so với CLAUDE.md — cần user xác nhận

### Trang chủ dựng bằng PHP, không phải Elementor

CLAUDE.md ghi *"Homepage: Build bằng Elementor"*. Bản build này dùng `front-page.php`.

**Lý do:**
- `Structure homepage` nằm trong OPEN ITEMS — **chưa bao giờ được chốt**
- User yêu cầu bản nền chạy được ngay để "ghép ghép là xong"
- PHP thì versioned trong git, diff được, review được; Elementor nằm trong database

**Đường lui còn nguyên:** mỗi section là một template part độc lập và đều có shortcode.
Muốn chuyển sang Elementor thì tạo trang Elementor, chèn shortcode từng section,
đặt làm trang chủ, xoá `front-page.php`. Không mất gì.

### Shortcode giữ lại làm lớp tương thích

CLAUDE.md ghi *"Bỏ shortcode"*. Bản này **giữ** `[vt_header]` `[vt_footer]` `[vt_banner]`
`[vt_products]` nhưng chúng chỉ còn là vỏ mỏng gọi `get_template_part()`, không còn logic.

**Lý do:** xoá ngay thì trang Elementor cũ đang chèn chúng sẽ in ra chuỗi thô cho khách thấy.
Gỡ hẳn sau khi đã kiểm tra không trang nào còn dùng.

---

## 6. Cách chạy lại bộ kiểm

Script đã lưu tại `docs/check-theme.py`:

```bash
python check.py "E:/Vitalite website/repo/vitalite-website/vitalite-theme/vitalite-theme"
```

Nó kiểm 7 mục ở phần 1. Chạy lại sau **mỗi lần sửa theme**.

**Nó không thay được `php -l`.** Nếu có PHP trên máy, chạy thêm:

```bash
find . -name "*.php" -exec php -l {} \;
```
