# CHỜ ĐIỀN SAU

**Soạn:** 2026-08-30 · **Trạng thái:** 11 trang tĩnh đã publish, không còn ô cam nào

Ngày 30/08 chốt: **thiếu fact thì bỏ hẳn câu đó khỏi trang**, không để chỗ chờ trên mặt site.
File này là chỗ ghi lại **cái gì đã bị bỏ, bỏ khỏi đâu, và điền lại thế nào khi có thông tin**.

> Đây là file **nội bộ**. Không có gì trong đây xuất hiện trên site.
> Trang không bao giờ để lộ rằng có chỗ đang thiếu.

## Cách dùng

1. Có thông tin mới → tìm mục tương ứng dưới đây
2. Sửa **`docs/make-pages.py`** (không sửa file `.html` — nó là kết quả sinh ra)
3. Chạy `python docs/make-pages.py`
4. Đánh dấu ✅ vào mục đó trong file này, ghi ngày

---

## A. Trang chính sách

### A1. `returns` — mục Refunds *(đã bỏ toàn bộ mục)*

**Thiếu:** có hoàn tiền không · nếu có thì bao nhiêu ngày làm việc · hoàn về kênh nào
**Hiện tại:** trang chỉ nói **đổi hàng**, không hứa hoàn tiền ở đâu cả. Không mâu thuẫn, chỉ là im lặng.
**Điền lại:** thêm một tuple `('refunds', 'Refunds', ...)` vào `page('returns', ...)`, đặt sau
`shipping-cost` và trước `how`. Mục lục bên trái tự cập nhật.

### A2. `returns` — đổi trả cho đơn đi Mỹ *(đã bỏ 1 dòng trong bảng)*

**Thiếu:** đơn đi Mỹ có đổi trả được không, ai chịu phí
**Hiện tại:** bảng "Who pays return shipping" chỉ có 2 dòng: lỗi của shop, và khách chọn nhầm size.
**Điền lại:** thêm dòng thứ 3 vào `table([...])` trong section `shipping-cost`.
⚠️ Nhớ mô hình xách tay: hàng trả từ Mỹ có thể gửi cho người phân phối bên Mỹ chứ không gửi về VN.
Đó có thể là câu trả lời rẻ hơn nhiều so với gửi ngược quốc tế.

### A3. `returns` — địa chỉ nhận hàng đổi trả *(đã xử lý bằng quy trình, không phải bỏ)*

**Hiện tại:** trang ghi *"We confirm the return address when we approve the request"*.
**Có thể để nguyên vĩnh viễn.** Nếu muốn công khai địa chỉ thì thay câu đó trong section `how`.

### A4. `complaints` — mục How long we take *(đã bỏ toàn bộ mục)*

**Thiếu:** thời hạn phản hồi khiếu nại · thời hạn giải quyết
**Điền lại:** thêm `('times', 'How long we take', ...)` vào `page('complaints', ...)`,
đặt giữa `channel` và `escalate`.
⚠️ Đây là **cam kết thời gian**, không phải copy. Viết ra là khách có quyền bắt thực hiện.

### A5. `complaints` — địa chỉ nhận khiếu nại

**Hiện tại:** đang dùng **địa chỉ đăng ký kinh doanh** (`ADDR` trong `make-pages.py`).
**Nếu địa chỉ khiếu nại khác:** tạo hằng riêng, đừng sửa `ADDR` vì nó còn dùng ở
`seller-information`. Ghi ở `docs/ASSUMPTIONS.md`.

### A6. `contact` — giờ làm việc *(đã bỏ)*

**Thiếu:** giờ làm việc, hoặc cam kết trả lời trong bao lâu
**Điền lại:** thêm một dòng `<div><dt>Hours</dt><dd>...</dd></div>` vào `<dl class="vtp-spec">`
trong section `where`, ngay sau dòng `Phone`.

### A7. `shipping` — mục Order processing *(đã bỏ toàn bộ mục)*

**Thiếu:** bao lâu sau khi đặt thì hàng rời kho · những ngày không gửi hàng (Chủ nhật? Lễ? Tết?)
**Điền lại:** thêm `('processing', 'Order processing', ...)` vào `page('shipping', ...)`,
đặt giữa `international` và `damage`.
⚠️ Với đơn đi Mỹ, "rời kho" còn phụ thuộc chuyến xách tay kế tiếp — hai con số khác nhau.

