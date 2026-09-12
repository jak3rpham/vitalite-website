# WOOCOMMERCE — CẤU TRÚC & QUY TRÌNH MỞ ĐƯỜNG NHẬP SẢN PHẨM

**Cập nhật:** 2026-09-08 · **Thay thế hoàn toàn** bản 19/08
**Cho:** user tự bấm trong wp-admin (Claude không có SSH, không có quyền admin)
**Đây là bước E** trong `docs/HANDOFF.md`.

> 🔴 Bản 19/08 có ba chỗ đã lỗi thời, ai còn cầm thì bỏ:
> — "EN là ngôn ngữ mặc định tại root" → sai, từ 05/09 là **`/en` + `/vi`, cả hai đều có prefix**
> — mục 6 hỏi "phí ship quốc tế bao nhiêu" → đã có đáp án: **xách tay theo lô, phân phối nội địa Mỹ**
> — mục 7 liệt bảng số đo là blocker → đã chốt S/M/L, đã nằm trong `inc/woocommerce.php`

---

## 0. Trạng thái ngay lúc này — đo 08/09

| | |
|---|---|
| `/` → `/en/` | ✅ 302 đúng, hreflang + canonical đã sạch |
| `sample-page` | ✅ đã xoá, trả 404 |
| Polylang EN + VI | ✅ đang chạy, chưa dịch nội dung |
| Product categories | ✅ **đã có** — `t-shirts` · `outerwear` · `bottoms` đều trả 200 *(đo 08/09)* |
| Attributes | ✅ **đã tạo 6 cái**, Custom ordering. `pa_collection` + `pa_print` **chưa có term** |
| Dịch attribute | ⚠️ **không tắt được** — phải dịch, giữ tên EN cho `pa_color`. Xem 1.1 |
| Shipping zone | ❌ chưa có — **chặn checkout, không chặn attribute** |
| Sản phẩm | **0** |

**Thứ tự dưới đây là thứ tự bấm. Không đảo.** Lý do từng chỗ ghi ngay tại chỗ đó.

---

## 1. 🔴 QUYẾT ĐỊNH PHẢI CHỐT TRƯỚC KHI TẠO TERM ĐẦU TIÊN

### 1.1 — Term attribute PHẢI dịch, và cách dịch để không vỡ chấm màu

**Không tắt được dịch cho `pa_*`.** Đã thử filter `pll_get_taxonomies` ở cả theme lẫn
mu-plugin, cả hai đều không ăn — Polylang for WooCommerce đăng ký attribute taxonomy bằng
cơ chế riêng. Và theo tài liệu chính thức thì dịch term là **bắt buộc**, không dịch sẽ
sinh lỗi đồng bộ giữa các bản dịch sản phẩm.

🔴 **Rủi ro thật:** `inc/helpers.php` map **tên term** sang mã màu
(`'black' => '#0A0A0A'`…). Dịch `Black` thành `Đen` → không khớp → rơi về `#DDDDE1`,
**mọi chấm màu trên `/vi/` thành xám, không có cảnh báo nào.**

**Cách tránh — đặt tên bản dịch Y HỆT tiếng Anh:** bấm `+` ở cột 🇻🇳, ô Name gõ `Black`.
Polylang tự thêm hậu tố vào slug, tên giữ nguyên → chấm màu vẫn đúng.

| Attribute | Bản VI đặt tên |
|---|---|
| `pa_color` · `pa_size` · `pa_collection` | **y hệt tiếng Anh** — bắt buộc với `pa_color` |
| `pa_print` · `pa_fabric` · `pa_fit` | dịch thật, thoải mái |

Chi tiết + thứ tự làm: `deliverables/woo/NHAP-SAN-PHAM.md` mục 1.

### 1.2 — Thuế

Site đang bán với tư cách **hộ kinh doanh** (MST `079203010516`). Giá Shopee hiện tại là
giá cuối khách trả.

**Khuyến nghị: để `Enable taxes` TẮT.** Giá nhập vào Woo là giá khách trả, không tính thêm gì.
Bật thuế là phải khai thuế suất, và một khi bật thì mọi giá đã nhập phải xem lại nghĩa là
giá trước hay sau thuế.

⚠️ Đây là **policy fact**, không phải copy. Nếu kế toán nói khác thì làm theo kế toán —
nhưng phải quyết **trước** khi nhập SKU đầu tiên, không phải sau.

---

## 2. Bấm gì — Woo General Settings

`WooCommerce → Settings → General`

