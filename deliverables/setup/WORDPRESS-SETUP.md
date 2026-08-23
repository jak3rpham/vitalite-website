# WORDPRESS — CẤU HÌNH TỪNG BƯỚC
**Ngày:** 2026-08-20 · Làm theo đúng thứ tự. Mỗi bước ghi rõ vì sao.

---

## ⛔ Trước khi bắt đầu

| | |
|---|---|
| ✅ Backup UpdraftPlus | user xác nhận đã xong 2026-08-19 |
| ⬜ Upload theme mới lên hosting | xem `deliverables/setup/DEPLOY.md` |
| ⬜ Xem thử site sau khi upload | **trước khi làm bất kỳ bước nào dưới đây** |

---

## 1. Cài đặt chung

`Cài đặt → Chung`

| Trường | Đặt thành | Vì sao |
|---|---|---|
| Tiêu đề trang web | `VITALITÉ` | Đang là `Vitalite`. Tên đúng **có dấu sắc** |
| Khẩu hiệu | `Streetwear made in Vietnam` | 🔴 Đang là **"My WordPress Blog"** — mặc định WordPress, chưa từng đổi, và **đang hiện trong `<title>` trên production** |
| Địa chỉ WordPress / Trang web | `https://vitalite.io.vn` | không có `www`, có `https` |
| Múi giờ | `UTC+7` hoặc `Ho Chi Minh` | ảnh hưởng ngày đăng → ảnh hưởng badge "New" |
| Định dạng ngày | `Y-m-d` | |
| Ngôn ngữ trang | ⚠️ **để `English (United States)` cho tới khi cài Polylang** | Root là EN. Đổi sang tiếng Việt bây giờ sẽ phải đảo lại ở bước Polylang |

> `<html lang="en-US">` hiện tại đang **đúng** với hướng EN-first, dù nội dung cũ là tiếng Việt.
> Sau khi nội dung chuyển sang EN thì nó khớp. Polylang sẽ tự lo `lang` cho `/vi/`.

---

## 2. Đọc

`Cài đặt → Đọc`

| Trường | Đặt thành |
|---|---|
| Trang chủ hiển thị | **Bài viết mới nhất** ⚠️ xem ghi chú |
| Ngăn công cụ tìm kiếm | **để nguyên TICK cho tới ngày launch** |

> **Ghi chú trang chủ.** Theme dùng `front-page.php`, template này **thắng mọi cài đặt**:
> để "Bài viết mới nhất" hay "Một trang tĩnh" thì WordPress vẫn dùng `front-page.php`.
> Nên cứ để "Bài viết mới nhất" cho gọn.
> Muốn chuyển sang dựng trang chủ bằng Elementor thì xoá `front-page.php` đi rồi mới
> chọn "Một trang tĩnh".

> 🔴 **`Ngăn công cụ tìm kiếm` đang BẬT trên production.** Đó là lý do site chưa lọt ra Google —
> và đó là điều tốt lúc này, vì sản phẩm giả và giá giả đã từng hiển thị trên đó.
> **Nhưng phải TẮT vào ngày launch.** Đây là lỗi bị quên nhiều nhất khi launch WordPress.
> Theme đã cài sẵn cảnh báo thường trực trong admin (`inc/seo.php`) cho tới khi tắt.

---

## 3. Đường dẫn tĩnh

`Cài đặt → Đường dẫn tĩnh`

```
Tuỳ chỉnh:  /%postname%
```

Không có dấu `/` ở cuối. Quyết định đã chốt trong CLAUDE.md.

> Biết trước: archive và phân trang **vẫn có** dấu `/` ở cuối. Đó là WordPress core,
> không sửa được mà không phá rewrite rule. Không phải lỗi.

Phần **Product permalinks** ở dưới cùng:

```
Product category base:  product-category      ← giữ mặc định
Product permalinks:     Standard  →  /product/
```

> Theme dùng `vt_cat_url('t-shirts')` sinh link category, mà hàm đó tra term thật
> qua `get_term_link()`. Nên đổi base sau này cũng không phá link nào.

**Sau khi đổi permalink: vào lại trang này và bấm Lưu một lần nữa.** WordPress cần flush rewrite rules.

---

## 4. Thảo luận

`Cài đặt → Thảo luận`

- ❌ Bỏ tick **Cho phép bình luận trên bài viết mới**

Site không có blog. Bình luận mở là bề mặt spam thuần tuý.

---

## 5. Tạo Product Categories

`Sản phẩm → Danh mục`

| Tên | Slug | Ghi chú |
|---|---|---|
| T-Shirts | `t-shirts` | ⚠️ **slug phải đúng** — theme và nav dò theo slug này |
| Outerwear | `outerwear` | ⚠️ **slug phải đúng** |
| Bottoms | `bottoms` | tạo sẵn, chưa có hàng |