### A8. `shipping` — phí ship nội địa 30k có phải toàn quốc không

**Hiện tại:** trang ghi **30.000₫**, coi như giá chung toàn quốc.
**Nguồn:** brand trả lời câu 7 là "nội địa 30k", nhưng câu 12/13 lại ghi "tùy khoảng cách".
**Nếu thật sự tùy vùng:** phải đổi câu trong section `vietnam` **và** đổi cấu hình shipping zone
trong WooCommerce. Hai chỗ, sửa cả hai.

### A9. `payment` — mọi phương thức ngoài COD *(đã bỏ mục Card security)*

**Thiếu:** cổng thanh toán · chuyển khoản · thẻ quốc tế
**Hiện tại:** trang nói COD nội địa + *"Every method available to you is shown at checkout"*.
🔴 **Câu đó chỉ đúng nếu checkout thật sự có phương thức cho khách Mỹ.** Nếu tới launch mà
checkout trống với khách Mỹ thì phải sửa câu đó, hoặc sửa checkout.
**Điền lại:** liệt kê phương thức trong section `methods`, và thêm lại
`('security', 'Card security', ...)` **chỉ khi** đã biết tên nhà cung cấp thật.

### A10. `terms` — mục Limitation of liability *(đã bỏ toàn bộ mục)*

**Thiếu:** cần luật sư, không phải cần thông tin từ brand
**Điền lại:** thêm `('liability', 'Limitation of liability', ...)` vào `page('terms', ...)`,
đặt giữa `ip` và `law`.
🔴 **Không viết mục này từ bản mẫu.** Bỏ trống an toàn hơn viết sai.

### A11. `privacy` — thời gian lưu trữ *(đã xử lý bằng phát biểu tuân thủ)*

**Hiện tại:** *"Order records are kept for as long as Vietnamese law requires us to keep them."*
**Có thể để nguyên vĩnh viễn.** Nếu muốn ghi con số cụ thể thì kiểm với kế toán trước —
Luật Kế toán yêu cầu chứng từ tối thiểu 10 năm.

---

## B. Dữ liệu sản phẩm

### B1. `size-guide` — bảng số đo outerwear *(đã bỏ bảng)*

**Thiếu:** số đo `THE MOMENTS BOXY HOODIE` — dài áo, rộng ngực, dài tay, cho S/M/L, đo phẳng, cm
**Hiện tại:** section `outerwear` chỉ nói chất liệu 500+ GSM và mời nhắn tin hỏi size.
**Điền lại:** thêm `table([...])` vào section `outerwear`, theo đúng khuôn của section `tees`.
🔴 **Tuyệt đối không suy ra từ số đo áo thun.** Số đo sai là tỷ lệ trả hàng và rủi ro pháp lý.
**Kéo theo:** PDP hoodie cũng đang không hiện bảng size — sửa cả hai chỗ.

### B2. `collection` — mô tả 4 dòng cũ *(đã bỏ ô chờ, giữ danh sách tên)*

**Thiếu:** một dòng mô tả cho `PINK GRAFFITI` · `PORSCHE` · `STARLIGHT` · `OLD MONEY`
**Hiện tại:** section `archive` liệt kê 4 tên kèm một cụm ngắn (best seller, varsity longsleeve…),
lấy từ `reference/BRAND_ASSETS_AUDIT.md`. Không bịa gì thêm.
**Điền lại:** nâng chúng lên thành khối `<div class="vtp-era">` như `THE ICONIC` / `THE MOMENTS`
ở section `now`, khi có câu của brand.
⚠️ Đây là **tiếng nói thương hiệu**. Claude không viết hộ.

### B3. `STARLIGHT` còn bán không

**Thiếu:** còn bán không, giá bao nhiêu
**Hiện tại:** `collection` ghi *"shown on Instagram, not yet listed on Shopee"* — đúng với
những gì quan sát được, không hứa gì.
**Nếu ngừng bán:** gỡ khỏi danh sách. **Nếu còn bán:** nhập thành SKU thật.

