# -*- coding: utf-8 -*-
"""Sinh bản PDF trình bày của brand guideline.

    deliverables/brand/tokens.css
        -> deliverables/brand/guideline-print.html
        -> deliverables/brand/VITALITE-Brand-Guideline.pdf

Đây là bản ĐỂ ĐƯA CHO BRAND XEM. Khác với guideline.html:

    guideline.html        bảng tra nội bộ, cuộn dọc, dày chữ
    guideline-print.html  16 trang A4 ngang, hình là chính, chữ tối thiểu

Màu vẫn đọc từ tokens.css nên không lệch với site.

CHẠY
    cd "E:\\Vitalite website"; python docs/make-guideline-pdf.py

Cần Chrome hoặc Edge. Script tự dò. Không có thì nó vẫn ghi file HTML ra,
mở bằng trình duyệt rồi Ctrl+P > Save as PDF cũng ra đúng bản đó.
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, 'deliverables', 'brand', 'tokens.css')
OUT_HTML = os.path.join(ROOT, 'deliverables', 'brand', 'guideline-print.html')
OUT_PDF = os.path.join(ROOT, 'deliverables', 'brand', 'VITALITE-Brand-Guideline.pdf')

BROWSERS = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
]

LOGO = '../../Logo/Black Sabbath/vitalite_LOGO-%s.png'
MODEL = '../../model/%s'
MOCK = '../../mockup-all/webp/%s.webp'

MODELS = [
    '770354218_4929000030660174_696358091530716839_n.jpg',   # hoodie xám, đường phố
    '769838759_1571742234448867_338508910782118873_n.jpg',   # hoodie xám ngồi
    '770000434_888043017397163_2569307657965761224_n.jpg',   # tee đen graffiti hồng
    '774008184_1479953747234149_6694926411915517100_n.jpg',  # mark hoa in lưng
    '771854804_1375089277925064_5285329065371981670_n.jpg',  # tee trắng graffiti
]


def tokens():
    src = io.open(TOKENS, encoding='utf-8').read()
    body = re.search(r':root\s*\{(.*)\n\}', src, re.S).group(1)
    body = re.sub(r'/\*.*?\*/', '', body, flags=re.S)
    out = {}
    for part in body.split(';'):
        if ':' in part:
            k, v = part.split(':', 1)
            out[k.strip()] = ' '.join(v.split())
    return out


def root_block(tk):
    return ':root{' + ';'.join('%s:%s' % (k, v) for k, v in tk.items()) + ';}'


# --------------------------------------------------------------- tương phản
def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lum(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return .2126 * _lin(r) + .7152 * _lin(g) + .0722 * _lin(b)


def contrast(a, b):
    x, y = _lum(a), _lum(b)
    hi, lo = max(x, y), min(x, y)
    return (hi + .05) / (lo + .05)


# --------------------------------------------------------------- cắt cận chữ e
def crop_e():
    """Cắt vùng chữ `e` của LOGO-20 và LOGO-21 ra file riêng.

    Trang 5 nói hai bản khác nhau ở chữ `e`. Đặt cạnh nhau nguyên wordmark thì
    ở cỡ in không ai thấy khác biệt, tức là trang đó KHẲNG ĐỊNH chứ không
    CHỨNG MINH. Cắt cận thì nhìn phát ra ngay.
    """
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return False
    outdir = os.path.join(ROOT, 'deliverables', 'brand', 'assets')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    for num in ('20', '21'):
        src = os.path.join(ROOT, 'Logo', 'Black Sabbath', 'vitalite_LOGO-%s.png' % num)
        im = Image.open(src).convert('RGBA')
        a = np.asarray(im)[:, :, 3]
        ys, xs = np.where(a > 16)
        x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
        w, h = x1 - x0, y1 - y0
        # chữ `e` của "vitalité" nằm khoảng 63-80% bề ngang wordmark
        cx0 = x0 + int(w * 0.60)
        cx1 = x0 + int(w * 0.83)
        pad = int(h * 0.34)
        box = (max(0, cx0 - pad), max(0, y0 - pad),
               min(im.width, cx1 + pad), min(im.height, y1 + pad))
        crop = im.crop(box)
        bg = Image.new('RGBA', crop.size, (244, 244, 244, 255))
        bg.alpha_composite(crop)
        bg.convert('RGB').save(os.path.join(outdir, 'e-%s.png' % num), 'PNG')

    # Bản wordmark CẮT SÁT MỰC cho sơ đồ khoảng thở.
    # File gốc là canvas vuông 994px nên tự nó đã có sẵn khoảng trắng; dùng
    # nguyên bản thì cái nhãn "nửa chiều cao" trỏ vào một khoảng cách sai.
    src = os.path.join(ROOT, 'Logo', 'Black Sabbath', 'vitalite_LOGO-20.png')
    im = Image.open(src).convert('RGBA')
    a = np.asarray(im)[:, :, 3]
    ys, xs = np.where(a > 16)
    im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))       .save(os.path.join(outdir, 'wordmark-trim.png'), 'PNG')
    return True


# --------------------------------------------------------------- khối dựng
def page(n, label, body, cls=''):
    return ('<section class="pg %s"><div class="pg-in">%s</div>'
            '<footer class="pg-ft"><span>Vitalité &#174; &middot; Brand Guideline</span>'
            '<span>%s</span><span>%02d</span></footer></section>'
            % (cls, body, label, n))


def swatch(tk, name, label, on=None, big=False):
    v = tk.get(name, '')
    ratio = ''
    if on and v.startswith('#'):
        ratio = '<i>%.1f:1</i>' % contrast(v, tk[on])
    return ('<div class="sw %s"><span class="sw-c" style="background:%s"></span>'
            '<b>%s</b><code>%s</code>%s</div>'
            % ('sw--big' if big else '', v, label, v.upper(), ratio))


def build_html():
    tk = tokens()
    P = []

    # ---------- 01 BÌA ----------
    P.append(page(1, 'Cover', """
      <img class="cover-bg" src="%s" alt="">
      <div class="cover-scrim"></div>
      <div class="cover-txt">
        <img class="cover-logo" src="%s" alt="vitalité">
        <p class="k">Brand Guideline</p>
        <h1>Even in chaos,<br>you are alive.</h1>
        <p class="k k--dim">Version 1.0 &middot; 08.2026 &middot; vitalite.io.vn</p>
      </div>""" % (MODEL % MODELS[0], LOGO % '20'), 'pg--cover'))

    # ---------- 02 CÁCH ĐỌC ----------
    P.append(page(2, 'Cách đọc', """
      <p class="k">00</p>
      <h2>Đọc nhãn<br>trước khi đọc nội dung</h2>
      <p class="lead">Tài liệu này dựng ngược từ ba nguồn: tài sản gốc của thương hiệu,
      kênh công khai trên Shopee và Instagram, và những quyết định đã ra khi làm website.
      Không phải mọi thứ trong đây đều là quy chuẩn của thương hiệu, nên mỗi mục có nhãn riêng.</p>
      <div class="cards3">
        <div class="card card--ok"><b>Đo được</b>
          <p>Lấy từ file gốc hoặc kênh chính thức. Có nguồn dẫn được.
          Chỉ thương hiệu mới đổi được.</p></div>
        <div class="card card--mid"><b>Đề xuất</b>
          <p>Lựa chọn của bên làm website, có lý do, và <b>đổi được</b>.
          Đây là chỗ chờ thương hiệu duyệt hoặc thay.</p></div>
        <div class="card card--no"><b>Còn thiếu</b>
          <p>Đang trống. Bốn mục ở trang cuối là thứ thật sự thay đổi
          diện mạo website.</p></div>
      </div>"""))

    # ---------- 03 LOGO hệ thống ----------
    P.append(page(3, 'Logo', """
      <p class="k">01 &middot; Logo &middot; <em class="tag tag--ok">Đo được</em></p>
      <h2>Tám dấu hiệu,<br>ba vai trò</h2>
      <div class="lg8">%s</div>
      <p class="note">Tất cả 995&times;994px, PNG nền trong suốt, đen tuyền 100%%.
      Số bên dưới là kích thước phần mực thật, không phải khung ảnh.</p>"""
      % ''.join(
          '<figure><span><img src="%s" alt=""></span><b>%s</b><i>%s</i></figure>' % (LOGO % num, nm, ro)
          for num, nm, ro in [
              ('17', 'Mark hoa', 'Symbol · 512×645'),
              ('18', 'Emblem', 'Phụ · 663×654'),
              ('19', 'Hoa in', 'Trang trọng · 697×137'),
              ('20', 'Wordmark', 'CHÍNH · 617×137'),
              ('21', 'Lockup', 'Chữ ký · 615×137'),
              ('22', 'Chữ ký', 'Trang trí · 807×287'),
              ('23', 'Tag mảnh', 'Đồ hoạ SP · 724×337'),
              ('24', 'Tag dày', 'Đồ hoạ SP · 724×391'),
          ])))

    # ---------- 04 WORDMARK + clear space ----------
    P.append(page(4, 'Wordmark', """
      <p class="k">01.1 &middot; Wordmark chính</p>
      <div class="split">
        <div>
          <div class="cs">
            <div class="cs-box"><img src="assets/wordmark-trim.png" alt="vitalité"></div>
            <span class="cs-t">½ h</span><span class="cs-b">½ h</span>
            <span class="cs-l">½&nbsp;h</span><span class="cs-r">½&nbsp;h</span>
          </div>
          <p class="note">Khoảng thở bằng <b>nửa chiều cao wordmark</b> ở cả bốn phía.
          Không đặt chữ, đường kẻ, mép ảnh hay mép nút vào vùng đó.</p>
        </div>
        <div>
          <h3>Cỡ nhỏ nhất</h3>
          <table class="tb">
            <tr><td><b class="lb">Wordmark</b><i>LOGO-20</i></td><td class="num">96px</td>
                <td>Dưới mức đó dấu sắc trên <b>é</b> dính vào vòng <b>®</b></td></tr>
            <tr><td><b class="lb">Mark</b><i>LOGO-17</i></td><td class="num">24px</td>
                <td>Bốn khối tròn còn tách được ở cỡ favicon</td></tr>
            <tr><td><b class="lb">Lockup</b><i>LOGO-21</i></td><td class="num">140px</td>
                <td>Gợn nước trong chữ <b>e</b> là chi tiết mảnh nhất cả bộ</td></tr>
          </table>
          <div class="flag"><b>Còn thiếu</b>
          Chưa có file vector và chưa có bản trắng. Header website đang dùng ảnh raster nên
          mờ trên màn hình mật độ cao, và đen tuyền thì không đặt được lên nền tối.</div>
        </div>
      </div>"""))

    # ---------- 05 LOCKUP 20 vs 21 ----------
    has_crop = crop_e()
    detail = ('<div class="zoom">'
              '<figure><span><img src="assets/e-20.png" alt=""></span>'
              '<b>LOGO-20</b><i>chữ e thường</i></figure>'
              '<figure><span><img src="assets/e-21.png" alt=""></span>'
              '<b>LOGO-21</b><i>e là emblem, có gợn nước</i></figure>'
              '</div>') if has_crop else ''
    P.append(page(5, 'Lockup', """
      <p class="k">01.2 &middot; Hai bản gần giống nhau</p>
      <h2>Khác đúng một chữ</h2>
      <div class="split">
        <div>
          <div class="vs">
            <figure><span><img src="%s" alt=""></span><b>LOGO-20</b></figure>
            <figure><span><img src="%s" alt=""></span><b>LOGO-21</b></figure>
          </div>
          <p class="note">Ở cỡ này gần như không phân biệt được. Đối chiếu từng điểm ảnh
          cho thấy hai bản khác nhau <b>47,3%%</b>, và toàn bộ khác biệt nằm ở chữ
          <b>e</b>. Phóng to lên thì rõ ngay.</p>
        </div>
        <div>
          %s
          <table class="tb">
            <tr><td><b class="lb">LOGO-20</b><i>Giao diện</i></td>
                <td>Header, footer, hoá đơn. Chỗ cần đọc nhanh ở cỡ nhỏ.</td></tr>
            <tr><td><b class="lb">LOGO-21</b><i>Thương hiệu</i></td>
                <td>Nhãn sản phẩm, bao bì, ảnh mạng xã hội. Chỗ có chỗ thở.</td></tr>
          </table>
          <div class="flag flag--ask"><b>Cần xác nhận</b>
          Cách phân vai trên là <b>đề xuất</b>. Thương hiệu xác nhận giúp bản nào dùng ở đâu.</div>
        </div>
      </div>""" % (LOGO % '20', LOGO % '21', detail)))

    # ---------- 06 KHÔNG NÊN ----------
    P.append(page(6, 'Không nên', """
      <p class="k">01.3 &middot; Không nên</p>
      <h2>Sáu cách làm hỏng logo</h2>
      <div class="dont">%s</div>"""
      % ''.join(
          '<figure><span class="dont-box%s"%s><img src="%s" alt="" style="%s"></span><b>%s</b></figure>'
          % ((' dont-box--photo' if i == 0 else ''),
             (' style="background-image:url(%s)"' % (MODEL % MODELS[2]) if i == 0 else ''),
             LOGO % '20', st, cap)
          for i, (st, cap) in enumerate([
              ('', 'Đặt thẳng lên ảnh rối, không có khối nền'),
              ('transform:scaleX(1.45)', 'Kéo méo theo chiều ngang'),
              ('transform:skewX(-16deg)', 'Làm nghiêng'),
              ('filter:drop-shadow(4px 5px 0 rgba(0,0,0,.45))', 'Thêm bóng đổ hoặc hiệu ứng'),
              ('transform:rotate(-14deg)', 'Xoay tuỳ tiện'),
              ('opacity:.32', 'Giảm độ đậm để làm nền'),
          ]))))

    # ---------- 07 MÀU trung tính ----------
    P.append(page(7, 'Màu', """
      <p class="k">02 &middot; Màu &middot; <em class="tag tag--mid">Đề xuất</em></p>
      <h2>Đen, trắng,<br>và khoảng giữa</h2>
      <p class="lead">Website chủ yếu là ba màu này. Không phải vì thiếu màu, mà vì vùng sản phẩm
      để trắng thì hàng tự nói, và màu nhấn của thời kỳ mới thì chưa có mã.</p>
      <div class="sws">%s</div>
      <p class="note">Số bên dưới mỗi ô là tỷ lệ tương phản trên nền trắng, đo theo chuẩn WCAG.
      Từ 4,5:1 trở lên là đạt mức AA cho chữ thường.</p>"""
      % ''.join([
          swatch(tk, '--vt-paper', 'Paper'),
          swatch(tk, '--vt-tint', 'Tint'),
          swatch(tk, '--vt-line', 'Line'),
          swatch(tk, '--vt-line-strong', 'Line strong'),
          swatch(tk, '--vt-dim', 'Dim', '--vt-paper'),
          swatch(tk, '--vt-muted', 'Muted', '--vt-paper'),
          swatch(tk, '--vt-ink-soft', 'Ink soft', '--vt-paper'),
          swatch(tk, '--vt-ink', 'Ink', '--vt-paper'),
      ])))

    # ---------- 08 MÀU nhấn ----------
    P.append(page(8, 'Màu nhấn', """
      <p class="k">02.1 &middot; Màu nhấn &middot; <em class="tag tag--no">Còn thiếu</em></p>
      <div class="split split--wide">
        <div>
          <h2>Đang là đen,<br>và đó là chủ ý</h2>
          <p class="lead">Thời kỳ mới của thương hiệu đi theo xanh dương và tím, nhưng
          <b>chưa có mã màu chính thức</b>. Đóng đinh vào một màu đoán được thì cả website
          phải sơn lại khi có mã thật.</p>
          <p class="lead">Cần <b>mã hex lấy từ file thiết kế gốc</b>, không lấy từ ảnh chụp.
          Màu trong ảnh là màu vải qua ánh sáng ngoài trời cộng thêm nén JPEG, không phải màu spec.</p>
          <div class="flag flag--ask"><b>Cần từ thương hiệu</b>
          Một mã tím, một mã xanh dương. Đưa được hai mã đó là toàn bộ website đổi theo
          chỉ bằng một dòng.</div>
        </div>
        <div class="accent-now">
          <span style="background:%s"></span>
          <b>Hiện tại</b><code>%s</code>
          <i>Trung tính, an toàn, và tạm thời</i>
        </div>
      </div>""" % (tk['--vt-accent'], tk['--vt-accent'].upper())))

    # ---------- 09 HỒNG ARCHIVE ----------
    pinks = [('#CF1D57', '340°'), ('#C52458', '341°'), ('#D84361', '348°'),
             ('#E24968', '348°'), ('#C8497C', '336°'), ('#FD679F', '338°')]
    P.append(page(9, 'Hồng archive', """
      <p class="k">02.2 &middot; Hồng thời kỳ cũ &middot; <em class="tag tag--ok">Đo được</em></p>
      <h2>Không phải đỏ.<br>Là hồng rose.</h2>
      <div class="split">
        <div>
          <div class="pinks">%s</div>
          <p class="note">Đo trực tiếp trên vùng in lớn nhất của sáu mẫu sản phẩm thật.
          Sắc màu bám rất chặt trong khoảng <b>336° đến 348°</b>. Đó là hồng rose,
          không phải đỏ.</p>
          <div class="flag"><b>Không dùng cho giao diện</b>
          Màu này thuộc về dòng sản phẩm cũ. Chỉ dùng khi đang nói về chính dòng đó.</div>
        </div>
        <div class="pinkshot"><img src="%s" alt=""><img src="%s" alt=""></div>
      </div>""" % (
        ''.join('<div class="pk"><span style="background:%s"></span><code>%s</code><i>%s</i></div>'
                % (h, h, hue) for h, hue in pinks),
        MOCK % '5', MOCK % '7')))

    # ---------- 10 VÁNG DẦU ----------
    P.append(page(10, 'Váng dầu', """
      <p class="k">02.3 &middot; Váng dầu &middot; <em class="tag tag--mid">Quan sát</em></p>
      <h2>Chỉ dùng cho mảng nền</h2>
      <div class="iri"></div>
      <div class="split">
        <p class="lead">Bốn màu này quan sát từ ảnh Instagram của thời kỳ mới, <b>không phải mã spec</b>.
        Chúng dùng cho hero, dải ngăn giữa các phần, và phần đóng trang giới thiệu.</p>
        <div class="flag"><b>Không dùng cho chữ</b>
        Bề mặt này chuyển động và đổi độ sáng liên tục, nên không có tỷ lệ tương phản nào
        đảm bảo được. Chữ đặt lên đây là chữ có lúc đọc được có lúc không.</div>
      </div>"""))

    # ---------- 11 CHỮ ----------
    P.append(page(11, 'Chữ', """
      <p class="k">03 &middot; Chữ &middot; <em class="tag tag--mid">Đề xuất</em></p>
      <h2>Ba họ, ba việc</h2>
      <div class="fonts">
        <div><p class="k k--dim">Tiêu đề · Archivo Expanded 800</p>
             <p class="fd">HEAVY IN WEIGHT</p></div>
        <div><p class="k k--dim">Chữ chạy · Archivo 400–700</p>
             <p class="fp">Finding harmony within chaos. Chasing the lights,
             but we are the main source.</p></div>
        <div><p class="k k--dim">Kỹ thuật · JetBrains Mono 400–500</p>
             <p class="fm">500+ GSM · S / M / L · 599.100&#8363; · #12034</p></div>
      </div>
      <p class="note">Mono không phải trang trí. Mọi thứ <b>đo được</b> thì viết bằng mono:
      giá, số đo, mã đơn, định lượng vải, ngày. Mắt học được luật đó sau vài màn hình,
      rồi tự phân loại thông tin hộ mình.</p>
      <div class="flag flag--ask"><b>Cần xác nhận</b>
      Ba phông này là <b>đề xuất của bên làm website</b>, không phải phông của thương hiệu.
      Thương hiệu có bộ phông riêng thì gửi, đổi được ở một chỗ duy nhất.</div>"""))

    # ---------- 12 THANG CHỮ ----------
    ladder = [('--vt-t-hero', 'Hero'), ('--vt-t-2xl', 'Tiêu đề phần'),
              ('--vt-t-xl', 'Tiêu đề khối'), ('--vt-t-lg', 'Tiêu đề phụ'),
              ('--vt-t-md', 'Chữ nhấn'), ('--vt-t-base', 'Chữ giao diện')]
    P.append(page(12, 'Thang chữ', """
      <p class="k">03.1 &middot; Thang chữ</p>
      <h2>Co giãn theo màn hình</h2>
      <div class="ladder">%s</div>
      <p class="note">Cỡ chữ không cố định. Hai số trong ngoặc là nhỏ nhất và lớn nhất;
      giữa hai mốc đó chữ co giãn theo bề rộng màn hình. Nhờ vậy tiêu đề trên điện thoại
      không bị vỡ, mà trên màn lớn vẫn đủ sức nặng.</p>"""
      % ''.join('<div class="ld"><span class="ld-m"><code>%s</code><i>%s</i></span>'
                '<span class="ld-d" style="font-size:%s">Even in chaos</span></div>'
                % (t.replace('--vt-t-', ''), tk[t], tk[t]) for t, lb in ladder)))

    # ---------- 13 BỐ CỤC ----------
    P.append(page(13, 'Bố cục', """
      <p class="k">04 &middot; Bố cục</p>
      <h2>Khe hở làm đường kẻ</h2>
      <div class="split">
        <div>
          <div class="hair"><div>Ô một</div><div>Ô hai</div><div>Ô ba</div>
                            <div>Ô bốn</div><div>Ô năm</div><div>Ô sáu</div></div>
          <p class="note">Các ô cách nhau <b>2px</b> và nền lộ ra qua khe, tạo thành đường kẻ.
          Không dùng viền. Nhờ vậy chỗ hai ô giáp nhau không bao giờ có đường kẻ đôi.</p>
        </div>
        <div>
          <h3>Nút</h3>
          <div class="btns"><span class="bt">Add to cart</span>
                            <span class="bt bt--g">Size guide</span></div>
          <p class="note">Bo tròn hoàn toàn, không có ngoại lệ.
          Nút chính là khối đặc, di chuột vào thì rỗng ruột. Nút phụ ngược lại.</p>
          <h3>Bề rộng</h3>
          <table class="tb">
            <tr><td><b class="lb">Trang thương hiệu</b><i>chủ, giới thiệu, shop, sản phẩm</i></td>
                <td class="num">Tràn viền</td></tr>
            <tr><td><b class="lb">Trang tài liệu</b><i>chính sách, giỏ, thanh toán</i></td>
                <td class="num">1180px</td></tr>
          </table>
        </div>
      </div>"""))

    # ---------- 14 ẢNH ----------
    P.append(page(14, 'Ảnh', """
      <p class="k">05 &middot; Ảnh</p>
      <h2>Hai vùng, hai kiểu</h2>
      <div class="shots">%s</div>
      <div class="split">
        <p class="lead"><b>Vùng sản phẩm để nền trắng.</b> Lưới hàng và trang sản phẩm dùng ảnh
        nền trắng, nhất quán, để mắt so sánh được giữa các mẫu.</p>
        <p class="lead"><b>Vùng kể chuyện đi nền tối.</b> Hero, dải ngăn, trang giới thiệu dùng
        ảnh đời thường và bề mặt váng dầu.</p>
      </div>
      <div class="flag flag--ask"><b>Cần từ thương hiệu</b>
      Ảnh chụp sản phẩm thật từ <b>1600px</b> trở lên, mỗi mã hàng cần 2 đến 3 ảnh mặc trên người,
      1 ảnh trải phẳng và 1 đến 2 ảnh cận đường may. Đây là thứ nâng trang sản phẩm lên nhiều nhất.</div>"""
      % ''.join('<figure><img src="%s" alt=""></figure>' % (MODEL % m) for m in MODELS[1:5])))

    # ---------- 15 SO SÁNH HAI THỜI KỲ ----------
    P.append(page(15, 'Hai thời kỳ', """
      <p class="k">06 &middot; Hai thời kỳ &middot; <em class="tag tag--ok">Đo được</em></p>
      <h2>Cùng một nhãn,<br>hai ngôn ngữ hình</h2>
      <div class="eras">
        <div class="era">
          <p class="k k--dim">Đến 2023</p>
          <div class="era-sw"><span style="background:#C52458"></span><span style="background:#0A0A0A"></span><span style="background:#FFFFFF"></span></div>
          <ul><li>Hồng rose làm màu nhấn</li><li>Chụp phẳng, ánh sáng đều</li>
              <li>Caption tiếng Việt</li><li>Pink Graffiti · Porsche · Starlight</li></ul>
        </div>
        <div class="era era--dark">
          <p class="k k--dim">Từ 04.2026</p>
          <div class="era-sw"><span style="background:%s"></span><span style="background:%s"></span><span style="background:%s"></span></div>
          <ul><li>Váng dầu xanh tím</li><li>Ánh sáng gắt, chụp có chỉ đạo</li>
              <li>Caption tiếng Anh</li><li>The Iconic · The Moments · Old Money</li></ul>
        </div>
      </div>
      <p class="note">Hàng của thời kỳ trước <b>không bị gỡ khỏi catalog</b>. Bảng size dùng chung,
      và chính thương hiệu đã đóng khung nó bằng câu <i>old things still shine</i>.</p>"""
      % (tk['--vt-iri-1'], tk['--vt-iri-4'], tk['--vt-iri-2'])))

    # ---------- 16 CẦN GÌ ----------
    P.append(page(16, 'Cần từ thương hiệu', """
      <p class="k">07</p>
      <h2>Bốn thứ<br>đổi được diện mạo</h2>
      <div class="needs">
        <div><span class="nm">01</span><b>Mã hex tím và xanh dương</b>
          <i>Lấy từ file thiết kế gốc. Website đang dùng đen tạm thời.</i></div>
        <div><span class="nm">02</span><b>File vector của logo</b>
          <i>Định dạng .ai hoặc .svg. Bản đang dùng là ảnh raster nên mờ trên màn mật độ cao.</i></div>
        <div><span class="nm">03</span><b>Bản logo màu trắng</b>
          <i>Bản hiện có đen tuyền, không đặt được lên nền tối, mà header có hai chế độ.</i></div>
        <div><span class="nm">04</span><b>Ảnh sản phẩm từ 1600px</b>
          <i>Điều kiện để bật phóng to trên trang sản phẩm.</i></div>
      </div>
      <p class="note">Ngoài bốn mục trên còn ba câu nhỏ hơn: cách phân vai giữa LOGO-20 và LOGO-21,
      tên bộ <i>Black Sabbath</i> là tên chính thức hay tên thư mục, và thương hiệu có bộ phông riêng không.</p>
      <p class="end">vitalitevn@gmail.com</p>"""))

    html = SHELL % dict(tokens=root_block(tk), pages=''.join(P))
    io.open(OUT_HTML, 'w', encoding='utf-8', newline='\n').write(html)
    return OUT_HTML


SHELL = """<!doctype html><html lang="vi"><head><meta charset="utf-8">
<title>VITALITE Brand Guideline</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Archivo+Expanded:wght@800&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
%(tokens)s
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;padding:0;background:#8A8A92}
body{font-family:var(--vt-font-primary);color:var(--vt-ink);font-size:11pt;line-height:1.6}

