"""
Sinh HTML cho các trang tĩnh của VITALITÉ, dán thẳng vào widget HTML của Elementor.

VÌ SAO LÀ SCRIPT CHỨ KHÔNG PHẢI 9 FILE HTML VIẾT TAY
    Chín trang dùng CHUNG một hệ thiết kế. Viết tay thì sửa một chi tiết phải sửa
    chín chỗ, và chỉ cần quên một chỗ là bộ trang lệch nhau. Ở đây CSS nằm đúng
    một bản, nội dung nằm đúng một bản, HTML là thứ sinh ra.

CHẠY
    cd "E:\\Vitalite website"; python docs/make-pages.py
    -> ghi ra deliverables/pages-html/*.html

DÁN VÀO ĐÂU
    Elementor -> thêm widget "HTML" -> dán TOÀN BỘ nội dung file.
    Không cần thêm gì khác. Mỗi file tự mang CSS của nó, scope trong .vtp
    nên không rò ra phần còn lại của trang.

MÀU VÀ FONT
    Ăn theo biến CSS của theme (--vt-ink, --vt-font-display…) và có giá trị dự phòng.
    Theme đổi màu nhấn thì các trang này đổi theo, không phải sửa lại.
"""
import io
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'deliverables', 'pages-html')

# ---------------------------------------------------------------- CSS dùng chung
CSS = """
.vtp{
  --p-ink:var(--vt-ink,#0A0A0A);
  --p-paper:var(--vt-paper,#FFFFFF);
  --p-line:var(--vt-line,#E4E4E6);
  --p-strong:var(--vt-line-strong,#C9C9CE);
  --p-muted:var(--vt-muted,#6B6B70);
  --p-tint:var(--vt-tint,#F7F7F8);
  --p-flag:#B45309;
  --p-flagbg:#FEF6E7;
  --p-mono:var(--vt-font-mono,"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace);
  --p-disp:var(--vt-font-display,"Archivo Expanded","Archivo",system-ui,sans-serif);
  color:var(--p-ink);
  font-size:16px;line-height:1.7;
  -webkit-font-smoothing:antialiased;

  /* 🔴 FRAGMENT PHAI TU SON NEN, DUNG GO.
     Khoi nay la mot manh dan vao trang khac. Khong tu dat nen thi no an nen
     cua trang chu nha: mo thang file .html trong trinh duyet dark mode la ra
     nen den + chu den, khong doc duoc gi. Tren WordPress cung vo y het neu
     section Elementor chua no duoc dat nen toi.
     `color-scheme:light` de input, select, scrollbar khong bi trinh duyet tu
     dao mau o dark mode. */
  background:var(--p-paper);
  color-scheme:light;
}
.vtp *,.vtp *::before,.vtp *::after{box-sizing:border-box;}

/* 🔴 `:where()` KHONG PHAI TRANG TRI, DUNG DOI VE SELECTOR THUONG.
   Ban cu viet `.vtp p,.vtp ul,...{margin:0}` -- do dac hieu (0,1,1), CAO HON
   moi class nhu `.vtp-lede{margin-top:20px}` (0,1,0). Ket qua: TOAN BO khoang
   cach giua cac doan trong 9 trang chinh sach bi nuot, computed margin = 0px.
   `:where()` dong gop do dac hieu BANG 0 nen moi class thang no.
   Kiem lai: getComputedStyle($('.vtp-lede')).marginTop === '20px' */
:where(.vtp) :where(p,ul,ol,table,h1,h2,h3){margin:0;}

/* ---- Đầu trang: eyebrow đánh số + tiêu đề lớn + đường kẻ đen ---- */
.vtp-head{padding-bottom:26px;border-bottom:1px solid var(--p-ink);}
.vtp-eyebrow{
  font-family:var(--p-mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--p-muted);margin-bottom:16px;
}
.vtp-title{
  font-family:var(--p-disp);font-weight:800;text-transform:uppercase;
  font-size:clamp(30px,5vw,60px);line-height:1.02;letter-spacing:-.03em;
}
.vtp-lede{margin-top:20px;max-width:62ch;font-size:clamp(16px,1.3vw,19px);color:var(--p-muted);}
.vtp-stamp{
  margin-top:22px;font-family:var(--p-mono);font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--p-muted);
}

/* ---- Khung do rong ----
   9 trang nay dan vao section Elementor full-width. Khong chan lai thi tren man
   1920 cot noi dung rong ~1700px trong khi doan van chi 68ch (~640px), bo trong
   ca nghin pixel ben phai.
   KHONG mau thuan voi quyet dinh "FULL-WIDTH" o CLAUDE.md muc 5: quyet dinh do noi
   ve ngon ngu layout trang BRAND (hero, tieu de section, luoi). Chin trang nay la
   TAI LIEU phap ly, do dai dong la yeu to de doc duoc. */
.vtp-head,.vtp-body{max-width:1180px;margin-inline:auto;}

/* ---- Thân trang: mục lục dính bên trái, nội dung bên phải ---- */
.vtp-body{display:grid;grid-template-columns:210px 1fr;gap:clamp(28px,5vw,72px);margin-top:clamp(32px,4vw,56px);}
.vtp-toc{position:sticky;top:100px;align-self:start;}
.vtp-toc p{
  font-family:var(--p-mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--p-muted);padding-bottom:10px;border-bottom:1px solid var(--p-line);margin-bottom:12px;
}
.vtp-toc a{
  display:block;padding:7px 0;font-size:13.5px;text-decoration:none;color:var(--p-muted);
  border-bottom:1px solid var(--p-line);transition:color .18s;
}
.vtp-toc a:hover{color:var(--p-ink);}
.vtp-content{min-width:0;}

.vtp-sec{padding-top:clamp(26px,3vw,40px);}
.vtp-sec:first-child{padding-top:0;}
.vtp-sec + .vtp-sec{margin-top:clamp(26px,3vw,40px);border-top:1px solid var(--p-line);}
.vtp-sec h2{
  font-family:var(--p-disp);font-weight:800;text-transform:uppercase;
  font-size:clamp(19px,2vw,26px);letter-spacing:-.01em;line-height:1.15;margin-bottom:18px;
}
.vtp-sec h3{font-size:15px;font-weight:700;letter-spacing:.02em;margin:26px 0 10px;}
.vtp-sec p{max-width:68ch;}
.vtp-sec p + p{margin-top:14px;}
.vtp-sec > p:first-of-type{margin-top:0;}

/* ---- Danh sách ---- */
.vtp-list{list-style:none;padding:0;margin-top:14px;}
.vtp-list li{position:relative;padding-left:22px;margin-top:9px;max-width:68ch;}
.vtp-list li::before{content:"";position:absolute;left:0;top:.72em;width:9px;height:1px;background:var(--p-ink);}
.vtp-yes li::before,.vtp-no li::before{width:auto;height:auto;top:0;font-family:var(--p-mono);font-size:13px;font-weight:600;line-height:1.7;}
.vtp-yes li::before{content:"+";color:#166534;}
.vtp-no li::before{content:"\\00d7";color:var(--vt-sale,#C2452D);}

/* ---- Hai cột được / không được ---- */
.vtp-split{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--p-line);margin-top:20px;}
.vtp-split > div{background:var(--p-paper);padding:20px;}
.vtp-split h3{margin-top:0;}

/* ---- Bảng hairline, cuộn ngang trên màn hẹp ---- */
.vtp-scroll{overflow-x:auto;margin-top:18px;-webkit-overflow-scrolling:touch;}
.vtp table{width:100%;border-collapse:collapse;min-width:440px;}
.vtp th,.vtp td{padding:13px 14px;text-align:left;border-bottom:1px solid var(--p-line);vertical-align:top;}
.vtp thead th{
  font-family:var(--p-mono);font-size:10.5px;font-weight:500;letter-spacing:.16em;
  text-transform:uppercase;color:var(--p-muted);border-bottom-color:var(--p-ink);white-space:nowrap;
}
.vtp tbody th{font-family:var(--p-mono);font-weight:600;white-space:nowrap;}

/* ---- Ô cảnh báo: chỗ CHƯA CÓ DỮ LIỆU, không được publish khi còn ---- */
.vtp-flag{
  margin-top:18px;padding:16px 18px;background:var(--p-flagbg);
  border-left:3px solid var(--p-flag);font-size:14.5px;
}
.vtp-flag b{
  display:block;font-family:var(--p-mono);font-size:10.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--p-flag);margin-bottom:7px;
}
.vtp-flag ul{list-style:none;padding:0;margin:8px 0 0;}
.vtp-flag li{padding-left:16px;position:relative;margin-top:5px;}
.vtp-flag li::before{content:"?";position:absolute;left:0;color:var(--p-flag);font-family:var(--p-mono);font-weight:700;}

/* ---- Ghi chú nhạt ---- */
.vtp-note{margin-top:18px;padding:15px 18px;background:var(--p-tint);border-left:3px solid var(--p-strong);font-size:14.5px;color:var(--p-muted);}
.vtp-note strong{color:var(--p-ink);}

/* ---- Nút pill ---- */
.vtp-cta{margin-top:26px;display:flex;gap:12px;flex-wrap:wrap;}
.vtp-btn{
  display:inline-flex;align-items:center;gap:9px;padding:13px 24px;border-radius:999px;
  border:1px solid var(--p-ink);background:var(--p-ink);color:var(--p-paper);
  font-family:var(--p-mono);font-size:11px;font-weight:500;letter-spacing:.14em;
  text-transform:uppercase;text-decoration:none;transition:background .18s,color .18s;
}
.vtp-btn:hover{background:transparent;color:var(--p-ink);}
.vtp-btn--ghost{background:transparent;color:var(--p-ink);}
.vtp-btn--ghost:hover{background:var(--p-ink);color:var(--p-paper);}

.vtp-content a:not(.vtp-btn){color:inherit;text-decoration:underline;text-underline-offset:3px;}

/* ================= Riêng cho trang ABOUT =================
   Trang thương hiệu, không phải trang chính sách. Chữ to hơn, nhịp thưa hơn,
   và có vài khối chỉ dùng đúng ở đây. */
.vtp-manifesto{
  font-family:var(--p-disp);font-weight:800;text-transform:uppercase;
  font-size:clamp(26px,3.6vw,50px);line-height:1.06;letter-spacing:-.03em;
  max-width:16ch;margin:0;
}
.vtp-manifesto span{color:var(--p-muted);}
.vtp-said{
  margin-top:18px;font-family:var(--p-mono);font-size:10.5px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--p-muted);
}
/* Dải số — hairline, không phải thẻ bo góc */
.vtp-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--p-line);margin-top:24px;border:1px solid var(--p-line);}
.vtp-stats > div{background:var(--p-paper);padding:20px 16px;}
.vtp-stats b{display:block;font-family:var(--p-disp);font-weight:800;font-size:clamp(22px,2.6vw,34px);line-height:1;letter-spacing:-.02em;}
.vtp-stats span{display:block;margin-top:9px;font-family:var(--p-mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--p-muted);}
/* Hai thời kỳ */
.vtp-era{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--p-line);margin-top:22px;}
.vtp-era > div{background:var(--p-paper);padding:22px;}
.vtp-era > div:first-child{background:var(--p-tint);}
.vtp-era em{
  display:block;font-style:normal;font-family:var(--p-mono);font-size:10px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--p-muted);margin-bottom:12px;
}
.vtp-era strong{display:block;font-family:var(--p-disp);font-weight:800;text-transform:uppercase;font-size:clamp(16px,1.6vw,21px);letter-spacing:-.01em;margin-bottom:10px;}
/* Khối spec theo đúng khuôn brand tự viết trên Instagram */
.vtp-spec{margin-top:20px;border-top:1px solid var(--p-ink);}
.vtp-spec div{display:flex;gap:18px;padding:12px 0;border-bottom:1px solid var(--p-line);}
.vtp-spec dt{flex:0 0 108px;font-family:var(--p-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--p-muted);padding-top:2px;}
.vtp-spec dd{margin:0;font-weight:600;}

/* ---- Mobile: bỏ mục lục dính, xếp một cột ---- */
@media (max-width:900px){
  .vtp-body{grid-template-columns:1fr;gap:26px;}
  .vtp-toc{position:static;}
  .vtp-toc a{display:inline-block;border:1px solid var(--p-line);border-radius:999px;padding:6px 13px;margin:0 6px 6px 0;font-size:12px;}
  .vtp-split{grid-template-columns:1fr;}
  .vtp-era{grid-template-columns:1fr;}
  .vtp-stats{grid-template-columns:1fr 1fr;}
}
"""


