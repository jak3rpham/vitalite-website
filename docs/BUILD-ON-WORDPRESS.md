# KẾ HOẠCH DỰNG SITE TRÊN WORDPRESS

**Cập nhật:** 2026-08-21 · **Đọc sau:** `CLAUDE.md` → `docs/HANDOFF.md`

Đây là **runbook chủ**. Nó không lặp lại nội dung các file khác — nó xếp thứ tự và
nói rõ *vì sao thứ tự đó*, chỗ nào không được đảo. Chi tiết từng bước nằm ở file được
dẫn link.

---

## 0. Đọc trước: ba luật không được phá

**Luật 1 — Polylang phải bật TRƯỚC khi tạo attribute và nhập sản phẩm.**
Attribute term (`S`, `M`, `L`, mỗi màu) là taxonomy term. Tạo trước rồi mới bật
Polylang thì phải vào gán ngôn ngữ **tay từng term và từng SKU**. Với 40 sản phẩm ×
6 biến thể thì đó là một buổi chiều làm việc vô nghĩa.

**Luật 2 — nhập ĐÚNG 2 sản phẩm test rồi dừng lại kiểm.**
Sửa cấu trúc lúc có 2 sản phẩm là 10 phút. Lúc có 40 sản phẩm là làm lại từ đầu.
Bước này **không được bỏ**, kể cả khi thấy mọi thứ đang chạy ngon.

**Luật 3 — không bật LiteSpeed minify CSS/JS.**
Xung đột với Elementor. Đã chốt trong `CLAUDE.md`, đừng thử lại.

---

## 1. Bản đồ: cái gì dựng bằng gì

Đây là câu trả lời cho "site này build kiểu gì". Không phải mọi thứ đều Elementor,
cũng không phải mọi thứ đều code.

| Phần của site | Dựng bằng | File / nơi chỉnh |
|---|---|---|
| Header · Footer | **Theme PHP** | `template-parts/site-header.php` · `site-footer.php` |
| Trang chủ | **Theme PHP** | `front-page.php` — 6 section |
| Shop · Category · Tag | **Theme PHP** đè Woo | `woocommerce/archive-product.php` |
| Thẻ sản phẩm (mọi nơi) | **Theme PHP** | `template-parts/product-card.php` — sửa một chỗ, đổi mọi nơi |
| Trang sản phẩm (PDP) | **WooCommerce mặc định** + hook | `inc/woocommerce.php` — bảng size chèn bằng hook |
| Giỏ hàng · Thanh toán · Tài khoản | **WooCommerce mặc định** + lớp sơn CSS | Khung ở `page.php`, sơn ở `style.css` |
| 6 trang tĩnh (About, Shipping…) | **Elementor hoặc trình soạn thảo** | Nội dung: `deliverables/content/PAGES-CONTENT.md` |
| Bài viết đơn | **Theme PHP** | `single.php` — lưới an toàn, site chưa có blog |

**Header/footer KHÔNG dùng Elementor Theme Builder.** Đã chốt (`CLAUDE.md` mục 5).
Lý do kỹ thuật giờ mạnh hơn lúc chốt: hệ thống **header xuyên thấu** sống trong theme
(`vt_top_banner_tone()`, `.is-transparent`, `.is-light-bg`, sentinel, header trượt).
Elementor Theme Builder không biết trang nào có banner tối để đảo màu chữ.
Chuyển sang Elementor = **vứt toàn bộ phần đó đi**.

### Đường lui vẫn còn nguyên
Mỗi section trang chủ là một template part độc lập **và đều có shortcode**:
`[vt_banner]` `[vt_products]` `[vt_collection]` `[vt_gallery]` `[vt_services]`.
Muốn chuyển trang chủ sang Elementor: tạo trang Elementor → chèn shortcode → đặt làm
trang chủ → xoá `front-page.php`. Không phải viết lại gì.

---

## 2. Thứ tự thực thi

```
┌─ HẠ TẦNG ────────────────────────────────────────────────
│ 1. Backup UpdraftPlus                          ✅ XONG
│ 2. Dọn theme + nén video                       ✅ XONG (122MB → 5.8MB)
│ 3. Deploy theme song song → đổi theme → xem    ← ĐANG Ở ĐÂY
│ 4. Cấu hình WordPress cơ bản
│ 5. LiteSpeed Cache
├─ NGÔN NGỮ (chặn phần dưới) ──────────────────────────────
│ 6. Polylang — 6 quyết định, CHƯA dịch gì
├─ SẢN PHẨM ───────────────────────────────────────────────
│ 7. Tạo attribute + category
│ 8. Nhập 2 SẢN PHẨM TEST → kiểm toàn bộ luồng → sửa
│ 9. Nhập phần còn lại
├─ NỘI DUNG ───────────────────────────────────────────────
│ 10. 6 trang tĩnh + menu
│ 11. Ảnh gallery trang chủ
├─ LAUNCH ─────────────────────────────────────────────────
│ 12. Dịch VI
│ 13. Kiểm lần cuối → TẮT "Ngăn công cụ tìm kiếm"
└──────────────────────────────────────────────────────────
```

