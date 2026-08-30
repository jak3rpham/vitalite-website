<?php
/**
 * VITALITÉ — Bảng quản lý nội dung trang chủ
 *
 * Giao diện: Appearance → Vitalité
 *
 * VÌ SAO CÓ FILE NÀY
 *     Trước đây gallery đọc thẳng thư mục `assets/gallery/` và hero khai cứng
 *     trong `template-parts/hero.php`. Đổi một tấm ảnh nghĩa là sửa file trong
 *     theme, nén lại, upload lại cả theme. Đó là vòng lặp sai.
 *
 *     Luật ở đây: **theme giữ BỐ CỤC, admin giữ NỘI DUNG.** Lưới, khoảng cách,
 *     kiểu chữ nằm trong CSS. Ảnh, chữ, thứ tự, link nằm trong wp-admin.
 *
 * KHÔNG PHẢI PAGE BUILDER
 *     Bảng này cố tình KHÔNG cho đổi bố cục. Không thêm section, không đổi lưới,
 *     không chèn HTML tự do. Cho đổi bố cục trong admin là đúng một tháng sau
 *     trang chủ không còn giống thiết kế nữa. Quyết định "Con đường A" trong
 *     CLAUDE.md vẫn nguyên: bố cục là code.
 *
 * ĐA NGÔN NGỮ
 *     Polylang chốt TẮT dịch media (CLAUDE.md mục 5), nên **ảnh dùng chung**
 *     cho mọi ngôn ngữ — không phải upload hai lần. Chỉ CHỮ mới có ô riêng
 *     cho từng ngôn ngữ. Chưa bật Polylang thì chỉ hiện một cột.
 *
 * @package VitaliteTheme
 */

if (!defined('ABSPATH')) exit;

const VT_OPT = 'vt_home';

/* -------------------------------------------------------------------------
 * 1. Ngôn ngữ
 * ---------------------------------------------------------------------- */

/**
 * Danh sách mã ngôn ngữ đang bật.
 *
 * Đọc từ Polylang nếu có. Chưa cài / chưa bật thì trả về một phần tử `en`,
 * khớp với quyết định "EN mặc định tại root" ở CLAUDE.md mục 5.
 *
 * @return string[]
 */
function vt_langs() {
    if (function_exists('pll_languages_list')) {
        $list = pll_languages_list(array('fields' => 'slug'));
        if (is_array($list) && $list) {
            return array_map('sanitize_key', $list);
        }
    }
    return array('en');
}

/**
 * Mã ngôn ngữ đang hiển thị ở frontend.
 *
 * @return string
 */
function vt_lang() {
    if (function_exists('pll_current_language')) {
        $cur = pll_current_language('slug');
        if ($cur) {
            return sanitize_key($cur);
        }
    }
    $langs = vt_langs();
    return $langs[0];
}

/**
 * Lấy một chuỗi đa ngôn ngữ, có đường lùi.
 *
 * Thứ tự thử: ngôn ngữ hiện tại → ngôn ngữ đầu tiên → chuỗi rỗng.
 * Đường lùi này quan trọng: dịch VI là bước 12 trong thứ tự thực thi, nên sẽ
 * có một quãng dài site chạy EN mà chưa có chữ VI. Không có đường lùi thì
 * trang VI hiện ra trống trơn.
 *
 * @param array  $bag Mảng dạng ['en' => '...', 'vi' => '...'].
 * @param string $key Khoá con, để rỗng nếu $bag đã là mảng chuỗi theo ngôn ngữ.
 * @return string
 */
function vt_i18n($bag, $key = '') {
    if (!is_array($bag)) {
        return '';
    }
    $langs = vt_langs();
    $order = array_unique(array_merge(array(vt_lang()), $langs));

    foreach ($order as $lang) {
        if (!isset($bag[$lang])) {
            continue;
        }
        $val = $bag[$lang];
        if ($key !== '') {
            $val = isset($val[$key]) ? $val[$key] : '';
        }
        if (is_string($val) && $val !== '') {
            return $val;
        }
    }
    return '';
}

/* -------------------------------------------------------------------------
 * 2. Đọc / ghi option
 * ---------------------------------------------------------------------- */

/**
 * Toàn bộ nội dung đã cấu hình.
 *
 * @return array
 */
