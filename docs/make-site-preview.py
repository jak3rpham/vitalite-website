# -*- coding: utf-8 -*-
"""Sinh BẢN XEM TRƯỚC TOÀN SITE, bấm qua lại được, chạy trên localhost.

    python3 docs/make-site-preview.py
    python3 -m http.server 8000 -d deliverables/preview/site

🔴 ĐÂY KHÔNG PHẢI SITE THẬT, VÀ KHÔNG CHỨNG MINH ĐƯỢC THEME CHẠY.
Theme thật là PHP + WooCommerce. Máy này không có PHP, nên bản này chỉ dựng lại
phần NHÌN THẤY ĐƯỢC bằng HTML tĩnh. Nó trả lời được "bố cục và điều hướng có ổn
không", KHÔNG trả lời được "template có render đúng trên hosting không".
Câu thứ hai chỉ deploy mới trả lời được — xem deliverables/setup/DEPLOY.md.

CÁI GÌ LÀ THẬT, CÁI GÌ LÀ GIẢ
  THẬT   style.css lấy thẳng từ theme (COPY, không chép tay lại — nên không bao
         giờ lệch với production), toàn bộ ảnh/video/gallery/frame thật,
         site.js thật, và 12 fragment HTML đã duyệt.
  GIẢ    thẻ sản phẩm. Site CHƯA CÓ SẢN PHẨM NÀO. Mọi thẻ đều gắn nhãn
         [PLACEHOLDER] và badge "PH" theo đúng CLAUDE.md §2.
         Ảnh mockup là ảnh thật, nhưng tên và giá thì KHÔNG.

VÌ SAO HEADER/FOOTER Ở ĐÂY LÀ BẢN CHÉP
  Không có PHP thì không chạy được `site-header.php`. Markup dưới đây chép theo
  nó. Đây là NGUỒN SỰ THẬT THỨ HAI và nó sẽ trôi khỏi bản thật — đúng loại lỗi
  đã phải archive `header-woocommerce.php` vì nó.
  Giới hạn thiệt hại: file này KHÔNG mang CSS riêng dòng nào. Style đến từ đúng
  một chỗ là style.css của theme. Lệch markup thì thấy ngay bằng mắt; lệch màu
  thì không, nên chỗ nguy hiểm hơn đã được chặn.
  Sửa `site-header.php` hay `site-footer.php` thì sửa cả đây.
"""
import io
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(ROOT, 'repo', 'vitalite-website', 'vitalite-theme', 'vitalite-theme-2')
OUT = os.path.join(ROOT, 'deliverables', 'preview', 'site')
NL = '\n'

BRAND = 'VITALITÉ'
EMAIL = 'vitalitevn@gmail.com'          # inc/helpers.php vt_contact_info()

ICONS = {
    'bag':    '<path d="M6 7h12l1 13H5L6 7Z"/><path d="M9 7V5a3 3 0 0 1 6 0v2"/>',
    'menu':   '<path d="M3 6h18M3 12h18M3 18h18"/>',
    'close':  '<path d="M5 5l14 14M19 5L5 19"/>',
    'arrow':  '<path d="M4 12h15M13 6l6 6-6 6"/>',
}


def icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            '%s</svg>' % ICONS[name])


# ---------------------------------------------------------------------------
# Bản đồ trang. Thứ tự ở đây quyết định thứ tự trong nav.
# ---------------------------------------------------------------------------

NAV_MAIN = [
    ('shop.html',       'Shop All'),
    ('product.html',    'Product'),
    ('collection.html', 'Collection'),
    ('about.html',      'About'),
]

FOOT_SHOP = [('shop.html', 'Shop All'), ('shop.html', 'New Arrivals'),
             ('shop.html', 'T-Shirts'), ('shop.html', 'Outerwear'), ('shop.html', 'Sale')]
FOOT_SUPPORT = [('size-guide.html', 'Size Guide'), ('shipping.html', 'Shipping'),
                ('returns.html', 'Returns'), ('contact.html', 'Contact'), ('faq.html', 'FAQ'),
                ('account.html', 'My Account')]
