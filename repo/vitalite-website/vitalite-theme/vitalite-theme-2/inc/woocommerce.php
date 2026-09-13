<?php
/**
 * VITALITÉ — WooCommerce
 *
 * NGUYÊN TẮC: mọi tuỳ biến đi qua hook, KHÔNG copy đè file template của Woo
 * (trừ archive-product.php và content-product.php, là hai file bắt buộc phải
 * đè để đổi cấu trúc lưới).
 *
 * KHÔNG ĐỤNG VÀO CART VÀ CHECKOUT. Sửa checkout là thay đổi rủi ro cao nhất
 * trong toàn bộ stack. Chỉ style bằng CSS, không đổi logic, không đổi field.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

/* -------------------------------------------------------------------------
 * 1. Số lượng giỏ hàng cập nhật thời gian thực
 * ---------------------------------------------------------------------- */

/**
 * In ra badge số lượng. Rỗng → thêm class is-empty, CSS ẩn hẳn số.
 */
function vt_cart_count_markup() {
    $count = 0;
    if (function_exists('WC') && WC() && WC()->cart) {
        $count = WC()->cart->get_cart_contents_count();
    }
    printf(
        '<span class="vt-cart-count%s" aria-hidden="%s">%s</span>',
        $count > 0 ? '' : ' is-empty',
        $count > 0 ? 'false' : 'true',
        esc_html($count)
    );
}

add_filter('woocommerce_add_to_cart_fragments', function ($fragments) {
    ob_start();
    vt_cart_count_markup();
    $fragments['span.vt-cart-count'] = ob_get_clean();
    return $fragments;
});

/* -------------------------------------------------------------------------
 * 2. Dọn hook mặc định của archive
 * ---------------------------------------------------------------------- */

/**
 * Khung bọc nội dung WooCommerce — THAY cho khung mặc định.
 *
 * VÌ SAO PHẢI THAY
 *   `woocommerce_output_content_wrapper()` in ra
 *   `<div id="primary"><main id="main" class="site-main">`.
 *   Nhưng header.php của theme ĐÃ mở `<main id="vt-main">` rồi.
 *   → `<main>` lồng `<main>`: HTML không hợp lệ, và máy đọc màn hình thấy hai
 *   vùng "nội dung chính" trong một trang, không biết vào đâu.
 *
 *   Gỡ hẳn khung mặc định thì trang sản phẩm / giỏ hàng mất container, chữ dính
 *   sát mép. Nên KHÔNG gỡ suông — thay bằng khung của mình.
 *
 * HAI CHẾ ĐỘ
 *   `bare`  — shop / category / tag. Template tự lo bố cục vì banner phải tràn
 *             sát mép còn lưới sản phẩm thì phải có lề. Chỉ bọc một div trơn.
 *   default — trang sản phẩm đơn. Bọc thêm .vt-section + .vt-wrap để có lề và
 *             khoảng đệm trên dưới như mọi trang khác.
 *
 * ⚠️ KHÔNG đụng vào bất kỳ hook nào của luồng thêm giỏ / thanh toán.
 *   Đây thuần là khung bọc. Giỏ hàng và thanh toán là trang WordPress thường
 *   chứa shortcode, chúng đi qua page.php chứ không qua đường này.
 */
function vt_woo_wrapper_is_bare($set = null) {
    static $bare = false;
    if ($set !== null) $bare = (bool) $set;
    return $bare;
}

function vt_woo_wrapper_start() {
    $bare = (function_exists('is_shop') && is_shop())
         || (function_exists('is_product_taxonomy') && is_product_taxonomy());
    vt_woo_wrapper_is_bare($bare);

    // Hai chuỗi hằng, không có dữ liệu ngoài nào lọt vào — nhưng vẫn viết tách
    // if/else thay vì ternary trong echo, để mắt người (và script quét) thấy ngay
    // là không có biến nào đang được in ra.
    if ($bare) {
        echo '<div class="vt-woo vt-woo--bare">';
    } else {
        echo '<div class="vt-woo vt-section"><div class="vt-wrap">';
    }
}

function vt_woo_wrapper_end() {
    if (vt_woo_wrapper_is_bare()) {
        echo '</div>';
    } else {
        echo '</div></div>';
    }
}

