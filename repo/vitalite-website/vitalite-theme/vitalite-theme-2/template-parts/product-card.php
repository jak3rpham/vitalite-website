<?php
/**
 * Thẻ sản phẩm — dùng chung cho trang chủ, shop archive, kết quả tìm kiếm.
 *
 * Một file duy nhất. Sửa thẻ sản phẩm ở đây là sửa mọi nơi.
 *
 * ẢNH HOVER ĐỔI MẶT TRƯỚC ↔ MẶT SAU
 *   Quy ước nhập hàng: Product image = MẶT TRƯỚC, Gallery ảnh ĐẦU TIÊN = MẶT SAU.
 *   Không có ảnh gallery → không hover, không lỗi.
 *   Trên thiết bị cảm ứng ảnh mặt sau bị CSS ẩn hẳn (@media hover:none) và
 *   thẻ <img> dùng loading="lazy" nên không tốn băng thông vô ích.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

// WooCommerce tắt (khi debug, hoặc trước khi cài) thì im lặng bỏ qua,
// không để trắng site vì gọi hàm không tồn tại.
if (!function_exists('wc_get_product') || !class_exists('WC_Product')) return;

global $product;
if (!$product instanceof WC_Product) {
    $product = wc_get_product(get_the_ID());
}
if (!$product) return;

$vt_id    = $product->get_id();
$vt_link  = get_permalink($vt_id);
$vt_front = get_the_post_thumbnail_url($vt_id, 'vt-card');
if (!$vt_front && function_exists('wc_placeholder_img_src')) {
    $vt_front = wc_placeholder_img_src('vt-card');
}
$vt_back  = vt_product_back_image($product, 'vt-card');

/*
 * Màu + ảnh mặt trước của từng màu, để rê vào chấm màu là ảnh trên thẻ đổi theo.
 * Sản phẩm đơn (không biến thể) thì trả mảng rỗng → rơi về bản chỉ đọc pa_color,
 * chấm màu vẫn vẽ nhưng không bấm được. Không có màu nào → không vẽ gì.
 */
$vt_colors = vt_product_color_variants($product, 'vt-card');
if (empty($vt_colors)) {
    $vt_colors = vt_product_color_swatches($product);
}

// Có ít nhất một màu kèm ảnh thì mới đáng gắn JS.
$vt_has_color_img = false;
foreach ($vt_colors as $vt_c) {
    if (!empty($vt_c['img'])) { $vt_has_color_img = true; break; }
}
?>