FOOT_LEGAL = [('payment.html', 'Payment'), ('privacy.html', 'Privacy'), ('terms.html', 'Terms'),
              ('complaints.html', 'Complaints'), ('seller-information.html', 'Seller Information')]
SOCIAL = [('IG', 'https://www.instagram.com/vitalitevn/'),
          ('TIKTOK', 'https://www.tiktok.com/@vitalitevn'),
          ('SHOPEE', 'https://shopee.vn/vitalitevn')]


# ---------------------------------------------------------------------------
# Khung trang
# ---------------------------------------------------------------------------

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s — %(brand)s</title>
<meta name="theme-color" content="%(theme_color)s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Archivo+Expanded:wght@800&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="theme/style.css">
<link rel="stylesheet" href="preview-bar.css">
</head>
<body class="%(body_class)s">

<div class="vtpv-bar">
  <strong>BẢN XEM TRƯỚC TĨNH</strong>
  <span>Không phải site thật · không có PHP/WooCommerce · thẻ sản phẩm là <b>[PLACEHOLDER]</b></span>
  <a href="index.html">Trang chủ</a>
</div>
"""


def header(active, tone=''):
    """Chép theo template-parts/site-header.php. Không mang CSS riêng.

    `tone` = tone của banner đầu trang ('dark' | 'light' | ''). Giống bản thật,
    trạng thái đầu được render SẴN ở đây chứ không chờ JS — nếu chờ, header
    trắng sẽ loé lên một nhịp rồi mới trong suốt."""
    cls = 'vt-header'
    if tone:
        cls += ' is-transparent'
    if tone == 'light':
        cls += ' is-light-bg'
    nav = ''.join(
        '<li%s><a href="%s">%s</a></li>' % (
            ' class="current-menu-item"' if href == active else '', href, label)
        for href, label in NAV_MAIN)
    mob = ''.join('<a href="%s">%s</a>' % (h, l) for h, l in NAV_MAIN)
    return """
<a class="vt-skip" href="#vt-main">Skip to content</a>

<header id="vt-header" class="%(cls)s" data-banner-tone="%(tone)s">
  <div class="vt-header-left">
    <button type="button" class="vt-burger" aria-label="Open menu" aria-expanded="false"
            aria-controls="vt-mobile-nav" data-vt-menu-open>%(menu)s</button>
    <a class="vt-brand" href="index.html" rel="home">
      <img src="theme/assets/vitalite-wordmark-trim.png" alt="%(brand)s"
           class="vt-brand-mark" width="140" height="20" decoding="async">
    </a>
    <nav class="vt-nav-wrap" aria-label="Primary"><ul class="vt-nav">%(nav)s</ul></nav>
  </div>

  <div class="vt-header-right">
    <div class="vt-lang">
      <a href="#" class="is-active" lang="en">EN</a>
      <span class="vt-lang-sep" aria-hidden="true">/</span>
      <a href="#" lang="vi">VI</a>
    </div>
    <a class="vt-util vt-util--search" href="#">Search</a>
    <a class="vt-util vt-util--account" href="account.html">Account</a>
    <a class="vt-cart" href="cart.html">%(bag)s
      <span class="screen-reader-text">Cart</span>
      <span class="vt-cart-count is-empty" aria-hidden="true">0</span>
    </a>
  </div>
</header>

<div id="vt-mobile-nav" class="vt-mobile-nav" hidden>
  <button type="button" class="vt-mobile-close" aria-label="Close menu" data-vt-menu-close>%(close)s</button>
  %(mob)s
  <div class="vt-mobile-foot">
    <a href="#">Search</a><a href="account.html">Account</a>
    %(social)s
  </div>
</div>

<main id="vt-main" class="vt-main">
""" % dict(menu=icon('menu'), close=icon('close'), bag=icon('bag'),
           brand=BRAND, nav=nav, mob=mob, cls=cls, tone=tone,
           social=''.join('<a href="%s" target="_blank" rel="noopener me">%s</a>' % (u, l)
                          for l, u in SOCIAL))


def col(title, links):
    return ('<div><div class="vt-footer-col-title">%s</div><div class="vt-footer-links">%s</div></div>'
            % (title, ''.join('<a href="%s">%s</a>' % (h, l) for h, l in links)))


def footer():
    """Chép theo template-parts/site-footer.php."""
    return """</main>

