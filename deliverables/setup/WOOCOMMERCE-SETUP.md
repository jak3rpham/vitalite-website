# WOOCOMMERCE — NHẬP SẢN PHẨM & CẤU HÌNH TÀI KHOẢN

> **Phạm vi.** File này nói về **từng sản phẩm** và **tài khoản khách**.
> Cấu hình TOÀN CỤC (tạo attribute, tiền tệ, cỡ ảnh, trang Shop) nằm ở
> `WORDPRESS-SETUP.md` mục 6–8. **Đừng chép lại sang đây**, hai bản sẽ trôi khỏi nhau.
>
> Thứ tự bắt buộc, đã chốt ở `CLAUDE.md` mục 6:
> **Polylang (bước 6) → attributes → nhập 2 SẢN PHẨM TEST (bước 8) → nhập phần còn lại.**
> Attribute term là taxonomy term. Tạo trước khi bật Polylang là phải gán ngôn ngữ
> tay cho từng term và từng SKU.

---

## 1. Bấm màu thì hiện ảnh của màu đó — làm thế nào

Đây là câu hỏi chính. Trả lời ngắn: **sản phẩm phải là Variable product, và mỗi
biến thể phải được gắn ảnh riêng.**

### 1.1 Dựng sản phẩm

`Sản phẩm → Thêm mới`

1. Khung **Product data** → chọn **Variable product** (không phải Simple).
2. Tab **Attributes** → `Add existing` → chọn `Color`.
   - Value(s): chọn đúng những màu sản phẩm này có
   - ✅ **Used for variations** ← **không tick là mọi thứ dưới đây vô nghĩa**
   - ✅ Visible on the product page
3. Làm y hệt với `Size`.
4. Tab **Variations** → `Generate variations`.
   Có 2 màu × 3 size thì ra **6 biến thể**.
5. Mở từng biến thể ra, điền:

| Ô | Điền gì |
|---|---|
| **Image** | 🔴 **Ảnh của ĐÚNG màu đó.** Đây là ô làm nên toàn bộ hiệu ứng đổi ảnh. Bỏ trống là biến thể đó dùng ảnh chung, bấm màu không thấy gì đổi |
| Regular price | Giá gốc |
| Sale price | Để trống nếu không giảm |
| SKU | Mã riêng từng biến thể |
| Stock | Bật `Manage stock` để hết size nào tự khoá size đó |

> **Ảnh giống nhau giữa các size.** Grey/S, Grey/M, Grey/L đều gắn CÙNG một ảnh grey.
> Ảnh phân biệt theo **màu**, không theo size.

### 1.2 🔴 Giới hạn của WooCommerce lõi — đọc kỹ, đây là chỗ dễ vỡ kỳ vọng

WooCommerce chỉ đổi ảnh khi khách chọn **ĐỦ MỌI thuộc tính biến thể**.
Có cả Color và Size thì bấm mỗi màu **chưa đủ** — Woo chưa xác định được biến thể
nào, nên ảnh **đứng yên** cho tới khi khách chọn nốt size.

Và Woo chỉ đổi **ẢNH CHÍNH**, không đổi cả bộ gallery.

Ba đường đi, chọn một:

| Cách | Được gì | Mất gì |
|---|---|---|
| **A. Để nguyên Woo lõi** | 0 công, 0 plugin | Bấm màu chưa thấy đổi ảnh cho tới khi chọn size. **Đúng cái bạn không muốn** |
| **B. Plugin** (Premmerce Variation Swatches, Additional Variation Images) | Có ngay, có cả gallery theo màu | Thêm JS/CSS mỗi lượt tải trang; Premmerce **chưa test với Polylang** — đang là một mục treo trong `CLAUDE.md` mục 7 |
| **C. ~30 dòng JS trong theme** ⭐ | Bấm màu là đổi ảnh ngay, không chờ size. Không plugin, không thêm request | Phải viết và tự bảo trì |

**Đề xuất: C.** Bản mẫu đã dựng sẵn và chạy được ở `deliverables/woo-templates/pdp.html`.
Chuyển sang PHP chỉ là thay dữ liệu cứng bằng vòng lặp biến thể.

**Cách dải ảnh hoạt động — đọc kỹ, đây là quyết định về hành vi mua hàng:**

> Dải thumbnail **luôn hiện đủ ảnh của MỌI màu**. Không lọc, không giấu.
>
> Bản đầu tôi làm kiểu lọc — bấm màu thì giấu ảnh các màu khác đi. Nghe gọn
> nhưng nó giấu mất chính thứ đang bán: khách không biết sản phẩm còn màu nào
> nếu không lần lượt bấm từng ô màu. Với hàng thời trang, **cuộn qua cả bộ ảnh
> LÀ hành vi mua hàng** — đó là lúc khách quyết.
>
> Nên ô màu chỉ là **phím tắt nhảy tới** ảnh đầu tiên của màu đó. Bấm
> `Pure White` vẫn thấy áo trắng ngay — không mất gì — mà vẫn cuộn tiếp sang
> màu khác được.
>
> **Đồng bộ hai chiều:** chọn thumbnail của màu khác thì ô màu tự đổi theo.
> Đang xem ảnh áo trắng mà ô màu vẫn đứng ở `Grey` là trang tự mâu thuẫn, và
> đúng chỗ đó khách bấm Add to cart.
>
> Ảnh đầu của mỗi màu mang `data-first-of-colour`; CSS vẽ một vạch mảnh để mắt
> tách được nhóm màu, không cần thêm chữ.

