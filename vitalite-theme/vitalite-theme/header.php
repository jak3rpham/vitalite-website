<?php
/**
 * Header của site.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <?php
  /*
   * theme_color phải khớp nền THẬT ở đỉnh trang, nếu không thanh địa chỉ trên
   * Chrome Android sẽ lệch màu so với đầu trang.
   * Trang mở bằng banner tối → tối. Không có banner → nền trắng.
   */
  $vt_theme_color = (vt_top_banner_tone() === 'dark') ? '#0A0A0A' : '#FFFFFF';
  ?>
  <meta name="theme-color" content="<?php echo esc_attr($vt_theme_color); ?>">
  <link rel="profile" href="https://gmpg.org/xfn/11">
  <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<a class="vt-skip" href="#vt-main"><?php esc_html_e('Skip to content', 'vitalite'); ?></a>

<?php get_template_part('template-parts/site-header'); ?>

<main id="vt-main" class="vt-main">