add_action('init', function () {
    if (!class_exists('WooCommerce')) return;

    // Khung bọc: gỡ bản mặc định (in ra <main> lồng <main>), gắn bản của theme
    remove_action('woocommerce_before_main_content', 'woocommerce_output_content_wrapper', 10);
    remove_action('woocommerce_after_main_content', 'woocommerce_output_content_wrapper_end', 10);
    add_action('woocommerce_before_main_content', 'vt_woo_wrapper_start', 10);
    add_action('woocommerce_after_main_content', 'vt_woo_wrapper_end', 10);

    /*
     * 🔴 Breadcrumb mặc định của Woo — PHẢI gỡ.
     *
     * WooCommerce gắn `woocommerce_breadcrumb` vào `woocommerce_before_main_content`
     * ở ƯU TIÊN 20. Khung bọc của ta chạy ở ưu tiên 10, nên thứ tự in ra là:
     *     [khung mở]  →  [breadcrumb của Woo]  →  [banner của ta]
     * Breadcrumb chữ đen trên nền trắng chen VÀO TRƯỚC banner → đúng cái vệt trắng
     * nằm giữa header và banner.
     *
     * Và nó còn bị in HAI LẦN: `archive-product.php` đã tự gọi woocommerce_breadcrumb()
     * ở .vt-shop-head, đúng chỗ nó phải nằm — DƯỚI banner.
     */
    remove_action('woocommerce_before_main_content', 'woocommerce_breadcrumb', 20);

    // Sidebar mặc định — không dùng, lọc đi bằng Premmerce ở toolbar
    remove_action('woocommerce_sidebar', 'woocommerce_get_sidebar', 10);

    // Bọc ảnh + tiêu đề + giá của thẻ sản phẩm — ta tự dựng ở content-product.php
    remove_action('woocommerce_before_shop_loop_item', 'woocommerce_template_loop_product_link_open', 10);
    remove_action('woocommerce_before_shop_loop_item_title', 'woocommerce_show_product_loop_sale_flash', 10);
    remove_action('woocommerce_before_shop_loop_item_title', 'woocommerce_template_loop_product_thumbnail', 10);
    remove_action('woocommerce_shop_loop_item_title', 'woocommerce_template_loop_product_title', 10);
    remove_action('woocommerce_after_shop_loop_item_title', 'woocommerce_template_loop_rating', 5);
    remove_action('woocommerce_after_shop_loop_item_title', 'woocommerce_template_loop_price', 10);
    remove_action('woocommerce_after_shop_loop_item', 'woocommerce_template_loop_product_link_close', 5);
    remove_action('woocommerce_after_shop_loop_item', 'woocommerce_template_loop_add_to_cart', 10);
}, 20);   // ưu tiên 20: chạy sau khi WooCommerce đã đăng ký xong hook mặc định

/**
 * Số sản phẩm mỗi trang. 12 chia hết cho cả lưới 4 cột lẫn 2 cột.
 */
add_filter('loop_shop_per_page', function () { return 12; }, 20);

/**
 * Số cột lưới.
 */
add_filter('loop_shop_columns', function () { return 4; }, 20);

/* -------------------------------------------------------------------------
 * 3. Sắp xếp — "New Arrivals" và "Sale" là CÁCH SẮP XẾP, không phải category
 * ---------------------------------------------------------------------- */

/**
 * Hỗ trợ ?on_sale=1 trên trang shop.
 * Nhờ vậy link "Sale" ở nav và footer không cần một category riêng.
 */
add_action('woocommerce_product_query', function ($q) {
    if (is_admin() || !$q->is_main_query()) return;
    if (empty($_GET['on_sale'])) return;

    $ids = wc_get_product_ids_on_sale();
    // Mảng rỗng nghĩa là "không có gì đang sale" — phải trả về rỗng thật,
    // không được để Woo hiểu thành "không lọc gì cả" rồi hiện toàn bộ sản phẩm.
    $q->set('post__in', !empty($ids) ? $ids : array(0));
}, 20);

/**
 * Tiêu đề trang shop đổi theo bộ lọc đang bật, để khách biết mình đang xem gì.
 */
function vt_shop_heading() {
    if (!empty($_GET['on_sale']))                                   return __('Sale', 'vitalite');
    if (isset($_GET['orderby']) && $_GET['orderby'] === 'date')     return __('New Arrivals', 'vitalite');
    if (is_product_category() || is_product_tag())                  return single_term_title('', false);
    if (is_search())                                                return __('Search results', 'vitalite');
    return __('Shop All', 'vitalite');
}

