# BỘ FILE SẴN SÀNG NHẬP SẢN PHẨM

**Ngày:** 2026-09-12 · **Cho:** nhập hàng vào WooCommerce, không phải đi tìm file nữa
**Đi kèm:** `deliverables/woo/product-images/` (16 ảnh)

---

## 0. Hai thứ trong gói này

| Thứ | Ở đâu | Làm gì với nó |
|---|---|---|
| **16 ảnh sản phẩm** | `product-images/` | Upload thẳng vào Media Library |
| **Bảng nhập bên dưới** | file này | Vừa nhập vừa nhìn, mục 3 |

---

## 1. Cột cờ ngôn ngữ — KHÔNG tắt, và đó là đúng

Đã thử hai lần tắt bằng filter `pll_get_taxonomies`: đặt trong theme, rồi đặt trong
mu-plugin. **Cả hai đều không ăn.** Polylang for WooCommerce đăng ký `pa_*` bằng cơ chế
riêng, filter đó không với tới.

Tra tài liệu chính thức mới thấy đó không phải lỗi mà là **thiết kế**:

> *"You must translate the attributes and their terms before using them in your products.
> Otherwise you will have some synchronization issues between the product translations."*
> — Polylang, *Managing WooCommerce Products*

→ Né bằng code là đi ngược plugin, và cái giá là lỗi đồng bộ giữa bản dịch sản phẩm —
đúng thứ sẽ nổ lúc có 40 SKU chứ không phải lúc có 2.

### Cách làm đúng: dịch term, nhưng ĐẶT TÊN Y HỆT TIẾNG ANH

`Products → Attributes → Color → Configure terms` → bấm `+` ở cột 🇻🇳 → ô **Name** gõ
**`Black`** (không phải `Đen`) → Save.

Polylang tự thêm hậu tố vào *slug* để không trùng, nhưng **tên term vẫn là `Black`**.
`vt_product_color_swatches()` map theo **tên**, nên chấm màu trên `/vi/` vẫn đúng.
**Không phải sửa theme dòng nào.**

| Attribute | Số term | Tên bản VI |
|---|---|---|
| `pa_color` | 5 | y hệt EN — `Black` `Cream` `Grey` `Pure White` `White` |
| `pa_size` | 3 | y hệt EN — `S` `M` `L` |
| `pa_collection` | 7 | y hệt EN — tên riêng, không dịch |
| `pa_print` | 1 | `In lụa` ✅ dịch được, không ảnh hưởng gì |
| `pa_fabric` · `pa_fit` | 4 | ✅ **dịch thật** — đây là chỗ dịch có ích |

**Tổng 20 term, làm một lần.** Không phải việc lặp lại — thêm màu mới sau này mới phải
thêm một cặp.

🔴 **Làm trước khi nhập sản phẩm đầu tiên.** Đúng lời cảnh báo của vendor: nhập SKU trước
rồi mới dịch term là tự tạo lỗi đồng bộ.

> **Dọn rác của hai lần thử hỏng:**
> — Xoá `wp-content/mu-plugins/vitalite-shared-attributes.php` khỏi hosting nếu đã upload
> — Mục 9 trong `inc/woocommerce.php` của theme là code chết, vô hại. Gỡ ở lần deploy sau

## 2. 🔴 Đính chính `reference/BRAND_ASSETS_AUDIT.md`

Audit ngày 19/08 đọc 19 mockup thành "8 dòng sản phẩm" và kết luận *"chỉ có mockup phẳng"*,
*"phần lớn SKU không có ảnh"*. **Đọc lại từng ảnh ngày 12/09: sai.**

File đi theo **cặp mặt trước + mặt sau của CÙNG một áo**, không phải mỗi file một sản phẩm:

- `1` (script nhỏ ngực, đen) và `2` (graffiti xanh in lưng, đen) là **hai mặt của một áo**
- `6` (script hồng lớn mặt trước) và `5` (chữ `lité` mặt sau) cũng vậy — bản in chạy vòng thân áo

→ Không phải 8 dòng. Là **4 sản phẩm, mỗi cái 2 màu, mỗi màu đủ trước + sau.**
→ Đúng cái quy ước hover theme cần: `Product image` = trước, gallery ảnh đầu = sau.

`17` (OLD MONEY) và `18` (quần) là **bản vẽ kỹ thuật phẳng** — không có wordmark đầu ảnh,
không có nền blob, `18` còn có chú thích số đo tiếng Việt. **Không phải ảnh sản phẩm,
không đưa lên site.** `19` rỗng 7KB.

---

## 3. Bảng nhập — 4 sản phẩm

Tất cả đều **Variable product**, category **T-Shirts** trừ hoodie (**Outerwear**).

### 3.0 — Giá và tồn kho — áp cho MỌI sản phẩm

