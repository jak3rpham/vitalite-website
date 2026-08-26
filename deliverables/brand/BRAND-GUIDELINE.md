# BRAND GUIDELINE — VITALITÉ ®

**Phiên bản:** 1.0 · **Ngày:** 2026-08-27 · **Phạm vi:** website `vitalite.io.vn`

---

## 0. Cách đọc file này

Đây **không phải** bộ guideline do brand cấp. Brand chưa cấp bộ nào.
Đây là bộ dựng ngược từ ba nguồn: tài sản brand có thật trong repo, quan sát công khai trên
Shopee và Instagram, và những quyết định đã ra trong lúc build site.

Mỗi mục dưới đây gắn một trong ba nhãn. **Đọc nhãn trước khi đọc nội dung.**

| Nhãn | Nghĩa | Ai được đổi |
|---|---|---|
| ✅ **ĐO ĐƯỢC** | Lấy từ file gốc hoặc kênh chính thức của brand. Có nguồn dẫn được | Chỉ brand |
| 🔧 **QUYẾT ĐỊNH BUILD** | Không phải brand đặt ra. Đây là lựa chọn của bản dựng, có lý do, và **đổi được** | Được, nhưng phải đổi ở token |
| 🔴 **CHƯA CÓ** | Đang trống, đang chặn việc gì đó | Chờ brand trả lời |

Trộn ba nhãn này lại là cách bộ guideline biến thành bịa. Đừng trộn.

**Nguồn sự thật kỹ thuật:** `deliverables/brand/tokens.css`.
Guideline giải thích *vì sao*, tokens giữ *giá trị*. Sửa màu thì sửa tokens, không sửa file này.

---
---

# 1. LOGO

## 1.1 Hệ tám asset ✅ ĐO ĐƯỢC

Nguồn: `Logo/Black Sabbath/`, 8 file PNG RGBA, canvas 995×994, **đen tuyền 100%**, nền trong suốt.
Số đo dưới đây là hộp bao phần mực thật, không phải kích thước canvas.

| File | Là gì | Hộp mực | Tỷ lệ | Vai trò |
|---|---|---|---|---|
| `LOGO-17` | Mark hoa bốn cánh | 512×645 | 0,79 | **Symbol chính.** Favicon, app icon, nhãn cổ áo |
| `LOGO-18` | Emblem chữ `e` + bóng nước | 663×654 | 1,01 | Emblem phụ. Dùng hiếm |
| `LOGO-19` | `VITALITÉ ®` hoa in | 697×137 | 5,09 | Wordmark trang trọng |
| `LOGO-20` | `vitalité ®` thường | 617×137 | 4,50 | ⭐ **Wordmark chính.** Đúng bản dùng trên mockup Shopee |
| `LOGO-21` | `vitalité ®` thường, chữ `e` thay bằng emblem | 615×137 | 4,49 | **Lockup chữ ký.** Xem 1.2 |
| `LOGO-22` | `Vitalité` chữ ký nghiêng | 807×287 | 2,81 | Trang trí, in ngực |
| `LOGO-23` | Tag graffiti nét mảnh | 724×337 | 2,15 | Đồ hoạ sản phẩm |
| `LOGO-24` | Tag graffiti nét dày | 724×391 | 1,85 | Đồ hoạ sản phẩm |

## 1.2 LOGO-20 với LOGO-21 khác nhau chỗ nào ✅ ĐO ĐƯỢC

`BRAND_ASSETS_AUDIT.md` để ngỏ câu này. Đã đối chiếu pixel, **47,3% khác nhau**, và khác đúng một chỗ:

> **LOGO-21 thay chữ `e` bằng chính emblem mặt trời lặn có gợn nước của LOGO-18.**

Nên nó không phải bản trùng lặp, mà là **lockup chữ ký**: wordmark có emblem cài vào.

**Đề xuất phân vai:**

- `LOGO-20` cho **giao diện** — header, footer, hoá đơn. Chỗ cần đọc nhanh ở cỡ nhỏ.
- `LOGO-21` cho **thương hiệu** — nhãn sản phẩm, ảnh chia sẻ mạng xã hội, bao bì. Chỗ có chỗ thở.

