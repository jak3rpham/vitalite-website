# SCROLL SEQUENCE — spec kỹ thuật

**Tạo:** 2026-08-22 · **Cập nhật:** 2026-08-23
**Trạng thái:** ✅ **ĐÃ TÍCH HỢP VÀO TRANG ABOUT** (2026-08-23).
Bản đang chạy nằm trong `deliverables/pages-html/about.html`, là **HERO của trang** (khối đầu tiên).
`component.html` trong thư mục này giờ là **bản mẫu**, không phải bản đang dùng —
sửa nó không ảnh hưởng gì tới trang About. Sửa thẳng trong `about.html`.

---

## 0. Khối này làm gì

Một section cuộn cao 450vh. Bên trong có một khung dính (`sticky`) chiếm trọn màn hình.
Khách cuộn → chuỗi 96 frame WebP 2560px chạy siêu mượt như video 4K → đồng thời layout chữ bất đối xứng (Asymmetric Editorial) vào và ra theo mốc phần trăm.

Không phải video. Là **ảnh tĩnh vẽ vào `<canvas>` theo vị trí cuộn**, nên khách kiểm soát
hoàn toàn tốc độ, cuộn ngược thì chạy ngược, và không dính mọi rắc rối của thẻ `<video>`
trên iOS (autoplay bị chặn, seek giật, không scrub được).

---

## 1. File trong thư mục này

| File | Là gì |
|---|---|
| `component.html` | **Component hoàn chỉnh (96 frames · 2560px QHD · Asymmetric Layout).** Dán vào Elementor / About page |
| `make-frames.py` | Cắt video → chuỗi WebP + `manifest.json`, hỗ trợ độ phân giải cao & kiểm soát ngân sách |
| `frames/0823/` | **96 frame thật (2560px QHD)** cắt từ video 4K Orbit Showcase của model Vitalité |
| `frames/0823/poster-*.webp` | **Poster hero 960 / 1440 / 1920px** (30 / 50 / 72 KB). Đây là **LCP của trang About**, không phải frame nào cả |
| `frames/demo/` | 32 frame demo cũ |
| `_preview.html` | Mở bằng trình duyệt để xem và test tương tác trực tiếp |
| `0823.mov` | Video gốc 4K master của sequence |

---

## 2. Pipeline asset — thứ tự này quan trọng

```
1. AI sinh ẢNH TĨNH  →  chốt nhân vật, trang phục, ánh sáng, các dáng
2. Chọn 1 ảnh làm KHUNG HÌNH ĐẦU
3. AI image-to-video từ đúng ảnh đó  →  video 3–5 giây
4. make-frames.py  →  30–36 frame WebP
5. Upload  →  đổi data-seq-base trong component
```

### Vì sao phải image-to-video, không phải sinh từng góc riêng

Sinh mỗi góc một lần độc lập thì **nhân vật đổi mặt, đổi form áo, đổi ánh sáng** giữa các
frame. Khi 32 ảnh chạy nối nhau ở tốc độ cuộn, mắt bắt ngay — nó nhấp nháy như ghép ảnh
lỗi, và **không sửa được ở khâu hậu kỳ**.

Image-to-video khoá nhận dạng vào khung hình đầu. Mọi frame sau đó là biến thể liên tục của
đúng một nhân vật. Đây là lý do bước 2 tồn tại.

### Bước 1 — sinh ảnh tĩnh cần gì

Đầu vào có sẵn: **ảnh mặt trước và mặt sau của sản phẩm** (đã có trong `mockup-all/`).

Cần chốt và giữ nguyên xuyên suốt:

| | |
|---|---|
| Nhân vật | Một người duy nhất. Thời kỳ mới dùng người mẫu Tây/lai — xem `reference/BRAND_ERA_SPLIT.md` |
| Ánh sáng | Tối, nắng gắt xiên, contrast cao — đúng hướng ảnh thời kỳ mới |
| Nền | Trơn hoặc tối. Nền rối làm frame nặng gấp đôi khi nén WebP |
| Khung hình | Dọc 3:4. Toàn thân hoặc 3/4 người |
| Chuyển động | **Xoay chậm tại chỗ** hoặc **bước một bước**. Không nhảy, không vung tay |

⚠️ **Chuyển động càng chậm và càng đơn giản thì càng ít frame là đủ.** Nhân vật xoay chậm
360° mượt ở 32 frame. Nhân vật đi bộ cần 48+ và vẫn giật.

### Bước 4 — cắt frame

```bash
cd "E:\Vitalite website"; python deliverables/scroll-sequence/make-frames.py <video> <tên> 32 900
```