**User chốt 12/09:** giá gốc hiển thị đúng như Shopee, cộng đúng % giảm như Shopee.
Trong WooCommerce nghĩa là hai ô, không phải một:

| Ô Woo | Điền gì |
|---|---|
| **Regular price** | Giá **gạch ngang** trên Shopee *(giá gốc)* |
| **Sale price** | Giá **đang bán** trên Shopee *(sau giảm)* |

Woo tự tính và hiện `-14%`. Không phải gõ % vào đâu cả.

🔴 **Còn thiếu đúng hai con số.** Đo Shopee 12/09: trang shop công khai cho xem header
nhưng **chặn danh sách sản phẩm, đòi đăng nhập** — Claude không đăng nhập tài khoản của bạn.
`reference/BRAND_FACTS_OBSERVED.md` chỉ ghi giá **sau giảm** và **%**, không ghi giá gạch ngang.

**Tính ngược ra giá gốc là bịa số** — `276.100 ÷ 0,84 = 328.690,47`, một con số không ai
đặt bao giờ. % trên Shopee là số đã làm tròn, nên phép chia ngược không ra giá thật.

→ Mở Shopee, đọc **giá gạch ngang** của hai thứ, điền vào đây:

| Sản phẩm | Giá đang bán *(đã biết)* | Giá gạch ngang *(cần bạn)* |
|---|---|---|
| Áo thun — `PINK GRAFFITI ĐEN` | `276.100₫` · -16% | `[CHỜ]` |
| Áo thun — các mã còn lại | `282.680₫` · -14% | `[CHỜ]` |
| Hoodie `THE MOMENTS` | `599.100₫` · -14% | `[CHỜ]` |

*(Nếu mọi áo thun dùng chung một giá gốc thì chỉ cần 2 con số.)*

**Tồn kho — user chốt: KHÔNG quản lý.**
Trong tab *Inventory* của từng sản phẩm: **bỏ tick** `Manage stock?`, để `Stock status` = `In stock`.
Không nhập số ở cấp variation.

⚠️ Đánh đổi đã chấp nhận: bán quá số hàng thật thì phải tự xin lỗi khách. Đổi sang quản lý
tồn kho sau được, **không phải làm lại sản phẩm** — chỉ tick lại ô đó.

### 3.1 — ICONIC

| | |
|---|---|
| Category | `T-Shirts` · `pa_collection` `The Iconic` |
| `pa_color` | `Black` · `White` |
| `pa_size` | `S` `M` `L` |
| `pa_fabric` | `250 GSM Cotton` |
| `pa_fit` | `Unisex Regular` |
| `pa_print` | `Silkscreen` |
| Variation | **6** |

| Màu | Product image *(trước)* | Gallery ảnh đầu *(sau)* |
|---|---|---|
| Black | `graffiti-blue-black-front.webp` | `graffiti-blue-black-back.webp` |
| White | `graffiti-blue-white-front.webp` | `graffiti-blue-white-back.webp` |

### 3.2 — Pink Graffiti

Mặt sau in `2023©VITALITÉ SIGNATURE COLLECTION` → `pa_collection` = **`Signature`**.

| | |
|---|---|
| Category | `T-Shirts` · `pa_collection` `Signature` |
| `pa_color` | `Black` · `White` |
| Vải / fit / print | `250 GSM Cotton` · `Unisex Regular` · `Silkscreen` |
| Variation | **6** |
| Ghi chú | Shopee ghi **bán chạy nhất, 2k+ đã bán** |

| Màu | Trước | Sau |
|---|---|---|
| Black | `pink-graffiti-black-front.webp` | `pink-graffiti-black-back.webp` |
| White | `pink-graffiti-white-front.webp` | `pink-graffiti-white-back.webp` |

🔴 **Số file bị ngược:** mặt trước là `6.webp`, mặt sau là `5.webp`. Đã đổi tên đúng
trong `product-images/` rồi — cứ theo tên file, đừng theo số.

### 3.3 — Need Money For Porsche

| | |
|---|---|
| Category | `T-Shirts` · `pa_collection` `Porsche` |
| `pa_color` | `Black` · `White` |
| Vải / fit / print | `250 GSM Cotton` · `Unisex Regular` · `Silkscreen` |
| Variation | **6** |

| Màu | Trước | Sau |
|---|---|---|
| Black | `porsche-black-front.webp` | `porsche-black-back.webp` |
| White | `porsche-white-front.webp` | `porsche-white-back.webp` |

✅ **User chốt 12/09: `White`**, không phải `Cream`. Dùng chung term với các áo trắng khác.

### 3.4 — The Moments Boxy Hoodie

| | |
|---|---|
| Category | **`Outerwear`** |
| `pa_color` | `Grey` · `Pure White` |
| `pa_fabric` | `500+ GSM Heavyweight Cotton Blend` |
| `pa_fit` | `Signature Boxy Fit` |
| `pa_collection` | `The Moments` |
| Variation | **6** |

