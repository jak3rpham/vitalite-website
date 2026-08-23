<?php
/**
 * VITALITÉ — Theme setup, menu, kích thước ảnh, bảo mật
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

/* -------------------------------------------------------------------------
 * 1. Theme support
 * ---------------------------------------------------------------------- */

add_action('after_setup_theme', function () {

    load_theme_textdomain('vitalite', get_stylesheet_directory() . '/languages');

    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('automatic-feed-links');
    add_theme_support('html5', array('search-form', 'gallery', 'caption', 'style', 'script', 'navigation-widgets'));
    add_theme_support('responsive-embeds');

    // WooCommerce
    add_theme_support('woocommerce', array(
        'thumbnail_image_width' => 600,
        'single_image_width'    => 1000,   // mockup gốc chỉ 1000px — xem ghi chú zoom bên dưới
        'product_grid'          => array(
            'default_columns' => 4,
            'min_columns'     => 2,
            'max_columns'     => 4,
        ),
    ));

    /*
     * KHÔNG bật 'wc-product-gallery-zoom'.
     * Mockup hiện tại là 1000×1000. Zoom cần ảnh ≥1600px thì mới nét;
     * zoom vào ảnh 1000px chỉ phóng to điểm ảnh — trông như hàng rẻ tiền.
     * Có ảnh lớn hơn thì bật lại dòng dưới.
     * add_theme_support('wc-product-gallery-zoom');
     */
    add_theme_support('wc-product-gallery-lightbox');
    add_theme_support('wc-product-gallery-slider');

    register_nav_menus(array(
        'primary' => __('Primary menu', 'vitalite'),
        'footer_shop'    => __('Footer — Shop', 'vitalite'),
        'footer_support' => __('Footer — Support', 'vitalite'),
    ));
});

/* -------------------------------------------------------------------------
 * 2. Kích thước ảnh
 * ---------------------------------------------------------------------- */

add_action('after_setup_theme', function () {
    // Thẻ sản phẩm là ô vuông 1:1 — khớp đúng tỉ lệ mockup 1000×1000
    add_image_size('vt-card', 600, 600, true);
    add_image_size('vt-card-2x', 1000, 1000, true);
    // Ảnh editorial dọc 4:5, hợp với ảnh model đang có (đa số 3:4 và 4:5)
    add_image_size('vt-editorial', 900, 1125, true);
});

/*
 * WooCommerce cắt ảnh sản phẩm theo tỉ lệ đặt trong Customizer.
 * Ép về 1:1 để lưới luôn thẳng hàng, không phụ thuộc người nhập hàng
 * có upload đúng tỉ lệ hay không.
 */
add_filter('woocommerce_get_image_size_thumbnail', function ($size) {
    return array('width' => 600, 'height' => 600, 'crop' => 1);
});

/* -------------------------------------------------------------------------
 * 3. Bảo mật
 * ---------------------------------------------------------------------- */

/**
 * SVG upload — CHỈ admin.
 * SVG là XML và nhúng được <script>. Cho mọi role upload = lỗ XSS.
 * WordPress KHÔNG sanitize SVG, nên vẫn chỉ upload file tự tạo.
 */
add_filter('upload_mimes', function ($mimes) {
    if (current_user_can('manage_options')) {
        $mimes['svg'] = 'image/svg+xml';
    } else {
        unset($mimes['svg']);
    }
    return $mimes;
});

/**
 * Kiểm tra thật nội dung file khi upload SVG — chặn đổi đuôi file.
 */
add_filter('wp_check_filetype_and_ext', function ($data, $file, $filename, $mimes) {
    if (substr(strtolower($filename), -4) === '.svg') {
        if (!current_user_can('manage_options')) {
            return array('ext' => false, 'type' => false, 'proper_filename' => false);
        }
        $data['ext']  = 'svg';
        $data['type'] = 'image/svg+xml';
    }
    return $data;
}, 10, 4);

// Tắt XML-RPC — không dùng, mà là bề mặt bị dò mật khẩu thường xuyên nhất
add_filter('xmlrpc_enabled', '__return_false');
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wlwmanifest_link');

// Ẩn phiên bản WordPress khỏi HTML và khỏi query string của asset
remove_action('wp_head', 'wp_generator');
add_filter('the_generator', '__return_empty_string');

// Thông báo đăng nhập chung chung — không tiết lộ username có tồn tại hay không
add_filter('login_errors', function () {
    return __('Login failed. Check your details and try again.', 'vitalite');
});

