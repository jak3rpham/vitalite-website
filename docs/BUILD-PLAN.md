# KẾ HOẠCH BUILD — BẢN NỀN TOÀN SITE

> ⚠️ **Đây là kế hoạch của phiên build đêm 19–20/08, ĐÃ THỰC THI XONG.**
> Sau đó layout được **làm lại toàn bộ** theo prototype: full-width, hero 3 slide,
> lưới hairline, gallery mosaic. Kế hoạch dưới đây mô tả bản boxed 1440px **không còn đúng**.
> Trạng thái hiện tại: `docs/HANDOFF.md`.

**Bắt đầu:** 2026-08-20 · **Chế độ:** tự chạy, user đang ngủ
**Mục tiêu user đặt:** *"tổng thể website luôn, thành cái nền để cùng update trên đó"*

---

## 0. Nguyên tắc cho toàn bộ bản build này

| | |
|---|---|
| **Không bịa fact** | Chỉ dùng dữ liệu đã xác minh trong `reference/BRAND_FACTS_OBSERVED.md`. Thiếu thì `[NEED: …]` inline, không điền đại |
| **Nền trắng cho vùng sản phẩm** | Lưới shop, PDP → trắng. Hero / band / About → tối + iridescent |
| **EN default tại root** | Mọi string bọc `__()` / `esc_html_e()` sẵn cho Polylang. Chưa dịch gì |
| **Solo operator** | Không đề xuất gì cần dev team. Mọi bước user tự làm được |
| **LCP < 2.5s mobile** | Ràng buộc cứng, kiểm ở từng quyết định |
| **Loop-safe** | Không hardcode dữ liệu sản phẩm. Mọi thứ chạy qua WooCommerce |
| **Không đụng cart/checkout** | Flow mặc định Woo. Chỉ style, không sửa logic |

---

## 1. Quyết định kiến trúc

### 1.1 — Theme PHP, không Elementor Theme Builder
Giữ nguyên quyết định "Con đường A" trong CLAUDE.md.

### 1.2 — Bỏ shortcode, chuyển sang template chuẩn WordPress
`[vt_header]` `[vt_banner]` `[vt_products]` `[vt_footer]` → `header.php` / `footer.php` / `template-parts/`.
Đây là bước 2 trong thứ tự thực thi của CLAUDE.md, chưa từng làm.

**Shortcode vẫn giữ lại làm lớp tương thích** — nếu trang Elementor hiện tại đang chèn
`[vt_banner]` thì nó vẫn chạy, không vỡ. Nhưng chúng chỉ còn là vỏ gọi `get_template_part()`.

### 1.3 — Homepage build bằng PHP (`front-page.php`), không phải Elementor
⚠️ **Đây là điểm lệch so với CLAUDE.md**, nêu rõ để user quyết lại.

CLAUDE.md ghi *"Homepage: Build bằng Elementor"*. Nhưng:
- `Structure homepage` nằm trong OPEN ITEMS — **chưa bao giờ chốt**
- User yêu cầu "tổng thể website luôn… t chỉ ghép ghép là xong" → cần thứ chạy được ngay
- Homepage PHP thì versioned trong git, review được, không phụ thuộc DB
- Elementor homepage nằm trong database → không đưa vào git được, không diff được

**Đường lui vẫn mở:** mọi section là `template-part` riêng, và mỗi cái có shortcode.
Muốn chuyển sang Elementor thì tạo trang Elementor rồi chèn shortcode từng section, hoặc
dùng Loop Grid của Elementor thay `section-products`. Không mất gì.

### 1.4 — Không đụng `single-product.php` và `cart/checkout`
PDP dùng template mặc định của Woo + hook. Sửa file `single-product.php` là chỗ dễ vỡ nhất
khi Woo update. Toàn bộ tuỳ biến PDP đi qua `add_action()` trong `inc/woocommerce.php`.

---

## 2. Danh sách file sẽ tạo

