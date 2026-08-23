<?php
/**
 * Shop archive — override của WooCommerce.
 *
 * Đây là MỘT TRONG HAI file template Woo bị đè (file kia là content-product.php).
 * Đè hai file này là bắt buộc để đổi cấu trúc lưới. Mọi thứ khác đi qua hook
 * trong inc/woocommerce.php, để Woo update không phá.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

get_header();

/**
 * Hook: woocommerce_before_main_content — giữ lại cho plugin (Premmerce…) cắm vào
 */
do_action('woocommerce_before_main_content');

/*
 * BANNER ĐẦU TRANG — nền tối + váng dầu, tràn hai mép.
 *
 * Nó thay cho ảnh campaign của category. Chưa category nào có ảnh riêng, và
 * để một khối xám trống thì tệ hơn hẳn. Banner này 0 KB, chạy được ngay.
 * Khi có ảnh thật: truyền thêm vào section-page-banner và nhớ PRELOAD —
 * banner nằm trên cùng nên ảnh ở đây sẽ thành phần tử LCP.
 *
 * <h1> của trang nằm TRONG banner, không phải trong .vt-shop-head. Chỉ có một h1.
 */
$vt_found = isset($GLOBALS['wp_query']) ? (int) $GLOBALS['wp_query']->found_posts : 0;

// Mô tả category — chỉ hiện nếu người nhập hàng có viết thật. Không có thì bỏ trống,
// KHÔNG sinh câu mô tả tự động: đó là bịa nội dung brand.
$vt_lede = is_product_category() ? term_description() : '';

get_template_part('template-parts/section-page-banner', null, array(
    'eyebrow' => __('Shop', 'vitalite'),
    'title'   => vt_shop_heading(),
    'lede'    => $vt_lede,
    'meta'    => $vt_found
        ? sprintf(
            /* translators: %s: số sản phẩm */
            _n('%s product', '%s products', $vt_found, 'vitalite'),
            number_format_i18n($vt_found)
          )
        : '',
    'tag'     => 'h1',
));
?>

<div class="vt-wrap">

  <header class="vt-shop-head">
    <?php woocommerce_breadcrumb(); ?>
  </header>

  <?php if (woocommerce_product_loop()) : ?>

    <div class="vt-shop-toolbar">
      <?php
      /*
       * Bộ lọc của Premmerce Product Filter cắm vào đây qua hook
       * woocommerce_before_shop_loop (ưu tiên < 20).
       */
      do_action('woocommerce_before_shop_loop');
      ?>
    </div>

    <?php
    /*
     * Giữ class "products" bên cạnh "vt-grid".
     * Ta không gọi woocommerce_product_loop_start() (nó in ra <ul class="products">
     * mà ta không muốn), nhưng nhiều plugin — trong đó có bộ lọc AJAX của Premmerce —
     * tìm container theo selector .products để thay nội dung. Thiếu class này thì
     * lọc AJAX không tìm thấy chỗ để đổ kết quả vào.
     *
     * Và KHÔNG kiểm tra wc_get_loop_prop('total') ở đây: giá trị đó do
     * woocommerce_product_loop_start() đặt, mà ta không gọi hàm đó — nên nó bằng 0
     * và vòng lặp sẽ không bao giờ chạy. have_posts() là điều kiện đúng.
     */
    ?>
    <div class="vt-grid products">
      <?php
      while (have_posts()) {
          the_post();
          do_action('woocommerce_shop_loop');
          wc_get_template_part('content', 'product');
      }
      ?>
    </div>

    <?php
    // Phân trang
    do_action('woocommerce_after_shop_loop');
    ?>

  <?php else : ?>

    <div class="vt-grid">
      <?php get_template_part('template-parts/empty-state'); ?>
    </div>

  <?php endif; ?>

</div>

<?php
do_action('woocommerce_after_main_content');

get_footer();
