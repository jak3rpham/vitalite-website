<?php
/**
 * Footer.
 *
 * Hai nguyên tắc:
 *   1. Không in link tới page chưa tồn tại. vt_maybe_link() im lặng bỏ qua.
 *      Cột Support tự đầy lên khi user tạo page — không phải sửa lại file này.
 *   2. Không có form newsletter cho tới khi nối provider thật.
 *      Form nhận email rồi vứt đi là lừa khách.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

if (function_exists('vt_mark_rendered')) { vt_mark_rendered('vt_footer'); }

$vt_contact = vt_contact_info();
$vt_shop    = vt_shop_url();
?>

<footer class="vt-footer">
  <div class="vt-wrap">
    <div class="vt-footer-grid">

      <div class="vt-footer-brand">
        <?php vt_logo('vt-footer-logo'); ?>
        <?php
        /*
         * "Made in Vietnam" — fact đã xác minh: user xác nhận, và Shopee khai
         * xuất xứ Việt Nam trong thuộc tính sản phẩm.
         * ĐÃ GỠ "Sản xuất giới hạn, phát hành theo đợt" — user xác nhận không cần nêu.
         * Không thêm claim nào khác vào đây mà chưa có nguồn.
         */
        ?>
        <p class="vt-footer-desc"><?php esc_html_e('Streetwear made in Vietnam.', 'vitalite'); ?></p>
      </div>

      <div>
        <div class="vt-footer-col-title"><?php esc_html_e('Shop', 'vitalite'); ?></div>
        <div class="vt-footer-links">
          <?php
          if (has_nav_menu('footer_shop')) {
              wp_nav_menu(array(
                  'theme_location' => 'footer_shop',
                  'container'      => false,
                  'items_wrap'     => '%3$s',
                  'depth'          => 1,
                  'fallback_cb'    => false,
              ));
          } else {
              printf('<a href="%s">%s</a>', esc_url($vt_shop), esc_html__('Shop All', 'vitalite'));
              printf('<a href="%s">%s</a>', esc_url(add_query_arg('orderby', 'date', $vt_shop)), esc_html__('New Arrivals', 'vitalite'));
              printf('<a href="%s">%s</a>', esc_url(vt_cat_url('t-shirts')), esc_html__('T-Shirts', 'vitalite'));
              printf('<a href="%s">%s</a>', esc_url(vt_cat_url('outerwear')), esc_html__('Outerwear', 'vitalite'));
              printf('<a href="%s">%s</a>', esc_url(add_query_arg('on_sale', '1', $vt_shop)), esc_html__('Sale', 'vitalite'));
          }
          ?>
        </div>
      </div>

      <div>
        <div class="vt-footer-col-title"><?php esc_html_e('Support', 'vitalite'); ?></div>
        <div class="vt-footer-links">
          <?php
          if (has_nav_menu('footer_support')) {
              wp_nav_menu(array(
                  'theme_location' => 'footer_support',
                  'container'      => false,
                  'items_wrap'     => '%3$s',
                  'depth'          => 1,
                  'fallback_cb'    => false,
              ));
          } else {
              // Chỉ in link khi page có thật. Nội dung 4 trang này là policy fact — user viết.
              vt_maybe_link('size-guide', __('Size Guide', 'vitalite'), '');
              vt_maybe_link('shipping',   __('Shipping', 'vitalite'), '');
              vt_maybe_link('returns',    __('Returns', 'vitalite'), '');
              vt_maybe_link('contact',    __('Contact', 'vitalite'), '');
          }
          ?>
          <a href="mailto:<?php echo esc_attr($vt_contact['email']); ?>"><?php echo esc_html($vt_contact['email']); ?></a>
        </div>
      </div>

      <div>
        <div class="vt-footer-col-title"><?php esc_html_e('Follow', 'vitalite'); ?></div>
        <div class="vt-footer-links">
          <?php foreach (vt_social_links() as $vt_label => $vt_href) : ?>
            <a href="<?php echo esc_url($vt_href); ?>" target="_blank" rel="noopener me"><?php echo esc_html($vt_label); ?></a>
          <?php endforeach; ?>
        </div>
        <?php
        /*
         * KHÔNG có form newsletter ở đây.
         * Bản cũ có <form onsubmit="alert('Cảm ơn bạn đã đăng ký!')"> và không lưu email
         * đi đâu cả. Khách nhập email, nhận lời cảm ơn, không có gì xảy ra.
         * Bật lại khi đã nối Mailchimp / Klaviyo / Brevo thật — không phải trước đó.
         */
        ?>
      </div>

    </div>

    <div class="vt-footer-bottom">
      <span>&copy; <?php echo esc_html(date_i18n('Y')); ?> <?php echo esc_html(vt_brand_name()); ?>&reg;</span>
      <span><?php echo esc_html($vt_contact['city']); ?></span>
    </div>
  </div>
</footer>
