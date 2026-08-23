# HANDOFF — VITALITÉ WEBSITE
**Cập nhật:** 2026-08-22 · **Dành cho:** phiên Claude Code mới
**Đọc file này ngay sau `CLAUDE.md`, trước khi làm bất cứ việc gì.**

> ⚠️ **Terminal máy này là Windows PowerShell 5.1 — `&&` KHÔNG tồn tại.**
> Nối lệnh bằng `;`. Viết `&&` là user bấm Run và nhận parser error.

---

## 0. Đứng ở đâu — một đoạn

Theme **đã deploy và đang chạy thật** trên `vitalite.io.vn`, thư mục
`wp-content/themes/vitalite-theme-2/`. Git sạch, đã push, lịch sử đã gỡ 93MB video.

> 🔴 **23/08/2026: repo git chuyển lên GỐC PROJECT.**
> Trước đây `.git` nằm ở `repo/vitalite-website/` và chỉ track theme.
> Bây giờ nó ở `E:\Vitalite website\` và track **tất cả**: `docs/`, `deliverables/`,
> `reference/`, `CLAUDE.md`, `Logo/`, `mockup-all/`, `model/`, và theme ở vị trí cũ.
> Lịch sử giữ nguyên (62 rename), `git log --follow` vẫn chạy.
> Chạy `git` từ gốc project, **đừng `cd repo/vitalite-website`** nữa.

Phần code coi như xong. **Thứ còn lại là NỘI DUNG và DỮ LIỆU, không phải code** —
và phần lớn đang chờ những con số chỉ user mới có.

---

## 1. Việc kế tiếp

📍 **User đọc `docs/VIEC-CUA-BAN.md`** — đó là bản tổng hợp việc, viết cho user chứ không
phải cho Claude. Đừng bắt user đọc lại toàn bộ tài liệu.

### Đang chờ user làm

```
1. Upload 2 file theme mới nhất  →  style.css · template-parts/site-footer.php
2. Đổi template trang chủ về "Mẫu mặc định" (Sửa nhanh, KHÔNG mở Elementor)
3. Cấu hình WP: tiêu đề site vẫn là "Vitalite – My WordPress Blog"
4. Tạo trang + dán HTML từ deliverables/pages-html/
5. Trả lời 11 câu ở VIEC-CUA-BAN.md mục 3
```

### ✅ Đã hoàn thành bởi Antigravity (Sẵn sàng cho Claude)

Chuỗi **Scroll-Sequence 4K/2K** đã hoàn thiện 100% về cả asset và component:
- **Chuỗi frame thực tế:** `deliverables/scroll-sequence/frames/0823/` (96 frame · 2560px QHD Ultra-Sharp · WebP nén tối ưu).
- **Component HTML/CSS/JS hoàn chỉnh:** `deliverables/scroll-sequence/component.html` (Bố cục chữ Asymmetric Editorial bất đối xứng 2 bên, HUD Header `vitalité ® // ARCHIVE`, live frame counter `001/096`, thanh tiến trình).
- **File test preview:** `deliverables/scroll-sequence/_preview.html`.
- **Bộ tư liệu & prompt gốc:** `deliverables/video-scenes/scroll-orbit-item-focus/`.

✅ **ĐÃ TÍCH HỢP (2026-08-23).** Chuỗi frame **là HERO của trang About**, khối đầu tiên,
thay hẳn banner váng dầu cũ. Thứ tự trang giờ là:

```
HERO   chuỗi frame dính màn hình, 4 mốc chữ
       Marquee
01     The name
02     The comeback
03     Two eras, one label
04     What it is made of
05     The record          ← váng dầu iridescent chuyển xuống đây đóng trang
```

Bốn mốc chữ trong hero: **H1 của trang** (*Even in chaos, you are alive.*) rồi
*Heavy in weight* · *Unmatched in fit* · *Holds its shape all day*. Ba câu sau nguyên văn IG 25/07/2026.

### 🔴 LCP — hai thứ giữ cho trang không sập, đừng gỡ cái nào

