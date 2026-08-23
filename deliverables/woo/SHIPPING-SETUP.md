# VẬN CHUYỂN — cấu hình WooCommerce

**Cập nhật:** 2026-08-22
**Đã chốt:** phí ship trong nước **tính theo địa chỉ khách điền ở checkout**.
**Chưa có:** ship quốc tế — toàn bộ.

---

## 0. Một câu phải đọc trước khi nhập sản phẩm

> 🔴 **Quyết cách tính ship TRƯỚC khi nhập 40 sản phẩm.**
> Nếu chọn cách B (API hãng vận chuyển) thì **mọi SKU phải có cân nặng**. Nhập xong 40 sản phẩm
> rồi mới phát hiện thiếu cân nặng là mở lại từng sản phẩm một để điền tay.
>
> Đây cùng loại với luật "nhập 2 sản phẩm test rồi dừng" — sửa lúc có 2 là 10 phút,
> lúc có 40 là một buổi chiều.

---

## 1. "Tính theo địa chỉ" — có hai cách làm, khác nhau rất xa

### Cách A — Shipping Zones của WooCommerce *(native, không plugin)*

Chia tỉnh thành vùng, mỗi vùng một mức phí cố định.

```
Zone 1  TP.HCM                    →  [NEED: … ₫]
Zone 2  Các tỉnh miền Nam         →  [NEED: … ₫]
Zone 3  Miền Trung                →  [NEED: … ₫]
Zone 4  Miền Bắc                  →  [NEED: … ₫]
```

| | |
|---|---|
| Cần gì | **Chỉ 4 con số.** Không cần tài khoản hãng, không cần API, không cần cân nặng |
| Checkout | Khách chọn Tỉnh/Thành → phí hiện ra ngay, **không gọi mạng** |
| Rủi ro | Gần như không. Đây là tính năng lõi của WooCommerce |
| Nhược | Phí cố định. Đơn 1 áo và đơn 5 áo trả cùng một mức. Lệch với giá hãng thật |

WooCommerce **có sẵn danh sách tỉnh/thành Việt Nam**, không phải cài thêm gì.

### Cách B — Plugin hãng vận chuyển gọi API lấy giá thật *(GHN · GHTK · Viettel Post)*

Plugin gửi điểm đến + cân nặng sang hãng, hãng trả về phí thật.

| | |
|---|---|
| Cần gì | Tài khoản hãng · API key · **cân nặng cho từng SKU** · **quận/huyện và phường/xã ở checkout** |
| Checkout | Mỗi lần khách đổi địa chỉ là **một lần gọi mạng**. Hãng chậm thì ô phí quay vòng |
| Rủi ro | 🔴 **Cao.** Nó sửa form checkout — thêm ô quận/huyện, phường/xã |
| Ưu | Phí đúng thực tế. Không phải bảo trì bảng giá tay |

#### 🔴 Vì sao cách B rủi ro hơn nó trông

WooCommerce chỉ có **Tỉnh/Thành**. GHN và GHTK cần tối thiểu **Quận/Huyện**, thường cần cả
**Phường/Xã** mới ra được phí. Nghĩa là plugin phải **chèn thêm ô vào form checkout** —
đúng cái chỗ `CLAUDE.md` gọi là thay đổi rủi ro cao nhất trong stack.

Và nếu API hãng chậm hoặc lỗi, khách thấy ô phí ship quay mãi không ra số. Ở bước cuối cùng
trước khi trả tiền. Đó là chỗ mất đơn đắt nhất.

---

## 2. Đề xuất

**Launch bằng cách A. Chuyển sang cách B sau, khi đã có đơn thật.**

Lý do:

1. Cách A cần **4 con số**, cách B cần tài khoản + API + cân nặng 40 SKU + sửa checkout.
   Cái nào chặn launch lâu hơn thì rõ.
2. Chưa có đơn nào thì chưa biết phân bố khách theo vùng. Đặt 4 mức phẳng, chạy một tháng,
   nhìn số liệu thật rồi mới biết cách B có đáng không.
3. Đổi từ A sang B **không phải làm lại gì** — chỉ tắt zone, bật plugin. Ngược lại cũng vậy.
4. Ràng buộc solo operator: cách B thêm một plugin phải theo dõi, một API có thể chết, và
   một form checkout đã bị sửa.

### Nhưng vẫn nhập cân nặng ngay từ đầu

Kể cả chọn cách A, **cứ điền cân nặng cho mọi sản phẩm khi nhập**. Nó miễn phí ở thời điểm
nhập, và là thứ duy nhất chặn đường sang cách B sau này.

Cân nặng ước tính — `[NEED: cân thật một cái áo và một cái hoodie]`:

| | Ước tính |
|---|---|
| Áo thun 250 GSM | ~200–250 g |
| Hoodie 500+ GSM | ~600–800 g |

⚠️ Đây là **ước tính theo GSM, không phải số đo**. Cân thật rồi ghi đè.

---

## 3. Còn thiếu gì

### Trong nước
- `[NEED: hãng vận chuyển]` — GHN / GHTK / Viettel Post / J&T
- `[NEED: phí TP.HCM]`
- `[NEED: phí miền Nam]`
- `[NEED: phí miền Trung]`
- `[NEED: phí miền Bắc]`
- `[NEED: có ngưỡng miễn phí ship không]`
- `[NEED: COD hay trả trước 100%]`
- `[NEED: cân nặng thật của áo thun và hoodie]`

> Cách chia vùng ở trên là **đề xuất**, không phải quyết định. Hãng vận chuyển nào cũng có
> bảng vùng riêng của họ — lấy bảng đó rồi chia zone theo cho khớp, đừng chia theo cảm tính.

### Quốc tế — vẫn trống hoàn toàn
- `[NEED: hãng]`
- `[NEED: ship tới nước nào]`
- `[NEED: phí theo vùng]`
- `[NEED: thời gian]`
- `[NEED: thuế nhập khẩu — DDP hay DDU]`

Đây vẫn là mục chặn lớn nhất của dự án. Website tồn tại để phục vụ khách quốc tế, mà đó là
tệp khách duy nhất chưa có một con số nào.

---

## 4. Khi có số rồi thì làm gì

```
1. WooCommerce → Cài đặt → Vận chuyển → thêm Zone theo bảng vùng của hãng
2. Mỗi zone: thêm phương thức Flat rate → điền phí
3. Nếu có ngưỡng miễn phí ship: thêm Free shipping với điều kiện "Minimum order amount"
4. Đặt thử một đơn tới mỗi zone, kiểm phí hiện đúng
5. Viết trang shipping từ deliverables/pages-html/shipping.html — xoá hết ô cam
```

Bước 4 không được bỏ. Zone cấu hình sai thì không báo lỗi — nó chỉ **im lặng tính sai tiền**.

---

## 5. Liên quan

| | |
|---|---|
| Trang chính sách giao hàng | `deliverables/pages-html/shipping.html` |
| So sánh với 2 đối thủ | `deliverables/content/POLICIES.md` |
| Cấu trúc sản phẩm, attribute | `deliverables/woo/STRUCTURE-SETUP.md` |
| Thứ tự dựng site | `docs/BUILD-ON-WORDPRESS.md` |