### Theme
```
style.css                          token + toàn bộ CSS
functions.php                      bootstrap, nạp inc/
inc/setup.php                      theme support, menu, image size, security
inc/helpers.php                    vt_shop_url, vt_cat_url, vt_page_url, vt_maybe_link, vt_logo
inc/enqueue.php                    asset, font, nạp có điều kiện
inc/woocommerce.php                hook Woo, product card, hover mặt sau, badge, breadcrumb
inc/seo.php                        title, meta, OG, JSON-LD, hreflang
header.php  footer.php
front-page.php                     homepage
page.php  index.php  404.php  search.php  searchform.php
template-parts/site-header.php
template-parts/site-footer.php
template-parts/hero.php            video + iridescent overlay
template-parts/section-products.php
template-parts/section-iridescent.php
template-parts/section-editorial.php
template-parts/product-card.php
template-parts/empty-state.php
woocommerce/archive-product.php
woocommerce/content-product.php
assets/js/site.js
```

### Tài liệu
```
deliverables/content/PAGES-CONTENT.md      nội dung 8 trang, đánh dấu chỗ thiếu fact
deliverables/setup/WORDPRESS-SETUP.md      setting, permalink, Woo config, trang cần tạo
deliverables/setup/PLUGINS.md              plugin nào, vì sao, chi phí performance
deliverables/setup/HOSTING-LITESPEED.md    cPanel, LiteSpeed Cache, PHP, bảo mật
deliverables/setup/PERFORMANCE.md          LCP, ảnh, font, cache, đo thế nào
deliverables/seo/SEO-PLAN.md               sitemap, schema, meta, hreflang, robots
deliverables/analytics/TRACKING-PLAN.md    GA4, event, ecommerce, report
docs/BUILD-CHECK.md                        kết quả tự kiểm
```

---

## 3. Cấu trúc trang

| Trang | Template | Trạng thái nội dung |
|---|---|---|
| Home | `front-page.php` | ✅ layout đủ, copy thật từ IG |
| Shop | `woocommerce/archive-product.php` | ✅ |
| PDP | Woo mặc định + hook | ✅ |
| Cart / Checkout / Account | Woo mặc định, chỉ style | ✅ không đụng logic |
| Search | `search.php` | ✅ |
| 404 | `404.php` | ✅ |
| About | `page.php` | ⚠️ khung + copy thật từ IG/FB, chỗ thiếu đánh dấu |
| Size Guide | `page.php` | ✅ **có số đo thật** |
| Returns | `page.php` | ✅ **có chính sách thật** |
| Contact | `page.php` | ✅ email + hotline thật |
| Shipping | `page.php` | 🔴 **KHÔNG CÓ DỮ LIỆU** — chỉ dựng khung, để `[NEED]` |
| Collection | `page.php` | ⚠️ khung, chờ chốt collection nào lên |

---

## 4. Thứ tự thực thi trong phiên này

```
1. style.css — token hệ thống          ← mọi thứ khác phụ thuộc
2. inc/helpers.php + inc/setup.php
3. inc/enqueue.php
4. header.php + footer.php + template-parts/site-*
5. inc/woocommerce.php                 ← product card, hover mặt sau
6. template-parts/* còn lại
7. front-page.php
8. page.php, 404.php, search.php, index.php
9. woocommerce/archive-product.php, content-product.php
10. functions.php (bootstrap cuối, sau khi biết cần nạp gì)
11. assets/js/site.js
12. Nội dung 8 trang
13. Tài liệu setup / SEO / tracking
14. TỰ KIỂM → sửa → kiểm lại
```

---

## 5. Cách tự kiểm (bước 14)

Không có PHP CLI trên máy này nên không lint thật được. Thay bằng:

| Kiểm | Cách |
|---|---|
| Cân bằng cú pháp | scanner ký tự: `{}` `()` `[]` `<?php`/`?>` từng file |
| Hàm gọi mà chưa định nghĩa | quét `vt_*(` đối chiếu `function vt_*` |
| `get_template_part()` trỏ file không tồn tại | quét đường dẫn, đối chiếu filesystem |
| Class CSS dùng mà không có rule | quét class trong PHP đối chiếu `style.css` |
| Chuỗi chưa bọc i18n | quét text node tiếng Anh nằm ngoài `__()` |
| Fact bịa | quét lại danh sách chuỗi cấm (`480GSM`, `SS26`, giá cũ…) |
| Escape output | quét `echo $` không qua `esc_*` |

Kết quả ghi vào `docs/BUILD-CHECK.md`, sửa hết rồi kiểm lại.