.pg{width:297mm;height:210mm;background:var(--vt-paper);position:relative;overflow:hidden;
    page-break-after:always;break-after:page;margin:0 auto}
.pg:last-child{page-break-after:auto;break-after:auto}
.pg-in{position:absolute;inset:16mm 18mm 20mm}
.pg-ft{position:absolute;left:18mm;right:18mm;bottom:9mm;display:flex;justify-content:space-between;
  font-family:var(--vt-font-mono);font-size:7pt;letter-spacing:.18em;text-transform:uppercase;
  color:var(--vt-dim);border-top:1px solid var(--vt-line);padding-top:4mm}

h1{font-family:var(--vt-font-display);font-weight:800;text-transform:uppercase;
   font-size:34pt;line-height:.96;letter-spacing:-.035em;margin:0}
h2{font-family:var(--vt-font-display);font-weight:800;text-transform:uppercase;
   font-size:26pt;line-height:1;letter-spacing:-.035em;margin:0 0 6mm}
h3{font-family:var(--vt-font-mono);font-size:8pt;letter-spacing:.2em;text-transform:uppercase;
   color:var(--vt-muted);margin:8mm 0 3mm;font-weight:500}
p{margin:0 0 3mm}
.k{font-family:var(--vt-font-mono);font-size:8pt;letter-spacing:.22em;text-transform:uppercase;
   color:var(--vt-muted);margin:0 0 5mm}
