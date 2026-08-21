<?php
/**
 * Bài viết đơn.
 *
 * VÌ SAO FILE NÀY TỒN TẠI DÙ SITE KHÔNG CÓ BLOG
 *   Thiếu `single.php` thì WordPress rơi xuống `index.php`. Mà `index.php` là
 *   template DANH SÁCH: nó in tiêu đề + trích đoạn. Mở một bài viết ra sẽ thấy
 *   đúng hai dòng và KHÔNG có nội dung bài — vì `the_content()` không được gọi
 *   ở đó bao giờ. Lỗi này chỉ lộ ra vào đúng ngày ai đó đăng bài đầu tiên.
 *
 *   File này là lưới an toàn, không phải lời mời làm blog.
 *
 * Sản phẩm KHÔNG đi qua đây — WooCommerce có `single-product.php` riêng,
 * và theme cố ý không đè file đó (xem HANDOFF mục "2 file Woo duy nhất bị đè").
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

get_header();

while (have_posts()) :
    the_post();
    ?>

    <article <?php post_class('vt-page'); ?>>

      <header class="vt-section vt-section--tight">
        <div class="vt-wrap vt-wrap-narrow">
          <p class="vt-eyebrow">
            <?php echo esc_html(get_the_date()); ?>
          </p>
          <h1 class="vt-title vt-title--sm"><?php the_title(); ?></h1>
        </div>
      </header>

      <?php if (has_post_thumbnail()) : ?>
        <?php
        /* Ảnh đại diện tràn sát mép — cùng ngôn ngữ với gallery và banner.
           Chữ thụt lề, hình thì không. */
        ?>
        <div class="vt-bleed">
          <?php the_post_thumbnail('full', array(
              'loading'  => 'eager',
              'decoding' => 'async',
              'style'    => 'width:100%;height:auto;display:block;',
          )); ?>
        </div>
      <?php endif; ?>

      <div class="vt-section">
        <div class="vt-wrap vt-wrap-narrow">
          <div class="vt-prose">
            <?php
            the_content();
            wp_link_pages(array(
                'before' => '<nav class="vt-page-links">',
                'after'  => '</nav>',
            ));
            ?>
          </div>
        </div>
      </div>

      <?php
      // Điều hướng bài trước / bài sau. Không có bài nào khác thì không in gì.
      $vt_prev = get_previous_post();
      $vt_next = get_next_post();
      if ($vt_prev || $vt_next) :
      ?>
        <nav class="vt-section vt-section--tight" aria-label="<?php esc_attr_e('Post navigation', 'vitalite'); ?>">
          <div class="vt-wrap vt-wrap-narrow vt-postnav">
            <?php if ($vt_prev) : ?>
              <a class="vt-link vt-mono" href="<?php echo esc_url(get_permalink($vt_prev)); ?>">
                ← <?php echo esc_html(get_the_title($vt_prev)); ?>
              </a>
            <?php endif; ?>
            <?php if ($vt_next) : ?>
              <a class="vt-link vt-mono" href="<?php echo esc_url(get_permalink($vt_next)); ?>">
                <?php echo esc_html(get_the_title($vt_next)); ?> →
              </a>
            <?php endif; ?>
          </div>
        </nav>
      <?php endif; ?>

    </article>

    <?php
endwhile;

get_footer();