<article <?php wc_product_class('vt-card', $product); ?>>

  <?php
  /*
   * .vt-card-media LÀ <div>, KHÔNG phải <a>.
   * Lý do: bên trong nó có các link chọn nhanh size. <a> lồng trong <a> là HTML
   * không hợp lệ — trình duyệt tự đóng thẻ ngoài và ĐẨY các <a> con ra ngoài,
   * chúng rơi khỏi .vt-card-media nên mất sạch CSS: S/M/L xếp dọc, có gạch chân.
   * Link phủ ảnh nằm riêng ở .vt-card-media-link.
   */
  ?>
  <div class="vt-card-media">
    <a class="vt-card-media-link" href="<?php echo esc_url($vt_link); ?>" tabindex="-1" aria-hidden="true"></a>

    <?php if (!$product->is_in_stock()) : ?>
      <span class="vt-card-badge vt-card-badge--out"><?php esc_html_e('Sold out', 'vitalite'); ?></span>
    <?php elseif ($product->is_on_sale()) : ?>
      <span class="vt-card-badge vt-card-badge--sale"><?php esc_html_e('Sale', 'vitalite'); ?></span>
    <?php elseif (vt_product_is_new($vt_id)) : ?>
      <span class="vt-card-badge"><?php esc_html_e('New', 'vitalite'); ?></span>
    <?php endif; ?>

    <?php if ($vt_front) : ?>
      <img class="vt-card-front"
           src="<?php echo esc_url($vt_front); ?>"
           alt=""
           width="600" height="600"
           loading="lazy" decoding="async">
    <?php endif; ?>

    <?php if ($vt_back) : ?>
      <img class="vt-card-back"
           src="<?php echo esc_url($vt_back); ?>"
           alt=""
           width="600" height="600"
           loading="lazy" decoding="async">
    <?php endif; ?>
    <?php
    /*
     * Nút chọn nhanh size — hiện khi rê chuột.
     * KHÔNG phải nút thêm giỏ hàng: nó dẫn tới PDP với size chọn sẵn.
     * Thêm thẳng vào giỏ từ lưới sẽ bỏ qua bước xem bảng số đo,
     * mà chọn sai size là nguyên nhân trả hàng số một trong thời trang online.
     */
    $vt_sizes = array();
    if ($product->is_type('variable')) {
        $vt_attr = $product->get_variation_attributes();
        if (!empty($vt_attr['pa_size'])) {
            $vt_sizes = array_slice($vt_attr['pa_size'], 0, 4);
        }
    }
    if (!empty($vt_sizes)) : ?>
      <span class="vt-card-quick">
        <?php foreach ($vt_sizes as $vt_sz) : ?>
          <a href="<?php echo esc_url(add_query_arg('attribute_pa_size', rawurlencode($vt_sz), $vt_link)); ?>">
            <?php echo esc_html(strtoupper($vt_sz)); ?>
          </a>
        <?php endforeach; ?>
      </span>
    <?php endif; ?>
  </div>

  <div class="vt-card-body">
    <h3 class="vt-card-title">
      <a href="<?php echo esc_url($vt_link); ?>"><?php echo esc_html($product->get_name()); ?></a>
    </h3>

    <div class="vt-card-price">
      <?php
      // get_price_html() trả về markup <del>/<ins> của Woo — đã an toàn, không escape lại
      echo wp_kses_post($product->get_price_html());
      ?>
    </div>

    <?php if (!empty($vt_colors)) : ?>
      <?php
      /*
       * Chấm màu.
       *
       * Có ảnh theo màu  → <button>, rê/bấm là ảnh trên thẻ đổi. JS đọc data-vt-img.
       * Không có ảnh     → <span> trơ như cũ. Không dựng nút bấm mà bấm không ra gì —
       *                    đó là lừa người dùng, và hỏng cả bàn phím lẫn trình đọc màn hình.
       *
       * Ảnh mặt sau (hover) là ảnh cấp SẢN PHẨM, không có bản theo màu. Nên khi
       * đang xem màu khác, CSS tắt luôn hiệu ứng hover — thà không đổi còn hơn
       * đổi sang mặt sau của màu khác.
       */
      ?>
      <?php $vt_sw_class = $vt_has_color_img ? 'vt-card-swatches is-interactive' : 'vt-card-swatches'; ?>
      <div class="<?php echo esc_attr($vt_sw_class); ?>"
           aria-label="<?php esc_attr_e('Available colours', 'vitalite'); ?>">
        <?php foreach ($vt_colors as $vt_c) : ?>
          <?php if ($vt_has_color_img && !empty($vt_c['img'])) : ?>
            <button type="button" class="vt-card-swatch"
                    style="background: <?php echo esc_attr($vt_c['hex']); ?>"
                    data-vt-img="<?php echo esc_url($vt_c['img']); ?>"
                    title="<?php echo esc_attr($vt_c['name']); ?>">
              <span class="screen-reader-text"><?php echo esc_html($vt_c['name']); ?></span>
            </button>
          <?php else : ?>
            <span class="vt-card-swatch"
                  style="background: <?php echo esc_attr($vt_c['hex']); ?>"
                  title="<?php echo esc_attr($vt_c['name']); ?>"></span>
          <?php endif; ?>
        <?php endforeach; ?>
      </div>
    <?php endif; ?>
  </div>
</article>