<footer class="vt-footer">
  <div class="vt-wrap">
    <div class="vt-footer-grid">
      <div class="vt-footer-brand">
        <img src="theme/assets/vitalite-wordmark-trim.png" alt="%(brand)s" class="vt-footer-logo"
             width="140" height="20" decoding="async">
        <p class="vt-footer-desc">Streetwear made in Vietnam.</p>
      </div>
      %(shop)s
      <div><div class="vt-footer-col-title">Support</div><div class="vt-footer-links">%(sup)s
        <a href="mailto:%(email)s">%(email)s</a></div></div>
      %(legal)s
      <div><div class="vt-footer-col-title">Follow</div><div class="vt-footer-links">%(social)s</div></div>
    </div>
    <div class="vt-footer-bottom">
      <span>© 2026 %(brand)s ®</span>
      <span class="vt-mono">Saigon, Vietnam</span>
    </div>
  </div>
</footer>

<script src="theme/assets/js/site.js" defer></script>
</body>
</html>
""" % dict(brand=BRAND, email=EMAIL,
           shop=col('Shop', FOOT_SHOP),
           sup=''.join('<a href="%s">%s</a>' % (h, l) for h, l in FOOT_SUPPORT),
           legal=col('Legal', FOOT_LEGAL),
           social=''.join('<a href="%s" target="_blank" rel="noopener me">%s</a>' % (u, l)
                          for l, u in SOCIAL))


def shell(title, body, active='', tone='', body_class=''):
    return (HEAD % dict(title=title, brand=BRAND, body_class=body_class,
                        theme_color='#0A0A0A' if tone == 'dark' else '#FFFFFF')
            + header(active, tone) + body + footer())


# ---------------------------------------------------------------------------
# Thẻ sản phẩm GIẢ
#
# 🔴 Site chưa có sản phẩm nào. Bản thật render empty-state, không render lưới.
# Ở đây cố tình dựng lưới GIẢ vì mục đích của bản xem trước là DUYỆT BỐ CỤC —
# hai section trống thì không duyệt được gì.
#
# CLAUDE.md §2: "Placeholder chỉ chấp nhận khi gắn nhãn [PLACEHOLDER] rõ ràng."
# Nên mỗi thẻ mang badge "PH", tên bắt đầu bằng [PLACEHOLDER], giá là 0.000.000 ₫.
# Không có tên SKU thật, không có giá thật, không có màu thật ở đây.
# Ảnh mockup là ảnh THẬT — chúng chỉ minh hoạ tỷ lệ khung, không gắn với SKU nào.
# ---------------------------------------------------------------------------

# Độ dài tên khác nhau là CÓ CHỦ Ý: tên dài mới lộ ra chỗ thẻ bị vỡ dòng.
PH_NAMES = [
    'Sample Tee',
    'Sample Heavyweight Boxy Hoodie In Washed Black',
    'Sample Tee Two',
    'Sample Longsleeve',
    'Sample Cap',
    'Sample Oversized Tee With A Deliberately Long Name',
    'Sample Shorts',
    'Sample Jacket',
]


def card(i, mock_count):
    front = 'theme/mockups/%d.webp' % ((i % mock_count) + 1)
    back = 'theme/mockups/%d.webp' % (((i + 1) % mock_count) + 1)
    sizes = ''.join('<a href="product.html">%s</a>' % s for s in ('S', 'M', 'L'))
    return """
<article class="vt-card">
  <div class="vt-card-media">
    <a class="vt-card-media-link" href="product.html" tabindex="-1" aria-hidden="true"></a>
    <span class="vt-card-badge vtpv-ph">PH</span>
    <img class="vt-card-front" src="%(f)s" alt="" width="600" height="600" loading="lazy" decoding="async">
    <img class="vt-card-back" src="%(b)s" alt="" width="600" height="600" loading="lazy" decoding="async">
    <span class="vt-card-quick">%(sizes)s</span>
  </div>
  <div class="vt-card-body">
    <h3 class="vt-card-title"><a href="product.html">[PLACEHOLDER] %(name)s</a></h3>
    <div class="vt-card-price"><span class="woocommerce-Price-amount">0.000.000&nbsp;₫</span></div>
  </div>
