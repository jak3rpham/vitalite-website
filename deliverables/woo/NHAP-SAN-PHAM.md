# BỘ FILE SẴN SÀNG NHẬP SẢN PHẨM

**Ngày:** 2026-09-12 · **Cho:** nhập hàng vào WooCommerce, không phải đi tìm file nữa
**Đi kèm:** `deliverables/woo/product-images/` (16 ảnh) · `deliverables/woo/mu-plugin/`

---

## 0. Ba thứ trong gói này

| Thứ | Ở đâu | Làm gì với nó |
|---|---|---|
| **16 ảnh sản phẩm** | `product-images/` | Upload thẳng vào Media Library |
| **1 file mu-plugin** | `mu-plugin/vitalite-shared-attributes.php` | Upload vào `wp-content/mu-plugins/` — sửa lỗi cột cờ ngôn ngữ |
| **Bảng nhập bên dưới** | file này | Vừa nhập vừa nhìn, mục 3 |

---

## 1. 🔴 Sửa lỗi cột cờ ngôn ngữ — làm TRƯỚC

Filter đặt trong theme **không ăn**. Lý do là thứ tự nạp của WordPress:

```
mu-plugins  →  plugins (Polylang)  →  theme functions.php
```

Polylang chốt danh sách taxonomy được dịch ngay khi nó khởi động — **trước** khi file theme
được đọc. Filter đăng ký trong theme là đăng ký sau khi tàu đã chạy.

**Cách sửa:** upload `mu-plugin/vitalite-shared-attributes.php` vào
`wp-content/mu-plugins/`. Chưa có thư mục đó thì tạo. **Không cần kích hoạt** — mu-plugin
luôn chạy, không hiện trong danh sách Plugins.

**Kiểm:** `Products → Attributes → Color → Configure terms` → **hai cột cờ phải biến mất.**

> Mục 9 trong `inc/woocommerce.php` của theme giờ là code chết. Vô hại, để đó,
> gỡ ở lần deploy theme kế tiếp. Ghi lại ở đây để sáu tháng nữa không ai đi tìm hai chỗ.

---

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

### 3.1 — Áo graffiti xanh *(⚠️ tên sản phẩm chưa chốt, xem 3.5)*

| | |
|---|---|
| Category | `T-Shirts` |
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

⚠️ Bản trắng (`9`/`10`) trông hơi ngả ấm so với bản trắng của áo khác. **Trắng hay kem —
bạn xác nhận.** Nếu là kem thì term là `Cream`, không phải `White`.

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

### 3.5 — ⚠️ Một tên sản phẩm tôi không tự quyết được

Audit cũ gọi mặt trước là `ICONIC` và mặt sau là `STARLIGHT` — **hai tên cho một cái áo.**
Một trong hai sai. Shopee có listing tên `ICONIC`; `STARLIGHT` audit ghi *"chỉ IG"*.

**Bạn biết sản phẩm, bạn chốt.** Tôi không đoán tên SKU — đó là fact, không phải copy.
Tên file `graffiti-blue-*` chỉ là nhãn tạm để nhận dạng, đổi thoải mái.

---

## 4. Ảnh — ba điều cần biết trước khi upload

| | |
|---|---|
| **Kích thước** | `1000×1000` — đây là **trần**, không có bản lớn hơn. Woo zoom muốn ≥1600px, nên **zoom ở PDP sẽ mờ**. Chấp nhận, hoặc chụp lại |
| **Định dạng** | WebP, 9–36 KB/ảnh, tổng **310 KB** cho cả 16. Bản PNG gốc cùng 1000px nhưng 145–530 KB — **đừng dùng PNG**, cùng số điểm ảnh mà nặng gấp 15 lần |
| **LCP** | 16 ảnh × ~19 KB trung bình. Grid shop archive tải 8 ảnh ≈ **150 KB** — không đe doạ mốc LCP < 2,5s. Đây là lý do giữ WebP |

**Alt text khi upload** — Media Library lấy từ tên file, sửa lại cho người đọc:
`VITALITÉ Pink Graffiti T-Shirt, màu đen, mặt trước` chứ không phải `pink-graffiti-black-front`.

---

## 5. 🔴 Ba thứ CHƯA CÓ — không lấy được từ ảnh

Nhập được cấu trúc, ảnh, attribute. **Không nhập được sản phẩm hoàn chỉnh nếu thiếu ba thứ này:**

| | Vì sao chặn |
|---|---|
| **Giá từng variation** | Bằng giá Shopee đang bán, hay giá gốc chưa giảm? Chưa chốt thì không lưu được sản phẩm |
| **Cân nặng (kg)** | Cân một áo thun + một hoodie là đủ, dùng chung cả dòng. Điền lúc nhập là miễn phí; điền bù cho 40 SKU là mở lại từng cái |
| **Tồn kho mỗi variation** | Hoặc tắt quản lý tồn kho và để `In stock` — nhưng phải quyết, không để mặc định |

Thiếu số đo hoodie thì **không phải thứ chặn** — đã xử lý bằng cách không hiện bảng size.

---

## 6. Thứ tự bấm

```
1. Upload mu-plugin  → kiểm cột cờ biến mất          ← chặn mọi thứ sau
2. Upload 16 ảnh vào Media Library, sửa alt
3. Thêm term pa_collection (Signature, Porsche, The Moments) + pa_print (Silkscreen)
4. Shipping zone                                      ← chặn checkout
5. Nhập 2 sản phẩm TEST: Pink Graffiti + The Moments Hoodie
6. Kiểm 8 mục ở STRUCTURE-SETUP.md mục 7
7. Vỡ chỗ nào sửa chỗ đó, RỒI mới nhập 2 cái còn lại
```

Bước 5 chọn đúng hai cái đó là cố ý: một áo thun (có bảng size) + một hoodie (không có
bảng size) — kiểm được cả hai nhánh của `inc/woocommerce.php:222` trong một lượt.
