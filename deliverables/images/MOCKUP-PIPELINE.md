# MOCKUP — TÌNH TRẠNG & QUY TRÌNH ẢNH
**Ngày:** 2026-08-20 · **Nguồn:** `mockup-all/` (19 file, 1000×1000 PNG)

---

## 1. Cắt nền tự động — ĐÃ THỬ, KHÔNG DÙNG ĐƯỢC

User cần ảnh nền trong suốt để đặt sản phẩm lên nền tối.
Đã thử flood-fill từ 4 góc (chỉ ăn vùng trắng **liền mạch**, không đụng highlight bên trong áo).

### Kết quả đo trên cả 18 file

| Nhóm | Số file | Kết quả |
|---|---|---|
| **Áo tối** (độ sáng < 150) | **6** — `1 2 5 6 11 12` | ✅ cắt sạch |
| **Rủi ro** (150–210) | **6** — `4 7 10 13 14 17` | ⚠️ mất mảng, có quầng |
| **Áo sáng** (> 210) | **6** — `3 8 9 15 16 18` | ❌ **hỏng hoàn toàn** |
| Trống | `19` | — |

### Vì sao áo sáng hỏng

Nền là `#FFFFFF` thuần. Áo trắng cũng có vùng `#FFFFFF` thuần, và những vùng đó
**nối liền với nền qua mép khử răng cưa**. Flood-fill không phân biệt được — nó tràn vào trong áo.
Ảnh thử `mockup-all/cutout/7_on_dark.png` cho thấy áo trắng bị khoét thủng từng mảng.

**Không có ngưỡng nào cứu được.** Chặt hơn thì để lại quầng trắng, lỏng hơn thì khoét sâu hơn.

### Và kể cả nếu chạy được thì vẫn không nên

Nửa catalog cắt được, nửa không → **lưới sản phẩm không đồng nhất**.
Sáu áo đen nổi trên nền tối, sáu áo trắng vẫn mang khối nền trắng vuông. Xấu hơn là không làm gì.

**Kết luận: sửa ở nguồn, không sửa ở hậu kỳ.**

### Ba đường ra

| | Cách | Chi phí |
|---|---|---|
| **A** | Xuất lại từ Canva với nền trong suốt (**Canva Pro**, hoặc Background Remover) | tiền thuê bao |
| **B** | Chụp lại flatlay trên nền trắng có **đổ bóng thật**, rồi cắt bằng công cụ có nhận biết mép | thời gian |
| **C** | **Không cắt.** Giữ mockup nguyên bản trên nền trắng | **0** |

---

## 2. Về hướng "nền tối tôn áo trắng"

Ý đúng — nhưng bộ mockup hiện tại **chống lại nó**.

Mockup không phải ảnh sản phẩm trần. Nó là **template Canva có bố cục sẵn**:
nền trắng + cụm blob mây + wordmark `vitalité®` canh giữa trên đầu.
Blob và wordmark là **một phần của khung**, không phải sản phẩm.
Cắt nền ra khỏi chúng là đánh nhau với chính asset.

**Đề xuất tách hai vùng, không ép một cái:**

| Vùng | Nền | Vì sao |
|---|---|---|
| **Lưới sản phẩm, PDP** | **trắng** | Dùng mockup nguyên bản. Nhất quán, không tốn gì, đúng chuẩn site fashion |
| **Hero · band ngăn · About · intro collection** | **tối + iridescent** | Không có mockup ở đây. Dùng ảnh model, typo, hoặc chỉ nền |

Site vẫn "tối tối" đúng tông IG ở những chỗ kể chuyện, mà lưới sản phẩm vẫn trắng để tôn hàng.
Không cần ảnh trong suốt cho phương án này — **chạy được ngay hôm nay.**

Khi nào có ảnh trong suốt thật thì mở thêm được: sản phẩm nổi trên nền tối ở section feature.
Nhưng đó là bước sau, không phải điều kiện để launch.

