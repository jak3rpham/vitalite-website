<?php
/**
 * Empty state — chưa có sản phẩm nào.
 *
 * Trung thực chứ không giả vờ có hàng. Và tận dụng đúng tài sản đang có:
 * Shopee đã bán 4 năm với 973 đánh giá / 4.9 sao. Site thì mới tinh.
 * Trong lúc chưa nhập hàng, đẩy khách sang chỗ mua được thật vẫn tốt hơn ngõ cụt.
 *
 * Gỡ link Shopee đi khi site đã có đủ sản phẩm.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;
?>
<div class="vt-empty">
  <p><?php esc_html_e('Products are being added.', 'vitalite'); ?></p>
  <a class="vt-btn vt-btn--ghost" href="https://shopee.vn/vitalitevn" target="_blank" rel="noopener">
    <?php esc_html_e('Shop on Shopee', 'vitalite'); ?>
    <?php vt_icon('arrow'); ?>
  </a>
</div>
