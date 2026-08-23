# WOOCOMMERCE — CẤU TRÚC DANH MỤC & THUỘC TÍNH
**Cho:** user tự setup trong wp-admin · **Ngày:** 2026-08-19
**Căn cứ:** `reference/BRAND_FACTS_OBSERVED.md` · `reference/BRAND_ERA_SPLIT.md`

---

## ⛔ 0. ĐỌC TRƯỚC — hai thứ chặn, không được bỏ qua

### 0.1 — Polylang phải xong TRƯỚC khi tạo sản phẩm

CLAUDE.md mục 6, bước 5 trước bước 8. Lý do cụ thể ở đây:
attribute term (`Black`, `White`, `S`, `M`, `L`) là **taxonomy term** — Polylang dịch term
theo cơ chế riêng. Tạo term trước khi bật Polylang cho product taxonomy
→ phải gán ngôn ngữ tay cho **từng term và từng sản phẩm**.

**Thứ tự đúng:** cấu hình Polylang → bật ngôn ngữ cho `product`, `product_cat`, `pa_*` → rồi mới tạo term.

### 0.2 — ✅ ĐÃ CHỐT: hệ size là `S / M / L`

User chốt 2026-08-19: **toàn bộ catalog theo thời kỳ mới. Chỉ một hệ size: `S / M / L`.**
Hàng thời kỳ cũ cũng chuyển sang S/M/L, không giữ 1/2/3 song song.

✅ **Bảng số đo: user chốt S/M/L dùng CHUNG bảng cũ.** Hết chặn.

| Size | Dài (cm) | Rộng (cm) | Chiều cao | Cân nặng |
|:--:|:--:|:--:|---|---|
| **S** | 70 | 55 | 1m55 – 1m65 | dưới 60kg |
| **M** | 73 | 58 | 1m60 – 1m75 | dưới 75kg |
| **L** | 76 | 61 | 1m75 – 1m9 | dưới 100kg |

> *(*) Trong quá trình sản xuất hàng loạt, các thông số có độ chênh lệch từ 2-3cm so với thông số trên.*

Câu disclaimer giữ nguyên khi lên trang Size Guide — nó là lá chắn cho tỷ lệ đổi trả.
Bảng trên áp cho **áo thun**. Hoodie `THE MOMENTS` vẫn chưa có số đo riêng.



---

## 1. Product Categories

`Sản phẩm → Danh mục` — **slug tiếng Anh** (EN là ngôn ngữ mặc định tại root).

```
T-Shirts          slug: t-shirts
Outerwear         slug: outerwear
Bottoms           slug: bottoms          ← tạo sẵn, ẩn cho tới khi có hàng
```

**Không tạo:** `New Arrivals`, `Sale`, `Collection`, `Best Sellers`.
Đó **không phải danh mục** — chúng là *cách sắp xếp* của cùng một tập sản phẩm.
Làm bằng shop archive + tham số sắp xếp / filter, không phải bằng category riêng.
Tạo category cho chúng là tự tạo trùng lặp nội dung và loãng SEO.

> Nav hiện tại đang trỏ `/new-arrivals` và `/sale` → cả hai đang 404.
> Sửa thành `/shop?orderby=date` và `/shop?on_sale=1` (hoặc trang shop có filter sẵn), không tạo page mới.

Danh mục Shopee `Thời Trang Nữ > Áo > Áo thun` là taxonomy của Shopee, **không mang sang**.
Mọi sản phẩm đều Unisex — **không tạo danh mục Nam / Nữ.**

### 1.1 — Không dùng `Archive`

User chốt: **hàng thời kỳ cũ treat như hàng bình thường.** Không tách category, không tách filter.
Pink Graffiti / Porsche / Starlight nằm chung `T-Shirts` với The Iconic.

*(Bỏ đề xuất category `Archive` ở bản trước. `pa_collection` vẫn giữ — nó phục vụ lọc theo dòng
sản phẩm, không phải để tách cũ/mới.)*

---

## 2. Attributes — chia làm hai nhóm, đây là chỗ hay sai nhất

`Sản phẩm → Thuộc tính`. Phân biệt rõ:

- **Nhóm A — dùng cho variation:** khách chọn, ảnh hưởng giá/tồn kho/SKU
- **Nhóm B — spec, KHÔNG variation:** thông tin mô tả, dùng để lọc và hiển thị bảng

