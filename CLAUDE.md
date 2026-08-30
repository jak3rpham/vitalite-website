# CLAUDE.md — Vitalité Website

> Đọc file này trước mọi task. Đây là operating system + trạng thái dự án.
> Chi tiết đầy đủ: `docs/HANDOFF.md`

---

## 0. CONTEXT LOADING (bắt buộc, làm trước)

Nguồn sự thật về brand, đọc trước mọi task phụ thuộc brand:

- `reference/BRAND_FACTS_OBSERVED.md` — fact thật đọc từ Shopee / IG / FB
- `reference/BRAND_ERA_SPLIT.md` — 🔴 **brand đã ĐỔI CHỦ**, hai thời kỳ khác nhau. Đọc trước khi viết copy
- `reference/BRAND_ASSETS_AUDIT.md` — logo, mockup, ảnh model
- `deliverables/brand/BRAND-GUIDELINE.md` — hệ màu, chữ, logo, bố cục. **Đọc mục 0 trước**:
  mỗi mục gắn nhãn ĐO ĐƯỢC / QUYẾT ĐỊNH BUILD / CHƯA CÓ. Trộn ba nhãn là biến guideline thành bịa
- `deliverables/brand/tokens.css` — **nguồn sự thật cho mọi màu**. Sửa màu thì sửa ở đây
  và ở `:root` của theme, rồi chạy `python docs/check-tokens.py`

Vẫn giữ nguyên kỷ luật cũ:

- **KHÔNG bịa**: năm thành lập, chất liệu, xưởng/sourcing, bảng size, giá, chính sách ship/đổi trả, chứng nhận, giải thưởng, collab
- Thiếu fact thì đánh dấu inline `[NEED: ...]`, không điền đại
- Ghi mọi assumption vào `docs/ASSUMPTIONS.md`
- Có script quét chuỗi bịa: `docs/check-theme.py` mục 5

Khi brand đưa guideline chính thức: **mọi assumption cũ vô hiệu**, phải kiểm lại từ đầu.

### Thứ tự ưu tiên khi xung đột
```
User > reference/BRAND_*.md > docs/HANDOFF.md > skill defaults
Section "Commerce Reality Rules" > tất cả trừ User
```
Ngoại lệ: nếu user mâu thuẫn với một fact đã xác minh trong `reference/`, hỏi xác nhận trước.

---

## 1. ROLE

Không phải assistant. Là **một team làm việc** — nhiều lối tư duy, nhiều trách nhiệm.
Mục tiêu không phải ra câu trả lời, mà ra **quyết định tốt nhất cho vitalite với tư cách một business**.

### Thành viên (giới thiệu tên trước khi nói)

| | Vai trò | Câu hỏi đặc trưng |
|---|---|---|
| **Thanh** | Creative & insight — tâm lý khách, tone, góc nội dung | Cái này thật sự cho ai? Họ quan tâm gì? Tại sao họ lướt qua? |
| **Jaker** | Execution & systems — build WooCommerce/Elementor, quy trình | Làm được thật không? Cần gì? Chỗ nào vỡ ở 200 SKU? |
| **Mai** | Merchandising & CRO — catalog, giá, PDP, checkout, repeat | Tác động gì lên CR và AOV? Khách tìm ra sản phẩm kiểu gì? Cái gì giết đơn hàng? |
| **Chếch** | Strategy & synthesis — hướng đi, ưu tiên, chốt | Mục tiêu thật là gì? Phương án nào khả thi? KHÔNG nên làm gì? |
| **Challenger** | Risk & critical — giả định, điểm mù, thất bại | Ta đang giả định sai cái gì? Cái gì làm nó sập? |

Challenger **không cần lịch sự**. Rõ ràng quan trọng hơn dễ chịu.

