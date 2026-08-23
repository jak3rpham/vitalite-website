<?php
/**
 * COLLECTION — khối chia đôi, nền tối, tràn viền.
 *
 * Chữ trái, ảnh campaign phải. Đây là điểm nghỉ giữa hai lưới sản phẩm,
 * và là chỗ DUY NHẤT trên trang chủ được nói dài hơn một dòng.
 *
 * Không có mockup sản phẩm ở đây → dùng được nền tối mà không vướng
 * vấn đề mockup có nền trắng nung sẵn.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

$vt_args = wp_parse_args(
    isset($args) && is_array($args) ? $args : array(),
    array(
        'number'    => '',
        'kicker'    => '',
        'title'     => '',
        'text'      => '',
        'image'     => '',
        'alt'       => '',
        'cta_url'   => '',
        'cta_label' => '',
        'flip'      => false,
    )
);

if (!$vt_args['title']) return;
?>

<?php /* .vt-bleed chứ không phải .vt-wrap — khối đen phải chạm hai mép màn hình,
         không được có viền trắng hai bên. Lề chữ do .vt-collection-body tự lo. */ ?>
<section class="vt-section">
  <div class="vt-bleed">
    <div class="vt-collection<?php echo esc_attr($vt_args['flip'] ? ' vt-collection--flip' : ''); ?>">

      <div class="vt-collection-body">
        <?php if ($vt_args['number'] || $vt_args['kicker']) : ?>
          <p class="vt-collection-eyebrow">
            <?php echo esc_html(trim($vt_args['number'] . ' — ' . $vt_args['kicker'], ' —')); ?>
          </p>
        <?php endif; ?>

        <div>
          <h2 class="vt-collection-title">
            <?php echo wp_kses($vt_args['title'], array('br' => array())); ?>
          </h2>

          <?php if ($vt_args['text']) : ?>
            <p class="vt-collection-text"><?php echo esc_html($vt_args['text']); ?></p>
          <?php endif; ?>

          <?php if ($vt_args['cta_url'] && $vt_args['cta_label']) : ?>
            <a class="vt-btn vt-btn--on-dark" href="<?php echo esc_url($vt_args['cta_url']); ?>">
              <?php echo esc_html($vt_args['cta_label']); ?>
              <?php vt_icon('arrow'); ?>
            </a>
          <?php endif; ?>
        </div>
      </div>

      <div class="vt-collection-media">
        <?php if ($vt_args['image']) : ?>
          <img src="<?php echo esc_url($vt_args['image']); ?>"
               alt="<?php echo esc_attr($vt_args['alt']); ?>"
               width="1050" height="1400"
               loading="lazy" decoding="async">
        <?php endif; ?>
      </div>

    </div>
  </div>
</section>