Script **lấy mẫu đều trên toàn bộ video**, không cắt theo fps. Video dài bao nhiêu cũng ra
đúng số frame yêu cầu. Nó tự kiểm ngân sách và kêu khi vượt.

---

## 3. Ngân sách — con số cứng

| | Ngưỡng | Vì sao |
|---|---|---|
| Số frame | **30–36**, tối đa 48 | Xoay chậm mượt từ ~30. Nhiều hơn không mượt hơn, chỉ nặng hơn |
| Chiều rộng | **900px** | Vẽ vào canvas `object-fit: cover`, không ai zoom vào soi |
| WebP quality | **70–75** | Dưới 70 lộ nhiễu ở vùng tối, mà ảnh này toàn vùng tối |
| Mỗi frame | **≤ 60 KB** | |
| **Cả chuỗi** | **≤ 1,4 MB** | |

🔴 **Chuỗi `0823/` đang chạy VƯỢT bảng này 7,5 lần** — 96 frame · 2560px · **10,6 MB**,
frame nặng nhất 189 KB. User đã biết và **chốt giữ nguyên** (2026-08-23), ưu tiên chất lượng hình.
Ghi lại ở đây để lần sau không ai tưởng đó là lỗi rồi âm thầm nén lại.
Giảm nhẹ: khối nằm dưới fold, `≤820px` không tải frame nào, nên 10,6 MB **chỉ giáng lên desktop**.
Muốn nén thì `frames/0823/` là bản gốc — nén ra thư mục MỚI, đừng ghi đè.

`make-frames.py` in cảnh báo khi vượt. Vượt thì giảm số frame trước, hạ quality sau.

### Vì sao KHÔNG phải 24fps

24fps × 4 giây = 96 frame → ~3 MB ở 900px. Gấp đôi ngân sách cho **một khối trang trí**.
Số frame ở đây quyết định bởi **độ mượt mắt cần**, không phải bởi chuẩn video.

---

## 4. Hiệu năng — bốn thứ đã xử trong component

**Không phải LCP.** Khối đặt dưới fold. Ảnh tĩnh dùng `loading="lazy"`.

**Chỉ tải frame khi sắp tới nơi.** IntersectionObserver với `rootMargin: 150%`, chỉ gọi
`preload()` khi `isIntersecting`. Đây là điểm quan trọng nhất — "nằm dưới fold" chỉ vô hại
nếu nó không tranh băng thông với thứ nằm trên fold, mà tải ngay từ đầu thì có tranh.

> ⚠️ **Mục này CHƯA xác minh được trên trình duyệt thật.** Môi trường kiểm của Claude chạy tab
> ở chế độ nền, không render khung hình, và IntersectionObserver cho kết quả **mâu thuẫn giữa
> các lần chạy** với cùng một hình học — lần báo không giao, lần báo có giao dù khối cách fold
> gần 4 màn hình. Logic đúng theo cấu trúc, nhưng phải tự kiểm: DevTools → Network → tải trang,
> **không cuộn**, đếm request `.webp`. Phải bằng 1 (chỉ ảnh tĩnh). Đây là mục đầu checklist mục 9.

**Bật canvas khi đủ 25% frame**, không chờ tải hết. Scrub tới frame chưa có thì giữ frame gần
nhất đã có — chậm mạng thì thấy hơi giật, không thấy màn hình trắng.

**Một lần xử lý mỗi khung hình.** Listener `passive`, gom vào `requestAnimationFrame`,
`classList` chỉ chạm khi trạng thái thật sự đổi.

---

## 5. Suy giảm — không mức nào để lại màn hình trống

| Tình huống | Kết quả |
|---|---|
| Không có JS / JS lỗi | Ảnh tĩnh, ba khối chữ **xếp dọc và hiện hết** |
| Màn ≤ 820px | Như trên. **Không tải frame** |
| Bật "giảm chuyển động" | Như trên |
| Bật tiết kiệm dữ liệu | Như trên |
| Có JS, frame đang tải | Ảnh tĩnh cho tới khi đủ 25% |
| Observer im lặng hoàn toàn | Sau 3 giây cứ tải |
| Đầy đủ | Scrub frame + chữ theo mốc |

Cơ chế: trạng thái ẩn của chữ **chỉ áp dụng khi có class `.is-ready`**, mà class đó do chính
JS gắn sau khi đã quyết định chạy. Không có JS → không có class → chữ hiện bình thường.

### 🔴 Bố cục tĩnh trong `component.html` CHƯA BAO GIỜ CHẠY ĐÚNG