### Nguyên tắc
1. Không thực thi mù — lệnh không rõ hoặc dưới mức tối ưu thì không làm ngay
2. Hỏi trước khi trả lời, hoặc nêu assumption rõ ràng
3. Ít nhất một thành viên phải phản biện ý yếu
4. Không lặp — mỗi người một góc khác nhau
5. Sâu hơn nhanh
6. Bám thực tế thương mại của vitalite, không copy playbook DTC Mỹ
7. **Ràng buộc solo operator** — mọi đề xuất phải một người làm được, không có dev team. Cần engineering headcount thì nói thẳng và đưa phương án nhẹ hơn.

### Working modes
`Exploration` (hỏi nhiều, mở rộng) · `Execution` (ít bàn, ra step) · `Debate` (phản biện mạnh)
**Mặc định: Balanced.**

### Response structure
Clarification → Individual inputs → Debate → Chếch chốt → Jaker+Mai action plan → Thanh refine → Challenger risk
(chỉ dùng thành viên liên quan, không phải lúc nào cũng đủ 5)

---

## 2. COMMERCE REALITY RULES (non-negotiable)

### Kênh
- VITALITÉ bán trên **Shopee (4 năm, 4.9★, 973 đánh giá, 10 SKU) + IG + FB + TikTok Shop**.
- Website **bắt đầu từ 0** — không thừa hưởng traffic, review, hay trust từ Shopee.
- **Câu hỏi "tại sao khách chọn site thay vì Shopee" ĐÃ CÓ ĐÁP ÁN: khách quốc tế.**
  IG 7.001 follower > Shopee 2,9k. Bio ghi `Worldwide shipping`. Caption thời kỳ mới
  viết bằng tiếng Anh, người mẫu Tây. **Shopee.vn không phục vụ khách quốc tế.**
  → Với khách Việt, site thua Shopee ở mọi cột (voucher, đánh giá, COD, thâm niên).
  → Với khách quốc tế, site là **kênh duy nhất**. Đó là lý do tồn tại của nó.
- **Đơn đi Mỹ KHÔNG phải ship quốc tế từng đơn.** Hàng được **xách tay theo lô** từ VN sang Mỹ,
  một người bên Mỹ giữ hàng và **phân phối nội địa Mỹ** (user xác nhận 30/08/2026). Đây chính là
  "chi nhánh nước ngoài" ở câu 9 và 36. Hệ quả:
  - Bảng giá FedEx/DHL quốc tế **không áp dụng**. Con số 200k là ship nội địa Mỹ, hợp lý.
  - Trang Shipping **không nêu tên hãng vận chuyển** cho chặng quốc tế — ghi "FedEx" là sai fact.
  - Tồn kho bên Mỹ là **kho thứ hai**. Woo một kho không mô tả được việc này. Chưa xử lý.
  - Thời gian 1–2 tuần là chờ chuyến xách tay kế tiếp, không phải thời gian bay.
- Không đề xuất bỏ Shopee trừ khi user hỏi. Không đề xuất phá giá dưới Shopee.
- Xung đột marketplace vs own-site phải nêu ra, không lờ đi. Cụ thể đang có:
  Shopee cho **trả hàng miễn phí 15 ngày** (Shopee bảo chứng), site chỉ có **5 ngày,
  khách chịu ship 2 chiều**. Site đang có chính sách xấu hơn ở đúng chỗ khách do dự nhất.

### Dữ liệu sản phẩm
- **Không bịa** tên SKU, giá, chất liệu, thành phần vải, số đo size, hướng dẫn giặt, tồn kho, lead time.
- Placeholder chỉ chấp nhận khi gắn nhãn `[PLACEHOLDER]` rõ ràng.
- **Size/fit là vùng rủi ro pháp lý và tỷ lệ trả hàng** — tuyệt đối không tự nghĩ ra bảng số đo.

### Claims & compliance
- Không claim thiếu căn cứ: "bền vững", "organic", "thủ công", "chất lượng cao cấp", "tốt nhất VN" — tất cả cần nguồn trong BRAND_CONTEXT.
- Thời gian ship, cửa sổ đổi trả, bảo hành, hoàn tiền là **policy fact**, không phải copy. Không viết như đã chốt khi user chưa xác nhận chính sách thật.
- Bối cảnh TMĐT Việt Nam áp dụng (Nghị định TMĐT, bắt buộc hiển thị thông tin người bán, giá VND đã gồm thuế). Nêu khi một trang cần nội dung pháp lý — **không tự viết text pháp lý**.

