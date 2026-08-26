# -*- coding: utf-8 -*-
"""Sinh bảng xem trực quan cho brand guideline.

    deliverables/brand/tokens.css  ->  deliverables/brand/guideline.html

Mọi ô màu, mọi mã hex, mọi tỷ lệ tương phản trong trang đều ĐỌC TỪ tokens.css
và TÍNH tại lúc sinh. Không chép tay số nào. Đổi một màu trong tokens.css rồi
chạy lại là bảng tự đúng, kể cả cột tương phản.

    cd "E:\\Vitalite website"; python docs/make-guideline.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, 'deliverables', 'brand', 'tokens.css')
OUT = os.path.join(ROOT, 'deliverables', 'brand', 'guideline.html')
LOGO_DIR = os.path.join(ROOT, 'Logo', 'Black Sabbath')


# ---------------------------------------------------------------- đọc token
def read_tokens():
    src = io.open(TOKENS, encoding='utf-8').read()
    body = re.search(r':root\s*\{(.*)\n\}', src, re.S).group(1)
    body = re.sub(r'/\*.*?\*/', '', body, flags=re.S)
    out = {}
    for part in body.split(';'):
        if ':' not in part:
            continue
        k, v = part.split(':', 1)
        out[k.strip()] = ' '.join(v.split())
    return out


def root_block(tk):
    return ':root{' + ';'.join('%s:%s' % (k, v) for k, v in tk.items()) + ';}'


# ---------------------------------------------------------------- tương phản
def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lum(hexv):
    h = hexv.lstrip('#')
    if len(h) == 3:
        h = ''.join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return .2126 * _lin(r) + .7152 * _lin(g) + .0722 * _lin(b)


def contrast(fg, bg):
    a, b = _lum(fg), _lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + .05) / (lo + .05)


def grade(r, large=False):
    if large:
        return 'AAA' if r >= 4.5 else ('AA' if r >= 3 else 'trượt')
    return 'AAA' if r >= 7 else ('AA' if r >= 4.5 else 'trượt')


# ---------------------------------------------------------------- các khối
def swatch_row(tk, name, note, on=None):
    """Một hàng ô màu. `on` là nền để đo tương phản, None thì không đo."""
    val = tk.get(name, '')
    is_hex = val.startswith('#')
    ratio_cell = '<td class="g-dim">không đo, đây không phải màu chữ</td>'
    if on and is_hex:
        r = contrast(val, tk[on])
        cls = 'g-pass' if r >= 4.5 else ('g-warn' if r >= 3 else 'g-fail')
        ratio_cell = ('<td><b class="%s">%.2f</b><span class="g-dim"> trên %s · %s</span></td>'
                      % (cls, r, on.replace('--vt-', ''), grade(r)))
    return ('<tr>'
            '<td><span class="g-chip" style="background:%s"></span></td>'
            '<td><code>%s</code></td>'
            '<td class="g-mono">%s</td>'
            '<td>%s</td>'
            '%s</tr>' % (val, name, val, note, ratio_cell))


LOGOS = [
    ('vitalite_LOGO-17.png', 'Mark hoa bốn cánh', 'Symbol chính. Favicon, app icon, nhãn cổ', '512×645'),
    ('vitalite_LOGO-18.png', 'Emblem e + bóng nước', 'Emblem phụ, dùng hiếm', '663×654'),
    ('vitalite_LOGO-19.png', 'VITALITÉ hoa in', 'Wordmark trang trọng', '697×137'),
    ('vitalite_LOGO-20.png', 'vitalité thường', '⭐ Wordmark chính, dùng cho giao diện', '617×137'),
    ('vitalite_LOGO-21.png', 'vitalité, e là emblem', 'Lockup chữ ký, dùng cho thương hiệu', '615×137'),
    ('vitalite_LOGO-22.png', 'Vitalité chữ ký', 'Trang trí, in ngực', '807×287'),
    ('vitalite_LOGO-23.png', 'Tag graffiti mảnh', 'Đồ hoạ sản phẩm, KHÔNG phải logo giao diện', '724×337'),
    ('vitalite_LOGO-24.png', 'Tag graffiti dày', 'Đồ hoạ sản phẩm, KHÔNG phải logo giao diện', '724×391'),
]

SCALE = [
    ('--vt-t-hero', 'Hero', 'display'),
    ('--vt-t-2xl', 'Tiêu đề section', 'display'),
    ('--vt-t-xl', 'Tiêu đề khối', 'display'),
    ('--vt-t-lg', 'Tiêu đề phụ', 'display'),
    ('--vt-t-md', 'Chữ nhấn', 'primary'),
    ('--vt-t-base', 'Chữ giao diện', 'primary'),
    ('--vt-t-sm', 'Chú thích', 'primary'),
    ('--vt-t-xs', 'Eyebrow', 'mono'),
]


def build():
    tk = read_tokens()

    colors_neutral = [
        ('--vt-paper', 'Nền chính: lưới sản phẩm, PDP, trang chính sách', None),
        ('--vt-tint', 'Nền phụ, khối nhấn nhẹ', None),
        ('--vt-ink', 'Chữ chính, VÀ nền của mọi vùng tối', '--vt-paper'),
        ('--vt-ink-soft', 'Nền tối hạng hai', None),
        ('--vt-line', 'Đường kẻ mảnh', None),
        ('--vt-line-strong', 'Viền ô nhập, mép thẻ', None),
        ('--vt-muted', 'Chữ phụ', '--vt-paper'),
        ('--vt-dim', 'Chữ mờ nhất còn đọc được', '--vt-paper'),
    ]
    colors_dark = [
        ('--vt-on-dark', 'Chữ trên nền tối', '--vt-ink'),
    ]
    colors_state = [
        ('--vt-sale', 'Giảm giá, xoá, lỗi', '--vt-paper'),
        ('--vt-ok', 'Còn hàng, thành công', '--vt-paper'),
        ('--vt-yes', 'Dấu + trong danh sách được phép', '--vt-paper'),
    ]
    colors_brand = [
        ('--vt-accent', 'Màu nhấn. ĐANG LÀ ĐEN vì brand chưa cấp mã', '--vt-paper'),
        ('--vt-archive-pink', 'Hồng thời kỳ cũ, ĐO ĐƯỢC. Không dùng cho UI', '--vt-paper'),
    ]
    colors_tool = [
        ('--vt-flag', 'Viền ô chưa có dữ liệu', '--vt-flag-bg'),
        ('--vt-flag-bg', 'Nền ô đó', None),
    ]

    def table(rows):
        return ('<table class="g-table"><thead><tr><th></th><th>Token</th><th>Giá trị</th>'
                '<th>Dùng vào</th><th>Tương phản</th></tr></thead><tbody>'
                + ''.join(swatch_row(tk, n, note, on) for n, note, on in rows)
                + '</tbody></table>')

    logo_cards = ''.join(
        '<figure class="g-logo"><div class="g-logo-box"><img src="../../Logo/Black Sabbath/%s" alt="%s" loading="lazy"></div>'
        '<figcaption><b>%s</b><span>%s</span><span class="g-mono g-dim">%s · %s</span></figcaption></figure>'
        % (f, name, name, role, f.replace('vitalite_', '').replace('.png', ''), box)
        for f, name, role, box in LOGOS)

    scale_rows = ''.join(
        '<div class="g-scale-row"><div class="g-scale-meta"><code>%s</code><span class="g-mono g-dim">%s</span>'
        '<span class="g-dim">%s</span></div>'
        '<div class="g-scale-demo" style="font-size:var(%s);font-family:var(--vt-font-%s);'
        '%s">Even in chaos</div></div>'
        % (tok, tk.get(tok, ''), label, tok, fam,
           'font-weight:800;text-transform:uppercase;letter-spacing:-.035em;line-height:1.02;'
           if fam == 'display' else
           ('letter-spacing:.2em;text-transform:uppercase;' if fam == 'mono' else ''))
        for tok, label, fam in SCALE)

    weights = ''.join(
        '<div class="g-w"><span class="g-mono g-dim">%s</span>'
        '<p style="font-weight:%s;font-size:22px">Heavy in weight</p></div>' % (w, w)
        for w in (400, 500, 600, 700, 800))

    html = HTML % dict(
        tokens=root_block(tk),
        logos=logo_cards,
        neutral=table(colors_neutral),
        dark=table(colors_dark),
        state=table(colors_state),
        brandc=table(colors_brand),
        tool=table(colors_tool),
        scale=scale_rows,
        weights=weights,
        hair=tk.get('--vt-hair', '2px'),
        maxdoc=tk.get('--vt-max-doc', '1180px'),
    )
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(html)
    return OUT


HTML = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VITALITÉ Brand guideline</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Archivo+Expanded:wght@800&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
%(tokens)s
*{box-sizing:border-box}
body{margin:0;background:var(--vt-paper);color:var(--vt-ink);
     font-family:var(--vt-font-primary);font-size:16px;line-height:1.7;color-scheme:light}
main{max-width:1180px;margin:0 auto;padding:clamp(28px,5vw,72px) clamp(20px,5vw,64px) 120px}
h1{font-family:var(--vt-font-display);font-weight:800;text-transform:uppercase;
   font-size:clamp(34px,6vw,72px);line-height:.98;letter-spacing:-.04em;margin:0}
h2{font-family:var(--vt-font-display);font-weight:800;text-transform:uppercase;
   font-size:clamp(22px,3vw,38px);letter-spacing:-.03em;line-height:1.06;margin:0 0 6px}
h3{font-family:var(--vt-font-mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
   color:var(--vt-muted);margin:34px 0 14px;font-weight:500}
p{margin:0 0 14px;max-width:68ch}
code{font-family:var(--vt-font-mono);font-size:12.5px}
.g-mono{font-family:var(--vt-font-mono);font-size:12px}
.g-dim{color:var(--vt-muted)}
.g-eyebrow{font-family:var(--vt-font-mono);font-size:11px;letter-spacing:.22em;
  text-transform:uppercase;color:var(--vt-muted);padding-bottom:14px;
  border-bottom:1px solid var(--vt-ink);margin-bottom:26px}
section{padding-top:clamp(46px,7vw,90px)}
.g-lead{font-size:17px;max-width:64ch;color:var(--vt-muted)}

.g-note{border-left:3px solid var(--vt-flag);background:var(--vt-flag-bg);
  padding:15px 18px;margin:18px 0;font-size:14.5px;max-width:76ch}
.g-note b{display:block;font-family:var(--vt-font-mono);font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--vt-flag);margin-bottom:7px}

.g-table{width:100%%;border-collapse:collapse;margin-top:10px}
.g-table th,.g-table td{padding:11px 12px;text-align:left;border-bottom:1px solid var(--vt-line);
  vertical-align:middle;font-size:14px}
.g-table thead th{font-family:var(--vt-font-mono);font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--vt-muted);border-bottom-color:var(--vt-ink);font-weight:500}
.g-table td:first-child{width:52px}
.g-chip{display:block;width:36px;height:36px;border:1px solid var(--vt-line-strong)}
.g-pass{color:var(--vt-yes)}
.g-warn{color:var(--vt-flag)}
.g-fail{color:var(--vt-sale)}

.g-logos{display:grid;grid-template-columns:repeat(4,1fr);gap:%(hair)s;background:var(--vt-line);
  border:1px solid var(--vt-line);margin-top:14px}
.g-logo{margin:0;background:var(--vt-paper);padding:18px}
.g-logo-box{aspect-ratio:1/1;display:grid;place-items:center;background:var(--vt-tint);padding:16%%}
.g-logo img{max-width:100%%;max-height:100%%;display:block}
.g-logo figcaption{margin-top:12px;display:grid;gap:3px;font-size:12.5px;line-height:1.45}
.g-logo b{font-size:13px}
@media(max-width:900px){.g-logos{grid-template-columns:1fr 1fr}}

.g-scale-row{display:grid;grid-template-columns:210px 1fr;gap:20px;align-items:baseline;
  padding:16px 0;border-bottom:1px solid var(--vt-line)}
.g-scale-meta{display:grid;gap:2px;font-size:12px}
.g-scale-demo{overflow:hidden}
@media(max-width:760px){.g-scale-row{grid-template-columns:1fr}}

.g-ws{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:12px}
.g-w{border:1px solid var(--vt-line);padding:14px}
.g-w p{margin:6px 0 0}
@media(max-width:760px){.g-ws{grid-template-columns:1fr 1fr}}

.g-dark{background:var(--vt-ink);color:var(--vt-on-dark);padding:clamp(20px,3vw,34px);margin-top:14px}
.g-dark .g-table th,.g-dark .g-table td{border-bottom-color:var(--vt-on-dark-line)}
.g-dark .g-table thead th{color:var(--vt-on-dark-muted);border-bottom-color:var(--vt-on-dark)}
.g-dark .g-dim{color:var(--vt-on-dark-muted)}

.g-btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:14px}
.g-btn{display:inline-flex;align-items:center;padding:15px 28px;border-radius:999px;
  border:1px solid var(--vt-ink);background:var(--vt-ink);color:var(--vt-paper);
  font-family:var(--vt-font-mono);font-size:11px;letter-spacing:.15em;text-transform:uppercase;
  cursor:pointer;transition:background var(--vt-fast) var(--vt-ease),color var(--vt-fast) var(--vt-ease)}
.g-btn:hover{background:transparent;color:var(--vt-ink)}
.g-btn--ghost{background:transparent;color:var(--vt-ink)}
.g-btn--ghost:hover{background:var(--vt-ink);color:var(--vt-paper)}

.g-hair{display:grid;grid-template-columns:repeat(4,1fr);gap:%(hair)s;background:var(--vt-line);
  border:1px solid var(--vt-line);margin-top:14px}
.g-hair div{background:var(--vt-paper);padding:26px 16px;font-family:var(--vt-font-mono);
  font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--vt-muted)}

.g-do{display:grid;grid-template-columns:1fr 1fr;gap:%(hair)s;background:var(--vt-line);
  border:1px solid var(--vt-line);margin-top:14px}
.g-do > div{background:var(--vt-paper);padding:20px}
.g-do h4{margin:0 0 10px;font-family:var(--vt-font-mono);font-size:10.5px;letter-spacing:.18em;
  text-transform:uppercase}
.g-do ul{margin:0;padding:0;list-style:none}
.g-do li{padding:6px 0 6px 20px;position:relative;font-size:14px;border-top:1px solid var(--vt-line)}
.g-do li:first-child{border-top:0}
.g-do li::before{position:absolute;left:0;font-family:var(--vt-font-mono);font-weight:600}
.g-yes li::before{content:"+";color:var(--vt-yes)}
.g-no li::before{content:"\\00d7";color:var(--vt-sale)}
@media(max-width:760px){.g-do{grid-template-columns:1fr}}
</style></head><body>
<main>

<p class="g-eyebrow">Vitalité &#174; &middot; Brand guideline &middot; v1.0</p>
<h1>Bảng<br>xem nhanh</h1>
<p class="g-lead" style="margin-top:22px">Trang này <b>sinh tự động</b> từ
<code>deliverables/brand/tokens.css</code>. Mọi ô màu, mã hex và tỷ lệ tương phản đều đọc từ đó
và tính lúc sinh, không chép tay. Đổi màu trong tokens rồi chạy lại
<code>python docs/make-guideline.py</code> là bảng tự đúng.</p>
<p class="g-lead">Phần giải thích <i>vì sao</i> nằm ở <code>BRAND-GUIDELINE.md</code>.</p>

<div class="g-note">
  <b>Đây không phải guideline do brand cấp</b>
  Brand chưa cấp bộ nào. Đây là bộ dựng ngược từ tài sản có thật, quan sát công khai, và những
  quyết định đã ra trong lúc build. Đọc mục 0 của <code>BRAND-GUIDELINE.md</code> để biết mục nào
  là fact, mục nào là lựa chọn của bản dựng.
</div>

<section>
  <p class="g-eyebrow">01 &middot; Logo</p>
  <h2>Tám asset, ba vai trò</h2>
  <p class="g-lead">Tất cả 995&times;994 PNG RGBA, đen tuyền, nền trong suốt.
  Số đo là hộp bao phần mực thật.</p>
  <div class="g-logos">%(logos)s</div>

  <div class="g-note">
    <b>Chưa có SVG, chưa có bản trắng</b>
    Header đang dùng raster 995px nên mờ trên màn 2x. Và đen tuyền thì không đặt được lên nền tối,
    mà header có hai chế độ. Cần file vector gốc.
  </div>

  <h3>Nên và không nên</h3>
  <div class="g-do">
    <div><h4>Nên</h4><ul class="g-yes">
      <li>Chừa khoảng thở bằng nửa chiều cao wordmark</li>
      <li>Wordmark tối thiểu 96px rộng, mark tối thiểu 24px</li>
      <li>Đặt lên khối đặc khi nền là ảnh</li>
      <li>Dùng LOGO-20 cho giao diện, LOGO-21 cho thương hiệu</li>
    </ul></div>
    <div><h4>Không nên</h4><ul class="g-no">
      <li>Đổi sang màu khác đen hoặc trắng</li>
      <li>Thêm bóng, viền, gradient</li>
      <li>Kéo méo, nghiêng, uốn cong</li>
      <li>Gõ lại chữ bằng font khác rồi coi là logo</li>
      <li>Dùng tag graffiti làm logo giao diện</li>
    </ul></div>
  </div>
</section>

<section>
  <p class="g-eyebrow">02 &middot; Màu</p>
  <h2>Thang trung tính</h2>
  <p class="g-lead">Site này chủ yếu đen, trắng, xám. Không phải vì thiếu màu, mà vì vùng sản phẩm
  phải để trắng cho hàng tự nói, và màu nhấn thời kỳ mới chưa có mã.</p>
  %(neutral)s

  <h3>Đảo màu cho vùng tối</h3>
  <div class="g-dark">%(dark)s</div>

  <h3>Màu thương hiệu</h3>
  %(brandc)s
  <div class="g-note">
    <b>Màu nhấn đang là đen, và đó là chủ ý</b>
    Brand đổi chủ. Thời kỳ mới đi xanh dương và tím nhưng chưa cấp mã. Có mã rồi thì đổi đúng
    <code>--vt-accent</code> trong <code>tokens.css</code>, cả site đổi theo.
    Câu <b>42</b> trong <code>CAU-HOI-CHO-BRAND.md</code>. Lấy mã từ file gốc, đừng lấy từ ảnh chụp.
  </div>

  <h3>Màu trạng thái</h3>
  <p class="g-lead">Màu chức năng, không phải màu thương hiệu.</p>
  %(state)s

  <h3>Màu công cụ nội bộ</h3>
  <p class="g-lead">Mọi ô cam phải biến mất trước khi publish. Chúng cố tình chói mắt.</p>
  %(tool)s
</section>

<section>
  <p class="g-eyebrow">03 &middot; Chữ</p>
  <h2>Ba họ, ba việc</h2>
  <p class="g-lead">Mono không phải trang trí. Mọi thứ <i>đo được</i> thì viết bằng mono: giá,
  số đo, mã đơn, GSM, ngày. Mắt học được luật đó sau vài màn hình.</p>
  %(scale)s

  <h3>Độ đậm</h3>
  <div class="g-ws">%(weights)s</div>
  <div class="g-note">
    <b>Weight 700 từng được dùng 48 chỗ mà chưa bao giờ được tải</b>
    Trình duyệt tự bắt sang 600 hoặc 800 nên những chỗ đó sai độ đậm mà không ai biết.
    Đã thêm vào cả theme lẫn bản xem trước.
  </div>
</section>

<section>
  <p class="g-eyebrow">04 &middot; Bố cục</p>
  <h2>Khe 2px, không phải viền</h2>
  <p class="g-lead">Các ô cách nhau <code>--vt-hair</code>, nền lộ ra qua khe tạo thành đường kẻ.
  Nhờ vậy không bao giờ có đường kẻ đôi ở chỗ hai ô giáp nhau.</p>
  <div class="g-hair"><div>Ô một</div><div>Ô hai</div><div>Ô ba</div><div>Ô bốn</div></div>

  <h3>Nút</h3>
  <p class="g-lead">Bo tròn hoàn toàn, không có ngoại lệ.</p>
  <div class="g-btns">
    <button class="g-btn">Add to cart</button>
    <button class="g-btn g-btn--ghost">Size guide</button>
  </div>

  <h3>Bề rộng</h3>
  <p class="g-lead">Trang brand chạy full-width. Trang tài liệu chặn ở
  <code>%(maxdoc)s</code> vì độ dài dòng là yếu tố đọc được.</p>
</section>

<section>
  <p class="g-eyebrow">05 &middot; Còn thiếu</p>
  <h2>Bốn thứ đổi được diện mạo</h2>
  <div class="g-do">
    <div><h4>Chặn thật</h4><ul class="g-no">
      <li>Mã hex tím và xanh dương, lấy từ file gốc</li>
      <li>File vector logo, .ai hoặc .svg</li>
      <li>Bản logo trắng cho nền tối</li>
      <li>Ảnh chụp sản phẩm thật từ 1600px</li>
    </ul></div>
    <div><h4>Dọn dẹp</h4><ul class="g-yes">
      <li>Xác nhận phân vai LOGO-20 với LOGO-21</li>
      <li>Xác nhận Black Sabbath là tên bộ hay tên tuỳ hứng</li>
      <li>Brand có typeface riêng không</li>
    </ul></div>
  </div>
</section>

</main></body></html>
"""


if __name__ == '__main__':
    print('OK  %s' % os.path.relpath(build(), ROOT))