Chuỗi 10,6 MB giờ nằm **ngay đầu trang**, đúng cái mà `scroll-sequence/README.md` §6 cấm.
Nó chạy được vì hai hàng rào:

| | |
|---|---|
| **LCP là poster riêng, không phải frame** | `poster-960/1440/1920.webp` — **30 / 50 / 72 KB**, srcset, `eager` + `fetchpriority=high`. KHÔNG dùng `001.webp` (2560px, 189 KB) |
| **96 frame chỉ tải SAU `window.load`** | IntersectionObserver không còn là cái van (khối ở đầu trang thì nó báo "thấy rồi" ngay khung hình đầu). Van bây giờ là `load` |

Đo trên preview: poster xong ở **147 ms**, `loadEventEnd` **234 ms**, request frame đầu tiên
**589 ms**. Gỡ hàng rào `load` là trang đầu tải 10,6 MB trước khi khách thấy gì.

Trên mobile (≤820px) **không một frame nào được tải** — đã đo, 0 request. Chỉ poster 30 KB.

### Đã sửa so với bản `component.html` gốc, đừng dựng lại

| Bản gốc | Đã sửa thành | Vì sao |
|---|---|---|
| `500+ GSM ... COTTON FLEECE` | `500+ GSM COTTON BLEND` | Brand ghi **Cotton Blend**, không phải fleece |
| `HARDWARE: ACETATE EYEWEAR`, `COORDINATES 10.7769° N` | bỏ hẳn | Vitalité **không bán kính**. Liệt kê vào bảng spec là dựng ra sản phẩm |
| `Engineered and crafted in Saigon` | bỏ, chỉ còn `Made in: Vietnam` | Claim về xưởng — `CLAUDE.md` §2 cấm |
| `#CA2058` magenta | trắng | Magenta là màu **thời kỳ cũ**; hàng trong ảnh là thời kỳ **mới** |
| `// ARCHIVE` | `Vitalité ® · Saigon · Est. 2022` | Đây không phải hàng archive |
| `Unmatched in cut` | `Unmatched in fit` | Brand viết *fit*. Đó là câu trích nguyên văn, không được sửa |

### 🔴 Hai lỗi bố cục tĩnh trong bản gốc — đã sửa, đừng để tái phát

Mức suy giảm mà `component.html` mô tả **chưa bao giờ chạy đúng**. Đây là bố cục **mặc định của
mọi khách mobile**, nên hỏng ở đây là hỏng với đa số:

1. `.vsq-stage` giữ `overflow:hidden` + `.vsq-viewport` giữ `height:100%` → chữ xếp dọc bị
   **cắt cụt**, đo được 722px trong khi nội dung cao 1703px. Mất 3/4 nội dung.
2. Bốn mốc chữ đều đặt `grid-area:1/1` để chồng lên nhau lúc chạy thật. Cột cha vẫn
   `display:grid` ở bố cục tĩnh → chúng **vẫn chồng**, khách chỉ đọc được mốc cuối. Đo được
   8 khối dùng chung 2 hộp.

Cả hai đã vá trong khối `.vsq:not(.is-ready)` của `about.html`, có ghi chú 🔴 tại chỗ.

### 🟡 Còn một việc chưa xử

Cái áo trong 96 frame là **ảnh CGI**, không phải ảnh chụp hàng thật. Lưng áo in dòng
*"IT'S THE ONLY MOMENT THAT MATTERS"* — **không có trong bất kỳ nguồn brand nào**.
HUD ghi `CGI visualisation` để không nhận đây là ảnh sản phẩm. Muốn bỏ dòng đó thì phải
đổi asset trước, không phải đổi chữ.

⚠️ **Trước khi publish:** upload `deliverables/scroll-sequence/frames/0823/` lên
`wp-content/uploads/seq/0823/` — **99 file**: 96 frame (10,6 MB) + 3 poster.
Thiếu frame thì hero chỉ còn ảnh tĩnh, không sập trang. **Thiếu poster thì hero trống.**


