# ASSUMPTIONS.md

> Mọi giả định đã dùng khi `BRAND_CONTEXT.md` và `BRAND_GUIDELINE.md` chưa tồn tại.
> **Khi 2 file đó được upload: tất cả bên dưới VÔ HIỆU và phải kiểm lại từng dòng.**

Cập nhật lần cuối: 2026-08-19

---

## A. Visual identity — lấy từ code hiện tại, CHƯA phải guideline đã chốt

| Giả định | Nguồn | Trạng thái |
|---|---|---|
| Màu tối `#0A0A0A` | `style.css` `--vt-bg-dark` | ⚠️ suy ra từ code |
| Màu sáng `#F4F4F4` | `style.css` `--vt-bg-light` | ⚠️ suy ra từ code |
| Font body: Archivo | `style.css` `--vt-font-primary` | ⚠️ suy ra từ code |
| Font display: Archivo Expanded | `style.css` `--vt-font-display` | ⚠️ suy ra từ code |
| Font mono: JetBrains Mono | `style.css` `--vt-font-mono` | ⚠️ suy ra từ code |
| Header height 76px desktop / 64px mobile | `header-woocommerce.php` | ⚠️ suy ra từ code |
| Đỏ badge `#E0202A` | **Claude tự chọn** | 🔴 **PLACEHOLDER — cần mã thật** |

**Lưu ý quan trọng:** các giá trị này đến từ theme do Antigravity sinh ra, không phải từ một brand guideline được duyệt. Có thể chúng đúng, có thể chúng chỉ là default. Phải xác nhận.

---

## B. Quyết định thiết kế Claude tự đưa ra (cần user duyệt)

| Quyết định | Lý do | Trạng thái |
|---|---|---|
| Hover = tăng contrast, không đổi hue | Không bao giờ chìm ở bất kỳ mode nào | ✅ user đồng ý ngầm (chưa phản đối) |
| Badge đỏ giữ nguyên ở cả 2 mode | Badge là signal, không phải trang trí | ✅ user yêu cầu "traditional trắng trên tròn đỏ" |
| Cart rỗng → ẩn số hoàn toàn | User yêu cầu rõ | ✅ chốt |
| Search/Account: mono 600 @ 12px, tracking .09em | Mono 400@11px trên blur quá mảnh | ⚠️ chưa xem kết quả thật |
| Language switcher text `EN / VI`, không cờ | Cờ = quốc gia ≠ ngôn ngữ | ⚠️ Claude đề xuất |
| Icon cart: outline shopping bag, stroke 1.6 | Hợp tông minimalist | ⚠️ Claude tự vẽ, có thể thay |

---

## C. Giả định về hạ tầng

| Giả định | Trạng thái |
|---|---|
| Hosting shared cPanel zhost.vn, LiteSpeed | ✅ đã xác nhận trước đó |
| PHP 8.3 | ✅ |
| DB prefix `vtl_` | ✅ |
| Currency VND | ✅ |
| Theme `vitalite-theme` đang active trên production | ✅ user xác nhận |
| Parent theme = Hello Elementor | ✅ xác nhận qua `style.css` header |

---

## D. KHOẢNG TRỐNG — chưa có, không được điền đại

- ✅ **ĐÃ GIẢI QUYẾT (user xác nhận 2026-08-19): copy hero + tên sản phẩm + giá là BỊA HẾT.**
  `cotton 480GSM` · `in lụa thủ công` · `form rộng` · `phát hành chính thức 20.08` ·
  `SS26` · `Sống Hết Công Suất` · `Heavyweight Hoodie 480GSM` · `1.290.000₫`
  → Nguồn: prototype Claude Design (`Vitalite Homepage.dc.html`), lọt vào theme khi dịch sang PHP.
  → **Không giữ dòng nào.** Bản thay thế: `deliverables/copy/hero-clean.md` (chưa áp dụng, chờ backup).
  → `homepage-woocommerce.php` hardcode array sản phẩm → lỗi kiến trúc, xử lý ở bước 7.

- ✅ **`#vtSearchModal` KHÔNG TỒN TẠI** (xác nhận 2026-08-19).
  `header-woocommerce.php:270` gọi `getElementById('vtSearchModal')?.classList.toggle()`.
  Grep toàn repo: 1 hit duy nhất, chính là dòng gọi. `?.` nuốt lỗi → nút SEARCH là click chết trên production.
  → Fix tạm: trỏ `href` sang `home_url('/?s=&post_type=product')`. Modal gộp vào batch JS bước 4.

