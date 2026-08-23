<?php
/**
 * VITALITÉ — CART ICON (i18n-ready)
 * Đích: template-parts/header/cart-icon.php
 *
 * Mọi chuỗi đi qua __() / _n() với text domain 'vitalite-theme'
 * → dịch được bằng Loco Translate, không cần sửa code.
 */
if (!defined('ABSPATH')) exit;

$count    = (function_exists('WC') && WC()->cart) ? WC()->cart->get_cart_contents_count() : 0;
$cart_url = function_exists('wc_get_cart_url') ? wc_get_cart_url() : home_url('/cart');
?>
<a href="<?php echo esc_url($cart_url); ?>"
   class="vt-cart"
   aria-label="<?php
     /* translators: %d = số sản phẩm trong giỏ */
     echo esc_attr(sprintf(
       _n('Shopping bag, %d item', 'Shopping bag, %d items', $count, 'vitalite-theme'),
       $count
     ));
   ?>">

  <svg class="vt-cart__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
    <path d="M5 8h14l-1.2 11.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8L5 8Z"/>
    <path d="M9 8V6.2a3 3 0 0 1 6 0V8"/>
  </svg>

  <span class="vt-cart__count" data-count="<?php echo esc_attr($count); ?>" aria-hidden="true"><?php
    echo esc_html($count > 99 ? '99+' : $count);
  ?></span>
</a>
<?php
/* ==================================================================
   1. THAY filter cũ trong functions.php bằng đoạn này.
      Fragment PHẢI khớp selector mới, nếu không badge sẽ không
      update sau AJAX add-to-cart.
   ==================================================================

add_filter('woocommerce_add_to_cart_fragments', function ($fragments) {
    $count = (function_exists('WC') && WC()->cart) ? WC()->cart->get_cart_contents_count() : 0;
    ob_start(); ?>
    <span class="vt-cart__count" data-count="<?php echo esc_attr($count); ?>" aria-hidden="true"><?php
      echo esc_html($count > 99 ? '99+' : $count);
    ?></span>
    <?php
    $fragments['span.vt-cart__count'] = ob_get_clean();
    return $fragments;
});

   ==================================================================
   2. HEADER RIGHT — markup mới cho SEARCH / ACCOUNT (đậm hơn + i18n)
   ==================================================================

<a href="#" class="vt-util-link vt-search-toggle" data-vt-search>
  <?php esc_html_e('Search', 'vitalite-theme'); ?>
</a>

<a href="<?php echo esc_url(wc_get_page_permalink('myaccount')); ?>" class="vt-util-link">
  <?php esc_html_e('Account', 'vitalite-theme'); ?>
</a>

<?php get_template_part('template-parts/header/cart-icon'); ?>

   QUY ƯỚC STRING: viết Title Case ('Search') trong code, để CSS
   text-transform: uppercase lo phần hiển thị.
   Lý do: tiếng Việt uppercase toàn bộ mất dấu khó đọc — sau này
   chỉ cần bỏ text-transform ở bản VI, không phải sửa string.

   ==================================================================
   3. TODO khi implement
   ==================================================================
   [ ] #vtSearchModal chưa tồn tại trong header — kiểm tra support.js
       hoặc build mới. Hiện onclick trỏ vào element không có.
   [ ] Lấy mã đỏ chính thức cho --vt-badge-red (đang placeholder #E0202A)
*/
