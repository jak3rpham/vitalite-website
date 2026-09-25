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

from theme_fonts import font_url

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
<!-- Bản demo cho portfolio. KHÔNG được để công cụ tìm kiếm lập chỉ mục:
     nó mang đúng tên và giá thật của cửa hàng, index vào là cạnh tranh
     từ khoá với chính vitalite.io.vn và dẫn khách vào chỗ không mua được. -->
<meta name="robots" content="noindex, nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="%(fonts)s">
<link rel="stylesheet" href="theme/style.css">
<link rel="stylesheet" href="preview-bar.css">
</head>
<body class="%(body_class)s">

<div class="vtpv-bar">
  <strong>DEMO</strong>
  <span>Bản dựng tĩnh để xem giao diện · sản phẩm và giá là thật, nhưng <b>không bán được ở đây</b></span>
  <a href="https://vitalite.io.vn" rel="noopener">Cửa hàng thật →</a>
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
                        fonts=font_url(),
                        theme_color='#0A0A0A' if tone == 'dark' else '#FFFFFF')
            + header(active, tone) + body + footer())


# ---------------------------------------------------------------------------
# Thẻ sản phẩm GIẢ
#
# 🔴 CATALOG DƯỚI ĐÂY LÀ THẬT. Không có [PLACEHOLDER] nào nữa.
#
# Trước 25/09/2026 chỗ này dựng lưới GIẢ vì site chưa nhập sản phẩm. Nhưng dữ
# liệu thật đã có sẵn từ 12/09 và nằm rải ở ba file:
#
#   reference/BRAND_FACTS_OBSERVED.md §3  — giá đọc trực tiếp từ Shopee
#   deliverables/woo/NHAP-SAN-PHAM.md §3  — tên, màu, vải, fit, print (user chốt 12/09)
#   deliverables/woo/product-images/      — 16 ảnh thật, đủ trước+sau × 2 màu × 4 SP
#
# Nên bản xem trước không cần bịa gì cả. Mọi con số dưới đây truy được về một
# trong ba nguồn trên. CLAUDE.md §2 cấm bịa tên/giá/chất liệu — luật đó vẫn
# nguyên, ta chỉ thôi không cần lách nó nữa.
#
# 🔴 KHÔNG CÓ GIÁ GẠCH NGANG. Shopee hiện -14%/-16%, nhưng NHAP-SAN-PHAM §3.0
# ghi rõ giá gốc CHƯA ĐỌC ĐƯỢC (trang shop chặn danh sách, đòi đăng nhập).
# Tính ngược 276.100 ÷ 0,84 = 328.690 là BỊA. Nên ở đây hiện ĐÚNG MỘT GIÁ —
# giá đang bán. Thiếu fact thì bỏ hẳn, không suy ra.
#
# Mỗi sản phẩm là MỘT thẻ mang nhiều màu, không phải mỗi màu một thẻ. Đó là
# mô hình WooCommerce đã chốt (variation), và cũng là lý do v2.6.0 làm chấm màu.
# ---------------------------------------------------------------------------

# Tên màu → hex. Chép y theo vt_color_hex() trong inc/helpers.php.
# Lệch bảng này là chấm màu trên bản xem trước khác production.
COLOR_HEX = {
    'Black': '#0A0A0A',
    'White': '#FFFFFF',
    'Pure White': '#FFFFFF',
    'Grey': '#B8B8BC',
    'Cream': '#EFE7D2',
}

IMG = 'theme/products/%s'

