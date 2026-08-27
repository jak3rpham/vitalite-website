# Header experiments — KHÔNG PHẢI FILE CHẠY THẬT

Thư mục này chứa bản nháp header. **Không copy thẳng vào theme.**
Header đang chạy thật là:

- `vitalite-theme-2/header.php` → gọi `template-parts/site-header.php`
- CSS ở `vitalite-theme-2/style.css`, mục `HEADER`

---

## `header-woocommerce.php` (27/08/2026)

Bản nháp "liquid glass". Đã lấy phần hay ra, phần còn lại giữ đây để tham khảo.

### ✅ Đã hút vào theme
- Chiều sâu kính: `blur(20px) saturate(190%)`, viền sáng `inset` ở mép trên,
  đổ bóng dưới header. Đã token hoá thành `--vt-glass-*` trong `tokens.css`.

### 🔴 Vì sao KHÔNG dùng nguyên file — 8 lỗi

1. **`add_filter()` nằm trong template.** Dòng 236 đăng ký
   `woocommerce_add_to_cart_fragments` mỗi lần render. Lúc Woo gọi AJAX thì
   template không được nạp → filter không tồn tại → số giỏ hàng không bao giờ
   cập nhật. Hook phải nằm ở `inc/`, và **đã có sẵn** ở
   `inc/woocommerce.php` dòng 37.
2. **Đè class của theme.** `.vt-nav`, `.vt-header-left`, `.vt-header-right`
   trùng tên với rule đang có trong `style.css` → hai bộ luật đánh nhau.
3. **`:root` thứ ba.** Định nghĩa lại `--vt-header-h`, `--vt-dark-bg`… trong
   `<style>` inline. Vi phạm CLAUDE.md mục 0: màu chỉ có một nguồn là
   `deliverables/brand/tokens.css` + `:root` của theme.
4. **Không có menu mobile.** `@media (max-width:1024px) { .vt-nav { display:none } }`
   mà không có nút burger thay thế → dưới 1024px header chỉ còn logo và giỏ hàng.
5. **Nút SEARCH chết.** `onclick` mở `#vtSearchModal` — phần tử đó không tồn
   tại ở đâu trong theme.
6. **Link nav trỏ vào 404.** `/new-arrivals`, `/product-category/ao`,
   `/quan`, `/sale` là URL bịa. Theme dùng `vt_cat_url()` / `vt_page_url()`,
   chỉ in link khi taxonomy/page có thật.
7. **Không i18n.** Chuỗi viết cứng, không qua `__()`. Site EN default, mà nav
   lại ghi "Áo" / "Quần". Và `VI/EN` là hai `<span>` tĩnh, không bấm được,
   sai cả thứ tự (quyết định đã chốt: EN trước).
8. **`scrollY > 500` viết cứng.** Theme dùng IntersectionObserver bám
   `[data-vt-header-sentinel]` ở đáy banner, đúng với mọi chiều cao banner.
   Scroll listener chạy hàng chục lần mỗi giây; ngưỡng cứng 500px thì sai ngay
   khi banner cao khác đi.

### 💡 Ý còn đáng làm — CHƯA làm, cần cân nhắc

**Logo bằng CSS mask thay cho `filter: invert(1)`** (dòng 71–85).
Cho `<span>` nền `currentColor` + `mask: url(logo.png)`, logo tự đổi màu theo
header, bỏ được 3 chỗ hack `filter: invert(1)` đang rải trong `style.css`
(dòng 356, 357, 1198). Đúng hướng cái TODO đang ghi ở `inc/helpers.php` dòng 118.

Chưa làm vì site **chưa deploy thử lần nào**. Đổi cách render logo ngay trước
lần chạy thật đầu tiên là thêm biến số không cần thiết. Làm sau khi deploy xong.