⚠️ **Dải này dài theo số màu.** 2 màu × 2 ảnh = 4 thumbnail, vừa đẹp.
4 màu × 3 ảnh = **12 thumbnail**, rail dọc sẽ cao hơn cả ảnh chính.
Tới lúc đó phải quyết một trong hai: cho rail tự cuộn dọc, hay quay lại lọc theo
màu. **Kiểm ngay ở sản phẩm nhiều màu nhất** khi nhập 2 sản phẩm test.

⚠️ Chọn C thì **không được** bật thêm plugin swatch. Hai bên cùng đổi `src` của
ảnh chính là đánh nhau.

### 1.3 Swatch hiển thị đúng màu

Ô màu tròn ở lưới sản phẩm do `vt_product_color_swatches()` vẽ
(`inc/helpers.php`). Nó dò **tên term** trong một bảng cứng:

| Tên term (viết đúng thế này) | Mã màu |
|---|---|
| `Black` | `#0A0A0A` |
| `White` / `Pure White` | `#FFFFFF` |
| `Grey` / `Gray` | `#B8B8BC` |
| `Cream` | `#EFE7D2` |

> Đặt tên term khác bảng trên — ví dụ `Off White`, `Xám` — thì **không lỗi**,
> nhưng ô màu ra **xám mặc định `#DDDDE1`**, sai màu thật.
> Thêm màu mới thì thêm vào bảng `$map` trong `vt_product_color_swatches()`.

---

## 2. Ảnh sản phẩm — quy ước BẮT BUỘC

Hiệu ứng rê chuột đổi mặt trước ↔ mặt sau ở lưới sản phẩm phụ thuộc **hoàn toàn**
vào quy ước này. Nhập sai là hỏng, không có thông báo lỗi nào.

| Ô trong wp-admin | Phải là ảnh gì |
|---|---|
| **Product image** | **MẶT TRƯỚC** của áo |
| **Product gallery**, ảnh **đầu tiên** | **MẶT SAU** của áo |
| Product gallery, ảnh còn lại | Chi tiết, ảnh model |
| **Variation → Image** | Mặt trước của **đúng màu** biến thể đó |

> Theme đã cài sẵn một hộp nhắc ngay trong màn hình sửa sản phẩm
> (`inc/woocommerce.php`, mục 7) để người nhập hàng không phải nhớ.

**Cỡ ảnh:** mockup hiện có là `1000×1000`. Theme **tắt zoom** vì zoom ảnh 1000px
chỉ phóng to điểm ảnh. Có ảnh ≥1600px thì bật lại trong `inc/setup.php`.

---

## 3. Thuộc tính spec — KHÔNG tick "Used for variations"

`Fabric` · `Fit` · `Collection` · `Print` đổ vào tab **Details** của trang sản phẩm.

🔴 Tick nhầm "Used for variations" cho chúng là **nổ số biến thể theo cấp số nhân**:
3 size × 2 màu = 6 biến thể thật; thêm fabric và fit vào thành **24**, mỗi cái phải
điền giá và tồn kho tay.

Danh sách term đầy đủ: `WORDPRESS-SETUP.md` mục 6.

---

## 4. Bảng size

Theme tự chèn bảng số đo vào trang sản phẩm, **chỉ cho hàng thuộc danh mục áo thun**
(`t-shirts`, `tshirts`, hoặc `ao-thun`). Số đo lấy từ Shopee, xác minh 2026-08-19:

| Size | Dài | Rộng |
|---|---|---|
| S | 70 | 55 |
| M | 73 | 58 |
| L | 76 | 61 |

🔴 **Hoodie CHƯA có số đo riêng** và theme **cố tình không hiện bảng** cho nó —
thà không có còn hơn hiện số sai. Đây là vùng rủi ro trả hàng, không được tự nghĩ số.
Có số thật thì sửa `vt_size_table_tshirt()` trong `inc/woocommerce.php`.

---

## 5. Tài khoản khách

`WooCommerce → Cài đặt → Tài khoản & Quyền riêng tư`

| Mục | Đặt | Vì sao |
|---|---|---|
| Cho phép khách đặt hàng không cần tài khoản | ✅ **BẬT** | Bắt tạo tài khoản trước khi mua là một trong những thứ giết đơn hàng mạnh nhất. Bản mẫu cũng đang ghi đúng câu này cho khách đọc |
| Cho phép tạo tài khoản khi thanh toán | ✅ Bật | Tạo tài khoản ngay lúc đã quyết mua, không cản đường |
| Cho phép tạo tài khoản ở trang "Tài khoản" | ✅ Bật | Header có link Account trỏ tới đây |
| Tự sinh tên đăng nhập từ email | ✅ Bật | |
| Tự sinh mật khẩu | ❌ **Tắt** | Để khách tự đặt. Mật khẩu tự sinh gửi qua mail hay rơi vào spam |
| Xoá dữ liệu cá nhân khi có yêu cầu | ✅ Bật | |

