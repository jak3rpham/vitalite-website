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
 * 7. Cảnh báo trong admin khi nhập hàng sai quy ước
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