function vt_home_opt() {
    $opt = get_option(VT_OPT, array());
    if (!is_array($opt)) {
        $opt = array();
    }
    $opt += array('gallery' => array(), 'hero' => array());
    if (!is_array($opt['gallery'])) {
        $opt['gallery'] = array();
    }
    if (!is_array($opt['hero'])) {
        $opt['hero'] = array();
    }
    return $opt;
}

/**
 * Ba cỡ ô hợp lệ trong lưới gallery.
 *
 * Đây là những cỡ CSS thật sự có luật. Cho nhập cỡ tự do là mở đường cho một
 * lưới vỡ mà không ai kiểm được.
 *
 * @return array
 */
function vt_gallery_sizes() {
    return array(
        '1x1' => __('Normal — 1 cell', 'vitalite'),
        '1x2' => __('Tall — 1 wide, 2 high', 'vitalite'),
        '2x1' => __('Wide — 2 wide, 1 high', 'vitalite'),
        '2x2' => __('Large — 2 by 2', 'vitalite'),
        '4x1' => __('Full row — 4 wide', 'vitalite'),
    );
}

/**
 * Làm sạch dữ liệu trước khi lưu.
 *
 * Mọi giá trị đi qua đây. Không tin gì từ $_POST, kể cả khi người gửi là admin —
 * một bảng option hỏng làm trắng trang chủ, và trên shared hosting không SSH
 * thì sửa lại rất phiền.
 *
 * @param mixed $raw
 * @return array
 */
function vt_home_sanitize($raw) {
    $langs = vt_langs();
    $sizes = array_keys(vt_gallery_sizes());
    $out   = array('gallery' => array(), 'hero' => array());

    if (!is_array($raw)) {
        return $out;
    }

    // ---- Gallery ----
    if (!empty($raw['gallery']) && is_array($raw['gallery'])) {
        foreach ($raw['gallery'] as $row) {
            if (empty($row['id'])) {
                continue;
            }
            $id = absint($row['id']);
            if (!$id || get_post_type($id) !== 'attachment') {
                continue;
            }
            $size = isset($row['size']) ? sanitize_key($row['size']) : '1x1';
            if (!in_array($size, $sizes, true)) {
                $size = '1x1';
            }
            $alt = array();
            foreach ($langs as $lang) {
                $alt[$lang] = isset($row['alt'][$lang])
                    ? sanitize_text_field($row['alt'][$lang])
                    : '';
            }
            $out['gallery'][] = array('id' => $id, 'size' => $size, 'alt' => $alt);
        }
    }

    // ---- Hero ----
    if (!empty($raw['hero']) && is_array($raw['hero'])) {
        $i = 0;
        foreach ($raw['hero'] as $row) {
            if ($i >= 3) {
                break;   // ba slide là quyết định đã chốt, không mở rộng ở đây
            }
            $id = isset($row['id']) ? absint($row['id']) : 0;
            if ($id && get_post_type($id) !== 'attachment') {
                $id = 0;
            }
            $tone = (isset($row['tone']) && $row['tone'] === 'light') ? 'light' : 'dark';

            $text = array();
            foreach ($langs as $lang) {
                $text[$lang] = array(
                    'tag'   => isset($row['text'][$lang]['tag'])   ? sanitize_text_field($row['text'][$lang]['tag'])   : '',
                    // `title` cho phép <br> để ngắt dòng đúng chỗ trong thiết kế.
                    // wp_kses giới hạn đúng một thẻ đó, không mở cửa cho gì khác.
                    'title' => isset($row['text'][$lang]['title']) ? wp_kses($row['text'][$lang]['title'], array('br' => array())) : '',
                    'sub'   => isset($row['text'][$lang]['sub'])   ? sanitize_text_field($row['text'][$lang]['sub'])   : '',
                    'cta'   => isset($row['text'][$lang]['cta'])   ? sanitize_text_field($row['text'][$lang]['cta'])   : '',
                );
            }

            $out['hero'][] = array(
                'id'    => $id,
                'tone'  => $tone,
                'url'   => isset($row['url']) ? esc_url_raw($row['url']) : '',
                'label' => isset($row['label']) ? sanitize_text_field($row['label']) : '',
                'text'  => $text,
            );
            $i++;
        }
    }

    // Nội dung đổi thì cache gallery phải bỏ, nếu không sửa xong không thấy gì.
    delete_transient('vt_gallery');

    return $out;
}

/* -------------------------------------------------------------------------
 * 3. Trang admin
 * ---------------------------------------------------------------------- */