.k--dim{color:var(--vt-dim)}
.lead{font-size:10.5pt;max-width:62ch;color:var(--vt-ink)}
.note{font-size:8.5pt;color:var(--vt-muted);max-width:74ch;margin-top:4mm;line-height:1.55}
.tag{font-style:normal;padding:1mm 2.4mm;border-radius:999px;font-size:7pt;letter-spacing:.14em}
.tag--ok{background:var(--vt-yes);color:#fff}
.tag--mid{background:var(--vt-flag);color:#fff}
.tag--no{background:var(--vt-sale);color:#fff}

/* ---------- bìa ---------- */
.pg--cover{background:var(--vt-ink)}
.cover-bg{position:absolute;top:0;left:0;width:297mm;height:211mm;object-fit:cover;object-position:50%% 30%%}
.cover-scrim{position:absolute;inset:0;background:linear-gradient(105deg,
  rgba(10,10,10,.94) 0%%,rgba(10,10,10,.82) 42%%,rgba(10,10,10,.26) 78%%,rgba(10,10,10,.5) 100%%)}
.cover-txt{position:absolute;left:18mm;right:18mm;bottom:18mm;color:var(--vt-on-dark)}
.cover-txt .k{color:var(--vt-on-dark-muted)}
.cover-logo{width:62mm;display:block;margin-bottom:14mm;filter:invert(1)}
.pg--cover h1{font-size:40pt;margin-bottom:8mm}
.pg--cover .pg-ft{display:none}

/* ---------- thẻ ---------- */
.cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm;margin-top:12mm}
.card{min-height:74mm}
.card{border:1px solid var(--vt-line);padding:7mm;border-top:3px solid var(--vt-ink)}
.card>b{display:block;font-family:var(--vt-font-display);font-weight:800;text-transform:uppercase;
  font-size:13pt;letter-spacing:-.02em;margin-bottom:3mm}
.card p{font-size:9pt;color:var(--vt-muted);margin:0}
.card--ok{border-top-color:var(--vt-yes)}
.card--mid{border-top-color:var(--vt-flag)}
.card--no{border-top-color:var(--vt-sale)}

/* ---------- lưới 8 logo ---------- */
.lg8{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--vt-line);
  border:1px solid var(--vt-line);margin-top:2mm}
.lg8 figure{margin:0;background:var(--vt-paper);padding:5mm;text-align:center}
.lg8 span{display:block;height:34mm;background:var(--vt-tint);padding:5mm;margin-bottom:3mm}
.lg8 img{width:100%%;height:24mm;object-fit:contain;display:block}
.lg8 figure>b{display:block;font-size:9pt}
.lg8 i{display:block;font-family:var(--vt-font-mono);font-size:6.6pt;letter-spacing:.1em;
  text-transform:uppercase;color:var(--vt-dim);font-style:normal;margin-top:1mm}

/* ---------- chia đôi ---------- */
.split{display:grid;grid-template-columns:1fr 1fr;gap:12mm;align-items:start}
.split--wide{grid-template-columns:1.3fr .7fr}

/* ---------- clear space ---------- */
.cs{position:relative;border:1px dashed var(--vt-line-strong);padding:13mm;background:var(--vt-tint)}
.cs-box{border:1px solid var(--vt-ink);padding:5mm;background:var(--vt-paper)}
.cs-box img{width:100%%;display:block}
.cs span{position:absolute;font-family:var(--vt-font-mono);font-size:7pt;color:var(--vt-muted)}
.cs-t{top:5mm;left:50%%}.cs-b{bottom:5mm;left:50%%}
.cs-l{left:3mm;top:50%%}.cs-r{right:3mm;top:50%%}

.tb{width:100%%;border-collapse:collapse;margin-top:2mm}
.tb td{padding:3mm 2mm;border-bottom:1px solid var(--vt-line);vertical-align:top;font-size:9pt}
.tb b.lb{display:block}
.tb td i{font-family:var(--vt-font-mono);font-size:7pt;letter-spacing:.1em;text-transform:uppercase;
  color:var(--vt-dim);font-style:normal}
.tb .num{font-family:var(--vt-font-mono);font-size:11pt;white-space:nowrap;width:22mm}

.flag{border-left:3px solid var(--vt-flag);background:var(--vt-flag-bg);padding:4mm 5mm;
  font-size:8.5pt;margin-top:5mm;line-height:1.5}
.flag>b:first-child{display:block;font-family:var(--vt-font-mono);font-size:7pt;letter-spacing:.16em;
  text-transform:uppercase;color:var(--vt-flag);margin-bottom:1.5mm}
.flag--ask{border-left-color:var(--vt-ink);background:var(--vt-tint)}
.flag--ask b{color:var(--vt-ink)}

/* ---------- 20 vs 21 ---------- */
.vs{display:grid;grid-template-columns:1fr;gap:2px;background:var(--vt-line);
  border:1px solid var(--vt-line)}
.vs figure{margin:0;background:var(--vt-paper);padding:6mm}
.zoom{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--vt-line);
  border:1px solid var(--vt-line);margin-bottom:6mm}