/* -------------------------------------------------------------------------
 * 4. PDP — chỉ thêm bằng hook
 * ---------------------------------------------------------------------- */

/**
 * Chèn bảng size vào ngay dưới nút chọn size, thay vì bắt khách rời trang.
 * Chọn sai size là nguyên nhân trả hàng số một trong thời trang online,
 * nên bảng số đo phải nằm ĐÚNG CHỖ khách đang phân vân.
 *
 * Số đo lấy nguyên văn từ mô tả sản phẩm trên Shopee (xác minh 2026-08-19).
 * ÁP DỤNG CHO ÁO THUN. Hoodie chưa có số đo riêng — xem điều kiện bên dưới.
 */
function vt_size_table_tshirt() {
    ?>
    <div class="vt-table-scroll">
      <table class="vt-size-table">
        <caption class="screen-reader-text"><?php esc_html_e('Size chart in centimetres', 'vitalite'); ?></caption>
        <thead>
          <tr>
            <th scope="col"><?php esc_html_e('Size', 'vitalite'); ?></th>
            <th scope="col"><?php esc_html_e('Length (cm)', 'vitalite'); ?></th>
            <th scope="col"><?php esc_html_e('Width (cm)', 'vitalite'); ?></th>
            <th scope="col"><?php esc_html_e('Height', 'vitalite'); ?></th>
            <th scope="col"><?php esc_html_e('Weight', 'vitalite'); ?></th>
          </tr>
        </thead>
        <tbody>
          <tr><th scope="row">S</th><td>70</td><td>55</td><td>155–165 cm</td><td>&lt; 60 kg</td></tr>
          <tr><th scope="row">M</th><td>73</td><td>58</td><td>160–175 cm</td><td>&lt; 75 kg</td></tr>
          <tr><th scope="row">L</th><td>76</td><td>61</td><td>175–190 cm</td><td>&lt; 100 kg</td></tr>
        </tbody>
      </table>
    </div>
    <p class="vt-size-note">
      <?php esc_html_e('Measurements may vary by 2–3 cm due to batch production.', 'vitalite'); ?>
    </p>
    <?php
}

/**
 * Chỉ hiện bảng size cho sản phẩm THUỘC DANH MỤC ÁO THUN.
 * Hoodie và các dòng khác chưa có số đo → không hiện gì còn hơn hiện số sai.
 */
add_action('woocommerce_single_product_summary', function () {
    global $product;
    if (!$product) return;
    if (!has_term(array('t-shirts', 'tshirts', 'ao-thun'), 'product_cat', $product->get_id())) return;

    echo '<details class="vt-size-guide"><summary>' . esc_html__('Size guide', 'vitalite') . '</summary>';
    vt_size_table_tshirt();
    echo '</details>';
}, 25);

/**
 * Đổi nhãn tab "Additional information" thành "Details".
 * Bốn thuộc tính Fabric / Fit / Sizing / Print đổ vào tab này —
 * đúng khuôn brand vẫn dùng trên Instagram.
 */
add_filter('woocommerce_product_tabs', function ($tabs) {
    if (isset($tabs['additional_information'])) {
        $tabs['additional_information']['title'] = __('Details', 'vitalite');
    }
    unset($tabs['reviews']);   // chưa có đánh giá nào — tab rỗng làm site trông bỏ hoang
    return $tabs;
}, 98);

/**
 * Nhãn nút thêm giỏ hàng.
 */
add_filter('woocommerce_product_single_add_to_cart_text', function () {
    return __('Add to cart', 'vitalite');
});

/* -------------------------------------------------------------------------
 * 5. Breadcrumb
 * ---------------------------------------------------------------------- */

add_filter('woocommerce_breadcrumb_defaults', function ($args) {
    $args['delimiter']   = ' <span aria-hidden="true">/</span> ';
    $args['wrap_before'] = '<nav class="woocommerce-breadcrumb" aria-label="' . esc_attr__('Breadcrumb', 'vitalite') . '">';
    $args['wrap_after']  = '</nav>';
    $args['home']        = __('Home', 'vitalite');
    return $args;
});

/* -------------------------------------------------------------------------
 * 6. Bỏ những thứ không dùng
 * ---------------------------------------------------------------------- */

