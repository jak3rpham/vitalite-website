# AUDIT BỘ ASSET BRAND
**Ngày:** 2026-08-19 · **Nguồn:** `Logo/Black Sabbath/` (8) · `mockup-all/` (19) · `model/` (5)
**Phương pháp:** đọc ảnh trực tiếp + đo màu bằng Pillow. Mọi mã hex dưới đây là **đo được**, không phỏng đoán.

---

## 1. Hệ logo — 8 asset, đây là nửa `BRAND_GUIDELINE.md`

| File | Là gì | Vai trò đề xuất |
|---|---|---|
| `LOGO-17` | **Mark hoa 4 cánh** (4 khối tròn) | Symbol chính — favicon, app icon, nhãn cổ áo |
| `LOGO-18` | **Emblem chữ "e" + mặt nước phản chiếu** | Emblem phụ — dùng hiếm, hạn chế web |
| `LOGO-19` | `VITALITÉ ®` **hoa in đậm** | Wordmark trang trọng |
| `LOGO-20` | `vitalité ®` **thường** | ⭐ **Wordmark chính** — đúng bản dùng trên mockup Shopee |
| `LOGO-21` | `vitalité ®` thường, ® khác | Biến thể — cần user chỉ rõ khác nhau chỗ nào |
| `LOGO-22` | `Vitalité` **chữ ký nghiêng** | Trang trí / in ngực |
| `LOGO-23` | **Tag graffiti** nét mảnh | Đồ hoạ sản phẩm |
| `LOGO-24` | **Tag graffiti** nét dày | Đồ hoạ sản phẩm |

Cả 8: `995×994` PNG RGBA, **đen tuyền 100%**, nền trong suốt.

### 🔴 Ba vấn đề kỹ thuật

1. **Không có SVG.** Header logo là raster 995px. Trên màn 2x/3x sẽ mờ hoặc phải tải file nặng vô lý.
   Logo là hình khối phẳng đơn sắc → **SVG là định dạng đúng**, ~2KB thay vì 13KB, sắc nét mọi DPR.
   Cần file vector gốc (.ai/.svg). Nếu không có, vector hoá được `LOGO-20` và `LOGO-17`.
2. **Đen tuyền = không dùng được trên nền tối.** Header có 2 mode (dark hero / light scrolled).
   Cần bản trắng. Với PNG alpha thì `filter: invert(1)` xử lý được, với SVG thì `fill: currentColor` — sạch hơn nhiều.
3. **Repo mới có 2/8.** `vitalite-mark.png` + `vitalite-wordmark.png`. Sáu asset còn lại chưa vào theme.

**Tên folder `Black Sabbath`** — cần user xác nhận đây là tên bộ (all-black variant set) hay chỉ tên thư mục tuỳ hứng.

---

## 2. Màu — brand KHÔNG có đỏ, brand có HỒNG

Đây là phát hiện làm đổi quyết định đã chốt.

Đo hex trên vùng in lớn nhất của từng mockup:

| Mockup | Hex | Hue | S | L |
|---|---|:--:|:--:|:--:|
| `7.png` in trên áo **trắng** | `#CF1D57` | 340° | 75% | 46% |
| `8.png` in trên áo **trắng** | `#C52458` | 341° | 69% | 46% |
| `6.png` in trên áo đen | `#D84361` | 348° | 66% | 55% |
| `5.png` in trên áo đen | `#E24968` | 348° | 73% | 59% |
| `12.png` PORSCHE trên đen | `#C8497C` | 336° | 54% | 54% |
| `16.png` hồng nhạt | `#FD679F` | 338° | 97% | 70% |

**Hue bám rất chặt trong khoảng 336°–348°.** Đó là **hồng crimson / rose**, không phải đỏ.

Đối chiếu placeholder tôi tự chọn trước đây:

```
--vt-badge-red: #E0202A    hue 357°   ← đỏ cứu hoả, cam
đo được từ sản phẩm thật:  hue ~341°  ← hồng rose
```

**Hai màu này không cùng họ.** `#E0202A` sai — không phải sai sắc độ, sai cả hướng.