🔴 **Cần brand xác nhận** cách phân vai này, và xác nhận tên thư mục `Black Sabbath` là tên bộ hay tên đặt tuỳ hứng.

## 1.3 Khoảng thở 🔧 QUYẾT ĐỊNH BUILD

Chiều cao chữ `x` của wordmark là **137px** trên canvas gốc. Lấy đó làm đơn vị:

```
        ┌─────────────────────────────────┐
        │        ↕ 0,5 × chiều cao        │
        │   ┌───────────────────────┐     │
   0,5× │   │   v i t a l i t é ®   │     │ 0,5×
        │   └───────────────────────┘     │
        │        ↕ 0,5 × chiều cao        │
        └─────────────────────────────────┘
```

**Không đặt bất cứ thứ gì trong vùng đó**: chữ, đường kẻ, mép ảnh, mép nút.

Với mark `LOGO-17` thì đơn vị là **chiều rộng một cánh hoa**, tức 512 ÷ 2 = 256px gốc.

## 1.4 Cỡ nhỏ nhất 🔧 QUYẾT ĐỊNH BUILD

| | Nhỏ nhất | Vì sao |
|---|---|---|
| Wordmark `LOGO-20` | **96px rộng** | Dưới mức đó dấu sắc trên `é` và vòng `®` dính vào nhau |
| Mark `LOGO-17` | **24px rộng** | Bốn khối tròn, còn tách được ở cỡ favicon |
| Lockup `LOGO-21` | **140px rộng** | Gợn nước trong chữ `e` là chi tiết mảnh nhất cả bộ |

## 1.5 Cấm ⛔

- Không đổi màu wordmark sang màu khác đen hoặc trắng
- Không thêm bóng đổ, viền, gradient, hiệu ứng
- Không kéo méo, không nghiêng, không uốn cong
- Không xoay, trừ đúng 90° trong bố cục dọc có chủ ý
- Không đặt lên ảnh rối. Cần nền thì đặt lên khối đặc trước
- Không tự gõ lại chữ `vitalité` bằng font khác rồi coi đó là logo
- Không dùng tag graffiti (`23`, `24`) làm logo giao diện. Chúng là **đồ hoạ sản phẩm**

## 1.6 Ba vấn đề kỹ thuật 🔴 CHƯA CÓ

1. **Không có SVG.** Header đang dùng raster 995px. Logo là hình khối phẳng đơn sắc,
   SVG là định dạng đúng: khoảng 2KB thay vì 13KB, sắc nét ở mọi mật độ điểm ảnh.
   Cần file vector gốc. Không có thì vector hoá được `LOGO-20` và `LOGO-17`.
2. **Không có bản trắng.** Đen tuyền không dùng được trên nền tối, mà header có hai chế độ.
   PNG alpha thì `filter: invert(1)` chữa tạm được; SVG thì `fill: currentColor`, sạch hơn nhiều.
3. **Theme mới có 2/8 asset.** Sáu file còn lại chưa vào repo theme.

---
---

# 2. MÀU

## 2.1 Nguyên tắc trước đã

Site này **chủ yếu là đen, trắng và xám**. Đó không phải vì thiếu màu, mà vì:

- Vùng sản phẩm phải để **trắng** để hàng tự nói. Quyết định đã chốt.
- Màu nhấn của thời kỳ mới **chưa có mã**. Đóng đinh vào màu sai còn tệ hơn không có màu.

## 2.2 Thang trung tính ✅ dùng thật, 🔧 giá trị do build đặt

| Token | Hex | Dùng vào | Tương phản trên trắng |
|---|---|---|---|
| `--vt-paper` | `#FFFFFF` | Nền chính: lưới sản phẩm, PDP, trang chính sách | — |
| `--vt-tint` | `#F4F4F4` | Nền phụ, khối nhấn nhẹ | — |
| `--vt-ink` | `#0A0A0A` | Chữ chính, **và nền của mọi vùng tối** | 19,80 ✅ AAA |
| `--vt-ink-soft` | `#16161A` | Nền tối hạng hai, tách lớp trong vùng tối | — |
| `--vt-line` | `#E4E4E6` | Đường kẻ mảnh mặc định | — |
| `--vt-line-strong` | `#C9C9CE` | Viền ô nhập, mép thẻ | — |
| `--vt-muted` | `#6E6E76` | Chữ phụ | 5,05 ✅ AA |
| `--vt-dim` | `#75757F` | Chữ mờ nhất **còn đọc được** | 4,56 ✅ AA |

