<?php
/**
 * VITALITÉ — Helper
 *
 * Nguyên tắc: KHÔNG BAO GIỜ in ra link 404.
 * Site đang ở giai đoạn chưa có sản phẩm và chưa có page chính sách.
 * Các helper dưới đây tự lành: có thì trỏ đúng, chưa có thì trỏ Shop hoặc ẩn hẳn link.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

/* -------------------------------------------------------------------------
 * URL
 * ---------------------------------------------------------------------- */

/**
 * URL trang Shop. An toàn kể cả khi WooCommerce chưa bật.
 */
function vt_shop_url() {
    if (function_exists('wc_get_page_permalink')) {
        $url = wc_get_page_permalink('shop');
        if ($url) return $url;
    }
    return home_url('/shop');
}

/**
 * URL của một product_cat theo slug.
 * Category chưa tạo → trả về Shop, không trả 404.
 *
 * @param string $slug ví dụ 't-shirts'
 */
function vt_cat_url($slug) {
    if (taxonomy_exists('product_cat')) {
        $term = get_term_by('slug', $slug, 'product_cat');
        if ($term && !is_wp_error($term)) {
            $url = get_term_link($term);
            if (!is_wp_error($url)) return $url;
        }
    }
    return vt_shop_url();
}

/**
 * Permalink của một page theo slug, hoặc false nếu chưa tồn tại / chưa publish.
 *
 * @return string|false
 */
function vt_page_url($slug) {
    $page = get_page_by_path($slug);
    if ($page && $page->post_status === 'publish') {
        return get_permalink($page);
    }
    return false;
}

/**
 * In thẻ <a> CHỈ KHI page tồn tại. Chưa có page thì không in gì.
 * Nhờ vậy cột footer tự đầy lên khi user tạo page — không phải sửa lại code.
 */
function vt_maybe_link($slug, $label, $class = '') {
    $url = vt_page_url($slug);
    if (!$url) return;
    if ($class !== '') {
        printf('<a href="%s" class="%s">%s</a>', esc_url($url), esc_attr($class), esc_html($label));
    } else {
        printf('<a href="%s">%s</a>', esc_url($url), esc_html($label));
    }
}

/**
 * URL tìm kiếm giới hạn trong sản phẩm.
 * WooCommerce bật → tìm trong product. Chưa bật → tìm toàn site.
 */
function vt_search_url() {
    return class_exists('WooCommerce')
        ? home_url('/?s&post_type=product')
        : home_url('/?s');
}

/**
 * URL trang tài khoản.
 */
function vt_account_url() {
    if (function_exists('wc_get_page_permalink')) {
        $url = wc_get_page_permalink('myaccount');
        if ($url) return $url;
    }
    return wp_login_url();
}

/**
 * URL giỏ hàng.
 */
function vt_cart_url() {
    if (function_exists('wc_get_cart_url')) return wc_get_cart_url();
    return home_url('/cart');
}

/* -------------------------------------------------------------------------
 * Thương hiệu
 * ---------------------------------------------------------------------- */

/**
 * Tên brand đúng chính tả — có dấu sắc, có ®.
 * Dùng hàm này thay vì gõ tay, để một chỗ sửa là sửa hết.
 */
function vt_brand_name() {
    return 'VITALITÉ';
}

/**
 * In logo wordmark.
 * File hiện có là PNG đen tuyền, nền trong suốt (Logo/Black Sabbath/vitalite_LOGO-20.png).
 * CSS đảo màu bằng filter:invert(1) khi nằm trên nền tối.
 *
 * TODO khi có SVG: đổi <img> thành inline <svg fill="currentColor">, bỏ được filter,
 * nhẹ hơn (~2KB thay vì 13KB) và sắc nét ở mọi mật độ điểm ảnh.
 */
function vt_logo($class = 'vt-brand-mark') {
    $src = get_stylesheet_directory_uri() . '/assets/vitalite-wordmark-trim.png';
    printf(
        '<img src="%s" alt="%s" class="%s" width="140" height="20" decoding="async" />',
        esc_url($src),
        esc_attr(vt_brand_name()),
        esc_attr($class)
    );
}

/**
 * Danh sách kênh mạng xã hội THẬT.
 * Xác minh 2026-08-19 bằng cách mở trực tiếp từng trang.
 * Không dùng link trang chủ nền tảng.
 */
function vt_social_links() {
    return array(
        'IG'     => 'https://www.instagram.com/vitalitevn/',
        'TIKTOK' => 'https://www.tiktok.com/@vitalitevn',
        'FB'     => 'https://www.facebook.com/vitalitevn',
        'SHOPEE' => 'https://shopee.vn/vitalitevn',
    );
}

