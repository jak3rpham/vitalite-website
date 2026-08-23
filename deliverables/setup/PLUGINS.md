# PLUGIN — cài gì, vì sao, giá phải trả
**Ngày:** 2026-08-20

---

## Nguyên tắc

Mỗi plugin là một khoản nợ: nó chạy trên **mọi** lượt xem trang, nó phải được cập nhật,
và nó là một bề mặt bảo mật nữa. Trên shared hosting, plugin là nguyên nhân chậm số một —
đứng trên cả ảnh chưa nén.

Mỗi mục dưới đây trả lời ba câu: **làm gì · tốn gì · có cách nào không cần plugin không.**

---

## Đang cài — giữ

### Elementor Pro
**Làm gì:** dựng trang tĩnh (About, Collection).
**Tốn:** ~90KB CSS+JS trên trang có dùng. Theme đã cấu hình để trang không dùng Elementor thì không nạp.
**Lưu ý:** ❌ **Không dùng Elementor Theme Builder** cho header/footer — quyết định đã chốt.
Header/footer là PHP template. Dùng cả hai là hai nguồn sự thật, chắc chắn vỡ.

### WooCommerce
Bắt buộc.

### Premmerce Product Filter
**Làm gì:** lọc theo Size, Color.
**Tốn:** vừa. Query lọc nặng nếu catalog lớn — với 10–20 SKU thì không thành vấn đề.
⚠️ **Chưa test với Polylang.** Test bằng 2 sản phẩm giả trước khi nhập thật.
**Lưu ý:** theme giữ class `.products` trên lưới shop để bộ lọc AJAX tìm được container.

### UpdraftPlus
**Làm gì:** backup tự động lên Google Drive.
**Tốn:** chỉ chạy theo lịch, không ảnh hưởng front-end.
**Cấu hình:** hằng tuần, giữ 4 bản, cả file lẫn database.

---

## Cần cài

### 1. Polylang — 🔴 ƯU TIÊN CAO NHẤT

**Làm gì:** EN ở root, VI ở `/vi/`.
**Tốn:** nhẹ ở front-end. Nặng ở khâu vận hành — mỗi nội dung phải có hai bản.
**Vì sao phải cài TRƯỚC khi nhập sản phẩm:** attribute term (`S`, `M`, `Black`…) là taxonomy term.
Tạo term trước khi bật Polylang cho `pa_*` thì phải gán ngôn ngữ **tay cho từng term và từng SKU**.

**Sáu quyết định khi cài:**

| | Chọn | Vì sao |
|---|---|---|
| Ngôn ngữ | `English (en_US)` + `Tiếng Việt (vi)` | |
| Ngôn ngữ mặc định | **English** | quyết định đã chốt: EN ở root |
| Cấu trúc URL | **Thư mục con**, `/vi/` | EN không có tiền tố |
| Ẩn tiền tố ngôn ngữ mặc định | ✅ **có** | root là EN sạch, không phải `/en/` |
| Tự dò ngôn ngữ trình duyệt | ❌ **KHÔNG** | phá cache, hại SEO, tín hiệu không đáng tin. Đã chốt |
| Dịch media | ❌ **TẮT** | đã chốt. Ảnh không cần bản dịch — chỉ nhân đôi thư viện |

⚠️ **Chưa dịch gì cả ở bước này.** Chỉ cấu hình. Dịch sau khi build xong EN.

---

### 2. LiteSpeed Cache

**Làm gì:** cache trang, tối ưu ảnh, CDN QUIC.cloud.
**Tốn:** gần như không — nó chạy ở tầng server, không phải PHP.
**Vì sao chọn cái này:** hosting là LiteSpeed. Dùng cache plugin khác (WP Rocket, W3TC)
là bỏ phí cache tầng server và thêm một lớp trùng lặp.

🔴 **Cấu hình cực kỳ quan trọng:** xem `HOSTING-LITESPEED.md`.
Đặc biệt: **TẮT minify CSS/JS** — xung đột với Elementor.

---

### 3. Plugin SEO — chọn **một**

| | Ưu | Nhược |
|---|---|---|
| **Rank Math** ⭐ | sitemap + schema + redirect trong bản free, nhẹ hơn Yoast | UI nhiều thứ, dễ rối |
| Yoast SEO | quen thuộc, tài liệu nhiều | redirect nằm ở bản trả phí |
| Không cài | 0 chi phí | phải tự làm sitemap, không có công cụ redirect |