---

## 2. Cấu trúc theme hiện tại

`repo/vitalite-website/vitalite-theme/vitalite-theme-2/`

⚠️ Thư mục tên **`vitalite-theme-2`** — đổi tên để deploy song song, khớp với
tên trên hosting. Bản cũ `vitalite-theme` vẫn còn trên production để lùi lại được.

```
style.css                     hệ token đầy đủ + toàn bộ CSS (~40KB thô)
functions.php                 chỉ bootstrap, nạp inc/
inc/
  helpers.php                 vt_shop_url, vt_cat_url, vt_page_url, vt_maybe_link,
                              vt_gallery_images, vt_product_back_image, vt_icon…
  setup.php                   theme support, menu, image size, bảo mật, shortcode compat
  enqueue.php                 asset, font, preload LCP, bỏ CSS/JS Woo ở trang không cần
  woocommerce.php             hook Woo, cart badge, bảng size PDP, ?on_sale=1
  seo.php                     meta, OG, JSON-LD — TỰ TẮT khi có plugin SEO
header.php  footer.php
front-page.php                trang chủ, 6 section
page.php  index.php  404.php  search.php  searchform.php
single.php                    bài viết đơn — lưới an toàn, thiếu nó thì bài viết
                              rơi xuống index.php và KHÔNG in ra nội dung
screenshot.jpg                ảnh theme trong Giao diện → Themes
languages/vitalite.pot        90 chuỗi giao diện. Sinh lại: python docs/make-pot.py
template-parts/
  site-header  site-footer  hero  product-card  empty-state
  section-products  section-collection  section-gallery
  section-iridescent  section-editorial  section-services
  section-page-banner           banner váng dầu đầu trang archive/category, 0 KB
woocommerce/
  archive-product.php  content-product.php     ← 2 file Woo duy nhất bị đè
assets/
  js/site.js                  slider, header xuyên thấu + trượt ẩn/hiện, menu mobile, iridescent
  gallery/                    8 ảnh — THẢ FILE VÀO LÀ HIỆN, không cần wp-admin
  hero-poster.webp  cb-poster.webp  slide-03.webp  collection-01.webp
  editorial-01.webp  og-default.jpg  logo PNG
  video/                      ✅ 4.1MB — hero-1280.mp4 (2.43MB) + hero-1280.webm (1.66MB)
                              master nằm ở repo/vitalite-website/_not-in-theme/, KHÔNG commit
(product-images/ đã gỡ — 17 PNG không được reference ở đâu, chuyển ra _not-in-theme/)
```

### Ngôn ngữ layout (đừng làm ngược lại)
- **FULL-WIDTH.** Không có khung 1440px. Chỉ có lề `clamp(16px, 2.4vw, 32px)`.
- **HEADER XUYÊN THẤU.** Trang mở bằng banner (`body.vt-banner-top`) → nội dung bắt đầu
  từ mép trên viewport, header trong suốt đè lên banner. Trang không banner → đệm
  `var(--vt-header-h)`, header đục. Quyết định ở **một chỗ duy nhất**:
  `vt_top_banner_tone()` trong `inc/helpers.php`. Thêm banner ở đâu thì khai báo ở đó.
- **Tràn sát mép (`.vt-bleed`, lề 0):** collection · gallery mosaic · banner archive.
  **Giữ lề (`.vt-wrap`):** lưới sản phẩm `.vt-grid` · đầu section · breadcrumb · toolbar.
  Lưới sản phẩm cần lề để đọc được như bảng giá; khối hình ảnh cần tràn để có sức nặng.
  Đây là quyết định của user, đã xác nhận 2026-08-20 — đừng đảo lại.
- Tiêu đề section **khổng lồ**: `clamp(38px, 5.4vw, 84px)`, Archivo Expanded 800, in hoa.
- Mỗi section có eyebrow **đánh số** (`01 — FEATURED`) + **đường kẻ đen** dưới tiêu đề.
  Đường kẻ đó giữ nhịp cho cả trang.
