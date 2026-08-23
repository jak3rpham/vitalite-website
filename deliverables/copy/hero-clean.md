# HERO COPY — bản sạch claim

> ⚠️ **FILE NÀY ĐÃ LỖI THỜI (2026-08-20).**
> Nó đề xuất hero tối giản một slide. Thực tế đã dựng **hero 3 slide** với copy nguyên văn
> từ Instagram. Xem `template-parts/hero.php` và `docs/HANDOFF.md` mục 4.
> Giữ lại vì phần **truy vết chuỗi bịa** ở mục 1 vẫn còn giá trị tham chiếu.


> **Trạng thái:** user xác nhận 2026-08-19 — toàn bộ copy hero, tên sản phẩm và giá trong
> theme hiện tại là **bịa từ prototype Claude Design**. Không giữ lại dòng nào.
> File này là bản thay thế tạm, dùng cho tới khi có `BRAND_CONTEXT.md`.

---

## 1. Cái gì phải gỡ

### `banner-video.php:160`

```php
<p class="vt-hero-desc">BST Đường Phố SS26 — cotton 480GSM, form rộng, in lụa thủ công. Phát hành chính thức 20.08.</p>
```

| Chuỗi | Loại | Phán quyết |
|---|---|---|
| `cotton 480GSM` | product spec | 🔴 bịa — gỡ |
| `in lụa thủ công` | phương pháp sản xuất | 🔴 bịa — gỡ |
| `form rộng` | fit | 🔴 bịa — gỡ |
| `Phát hành chính thức 20.08` | ngày drop | 🔴 bịa — gỡ (false scarcity) |
| `BST Đường Phố SS26` | tên collection | 🔴 bịa — gỡ |
| `Sống Hết Công Suất` (h1) | tagline | 🔴 chưa duyệt — gỡ |
| `SS26 CAMPAIGN — 01 / 03` (tag) | — | 🔴 gỡ, và "01 / 03" ám chỉ 3 slide không tồn tại |
| `href="/collection/ss26"` | route | 🔴 route không tồn tại → 404 |

### `homepage-woocommerce.php:~220`

Hardcode array tên + giá sản phẩm (`Heavyweight Hoodie 480GSM`, `1.290.000₫`, ...).
**Không phải lỗi copy — là lỗi kiến trúc.** Vi phạm rule "template phải loop-safe".
Xử lý ở bước 7 (build homepage Elementor + Loop Grid động), không vá ở đây.

---

## 2. Nguyên tắc cho bản thay thế

Khi chưa có một fact nào được xác minh, hero **không được bán gì cụ thể**.
Việc duy nhất nó còn làm được — và vẫn là việc chính của hero — là: **giữ người xem lại, rồi đẩy vào catalog.**

Ba thứ được phép dùng, vì không cái nào là claim:
1. **Tên brand** — sự thật hiển nhiên
2. **Video** — hình ảnh tự nói, không phát biểu gì
3. **Điều hướng** — "xem hàng" là hành động, không phải lời hứa

Ba thứ bị cấm cho tới khi có BRAND_CONTEXT: chất liệu · phương pháp · ngày · tên collection · số lượng · giá.

---

## 3. Ba phương án

### A — Tối giản điều hướng ✅ khuyến nghị

```
[tag]   (bỏ hẳn)
[h1]    VITALITE
[desc]  (bỏ hẳn)
[cta]   Xem tất cả →     → /shop
```

Hero = video full-bleed + wordmark + 1 CTA. Không chữ thừa nào.
**Vì sao chọn cái này:** đây là trạng thái đúng của một site ngày đầu — chưa có gì để khoe thì
đừng khoe. Nó không trông "thiếu", nó trông *có chủ ý*. Nike homepage cũng hero video + 1 CTA.
Và khi BRAND_CONTEXT về, thêm chữ vào dễ hơn gỡ chữ ra.

### B — Có một dòng posture, zero-claim

```
[tag]   (bỏ)
[h1]    VITALITE
[desc]  Đồ mặc hằng ngày. Làm tại Việt Nam.        [NEED: xác nhận "làm tại VN" có đúng không]
[cta]   Xem tất cả →     → /shop
```

⚠️ "Làm tại Việt Nam" **vẫn là một claim về sourcing**. Chỉ dùng nếu ông xác nhận.
Nếu hàng nhập/gia công nước ngoài → bỏ dòng này, quay về phương án A.

### C — Placeholder có nhãn (chỉ dùng khi review nội bộ)

```
[h1]    VITALITE
[desc]  [PLACEHOLDER — chờ BRAND_CONTEXT.md]
[cta]   Xem tất cả →     → /shop
```

Không đẩy lên production. Chỉ để nhìn thấy chỗ trống khi review layout.

---

## 4. Patch cho `banner-video.php` (phương án A)

> ⛔ **CHƯA ÁP DỤNG.** Theme đang production, chờ backup UpdraftPlus verify xong.

```php
  <div class="vt-hero-content">
    <h1 class="vt-hero-title">VITALITE</h1>
    <div class="vt-hero-footer">
      <a href="<?php echo esc_url( wc_get_page_permalink('shop') ); ?>" class="vt-hero-cta">
        <?php esc_html_e('Xem tất cả', 'vitalite'); ?>
        <span aria-hidden="true" style="font-family:'JetBrains Mono',monospace;">→</span>
      </a>
    </div>
  </div>
```

Ba thay đổi kèm theo, không phải copy:
- `wc_get_page_permalink('shop')` thay `/collection/ss26` hardcode → không bao giờ 404
- bọc `esc_html_e()` sẵn cho bước 6 (i18n)
- `aria-hidden` cho mũi tên → screen reader không đọc "mũi tên phải"

CSS `.vt-hero-desc` và `.vt-hero-tag` giữ nguyên trong `style.css`, không xoá —
sẽ dùng lại khi có copy thật.

---

## 5. Câu hỏi mở

Hero nói gì được là hệ quả của **một câu chưa có lời đáp**:
*tại sao khách mua trên site thay vì Shopee?*

Trả lời được câu đó thì hero tự có nội dung. Chưa trả lời được thì mọi chữ viết thêm
vào hero đều chỉ là trang trí.
