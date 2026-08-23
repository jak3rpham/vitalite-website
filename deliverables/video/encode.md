# VIDEO — nén hero + poster

## Vấn đề

| File hiện tại | Size |
|---|---|
| `260417_VTL_PROMO_02.mp4` | **63 MB** |
| `260417_VTL_PROMO_02_optimized.mp4` | **17.8 MB** ← đang dùng cho hero |
| `260418_VTL_CB.mp4` | 33 MB |
| `260418_VTL_CB_optimized.mp4` | 6.2 MB |

17.8MB hero trên shared hosting = không dùng được. Cả 4 file đang trong git → repo phình.

---

## Về câu hỏi "blob: như Nike" — KHÔNG

Nike dùng `blob:` vì họ chạy **adaptive streaming (HLS/DASH qua MSE)**. Player JS fetch segment, feed vào `SourceBuffer`, browser tạo blob URL nội bộ. `blob:` là **hệ quả**, không phải kỹ thuật.

| | MP4 tĩnh | blob: / MSE |
|---|---|---|
| Preload | ✅ `<link rel=preload>` | ❌ phải chờ JS |
| LCP | Sớm | Muộn — JS parse → fetch manifest → fetch segment |
| Range request | ✅ browser tự lo | Player tự implement |
| JS thêm | 0 | ~150KB (hls.js) |
| Setup | Upload file | Encode multi-bitrate + segment + manifest |

Nike có video dài, nhiều bitrate, CDN riêng, hàng triệu user đa dạng đường mạng.
vitalite có **1 hero ngắn trên shared hosting**. Sau khi nén còn 8s/2MB thì adaptive streaming hoàn toàn vô nghĩa.

---

## Về câu hỏi "chuyển MP4 → WebM" — có, nhưng là bước CUỐI

VP9/WebM nhỏ hơn H.264 ~30–50% cùng chất lượng. Nhưng đang ở 17.8MB → đổi codec chỉ xuống ~10MB. Vẫn không dùng được.

**Thứ tự tối ưu đúng — codec là bước 5, không phải bước 1:**

| # | Bước | Tác động | Lý do |
|---|---|---|---|
| 1 | Cắt duration còn 6–8s loop | **Lớn nhất** | Hero loop không ai xem hết 30s |
| 2 | Bỏ audio track hoàn toàn | ~10–15% | Video `muted` mà vẫn mang audio là lãng phí thuần |
| 3 | Cap 1280×720 | Lớn | Có scrim đen đè + `object-fit: cover` → không ai thấy khác biệt |
| 4 | CRF cao hơn | Vừa | Video nền có motion blur, chịu nén tốt |
| 5 | Thêm WebM VP9 | 30–40% | Sau khi 1–4 xong |

---

## Lệnh

> ✅ **ĐÃ CHẠY 2026-08-21.** ffmpeg 9.0 đã có sẵn trên máy. Kết quả ở cuối file.

```bash
# MP4 baseline (fallback, chạy mọi nơi)
ffmpeg -i 260417_VTL_PROMO_02.mp4 \
  -t 8 -an \
  -vf "scale=1280:-2" \
  -c:v libx264 -crf 30 -preset slow \
  -profile:v main -pix_fmt yuv420p \
  -movflags +faststart \
  hero-1280.mp4

# WebM VP9 (source đầu tiên, browser hiện đại lấy cái này)
ffmpeg -i 260417_VTL_PROMO_02.mp4 \
  -t 8 -an \
  -vf "scale=1280:-2" \
  -c:v libvpx-vp9 -crf 38 -b:v 0 \
  -row-mt 1 -deadline good \
  hero-1280.webm

# Poster WebP
ffmpeg -i 260417_VTL_PROMO_02.mp4 -ss 00:00:01 -frames:v 1 \
  -vf "scale=1920:-2" -c:v libwebp -quality 78 hero-poster.webp
```

`-movflags +faststart` quan trọng: đẩy moov atom lên đầu file để browser play ngay thay vì phải tải hết.

**Target:** MP4 ≤ 2.5MB · WebM ≤ 1.5MB · poster WebP ≤ 120KB
Vượt target → cắt xuống 5s.

---

## Sửa `banner-video.php`

### Bug hiện tại

```php
/* comment trong code nói "LCP ĐẠT 100/100" — SAI */
.vt-hero-poster { background-image: url(...hero-poster.jpg) }
```

CSS `background-image`:
- Không preload tự nhiên được
- Browser chỉ phát hiện **sau khi** parse xong CSS
- Không set được `fetchpriority`

Đây là LCP element của homepage, đang load muộn. File cũng là JPG 163KB.

### Cần đổi

1. Poster từ CSS background → `<img>` thật, `fetchpriority="high"`, `decoding="async"`, có `width`/`height`
2. Thêm `<link rel="preload" as="image" href=".../hero-poster.webp">` trong `<head>` (chỉ trên homepage)
3. Thêm `<source type="video/webm">` **trước** MP4
4. Bỏ `setTimeout(initPerformanceVideo, 200)` — hero đã nằm trong viewport ngay từ đầu, IntersectionObserver + delay chỉ làm chậm video vô nghĩa. Load ngay sau `window.load` hoặc khi `requestIdleCallback`.
5. Cân nhắc: **mobile không load video, chỉ poster.** Người Việt xem điện thoại, 4G, data tính tiền. Kiểm bằng `matchMedia('(max-width: 768px)')` hoặc `navigator.connection.saveData`.

---

## Git — ĐÃ XỬ LÝ (2026-08-19)

Repo là phương tiện chuyển máy, không phải nơi lưu dữ liệu thật (dữ liệu thật: WordPress + cPanel).
Nên nguyên tắc: **master gốc không đi qua git, bản _optimized thì có** — để clone về máy khác vẫn chạy được site.

