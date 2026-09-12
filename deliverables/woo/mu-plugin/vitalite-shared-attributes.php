<?php
/**
 * Plugin Name: VITALITÉ — attribute dùng chung hai ngôn ngữ
 * Description: Gỡ pa_size, pa_color, pa_collection, pa_print khỏi danh sách taxonomy
 *              được Polylang dịch. Term dùng chung cho cả EN lẫn VI.
 * Version:     1.0.0
 * Author:      VITALITÉ
 *
 * ---------------------------------------------------------------------------
 * VÌ SAO LÀ MU-PLUGIN CHỨ KHÔNG PHẢI THEME
 * ---------------------------------------------------------------------------
 * Bản đầu đặt filter này trong inc/woocommerce.php của theme và KHÔNG ăn —
 * cột cờ ngôn ngữ vẫn còn nguyên. Lý do là thứ tự nạp:
 *
 *     mu-plugins  →  plugins (Polylang)  →  theme functions.php
 *
 * Polylang dựng danh sách taxonomy được dịch ngay khi nó khởi động, tức là
 * TRƯỚC khi file theme được đọc. Filter đăng ký trong theme là đăng ký sau
 * khi danh sách đã chốt — không bao giờ chạy.
 *
 * mu-plugins nạp trước tất cả. Đây là chỗ duy nhất đúng cho filter này.
 *
 * ---------------------------------------------------------------------------
 * VẤN ĐỀ NÓ GIẢI QUYẾT
 * ---------------------------------------------------------------------------
 * vt_product_color_swatches() trong theme (inc/helpers.php) map TÊN term sang
 * mã màu để vẽ chấm màu trên thẻ sản phẩm:
 *
 *     'black' => '#0A0A0A', 'white' => '#FFFFFF', 'grey' => '#B8B8BC', …
 *
 * Dịch `Black` thành `Đen` là không khớp map, rơi về #DDDDE1 — mọi chấm màu
 * trên /vi/ thành xám. Không có lỗi PHP, không có cảnh báo, chỉ là trông hỏng.
 *
 * Bốn taxonomy dưới đây không có gì để dịch:
 *   pa_size        S / M / L giống hệt nhau ở hai ngôn ngữ
 *   pa_color       xem trên
 *   pa_collection  Pink Graffiti, Porsche… là tên riêng
 *   pa_print       một term duy nhất
 *
 * pa_fabric và pa_fit CỐ Ý không có trong danh sách — "Signature Boxy Fit"
 * dịch sang tiếng Việt có ích thật. Muốn tắt nốt thì thêm vào mảng $shared.
 *
 * ---------------------------------------------------------------------------
 * CÀI
 * ---------------------------------------------------------------------------
 * Upload file này vào:  wp-content/mu-plugins/vitalite-shared-attributes.php
 * Chưa có thư mục mu-plugins thì tạo. Không cần kích hoạt — mu-plugin luôn chạy.
 *
 * KIỂM: Products → Attributes → Color → Configure terms.
 *       Hai cột cờ 🇻🇳 🇺🇸 phải biến mất.
 *
 * ĐẢO LẠI: xoá file này. Polylang bật dịch lại như cũ, không mất dữ liệu.
 *
 * @package Vitalite
 */

defined('ABSPATH') || exit;

/**
 * Taxonomy sản phẩm dùng chung cho mọi ngôn ngữ.
 *
 * Polylang chạy filter này để biết taxonomy nào được dịch. Gỡ khỏi mảng
 * là Polylang thôi chia term theo ngôn ngữ, và cột cờ trong admin biến mất.
 *
 * @param array $taxonomies Mảng taxonomy được dịch, key = tên taxonomy.
 * @param bool  $is_settings True khi đang dựng màn hình cài đặt Polylang.
 * @return array
 */
add_filter('pll_get_taxonomies', function ($taxonomies, $is_settings) {

    $shared = array(
        'pa_size',
        'pa_color',
        'pa_collection',
        'pa_print',
    );

    foreach ($shared as $taxonomy) {
        unset($taxonomies[$taxonomy]);
    }

    return $taxonomies;
}, 100, 2);