| Ô | Giá trị | Vì sao |
|---|---|---|
| Selling location | **Sell to specific countries** → `Vietnam`, `United States` | Không mở Mỹ ở đây thì zone Mỹ ở mục 5 vô dụng |
| Shipping location | **Ship to specific countries** → `Vietnam`, `United States` | Cùng lý do |
| Default customer location | `Shop base address` | |
| Enable taxes | **bỏ tick** | Xem 1.2 |
| Currency | `Vietnamese đồng (₫)` · Position **Right** · Thousand sep `.` · Decimal sep `,` · **Decimals `0`** | VND không có phần lẻ. Để `2` là giá hiện `280.000,00 ₫` |

`WooCommerce → Settings → Products`

| Ô | Giá trị |
|---|---|
| Weight unit | **kg** |
| Dimensions unit | **cm** |
| Enable reviews | **bỏ tick** — tab review đã bị `unset` trong `inc/woocommerce.php`, để bật là dữ liệu treo lơ lửng |

---

## 3. Product Categories

`Products → Categories`. **Slug phải đúng chuỗi tiếng Anh dưới đây** — theme dò cứng:
`inc/woocommerce.php:222` chỉ hiện bảng size khi sản phẩm thuộc `t-shirts` / `tshirts` / `ao-thun`.

```
T-Shirts     slug: t-shirts      ← bảng size tự hiện ở PDP nhờ slug này
Outerwear    slug: outerwear
Bottoms      slug: bottoms       ← tạo sẵn, chưa có hàng
```

**Không tạo:** `New Arrivals` · `Sale` · `Collection` · `Best Sellers` · `Nam` · `Nữ` · `Archive`.

- Ba cái đầu là **cách sắp xếp**, làm bằng `?orderby=date` và `?on_sale=1`. Tạo category
  cho chúng là tự tạo trùng nội dung.
- Mọi sản phẩm đều Unisex → không có category giới tính.
- Hàng thời kỳ cũ (Pink Graffiti / Porsche / Starlight) nằm chung `T-Shirts` với The Iconic.
  User đã chốt: **không tách `Archive`**.

Danh mục Shopee `Thời Trang Nữ > Áo > Áo thun` là taxonomy của Shopee, **không mang sang**.

---

## 4. Attributes — chỗ hay sai nhất

`Products → Attributes`. Hai nhóm, đừng trộn.

Trộn nhầm là nổ số variation theo cấp số nhân: 3 size × 2 màu = 6 variation thật.
Thêm nhầm fabric + fit vào variation → 6 × 2 × 2 = **24 variation** cho một sản phẩm chỉ có 6 SKU.

### Nhóm A — sẽ dùng cho variation

🔴 **Ô "Used for variations" KHÔNG nằm ở màn hình `Products → Attributes`.** Nó không phải
thuộc tính của attribute mà của **cặp (sản phẩm, attribute)** — cùng một `pa_color` có thể là
variation ở sản phẩm này và chỉ là spec ở sản phẩm khác. Xem mục 6.1.

| Name | Slug | Terms | Ghi chú bắt buộc |
|---|---|---|---|
| **Size** | `size` → thành `pa_size` | `S` `M` `L` | 🔴 Đặt `Custom ordering` **chưa đủ** — phải vào `Configure terms` và **kéo thả** cho đúng S→M→L. Chưa kéo thì vẫn ra `L, M, S` |
| **Color** | `color` → thành `pa_color` | `Black` `White` `Grey` `Pure White` `Cream` | 🔴 **Tên term phải viết đúng y như vậy** — xem 1.1. `Pure White` và `White` là hai term khác nhau, đừng gộp |

> Ô "Slug" khi tạo attribute nhập `size`, WooCommerce tự thêm tiền tố `pa_`.
> Nhập `pa_size` là thành `pa_pa_size`.

`template-parts/product-card.php:85` đọc `pa_size` để in tối đa 4 size lên thẻ sản phẩm ở
trang shop, mỗi size là một link lọc sẵn. Không có `pa_size` thì phần đó im lặng biến mất.

### Nhóm B — spec, **không** đưa vào variation

| Name | Slug | Terms |
|---|---|---|
| **Fabric** | `pa_fabric` | `250 GSM Cotton` · `500+ GSM Heavyweight Cotton Blend` |
| **Fit** | `pa_fit` | `Signature Boxy Fit` · `Unisex Regular` |
| **Collection** | `pa_collection` | `The Iconic` · `The Moments` · `Starlight` · `Pink Graffiti` · `Porsche` · `Old Money` · `Signature` |
| **Print** | `pa_print` | `Silkscreen` |

Bốn cái này đổ vào tab **Details** của PDP (`inc/woocommerce.php` đã đổi nhãn từ
*Additional information*). Đúng khuôn 4 gạch đầu dòng brand vẫn dùng trên IG.
**Không viết lại thành văn xuôi trong Description.**

`pa_collection` thay cho việc tạo category cho từng drop: một sản phẩm thuộc **một** loại
(T-Shirt) nhưng thuộc collection nào cũng được — hai trục độc lập, phải là hai taxonomy.