- Lưới sản phẩm **gap 2px** trên nền màu đường kẻ → khe hở thành hairline, ô sát nhau.
- Nút **bo tròn hoàn toàn** (`border-radius: 999px`).

---

## 3. Quyết định đã chốt — KHÔNG mở lại nếu không có lý do mới

| Chủ đề | Chốt |
|---|---|
| Header/footer | Theme PHP, **KHÔNG** Elementor Theme Builder |
| Shortcode | Còn giữ làm **lớp tương thích** (vỏ mỏng gọi template part), có chống render 2 lần |
| Trang chủ | Dựng bằng **PHP** `front-page.php` ⚠️ lệch CLAUDE.md — xem mục 7 |
| Ngôn ngữ | **EN tại root**, VI tại `/vi/`. Build EN xong hết → dịch → launch cùng lúc |
| Auto-detect ngôn ngữ | **KHÔNG** |
| Permalink | `/%postname%` không trailing slash |
| Language switcher | Chữ `EN / VI`, không dùng cờ |
| Hero | **3 slide** cross-fade + thanh tiến trình. Video CHỈ ở slide 1 |
| Cart | Icon + badge. Rỗng → ẩn số. **KHÔNG** mini-cart drawer |
| Nền site | **TRẮNG** ở vùng sản phẩm. Tối + iridescent chỉ ở vùng kể chuyện |
| Màu nhấn | `--vt-accent` đang là **ĐEN** tạm thời — brand đổi chủ, hệ màu mới chưa chốt |
| Logo | Dùng bản **ĐEN** (`Logo/Black Sabbath/`) |
| Hệ size | **S / M / L** duy nhất, hàng cũ cũng đổi sang |
| Bảng số đo | S 70/55 · M 73/58 · L 76/61 — **dùng chung cho cả hàng cũ** |
| Hàng thời kỳ cũ | Treat như hàng bình thường, **không** tách `Archive` |
| Chính sách đổi trả | **Giữ nguyên** 5 ngày, 1 lần/đơn, khách chịu ship 2 chiều |
| Shopee | Vẫn bán song song |
| Media translation | **TẮT** trong Polylang |
| Minify CSS/JS | **TẮT** trong LiteSpeed — xung đột Elementor |

---

## 4. Fact brand đã xác minh — dùng trực tiếp, không hỏi lại

Nguồn: đọc trực tiếp Shopee / Instagram / Facebook ngày 2026-08-19.
Chi tiết đầy đủ: `reference/BRAND_FACTS_OBSERVED.md` + `reference/BRAND_ERA_SPLIT.md`

| | |
|---|---|
| Tên đúng | **`VITALITÉ ®`** — có dấu sắc, có ® |
| Email | `vitalitevn@gmail.com` |
| Kênh | IG `@vitalitevn` (7.001) · FB `/vitalitevn` (6,8K) · Shopee `shopee.vn/vitalitevn` (2,9k) · TikTok `@vitalitevn` |
| Shopee | **4.9 sao · 973 đánh giá · 4 năm · 10 SKU** |
| Giá thật | **276.100₫ – 599.100₫** |
| Áo thun | **250 GSM Cotton**, in lụa, unisex |
| Áo khoác | **500+ GSM Heavyweight Cotton Blend**, Signature Boxy Fit |
| Xuất xứ | **Việt Nam** — xác nhận cả từ user lẫn Shopee |
| Dòng sản phẩm | THE ICONIC · THE MOMENTS · PINK GRAFFITI · PORSCHE · STARLIGHT · OLD MONEY |
| Bio IG | `Quality and quantity` · `Worldwide shipping` · `Based in Saigon` |

### 🔴 Brand ĐÃ ĐỔI CHỦ — đọc `BRAND_ERA_SPLIT.md` trước khi viết bất kỳ copy nào
Thời kỳ cũ (hồng magenta, size 1/2/3) ≠ thời kỳ mới (xanh dương + tím, S/M/L, caption tiếng Anh,
người mẫu Tây). Comeback 18/04/2026. Mọi thứ theo **thời kỳ mới**.