- ✅ **`support.js` đã audit** (2026-08-19). Là `dc-runtime` — runtime React của Claude Design canvas,
  build từ TypeScript. **Không liên quan gì đến WordPress theme.** Rác prototype, cùng nhóm với
  `Vitalite Homepage.dc.html` và `uploads/`.

- ✅ **Logo là ĐEN TUYỀN 100%** (đo 2026-08-19, Pillow, 4 file PNG trong `assets/`).
  `#000000`, sat=0.00, alpha mask. **Brand mark là monochrome — không trích được đỏ từ logo.**
  → `--vt-badge-red` không có nguồn nào trong repo. Bắt buộc user cung cấp, hoặc lấy từ Shopee/social.

- ⬜ Bảng size / số đo — **chưa có, tuyệt đối không tự tạo**
- ⬜ Chính sách ship / đổi trả / bảo hành — **chưa có, không viết như đã chốt**
- ⬜ Giá và price tier
- ⬜ Danh mục sản phẩm chính thức (hiện thấy: Áo/Tops, Quần — chưa rõ đầy đủ)
- ⬜ Số SKU hiện tại (repo có 17 ảnh sản phẩm, **không suy ra được 17 SKU**)
- ⬜ Tỷ lệ khách VN vs quốc tế
- ⬜ Baseline hiệu quả Shopee
- ⬜ Lý do khách chọn site thay vì Shopee
- ⬜ Năng lực chụp ảnh mỗi SKU
- ⬜ Logo behavior rules (clear space, min size, biến thể)
- ⬜ Photography direction (model vs flatlay, tỷ lệ, tông màu)

---

## E. Chưa audit

- ~~`support.js`~~ ✅ audit xong 2026-08-19 — là dc-runtime, không liên quan theme
- `footer-elementor.php` — chưa đọc kỹ
- `homepage-woocommerce.php` — đã thấy hardcode sản phẩm, chưa đọc hết
- `Vitalite Homepage.dc.html` — đã xác định là prototype, không cần audit sâu

---

## F. Brand audit qua nguồn ngoài — ✅ ĐÃ LÀM 2026-08-19

Đã xem trực tiếp: Facebook `/vitalitevn` · Instagram `@vitalitevn` · Shopee `shopee.vn/vitalitevn`.
**Kết quả đầy đủ: `reference/BRAND_FACTS_OBSERVED.md`.**

Những giả định bị vô hiệu ngay:

| Trước | Sau |
|---|---|
| Tên brand `Vitalite` | **`VITALITÉ ®`** — có dấu, có ® |
| `cotton 480GSM` | **Cotton 250gsm** |
| size S/M/L | **1 / 2 / 3** |
| giá 450k–1.45tr | **276k–599k** |
| "17 ảnh, không suy ra 17 SKU" | **10 SKU trên Shopee**, 2 danh mục: T-SHIRT / OUTER WEAR |
| "chưa có bảng size" | **✅ CÓ — bảng số đo thật, đã ghi lại nguyên văn** |
| "chưa có chính sách đổi trả" | **✅ CÓ — 5 ngày, 1 lần/đơn, khách chịu ship 2 chiều** |
| "chưa rõ lý do mua trên site" | **✅ Trả lời được: khách quốc tế.** IG 7k follower, bio ghi "Worldwide shipping", Shopee.vn không phục vụ quốc tế |
| "cần đăng ký kinh doanh cho payment" | Shopee hiển thị **Công Ty/HKD đã đăng ký** → rào cản có thể nhỏ hơn tưởng |

Vẫn thiếu:
- Mã đỏ chính thức (logo đen tuyền; đỏ chỉ thấy trên print sản phẩm, không lấy hex từ ảnh chụp được)
- Spec + size của `THE MOMENTS BOXY HOODIE`
- 3/10 SKU chưa liệt kê được
- Chính sách vận chuyển (đặc biệt: ship quốc tế thật ra sao)

---

## G. ĐỔI CHỦ — phát hiện 2026-08-19, làm vô hiệu một phần mục F

User cho biết brand **đã đổi chủ**. Đối chiếu lại: dữ liệu Shopee và dữ liệu IG
**không cùng một brand direction** — hai thời kỳ khác nhau.

👉 **`reference/BRAND_ERA_SPLIT.md`**

