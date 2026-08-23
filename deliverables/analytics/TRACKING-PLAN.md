# TRACKING & REPORT
**Ngày:** 2026-08-20 · Solo operator · shared hosting

---

## 0. Nguyên tắc

Đo ít mà đúng, hơn đo nhiều mà không ai đọc.

Với một người vận hành, mỗi chỉ số theo dõi là một khoản nợ chú ý.
Kế hoạch này chỉ đo những gì **dẫn tới một hành động cụ thể**. Số nào không đổi được
quyết định nào thì không đo.

Và một điều kiện nữa: **mỗi script analytics là một khoản chi phí LCP thật.**
GA4 ~45KB. Nhồi thêm Hotjar, Clarity, Meta Pixel, TikTok Pixel là đủ giết mục tiêu
LCP < 2.5s trên shared hosting.

---

## 1. Cài gì

| Công cụ | Có? | Vì sao |
|---|---|---|
| **GA4** | ✅ bắt buộc | miễn phí, có ecommerce, nối được Search Console |
| **Google Search Console** | ✅ bắt buộc | nguồn duy nhất cho dữ liệu organic thật |
| **Google Tag Manager** | ⚠️ **KHÔNG** ở giai đoạn này | thêm một lớp trừu tượng + ~90KB. Với 3–4 event thì gắn thẳng GA4 đơn giản hơn. Cài GTM khi cần chạy quảng cáo nhiều nền tảng |
| **Meta Pixel** | ⏸ khi bắt đầu chạy ads | không chạy ads thì nó chỉ là 70KB gửi dữ liệu khách cho Meta |
| **TikTok Pixel** | ⏸ khi bắt đầu chạy ads | brand có TikTok Shop — nhưng đó là kênh riêng |
| **Hotjar / Clarity** | ⏸ sau khi có traffic | ghi hình phiên chỉ hữu ích khi có đủ phiên để xem. Clarity miễn phí và nhẹ hơn Hotjar |

**Bắt đầu bằng đúng GA4 + Search Console.** Hai cái đó trả lời được 90% câu hỏi
của ba tháng đầu.

---

## 2. Cài GA4

### Bước 1 — tạo property
`analytics.google.com` → Admin → Create Property
- Múi giờ: **(GMT+07:00) Ho Chi Minh**
- Tiền tệ: **VND**
- Data stream: Web → `https://vitalite.io.vn`

### Bước 2 — bật Enhanced Measurement
Tự đo mà không cần code: page view, scroll, outbound click, site search, file download.

⚠️ **Site search:** GA4 dò tham số `q, s, search, query, keyword`.
Site dùng `?s=` → đã khớp mặc định. Không phải cấu hình gì.

### Bước 3 — gắn mã

**Không cài plugin cho việc này.** Một plugin nữa cho một đoạn script là không đáng.
Thêm vào `inc/enqueue.php`:

```php
/**
 * GA4. Gắn ở footer, không chặn render.
 * Không đo admin — dữ liệu của mình làm nhiễu dữ liệu khách.
 */
add_action('wp_footer', function () {
    if (current_user_can('edit_posts')) return;   // bỏ qua người đang đăng nhập quản trị
    $id = 'G-XXXXXXXXXX';                          // [NEED] Measurement ID thật
    if ($id === 'G-XXXXXXXXXX') return;            // chưa điền thì không in gì
    ?>
    <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr($id); ?>"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '<?php echo esc_js($id); ?>');
    </script>
    <?php
}, 20);
```

> `if (current_user_can('edit_posts')) return;` — quan trọng hơn vẻ ngoài của nó.
> Trong tháng đầu, user sẽ tự vào site vài chục lần mỗi ngày. Không lọc thì
> dữ liệu ba tháng đầu vô nghĩa.

---

## 3. Ecommerce event

GA4 có bộ event ecommerce chuẩn. **WooCommerce không tự gửi** — phải gắn.

### Cách rẻ nhất: dùng plugin cho phần ecommerce

Đây là chỗ **nên** dùng plugin, vì tự viết đúng bộ event ecommerce là việc dễ sai
và khó kiểm chứng.