add_action('admin_menu', function () {
    add_theme_page(
        __('Vitalité — Home content', 'vitalite'),
        __('Vitalité', 'vitalite'),
        'edit_theme_options',
        'vt-home',
        'vt_home_page_render'
    );
});

add_action('admin_init', function () {
    register_setting('vt_home_group', VT_OPT, array(
        'type'              => 'array',
        'sanitize_callback' => 'vt_home_sanitize',
        'default'           => array(),
    ));
});

/**
 * Nạp media picker + sortable, CHỈ trên trang này.
 *
 * `wp_enqueue_media()` kéo theo khá nhiều script. Nạp nó trên mọi màn hình
 * admin là làm chậm toàn bộ khu quản trị vì một trang.
 */
add_action('admin_enqueue_scripts', function ($hook) {
    if ($hook !== 'appearance_page_vt-home') {
        return;
    }
    wp_enqueue_media();
    wp_enqueue_script(
        'vt-admin-options',
        VT_URI . '/assets/js/admin-options.js',
        array('jquery', 'jquery-ui-sortable'),
        VT_VERSION,
        true
    );
    wp_localize_script('vt-admin-options', 'VT_ADMIN', array(
        'pickTitle'  => __('Choose images', 'vitalite'),
        'pickButton' => __('Use these', 'vitalite'),
        'pickOne'    => __('Choose an image', 'vitalite'),
        'useOne'     => __('Use this image', 'vitalite'),
        'remove'     => __('Remove', 'vitalite'),
        'confirmDel' => __('Remove this image from the gallery?', 'vitalite'),
        'sizes'      => vt_gallery_sizes(),
        'langs'      => vt_langs(),
        'optName'    => VT_OPT,
    ));
    wp_add_inline_style('wp-admin', vt_admin_css());
});

/**
 * CSS của trang admin. Nhỏ nên để inline, không đáng một request riêng.
 *
 * @return string
 */
