<?php
/**
 * VITALITÉ — Bootstrap
 *
 * File này KHÔNG chứa logic. Nó chỉ nạp các module trong inc/.
 * Thứ tự nạp có ý nghĩa: helpers phải có trước, mọi file sau đều gọi tới nó.
 *
 * Kiến trúc (chốt trong CLAUDE.md, "Con đường A"):
 *   - Header/footer bằng PHP template, KHÔNG dùng Elementor Theme Builder
 *   - Không hardcode dữ liệu sản phẩm ở bất kỳ đâu
 *   - Không đụng logic cart/checkout
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

define('VT_VERSION', '2.0.0');
define('VT_DIR', get_stylesheet_directory());
define('VT_URI', get_stylesheet_directory_uri());

$vt_modules = array(
    'helpers',       // phải nạp đầu tiên — mọi file sau đều dùng
    'setup',
    'enqueue',
    'seo',
);

// WooCommerce có thể bị tắt (khi debug, hoặc trước khi cài). Không được để trắng site.
if (class_exists('WooCommerce')) {
    $vt_modules[] = 'woocommerce';
}

foreach ($vt_modules as $vt_module) {
    $vt_file = VT_DIR . '/inc/' . $vt_module . '.php';
    if (file_exists($vt_file)) {
        require_once $vt_file;
    }
}
unset($vt_modules, $vt_module, $vt_file);