### 4.1 — Polylang: không phải bấm gì, nhưng phải ĐO một thứ

`Languages → Settings → Custom post types and Taxonomies` **không liệt kê** `product`,
`product_cat`, `product_tag` hay `pa_*`. Đo 08/09: danh sách chỉ còn hai mục Elementor
(`Floating Elements`, `My Templates`).

Đó **không phải lỗi**. Polylang for WooCommerce tiếp quản toàn bộ nhóm WooCommerce và bật
dịch cho chúng mặc định, nên chúng bị gỡ khỏi danh sách tuỳ chọn — không còn là thứ để chọn.

→ **Không có gì để tick ở đây.** Việc duy nhất cần làm là **phép đo ở mục 1.1**: mở
`Products → Attributes → Color → Configure terms` xem có cột ngôn ngữ không.

---

## 5. Shipping zone — bước D, làm trước khi có SKU test

📄 Quy trình bấm-từng-bước: **`deliverables/woo/SHIPPING-SETUP.md`**

Tóm tắt cái phải đứng:

| Zone | Method |
|---|---|
| **Việt Nam** | **Free shipping** (Requires = *N/A*) đặt **TRÊN** → **Flat rate `30000`** |
| **United States** | Flat rate — con số cần bạn chốt, đề xuất `200000` |

🔴 Thứ tự hai method trong zone VN là thật, không phải thẩm mỹ. Đơn từ 3 áo hiện cả hai và
Woo chọn sẵn cái đứng đầu. Flat rate đứng trên = khách không để ý trả 30.000₫ cho đơn lẽ ra
miễn phí.

⚠️ Ô **"Minimum order amount"** của Woo **vô tác dụng** ở đây — chính sách tính theo *số lượng*
(3 áo), không theo tiền. Luật thật ở `inc/woocommerce.php` mục 7, `VT_FREE_SHIP_MIN_QTY = 3`.
Theme có admin notice nhắc ngay trên màn hình Shipping.

---

## 6. Sản phẩm phải là **Variable**, không phải Simple

Shopee tách mỗi màu một listing:
```
Áo Thun VITALITÉ PINK GRAFFITI Unisex - ĐEN     276.100₫
Áo Thun VITALITÉ PINK GRAFFITI Unisex - TRẮNG   282.680₫
```

Trên site gộp thành **một Variable Product**:

```
Product:  VITALITÉ Pink Graffiti T-Shirt
  ├─ pa_color: Black, White        ✅ used for variations
  ├─ pa_size:  S, M, L             ✅ used for variations
  ├─ pa_fabric:     250 GSM Cotton         (spec, không tick)
  ├─ pa_fit:        Unisex Regular         (spec, không tick)
  ├─ pa_collection: Pink Graffiti          (spec, không tick)
  └─ 6 variation · mỗi cái có giá + tồn kho + SKU riêng
```

Giá khác nhau giữa màu là bình thường — set ở **cấp variation**.

**Nguyên tắc tách:** cùng thân áo, khác màu → **variation**. Khác đồ hoạ → **product riêng**.
→ `THE MOMENTS BOXY HOODIE` Pure White + Grey = một product, hai variation màu.
→ `The Iconic` và `Pink Graffiti` = hai product riêng.

### 6.1 — 🔴 "Used for variations" nằm ở ĐÂY, không nằm ở màn hình Attributes

```
Products → Add new product
  → khối "Product data"
  → đổi dropdown "Simple product" thành "Variable product"      ← BƯỚC BỊ QUÊN NHIỀU NHẤT
  → tab "Attributes" → "Add existing" → chọn Size
  → lúc này checkbox "Used for variations" mới hiện ra
  → tick cho Size và Color · KHÔNG tick cho Fabric / Fit / Collection / Print
  → Save attributes → sang tab "Variations" → "Generate variations"
```

Chưa đổi sang **Variable product** thì checkbox đó **không bao giờ xuất hiện**, và tab
Variations cũng không có. Không phải thiếu plugin, không phải lỗi theme.

### Bốn việc bắt buộc ở mỗi sản phẩm

1. **Ảnh:** `Product image` = **MẶT TRƯỚC** của màu chủ đạo · ảnh **đầu tiên** trong
   gallery = **MẶT SAU của cùng màu đó**. `vt_product_back_image()` đọc gallery ở **cấp
   sản phẩm**, nên một sản phẩm chỉ có **một cặp** trước/sau cho hover — phải chọn màu
   chủ đạo. Có meta box nhắc ngay trong màn hình sửa sản phẩm.
2. **Ảnh riêng theo variation màu.** Chọn Black → ảnh chính đổi sang mockup áo đen.
   🔴 Woo cho variation **đúng một ảnh**, không có gallery theo màu — nên đổi màu **không**
   đổi được mặt sau. Chi tiết: `NHAP-SAN-PHAM.md` mục 3.6.
