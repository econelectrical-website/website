(function () {
  window.__econReady = true;
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = document.querySelector('.site-header');

  /* New pages always open at the top.
     Some viewers (and some phones) keep the previous page's scroll position when a link is followed,
     which made project pages open part way down. Links to a section (#...) and the back button are left alone. */
  var NAV_KEY = 'econ:nav';
  function session(fn) { try { return fn(window.sessionStorage); } catch (err) { return null; } }
  var navStamp = session(function (s) { var v = s.getItem(NAV_KEY); s.removeItem(NAV_KEY); return v; });
  var fromLink = !!navStamp && Date.now() - parseInt(navStamp, 10) < 15000;
  var navType = 'navigate';
  try { var navEntry = performance.getEntriesByType('navigation')[0]; if (navEntry && navEntry.type) navType = navEntry.type; } catch (err) {}
  var userScrolled = false;
  ['wheel', 'touchmove', 'keydown', 'mousedown'].forEach(function (t) {
    window.addEventListener(t, function () { userScrolled = true; }, { passive: true });
  });
  var marker = document.querySelector('.top-marker');
  function toTop() {
    if (userScrolled || location.hash) return;
    if (window.scrollY || window.scrollX) window.scrollTo(0, 0);
    // Also bring the top of the page into view when the site is shown inside another page
    if (fromLink && marker && marker.scrollIntoView) { try { marker.scrollIntoView({ block: 'nearest', inline: 'nearest' }); } catch (err) {} }
  }
  if (!location.hash && (fromLink || navType === 'navigate')) {
    toTop();
    window.addEventListener('load', function () { toTop(); setTimeout(toTop, 120); });
  }
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a || ev.defaultPrevented || ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
    if (a.target === '_blank' || a.hasAttribute('download')) return;
    var href = a.getAttribute('href') || '';
    if (/^(tel:|mailto:|https?:|\/\/)/i.test(href)) return;
    var url;
    try { url = new URL(a.href, location.href); } catch (err) { return; }
    var samePage = url.pathname === location.pathname && url.search === location.search;
    if (samePage && url.hash) {
      // A link to a section on this page: glide to it
      var target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      if (!target) return;
      ev.preventDefault();
      target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      try { history.pushState(null, '', url.hash); } catch (err) {}
      return;
    }
    if (!url.hash) session(function (s) { s.setItem(NAV_KEY, String(Date.now())); });
  });

  /* Header: solid once the page moves */
  function onScroll() {
    if (!header) return;
    header.classList.toggle('is-scrolled', window.scrollY > 30);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Mega menus: hover on desktop is CSS; clicks and keys open them everywhere */
  function closeMenus(except) {
    document.querySelectorAll('.nav-item.open').forEach(function (li) {
      if (li === except) return;
      li.classList.remove('open');
      var b = li.querySelector('.nav-link');
      if (b) b.setAttribute('aria-expanded', 'false');
    });
    if (header) header.classList.toggle('has-open', !!document.querySelector('.nav-item.open'));
  }
  document.querySelectorAll('.nav-item.has-mega > .nav-link').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentElement;
      var willOpen = !li.classList.contains('open');
      closeMenus(li);
      li.classList.toggle('open', willOpen);
      btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
      header.classList.toggle('has-open', willOpen);
    });
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.nav-item.has-mega')) closeMenus(); });

  /* Mobile menu */
  var toggle = document.querySelector('.menu-toggle');
  function setMenu(open) {
    header.classList.toggle('menu-open', open);
    document.body.classList.toggle('menu-locked', open);
    if (toggle) toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  if (toggle) toggle.addEventListener('click', function () { setMenu(!header.classList.contains('menu-open')); });
  document.querySelectorAll('.mobile-nav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    closeMenus();
    if (header && header.classList.contains('menu-open')) { setMenu(false); if (toggle) toggle.focus(); }
  });

  /* Scroll reveals */
  var revealEls = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
  document.querySelectorAll('[data-stagger]').forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) {
      revealEls.push(child);
      child.style.setProperty('--d', (Math.min(i, 6) * 0.09).toFixed(2) + 's');
    });
  });
  if (reduce || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* Statement: words light up as it scrolls through */
  var statements = document.querySelectorAll('.statement[data-highlight]');
  function paintStatements() {
    statements.forEach(function (st) {
      var words = st.querySelectorAll('.wd');
      var r = st.getBoundingClientRect();
      var vh = window.innerHeight;
      var p = (vh * 0.85 - r.top) / (vh * 0.5 + r.height * 0.6);
      p = Math.max(0, Math.min(1, p));
      var n = Math.round(p * words.length);
      words.forEach(function (w, i) { w.classList.toggle('on', i < n); });
    });
  }
  if (statements.length) {
    if (reduce) statements.forEach(function (st) { st.querySelectorAll('.wd').forEach(function (w) { w.classList.add('on'); }); });
    else { window.addEventListener('scroll', paintStatements, { passive: true }); window.addEventListener('resize', paintStatements); paintStatements(); }
  }

  /* Counters */
  var counters = document.querySelectorAll('[data-count]');
  function runCount(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    if (reduce) { el.textContent = target + suffix; return; }
    var start = null, dur = 1600;
    function step(t) {
      if (!start) start = t;
      var k = Math.min(1, (t - start) / dur);
      var eased = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (counters.length) {
    if (!('IntersectionObserver' in window)) counters.forEach(runCount);
    else {
      var co = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { runCount(en.target); co.unobserve(en.target); } });
      }, { threshold: 0.6 });
      counters.forEach(function (c) { co.observe(c); });
    }
  }

  /* Carousels */
  document.querySelectorAll('[data-carousel]').forEach(function (wrap) {
    var track = wrap.querySelector('.carousel-track');
    var prev = wrap.querySelector('[data-prev]');
    var next = wrap.querySelector('[data-next]');
    if (!track) return;
    function stepSize() {
      var first = track.children[0];
      if (!first) return track.clientWidth;
      var gap = parseFloat(getComputedStyle(track).columnGap) || 24;
      return first.getBoundingClientRect().width + gap;
    }
    function update() {
      var max = track.scrollWidth - track.clientWidth - 2;
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= max;
    }
    if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -stepSize(), behavior: reduce ? 'auto' : 'smooth' }); });
    if (next) next.addEventListener('click', function () { track.scrollBy({ left: stepSize(), behavior: reduce ? 'auto' : 'smooth' }); });
    track.addEventListener('scroll', function () { window.requestAnimationFrame(update); }, { passive: true });
    window.addEventListener('resize', update);
    update();
  });

  /* Hero video: honour reduced motion and offer a pause control */
  document.querySelectorAll('[data-video]').forEach(function (wrap) {
    var video = wrap.querySelector('video');
    var btn = wrap.querySelector('.video-toggle');
    if (!video) return;
    function label() {
      if (!btn) return;
      var paused = video.paused;
      btn.querySelector('.txt').textContent = paused ? 'Play' : 'Pause';
      btn.setAttribute('aria-label', paused ? 'Play background video' : 'Pause background video');
      btn.querySelector('.i-pause').style.display = paused ? 'none' : '';
      btn.querySelector('.i-play').style.display = paused ? '' : 'none';
    }
    if (reduce) { video.removeAttribute('autoplay'); video.pause(); }
    else { var p = video.play(); if (p && p.catch) p.catch(label); }
    video.addEventListener('play', label);
    video.addEventListener('pause', label);
    if (btn) btn.addEventListener('click', function () {
      if (video.paused) { var r = video.play(); if (r && r.catch) r.catch(function () {}); } else { video.pause(); }
    });
    label();
  });

  /* Gallery lightbox; without script the links open the full photo */
  var galleries = document.querySelectorAll('[data-gallery]');
  if (galleries.length && typeof HTMLDialogElement === 'function') {
    var dlg = document.createElement('dialog');
    dlg.className = 'lightbox';
    dlg.setAttribute('aria-label', 'Project photos');
    dlg.innerHTML = '<div class="lb-bar"><span class="lb-count"></span><div class="lb-nav">' +
      '<button class="round-btn" type="button" data-lb="prev" aria-label="Previous photo">' + arrowSvg(true) + '</button>' +
      '<button class="round-btn" type="button" data-lb="next" aria-label="Next photo">' + arrowSvg(false) + '</button>' +
      '<button class="round-btn" type="button" data-lb="close" aria-label="Close">' + closeSvg() + '</button></div></div>' +
      '<div class="lb-stage"><img alt=""></div><p class="lb-caption"></p>';
    document.body.appendChild(dlg);
    var img = dlg.querySelector('img'), cap = dlg.querySelector('.lb-caption'), count = dlg.querySelector('.lb-count');
    var items = [], index = 0;
    function show(i) {
      index = (i + items.length) % items.length;
      var a = items[index], thumb = a.querySelector('img');
      img.src = a.getAttribute('href');
      img.alt = thumb ? thumb.alt : '';
      cap.textContent = thumb ? thumb.alt : '';
      count.textContent = (index + 1) + ' of ' + items.length;
    }
    galleries.forEach(function (g) {
      var links = Array.prototype.slice.call(g.querySelectorAll('a'));
      links.forEach(function (a, i) {
        a.addEventListener('click', function (e) { e.preventDefault(); items = links; show(i); dlg.showModal(); });
      });
    });
    dlg.addEventListener('click', function (e) {
      var act = e.target.closest('[data-lb]');
      if (act) {
        var w = act.getAttribute('data-lb');
        if (w === 'prev') show(index - 1); else if (w === 'next') show(index + 1); else dlg.close();
        return;
      }
      if (e.target === dlg || e.target.classList.contains('lb-stage')) dlg.close();
    });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
  }
  function arrowSvg(left) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      (left ? '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>' : '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>') + '</svg>';
  }
  function closeSvg() {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';
  }

  /* Contact form on the preview: there is nowhere to send it yet */
  var form = document.querySelector('form[data-preview]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var status = form.querySelector('.form-status');
      status.hidden = false;
      status.textContent = 'This is the preview of the new site, so nothing was sent. Once the site is live, messages from this form go straight to ' + form.getAttribute('data-email') + '.';
    });
  }

  /* Blog topic filters; without script every article is listed */
  var blog = document.querySelector('[data-blog]');
  if (blog) {
    var filterBtns = Array.prototype.slice.call(blog.querySelectorAll('.filter'));
    var postCards = Array.prototype.slice.call(blog.querySelectorAll('.post-card'));
    var filterStatus = blog.querySelector('.filter-status');
    var applyFilter = function (cat) {
      var known = filterBtns.some(function (b) { return b.getAttribute('data-filter') === cat; });
      if (!known) cat = 'all';
      filterBtns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-filter') === cat ? 'true' : 'false'); });
      blog.classList.toggle('is-filtered', cat !== 'all');
      var shown = 0;
      postCards.forEach(function (c) {
        var show = cat === 'all' || c.getAttribute('data-cat') === cat;
        c.hidden = !show;
        if (show) { shown++; c.classList.add('is-in'); }
      });
      if (filterStatus) filterStatus.textContent = shown + (shown === 1 ? ' article' : ' articles') + ' shown';
      return cat;
    };
    filterBtns.forEach(function (b) {
      b.addEventListener('click', function () {
        var cat = applyFilter(b.getAttribute('data-filter'));
        try { history.replaceState(null, '', cat === 'all' ? location.pathname + location.search : '#' + cat); } catch (err) {}
      });
    });
    if (location.hash) applyFilter(decodeURIComponent(location.hash.slice(1)));
    window.addEventListener('hashchange', function () { applyFilter(decodeURIComponent(location.hash.slice(1)) || 'all'); });
  }

  /* Cookie choice. Google Analytics and the Google map only load once a visitor accepts. */
  var CONSENT_KEY = 'econ:consent';
  var consentMemory = null;
  function readConsent() { try { return window.localStorage.getItem(CONSENT_KEY) || consentMemory; } catch (err) { return consentMemory; } }
  function saveConsent(v) { consentMemory = v; try { window.localStorage.setItem(CONSENT_KEY, v); } catch (err) {} }
  function clearAnalyticsCookies() {
    document.cookie.split(';').forEach(function (c) {
      var name = c.split('=')[0].trim();
      if (name.indexOf('_ga') !== 0) return;
      var host = location.hostname.replace(/^www\./, '');
      ['', '; domain=' + host, '; domain=.' + host].forEach(function (d) { document.cookie = name + '=; Max-Age=0; path=/' + d; });
    });
  }
  function loadMap(box) {
    if (!box || box.querySelector('iframe')) return;
    var f = document.createElement('iframe');
    f.src = box.getAttribute('data-map-src');
    f.title = box.getAttribute('data-map-title') || 'Map';
    f.loading = 'lazy';
    f.referrerPolicy = 'no-referrer-when-downgrade';
    f.setAttribute('allowfullscreen', '');
    Array.prototype.forEach.call(box.children, function (el) { el.hidden = true; });
    box.appendChild(f);
  }
  function applyConsent() {
    if (readConsent() !== 'granted') return;
    if (typeof window.econAnalytics === 'function') window.econAnalytics();
    document.querySelectorAll('[data-map-src]').forEach(loadMap);
  }
  document.querySelectorAll('[data-map-load]').forEach(function (b) {
    b.addEventListener('click', function () { loadMap(b.closest('[data-map-src]')); });
  });
  var consentBar = null;
  function showConsent() {
    if (!consentBar) {
      var privacy = document.querySelector('[data-privacy-link]');
      consentBar = document.createElement('div');
      consentBar.className = 'consent';
      consentBar.setAttribute('role', 'region');
      consentBar.setAttribute('aria-label', 'Cookie choice');
      consentBar.innerHTML = '<p><strong>Cookies</strong>We use cookies for website analytics and to show Google Maps. You can accept or decline them.' +
        (privacy ? ' <a href="' + privacy.getAttribute('href') + '">Privacy notice</a>' : '') + '</p>' +
        '<div class="consent-actions"><button type="button" class="btn btn-primary plain" data-consent="granted">Accept</button>' +
        '<button type="button" class="btn btn-glass plain" data-consent="denied">Decline</button></div>';
      document.body.appendChild(consentBar);
      consentBar.addEventListener('click', function (e) {
        var choice = e.target.closest('[data-consent]');
        if (!choice) return;
        var v = choice.getAttribute('data-consent');
        saveConsent(v);
        if (v === 'denied') clearAnalyticsCookies();
        hideConsent();
        applyConsent();
      });
    }
    consentBar.hidden = false;
    root.classList.add('consent-open');
  }
  function hideConsent() { if (consentBar) consentBar.hidden = true; root.classList.remove('consent-open'); }
  document.querySelectorAll('[data-cookie-settings]').forEach(function (b) { b.addEventListener('click', showConsent); });
  if (readConsent()) applyConsent(); else showConsent();

  /* Home solar illustration: on phones it can be swiped sideways, starting centred on the house */
  document.querySelectorAll('[data-art-scroll]').forEach(function (box) {
    if (box.scrollWidth <= box.clientWidth + 2) return;
    box.scrollLeft = box.scrollWidth * 0.457 - box.clientWidth / 2;
    var hint = box.parentElement.querySelector('.swipe-hint');
    if (!hint) return;
    window.requestAnimationFrame(function () {
      box.addEventListener('scroll', function () { hint.classList.add('gone'); }, { passive: true, once: true });
    });
  });

  /* Reading progress on blog posts */
  var bar = document.querySelector('.progress');
  var article = document.querySelector('[data-article]');
  if (bar && article) {
    var paint = function () {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight * 0.6;
      var p = total > 0 ? Math.max(0, Math.min(1, -r.top / total)) : 0;
      bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    };
    window.addEventListener('scroll', paint, { passive: true });
    paint();
  }

  /* Copy link on blog posts */
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-copy');
      var txt = btn.querySelector('.txt');
      var done = function (msg) { txt.textContent = msg; setTimeout(function () { txt.textContent = 'Copy link'; }, 2500); };
      var fallback = function () {
        var f = document.createElement('input');
        f.value = url; f.setAttribute('readonly', ''); f.style.position = 'absolute'; f.style.left = '-9999px';
        document.body.appendChild(f); f.select();
        var ok = false; try { ok = document.execCommand('copy'); } catch (err) { ok = false; }
        document.body.removeChild(f);
        done(ok ? 'Link copied' : 'Copy failed');
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(function () { done('Link copied'); }, fallback);
      else fallback();
    });
  });
})();