❌ **Không tạo** `New Arrivals`, `Sale`, `Collection`, `Best Sellers`.
Đó không phải danh mục — chúng là *cách sắp xếp* cùng một tập sản phẩm.
Theme đã làm bằng `?orderby=date` và `?on_sale=1` trên trang shop.
Tạo category cho chúng là tự tạo nội dung trùng lặp và loãng SEO.

Xoá category `Uncategorized` sau khi đã có category thật.

---

## 6. Tạo Attributes

`Sản phẩm → Thuộc tính`

### Dùng cho variation

| Tên | Slug | Terms | Bắt buộc |
|---|---|---|---|
| Size | `size` | `S` `M` `L` | ✅ tick *Enable archives* = **không**. Sắp xếp: **Custom ordering** |
| Color | `color` | `Black` `White` `Grey` `Pure White` `Cream` | ✅ |

> ⚠️ **Size phải đặt Custom ordering.** Để mặc định alphabet thì thứ tự ra `L, M, S` — sai.
> Vào `Sản phẩm → Thuộc tính → Size → Configure terms` rồi kéo thả đúng thứ tự S, M, L.

### Chỉ là spec, KHÔNG tick "Used for variations" khi gán vào sản phẩm

| Tên | Slug | Terms |
|---|---|---|
| Fabric | `fabric` | `250 GSM Cotton` · `500+ GSM Heavyweight Cotton Blend` |
| Fit | `fit` | `Signature Boxy Fit` · `Unisex Regular` |
| Collection | `collection` | `The Iconic` · `The Moments` · `Starlight` · `Pink Graffiti` · `Porsche` · `Old Money` |
| Print | `print` | `Silkscreen` |

> Bốn thuộc tính này đổ vào tab **Details** của PDP — đúng khuôn 4 gạch đầu dòng
> brand vẫn dùng trên Instagram (`• Fabric: … • Fit: … • Sizing: …`).
>
> Đưa nhầm chúng vào variation là nổ số variation theo cấp số nhân:
> 3 size × 2 màu = 6 variation thật, thêm fabric và fit vào thành 24.

⚠️ **Polylang phải cấu hình xong TRƯỚC bước này.** Attribute term là taxonomy term.
Tạo term trước khi bật Polylang cho `pa_*` thì phải gán ngôn ngữ tay cho từng term.

---

## 7. WooCommerce

`WooCommerce → Cài đặt`

### Chung
| | |
|---|---|
| Địa chỉ cửa hàng | 🔴 `[NEED: địa chỉ kho thật]` — dùng để tính phí ship |
| Vị trí bán hàng | `Bán cho tất cả các nước` ← định hướng quốc tế |
| Vị trí giao hàng | 🔴 `[NEED]` — chờ số liệu ship quốc tế |
| Đơn vị tiền tệ | `Vietnamese đồng (₫)` |
| Vị trí tiền tệ | `Bên phải` |
| Dấu phân cách hàng nghìn | `.` |
| Dấu thập phân | `,` |
| Số chữ số thập phân | **`0`** ← VND không có hào |

### Sản phẩm
| | |
|---|---|
| Trang cửa hàng | `Shop` |
| Thêm vào giỏ | ❌ **không** tick "Chuyển hướng đến giỏ hàng sau khi thêm" |
| | ✅ tick "Bật nút thêm vào giỏ trên archive" |
| Đơn vị đo | `cm` / `kg` |
| Đánh giá | ❌ **tắt** — chưa có đánh giá nào, tab rỗng làm site trông bỏ hoang. Theme cũng đã ẩn tab này |

### Hình ảnh sản phẩm
| | |
|---|---|
| Chiều rộng ảnh chính | `1000` |
| Chiều rộng thumbnail | `600` |
| Cắt thumbnail | **1:1** |

> Mockup gốc chỉ `1000×1000`. Theme đã **tắt zoom** vì zoom vào ảnh 1000px chỉ phóng to
> điểm ảnh — trông như hàng rẻ tiền. Có ảnh ≥1600px thì bật lại
> (`inc/setup.php`, bỏ comment dòng `wc-product-gallery-zoom`).

### Thanh toán
🔴 Chưa cấu hình được. Cần đăng ký kinh doanh + thông báo Bộ Công Thương.
Shopee hiển thị brand **đã có pháp nhân** → rào cản có thể chỉ còn phần thông báo. Cần kiểm lại.

Trong lúc chờ: bật **Thanh toán khi nhận hàng (COD)** để test được full flow.
🔴 `[NEED: có làm COD thật không? Shopee có COD]`