| Màu | Trước | Sau |
|---|---|---|
| Grey | `moments-hoodie-grey-front.webp` | `moments-hoodie-grey-back.webp` |
| Pure White | `moments-hoodie-pure-white-front.webp` | `moments-hoodie-pure-white-back.webp` |

🔴 **PDP hoodie sẽ KHÔNG hiện bảng size** — `inc/woocommerce.php:222` chỉ hiện cho category
`t-shirts`, và hoodie chưa có số đo riêng. Đó là **cố ý**: không hiện còn hơn hiện số sai.
Có số đo thật thì xem `docs/CHO-DIEN-SAU.md`.

### 3.5 — ✅ Tên `ICONIC` — cách suy ra, để sau này kiểm lại được

Audit cũ gán `ICONIC` cho mặt trước và `STARLIGHT` cho mặt sau — hai tên cho **một cái áo**.

Chốt `ICONIC`, căn cứ:

1. `reference/BRAND_FACTS_OBSERVED.md` đọc được **7/10 listing Shopee**: PINK GRAFFITI ×2,
   PORSCHE, **ICONIC ×2**, THE MOMENTS HOODIE ×2
2. Ba trong bốn mockup đã khớp tên Shopee: pink graffiti · porsche · hoodie
3. `ICONIC` là **tên áo thun Shopee duy nhất còn lại chưa gán**
4. Audit mô tả ICONIC là *"script ngực nhỏ"* — đúng mặt trước `1`/`3`

`STARLIGHT` là tên line có thật *(mục 7 `BRAND_FACTS_OBSERVED.md`)* nhưng **không phải áo này** —
nhiều khả năng là một trong 3 SKU Shopee chưa đọc được, hoặc hàng chỉ bán qua IG.

⚠️ Đây là **suy luận từ bằng chứng**, không phải fact đọc trực tiếp. Mở được listing Shopee
thì đối chiếu lại ảnh. Sai thì đổi tên sản phẩm — không ảnh hưởng cấu trúc.

## 4. Ảnh — ba điều cần biết trước khi upload

| | |
|---|---|
| **Kích thước** | `1000×1000` — đây là **trần**, không có bản lớn hơn. Woo zoom muốn ≥1600px, nên **zoom ở PDP sẽ mờ**. Chấp nhận, hoặc chụp lại |
| **Định dạng** | WebP, 9–36 KB/ảnh, tổng **310 KB** cho cả 16. Bản PNG gốc cùng 1000px nhưng 145–530 KB — **đừng dùng PNG**, cùng số điểm ảnh mà nặng gấp 15 lần |
| **LCP** | 16 ảnh × ~19 KB trung bình. Grid shop archive tải 8 ảnh ≈ **150 KB** — không đe doạ mốc LCP < 2,5s. Đây là lý do giữ WebP |

**Alt text khi upload** — Media Library lấy từ tên file, sửa lại cho người đọc:
`VITALITÉ Pink Graffiti T-Shirt, màu đen, mặt trước` chứ không phải `pink-graffiti-black-front`.

---

## 5. Còn thiếu gì

| | Trạng thái |
|---|---|
| **Giá gạch ngang Shopee** | 🔴 **CHẶN** — 2–3 con số, xem mục 3.0 |
| Giá sau giảm | ✅ đã có trong `BRAND_FACTS_OBSERVED.md` |
| Tồn kho | ✅ chốt: không quản lý, `In stock` |
| Tên sản phẩm | ✅ chốt cả 4 |
| Màu | ✅ chốt |
| **Cân nặng (kg)** | 🟡 cân một áo thun + một hoodie. Không chặn lưu sản phẩm, nhưng điền bù cho 40 SKU là mở lại từng cái |
| Số đo hoodie | ⚪ không chặn — PDP hoodie cố ý không hiện bảng size |

## 6. Thứ tự bấm

```
1. Thêm term còn thiếu: pa_collection (7) + pa_print (Silkscreen)
2. Dịch VI cho 20 term — GIỮ TÊN TIẾNG ANH, xem mục 1   ← chặn bước 5
3. Upload 16 ảnh vào Media Library, sửa alt
4. Shipping zone                                      ← chặn checkout
5. Nhập 2 sản phẩm TEST: Pink Graffiti + The Moments Hoodie
6. Kiểm 8 mục ở STRUCTURE-SETUP.md mục 7
7. Vỡ chỗ nào sửa chỗ đó, RỒI mới nhập 2 cái còn lại
```

Bước 5 chọn đúng hai cái đó là cố ý: một áo thun (có bảng size) + một hoodie (không có
bảng size) — kiểm được cả hai nhánh của `inc/woocommerce.php:222` trong một lượt.
