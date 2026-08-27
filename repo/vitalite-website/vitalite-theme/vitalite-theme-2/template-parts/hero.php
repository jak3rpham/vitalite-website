<?php
/**
 * HERO — 3 slide, cross-fade, thanh tiến trình điều hướng.
 *
 * TONE SÁNG / TỐI
 *   Slide 3 nền trắng. Chữ trắng đặt lên đó là mất hút, nên mỗi slide khai
 *   `data-tone` và JS đảo màu cả header lẫn thanh điều hướng theo.
 *
 * LCP — carousel above the fold vốn hại LCP. Cách giữ được:
 *   1. Chỉ ảnh SLIDE 1 là eager + fetchpriority=high + preload trong <head>.
 *      Hai slide sau `loading="lazy"`, không tranh băng thông ở giây đầu.
 *   2. Video chỉ có ở slide 1, `preload="none"`, source gắn bằng JS sau khi
 *      trang tải xong, và KHÔNG tải trên mobile / tiết kiệm dữ liệu.
 *   3. Slide 2, 3 chỉ là ảnh — ba video tự động chạy là không thể chấp nhận
 *      trên shared hosting.
 *
 * COPY — cả ba câu là NGUYÊN VĂN từ Instagram @vitalitevn, không tự nghĩ:
 *   slide 1  29/07/2026  'THE ICONIC'
 *   slide 2  25/07/2026  'THE MOMENTS' hoodie
 *   slide 3  20/07/2026  đóng khung dòng cũ là archive
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

$vt_uri = get_stylesheet_directory_uri();
$vt_dir = get_stylesheet_directory();

// Hai closure này KHÔNG đặt tiền tố vt_ để không lẫn với hàm thật của theme
$asset_exists = function ($rel) use ($vt_dir) { return file_exists($vt_dir . $rel); };
$asset_url    = function ($rel) use ($vt_uri) { return $vt_uri . $rel; };

/*
 * Video chỉ dùng bản đã nén. Bản master KHÔNG nằm trong theme và không bao giờ
 * phục vụ khách — nó ở `repo/vitalite-website/_not-in-theme/video-masters/`.
 *
 * `hero-1280` = master 29s / 2048×1080 / 63MB đã cắt còn 8s, bỏ audio,
 * hạ về 1280 và nén CRF 30. Lệnh đầy đủ: deliverables/video/encode.md
 *   MP4  2.4MB  — fallback, chạy mọi nơi
 *   WebM        — VP9, trình duyệt hiện đại lấy cái này trước
 *
 * Thiếu file nào thì biến tương ứng rỗng và <source> đó không được in ra.
 * Thiếu cả hai thì thẻ <video> biến mất hẳn, hero còn poster — không vỡ.
 */
$vt_mp4  = $asset_exists('/video/hero-1280.mp4')  ? $asset_url('/video/hero-1280.mp4')  : '';
$vt_webm = $asset_exists('/video/hero-1280.webm') ? $asset_url('/video/hero-1280.webm') : '';

$vt_slides = array(
    array(
        'tone'  => 'dark',
        'label' => 'The Iconic',
        'tag'   => __('The Iconic · T-Shirt', 'vitalite'),
        'title' => 'Even in chaos,<br>you are alive.',
        'sub'   => __('Two sides of the same street culture.', 'vitalite'),
        'cta'   => __('Shop All', 'vitalite'),
        'url'   => vt_shop_url(),
        'img'   => $asset_exists('/assets/hero-poster.webp') ? $asset_url('/assets/hero-poster.webp') : $asset_url('/assets/hero-poster.jpg'),
        'video' => true,
    ),
    array(
        'tone'  => 'dark',
        'label' => 'The Moments',
        'tag'   => __('The Moments · Boxy Hoodie', 'vitalite'),
        'title' => 'Heavy in weight.<br>Unmatched in fit.',
        'sub'   => __('500+ GSM heavyweight cotton blend. Signature boxy fit.', 'vitalite'),
        'cta'   => __('Outerwear', 'vitalite'),
        'url'   => vt_cat_url('outerwear'),
        'img'   => $asset_exists('/assets/cb-poster.webp') ? $asset_url('/assets/cb-poster.webp') : '',
        'video' => false,
    ),
    array(
        'tone'  => 'light',
        'label' => 'Archive',
        'tag'   => __('Archive', 'vitalite'),
        'title' => 'Old things<br>still shine.',
        'sub'   => __('Earlier drops, still in stock.', 'vitalite'),
        'cta'   => __('T-Shirts', 'vitalite'),
        'url'   => vt_cat_url('t-shirts'),
        'img'   => $asset_exists('/assets/slide-03.webp') ? $asset_url('/assets/slide-03.webp') : '',
        'video' => false,
    ),
);