| File | Track? | Lý do |
|---|---|---|
| `260417_VTL_PROMO_02.mp4` (61MB) | ❌ bỏ | master, không reference ở đâu |
| `260417_VTL_PROMO_02_optimized.mp4` (17MB) | ✅ giữ | **file duy nhất đang được `banner-video.php` dùng** |
| `260418_VTL_CB.mp4` (32MB) | ❌ bỏ | master, không reference |
| `260418_VTL_CB_optimized.mp4` (6MB) | ✅ giữ | banner 2 chưa build, nhưng nhẹ |

`.gitignore` đã thêm ignore-all + negation cho `*_optimized`:

```gitignore
*.mp4
*.webm
!vitalite-theme/vitalite-theme/video/*_optimized.mp4
!vitalite-theme/vitalite-theme/video/*_optimized.webm
```

→ file `hero-1280.webm` sinh ra ở trên sẽ **bị ignore**. Đổi tên thành `hero-1280_optimized.webm`,
hoặc thêm negation riêng khi tới bước đó.

**Master gốc chuyển máy bằng Drive/USB, không qua git.**

### Lệnh còn lại phải chạy tay

Repo chỉ có 1 commit (`e62f01f`, root) và origin đứng đúng SHA đó → amend là đủ, không cần `filter-repo`.
Index đã stage sẵn (bỏ 2 master, giữ .gitignore mới). Chỉ còn:

```bash
git commit --amend --no-edit
git push --force origin main
git reflog expire --expire=now --all
git gc --prune=now
```

Sau `gc`: `.git` từ **121MB → ~25MB**.

---

## Hosting

Nếu video quan trọng với brand: shared hosting bandwidth là giới hạn thật → cân nhắc Cloudflare Stream / Bunny (~$1–5/tháng).


---

## ✅ KẾT QUẢ THẬT — chạy 2026-08-21

### Nguồn
`260417_VTL_PROMO_02.mp4` — 2048×1080, 24fps, **29.17s**, 63.2MB

### File đang ship trong theme
| File | Size | Ghi chú |
|---|---|---|
| `video/hero-1280.mp4` | **2.43MB** | x264 CRF 30, 8s, không audio, `+faststart` |
| `video/hero-1280.webm` | **1.66MB** | VP9 CRF 46 |
| `assets/hero-poster.webp` | 38KB | đã có sẵn, dưới target 120KB — không encode lại |

### 🔴 WebM CRF 38 trong lệnh gốc là SAI — nó LỚN HƠN MP4
Chạy đúng lệnh ghi ở trên ra **2.88MB**, trong khi MP4 chỉ 2.43MB.
`<source webm>` đứng trước `<source mp4>` nên trình duyệt hiện đại sẽ tải **file nặng hơn**.
Đúng bằng ngược lại mục đích thêm WebM.

Đã dò lại và đo SSIM so với chính bản MP4 đang ship:

| VP9 CRF | Size | SSIM | |
|---|---|---|---|
| 38 (lệnh gốc) | 2.88MB | — | ❌ lớn hơn MP4 |
| 44 | 1.92MB | 0.9629 | |
| **46** | **1.66MB** | **0.9597** | ✅ **đang dùng** |
| 50 | 1.26MB | 0.9534 | đạt target 1.5MB nhưng nén sâu hơn cần thiết |

**Vì sao chọn 46 mà không phải 50 dù doc đặt target ≤1.5MB:**
Video này **tải sau `window.load` và KHÔNG tải trên mobile** → nó không nằm trên
đường LCP. 400KB chênh lệch là dòng băng thông, không phải dòng tốc độ.
Với brand thời trang thì chất lượng hình đáng giá hơn 400KB. SSIM 0.96 so với
0.953 — giữ phần nhìn.

### Lệnh đã chạy
```bash
# MP4 — 2.43MB
ffmpeg -y -i 260417_VTL_PROMO_02.mp4 -t 8 -an -vf "scale=1280:-2"   -c:v libx264 -crf 30 -preset slow -profile:v main -pix_fmt yuv420p   -movflags +faststart video/hero-1280.mp4

# WebM — 1.66MB  (CRF 46, KHÔNG phải 38)
ffmpeg -y -i 260417_VTL_PROMO_02.mp4 -t 8 -an -vf "scale=1280:-2"   -c:v libvpx-vp9 -crf 46 -b:v 0 -row-mt 1 -deadline good video/hero-1280.webm
```

### Dọn thư mục theme
| Chuyển ra `repo/vitalite-website/_not-in-theme/` | Size |
|---|---|
| `video-masters/260417_VTL_PROMO_02.mp4` | 63.2MB |
| `video-masters/260418_VTL_CB.mp4` | 33.2MB |
| `video-masters/260418_VTL_CB_optimized.mp4` | 6.2MB — **không được reference ở đâu** |
| `video-masters/260417_VTL_PROMO_02_optimized.mp4` | 17.8MB — bản cũ, đã thay bằng hero-1280 |
| `product-images-unused/*.png` (17 file) | 5.4MB — **không được reference ở đâu** |

**CHUYỂN chứ không XOÁ.** Muốn lấy lại thì `mv` ngược lại.

### 🔴 Kích thước theme: 122MB → **5.7MB**
Giờ nén zip upload qua cPanel File Manager là chuyện vài giây.

### `.gitignore` đã sửa
Luật whitelist cũ là `!.../video/*_optimized.mp4`. File mới tên `hero-1280.mp4`
**không khớp** → sẽ bị git nuốt mất, clone về máy khác là mất video.
Đã thêm `!.../video/hero-*.mp4` và `hero-*.webm`, cộng `_not-in-theme/`.
Đã kiểm bằng `git check-ignore`: master **IGNORED**, hai file hero **tracked**.
