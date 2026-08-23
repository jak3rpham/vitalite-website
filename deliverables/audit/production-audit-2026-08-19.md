# AUDIT PRODUCTION — vitalite.io.vn
**Ngày:** 2026-08-19 · **Phương pháp:** xem trực tiếp qua browser, fetch status code thật

---

## 0. Tin tốt trước

```
<meta name="robots" content="noindex, nofollow">
```

**Site đang `noindex`.** Toàn bộ tên sản phẩm bịa và giá bịa **chưa lọt ra Google.**
Không có thiệt hại SEO, không có giá sai ngoài index.

> ⚠️ Đây là setting `Cài đặt → Đọc → Ngăn công cụ tìm kiếm` của WordPress.
> **Phải TẮT vào ngày launch.** Đây là lỗi bị quên nhiều nhất khi launch WP —
> site chạy vài tháng mà không ai index được. Ghi vào checklist launch ngay bây giờ.

---

## 1. Sản phẩm hiển thị là markup GIẢ, không phải WooCommerce

Đo trên DOM live:

| Selector | Số lượng |
|---|---|
| `.add_to_cart_button` | **0** |
| `a[href*="/product/"]` | **0** |

8 sản phẩm trên homepage — `Boxy Tee "Vitalité Mark"` 480.000₫, `Heavyweight Hoodie 480GSM`
1.290.000₫, `Washed Tee "Đường Phố"` 520.000₫, `Cropped Zip Jacket` 1.450.000₫, ... —
**không có cái nào là product thật.** Nút "THÊM VÀO GIỎ +" là `<button>` trơn,
bấm không xảy ra gì. Không link tới PDP vì không có PDP.

Khớp với `homepage-woocommerce.php:~220` — array hardcode.

**Mai:** Nghĩa là "Gate 2 — full purchase flow confirmed" trong CLAUDE.md là confirm trên
**sản phẩm test**, không phải qua đường này. Homepage hiện tại không nối vào cart flow ở bất kỳ điểm nào.

---

## 2. 9/14 route là 404

| Route | Status | Nguồn |
|---|---|---|
| `/shop` | ✅ 200 | footer + nav |
| `/cart` | ✅ 200 | header |
| `/checkout` | ✅ 200 → redirect `/cart` | (đúng — giỏ rỗng) |
| `/my-account` | ✅ 200 | header |
| `/?s=&post_type=product` | ✅ 200 | *chưa dùng — là fix đề xuất cho SEARCH* |
| `/collection/ss26` | 🔴 **404** | **CTA chính của hero** |
| `/new-arrivals` | 🔴 404 | nav + footer |
| `/product-category/ao` | 🔴 404 | nav |
| `/product-category/quan` | 🔴 404 | nav |
| `/category/ao` | 🔴 404 | footer — **và sai prefix**, Woo dùng `/product-category/` |
| `/category/quan` | 🔴 404 | footer — sai prefix |
| `/sale` | 🔴 404 | nav + footer |
| `/size-guide` | 🔴 404 | footer |
| `/shipping` | 🔴 404 | footer |
| `/returns` | 🔴 404 | footer |
| `/contact` | 🔴 404 | footer |
| `/collection`, `/about` | 🔴 nav, chưa test — gần như chắc 404 |

**Challenger:** Nút duy nhất trên hero — "SHOP SS26" — dẫn tới 404. Đường thoát duy nhất
khỏi homepage là "XEM TẤT CẢ (SHOP ALL)". Mọi lối khác đều chết.

Header và footer **không đồng bộ**: header `/product-category/ao`, footer `/category/ao`.
Hai người (hai lượt generate) viết ra, không ai đối chiếu.

---

## 3. Lỗi lặt vặt nhưng live

| Lỗi | Hiện tại | Đúng phải là |
|---|---|---|
| `<title>` | `Vitalite – My WordPress Blog` | tagline WP mặc định **chưa từng đổi** |
| `<html lang>` | `en-US` | nội dung là tiếng Việt → sai a11y, sai hreflang sau này |
| `#vtSearchModal` | `false` — không tồn tại trong DOM | nút SEARCH click chết (đã xác nhận) |
| Social footer | `https://instagram.com`, `tiktok.com`, `facebook.com` | **link về homepage nền tảng, không phải tài khoản vitalite** |
| Cart | `CART ( 0 )` dạng chữ | đã chốt: icon + badge đỏ, rỗng thì ẩn số |
| Lang switcher | `VI / EN`, VI active | đã chốt: **EN default tại root** |

Footer còn một claim: **"Streetwear made in Vietnam. Sản xuất giới hạn, phát hành theo đợt."**
→ `made in Vietnam` là claim sourcing, `sản xuất giới hạn` là claim scarcity.
Cùng loại với copy hero. **Cần xác nhận hoặc gỡ.**

---

## 4. Thứ tự sửa đề xuất

Không sửa 404 bằng cách tạo 10 trang rỗng. Phần lớn 404 sẽ **tự hết** khi có sản phẩm thật:

| Vấn đề | Hết khi nào |
|---|---|
| `/product-category/*` | Bước 8 — nhập sản phẩm + tạo category |
| `/new-arrivals`, `/sale`, `/collection` | Bước 8 — làm bằng shop archive có filter, không phải page riêng |
| Sản phẩm giả trên homepage | Bước 7 — build Elementor + Loop Grid động |
| `/size-guide` `/shipping` `/returns` `/contact` | **Chặn bởi user** — là policy fact, Claude không viết được |
| Hero CTA 404 | Sửa ngay được — trỏ về `wc_get_page_permalink('shop')` |
| SEARCH click chết | Sửa ngay được — 1 dòng |
| `<title>`, `lang`, footer social | Sửa ngay được |

**Nhóm "sửa ngay được" gom thành 1 lần chạm theme, sau khi backup xong.**

---

## 5. Chưa lấy được từ nguồn ngoài

Footer social trỏ về homepage nền tảng nên **không suy ra được tài khoản thật**.
Cần user cung cấp URL trực tiếp: Shopee shop · Instagram · TikTok · Facebook.
Đó là nơi duy nhất còn có brand fact thật (tên SKU, giá, mã đỏ, tone, chính sách).