// Không có blog sản phẩm, không dùng widget mặc định của Woo trong sidebar
add_filter('woocommerce_enqueue_styles', function ($styles) {
    unset($styles['woocommerce-smallscreen']);   // ta tự làm responsive
    return $styles;
});

/**
 * Ẩn ô "Ship to a different address" mặc định mở sẵn ở checkout.
 * ĐÂY LÀ THAY ĐỔI DUY NHẤT ĐỘNG TỚI CHECKOUT, và nó chỉ đổi trạng thái mặc định
 * của một ô tick, không đổi field, không đổi validate, không đổi luồng.
 * Có phàn nàn gì thì gỡ dòng này ra là về nguyên trạng.
 */
add_filter('woocommerce_ship_to_different_address_checked', '__return_false');

/* -------------------------------------------------------------------------
 * 7. Miễn phí vận chuyển theo SỐ LƯỢNG, không theo giá trị đơn
 * ---------------------------------------------------------------------- */

/**
 * Brand chốt 29/08/2026: miễn phí ship từ 3 áo trở lên.
 *
 * VÌ SAO PHẢI VIẾT TAY
 *     WooCommerce có sẵn Free Shipping, nhưng điều kiện duy nhất nó hiểu là
 *     "A minimum order amount" — tức theo TIỀN. Chính sách của brand tính theo
 *     SỐ MÓN. Không có ô nào trong giao diện đặt được điều kiện đó, nên nó
 *     phải là một filter.
 *
 * CHỈ ÁP DỤNG NỘI ĐỊA
 *     Đơn đi Mỹ không phải ship quốc tế từng đơn: hàng xách tay theo lô rồi
 *     một người bên Mỹ phân phối nội địa Mỹ. Chi phí chặng đó chưa ai chốt,
 *     và brand chưa bao giờ nói "3 áo" có áp cho đơn quốc tế hay không.
 *     Mặc định KHÔNG cho, vì cho nhầm rồi rút lại là đổi điều khoản với khách
 *     đang chờ hàng. Muốn mở thì sửa VT_FREE_SHIP_COUNTRY thành '' (mọi nước).
 *
 * ĐIỀU KIỆN ĐỦ ĐỂ NÓ CHẠY
 *     Phải có một phương thức "Free shipping" trong shipping zone Việt Nam.
 *     Chưa tạo zone thì filter này không làm gì cả — nó lọc một phương thức
 *     chưa tồn tại. Không lỗi, chỉ là chưa có tác dụng.
 *
 * ĐẾM CÁI GÌ
 *     Đếm số món CẦN GIAO. Sản phẩm ảo hoặc tải về không tính, vì chúng không
 *     phát sinh phí ship, để chúng đẩy đơn qua mốc 3 là cho không phí giao hàng.
 */

/** Số món tối thiểu để được miễn phí giao hàng. */
if (!defined('VT_FREE_SHIP_MIN_QTY')) {
    define('VT_FREE_SHIP_MIN_QTY', 3);
}

/** Chỉ áp dụng cho nước này. Để chuỗi rỗng nếu muốn áp dụng mọi nơi. */
if (!defined('VT_FREE_SHIP_COUNTRY')) {
    define('VT_FREE_SHIP_COUNTRY', 'VN');
}

/**
 * Đếm số món cần giao trong một package.
 *
 * @param array $package Package của WooCommerce.
 * @return int
 */
function vt_shipping_item_count($package) {
    $qty = 0;

    if (empty($package['contents']) || !is_array($package['contents'])) {
        return $qty;
    }

    foreach ($package['contents'] as $item) {
        if (empty($item['data']) || !is_object($item['data'])) {
            continue;
        }
        if (!method_exists($item['data'], 'needs_shipping') || !$item['data']->needs_shipping()) {
            continue;
        }
        $qty += isset($item['quantity']) ? (int) $item['quantity'] : 0;
    }

    return $qty;
}

/**
 * Quyết định Free Shipping có hiện ở checkout không.
 *
 * Trả về false thì phương thức bị ẩn và khách trả phí bình thường.
 * Ngoài nước VT_FREE_SHIP_COUNTRY thì trả nguyên giá trị Woo tính, tức là
 * để nguyên cấu hình trong admin, filter này không xen vào.
 *
 * @param bool  $available Woo tính sẵn.
 * @param array $package   Package đang xét.
 * @return bool
 */
