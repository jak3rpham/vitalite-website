<?php
/**
 * Lưới sản phẩm cho trang chủ.
 *
 * HOÀN TOÀN ĐỘNG. Không có mảng sản phẩm hardcode ở đây.
 * Bản cũ hardcode 8 SKU không có thật ('Heavyweight Hoodie 480GSM' 1.290.000₫…)
 * với nút thêm giỏ hàng chỉ chạy alert(). Đã xoá.
 *
 * Chưa có sản phẩm → hiện empty state trung thực, không giả vờ có hàng.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

if (!class_exists('WooCommerce')) return;

$vt_args = wp_parse_args(
    isset($args) && is_array($args) ? $args : array(),
    array(
        'title'   => __('New Arrivals', 'vitalite'),
        'number'  => '',        // '01' — số thứ tự section, để trống thì không in eyebrow
        'kicker'  => '',        // chữ sau số, ví dụ 'FEATURED'
        'count'   => 8,
        'orderby' => 'date',
        'cat'     => '',        // slug product_cat, để trống = tất cả
        'layout'  => 'uniform', // 'featured' = ô đầu tiên chiếm 2×2
    )
);

$vt_query_args = array(
    'post_type'           => 'product',
    'post_status'         => 'publish',
    'posts_per_page'      => (int) $vt_args['count'],
    'orderby'             => $vt_args['orderby'],
    'order'               => 'DESC',
    'ignore_sticky_posts' => 1,
    'no_found_rows'       => true,   // không cần đếm tổng — bỏ đi tiết kiệm một query
    'tax_query'           => array(
        array(
            'taxonomy' => 'product_visibility',
            'field'    => 'name',
            'terms'    => 'exclude-from-catalog',
            'operator' => 'NOT IN',
        ),
    ),
);

if ($vt_args['cat']) {
    $vt_query_args['tax_query'][] = array(
        'taxonomy' => 'product_cat',
        'field'    => 'slug',
        'terms'    => $vt_args['cat'],
    );
}

$vt_loop = new WP_Query($vt_query_args);
?>

<section class="vt-section">
  <div class="vt-wrap">

    <div class="vt-section-head">
      <div>
        <?php if ($vt_args['number'] || $vt_args['kicker']) : ?>
          <p class="vt-eyebrow">
            <?php echo esc_html(trim($vt_args['number'] . ' — ' . $vt_args['kicker'], ' —')); ?>
          </p>
        <?php endif; ?>
        <h2 class="vt-title"><?php echo esc_html($vt_args['title']); ?></h2>
      </div>
      <a class="vt-link vt-mono" href="<?php echo esc_url(vt_shop_url()); ?>">
        <?php esc_html_e('View all', 'vitalite'); ?> →
      </a>
    </div>

    <div class="vt-grid<?php echo esc_attr($vt_args['layout'] === 'featured' ? ' vt-grid--featured' : ''); ?>">
      <?php
      if ($vt_loop->have_posts()) {
          while ($vt_loop->have_posts()) {
              $vt_loop->the_post();
              get_template_part('template-parts/product-card');
          }
          wp_reset_postdata();
      } else {
          get_template_part('template-parts/empty-state');
      }
      ?>
    </div>

  </div>
</section>