.zoom figure{margin:0;background:var(--vt-paper);padding:5mm;text-align:center}
.zoom span{display:block;background:var(--vt-tint);margin-bottom:3mm}
.zoom img{width:100%%;height:38mm;object-fit:contain;display:block}
.zoom b{display:block;font-family:var(--vt-font-mono);font-size:7.5pt;letter-spacing:.16em}
.zoom i{font-style:normal;font-size:8pt;color:var(--vt-muted)}
.vs span{display:block;background:var(--vt-tint);padding:7mm;margin-bottom:4mm}
.vs img{width:100%%;height:22mm;object-fit:contain;display:block}
.vs figure>b{display:block;font-family:var(--vt-font-mono);font-size:8pt;letter-spacing:.16em;margin-bottom:2mm}
.vs i{font-style:normal;font-size:9pt;color:var(--vt-muted)}

/* ---------- không nên ---------- */
.dont{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:var(--vt-line);
  border:1px solid var(--vt-line);margin-top:2mm}
.dont figure{margin:0;background:var(--vt-paper);padding:5mm;text-align:center}
.dont-box--photo{background-size:cover;background-position:50%% 30%%}
.dont-box{display:block;height:40mm;background:var(--vt-tint);
  padding:9mm 7mm;margin-bottom:3mm;overflow:hidden}