CATALOG = [
    dict(slug='iconic', name='ICONIC', cat='T-Shirts',
         prices=[282680],
         colors=[('Black', 'graffiti-blue-black'), ('White', 'graffiti-blue-white')]),
    dict(slug='pink-graffiti', name='Pink Graffiti', cat='T-Shirts',
         # Hai màu KHÁC GIÁ trên Shopee: đen 276.100 (-16%), trắng 282.680 (-14%).
         # Woo hiện khoảng giá cho sản phẩm biến thể, nên thẻ cũng phải hiện khoảng.
         prices=[276100, 282680],
         colors=[('Black', 'pink-graffiti-black'), ('White', 'pink-graffiti-white')]),
    dict(slug='porsche', name='Need Money For Porsche', cat='T-Shirts',
         prices=[282680],
         colors=[('Black', 'porsche-black'), ('White', 'porsche-white')]),
    dict(slug='moments-hoodie', name="The Moments Boxy Hoodie", cat='Outerwear',
         prices=[599100],
         colors=[('Grey', 'moments-hoodie-grey'), ('Pure White', 'moments-hoodie-pure-white')]),
]


def vnd(n):
    """1234567 -> '1.234.567 ₫'. Dấu chấm phân nhóm, đúng quy ước VN."""
    return '{:,}'.format(int(n)).replace(',', '.') + '&nbsp;₫'


def price_html(prices):
    """Chép theo markup WooCommerce trả về từ get_price_html()."""
    lo, hi = min(prices), max(prices)
    amt = '<span class="woocommerce-Price-amount amount">%s</span>'
    if lo == hi:
        return amt % vnd(lo)
    return (amt % vnd(lo)) + ' – ' + (amt % vnd(hi))


def card(p):
    """Chép theo template-parts/product-card.php của theme v2.6.2.

    Ba thứ phải khớp bản thật, nếu không bản xem trước nói dối:
      · .vt-card-media là <div>, KHÔNG phải <a> — <a> lồng <a> là HTML hỏng
      · chấm màu dùng <button data-vt-img> và bọc trong .is-interactive,
        vì site.js (bản THẬT, copy nguyên) bắt đúng selector đó
      · ảnh mặt sau là ảnh cấp SẢN PHẨM, chỉ có cho màu đầu tiên
    """
    first = p['colors'][0][1]
    sizes = ''.join('<a href="product.html?c=%s&s=%s">%s</a>' % (p['slug'], s, s)
                    for s in ('S', 'M', 'L'))
    dots = []
    for cname, base in p['colors']:
        dots.append(
            '<button type="button" class="vt-card-swatch" style="background: %s"'
            ' data-vt-img="%s" title="%s">'
            '<span class="screen-reader-text">%s</span></button>'
            % (COLOR_HEX.get(cname, '#DDDDE1'), IMG % (base + '-front.webp'), cname, cname))
    return """
<article class="vt-card product">
  <div class="vt-card-media">
    <a class="vt-card-media-link" href="product.html?c=%(slug)s" tabindex="-1" aria-hidden="true"></a>
    <img class="vt-card-front" src="%(f)s" alt="" width="600" height="600" loading="lazy" decoding="async">
    <img class="vt-card-back" src="%(b)s" alt="" width="600" height="600" loading="lazy" decoding="async">
    <span class="vt-card-quick">%(sizes)s</span>
  </div>
  <div class="vt-card-body">
    <h3 class="vt-card-title"><a href="product.html?c=%(slug)s">%(name)s</a></h3>
    <div class="vt-card-price">%(price)s</div>
    <div class="vt-card-swatches is-interactive" aria-label="Available colours">%(dots)s</div>
  </div>
</article>""" % dict(slug=p['slug'], name=p['name'],
                     f=IMG % (first + '-front.webp'), b=IMG % (first + '-back.webp'),
                     sizes=sizes, price=price_html(p['prices']), dots=''.join(dots))


def grid(items, featured=False):
    return ('<div class="vt-grid%s">%s</div>'
            % (' vt-grid--featured' if featured else '',
               ''.join(card(p) for p in items)))


def by_cat(cat):
    return [p for p in CATALOG if p['cat'] == cat]


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