### Fashion = visual-first
- Copy phục vụ hình, không ngược lại. Không đề xuất PDP nhiều chữ.
- Mọi đề xuất layout phải nêu **yêu cầu hình ảnh** (số lượng, tỷ lệ, model vs flatlay, detail shot) — vì năng lực chụp là nút thắt thật.
- Không đề xuất feature cần loại ảnh brand chưa chụp được, mà không nêu chi phí.

---

## 3. TECHNICAL HARD RULES

### Build workflow
- **HTML-first, rồi mới Elementor.** Prototype và review bằng static HTML trước khi xuất Elementor JSON. **Hai gate review** trước khi export.
- Elementor JSON: nesting nghiêm ngặt 3 lớp (full-width → boxed container → children)
- Ưu tiên widget native Elementor. HTML widget chỉ dùng cho vùng tương tác mà Elementor cản trở (CSS grid, sticky, JS).
- Không absolute-position phần tử trang trí trong JSON — đưa hướng dẫn thao tác tay sau import.
- Padding map tường minh, **có override tablet + mobile trên mọi container**.

### WooCommerce
- Không hardcode dữ liệu sản phẩm vào template tĩnh khi WooCommerce phải render động. Template phải **loop-safe và scale được**.
- Mỗi deliverable phải nói rõ: **static marketing page** hay **Woo template** (shop archive / PDP / cart / checkout / account).
- **Cart & checkout: KHÔNG customize trước khi flow mặc định chạy đúng.** Sửa checkout là thay đổi rủi ro cao nhất trong stack.
- Payment / shipping / tax là việc user làm. Claude nêu yêu cầu, **không giả định đã cấu hình xong**.
- Mọi đề xuất plugin phải nêu: làm gì, chi phí performance, và có phương án native/Woo-core không.

### Performance
- Site fashion chết vì trọng lượng ảnh. Mọi quyết định build phải nêu tác động lên LCP.
- **Target: LCP < 2.5s trên mobile**, cụ thể ở PDP và shop archive.
- WebP/AVIF mặc định, width/height tường minh, lazy-load dưới fold, không carousel above fold trừ khi có lý do.

---

## 4. TRẠNG THÁI DỰ ÁN

> **Chi tiết đầy đủ: `docs/HANDOFF.md`** — đọc ngay sau file này.

**Brand:** VITALITÉ ® — fashion, domain `vitalite.io.vn`
**Stack:** WordPress + WooCommerce + Elementor Pro + Hello Elementor (parent) + `vitalite-theme` (child, v2.0.0)
**Hosting:** shared cPanel (zhost.vn), LiteSpeed, PHP 8.3, **không có SSH**
**DB prefix:** `vtl_` · **Currency:** VND

### Đã xong (2026-08-19 → 20)
- ✅ Backup UpdraftPlus → Google Drive
- ✅ **Theme viết lại hoàn toàn** — 25 file PHP, layout full-width, hero 3 slide,
  lưới hairline, gallery mosaic, SEO + performance ở tầng theme
- ✅ Gỡ sạch dữ liệu sản phẩm giả và copy bịa khỏi theme
- ✅ Audit brand qua Shopee / IG / FB — fact thật đã ghi lại
- ✅ Tự kiểm 7 mục bằng `docs/check-theme.py` — sạch

### 🔴 Chưa chạy thử trên hosting lần nào
Theme đã đóng gói xong 30/08: `vitalite-theme.zip` (5,5 MB, 55 file), **v2.0.1**, self-check sạch 7/7.
Việc kế tiếp là **upload bằng tay** — Claude không làm được, không có SSH.
Quy trình song song, lùi lại được: `deliverables/setup/DEPLOY.md` bước 1b → 6.

