# PERFORMANCE — quyết định đã có trong code, và việc còn lại
**Ngày:** 2026-08-20 · **Mục tiêu:** LCP < 2.5s trên mobile

---

## Vì sao đây là ràng buộc chứ không phải mong muốn

Site fashion chết vì trọng lượng ảnh. Với vitalité còn thêm hai yếu tố:
khách quốc tế (xa server hơn) và shared hosting (TTFB không kiểm soát được).
Nên mọi thứ tiết kiệm được ở tầng front-end đều là thật.

---

## 1. Đã làm sẵn trong code

| Việc | Ở đâu | Tại sao |
|---|---|---|
| **Bỏ `@import` font trong CSS** | `style.css` | `@import` bắt browser tải xong CSS mới biết cần tải font → hai request nối tiếp. Giờ font nạp bằng `<link>` + `preconnect` |
| **Preconnect tới font host** | `inc/enqueue.php` | bắt tay TLS chạy song song thay vì chờ |
| **`display=swap`** | `inc/enqueue.php` | chữ hiện ngay bằng font dự phòng, không có khoảng trắng chờ font |
| **Chỉ nạp weight thật sự dùng** | `inc/enqueue.php` | Archivo 400/500/600/800, Expanded 800, Mono 400/500 |
| **Preload ảnh poster hero** | `inc/enqueue.php` | poster là phần tử LCP của trang chủ. Preload **đúng một ảnh** — preload nhiều thứ là tự cạnh tranh băng thông |
| **Poster là `<img>` chứ không phải CSS background** | `template-parts/hero.php` | background-image chỉ được phát hiện sau khi parse CSS, và không đặt được `fetchpriority` |
| **Video `preload="none"`, source gắn bằng JS** | `hero.php` + `site.js` | video **không được** tranh băng thông với poster |
| **Không tải video trên mobile / saveData / mạng chậm** | `site.js` | người Việt xem điện thoại, 4G tính tiền. Poster đủ đẹp |
| **WebM đứng trước MP4** | `hero.php` | nhẹ hơn ~30–40% cùng chất lượng |
| **Video tạm dừng khi cuộn khỏi hero** | `site.js` | không giải mã video mà không ai xem |
| **Bỏ lazy cho 2 ảnh đầu mỗi trang** | `inc/enqueue.php` | WordPress lazy gần như mọi ảnh; ảnh trên màn hình đầu mà lazy thì hại LCP |
| **Không nạp CSS/JS WooCommerce ở trang không cần** | `inc/enqueue.php` | Woo mặc định nạp ở **mọi** trang, kể cả About — ~90KB lãng phí |
| **Bỏ `wc-cart-fragments`** | `inc/enqueue.php` | request AJAX chạy trên **mọi** lượt xem trang và **phá cache**. Số giỏ hàng đã cập nhật qua `add_to_cart_fragments`, chỉ chạy khi thật sự thêm hàng |
| **Bỏ `wp-block-library`** | `inc/enqueue.php` | ~30KB CSS block editor không dùng tới |
| **`IntersectionObserver` thay `scroll` listener** | `site.js` | scroll listener chạy hàng chục lần mỗi giây |
| **Iridescent dừng khi ra khỏi màn hình** | `site.js` | 4 lớp gradient bị blur là thứ tốn fill-rate nhất |
| **`contain: paint` trên hero và band** | `style.css` | giới hạn vùng browser phải vẽ lại |
| **`width`/`height` tường minh trên mọi ảnh** | mọi template | không có là **CLS** — layout nhảy khi ảnh tải xong |
| **`aspect-ratio` trên khung ảnh** | `style.css` | giữ chỗ trước khi ảnh về |
| **Tắt zoom PDP** | `inc/setup.php` | mockup chỉ 1000px; zoom vào chỉ phóng to điểm ảnh, mà vẫn tốn JS |
| **Ảnh mặt sau ẩn hẳn trên cảm ứng** | `style.css` | `@media (hover: none) { display: none }` — không tải, không chiếm chỗ |
| **`prefers-reduced-motion`** | `style.css` + `site.js` | |

---

## 2. Ngân sách trang

| Trang | Ngân sách | Ghi chú |
|---|---|---|
| Trang chủ | **< 1.5MB** chưa tính video | poster 38KB + 8 ảnh sản phẩm + editorial 76KB |
| Shop archive | **< 1.2MB** | 12 sản phẩm × 2 ảnh (trước/sau) |
| PDP | **< 1MB** | |
| CSS | **< 20KB** nén | theme hiện ~14KB thô |
| JS của theme | **< 6KB** | `site.js` ~5KB, không thư viện |

**Ảnh mỗi sản phẩm sau khi chuyển WebP: ~20KB.** Đã đo trên bộ mockup thật:
`5.61MB → 359KB` cho 18 ảnh, giảm 94%.