🔴 **`--vt-dim` vừa bị sửa.** Giá trị cũ `#9A9AA2` chỉ đạt **2,79:1**, trượt cả chuẩn chữ lớn.
Nó đang được dùng cho chú thích và số trang, tức là chữ thật chứ không phải trang trí.

## 2.3 Đảo màu cho vùng tối 🔧

| Token | Giá trị | Tương phản trên `--vt-ink` |
|---|---|---|
| `--vt-on-dark` | `#F2F2F4` | 17,71 ✅ AAA |
| `--vt-on-dark-muted` | `rgba(242,242,244,.68)` | 8,33 ✅ AAA |
| `--vt-on-dark-line` | `rgba(242,242,244,.18)` | đường kẻ, không phải chữ |

Không dùng trắng tinh làm chữ trên nền đen. `#F2F2F4` dịu hơn, giảm chói ở khối tối lớn.

## 2.4 Màu nhấn 🔴 CHƯA CÓ

```
--vt-accent: #0A0A0A     ← ĐEN, và đó là chủ ý
```

Brand đổi chủ. Thời kỳ cũ dùng hồng rose, thời kỳ mới đi xanh dương và tím nhưng **chưa cấp mã**.

Có mã chính thức thì đổi **đúng hai dòng** `--vt-accent` và `--vt-accent-on` trong `tokens.css`.
Cả site đổi theo. Câu **42** trong `CAU-HOI-CHO-BRAND.md`.

⚠️ **Lấy mã từ file gốc**, không lấy từ ảnh chụp. Màu trong ảnh là màu vải qua ánh sáng ngoài trời
cộng thêm nén JPEG, không phải màu spec.

## 2.5 Hồng thời kỳ cũ ✅ ĐO ĐƯỢC

Đo trên vùng in lớn nhất của sáu mockup thật (`BRAND_ASSETS_AUDIT.md` mục 2):

| Mockup | Hex | Hue |
|---|---|---|
| `7.png` | `#CF1D57` | 340° |
| `8.png` | `#C52458` | 341° |
| `6.png` | `#D84361` | 348° |
| `5.png` | `#E24968` | 348° |
| `12.png` | `#C8497C` | 336° |
| `16.png` | `#FD679F` | 338° |

**Hue bám chặt 336-348°. Đây là hồng rose, không phải đỏ.**
Token đại diện: `--vt-archive-pink: #C52458`.

⛔ **Không dùng cho UI.** Nó thuộc về hàng archive. Chỉ dùng khi đang nói về chính dòng sản phẩm cũ.

## 2.6 Váng dầu 🔧 QUAN SÁT, KHÔNG PHẢI SPEC

Bốn màu `--vt-iri-1` đến `--vt-iri-4` quan sát từ ảnh Instagram thời kỳ mới.

⛔ **Chỉ dùng cho mảng nền lớn.** Không dùng cho chữ, không dùng cho UI, không dùng cho bất cứ
thứ gì cần đọc được. Chúng chuyển động và đổi độ sáng liên tục, nên không có tỷ lệ tương phản nào
đảm bảo được.

## 2.7 Màu trạng thái 🔧

Đây là màu **chức năng**, không phải màu thương hiệu. Chúng tồn tại vì người dùng đã quen nghĩa
của chúng ở mọi site khác.

| Token | Hex | Nghĩa | Tương phản |
|---|---|---|---|
| `--vt-sale` | `#C2413A` | Giảm giá, xoá, lỗi | 5,11 ✅ AA |
| `--vt-ok` | `#188479` | Còn hàng, thành công | 4,55 ✅ AA |
| `--vt-yes` | `#166534` | Dấu `+` trong danh sách được phép | 7,13 ✅ AAA |

