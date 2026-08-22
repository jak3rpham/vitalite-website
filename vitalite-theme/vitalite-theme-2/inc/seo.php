<?php
/**
 * VITALITÉ — SEO ở tầng theme
 *
 * QUAN TRỌNG: mọi thứ trong file này TỰ TẮT khi có plugin SEO (Rank Math / Yoast / SEOPress).
 * Hai nguồn cùng in description và JSON-LD là lỗi khó tìm và làm Google bối rối.
 * Theme chỉ lấp chỗ trống khi chưa cài plugin.
 *
 * Kế hoạch đầy đủ: deliverables/seo/SEO-PLAN.md
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

/**
 * Có plugin SEO đang chạy không.
 */
function vt_seo_plugin_active() {
    return defined('WPSEO_VERSION')            // Yoast
        || class_exists('RankMath')            // Rank Math
        || defined('SEOPRESS_VERSION')         // SEOPress
        || defined('AIOSEO_VERSION');          // All in One SEO
}

/* -------------------------------------------------------------------------
 * 1. Description + Open Graph
 * ---------------------------------------------------------------------- */

add_action('wp_head', function () {

    if (vt_seo_plugin_active()) return;

    $title = wp_get_document_title();
    $desc  = '';
    $image = '';
    $type  = 'website';

    if (is_singular()) {
        $post = get_queried_object();
        $desc = has_excerpt($post) ? get_the_excerpt($post) : wp_strip_all_tags($post->post_content);
        $desc = trim(preg_replace('/\s+/', ' ', $desc));
        if (mb_strlen($desc) > 160) $desc = mb_substr($desc, 0, 157) . '…';
        if (has_post_thumbnail($post)) {
            $image = get_the_post_thumbnail_url($post, 'large');
        }
        $type = is_singular('product') ? 'product' : 'article';
    } elseif (is_tax() || is_category()) {
        $desc = wp_strip_all_tags(term_description());
    } else {
        $desc = get_bloginfo('description');
    }

    if (!$image) {
        $fallback = get_stylesheet_directory() . '/assets/og-default.jpg';
        if (file_exists($fallback)) {
            $image = get_stylesheet_directory_uri() . '/assets/og-default.jpg';
        }
    }

    if ($desc) {
        printf('<meta name="description" content="%s">' . "\n", esc_attr($desc));
    }

    printf('<meta property="og:site_name" content="%s">' . "\n", esc_attr(vt_brand_name()));
    printf('<meta property="og:type" content="%s">' . "\n", esc_attr($type));
    printf('<meta property="og:title" content="%s">' . "\n", esc_attr($title));
    if ($desc)  printf('<meta property="og:description" content="%s">' . "\n", esc_attr($desc));
    printf('<meta property="og:url" content="%s">' . "\n", esc_url(vt_current_url()));
    if ($image) printf('<meta property="og:image" content="%s">' . "\n", esc_url($image));

    // Twitter đọc được thẻ og:*, chỉ cần khai kiểu thẻ
    echo '<meta name="twitter:card" content="summary_large_image">' . "\n";

}, 5);

/**
 * URL hiện tại, đã chuẩn hoá. Dùng cho og:url và canonical.
 */
function vt_current_url() {
    if (is_front_page())  return home_url('/');
    if (is_singular())    return get_permalink();
    if (is_tax() || is_category() || is_tag()) {
        $link = get_term_link(get_queried_object());
        return is_wp_error($link) ? home_url('/') : $link;
    }
    if (function_exists('is_shop') && is_shop()) return vt_shop_url();
    // $GLOBALS['wp']->request rỗng ở trang chủ và một số route — không giả định nó có
    $req = isset($GLOBALS['wp']->request) ? $GLOBALS['wp']->request : '';
    return home_url('/' . ltrim($req, '/'));
}

/* -------------------------------------------------------------------------
 * 2. JSON-LD
 * ---------------------------------------------------------------------- */

/**
 * In một khối JSON-LD.
 * JSON_UNESCAPED_UNICODE để tiếng Việt không bị biến thành \uXXXX.
 */
function vt_jsonld($data) {
    echo '<script type="application/ld+json">'
       . wp_json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)
       . '</script>' . "\n";
}

