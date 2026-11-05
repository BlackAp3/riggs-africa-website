(function () {
  var root = document.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(id) { return document.getElementById(id); }
  function store(get, key, val) {
    try { if (get) return sessionStorage.getItem(key); sessionStorage.setItem(key, val); } catch (e) { return null; }
  }

  /* Header shadow */
  var header = $('header');
  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Mobile menu */
  var nav = $('nav'), menuBtn = $('menuBtn');
  function setMenu(open) {
    nav.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  menuBtn.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); setMega(false); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 1024) setMenu(false); });

  /* Services mega menu */
  var megaBtn = $('megaBtn'), mega = $('megaPanel');
  function setMega(open) { mega.hidden = !open; megaBtn.setAttribute('aria-expanded', String(open)); }
  megaBtn.addEventListener('click', function (e) { e.stopPropagation(); setMega(mega.hidden); setMenu(false); });
  mega.addEventListener('click', function (e) { if (e.target.closest('a')) setMega(false); });
  document.addEventListener('click', function (e) { if (!mega.hidden && !e.target.closest('.mega')) setMega(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (!mega.hidden) { setMega(false); megaBtn.focus(); }
    if (nav.classList.contains('open')) { setMenu(false); menuBtn.focus(); }
  });

  /* Banner carousel */
  var track = $('banTrack'), pipsBox = $('banPips');
  var cards = Array.prototype.slice.call(track.children);
  cards.forEach(function () { pipsBox.appendChild(document.createElement('span')); });
  var pips = Array.prototype.slice.call(pipsBox.children);
  function step() { return cards[0].getBoundingClientRect().width + 20; }
  function current() {
    var mid = track.scrollLeft + track.clientWidth / 2, best = 0, dist = Infinity;
    cards.forEach(function (c, i) { var d = Math.abs(c.offsetLeft + c.offsetWidth / 2 - mid); if (d < dist) { dist = d; best = i; } });
    return best;
  }
  function paint() { var i = current(); pips.forEach(function (p, k) { p.classList.toggle('on', k === i); }); }
  function go(dir) {
    var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    var atStart = track.scrollLeft <= 4;
    if (dir > 0 && atEnd) track.scrollTo({ left: 0 });
    else if (dir < 0 && atStart) track.scrollTo({ left: track.scrollWidth });
    else track.scrollBy({ left: dir * step() });
  }
  $('banPrev').addEventListener('click', function () { go(-1); });
  $('banNext').addEventListener('click', function () { go(1); });
  track.addEventListener('scroll', function () { window.requestAnimationFrame(paint); }, { passive: true });
  paint();
  if (!reduce) {
    var paused = false;
    var box = track.parentNode;
    box.addEventListener('mouseenter', function () { paused = true; });
    box.addEventListener('mouseleave', function () { paused = false; });
    track.addEventListener('focusin', function () { paused = true; });
    track.addEventListener('focusout', function () { paused = false; });
    track.addEventListener('touchstart', function () { paused = true; }, { passive: true });
    setInterval(function () { if (!paused && !document.hidden) go(1); }, 5000);
  }

  /* Testimonials (placeholders until real, approved quotes arrive) */
  var ts = [
    { org: '[Client organisation]', quote: '[Client testimonial — what Riggs Africa delivered, in one or two sentences.]', name: '[Client name], [Title]' },
    { org: '[Training participant]', quote: '[Participant feedback on a Riggs Africa programme.]', name: '[Name], [Organisation]' },
    { org: '[Board member]', quote: '[Feedback from a board or audit committee workshop.]', name: '[Name], [Role]' }
  ];
  var ti = 0, tBody = document.querySelector('.testi-body'), tPips = $('tPips');
  ts.forEach(function () { tPips.appendChild(document.createElement('span')); });
  function showT(i) {
    ti = (i + ts.length) % ts.length;
    tBody.classList.add('fade');
    setTimeout(function () {
      $('tOrg').textContent = ts[ti].org; $('tQuote').textContent = ts[ti].quote; $('tName').textContent = ts[ti].name;
      tBody.classList.remove('fade');
    }, reduce ? 0 : 250);
    Array.prototype.forEach.call(tPips.children, function (p, k) { p.classList.toggle('on', k === ti); });
  }
  $('tPrev').addEventListener('click', function () { showT(ti - 1); });
  $('tNext').addEventListener('click', function () { showT(ti + 1); });
  showT(0);

  /* Reveal on scroll + stagger grids */
  document.querySelectorAll('.tr-grid, .ways, .ind-grid, .fw-track').forEach(function (g) {
    g.classList.add('stagger');
    Array.prototype.forEach.call(g.children, function (el, i) { el.style.setProperty('--d', (i * 0.05) + 's'); });
  });
  var watch = document.querySelectorAll('.reveal, .stagger');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target; el.classList.add('in'); io.unobserve(el);
        if (el.classList.contains('stagger')) setTimeout(function () { el.classList.add('done'); }, 1400);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    watch.forEach(function (el) { io.observe(el); });

    /* Count-up */
    var counter = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        counter.unobserve(en.target);
        var el = en.target, end = +el.getAttribute('data-count'), suf = el.getAttribute('data-suffix') || '', t0 = null;
        requestAnimationFrame(function stepC(now) {
          if (!t0) t0 = now;
          var p = Math.min((now - t0) / 1300, 1);
          el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + (p === 1 ? suf : '');
          if (p < 1) requestAnimationFrame(stepC);
        });
      });
    }, { threshold: 0.6 });
    document.querySelectorAll('[data-count]').forEach(function (el) { el.textContent = '0'; counter.observe(el); });

    /* Active nav link */
    var links = Array.prototype.slice.call(nav.querySelectorAll('a:not(.btn)'));
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ['trending', 'ways', 'industries', 'contact'].forEach(function (id) { var s = $(id); if (s) spy.observe(s); });
  } else {
    watch.forEach(function (el) { el.classList.add('in', 'done'); });
  }

  /* Sticky call-back bar: hides over the form, and stays closed once dismissed */
  var bar = $('cbBar');
  function closed() { return store(true, 'cbBarClosed') === '1'; }
  if (closed()) { bar.classList.add('hide'); document.body.classList.add('bar-off'); }
  $('cbClose').addEventListener('click', function () {
    bar.classList.add('hide'); document.body.classList.add('bar-off'); store(false, 'cbBarClosed', '1');
  });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      if (closed()) return;
      bar.classList.toggle('hide', entries[0].isIntersecting);
    }, { threshold: 0.2 }).observe($('callback'));
  }

  /* Footer year */
  var y = $('year'); if (y) y.textContent = new Date().getFullYear();

  /* Call-back form */
  var form = $('contactForm'), status = $('formStatus');
  function setStatus(msg, kind) { status.textContent = msg; status.className = 'form-status ' + (kind || ''); }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = false;
    form.querySelectorAll('[required]').forEach(function (f) {
      var b = !f.value.trim() || (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value));
      f.classList.toggle('invalid', b); if (b) bad = true;
    });
    if (bad) { setStatus('Please add your name, phone and a valid email.', 'err'); return; }
    var d = new FormData(form);
    if (d.get('_gotcha')) return;
    if (form.action.indexOf('YOUR_FORM_ID') !== -1) {
      var body = 'Name: ' + d.get('first_name') + ' ' + d.get('surname') + '\nPhone: ' + d.get('phone') +
        '\nEmail: ' + d.get('email') + '\nCompany: ' + (d.get('company') || '') + '\nIndustry: ' + (d.get('industry') || '') +
        '\nTopic: ' + d.get('service');
      window.location.href = 'mailto:info@riggsafrica.com?subject=' + encodeURIComponent('Call back request — ' + d.get('service')) + '&body=' + encodeURIComponent(body);
      setStatus('Opening your email app to send the request…', 'ok');
      return;
    }
    var btn = form.querySelector('button[type="submit"]'); btn.disabled = true; setStatus('Sending…');
    fetch(form.action, { method: 'POST', body: d, headers: { Accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(); form.reset(); setStatus('Thank you — an advisor will call you back shortly.', 'ok'); })
      .catch(function () { setStatus('Something went wrong. Please call +254 716 845 482 or email info@riggsafrica.com.', 'err'); })
      .then(function () { btn.disabled = false; });
  });
})();