### Vận chuyển
🔴 Chưa cấu hình được — **chặn bởi việc chưa có số liệu phí ship**.
Xem `deliverables/content/PAGES-CONTENT.md` mục 3.

---

## 8. Tạo Pages

`Trang → Thêm mới`. **Slug phải đúng** — theme dò page theo slug, sai slug thì link footer không hiện.

| Tiêu đề | Slug | Trạng thái |
|---|---|---|
| Size Guide | `size-guide` | ✅ có nội dung đầy đủ |
| Returns & Exchanges | `returns` | ✅ có nội dung |
| Contact | `contact` | ⚠️ thiếu thông tin pháp nhân |
| About | `about` | ✅ dán được |
| Shipping | `shipping` | 🔴 **chưa tạo** — chưa có dữ liệu nào |
| Collections | `collection` | ⚠️ chỉ tạo sau khi có sản phẩm |

Nội dung: `deliverables/content/PAGES-CONTENT.md`

> Theme **không in link tới page chưa tồn tại**. Cứ để Shipping chưa tạo —
> footer tự bỏ qua, không có link chết. Tạo xong là link tự hiện.

---

## 9. Menu

`Giao diện → Menu`

Theme có 3 vị trí menu. **Không bắt buộc tạo** — chưa tạo thì theme dùng menu dựng sẵn,
mọi link đều tự lành. Tạo menu khi muốn kiểm soát thứ tự hoặc thêm mục.

| Vị trí | Dùng cho |
|---|---|
| `Primary menu` | nav chính (desktop + mobile) |
| `Footer — Shop` | cột Shop ở footer |
| `Footer — Support` | cột Support ở footer |

---

## 10. Xoá rác

| Xoá gì | Ở đâu |
|---|---|
| Bài viết mẫu "Hello world!" | `Bài viết` |
| Trang mẫu "Sample Page" | `Trang` |
| Bình luận mẫu | `Bình luận` |
| Plugin `Akismet`, `Hello Dolly` | `Plugin` — không dùng, vẫn bị quét |
| Theme không dùng (Twenty*) | `Giao diện → Giao diện` — giữ **Hello Elementor** (theme cha) |
| `wp-content/themes/vitalite-theme/product-images/` | 17 ảnh chỉ dùng cho lưới sản phẩm giả đã xoá. ✅ Bản build mới KHÔNG còn thư mục này — chỉ cần xoá trên production nếu bản cũ còn |

> ⚠️ **Giữ lại Hello Elementor.** Đó là theme cha. Xoá nó là trắng site.

---

## 11. Bảo mật — thêm vào `wp-config.php`

`cPanel → File Manager → public_html/wp-config.php`.
Chèn **trên** dòng `/* That's all, stop editing! */`:

```php
/* Chặn sửa file theme/plugin từ trong wp-admin.
   Tài khoản admin bị chiếm là chèn được PHP tuỳ ý qua màn hình editor. */
define('DISALLOW_FILE_EDIT', true);

/* Không cho cài/gỡ plugin từ wp-admin.
   ⚠️ Bật cái này thì phải cài plugin qua FTP. Chỉ bật SAU KHI đã cài xong hết. */
// define('DISALLOW_FILE_MODS', true);

/* Giới hạn số bản nháp lưu — mỗi bản nháp là một hàng trong DB */
define('WP_POST_REVISIONS', 5);

/* Dọn thùng rác sau 14 ngày thay vì 30 */
define('EMPTY_TRASH_DAYS', 14);
```

> **Chưa bật `DISALLOW_FILE_MODS`** cho tới khi cài xong Polylang và các plugin còn lại.
> Bật sớm là tự khoá mình ra ngoài.

---

## 12. Thứ tự tổng thể

```
1.  Upload theme  →  xem thử site  ← LÀM TRƯỚC MỌI THỨ
2.  Cài đặt chung + Đọc + Đường dẫn tĩnh
3.  Xoá rác (bước 10)
4.  wp-config (bước 11)
5.  LiteSpeed Cache          → HOSTING-LITESPEED.md
6.  Polylang                 → 6 quyết định, CHƯA dịch gì
7.  Product categories + attributes   ← PHẢI sau Polylang
8.  Cấu hình WooCommerce
9.  Tạo pages
10. Nhập 2 SẢN PHẨM TEST → kiểm tra toàn bộ luồng
11. Sửa cái gì vỡ, RỒI mới nhập phần còn lại
12. Analytics                → TRACKING-PLAN.md
13. Trước launch: TẮT "Ngăn công cụ tìm kiếm" + nộp sitemap
```

**Bước 10 không được bỏ.** Sửa cấu trúc lúc có 2 sản phẩm là 10 phút.
Lúc có 40 sản phẩm × 6 variation là làm lại từ đầu.
