# DEPLOY — đưa theme lên hosting
**Ngày:** 2026-08-20 · Shared cPanel zhost.vn · không có SSH

---

## Tình hình

| | |
|---|---|
| Hosting | shared cPanel zhost.vn, LiteSpeed |
| SSH / git trên server | ❌ không có |
| Cách user đang làm | sửa tay qua cPanel File Manager |
| Repo local | ✅ user đã tải theme production về và đồng bộ (2026-08-20) |
| Backup UpdraftPlus | ✅ xong |

---

## Bản build này thay đổi những gì

⚠️ Đây **không phải** sửa vài dòng. Đây là **tái cấu trúc theme**.

### File bị XOÁ
```
banner-video.php            → template-parts/hero.php
header-woocommerce.php      → template-parts/site-header.php
homepage-woocommerce.php    → template-parts/section-products.php
footer-elementor.php        → template-parts/site-footer.php
```

### File MỚI
```
header.php  footer.php  front-page.php  page.php  index.php
404.php  search.php  searchform.php
inc/helpers.php  inc/setup.php  inc/enqueue.php  inc/woocommerce.php  inc/seo.php
template-parts/  (8 file)
woocommerce/archive-product.php  woocommerce/content-product.php
assets/js/site.js
assets/hero-poster.webp  assets/cb-poster.webp  assets/editorial-01.webp  assets/og-default.jpg
```

### File bị GHI ĐÈ
```
functions.php     — giờ chỉ còn bootstrap nạp inc/
style.css         — viết lại toàn bộ, hệ token mới
```

---

## Xem trước mà chưa đụng production

PHP không mở bằng cách bấm đúp file — nó cần server chạy. Ba cách, theo thứ tự khuyến nghị:

### A. Bản xem trước tĩnh — xem NGAY, 0 cài đặt ⭐

`deliverables/preview/static-preview.html` — bấm đúp là mở.
Dựng lại 9 màn hình bằng HTML thuần, dùng **đúng `style.css` của theme** và **ảnh mockup thật**.

Thấy được: bố cục, chữ, màu, khoảng cách, thẻ sản phẩm, hover đổi mặt trước/sau,
band iridescent chuyển động, bảng size, empty state, 404, footer.

Không thấy được: dữ liệu WooCommerce, giỏ hàng, tìm kiếm, video hero, JS đổi chế độ header.

### B. WordPress chạy local — xem THẬT, không rủi ro ⭐⭐

**LocalWP** (localwp.com) — miễn phí, Windows, không cần biết gì về server.

1. Cài LocalWP → `Create a new site` → đặt tên `vitalite` → chọn **Preferred** (PHP 8.x)
2. Site chạy xong → `WP Admin` → cài **WooCommerce**
3. Copy thư mục `vitalite-theme` vào `.../Local Sites/vitalite/app/public/wp-content/themes/`
   *(LocalWP có nút `Go to site folder`)*
4. Cài theme cha **Hello Elementor** *(bắt buộc — đây là child theme)*
5. Kích hoạt `Vitalité Theme`
6. Tạo 2 sản phẩm test, đặt ảnh product image + gallery, xem thử

**Đây là cách đúng để kiểm mọi thứ trước khi lên production.** Hỏng cũng không sao —
không ai thấy, xoá đi tạo lại là xong.

> Muốn giống production hơn nữa: dùng UpdraftPlus export bản backup rồi import vào LocalWP.
> Lúc đó có đúng plugin, đúng dữ liệu, đúng cấu hình.

### C. Subdomain staging trên cPanel

`cPanel → Subdomains` → tạo `staging.vitalite.io.vn` → cài WordPress vào đó.
Chậm hơn LocalWP và tốn dung lượng hosting, nhưng chạy đúng môi trường LiteSpeed thật.

Nếu zhost.vn có công cụ **WP Staging** hay **Softaculous Staging** thì dùng nó — nó tự nhân bản site.

---

## Cách an toàn nhất: upload thư mục mới song song

**Không ghi đè lên thư mục theme đang chạy.** Upload thành thư mục thứ hai, đổi theme
trong wp-admin, xem thử, hỏng thì bấm đổi ngược lại. Đổi theme trong WordPress là
tức thời và không mất dữ liệu.

### ✅ Bước 0 — DỌN THEME · ĐÃ LÀM XONG 2026-08-21

Không phải làm gì nữa. Ghi lại để biết chuyện gì đã xảy ra.

**Theme: 122MB → 5.8MB.** Nén zip giờ mất vài giây.

Đã **chuyển** (không xoá) ra `repo/vitalite-website/_not-in-theme/`:

| File | Size | Vì sao |
|---|---|---|
| `video-masters/260417_VTL_PROMO_02.mp4` | 63.2MB | master |
| `video-masters/260418_VTL_CB.mp4` | 33.2MB | master |
| `video-masters/260418_VTL_CB_optimized.mp4` | 6.2MB | **không được reference ở đâu** |
| `video-masters/260417_VTL_PROMO_02_optimized.mp4` | 17.8MB | bản cũ, đã thay bằng `hero-1280` |
| `product-images-unused/*.png` (17 file) | 5.4MB | **không được reference ở đâu** |

Còn lại trong theme, đây là toàn bộ video ship cho khách:

```
video/hero-1280.mp4     2.43 MB   x264 CRF 30, 8s, không audio, +faststart
video/hero-1280.webm    1.66 MB   VP9 CRF 46
```

Thư mục `_not-in-theme/` đã được `.gitignore` — không bao giờ commit.
Muốn lấy lại file nào thì `mv` ngược lại.

### 🔴 Trên production CŨNG phải dọn

Bản deploy cũ nhiều khả năng vẫn còn hai file master ở
`public_html/wp-content/themes/vitalite-theme/video/`. Chúng ăn ~96MB dung lượng
hosting mà không phục vụ ai.

Quy trình song song bên dưới sẽ tạo thư mục theme MỚI, nên thư mục cũ vẫn còn nguyên
cả rác. Sau khi xác nhận theme mới chạy ổn, xoá luôn thư mục theme cũ qua File Manager.

---

### ✅ Bước 1 — nén ở máy · ĐÃ LÀM XONG 2026-08-30

Zip đã dựng sẵn ở gốc project:

```
E:\Vitalite website\vitalite-theme-2.zip     5,5 MB · 55 file
```

Dựng lại khi có sửa theme:

```bash
cd "E:/Vitalite website"; python docs/build-theme-zip.py
```

Script tự bỏ `.DS_Store`, `Thumbs.db`, `.log`, `.pyc`, `.map`, `node_modules`, `.git`.
Nó cũng in ra mọi file trên 500 KB để không bao giờ lọt file nặng vào zip mà không ai biết.
Hiện chỉ có hai, đều đúng chỗ: `video/hero-1280.mp4` 2,32 MB và `video/hero-1280.webm` 1,59 MB.

> ⚠️ **Thư mục trong zip tên là `vitalite-theme-2`, không phải `vitalite-theme`.**
> Đây là chủ ý, xem bước 2. Đừng đổi tên nó.

---

### Bước 1b — kiểm trước khi upload

Hai thứ phải đúng, nếu không thì kích hoạt theme sẽ lỗi.

**1. Theme cha `hello-elementor` phải có trên production.**
`wp-admin → Giao diện → Giao diện`, tìm **Hello Elementor** trong danh sách.
Không có thì cài trước: `Thêm mới → tìm "Hello Elementor" → Cài đặt`. **Không cần kích hoạt nó.**
`style.css` khai `Template: hello-elementor` — thiếu cha là WordPress từ chối kích hoạt con.

**2. Ghi lại tên theme đang chạy.**
`Giao diện → Giao diện`, theme nào đang "Đang kích hoạt". Ghi ra giấy.
Đây là thứ để quay về ở bước 5.

---

### Bước 2 — upload

`cPanel → File Manager → public_html/wp-content/themes/`

1. **Upload** `vitalite-theme-2.zip`
2. Chuột phải → **Extract**
3. Xoá file `.zip` sau khi giải nén xong

**Không phải đổi tên gì cả, và không có prompt ghi đè.** Thư mục mới tên `vitalite-theme-2`,
thư mục đang chạy tên `vitalite-theme` — hai tên khác nhau nên chúng nằm cạnh nhau, không đụng nhau.
Theme đang chạy **không bị động tới một byte nào**.

```
public_html/wp-content/themes/
├── hello-elementor/        ← theme cha
├── vitalite-theme/         ← ĐANG CHẠY, không đụng vào
└── vitalite-theme-2/       ← vừa upload
```

> Bản DEPLOY cũ bảo đổi tên thư mục đang chạy thành `vitalite-theme-old` rồi mới Extract.
> **Không cần nữa, và đừng làm.** Đổi tên thư mục của theme đang kích hoạt là site trắng ngay
> lập tức cho tới khi extract xong. Tên khác nhau thì không có khoảng thời gian nào site hỏng.

---

### Bước 3 — kích hoạt

`wp-admin → Giao diện → Giao diện`

Sẽ thấy **hai** theme cùng tên "Vitalité Theme". Phân biệt bằng số phiên bản — bản mới là
**2.0.0**. Bấm chuột lên từng cái để xem chi tiết nếu không chắc.

Kích hoạt bản `2.0.0`.

### Bước 4 — xem thử ngay

| Kiểm | Đường dẫn |
|---|---|
| Trang chủ | `/` — hero video, header trong suốt rồi chuyển trắng khi cuộn |
| Shop | `/shop` |
| Giỏ hàng | `/cart` |
| Thanh toán | `/checkout` |
| Tài khoản | `/my-account` |
| Tìm kiếm | bấm SEARCH trên header |
| 404 | `/khong-ton-tai-abc` |
| Mobile | thu nhỏ cửa sổ dưới 768px, mở menu |