// Slide thiếu ảnh thì bỏ hẳn — thà 2 slide đẹp còn hơn 3 slide có một ô đen
$vt_slides = array_values(array_filter($vt_slides, function ($s) { return !empty($s['img']); }));
if (empty($vt_slides)) return;
?>

<section class="vt-hero" id="vt-hero"
         data-vt-hero
         data-tone="<?php echo esc_attr($vt_slides[0]['tone']); ?>"
         data-duration="7000"
         aria-roledescription="carousel"
         aria-label="<?php esc_attr_e('Featured campaigns', 'vitalite'); ?>">

  <?php foreach ($vt_slides as $vt_i => $vt_s) : ?>
    <div class="vt-slide<?php echo esc_attr($vt_i === 0 ? ' is-active' : ''); ?>"
         data-tone="<?php echo esc_attr($vt_s['tone']); ?>"
         role="group"
         aria-roledescription="slide"
         aria-label="<?php echo esc_attr(sprintf('%d / %d — %s', $vt_i + 1, count($vt_slides), $vt_s['label'])); ?>"
         <?php if ($vt_i !== 0) { echo 'aria-hidden="true"'; } ?>>

      <div class="vt-slide-media">
        <img src="<?php echo esc_url($vt_s['img']); ?>"
             alt=""
             width="1920" height="1080"
             <?php if ($vt_i === 0) : ?>
               fetchpriority="high" loading="eager"
             <?php else : ?>
               loading="lazy"
             <?php endif; ?>
             decoding="async">

        <?php if (!empty($vt_s['video']) && ($vt_mp4 || $vt_webm)) : ?>
          <?php
          /* KHÔNG có `loop`. Clip phải KẾT THÚC thì sự kiện `ended` mới bắn,
             và đó là thứ chuyển sang slide 2 — xem initHero() trong site.js.
             Thêm `loop` lại là hero đứng im ở slide 1 vĩnh viễn. */
          ?>
          <video id="vt-hero-video" class="vt-slide-video"
                 muted playsinline preload="none" tabindex="-1" aria-hidden="true"
                 <?php if ($vt_webm) : ?>data-src-webm="<?php echo esc_url($vt_webm); ?>"<?php endif; ?>
                 <?php if ($vt_mp4) : ?>data-src-mp4="<?php echo esc_url($vt_mp4); ?>"<?php endif; ?>></video>
        <?php endif; ?>
      </div>

      <div class="vt-slide-scrim" aria-hidden="true"></div>

      <div class="vt-slide-content">
        <p class="vt-slide-tag"><?php echo esc_html($vt_s['tag']); ?></p>
        <?php
        // Chỉ cho phép <br> — chuỗi là hằng trong file này, không phải input người dùng
        printf(
            '<%1$s class="vt-slide-title">%2$s</%1$s>',
            $vt_i === 0 ? 'h1' : 'p',
            wp_kses($vt_s['title'], array('br' => array()))
        );
        ?>
        <div class="vt-slide-foot">
          <?php if ($vt_s['sub']) : ?>
            <p class="vt-slide-sub"><?php echo esc_html($vt_s['sub']); ?></p>
          <?php endif; ?>
          <a class="vt-btn vt-slide-cta" href="<?php echo esc_url($vt_s['url']); ?>"
             <?php if ($vt_i !== 0) { echo 'tabindex="-1"'; } ?>>
            <?php echo esc_html($vt_s['cta']); ?>
            <?php vt_icon('arrow'); ?>
          </a>
        </div>
      </div>
    </div>
  <?php endforeach; ?>

  <?php if (count($vt_slides) > 1) : ?>
    <div class="vt-hero-nav" role="tablist" aria-label="<?php esc_attr_e('Choose slide', 'vitalite'); ?>">
      <?php foreach ($vt_slides as $vt_i => $vt_s) : ?>
        <button type="button"
                class="vt-hero-dot<?php echo esc_attr($vt_i === 0 ? ' is-active' : ''); ?>"
                role="tab"
                data-vt-slide="<?php echo (int) $vt_i; ?>"
                aria-selected="<?php echo esc_attr($vt_i === 0 ? 'true' : 'false'); ?>">
          <span class="vt-hero-track"><span class="vt-hero-bar"></span></span>
          <span class="vt-hero-dot-label">
            <?php printf('%02d — %s', $vt_i + 1, esc_html($vt_s['label'])); ?>
          </span>
        </button>
      <?php endforeach; ?>
    </div>
  <?php endif; ?>

  <div class="vt-hero-sentinel" data-vt-hero-sentinel data-vt-header-sentinel aria-hidden="true"></div>
</section>