### Copy thật đang dùng trên site (nguyên văn IG, không tự nghĩ)
```
"Even in chaos, you are alive."          29/07  THE ICONIC        → hero slide 1
"Heavy in weight. Unmatched in fit."     25/07  THE MOMENTS       → hero slide 2
"Old things still shine."                20/07  archive           → hero slide 3
"Finding harmony within chaos"           29/07                    → band iridescent
```

### ⛔ TUYỆT ĐỐI KHÔNG dùng lại (đã gỡ, là chuỗi bịa)
`SS26` · `BST Đường Phố` · `Sống Hết Công Suất` · `cotton 480GSM` · `in lụa thủ công` ·
`phát hành 20.08` · `Heavyweight Hoodie 480GSM` · `1.290.000₫` · `1.450.000₫` ·
8 tên sản phẩm giả trong lưới cũ. Có script quét: `docs/check-theme.py` mục 5.

---

## 5. 🔴 Đang CHẶN — cập nhật 2026-08-22

### 5.1 Ship quốc tế — chặn nhiều nhất, VẪN TRỐNG HOÀN TOÀN
User xác nhận 22/08: **chưa có thông tin gì.**
Chặn: multi-currency · shipping zone · trang `shipping` · và thực tế chặn launch.

Áo ~280.000₫ (~$11), ship quốc tế thường $25–40 → **phí gấp 3 lần giá hàng**.
Website tồn tại để phục vụ khách quốc tế (IG 7.002 follower, bio `Worldwide shipping`,
Shopee.vn không phục vụ quốc tế). Nếu con số đó đúng thì đây là **rủi ro mô hình kinh doanh**,
không phải rủi ro kỹ thuật.

### 5.2 Ship trong nước — ✅ ĐÃ CHỐT MÔ HÌNH, thiếu con số
User chốt 22/08: **phí tính theo địa chỉ khách điền ở checkout.**

Phân tích đầy đủ hai cách làm: **`deliverables/woo/SHIPPING-SETUP.md`**
- Cách A: Shipping Zones native — chỉ cần 4 con số, không plugin. **Đề xuất dùng để launch**
- Cách B: plugin GHN/GHTK gọi API — chính xác hơn nhưng **sửa form checkout** (thêm ô
  quận/huyện, phường/xã vì Woo chỉ có Tỉnh/Thành)

🔴 **Dù chọn cách nào cũng phải điền CÂN NẶNG cho mọi SKU ngay lúc nhập.** Đó là thứ duy nhất
chặn đường sang cách B sau này, và nó miễn phí ở thời điểm nhập.

### 5.3 Thông tin pháp nhân
Bắt buộc theo pháp luật TMĐT Việt Nam. Shopee cho thấy brand **đã có pháp nhân** — chỉ cần
lấy thông tin ra. Chặn trang `seller-information`.

### 5.4 Số đo hoodie
`THE MOMENTS BOXY HOODIE` chưa có số đo nào. Theme cố ý **không hiện bảng size** cho sản phẩm
ngoài danh mục áo thun — không hiện còn hơn hiện sai.

---

## 6. 🟡 Chờ quyết

| | |
|---|---|
| Mã hex **tím / xanh** thời kỳ mới | `--vt-accent` đang đen. Có mã thì đổi **đúng một biến CSS** |
| Có hiện "4.9★ · 973 đánh giá Shopee" không? | Social proof thật, dẫn nguồn được — nhưng gửi khách sang Shopee. **Quyết định kinh doanh** |
| Ảnh mockup nền trong suốt | Cần Canva Pro. Đã thử cắt tự động: **hỏng với áo sáng** (`MOCKUP-PIPELINE.md`) |
| Số hotline nào còn dùng | FB About `093 838 14 07` vs bài 2023 `037 963 2222` |

---

## 7. ⚠️ Hai điểm lệch so với CLAUDE.md — cần user xác nhận