---

## 3. Bước 3 — Deploy theme

📄 **`deliverables/setup/DEPLOY.md`**

Quy trình **song song, lùi lại được trong 5 giây**: upload thư mục theme mới bên cạnh
thư mục cũ, đổi theme trong wp-admin, hỏng thì đổi ngược lại. Không đè lên bản đang chạy.

Theme giờ 5.8MB nên nén và upload qua cPanel File Manager mất vài giây.

**Kiểm ngay sau khi đổi theme — 6 điểm:**

1. Trang chủ: hero 3 slide tự chạy, thanh điều hướng đổi màu ở slide 3 (nền trắng)
2. Cuộn xuống: header **trượt lên ẩn**, cuộn lên thì hiện lại
3. Trang shop: banner váng dầu tối, **header trong suốt đè lên nó**, chữ header trắng
4. Cuộn qua khỏi banner: header thành kính trắng, chữ đen
5. Rê chuột lên thẻ sản phẩm: ảnh đổi mặt trước ↔ sau, nút S/M/L hiện ra **thành một hàng ngang**
6. Thu cửa sổ xuống 375px: mọi thứ trên vẫn đúng, banner thấp lại, header 64px

Điểm 5 là bài kiểm cho lỗi `<a>` lồng `<a>` đã sửa. Nếu S/M/L xếp **dọc và có gạch chân**
thì theme chưa được thay đúng.

---

## 4. Bước 4 — Cấu hình WordPress

📄 **`deliverables/setup/WORDPRESS-SETUP.md`**

Bốn thứ phải đúng trước khi đi tiếp:

| | |
|---|---|
| Tiêu đề + tagline | `Cài đặt → Chung`. **KHÔNG sửa trong file theme** |
| Permalink | `/%postname%`, **không** trailing slash |
| Múi giờ | `Cài đặt → Chung` → Ho Chi Minh |
| Ngăn công cụ tìm kiếm | **BẬT** trong lúc build, tắt ở bước 13 |

Theme đã cài **cảnh báo thường trực trong wp-admin** khi "Ngăn công cụ tìm kiếm"
còn bật — để không ai quên vào ngày launch.

---

## 5. Bước 5 — LiteSpeed Cache

📄 **`deliverables/setup/HOSTING-LITESPEED.md`**

🔴 **Minify CSS/JS = TẮT.** Xung đột Elementor. Không thương lượng.

Bật cache trang, bật object cache nếu host cho, gzip/brotli bật.

---

## 6. Bước 6 — Polylang 🔴 CHẶN BƯỚC 7 VÀ 8

📄 **`docs/I18N-SETUP.md`**

Sáu quyết định đã chốt, chỉ việc set:

| | |
|---|---|
| Ngôn ngữ | EN (mặc định, ở root) · VI (ở `/vi/`) |
| Auto-detect ngôn ngữ trình duyệt | **TẮT** |
| Media translation | **TẮT** |
| Chuyển ngôn ngữ | chữ `EN / VI`, **không dùng cờ** |
| URL | `/` cho EN, `/vi/` cho VI |
| Dịch nội dung | **CHƯA dịch gì ở bước này.** Build xong EN mới dịch |

**Bật Polylang trước, không dịch gì cả.** Mục đích của bước này chỉ là để mọi term
và mọi post tạo ra từ đây về sau **tự có ngôn ngữ**, khỏi gán tay.

### Chuỗi giao diện của theme
`languages/vitalite.pot` — **90 chuỗi**, đã sinh sẵn.

Đây là chuỗi *giao diện* (nút, nhãn, thông báo), **không phải** nội dung.
Dịch bằng Poedit → lưu thành `vitalite-vi.po` + `vitalite-vi.mo` → thả vào
`languages/`. `load_theme_textdomain()` trong `inc/setup.php` tự nạp.

⚠️ **Sửa theme thì phải sinh lại**, nếu không chuỗi mới không dịch được:
```bash
cd "E:\Vitalite website"; python docs/make-pot.py
```

Nội dung (tên sản phẩm, mô tả, chính sách) dịch bằng **Polylang**, không phải file này.

---

## 7. Bước 7 — Attribute và category