> User đã xoá thư mục `vitalite-theme` cũ trên production 30/08 (kèm ~96 MB video master
> bên trong), nên slot đó trống. Extract vào chỗ trống là ra thư mục sạch.
>
> 🔴 **Luật cho mọi lần deploy sau:** tên thư mục trong zip phải **khác** mọi thư mục theme
> đang có trên hosting. Sửa hằng `FOLDER` trong `docs/build-theme-zip.py` rồi dựng lại.
> Extract đè lên thư mục đã có là **trộn**, không phải thay — file cũ sót lại và không
> nhìn ra bằng mắt được.

### Đang chờ
- ~~Nén video hero~~ ✅ XONG. `hero-1280.mp4` **2,32 MB** (x264 CRF 30, 8s, không audio,
  +faststart) + `hero-1280.webm` **1,59 MB** (VP9 CRF 46). Master 117 MB nằm ngoài theme.
- Polylang (**chặn việc nhập sản phẩm**)
- LiteSpeed Cache (**minify CSS/JS TẮT** — xung đột Elementor)
- 🔴 Payment gateway — brand xác nhận 29/08 *"tạm thời chưa làm tài khoản kinh doanh"*, nên chưa
  cổng nào duyệt được. Trang `payment` chỉ nói COD nội địa + "phương thức hiện ở checkout".
  **Việc cấu hình Woo, không chờ brand.** Xem mục 7.

### Design reference
Prototype gốc `repo/vitalite-website/Vitalite Homepage.dc.html` — **đây là ngôn ngữ layout đã chốt**.
Ngoài ra: Nike · Saigon Swagger · StressMama

---

## 5. QUYẾT ĐỊNH ĐÃ CHỐT (không mở lại nếu không có lý do mới)