.dont img{width:100%%;height:22mm;object-fit:contain;display:block}
.dont b{font-size:8.5pt;font-weight:500;color:var(--vt-muted)}
.dont figure::before{content:"\\00d7";display:block;font-family:var(--vt-font-mono);
  color:var(--vt-sale);font-size:12pt;line-height:1;margin-bottom:2mm}

/* ---------- ô màu ---------- */
.sws{display:grid;grid-template-columns:repeat(8,1fr);gap:2px;background:var(--vt-line);
  border:1px solid var(--vt-line);margin-top:2mm}
.sw{background:var(--vt-paper);padding:4mm 3mm}
.sw-c{display:block;height:56mm;margin-bottom:3mm;border:1px solid var(--vt-line)}
.sw>b{display:block;font-size:8.5pt}
.sw code{display:block;font-family:var(--vt-font-mono);font-size:6.6pt;color:var(--vt-muted);margin-top:1mm}
.sw i{display:block;font-family:var(--vt-font-mono);font-size:6.6pt;color:var(--vt-dim);
  font-style:normal;margin-top:1mm}

.accent-now{border:1px solid var(--vt-line);padding:7mm;text-align:center}
.accent-now span{display:block;height:74mm;margin-bottom:4mm}
.accent-now>b{display:block;font-family:var(--vt-font-mono);font-size:8pt;letter-spacing:.16em;
  text-transform:uppercase}
