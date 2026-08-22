<?php
/**
 * Template dự phòng.
 *
 * WordPress bắt buộc theme phải có file này. Site không có blog, nên đây
 * chỉ là lưới an toàn cho archive nào không khớp template nào khác.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

get_header();
?>

<section class="vt-section">
  <div class="vt-wrap vt-wrap-narrow">

    <?php if (have_posts()) : ?>

      <h1 class="vt-title" style="margin-bottom: 32px;">
        <?php
        if (is_archive())      the_archive_title();
        elseif (is_home())     esc_html_e('Journal', 'vitalite');
        else                   esc_html_e('Latest', 'vitalite');
        ?>
      </h1>

      <div class="vt-result-list">
        <?php while (have_posts()) : the_post(); ?>
          <article <?php post_class('vt-result'); ?>>
            <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
            <p><?php echo esc_html(get_the_excerpt()); ?></p>
          </article>
        <?php endwhile; ?>
      </div>

      <?php
      the_posts_pagination(array(
          'mid_size'  => 1,
          'prev_text' => '←',
          'next_text' => '→',
      ));
      ?>

    <?php else : ?>
      <p><?php esc_html_e('Nothing here yet.', 'vitalite'); ?></p>
    <?php endif; ?>

  </div>
</section>

<?php
get_footer();