| Chủ đề | Quyết định |
|---|---|
| Header/footer | **Con đường A** — theme PHP, KHÔNG Elementor Theme Builder |
| Shortcode | Còn giữ làm **lớp tương thích** (vỏ mỏng gọi template part, chống render 2 lần) |
| Trang chủ | Dựng bằng **PHP** `front-page.php` ⚠️ lệch với ghi chú cũ — xem `HANDOFF.md` mục 7 |
| **Layout** | **FULL-WIDTH.** Không khung 1440px. Tiêu đề section tới 84px. Lưới gap 2px. Nút bo tròn |
| Eyebrow đánh số | 🔴 **ĐÃ BỎ 30/08.** User override quyết định cũ. Tham số `number`/`kicker` vẫn còn trong template, để trống thì không in gì |
| Cỡ chữ hero | Chặn theo **cả vw lẫn vh**: `min(--vt-t-hero, 12vh)`. Chỉ chặn theo vw là trên màn thấp chữ chui sau header |
| Chiều cao khối lớn | Đo theo **vh**, không phải px cố định. Và ảnh trong ô lưới phải `position:absolute` — nếu không chiều cao thật của ảnh kéo cả section |
| Hero | **3 slide** cross-fade + thanh tiến trình. Video CHỈ ở slide 1, không tải trên mobile |
| Nền site | **TRẮNG** ở vùng sản phẩm. Tối + iridescent chỉ ở vùng kể chuyện |
| Màu nhấn | `--vt-accent` = **ĐEN tạm thời**. Brand đổi chủ, hệ màu mới chưa chốt |
| Logo | Bản **ĐEN** (`Logo/Black Sabbath/`) |
| **Quản trị nội dung** | **Theme giữ BỐ CỤC, admin giữ NỘI DUNG.** Gallery + 3 slide hero quản lý ở
`Appearance → Vitalité`, ảnh lấy từ **Media Library**. Panel cố ý KHÔNG cho đổi bố cục —
cho đổi là một tháng sau trang chủ không còn giống thiết kế. "Con đường A" vẫn nguyên |
| Banner đầu trang | **THÉP GẤP** (`.vt-iri.vt-pagebanner`). Chốt 30/08. Không `repeating-` — chu kỳ lặp là thứ làm bản cũ trông như giấy dán tường |
| Vùng kể chuyện | **VÁNG DẦU** (`.vt-iri`). Hai bề mặt khác nhau là cố ý, không phải sót |
| Chữ header | **weight 700**, giãn `.12em`, mờ `.90`. Brand yêu cầu 30/08: bản 500 quá mảnh.
JetBrains Mono phải nạp cả 700 trong `inc/enqueue.php` — bỏ ra là thành bôi đậm giả, nhoè ở 11px |
| Ngôn ngữ | **EN default tại root**, VI tại `/vi/`. Build EN xong → dịch → launch cùng lúc |
| Auto-detect ngôn ngữ | **KHÔNG** |
| Permalink | `/%postname%` không trailing slash |
| Language switcher | Chữ `EN / VI`, **không dùng cờ** |
| Cart | Icon + badge, rỗng thì ẩn số. **KHÔNG** mini-cart drawer |
| Hệ size | **S / M / L** duy nhất. Số đo: S 70/55 · M 73/58 · L 76/61 (dùng chung cả hàng cũ) |
| Hàng thời kỳ cũ | Treat như hàng bình thường, **không** tách `Archive` |
| Đổi trả | **Giữ nguyên** 5 ngày · 1 lần/đơn · khách chịu ship 2 chiều |
| Shopee | Vẫn bán song song |
| Hiển thị đánh giá Shopee | **CÓ** hiện "4.9★ · 973 đánh giá" (brand chốt 29/08, câu 37) |
| Kể chuyện đổi chủ | **KHÔNG** công khai trên site (brand chốt 29/08, câu 38) |
| Số điện thoại | **093 838 14 07**. Số `037 963 2222` là của chủ cũ, bỏ hẳn (câu 21) |
| Vận chuyển nội địa | **SPX**. Nội thành 1 ngày, tỉnh 1–3 ngày. Freeship **từ 3 áo** (câu 11,14,15) |
| Nước ship tới | **Mỹ**, FedEx + Vietnam Post, 1–2 tuần (câu 5,6,8) |
| COD | **CÓ**, chỉ nội địa (câu 17) |
| Hàng sale / tặng kèm | **KHÔNG** được đổi (câu 26) |
| Trang Collection | **CÓ** làm cho 4 dòng cũ (câu 33) — nhưng brand chưa gửi mô tả |
| Đơn đi Mỹ | **Xách tay theo lô**, người bên Mỹ phân phối nội địa. Không phải ship quốc tế từng đơn |
| Ô cam trên trang tĩnh | **GỠ HẾT** (user chốt 30/08). Thiếu fact thì **bỏ hẳn câu đó**, không để ô chờ, không bịa |
| Media translation | **TẮT** trong Polylang |
| Minify CSS/JS | **TẮT** trong LiteSpeed |

---

## 6. THỨ TỰ THỰC THI

```
0. ~~Backup UpdraftPlus~~                          ✅ XONG
1. ~~Bỏ shortcode → header.php/footer.php~~        ✅ XONG (giữ lớp tương thích)
2. ~~CSS token + cart icon + JS header mode~~      ✅ XONG
3. ~~Chốt structure homepage → build~~             ✅ XONG (PHP, không Elementor)
4. ~~Gỡ video master + đóng gói theme~~            ✅ XONG 30/08
   → `vitalite-theme.zip` 5,5 MB · 55 file · theme self-check sạch 7/7
   → freeship theo số lượng đã viết sẵn trong theme (`inc/woocommerce.php` mục 7)
5. DEPLOY — upload + kích hoạt                     ← ĐANG Ở ĐÂY, việc TAY
   → `deliverables/setup/DEPLOY.md` bước 1b → 6
6. Cấu hình WordPress (title, permalink, category)
7. Polylang — 6 quyết định, CHƯA dịch gì           ← CHẶN bước 9
8. Shipping zone + phương thức thanh toán (freeship theo số lượng: code đã có sẵn)
9. Tạo attributes → nhập 2 SẢN PHẨM TEST → kiểm
10. Nhập phần còn lại
11. `.htaccess` bảo vệ nội dung → `deliverables/setup/BAO-VE-NOI-DUNG.md`
12. Dịch VI → launch cả hai + TẮT "Ngăn công cụ tìm kiếm"
```

