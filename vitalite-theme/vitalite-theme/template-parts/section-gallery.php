<?php
/**
 * GALLERY — lưới mosaic kiểu lookbook.
 *
 * Ô to nhỏ khác nhau (2×2, 1×2, 2×1, 1×1) để lưới có nhịp, không đều tăm tắp
 * như lưới sản phẩm. Đây là chỗ ảnh model phát huy tác dụng — khách thấy
 * dáng thật trên người thật, không phải mockup phẳng.
 *
 * ẢNH LẤY TỪ ĐÂU
 *   Đọc thẳng thư mục `assets/gallery/`, sắp theo tên file.
 *   Thả ảnh vào là hiện, không phải vào wp-admin làm gì cả.
 *   Quy ước tên: `01-…`, `02-…` — số ở đầu quyết định thứ tự và do đó quyết định
 *   ô nào to ô nào nhỏ (xem bảng VT_GALLERY_SPANS bên dưới).
 *
 *   Muốn quản lý bằng Media Library thay vì thư mục thì hook vào filter
 *   `vt_gallery_images` — trả về mảng ['url' => …, 'alt' => …, 'w' => …, 'h' => …].
 *
 * SỐ ẢNH BAO NHIÊU CŨNG CHẠY
 *   Mẫu span lặp lại theo chu kỳ 8. Có 3 ảnh cũng đẹp, có 20 ảnh cũng đẹp.
 *   `grid-auto-flow: dense` lấp nốt khoảng trống nên không bao giờ có lỗ hổng.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

$vt_args = wp_parse_args(
    isset($args) && is_array($args) ? $args : array(),
    array(
        'title'     => __('Lookbook', 'vitalite'),
        'number'    => '',
        'kicker'    => '',
        'eyebrow'   => '',
        'aside'     => '',      // chữ mono bên phải, ví dụ hashtag
        'limit'     => 8,
        'cta_url'   => '',
        'cta_label' => '',
    )
);

$vt_images = vt_gallery_images((int) $vt_args['limit']);
if (empty($vt_images)) return;   // không có ảnh thì section biến mất, không để khung vỡ

/*
 * Mẫu ô, lặp theo chu kỳ 8. Lưới 4 cột trên desktop.
 * Vị trí 1 và 8 là hai ô lớn — chúng neo mắt ở đầu và cuối khối.
 */
$vt_spans = array(
    'vt-g--2x2',   // 1  ảnh lớn nhất — model toàn thân
    'vt-g--1x1',   // 2  chi tiết
    'vt-g--1x2',   // 3  dọc — ảnh đường phố
    'vt-g--1x1',   // 4
    'vt-g--2x1',   // 5  ngang — ảnh nhóm
    'vt-g--1x1',   // 6
    'vt-g--1x1',   // 7
    'vt-g--4x1',   // 8  banner tràn ngang, đóng khối
);
?>

<?php /* Tiêu đề GIỮ lề (.vt-wrap) để thẳng hàng với các section khác,
         nhưng lưới ảnh TRÀN VIỀN (.vt-bleed) — ảnh lookbook có viền trắng
         hai bên là mất hết sức nặng thị giác. */ ?>
<section class="vt-section vt-gallery-section">
  <div class="vt-wrap">

    <div class="vt-section-head">
      <div>
        <?php
        $vt_eb = $vt_args['eyebrow'] ?: trim($vt_args['number'] . ' — ' . $vt_args['kicker'], ' —');
        if ($vt_eb) : ?>
          <p class="vt-eyebrow"><?php echo esc_html($vt_eb); ?></p>
        <?php endif; ?>
        <h2 class="vt-title"><?php echo esc_html($vt_args['title']); ?></h2>
      </div>
      <?php if ($vt_args['aside']) : ?>
        <span class="vt-mono" style="color: var(--vt-muted);"><?php echo esc_html($vt_args['aside']); ?></span>
      <?php elseif ($vt_args['cta_url'] && $vt_args['cta_label']) : ?>
        <a class="vt-link vt-mono" href="<?php echo esc_url($vt_args['cta_url']); ?>">
          <?php echo esc_html($vt_args['cta_label']); ?> →
        </a>
      <?php endif; ?>
    </div>
  </div>

  <div class="vt-bleed">
    <div class="vt-gallery">
      <?php foreach ($vt_images as $vt_i => $vt_img) :
          $vt_span = $vt_spans[$vt_i % count($vt_spans)];
      ?>
        <figure class="vt-g <?php echo esc_attr($vt_span); ?>">
          <img src="<?php echo esc_url($vt_img['url']); ?>"
               alt="<?php echo esc_attr($vt_img['alt']); ?>"
               <?php if (!empty($vt_img['w'])) : ?>width="<?php echo (int) $vt_img['w']; ?>"<?php endif; ?>
               <?php if (!empty($vt_img['h'])) : ?>height="<?php echo (int) $vt_img['h']; ?>"<?php endif; ?>
               loading="lazy" decoding="async">
        </figure>
      <?php endforeach; ?>
    </div>

  </div>
</section>
