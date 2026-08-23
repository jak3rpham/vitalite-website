# SEO — KẾ HOẠCH
**Ngày:** 2026-08-20 · **Site:** vitalite.io.vn · **Trạng thái:** chưa index (đang bật `noindex`)

---

## 0. Điểm xuất phát thật

| | |
|---|---|
| Tuổi domain | mới |
| Trang đã index | **0** — site đang `noindex, nofollow` |
| Backlink | ~0 |
| Nội dung | chưa có sản phẩm nào |
| Tài sản có sẵn | Shopee 4 năm · **973 đánh giá / 4.9 sao** · IG 7.001 · FB 6,8K |

**Chếch:** SEO ở đây **không phải** cuộc đua từ khoá. Với 10–20 SKU và domain mới,
không có cách nào thắng nổi Shopee hay các sàn trên từ khoá chung như *"áo thun oversize"*.

Ba việc thực tế, xếp theo giá trị:

1. **Từ khoá thương hiệu** — ai gõ `vitalite`, `vitalité vn`, `vitalite shop` phải thấy site,
   không phải chỉ thấy Shopee. Đây là thứ **thắng được chắc chắn**.
2. **Liên kết thực thể** — nói với Google rằng site này, IG này, FB này, Shopee shop này
   là **cùng một thực thể**. Đó là cách hợp lệ duy nhất để uy tín 4 năm kia có ý nghĩa với site mới.
3. **Từ khoá dài, tiếng Anh, quốc tế** — *"vietnamese streetwear brand"*,
   *"unisex heavyweight tee vietnam"*. Cạnh tranh thấp, và khớp đúng định hướng EN-first.

Cái **không** nên đuổi theo: từ khoá chung tiếng Việt. Sân đó là của Shopee, và
brand đã đứng sẵn ở đó rồi.

---

## 1. Ngày launch — 4 việc, theo đúng thứ tự

### 1.1 🔴 TẮT chặn index
`Cài đặt → Đọc` → bỏ tick **Ngăn công cụ tìm kiếm**.

> Đây là lỗi bị quên nhiều nhất khi launch WordPress. Site chạy nhiều tháng mà
> Google không index được dòng nào.
> Theme đã cài cảnh báo thường trực trong admin cho tới khi tắt (`inc/seo.php`).

**Không tắt trước khi có sản phẩm thật.** Để Google thu thập một site rỗng
là tạo ấn tượng đầu tiên xấu, và các trang rỗng đó nằm trong index rất lâu.

### 1.2 robots.txt
`Rank Math → General Settings → Edit robots.txt` (hoặc file thật ở gốc):

```
User-agent: *
Allow: /

Disallow: /cart/
Disallow: /checkout/
Disallow: /my-account/
Disallow: /*?add-to-cart=
Disallow: /*?orderby=
Disallow: /*?on_sale=
Disallow: /*?filter_
Disallow: /*?s=

Sitemap: https://vitalite.io.vn/sitemap_index.xml
```

**Vì sao chặn tham số lọc:** mỗi tổ hợp filter sinh một URL mới của **cùng một tập sản phẩm**.
Để Google thu thập hết là đốt crawl budget vào nội dung trùng lặp.
Theme cũng đã đặt `noindex` cho các URL này ở tầng meta (`inc/seo.php`) — hai lớp bảo vệ.

### 1.3 Sitemap
Rank Math sinh tự động. Bật:

| Bật | Tắt |
|---|---|
| Products | Posts (không có blog) |
| Product Categories | Tags |
| Pages | Product Tags |
| | Author archives |
| | Media/attachment |

Nộp `https://vitalite.io.vn/sitemap_index.xml` vào Search Console.

### 1.4 Search Console + Bing
- Xác minh domain qua bản ghi **DNS TXT** (không dùng thẻ HTML — nó mất khi đổi theme)
- Nộp sitemap
- Bing Webmaster Tools import thẳng từ Search Console
- **Cả hai đều miễn phí và bắt buộc.** Search Console là nguồn duy nhất cho biết
  Google thật sự thấy gì

---

## 2. 🔴 Redirect — có nợ phải trả

Site hiện có nhiều URL **đã từng tồn tại và đang 404**. Chúng đã từng nằm trong nav
và có thể đã được chia sẻ.

| URL cũ | Chuyển tới |
|---|---|
| `/collection/ss26` | `/shop` |
| `/new-arrivals` | `/shop?orderby=date` |
| `/category/ao` | `/product-category/t-shirts` |
| `/category/quan` | `/product-category/bottoms` *(tạm về `/shop`)* |
| `/product-category/ao` | `/product-category/t-shirts` |
| `/product-category/quan` | `/product-category/bottoms` |
| `/sale` | `/shop?on_sale=1` |

Dùng `Rank Math → Redirections`, kiểu **301**.

