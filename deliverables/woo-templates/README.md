# WOO TEMPLATES — thiết kế bố cục 7 màn thương mại

**Tạo:** 2026-08-24 · **Trạng thái:** prototype HTML, đã duyệt bằng số, **chưa lên theme**

---

## 0. Đọc trước: hai loại deliverable trong thư mục này, đừng nhầm

| | Màn | Cách đưa lên site | Rủi ro |
|---|---|---|---|
| `pdp.html` | Trang sản phẩm | **Đè template** → `woocommerce/single-product.php` | Trung bình |
| `cart-checkout-account.html` | Giỏ (có hàng) · Giỏ rỗng · Thanh toán · **Thank you** · **Đăng nhập** · Tài khoản | **CHỈ CSS.** Không đè template nào | Cao nếu làm sai |

Lý do tách: `CLAUDE.md` §3 ghi *"Cart & checkout: KHÔNG customize trước khi flow mặc định
chạy đúng. Sửa checkout là thay đổi rủi ro cao nhất trong stack."*
Site **chưa deploy lần nào**, nên chưa ai biết flow mặc định có chạy không.

Nên với ba màn giỏ/thanh toán/tài khoản, thứ duy nhất sẽ đi lên theme là **một khối CSS**,
và chỉ sau khi đã đặt thử một đơn thật trên staging. Không đụng field, không đụng validate,
không đổi thứ tự bước, không thêm bớt input nào.

⛔ **Không file nào trong thư mục này được dán vào Elementor.** Cả bốn màn đều do WooCommerce
render động. Dán tĩnh là hỏng ngay ở sản phẩm thứ hai.

---

## 0b. 🔴 Mở bằng LINK, đừng mở thẳng file

Hai file `pdp.html` và `cart-checkout-account.html` là **fragment**, không có `<meta charset>`
vì chúng sẽ được dán vào trang khác. Mở thẳng bằng trình duyệt thì:

- trình duyệt đoán bảng mã là `windows-1252` → **toàn bộ tiếng Việt hiện ra thành rác**

Nền thì đã sửa rồi: mỗi fragment giờ tự sơn `background` và đặt `color-scheme:light`, nên không
còn cảnh nền đen chữ đen khi máy đang bật dark mode. Nhưng bảng mã thì fragment không tự sửa được.

**Dùng hai file `_preview-*.html`** ở mục 1. Chúng có `<meta charset="utf-8">`.
Trên WordPress không có vấn đề này, WP luôn gửi UTF-8.

---

## 1. Xem thử

```
cd "E:\Vitalite website"; python -m http.server 8793
```

- PDP: `http://127.0.0.1:8793/deliverables/woo-templates/_preview-pdp.html`
- Sáu màn còn lại: `http://127.0.0.1:8793/deliverables/woo-templates/_preview-shop.html`

⚠️ **Phải chạy server từ GỐC PROJECT**, không phải từ `deliverables/`.
Ảnh mockup nằm ở `mockup-all/`, ngoài thư mục `deliverables/`, nên chạy sai chỗ là ảnh 404 hết.

Hai file `_preview-*.html` chỉ để xem. Nội dung thật nằm ở hai file kia.

---

## 2. PDP — cái đáng chú ý

### Gallery hai tầng, tự đổi theo số ảnh thật

Không phải sửa template khi sản phẩm có ít ảnh hay nhiều ảnh:

| Số ảnh | Bố cục |
|---|---|
| 1 | một khung lớn, không có gì trông thiếu |
| 2-3 | xếp dọc một cột |
| 4+ | lưới 2 cột, ảnh đầu chiếm cả hàng |
| màn ≤900px | luôn là dải cuộn ngang có scroll-snap, không JS |

Chạy được ngay hôm nay với mockup 1000px, tự tốt lên khi có ảnh chụp thật.
Dùng `:has()`; trình duyệt không hỗ trợ thì rơi về một cột, vẫn đọc được, không vỡ.

### Ảnh: theo đúng quyết định đã chốt, kèm một đánh đổi

`MOCKUP-PIPELINE.md` §2 đã chốt: lưới sản phẩm và PDP để **nền trắng, dùng mockup nguyên bản**.
Wordmark `vitalité®` và cụm blob là một phần khung Canva; cắt ra thì nửa catalog cắt được nửa không,
lưới mất đồng nhất.

🟡 **Đánh đổi phải biết:** wordmark đó lặp lại 4-6 lần trên một PDP nhiều ảnh. Bố cục hiện tại
giảm bằng cách cho ảnh đầu to hẳn, ảnh sau nhỏ lại, để wordmark đọc như motif khung chứ không
phải nhãn lặp. Có ảnh chụp thật thì vấn đề tự hết.

⛔ **Không bật zoom.** Mockup chỉ 1000×1000, Woo zoom cần ≥1600px.

### LCP

Ảnh đầu gallery là phần tử LCP của trang: `fetchpriority="high"`, **không** `loading="lazy"`,
có `width`/`height` thật để trình duyệt chừa chỗ. Ba ảnh còn lại `lazy`.

### Thanh mua dính đáy màn, chỉ mobile

Trên màn hẹp, cuộn qua khỏi summary là mất luôn nút mua. Đó là chỗ rơi đơn hàng rõ nhất
trên PDP di động.

### Hai ô cam trên PDP

- **Size guide** cho hoodie: chưa có số đo. Câu **22** trong `CAU-HOI-CHO-BRAND.md`.
- **Shipping & returns**: chưa có phí và thời gian. Câu **5-16** và **23-28**.

**Không publish PDP hoodie khi hai ô này còn.**

---