/**
 * Thông tin liên hệ đã xác minh (Facebook About, 2026-08-19).
 * [NEED] Hotline: FB About ghi 093 838 14 07, bài 2023 ghi 037 963 2222 — chưa rõ số nào còn dùng.
 */
function vt_contact_info() {
    return array(
        'email' => 'vitalitevn@gmail.com',
        'phone' => '093 838 14 07',
        'city'  => 'Saigon, Vietnam',
    );
}

/* -------------------------------------------------------------------------
 * Sản phẩm
 * ---------------------------------------------------------------------- */

/**
 * Ảnh MẶT SAU của sản phẩm, dùng cho hiệu ứng hover đổi mặt.
 *
 * QUY ƯỚC NHẬP HÀNG (bắt buộc, ghi trong deliverables/images/MOCKUP-PIPELINE.md):
 *   Product image        = MẶT TRƯỚC
 *   Gallery ảnh đầu tiên = MẶT SAU
 *   Gallery còn lại      = chi tiết, ảnh model
 *
 * Không có ảnh gallery → trả false → thẻ không hover, không lỗi.
 *
 * @param WC_Product $product
 * @return string|false URL ảnh
 */
function vt_product_back_image($product, $size = 'woocommerce_thumbnail') {
    if (!$product || !method_exists($product, 'get_gallery_image_ids')) return false;
    $ids = $product->get_gallery_image_ids();
    if (empty($ids)) return false;
    $url = wp_get_attachment_image_url($ids[0], $size);
    return $url ? $url : false;
}

/**
 * Sản phẩm có được coi là mới không.
 * Dùng ngày đăng, không dùng field tuỳ biến — để user không phải bảo trì thêm gì.
 */
function vt_product_is_new($product_id, $days = 30) {
    $posted = get_post_time('U', true, $product_id);
    if (!$posted) return false;
    return (time() - $posted) < ($days * DAY_IN_SECONDS);
}

/**
 * Danh sách mã màu của sản phẩm biến thể, để vẽ chấm màu trên thẻ.
 * Đọc từ attribute pa_color. Chưa có attribute → mảng rỗng, không vẽ gì.
 *
 * Map tên màu → hex nằm ở đây vì WooCommerce core không lưu hex cho term.
 * Thêm màu mới thì thêm vào mảng này.
 */
function vt_product_color_swatches($product) {
    if (!$product || !method_exists($product, 'get_attribute')) return array();
    $raw = $product->get_attribute('pa_color');
    if (!$raw) return array();

    $map = array(
        'black'      => '#0A0A0A',
        'white'      => '#FFFFFF',
        'pure white' => '#FFFFFF',
        'grey'       => '#B8B8BC',
        'gray'       => '#B8B8BC',
        'cream'      => '#EFE7D2',
    );

    $out = array();
    foreach (array_map('trim', explode(',', $raw)) as $name) {
        if ($name === '') continue;
        $key = strtolower($name);
        $out[] = array(
            'name' => $name,
            'hex'  => isset($map[$key]) ? $map[$key] : '#DDDDE1',
        );
    }
    return $out;
}

/* -------------------------------------------------------------------------
 * Gallery
 * ---------------------------------------------------------------------- */

/**
 * Danh sách ảnh cho lưới lookbook.
 *
 * Đọc thẳng thư mục `assets/gallery/`, sắp theo tên file.
 * Thả ảnh vào thư mục là hiện — không phải vào wp-admin thao tác gì.
 * Số ở đầu tên file quyết định thứ tự, và thứ tự quyết định ô nào to ô nào nhỏ.
 *
 * Kết quả được cache trong transient 12 tiếng: quét thư mục mỗi lượt tải trang
 * là I/O vô ích trên shared hosting. Thêm ảnh mới mà chưa thấy thì xoá transient
 * `vt_gallery` hoặc chờ 12 tiếng.
 *
 * Muốn quản lý bằng Media Library thay vì thư mục: hook vào filter `vt_gallery_images`.
 *
 * @param int $limit số ảnh tối đa
 * @return array danh sách ['url','alt','w','h']
 */
function vt_gallery_images($limit = 8) {

    $cached = get_transient('vt_gallery');
    if ($cached === false) {
        $dir  = get_stylesheet_directory() . '/assets/gallery/';
        $uri  = get_stylesheet_directory_uri() . '/assets/gallery/';
        $out  = array();

        if (is_dir($dir)) {
            $files = glob($dir . '*.{webp,jpg,jpeg,png}', GLOB_BRACE);
            if ($files) {
                sort($files, SORT_NATURAL);
                foreach ($files as $file) {
                    $name = basename($file);
                    $size = @getimagesize($file);
                    $out[] = array(
                        'url' => $uri . rawurlencode($name),
                        'alt' => '',   // ảnh trang trí — alt rỗng là ĐÚNG cho screen reader
                        'w'   => $size ? $size[0] : 0,
                        'h'   => $size ? $size[1] : 0,
                    );
                }
            }
        }
        set_transient('vt_gallery', $out, 12 * HOUR_IN_SECONDS);
        $cached = $out;
    }

    /**
     * Cho phép thay hẳn nguồn ảnh gallery.
     * @param array $cached
     */
    $images = apply_filters('vt_gallery_images', $cached);

    return $limit > 0 ? array_slice($images, 0, $limit) : $images;
}