</article>""" % dict(f=front, b=back, sizes=sizes, name=PH_NAMES[i % len(PH_NAMES)])


def grid(n, mock_count, featured=False):
    return ('<div class="vt-grid%s">%s</div>'
            % (' vt-grid--featured' if featured else '',
               ''.join(card(i, mock_count) for i in range(n))))


def section_head(number, kicker, title, right):
    eyebrow = ('<p class="vt-eyebrow">%s — %s</p>' % (number, kicker)) if number else ''
    return ('<div class="vt-section-head"><div>%s<h2 class="vt-title">%s</h2></div>%s</div>'
            % (eyebrow, title, right))


VIEW_ALL = '<a class="vt-link vt-mono" href="shop.html">View all →</a>'


# ---------------------------------------------------------------------------
# HERO — chép theo template-parts/hero.php. Ba slide, copy nguyên văn từ IG.
# ---------------------------------------------------------------------------

SLIDES = [
    dict(tone='dark', label='The Iconic', tag='The Iconic · T-Shirt',
         title='Even in chaos,<br>you are alive.',
         sub='Two sides of the same street culture.',
         cta='Shop All', url='shop.html',
         img='theme/assets/hero-poster.webp', video=True),
    dict(tone='dark', label='The Moments', tag='The Moments · Boxy Hoodie',
         title='Heavy in weight.<br>Unmatched in fit.',
         sub='500+ GSM heavyweight cotton blend. Signature boxy fit.',
         cta='Outerwear', url='shop.html',
         img='theme/assets/cb-poster.webp', video=False),
    dict(tone='light', label='Archive', tag='Archive',
         title='Old things<br>still shine.',
         sub='Earlier drops, still in stock.',
         cta='T-Shirts', url='shop.html',
         img='theme/assets/slide-03.webp', video=False),
]


def hero():
    out = ['<section class="vt-hero" id="vt-hero" data-vt-hero data-tone="dark" data-duration="7000"'
           ' aria-roledescription="carousel" aria-label="Featured campaigns">']
    for i, s in enumerate(SLIDES):
        vid = ''
        if s['video']:
            # KHÔNG có `loop` — khớp với template-parts/hero.php. Clip phải KẾT
            # THÚC thì sự kiện `ended` mới bắn, và đó là thứ chuyển sang slide 2.
            vid = ('<video id="vt-hero-video" class="vt-slide-video" muted playsinline '
                   'preload="none" tabindex="-1" aria-hidden="true" '
                   'data-src-webm="theme/video/hero-1280.webm" '
                   'data-src-mp4="theme/video/hero-1280.mp4"></video>')
        out.append("""
  <div class="vt-slide%(act)s" data-tone="%(tone)s" role="group" aria-roledescription="slide"
       aria-label="%(n)d / %(t)d — %(label)s"%(hid)s>
    <div class="vt-slide-media">
      <img src="%(img)s" alt="" width="1920" height="1080" %(load)s decoding="async">%(vid)s
    </div>
    <div class="vt-slide-scrim" aria-hidden="true"></div>
    <div class="vt-slide-content">
      <p class="vt-slide-tag">%(tag)s</p>
      <%(h)s class="vt-slide-title">%(title)s</%(h)s>
      <div class="vt-slide-foot">
        <p class="vt-slide-sub">%(sub)s</p>
        <a class="vt-btn vt-slide-cta" href="%(url)s"%(tab)s>%(cta)s %(arrow)s</a>
      </div>
    </div>
  </div>""" % dict(
            act=' is-active' if i == 0 else '', tone=s['tone'], n=i + 1, t=len(SLIDES),
            label=s['label'], hid='' if i == 0 else ' aria-hidden="true"',
            img=s['img'], vid=vid,
            load='fetchpriority="high" loading="eager"' if i == 0 else 'loading="lazy"',
            tag=s['tag'], h='h1' if i == 0 else 'p', title=s['title'], sub=s['sub'],
            url=s['url'], tab='' if i == 0 else ' tabindex="-1"',
            cta=s['cta'], arrow=icon('arrow')))

    dots = ''.join("""
    <button type="button" class="vt-hero-dot%(act)s" role="tab" data-vt-slide="%(i)d"
            aria-selected="%(sel)s">
      <span class="vt-hero-track"><span class="vt-hero-bar"></span></span>
      <span class="vt-hero-dot-label">%(num)02d — %(label)s</span>
    </button>""" % dict(act=' is-active' if i == 0 else '', i=i, num=i + 1,
                        sel='true' if i == 0 else 'false', label=s['label'])
        for i, s in enumerate(SLIDES))
    out.append('<div class="vt-hero-nav" role="tablist" aria-label="Choose slide">%s</div>' % dots)
    out.append('<div class="vt-hero-sentinel" data-vt-hero-sentinel data-vt-header-sentinel'
               ' aria-hidden="true"></div>')
    out.append('</section>')
    return ''.join(out)


# ---------------------------------------------------------------------------
# Các section còn lại của trang chủ
# ---------------------------------------------------------------------------

def section_collection():
    """Chép theo template-parts/section-collection.php.
    Copy nguyên văn Instagram 25/07/2026 — không tự nghĩ câu nào."""
    return """
