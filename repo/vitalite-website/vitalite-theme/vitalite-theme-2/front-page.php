<?php
/**
 * Trang chủ.
 *
 * NGÔN NGỮ LAYOUT — theo đúng prototype `Vitalite Homepage.dc.html`:
 *   · FULL-WIDTH. Không có khung 1440px ở giữa, chỉ có lề ~32px.
 *   · Chữ tiêu đề KHỔNG LỒ (clamp tới 84px, hero tới 152px), Archivo Expanded, in hoa.
 *   · Mỗi section có eyebrow ĐÁNH SỐ (`01 — FEATURED`) và một đường kẻ đen dưới tiêu đề.
 *     Đường kẻ đó giữ nhịp cho cả trang.
 *   · Lưới sản phẩm gap 2px trên nền màu đường kẻ → khe hở thành hairline, ô sát nhau.
 *   · Nút bo tròn hoàn toàn (pill).
 *
 * ⚠️ ĐIỂM LỆCH SO VỚI CLAUDE.md — cần user xác nhận lại.
 * CLAUDE.md ghi "Homepage: build bằng Elementor". Nhưng "Structure homepage"
 * nằm trong OPEN ITEMS và chưa bao giờ được chốt, còn user cần bản nền chạy được ngay.
 * ĐƯỜNG LUI VẪN MỞ: mỗi section là template part độc lập và đều có shortcode
 * ([vt_banner] [vt_products] [vt_collection] [vt_gallery] [vt_services]).
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

get_header();

/* ── Hero: 3 slide, cross-fade, thanh tiến trình ─────────── */
get_template_part('template-parts/hero');

/* ── 01 — Nổi bật ────────────────────────────────────────
   layout 'featured': ô đầu tiên chiếm 2×2, một sản phẩm được nâng lên
   làm trung tâm thay vì tám ô ngang hàng. */
get_template_part('template-parts/section-products', null, array(
    'number'  => '01',
    'kicker'  => __('Featured', 'vitalite'),
    'title'   => __('T-Shirts', 'vitalite'),
    'cat'     => 't-shirts',
    'count'   => 7,
    'layout'  => 'featured',
    'orderby' => 'date',
));

/* ── 02 — Bộ sưu tập ─────────────────────────────────────
   Khối chia đôi tràn viền, nền tối. Copy nguyên văn từ Instagram 25/07/2026.
   Không có mockup ở đây nên nền tối không vướng vấn đề mockup nền trắng. */
$vt_collection_img = '/assets/collection-01.webp';
get_template_part('template-parts/section-collection', null, array(
    'number'    => '02',
    'kicker'    => __('New Collection', 'vitalite'),
    'title'     => 'The<br>Moments',
    'text'      => __('Crafted with 500+ GSM premium cotton blend for a structured silhouette that holds its shape all day.', 'vitalite'),
    'image'     => file_exists(get_stylesheet_directory() . $vt_collection_img)
                    ? get_stylesheet_directory_uri() . $vt_collection_img : '',
    'alt'       => __('Model wearing VITALITÉ in Saigon', 'vitalite'),
    'cta_url'   => vt_cat_url('outerwear'),
    'cta_label' => __('Shop outerwear', 'vitalite'),
));

/* ── 03 — Gallery / Lookbook ─────────────────────────────
   Lưới mosaic ô to nhỏ. Ảnh đọc thẳng từ `assets/gallery/` —
   thả file vào là hiện, không phải thao tác trong wp-admin. */
get_template_part('template-parts/section-gallery', null, array(
    'number' => '03',
    'kicker' => __('Gallery', 'vitalite'),
    'title'  => __('On The Street', 'vitalite'),
    'aside'  => '#VITALITEDAILY',
    'limit'  => 8,
));

/* ── 04 — Iridescent ─────────────────────────────────────
   Nhịp nghỉ. Copy nguyên văn từ Instagram 29/07/2026. */
get_template_part('template-parts/section-iridescent', null, array(
    'eyebrow'   => 'Saigon',
    'title'     => 'Finding harmony within chaos',
    'cta_url'   => vt_shop_url(),
    'cta_label' => __('Shop All', 'vitalite'),
));

/* ── 05 — Áo khoác ───────────────────────────────────────
   Bắt lại người đã cuộn sâu. */
get_template_part('template-parts/section-products', null, array(
    'number'  => '04',
    'kicker'  => __('Outerwear', 'vitalite'),
    'title'   => __('Heavyweight', 'vitalite'),
    'cat'     => 'outerwear',
    'count'   => 4,
    'orderby' => 'date',
));

/* ── Dải đóng trang ──────────────────────────────────────
   CHỈ in những mục có fact thật. Không có "miễn phí vận chuyển"
   hay "đổi trả 30 ngày" — hai câu đó chưa có nguồn nào. */
get_template_part('template-parts/section-services');

get_footer();