def flag(title, items):
    """Ô cảnh báo cho dữ liệu còn thiếu. Cố tình chói mắt — publish nhầm là sai fact."""
    lis = ''.join('<li>%s</li>' % i for i in items)
    return ('<div class="vtp-flag"><b>%s</b>'
            '<p style="margin:0">Chưa có dữ liệu. Điền xong mới được publish trang này.</p>'
            '<ul>%s</ul></div>') % (title, lis)


def table(headers, rows, tbody_th=True):
    th = ''.join('<th scope="col">%s</th>' % h for h in headers)
    trs = []
    for r in rows:
        if tbody_th:
            cells = '<th scope="row">%s</th>' % r[0] + ''.join('<td>%s</td>' % c for c in r[1:])
        else:
            cells = ''.join('<td>%s</td>' % c for c in r)
        trs.append('<tr>%s</tr>' % cells)
    return ('<div class="vtp-scroll"><table><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>') % (th, ''.join(trs))


def ul(items, kind=''):
    cls = 'vtp-list' + (' ' + kind if kind else '')
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s</li>' % i for i in items))


MAIL = '<a href="mailto:vitalitevn@gmail.com">vitalitevn@gmail.com</a>'
IG = '<a href="https://www.instagram.com/vitalitevn/" target="_blank" rel="noopener">Instagram</a>'

