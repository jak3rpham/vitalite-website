# I18N SETUP — Polylang

**Mục tiêu:** setup đúng NGAY BÂY GIỜ, để sau này nhập bản dịch chỉ tốn công sửa title + description.
**Chốt:** EN default tại root, VI tại `/vi/`. Build EN xong hết → làm VI → **launch cả hai cùng lúc**.

> ⚠️ **6 quyết định dưới đây phải xong TRƯỚC khi nhập bất kỳ sản phẩm nào.**
> Sai một cái là sau này phải sửa tay từng SKU.

---

## Quyết định 1 — Ngôn ngữ mặc định = English, giấu prefix

`Polylang → Settings → URL modifications`
- ✅ `Hide URL language information for the default language`
- Kết quả: EN ở `vitalite.io.vn/shop`, VI ở `vitalite.io.vn/vi/shop`

⚠️ Đổi ngôn ngữ mặc định **sau khi** đã có content = URL đổi hàng loạt. **Chốt EN-default bây giờ.**

---

## Quyết định 2 — Permalink không trailing slash

`Settings → Permalinks → Custom: /%postname%`

**Biết trước giới hạn — đây là WP core, không phải bug:**

| | Có slash? |
|---|---|
| Page / Post / Product | ❌ không (đúng ý) |
| Category archive `/product-category/tops/` | ✅ có |
| Pagination `/shop/page/2/` | ✅ có |
| Woo endpoint `/my-account/orders/` | ✅ có |

Site sẽ **mixed**. Không sai SEO (canonical xử lý được). Muốn đồng nhất tuyệt đối phải viết rewrite rule + redirect — **không đáng công** ở giai đoạn này.

---

## Quyết định 3 — TẮT dịch Media

`Polylang → Settings → Media → tắt`

**Item tiết kiệm thời gian lớn nhất.** Bật lên thì mỗi ảnh phải có bản EN và VI riêng trong Media Library. Fashion 8–10 ảnh/SKU = địa ngục. Ảnh không có chữ → không cần dịch.

---

## Quyết định 4 — Taxonomy: tạo EN trước rồi DỊCH, không tạo song song

**Chỗ 90% người làm sai và không cứu được.**

```
✅ ĐÚNG
   Tạo category "Tops" (EN) → bấm + trong Language box → tạo bản dịch "Áo" (VI)
   → Polylang biết 2 cái này LÀ MỘT

❌ SAI
   Tạo "Tops" (EN) và tạo riêng "Áo" (VI) như 2 category độc lập
   → sản phẩm VI không liên kết EN → filter vỡ, hreflang vỡ
```

Áp dụng cho: **product category, attribute terms (giá trị Size/Color), tag**.

⚠️ **Premmerce Product Filter đang cài** filter theo attribute term. Term VI không liên kết term EN → filter ở trang VI trả kết quả rỗng.
`[NEED: test Premmerce × Polylang compatibility]`

---

## Quyết định 5 — Slug VI không dấu

`ao-thun` ✅ · `áo-thun` ❌

WP encode Unicode slug thành `%C3%A1o-thun` — xấu khi share link, một số analytics parse sai.

---

## Quyết định 6 — Nav menu: tạo 2 menu ngay từ đầu

Polylang tự thêm ô chọn ngôn ngữ cho menu.
Tạo menu EN bây giờ → gán vào location `primary`. Sau này duplicate → sửa label → gán bản VI.
Chỉ có 1 menu → trang VI hiện label EN.

---

## Plugin bắt buộc

### Polylang for WooCommerce — trả phí, ~€99/năm · BẮT BUỘC

Không có nó thì:
- Product không có ô chọn ngôn ngữ
- Attribute / category không dịch đúng
- **Stock KHÔNG sync giữa 2 bản** → bán 1 áo ở EN, bản VI vẫn hiện còn hàng → **oversell**

Cái stock sync là **rủi ro vận hành thật**, không phải tiện nghi.

### Loco Translate — free

Dịch string theme ngay trên browser, không đụng code. Điều kiện: mọi string trong theme phải bọc `__()`.

---

## Workflow nhập sản phẩm (sau khi setup đúng)

```
1. Tạo product EN đầy đủ (title, desc, ảnh, giá, size, stock)
2. Language box → bấm + cạnh cờ VI
3. Polylang duplicate TOÀN BỘ: ảnh, giá, SKU, attribute, stock, category
4. Chỉ sửa: title, description, short description   ← việc tay DUY NHẤT
5. Save
```

Bước 4 chỉ ngắn được nếu 6 quyết định trên làm đúng từ đầu.

---

## String trong theme

Hiện tại hardcode hết: `SEARCH`, `ACCOUNT`, `CART`, fallback nav `Shop All / Áo / Quần`.

```php
// SAI
<a href="#">SEARCH</a>

// ĐÚNG
<a href="#" class="vt-util-link"><?php esc_html_e('Search', 'vitalite-theme'); ?></a>
```

Có số đếm thì dùng `_n()`:
```php
sprintf(_n('Shopping bag, %d item', 'Shopping bag, %d items', $count, 'vitalite-theme'), $count)
```

