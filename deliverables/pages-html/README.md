# TRANG TĨNH — HTML dán vào Elementor

**Sinh bằng:** `docs/make-pages.py` · **Cập nhật:** 2026-08-23
**Thiết kế dựa trên:** cấu trúc chính sách của Saigon Swagger (8 trang) và StressMama (7 mục)

---

## Cách dùng

1. `Trang → Thêm mới`
2. Đặt **tiêu đề** và **slug** đúng như bảng bên dưới — theme dò page **theo slug**, sai slug là
   link ở footer không hiện
3. Sửa bằng Elementor → kéo widget **HTML** vào → dán **toàn bộ** nội dung file `.html`
4. Không cần thêm gì khác. Mỗi file tự mang CSS, scope trong `.vtp` nên không rò ra ngoài
5. `Xuất bản`

> **Đừng sửa file `.html` bằng tay.** Chúng được sinh ra. Sửa trong `docs/make-pages.py`
> rồi chạy lại, nếu không lần sinh sau sẽ ghi đè mất.
>
> ```bash
> cd "E:\Vitalite website"; python docs/make-pages.py
> ```

---

## 🔴 Ô cam = chưa được publish

Trong trang có những **ô nền cam** ghi *"Chưa có dữ liệu"*. Đó là chỗ Claude **cố ý không điền** —
bịa phí ship, thời gian giao, hay điều khoản pháp lý là bịa ra một hợp đồng với khách.

**Trang nào còn ô cam thì chưa publish.** Điền xong, xoá ô đó đi, rồi mới xuất bản.

Tổng: **23 ô** trên 11 trang.

---

## Cần làm những trang nào

### Nhóm 0 — thương hiệu

| Slug | Tiêu đề | File | Ô cam | Ghi chú |
|---|---|---|---|---|
| `about` | About | `about.html` | **1** | ✅ Đăng được. Ô cam là quyết định kinh doanh (có hiện 4.9★/973 đánh giá Shopee không), không phải thiếu dữ liệu. 🔴 **Phải upload frame trước** — xem ngay dưới |

**Riêng trang About — HERO là ảnh.** Khối đầu trang là chuỗi cuộn 96 frame WebP.
Trước khi publish, upload thư mục:

```
deliverables/scroll-sequence/frames/0823/   →   wp-content/uploads/seq/0823/
```

**99 file**: 96 frame (10,6 MB) + 3 poster `poster-960/1440/1920.webp` (30 / 50 / 72 KB).

- Thiếu **frame** thì hero chỉ còn ảnh tĩnh, chữ hiện đủ, không sập trang.
- Thiếu **poster** thì hero trống. Poster là bắt buộc, nó là LCP của cả trang.
- Để chỗ khác thì phải đổi `data-seq-base` **và** cả `src` lẫn `srcset` của `.vsq-poster`.

Khối này **không tải frame nào trên màn ≤820px** (đã đo: 0 request), nên 10,6 MB chỉ giáng
lên desktop, và chỉ sau `window.load`.

Mọi câu trích trong trang About là **nguyên văn** từ Instagram / Facebook `@vitalitevn`,
đã xác minh 2026-08-19, ghi lại ở `reference/BRAND_ERA_SPLIT.md`. Không có câu nào tự nghĩ.

### Nhóm A — chính sách thương mại

| Slug | Tiêu đề | File | Ô cam | Ghi chú |
|---|---|---|---|---|
| `returns` | Returns & Exchanges | `returns.html` | **3** | Gần đủ. Thiếu: hoàn tiền, ship đổi size, địa chỉ nhận |
| `shipping` | Shipping | `shipping.html` | **4** | 🔴 **Chặn launch.** Chưa có một con số nào |
| `payment` | Payment | `payment.html` | **3** | Chờ cấu hình cổng thanh toán thật |
| `size-guide` | Size Guide | `size-guide.html` | **1** | Áo thun đủ. Thiếu số đo hoodie |

### Nhóm B — bắt buộc theo luật TMĐT Việt Nam

Bốn trang này **không phải tuỳ chọn**. Thiếu là vi phạm.