# ---------------------------------------------------------------- Nội dung trang
PAGES = []


def page(slug, number, kicker, title, lede, sections, stamp='Last updated 23 August 2026'):
    PAGES.append(dict(slug=slug, number=number, kicker=kicker, title=title,
                      lede=lede, sections=sections, stamp=stamp))


# ---- 1. RETURNS -------------------------------------------------------------
page('returns', '01', 'Policy', 'Returns &amp; Exchanges',
     'One exchange per order, within 5 days of delivery. Read this before you order. '
     'Knowing your size costs nothing, an exchange costs shipping.',
     [
      ('window', 'The window', """
<p>You have <strong>5 days from the day your order is delivered</strong> to tell us you want an exchange.
Once we accept the request, your item must reach us within <strong>7 days</strong>.</p>
<p>Each order can be exchanged <strong>once</strong>.</p>
""" + table(['Step', 'Deadline'],
            [['Tell us', 'Within 5 days of delivery'],
             ['Item reaches us', 'Within 7 days of approval'],
             ['We inspect and reply', 'Within 3 working days of receipt']])),

      ('required', 'What we need from you', """
<p>Four things. Miss any one and we cannot process the exchange.</p>
""" + ul([
        '<strong>An unbroken unboxing video.</strong> One continuous take, no cuts, no blur, '
        'starting before the parcel is opened so the seal is visible. This is the only evidence '
        'that settles a dispute about the condition of an item on arrival, especially for '
        'international orders, where neither of us can inspect the parcel together.',
        '<strong>The item unworn and unwashed</strong>, with no smell of perfume, smoke or detergent.',
        '<strong>All tags, labels and packaging intact</strong>, including any free gift.',
        '<strong>Your order number.</strong>'], 'vtp-yes')),

      ('cases', 'When we exchange', """
<div class="vtp-split">
  <div>
    <h3>We exchange</h3>
""" + ul(['Manufacturing fault: stitching, print, fabric',
          'Wrong item, wrong colour or wrong size sent',
          'Item missing from the order',
          'Damage in transit, shown in the unboxing video'], 'vtp-yes') + """
  </div>
  <div>
    <h3>We do not exchange</h3>
""" + ul(['No unboxing video',
          'Worn, washed, stained, deformed or scented',
          'Tags or labels removed',
          'Damage from incorrect washing or storage'], 'vtp-no') + """
  </div>
</div>
""" + flag('Need a decision', [
        'Are sale items and free gifts excluded from exchanges?'])),

      ('shipping-cost', 'Who pays return shipping', """
<p>This depends entirely on whose mistake it was.</p>
""" + table(['Situation', 'Who pays'],
            [['Our fault: faulty item, wrong item sent', '<strong>VITALITÉ pays both ways</strong>'],
             ['You chose the wrong size', 'See note below'],
             ['International orders', 'See note below']]) + """
<div class="vtp-note"><strong>Commercial note for the owner, remove before publishing.</strong>
Both reference brands cover shipping when the fault is theirs, and StressMama covers one leg
even for a plain size swap. The current VITALITÉ policy, customer pays both ways in every case,
is stricter than both, and stricter than the free 15-day return the same customer gets on Shopee.
On an international order, two-way shipping can cost more than the shirt, which turns the right
to exchange into a right nobody can use.</div>
""" + flag('Need a decision', [
        'Size swap: keep "customer pays both ways", or cover one leg?',
        'International exchanges: possible at all, and at what cost?',
        'Return address for exchanges'])),

      ('refunds', 'Refunds', flag('Need a decision', [
        'Does VITALITÉ refund, or exchange only?',
        'If refunds exist: how many working days, and back to which method?'])),

      ('how', 'How to start an exchange', """
<p>Email %s or message us on %s. Include your order number and the unboxing video.</p>
<p>Do not send anything back before we confirm. An unannounced parcel cannot be matched to an order.</p>
<div class="vtp-cta">
  <a class="vtp-btn" href="mailto:vitalitevn@gmail.com">Email us</a>
  <a class="vtp-btn vtp-btn--ghost" href="/size-guide">Size guide</a>
</div>
""" % (MAIL, IG)),
     ])