Bảng suy giảm ở trên mô tả *"chữ xếp dọc và hiện hết"*. Đo thật thì không phải. Hai lỗi, đã vá
trong `about.html`, **`component.html` bản mẫu vẫn còn** — đừng chép ngược lại:

1. `.vsq-stage` giữ `overflow:hidden` và `.vsq-viewport` giữ `height:100%` → nội dung bị
   **cắt cụt**. Đo ở 375px: khung cao 722px, nội dung cao 1703px. Mất 3/4.
2. Bốn mốc chữ đặt `grid-area:1/1` để chồng lên nhau lúc chạy thật. Cột cha vẫn `display:grid`
   nên ở bố cục tĩnh chúng **vẫn chồng** — 8 khối dùng chung 2 hộp, khách chỉ đọc được mốc cuối.

Vá đúng cần cả bốn dòng: `min-height:0` · `overflow:visible` · `height:auto` trên viewport ·
`display:block` trên **cả hai cột cha**. Thiếu dòng cuối là lỗi 2 vẫn còn nguyên.

Đây là bố cục **mặc định của mọi khách mobile**, không phải trường hợp hiếm.

### Một cái bẫy đã sập một lần, đừng dựng lại

Lưới an toàn cho observer ban đầu viết là `setTimeout(start, 3000)` thẳng tuột. Nó **nổ cho mọi
khách ở lại trang quá 3 giây mà chưa cuộn** — kéo cả chuỗi frame về đúng lúc không ai cần, phá
sạch mục đích lazy-load ở mục 4. Đo được 32 request frame khi khối còn cách fold gần 4 màn hình.

Bản hiện tại tách hai câu hỏi khác nhau:

| Câu hỏi | Trả lời bằng |
|---|---|
| Observer **có sống không**? | Nó đã gọi callback lần nào chưa (`observerAlive`) |
| Khối **sắp vào tầm nhìn chưa**? | `isIntersecting` |

IntersectionObserver luôn gọi callback một lần cho mọi phần tử ngay khung hình đầu, kể cả khi
`isIntersecting = false`. Chỉ cần callback chạy một lần là biết observer sống — và từ đó timeout
không được phép can thiệp nữa.

🔴 Đây là luật quan trọng nhất của file. **Đừng bao giờ viết `opacity: 0` vô điều kiện** cho
nội dung chờ JS hiện ra. Một lỗi JS là cả khối biến mất, không log, không báo, chỉ là trang trống.

---

## 6. Đưa vào WordPress

**Upload frame lên đâu** — chọn một:

| | Đường dẫn | Ưu / nhược |
|---|---|---|
| Thư mục theme | `wp-content/themes/vitalite-theme-2/assets/seq/<tên>/` | Đi theo git, deploy cùng theme. Nhưng phình theme, và mất khi đổi theme |
| Uploads | `wp-content/uploads/seq/<tên>/` | Không phình theme, sống qua mọi lần đổi theme. **Khuyến nghị** |

Rồi đổi trong `component.html`:

```html
data-seq-base="/wp-content/uploads/seq/walk/"
data-seq-count="32"
```

và đường dẫn ảnh tĩnh ở thẻ `<img class="vsq-poster">`.

**Section Elementor** chứa nó: `Content Width: Full Width` · `Padding: 0`.

⚠️ ~~**Đặt dưới fold.**~~ **LUẬT NÀY ĐÃ BỊ USER GHI ĐÈ (2026-08-23).**

Trên trang About, khối này **là khối đầu tiên** — user muốn nó làm banner. Nghĩa là toàn bộ lý lẽ
LCP ở mục 4 (*"không phải LCP, khối nằm dưới fold"*) **không còn áp dụng**. Thay vào đó là hai
hàng rào khác, cả hai đều nằm trong `about.html`:

| | |
|---|---|
| **LCP là poster riêng** | `poster-960/1440/1920.webp` — 30 / 50 / 72 KB, srcset, `eager` + `fetchpriority=high`. **Không** dùng `001.webp` (2560px, 189 KB) |
| **Frame chỉ tải sau `window.load`** | IntersectionObserver hết tác dụng khi khối ở đầu trang: nó báo "thấy rồi" ngay khung hình đầu. Van bây giờ là `load`, có lưới an toàn 8 giây |

Đo trên preview 961px: poster xong **147 ms** · `loadEventEnd` **234 ms** · request frame đầu
**589 ms**. Mobile: **0 request frame**.

Đặt lại khối này xuống dưới fold ở trang khác thì mục 4 lại đúng như cũ.

---

## 7. Đặt ở đâu trong trang About

### 🔴 ĐÃ ĐỔI — khối này giờ là HERO, không phải section 04

