<?php
/**
 * Form tìm kiếm.
 *
 * Mặc định tìm trong SẢN PHẨM khi WooCommerce bật — người vào site fashion
 * tìm áo, không tìm bài viết. Trường ẩn post_type giới hạn phạm vi mà
 * không cần thêm giao diện chọn lọc nào.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

$vt_id = 'vt-search-' . wp_unique_id();
?>
<form role="search" method="get" class="vt-search-form" action="<?php echo esc_url(home_url('/')); ?>">
  <label class="screen-reader-text" for="<?php echo esc_attr($vt_id); ?>">
    <?php esc_html_e('Search products', 'vitalite'); ?>
  </label>
  <input type="search"
         id="<?php echo esc_attr($vt_id); ?>"
         name="s"
         value="<?php echo esc_attr(get_search_query()); ?>"
         placeholder="<?php esc_attr_e('Search products…', 'vitalite'); ?>"
         autocomplete="off">
  <?php if (class_exists('WooCommerce')) : ?>
    <input type="hidden" name="post_type" value="product">
  <?php endif; ?>
  <button type="submit" class="vt-btn">
    <span class="screen-reader-text"><?php esc_html_e('Search', 'vitalite'); ?></span>
    <?php vt_icon('search'); ?>
  </button>
</form>