Ba thứ trong tài liệu trước phải đọc lại:

| Đã ghi | Thực tế |
|---|---|
| Hệ size `1 / 2 / 3` | Đó là thời kỳ CŨ. Thời kỳ mới dùng **`S / M / L`** — 🔴 **chưa có bảng cm** |
| `--vt-accent: #CA2058` hồng | Hồng là màu thời kỳ CŨ. Thời kỳ mới: **xanh dương + tím** 🖤💜 — chưa có mã |
| `480GSM` = bịa hoàn toàn | Áo thun **250 GSM**, áo khoác **500+ GSM**. Gắn sai sản phẩm, nhưng 500+ GSM là fact thật |

Fact mới thời kỳ mới (IG 07–08/2026):
- Fit: **Signature Boxy Fit** · Unisex design
- Slogan: **`EVEN IN CHAOS, YOU ARE ALIVE.`** · **"Finding harmony within chaos"**
- Khuôn spec PDP cố định: `• Fabric / • Fit / • Sizing / • Status`
- Ảnh: tối, nắng gắt xiên, contrast cao, **người mẫu Tây/lai**, caption **tiếng Anh tuyệt đối**
- **"Old things still shine."** — hàng thời kỳ cũ được chủ mới đóng khung là **archive**

**Hệ quả chiến lược:** hướng quốc tế không còn là suy luận — chủ mới đang cố tình xây brand
nói với người nước ngoài từ Sài Gòn. Website EN-first là **kênh chính**, không phải kênh phụ.
Điều này đảo ngược giả định "website là kênh mới, không thay thế Shopee" trong CLAUDE.md.

---

## H. QUYẾT ĐỊNH USER CHỐT 2026-08-19 (sau khi có BRAND_ERA_SPLIT)

| Chủ đề | Chốt |
|---|---|
| Định hướng chung | **Mọi thứ theo THỜI KỲ MỚI** |
| Hệ size | **`S / M / L`** duy nhất. Hàng cũ cũng đổi sang. Không giữ 1/2/3 |
| Hàng thời kỳ cũ | **Treat như hàng bình thường.** Không tách `Archive` |
| Shopee | **Vẫn bán song song** |
| Chính sách đổi trả | **Giữ nguyên**: 5 ngày · 1 lần/đơn · khách chịu ship 2 chiều |
| Logo | **Dùng bản ĐEN** (`Logo/Black Sabbath/`), bỏ qua wordmark navy trên avatar IG |
| Brand guideline | **Chưa chốt** — vẫn phải đánh dấu assumption |
| Ảnh model | Dùng tạm 5 ảnh hiện có, thay sau |
| Ship quốc tế | "như bình thường" — **vẫn chưa có phí/hãng/thời gian cụ thể** |
| Multi-currency | User muốn có. Mô hình chưa chốt (chờ số phí ship) |

**Còn chặn:**
- 🔴 Bảng số đo cm cho `S/M/L` → chặn trang Size Guide và chặn nhập hàng loạt
- 🔴 Phí + hãng + thời gian ship quốc tế → chặn quyết định multi-currency và checkout
- 🟡 Mã hex tím/xanh thời kỳ mới → badge tạm đen/trắng

**Yêu cầu mới:** brand team thích dạng nền **iridescent (oil-slick)** như post IG 29/07,
muốn có **motion** ở một phần nào đó của site. → `deliverables/motion/iridescent.html`

---

## I. MỞ KHOÁ 2026-08-19 (cuối ngày)

| | |
|---|---|
| **Backup UpdraftPlus** | ✅ **XONG** — hết chặn mọi việc đụng theme |
| **Bảng size S/M/L** | ✅ **Dùng chung bảng cũ**: S=70/55 · M=73/58 · L=76/61 — hết chặn nhập hàng |
| **Nền toàn site** | ✅ **TRẮNG.** Site fashion để nền trắng để tôn sản phẩm |
| **Motion iridescent** | Oil slick giống nhất. Cái quyết định là **chuyển động KHÔNG TRẬT TỰ**, không phải kỹ thuật cụ thể |

**Hệ quả của "nền trắng":** iridescence **không thể là nền toàn trang**.
Nó phải là **phần tử có giới hạn** trên nền trắng — band, thẻ, badge, hover.
Và trên nền trắng nó đổi bản chất: từ *oil-slick* (váng dầu trên đen) thành
*pearlescent / nacre* (xà cừ, bong bóng xà phòng) — sáng hơn, pastel hơn.