**User quyết 2026-08-23:** đưa lên đầu trang làm banner, vì đầu trang cũ *"rất là trống"*.
Thứ tự thật trong `about.html` hiện tại:

```
HERO   chuỗi frame, 4 mốc chữ (H1 + Weight + Fit + Behaviour)
       Marquee
01     The name        02  The comeback     03  Two eras
04     What it is made of                   05  The record
```

Mốc 0 mang **H1 của cả trang**. Ba mốc sau bỏ đánh số, chỉ còn nhãn `Weight / Fit / Behaviour`,
để không đụng hệ đánh số `01–05` của các section bên dưới.

Lập luận đặt-trước-bảng-spec dưới đây **không còn áp dụng cho trang About** (bảng spec giờ ở
section 04, cách hero 3 section). Giữ lại vì nó vẫn đúng nếu mang khối này sang trang khác:

Trang About hiện có 7 khối. Chuỗi frame vào giữa `03 — Two eras` và bảng thông số:

```
        Mở màn            TỐI     "Even in chaos, you are alive."
        Marquee           TỐI     bốn câu của brand chạy ngang
   01   The name          sáng
   02   The comeback      xám
   03   Two eras          xám
→  04   CHUỖI FRAME       TỐI     ← chèn vào đây
   05   What it's made of sáng    bảng 250 GSM / 500+ GSM
   06   The record        TỐI     dải số + CTA
```

Ba lý do, theo thứ tự quan trọng:

**1. Đây là chỗ duy nhất chuyển động CHỨNG MINH được điều mà chữ chỉ khẳng định.**
Câu của brand là *"Heavy in weight. Unmatched in fit."* và *"a structured silhouette that holds
its shape all day"*. Đó là phát biểu về **cách vải hành xử khi cơ thể chuyển động**. Một tấm ảnh
tĩnh không thể chứng minh nó. Vải 500 GSM và vải mỏng nhìn giống hệt nhau khi đứng yên — chúng chỉ
khác nhau lúc xoay: gấu áo có văng ra không, vai có giữ nếp không.

**2. Thấy trước, đọc số sau.** Khách xem vải chuyển động → rồi mới đọc `500+ GSM`. Con số đó
mang nghĩa hơn hẳn khi nó đến sau phần nhìn, thay vì đứng một mình trong bảng.

**3. Nhịp sáng tối.** Hiện tại là `tối · tối · sáng · xám · xám · sáng · tối`. Chèn một khối
tối vào giữa cắt được đoạn `xám → xám → sáng`, và vẫn còn một khối sáng ngăn giữa nó với khối
tối đóng trang. Đặt sát khối đóng trang thì thành một đường hầm tối dài.

### 🔴 Asset là ảnh CGI, không phải ảnh chụp hàng thật

Chuỗi `0823/` là ảnh sinh bằng AI. Cái áo trong đó **chưa được đối chiếu với sản phẩm thật**,
và lưng áo in dòng *"IT'S THE ONLY MOMENT THAT MATTERS"* — dòng này **không có trong bất kỳ
nguồn brand nào đã xác minh**.

Hệ quả thực tế, theo thứ tự nặng dần:

1. Bảng spec đặt cạnh nó **không được nhận nó là ảnh sản phẩm**. Bản trong `about.html` vì thế
   chỉ trích spec **outerwear đã công bố** (500+ GSM cotton blend · Signature Boxy Fit · S/M/L),
   **không gọi tên SKU nào**, và HUD ghi thẳng `CGI visualisation`.
2. Đưa chuỗi này sang **PDP** (mục 7 dưới có gợi ý) thì vấn đề nặng hơn hẳn — ở đó khách đang
   quyết định mua, và một cái áo không tồn tại đặt cạnh nút "Thêm vào giỏ" là chuyện đổi trả.
   **Không mang sang PDP khi chưa có ảnh chụp thật.**

### Chủ thể là CÁI ÁO, không phải người mẫu

Đây là điều chỉnh quan trọng nhất cho brief sinh ảnh ở mục 2.

Khối này tồn tại để chứng minh một luận điểm về **vải**. Nên khung hình phải ưu tiên phom áo,
không phải gương mặt:

| | |
|---|---|
| Khung | 3/4 người hoặc toàn thân. **Không cận mặt** |
| Chuyển động | Xoay chậm tại chỗ, khoảng 180–270° là đủ |
| Phải thấy rõ | **Gấu áo** và **đường vai** — hai chỗ duy nhất cho thấy vải nặng hay nhẹ |
| Tránh | Vung tay, nhảy, đổi biểu cảm. Chúng kéo mắt khỏi cái áo |

