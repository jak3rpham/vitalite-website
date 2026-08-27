# Bản xem trước toàn site

```bash
python3 docs/make-site-preview.py
python3 -m http.server 8000 -d deliverables/preview/site
```

Mở http://localhost:8000 — 16 trang, bấm qua lại được bằng header và footer.

`site/` **sinh ra tự động** và đã nằm trong `.gitignore`. Chạy lại script là dựng
lại từ đầu. Đừng sửa tay trong đó, sửa `docs/make-site-preview.py`.

---

## 🔴 Bản này KHÔNG chứng minh theme chạy được

Theme thật là **PHP + WooCommerce**. Máy dev không có PHP, nên đây là bản dựng lại
bằng HTML tĩnh.

| Trả lời được | KHÔNG trả lời được |
|---|---|
| Bố cục có ổn không | Template PHP có render đúng trên hosting không |
| Điều hướng có thông không | Vòng lặp WooCommerce có chạy không |
| Chữ có tràn, có vỡ dòng không | Cart / checkout có hoạt động không |
| Responsive gãy ở đâu | Polylang, LiteSpeed, gateway thanh toán |

Ba câu bên phải chỉ **deploy** mới trả lời được — `deliverables/setup/DEPLOY.md`.

---

## Thật / giả

**THẬT** — `style.css` **copy thẳng** từ theme (không chép tay, nên không bao giờ
lệch màu với production), `site.js` thật, toàn bộ ảnh hero / gallery / collection,
video hero đã nén, 96 frame scroll-sequence, và 14 fragment HTML đã duyệt.

**GIẢ** — **mọi thẻ sản phẩm.** Site chưa có SKU nào. Mỗi thẻ mang badge `PH`,
tên bắt đầu bằng `[PLACEHOLDER]`, giá là `0.000.000 ₫`.
Ảnh mockup là ảnh thật nhưng **không gắn với SKU nào** — chỉ để xem tỷ lệ khung.
Bản thật render `empty-state` chứ không render lưới; ở đây cố tình dựng lưới giả
vì hai section trống thì không duyệt được bố cục.

Thanh cam dưới đáy màn hình nhắc điều này ở mọi trang.

---

## Giới hạn đã biết

- **Header/footer ở đây là bản CHÉP** của `site-header.php` / `site-footer.php`.
  Không chạy được PHP thì không có cách nào khác. Sửa file theme thì **sửa cả
  `docs/make-site-preview.py`**, nếu không hai bên trôi khỏi nhau.
  Giới hạn thiệt hại: script **không mang CSS riêng dòng nào** — màu và style chỉ
  đến từ `style.css` của theme. Lệch markup thì nhìn thấy ngay; lệch màu thì không,
  nên chỗ nguy hiểm hơn đã được chặn.
- **Không có query string.** `?orderby=date`, `?on_sale=1`, `?collection=…` rụng hết,
  mọi link kiểu đó đổ về `shop.html`. Nên "New Arrivals", "Sale", "T-Shirts" trong nav
  và footer đều ra cùng một trang.
- **Search không chạy** — cần WordPress.
- `product.html` và `cart.html` là **prototype**, không phải template thật.
  Đọc phần đầu file gốc trong `deliverables/woo-templates/` trước khi dùng.
