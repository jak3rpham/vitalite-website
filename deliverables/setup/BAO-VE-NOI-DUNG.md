# BẢO VỆ NỘI DUNG — cái gì làm được, cái gì không

**Soạn:** 2026-08-30 · **Áp dụng:** zhost.vn, LiteSpeed, cPanel, không SSH

---

## 0. Đọc mục này trước, nó tiết kiệm thời gian

### Không thể chặn người xem HTML/CSS/JS. Đừng thử.

Trình duyệt **phải** nhận được HTML, CSS và JS thì mới hiển thị được trang. Khi nó đã nằm trên
máy người ta thì nó là của người ta. Mọi thủ thuật "chặn xem mã nguồn" đều là **chặn người không
có ý định copy**, và không cản được một phút nào người có ý định.

Cụ thể, các cách thường được đề xuất và cách phá chúng:

| Thủ thuật | Phá bằng |
|---|---|
| Chặn chuột phải | `Ctrl+U`, hoặc gõ `view-source:` trước URL |
| Chặn `F12` / `Ctrl+Shift+I` | Menu trình duyệt → More tools → Developer tools |
| Phát hiện devtools mở rồi chuyển trang | Tắt JavaScript, trang vẫn tải |
| Làm rối (obfuscate) JS | Prettier / de-obfuscator, mất 10 giây |
| Chặn `Ctrl+S` | `curl https://vitalite.io.vn > page.html` |

Và cái giá phải trả là thật:

- 🔴 **Chặn chính mình.** Anh nói muốn dùng inspect để xem performance và lỗi. Script chặn devtools
  không phân biệt được anh với người khác.
- 🔴 **Phá trợ năng.** Chặn phím tắt và chuột phải làm hỏng cách dùng của người đọc màn hình và
  người điều khiển bằng bàn phím.
- 🔴 **Chậm trang.** Thêm JS chạy trên mọi lần tải, trong khi mục tiêu đang là **LCP < 2,5s mobile**.
- 🟡 **Rủi ro SEO.** Một số kỹ thuật chặn tự động bị Googlebot đọc thành nội dung khác với người dùng.

### Thứ đáng bảo vệ không phải HTML

Layout copy được, nhưng copy xong vẫn không bán được. Đối thủ lấy nguyên CSS về vẫn không có:
ảnh sản phẩm, 973 đánh giá 4.9★ tích trong 4 năm, 7.001 follower Instagram, và hàng để giao.

Thứ **thật sự** có giá trị và **thật sự** bị lấy được:

1. **Ảnh sản phẩm và ảnh model** — copy về là dùng ngay được để chạy quảng cáo hàng nhái.
2. **96 frame chuỗi CGI** trong `wp-content/uploads/seq/0823/` — 10,6 MB tài sản dựng hình.
3. **Băng thông** — người khác nhúng ảnh của mình vào site họ, mình trả tiền hosting.

### Cái vốn đã an toàn, không cần làm gì

**Toàn bộ code PHP.** Theme `vitalite-theme` 25 file PHP, WooCommerce, mọi thứ trong `wp-content`
đuôi `.php` — server chạy chúng rồi mới gửi kết quả xuống. Trình duyệt **không bao giờ** thấy
mã nguồn PHP. Phần logic thật của site đã kín sẵn.

---

## 1. Việc nên làm — có tác dụng thật

Bốn thứ dưới đây đều đặt ở tầng server, không thêm một dòng JS nào vào trang, không ảnh hưởng LCP.

### 1.1 Chống hotlink ảnh

Chặn site khác nhúng trực tiếp ảnh của mình. Đây là thứ **duy nhất** trong danh sách này thật sự
ngăn được việc lấy dùng, chứ không chỉ làm khó.

### 1.2 Tắt liệt kê thư mục

Không có cái này thì vào `vitalite.io.vn/wp-content/uploads/seq/0823/` là thấy **danh sách 99 file**,
tải hàng loạt trong một lệnh. Có nó thì phải đoán từng tên file.

### 1.3 Chặn công cụ clone nguyên site

HTTrack, WebCopier, Wget và họ hàng tải cả site về trong một lần chạy. Chặn theo user-agent không
phải tường thành, nhưng nó lọc được đúng nhóm "bấm một nút clone cả site" — nhóm đông nhất.

### 1.4 Khoá file nhạy cảm

`wp-config.php`, `.git`, `readme.html`, `xmlrpc.php`. Cái này là bảo mật cơ bản, không liên quan
copy nội dung, nhưng đã sửa `.htaccess` thì làm luôn.

---

## 2. Cách làm

**Không có SSH**, nên làm qua cPanel File Manager.

1. cPanel → **File Manager** → `public_html`
2. Settings (góc trên phải) → tick **Show Hidden Files** → Save
3. Mở `.htaccess` → **Edit**
4. 🔴 **Copy toàn bộ nội dung hiện tại ra một file text trên máy trước khi sửa.**
   `.htaccess` hỏng là site trả lỗi 500, trắng trơn.
5. Dán khối dưới đây vào **TRƯỚC** dòng `# BEGIN WordPress`

> ⚠️ Khối WordPress nằm giữa `# BEGIN WordPress` và `# END WordPress` là **của WordPress quản lý**,
> nó ghi đè khi mình đổi permalink. Đừng đặt gì vào trong đó.