# ---- 2. SHIPPING ------------------------------------------------------------
page('shipping', '02', 'Policy', 'Shipping',
     'Where we ship, what it costs, how long it takes.',
     [
      ('blocked', 'This page is not ready', """
<div class="vtp-flag"><b>Do not publish yet</b>
<p style="margin:0">Every figure on this page is missing. The structure below is correct.
The numbers are not written because inventing shipping costs and delivery times would be
inventing a contract with the customer.</p></div>
"""),
      ('vietnam', 'Vietnam', """
<p>Shipping inside Vietnam is calculated from the delivery address you enter at checkout.
Pick your province and the cost appears before you pay. There is no separate quote step,
and nothing is added to the total afterwards.</p>
""" + flag('Need data', [
        'Carrier: GHN, GHTK, Viettel Post, J&amp;T?',
        'Fee per region (zone table should follow the carrier&#39;s own regions)',
        'Free-shipping threshold, if any',
        'Delivery time HCMC (reference: competitors quote 1-4 days)',
        'Delivery time provinces (reference: competitors quote 3-7 working days)',
        'Cash on delivery: yes or no?']) + """
<div class="vtp-note"><strong>Ghi chú cho chủ site, xoá trước khi publish.</strong>
Cách cấu hình phía WooCommerce đã phân tích ở <strong>deliverables/woo/SHIPPING-SETUP.md</strong>:
hai cách làm, và một cảnh báo phải đọc TRƯỚC khi nhập sản phẩm hàng loạt.</div>
"""),

      ('international', 'International', """
<p>The website exists to serve customers Shopee cannot reach. This section is the one that
decides whether that is actually possible.</p>
""" + flag('Need data', [
        'Carrier: DHL, FedEx, EMS, Vietnam Post?',
        'Which countries do we ship to?',
        'Cost per zone',
        'Delivery time per zone',
        'Import duty and tax: paid by us (DDP) or by the customer (DDU)?']) + """
<div class="vtp-note"><strong>The number to look at first.</strong>
A shirt sells at roughly 280,000&#8363; (about $11). International shipping typically runs $25-40,
<strong>three times the price of the product</strong>. If that holds, the model does not work at the
current price point, and the answer is a business decision, not a technical one:
bundles, a different international price, or accepting a loss on shipping to buy the customer. This has to be
known <em>before</em> launch, not after.</div>
"""),

      ('processing', 'Order processing', flag('Need data', [
        'How long between order placed and parcel leaving?',
        'Which days do we not ship: Sunday, public holidays, T&#7871;t?'])),

      ('damage', 'Damage in transit', """
<p>Please check the parcel when it is handed to you. Signing for a delivery without noting a
problem is treated as accepting the order in the condition it arrived.</p>
<p>If something is wrong, the unboxing video described in our
<a href="/returns">returns policy</a> is what lets us make a claim with the carrier on your behalf.</p>
"""),
     ])

# ---- 3. PAYMENT -------------------------------------------------------------
page('payment', '03', 'Policy', 'Payment',
     'How you can pay, when we charge, and what currency you are charged in.',
     [
      ('methods', 'Accepted methods', flag('Need data', [
        'Which payment gateways are actually configured in WooCommerce?',
        'Bank transfer: account name, number, bank, branch',
        'Cash on delivery: offered or not?',
        'Do we accept international cards? Which ones?'])),

      ('currency', 'Currency', """
<p>Prices are shown in Vietnamese &#273;&#7891;ng (&#8363;) and include tax.</p>
""" + flag('Need a decision', [
        'Do international customers see prices in their own currency?',
        'If yes: which currencies, and who sets the exchange rate?'])),

      ('when', 'When we charge', """
<p>Payment is taken when the order is placed. An order is only confirmed once payment clears. Until then the items are not reserved.</p>
"""),
      ('security', 'Card security', """
<p>Card details are handled entirely by the payment provider. They never reach our servers and
we never store them.</p>
""" + flag('Need data', ['Name of the payment provider, to state here explicitly'])),
     ])

