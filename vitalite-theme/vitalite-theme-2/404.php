<?php
/**
 * 404.
 *
 * Site đang có nhiều URL cũ trỏ vào chỗ không tồn tại (link chia sẻ trước đây,
 * bookmark, và cả link nội bộ chưa dọn hết). Trang 404 phải là ngã rẽ, không phải ngõ cụt:
 * ô tìm kiếm + đường về Shop, ngay trên màn hình đầu.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

get_header();
?>

<section class="vt-center-page">
  <div class="vt-wrap vt-wrap-narrow">

    <p class="vt-mono" style="color: var(--vt-muted); margin: 0 0 12px;">404</p>

    <h1 class="vt-display"><?php esc_html_e('This page does not exist', 'vitalite'); ?></h1>

    <p class="vt-lede" style="margin: 0 auto 32px;">
      <?php esc_html_e('The link may be old, or the page may have moved.', 'vitalite'); ?>
    </p>

    <?php get_search_form(); ?>

    <p style="margin-top: 28px;">
      <a class="vt-btn" href="<?php echo esc_url(vt_shop_url()); ?>">
        <?php esc_html_e('Shop All', 'vitalite'); ?>
        <?php vt_icon('arrow'); ?>
      </a>
    </p>

  </div>
</section>

<?php
get_footer();
