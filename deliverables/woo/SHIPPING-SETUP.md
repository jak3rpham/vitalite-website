# VẬN CHUYỂN — cấu hình WooCommerce

**Cập nhật:** 2026-09-01 · **Thay thế hoàn toàn** bản 22/08
**Trạng thái:** đây là **bước D** trong `docs/HANDOFF.md` — việc đang **chặn nhập sản phẩm**.

> 🔴 Bản 22/08 của file này đề xuất **4 zone chia theo miền** và để trống 8 ô `[NEED:]`.
> Cả hai đều đã hết hiệu lực: brand trả lời 29/08 là **một mức 30.000₫ toàn quốc**, và
> `CLAUDE.md` mục 5 đã chốt như vậy. Ai còn cầm bản cũ thì bỏ đi.

---

## 0. Vì sao đây là việc chặn

Chưa có shipping zone thì WooCommerce **không tính được phí ở checkout**. Khách bấm vào giỏ
hàng và thấy *"There are no shipping methods available."* Đơn dừng ngay tại đó.

Và nó chặn cả bước nhập sản phẩm: nhập 40 SKU rồi mới phát hiện phải sửa cấu trúc vận chuyển
là mở lại từng sản phẩm. Nhập 2 SKU test **sau khi** zone đã đứng thì kiểm được cả chuỗi
giỏ hàng → phí ship → checkout trong một lượt.

---

## 1. Số liệu — đã chốt, không phải đề xuất

| | |
|---|---|
| Hãng nội địa | **SPX** |
| Phí nội địa | **30.000₫**, một mức, toàn quốc |
| Miễn phí ship | **từ 3 áo trở lên** — theo *số lượng*, không theo tiền |
| Thời gian | Nội thành TP.HCM 1 ngày · tỉnh khác 1–3 ngày |
| COD | **Có**, chỉ nội địa |
| Quốc tế | **Chỉ Hoa Kỳ.** 1–2 tuần. Xách tay theo lô, người bên Mỹ phân phối nội địa |

Nguồn: brand trả lời 29/08 · `CLAUDE.md` mục 5 · `reference/BRAND_FACTS_OBSERVED.md`.

⚠️ Một điểm chưa khớp còn treo: brand trả lời câu 7 là "nội địa 30k" nhưng câu 12/13 lại ghi
"tùy khoảng cách". Trang `shipping` đang publish **30.000₫ toàn quốc**. Nếu thật sự tùy vùng
thì phải sửa **hai chỗ**: câu trong `docs/make-pages.py` và zone ở đây. Xem `docs/CHO-DIEN-SAU.md` A8.

---

## 2. Trước khi tạo zone — kiểm một ô dễ bỏ sót

`WooCommerce → Settings → General`

| Ô | Phải là |
|---|---|
| **Selling location(s)** | *Sell to specific countries* → **Vietnam** + **United States** |
| **Shipping location(s)** | *Ship to specific countries only* → **Vietnam** + **United States** |
| **Default customer location** | *Shop country/region* |

🔴 Không mở Hoa Kỳ ở ô này thì zone Mỹ dựng xong vẫn vô dụng — khách Mỹ không chọn được nước
của họ ở checkout. Đây là chỗ hay mất nửa tiếng đi tìm.

---

## 3. Zone 1 — Việt Nam

`WooCommerce → Settings → Shipping → Add zone`

| Ô | Điền |
|---|---|
| Zone name | `Việt Nam` |
| Zone region(s) | `Vietnam` |

Thêm **hai** phương thức, **theo đúng thứ tự này**:

### 3.1 Free shipping *(thêm TRƯỚC)*

| Ô | Điền |
|---|---|
| Method title | `Miễn phí giao hàng — từ 3 sản phẩm` |
| Free shipping requires… | **N/A** |
| Minimum order amount | *(để trống)* |

🔴 **Ô "Minimum order amount" vô tác dụng ở site này.** Chính sách tính theo **số lượng**,
mà ô của Woo tính theo **tiền**. Điều kiện thật nằm trong theme:
`inc/woocommerce.php` mục 7 — `VT_FREE_SHIP_MIN_QTY = 3`, `VT_FREE_SHIP_COUNTRY = 'VN'`.
Theme có admin notice hiện ngay trên màn hình Shipping nhắc việc này.

Đặt "requires" = **N/A** là đúng: theme quyết định, không phải Woo. Chọn giá trị khác chỉ
làm màn hình admin nói một đằng còn checkout làm một nẻo.

### 3.2 Flat rate *(thêm SAU)*

| Ô | Điền |
|---|---|
| Method title | `SPX — giao tiêu chuẩn` |
| Tax status | `Taxable` |
| Cost | `30000` |

⚠️ Gõ `30000`, **không dấu chấm, không `₫`**. VND không có phần thập phân.

### 3.3 Vì sao thứ tự quan trọng

Đơn từ 3 áo trở lên sẽ hiện **cả hai** phương thức. WooCommerce chọn sẵn cái **đứng đầu
danh sách**. Free shipping đứng trên thì khách mặc định được miễn phí; Flat rate đứng trên
thì khách phải tự bấm chuyển, và người không để ý sẽ trả 30.000₫ cho một đơn lẽ ra miễn phí.