.accent-now code{display:block;font-family:var(--vt-font-mono);font-size:12pt;margin:2mm 0}
.accent-now i{font-size:8.5pt;color:var(--vt-muted)}

.pinks{display:grid;grid-template-columns:repeat(3,1fr);gap:3mm}
.pk span{display:block;height:30mm;margin-bottom:2mm}
.pk code{display:block;font-family:var(--vt-font-mono);font-size:7.5pt}
.pk i{display:block;font-family:var(--vt-font-mono);font-size:6.6pt;color:var(--vt-dim);font-style:normal}
.pinkshot{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.pinkshot img{width:100%%;display:block;border:1px solid var(--vt-line)}

.iri{height:82mm;margin:2mm 0 6mm;background:
  radial-gradient(46%% 58%% at 22%% 28%%,var(--vt-iri-1),transparent 62%%),
  radial-gradient(52%% 46%% at 78%% 36%%,var(--vt-iri-2),transparent 64%%),
  radial-gradient(44%% 52%% at 58%% 78%%,var(--vt-iri-3),transparent 62%%),
  radial-gradient(60%% 60%% at 12%% 88%%,var(--vt-iri-4),transparent 66%%),var(--vt-ink)}

/* ---------- chữ ---------- */
.fonts>div{padding:7mm 0;border-bottom:1px solid var(--vt-line)}
.fonts .k{margin-bottom:2mm}
.fd{font-family:var(--vt-font-display);font-weight:800;font-size:32pt;letter-spacing:-.035em;
  line-height:1;margin:0}
.fp{font-size:13pt;line-height:1.45;max-width:60ch;margin:0}
.fm{font-family:var(--vt-font-mono);font-size:13pt;letter-spacing:.04em;margin:0}

.ladder{margin-top:2mm}
.ld{display:grid;grid-template-columns:44mm 1fr;gap:6mm;align-items:baseline;
  padding:3mm 0;border-bottom:1px solid var(--vt-line)}
.ld-m code{font-family:var(--vt-font-mono);font-size:8pt;display:block}
.ld-m i{font-family:var(--vt-font-mono);font-size:6.6pt;color:var(--vt-dim);font-style:normal}
.ld-d{font-family:var(--vt-font-display);font-weight:800;text-transform:uppercase;
  letter-spacing:-.035em;line-height:1;white-space:nowrap;overflow:hidden}

/* ---------- bố cục ---------- */
.hair{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:var(--vt-line);
  border:1px solid var(--vt-line)}
.hair div{background:var(--vt-paper);padding:14mm 4mm;font-family:var(--vt-font-mono);
  font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--vt-muted);text-align:center}
