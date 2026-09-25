<?php

if (!defined('ABSPATH')) exit; // Prevent direct access

$cart_count = (function_exists('WC') && WC()->cart) ? WC()->cart->get_cart_contents_count() : 0;
$cart_url   = function_exists('wc_get_cart_url') ? wc_get_cart_url() : '#';
$account_url = function_exists('wc_get_page_permalink') ? wc_get_page_permalink('myaccount') : '#';
$shop_url    = function_exists('wc_get_page_permalink') ? wc_get_page_permalink('shop') : '#';
$home_url    = esc_url(home_url('/'));
?>

<style>
  :root {
    --vt-header-h: 76px;
    --vt-dark-bg: rgba(10, 10, 10, 0.75);
    --vt-light-bg: rgba(244, 244, 244, 0.82);
    --vt-glass-border-dark: rgba(255, 255, 255, 0.12);
    --vt-glass-border-light: rgba(10, 10, 10, 0.08);
    --vt-glass-shine: inset 0 1px 1px 0 rgba(255, 255, 255, 0.2);
  }

  .vt-glass-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: var(--vt-header-h);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    font-family: 'Archivo', sans-serif;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    
    /* GLASS LIQUID CORE STYLES */
    background: var(--vt-dark-bg);
    color: #FFFFFF;
    border-bottom: 1px solid var(--vt-glass-border-dark);
    backdrop-filter: blur(20px) saturate(190%) contrast(90%);
    -webkit-backdrop-filter: blur(20px) saturate(190%) contrast(90%);
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), var(--vt-glass-shine);
  }

  /* Scrolled Light State */
  .vt-glass-header.vt-scrolled-light {
    background: var(--vt-light-bg);
    color: #0A0A0A;
    border-bottom: 1px solid var(--vt-glass-border-light);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06), inset 0 1px 0 0 rgba(255, 255, 255, 0.6);
  }

  .vt-header-left {
    display: flex;
    align-items: center;
    gap: 32px;
    flex: 1 1 auto;
    min-width: 0;
  }

  .vt-brand-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
    text-decoration: none;
    color: inherit;
  }

  /* CSS Mask cho Logo kế thừa currentColor của Header (White/Black) */
  .vt-mark {
    width: 19px;
    height: 24px;
    background: currentColor;
    -webkit-mask: url('<?php echo get_stylesheet_directory_uri(); ?>/assets/vitalite-mark-trim.png') center/contain no-repeat;
    mask: url('<?php echo get_stylesheet_directory_uri(); ?>/assets/vitalite-mark-trim.png') center/contain no-repeat;
  }

  .vt-wordmark {
    width: 112px;
    height: 22px;
    background: currentColor;
    -webkit-mask: url('<?php echo get_stylesheet_directory_uri(); ?>/assets/vitalite-wordmark-trim.png') left center/contain no-repeat;
    mask: url('<?php echo get_stylesheet_directory_uri(); ?>/assets/vitalite-wordmark-trim.png') left center/contain no-repeat;
  }

  .vt-nav {
    display: flex;
    align-items: center;
    gap: 26px;
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .vt-nav a, .vt-nav-link {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: inherit;
    text-decoration: none;
    position: relative;
    padding: 6px 0;
    transition: opacity 0.25s ease;
  }

  .vt-nav a::after, .vt-nav-link::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0%;
    height: 1.5px;
    background: currentColor;
    transition: width 0.3s ease;
  }

  .vt-nav a:hover::after, .vt-nav-link:hover::after {
    width: 100%;
  }

  .vt-header-right {
    display: flex;
    align-items: center;
    gap: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
  }

  .vt-lang-switch {
    opacity: 0.75;
    display: flex;
    gap: 6px;
  }

  .vt-cart-btn {
    border: 1px solid currentColor;
    padding: 6px 14px;
    border-radius: 999px;
    text-decoration: none;
    color: inherit;
    transition: background 0.3s, color 0.3s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .vt-cart-btn:hover {
    background: currentColor;
    color: #0A0A0A;
  }

  .vt-glass-header.vt-scrolled-light .vt-cart-btn:hover {
    color: #FFFFFF;
  }

  @media (max-width: 1024px) {
    .vt-nav, .vt-lang-switch { display: none; }
    .vt-glass-header { padding: 0 20px; height: 64px; }
  }
</style>

<header class="vt-glass-header" id="vtHeader">
  <div class="vt-header-left">
    <a href="<?php echo $home_url; ?>" class="vt-brand-logo" title="Vitalité Home">
      <div class="vt-mark"></div>
      <div class="vt-wordmark"></div>
    </a>

    <!-- WOOCOMMERCE / WORDPRESS DYNAMIC NAV MENU -->
    <nav>
      <?php
      if (has_nav_menu('primary')) {
        wp_nav_menu(array(
          'theme_location' => 'primary',
          'container'      => false,
          'menu_class'     => 'vt-nav',
          'depth'          => 1,
        ));
      } else {
      ?>
        <ul class="vt-nav">
          <li><a href="<?php echo $shop_url; ?>" class="vt-nav-link">Shop All</a></li>
          <li><a href="<?php echo esc_url(home_url('/new-arrivals')); ?>" class="vt-nav-link">New Arrivals</a></li>
          <li><a href="<?php echo esc_url(home_url('/product-category/ao')); ?>" class="vt-nav-link">Áo</a></li>
          <li><a href="<?php echo esc_url(home_url('/product-category/quan')); ?>" class="vt-nav-link">Quần</a></li>
          <li><a href="<?php echo esc_url(home_url('/collection')); ?>" class="vt-nav-link">Collection</a></li>
          <li><a href="<?php echo esc_url(home_url('/about')); ?>" class="vt-nav-link">About</a></li>
          <li><a href="<?php echo esc_url(home_url('/sale')); ?>" class="vt-nav-link">Sale</a></li>
        </ul>
      <?php } ?>
    </nav>
  </div>

  <div class="vt-header-right">
    <div class="vt-lang-switch">
      <span>VI</span>/<span>EN</span>
    </div>

    <!-- DYNAMIC SEARCH & ACCOUNT & WOOCOMMERCE CART -->
    <a href="#" onclick="event.preventDefault(); document.getElementById('vtSearchModal')?.classList.toggle('active');" style="color: inherit; text-decoration: none;">SEARCH</a>
    <a href="<?php echo esc_url($account_url); ?>" style="color: inherit; text-decoration: none;">ACCOUNT</a>
    
    <!-- Dynamic Cart Button with AJAX Class for WooCommerce Auto Update -->
    <a href="<?php echo esc_url($cart_url); ?>" class="vt-cart-btn vt-woocommerce-cart-link">
      CART (<span class="vt-cart-count"><?php echo esc_html($cart_count); ?></span>)
    </a>
  </div>
</header>

<script>
  (function() {
    const header = document.getElementById('vtHeader');
    if (!header) return;
    
    function updateHeaderGlass() {
      if (window.scrollY > 500) {
        header.classList.add('vt-scrolled-light');
      } else {
        header.classList.remove('vt-scrolled-light');
      }
    }

    window.addEventListener('scroll', updateHeaderGlass, { passive: true });
    updateHeaderGlass();
  })();
</script>

<?php
/**
 * WOOCOMMERCE AJAX CART FRAGMENT UPDATER
 * Giúp số lượng trên nút CART (X) tự động cập nhật khi khách bấm "Thêm vào giỏ" mà không cần reload trang!
 */
add_filter('woocommerce_add_to_cart_fragments', function($fragments) {
    ob_start();
    $count = WC()->cart ? WC()->cart->get_cart_contents_count() : 0;
    ?>
    <span class="vt-cart-count"><?php echo esc_html($count); ?></span>
    <?php
    $fragments['span.vt-cart-count'] = ob_get_clean();
    return $fragments;
});
?>