Đưa nhầm nhóm B vào variation → nổ số variation theo cấp số nhân. 3 size × 2 màu = 6.
Thêm nhầm fabric và fit vào → 6 × 2 × 2 = 24 variation cho một sản phẩm chỉ có 6 SKU thật.

### Nhóm A — variation

| Attribute | Slug | Terms | Ghi chú |
|---|---|---|---|
| **Size** | `pa_size` | **`S` `M` `L`** | ✅ *Used for variations* · Archive ordering: **Custom ordering** (không alphabet — `L, M, S` sai thứ tự) |
| **Color** | `pa_color` | `Black` `White` `Grey` `Pure White` `Cream` | ✅ *Used for variations* |

Term màu lấy đúng tên brand đang dùng: `PURE WHITE` và `GREY` là tên Shopee dùng cho hoodie;
`White` cho áo thun. Giữ nguyên, đừng gộp `Pure White` vào `White` — chúng là hai sản phẩm khác nhau.

### Nhóm B — spec, KHÔNG tick "Used for variations"

| Attribute | Slug | Terms |
|---|---|---|
| **Fabric** | `pa_fabric` | `250 GSM Cotton` · `500+ GSM Heavyweight Cotton Blend` |
| **Fit** | `pa_fit` | `Signature Boxy Fit` · `Unisex Regular` |
| **Collection** | `pa_collection` | `The Iconic` · `The Moments` · `Starlight` · `Pink Graffiti` · `Porsche` · `Old Money` · `Signature` |
| **Print** | `pa_print` | `Silkscreen` *(“In lụa” — fact thật từ Shopee PDP)* |

Bốn cái này đổ thẳng vào tab **Additional Information** của PDP — đúng khuôn 4 gạch đầu dòng
mà chủ mới đã dùng trên IG (`• Fabric: … • Fit: … • Sizing: …`). **Không viết lại thành văn xuôi.**

> `pa_collection` thay cho việc tạo category cho từng drop. Một sản phẩm thuộc **một** loại
> (T-Shirt) nhưng có thể thuộc collection nào cũng được — hai trục độc lập, nên phải là
> hai taxonomy khác nhau, không phải category lồng nhau.

---

## 3. Sản phẩm phải là Variable, không phải Simple

Trên Shopee mỗi màu là **một listing riêng**:
```
Áo Thun VITALITÉ PINK GRAFFITI Unisex - ĐEN     276.100₫
Áo Thun VITALITÉ PINK GRAFFITI Unisex - TRẮNG   282.680₫
```

Trên site phải gộp thành **một Variable Product**:

```
Product:  VITALITÉ Pink Graffiti T-Shirt
  ├─ pa_color: Black, White        (used for variations)
  ├─ pa_size:  S, M, L             (used for variations)
  ├─ pa_fabric:     250 GSM Cotton         (spec)
  ├─ pa_fit:        Unisex Regular         (spec)
  ├─ pa_collection: Pink Graffiti          (spec)
  └─ 6 variation, mỗi variation có giá + tồn kho + SKU riêng
```

Giá khác nhau giữa màu là bình thường — set giá ở cấp variation.

**Ba việc bắt buộc ở cấp variation:**
1. **Ảnh riêng theo màu.** Chọn màu Black → ảnh đổi sang mockup áo đen. Không set thì khách chọn màu mà ảnh đứng im.
2. **SKU riêng.** Gợi ý: `VTL-PG-BLK-M`. Cần cho tồn kho và đối soát với Shopee.
3. **Quản lý tồn kho ở cấp variation**, không phải cấp product.

**Tách hay không tách:** `THE MOMENTS BOXY HOODIE` PURE WHITE và GREY → **một product, hai variation màu.**
Nhưng `The Iconic` và `Pink Graffiti` → **hai product riêng** (đồ hoạ khác nhau hoàn toàn).
Nguyên tắc: **cùng thân áo, khác màu → variation. Khác đồ hoạ → product riêng.**

---

## 4. Premmerce Filter — map lại

Premmerce đang cấu hình lọc theo Size, Color. Sau khi có thêm attribute, cấu hình lại:

| Attribute | Hiện trên filter? | Kiểu |
|---|---|---|
| `pa_size` | ✅ | button |
| `pa_color` | ✅ | swatch màu |
| `pa_collection` | ✅ | checkbox |
| `pa_fabric` | ⬜ tuỳ | checkbox |
| `pa_fit` | ❌ | chỉ hiển thị ở PDP |
| `pa_print` | ❌ | chỉ hiển thị ở PDP |