**Trang cần có:** `WooCommerce → Cài đặt → Nâng cao` phải trỏ đúng
`Cart` → `/cart`, `Checkout` → `/checkout`, `My account` → `/my-account`.
Theme lấy link Account bằng `vt_account_url()`, hàm này đọc thẳng cấu hình đó —
đặt sai trang thì icon tài khoản trên header dẫn đi sai chỗ.

🔴 **Mail giao dịch.** Shared hosting gửi mail bằng `mail()` của PHP thường bị
Gmail đẩy vào spam. Khách tạo tài khoản mà không nhận được mail là mất luôn.
Cần một SMTP thật (FluentSMTP + Brevo/SendGrid, cả hai đều có bậc miễn phí).
Đây là **việc phải làm trước khi bật đăng ký**, không phải việc tối ưu sau.

---

## 6. 🟡 Thông báo khuyến mãi — CHƯA làm được, và đây là lý do

Bạn muốn: khách để lại thông tin, có promotion thì báo.

`CLAUDE.md` đang cấm dựng form này, và cấm đúng:
> *"Không có form newsletter cho tới khi nối provider thật.
> Form nhận email rồi vứt đi là lừa khách."*

Ô nhập email không nối vào đâu thì khách tưởng đã đăng ký, tới đợt drop không ai
báo. Tệ hơn là không có ô nào.

**Cần quyết ba việc trước khi dựng:**

1. **Gửi bằng gì.** Woo lõi **không** có công cụ gửi chiến dịch — nó chỉ gửi mail
   đơn hàng. Cần một dịch vụ:

   | | Miễn phí tới | Ghi chú |
   |---|---|---|
   | **Klaviyo** ⭐ | 250 liên hệ / 500 mail tháng | Chuẩn ngành thời trang, có sẵn tích hợp Woo |
   | Brevo | 300 mail/ngày | Rẻ nhất khi lên số lượng, có SMS |
   | Mailchimp | 500 liên hệ | Plugin Woo hay hỏng khi Woo lên phiên bản mới |

2. **Xin đồng ý thế nào.** Khách quốc tế là lý do tồn tại của site này (`CLAUDE.md`
   mục 2), nên **GDPR áp dụng**: ô tick phải **để trống sẵn**, và câu chữ phải nói
   rõ đăng ký nhận cái gì. Tick sẵn hộ khách là vi phạm.

3. **Đặt ở đâu.** Đề xuất hai chỗ, không hơn:
   - ô tick ở **checkout** — khách đã tin đủ để trả tiền, đây là chỗ đồng ý cao nhất
   - một khối ở **footer** — nhưng chỉ dựng sau khi đã có provider ở mục 1

**Làm được ngay hôm nay mà không cần provider:** thêm một ô tick ở checkout, lưu
vào order meta. Không gửi gì cả, chỉ **thu thập sự đồng ý** để sau này có provider
thì nhập vào. Trung thực, vì câu chữ chỉ hứa "sẽ nhận email", không hứa tần suất.
Cần thì bảo, tôi viết đoạn hook đó — khoảng 20 dòng, không cần plugin.

---

## 7. Nhập 2 sản phẩm test trước — KHÔNG được bỏ

`CLAUDE.md` mục 6 ghi rõ, nhắc lại vì đây là chỗ tốn thời gian nhất nếu bỏ qua:

> Sửa cấu trúc lúc có 2 sản phẩm là **10 phút**.
> Lúc có 40 sản phẩm × 6 biến thể là **làm lại từ đầu**.

Nhập xong 2 sản phẩm, kiểm đủ 8 mục sau rồi mới nhập tiếp:

- [ ] Lưới shop: rê chuột đổi mặt trước ↔ mặt sau
- [ ] Ô màu ở thẻ sản phẩm ra **đúng màu**, không phải xám mặc định
- [ ] Bấm ô màu ở trang sản phẩm → ảnh chính nhảy tới màu đó (xem mục 1.2 đã chọn cách nào)
- [ ] Dải thumbnail hiện **đủ ảnh mọi màu**, và bấm ảnh màu khác thì ô màu tự đổi theo
- [ ] Sản phẩm **nhiều màu nhất** — đếm xem dải thumbnail có dài quá không (mục 1.2)
- [ ] Chọn size hết hàng → nút thêm giỏ khoá lại
- [ ] Giá hiện `599.100 ₫` — **không có** `,00` ở đuôi
- [ ] Bảng size hiện ở áo thun, **không** hiện ở hoodie
- [ ] Tab **Details** có đủ Fabric / Fit / Collection / Print
- [ ] Thêm vào giỏ → số trên icon giỏ đổi **mà không tải lại trang**

Mục cuối kiểm luôn `woocommerce_add_to_cart_fragments` trong `inc/woocommerce.php`
có chạy không — nếu số không đổi thì hook đó hỏng, đừng nhập tiếp.