/* -------------------------------------------------------------------------
 * Hiển thị
 * ---------------------------------------------------------------------- */

/**
 * Trang hiện tại có hero video tràn viền không.
 * Quyết định header khởi đầu ở chế độ trong suốt hay chế độ kính trắng.
 */
function vt_has_hero() {
    return is_front_page() && !is_paged();
}

/**
 * Trang này có BANNER ĐẦU TRANG không, và banner đó tông gì?
 *
 * Trả về 'dark' | 'light' | '' (không có banner).
 *
 * VÌ SAO CẦN HÀM NÀY
 *   Header dán trên đỉnh và TRONG SUỐT khi nằm đè lên banner. Muốn vậy, nội dung
 *   trang phải bắt đầu từ đúng mép trên viewport, không có khoảng đệm bằng chiều
 *   cao header. Nhưng trang KHÔNG có banner thì vẫn cần khoảng đệm đó, nếu không
 *   chữ chui xuống dưới header. Hàm này là chỗ DUY NHẤT quyết định điều đó,
 *   dùng chung cho: body class, meta theme-color, và CSS padding.
 *
 * ⚠️ PHẢI KHỚP VỚI TEMPLATE THẬT.
 *   Thêm banner vào template nào thì thêm điều kiện vào đây. Ngược lại cũng vậy.
 *   Lệch nhau thì header trong suốt nằm trên nền trắng = header tàng hình.
 *   JS có lưới an toàn: không tìm thấy sentinel thì tự trả header về chế độ đục
 *   và trả lại khoảng đệm — nhưng đừng dựa vào nó, hãy sửa cho khớp.
 *
 * @return string 'dark' | 'light' | ''
 */
function vt_top_banner_tone() {
    // Trang chủ: hero. Slide 1 tông tối — xem template-parts/hero.php
    if (vt_has_hero()) return 'dark';

    // Shop / category / tag: banner váng dầu, luôn tông tối
    // — xem woocommerce/archive-product.php
    if (function_exists('is_shop')
        && (is_shop() || is_product_category() || is_product_tag())) {
        return 'dark';
    }

    // Trang kết quả tìm kiếm: cùng banner với archive — xem search.php
    if (is_search()) return 'dark';

    /*
     * TRANG TĨNH CÓ BANNER TỐI Ở ĐẦU.
     *
     * Trang About mở bằng chuỗi frame nền đen cao 500vh. Header kính TRẮNG đè
     * lên đó cắt trang làm hai mảnh ngay giây đầu tiên — đúng thứ không được
     * xảy ra ở màn hình đầu.
     *
     * Theme không tự biết được: nội dung trang nằm trong post_content do user
     * dán vào, PHP ở đây không đọc được nó có banner tối hay không. Nên phải
     * KHAI BÁO. Thêm trang mới có banner tối thì thêm slug vào đây — hoặc hook
     * vào filter, không phải sửa file này.
     *
     * Đây chỉ là trạng thái ĐẦU. Cuộn qua hết banner thì site.js trả header về
     * kính trắng, dựa vào [data-vt-header-sentinel] mà fragment tự mang.
     */
    $vt_dark_pages = apply_filters('vt_dark_banner_pages', array('about'));
    if (!empty($vt_dark_pages) && is_page($vt_dark_pages)) return 'dark';

    // Mọi trang khác CHƯA có banner: page, single, cart, checkout, 404
    return '';
}

/**
 * In icon SVG inline. Inline chứ không dùng sprite hay icon font:
 * chỉ có vài icon, và inline thì ăn theo currentColor, không thêm request nào.
 */
function vt_icon($name) {
    $icons = array(
        'bag'    => '<path d="M6 7h12l1 13H5L6 7Z"/><path d="M9 7V5a3 3 0 0 1 6 0v2"/>',
        'search' => '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
        'user'   => '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/>',
        'menu'   => '<path d="M3 6h18M3 12h18M3 18h18"/>',
        'close'  => '<path d="M5 5l14 14M19 5L5 19"/>',
        'arrow'  => '<path d="M4 12h15M13 6l6 6-6 6"/>',
    );
    if (!isset($icons[$name])) return;
    printf(
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>',
        $icons[$name] // markup nội bộ, không phải input người dùng
    );
}