**Còn chặn:** phí + hãng + thời gian ship quốc tế → chặn quyết định multi-currency.

---

## J. LÀM LẠI LAYOUT — 2026-08-20

User xem bản build đầu rồi phản hồi: **thích layout của prototype `Vitalite Homepage.dc.html` hơn.**
Cụ thể: full-width, có điểm nhấn hơn, và **banner cần 3 slide**.

Bản build đầu của Claude là **boxed 1440px, heading tối đa 40px** — nhỏ và an toàn hơn hẳn
prototype. Đó là hiểu sai yêu cầu, không phải lựa chọn thiết kế.

### Ngôn ngữ layout đã chốt (đọc từ prototype)

| | |
|---|---|
| Chiều rộng | **FULL-WIDTH**, không khung giữa, lề `clamp(16px, 2.4vw, 32px)` |
| Tiêu đề section | `clamp(38px, 5.4vw, 84px)` Archivo Expanded 800 in hoa |
| Hero | `clamp(50px, 8.4vw, 152px)` |
| Eyebrow | **đánh số** `01 — FEATURED`, có **đường kẻ đen** dưới tiêu đề |
| Lưới sản phẩm | **gap 2px** trên nền màu đường kẻ → hairline, ô sát nhau |
| Nút | **bo tròn hoàn toàn** `border-radius: 999px` |
| Hero | **3 slide** cross-fade + **thanh tiến trình** làm điều hướng |
| Thêm | nút chọn nhanh size khi hover · lưới `featured` ô đầu 2×2 · khối Collection chia đôi · dải services 3 cột |

### Ba slide hero — copy nguyên văn Instagram, không tự nghĩ

| | Tone | Copy | Nguồn |
|---|---|---|---|
| 01 THE ICONIC | tối | *Even in chaos, you are alive.* | IG 29/07/2026 |
| 02 THE MOMENTS | tối | *Heavy in weight. Unmatched in fit.* | IG 25/07/2026 |
| 03 ARCHIVE | **sáng** | *Old things still shine.* | IG 20/07/2026 |

Slide 03 tone sáng → header tự đảo sang chữ đen, logo bỏ invert, badge giỏ đảo màu.

### Đánh đổi LCP đã chấp nhận

Carousel above the fold vốn hại LCP — Claude tránh nó ở bản đầu vì lý do đó.
User cần 3 slide, nên giữ được bằng cách:
- chỉ ảnh **slide 1** `fetchpriority=high` + preload; slide 2, 3 `loading="lazy"`
- **video chỉ ở slide 1**, `preload="none"`, gắn source bằng JS sau `load`, không tải trên mobile
- thanh tiến trình chạy bằng **CSS animation**, không phải `setInterval` — chạy trên compositor
- dừng khi rê chuột / tab ẩn / cuộn khỏi hero

### Gallery mosaic
User chỉ ra Claude thiếu hẳn phần này so với prototype. Đã bổ sung:
lưới ô to nhỏ `2×2 · 1×1 · 1×2 · 1×1 · 2×1 · 1×1 · 1×1 · 4×1`, lặp chu kỳ 8, `grid-auto-flow: dense`.
Ảnh đọc thẳng từ `assets/gallery/` — thả file vào là hiện, không cần wp-admin.


---

## 2026-08-20 — Vòng sửa giao diện sau review của user

### Lỗi thật, không phải giả định

**S/M/L xếp dọc, có gạch chân** — `<a>` chọn size nằm LỒNG trong `<a class="vt-card-media">`.
`<a>` trong `<a>` là HTML không hợp lệ: trình duyệt tự đóng thẻ ngoài rồi ĐẨY các link con
ra ngoài, chúng rơi khỏi `.vt-card-media` nên mất sạch CSS. Đã xác minh trong browser:
`.vt-card` có 5 con `A.vt-card-media, A, A, A, DIV.vt-card-body` thay vì 2.
Sửa: `.vt-card-media` thành `<div>`, link phủ ảnh tách riêng ra `.vt-card-media-link`.

**Nav hero mất hút trên slide 3** — `.vt-hero-nav` là ANH EM của `.vt-slide`, không nằm
trong nó, nên không thừa hưởng `color` của slide. Nó luôn trắng, kể cả trên slide nền trắng.
Sửa: JS gắn `data-tone` lên chính `.vt-hero`, CSS đảo màu nav theo.