**Khuyến nghị: Rank Math free.**

> Theme **tự tắt** phần SEO của nó khi phát hiện có plugin SEO (`inc/seo.php`,
> hàm `vt_seo_plugin_active()`). Không lo hai nguồn cùng in meta description
> hay JSON-LD. Không cài plugin thì theme tự lo — nhưng không có sitemap và không có redirect.

**Vì sao cần công cụ redirect:** site đang có nhiều URL cũ đã 404
(`/collection/ss26`, `/new-arrivals`, `/category/ao`…). Link cũ đã chia sẻ ra ngoài
cần được chuyển hướng chứ không phải trả 404.

Cấu hình chi tiết: `deliverables/seo/SEO-PLAN.md`.

---

### 4. 🔴 Multi-currency — CHƯA CÀI

**Chưa chốt được mô hình** vì chưa có số liệu phí ship quốc tế.

**Ràng buộc cứng cần biết trước:**

| Cổng | Quyết toán được |
|---|---|
| MoMo / VNPay | **chỉ VND** |
| PayPal | USD, EUR, và nhiều loại |
| Stripe | **không nhận merchant VN trực tiếp** |

Plugin multi-currency đổi được **con số hiển thị**, nhưng **không tạo ra khả năng quyết toán**.

| Mô hình | Cách làm | Plugin |
|---|---|---|
| **A. Hiển thị đa tiền tệ, thu VND** ⭐ | đổi tỉ giá để hiển thị, checkout tính VND | phần lớn **không cần plugin** |
| B. Thu thật đa tiền tệ | VND qua MoMo/VNPay, USD qua PayPal | cần plugin, hai luồng đối soát |

**Khuyến nghị: A trước, B sau khi có đơn quốc tế thật.**
Làm B trước khi có đơn nào là đầu tư vào một giả định.

---

## KHÔNG cài

| Plugin | Vì sao không |
|---|---|
| Slider Revolution / bất kỳ slider nào | Hero đã là video. Slider = ~200KB JS cho một thứ không ai vuốt |
| Popup / newsletter popup | Chưa có danh sách email, chưa có provider. Popup chặn khách để lấy thứ không dùng được |
| Trình tạo trang thứ hai (WPBakery, Divi…) | Đã có Elementor. Hai builder cùng lúc là hỏng chắc chắn |
| Plugin "tối ưu tốc độ" thứ hai | Đã có LiteSpeed Cache. Hai cache chồng nhau gây lỗi khó tìm nhất trong WordPress |
| Jetpack | Cồng kềnh, phần lớn tính năng không dùng, gọi ra ngoài mỗi lần tải trang |
| Plugin đánh giá giả / social proof giả | Đang có **973 đánh giá thật** trên Shopee. Không cần bịa, và bịa là vi phạm chính sách Google |
| Contact Form 7 | Trang Contact chỉ có email + link social. Một `mailto:` đủ dùng. Cài khi thật sự cần form |
| Plugin "security" toàn diện (Wordfence full…) | Trên shared hosting nó tốn CPU thật. Theme đã tắt XML-RPC, chặn SVG cho non-admin, thêm header bảo mật. Cộng với `DISALLOW_FILE_EDIT` là đủ cho quy mô này |

---

## Thứ tự cài

```
1. LiteSpeed Cache      ← trước, để đo được cải thiện của các bước sau
2. Polylang             ← CHẶN việc nhập sản phẩm
3. Rank Math            ← trước khi có nội dung, để sitemap sinh đúng từ đầu
4. (sau) multi-currency ← chờ số liệu ship quốc tế
```

Sau mỗi plugin: xem thử trang chủ, shop, PDP, giỏ hàng. Vỡ thì biết ngay do plugin nào.

---

## Ngân sách

| | Giá | Bắt buộc? |
|---|---|---|
| Polylang free | 0 | ✅ đủ dùng |
| LiteSpeed Cache | 0 | ✅ |
| Rank Math free | 0 | ✅ đủ dùng |
| UpdraftPlus free | 0 | ✅ |
| Premmerce free | 0 | ✅ |
| Elementor Pro | đã mua | |
| **Canva Pro** | ~$10/tháng | 🟡 cần nếu muốn ảnh mockup nền trong suốt |

Toàn bộ nền tảng chạy được với **0₫ plugin**. Khoản duy nhất đáng cân nhắc là Canva Pro,
và đó là chi phí ảnh chứ không phải chi phí web.
