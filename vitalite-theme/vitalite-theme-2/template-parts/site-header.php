<?php
/**
 * Header — thanh điều hướng dán trên đỉnh.
 *
 * Hai chế độ hiển thị:
 *   .is-transparent  — trong suốt, không viền, chữ trắng. Dùng khi header đang
 *                      ĐÈ LÊN BANNER đầu trang (hero trang chủ, banner archive…)
 *   .is-light-bg     — thêm vào khi banner bên dưới tông SÁNG, chữ đảo sang đen
 *   mặc định         — kính trắng mờ, chữ đen
 *
 * Chế độ do JS đổi bằng IntersectionObserver theo dõi [data-vt-header-sentinel]
 * — phần tử 1px dán ở đáy banner. Không dành riêng cho hero nữa.
 * Không nghe sự kiện scroll — scroll listener chạy hàng chục lần mỗi giây,
 * IntersectionObserver chỉ chạy đúng lúc vượt ngưỡng.
 *
 * Trạng thái khởi đầu render sẵn ở server để không bị nháy khi tải trang.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

// Đánh dấu đã render — chặn [vt_header] trên trang Elementor cũ render lần hai
if (function_exists('vt_mark_rendered')) { vt_mark_rendered('vt_header'); }

// Tone banner đầu trang: 'dark' | 'light' | '' — xem inc/helpers.php
$vt_tone     = vt_top_banner_tone();
$vt_cart_url = vt_cart_url();

$vt_header_class = 'vt-header';
if ($vt_tone)              $vt_header_class .= ' is-transparent';
if ($vt_tone === 'light')  $vt_header_class .= ' is-light-bg';
?>

<header id="vt-header"
        class="<?php echo esc_attr($vt_header_class); ?>"
        data-banner-tone="<?php echo esc_attr($vt_tone); ?>">

  <div class="vt-header-left">

    <button type="button" class="vt-burger" aria-label="<?php esc_attr_e('Open menu', 'vitalite'); ?>"
            aria-expanded="false" aria-controls="vt-mobile-nav" data-vt-menu-open>
      <?php vt_icon('menu'); ?>
    </button>

    <a class="vt-brand" href="<?php echo esc_url(home_url('/')); ?>" rel="home">
      <?php vt_logo(); ?>
      <span class="screen-reader-text"><?php echo esc_html(vt_brand_name()); ?></span>
    </a>

    <nav class="vt-nav-wrap" aria-label="<?php esc_attr_e('Primary', 'vitalite'); ?>">
      <?php
      /*
       * Menu do user tạo trong Giao diện → Menu thì dùng menu đó.
       * Chưa tạo thì rơi xuống menu dựng sẵn bên dưới — mọi link đều tự lành,
       * không có link nào trỏ vào 404.
       */
      if (has_nav_menu('primary')) {
          wp_nav_menu(array(
              'theme_location' => 'primary',
              'container'      => false,
              'menu_class'     => 'vt-nav',
              'depth'          => 1,
              'fallback_cb'    => false,
          ));
      } else {
          $vt_shop = vt_shop_url();
          $vt_items = array(
              array('url' => $vt_shop, 'label' => __('Shop All', 'vitalite')),
              array('url' => add_query_arg('orderby', 'date', $vt_shop), 'label' => __('New Arrivals', 'vitalite')),
              array('url' => vt_cat_url('t-shirts'), 'label' => __('T-Shirts', 'vitalite')),
              array('url' => vt_cat_url('outerwear'), 'label' => __('Outerwear', 'vitalite')),
              array('url' => add_query_arg('on_sale', '1', $vt_shop), 'label' => __('Sale', 'vitalite')),
          );
          // Collection và About chỉ hiện khi page đã tồn tại
          foreach (array('collection' => __('Collection', 'vitalite'), 'about' => __('About', 'vitalite')) as $vt_slug => $vt_label) {
              if ($vt_url = vt_page_url($vt_slug)) {
                  $vt_items[] = array('url' => $vt_url, 'label' => $vt_label);
              }
          }
          echo '<ul class="vt-nav">';
          foreach ($vt_items as $vt_item) {
              printf('<li><a href="%s">%s</a></li>', esc_url($vt_item['url']), esc_html($vt_item['label']));
          }
          echo '</ul>';
      }
      ?>
    </nav>
  </div>

  <div class="vt-header-right">

    <?php
    /*
     * Chuyển ngôn ngữ.
     * Chỉ hiện khi Polylang đã bật VÀ có từ 2 ngôn ngữ trở lên.
     * Chữ EN / VI, KHÔNG dùng cờ quốc gia — cờ là quốc gia, không phải ngôn ngữ.
     */
    if (function_exists('pll_the_languages')) {
        $vt_langs = pll_the_languages(array('raw' => 1, 'hide_if_no_translation' => 0));
        if (is_array($vt_langs) && count($vt_langs) > 1) {
            echo '<div class="vt-lang">';
            $vt_i = 0;
            foreach ($vt_langs as $vt_lang) {
                if ($vt_i > 0) echo '<span class="vt-lang-sep" aria-hidden="true">/</span>';
                printf(
                    '<a href="%s" class="%s" lang="%s">%s</a>',
                    esc_url($vt_lang['url']),
                    !empty($vt_lang['current_lang']) ? 'is-active' : '',
                    esc_attr($vt_lang['slug']),
                    esc_html(strtoupper($vt_lang['slug']))
                );
                $vt_i++;
            }
            echo '</div>';
        }
    }
    ?>

    <a class="vt-util vt-util--search" href="<?php echo esc_url(vt_search_url()); ?>">
      <?php esc_html_e('Search', 'vitalite'); ?>
    </a>

    <a class="vt-util vt-util--account" href="<?php echo esc_url(vt_account_url()); ?>">
      <?php esc_html_e('Account', 'vitalite'); ?>
    </a>

    <a class="vt-cart" href="<?php echo esc_url($vt_cart_url); ?>">
      <?php vt_icon('bag'); ?>
      <span class="screen-reader-text"><?php esc_html_e('Cart', 'vitalite'); ?></span>
      <?php
      if (function_exists('vt_cart_count_markup')) {
          vt_cart_count_markup();
      }
      ?>
    </a>
  </div>