🔴 **`--vt-ok` vừa bị sửa.** Cũ là `#18857A`, đạt 4,49, **hụt chuẩn AA đúng 0,01**.

## 2.8 Màu công cụ nội bộ ⛔ KHÔNG PHẢI MÀU BRAND

| Token | Hex | Dùng vào |
|---|---|---|
| `--vt-flag` | `#B45309` | Viền ô "chưa có dữ liệu" |
| `--vt-flag-bg` | `#FEF6E7` | Nền ô đó |

Mọi ô cam **phải biến mất trước khi publish**. Chúng cố tình chói mắt.
Trước đây hai màu này hardcode rải rác **42 chỗ** nên không tắt một lần được. Giờ là token.

## 2.9 Tỷ lệ dùng màu 🔧

Cho một trang bất kỳ:

```
trắng + xám nhạt   ~75%     nền, chỗ thở
đen                ~20%     chữ, khối tối kể chuyện, nút
màu trạng thái      ~4%     chỉ khi có trạng thái thật
màu nhấn            ~1%     hiện đang là đen, nên chưa thấy
```

Váng dầu không nằm trong tỷ lệ này. Nó là **sự kiện**, dùng đúng một hoặc hai chỗ mỗi trang.

---
---

# 3. CHỮ

## 3.1 Ba họ 🔧 QUYẾT ĐỊNH BUILD

🔴 **Brand chưa cấp typeface.** Ba font dưới đây là lựa chọn của bản dựng.
Brand có font riêng thì đổi ở `--vt-font-*` trong `tokens.css`.

| Token | Font | Dùng vào |
|---|---|---|
| `--vt-font-display` | **Archivo Expanded** 800 | Tiêu đề, tên sản phẩm, số liệu lớn. Chữ in hoa |
| `--vt-font-primary` | **Archivo** 400/500/600/700 | Chữ chạy, đoạn văn, nhãn |
| `--vt-font-mono` | **JetBrains Mono** 400/500 | Eyebrow, spec, giá, mã đơn, nhãn kỹ thuật |

**Vì sao ba họ chứ không phải hai.** Mono không phải trang trí ở đây, nó mang nghĩa:
mọi thứ *đo được* thì viết bằng mono. Giá, số đo, mã đơn, GSM, ngày. Mắt học được luật đó
sau vài màn hình, và sau đó nó tự phân loại thông tin hộ mình.

## 3.2 Weight nào được tải 🔴 ĐÃ SỬA MỘT LỖI

| Weight | Được tải | Dùng bao nhiêu chỗ |
|---|---|---|
| 400 | ✅ | 2 |
| 500 | ✅ | 75 |
| 600 | ✅ | 86 |
| **700** | ✅ **vừa thêm** | **48** |
| 800 | ✅ | 148 |

🔴 **Weight 700 đang được dùng 48 chỗ nhưng CHƯA BAO GIỜ được tải.** Trình duyệt tự bắt sang
600 hoặc 800, nên những chỗ đó hiển thị sai độ đậm mà không ai biết. Đã thêm `700` vào cả
`inc/enqueue.php` của theme lẫn bản xem trước.

## 3.3 Thang chữ ✅ đang dùng thật

| Token | Giá trị | Dùng vào |
|---|---|---|
| `--vt-t-xs` | `11px` | Eyebrow mono, nhãn nhỏ |
| `--vt-t-sm` | `13px` | Chú thích |
| `--vt-t-base` | `15px` | Chữ giao diện |
| `--vt-t-md` | `17px` | Chữ nhấn |
| `--vt-t-lg` | `clamp(20px, 2.4vw, 26px)` | Tiêu đề phụ |
| `--vt-t-xl` | `clamp(24px, 3vw, 34px)` | Tiêu đề khối |
| `--vt-t-2xl` | `clamp(38px, 5.4vw, 84px)` | **Tiêu đề section. Điểm nhấn chính** |
| `--vt-t-hero` | `clamp(50px, 8.4vw, 152px)` | Hero |

Chữ đoạn văn thì **không** dùng thang này, nó dùng `16px` với `line-height 1.7`.
Thang trên dành cho chữ có vai trò cấu trúc.