📄 **`deliverables/woo/STRUCTURE-SETUP.md`**

### Category — slug phải ĐÚNG CHUỖI NÀY
`t-shirts` · `outerwear` · `bottoms`

**Slug tiếng Anh.** Theme dò theo đúng ba chuỗi này để dựng link trên trang chủ.
Đặt slug tiếng Việt là link trang chủ trỏ vào hư không.

### KHÔNG tạo ba category này
`New Arrivals` · `Sale` · `Collection`

Chúng là **cách sắp xếp**, không phải phân loại. Theme đã làm bằng
`?orderby=date` và `?on_sale=1`. Tạo thành category là chia đôi kho hàng
và làm hỏng SEO bằng nội dung trùng.

### Attribute

| Attribute | Dùng cho biến thể? | Giá trị |
|---|---|---|
| `pa_size` | ✅ **CÓ** | S · M · L — đặt **Custom ordering**, nếu không nó sắp theo abc thành L, M, S |
| `pa_color` | ✅ **CÓ** | theo màu thật của từng dòng |
| `pa_fabric` | ❌ KHÔNG | `250 GSM Cotton` · `500+ GSM Heavyweight Cotton Blend` |
| `pa_fit` | ❌ KHÔNG | `Signature Boxy Fit`… |
| `pa_collection` | ❌ KHÔNG | THE ICONIC · THE MOMENTS · PINK GRAFFITI · PORSCHE · STARLIGHT · OLD MONEY |
| `pa_print` | ❌ KHÔNG | |

Bốn cái dưới **không được tick "Used for variations"** — chúng là thông số, không phải
lựa chọn mua hàng. Tick nhầm sẽ sinh ra hàng trăm biến thể rác.

---

## 8. Bước 8 — HAI sản phẩm test 🔴 KHÔNG ĐƯỢC BỎ

Nhập **đúng 2** sản phẩm: **một áo thun và một áo khoác**. Hai loại vì chúng đi qua
hai nhánh code khác nhau (bảng size chỉ hiện cho áo thun).

### Quy ước nhập ảnh — sai là hỏng hiệu ứng
| | |
|---|---|
| `Product image` | **MẶT TRƯỚC** |
| `Gallery` ảnh **đầu tiên** | **MẶT SAU** |

Rê chuột trên lưới sẽ đổi trước ↔ sau. Theme đã cài **meta box nhắc** ngay trong màn
hình sửa sản phẩm.

Sản phẩm phải là **Variable**. Shopee tách mỗi màu thành một listing; trên Woo gộp
thành **một product nhiều biến thể**.

### Kiểm 12 điểm rồi mới đi tiếp

**Lưới và thẻ**
1. Sản phẩm hiện đúng trên trang chủ và trang shop
2. Rê chuột đổi ảnh trước ↔ sau
3. Nút S/M/L hiện ra **một hàng ngang**, bấm vào ra PDP đã chọn sẵn size
4. Badge `New` / `Sale` / `Sold out` đúng trạng thái

**Trang sản phẩm**
5. Chọn size → giá và ảnh cập nhật
6. **Bảng size hiện ở áo thun**, và **KHÔNG hiện ở áo khoác** (chưa có số đo hoodie)
7. Thêm vào giỏ → **badge giỏ trên header tăng số**

**Giỏ và thanh toán** — phần vừa dựng, kiểm kỹ
8. Trang giỏ: bảng **không bị bóp**, ảnh sản phẩm đúng kích thước
9. Đổi số lượng → cập nhật đúng
10. Trang thanh toán: form hai cột trên desktop, một cột trên mobile
11. **Trên điện thoại thật**: bấm vào ô nhập → **trang KHÔNG tự phóng to**
12. Nút đặt hàng chiếm hết chiều ngang

Điểm 11 là lỗi mất đơn kinh điển trên iOS. Đã xử bằng `font-size: 16px` cho ô nhập
ở mobile, nhưng phải kiểm trên máy thật.

**Vỡ chỗ nào sửa chỗ đó, RỒI mới sang bước 9.**

---

## 9. Bước 9 — Nhập phần còn lại

Đã có bảng số đo dùng chung: **S 70/55 · M 73/58 · L 76/61** — áp cho cả hàng thời kỳ cũ.

Hàng thời kỳ cũ nhập như hàng bình thường, **không tách category `Archive`** (đã chốt).

🔴 `THE MOMENTS BOXY HOODIE` **chưa có số đo nào**. Theme cố ý **không hiện bảng size**
cho sản phẩm ngoài danh mục áo thun — không hiện còn hơn hiện sai. Có số đo thật thì
bổ sung vào `inc/woocommerce.php`.

