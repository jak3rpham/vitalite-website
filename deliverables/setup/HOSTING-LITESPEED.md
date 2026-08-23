# HOSTING & LITESPEED CACHE
**Ngày:** 2026-08-20 · shared cPanel zhost.vn · LiteSpeed · PHP 8.3 · DB prefix `vtl_`

---

## 1. PHP

`cPanel → Select PHP Version`

| | Đặt | Vì sao |
|---|---|---|
| Phiên bản | **8.3** ✅ đang đúng | |
| `memory_limit` | `256M` | WooCommerce + Elementor cùng lúc ăn hơn 128M khi lưu trang |
| `max_execution_time` | `120` | import sản phẩm và backup cần thời gian |
| `upload_max_filesize` | `64M` | đủ cho ảnh; video **không upload qua WordPress** |
| `post_max_size` | `64M` | phải ≥ upload_max_filesize |
| `max_input_vars` | `3000` | Elementor lưu trang phức tạp sẽ **âm thầm mất dữ liệu** nếu giá trị này thấp |

**Extension cần bật:** `imagick` (hoặc `gd`), `intl`, `zip`, `curl`, `mbstring`, `opcache`.

> `opcache` là thứ tăng tốc lớn nhất mà không tốn gì. Nếu chưa bật, bật.

---

## 2. LiteSpeed Cache — cấu hình chi tiết

`wp-admin → LiteSpeed Cache`

### 🔴 Quy tắc quan trọng nhất

```
Page Optimization → CSS Settings → CSS Minify        = OFF
Page Optimization → JS Settings  → JS Minify         = OFF
Page Optimization → CSS/JS Combine                   = OFF
```

**Minify CSS/JS xung đột với Elementor.** Đây là quyết định đã chốt trong CLAUDE.md.
Elementor sinh CSS động theo từng trang; minify/combine làm hỏng thứ tự và gây lỗi
layout ngẫu nhiên, rất khó tìm vì nó chỉ xuất hiện sau khi cache được sinh.

Lợi ích của minify với site này gần như bằng 0: CSS của theme chỉ ~14KB, và server
đã nén gzip/brotli rồi.

### Cache

| Mục | Đặt |
|---|---|
| Enable Cache | ✅ ON |
| Cache Logged-in Users | ❌ OFF |
| Cache Commenters | ❌ OFF |
| Cache REST API | ✅ ON |
| Cache Login Page | ✅ ON |
| Cache Mobile | ❌ OFF — theme responsive, một bản HTML dùng chung |

### Purge

| Mục | Đặt |
|---|---|
| Purge All On Upgrade | ✅ ON |
| Auto Purge Rules | giữ mặc định |
| Serve Stale | ✅ ON — khách vẫn nhận bản cũ trong lúc bản mới đang sinh, thay vì phải chờ |

### Excludes — 🔴 BẮT BUỘC

`Cache → Excludes → Do Not Cache URIs`, mỗi dòng một mục:

```
/cart
/checkout
/my-account
```

**Cache trang giỏ hàng là lỗi kinh điển và hậu quả rất nặng:** khách A tải `/cart`,
bản HTML đó vào cache, khách B vào `/cart` và **thấy giỏ hàng của khách A**.
WooCommerce thường tự loại trừ, nhưng phải khai tay để chắc chắn.

`Do Not Cache Cookies`:
```
woocommerce_items_in_cart
woocommerce_cart_hash
wp_woocommerce_session_
```

`Do Not Cache Query Strings`:
```
add-to-cart
```

### Ảnh

| Mục | Đặt | Ghi chú |
|---|---|---|
| Image WebP Replacement | ✅ ON | tự phục vụ WebP cho browser hỗ trợ |
| Optimize Original Images | ✅ ON | |
| Auto Request Cron | ✅ ON | |
| Preserve EXIF | ❌ OFF | metadata máy ảnh không cần cho khách, chỉ làm nặng file |
| Lazy Load Images | ⚠️ **OFF** | WordPress core đã có `loading="lazy"`. Lazy load bằng JS của plugin đè lên là **hại LCP** vì ảnh hero phải chờ JS chạy |
| Lazy Load Iframes | ✅ ON | |

### Tuning

| Mục | Đặt |
|---|---|
| Font Display Optimization | `Swap` |
| Remove WordPress Emoji | ✅ ON — theme cũng đã gỡ, bật thêm không hại |
| Remove Noscript Tags | ❌ OFF |

### Database

`Database → Manage` — chạy tay mỗi vài tháng, **không** đặt lịch tự động:
- Post Revisions
- Auto Drafts
- Trashed Posts
- Spam Comments
- Expired Transients

### QUIC.cloud CDN

⚠️ **Chưa bật vội.** Cân nhắc lại sau khi có traffic thật.

Lý do: CDN chỉ đáng giá khi khách ở xa server. Định hướng site là khách quốc tế —
nên **nó sẽ đáng giá**, nhưng chỉ đo được sau khi có khách thật.
Bật CDN lúc chưa có traffic là thêm một biến số vào lúc đang cần môi trường sạch để debug.