### Bước 5 — hỏng thì lùi

`Giao diện → Giao diện` → kích hoạt lại theme cũ. Xong. Không mất gì.

### Bước 6 — ổn rồi thì dọn

Sau khi chạy ổn **vài ngày**, không phải vài phút:

1. Xoá thư mục `vitalite-theme` cũ qua File Manager.
   🔴 Bản cũ nhiều khả năng còn hai file video master trong `video/`, ăn **~96 MB** dung lượng
   hosting mà không phục vụ ai. Xoá cả thư mục là xong luôn.
2. Kiểm lại `/` và `/shop` một lần nữa sau khi xoá.

> Đừng xoá sớm. Thư mục cũ chính là đường lùi ở bước 5.

---

## Bước 7 — bảo vệ nội dung (sau khi site đã chạy ổn)

Sửa `.htaccess` để chống hotlink ảnh, tắt liệt kê thư mục, chặn công cụ clone cả site,
khoá file nhạy cảm. Snippet đầy đủ + 5 bước kiểm sau khi lưu:
**`deliverables/setup/BAO-VE-NOI-DUNG.md`**

🔴 **Làm sau khi site đã chạy ổn, không làm cùng lúc với deploy.** `.htaccess` hỏng là site
trả lỗi 500 trắng trơn, và nếu làm cùng lúc thì không biết lỗi đến từ theme hay từ `.htaccess`.

🔴 **Copy `.htaccess` hiện tại ra file text trên máy trước khi sửa.**

Cái này đặc biệt cần cho `wp-content/uploads/seq/0823/` — 99 file chuỗi frame. Không tắt liệt kê
thư mục thì mở URL đó ra là thấy nguyên danh sách, tải hàng loạt trong một lệnh.

---

## Về sau: dùng FTP thay File Manager

File Manager ổn cho một lần upload lớn. Sửa lặt vặt hằng ngày thì FTP nhanh hơn nhiều.

### Cài đặt

1. Tải **FileZilla Client** (miễn phí)
2. `cPanel → FTP Accounts` → tạo tài khoản mới
   - Directory: `public_html/wp-content/themes/vitalite-theme`
   - ⚠️ **Giới hạn thư mục là điểm quan trọng nhất.** Kể cả lộ mật khẩu thì cũng chỉ
     chạm được thư mục theme — không chạm được `wp-config.php`, không chạm được database.
     Đó là lý do nó **an toàn hơn** dùng tài khoản cPanel chính.
3. FileZilla → `File → Site Manager → New Site`

```
Protocol:    FTP
Host:        ftp.vitalite.io.vn
Port:        21
Encryption:  Require explicit FTP over TLS     ← BẮT BUỘC
Logon Type:  Normal
User / Pass: tài khoản vừa tạo
```

> ⚠️ **Encryption phải là "Require explicit FTP over TLS".** Để `Plain FTP` là gửi
> mật khẩu dưới dạng chữ thường qua mạng. Nếu zhost.vn không hỗ trợ FTPS thì
> quay lại dùng File Manager — File Manager chạy qua HTTPS nên vẫn được mã hoá.

### Dùng hằng ngày

Sửa file ở máy → kéo từ khung trái sang khung phải. FileZilla hỏi ghi đè, chọn
**Overwrite if source newer**.

---

## Checklist sau mỗi lần deploy

- [ ] Xoá cache LiteSpeed (`LiteSpeed Cache → Toolbox → Purge All`)
- [ ] Xoá cache Elementor (`Elementor → Tools → Regenerate CSS`)
- [ ] Ctrl+F5 trên trình duyệt
- [ ] Xem trang chủ, shop, một PDP, giỏ hàng
- [ ] Xem trên điện thoại thật, không chỉ thu nhỏ cửa sổ
- [ ] Kiểm Console trình duyệt xem có lỗi JS đỏ không

---

## Nếu site trắng trơn sau khi đổi theme

Lỗi PHP. Không hoảng — làm theo thứ tự:

1. `cPanel → File Manager` → đổi tên `vitalite-theme` thành `vitalite-theme-broken`
   → WordPress tự rơi về theme mặc định, site sống lại
2. Bật hiện lỗi để biết hỏng ở đâu — thêm vào `wp-config.php`:
   ```php
   define('WP_DEBUG', true);
   define('WP_DEBUG_LOG', true);
   define('WP_DEBUG_DISPLAY', false);
   ```
3. Lỗi ghi vào `wp-content/debug.log`. Mở ra đọc dòng đầu tiên.
4. Gửi dòng đó cho Claude.
5. **Tắt `WP_DEBUG` lại sau khi xong.** Để bật trên production là rò thông tin hệ thống.