---

## 10. Bước 10 — Trang tĩnh và menu

📄 **`deliverables/content/PAGES-CONTENT.md`**

Sáu trang: About · Size Guide · Shipping · Returns · Contact · Collection.

🔴 **Hai trang KHÔNG viết được cho tới khi có fact thật:**

| Trang | Thiếu gì |
|---|---|
| **Shipping** | Phí + hãng + thời gian ship quốc tế · thuế ai chịu · ship tới nước nào |
| **Trang pháp lý** | Tên pháp nhân · mã số ĐKKD · địa chỉ đăng ký — **bắt buộc theo pháp luật TMĐT Việt Nam** |

Claude **không viết text pháp lý** và không bịa phí ship. Hai trang này chờ user.

Shopee cho thấy brand **đã có pháp nhân** — chỉ cần lấy thông tin ra, không phải đăng ký mới.

---

## 11. Bước 11 — Ảnh gallery trang chủ

Thả file vào `assets/gallery/`, đặt tên `01-…` `02-…`.
**Số ở đầu quyết định ô to hay nhỏ** — mẫu lặp theo chu kỳ 8.

Không cần vào wp-admin. Cache 12 giờ — chưa thấy đổi thì xoá transient `vt_gallery`.

---

## 12. Bước 12 — Dịch VI

Chỉ làm khi **bản EN đã xong hết và đã kiểm**.

1. Chuỗi giao diện: Poedit → `vitalite-vi.po` + `.mo` vào `languages/`
2. Nội dung: Polylang, từng trang và từng sản phẩm
3. Menu: Polylang tạo bộ menu riêng cho VI

---

## 13. Bước 13 — Launch

| | |
|---|---|
| 🔴 | **TẮT "Ngăn công cụ tìm kiếm"** — `Cài đặt → Đọc`. Quên bước này là site vô hình |
| | Gửi sitemap lên Google Search Console 📄 `deliverables/seo/SEO-PLAN.md` |
| | Gắn GA4 📄 `deliverables/analytics/TRACKING-PLAN.md` |
| | Đặt một đơn hàng thật bằng tiền thật, rồi hoàn lại |
| | Backup lần nữa |

Đơn hàng thật là bài kiểm duy nhất đáng tin cho luồng thanh toán. Sandbox không bắt
được lỗi cấu hình tài khoản nhận tiền.

---

## 14. Đang chặn — không đi tiếp được nếu thiếu

| | Chặn cái gì |
|---|---|
| 🔴 **Phí + hãng + thời gian ship quốc tế** | Multi-currency · shipping zone · trang Shipping · **và thực tế chặn launch** |
| 🔴 **Thông tin pháp nhân** | Bắt buộc theo pháp luật TMĐT Việt Nam |
| 🔴 **Số đo hoodie** | PDP hoodie không có bảng size |
| 🟡 Mã hex tím / xanh dương thời kỳ mới | `--vt-accent` đang là đen tạm. Có mã thì đổi **đúng một biến CSS** |
| 🟡 Có hiện "4.9★ · 973 đánh giá Shopee" không | Social proof thật, dẫn nguồn được — nhưng gửi khách sang Shopee. **Quyết định kinh doanh** |

Về ship quốc tế, con số đáng lo: áo ~280.000₫ (~$11) mà ship quốc tế $25–40 thì
**phí gấp 3 lần giá hàng**. Đây là rủi ro mô hình kinh doanh, không phải rủi ro kỹ thuật.
Website tồn tại là để bán cho khách quốc tế (IG 7.001 follower, bio ghi
`Worldwide shipping`, Shopee.vn không phục vụ quốc tế). Nếu phí ship giết chết chuyện
đó thì phải biết **trước** khi launch, không phải sau.

---

## 15. Sau mỗi lần sửa theme

> ⚠️ **Terminal máy này là Windows PowerShell 5.1.** `&&` không tồn tại ở đó —
> nối lệnh bằng `;`. Mọi lệnh trong tài liệu dự án viết theo cú pháp PowerShell.

```bash
cd "E:\Vitalite website"; python docs/check-theme.py "repo/vitalite-website/vitalite-theme/vitalite-theme"
```

```bash
cd "E:\Vitalite website"; python docs/make-pot.py
```

Kiểm 7 mục: cân bằng cú pháp · hàm `vt_*` chưa định nghĩa · `get_template_part()` trỏ
file có thật · class CSS thiếu rule · **chuỗi bịa còn sót** · `echo` biến chưa escape ·
text-domain nhất quán.

⚠️ Nó **không thay được `php -l`**. Máy không có PHP CLI.
