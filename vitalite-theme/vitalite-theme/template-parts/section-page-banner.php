<?php
/**
 * BANNER ĐẦU TRANG — nền tối + váng dầu iridescent, tràn hai mép.
 *
 * DÙNG Ở ĐÂU
 *   Đầu trang shop archive và trang category (`woocommerce/archive-product.php`).
 *   Đây là thứ thay cho ảnh campaign: category chưa có ảnh riêng nào, mà để
 *   một khối xám trống thì tệ hơn hẳn. Váng dầu lấp chỗ đó bằng 0 KB.
 *
 * VÌ SAO KHÔNG DÙNG ẢNH
 *   Mỗi category một ảnh banner = 3–6 ảnh phải chụp và cắt đúng tỷ lệ.
 *   Năng lực chụp là nút thắt thật của brand. Banner này chạy được HÔM NAY,
 *   và thay bằng ảnh sau chỉ là truyền thêm 'image' vào $args.
 *
 * CHI PHÍ LCP
 *   0 KB. Không ảnh, không font mới, không JS mới. Bốn radial-gradient làm mờ,
 *   chạy bằng transform trên GPU. Class `vt-iri` + `data-vt-iri` nối thẳng vào
 *   observer sẵn có trong site.js — cuộn ra khỏi màn hình là animation dừng.
 *
 *   ⚠️ Banner này Ở TRÊN CÙNG trang archive, nên nó rất dễ trở thành phần tử LCP.
 *   Nó là text + gradient nên LCP vẫn rẻ — nhưng ĐỪNG thêm ảnh nền vào đây
 *   mà không preload, nếu không LCP của toàn bộ trang category sẽ tụt.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

$vt_args = wp_parse_args(
    isset($args) && is_array($args) ? $args : array(),
    array(
        'eyebrow' => '',      // chữ mono nhỏ phía trên, ví dụ 'Shop — T-Shirts'
        'title'   => '',      // bắt buộc
        'lede'    => '',      // mô tả category — đã là HTML, KHÔNG escape lại
        'meta'    => '',      // chữ mono góc phải, ví dụ '12 sản phẩm'
        'tag'     => 'h1',    // h1 trên trang archive; đổi thành h2 nếu nhúng giữa trang
    )
);

if (!$vt_args['title']) return;

$vt_tag = in_array($vt_args['tag'], array('h1', 'h2'), true) ? $vt_args['tag'] : 'h1';
?>

<?php
/*
 * data-tone="dark" — header đọc chuỗi này để biết phải đổi chữ sang trắng hay đen
 * khi nó đang đè lên banner. Váng dầu luôn chạy trên nền `--vt-ink`, nên tối.
 * Đổi nền banner sang sáng thì PHẢI đổi luôn chuỗi này.
 */
?>
<section class="vt-iri vt-pagebanner" data-vt-iri data-tone="dark">
  <div class="vt-iri-layer" aria-hidden="true"></div>

  <div class="vt-wrap vt-pagebanner-inner">
    <div class="vt-pagebanner-text">
      <?php if ($vt_args['eyebrow']) : ?>
        <p class="vt-pagebanner-eyebrow"><?php echo esc_html($vt_args['eyebrow']); ?></p>
      <?php endif; ?>

      <?php printf(
          '<%1$s class="vt-pagebanner-title">%2$s</%1$s>',
          $vt_tag,
          esc_html($vt_args['title'])
      ); ?>

      <?php if ($vt_args['lede']) : ?>
        <div class="vt-pagebanner-lede"><?php echo wp_kses_post($vt_args['lede']); ?></div>
      <?php endif; ?>
    </div>

    <?php if ($vt_args['meta']) : ?>
      <p class="vt-pagebanner-meta"><?php echo esc_html($vt_args['meta']); ?></p>
    <?php endif; ?>
  </div>

  <?php /* 1px vô hình ở đáy banner — mốc để JS bật/tắt chế độ trong suốt của header */ ?>
  <div class="vt-banner-sentinel" data-vt-header-sentinel aria-hidden="true"></div>
</section>