| Plugin | Ghi chú |
|---|---|
| **GTM4WP** ⭐ | miễn phí, gửi đúng chuẩn GA4, dùng được cả khi không có GTM |
| Woo Google Analytics của WooCommerce | chính chủ, đơn giản hơn, ít event hơn |

**Khuyến nghị: GTM4WP**, bật chế độ gửi thẳng GA4 (không cần GTM container).

### Bốn event thật sự cần đọc

| Event | Trả lời câu hỏi |
|---|---|
| `view_item` | sản phẩm nào được xem nhiều nhất? |
| `add_to_cart` | sản phẩm nào được thêm giỏ? **Tỉ lệ view→cart là chỉ số PDP quan trọng nhất** |
| `begin_checkout` | bao nhiêu người từ giỏ đi tới thanh toán? |
| `purchase` | doanh thu thật |

Bốn event đó cho ra một cái phễu, và phễu chỉ ra chỗ vỡ:

```
view_item  →  add_to_cart  →  begin_checkout  →  purchase
            ↑ PDP yếu?      ↑ giỏ hàng vỡ?    ↑ CHECKOUT VỠ
```

**Rơi mạnh nhất ở đâu thì sửa chỗ đó trước.** Đừng tối ưu trang chủ khi
người ta rụng ở checkout.

---

## 4. Ba event tuỳ chỉnh — đặc thù của site này

Ngoài bộ chuẩn, ba thứ này trả lời đúng những câu hỏi mở của dự án:

### 4.1 `size_guide_open`
```js
gtag('event', 'size_guide_open', { item_name: '<tên sản phẩm>' });
```
**Vì sao:** chọn sai size là nguyên nhân trả hàng số một, mà chính sách đổi trả
lại bắt khách chịu ship 2 chiều. Tỉ lệ mở bảng size cao = khách đang không chắc.
→ Cần ảnh rõ hơn, hoặc số đo chi tiết hơn, hoặc thêm ảnh model mặc từng size.

### 4.2 `outbound_shopee`
```js
gtag('event', 'outbound_shopee', { link_url: '<url>' });
```
**Vì sao:** empty state và footer đang có link sang Shopee. Cần biết **bao nhiêu người
rời site để đi mua ở Shopee**. Con số này lớn nghĩa là site chưa cho khách lý do ở lại —
đúng câu hỏi mở lớn nhất của dự án.
*(Enhanced Measurement đã tự đo outbound click, nhưng event riêng dễ đọc hơn.)*

### 4.3 `currency_switch` — khi làm multi-currency
```js
gtag('event', 'currency_switch', { currency: 'USD' });
```
**Vì sao:** đo được **tỉ lệ khách quốc tế thật**, thay vì đoán.
Toàn bộ chiến lược EN-first đang dựa trên giả định này. Đây là cách kiểm chứng nó.

---

## 5. Câu hỏi kinh doanh → chỉ số nào trả lời

| Câu hỏi đang mở | Đo bằng | Ở đâu |
|---|---|---|
| **Tỉ lệ khách VN vs quốc tế?** | Users theo Country | GA4 → Reports → Demographics |
| **Có ai từ IG sang site không?** | Sessions theo Source/Medium | GA4 → Acquisition |
| **Khách rời site sang Shopee bao nhiêu?** | `outbound_shopee` | GA4 → Events |
| **Chỗ nào giết đơn hàng?** | phễu 4 event | GA4 → Explore → Funnel |
| **Khách quốc tế có bỏ giỏ ở checkout vì thấy giá VND không?** | `begin_checkout` chia theo Country | GA4 → Explore |
| **Sản phẩm nào đáng nhập thêm?** | `view_item` vs `purchase` theo item | GA4 → Monetisation |
| **Site đã đứng trên Shopee cho từ "vitalite" chưa?** | thứ hạng từ khoá thương hiệu | Search Console → Queries |
| **Trang nào chậm với khách thật?** | Core Web Vitals | Search Console |

> Cột giữa là lý do tồn tại của cả file này. Số nào không nằm ở cột trái thì không cần đo.