## 3.4 Luật dùng chữ

**Tiêu đề display**
- Luôn `text-transform: uppercase`
- `letter-spacing` **âm**: `-.03em` đến `-.04em`. Chữ càng to càng siết chặt
- `line-height` từ `0,94` đến `1,04`
- ⚠️ `line-height` dưới 1 làm dấu tiếng Việt tràn khỏi hộp dòng. **Phải chừa khoảng cách phía trên.**
  Đây là lỗi đã xảy ra thật: dấu sắc của `VITALITÉ` dính vào gạch ngang phía trên

**Eyebrow mono**
- `11px`, `letter-spacing: .18em` đến `.28em`, in hoa
- Có gạch ngang đen bên dưới ở tiêu đề section
- Đánh số: `01 · The name`. **Dùng dấu chấm giữa, không dùng gạch ngang dài**

**Chữ chạy**
- `16px`, `line-height 1.7`, tối đa `68ch`
- Quá `68ch` thì mắt bắt đầu lạc dòng khi xuống hàng

**⛔ Không dùng dấu gạch ngang dài trong nội dung hiển thị.** Đã gỡ sạch 46 chỗ.
Thay bằng dấu chấm, dấu hai chấm, hoặc tách câu.

---
---

# 4. BỐ CỤC

## 4.1 Full-width, và ngoại lệ của nó ✅ ĐÃ CHỐT

Trang **brand** chạy full-width, không có khung 1440px ở giữa. Đây là ngôn ngữ layout của prototype gốc.

**Ngoại lệ:** trang **tài liệu** chặn ở `--vt-max-doc: 1180px`.

| Loại trang | Bề rộng | Vì sao |
|---|---|---|
| Trang chủ, About, shop, PDP | Full-width | Ngôn ngữ brand. Hình chạm hai mép |
| 11 trang chính sách, giỏ, thanh toán, tài khoản | 1180px, canh giữa | Là tài liệu. Độ dài dòng là yếu tố đọc được |

Không chặn thì trên màn 1920, cột nội dung rộng ~1700px trong khi đoạn văn chỉ 68ch (~640px),
bỏ trống cả nghìn pixel bên phải.

## 4.2 Lề và khe

| Token | Giá trị | Dùng vào |
|---|---|---|
| `--vt-gutter` | `clamp(16px, 2.4vw, 32px)` | Lề trong theme |
| `--vt-gutter-page` | `clamp(20px, 5vw, 72px)` | Lề trong các fragment trang |
| `--vt-hair` | `2px` | **Khe giữa các ô** |

`--vt-hair` là chi tiết đặc trưng: các ô đặt cạnh nhau cách nhau `2px`, **nền lộ ra qua khe** tạo
thành đường kẻ. Không dùng `border`. Nhờ vậy không bao giờ có đường kẻ đôi ở chỗ hai ô giáp nhau.

## 4.3 Điểm ngắt

| | Đổi gì |
|---|---|
| `1200px` | Bảng spec trong About tách hai cột |
| `980px` | Checkout xếp một cột |
| `900px` | Lưới hai cột xếp dọc; gallery PDP thành dải cuộn ngang; summary hết dính |
| `820px` | Hero About ngừng tải frame; lưới hai thời kỳ xếp dọc |
| `760px` | **Giỏ hàng đổi từ bảng sang thẻ dọc** |
| `600px` | Ô nhập họ/tên tách thành hai dòng |

## 4.4 Nút

Bo tròn hoàn toàn: `border-radius: 999px`. Không có ngoại lệ.
Nút chính là khối đặc `--vt-ink`, hover thì rỗng ruột. Nút phụ ngược lại.

---
---

# 5. CHUYỂN ĐỘNG 🔧

| Token | Giá trị | Dùng vào |
|---|---|---|
| `--vt-fast` | `.18s` | Hover, đổi trạng thái |
| `--vt-slow` | `.45s` | Chuyển cảnh, hiện dần |
| `--vt-ease` | `cubic-bezier(.22,.61,.36,1)` | Mặc định |

**Ba luật:**