⚠️ **Chưa test Premmerce với Polylang** (vẫn nằm trong OPEN ITEMS của CLAUDE.md).
Test bằng **2 sản phẩm giả** trước khi nhập thật. Nếu filter vỡ ở bản dịch VI thì
phát hiện lúc có 2 SKU dễ hơn lúc có 40.

---

## 5. Thứ tự thao tác

```
1. ~~Chốt hệ size~~ ✅ S/M/L
2. Cấu hình Polylang, bật cho product + taxonomy  ← CHẶN bước 4
3. Tạo product categories (mục 1)
4. Tạo attributes + terms (mục 2)
5. Cấu hình Premmerce (mục 4)
6. Nhập 2 sản phẩm test — 1 áo thun, 1 hoodie
7. Test: filter · variation · ảnh đổi theo màu · thêm giỏ · checkout · bản VI
8. Vỡ chỗ nào sửa chỗ đó, RỒI mới nhập phần còn lại
```

**Bước 6–7 không được bỏ.** Sửa cấu trúc lúc có 2 sản phẩm là 10 phút.
Lúc có 40 sản phẩm × 6 variation là làm lại từ đầu.

---

## 6. Multi-currency — nêu ràng buộc thật trước khi chọn plugin

User muốn multi-currency. Nhưng vấn đề thật **không nằm ở chỗ hiển thị giá.**

### Ràng buộc cứng

| Cổng thanh toán | Loại tiền quyết toán được |
|---|---|
| MoMo / VNPay | **Chỉ VND** |
| PayPal | USD, EUR, và nhiều loại khác |
| Stripe | **Không hỗ trợ merchant VN trực tiếp** *(đã ghi trong CLAUDE.md)* |

→ Khách quốc tế trả bằng USD thì **chỉ đi được qua PayPal**.
→ Plugin multi-currency đổi được **con số hiển thị**, nhưng **không tạo ra được khả năng quyết toán**.

### Hai mô hình

| | Cách làm | Ưu | Nhược |
|---|---|---|---|
| **A. Hiển thị đa tiền tệ, thu VND** | Đổi tỉ giá để hiển thị, checkout tính VND | Đơn giản, không đụng gateway, 1 loại tiền đối soát | Khách nước ngoài thấy VND ở bước cuối → **rơi đơn ở checkout** |
| **B. Thu thật đa tiền tệ** | VND qua MoMo/VNPay, USD qua PayPal | Trải nghiệm quốc tế đúng nghĩa | Hai luồng quyết toán, hai bảng đối soát, cấu hình phức tạp hơn nhiều |

**Khuyến nghị: A trước, B sau.** Launch bằng A — hiển thị USD/EUR, thu VND, nói rõ ở PDP và checkout.
Có đơn quốc tế thật rồi mới làm B. Làm B trước khi có đơn nào là đầu tư vào giả định.

### 🔴 Câu chưa ai trả lời

**Phí ship quốc tế bao nhiêu, đi hãng nào, bao lâu?**

Đây không phải chi tiết nhỏ. Một cái áo 280.000₫ (~$11) mà ship quốc tế $25–40 thì
**phí ship gấp 3 lần giá hàng.** Toàn bộ chiến lược quốc tế phụ thuộc con số này.
Cần biết trước khi build checkout, và trước khi chốt có làm multi-currency thật hay không.

**Chưa có con số này thì chưa quyết được A hay B.**

### Về plugin

Chưa đề xuất plugin cụ thể. Chọn plugin trước khi chốt A/B là chọn ngược.
Chốt mô hình rồi mới chọn — và khi chọn sẽ nêu rõ: làm gì, nặng bao nhiêu, có cách native không.
Mô hình A phần lớn làm được **không cần plugin nào**.

---

## 7. Chưa có, cần trước khi nhập hàng loạt

- [ ] 🔴 **Bảng số đo cm cho S/M/L** — chặn trang Size Guide
- [ ] Giá site cho từng SKU — bán bằng Shopee, hay bằng giá gốc chưa giảm?
- [ ] Số đo + chất liệu `THE MOMENTS BOXY HOODIE`
- [ ] Spec `OLD MONEY` varsity longsleeve và dòng quần
- [ ] 3/10 SKU Shopee chưa liệt kê được
- [ ] Phí + thời gian ship quốc tế
- [x] ~~Chính sách đổi trả~~ ✅ giữ nguyên 5 ngày, khách chịu ship 2 chiều