---

## 3. Cặp mặt trước / mặt sau — ĐÃ KIỂM, ĐÚNG 8/9

User nhớ đúng: **hai file liền nhau là một cặp trước/sau.** Nhưng có hai ngoại lệ.

| Cặp | Sản phẩm | Trước | Sau | |
|---|---|:--:|:--:|---|
| 1 + 2 | ICONIC Black | `1` | `2` | ✅ |
| 3 + 4 | ICONIC White | `3` | `4` | ✅ |
| 5 + 6 | Pink Graffiti Black | **`6`** | **`5`** | ⚠️ **ngược thứ tự** |
| 7 + 8 | Pink Graffiti White | `7` | `8` | ✅ |
| 9 + 10 | PORSCHE Grey | `9` | `10` | ✅ |
| 11 + 12 | PORSCHE Black | `11` | `12` | ✅ |
| 13 + 14 | THE MOMENTS Hoodie Grey | `13` | `14` | ✅ |
| 15 + 16 | THE MOMENTS Hoodie White | `15` | `16` | ✅ |
| 17 + 18 | — | — | — | ❌ **KHÔNG phải cặp** |

**Ngoại lệ 1 — cặp 5/6 ngược.**
Chữ ký chạy vắt qua hai mặt: mặt trước là `Vrita…` (file `6`), mặt sau là `…lité` (file `5`).
Ghép lại thành `Vitalité`. Cặp trắng 7/8 thì đúng thứ tự.
→ **Nhập tay phải để ý cặp này**, đừng dựa vào quy tắc "lẻ = trước".

**Ngoại lệ 2 — 17 và 18 không liên quan nhau.**
`17` = varsity longsleeve `OLD MONEY` (chỉ có mặt trước).
`18` = **tech pack quần**, không phải mockup sản phẩm.
`19` trống.
→ Ba file cuối **không đưa vào lưới sản phẩm**.

---

## 4. Spec hover đổi mặt trước ↔ mặt sau

WooCommerce **không có sẵn** tính năng này. Nhưng làm bằng ảnh gallery thì không cần plugin.

**Quy ước bắt buộc khi nhập hàng:**

```
Product image      = MẶT TRƯỚC
Gallery ảnh đầu    = MẶT SAU        ← luôn luôn, không đổi thứ tự
Gallery ảnh sau đó = chi tiết, ảnh model
```

Theme đọc `wc_get_gallery_image_ids()[0]` làm ảnh hover. Nếu sản phẩm không có ảnh gallery
thì không hover — không lỗi, chỉ là đứng im.

**Hành vi:**
- Desktop: hover thẻ → mờ dần sang mặt sau, ~250ms
- **Mobile: KHÔNG có hover.** Phải là swipe trong gallery hoặc bỏ hẳn. Không dùng tap để đổi ảnh — nó ăn mất cú tap vào sản phẩm
- Ảnh mặt sau **phải preload lười** — nếu không, hover lần đầu sẽ chớp trắng

**Chi phí:** lưới 12 sản phẩm = 24 ảnh thay vì 12. Sau khi chuyển WebP thì
24 × ~20KB ≈ **480KB**, chấp nhận được. Nhưng ảnh mặt sau phải `loading="lazy"`
và **không** nằm trong LCP candidate.

---

## 5. Việc còn phải làm với ảnh

- [x] Chuyển 18 mockup sang WebP — **5,61MB → 359KB** (`mockup-all/webp/`)
- [ ] Ảnh nền trong suốt — **chặn bởi Canva Pro**, xem mục 1
- [ ] Mockup chỉ `1000×1000` — Woo PDP zoom muốn ≥1600px. Không có bản lớn thì **tắt zoom**
- [ ] `19.png` trống — xoá
- [ ] Ảnh model: 5 file, 4 dọc 1 ngang, đã bị Facebook nén. Dùng tạm, thay sau