```apache
# ==========================================================
# VITALITÉ — bảo vệ nội dung
# Đặt TRƯỚC khối "# BEGIN WordPress"
# ==========================================================

# ---------- 1. Tắt liệt kê thư mục ----------
# Không có dòng này thì /wp-content/uploads/seq/0823/ hiện ra
# danh sách 99 file, tải hàng loạt được.
Options -Indexes

# ---------- 2. Chống hotlink ảnh ----------
# Chỉ cho phép ảnh hiện trên chính domain của mình, trên Google
# (để ảnh còn lên Google Images), và khi mở trực tiếp (không referer).
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{HTTP_REFERER} !^$
RewriteCond %{HTTP_REFERER} !^https?://(www\.)?vitalite\.io\.vn [NC]
RewriteCond %{HTTP_REFERER} !^https?://(www\.)?google\. [NC]
RewriteCond %{HTTP_REFERER} !^https?://(www\.)?bing\. [NC]
RewriteRule \.(jpe?g|png|webp|avif|gif|svg|mp4|webm)$ - [F,NC,L]
</IfModule>

# ---------- 3. Chặn công cụ clone cả site ----------
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{HTTP_USER_AGENT} (HTTrack|WebCopier|WebZIP|Teleport|SiteSucker|Offline\ Explorer|WebStripper|WebWhacker|wget|curl|Xenu|Screaming\ Frog) [NC]
RewriteRule .* - [F,L]
</IfModule>

# ---------- 4. Khoá file nhạy cảm ----------
<FilesMatch "^(wp-config\.php|readme\.html|license\.txt|xmlrpc\.php|\.htaccess|\.gitignore)$">
  Require all denied
</FilesMatch>

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule ^\.git - [F,L]
RewriteRule ^\.git/ - [F,L]
</IfModule>

# ==========================================================
# HẾT phần VITALITÉ
# ==========================================================
```

### Kiểm sau khi lưu — làm đủ 5 cái, theo thứ tự

| # | Thao tác | Đúng thì thấy |
|---|---|---|
| 1 | Mở `vitalite.io.vn` | Trang chạy bình thường. **Nếu lỗi 500 → dán lại file cũ ngay** |
| 2 | Mở một trang sản phẩm | Ảnh hiện đủ, không vỡ |
| 3 | Mở `vitalite.io.vn/wp-content/uploads/` | Lỗi **403**, không phải danh sách file |
| 4 | Mở `vitalite.io.vn/wp-config.php` | Lỗi **403** |
| 5 | Vào trang admin, upload thử một ảnh | Upload được, ảnh hiện trong Media Library |

🔴 **Bước 2 và 5 là bước dễ vỡ nhất.** Luật chống hotlink viết sai một ký tự là ảnh trên chính
site mình cũng bị chặn. Nếu ảnh vỡ, xoá riêng mục 2 rồi thử lại.

---

## 3. Việc nên làm ở tầng khác

### 3.1 Ảnh — thứ đáng bảo vệ nhất

`.htaccess` chặn **nhúng**, không chặn **tải về**. Chuột phải → Save image vẫn chạy, và không có
cách nào ngăn được, vì trình duyệt phải tải ảnh xuống mới hiện được.

Ba việc thật sự giảm thiệt hại:

- **Không upload ảnh gốc độ phân giải cao.** Ảnh sản phẩm 2000px là đủ để zoom trên web và
  **không đủ** để in lookbook hay chạy billboard. Ảnh gốc giữ ở máy.
- **Watermark mờ ở một góc** cho ảnh lookbook. Không phải cho ảnh PDP — watermark trên ảnh sản phẩm
  làm giảm tỷ lệ chuyển đổi, đây là đánh đổi thật, không phải cẩn thận thừa.
- **Chuỗi 96 frame CGI**: đây là tài sản dựng hình đắt nhất trên site. Cân nhắc giảm còn 48 frame
  và nén sâu hơn — vừa nhẹ site vừa giảm giá trị của bản bị lấy. *(Chưa làm, cần quyết.)*

### 3.2 Pháp lý — cái này mới là cái ngăn được thật

Trang `terms` đã có mục **Intellectual property** ghi rõ tên, logo, thiết kế, hoạ tiết và ảnh
thuộc về VITALITÉ. Đó là căn cứ để gửi **DMCA takedown**.

Thực tế: một yêu cầu gỡ gửi tới Shopee, Facebook hoặc host của site nhái có hiệu lực nhanh hơn
mọi biện pháp kỹ thuật trong file này. Kỹ thuật làm chậm việc copy; pháp lý mới gỡ được bản copy.

Cần khi đó: ảnh gốc có metadata ngày chụp, và bài đăng Instagram gốc — cả hai đều chứng minh
mình có trước.

### 3.3 Không làm — đã cân nhắc và loại

| Đề xuất | Vì sao loại |
|---|---|
| Chặn chuột phải / F12 | Phá inspect của chính mình, phá trợ năng, phá được trong 5 giây |
| Obfuscate JS | De-obfuscate mất 10 giây. Và **minify đang phải TẮT** vì xung đột Elementor |
| Ảnh nền CSS thay `<img>` | Phá SEO ảnh, phá `alt`, phá lazy-load. Vẫn tải về được từ tab Network |
| Canvas / watermark bằng JS | Chậm, phá SEO, tắt JS là hết |
| Tắt hẳn `view-source:` | Không tồn tại. Không có cách nào |

---

## 4. Tóm lại

| Muốn | Làm được không | Cách |
|---|---|---|
| Giấu code PHP | ✅ Đã kín sẵn | Không cần làm gì |
| Chặn xem HTML/CSS/JS | ❌ Không | Đừng thử |
| Chặn site khác nhúng ảnh mình | ✅ Được | `.htaccess` mục 2 |
| Chặn tải hàng loạt cả thư mục | ✅ Được | `.htaccess` mục 1 |
| Chặn công cụ clone cả site | 🟡 Phần lớn | `.htaccess` mục 3 |
| Chặn lưu một tấm ảnh | ❌ Không | Giảm độ phân giải + watermark |
| Gỡ bản copy đã tồn tại | ✅ Được | DMCA, dựa trên mục IP ở `terms` |