**Preview thiếu `<meta charset>`** — vì thế `₫` và `é` hiện thành ký tự rác trong ảnh chụp
màn hình của user. Đã thêm charset + viewport vào `static-preview.html`.

### Giả định — CẦN USER XÁC NHẬN

| Giả định | Diễn giải | Lùi lại thế nào |
|---|---|---|
| ~~oil slick đặt lên slide 3 của hero~~ | ❌ **ĐOÁN SAI, đã gỡ hoàn toàn.** Xem mục dưới. | — |
| Lưới **sản phẩm** vẫn giữ lề | User xác nhận: *"gallery thì full width còn grid sản phẩm thì phải khác chứ"*. Đo được `.vt-grid` giữ lề 31px, gallery/collection/banner tràn sát mép. | — |

### Chi phí LCP của vòng này
Bằng 0. Không thêm file, không thêm ảnh, không thêm JS. Váng dầu là 4 radial-gradient
chạy bằng `transform` trên GPU, và chỉ chạy khi slide đang hiện (`.vt-slide.is-active`).
Bỏ `.vt-wrap` ở collection/gallery không đổi số byte.


---

## 2026-08-20 — Sửa lại: oil slick là BANNER ĐẦU TRANG, không phải slide hero

User làm rõ: *"sẽ có trang archive là show chỉ các sản phẩm ấy thì cái banner ở trên
trang sẽ là oil slick chẳng hạn"*. Tức là váng dầu là **treatment cho banner đầu trang
archive / category**, không phải hiệu ứng đắp lên hero.

Đã gỡ sạch `vt-slide-iri` khỏi `hero.php` và `style.css`. Hero trở lại đúng như cũ —
**fix màu thanh nav vẫn giữ**, đó là bug thật, độc lập với chuyện váng dầu.

### Cái mới: `template-parts/section-page-banner.php`

| | |
|---|---|
| Dùng ở | `woocommerce/archive-product.php` — cả shop, category, tag, `?on_sale=1`, `?orderby=date` |
| Kỹ thuật | `class="vt-iri vt-pagebanner" data-vt-iri` — **dùng lại nguyên bộ CSS iridescent sẵn có**, không nhân bản gradient. `data-vt-iri` nối thẳng vào observer trong `site.js`: cuộn khỏi màn hình là animation dừng |
| Chiều cao | `clamp(220px, 30vh, 380px)` — **cố ý KHÔNG phải hero**. Trang category tồn tại để khách xem hàng; banner 100vh là đẩy sản phẩm xuống dưới nếp gấp mà không đổi lại được gì |
| `<h1>` | Nằm **trong banner**, `.vt-shop-head` giờ chỉ còn breadcrumb. Đúng một h1 mỗi trang |
| Nội dung | eyebrow `Shop` · title = `vt_shop_heading()` · lede = `term_description()` **chỉ khi người nhập hàng viết thật** · meta = số sản phẩm thật từ `found_posts` |
| Chi phí LCP | 0 KB. Không ảnh, không font mới, không JS mới |

### 🔴 Cảnh báo cho lần sau
Banner nằm **trên cùng** trang archive → nó rất dễ thành phần tử LCP.
Hiện là text + gradient nên rẻ. **Thêm ảnh nền vào đây mà không `preload` là tụt LCP
của TOÀN BỘ trang category.** Đã ghi cảnh báo này ngay trong docblock của file.

### Chưa làm — chờ user quyết
- `search.php` cũng là trang kết quả sản phẩm nhưng **chưa gắn banner**. User nói "archive", tôi không tự mở rộng.
- Category chưa cái nào có **ảnh campaign riêng**. Banner váng dầu là chỗ giữ tạm, tốt hơn khối xám trống. Khi có ảnh thật thì truyền vào `section-page-banner` — nhớ preload.


---

## 2026-08-20 — HEADER XUYÊN THẤU TOÀN SITE (đổi cấu trúc, không phải chỉnh CSS)

Trước: header trong suốt **chỉ trên trang chủ**, vì nó bám cứng vào `vt_has_hero()`.
Mọi trang khác bị đẩy xuống `padding-top: var(--vt-header-h)`.

Giờ: **bất kỳ trang nào mở bằng banner** đều có header xuyên thấu. Nội dung bắt đầu từ
đúng mép trên viewport, banner chui xuống dưới header.