| Slug | Tiêu đề | File | Ô cam | Ghi chú |
|---|---|---|---|---|
| `seller-information` | Seller Information | `seller-information.html` | **2** | 🔴 Thiếu toàn bộ thông tin pháp nhân |
| `privacy` | Privacy Policy | `privacy.html` | **3** | Cấu trúc đủ, cần người có thẩm quyền duyệt |
| `terms` | Terms of Service | `terms.html` | **2** | Mục giới hạn trách nhiệm phải có luật sư |
| `complaints` | Complaints | `complaints.html` | **2** | Thiếu hotline + thời hạn xử lý |

### Nhóm C — nên có

| Slug | Tiêu đề | File | Ô cam | Ghi chú |
|---|---|---|---|---|
| `faq` | How to Order | `faq.html` | **1** | Giảm tin nhắn hỏi lặp |
| `contact` | Contact | `contact.html` | **1** | Email + IG + FB đã xác minh. Ô cam: số điện thoại nào còn dùng, và có công bố giờ trả lời không. Tạo trang này là link **Contact** ở footer tự hiện |

### Nhóm D — đã có nội dung, chưa có HTML

Nội dung nằm ở `deliverables/content/PAGES-CONTENT.md`, dán bằng trình soạn thảo thường.

| Slug | Tiêu đề | Trạng thái |
|---|---|---|
| `collection` | Collection | ⚠️ mới là khung. **Chưa dựng HTML** vì mỗi dòng cần link tới filter `pa_collection` có thật, mà sản phẩm chưa nhập. Dựng sau bước 9 |

> `contact` đã chuyển lên nhóm C, có HTML rồi. Xem bảng bên trên.

---

## Footer tự nối link — không phải sửa code

`vt_maybe_link()` chỉ in link khi page **tồn tại và đã publish**. Nên cứ tạo dần, footer tự đầy lên.

| Cột footer | Slug nó dò |
|---|---|
| **Support** | `size-guide` · `shipping` · `returns` · `contact` |
| **Legal** | `payment` · `privacy` · `terms` · `complaints` · `seller-information` |

Cột **Legal** vừa được thêm vào `template-parts/site-footer.php`. Chưa publish trang pháp lý nào
thì cả cột tự ẩn, lưới footer không vỡ.

⚠️ Đổi slug ở đây thì phải đổi cả trong `site-footer.php`, nếu không link biến mất.

---

## Ngôn ngữ

Bộ HTML này là **tiếng Anh** — đúng theo quyết định đã chốt: EN ở root, VI ở `/vi/`.

Bản tiếng Việt làm ở **bước 12**, bằng Polylang, sau khi bản EN xong hết. Đừng dịch sớm —
mỗi lần sửa nội dung là phải sửa hai lần.

⚠️ Trang **pháp lý** có thể cần bản tiếng Việt ngay từ đầu để đúng luật.
`[NEED: xác nhận với người có chuyên môn]`

---

## Thiết kế — nó ăn theo theme

CSS dùng biến của theme và có giá trị dự phòng:

```
--vt-ink · --vt-paper · --vt-line · --vt-muted · --vt-tint · --vt-sale
--vt-font-display · --vt-font-mono
```

Nghĩa là khi brand chốt mã màu tím/xanh dương thời kỳ mới và bạn đổi `--vt-accent` trong
`style.css`, **cả 10 trang này đổi theo**, không phải sửa lại từng trang.

Ngôn ngữ layout giữ đúng phần còn lại của site: eyebrow mono đánh số, tiêu đề Archivo Expanded
in hoa, đường kẻ đen dưới đầu trang, bảng hairline, nút bo tròn hoàn toàn.

**Mục lục dính bên trái** trên desktop; dưới 900px nó thành hàng pill nằm ngang.
Bảng cuộn ngang trong khung riêng — trang không bao giờ tràn ngang. Đã đo ở 390px và 1280px.

---

## Xem thử không cần WordPress

`_preview-all.html` gộp cả 10 trang chính sách vào một file, mỗi trang trong một khung giống
Elementor. `_preview-about.html` là trang About riêng, full-bleed.

🔴 **Hai file preview giờ SINH TỰ ĐỘNG** cùng lúc với các trang, bởi `docs/make-pages.py`.
Trước đây chúng làm tay nên lệch với trang thật sau mỗi lần sửa. Đừng sửa tay chúng nữa.
Mở thẳng bằng trình duyệt.

File đó **chỉ để xem** — đừng dán nó vào WordPress.