## 3. Cart / Checkout / Account — cái đáng chú ý

### Markup chép đúng WooCommerce

Tên class trong prototype là tên thật của Woo: `.shop_table.cart`, `.cart_item`,
`.product-thumbnail`, `.woocommerce-billing-fields`, `#order_review`, `.wc_payment_methods`,
`.woocommerce-MyAccount-navigation`. Để CSS viết ở đây rơi thẳng vào bản thật.

Tám field billing là **bộ mặc định của Woo**, đúng `name` và `id`. Không bớt, không đổi thứ tự.

### 🔴 Giỏ hàng trên mobile: đã sửa một lỗi thật

Bảng giỏ 6 cột đo ở 550px cho ra **cột tên sản phẩm rộng 80px**. Không đọc được, và ở 375px
còn tệ hơn. Đây là màn mọi khách đều đi qua trước khi trả tiền.

Đã xếp lại thành **thẻ dọc** dưới 760px: ảnh 88px neo trái, tên 231px, tổng tiền neo phải,
cột đơn giá ẩn đi vì trùng với tổng khi số lượng bằng 1.

Làm được **mà không đè template**, vì Woo đã tự in `data-title` lên từng ô.

### Hai ô cam

- **Giỏ hàng**: chưa có phí ship. Chưa cấu hình shipping zone thì Woo báo *"No shipping options"*
  ở checkout và **khách không đặt được đơn nào**.
- **Thanh toán**: hai phương thức đang hiện là **mặc định của Woo**, không phải lựa chọn đã chốt.
  Khách quốc tế không chuyển khoản nội địa được và cũng không COD được, nên nếu chỉ có hai cái
  này thì site không bán được cho đúng tệp khách nó sinh ra để phục vụ. Câu **17-20**.

---

## 3b. Ba màn thêm ngày 24/08

### Giỏ hàng rỗng
Ai cũng gặp, kể cả khách bấm nhầm icon giỏ. Phải có **lối ra**, không được là ngõ cụt.
Hai nút: `Shop all` và `Browse collections`.

### Order received, màn sau khi trả tiền
Đây là màn duy nhất chắc chắn được đọc kỹ. Nó phải trả lời **ba câu**: đơn số mấy, trả bao nhiêu,
**bao giờ hàng tới**.

🔴 Câu thứ ba hiện **chưa trả lời được**, cần thời gian giao (câu **14** và **16**).
Không có nó thì khách vừa trả tiền xong lại phải đi hỏi, và đó thành tin nhắn đầu tiên của
mọi đơn hàng. Đã để ô cam ngay tại chỗ.

### Login / Register
Header đã có icon tài khoản trỏ tới đây (`vt_account_url()`), nên chắc chắn có người vào.
Ghi rõ **không cần tài khoản vẫn đặt được hàng**, để ô đăng ký không thành rào cản.

---

## 3c. 🔴 Một lỗi gán ảnh đã sửa

Bản đầu của PDP dùng mockup **17** và **18** làm ảnh chi tiết của hoodie. Sai sản phẩm.
Theo `reference/BRAND_ASSETS_AUDIT.md`:

| Mockup | Là gì |
|---|---|
| 13-16 | `THE MOMENTS BOXY HOODIE`, xám và trắng ← đúng sản phẩm này |
| 17 | `OLD MONEY` varsity longsleeve, **chưa ra mắt** |
| 18 | tech pack **quần**, chưa sản xuất |

Đã đổi sang 13-16. **Đọc bảng mockup trong `BRAND_ASSETS_AUDIT.md` trước khi gán ảnh cho SKU.**
Gán nhầm là khách nhận về thứ khác với thứ đã xem.

---

## 4. Việc tiếp theo, theo đúng thứ tự

1. **Duyệt bố cục** hai file prototype. Đây là gate review thứ nhất theo `CLAUDE.md` §3.
2. Chuyển `pdp.html` → `woocommerce/single-product.php`. Mọi dữ liệu thay bằng hàm Woo,
   template phải **loop-safe**. Gate review thứ hai.
3. **Deploy, rồi đặt thử một đơn thật** bằng giao diện mặc định của Woo.
4. Chỉ sau bước 3 mới viết CSS cho cart/checkout/account vào theme.

🔴 **Bước 4 chưa làm được bây giờ, và cố tình chưa làm.** CSS trong prototype đang bọc trong
`.vwc` và dựa vào mấy div khung của riêng prototype (`.vwc-wrap`, `.vwc-cart-grid`…) mà Woo
không sinh ra. Viết sẵn một file CSS "dán vào là chạy" lúc này là đoán DOM thật của Woo trên
hosting này. Phải có DOM thật rồi mới viết, nếu không thì viết xong vẫn phải sửa lại.

---

## 5. Đã kiểm được gì

Đo trên trình duyệt, không phải nhìn bằng mắt:

| | Desktop 1280 | Mobile 375 |
|---|---|---|
| PDP gallery | 2 cột, ảnh đầu span 622px | flex + scroll-snap, 323px mỗi ảnh |
| PDP summary | `sticky` | `static` + thanh mua dính đáy |
| Cart | 640 + 360, tổng tiền `sticky` | thẻ dọc, tên 231px |
| Checkout | 522 + 472, order review `sticky` | một cột |
| Account | 220 + 780 | một cột |
| Tràn ngang | không | không |

Cả hai file cân tag, 0 dấu gạch dài, ảnh trả 200.

**Chưa kiểm được:** nhìn bằng mắt. Tab của Claude chạy nền nên không chụp được màn hình ổn định.
Mở hai link preview ở mục 1 mà liếc qua trước khi duyệt.
