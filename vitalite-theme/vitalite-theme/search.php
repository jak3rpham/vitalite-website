<?php
/**
 * Kết quả tìm kiếm.
 *
 * Tìm sản phẩm → hiện lưới thẻ sản phẩm giống trang shop.
 * Tìm nội dung khác → hiện danh sách chữ.
 *
 * Nút SEARCH trên header trỏ thẳng vào đây với post_type=product.
 * (Bản cũ trỏ vào #vtSearchModal — một element không tồn tại trong bất kỳ file nào,
 * nên nút đó là click chết trên production. Đã thay.)
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

get_header();

$vt_is_product_search = isset($_GET['post_type']) && $_GET['post_type'] === 'product';
$vt_term  = get_search_query();
$vt_found = isset($GLOBALS['wp_query']) ? (int) $GLOBALS['wp_query']->found_posts : 0;

/*
 * Banner váng dầu — cùng loại với trang shop/category.
 * Trang kết quả tìm kiếm cũng là một dạng archive: cùng nhiệm vụ "bạn đang ở đâu,
 * có bao nhiêu kết quả". Để nó khác kiểu là khách tưởng mình rời khỏi shop.
 *
 * ⚠️ Thêm banner ở đây thì PHẢI khai báo trong vt_top_banner_tone() (inc/helpers.php),
 * nếu không header sẽ đục trong khi banner tối nằm ngay dưới.
 */
get_template_part('template-parts/section-page-banner', null, array(
    'eyebrow' => __('Search', 'vitalite'),
    'title'   => $vt_term
        /* translators: %s: search term */
        ? sprintf(__('Results for “%s”', 'vitalite'), $vt_term)
        : __('Search', 'vitalite'),
    'meta'    => $vt_found
        ? sprintf(
            /* translators: %s: số kết quả */
            _n('%s result', '%s results', $vt_found, 'vitalite'),
            number_format_i18n($vt_found)
          )
        : __('No results', 'vitalite'),
    'tag'     => 'h1',
));
?>

<section class="vt-section">
  <div class="vt-wrap">

    <div class="vt-section-head">
      <div>
        <p class="vt-eyebrow"><?php esc_html_e('Refine', 'vitalite'); ?></p>
      </div>
      <?php get_search_form(); ?>
    </div>

    <?php if (have_posts()) : ?>

      <?php if ($vt_is_product_search) : ?>

        <div class="vt-grid">
          <?php
          while (have_posts()) {
              the_post();
              get_template_part('template-parts/product-card');
          }
          ?>
        </div>

      <?php else : ?>

        <div class="vt-result-list vt-wrap-narrow" style="padding: 0;">
          <?php while (have_posts()) : the_post(); ?>
            <article <?php post_class('vt-result'); ?>>
              <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
              <p><?php echo esc_html(get_the_excerpt()); ?></p>
            </article>
          <?php endwhile; ?>
        </div>

      <?php endif; ?>

      <?php
      the_posts_pagination(array(
          'mid_size'  => 1,
          'prev_text' => '←',
          'next_text' => '→',
      ));
      ?>

    <?php else : ?>

      <div class="vt-empty">
        <p><?php esc_html_e('No results', 'vitalite'); ?></p>
        <a class="vt-btn vt-btn--ghost" href="<?php echo esc_url(vt_shop_url()); ?>">
          <?php esc_html_e('Shop All', 'vitalite'); ?>
          <?php vt_icon('arrow'); ?>
        </a>
      </div>

    <?php endif; ?>

  </div>
</section>

<?php
get_footer();