add_filter('woocommerce_shipping_free_shipping_is_available', function ($available, $package) {
    $country = '';
    if (!empty($package['destination']['country'])) {
        $country = $package['destination']['country'];
    }

    // Ngoài vùng áp dụng → không đụng tới, admin toàn quyền.
    if (VT_FREE_SHIP_COUNTRY !== '' && $country !== VT_FREE_SHIP_COUNTRY) {
        return $available;
    }

    return vt_shipping_item_count($package) >= VT_FREE_SHIP_MIN_QTY;
}, 20, 2);

/**
 * Nhắc người cấu hình, hiện trong màn hình Shipping của WooCommerce.
 *
 * Không có dòng này thì sáu tháng nữa có người vào sửa "Minimum order amount"
 * của Free Shipping, thấy nó không có tác dụng gì, rồi mất buổi đi tìm.
 */
add_action('admin_notices', function () {
    $screen = function_exists('get_current_screen') ? get_current_screen() : null;
    if (!$screen || $screen->id !== 'woocommerce_page_wc-settings') {
        return;
    }
    if (!isset($_GET['tab']) || $_GET['tab'] !== 'shipping') {
        return;
    }

    printf(
        '<div class="notice notice-info"><p><strong>%s</strong> %s</p></div>',
        esc_html__('VITALITÉ:', 'vitalite'),
        sprintf(
            /* translators: 1: số món tối thiểu, 2: mã quốc gia */
            esc_html__('Free shipping is decided by ITEM COUNT, not order value: %1$d or more items, %2$s only. The rule lives in the theme, at inc/woocommerce.php section 7. Changing "Minimum order amount" here will have no effect.', 'vitalite'),
            (int) VT_FREE_SHIP_MIN_QTY,
            esc_html(VT_FREE_SHIP_COUNTRY)
        )
    );
});

/* -------------------------------------------------------------------------
 * 8. Cảnh báo trong admin khi nhập hàng sai quy ước
 * ---------------------------------------------------------------------- */

/**
 * Hiệu ứng hover đổi mặt trước ↔ mặt sau phụ thuộc HOÀN TOÀN vào quy ước:
 *   Product image = mặt trước, Gallery ảnh đầu tiên = mặt sau.
 * Người nhập hàng không đọc tài liệu thì sẽ quên. Nhắc ngay trong màn hình sửa sản phẩm.
 */
add_action('add_meta_boxes', function () {
    add_meta_box(
        'vt_image_convention',
        __('VITALITÉ — image convention', 'vitalite'),
        function () {
            echo '<p style="margin:0 0 8px"><strong>' . esc_html__('Product image', 'vitalite') . '</strong> = ' . esc_html__('FRONT of the garment', 'vitalite') . '</p>';
            echo '<p style="margin:0 0 8px"><strong>' . esc_html__('Gallery, first image', 'vitalite') . '</strong> = ' . esc_html__('BACK of the garment', 'vitalite') . '</p>';
            echo '<p style="margin:0;color:#666">' . esc_html__('Hover on the shop grid swaps front to back. Any other order breaks it.', 'vitalite') . '</p>';
        },
        'product',
        'side',
        'low'
    );
});

/* -------------------------------------------------------------------------
 * 9. PDP — sửa bốn chỗ của template mặc định WooCommerce
 *
 * Theme KHÔNG đè template trang sản phẩm đơn (chỉ đè archive-product.php và
 * content-product.php). Bốn filter dưới đây vá những chỗ chướng nhất của bản
 * mặc định — không phải thiết kế lại PDP.
 * ---------------------------------------------------------------------- */

/**
 * 9.1 — Ảnh PDP: dùng file gốc, đừng dùng bản 600px.
 *
 * Đo 13/09: `woocommerce_single` của ảnh đã upload được sinh ở **600×600**, trong
 * khi PDP hiển thị ở 653px → phóng to, mờ. Theme khai `single_image_width => 1000`
 * nhưng option `woocommerce_single_image_width` trong database ghi đè theme support,
 * và ảnh đã upload thì đổi option cũng KHÔNG sinh lại cỡ — phải regenerate.
 *
 * Trả 'full' là bỏ qua toàn bộ chuyện đó: file gốc đã là 1000×1000.
 *
 * 🔴 An toàn CHỈ VÌ ảnh sản phẩm hiện tại là mockup 1000×1000, ≤36 KB mỗi file.
 * Ngày nào upload ảnh chụp 3000px thì dòng này thành phục vụ ảnh 3000px cho mọi
 * khách — lúc đó đổi sang một cỡ đã đăng ký và regenerate.
 */