<section class="vt-section"><div class="vt-bleed"><div class="vt-collection">
  <div class="vt-collection-body">
    <p class="vt-collection-eyebrow">02 — New Collection</p>
    <div>
      <h2 class="vt-collection-title">The<br>Moments</h2>
      <p class="vt-collection-text">Crafted with 500+ GSM premium cotton blend for a structured
        silhouette that holds its shape all day.</p>
      <a class="vt-btn vt-btn--on-dark" href="shop.html">Shop outerwear %s</a>
    </div>
  </div>
  <div class="vt-collection-media">
    <img src="theme/assets/collection-01.webp" alt="Model wearing VITALITÉ in Saigon"
         width="1050" height="1400" loading="lazy" decoding="async">
  </div>
</div></div></section>""" % icon('arrow')


GALLERY_SPANS = ['vt-g--2x2', 'vt-g--1x1', 'vt-g--1x2', 'vt-g--1x1',
                 'vt-g--2x1', 'vt-g--1x1', 'vt-g--1x1', 'vt-g--4x1']


def section_gallery(images):
    """Chép theo template-parts/section-gallery.php. Ảnh THẬT từ assets/gallery/."""
    figs = ''.join(
        '<figure class="vt-g %s"><img src="theme/assets/gallery/%s" alt="" loading="lazy"'
        ' decoding="async"></figure>' % (GALLERY_SPANS[i % 8], name)
        for i, name in enumerate(images))
    aside = '<span class="vt-mono" style="color: var(--vt-muted);">#VITALITEDAILY</span>'
    return ('<section class="vt-section vt-gallery-section"><div class="vt-wrap">%s</div>'
            '<div class="vt-bleed"><div class="vt-gallery">%s</div></div></section>'
            % (section_head('03', 'Gallery', 'On The Street', aside), figs))


def section_iridescent():
    """Chép theo template-parts/section-iridescent.php.
    Copy nguyên văn Instagram 29/07/2026."""
    return """
<section class="vt-iri vt-section" data-vt-iri>
  <div class="vt-iri-layer" aria-hidden="true"></div>
  <div class="vt-wrap"><div class="vt-iri-content" style="max-width: 24ch;">
    <p class="vt-mono" style="color: var(--vt-on-dark-muted); margin: 0 0 14px;">Saigon</p>
    <h2 class="vt-display" style="color: var(--vt-on-dark); font-size: var(--vt-t-2xl);">
      Finding harmony within chaos</h2>
    <p style="margin-top: 28px;">
      <a class="vt-btn vt-btn--on-dark" href="shop.html">Shop All %s</a></p>
  </div></div>
</section>""" % icon('arrow')


def section_services():
    """Chép theo template-parts/section-services.php.
    Ba mục, mỗi mục có nguồn. KHÔNG thêm mục nào không có nguồn."""
    return """