# ---- 4. SIZE GUIDE ----------------------------------------------------------
page('size-guide', '04', 'Guide', 'Size Guide',
     'All VITALITÉ pieces are unisex. Measurements are taken flat, in centimetres.',
     [
      ('tees', 'T-Shirts', """
<p>Fabric is <strong>250 GSM cotton</strong>, screen printed.</p>
""" + table(['Size', 'Length', 'Width', 'Height', 'Weight'],
            [['S', '70 cm', '55 cm', '155-165 cm', 'under 60 kg'],
             ['M', '73 cm', '58 cm', '160-175 cm', 'under 75 kg'],
             ['L', '76 cm', '61 cm', '175-190 cm', 'under 100 kg']]) + """
<p style="margin-top:16px">Measurements can vary by 2 to 3 cm between production batches.</p>
"""),
      ('outerwear', 'Outerwear', """
<p>Fabric is <strong>500+ GSM heavyweight cotton blend</strong>, signature boxy fit.</p>
""" + flag('Need data', [
        'Measurements for THE MOMENTS BOXY HOODIE: length, width, sleeve']) + """
<div class="vtp-note">Until these exist, the product page deliberately shows no size table for
outerwear. Showing nothing is better than showing a number that turns into a return.</div>
"""),
      ('between', 'Between two sizes?', """
<p>Our fit is boxy by design. If you are between sizes and want a closer fit, size down.</p>
<p>Still not sure? Message us on %s or email %s <strong>before</strong> you order. It is faster
than an exchange, and it costs neither of us shipping.</p>
<div class="vtp-cta">
  <a class="vtp-btn" href="https://www.instagram.com/vitalitevn/" target="_blank" rel="noopener">Ask on Instagram</a>
  <a class="vtp-btn vtp-btn--ghost" href="/returns">Returns policy</a>
</div>
""" % (IG, MAIL)),
     ])

# ---- 5. FAQ -----------------------------------------------------------------
page('faq', '05', 'Help', 'How to Order',
     'Five steps, and the questions we get asked most.',
     [
      ('steps', 'Placing an order', """
<ol class="vtp-list">
<li>Pick your piece, choose colour and size, add it to the bag.</li>
<li>Open the bag and check quantities.</li>
<li>Go to checkout and fill in name, email, address and phone.</li>
<li>Choose a payment method and confirm.</li>
<li>You receive a confirmation email with your order number. Keep it. Every request we handle starts with that number.</li>
</ol>
"""),
      ('change', 'Changing or cancelling an order', """
<p>Contact us within <strong>12 hours</strong> of ordering. After the parcel is handed to the
carrier we can no longer change the address or the contents.</p>
"""),
      ('where', 'Where to buy', """
<p>This website ships worldwide. Inside Vietnam you can also buy from our Shopee store,
which has been running for four years.</p>
<p>We sell on Instagram, Facebook, TikTok and Shopee under <strong>@vitalitevn</strong>.
Anything else is not us.</p>
"""),
      ('care', 'Looking after your piece', """
<p>Wash cold, inside out. Do not tumble dry. Do not iron directly on the print.</p>
<p>Damage from incorrect washing is not covered by the
<a href="/returns">returns policy</a>, so this matters.</p>
"""),
      ('stock', 'Sold out pieces', flag('Need a decision', [
        'Do we restock, or is every drop final?',
        'Is there a back-in-stock notification?'])),
     ])

# ---- 6. PRIVACY -------------------------------------------------------------
page('privacy', '06', 'Legal', 'Privacy Policy',
     'What we collect, why, and who else sees it.',
     [
      ('review', 'Needs review before publishing', """
<div class="vtp-flag"><b>Structure only</b>
<p style="margin:0">The sections below are the ones required, in the order that is standard for
Vietnamese e-commerce. The wording still needs to be checked by whoever is legally responsible
for the business. This is a contract with the customer, not marketing copy.</p></div>
"""),
      ('collect', 'What we collect', """
<p>Only what an order needs: name, email address, delivery address, phone number, and the
contents of your order. Payment card details are handled by the payment provider and never
reach us.</p>
"""),
      ('why', 'Why we collect it', ul([
        'To process, pack and deliver your order',
        'To contact you about that order',
        'To handle exchanges and complaints',
        'To meet record-keeping obligations under Vietnamese law'])),
      ('who', 'Who else sees it', """
<p>Only the parties who need it to complete your order:</p>
""" + ul(['The delivery carrier: name, address, phone',
          'The payment provider: the amount and the order reference']) + """
<p>We do not sell your data. We do not share it with anyone else unless a competent Vietnamese
authority requires it by law.</p>
"""),
      ('cookies', 'Cookies', """
<p>This site uses cookies to keep your bag between pages and to understand which pages people
actually read. You can block them in your browser. The shop will still work, but your bag may
not survive a page reload.</p>
"""),
      ('rights', 'Your rights', """
<p>You can ask us what we hold about you, ask us to correct it, or ask us to delete it. Email %s.</p>
""" % MAIL + flag('Needs specialist confirmation', [
        'Selling to EU customers may bring GDPR obligations. This needs confirming by someone qualified. It is not a question to guess at.'])),
      ('holding', 'How long we keep it', flag('Need a decision', [
        'Retention period for order records',
        'Retention period for accounts that are never used again'])),
     ])