add_filter('woocommerce_gallery_image_size', function ($size) {
    return 'full';
});

/**
 * 9.2 — Tiêu đề trong tab: "Additional information" → "Details".
 *
 * Mục 4 đã đổi NHÃN của tab, nhưng tiêu đề <h2> bên trong là chuỗi riêng.
 * Bỏ sót là tab ghi "Details" mà nội dung mở ra ghi "Additional information".
 */
add_filter('woocommerce_product_additional_information_heading', function () {
    return __('Details', 'vitalite');
});

/**
 * 9.3 — Bỏ Color và Size khỏi bảng Details.
 *
 * Chúng là thuộc tính biến thể — khách vừa chọn ngay phía trên. Liệt kê lại
 * "COLOR: Black, White" bên dưới là nhắc lại thứ đã chọn, và tệ hơn: nó liệt
 * MỌI màu chứ không phải màu khách đang xem.
 *
 * Bảng chỉ nên còn spec thật: Fabric · Fit · Collection · Print.
 */
add_filter('woocommerce_display_product_attributes', function ($attributes, $product) {
    unset($attributes['attribute_pa_color'], $attributes['attribute_pa_size']);
    return $attributes;
}, 10, 2);

/* -------------------------------------------------------------------------
 * 10. PDP — chấm màu và nút size thay cho dropdown "Choose an option"
 *
 * 🔴 KHÔNG bỏ thẻ <select>. JS biến thể của WooCommerce đọc thẳng từ nó để
 * tính giá, đổi ảnh, kiểm tồn kho. Thay nó bằng markup tự chế là phải viết lại
 * toàn bộ logic đó — và là chỗ dễ vỡ nhất trong stack.
 *
 * Cách làm: giữ <select>, ẩn khỏi mắt (vẫn focus được, trình đọc màn hình vẫn
 * đọc), rồi vẽ nút bên cạnh. Bấm nút → gán giá trị vào select → bắn sự kiện
 * `change`. Woo lo phần còn lại y như khách tự chọn trong dropdown.
 * ---------------------------------------------------------------------- */

add_filter('woocommerce_dropdown_variation_attribute_options_html', function ($html, $args) {

    $attribute = isset($args['attribute']) ? $args['attribute'] : '';
    if (!in_array($attribute, array('pa_color', 'pa_size'), true)) {
        return $html;
    }

    $product = isset($args['product']) ? $args['product'] : false;
    $options = isset($args['options']) ? $args['options'] : array();
    if (!$product || empty($options)) {
        return $html;
    }

    // slug → tên hiển thị. Đọc term để lấy đúng tên, không đoán từ slug.
    $names = array();
    $terms = wc_get_product_terms($product->get_id(), $attribute, array('fields' => 'all'));
    if (!is_wp_error($terms)) {
        foreach ($terms as $term) {
            $names[$term->slug] = $term->name;
        }
    }

    $is_color = ($attribute === 'pa_color');
    $buttons  = '';

    foreach ($options as $slug) {
        $label = isset($names[$slug]) ? $names[$slug] : $slug;

        if ($is_color) {
            $hex = vt_color_hex(isset($names[$slug]) ? $names[$slug] : $slug);
            if ($hex === '#DDDDE1') $hex = vt_color_hex($slug);

            $buttons .= sprintf(
                '<button type="button" class="vt-varpick-dot" data-value="%1$s" aria-pressed="false" title="%2$s" style="background:%3$s"><span class="screen-reader-text">%2$s</span></button>',
                esc_attr($slug),
                esc_attr($label),
                esc_attr($hex)
            );
        } else {
            $buttons .= sprintf(
                '<button type="button" class="vt-varpick-btn" data-value="%1$s" aria-pressed="false">%2$s</button>',
                esc_attr($slug),
                esc_html(strtoupper($label))
            );
        }
    }

    return sprintf(
        '<div class="vt-varpick vt-varpick--%1$s">%2$s<div class="vt-varpick-list">%3$s</div></div>',
        $is_color ? 'color' : 'size',
        $html,
        $buttons
    );
}, 10, 2);
