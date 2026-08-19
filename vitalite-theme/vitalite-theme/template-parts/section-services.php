<?php
/**
 * SERVICES — dải 3 cột đóng trang.
 *
 * ⚠️ CHỈ IN RA NHỮNG MỤC CÓ FACT THẬT.
 * Đây đúng là chỗ site thương mại điện tử hay bịa nhất:
 * "Miễn phí vận chuyển", "Đổi trả 30 ngày", "Bảo hành trọn đời" —
 * viết cho đẹp rồi không ai kiểm.
 *
 * Mỗi mục dưới đây phải có nguồn. Chưa có thì để mảng rỗng và section biến mất.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

$vt_items = array();

/*
 * ✅ ĐÃ XÁC MINH — Shopee khai xuất xứ Việt Nam trong thuộc tính sản phẩm,
 * và user xác nhận trực tiếp 2026-08-19.
 */
$vt_items[] = array(
    'title' => __('Made in Vietnam', 'vitalite'),
    'text'  => __('Cut and printed in Saigon.', 'vitalite'),
);

/*
 * ✅ ĐÃ XÁC MINH — nguyên văn chính sách VITALITÉ đăng trên Shopee,
 * user xác nhận giữ nguyên. Chỉ in khi trang Returns đã tồn tại,
 * để câu này luôn có chỗ dẫn tới chi tiết đầy đủ.
 */
if (vt_page_url('returns')) {
    $vt_items[] = array(
        'title' => __('Exchanges', 'vitalite'),
        'text'  => __('One exchange per order, within 5 days of delivery.', 'vitalite'),
        'url'   => vt_page_url('returns'),
    );
}

/*
 * ✅ ĐÃ XÁC MINH — bio Instagram ghi "Worldwide shipping".
 * 🔴 NHƯNG phí, hãng và thời gian thì CHƯA CÓ SỐ LIỆU NÀO.
 * Nên chỉ nêu sự thật "có ship quốc tế", tuyệt đối không hứa gì về giá hay tốc độ.
 * Có trang Shipping rồi thì dẫn sang đó.
 */
$vt_items[] = array(
    'title' => __('Worldwide shipping', 'vitalite'),
    'text'  => __('We ship internationally from Saigon.', 'vitalite'),
    'url'   => vt_page_url('shipping') ?: '',
);

if (empty($vt_items)) return;
?>

<section class="vt-section vt-section--tight">
  <div class="vt-wrap">
    <div class="vt-services">
      <?php foreach ($vt_items as $vt_it) : ?>
        <div>
          <p class="vt-services-title"><?php echo esc_html($vt_it['title']); ?></p>
          <p>
            <?php echo esc_html($vt_it['text']); ?>
            <?php if (!empty($vt_it['url'])) : ?>
              <br><a class="vt-link" href="<?php echo esc_url($vt_it['url']); ?>"><?php esc_html_e('Read more', 'vitalite'); ?> →</a>
            <?php endif; ?>
          </p>
        </div>
      <?php endforeach; ?>
    </div>
  </div>
</section>