</header>

<?php
/*
 * Menu mobile. Render sẵn trong HTML thay vì dựng bằng JS —
 * mở ra là hiện ngay, không chờ script, và bot đọc được link.
 */
?>
<div id="vt-mobile-nav" class="vt-mobile-nav" hidden>
  <button type="button" class="vt-mobile-close" aria-label="<?php esc_attr_e('Close menu', 'vitalite'); ?>" data-vt-menu-close>
    <?php vt_icon('close'); ?>
  </button>

  <?php
  if (has_nav_menu('primary')) {
      wp_nav_menu(array(
          'theme_location' => 'primary',
          'container'      => false,
          'depth'          => 1,
          'items_wrap'     => '%3$s',
          'fallback_cb'    => false,
      ));
  } else {
      $vt_shop = vt_shop_url();
      printf('<a href="%s">%s</a>', esc_url($vt_shop), esc_html__('Shop All', 'vitalite'));
      printf('<a href="%s">%s</a>', esc_url(add_query_arg('orderby', 'date', $vt_shop)), esc_html__('New Arrivals', 'vitalite'));
      printf('<a href="%s">%s</a>', esc_url(vt_cat_url('t-shirts')), esc_html__('T-Shirts', 'vitalite'));
      printf('<a href="%s">%s</a>', esc_url(vt_cat_url('outerwear')), esc_html__('Outerwear', 'vitalite'));
      printf('<a href="%s">%s</a>', esc_url(add_query_arg('on_sale', '1', $vt_shop)), esc_html__('Sale', 'vitalite'));
      foreach (array('collection' => __('Collection', 'vitalite'), 'about' => __('About', 'vitalite')) as $vt_slug => $vt_label) {
          if ($vt_url = vt_page_url($vt_slug)) {
              printf('<a href="%s">%s</a>', esc_url($vt_url), esc_html($vt_label));
          }
      }
  }
  ?>

  <div class="vt-mobile-foot">
    <a href="<?php echo esc_url(vt_search_url()); ?>"><?php esc_html_e('Search', 'vitalite'); ?></a>
    <a href="<?php echo esc_url(vt_account_url()); ?>"><?php esc_html_e('Account', 'vitalite'); ?></a>
    <?php foreach (vt_social_links() as $vt_label => $vt_href) : ?>
      <a href="<?php echo esc_url($vt_href); ?>" target="_blank" rel="noopener me"><?php echo esc_html($vt_label); ?></a>
    <?php endforeach; ?>
  </div>
</div>