---

## 3. Còn phải làm

### 🔴 Video hero — việc lớn nhất còn lại
17MB. Cần nén xuống ≤ 2.5MB MP4 + 1.5MB WebM. Lệnh trong `deliverables/video/encode.md`.
Cần `ffmpeg`: `winget install Gyan.FFmpeg`.

### 🔴 Ảnh sản phẩm phải là WebP trước khi upload
Đã có sẵn bản chuyển: `mockup-all/webp/` (18 file, 359KB).
**Upload bản WebP, không upload bản PNG.** LiteSpeed có tính năng chuyển WebP nhưng
chuyển sẵn ở máy thì chắc chắn hơn và không tốn CPU server.

### 🟡 Logo nên là SVG
Hiện là PNG 995×994, ~13KB. SVG cùng hình chỉ ~2KB, sắc nét ở mọi mật độ điểm ảnh,
và `fill: currentColor` giải quyết luôn bài toán đảo màu trên nền tối
(hiện đang phải dùng `filter: invert(1)`).
User chỉ có PNG → cần vector hoá hoặc xin file gốc `.ai`.

### 🟡 Font — cân nhắc self-host
Google Fonts là một origin thứ ba: thêm DNS + TLS + request.
Self-host tiết kiệm ~100–200ms ở lượt truy cập đầu.
**Nhưng** phải tự lo subset và định dạng woff2 — thêm việc bảo trì.
Khuyến nghị: **để Google Fonts trước**, đo bằng WebPageTest, nếu font thật sự nằm
trên đường tới LCP thì mới self-host.

### 🟡 `Archivo Expanded` — kiểm tra có thật không tải nặng
Font display chỉ dùng cho `<h1>` hero và vài heading. Nếu WebPageTest cho thấy
nó chặn render thì cân nhắc bỏ, dùng `Archivo` weight 800 với `font-stretch`.

---

## 4. Bẫy hay gặp — đừng làm

| ❌ | Vì sao |
|---|---|
| Bật minify CSS/JS trong LiteSpeed | xung đột Elementor. Đã chốt. Lợi ích ~0 vì CSS chỉ 14KB và server đã gzip |
| Bật lazy load ảnh của plugin cache | đè lên `loading="lazy"` của core và **hại LCP** vì ảnh hero phải chờ JS |
| Cài plugin tối ưu thứ hai | hai cache chồng nhau là lỗi khó tìm nhất trong WordPress |
| Bật CDN lúc chưa có traffic | thêm biến số vào lúc cần môi trường sạch để debug |
| Preload nhiều tài nguyên | preload nhiều = tự cạnh tranh băng thông với chính mình |
| Carousel above the fold | mỗi slide là một ảnh phải tải, mà khách chỉ thấy slide đầu |
| Upload video qua thư viện WordPress | video không nên đi qua PHP. Để trong theme hoặc dùng dịch vụ ngoài |

---

## 5. Đo thế nào

### Trước khi đổi bất cứ thứ gì
Đo bản hiện tại và **ghi số lại**. Không có số gốc thì không biết mình cải thiện hay làm tệ đi.

### Công cụ

| | Đo gì | Lưu ý |
|---|---|---|
| PageSpeed Insights | LCP, CLS, INP | **xem tab Mobile.** Desktop cáp quang thì trang nào cũng đẹp |
| WebPageTest | waterfall | thấy được thứ gì chặn thứ gì — đây là công cụ hữu ích nhất |
| Chrome DevTools → Network | dung lượng thật | bật throttling `Fast 3G` |
| Chrome DevTools → Performance | main thread | tìm long task |

### Ba trang phải đo
```
/            trang chủ — nặng nhất, có video
/shop        lưới sản phẩm — nhiều ảnh nhất
/product/…   PDP — trang quyết định mua
```

### Cách đọc LCP
DevTools → Performance → tick **Web Vitals** → tìm nhãn `LCP`.
Nó chỉ đúng vào phần tử đang là LCP. Nếu **không phải** ảnh poster hero
trên trang chủ thì có gì đó sai — poster phải là LCP.

---

## 6. Sau khi launch

| Việc | Tần suất |
|---|---|
| PageSpeed Insights 3 trang chính | hằng tháng |
| Kiểm Core Web Vitals trong Search Console | hằng tháng — đây là **số liệu người dùng thật**, khác với số đo trong phòng thí nghiệm |
| Xem dung lượng ảnh sản phẩm mới nhập | mỗi đợt nhập hàng |
| Dọn database LiteSpeed | mỗi quý |
| Kiểm SSL còn hạn | mỗi quý |

> Search Console → Core Web Vitals là nguồn duy nhất phản ánh **khách thật, máy thật,
> mạng thật**. PageSpeed Insights chỉ là mô phỏng. Khi hai bên lệch nhau, tin Search Console.