function vt_admin_css() {
    return '
    .vt-adm{max-width:1080px}
    .vt-adm h2{margin-top:34px}
    .vt-adm .vt-hint{color:#646970;max-width:70ch;line-height:1.6}
    .vt-adm .vt-warn{border-left:3px solid #d63638;background:#fcf0f1;padding:10px 14px;margin:14px 0;max-width:70ch}
    .vt-gal{display:flex;flex-wrap:wrap;gap:12px;margin:16px 0;padding:0;list-style:none}
    .vt-gal li{width:190px;border:1px solid #dcdcde;background:#fff;padding:8px;position:relative}
    .vt-gal li.ui-sortable-helper{box-shadow:0 6px 18px rgba(0,0,0,.18)}
    .vt-gal .vt-ph{width:100%;height:130px;object-fit:cover;display:block;background:#f0f0f1;cursor:move}
    .vt-gal label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#646970;margin:8px 0 2px}
    .vt-gal select,.vt-gal input[type=text]{width:100%}
    .vt-gal .vt-del{position:absolute;top:10px;right:10px;background:#111;color:#fff;border:0;
      width:24px;height:24px;border-radius:999px;cursor:pointer;line-height:1;font-size:14px}
    .vt-slide{border:1px solid #dcdcde;background:#fff;padding:16px;margin:14px 0;display:grid;
      grid-template-columns:230px 1fr;gap:20px}
    .vt-slide .vt-thumb{width:100%;height:150px;object-fit:cover;background:#f0f0f1;display:block;margin-bottom:8px}
    .vt-slide .vt-f{margin-bottom:10px}
    .vt-slide .vt-f label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#646970;margin-bottom:2px}
    .vt-slide input[type=text],.vt-slide input[type=url]{width:100%}
    .vt-langtabs{display:flex;gap:6px;margin:0 0 10px}
    .vt-langtabs button{background:#f0f0f1;border:1px solid #dcdcde;padding:4px 12px;cursor:pointer;
      text-transform:uppercase;font-size:11px;letter-spacing:.08em}
    .vt-langtabs button.is-on{background:#111;color:#fff;border-color:#111}
    .vt-langpane[hidden]{display:none}
    @media(max-width:782px){.vt-slide{grid-template-columns:1fr}}
    ';
}

/**
 * In ra trang admin.
 */
function vt_home_page_render() {
    if (!current_user_can('edit_theme_options')) {
        return;
    }
    $opt   = vt_home_opt();
    $langs = vt_langs();
    $sizes = vt_gallery_sizes();
    $n     = VT_OPT;
    ?>
    <div class="wrap vt-adm">
      <h1><?php esc_html_e('Vitalité — Home content', 'vitalite'); ?></h1>
      <p class="vt-hint">
        <?php esc_html_e('This page controls the pictures and words on the home page. It does not control layout — grid, spacing and type live in the theme, on purpose.', 'vitalite'); ?>
      </p>

      <?php if (count($langs) > 1) : ?>
        <p class="vt-hint">
          <?php esc_html_e('Images are shared across languages. Only text has a box per language.', 'vitalite'); ?>
        </p>
      <?php endif; ?>

      <form method="post" action="options.php">
        <?php settings_fields('vt_home_group'); ?>

        <h2><?php esc_html_e('Gallery', 'vitalite'); ?></h2>
        <p class="vt-hint">
          <?php esc_html_e('Drag a picture to reorder. The first eight are the ones that show.', 'vitalite'); ?>
        </p>

        <?php if (empty($opt['gallery'])) : ?>
          <div class="vt-warn">
            <strong><?php esc_html_e('Nothing chosen yet.', 'vitalite'); ?></strong><br>
            <?php esc_html_e('Until you add pictures here, the home page falls back to the eight images shipped inside the theme. Those get overwritten every time the theme is re-uploaded, which is exactly what this page exists to stop.', 'vitalite'); ?>
          </div>
        <?php endif; ?>

        <ul class="vt-gal" id="vt-gal"
            data-name="<?php echo esc_attr($n); ?>"
            data-langs="<?php echo esc_attr(implode(',', $langs)); ?>">
          <?php foreach ($opt['gallery'] as $i => $row) :
              $src = wp_get_attachment_image_url((int) $row['id'], 'medium');
              if (!$src) { continue; }
              ?>
            <li data-i="<?php echo esc_attr($i); ?>">
              <input type="hidden" name="<?php echo esc_attr($n); ?>[gallery][<?php echo esc_attr($i); ?>][id]"
                     value="<?php echo esc_attr($row['id']); ?>">
              <button type="button" class="vt-del" aria-label="<?php esc_attr_e('Remove', 'vitalite'); ?>">&times;</button>
              <img class="vt-ph" src="<?php echo esc_url($src); ?>" alt="">
              <label><?php esc_html_e('Cell size', 'vitalite'); ?></label>
              <select name="<?php echo esc_attr($n); ?>[gallery][<?php echo esc_attr($i); ?>][size]">
                <?php foreach ($sizes as $key => $lbl) : ?>
                  <option value="<?php echo esc_attr($key); ?>" <?php selected($row['size'], $key); ?>>
                    <?php echo esc_html($lbl); ?>
                  </option>
                <?php endforeach; ?>
              </select>
              <?php foreach ($langs as $lang) : ?>
                <label><?php echo esc_html(sprintf(__('Alt text (%s)', 'vitalite'), strtoupper($lang))); ?></label>
                <input type="text"
                       name="<?php echo esc_attr($n); ?>[gallery][<?php echo esc_attr($i); ?>][alt][<?php echo esc_attr($lang); ?>]"
                       value="<?php echo esc_attr(isset($row['alt'][$lang]) ? $row['alt'][$lang] : ''); ?>">
              <?php endforeach; ?>
            </li>
          <?php endforeach; ?>
        </ul>

        <p>
          <button type="button" class="button button-secondary" id="vt-gal-add">
            <?php esc_html_e('Add pictures', 'vitalite'); ?>
          </button>
        </p>
        <p class="vt-hint">
          <?php esc_html_e('Leave alt text empty for pictures that are decoration only. An empty alt is the correct answer for a screen reader, not a missing one.', 'vitalite'); ?>
        </p>

        <h2><?php esc_html_e('Hero slides', 'vitalite'); ?></h2>
        <p class="vt-hint">
          <?php esc_html_e('Three slides, cross-fading. Slide 1 also carries the video — that part stays in the theme because it has to not load on mobile.', 'vitalite'); ?>
        </p>

        <?php
        for ($i = 0; $i < 3; $i++) :
            $row  = isset($opt['hero'][$i]) ? $opt['hero'][$i] : array();
            $id   = isset($row['id']) ? (int) $row['id'] : 0;
            $src  = $id ? wp_get_attachment_image_url($id, 'medium') : '';
            $tone = isset($row['tone']) ? $row['tone'] : 'dark';
            ?>
          <div class="vt-slide">
            <div>
              <img class="vt-thumb vt-hero-thumb" src="<?php echo esc_url($src); ?>" alt="">
              <input type="hidden" class="vt-hero-id"
                     name="<?php echo esc_attr($n); ?>[hero][<?php echo esc_attr($i); ?>][id]"
                     value="<?php echo esc_attr($id); ?>">
              <button type="button" class="button vt-hero-pick" style="width:100%">
                <?php esc_html_e('Choose image', 'vitalite'); ?>
              </button>
              <div class="vt-f" style="margin-top:10px">
                <label><?php esc_html_e('Tone', 'vitalite'); ?></label>
                <select name="<?php echo esc_attr($n); ?>[hero][<?php echo esc_attr($i); ?>][tone]">
                  <option value="dark" <?php selected($tone, 'dark'); ?>><?php esc_html_e('Dark picture — white text', 'vitalite'); ?></option>
                  <option value="light" <?php selected($tone, 'light'); ?>><?php esc_html_e('Light picture — black text', 'vitalite'); ?></option>
                </select>
              </div>
            </div>

            <div>
              <h3 style="margin:0 0 10px"><?php echo esc_html(sprintf(__('Slide %d', 'vitalite'), $i + 1)); ?></h3>

              <div class="vt-f">
                <label><?php esc_html_e('Internal name — not shown to customers', 'vitalite'); ?></label>
                <input type="text" name="<?php echo esc_attr($n); ?>[hero][<?php echo esc_attr($i); ?>][label]"
                       value="<?php echo esc_attr(isset($row['label']) ? $row['label'] : ''); ?>">
              </div>
              <div class="vt-f">
                <label><?php esc_html_e('Button link', 'vitalite'); ?></label>
                <input type="url" name="<?php echo esc_attr($n); ?>[hero][<?php echo esc_attr($i); ?>][url]"
                       value="<?php echo esc_attr(isset($row['url']) ? $row['url'] : ''); ?>"
                       placeholder="https://vitalite.io.vn/shop">
              </div>

              <?php if (count($langs) > 1) : ?>
                <div class="vt-langtabs" data-target="vt-hero-<?php echo esc_attr($i); ?>">
                  <?php foreach ($langs as $k => $lang) :
                      // Không viết ternary trong echo — cùng luật với inc/woocommerce.php:
                      // mắt người và script quét đều phải thấy ngay là không có biến ngoài nào lọt vào.
                      $vt_on = '';
                      if ($k === 0) {
                          $vt_on = 'is-on';
                      }
                      ?>
                    <button type="button" class="<?php echo esc_attr($vt_on); ?>"
                            data-lang="<?php echo esc_attr($lang); ?>"><?php echo esc_html(strtoupper($lang)); ?></button>
                  <?php endforeach; ?>
                </div>
              <?php endif; ?>

              <?php foreach ($langs as $k => $lang) :
                  $t = isset($row['text'][$lang]) ? $row['text'][$lang] : array();
                  ?>
                <?php
                $vt_hidden = 'hidden';
                if ($k === 0) {
                    $vt_hidden = '';
                }
                ?>
                <div class="vt-langpane" data-group="vt-hero-<?php echo esc_attr($i); ?>"
                     data-lang="<?php echo esc_attr($lang); ?>" <?php echo esc_attr($vt_hidden); ?>>
                  <?php
                  $fields = array(
                      'tag'   => __('Eyebrow — small line above', 'vitalite'),
                      'title' => __('Headline — use <br> to break the line', 'vitalite'),
                      'sub'   => __('Sub-line', 'vitalite'),
                      'cta'   => __('Button label', 'vitalite'),
                  );
                  foreach ($fields as $fk => $flabel) : ?>
                    <div class="vt-f">
                      <label><?php echo esc_html($flabel); ?></label>
                      <input type="text"
                             name="<?php echo esc_attr($n); ?>[hero][<?php echo esc_attr($i); ?>][text][<?php echo esc_attr($lang); ?>][<?php echo esc_attr($fk); ?>]"
                             value="<?php echo esc_attr(isset($t[$fk]) ? $t[$fk] : ''); ?>">
                    </div>
                  <?php endforeach; ?>
                </div>
              <?php endforeach; ?>
            </div>
          </div>
        <?php endfor; ?>

        <p class="vt-hint">
          <?php esc_html_e('A slide with no picture is skipped. Two good slides beat three with a black gap.', 'vitalite'); ?>
        </p>

        <?php submit_button(); ?>
      </form>
    </div>
    <?php
}