> **Vì sao 301 chứ không phải để 404:** 404 thì mất luôn người click, và nếu URL đó
> từng có backlink thì mất luôn giá trị link. 301 giữ cả hai.
>
> **Nhưng:** nếu chưa từng có ai chia sẻ những URL đó (site đang noindex nên khả năng cao là chưa),
> thì đây chỉ là dọn dẹp, không phải cấp bách. Vẫn nên làm — 15 phút.

Sau khi tạo redirect, **kiểm lại từng cái**. Redirect vòng lặp là lỗi tự gây ra hay gặp nhất.

---

## 3. Cấu trúc URL

```
/                              trang chủ
/shop                          tất cả sản phẩm
/product-category/t-shirts     danh mục
/product-category/outerwear
/product/{ten-san-pham}        PDP
/about  /size-guide  /shipping  /returns  /contact
/vi/…                          bản tiếng Việt (Polylang)
```

**Slug sản phẩm:** tiếng Anh, có tên dòng, không có mã SKU.
```
✅ /product/the-iconic-t-shirt-black
❌ /product/ao-thun-vitalite-iconic-unisex-den
❌ /product/vtl-ic-blk-001
```

> Slug tiếng Anh vì root là EN. Bản VI sẽ có slug tiếng Việt riêng do Polylang quản lý.

**Không đổi slug sau khi đã index.** Đổi là phải redirect, và mỗi redirect là một
bước nhảy phụ. Chốt quy ước ngay từ sản phẩm đầu tiên.

---

## 4. Title & meta

### Khuôn

| Trang | Title | Meta description |
|---|---|---|
| Trang chủ | `VITALITÉ — Streetwear made in Vietnam` | Unisex streetwear from Saigon. Heavyweight cotton, boxy fits, silkscreen graphics. Worldwide shipping. |
| Shop | `Shop All — VITALITÉ` | Every VITALITÉ piece. Unisex sizing S–L, made in Vietnam. |
| Danh mục | `{Tên danh mục} — VITALITÉ` | viết tay từng cái, 1–2 câu |
| PDP | `{Tên sản phẩm} — VITALITÉ` | `{fabric}, {fit}, sizes S–M–L. Made in Vietnam.` |
| About | `About — VITALITÉ` | |

**Độ dài:** title ≤ 60 ký tự, description 120–155.

⚠️ **Description không phải yếu tố xếp hạng.** Nó là **quảng cáo trong kết quả tìm kiếm** —
viết để người ta bấm vào, không phải để nhồi từ khoá.

⚠️ **Không tự động sinh description từ mô tả sản phẩm.** Mô tả sản phẩm là 4 gạch đầu dòng
spec — cắt 155 ký tự đầu ra sẽ thành `• Fabric: 250 GSM Cotton • Fit: Signature…`, đọc như máy.
Viết tay cho từng SKU. Với 10–20 SKU thì đó là một buổi làm việc, không phải dự án.

---

## 5. Dữ liệu có cấu trúc

Theme đã tự in khi **chưa** có plugin SEO (`inc/seo.php`), và **tự tắt** khi có plugin
để tránh in hai lần.

| Loại | Ở đâu | Ghi chú |
|---|---|---|
| `Organization` | trang chủ | có `sameAs` trỏ IG · TikTok · FB · Shopee |
| `WebSite` + `SearchAction` | trang chủ | |
| `Product` + `Offer` | PDP | chỉ khai trường **có thật** |
| `BreadcrumbList` | mọi trang con | |

### 🔴 `sameAs` là mục quan trọng nhất

```json
"sameAs": [
  "https://www.instagram.com/vitalitevn/",
  "https://www.tiktok.com/@vitalitevn",
  "https://www.facebook.com/vitalitevn",
  "https://shopee.vn/vitalitevn"
]
```

Đây là cách nói với Google rằng bốn hồ sơ kia và site này là **cùng một thực thể**.
Với brand có 973 đánh giá trên Shopee mà website mới tinh, đây là con đường hợp lệ
duy nhất để uy tín kia có ý nghĩa gì đó với site.

Làm cho nó chắc hơn: **link ngược lại** từ mỗi hồ sơ về `vitalite.io.vn`
(bio Instagram, About Facebook, mô tả shop Shopee nếu Shopee cho).
Liên kết hai chiều mạnh hơn hẳn một chiều.

### ❌ Tuyệt đối không khai

`aggregateRating` và `review` khi site chưa có đánh giá nào.
Lấy con số 4.9/973 của Shopee gắn vào schema của site là **khai báo sai** —
vi phạm chính sách dữ liệu có cấu trúc của Google và bị phạt thủ công.