### Chỗ duy nhất quyết định: `vt_top_banner_tone()` — `inc/helpers.php`

Trả `'dark' | 'light' | ''`. Một hàm, ba nơi dùng: body class, `<meta theme-color>`,
và trạng thái khởi đầu của header. **Thêm banner vào template nào thì thêm điều kiện
vào đây**, lệch nhau là header tàng hình.

Hiện trả `'dark'` cho: trang chủ (hero) · shop · category · tag.
Trả `''` (không banner) cho: page · single · search · cart · checkout · 404.

### Đổi tên class — nghĩa cũ đã sai
| Cũ | Mới | Vì sao |
|---|---|---|
| `.is-over-hero` | `.is-transparent` | Không còn dành riêng cho hero |
| `.is-light-slide` | `.is-light-bg` | Banner tĩnh không có "slide" nào cả |
| `[data-vt-hero-sentinel]` | `[data-vt-header-sentinel]` | Sentinel giờ là hợp đồng chung; hero giữ cả hai attribute |

### Mặc định an toàn + hai lưới an toàn trong JS
CSS mặc định là **CÓ đệm** (`.vt-main { padding-top: var(--vt-header-h) }`), trang có
banner mới bỏ đệm. Quên khai báo thì tệ nhất là thừa khoảng trắng — **không phải chữ
chui xuống dưới header**.

JS tự sửa cả hai chiều:
- không tìm thấy sentinel → gỡ `is-transparent` **và** gỡ `vt-banner-top` (trả lại đệm)
- tìm thấy sentinel mà body thiếu class → thêm `vt-banner-top`

### Responsive — không thêm media query nào
`--vt-header-h` đã tự đổi `76px → 64px` ở `≤768px`. Banner chừa chỗ bằng
`calc(var(--vt-header-h) + …)` nên ăn theo sẵn. `rootMargin` của observer đọc
`header.offsetHeight` lúc khởi tạo nên cũng đúng ở cả hai cỡ.

**Đo thật trong browser:**

| | viewport | header | cao banner | tiêu đề | lede | eyebrow qua khỏi header |
|---|---|---|---|---|---|---|
| Desktop | 1280 | 76px | 306px | 53.8px | hiện | ✅ 110px |
| Mobile | 375 | 64px | 178px | 30px | ẩn | ✅ 91px |

Banner tràn sát mép ở cả hai cỡ (lệch 1px = viền của khung preview).

### Banner archive: THẤP và ĐƠN GIẢN
`min-height: calc(var(--vt-header-h) + clamp(110px, 14vh, 170px))`.
Chiều cao thật = header + khối chữ, không phải một con số `vh` cố định.
Tiêu đề `clamp(30px, 4.2vw, 62px)` — **nhỏ hơn tiêu đề section một bậc**, vì banner là
chỉ dẫn "bạn đang ở đâu", không phải tuyên ngôn.
Mobile ẩn lede: chuỗi vẫn trong HTML cho bot, nhưng `display:none` thì máy đọc màn hình
không đọc — mô tả category không phải thông tin thiết yếu để mua nên chấp nhận đánh đổi.

### 🔴 Phát hiện phụ, CHƯA sửa — cần user quyết
`woocommerce_output_content_wrapper` **chưa bị gỡ**. Nó in `<div id="primary"><main
id="main" class="site-main">` vào trong `<main id="vt-main">` → **`<main>` lồng `<main>`**,
HTML không hợp lệ và ảnh hưởng máy đọc màn hình.

CSS đã chặn hậu quả layout (selector `.site-main` có trong cả hai quy tắc đệm), nên
**không vỡ giao diện**. Nhưng gỡ nó thì cart / checkout / trang sản phẩm mất container —
và `CLAUDE.md` ghi rõ *"cart & checkout: KHÔNG customize trước khi flow mặc định chạy đúng"*.
→ Để nguyên, kiểm lại sau bước 8 khi đã có sản phẩm test chạy thật.


---

## 2026-08-21 — Cart/Checkout, header trượt, dọn theme

### User bác bỏ một luật do Claude tự đặt
`CLAUDE.md` ghi *"Cart & checkout: KHÔNG customize trước khi flow mặc định chạy đúng"*.
User nói thẳng: **luật đó là Claude tự quy định, không phải user**. → đã làm.