### Ứng viên đề xuất

```css
--vt-accent: #CA2058;   /* H341 S72% L46% */
```

Lấy trung bình `7.png` và `8.png` — hai bản in trên **áo trắng**, ánh sáng studio đều nhất,
ít nhiễu nhất trong bộ. Hai mẫu này lệch nhau chưa tới 3%.

⚠️ **Vẫn chưa phải mã canonical.** Đây là màu mực in đã qua render mockup, không phải giá trị spec.
Muốn chuẩn phải lấy từ **file vector artwork** hoặc file thiết kế mockup (.ai/.psd/.fig).

### Câu hỏi phải chốt lại

Quyết định cũ ghi: *"cart badge — traditional trắng trên tròn đỏ"*.
Nhưng brand không dùng đỏ ở đâu cả. Ba hướng:

| | Ưu | Nhược |
|---|---|---|
| **A. Badge dùng `#CA2058`** | Là màu duy nhất brand thật sự có | Không phải "đỏ truyền thống" như đã hình dung |
| **B. Badge đỏ riêng, không liên quan brand** | Đỏ = tín hiệu, quen mắt | Thêm một màu thứ 3 vào hệ chỉ có đen/trắng/hồng |
| **C. Badge đen, không màu** | Trung thành tuyệt đối với hệ monochrome | Badge mất chức năng báo hiệu |

**Khuyến nghị: A.** Badge giỏ hàng là điểm màu duy nhất trên toàn header — để nó là màu brand
thì nó vừa báo hiệu vừa xây nhận diện. Thêm màu đỏ thứ 3 chỉ để "cho giống người ta" là lãng phí.

**Màu phụ thấy được:** xanh dương `#0048B0` — chỉ trên **nhãn cổ áo và nhãn sườn**.
Đó là chi tiết may, không phải màu hệ thống. **Không đưa lên web.**

---

## 3. Mockup sản phẩm — hệ đã có sẵn, dùng thẳng được

19 file, tất cả `1000×1000` PNG. Template thống nhất tuyệt đối:
nền trắng · cụm hình mây/blob trắng phía sau · wordmark `vitalité®` canh giữa trên đầu · áo chụp phẳng chính diện.

### Catalog đọc được từ mockup

| # | Sản phẩm | Có trên Shopee? |
|---|---|---|
| 1, 3 | **ICONIC** — script ngực nhỏ · đen / trắng | ✅ |
| 2, 4 | **STARLIGHT** — graffiti hoa xanh, in lưng · đen / trắng | ❌ **chỉ IG** |
| 5, 8 | **"lité" SIGNATURE** — script lớn hồng · đen / trắng | ❌ |
| 6, 7 | **PINK GRAFFITI** — "Vrita" · đen / trắng | ✅ (bán chạy nhất, 2k+) |
| 9, 11 | **Mark hoa ngực nhỏ** · xám / đen | ❌ |
| 10, 12 | **NEED MONEY FOR PORSCHE** · xám / đen | ✅ (tên Shopee: `PORSCHE`) |
| 13–16 | **THE MOMENTS BOXY HOODIE** — lưng in *"IT'S THE ONLY MOMENT THAT MATTERS."* · xám / trắng | ✅ |
| 17 | **Varsity longsleeve "OLD MONEY"** — kem/ngà, bo cổ đen | ❌ **chưa ra mắt** |
| 18 | **Tech pack QUẦN** — chú thích tiếng Việt, nhãn đỏ túi sau | ❌ **chưa sản xuất** |
| 19 | trống (7KB) | — |

**Mai:** Shopee bán 10 SKU. Mockup cho thấy ít nhất **8 dòng sản phẩm**, trong đó
**4 dòng chưa lên Shopee**: `STARLIGHT`, `lité SIGNATURE`, `OLD MONEY`, và **quần**.

→ Trục "catalog độc quyền" trong `BRAND_FACTS_OBSERVED.md` mục 9 **không phải giả thuyết nữa — có hàng thật.**

