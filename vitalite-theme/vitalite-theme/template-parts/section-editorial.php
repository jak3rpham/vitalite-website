<?php
/**
 * Khối editorial — một ảnh, một đoạn chữ.
 *
 * Dùng ảnh MODEL, không dùng mockup. Đây là chỗ duy nhất trên trang chủ mà
 * ảnh model phát huy tác dụng: khách cần thấy dáng thật trên người thật.
 *
 * RÀNG BUỘC THẬT: hiện chỉ có 5 ảnh model, tải từ CDN Facebook, 4 dọc 1 ngang,
 * đã bị nén một lần. Khung 4:5 chọn theo đúng tỉ lệ đa số ảnh đang có.
 * Không thiết kế thứ gì cần loại ảnh brand chưa chụp được.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

$vt_args = wp_parse_args(
    isset($args) && is_array($args) ? $args : array(),
    array(
        'image'     => '',
        'alt'       => '',
        'eyebrow'   => '',
        'title'     => '',
        'text'      => '',
        'cta_url'   => '',
        'cta_label' => '',
        'flip'      => false,
    )
);

if (!$vt_args['image']) return;
?>

<section class="vt-section">
  <div class="vt-wrap">
    <div class="vt-editorial<?php echo esc_attr($vt_args['flip'] ? ' vt-editorial--flip' : ''); ?>">

      <div class="vt-editorial-media">
        <img src="<?php echo esc_url($vt_args['image']); ?>"
             alt="<?php echo esc_attr($vt_args['alt']); ?>"
             width="900" height="1125"
             loading="lazy" decoding="async">
      </div>

      <div class="vt-editorial-body">
        <?php if ($vt_args['eyebrow']) : ?>
          <p class="vt-mono" style="color: var(--vt-muted); margin: 0;"><?php echo esc_html($vt_args['eyebrow']); ?></p>
        <?php endif; ?>

        <?php if ($vt_args['title']) : ?>
          <h2 class="vt-title"><?php echo esc_html($vt_args['title']); ?></h2>
        <?php endif; ?>

        <?php if ($vt_args['text']) : ?>
          <p class="vt-lede"><?php echo esc_html($vt_args['text']); ?></p>
        <?php endif; ?>

        <?php if ($vt_args['cta_url'] && $vt_args['cta_label']) : ?>
          <p>
            <a class="vt-btn vt-btn--ghost" href="<?php echo esc_url($vt_args['cta_url']); ?>">
              <?php echo esc_html($vt_args['cta_label']); ?>
              <?php vt_icon('arrow'); ?>
            </a>
          </p>
        <?php endif; ?>
      </div>

    </div>
  </div>
</section>