Đó là một khiếu nại thật, xảy ra ở đúng bước cuối cùng trước khi trả tiền. Kéo thả để
**Free shipping nằm trên**.

---

## 4. Zone 2 — Hoa Kỳ

| Ô | Điền |
|---|---|
| Zone name | `United States` |
| Zone region(s) | `United States (US)` |
| Phương thức | Flat rate |
| Method title | `US delivery` |
| Cost | 🔴 **cần chốt — xem dưới** |

### 🔴 Con số cho zone Mỹ — cần user quyết trước khi bấm

Brand trả lời câu 7: **"ngoài nước: 200k"**.

Ngày 29/08 con số này bị gác lại vì so với bảng giá FedEx VN→Mỹ ($40–60) nó thấp gấp 5–8 lần.
**Fact ngày 30/08 lật lại kết luận đó:** đơn đi Mỹ không phải ship quốc tế từng đơn — hàng
**xách tay theo lô**, người bên Mỹ giữ hàng và **phân phối nội địa Mỹ**. Với chặng nội địa Mỹ,
200.000₫ ≈ $8 là **hợp lý**. `CLAUDE.md` mục 2 đã ghi nhận đúng như vậy.

→ Đề xuất: **`200000`**.
→ Nhưng đây là tiền thật chảy ra mỗi đơn, nên **user xác nhận trước khi điền**.

⚠️ Zone Mỹ **không được để trống**. Trang `shipping` đang publish câu *"Shipping is calculated
at checkout and shown before you pay"* cho khách Mỹ. Không có zone thì câu đó thành lời hứa
suông và checkout Mỹ đứng im — đúng cái rủi ro đã ghi ở `HANDOFF.md` mục 5.

⚠️ **Không** bật COD cho zone Mỹ. COD chỉ nội địa.

---

## 5. Kiểm lại — bắt buộc, không được bỏ

Zone cấu hình sai **không báo lỗi**. Nó im lặng tính sai tiền.

Chỉ kiểm được sau khi có **ít nhất 1 sản phẩm** (bước E). Làm ngay trong lượt nhập 2 SKU test.

| # | Làm | Phải thấy |
|---|---|---|
| 1 | Cart, địa chỉ VN, **1 áo** | Phí **30.000₫** |
| 2 | Tăng lên **2 áo** | Vẫn **30.000₫** |
| 3 | Tăng lên **3 áo** | Hiện **Miễn phí giao hàng**, và nó **được chọn sẵn** |
| 4 | Giảm về **2 áo** | Quay lại 30.000₫, không còn dòng miễn phí |
| 5 | Đổi địa chỉ sang **United States** | Hiện `US delivery`, **không** có dòng miễn phí, **không** có COD |
| 6 | Checkout với địa chỉ VN | COD có trong danh sách phương thức thanh toán |

Bước 4 là bước hay bị bỏ nhất, và nó bắt được lỗi ngược chiều — miễn phí ship "dính" lại
trong session sau khi giỏ hàng đã tụt xuống dưới 3 món.

---

## 6. Cân nặng — vẫn phải điền, kể cả khi chưa dùng tới

Cấu hình trên đây **không cần cân nặng**. Nhưng cứ điền cân nặng cho **mọi SKU ngay lúc nhập**.

Nó miễn phí ở thời điểm nhập, và là thứ **duy nhất** chặn đường sang cách tính phí theo API
hãng vận chuyển sau này. Nhập xong 40 SKU rồi mới cần cân nặng là mở lại từng sản phẩm một.

Ước tính theo GSM — `[NEED: cân thật một áo và một hoodie]`:

| | Ước tính |
|---|---|
| Áo thun 250 GSM | ~200–250 g |
| Hoodie 500+ GSM | ~600–800 g |

⚠️ Đây là **ước tính từ định lượng vải, không phải số đo**. Cân thật rồi ghi đè.

---

## 7. Chuyển sang API hãng vận chuyển — để sau, và biết trước cái giá

Không làm bây giờ. Ghi lại để lần sau không phải phân tích lại.

GHN / GHTK / Viettel Post gọi API lấy giá thật, nhưng WooCommerce chỉ có ô **Tỉnh/Thành**,
còn các hãng cần tối thiểu **Quận/Huyện**, thường cả **Phường/Xã**. Nghĩa là plugin phải
**chèn thêm ô vào form checkout** — đúng cái mà `CLAUDE.md` gọi là thay đổi rủi ro cao nhất
trong stack. Và khi API hãng chậm, khách thấy ô phí quay mãi không ra số, ở bước cuối cùng
trước khi trả tiền.

Đổi từ zone sang plugin **không phải làm lại gì** — tắt zone, bật plugin. Ngược lại cũng vậy.
Nên chạy zone một tháng, nhìn đơn thật, rồi mới quyết.

---

## 8. Liên quan

| | |
|---|---|
| Trang chính sách giao hàng | sinh từ `docs/make-pages.py` mục 2 |
| Cái gì bị bỏ khỏi trang, cách điền lại | `docs/CHO-DIEN-SAU.md` A8 |
| Luật freeship trong theme | `inc/woocommerce.php` mục 7 |
| Cấu trúc sản phẩm, attribute | `deliverables/woo/STRUCTURE-SETUP.md` |
| Thứ tự việc | `docs/HANDOFF.md` mục 1 |