// Header bảo mật cơ bản. Không đặt CSP ở đây — CSP sai là vỡ trang, cần làm riêng và test kỹ.
add_action('send_headers', function () {
    if (is_admin()) return;
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('X-Frame-Options: SAMEORIGIN');
});

/* -------------------------------------------------------------------------
 * 4. Dọn rác trong <head>
 * ---------------------------------------------------------------------- */

remove_action('wp_head', 'wp_shortlink_wp_head');
remove_action('wp_head', 'adjacent_posts_rel_link_wp_head', 10);
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');
remove_action('admin_print_scripts', 'print_emoji_detection_script');
remove_action('admin_print_styles', 'print_emoji_styles');
add_filter('emoji_svg_url', '__return_false');

/* -------------------------------------------------------------------------
 * 5. Lớp tương thích shortcode
 * ---------------------------------------------------------------------- */

/*
 * Quyết định đã chốt: bỏ shortcode, dùng header.php/footer.php + template parts.
 * Nhưng nếu trang Elementor hiện tại đang chèn [vt_banner] hay [vt_products] thì
 * xoá shortcode ngay lập tức sẽ làm trang đó in ra chuỗi thô.
 *
 * Nên giữ shortcode làm VỎ MỎNG gọi template part. Không còn logic bên trong.
 * Gỡ hẳn khi đã kiểm tra không trang nào còn dùng.
 */
$vt_shortcodes = array(
    'vt_header'   => 'template-parts/site-header',
    'vt_footer'   => 'template-parts/site-footer',
    'vt_banner'   => 'template-parts/hero',
    'vt_products' => 'template-parts/section-products',
    'vt_gallery'  => 'template-parts/section-gallery',
    'vt_collection' => 'template-parts/section-collection',
    'vt_services'   => 'template-parts/section-services',
);
foreach ($vt_shortcodes as $vt_tag => $vt_part) {
    add_shortcode($vt_tag, function () use ($vt_tag, $vt_part) {

        /*
         * CHỐNG RENDER HAI LẦN.
         * Trang Elementor cũ có thể vẫn đang chèn [vt_header] / [vt_footer].
         * Nhưng header.php và footer.php GIỜ ĐÃ tự render chúng rồi.
         * Không chặn thì trang đó sẽ có hai header chồng nhau.
         *
         * vt_mark_rendered() trả false ở lần gọi thứ hai trở đi → shortcode im lặng.
         * Gỡ toàn bộ khối shortcode này khi đã dọn hết trang Elementor cũ.
         */
        if (in_array($vt_tag, array('vt_header', 'vt_footer'), true) && !vt_mark_rendered($vt_tag)) {
            return '';
        }

        ob_start();
        get_template_part($vt_part);
        return ob_get_clean();
    });
}
unset($vt_shortcodes, $vt_tag, $vt_part);

/**
 * Đánh dấu một khối đã render trong lượt tải trang này.
 *
 * @return bool true nếu đây là lần đầu (được phép render), false nếu đã render rồi.
 */
function vt_mark_rendered($key) {
    static $done = array();
    if (isset($done[$key])) return false;
    $done[$key] = true;
    return true;
}

/* -------------------------------------------------------------------------
 * 6. Nội dung
 * ---------------------------------------------------------------------- */

// Excerpt gọn hơn, dấu ba chấm thật thay vì [...]
add_filter('excerpt_length', function () { return 26; });
add_filter('excerpt_more', function () { return '…'; });

// Xoá cache gallery khi có thay đổi thư viện ảnh
add_action('add_attachment', function () { delete_transient('vt_gallery'); });
add_action('delete_attachment', function () { delete_transient('vt_gallery'); });

/**
 * Class trên <body> để CSS biết trang có hero hay không, khỏi phải đoán.
 */
add_filter('body_class', function ($classes) {
    if (vt_has_hero()) $classes[] = 'vt-has-hero';

    /*
     * vt-banner-top = trang này mở bằng một banner tràn lên tận mép trên viewport,
     * header nằm ĐÈ lên nó. CSS dùng class này để bỏ khoảng đệm bằng chiều cao header.
     * Không có class này → khoảng đệm giữ nguyên, header đục như thường.
     */
    if (vt_top_banner_tone()) $classes[] = 'vt-banner-top';

    return $classes;
});
