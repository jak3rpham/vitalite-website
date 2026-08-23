<?php
/**
 * Band iridescent — vùng kể chuyện, KHÔNG có mockup sản phẩm.
 *
 * VÌ SAO Ở ĐÂY MÀ KHÔNG PHẢI CHỖ KHÁC
 *   Nền toàn site là trắng để tôn sản phẩm — đúng chuẩn site fashion.
 *   Mockup hiện tại lại có nền trắng nung sẵn (xuất từ Canva), nên đặt sản phẩm
 *   lên nền tối sẽ lộ khối trắng vuông. Đã thử cắt nền tự động: chỉ được với áo tối,
 *   áo trắng bị khoét thủng (xem deliverables/images/MOCKUP-PIPELINE.md).
 *
 *   Nên: vùng có sản phẩm giữ nền trắng, vùng kể chuyện đi nền tối + iridescent.
 *   Không cần ảnh nền trong suốt để chạy được ngay hôm nay.
 *
 * CHI PHÍ
 *   0 KB. Bốn radial-gradient, làm mờ, chạy bằng transform trên GPU.
 *   Bốn chu kỳ 17/23/31/41 giây là số nguyên tố không chia hết nhau → tổ hợp
 *   gần như không lặp, nên chuyển động trông "không có trật tự" như váng dầu
 *   mà không cần canvas hay WebGL.
 *   JS tạm dừng animation khi band cuộn ra khỏi màn hình.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

$vt_args = wp_parse_args(
    isset($args) && is_array($args) ? $args : array(),
    array(
        // Nguyên văn từ Instagram @vitalitevn, 29/07/2026. Copy thật của brand.
        'eyebrow' => '',
        'title'   => 'Finding harmony within chaos',
        'text'    => '',
        'cta_url' => '',
        'cta_label' => '',
    )
);
?>

<section class="vt-iri vt-section" data-vt-iri>
  <div class="vt-iri-layer" aria-hidden="true"></div>

  <div class="vt-wrap">
    <div class="vt-iri-content" style="max-width: 24ch;">
      <?php if ($vt_args['eyebrow']) : ?>
        <p class="vt-mono" style="color: var(--vt-on-dark-muted); margin: 0 0 14px;">
          <?php echo esc_html($vt_args['eyebrow']); ?>
        </p>
      <?php endif; ?>

      <h2 class="vt-display" style="color: var(--vt-on-dark); font-size: var(--vt-t-2xl);">
        <?php echo esc_html($vt_args['title']); ?>
      </h2>

      <?php if ($vt_args['text']) : ?>
        <p style="color: var(--vt-on-dark-muted); margin-top: 18px; max-width: 46ch;">
          <?php echo esc_html($vt_args['text']); ?>
        </p>
      <?php endif; ?>

      <?php if ($vt_args['cta_url'] && $vt_args['cta_label']) : ?>
        <p style="margin-top: 28px;">
          <a class="vt-btn vt-btn--on-dark" href="<?php echo esc_url($vt_args['cta_url']); ?>">
            <?php echo esc_html($vt_args['cta_label']); ?>
            <?php vt_icon('arrow'); ?>
          </a>
        </p>
      <?php endif; ?>
    </div>
  </div>
</section>