# ---- 7. TERMS ---------------------------------------------------------------
page('terms', '07', 'Legal', 'Terms of Service',
     'The rules that apply when you use this site or place an order.',
     [
      ('review', 'Needs review before publishing', """
<div class="vtp-flag"><b>Structure only</b>
<p style="margin:0">Required sections in standard order. Wording must be approved by whoever is
legally responsible for the business.</p></div>
"""),
      ('scope', 'Scope', """
<p>Using this website means you accept these terms and our
<a href="/privacy">privacy policy</a>. If you do not accept them, please do not use the site.</p>
"""),
      ('accounts', 'Accounts', """
<p>You are responsible for keeping your account details accurate and your password private.
Never enter your VITALITÉ password on any site that is not vitalite.io.vn.</p>
"""),
      ('pricing', 'Prices and orders', """
<p>Prices are in Vietnamese &#273;&#7891;ng and include tax. Stock is limited, and placing an
order is an offer to buy. The sale is complete when we confirm it and payment clears.</p>
<p>If an item is listed at an obviously incorrect price, we may cancel the order and refund
it in full rather than fulfil it.</p>
"""),
      ('ip', 'Intellectual property', """
<p>The VITALITÉ name, the logo, the garment designs, the prints and the photography on this site
belong to VITALITÉ. Reproducing them for commercial use is not permitted.</p>
"""),
      ('liability', 'Limitation of liability', flag('Needs legal review', [
        'This section carries real legal weight and must not be drafted from a template. Have it approved.'])),
      ('law', 'Governing law', """
<p>These terms are governed by the laws of Vietnam.</p>
"""),
     ])

# ---- 8. COMPLAINTS ----------------------------------------------------------
page('complaints', '08', 'Legal', 'Complaints',
     'How to raise a problem, and how long we take to answer.',
     [
      ('channel', 'How to reach us', """
<p>Email %s with your order number and a description of the problem. If it concerns the condition
of an item, attach the unboxing video.</p>
""" % MAIL + flag('Need data', [
        'Which phone number is current? Facebook lists 093 838 14 07, a 2023 post lists 037 963 2222. One of them has to go.',
        'Registered business address for formal complaints'])),
      ('times', 'How long we take', flag('Need a decision', [
        'Deadline to acknowledge a complaint',
        'Deadline to resolve one'])),
      ('escalate', 'If we cannot agree', """
<p>If we cannot reach an agreement, the matter is settled under Vietnamese law, and you retain
your right to refer it to the competent consumer-protection authority.</p>
"""),
     ])

# ---- 9. SELLER INFORMATION --------------------------------------------------
page('seller-information', '09', 'Legal', 'Seller Information',
     'Who you are actually buying from. Required by Vietnamese e-commerce law.',
     [
      ('who', 'The business', """
<div class="vtp-flag"><b>Legally required, currently blank</b>
<p style="margin:0">Vietnamese e-commerce regulation requires the seller&#39;s legal identity to be
visible on the site. The Shopee store shows the brand already trades through a registered entity,
so this is a matter of retrieving the details, not registering anything new.</p></div>
""" + flag('Need data', [
        'Full registered name of the company or household business',
        'Business registration number / tax code',
        'Registered address',
        'Official phone number'])),
      ('contact', 'Contact', """
<p>Email %s &middot; %s</p>
<p>Based in Saigon. All pieces are made in Vietnam.</p>
""" % (MAIL, IG)),
     ])


# ---- 10. CONTACT -----------------------------------------------------------
# Noi dung lay tu deliverables/content/PAGES-CONTENT.md muc 4. Email, IG, FB da
# xac minh o reference/BRAND_FACTS_OBSERVED.md. So dien thoai va phap nhan thi CHUA,
# nen chung nam trong o cam chu khong duoc dien dai.
page('contact', '10', 'Contact', 'Contact',
     'One inbox, one handle. Write to us with your order number and we will pick it up.',
     [
      ('where', 'Where to write', """
<p>Email is the record we work from. Everything to do with an order, an exchange or a complaint
should go there, because it is the only channel where the whole history stays in one place.</p>
<dl class="vtp-spec">
  <div><dt>Email</dt><dd><a href="mailto:vitalitevn@gmail.com">vitalitevn@gmail.com</a></dd></div>
  <div><dt>Instagram</dt><dd><a href="https://www.instagram.com/vitalitevn/" target="_blank" rel="noopener">@vitalitevn</a>, fastest for a quick question</dd></div>
  <div><dt>Facebook</dt><dd><a href="https://www.facebook.com/vitalitevn" target="_blank" rel="noopener">Vitalit&#233;</a></dd></div>
  <div><dt>Based in</dt><dd>Saigon, Vietnam</dd></div>
</dl>
<p style="margin-top:16px">We are <strong>@vitalitevn</strong> on Instagram, Facebook, TikTok and
Shopee. Any other account using this name is not us.</p>
""" + flag('Need data', [
        'Which phone number is current? Facebook lists 093 838 14 07, a 2023 post lists 037 963 2222. Publishing both is worse than publishing neither.',
        'Opening hours, or a stated reply window. Without one, every unanswered message reads as being ignored.'])),

      ('include', 'What to put in the message', """
<p>Four things let us answer on the first reply instead of the third.</p>
""" + ul([
        'Your order number, from the confirmation email',
        'What the piece is, and which size',
        'What is wrong, in one line',
        'Photographs, or the unboxing video if the item arrived damaged',
      ]) + """
<div class="vtp-note"><strong>The unboxing video matters more than it sounds.</strong>
It is the only thing that settles a disagreement about the condition of an item on arrival,
and it cannot be produced after the parcel is open. Film the parcel before you cut it.</div>
"""),

      ('first', 'Answered already', """
<p>Most messages we get are one of these four. The answer is faster on the page than in the inbox.</p>
""" + ul([
        '<a href="/size-guide">Size guide</a>, measurements for every size, taken flat',
        '<a href="/returns">Returns and exchanges</a>, what qualifies and how long you have',
        '<a href="/shipping">Shipping</a>, cost and delivery time',
        '<a href="/faq">How to order</a>, the whole flow from bag to delivery',
      ])),

      ('business', 'The business behind the site', """
<p>Vietnamese e-commerce regulation requires the seller&#39;s legal identity to be published on the
site. Those details live on one page, kept separate so there is a single place to correct them.</p>
<div class="vtp-cta"><a class="vtp-btn vtp-btn--ghost" href="/seller-information">Seller information</a></div>
"""),
     ])