**7.1 — Trang chủ dựng bằng PHP, không phải Elementor.**

🔴 **Trên production, Elementor ĐANG CHIẾM QUYỀN trang chủ.** Trang chủ là một page Elementor
(ID 28) dùng template `elementor_header_footer`. Elementor ghi đè `front-page.php` qua filter
`template_include`, chạy SAU template hierarchy nên nó thắng. Hệ quả: trang chủ chỉ render
**2 trong 6 section** (hero + một lưới sản phẩm), vì page đó chỉ chèn hai shortcode.

**Cách sửa:** `Trang → Tất cả trang → Sửa nhanh → Mẫu → Mẫu mặc định → Cập nhật`.
⚠️ **KHÔNG mở Elementor để đổi** — nó báo *"the content area was not found"* và không cho đổi,
vì `front-page.php` không gọi `the_content()`. Sửa nhanh không load Elementor nên không dính.

CLAUDE.md ghi *"Homepage: build bằng Elementor"*. Nhưng `Structure homepage` nằm trong
OPEN ITEMS và chưa bao giờ được chốt, còn user cần bản nền chạy được ngay.
**Đường lui còn nguyên:** mỗi section là template part độc lập và đều có shortcode
(`[vt_banner]` `[vt_products]` `[vt_collection]` `[vt_gallery]` `[vt_services]`).
Muốn chuyển sang Elementor: tạo trang Elementor, chèn shortcode, đặt làm trang chủ, xoá `front-page.php`.

**7.2 — Shortcode chưa gỡ hẳn.**
CLAUDE.md ghi *"Bỏ shortcode"*. Hiện chúng vẫn còn nhưng chỉ là vỏ mỏng gọi
`get_template_part()`, và có `vt_mark_rendered()` chống render hai lần.
Lý do: xoá ngay thì trang Elementor cũ đang chèn chúng sẽ in chuỗi thô cho khách thấy.
Gỡ hẳn sau khi kiểm tra không trang nào còn dùng.

---

## 8. Quy ước phải nhớ khi nhập sản phẩm

| | |
|---|---|
| **Ảnh** | `Product image` = **MẶT TRƯỚC** · `Gallery ảnh đầu tiên` = **MẶT SAU**. Hover trên lưới đổi trước↔sau. Sai thứ tự là hỏng hiệu ứng. Đã có meta box nhắc trong màn hình sửa sản phẩm |
| **Category slug** | `t-shirts` · `outerwear` · `bottoms` — **slug tiếng Anh**, theme dò theo đúng chuỗi này |
| **Attribute variation** | `pa_size` (S/M/L, **Custom ordering**) · `pa_color` |
| **Attribute spec** | `pa_fabric` · `pa_fit` · `pa_collection` · `pa_print` — **KHÔNG** tick "used for variations" |
| **Sản phẩm** | Phải là **Variable**. Shopee tách mỗi màu một listing; trên Woo gộp thành 1 product |
| **Gallery trang chủ** | Thả ảnh vào `assets/gallery/`, đặt tên `01-…` `02-…`. Số đầu quyết định ô to nhỏ. Cache 12h — xoá transient `vt_gallery` nếu chưa thấy |
| **Không tạo category** | `New Arrivals` `Sale` `Collection` — chúng là *cách sắp xếp*, theme đã làm bằng `?orderby=date` và `?on_sale=1` |

---

## 9. Bản đồ tài liệu