def home(images):
    return ''.join([
        hero(),
        '<section class="vt-section"><div class="vt-wrap">',
        section_head('01', 'Featured', 'T-Shirts', VIEW_ALL),
        grid(by_cat('T-Shirts'), featured=True),
        '</div></section>',
        section_collection(),
        section_gallery(images),
        section_iridescent(),
        '<section class="vt-section"><div class="vt-wrap">',
        section_head('04', 'Outerwear', 'Heavyweight', VIEW_ALL),
        grid(by_cat('Outerwear')),
        '</div></section>',
        section_services(),
    ])


def shop():
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
    <span class="vt-mono" style="color: var(--vt-muted);">Sort by latest</span></div>
  %(grid)s
</div></div>""" % dict(n=len(CATALOG), grid=grid(CATALOG))


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

    # 16 ảnh sản phẩm THẬT — nguồn cho mọi thẻ trong CATALOG.
    # Cùng bộ file mà deliverables/woo/NHAP-SAN-PHAM.md §3 dặn upload lên
    # Media Library, nên thẻ ở đây dùng đúng ảnh sẽ chạy trên production.
    prod_src = os.path.join(ROOT, 'deliverables', 'woo', 'product-images')
    prod_out = os.path.join(theme_out, 'products')
    os.makedirs(prod_out)
    if os.path.isdir(prod_src):
        for f in sorted(os.listdir(prod_src)):
            if f.endswith('.webp'):
                shutil.copy2(os.path.join(prod_src, f), os.path.join(prod_out, f))

    # Mockup — CHƯA bỏ được: fragment PDP/cart vẫn trỏ vào chúng qua relink().
    # Gỡ nốt khi PDP dùng ảnh thật.
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


def real_pdp(html):
    """Thay ảnh mockup + số BỊA trong `pdp.html` bằng dữ liệu thật.

    🔴 VÌ SAO SỬA Ở ĐÂY CHỨ KHÔNG SỬA `pdp.html`.
    Prototype đó tự khai trong comment rằng 697.000₫ là SUY RA (599.100 / 0,86),
    giữ lại để duyệt bố cục khối giá lúc có sale. Với một file nội bộ, có nhãn
    rõ ràng, đó là lựa chọn hợp lệ — và vẫn cần, vì không có nó thì không ai
    duyệt được layout <del> + phần trăm giảm.

    Nhưng bản demo này ĐƯA RA CÔNG KHAI dưới đúng tên brand. Một con số suy ra
    hiển thị như giá gạch thật ở đó không còn là ghi chú nội bộ nữa — nó là bịa
    giá, đúng thứ CLAUDE.md §2 cấm. Nên demo hiện ĐÚNG MỘT GIÁ.

    Tách ở tầng build giữ được cả hai: prototype còn nguyên công dụng,
    bản công khai không mang số nào không đọc được từ Shopee.
    """
    M = '../../mockup-all/webp/%s.webp'
    P = '../../../woo/product-images/%s.webp'   # relink() không đụng, sẽ đổi ở dưới

    # Gallery hoodie: 4 ô mockup -> đúng 4 ảnh thật (trước/sau × 2 màu),
    # khớp luôn hai swatch Grey / Pure White đã có sẵn trong fragment.
    for mock, real in (('13', 'moments-hoodie-grey-front'),
                       ('14', 'moments-hoodie-grey-back'),
                       ('15', 'moments-hoodie-pure-white-front'),
                       ('16', 'moments-hoodie-pure-white-back'),
                       ('1',  'graffiti-blue-black-front'),
                       ('5',  'pink-graffiti-black-front'),
                       ('9',  'porsche-black-front')):
        html = html.replace(M % mock, 'theme/products/%s.webp' % real)

    # Giá gạch + % giảm: cả hai đều suy ra từ 599.100. Gỡ hẳn.
    html = re.sub(r'\s*<del>697\.000&#8363;</del>', '', html)
    html = re.sub(r'\s*<span class="vpd-off">&#8722;14%</span>', '', html)

    # Sản phẩm liên quan: 280.000₫ không khớp giá thật nào (thật: 276.100 / 282.680).
    # 'Starlight' có trên IG nhưng KHÔNG có trên Shopee — không có giá, không có
    # ảnh nào xác minh được. Thay bằng SKU thật đã có đủ cả hai.
    for name, newname, price in (
            ('The Iconic Tee', 'ICONIC', '282.680&#8363;'),
            ('Pink Graffiti Tee', 'Pink Graffiti', '276.100&#8363; – 282.680&#8363;'),
            ('Starlight Tee', 'Need Money For Porsche', '282.680&#8363;')):
        html = html.replace(
            '<p class="vpd-card-name">%s</p><p class="vpd-card-price">280.000&#8363;</p>' % name,
            '<p class="vpd-card-name">%s</p><p class="vpd-card-price">%s</p>' % (newname, price))

    # Tiêu đề khối: 'More from The Moments' mà liệt kê 3 áo thun dòng khác là sai.
    html = html.replace('More from The Moments', 'More from VITALITÉ')

    # Badge 'Sale' đi kèm giá gạch. Gỡ giá gạch mà giữ badge là nói có giảm giá
    # nhưng không cho thấy giảm từ đâu — khách không kiểm được, và đó là kiểu
    # nhãn giảm giá mà luật bảo vệ người tiêu dùng soi đầu tiên.
    html = re.sub(r'\s*<span class="vpd-tag vpd-tag--sale">Sale</span>', '', html)

    # ---- Ba ô cam nội bộ. Cả ba đều ĐÃ LỖI THỜI, không chỉ "không nên công khai".
    #
    # Chúng trỏ vào CAU-HOI-CHO-BRAND.md, mà CLAUDE.md §7 đã khai tử file đó từ
    # 30/08: "những gì brand không trả lời là KHÔNG CÓ, không phải chờ trả lời".
    # Hai trong ba ô hỏi những thứ brand ĐÃ trả lời ngày 29/08.

    # 1. Shipping & returns — đã có fact thật, điền vào thay vì xoá trắng.
    #    Nguồn: CLAUDE.md §5. Không nêu tên hãng cho chặng quốc tế: đơn đi Mỹ là
    #    hàng xách tay theo lô, ghi "FedEx" là sai fact.
    ship_real = """<dl class="vpd-spec">
            <div><dt>Việt Nam</dt><dd>SPX · 30.000₫<br>Miễn phí từ 3 áo</dd></div>
            <div><dt>Thời gian</dt><dd>Nội thành 1 ngày<br>Tỉnh 1–3 ngày</dd></div>
            <div><dt>COD</dt><dd>Có<br>chỉ nội địa</dd></div>
            <div><dt>Hoa Kỳ</dt><dd>1–2 tuần<br>phân phối nội địa Mỹ</dd></div>
            <div><dt>Đổi trả</dt><dd>5 ngày · 1 lần/đơn<br>khách chịu ship 2 chiều</dd></div>
            <div><dt>Không đổi</dt><dd>Hàng sale<br>và hàng tặng kèm</dd></div>
          </dl>"""
    html = re.sub(r'<div class="vpd-flag">\s*<b>Chưa có dữ liệu vận chuyển</b>[\s\S]*?</div>',
                  ship_real, html)

    # 2. Số đo hoodie — KHÔNG có thật, và cũng không được bịa (CLAUDE.md §2:
    #    "size/fit là vùng rủi ro pháp lý"). Nên gỡ HẲN cả khối lẫn link trỏ tới nó.
    #    Đây đúng là hành vi của theme thật: inc/woocommerce.php:222 chỉ in bảng
    #    số đo cho category `t-shirts`, hoodie không có bảng. Bỏ hẳn khối này là
    #    KHỚP production, không phải né tránh.
    html = re.sub(r'\s*<details id="size">[\s\S]*?</details>', '', html)
    html = html.replace('<span>Size</span><a href="#size">Size guide</a>', '<span>Size</span>')
    return html


def real_cart(html):
    """Giỏ hàng mẫu: thay giá bịa 280.000₫ bằng giá thật, tính lại tổng.

    Giá thật của ICONIC là 282.680₫ (BRAND_FACTS_OBSERVED §3), không phải
    280.000₫ — số tròn đó không khớp SKU nào. Sửa giá thì phải sửa cả dòng
    thành tiền và tổng, nếu không màn giỏ hàng cộng sai ngay trước mắt người xem.

      282.680 × 2 = 565.360        (trước: 280.000 × 2 = 560.000)
      599.100 + 565.360 = 1.164.460  (trước: 1.159.100)

    Giỏ đang có 3 áo nên freeship nội địa đã kích hoạt (VT_FREE_SHIP_MIN_QTY = 3
    trong inc/woocommerce.php) — vì thế tổng bằng đúng tạm tính, không cộng ship.
    """
    for old, new in (('280.000', '282.680'), ('560.000', '565.360'),
                     ('1.159.100', '1.164.460')):
        html = html.replace(old + '&#8363;', new + '&#8363;')
    for mock, real in (('1', 'graffiti-blue-black-front'),
                       ('13', 'moments-hoodie-grey-front')):
        html = html.replace('../../mockup-all/webp/%s.webp' % mock,
                            'theme/products/%s.webp' % real)

    # 🔴 `.vwc-flag` là ghi chú NỘI BỘ được in thẳng ra trang, không phải comment
    # nên strip_comments() không với tới. Ba khối, nội dung kiểu "Chưa có phí ship
    # — xem câu 5 đến 16 trong CAU-HOI-CHO-BRAND.md". Trên prototype để duyệt thì
    # đúng chỗ; trên bản công khai thì vừa lộ trạng thái dự án, vừa trỏ vào một
    # file không ai ngoài đọc được, lại còn SAI: shipping đã chốt từ 29/08
    # (SPX, 30k, freeship từ 3 áo — CLAUDE.md §5).
    # `class="vwc-flag"` có khối kèm thêm style inline, nên khớp theo tiền tố
    # chứ không khớp đúng dấu `>` — thiếu chỗ này là sót đúng một ô ở màn 3.
    html = re.sub(r'\s*<div class="vwc-flag"[^>]*>[\s\S]*?</div>', '', html)
    return html


# Comment HTML là ghi chú nội bộ: lý do kỹ thuật, số đã biết là suy ra, chỗ còn
# nợ. Trên bản nội bộ chúng đáng giá. Trên bản công khai chúng vừa lộ ghi chú
# vừa nặng thêm. `docs/make-pages.py` đã cắt từ 31/08 (c315e60), đây làm y vậy.
RE_COMMENT = re.compile(r'<!--(?!\[if)(?!<!)[\s\S]*?-->')


def strip_comments(html):
    return RE_COMMENT.sub('', html)


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
        html = strip_comments(shell(title, body, active, tone, body_class))
        io.open(os.path.join(OUT, name), 'w', encoding='utf-8', newline=NL).write(html)
        made.append((name, len(html)))

    # Trang chủ — body.vt-banner-top: header đè lên hero, đúng như front-page.php
    write('index.html', 'Home', home(images),
          active='', tone='dark', body_class='vt-banner-top')
    write('shop.html', 'Shop All', shop(),
          active='shop.html', tone='dark', body_class='vt-banner-top')

    for name, title, src, active, screens in FRAGMENTS:
        if not os.path.exists(src):
            print('  BO QUA (khong co file): %s' % name)
            continue
        body = read_fragment(src)
        if name == 'product.html':
            body = real_pdp(body)
        if screens:
            body = woo_screens(body, set(screens))
            body = real_cart(body)
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