**Đã làm ĐÚNG phần khung và lớp sơn, KHÔNG đụng luồng:**
không gỡ field, không đổi thứ tự bước, không hook vào luồng đặt hàng, markup vẫn
100% của WooCommerce → plugin thanh toán cắm vào được, Woo update không phá.

| Việc | Chi tiết |
|---|---|
| Gỡ `<main>` lồng `<main>` | `woocommerce_output_content_wrapper` in ra `<main id="main">` bên trong `<main id="vt-main">`. Thay bằng `vt_woo_wrapper_start/end`, hai chế độ: `bare` cho shop/category (template tự lo vì banner phải tràn viền), có `.vt-wrap` cho trang sản phẩm đơn |
| Giỏ/Thanh toán/Tài khoản | Là trang WP thường chứa shortcode → đi qua `page.php`, KHÔNG qua template Woo. Trước đây chúng rơi vào khung đọc **860px + `.vt-prose`** — bảng bị bóp, `.vt-prose` đặt margin lên mọi phần tử liền kề nên phá khoảng cách form. Giờ có nhánh riêng: `.vt-wrap` rộng + `.vt-woo-page` |
| Lớp sơn Woo | Bảng hairline, nhãn mono in hoa, ô nhập vuông viền 1px, nút bo tròn hoàn toàn |

**Hai chi tiết thương mại đáng nói:**
- Ô nhập **16px trên mobile**. Dưới 16px là Safari iOS tự phóng to trang khi khách bấm vào ô. Đang điền địa chỉ mà trang nhảy là mất đơn.
- `#place_order` **chiếm hết chiều ngang**. Hành động cuối, không để khách phải tìm.
- Bảng cho **cuộn ngang** trên màn hẹp thay vì bóp cột — bóp cột làm giá và số lượng xuống hàng, khách đọc nhầm số tiền.

### Header trượt — ẩn khi kéo xuống, hiện khi kéo lên
**Đây là chỗ DUY NHẤT trong theme dùng scroll listener.** IntersectionObserver
không biết HƯỚNG cuộn, mà toàn bộ hành vi này là về hướng. Đổi lại làm rẻ nhất có thể:
`passive: true` · gom vào `requestAnimationFrame` (tối đa 1 lần/khung hình) ·
chỉ đọc `window.scrollY`, **không** đọc `offsetHeight`/`getBoundingClientRect` trong
lúc cuộn (tránh ép tính lại layout) · chỉ chạm `classList` khi trạng thái thật sự đổi.

Ba luật: vùng tự do 120px đầu trang luôn hiện · ngưỡng 8px mới đổi (không có ngưỡng
thì trackpad nảy và đà trượt iOS làm header nhấp nháy) · menu mobile mở thì bất động
(nút đóng nằm trong header). Kẹp `scrollY < 0` vì iOS cho cuộn quá đà giá trị âm.

### ⚠️ User nói có thể tự làm header bằng Elementor Theme Builder
**Nếu làm vậy thì mất toàn bộ hệ thống header xuyên thấu vừa dựng** — nó sống trong
theme PHP + CSS + JS: `vt_top_banner_tone()`, `.is-transparent`, `.is-light-bg`,
sentinel, và cả header trượt. Elementor Theme Builder **không biết** trang nào có
banner tối để đảo màu chữ.

Ngoài ra `CLAUDE.md` mục 5 đã chốt **"Con đường A — theme PHP, KHÔNG Elementor
Theme Builder"**. Đây là quyết định đã chốt, chỉ mở lại nếu user muốn.
→ **Đã dựng trong theme.** Cần user xác nhận có đổi hướng không.

### Trang tìm kiếm cũng đã gắn banner
User nói "làm hết luôn". `search.php` giờ dùng cùng banner váng dầu và đã khai báo
trong `vt_top_banner_tone()`.

### 🔴 CHƯA làm — cần user cho phép rõ ràng
`git commit --amend` + `git push --force` để gỡ 93MB khỏi lịch sử git (ghi trong
`HANDOFF.md` mục 11). **Force-push viết đè lịch sử trên remote, không lùi lại được
dễ dàng.** Không tự chạy. User bảo chạy thì chạy.

---

## Trang About — chuỗi frame làm HERO (2026-08-23)