| Cần gì | Đọc file |
|---|---|
| **VIỆC CỦA USER — đọc cái này trước** | **`docs/VIEC-CUA-BAN.md`** 📍 |
| HTML 10 trang tĩnh, dán vào Elementor | `deliverables/pages-html/README.md` |
| So sánh chính sách với Saigon Swagger + StressMama | `deliverables/content/POLICIES.md` |
| **Kế hoạch dựng site trên WordPress — runbook chủ** | **`docs/BUILD-ON-WORDPRESS.md`** 🔴 |
| Bắt đầu / tổng quan | `docs/START-HERE.md` |
| Deploy lên hosting | `deliverables/setup/DEPLOY.md` |
| Cấu hình WordPress | `deliverables/setup/WORDPRESS-SETUP.md` |
| Plugin nào, không cài gì | `deliverables/setup/PLUGINS.md` |
| cPanel / LiteSpeed / bảo mật | `deliverables/setup/HOSTING-LITESPEED.md` |
| Tối ưu tốc độ | `deliverables/setup/PERFORMANCE.md` |
| Cấu trúc WooCommerce | `deliverables/woo/STRUCTURE-SETUP.md` |
| Nội dung 6 trang tĩnh (dạng chữ) | `deliverables/content/PAGES-CONTENT.md` |
| **HTML 10 trang tĩnh, dán vào Elementor** | `deliverables/pages-html/README.md` |
| So sánh chính sách với Saigon Swagger + StressMama | `deliverables/content/POLICIES.md` |
| **Cấu hình vận chuyển WooCommerce** | `deliverables/woo/SHIPPING-SETUP.md` |
| **Chuỗi frame scroll — spec cho Antigravity** | `deliverables/scroll-sequence/README.md` |
| SEO / sitemap / redirect | `deliverables/seo/SEO-PLAN.md` |
| GA4 / event / báo cáo | `deliverables/analytics/TRACKING-PLAN.md` |
| Ảnh mockup, cặp trước/sau | `deliverables/images/MOCKUP-PIPELINE.md` |
| Nén video | `deliverables/video/encode.md` |
| Fact brand | `reference/BRAND_FACTS_OBSERVED.md` |
| **Brand đổi chủ** | `reference/BRAND_ERA_SPLIT.md` 🔴 |
| Logo / mockup / ảnh model | `reference/BRAND_ASSETS_AUDIT.md` |
| Audit production cũ | `deliverables/audit/production-audit-2026-08-19.md` |
| Kết quả tự kiểm | `docs/BUILD-CHECK.md` |
| Sinh lại file dịch `.pot` | `docs/make-pot.py` |
| Sinh lại HTML 9 trang chính sách | `docs/make-pages.py` |
| Mọi giả định theo thời gian | `docs/ASSUMPTIONS.md` |
| Xem giao diện không cần server | `deliverables/preview/static-preview.html` |
| Nghiên cứu motion iridescent | `deliverables/motion/iridescent.html` |

---

## 10. Công cụ tự kiểm

```bash
python docs/check-theme.py "E:/Vitalite website/repo/vitalite-website/vitalite-theme/vitalite-theme"
```

Kiểm 7 mục: cân bằng cú pháp · hàm `vt_*` chưa định nghĩa · `get_template_part()` trỏ file có thật ·
class CSS thiếu rule · **chuỗi bịa còn sót** · `echo` biến chưa escape · text-domain nhất quán.

**Chạy lại sau MỖI lần sửa theme.** Lần chạy gần nhất: sạch.

⚠️ Nó **không thay được `php -l`**. Máy không có PHP CLI. Có PHP thì chạy thêm:
```bash
find . -name "*.php" -exec php -l {} \;
```

---

## 10b. 🔴 Hạn chế môi trường — đọc trước khi tự kiểm bằng browser

Ba thứ đã làm mất thời gian, ghi lại để phiên sau không vấp:

**1. Tab browser trong app KHÔNG render khung hình.**
Nó chạy nền, không composite. Hệ quả:
- `IntersectionObserver` **không đáng tin** — có lượt callback không chạy lần nào, có lượt
  lại báo `isIntersecting: true` cho phần tử cách fold gần 4 màn hình. **Cùng một hình học,
  hai kết quả trái ngược.**
- `requestAnimationFrame` không chạy → animation đếm số, transition không tiến
- `computer{action:"screenshot"}` báo lỗi *"Browser pane is not displayed"*

→ **Đo cấu trúc thì được** (getBoundingClientRect, getComputedStyle, class, DOM, số request).
**Đừng kết luận về hành vi cuộn hay animation.** Nếu một khẳng định phụ thuộc IO/rAF thì phải
nói thẳng là chưa xác minh được, đừng báo cáo như đã kiểm.