→ Và nav hiện tại có mục **QUẦN** đang 404. Hoá ra không phải link rác — có dòng quần đang làm.
Nhưng `18.png` mới là **tech pack**, chưa phải sản phẩm. **Chưa được lên site.**

### 🔴 Vấn đề kỹ thuật

| Vấn đề | Hệ quả |
|---|---|
| **1000×1000 là nhỏ** | PDP cần zoom. Woo zoom muốn ≥1600px. 1000px zoom vào là vỡ |
| **PNG cho ảnh chụp** | Sai định dạng. 300–530KB/ảnh. WebP q80 cùng chất lượng còn ~60–90KB |
| **19.png trống** | Xoá hoặc thay |
| Tỉ lệ 1:1 | Hợp grid shop archive. Nhưng **không có ảnh dọc 3:4 cho PDP** — cần chọn một tỉ lệ và giữ nhất quán |

19 file PNG ≈ **6MB**. Chuyển WebP còn ~1.3MB. Bắt buộc làm trước bước 8.

---

## 4. Ảnh model — đây là nút thắt thật

5 file, tên kiểu `769838759_..._n.jpg` → **CDN Facebook/Instagram**. Không phải file gốc máy ảnh.

| Kích thước | Tỉ lệ | Dung lượng |
|---|---|---|
| 1536×2048 ×2 | 3:4 dọc | 403KB · 377KB |
| 1365×2048 | 2:3 dọc | 151KB |
| 1638×2048 | 4:5 dọc | 280KB |
| 2048×1365 | **3:2 ngang** ×1 | 110KB |

**Thanh:** Xem qua thì đây là ảnh đời thường / UGC, không phải campaign dàn dựng.
Ánh sáng tự nhiên, bối cảnh đường phố và quán, tông ấm. **4/5 là người mẫu nữ** — dù toàn bộ SKU
đặt tên "Unisex". Đó là tệp khách thật đang mặc đồ, không phải định vị marketing. Đáng chú ý.

### 🔴 Ba giới hạn cứng

1. **5 ảnh cho 8+ dòng sản phẩm.** Phần lớn SKU **không có ảnh mặc trên người**.
   Chỉ có mockup phẳng. Với thời trang, đó là thiếu hụt nghiêm trọng nhất — khách cần thấy dáng thật.
2. **Chỉ 1 ảnh ngang.** Hero desktop cần 16:9 hoặc rộng hơn. Bốn ảnh dọc còn lại
   crop sang ngang là mất đầu hoặc mất chân. → **Hero desktop hiện chỉ có video làm được**, đúng như đang làm.
3. **Đã bị Facebook nén rồi.** Nén lại lần nữa sẽ thấy rõ artifact. Với ảnh này nên
   **giữ nguyên**, chỉ resize, không tăng nén. Cần file gốc từ máy chụp.

**Ràng buộc thiết kế rút ra:** mọi layout đề xuất từ giờ **không được giả định có ảnh model cho mỗi SKU.**
Grid shop archive phải đẹp với mockup phẳng 1:1. Ảnh model là bonus dùng cho hero và section
lifestyle, không phải ảnh chính của sản phẩm.

---

## 5. Việc rút ra, theo thứ tự

**Làm được ngay, không đụng theme:**
1. Chuyển 19 mockup → WebP (6MB → ~1.3MB)
2. Vector hoá `LOGO-20` + `LOGO-17` → SVG (nếu user không có file gốc)
3. Xoá `19.png`

**Cần user quyết:**
4. Chốt `--vt-accent`: nhận `#CA2058`, hay đưa mã canonical từ file vector?
5. Badge giỏ hàng: phương án A / B / C ở mục 2
6. Mockup 1000px — có bản lớn hơn không? Nếu không, PDP zoom phải tắt
7. `Black Sabbath` là tên bộ hay tên thư mục tuỳ hứng?
8. `STARLIGHT` · `lité SIGNATURE` · `OLD MONEY` · **quần** — cái nào bán được trên site khi launch?

**Chặn bởi năng lực chụp:**
9. Ảnh model cho các dòng còn lại — hoặc chấp nhận thiết kế không phụ thuộc ảnh model