add_action('wp_head', function () {

    if (vt_seo_plugin_active()) return;

    /*
     * Organization — khai một lần ở trang chủ.
     * sameAs là danh sách hồ sơ chính thức: đây là cách nói với Google rằng
     * tài khoản Instagram/Facebook/Shopee kia là CÙNG MỘT thực thể với site này.
     * Với brand có 973 đánh giá trên Shopee mà site mới tinh, liên kết thực thể
     * là cách hợp lệ duy nhất để uy tín kia có ý nghĩa gì đó.
     */
    if (is_front_page()) {
        $contact = vt_contact_info();
        vt_jsonld(array(
            '@context' => 'https://schema.org',
            '@type'    => 'Organization',
            '@id'      => home_url('/#organization'),
            'name'     => vt_brand_name(),
            'url'      => home_url('/'),
            'email'    => $contact['email'],
            'logo'     => get_stylesheet_directory_uri() . '/assets/vitalite-wordmark.png',
            'address'  => array(
                '@type'          => 'PostalAddress',
                'addressLocality'=> 'Ho Chi Minh City',
                'addressCountry' => 'VN',
            ),
            'sameAs'   => array_values(vt_social_links()),
        ));

        vt_jsonld(array(
            '@context' => 'https://schema.org',
            '@type'    => 'WebSite',
            '@id'      => home_url('/#website'),
            'url'      => home_url('/'),
            'name'     => vt_brand_name(),
            'publisher'=> array('@id' => home_url('/#organization')),
            'potentialAction' => array(
                '@type'       => 'SearchAction',
                'target'      => array(
                    '@type'       => 'EntryPoint',
                    'urlTemplate' => home_url('/?s={search_term_string}&post_type=product'),
                ),
                'query-input' => 'required name=search_term_string',
            ),
        ));
    }

    /*
     * Product — chỉ khai những trường CÓ THẬT.
     * Không bịa aggregateRating hay review. Khai review không có thật là
     * vi phạm chính sách dữ liệu có cấu trúc của Google và bị phạt thủ công.
     */
    if (function_exists('is_product') && is_product()) {
        global $product;
        if ($product instanceof WC_Product) {

            $data = array(
                '@context'    => 'https://schema.org',
                '@type'       => 'Product',
                'name'        => $product->get_name(),
                'url'         => get_permalink($product->get_id()),
                'sku'         => $product->get_sku(),
                'brand'       => array('@type' => 'Brand', 'name' => vt_brand_name()),
                'description' => wp_strip_all_tags($product->get_short_description() ?: $product->get_description()),
            );

            $img = wp_get_attachment_image_url($product->get_image_id(), 'full');
            if ($img) $data['image'] = array($img);

            $price = $product->get_price();
            if ($price !== '') {
                $data['offers'] = array(
                    '@type'         => 'Offer',
                    'url'           => get_permalink($product->get_id()),
                    'price'         => wc_format_decimal($price, wc_get_price_decimals()),
                    'priceCurrency' => get_woocommerce_currency(),
                    'availability'  => $product->is_in_stock()
                        ? 'https://schema.org/InStock'
                        : 'https://schema.org/OutOfStock',
                    'itemCondition' => 'https://schema.org/NewCondition',
                    'seller'        => array('@id' => home_url('/#organization')),
                );
            }

            vt_jsonld($data);
        }
    }

    // Breadcrumb — giúp Google hiểu cấu trúc site khi mới chỉ có vài trang
    if (is_singular() && !is_front_page()) {
        $items = array(
            array('@type' => 'ListItem', 'position' => 1, 'name' => __('Home', 'vitalite'), 'item' => home_url('/')),
        );
        if (function_exists('is_product') && is_product()) {
            $items[] = array('@type' => 'ListItem', 'position' => 2, 'name' => __('Shop', 'vitalite'), 'item' => vt_shop_url());
            $items[] = array('@type' => 'ListItem', 'position' => 3, 'name' => get_the_title());
        } else {
            $items[] = array('@type' => 'ListItem', 'position' => 2, 'name' => get_the_title());
        }
        vt_jsonld(array(
            '@context'        => 'https://schema.org',
            '@type'           => 'BreadcrumbList',
            'itemListElement' => $items,
        ));
    }

}, 6);

/* -------------------------------------------------------------------------
 * 3. Robots
 * ---------------------------------------------------------------------- */

/**
 * Chặn index những URL không có giá trị tìm kiếm và gây trùng lặp nội dung.
 * Trang lọc / sắp xếp sinh ra vô số biến thể của cùng một tập sản phẩm —
 * để Google index hết là tự làm loãng chính mình.
 */
add_filter('wp_robots', function ($robots) {

    if (is_search() || is_404()) {
        $robots['noindex'] = true;
        $robots['follow']  = true;
        return $robots;
    }

    // URL có tham số lọc / sắp xếp
    $noindex_params = array('orderby', 'on_sale', 'filter_size', 'filter_color', 'min_price', 'max_price', 'add-to-cart');
    foreach ($noindex_params as $p) {
        if (isset($_GET[$p])) {
            $robots['noindex'] = true;
            $robots['follow']  = true;
            return $robots;
        }
    }

    if (function_exists('is_cart') && (is_cart() || is_checkout() || is_account_page())) {
        $robots['noindex'] = true;
        $robots['nofollow'] = true;
    }

    return $robots;
});

/* -------------------------------------------------------------------------
 * 4. Nhắc trong admin khi site đang chặn index
 * ---------------------------------------------------------------------- */

/**
 * Site hiện đang bật "Ngăn công cụ tìm kiếm" — đúng cho lúc đang dựng,
 * nhưng đây là lỗi bị quên nhiều nhất khi launch WordPress: site chạy vài tháng
 * mà Google không index được dòng nào.
 *
 * Hiện cảnh báo thường trực trong admin cho tới khi tắt.
 */
add_action('admin_notices', function () {
    if (get_option('blog_public')) return;
    if (!current_user_can('manage_options')) return;
    echo '<div class="notice notice-warning"><p><strong>'
       . esc_html__('Search engines are blocked.', 'vitalite')
       . '</strong> '
       . esc_html__('Settings → Reading → uncheck “Discourage search engines”. Do this on launch day, not before.', 'vitalite')
       . '</p></div>';
});