.btns{display:flex;gap:4mm;margin:2mm 0 4mm}
.bt{display:inline-block;padding:3.4mm 8mm;border-radius:999px;border:1px solid var(--vt-ink);
  background:var(--vt-ink);color:var(--vt-paper);font-family:var(--vt-font-mono);
  font-size:7.5pt;letter-spacing:.15em;text-transform:uppercase}
.bt--g{background:transparent;color:var(--vt-ink)}

/* ---------- ảnh ---------- */
.shots{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--vt-line);
  border:1px solid var(--vt-line);margin-bottom:6mm}
.shots figure{margin:0;background:var(--vt-paper)}
.shots img{width:100%%;height:78mm;object-fit:cover;display:block}

/* ---------- hai thời kỳ ---------- */
.eras{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--vt-line);
  border:1px solid var(--vt-line);margin-top:2mm}
.era{background:var(--vt-paper);padding:8mm}
.era--dark{background:var(--vt-ink);color:var(--vt-on-dark)}
.era--dark .k{color:var(--vt-on-dark-muted)}
.era-sw{display:flex;gap:2px;margin-bottom:5mm}
.era-sw span{flex:1;height:24mm;border:1px solid var(--vt-line)}
.era ul{margin:0;padding:0;list-style:none}
.era li{padding:2.6mm 0;border-top:1px solid var(--vt-line);font-size:9pt}
.era--dark li{border-top-color:var(--vt-on-dark-line)}
.era li:first-child{border-top:0}