### B4. Định lượng vải 3 SKU

**Thiếu:** gsm và chất liệu của `ICONIC` · `PORSCHE` · `THE MOMENTS`
**Hiện tại:** PDP chỉ ghi spec đã công bố công khai (250 GSM cho áo thun, 500+ GSM outerwear).
**Điền lại:** khi nhập sản phẩm, ở phần mô tả từng SKU. Không sửa `make-pages.py`.

### B5. Ba SKU còn thiếu

Shopee ghi 10 SKU, đếm được 7. Ba cái còn lại chưa biết là gì.
**Không chặn gì** — nhập được cái nào thì nhập cái đó.

---

## C. Thương hiệu

### C1. Mã màu tím / xanh dương thời kỳ mới

**Thiếu:** hex lấy từ file gốc (artwork in lụa hoặc file thiết kế), **không lấy từ ảnh chụp**
**Hiện tại:** `--vt-accent` = **ĐEN**.
**Điền lại:** sửa ở **hai chỗ** — `deliverables/brand/tokens.css` **và** `:root` của theme.
Rồi chạy `python docs/check-tokens.py` để kiểm hai bên khớp nhau.

### C2. Năm thành lập

**Thiếu:** năm thật. Brand ghi 2023; Shopee hiển thị 4 năm hoạt động + 973 đánh giá.
**Hiện tại:** **không in "Est. 2023" ở đâu.** Trang About chỉ dùng "4 năm" và "973 đánh giá"
vì đó là con số quan sát được trên Shopee.
**Điền lại:** chỉ khi biết chắc. Xem `reference/BRAND_ERA_SPLIT.md` — hai con số này thuộc
hai thời kỳ khác nhau.

### C3. Tên đăng ký trên giấy phép

**Thiếu:** tên đầy đủ trên giấy chứng nhận đăng ký hộ kinh doanh
**Hiện tại:** `seller-information` ghi `Trading as: VITALITÉ` cùng MST, địa chỉ, SĐT, email.
🔴 **Đây là thiếu tuân thủ Nghị định TMĐT, không phải thiếu đẹp.** Đã chấp nhận và publish.
**Điền lại:** thêm dòng `<div><dt>Registered name</dt><dd>...</dd></div>` vào đầu
`<dl class="vtp-spec">` trong section `who`.
**Dấu hiệu nhận biết:** MST `079203010516` là 12 số, đầu `079` là mã TP.HCM trên CCCD → dạng
hộ kinh doanh. Tên trên giấy gần như chắc chắn **không phải** "Vitalité".

---

## D. Kỹ thuật — không phụ thuộc ai, tự làm được

- [ ] **Freeship theo số lượng** (từ 3 áo). Woo mặc định chỉ có ngưỡng theo **giá trị đơn** →
      cần snippet. Xem `deliverables/woo/SHIPPING-SETUP.md`.
      ⚠️ Chưa biết có áp dụng cho đơn đi Mỹ không — nếu có thì phải giới hạn theo zone.
- [ ] **Shipping zone.** Nội địa: 30k flat, freeship từ 3 áo. Zone thứ hai: Mỹ.
- [ ] **Phương thức thanh toán ở checkout cho khách Mỹ.** Xem A9 — trang `payment` đang hứa
      "phương thức hiện ở checkout".
- [ ] **Kho bên Mỹ là kho thứ hai.** Hàng xách tay theo lô, người bên Mỹ giữ hàng và phân phối
      nội địa Mỹ. Woo đang một kho. Bán một chiếc đang nằm ở TP.HCM cho khách Mỹ thì phải chờ
      chuyến kế. Chưa có cơ chế nào mô tả việc này. Quyết định khi nhập sản phẩm.
- [ ] **`.htaccess` bảo vệ nội dung.** Xem `deliverables/setup/BAO-VE-NOI-DUNG.md`.
- [ ] Ảnh mockup nền trong suốt → cần Canva Pro
- [ ] Premmerce có tương thích Polylang không (test bằng 2 SKU giả)

---

## E. Đã điền

*(Trống. Ghi vào đây khi điền được cái đầu tiên, kèm ngày.)*
