/**
 * VITALITÉ — JS của site
 *
 * Nguyên tắc:
 *   - Không phụ thuộc thư viện nào. Không jQuery.
 *   - Không dùng scroll listener. IntersectionObserver rẻ hơn hẳn:
 *     scroll listener chạy hàng chục lần mỗi giây, observer chỉ chạy khi vượt ngưỡng.
 *   - Mọi thứ tôn trọng prefers-reduced-motion.
 *   - Hỏng một phần thì phần còn lại vẫn chạy — mỗi khối tự lo lấy.
 *
 * Bốn việc:
 *   1. Header đổi chế độ khi rời hero, và đảo màu theo tone slide đang hiện
 *   2. Hero 3 slide — cross-fade, thanh tiến trình, video chỉ ở slide 1
 *   3. Menu mobile
 *   4. Tạm dừng animation iridescent khi cuộn ra khỏi màn hình
 */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;
  var heroApi = null;   // khối header bên dưới có tham chiếu tới, nên khai báo sớm

  /* ---------------------------------------------------------------
   * 1. Header xuyên thấu — trong suốt khi đè lên banner, đục khi rời banner
   *
   * KHÔNG còn dành riêng cho hero. Bất kỳ banner đầu trang nào cũng chạy:
   * hero trang chủ, banner váng dầu trang archive, và banner nào thêm sau này.
   * Điều kiện duy nhất: banner đặt `position: relative` và chứa một phần tử
   * `[data-vt-header-sentinel]` cao 1px dán ở đáy nó.
   *
   * TONE
   *   Banner tĩnh khai `data-tone="dark|light"` trên chính nó.
   *   Hero đổi tone theo từng slide nên nó tự lo, qua heroApi.applyTone().
   *
   * LƯỚI AN TOÀN
   *   PHP (`vt_top_banner_tone()`) đã bỏ khoảng đệm đầu trang vì tin là có banner.
   *   Nếu thực tế KHÔNG có sentinel nào — template lệch với helper — thì trả
   *   header về chế độ đục VÀ trả lại khoảng đệm, nếu không nội dung sẽ chui
   *   xuống dưới header. Thà thừa khoảng trắng còn hơn mất chữ.
   * ------------------------------------------------------------ */
  (function initHeader() {
    var header = document.getElementById('vt-header');
    if (!header) return;

    var sentinel = document.querySelector('[data-vt-header-sentinel]');

    if (!sentinel || !hasIO) {
      header.classList.remove('is-transparent', 'is-light-bg');
      // Trả lại khoảng đệm — xem khối "HEADER XUYÊN THẤU" trong style.css
      document.body.classList.remove('vt-banner-top');
      return;
    }

    // Lưới an toàn chiều ngược lại: CÓ banner thật mà PHP quên khai báo thì
    // khoảng đệm thừa sẽ đẩy banner xuống, chừa một vệt trắng trên đỉnh. Sửa luôn.
    document.body.classList.add('vt-banner-top');

    // Banner tĩnh: lấy tone một lần. Hero không dùng đường này — heroApi lo.
    var banner     = sentinel.parentElement;
    var staticTone = banner ? banner.getAttribute('data-tone') : null;

    new IntersectionObserver(function (entries) {
      var overBanner = entries[0].isIntersecting;
      header.classList.toggle('is-transparent', overBanner);

      if (!overBanner) {
        // Rời banner: header thành kính trắng nền trắng, tone sáng vô nghĩa
        header.classList.remove('is-light-bg');
      } else if (heroApi) {
        heroApi.applyTone();                       // hero: theo slide đang hiện
      } else {
        header.classList.toggle('is-light-bg', staticTone === 'light');
      }
    }, {
      // Ngưỡng lùi đúng bằng chiều cao header: đổi chế độ ngay khi đáy banner
      // chạm gáy header, chứ không phải sau đó.
      // offsetHeight đọc lúc khởi tạo → tự đúng cả 76px desktop lẫn 64px mobile.
      rootMargin: '-' + header.offsetHeight + 'px 0px 0px 0px',
      threshold: 0
    }).observe(sentinel);
  })();

  /* ---------------------------------------------------------------
   * 1b. Header trượt: kéo XUỐNG thì ẩn, kéo LÊN thì hiện lại
   *
   * VÌ SAO ĐÂY LÀ CHỖ DUY NHẤT TRONG THEME DÙNG SCROLL LISTENER
   *   IntersectionObserver không biết HƯỚNG cuộn — nó chỉ báo "vượt ngưỡng",
   *   không báo "đang đi lên hay đi xuống". Mà toàn bộ hành vi này là về hướng.
   *   Nên buộc phải nghe scroll. Đổi lại, làm cho nó rẻ nhất có thể:
   *     · listener `passive: true` → trình duyệt không phải chờ xem có
   *       preventDefault hay không, cuộn không bao giờ bị giật
   *     · gom vào requestAnimationFrame → tối đa 1 lần xử lý mỗi khung hình,
   *       dù trình duyệt bắn ra 60 sự kiện
   *     · chỉ đọc window.scrollY, KHÔNG đọc offsetHeight/getBoundingClientRect
   *       trong lúc cuộn → không ép trình duyệt tính lại layout
   *     · chỉ chạm classList khi trạng thái THẬT SỰ đổi
   *
   * BA LUẬT
   *   1. Trong vùng TỰ DO ở đỉnh trang thì luôn hiện — chưa cuộn thật thì đừng
   *      giấu thanh điều hướng đi.
   *   2. Phải vượt NGƯỠNG mới đổi. Không có ngưỡng thì cuộn nảy trên trackpad
   *      và đà trượt trên iOS sẽ làm header nhấp nháy.
   *   3. Menu mobile đang mở thì bất động — nút đóng nằm trong header.
   * ------------------------------------------------------------ */
  (function initHeaderSlide() {
    var header = document.getElementById('vt-header');
    if (!header) return;

    var FREE_ZONE = 120;   // px đầu trang: luôn hiện
    var THRESHOLD = 8;     // px phải đi được mới tính là đổi hướng

    var last    = window.scrollY || 0;
    var hidden  = false;
    var ticking = false;

    function update() {
      ticking = false;
      var y = window.scrollY || 0;

      // Menu mobile mở: bất động, và nhớ lại mốc để lúc đóng không nhảy
      if (header.classList.contains('is-menu-open')) { last = y; return; }

      // iOS cuộn quá đà cho scrollY âm — kẹp lại, nếu không hướng bị đọc sai
      if (y < 0) y = 0;

      var delta = y - last;
      if (Math.abs(delta) < THRESHOLD) return;   // chưa đủ, giữ nguyên trạng thái

      var next = (y > FREE_ZONE) && (delta > 0);
      if (next !== hidden) {
        hidden = next;
        header.classList.toggle('is-hidden', hidden);
      }
      last = y;
    }

    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }, { passive: true });

    // Nhảy tới #anchor bằng bàn phím hoặc link: hiện header lại ngay,
    // nếu không khách bấm "Skip to content" xong không thấy điều hướng đâu
    window.addEventListener('hashchange', function () {
      hidden = false;
      header.classList.remove('is-hidden');
    });

    // Cho khối menu mobile bên dưới bật/tắt được trạng thái bất động
    header.vtSlideLock = function (on) {
      header.classList.toggle('is-menu-open', !!on);
      if (on) { hidden = false; header.classList.remove('is-hidden'); }
    };
  })();

  /* ---------------------------------------------------------------
   * 2. Hero — 3 slide, cross-fade, thanh tiến trình
   *
   * Thanh tiến trình chạy bằng CSS animation chứ không phải setInterval vẽ lại:
   * animation chạy trên compositor, không đụng main thread.
   * JS chỉ làm ba việc: đổi slide, reset animation, đảo màu header theo tone.
   * ------------------------------------------------------------ */
  (function initHero() {
    var hero = document.querySelector('[data-vt-hero]');
    if (!hero) return;

    var slides = Array.prototype.slice.call(hero.querySelectorAll('.vt-slide'));
    var dots   = Array.prototype.slice.call(hero.querySelectorAll('.vt-hero-dot'));
    var header = document.getElementById('vt-header');
    if (!slides.length) return;

    var dur = parseInt(hero.getAttribute('data-duration'), 10) || 7000;
    hero.style.setProperty('--vt-hero-dur', dur + 'ms');

    var index = 0, timer = null, paused = false;

    function applyTone(i) {
      var light = slides[i].getAttribute('data-tone') === 'light';

      // Thanh điều hướng là ANH EM của slide, không nằm trong nó, nên nó không
      // tự thừa hưởng màu. Gắn tone lên chính .vt-hero để CSS đảo màu nav.
      // Thiếu dòng này thì trên slide 3 nền trắng nav trắng-trên-trắng, mất hút.
      hero.setAttribute('data-tone', light ? 'light' : 'dark');

      if (!header) return;
      // Chỉ đổi màu chữ header khi nó còn ĐANG TRONG SUỐT trên hero
      header.classList.toggle('is-light-bg', light && header.classList.contains('is-transparent'));
    }

    function show(i) {
      index = (i + slides.length) % slides.length;

      slides.forEach(function (sl, k) {
        var on = (k === index);
        sl.classList.toggle('is-active', on);
        if (on) { sl.removeAttribute('aria-hidden'); } else { sl.setAttribute('aria-hidden', 'true'); }
        // Link trong slide đang ẩn không được bắt bằng phím Tab
        var cta = sl.querySelector('.vt-slide-cta');
        if (cta) {
          if (on) { cta.removeAttribute('tabindex'); } else { cta.setAttribute('tabindex', '-1'); }
        }
      });

      dots.forEach(function (d, k) {
        d.classList.toggle('is-active', k === index);
        d.classList.toggle('is-done', k < index);
        d.setAttribute('aria-selected', k === index ? 'true' : 'false');
        if (k === index) {
          // Ép trình duyệt chạy lại animation thanh tiến trình từ đầu
          var bar = d.querySelector('.vt-hero-bar');
          if (bar) { bar.style.animation = 'none'; void bar.offsetWidth; bar.style.animation = ''; }
        }
      });

      applyTone(index);
      syncVideo();
      schedule();
    }

    function schedule() {
      window.clearTimeout(timer);
      if (paused || reduceMotion || slides.length < 2) return;
      timer = window.setTimeout(function () { show(index + 1); }, dur);
    }

    function pause() {
      paused = true;
      hero.classList.add('is-paused');
      window.clearTimeout(timer);
    }

    function resume() {
      if (!paused) return;
      paused = false;
      hero.classList.remove('is-paused');
      schedule();
    }

    dots.forEach(function (d) {
      d.addEventListener('click', function () {
        show(parseInt(d.getAttribute('data-vt-slide'), 10) || 0);
      });
    });

    // Dừng khi rê chuột hoặc focus vào — người đang đọc thì đừng cướp nội dung đi
    hero.addEventListener('mouseenter', pause);
    hero.addEventListener('mouseleave', resume);
    hero.addEventListener('focusin', pause);
    hero.addEventListener('focusout', resume);

    // Mũi tên trái/phải khi focus đang ở trong hero
    hero.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { show(index + 1); }
      else if (e.key === 'ArrowLeft') { show(index - 1); }
    });

    // Tab bị ẩn → dừng. Không đốt pin chạy thứ không ai xem.
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { window.clearTimeout(timer); } else { schedule(); }
    });

    // Cuộn khỏi hero → dừng
    if (hasIO) {
      new IntersectionObserver(function (e) {
        if (e[0].isIntersecting) { schedule(); } else { window.clearTimeout(timer); }
      }, { threshold: 0 }).observe(hero);
    }

    /* ---- Video: chỉ có ở slide 1 ---- */
    var video = document.getElementById('vt-hero-video');
    var videoLoaded = false;

    function videoAllowed() {
      if (!video || reduceMotion) return false;
      var conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (conn && conn.saveData) return false;
      if (conn && /^([23]g|slow-2g)$/.test(conn.effectiveType || '')) return false;
      // Người Việt xem điện thoại, 4G tính tiền. Ảnh poster đã đủ đẹp.
      if (window.matchMedia('(max-width: 768px)').matches) return false;
      return true;
    }

    function addSource(src, type) {
      var el = document.createElement('source');
      el.src = src;
      el.type = type;
      video.appendChild(el);
    }

    function loadVideo() {
      if (videoLoaded || !videoAllowed()) return;
      videoLoaded = true;
      var webm = video.getAttribute('data-src-webm');
      var mp4  = video.getAttribute('data-src-mp4');
      // WebM trước — nhẹ hơn ~30–40%; trình duyệt lấy định dạng đầu tiên nó hiểu
      if (webm) addSource(webm, 'video/webm');
      if (mp4)  addSource(mp4, 'video/mp4');
      if (!webm && !mp4) return;
      video.load();
      video.addEventListener('canplay', function () {
        var p = video.play();
        if (p && typeof p.then === 'function') {
          p.then(function () { video.classList.add('is-ready'); }, function () {});
        }
      }, { once: true });
    }

    function syncVideo() {
      if (!video) return;
      var slide = video.parentNode ? video.parentNode.parentNode : null;
      var visible = slide && slide.classList.contains('is-active');
      if (visible) {
        loadVideo();
        if (videoLoaded && video.paused && video.readyState > 2) {
          var p = video.play();
          if (p && typeof p.then === 'function') { p.then(null, function () {}); }
        }
      } else if (!video.paused) {
        video.pause();
      }
    }

    // Chờ trang tải xong hẳn rồi mới đụng tới video — nó không được tranh
    // băng thông với ảnh poster, thứ đang là phần tử LCP
    if (document.readyState === 'complete') {
      idle(syncVideo);
    } else {
      window.addEventListener('load', function () { idle(syncVideo); }, { once: true });
    }

    show(0);
    heroApi = { applyTone: function () { applyTone(index); } };
  })();

  /* ---------------------------------------------------------------
   * 3. Menu mobile
   * ------------------------------------------------------------ */
  (function initMobileNav() {
    var nav = document.getElementById('vt-mobile-nav');
    var openBtn = document.querySelector('[data-vt-menu-open]');
    var closeBtn = document.querySelector('[data-vt-menu-close]');
    if (!nav || !openBtn) return;

    var lastFocus = null;

    function onKey(e) {
      if (e.key === 'Escape') close();
    }

    function open() {
      lastFocus = document.activeElement;
      nav.hidden = false;
      void nav.offsetWidth;              // ép reflow để transition chạy
      nav.classList.add('is-open');
      openBtn.setAttribute('aria-expanded', 'true');
      document.documentElement.style.overflow = 'hidden';
      // Header phải đứng yên và hiện: nút đóng nằm trong nó
      var hdr = document.getElementById('vt-header');
      if (hdr && hdr.vtSlideLock) hdr.vtSlideLock(true);
      var first = nav.querySelector('a, button');
      if (first) first.focus();
      document.addEventListener('keydown', onKey);
    }

    function close() {
      nav.classList.remove('is-open');
      openBtn.setAttribute('aria-expanded', 'false');
      document.documentElement.style.overflow = '';
      var hdr = document.getElementById('vt-header');
      if (hdr && hdr.vtSlideLock) hdr.vtSlideLock(false);
      document.removeEventListener('keydown', onKey);
      if (lastFocus) lastFocus.focus();
      // Ẩn hẳn sau transition để không bắt được focus bằng Tab
      window.setTimeout(function () {
        if (!nav.classList.contains('is-open')) nav.hidden = true;
      }, reduceMotion ? 0 : 450);
    }

    openBtn.addEventListener('click', open);
    if (closeBtn) closeBtn.addEventListener('click', close);
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) close();
    });
  })();

  /* ---------------------------------------------------------------
   * 4. Iridescent — dừng animation khi ra khỏi màn hình
   *
   * Bốn lớp gradient bị làm mờ là thứ tốn fill-rate. Chạy chúng khi
   * không ai nhìn là đốt pin và làm nóng máy mà chẳng được gì.
   * ------------------------------------------------------------ */
  (function initIridescent() {
    var bands = document.querySelectorAll('[data-vt-iri]');
    if (!bands.length || !hasIO) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        e.target.classList.toggle('is-idle', !e.isIntersecting);
      });
    }, { rootMargin: '100px' });

    /*
     * 🔴 KHÔNG đặt `is-idle` làm mặc định.
     *
     * Bản cũ gắn `is-idle` ngay rồi chờ observer gỡ ra. Vấn đề: nếu callback của
     * IntersectionObserver không chạy — tab nền, trình duyệt tiết kiệm pin, một
     * script khác ném lỗi trước đó — thì lớp váng dầu ĐỨNG IM VĨNH VIỄN và không
     * có gì báo lỗi cả. Nó chỉ trông như một cái nền gradient chết.
     *
     * Mặc định là CHẠY. Observer chỉ có nhiệm vụ TẮT khi cuộn ra khỏi màn hình.
     * Hỏng observer thì hậu quả tệ nhất là animation chạy hơi thừa — chứ không
     * phải mất hẳn hiệu ứng.
     */
    Array.prototype.forEach.call(bands, function (b) {
      b.classList.remove('is-idle');
      io.observe(b);
    });
  })();

  /* ---------------------------------------------------------------
   * Tiện ích
   * ------------------------------------------------------------ */
  function idle(fn) {
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(fn, { timeout: 2000 });
    } else {
      window.setTimeout(fn, 200);
    }
  }
})();