# ---- 11. COLLECTIONS --------------------------------------------------------
# Noi dung THE ICONIC va THE MOMENTS lay nguyen van tu Instagram 07/2026, ghi o
# deliverables/content/PAGES-CONTENT.md muc 6. Bon dong con lai CHUA co caption
# nao dung duoc -> de o cam, KHONG tu viet mo ta.
#
# Ten dong san pham va trang thai lay tu reference/BRAND_ASSETS_AUDIT.md:
#   ICONIC · PINK GRAFFITI · PORSCHE   dang ban tren Shopee
#   STARLIGHT · OLD MONEY              CHUA len Shopee, mockup da co
#
# 🔴 Trang nay CHI publish sau khi da nhap san pham. Moi nut "Shop" o day tro
# toi mot filter pa_collection co that; chua co san pham thi bam vao ra trang rong.
page('collection', '11', 'Shop', 'Collections',
     'Every drop the label has put out, old and new. Nothing here is retired.',
     [
      ('now', 'In production', """
<p>Two lines carry the current direction. The words below are the label&#39;s own, published with
the drop, not written for this page.</p>

<div class="vtp-era">
  <div>
    <em>The Iconic</em>
    <strong>An icon shaped by imperfect lines.</strong>
    <p>An icon shaped by imperfect lines, bold details, and your own way of wearing it.</p>
    <p class="vtp-said">Instagram &middot; 29 July 2026</p>
    <div class="vtp-cta"><a class="vtp-btn vtp-btn--ghost" href="/shop?collection=the-iconic">Shop The Iconic</a></div>
  </div>
  <div>
    <em>The Moments</em>
    <strong>Heavy in weight. Unmatched in fit.</strong>
    <p>500+ GSM cotton blend, cut to a signature boxy fit. The back carries one line:
    <em>it&#39;s the only moment that matters.</em></p>
    <p class="vtp-said">Instagram &middot; 25 July 2026</p>
    <div class="vtp-cta"><a class="vtp-btn vtp-btn--ghost" href="/shop?collection=the-moments">Shop The Moments</a></div>
  </div>
</div>
"""),

      ('archive', 'Still on the shelf', """
<p>Older drops are not retired and not hidden. They sit in the same catalogue, at the same
sizing, and they are still sold.</p>
""" + ul([
        '<strong>Pink Graffiti</strong>, the best seller, over 2,000 sold',
        '<strong>Porsche</strong>, listed as <em>Need Money For Porsche</em>',
        '<strong>Starlight</strong>, shown on Instagram, not yet listed on Shopee',
        '<strong>Old Money</strong>, a varsity longsleeve, not yet released',
      ]) + flag('Need data', [
        'One line of description for each of Pink Graffiti, Porsche, Starlight and Old Money. Question 33 in CAU-HOI-CHO-BRAND.md.',
        'Is Starlight still for sale, and at what price?',
        'Old Money has a mockup but no release date. Show it here, or hold it back?']) + """
<div class="vtp-note"><strong>Ghi chú cho chủ site, xoá trước khi publish.</strong>
Bốn ô trống trên là chỗ CHỜ, không phải chỗ thiếu ý tưởng. Claude không viết mô tả dòng sản phẩm
vì đó là tiếng nói thương hiệu, không phải copy chức năng. Có câu của brand thì thay thẳng vào.</div>
"""),

      ('how', 'How collections work here', """
<p>A collection is not a category. A piece belongs to one product type, a t&#8209;shirt or a piece
of outerwear, and separately to one collection. The two are independent, which is why the shop
lets you filter by either.</p>
<p>Sizing does not change between collections. S, M and L mean the same measurements across every
drop, old and new. The <a href="/size-guide">size guide</a> covers all of them.</p>
"""),
     ])


# ---- ABOUT ------------------------------------------------------------------
# CỐ Ý KHÔNG sinh ở đây. `deliverables/pages-html/about.html` là trang VIẾT TAY:
# nó là trang thương hiệu, có hệ thiết kế riêng (nền tối, váng dầu, marquee,
# hiện dần khi cuộn, đếm số) — không dùng chung khuôn với 9 trang chính sách.
# Chạy script này KHÔNG ghi đè lên about.html.