<section class="vt-section vt-section--tight"><div class="vt-wrap"><div class="vt-services">
  <div><p class="vt-services-title">Made in Vietnam</p><p>Cut and printed in Saigon.</p></div>
  <div><p class="vt-services-title">Exchanges</p><p>One exchange per order, within 5 days of
    delivery.<br><a class="vt-link" href="returns.html">Read more →</a></p></div>
  <div><p class="vt-services-title">Worldwide shipping</p><p>We ship internationally from
    Saigon.<br><a class="vt-link" href="shipping.html">Read more →</a></p></div>
</div></div></section>"""


def home(mock_count, images):
    return ''.join([
        hero(),
        '<section class="vt-section"><div class="vt-wrap">',
        section_head('01', 'Featured', 'T-Shirts', VIEW_ALL),
        grid(7, mock_count, featured=True),
        '</div></section>',
        section_collection(),
        section_gallery(images),
        section_iridescent(),
        '<section class="vt-section"><div class="vt-wrap">',
        section_head('04', 'Outerwear', 'Heavyweight', VIEW_ALL),
        grid(4, mock_count),
        '</div></section>',
        section_services(),
    ])


def shop(mock_count):
    """Shop archive. Chép theo woocommerce/archive-product.php:
    banner đầu trang (tràn viền) + breadcrumb + toolbar + lưới."""
    return """
<section class="vt-iri vt-pagebanner" data-vt-iri data-tone="dark">
  <div class="vt-iri-layer" aria-hidden="true"></div>
  <div class="vt-wrap vt-pagebanner-inner">
    <div class="vt-pagebanner-text">
      <p class="vt-pagebanner-eyebrow">Shop</p>
      <h1 class="vt-pagebanner-title">Shop All</h1>
    </div>
  </div>
  <div class="vt-banner-sentinel" data-vt-header-sentinel aria-hidden="true"></div>
</section>
<div class="vt-woo vt-woo--bare"><div class="vt-wrap">
  <nav class="woocommerce-breadcrumb" aria-label="Breadcrumb">
    <a href="index.html">Home</a> <span aria-hidden="true">/</span> Shop All</nav>
  <div class="vt-section-head"><div><p class="vt-eyebrow">%(n)d products</p></div>
    <span class="vt-mono" style="color: var(--vt-muted);">[PLACEHOLDER]</span></div>
  %(grid)s
</div></div>""" % dict(n=12, grid=grid(12, mock_count))


# ---------------------------------------------------------------------------
# CSS của thanh báo "đây là bản xem trước"
#
# Đây là CSS DUY NHẤT mà script này tự viết. Nó chỉ style thanh cảnh báo và
# badge PH — hai thứ KHÔNG tồn tại trên site thật. Không đụng vào class vt-* nào,
# nên không có nguy cơ bản xem trước hiển thị khác production.
# ---------------------------------------------------------------------------

# 🔴 `body{margin:0}` KHÔNG phải chuyện thẩm mỹ, nó là lỗi thật đã bắt được.
#
# Trên site thật, `inc/enqueue.php` nạp style.css của Hello Elementor (theme cha)
# TRƯỚC style.css của child, và bản cha mới là chỗ reset margin. Theme cha là
# theme tải từ WordPress.org, không nằm trong repo này, nên bản xem trước không
# có nó → body giữ margin mặc định 8px của trình duyệt.
#
# Hậu quả không phải "lệch 8px cho đẹp": hero bị đẩy xuống 8px, nên
# `.vt-hero-sentinel` ở đáy hero rơi RA NGOÀI màn hình (819 > 812 trên iPhone).
# IntersectionObserver báo không giao nhau → site.js gỡ `is-transparent` →
# header trắng đè lên hero tối, sai hẳn so với production.
#
# Nên dòng này là bản thay thế tối thiểu cho reset của theme cha, không phải
# style riêng của bản xem trước.
BAR_CSS = """body{margin:0}
.vtpv-bar{position:fixed;left:0;right:0;bottom:0;z-index:9999;
  display:flex;gap:12px;align-items:center;justify-content:center;
  height:30px;padding:0 14px;background:#B45309;color:#fff;white-space:nowrap;
  font:500 11px/1 'JetBrains Mono',ui-monospace,Menlo,monospace;letter-spacing:.03em}