**Quy ước:** viết Title Case trong code (`'Search'`), để CSS `text-transform: uppercase` lo hiển thị.
Lý do: tiếng Việt uppercase toàn bộ mất dấu khó đọc — sau này chỉ bỏ `text-transform` ở bản VI, không sửa string.

---

## Sửa ngay trong `header-woocommerce.php`

```php
// HIỆN TẠI — switcher biến mất trên mọi trang chưa dịch
'hide_if_no_translation' => 1

// ĐỔI THÀNH
'hide_if_no_translation' => 0
```

Với kế hoạch "EN xong hết rồi mới làm VI", giá trị `1` làm switcher ẩn/hiện thất thường suốt giai đoạn build → user tưởng code hỏng.

---

## hreflang

Polylang tự output. Hai điều phải kiểm:

1. **Phải có `x-default` trỏ về EN** — báo Google "không match ngôn ngữ nào thì dùng bản này". Khớp đúng chủ ý "mặc định tiếng Anh".
2. **Chỉ một nguồn hreflang.** Nếu cài Yoast/RankMath, cả hai có thể output → duplicate tag → Google bỏ qua cả hai. Tắt ở SEO plugin, để Polylang lo.

---

## Auto-detect ngôn ngữ theo browser — KHÔNG DÙNG

User có hỏi. Đã bác. Ba lý do:

**1. Cache poisoning.** LiteSpeed full-page cache lưu HTML theo URL. Redirect quyết định bởi `Accept-Language` → người Việt vào đầu tiên thì bản VI bị cache cho URL đó → người Mỹ tiếp theo nhận trang tiếng Việt. Muốn đúng phải cấu hình cache vary theo `Accept-Language` — LiteSpeed × Polylang phần này rất dễ vỡ và nhân đôi cache entry.

**2. SEO.** Googlebot crawl từ IP Mỹ với `Accept-Language: en`. Redirect → Googlebot có thể không bao giờ thấy bản VI. Google khuyến nghị **không auto-redirect** theo ngôn ngữ; dùng hreflang + để user tự chọn.

**3. Signal không đáng tin với người Việt.** Rất nhiều người Việt để browser/OS tiếng Anh nhưng muốn đọc tiếng Việt khi mua hàng. Ngược lại người Việt ở nước ngoài để tiếng Việt lại muốn EN vì ship quốc tế.

**Thay bằng:**
- Default EN tại `/`, VI tại `/vi/`
- Language switcher **hiện rõ trong header** (text `EN / VI`, không dùng cờ — cờ đại diện quốc gia chứ không phải ngôn ngữ, và cờ Anh cho English là sai với khách Mỹ/Úc/Singapore, đúng nhóm "international" đang nhắm)
- Lần chọn lưu cookie, lần sau tôn trọng cookie (cache exclude chỉ cho việc này, nhẹ hơn nhiều)
- hreflang đầy đủ + `x-default` → EN
- Không redirect Googlebot

Vẫn đạt kết quả mong muốn (khách quay lại thấy đúng ngôn ngữ) mà không phá cache, không phá SEO.

---

## Auto-translate

Polylang core **không** có. Các đường:

| Cách | Ghi chú |
|---|---|
| Polylang Pro + DeepL | Free tới 500k ký tự. Chỉ dịch string chưa có bản dịch, không ghi đè bản đã sửa tay. **Không tự cập nhật khi sửa bài gốc** — phải sửa tay hoặc xoá và dịch lại. |
| AutoPoly (free addon) | Dịch được page Elementor giữ nguyên style. Dựa vào Yandex / Chrome built-in AI — chất lượng không đoán trước. Thêm 1 plugin vào stack. |
| WPML | Auto-translate mạnh hơn nhưng nặng hơn Polylang đáng kể trên shared hosting. |

**Khuyến nghị:**

| Dùng auto-translate | KHÔNG dùng |
|---|---|
| Nav label, button, footer link, UI string | PDP description |
| | Size guide |
| | Policy (đổi trả, vận chuyển, bảo hành) |

Lý do: sizing/fit dịch máy sai = **rủi ro trả hàng**; policy sai điều khoản = **rủi ro pháp lý**; voice fashion không survive dịch máy ("oversized fit, dropped shoulder" → tiếng Việt máy dịch ra thứ không ai đọc).

Với ~17 SKU hiện có, **dịch tay nhanh hơn sửa bản dịch máy dở**.

---

## Ảnh hưởng lên thiết kế homepage

**Elementor page KHÔNG auto-dịch.** Homepage VI = duplicate page Elementor rồi gõ lại từng text widget. Mỗi lần sửa layout EN phải sửa lại VI.

→ **Homepage càng ít text widget rời rạc, công dịch càng nhẹ.**

Trùng với nguyên tắc fashion visual-first. Cụ thể khi thiết kế:

- Gom text thành **ít block lớn**, đừng rải 15 text widget nhỏ
- Section heading lấy từ **Woo category name** (dynamic) thay vì gõ tay → Polylang dịch tự động theo category
- Product card dùng **Loop Grid / Products widget**, không hardcode → Woo tự trả product theo ngôn ngữ hiện tại
- Chỉ hero copy + 2–3 editorial block là text tay

Làm đúng thì homepage VI tốn ~20 phút thay vì nửa ngày.