### 🔴 Cái áo trong 96 frame là ảnh CGI, chưa đối chiếu hàng thật
`deliverables/scroll-sequence/frames/0823/` do Antigravity sinh bằng AI. Lưng áo in dòng
*"IT'S THE ONLY MOMENT THAT MATTERS"* — **không có trong bất kỳ nguồn brand nào đã xác minh**
(Shopee, IG, FB). Màu xám và hoodie 2 lớp thì có thật (`'THE MOMENTS' BOXY HOODIE 2 LỚP - GREY`
đang bán trên Shopee), nhưng **thiết kế trong ảnh chưa ai đối chiếu với sản phẩm thật**.

**Đã xử tạm:** HUD ghi `CGI visualisation`; bảng spec cạnh nó **không gọi tên SKU nào**, chỉ
trích spec outerwear đã công bố. **Cần user xác nhận:** dòng chữ lưng áo có thật không, và cái
áo trong ảnh có giống hàng thật không. Nếu không thì hoặc thay asset, hoặc giữ nguyên nhãn CGI.

**Không mang chuỗi này sang PDP** khi chưa có ảnh chụp thật — ở đó nó thành cơ sở cho quyết định
mua, và lệch thiết kế biến thành đơn trả hàng.

### 🟡 Ngân sách ảnh vượt spec 7,5 lần — user đã biết và chốt giữ
`scroll-sequence/README.md` mục 3 quy định ≤ 1,4 MB / 30–36 frame / 900px. Chuỗi thật là
**10,6 MB / 96 frame / 2560px**. User chốt 2026-08-23: **giữ nguyên**, ưu tiên chất lượng hình.
Giảm nhẹ: khối dưới fold, `≤820px` không tải frame nào → chỉ desktop chịu. Không phải lỗi,
đừng âm thầm nén lại.

### 🔴 User ghi đè luật "đặt dưới fold" — đã bù bằng hai hàng rào khác
`scroll-sequence/README.md` §6 cấm đặt khối này làm khối đầu trang. User quyết 2026-08-23:
**đưa lên làm banner**, vì đầu trang cũ quá trống. Đã bù:

1. LCP là **poster riêng** `poster-960/1440/1920.webp` (30 / 50 / 72 KB, srcset, eager,
   `fetchpriority=high`), **không** phải `001.webp` 2560px/189 KB.
2. 96 frame chỉ tải **sau `window.load`**, lưới an toàn 8 giây.

Đo trên preview 961px: poster xong 147 ms · `loadEventEnd` 234 ms · frame đầu 589 ms.
Mobile 375px: **0 request frame**.
**Gỡ một trong hai là trang đầu tải 10,6 MB trước khi khách thấy gì.**

### ✅ Bố cục tĩnh của component gốc bị hỏng — đã vá
Bảng "suy giảm" trong `component.html` mô tả *"chữ xếp dọc và hiện hết"*, nhưng đo thật thì
nội dung bị cắt còn 722/1703px, và 8 khối chữ chồng lên nhau chỉ dùng 2 hộp. Đây là bố cục
**mặc định của mọi khách mobile**. Đã vá trong `about.html`; `component.html` bản mẫu vẫn còn lỗi.

### 🟡 Cổng chặn tải frame chỉ chạy MỘT LẦN lúc parse
Khách mở trang lúc cửa sổ hẹp (≤820px) rồi phóng to sau → vẫn ở bố cục tĩnh cho tới khi tải lại
trang. Đây là **hành vi cố ý** (mục 5 README): thêm kiểm tra lúc `resize` là mở đường cho việc
kéo 10,6 MB về đúng lúc không ai cần. Đang chấp nhận.

### ⚠️ Chưa kiểm được trên trình duyệt thật
Môi trường kiểm của Claude chạy tab nền: `requestAnimationFrame` không nổ, không chụp được màn hình.
**Đã xác minh bằng số:** 96 frame trả 200 · canvas khớp stage · scrub đúng (y=1440 → frame 049,
y=2600 → frame 087) · mốc chữ bật đúng từng đoạn · hàng rào `load` giữ được (frame đầu 589 ms
sau `loadEventEnd` 234 ms) · mobile 0 request frame · bố cục tĩnh 8/8 khối tách rời, không bị cắt,
không tràn ngang.

**Chưa xác minh được:** độ mượt thật khi scrub bằng mắt, và Lighthouse mobile.
Tab của Claude chạy nền, `requestAnimationFrame` chập chờn và không chụp được màn hình ổn định.
Chụp được đúng một khung ở đầu trang, phần còn lại kiểm bằng đo `getBoundingClientRect` và
`performance.getEntriesByType('resource')`.