1. **Mọi hiệu ứng phải tự tắt khi bật "giảm chuyển động".** Không có ngoại lệ.
2. **Không bao giờ viết `opacity: 0` vô điều kiện cho nội dung chờ JS hiện ra.**
   Một lỗi JS là cả khối biến mất, không log, không báo, chỉ là trang trống.
   Trạng thái ẩn chỉ được áp dụng khi có class do chính JS gắn.
3. **Chuyển động phải chứng minh được điều chữ chỉ khẳng định.** Chuyển động trang trí thuần
   thì bỏ. Chuỗi frame ở About tồn tại vì vải nặng và vải mỏng nhìn giống hệt nhau khi đứng yên.

---
---

# 6. GIỌNG ✅ RÚT TỪ CHÍNH LỜI BRAND

Bốn câu brand tự viết, đây là toàn bộ dữ liệu về giọng:

> *Finding harmony within chaos*
> *Chasing the lights, but we are the main source*
> *Old things still shine*
> *Heavy in weight. Unmatched in fit.*

**Rút ra được:**

| Có | Không |
|---|---|
| Câu ngắn, dứt điểm | Câu dài nhiều mệnh đề |
| Tương phản làm cấu trúc: hỗn loạn/hài hoà, cũ/sáng, nặng/vừa vặn | Tính từ chồng tính từ |
| Nói thẳng thông số: `500+ GSM`, `S / M / L` | Hình dung từ marketing rỗng |
| Không giải thích chính mình | Kể lể xuất xứ cảm hứng |

**Luật viết:**
- Trích brand thì trích **nguyên văn**. Không sửa `fit` thành `cut`
- Không claim `bền vững`, `organic`, `thủ công`, `cao cấp` khi không có nguồn
- Thông số viết như thông số, không viết thành văn xuôi
- Tiếng Anh là ngôn ngữ mặc định tại root, tiếng Việt ở `/vi/`

---
---

# 7. ẢNH ✅ + 🔴

## 7.1 Đang có gì

| Nguồn | Số lượng | Tình trạng |
|---|---|---|
| `mockup-all/` | 18 file 1000×1000 | Mockup Canva: nền trắng, cụm blob, wordmark in sẵn ở đầu ảnh |
| `model/` | 5 file | Ảnh model |
| `scroll-sequence/frames/0823/` | 96 frame 2560px | **Ảnh CGI**, không phải ảnh chụp |

## 7.2 Luật

- **Vùng sản phẩm để nền trắng**, dùng mockup nguyên bản. Cắt nền chỉ được nửa catalog,
  nửa còn lại hỏng, và lưới mất đồng nhất
- **Vùng kể chuyện** dùng nền tối và váng dầu. Hero, band ngăn, About
- ⛔ **Không bật zoom.** Mockup chỉ 1000px, Woo zoom cần từ 1600px
- 🔴 **Đọc bảng mockup trong `BRAND_ASSETS_AUDIT.md` trước khi gán ảnh cho SKU.**
  Mockup 17 là `OLD MONEY` chưa ra mắt, 18 là tech pack quần chưa sản xuất.
  Gán nhầm là khách nhận về thứ khác với thứ đã xem. Lỗi này đã xảy ra một lần

## 7.3 Ảnh cần chụp 🔴 CHƯA CÓ

Đây là nút thắt thật của cả site, không phải chi tiết:

| Cần | Bao nhiêu | Dùng ở |
|---|---|---|
| Ảnh mặc trên người | 2-3 mỗi SKU | PDP, lưới sản phẩm |
| Flatlay | 1 mỗi SKU | PDP |
| Ảnh chi tiết: đường may, gấu, cổ | 1-2 mỗi SKU | PDP, chứng minh chất lượng |
| Ảnh ≥1600px | mọi SKU | Điều kiện để bật zoom |

Tỷ lệ khuyến nghị **4:5 dọc**. Hiện tại mọi thứ là 1:1 vì mockup là 1:1.

---
---

# 8. TIẾP CẬN ĐƯỢC

Đo bằng công thức WCAG, không phải ước lượng.