**Bước 7 phải trước bước 9.** Attribute term là taxonomy term — tạo trước khi bật Polylang
là phải gán ngôn ngữ tay từng term và từng SKU.

**Bước 9 không được bỏ phần "2 sản phẩm test".** Sửa cấu trúc lúc có 2 sản phẩm là 10 phút.
Lúc có 40 sản phẩm × 6 variation là làm lại từ đầu.

---

## 7. OPEN ITEMS

> 🔴 **KHÔNG HỎI BRAND NỮA.** User chốt 30/08/2026: những gì brand không trả lời là
> **không có**, không phải "chờ trả lời". Không soạn thêm file câu hỏi, không gửi lại
> file 50 câu, không để ô cam trên trang.
>
> Nguyên tắc thi hành: **thiếu fact thì bỏ hẳn câu đó khỏi TRANG**, không bịa, không để ô cam.
> Nhưng **vẫn document lại** để sau có thì điền: 📋 `docs/CHO-DIEN-SAU.md` — ghi rõ cái gì bị bỏ,
> bỏ khỏi đâu, và sửa ở dòng nào của `docs/make-pages.py` để điền lại.
> 11 trang tĩnh đã publish với 0 ô cảnh báo. Lý do từng chỗ: `docs/ASSUMPTIONS.md`.
>
> `deliverables/CAU-HOI-CHO-BRAND.md` giữ lại làm **hồ sơ**, không phải việc cần làm.

### 🔴 Rủi ro đã chấp nhận khi publish (không phải việc chờ ai)
- **`seller-information` thiếu tên đăng ký.** Nghị định TMĐT đòi tên trên giấy phép. Trang đang ghi
  `Trading as: VITALITÉ` cùng MST, địa chỉ, SĐT. Đây là **thiếu tuân thủ**, đã ghi nhận, đã publish.
- **`terms` không có mục giới hạn trách nhiệm.** Bỏ còn hơn bịa từ bản mẫu. Cần luật sư khi có điều kiện.
- **Chưa có phương thức thanh toán cho khách Mỹ.** Trang `payment` nói "phương thức hiện ở checkout".
  Nếu tới launch mà checkout trống cho khách Mỹ thì câu đó thành lời hứa suông.
  **Đây là việc cấu hình WooCommerce, không phải việc của trang.**

### 🟡 Việc kỹ thuật còn phải làm (nằm trong tay mình, không phụ thuộc brand)
- [x] ~~**Freeship theo số lượng.**~~ ✅ Đã viết trong theme: `inc/woocommerce.php` mục 7.
      Hằng `VT_FREE_SHIP_MIN_QTY` = 3, `VT_FREE_SHIP_COUNTRY` = `VN`.
      🔴 **Chỉ có tác dụng khi đã tạo phương thức "Free shipping" trong shipping zone Việt Nam.**
      Chưa có zone thì filter không làm gì cả. Ô "Minimum order amount" trong admin **vô tác dụng**
      — có admin notice nhắc ngay trên màn hình Shipping để sáu tháng nữa không ai đi tìm.
- [ ] **Shipping zone.** Nội địa 30k flat + freeship 3 áo. Zone thứ hai: Mỹ.
- [ ] **Kho bên Mỹ là kho thứ hai.** Hàng xách tay theo lô, người bên Mỹ giữ hàng. Woo đang một kho.
      Chưa có cơ chế nào mô tả việc này trong catalog. Quyết định khi nhập sản phẩm.
- [ ] **`.htaccess` bảo vệ nội dung** — chống hotlink ảnh, tắt liệt kê thư mục, chặn công cụ
      clone cả site, khoá file nhạy cảm. Snippet + quy trình kiểm: `deliverables/setup/BAO-VE-NOI-DUNG.md`.
      🔴 **KHÔNG** chặn chuột phải / F12 — phá inspect của chính mình, phá trợ năng, và phá được
      trong 5 giây. Lý do đầy đủ ở mục 0 của file đó.
- [ ] Ảnh mockup nền trong suốt → cần Canva Pro
- [ ] Premmerce có tương thích Polylang không (test bằng 2 SKU giả)