**2. `git push --force` và rewrite lịch sử bị harness chặn.**
`git commit --amend` thì chạy được. `push --force` thì không — phải đưa lệnh cho user chạy tay.

**3. Heredoc trong Bash tool nuốt dấu backslash.**
Viết script Python nhiều `\` hoặc regex bằng heredoc là hỏng. Dùng **Write tool** để tạo
file script, hoặc **Edit tool** cho sửa chính xác. Đã vấp 3 lần.

**4. `python` in ra tiếng Việt bị lỗi encode trên Windows.**
Luôn đặt `PYTHONIOENCODING=utf-8` trước lệnh python nào có in tiếng Việt.

---

## 11. Việc lặt vặt còn treo

- [x] ~~Gỡ 93MB video khỏi lịch sử git~~ ✅ **XONG 21/08.** Remote đã sạch, `.git` 121MB → 5,5MB
- [x] ~~Đưa docs/deliverables lên git~~ ✅ **XONG 23/08.** `.git` chuyển lên gốc project,
      **355 file** trên remote (trước là 68), `.git` 5,6MB → 34MB. Video master vẫn ngoài git
      (`_not-in-theme/` 115MB, `0823.mov` 32MB) — đi Drive như cũ. 96 frame WebP thì CÓ commit
      (11MB, user quyết) để clone về là trang About chạy được ngay
- [x] ~~Hero video không vào git~~ ✅ **XONG 23/08.** Negation trong `.gitignore` trỏ tên thư mục
      theme cũ từ commit `65aed7d`, `*.mp4` nuốt mất `hero-1280.mp4` + `.webm` (3,9MB) mà không
      báo gì. Đổi sang `vitalite-theme/*/video/` để lần đổi tên sau không tái phát
- [x] ~~Nén video hero~~ ✅ **XONG.** 2,43MB mp4 + 1,66MB webm. Kết quả + SSIM: `deliverables/video/encode.md`
- [ ] 🔴 **Đổi link trong bio Instagram** — hiện trỏ về `shopee.vn/vitalitevn`, không phải site.
      7.002 follower là đúng tệp khách website sinh ra để phục vụ. Không đổi link vào ngày
      launch thì họ không bao giờ tới site. *(phát hiện 22/08, chưa có tài liệu nào khác ghi)*
- [ ] 🟡 **`vitalitevn.com` đã chết** — DNS không phân giải. Đó là site của chủ cũ, Google vẫn
      index. Cân nhắc mua lại hoặc ít nhất biết để không nhầm
- [ ] Highlight Instagram vẫn toàn tên **thời kỳ cũ** (White PG · Black PG · Black Porsche ·
      Pink Starlight · White Porsche). Mặt tiền IG đang kể câu chuyện cũ
- [ ] Vector hoá logo sang SVG *(hiện là PNG 995px, header cần SVG cho màn 2x/3x)*
- [ ] `<title>` và tagline: đổi trong `Cài đặt → Chung`, **không phải file theme**
- [ ] Xoá thư mục theme CŨ trên production sau khi chắc bản mới ổn *(nhiều khả năng còn ~96MB
      video master trong đó)*
- [ ] 🔴 **Ngày launch: TẮT "Ngăn công cụ tìm kiếm"** — theme đã cài cảnh báo thường trực trong admin

---

## 12. Cách làm việc user mong đợi

- Đội 5 người trong `CLAUDE.md` — giới thiệu tên trước khi nói, Challenger phản biện thẳng
- **Không bịa** brand fact, product spec, policy. Thiếu thì `[NEED: …]`, không điền đại
- Nêu tác động **LCP** ở mọi quyết định build
- Ràng buộc **solo operator** — không đề xuất gì cần dev team
- Không đụng logic **cart / checkout**
- User deploy bằng **cPanel File Manager** (chưa quen FTP, hosting không có SSH)