.vtpv-bar>*{overflow:hidden;text-overflow:ellipsis}
.vtpv-bar b{color:#FEF6E7}
.vtpv-bar a{color:#fff;text-decoration:underline;text-underline-offset:3px;flex:none}
body{padding-bottom:30px}
.vt-card-badge.vtpv-ph{background:#B45309;color:#fff}
@media(max-width:900px){.vtpv-bar span{display:none}}
"""


def copy_assets():
    """Copy chứ KHÔNG chép tay. style.css ở đây luôn là bản theme đang dùng."""
    theme_out = os.path.join(OUT, 'theme')
    os.makedirs(theme_out)
    shutil.copy2(os.path.join(THEME, 'style.css'), os.path.join(theme_out, 'style.css'))
    for sub in ('assets', 'video'):
        src = os.path.join(THEME, sub)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(theme_out, sub))

    # Mockup dùng cho thẻ [PLACEHOLDER]
    mock_src = os.path.join(ROOT, 'mockup-all', 'webp')
    mock_out = os.path.join(theme_out, 'mockups')
    os.makedirs(mock_out)
    n = 0
    if os.path.isdir(mock_src):
        for f in sorted(os.listdir(mock_src)):
            if f.endswith('.webp'):
                shutil.copy2(os.path.join(mock_src, f), os.path.join(mock_out, f))
                n += 1

    # Trang About trỏ tuyệt đối vào /wp-content/uploads/seq/0823/ — dựng đúng
    # đường đó trong thư mục phục vụ để chuỗi frame chạy y như trên hosting.
    seq_src = os.path.join(ROOT, 'deliverables', 'scroll-sequence', 'frames', '0823')
    if os.path.isdir(seq_src):
        shutil.copytree(seq_src, os.path.join(OUT, 'wp-content', 'uploads', 'seq', '0823'))

    io.open(os.path.join(OUT, 'preview-bar.css'), 'w', encoding='utf-8', newline=NL).write(BAR_CSS)
    return n


def read_fragment(path):
    return io.open(path, encoding='utf-8').read()


def relink(html):
    """Fragment viết link theo slug WordPress (`/shipping`, `/about`).
    Bản tĩnh chạy bằng file .html nên phải đổi sang tên file."""
    slugs = ['about', 'collection', 'complaints', 'contact', 'faq', 'payment', 'privacy',
             'returns', 'seller-information', 'shipping', 'size-guide', 'terms']
    for s in slugs:
        html = re.sub(r'href="/%s/?"' % re.escape(s), 'href="%s.html"' % s, html)
    # Link động của WordPress/Woo — gom hết về trang tương ứng của bản tĩnh.
    # Bản tĩnh không có query string nên `?collection=` hay `?orderby=` rụng đi;
    # đó là giới hạn đã biết, không phải lỗi.
    html = re.sub(r'href="/shop[^"]*"', 'href="shop.html"', html)
    html = re.sub(r'href="/product-category/[^"]*"', 'href="shop.html"', html)
    html = re.sub(r'href="/product/[^"]*"', 'href="product.html"', html)
    html = re.sub(r'href="/(?:my-account|cart|checkout)[^"]*"', 'href="cart.html"', html)
    html = re.sub(r'href="/"', 'href="index.html"', html)
    # Fragment PDP/cart trỏ ảnh mockup theo đường tương đối tính từ
    # deliverables/woo-templates/. Trong bản tĩnh chúng nằm ở theme/mockups/.
    html = html.replace('../../mockup-all/webp/', 'theme/mockups/')
    return html


def woo_screens(html, keep):
    """Tách `cart-checkout-account.html` thành từng màn.

    Fragment gốc gộp 6 màn vào một file vì nó là PROTOTYPE để duyệt một lượt.
    Nhưng trên site thật chúng là ba trang WordPress riêng (/cart, /checkout,
    /my-account), nên bản xem trước cũng phải tách ra — nếu không bấm
    "Account" ở header lại rơi vào đầu trang Cart, đúng lỗi đã gặp.

    Mốc cắt là chính khối chú thích `MÀN n —` trong file gốc.
    """
    marks = [(m.start(), int(m.group(1)))
             for m in re.finditer(r'<!-- =+\s*\n\s+MÀN (\d+)', html)]
    if not marks:
        return html
    head = html[:marks[0][0]]
    end_all = html.rfind('</div>')
    parts = []
    for i, (pos, num) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else end_all
        if num in keep:
            parts.append(html[pos:end])
    body = ''.join(parts)
    # Mỗi màn mở đầu bằng một `.vwc-sep` để tách nó khỏi màn TRƯỚC. Cắt ra
    # đứng riêng thì cái đầu tiên thành một dải trống vô nghĩa ở đỉnh trang.
    body = re.sub(r'^\s*<div class="vwc-sep"></div>\s*', '', body)
    return head + body + '\n</div>\n'


PAGES_DIR = os.path.join(ROOT, 'deliverables', 'pages-html')
WOO_DIR = os.path.join(ROOT, 'deliverables', 'woo-templates')

# (file ra, tiêu đề, nguồn fragment, active-nav)
FRAGMENTS = [
    ('about.html', 'About', os.path.join(PAGES_DIR, 'about.html'), 'about.html', None),
    ('collection.html', 'Collection', os.path.join(PAGES_DIR, 'collection.html'), 'collection.html', None),
    ('product.html', 'Product', os.path.join(WOO_DIR, 'pdp.html'), 'product.html', None),
    ('cart.html', 'Cart · Checkout',
     os.path.join(WOO_DIR, 'cart-checkout-account.html'), '', (1, 2, 3, 4)),
    ('account.html', 'Account',
     os.path.join(WOO_DIR, 'cart-checkout-account.html'), 'account.html', (5, 6)),
]
for _s, _t in [('shipping', 'Shipping'), ('returns', 'Returns'), ('size-guide', 'Size Guide'),
               ('faq', 'FAQ'), ('contact', 'Contact'), ('payment', 'Payment'),
               ('privacy', 'Privacy'), ('terms', 'Terms'), ('complaints', 'Complaints'),
               ('seller-information', 'Seller Information')]:
    FRAGMENTS.append((_s + '.html', _t, os.path.join(PAGES_DIR, _s + '.html'), '', None))


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    mock_count = copy_assets()
    gal_dir = os.path.join(THEME, 'assets', 'gallery')
    images = sorted(f for f in os.listdir(gal_dir)) if os.path.isdir(gal_dir) else []

    made = []

    def write(name, title, body, active='', tone='', body_class=''):
        html = shell(title, body, active, tone, body_class)
        io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline=NL).write(html)
        made.append((name, len(html)))

    # Trang chủ — body.vt-banner-top: header đè lên hero, đúng như front-page.php
    write('index.html', 'Home', home(mock_count, images),
          active='', tone='dark', body_class='vt-banner-top')
    write('shop.html', 'Shop All', shop(mock_count),
          active='shop.html', tone='dark', body_class='vt-banner-top')

    for name, title, src, active, screens in FRAGMENTS:
        if not os.path.exists(src):
            print('  BO QUA (khong co file): %s' % name)
            continue
        body = read_fragment(src)
        if screens:
            body = woo_screens(body, set(screens))
        # Trang About mở bằng chuỗi frame nền ĐEN cao 500vh. Header trắng đè lên
        # đó cắt trang làm hai ngay giây đầu. Khớp với vt_top_banner_tone()
        # trong inc/helpers.php, chỗ 'about' đã được khai là trang banner tối.
        tone = 'dark' if name == 'about.html' else ''
        cls = 'vt-banner-top' if tone else ''
        write(name, title, relink(body), active=active, tone=tone, body_class=cls)

    return made


if __name__ == '__main__':
    rows = build()
    print()
    for name, size in rows:
        print('  %-26s %8d' % (name, size))
    print('\n%d trang -> %s' % (len(rows), os.path.relpath(OUT, ROOT)))
    print('Chay:  python3 -m http.server 8000 -d %s' % os.path.relpath(OUT, ROOT))