/* ---------- cần gì ---------- */
.needs{display:grid;grid-template-columns:repeat(2,1fr);gap:7mm 10mm;margin-top:8mm}
.needs>div{border-top:2px solid var(--vt-ink);padding-top:4mm}
.nm{font-family:var(--vt-font-mono);font-size:7.5pt;letter-spacing:.2em;color:var(--vt-dim)}
.needs>div>b{display:block;font-family:var(--vt-font-display);font-weight:800;text-transform:uppercase;
  font-size:14pt;letter-spacing:-.025em;margin:2mm 0}
.needs i{font-style:normal;font-size:9pt;color:var(--vt-muted)}
.end{margin-top:8mm;font-family:var(--vt-font-mono);font-size:9pt;letter-spacing:.16em;
  text-transform:uppercase}
</style></head><body>
%(pages)s
</body></html>
"""


def to_pdf(html_path):
    exe = next((b for b in BROWSERS if os.path.isfile(b)), None)
    if not exe:
        print('Khong tim thay Chrome/Edge. Mo file HTML roi Ctrl+P > Save as PDF.')
        return None
    if os.path.exists(OUT_PDF):
        os.remove(OUT_PDF)
    url = 'file:///' + html_path.replace('\\', '/').replace(' ', '%20')
    cmd = [exe, '--headless=new', '--disable-gpu', '--no-sandbox',
           '--no-pdf-header-footer', '--print-to-pdf-no-header',
           '--virtual-time-budget=20000',
           '--print-to-pdf=' + OUT_PDF, url]
    subprocess.run(cmd, capture_output=True, timeout=180)
    return OUT_PDF if os.path.exists(OUT_PDF) else None


if __name__ == '__main__':
    h = build_html()
    print('HTML  %s' % os.path.relpath(h, ROOT))
    p = to_pdf(h)
    if p:
        print('PDF   %s  (%.1f MB)' % (os.path.relpath(p, ROOT),
                                       os.path.getsize(p) / 1048576.0))
    else:
        sys.exit(1)