---

## 3. Video — KHÔNG để trong theme lâu dài

> ✅ **ĐÃ LÀM XONG 2026-08-21.** Kết quả thật + SSIM đo được: `deliverables/video/encode.md`.
> Theme giờ ship `video/hero-1280.mp4` (2.43MB) + `video/hero-1280.webm` (1.66MB).
> ⚠️ Lệnh WebM ghi bên dưới dùng **CRF 38 — SAI**, nó ra file 2.88MB, LỚN HƠN bản MP4.
> Dùng **CRF 46**. Phần dưới giữ lại làm tham chiếu lịch sử.

Hiện tại (trước khi nén): `260417_VTL_PROMO_02_optimized.mp4` = **17MB**, trong thư mục theme.

**Vấn đề:**
- 17MB/lượt xem trên shared hosting là ăn hết băng thông rất nhanh
- Nằm trong theme nghĩa là mỗi lần deploy theme phải upload lại 17MB

**Cần làm (xem `deliverables/video/encode.md`):**

```bash
# Cắt 8 giây, bỏ audio, hạ 1280px
ffmpeg -i 260417_VTL_PROMO_02.mp4 -t 8 -an -vf "scale=1280:-2" \
  -c:v libx264 -crf 30 -preset slow -profile:v main -pix_fmt yuv420p \
  -movflags +faststart hero-1280.mp4

ffmpeg -i 260417_VTL_PROMO_02.mp4 -t 8 -an -vf "scale=1280:-2" \
  -c:v libvpx-vp9 -crf 38 -b:v 0 -row-mt 1 hero-1280.webm
```

**Mục tiêu:** MP4 ≤ 2.5MB · WebM ≤ 1.5MB. Vượt thì cắt xuống 5 giây.

~~Đổi tên thành `260417_VTL_PROMO_02_optimized.mp4`~~ → theme giờ tìm `hero-1280.mp4` / `.webm` —
`template-parts/hero.php` dò đúng hai tên đó, và ưu tiên WebM.

> `ffmpeg` chưa cài trên máy user: `winget install Gyan.FFmpeg` rồi mở terminal mới.

**Nếu video quan trọng với brand:** cân nhắc Cloudflare Stream hoặc Bunny (~$1–5/tháng).
Băng thông shared hosting là giới hạn thật, không phải lo xa.

---

## 4. Bảo mật ở tầng hosting

### SSL
✅ Let's Encrypt đã cài cho root + www.
🔴 **Cần xác minh tự động gia hạn.** Let's Encrypt hết hạn sau 90 ngày.
`cPanel → SSL/TLS Status` → xem cột ngày hết hạn và trạng thái AutoSSL.
Đặt nhắc lịch kiểm tra hằng quý.

### Bắt buộc HTTPS
`cPanel → Domains → Force HTTPS Redirect` = ON.

### Chặn XML-RPC ở tầng server
Theme đã tắt bằng filter PHP, nhưng chặn ở `.htaccess` thì request không tới PHP —
tiết kiệm CPU thật trên shared hosting:

```apache
<Files xmlrpc.php>
  Require all denied
</Files>
```

### Bảo vệ file nhạy cảm
Thêm vào `.htaccess` trong `public_html`:

```apache
# wp-config.php
<Files wp-config.php>
  Require all denied
</Files>

# Không cho liệt kê thư mục
Options -Indexes

# Chặn thực thi PHP trong thư mục uploads.
# Đây là đường tấn công phổ biến nhất: upload file .php trá hình rồi gọi thẳng.
<Directory "wp-content/uploads">
  <FilesMatch "\.(php|php5|php7|phtml)$">
    Require all denied
  </FilesMatch>
</Directory>
```

> ⚠️ Sửa `.htaccess` sai là **site trả lỗi 500 ngay lập tức**.
> Tải bản gốc về máy trước khi sửa. Hỏng thì upload lại bản gốc là xong.

### Đăng nhập
- Không dùng username `admin`
- Mật khẩu do trình quản lý mật khẩu sinh
- Bật 2FA nếu cPanel hỗ trợ

---

## 5. Đo trước và sau

**Trước khi đổi bất cứ thứ gì, đo bản hiện tại.** Không có số gốc thì không biết
mình cải thiện hay làm tệ đi.

| Công cụ | Đo gì |
|---|---|
| PageSpeed Insights | LCP, CLS, INP — **xem tab Mobile, không phải Desktop** |
| WebPageTest | waterfall — thấy được thứ gì chặn thứ gì |
| GTmetrix | tổng dung lượng trang |

**Mục tiêu:**

| | Ngưỡng | Ở đâu |
|---|---|---|
| LCP | < 2.5s | trang chủ, shop, PDP |
| CLS | < 0.1 | mọi trang |
| INP | < 200ms | |
| Tổng dung lượng trang chủ | < 1.5MB | chưa tính video |

Đo trên **mobile, mạng chậm mô phỏng**. Đo trên desktop cáp quang thì trang nào cũng đẹp.
