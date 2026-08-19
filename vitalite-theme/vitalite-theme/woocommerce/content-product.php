<?php
/**
 * Một ô sản phẩm trong lưới — override của WooCommerce.
 *
 * Chỉ là vỏ mỏng gọi template-parts/product-card.php, để thẻ sản phẩm
 * trên trang chủ, trang shop và trang tìm kiếm là CÙNG MỘT file.
 * Sửa thẻ ở một chỗ là sửa cả ba.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

global $product;

if (empty($product) || !$product->is_visible()) {
    return;
}

get_template_part('template-parts/product-card');