---

## 6. Báo cáo — nhịp cho một người

### Hằng tuần · 10 phút
GA4 → Reports snapshot

| Xem | Hỏi |
|---|---|
| Users, Sessions | tăng hay giảm so với tuần trước? |
| Sessions theo Source | traffic đến từ đâu? |
| `purchase` count + doanh thu | có đơn nào không? |
| Top 5 `view_item` | khách quan tâm gì? |

### Hằng tháng · 45 phút

1. **Phễu.** GA4 → Explore → Funnel với 4 event. Bước nào rụng mạnh nhất?
2. **Search Console → Queries.** Từ khoá nào đang hiển thị? Có từ nào ngoài dự đoán?
3. **Search Console → Pages.** Trang nào bị loại khỏi index và vì sao?
4. **Core Web Vitals.** Còn "Good" không?
5. **Country.** Tỉ lệ quốc tế thật là bao nhiêu? — đây là số kiểm chứng
   toàn bộ chiến lược EN-first
6. **`outbound_shopee`.** Bao nhiêu người bỏ site đi Shopee?

### Hằng quý

- Đối chiếu doanh thu site vs doanh thu Shopee
- Xem lại bộ event: cái nào chưa bao giờ dùng tới → **bỏ đi**
- Kiểm SSL còn hạn, chạy dọn database

---

## 7. Ngưỡng thực tế cho 90 ngày đầu

Site mới, 0 traffic, 10–20 SKU, không chạy ads.
Đây là ngưỡng để **biết có sống hay không**, không phải mục tiêu tăng trưởng.

| Chỉ số | 90 ngày | Ghi chú |
|---|---|---|
| Sessions/tháng | 300–800 | phần lớn từ IG bio |
| Tỉ lệ thêm giỏ | 3–6% | dưới 2% là PDP có vấn đề |
| Giỏ → checkout | > 40% | dưới nữa là giỏ hàng hoặc phí ship gây sốc |
| Checkout → mua | > 50% | **dưới 30% là checkout đang vỡ** — ưu tiên số một |
| Đơn/tháng | 5–20 | |
| Trang được index | ≥ số SKU + 8 | |

⚠️ **Đừng so với Shopee.** Shopee có 4 năm, 973 đánh giá, 6 voucher chồng nhau và
lưu lượng nội sàn. Site so với chính nó tháng trước, không so với Shopee.

---

## 8. Quyền riêng tư

| Việc | Trạng thái |
|---|---|
| Trang Privacy Policy | 🔴 **chưa có** — cần tạo. Bắt buộc nếu dùng GA4 |
| Cookie banner | 🟡 cần nếu có khách EU. Định hướng quốc tế → **có khả năng cần** |
| `anonymize_ip` | GA4 mặc định đã ẩn IP, không cần cấu hình |
| Thông tin người bán | 🔴 **bắt buộc theo pháp luật VN** — xem `PAGES-CONTENT.md` mục 4 |

> Claude **không viết text pháp lý**. Nêu ra là để user biết mục nào bắt buộc phải có.
> Trang Privacy Policy nên dùng mẫu của WordPress (`Cài đặt → Riêng tư`) làm khung
> rồi cho người có chuyên môn xem lại.

---

## 9. Thứ tự làm

```
1. Search Console + xác minh DNS TXT          ← làm được ngay, chưa cần launch
2. GA4 property + gắn mã                       ← trước khi có traffic
3. Lọc traffic nội bộ (đã có trong đoạn code)
4. GTM4WP cho ecommerce event                  ← sau khi có sản phẩm thật
5. Kiểm 4 event bằng GA4 DebugView             ← đặt một đơn thật để kiểm
6. Dựng Funnel trong Explore
7. (sau) 3 event tuỳ chỉnh
8. (sau, khi chạy ads) Meta / TikTok Pixel
```

**Bước 5 không được bỏ.** Event gắn sai mà không kiểm thì ba tháng sau mới phát hiện
là dữ liệu vô dụng — và lúc đó không lấy lại được.