# ---------------------------------------------------------------- Sinh file
SHELL = """<!-- ============================================================
     VITALITÉ %(title)s
     Dán TOÀN BỘ khối này vào một widget HTML của Elementor.
     Slug trang phải là: %(slug)s
     Sinh tự động bởi docs/make-pages.py. ĐỪNG sửa tay ở đây,
     sửa trong script rồi chạy lại, nếu không lần sau bị ghi đè.
     ============================================================ -->
<div class="vtp">
<style>%(css)s</style>

<header class="vtp-head">
  <p class="vtp-eyebrow">%(number)s &middot; %(kicker)s</p>
  <h1 class="vtp-title">%(title)s</h1>
  <p class="vtp-lede">%(lede)s</p>
  <p class="vtp-stamp">%(stamp)s</p>
</header>

<div class="vtp-body">
  <nav class="vtp-toc" aria-label="On this page">
    <p>On this page</p>
%(toc)s
  </nav>

  <div class="vtp-content">
%(secs)s
  </div>
</div>
</div>
"""


def build():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    css = ' '.join(CSS.split())          # nén nhẹ, giữ nguyên nghĩa
    made = []
    for p in PAGES:
        toc = '\n'.join(
            '    <a href="#%s-%s">%s</a>' % (p['slug'], sid, h)
            for sid, h, _ in p['sections'])
        secs = '\n'.join(
            '    <section class="vtp-sec" id="%s-%s">\n      <h2>%s</h2>\n%s\n    </section>'
            % (p['slug'], sid, h, body.strip())
            for sid, h, body in p['sections'])
        html = SHELL % dict(css=css, toc=toc, secs=secs, **p)
        path = os.path.join(OUT, p['slug'] + '.html')
        io.open(path, 'w', encoding='utf-8', newline='\n').write(html)
        made.append((p['slug'], len(html), html.count('<div class="vtp-flag">')))
    return made


PREVIEW_HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root{--vt-ink:#0A0A0A;--vt-paper:#fff;--vt-line:#E4E4E6;--vt-line-strong:#C9C9CE;--vt-muted:#6B6B70;--vt-tint:#F7F7F8;--vt-sale:#C2452D;
--vt-on-dark:#F2F2F4;--vt-on-dark-muted:rgba(242,242,244,.62);
--vt-iri-1:rgba(126,72,240,.85);--vt-iri-2:rgba(38,196,190,.72);--vt-iri-3:rgba(214,72,158,.60);--vt-iri-4:rgba(58,102,232,.75);
--vt-font-mono:"JetBrains Mono",monospace;--vt-font-display:"Archivo",sans-serif;}
*{box-sizing:border-box}body{margin:0;background:%(bg)s;font-family:"Archivo",system-ui,sans-serif;color:#0A0A0A}
%(extra)s
</style></head><body>
"""

PREVIEW_ALL_EXTRA = """.pv-top{position:sticky;top:0;z-index:9;background:#0A0A0A;color:#fff;padding:12px 20px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.pv-top b{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.18em;text-transform:uppercase;margin-right:10px}
.pv-top a{color:#fff;text-decoration:none;font-family:"JetBrains Mono";font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;opacity:.6;border:1px solid rgba(255,255,255,.25);padding:5px 10px;border-radius:999px}
.pv-top a:hover{opacity:1}
.pv-label{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#6B6B70;margin:44px 0 10px}
.pv-frame{background:#fff;border:1px solid #d8d8dc;padding:clamp(24px,4vw,64px)}
main{max-width:1240px;margin:0 auto;padding:0 20px 90px}"""


def build_previews():
    """Sinh lai hai file xem truoc. CHI de xem, KHONG dan len WordPress.

    Truoc day hai file nay lam TAY nen chung lech voi trang that sau moi lan sua.
    Gio chung sinh tu chinh cac file .html vua build ra, khong the lech nua."""
    made = []
    NL = "\n"

    # --- _preview-about.html: trang About full-bleed, khong khung ---
    about = os.path.join(OUT, "about.html")
    if os.path.isfile(about):
        body = io.open(about, encoding="utf-8").read()
        # ban dan WordPress tro vao uploads, ban xem truoc tro vao repo
        body = body.replace("/wp-content/uploads/seq/0823/", "../scroll-sequence/frames/0823/")
        html = (PREVIEW_HEAD % dict(title="ABOUT preview", bg="#fff", extra="")) + body + NL + "</body></html>" + NL
        io.open(os.path.join(OUT, "_preview-about.html"), "w", encoding="utf-8", newline=NL).write(html)
        made.append("_preview-about.html")

    # --- _preview-all.html: 9 trang chinh sach, moi trang mot khung ---
    slugs = [q["slug"] for q in PAGES]
    nav = " ".join('<a href="#%s">%s</a>' % (g, g) for g in slugs)
    parts = [PREVIEW_HEAD % dict(title="VITALITE - preview trang tinh", bg="#F0F0F2", extra=PREVIEW_ALL_EXTRA),
             '<div class="pv-top"><b>Preview trang tinh</b>%s</div><main>' % nav]
    for g in slugs:
        f = os.path.join(OUT, g + ".html")
        if not os.path.isfile(f):
            continue
        parts.append('<p class="pv-label" id="%s">%s.html</p><div class="pv-frame">%s</div>'
                     % (g, g, io.open(f, encoding="utf-8").read()))
    parts.append("</main></body></html>")
    io.open(os.path.join(OUT, "_preview-all.html"), "w", encoding="utf-8", newline=NL).write(NL.join(parts))
    made.append("_preview-all.html")
    return made


if __name__ == '__main__':
    rows = build()
    print('%-22s %8s  %s' % ('SLUG', 'BYTES', 'O CANH BAO'))
    for slug, size, flags in rows:
        print('%-22s %8d  %s' % (slug, size, flags if flags else '-'))
    print('')
    print('%d trang -> %s' % (len(rows), os.path.normpath(OUT)))
    for f in build_previews():
        print('preview  %s' % f)