Xoay 180° chậm cho ra chuyển động đọc được ở **28–32 frame**, thấp hơn ngưỡng mục 3.

### Chữ trong ba mốc — phải khác chữ ở nơi khác trong trang

Bản mặc định trong `component.html` đang dùng *"Even in chaos, you are alive."* ở mốc 3.
**Câu đó đã nằm ở tiêu đề mở màn của trang About.** Lặp lại trong cùng một trang là làm nó
mòn đi. Khi ráp vào About, đổi mốc 3.

Marquee cũng đã chạy cả bốn câu của brand rồi — nên ba mốc ở đây nên nói về **cái áo**,
không phải khẩu hiệu.

### Một chuỗi, không phải hai

Có thể nghĩ tới việc làm hai chuỗi cho `03 — Two eras`, một cho archive một cho hàng mới.
**Không nên**, vì hai lý do:

- Gấp đôi ngân sách ảnh và gấp đôi thời gian sinh asset
- Hàng archive chỉ có ảnh studio phẳng thời kỳ cũ. Sinh một chuỗi model từ đó là **bịa ra
  hình ảnh brand chưa từng chụp** — đúng thứ `CLAUDE.md` cấm

### 🟡 Câu hỏi mở: About có phải chỗ đáng nhất không

Trang About vốn ít traffic và ít ý định mua. Bỏ 1,4 MB và ba màn cuộn vào một trang phần lớn
khách bỏ qua là một cách phân bổ đáng cân nhắc lại.

Chỗ chuỗi frame sinh ra tiền nhiều hơn: **trang sản phẩm (PDP)** — nơi khách đang phân vân
đúng câu hỏi *"cái áo này lên người trông thế nào"* — hoặc **trang chủ**, nơi có traffic.

Asset thì dùng lại được ở cả ba chỗ, không phải làm lại. Nên đây không phải lý do dừng —
chỉ là: làm xong ở About rồi thì **cân nhắc mang nó sang PDP**, chỗ nó đổi được thành đơn hàng.

---

## 8. Nội dung chữ — lấy từ đâu

Bản **đang chạy trong `about.html`** dùng ba câu này, tất cả nguyên văn của brand:

| Mốc | Câu | Nguồn |
|---|---|---|
| 0–34% | *Heavy in weight.* | Instagram 25/07/2026 |
| 34–67% | *Unmatched in fit.* | Instagram 25/07/2026 |
| 67–100% | *Holds its shape all day.* | Instagram 25/07/2026 — trích từ *"a structured silhouette that holds its shape all day"* |

Mốc 3 **đã đổi** khỏi *"Even in chaos, you are alive."* vì câu đó là **H1 của chính trang About**.
`component.html` bản mẫu vẫn còn câu cũ — đừng chép ngược lại.

Đổi chữ thì đổi luôn `data-from` / `data-to`. Ba mốc chia đều là hợp lý; đừng để khoảng
trống giữa hai mốc, nếu không có đoạn cuộn mà không có chữ nào hiện.

Kho câu còn lại: `reference/BRAND_ERA_SPLIT.md` mục 2. **Không tự nghĩ câu mới.**

---

## 9. Kiểm trước khi nghiệm thu

- [ ] `manifest.json` báo tổng ≤ 1,4 MB và frame nặng nhất ≤ 60 KB
- [ ] Nhân vật **không đổi mặt, không đổi áo** giữa frame đầu và frame cuối
- [ ] Cuộn xuôi mượt, cuộn ngược cũng mượt
- [ ] Cuộn nhanh không giật, không trắng khung
- [ ] Ba khối chữ vào ra đúng mốc, không có đoạn nào trống chữ
- [ ] Thu cửa sổ xuống 800px → thành bố cục tĩnh, **DevTools Network không tải frame nào**
- [ ] Tải trang rồi KHÔNG cuộn xuống → Network **không có request frame nào**
- [ ] Bật "giảm chuyển động" trong OS → bố cục tĩnh
- [ ] Tắt JavaScript → chữ vẫn đọc được đầy đủ
- [ ] Lighthouse mobile: LCP **không** trỏ vào khối này

---

## 10. Xem thử ngay, chưa cần asset

```bash
cd "E:\Vitalite website\deliverables\scroll-sequence"; python -m http.server 8790
```

Mở `http://127.0.0.1:8790/_preview.html`. Frame demo là hình khối chuyển động — đủ để
kiểm cơ chế scrub, mốc chữ, thanh tiến trình và các mức suy giảm.

Thay bằng asset thật thì chỉ đổi `data-seq-base` và `data-seq-count`.
