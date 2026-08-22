<?php
/**
 * Trang tĩnh — About, Size Guide, Shipping, Returns, Contact, Collection…
 * VÀ các trang WooCommerce: Giỏ hàng, Thanh toán, Tài khoản.
 *
 * Trang dựng bằng Elementor sẽ tự chiếm quyền render nội dung; template này
 * chỉ lo phần khung (tiêu đề, khoảng cách, chiều rộng đọc). Nhờ vậy hai cách
 * dựng trang sống chung được, không phải chọn một.
 *
 * BA CHẾ ĐỘ KHUNG
 *   Elementor  — không khung gì cả, Elementor toàn quyền
 *   WooCommerce— khung RỘNG (.vt-wrap). Giỏ hàng và thanh toán là BẢNG và BIỂU MẪU
 *                hai cột; nhét vào khung đọc 860px là bảng bị bóp, cột địa chỉ
 *                xuống hàng lung tung. KHÔNG dùng .vt-prose ở đây — .vt-prose đặt
 *                margin lên mọi phần tử liền kề, nó phá khoảng cách của form Woo.
 *   Mặc định   — khung đọc hẹp + .vt-prose, cho trang chữ
 *
 * ⚠️ KHÔNG đụng logic giỏ hàng / thanh toán. Chỉ là khung và lớp sơn.
 *    Không gỡ field, không đổi thứ tự bước, không hook vào luồng đặt hàng.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

get_header();

while (have_posts()) :
    the_post();

    // Trang Elementor: bỏ header trang của theme, để Elementor toàn quyền
    $vt_is_elementor = class_exists('\Elementor\Plugin')
        && \Elementor\Plugin::$instance->documents->get(get_the_ID())
        && \Elementor\Plugin::$instance->documents->get(get_the_ID())->is_built_with_elementor();

    // Trang WooCommerce: giỏ hàng, thanh toán, tài khoản, "đã nhận đơn"
    $vt_is_woo_page = function_exists('is_cart')
        && (is_cart() || is_checkout() || is_account_page());

    if ($vt_is_elementor) {
        $vt_outer = $vt_inner = $vt_body = '';
    } elseif ($vt_is_woo_page) {
        $vt_outer = 'vt-section';
        $vt_inner = 'vt-wrap';
        $vt_body  = 'vt-woo-page';
    } else {
        $vt_outer = 'vt-section';
        $vt_inner = 'vt-wrap vt-wrap-narrow';
        $vt_body  = 'vt-prose';
    }
    ?>

    <article <?php post_class('vt-page'); ?>>

      <?php if (!$vt_is_elementor) : ?>
        <header class="vt-section vt-section--tight">
          <div class="<?php echo esc_attr($vt_is_woo_page ? 'vt-wrap' : 'vt-wrap vt-wrap-narrow'); ?>">
            <h1 class="vt-title"><?php the_title(); ?></h1>
          </div>
        </header>
      <?php endif; ?>

      <div class="<?php echo esc_attr($vt_outer); ?>">
        <div class="<?php echo esc_attr($vt_inner); ?>">
          <div class="<?php echo esc_attr($vt_body); ?>">
            <?php
            the_content();
            wp_link_pages(array(
                'before' => '<nav class="vt-page-links">',
                'after'  => '</nav>',
            ));
            ?>
          </div>
        </div>
      </div>

    </article>

    <?php
endwhile;

get_footer();