| Cặp màu | Tỷ lệ | Chữ thường | Chữ ≥24px |
|---|---|---|---|
| ink trên paper | 19,80 | AAA | AAA |
| ink trên tint | 18,00 | AAA | AAA |
| on-dark trên ink | 17,71 | AAA | AAA |
| on-dark-muted trên ink | 8,33 | AAA | AAA |
| yes trên paper | 7,13 | AAA | AAA |
| archive-pink trên paper | 5,57 | AA | AAA |
| sale trên paper | 5,11 | AA | AAA |
| muted trên paper | 5,05 | AA | AAA |
| flag trên flag-bg | 4,67 | AA | AAA |
| **dim trên paper** | **4,56** | AA | AAA |
| **ok trên paper** | **4,55** | AA | AAA |

**Hai token vừa sửa để đạt chuẩn:**

| Token | Cũ | Tỷ lệ cũ | Mới | Tỷ lệ mới |
|---|---|---|---|---|
| `--vt-dim` | `#9A9AA2` | **2,79 trượt cả chuẩn chữ lớn** | `#75757F` | 4,56 ✅ |
| `--vt-ok` | `#18857A` | **4,49 hụt AA đúng 0,01** | `#188479` | 4,55 ✅ |

**Luật khác:**
- `--vt-line-strong` chỉ đạt 1,65 trên trắng. Nó là **đường kẻ**, không phải chữ. Không bao giờ dùng làm màu chữ
- Focus phải nhìn thấy được: `outline: 2px solid` màu mực, `outline-offset` từ 2 đến 3px
- Ảnh trang trí để `alt=""`, không viết mô tả rác
- Ảnh sản phẩm phải có `alt` nói **đúng sản phẩm nào, màu gì, chụp mặt nào**

---
---

# 9. ÁP DỤNG: trang nào dùng gì

| Trang | Bề rộng | Nền | Display | Đặc trưng |
|---|---|---|---|---|
| Trang chủ | Full | Trắng + khối tối | `--vt-t-hero` | Hero 3 slide |
| About | Full | Tối mở đầu, trắng giữa, tối đóng | `--vt-t-hero` | Hero chuỗi frame, marquee, váng dầu đóng trang |
| Shop archive | Full | Trắng | `--vt-t-2xl` | Banner váng dầu, lưới khe 2px |
| PDP | Full | Trắng | `--vt-t-xl` | Gallery hai tầng, summary dính, thanh mua dính đáy trên mobile |
| Collections | 1180 | Trắng | `--vt-t-xl` | Lưới hai thời kỳ |
| 10 trang chính sách | 1180 | Trắng | `--vt-t-lg` | Mục lục dính trái |
| Giỏ, thanh toán, tài khoản | 1180 | Trắng | `--vt-t-xl` | Chỉ CSS, không đè template |

---
---

# 10. CÒN THIẾU 🔴

Xếp theo mức độ chặn:

| | Cần gì | Chặn gì | Câu hỏi |
|---|---|---|---|
| 1 | **Mã hex tím và xanh dương**, lấy từ file gốc | `--vt-accent` đang là đen, cả site không có màu | **42** |
| 2 | **File vector logo** (.ai hoặc .svg) | Header mờ trên màn 2x/3x | — |
| 3 | **Bản logo trắng** | Header chế độ tối phải dùng `invert()` | — |
| 4 | **Ảnh chụp sản phẩm thật ≥1600px** | Không bật được zoom, PDP dùng mockup có wordmark lặp | — |
| 5 | Xác nhận phân vai `LOGO-20` với `LOGO-21` | Chưa biết dùng bản nào ở đâu | — |
| 6 | Xác nhận `Black Sabbath` là tên bộ hay tên tuỳ hứng | Đặt tên file trong theme | — |
| 7 | Brand có typeface riêng không | Đang dùng Archivo, là lựa chọn của bản dựng | — |

Bốn mục đầu là thứ thật sự thay đổi diện mạo site. Ba mục sau là dọn dẹp.

---

*Giá trị kỹ thuật: `deliverables/brand/tokens.css`. Sửa màu thì sửa ở đó, file này chỉ giải thích vì sao.*
*Bảng xem màu và chữ trực quan: `deliverables/brand/guideline.html`.*