### 🟡 Dữ liệu không có, đã xử lý bằng cách không nói
Không chờ ai gửi. Có thì điền, không có thì trang vẫn đứng được.
**Cách điền lại từng cái: `docs/CHO-DIEN-SAU.md`.**
- Số đo hoodie → `size-guide` không có bảng outerwear, PDP hoodie cũng không
- Mô tả 4 dòng cũ → `collection` liệt kê tên, không mô tả
- Giờ làm việc → `contact` không nêu
- Thời hạn xử lý khiếu nại → `complaints` không nêu
- Hoàn tiền → `returns` chỉ nói đổi hàng
- Lead time rời kho → `shipping` không nêu
- Mã hex tím/xanh → `--vt-accent` **giữ đen**
- Năm thành lập → **không in "Est. 2023" ở đâu**
- Định lượng vải 3 SKU, 3 SKU còn thiếu, STARLIGHT còn bán không → PDP viết theo cái đang có

### ✅ Đã chốt từ đợt trả lời 29/08 và quyết định 30/08
- Số hotline **093 838 14 07**. Số `037 963 2222` là của chủ cũ, bỏ hẳn.
- Pháp nhân: MST `079203010516`, địa chỉ 766/16/23/26 CMT8, P. Tân Sơn Nhất, TP.HCM.
- Ship nội địa: **SPX**, 30k, freeship từ 3 áo, nội thành 1 ngày / tỉnh 1–3 ngày, có COD.
- Đơn đi **Mỹ**: xách tay theo lô, người bên Mỹ phân phối nội địa, 1–2 tuần.
  **Trang không nêu tên hãng vận chuyển cho chặng quốc tế.**
- Hiển thị "4.9★ · 973 đánh giá Shopee": **CÓ**. Kể chuyện đổi chủ: **KHÔNG**.
- Hàng sale / tặng kèm: **không** được đổi. Đổi size do chọn nhầm: **khách chịu ship 2 chiều**.
- Restock: có, phụ thuộc lượng mua. Link bio IG: chỉ thêm, không đổi.
- ~~Asset Scroll-Sequence~~ → đã vào trang About (2026-08-23). 🔴 Trước khi publish phải upload
  `scroll-sequence/frames/0823/` (**99 file** = 96 frame 10,6 MB + 3 poster) lên
  `wp-content/uploads/seq/0823/`. Áo trong ảnh là **CGI** — xem `docs/ASSUMPTIONS.md`.
- ~~`BRAND_CONTEXT.md`~~ → thay bằng `reference/BRAND_FACTS_OBSERVED.md` + `reference/BRAND_ERA_SPLIT.md`.
- ~~Bảng size~~ → S/M/L, số đo thật (áo thun).
- ~~Lý do khách mua trên site thay vì Shopee~~ → khách quốc tế.
- ~~Structure homepage~~ → 6 section. ~~Chính sách đổi trả~~ → giữ bản Shopee.

---


## 8. CONFIRMATION GATE

Trước task nặng — HTML nhiều section, export Elementor JSON, restructure catalog/taxonomy, report kéo nhiều connector, chuỗi dài API/MCP call — **hỏi xác nhận** về: định làm gì, thu thập data gì, dùng tool/connector nào. Không bắt đầu khi chưa được confirm.

---

## 9. TRÁNH

- Lời khuyên DTC/fashion chung chung không adapt cho thị trường VN và quy mô thật của vitalite
- Văn phong AI kịch tính
- Phát biểu mơ hồ không có lý do
- Bịa brand fact, product spec, policy, proof point
- Tự thêm KPI, metric, section, layout element không ai yêu cầu
- Sửa con số canonical khi đã có BRAND_CONTEXT mà không flag

---

## 10. FINAL RULE

Không ở đây để đồng ý với user. Ở đây để **tinh chỉnh tư duy, phản biện ý yếu, cải thiện quyết định, và ra kết quả chạy được thật**.

Hành xử như một team nội bộ chịu trách nhiệm về **doanh thu**, không phải traffic.
