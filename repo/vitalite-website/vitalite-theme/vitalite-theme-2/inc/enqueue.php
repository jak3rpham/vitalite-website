<?php
/**
 * VITALITÉ — Nạp CSS / JS / font
 *
 * Mục tiêu: LCP < 2.5s trên mobile.
 * Ba nguyên tắc áp dụng ở file này:
 *   1. Font nạp bằng <link> + preconnect, KHÔNG dùng @import trong CSS.
 *      @import bắt browser tải CSS xong mới biết cần tải font → nối tiếp request, hại LCP.
 *   2. JS nào cũng defer. Theme không có JS nào cần chạy trước khi parse xong HTML.
 *   3. CSS/JS của WooCommerce chỉ nạp trên trang có WooCommerce.
 *      Mặc định Woo nạp trên MỌI trang, kể cả trang About — đó là ~90KB lãng phí.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

/* -------------------------------------------------------------------------
 * 1. Gợi ý kết nối sớm cho host font
 * ---------------------------------------------------------------------- */

add_filter('wp_resource_hints', function ($hints, $relation) {
    if ($relation === 'preconnect') {
        $hints[] = array('href' => 'https://fonts.googleapis.com');
        $hints[] = array('href' => 'https://fonts.gstatic.com', 'crossorigin' => 'anonymous');
    }
    return $hints;
}, 10, 2);

/* -------------------------------------------------------------------------
 * 2. CSS + JS
 * ---------------------------------------------------------------------- */

add_action('wp_enqueue_scripts', function () {

    $dir = get_stylesheet_directory();
    $uri = get_stylesheet_directory_uri();

    /*
     * Font.
     * display=swap: chữ hiện ngay bằng font dự phòng rồi đổi — không bao giờ có
     * khoảng trắng chờ font (FOIT), thứ làm hỏng LCP.
     * Chỉ lấy đúng những weight thực sự dùng. Mỗi weight thừa là một file thừa.
     */
    wp_enqueue_style(
        'vitalite-fonts',
        'https://fonts.googleapis.com/css2'
            . '?family=Archivo:wght@400;500;600;700;800'   // 700 dung 48 cho trong CSS;
            // truoc day KHONG duoc tai nen trinh duyet tu bat sang 600 hoac 800
            . '&family=Archivo+Expanded:wght@800'
            . '&family=JetBrains+Mono:wght@400;500'
            . '&display=swap',
        array(),
        null
    );

    // CSS parent (Hello Elementor) rồi mới tới child
    wp_enqueue_style(
        'hello-elementor-parent',
        get_template_directory_uri() . '/style.css',
        array(),
        wp_get_theme(get_template())->get('Version')
    );

    $style_path = $dir . '/style.css';
    wp_enqueue_style(
        'vitalite',
        $uri . '/style.css',
        array('hello-elementor-parent', 'vitalite-fonts'),
        file_exists($style_path) ? filemtime($style_path) : '2.0.0'
    );

    // JS — defer, không phụ thuộc jQuery
    $js_path = $dir . '/assets/js/site.js';
    if (file_exists($js_path)) {
        wp_enqueue_script(
            'vitalite',
            $uri . '/assets/js/site.js',
            array(),
            filemtime($js_path),
            true
        );
        wp_script_add_data('vitalite', 'strategy', 'defer');
    }
}, 20);

/* -------------------------------------------------------------------------
 * 3. Không nạp asset WooCommerce ở trang không cần
 * ---------------------------------------------------------------------- */

add_action('wp_enqueue_scripts', function () {
    if (!class_exists('WooCommerce')) return;

    $needs_woo = is_woocommerce() || is_cart() || is_checkout() || is_account_page()
                 || is_front_page()   // trang chủ có lưới sản phẩm
                 || is_search();

    if ($needs_woo) return;

    wp_dequeue_style('woocommerce-general');
    wp_dequeue_style('woocommerce-layout');
    wp_dequeue_style('woocommerce-smallscreen');
    wp_dequeue_style('wc-blocks-style');
    wp_dequeue_script('wc-cart-fragments');
    wp_dequeue_script('woocommerce');
    wp_dequeue_script('wc-add-to-cart');
}, 99);

/*
 * cart-fragments là request AJAX chạy trên MỌI lượt xem trang để cập nhật số giỏ hàng.
 * Trên shared hosting nó là một trong những thứ tốn TTFB nhất, và nó phá cache trang.
 * Ta không cần: số giỏ hàng đã được cập nhật qua woocommerce_add_to_cart_fragments
 * ở inc/woocommerce.php, chỉ chạy khi thật sự thêm hàng vào giỏ.
 */
add_action('wp_enqueue_scripts', function () {
    if (!class_exists('WooCommerce')) return;
    if (is_cart() || is_checkout()) return;   // hai trang này thì cần thật
    wp_dequeue_script('wc-cart-fragments');
}, 100);

/* -------------------------------------------------------------------------
 * 4. Preload ảnh LCP
 * ---------------------------------------------------------------------- */

/**
 * Poster của hero là phần tử LCP của trang chủ.
 * Preload để browser tải nó song song với CSS thay vì chờ CSS parse xong.
 *
 * CHỈ preload đúng một ảnh. Preload nhiều thứ là tự cạnh tranh băng thông với chính mình.
 */
add_action('wp_head', function () {
    if (!vt_has_hero()) return;

    $poster = get_stylesheet_directory_uri() . '/assets/hero-poster.webp';
    $path   = get_stylesheet_directory() . '/assets/hero-poster.webp';
    if (!file_exists($path)) {
        $poster = get_stylesheet_directory_uri() . '/assets/hero-poster.jpg';
        $path   = get_stylesheet_directory() . '/assets/hero-poster.jpg';
        if (!file_exists($path)) return;
    }
    printf('<link rel="preload" as="image" href="%s" fetchpriority="high">' . "\n", esc_url($poster));
}, 2);

/* -------------------------------------------------------------------------
 * 5. Không lazy-load ảnh nằm trên màn hình đầu
 * ---------------------------------------------------------------------- */

/**
 * WordPress gắn loading="lazy" cho gần như mọi ảnh.
 * Ảnh trên màn hình đầu mà lazy thì LCP tệ đi — browser hoãn tải chính cái nó cần trước nhất.
 * Bỏ lazy cho 2 ảnh đầu tiên của mỗi trang.
 */
add_filter('wp_get_attachment_image_attributes', function ($attr) {
    static $count = 0;
    $count++;
    if ($count <= 2) {
        $attr['loading']       = 'eager';
        $attr['fetchpriority'] = 'high';
    }
    return $attr;
}, 10, 1);

/* -------------------------------------------------------------------------
 * 6. Bỏ CSS block editor ở front-end
 * ---------------------------------------------------------------------- */

/*
 * Site này dựng bằng theme PHP + Elementor. Không dùng block editor để dựng trang.
 * wp-block-library là ~30KB CSS không dùng tới trên mọi lượt xem trang.
 * Nếu sau này có dùng block ở bài viết thì bỏ đoạn này đi.
 */
add_action('wp_enqueue_scripts', function () {
    wp_dequeue_style('wp-block-library');
    wp_dequeue_style('wp-block-library-theme');
    wp_dequeue_style('classic-theme-styles');
    wp_dequeue_style('global-styles');
}, 100);