3. **SKU riêng từng variation.** Khuôn: `VTL-PG-BLK-M`. Cần cho tồn kho và đối soát Shopee.
4. 🔴 **Cân nặng — điền cho MỌI variation ngay lúc nhập.** Miễn phí lúc này. Đây là thứ duy
   nhất chặn đường sang tính phí ship theo API sau này, và điền bù cho 40 SKU là mở lại từng cái.

Quản lý tồn kho ở **cấp variation**, không phải cấp product.

---

## 7. Hai sản phẩm test — không được bỏ bước này

Nhập **1 áo thun + 1 hoodie**, rồi kiểm đủ 8 mục:

- [ ] Thẻ sản phẩm ở `/en/shop` hiện chấm màu đúng (không phải xám) và list size S·M·L
- [ ] Hover thẻ đổi mặt trước ↔ mặt sau
- [ ] PDP: chọn màu → ảnh đổi theo
- [ ] PDP áo thun: **bảng size tự hiện**. PDP hoodie: **không hiện** (chưa có số đo — đúng là không hiện)
- [ ] Tab *Details* hiện đủ Fabric / Fit / Collection / Print
- [ ] Thêm giỏ → checkout: zone VN ra 30.000₫; đủ **3 áo** → ra **Free shipping** và nó đứng sẵn
- [ ] Đổi địa chỉ sang US → zone Mỹ ra giá, **không** ra free shipping
- [ ] Mở `/vi/shop` — filter Premmerce còn chạy không, chấm màu còn đúng không

Hai thứ đang treo, kiểm luôn ở lượt này:
- **Premmerce Product Filter có tương thích Polylang không** (vỡ ở 2 SKU dễ sửa hơn ở 40)
- **Kho bên Mỹ là kho thứ hai** — hàng xách tay theo lô, người bên Mỹ giữ và phân phối nội
  địa Mỹ. Woo đang **một kho**, chưa có cơ chế nào mô tả việc này. Phải quyết ở đây

Vỡ chỗ nào sửa chỗ đó, **rồi mới** nhập phần còn lại.

---

## 8. Premmerce Filter — map lại sau khi có attribute

| Attribute | Lên filter? | Kiểu |
|---|---|---|
| `pa_size` | ✅ | button |
| `pa_color` | ✅ | swatch màu |
| `pa_collection` | ✅ | checkbox |
| `pa_fabric` | ⬜ tuỳ | checkbox |
| `pa_fit` · `pa_print` | ❌ | chỉ hiển thị ở PDP |

---

## 9. Dữ liệu CHƯA CÓ — cần trước khi nhập hàng loạt

Không chặn mục 1–5. Chặn mục 7 trở đi.


- [ ] 🔴 **Giá site từng SKU** — bán bằng giá Shopee, hay bằng giá gốc chưa giảm? Chưa quyết
      thì không nhập được cái nào
- [ ] 🔴 **Ảnh mặt trước + mặt sau** cho từng màu. Không có ảnh mặt sau thì hover không có gì để đổi
- [ ] Cân nặng thực tế mỗi áo (kg) — cân một cái là ra, dùng chung cả dòng
- [ ] Số đo + chất liệu `THE MOMENTS BOXY HOODIE` *(chưa có → PDP hoodie không hiện bảng size,
      đã xử lý bằng cách không nói — xem `docs/CHO-DIEN-SAU.md`)*
- [ ] Spec `OLD MONEY` varsity longsleeve và dòng quần
- [ ] 3/10 SKU Shopee chưa liệt kê được

---

## 10. Multi-currency — chưa làm, và đây là lý do

Premmerce Multi-Currency đang **inactive**, user chốt 01/09 giữ lại phòng sau.

Vấn đề thật không nằm ở hiển thị giá mà ở **quyết toán**:

| Cổng | Quyết toán được |
|---|---|
| MoMo · VNPay | **chỉ VND** |
| PayPal | USD, EUR… |
| Stripe | **không hỗ trợ merchant VN trực tiếp** |

Plugin multi-currency đổi được **con số hiển thị**, không tạo ra được **khả năng thu tiền**.
Và brand xác nhận 29/08 *"tạm thời chưa làm tài khoản kinh doanh"* → **chưa cổng nào duyệt được.**

→ **Không bật multi-currency cho tới khi có ít nhất một cổng thu được USD.** Bật trước là
hiển thị `$11.20` rồi bắt khách Mỹ trả VND qua một cổng chưa tồn tại.

🔴 Trang `payment` đang nói *"phương thức hiện ở checkout"*. Tới launch mà khách Mỹ mở
checkout không thấy gì bấm thì câu đó thành lời hứa suông. **Đây là rủi ro đã ghi nhận
trong `CLAUDE.md` mục 7, không phải việc bị bỏ quên.**
