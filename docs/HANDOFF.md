# HANDOFF — VITALITÉ WEBSITE

**Cập nhật:** 2026-09-01 · **Dành cho:** phiên Claude Code mới
**Đọc file này ngay sau `CLAUDE.md`, trước khi làm bất cứ việc gì.**

> ⚠️ **Terminal máy này là Windows PowerShell 5.1 — `&&` KHÔNG tồn tại.**
> Nối lệnh bằng `;`. Viết `&&` là user bấm Run và nhận parser error.

---

## 0. Đứng ở đâu — một đoạn

**Site đang chạy thật và đã có đủ khung.** `vitalite.io.vn`, theme **`Vitalité 2.0` v2.5.0**
ở `wp-content/themes/vitalite-2-0/`. Trang chủ đủ 6 section, 12 trang tĩnh đã publish,
footer tự đầy link, Polylang bật EN/VI, panel quản trị nội dung chạy.

**Thứ còn thiếu là SẢN PHẨM.** Chưa có một SKU nào trong WooCommerce. Mọi việc kỹ thuật còn
lại đều xoay quanh việc mở đường cho lần nhập hàng đầu tiên.

> 🔴 **Git ở GỐC PROJECT** (`E:\Vitalite website\`), không phải `repo/vitalite-website/`.
> Chạy `git` từ gốc.

---

## 1. 🔴 VIỆC KẾ TIẾP — làm theo thứ tự này

Việc trong wp-admin là **user làm, Claude không làm được** (không có SSH, không có
quyền admin). Claude soạn hướng dẫn và kiểm lại kết quả trên site thật.

### Bước A — Dọn plugin *(5 phút, an toàn)*

Đọc từ ảnh chụp user gửi 31/08. Hiện **10 plugin, 8 active**.
User chốt 01/09: **chỉ xoá Akismet.** Hai mục kia giữ nguyên.

| Plugin | Làm gì |
|---|---|
| **Akismet Anti-spam** — inactive | **Xoá.** Chống spam bình luận, mà site không có blog và tab review PDP đã bị `unset` trong `inc/woocommerce.php`. Nó còn cần API key mới chạy |
| **Premmerce Multi-Currency** — inactive | ✅ **GIỮ.** User chốt 01/09: để đó phòng khi sau này cần. Inactive nên không nạp code, chi phí runtime ~0. Vẫn phải cập nhật khi có bản vá |
| **Elementor Pro 4.2.1** | ✅ **KHÔNG cập nhật.** User chốt 01/09. Bản Pro không auto-update được (cần license), và 12 trang tĩnh đang là trang Elementor thật — cập nhật là rủi ro vỡ layout, đổi lấy một patch chưa rõ nội dung. Xem lại nếu 4.2.2 hoá ra là bản vá bảo mật |

### Bước B — ~~Tắt `WP_DEBUG_DISPLAY`~~ ✅ XONG 01/09

User đã sửa `wp-config.php`. Site Health critical về việc in lỗi PHP ra cho khách đã đóng.

⚠️ Ghi lại để lần sau không lặp: **đừng dùng `'sslverify' => false`** để dập cảnh báo
wordpress.org. Đó là tắt kiểm tra chứng chỉ, đổi một cảnh báo lấy một lỗ hổng.

### Bước C — Sửa URL tiếng Việt *(15 phút)*

🔴 **`/vi/` đang chuyển hướng sang `/vi/elementor-28`.** Đo được 31/08. `elementor-28` là
slug tự sinh của một trang Elementor rỗng — nó đang đóng vai trang chủ tiếng Việt.

Cần kiểm trong `Pages`, cột ngôn ngữ của Polylang: trang đó có thật sự được nối làm bản dịch
của trang chủ EN (page ID 28) không, và đổi slug cho tử tế.

Kiểm lại bằng: mở `vitalite.io.vn/vi/` — URL phải **đứng yên ở `/vi/`**, không nhảy đi đâu.

> ℹ️ `/vi/returns` hiện chuyển về `/returns` (bản EN). Đó là **đúng** ở giai đoạn này —
> chưa dịch trang nào. Dịch là bước cuối cùng trước launch.

### Bước D — 🔴 Shipping zone + phương thức thanh toán

**Đây là việc chặn nhập sản phẩm.** Không có zone thì checkout không tính được phí.

| Zone | Cấu hình |
|---|---|
| **Việt Nam** | Flat rate **30.000₫** + một phương thức **Free shipping** |
| **Hoa Kỳ** | Chưa có số. Xem `docs/CHO-DIEN-SAU.md` mục A8 |

🔴 **Phải tạo phương thức "Free shipping" trong zone Việt Nam** thì luật freeship-từ-3-áo
mới chạy. Code đã có sẵn: `inc/woocommerce.php` mục 7, hằng `VT_FREE_SHIP_MIN_QTY = 3`,
`VT_FREE_SHIP_COUNTRY = 'VN'`.

⚠️ Ô **"Minimum order amount"** của Woo ở màn hình đó **vô tác dụng** — chính sách tính theo
*số lượng*, không theo tiền. Theme có admin notice nhắc ngay tại chỗ.

Thanh toán: network log cho thấy **BACS (chuyển khoản) và COD đã bật**. Nhưng brand xác nhận
*chưa có tài khoản kinh doanh*, nên chưa cổng nào cho khách Mỹ. Trang `payment` đang nói
*"phương thức hiện ở checkout"* — nếu tới launch mà khách Mỹ không có gì bấm thì câu đó
thành lời hứa suông.

### Bước E — Nhập **2 sản phẩm test** rồi mới nhập cả bộ

Không được bỏ bước này. Sửa cấu trúc lúc có 2 sản phẩm là 10 phút; lúc có 40 SKU × 6
variation là làm lại từ đầu. Quy ước nhập: **mục 8** bên dưới.

Sau khi có 2 SKU test, kiểm luôn hai thứ đang treo:
- **Premmerce Product Filter có tương thích Polylang không**
- **Kho bên Mỹ là kho thứ hai** — hàng xách tay theo lô, người bên Mỹ giữ hàng và phân phối
  nội địa Mỹ. Woo đang một kho, chưa có cơ chế nào mô tả việc này

### Bước F — Việc còn lại, không chặn ai

- **Menu footer**: `faq` (How to Order) và `collection` hiện **không có link nào trỏ tới**.
  Sửa bằng `Appearance → Menus`, tạo menu gán vào vị trí `Footer — Support`.
  ⚠️ Gán menu là **thay toàn bộ** cột đó, phải tick đủ cả 4 mục đang có.
- **`.htaccess` bảo vệ nội dung** → `deliverables/setup/BAO-VE-NOI-DUNG.md`.
  Làm **sau** khi site chạy ổn, không làm chung lượt với việc khác — `.htaccess` hỏng là
  lỗi 500 trắng trơn và không biết lỗi từ đâu.
- **Redis object cache**: host có hỗ trợ. **Để sau bước E** — nó tăng tốc truy vấn database
  mà hiện chưa có sản phẩm nào để truy vấn. Bật bây giờ là bật mù.
- **Elementor JS thừa**: `frontend.min.js` nạp trên mọi trang và báo
  `elementorFrontendConfig is not defined` rồi chết. Vài trăm KB vô ích. Nhưng 12 trang tĩnh
  **là** trang Elementor thật nên không tắt cả loạt được — phải lọc theo trang, và phải sửa theme.
- **Link bio Instagram** vẫn trỏ `shopee.vn/vitalitevn`. Brand chốt *chỉ thêm, không đổi*.
  Ngày launch phải thêm link site, nếu không 7.001 follower không bao giờ tới.

### Bước G — Ngày launch

1. Dịch VI toàn bộ
2. `Settings → Reading` → **bỏ tick "Discourage search engines"**
   *(hiện đang tick, và đó là ĐÚNG cho tới ngày launch — theme có cảnh báo thường trực trong admin)*

---

## 2. Cấu trúc theme

Nguồn: `repo/vitalite-website/vitalite-theme/vitalite-theme-2/`
Trên hosting: `wp-content/themes/vitalite-2-0/`

> 🔴 **Tên thư mục nguồn ≠ tên thư mục trên hosting.** Thư mục trong zip suy ra từ
> `Theme Name` trong `style.css` qua `slug_from_name()`. Đổi Theme Name là thư mục và tên
> file zip tự đổi theo.

```
style.css                     token + toàn bộ CSS (~81KB thô). Theme Name: Vitalité 2.0
functions.php                 chỉ bootstrap, nạp inc/. VT_VERSION phải khớp style.css
inc/
  helpers.php                 vt_shop_url, vt_page_url, vt_maybe_link, vt_gallery_images…
  setup.php                   theme support, menu, image size, + CHÉP theme_mods khi đổi bản
  enqueue.php                 asset, font, preload LCP
  woocommerce.php             hook Woo · mục 7 = freeship theo SỐ LƯỢNG
  seo.php                     meta, OG, JSON-LD — tự tắt khi có plugin SEO
  admin-options.php           ⭐ Appearance → Vitalité: gallery + 3 slide hero
template-parts/               site-header · site-footer · hero · section-* · product-card
woocommerce/                  archive-product.php · content-product.php (2 file duy nhất bị đè)
assets/
  js/site.js                  slider, header xuyên thấu, menu mobile
  js/admin-options.js         ⭐ media picker + kéo thả, CHỈ chạy trong wp-admin
  gallery/                    8 ảnh — chỉ còn là ĐƯỜNG LÙI, xem mục 8
  video/hero-1280.mp4 + .webm 4,0 MB. Master ở _not-in-theme/, ngoài theme
```

### Đóng gói

```bash
cd "E:/Vitalite website"; python docs/build-theme-zip.py
```

Tự bỏ rác, in ra mọi file > 500 KB, rồi tự kiểm zip. **Luật: tên thư mục trong zip phải
KHÁC mọi thư mục theme đang có trên hosting** — extract đè lên thư mục đã tồn tại là **TRỘN**
chứ không phải thay.

✅ Đổi thư mục **không mất gì**: gallery + hero ở `option`, còn logo và vị trí menu ở
`theme_mods` thì hook `after_switch_theme` trong `inc/setup.php` tự chép sang.

### Ngôn ngữ layout

- **FULL-WIDTH**, lề `clamp(16px, 2.4vw, 32px)`
- **HEADER XUYÊN THẤU** — quyết định ở **một chỗ**: JS tìm `[data-vt-header-sentinel]`.
  Thấy mốc → header trong suốt + bỏ đệm đầu trang. Không thấy → header đục + có đệm.
  🔴 Mốc phải **nằm trong tầm nhìn ở scroll 0**. Khối cao hơn một khung nhìn thì mốc phải
  `position: sticky`, không phải `absolute; bottom:0` — xem `about.src.html`.
- **Không còn eyebrow đánh số** ở bất kỳ đâu (bỏ 30/08)
- Tiêu đề section `clamp(38px, 5.4vw, 84px)` · hero `min(--vt-t-hero, 12vh)`
- Lưới sản phẩm **gap 2px** · nút **bo tròn hoàn toàn**
- **Chiều cao khối lớn đo theo `vh`.** Và ảnh trong ô lưới phải `position:absolute` —
  nếu không chiều cao thật của ảnh kéo cả section (đã xảy ra: ảnh 1050×1400 kéo khối lên 899px)

---

## 3. Quyết định đã chốt — xem bảng đầy đủ ở `CLAUDE.md` mục 5

Những cái mới nhất, dễ bị làm ngược:

| Chủ đề | Chốt |
|---|---|
| Quản trị nội dung | **Theme giữ BỐ CỤC, admin giữ NỘI DUNG.** Panel cố ý KHÔNG cho đổi bố cục |
| Eyebrow đánh số | **ĐÃ BỎ** ở cả trang chủ lẫn 11 trang tĩnh |
| Banner đầu trang | **THÉP GẤP** (`.vt-iri.vt-pagebanner`) |
| Vùng kể chuyện | **VÁNG DẦU** (`.vt-iri`). Hai bề mặt khác nhau là cố ý |
| Chữ header | **weight 800**, giãn `.10em`, không dùng độ mờ |
| Font | **Archivo** (variable, `wdth 100..125`) + **JetBrains Mono**. `Archivo Expanded` KHÔNG tồn tại |
| Ngày trên trang chính sách | Đổi nội dung chính sách thì **phải** đổi ngày. Xem hằng `STAMP` |
| Đơn đi Mỹ | **Xách tay theo lô**, người bên Mỹ phân phối nội địa |

---

## 4. Fact brand — dùng trực tiếp, không hỏi lại

Chi tiết: `reference/BRAND_FACTS_OBSERVED.md` + `reference/BRAND_ERA_SPLIT.md`

| | |
|---|---|
| Tên | **`VITALITÉ ®`** — có dấu sắc, có ® |
| Email · SĐT | `vitalitevn@gmail.com` · **093 838 14 07** |
| Pháp nhân | MST `079203010516` · 766/16/23/26 CMT8, P. Tân Sơn Nhất, TP.HCM |
| Shopee | **4.9★ · 973 đánh giá · 4 năm · 10 SKU** · giá 276.100₫–599.100₫ |
| Vải | Áo thun **250 GSM cotton** · outerwear **500+ GSM cotton blend** |
| Ship nội địa | **SPX** · 30k · freeship từ **3 áo** · nội thành 1 ngày, tỉnh 1–3 ngày · có COD |
| Ship quốc tế | **Mỹ**, 1–2 tuần, **xách tay theo lô** |
| Size | S 70/55 · M 73/58 · L 76/61 (cm) |

### 🔴 Ba con số TUYỆT ĐỐI KHÔNG in ra

- **Năm thành lập.** Brand nói 2023, Shopee hiển thị 4 năm, một bản About cũ ghi 2022 — ba
  con số khác nhau. Không in ở đâu cho tới khi làm rõ. Được phép dùng *"four years"* vì đó
  là con số quan sát được thật trên Shopee.
- **"Worldwide shipping".** Brand trả lời **chỉ Mỹ**. Bio Instagram vẫn ghi worldwide —
  một trong hai phải sửa, nhưng **trang web nói theo brand**.
- **Phí ship quốc tế 200k.** Chưa publish. Xem `docs/ASSUMPTIONS.md`.

### ⛔ Chuỗi bịa đã gỡ, đừng dùng lại
`SS26` · `BST Đường Phố` · `cotton 480GSM` · `in lụa thủ công` · `1.290.000₫` · 8 tên
sản phẩm giả. Script quét: `docs/check-theme.py` mục 5.

---

## 5. 🔴 Rủi ro đã chấp nhận khi publish — KHÔNG phải việc chờ ai

User chốt 30/08: **không hỏi brand nữa.** Thiếu fact thì bỏ hẳn câu đó khỏi trang.

- **`seller-information` thiếu tên đăng ký.** MST 12 số đầu `079` là dạng hộ kinh doanh,
  nên tên trên giấy phép gần như chắc chắn không phải "Vitalité". Nghị định TMĐT đòi tên
  đăng ký. **Đây là thiếu tuân thủ, đã ghi nhận, đã publish.**
- **`terms` không có mục giới hạn trách nhiệm.** Bỏ còn hơn bịa từ bản mẫu. Cần luật sư.
- **Khách Mỹ chưa có phương thức thanh toán.** Xem bước D.

Mọi thứ bị bỏ khỏi trang và cách điền lại: **`docs/CHO-DIEN-SAU.md`**.

---

## 6. Trạng thái trên production — đo 31/08, không phải phỏng đoán

| | |
|---|---|
| Theme | `vitalite-2-0` v2.5.0 · active |
| Trang chủ | Đủ **6 section**, `front-page.php` kiểm soát. *(Cảnh báo cũ "Elementor chiếm quyền" đã hết hiệu lực)* |
| 12 trang tĩnh | 200 hết · slug đúng · 0 eyebrow · 0 ô cam · 0 comment lọt |
| Footer | Tự đầy 2 cột Support + Legal |
| Polylang | EN + VI đã bật, có hreflang. Chưa dịch nội dung |
| Tràn ngang | Sạch trên `/`, `/shop`, `/cart`, `/checkout`, `/my-account` |
| Font | Archivo 800 + JetBrains Mono 800 tải được, `--vt-display-wide: 125%` |
| Sản phẩm | **0** |

---

## 7. Quy ước nhập sản phẩm

| | |
|---|---|
| **Ảnh** | `Product image` = **MẶT TRƯỚC** · gallery ảnh đầu = **MẶT SAU**. Hover đổi trước↔sau. Có meta box nhắc trong màn hình sửa sản phẩm |
| **Category slug** | `t-shirts` · `outerwear` · `bottoms` — **tiếng Anh**, theme dò đúng chuỗi này |
| **Attribute variation** | `pa_size` (S/M/L, Custom ordering) · `pa_color` |
| **Attribute spec** | `pa_fabric` · `pa_fit` · `pa_collection` · `pa_print` — **KHÔNG** tick "used for variations" |
| **Loại sản phẩm** | **Variable.** Shopee tách mỗi màu một listing; Woo gộp thành 1 product |
| **Cân nặng** | 🔴 **Điền cho MỌI SKU ngay lúc nhập.** Miễn phí lúc này, và là thứ duy nhất chặn đường sang tính phí ship theo API sau này |
| **Không tạo category** | `New Arrivals` · `Sale` · `Collection` là *cách sắp xếp*, theme làm bằng `?orderby=date` và `?on_sale=1` |

🔴 **Polylang phải bật TRƯỚC khi tạo attribute.** Attribute term là taxonomy term — tạo
trước khi bật Polylang là phải gán ngôn ngữ tay từng term. *(Polylang đã bật rồi ✅)*

---

## 8. Gallery trang chủ — cách quản lý ĐÃ ĐỔI

**`Appearance → Vitalité`.** Chọn ảnh từ **Media Library**, kéo thả sắp xếp, chọn cỡ ô
(5 cỡ khớp đúng class CSS), alt riêng từng ngôn ngữ. Hero 3 slide cũng ở đây.

Thư mục `assets/gallery/` giờ **chỉ là đường lùi** khi chưa cấu hình gì — và đúng những ảnh
đó bị đè mỗi lần upload theme mới. Đó là lý do có panel.

⚠️ Video hero **cố ý không đưa lên admin**: nó gắn với logic không tải trên mobile và preload
trong `<head>`. Cho đổi trong admin là mở đường cho một file 60 MB rơi vào hero.

---

## 9. Bản đồ tài liệu

| Cần gì | Đọc file |
|---|---|
| **Cái gì bị bỏ khỏi trang và cách điền lại** | **`docs/CHO-DIEN-SAU.md`** 📍 |
| **Mọi giả định + rủi ro đã chấp nhận** | **`docs/ASSUMPTIONS.md`** 🔴 |
| Deploy theme | `deliverables/setup/DEPLOY.md` |
| Bảo vệ nội dung, `.htaccess` | `deliverables/setup/BAO-VE-NOI-DUNG.md` |
| Cấu hình vận chuyển Woo | `deliverables/woo/SHIPPING-SETUP.md` |
| Cấu trúc WooCommerce | `deliverables/woo/STRUCTURE-SETUP.md` |
| Cấu hình WordPress | `deliverables/setup/WORDPRESS-SETUP.md` |
| Plugin nào, không cài gì | `deliverables/setup/PLUGINS.md` |
| Hệ màu, chữ, token | `deliverables/brand/BRAND-GUIDELINE.md` + `tokens.css` |
| Fact brand · brand đổi chủ | `reference/BRAND_FACTS_OBSERVED.md` · `BRAND_ERA_SPLIT.md` 🔴 |
| Chuỗi frame scroll | `deliverables/scroll-sequence/README.md` |
| 50 câu hỏi brand *(hồ sơ, KHÔNG phải việc)* | `deliverables/CAU-HOI-CHO-BRAND.md` |
| SEO · analytics | `deliverables/seo/SEO-PLAN.md` · `deliverables/analytics/TRACKING-PLAN.md` |

### Script

```bash
python docs/check-theme.py "repo/vitalite-website/vitalite-theme/vitalite-theme-2"
python docs/check-tokens.py          # token khớp ở cả ba nơi
python docs/make-pages.py            # sinh 11 trang + about.html + preview
python docs/make-pot.py              # sinh lại .pot
python docs/build-theme-zip.py       # đóng gói theme
python docs/make-guideline.py        # sinh guideline.html từ tokens.css
```

🔴 **Sửa trang tĩnh thì sửa `docs/make-pages.py`, không sửa `.html`** — lần chạy sau ghi đè.
🔴 **Sửa trang About thì sửa `about.src.html`**, `about.html` là bản sinh ra.

---

## 10. 🔴 Hạn chế môi trường — đọc trước khi tự kiểm

**1. Tab browser NỀN cho kết quả sai, không phải chỉ thiếu.**
`IntersectionObserver` và `requestAnimationFrame` không chạy đáng tin ở tab nền — có lượt
không callback lần nào, có lượt treo cả tab 45 giây. Ngày 31/08 nó suýt làm kết luận nhầm
rằng "CSS bị đè" trong khi CSS hoàn toàn bình thường.
→ **Đưa tab ra trước (`tabs_select`) rồi mới đo hành vi cuộn.** Đo cấu trúc tĩnh
(`getBoundingClientRect`, `getComputedStyle`, DOM, số request) thì tab nền vẫn được.

**2. Kiểm "CSS có trong file" KHÁC kiểm "luật có ăn trên trang".**
Đã sai một lần: luật `.vt-woo .vt-woo-page .alignwide` đúng cú pháp, nằm đúng trong file,
và **không bao giờ khớp** vì `.vt-woo` không tồn tại trên trang đó. Phải đo trên trang thật:
tiêm luật vào rồi đo lại `getComputedStyle`.

**3. Heredoc trong Bash tool nuốt dấu backslash.**
Script Python nhiều `\` hoặc regex mà viết bằng heredoc là hỏng. **Dùng Write tool.**
Đã vấp 5 lần.

**4. `python` in tiếng Việt lỗi encode trên Windows.**
Luôn đặt `PYTHONIOENCODING=utf-8` trước lệnh python nào có in tiếng Việt.

**5. `git push --force` bị harness chặn.** `git commit --amend` thì chạy được.

**6. Không có PHP CLI.** `docs/check-theme.py` thay được phần lớn nhưng **không thay được
`php -l`**.

---

## 11. Cách làm việc user mong đợi

- Đội 5 người trong `CLAUDE.md` — giới thiệu tên trước khi nói, Challenger phản biện thẳng
- **Không bịa** brand fact, product spec, policy. Thiếu thì **bỏ hẳn câu đó**, không để ô cam
- **Đo trên site thật trước khi báo đã sửa.** User đã bắt được một lần báo sai
- Nêu tác động **LCP** ở mọi quyết định build
- Ràng buộc **solo operator** — không đề xuất gì cần dev team
- Không đụng logic **cart / checkout**
- User deploy bằng **cPanel File Manager** (hosting không có SSH)
- Sửa CSS thôi thì **gửi file lẻ**, đừng bắt upload lại cả theme