> Hiển thị *"4.9 sao · 973 đánh giá trên Shopee"* dưới dạng **chữ có dẫn nguồn công khai**
> thì được — đó là dẫn chiếu trung thực, không phải khai báo schema. Nhưng nó gửi khách
> sang Shopee, nên là quyết định kinh doanh. **Chưa làm, chờ user quyết.**

---

## 6. Hai ngôn ngữ

`hreflang` do Polylang lo. Kiểm tra sau khi cấu hình:

```html
<link rel="alternate" hreflang="en" href="https://vitalite.io.vn/shop" />
<link rel="alternate" hreflang="vi" href="https://vitalite.io.vn/vi/shop" />
<link rel="alternate" hreflang="x-default" href="https://vitalite.io.vn/shop" />
```

| Quy tắc | |
|---|---|
| `x-default` trỏ về **bản EN** | root là EN, và khách quốc tế là mặc định |
| Mỗi trang tự trỏ về chính nó | thiếu self-reference là hreflang bị bỏ qua hoàn toàn |
| Trỏ hai chiều | EN trỏ VI **và** VI trỏ EN, nếu không Google bỏ qua |
| Không tự dò ngôn ngữ trình duyệt | đã chốt: phá cache, hại SEO, tín hiệu không đáng tin |

> **Chỉ launch VI khi bản dịch đã đủ.** Trang VI thiếu nội dung sẽ được index rồi
> mới bị Google thấy là kém — tệ hơn là chưa từng có.
> Quyết định đã chốt: **build EN xong hết → dịch VI → launch cả hai cùng lúc.**

---

## 7. Liên kết nội bộ

Site nhỏ nên liên kết nội bộ đơn giản nhưng vẫn quan trọng: nó là cách Google
hiểu trang nào quan trọng.

| Từ | Tới |
|---|---|
| Trang chủ | Shop, T-Shirts, Outerwear, About |
| PDP | danh mục cha, Size Guide, Returns |
| Size Guide | Shop |
| About | Shop |
| Footer | mọi trang (đã có) |

**Đã cài sẵn trong theme:**
- Breadcrumb trên shop và PDP
- Bảng size gập/mở ngay trong PDP (không phải link ra ngoài — giảm ma sát khi mua)
- Footer đầy đủ trên mọi trang

---

## 8. Không làm ở giai đoạn này

| ❌ | Vì sao |
|---|---|
| Blog / nội dung SEO | Solo operator. Blog cần nhịp đều mới có tác dụng. Bỏ dở nửa chừng còn tệ hơn không làm |
| Mua backlink | rủi ro phạt, và với brand đã có social thật thì không cần |
| Nhồi từ khoá vào tên sản phẩm | `Áo thun nam nữ oversize form rộng streetwear` — đọc như hàng chợ, và Google không còn ăn cái này từ lâu |
| Landing page theo từ khoá | chưa có gì để nói mà không lặp lại trang shop |
| Đuổi từ khoá chung tiếng Việt | sân của Shopee, và brand đã đứng sẵn ở đó |

---

## 9. Việc cần làm, theo thứ tự

```
TRƯỚC LAUNCH
 1. Cài Rank Math, cấu hình sitemap
 2. Viết title + description cho: trang chủ, shop, 2 danh mục, mọi PDP
 3. Kiểm tra JSON-LD Organization có đủ sameAs
 4. Tạo redirect cho 7 URL cũ đang 404
 5. Kiểm hreflang sau khi cấu hình Polylang

NGÀY LAUNCH
 6. TẮT "Ngăn công cụ tìm kiếm"        ← quan trọng nhất
 7. Nộp sitemap vào Search Console + Bing
 8. Yêu cầu index trang chủ và shop bằng URL Inspection
 9. Thêm link về vitalite.io.vn vào bio IG, About FB, mô tả Shopee

SAU LAUNCH — 30 ngày đầu
10. Search Console → Coverage: kiểm trang nào bị loại và vì sao
11. Search Console → Core Web Vitals
12. Kiểm URL bị Google coi là trùng lặp (thường là URL lọc lọt lưới)
13. Tìm từ khoá thương hiệu: site đã đứng trên Shopee cho từ "vitalite" chưa?
```

---

## 10. Đo cái gì

| Chỉ số | Nguồn | Ngưỡng 90 ngày |
|---|---|---|
| Trang được index | Search Console → Pages | ≥ số SKU + 8 |
| Hiển thị từ khoá thương hiệu | Search Console → Queries | site đứng #1 cho `vitalite` |
| Click từ organic | Search Console | có xu hướng tăng |
| Core Web Vitals | Search Console | ≥ 90% URL "Good" |
| Lỗi thu thập | Search Console → Pages | 0 lỗi server |

**Không đo thứ hạng bằng công cụ bên thứ ba.** Thứ hạng khác nhau theo từng người,
từng nơi, từng thiết bị. Search Console là số liệu thật của chính mình.
