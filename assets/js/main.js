(function () {
  var header = document.getElementById('siteHeader');
  var nav = document.getElementById('nav');
  var menuBtn = document.getElementById('menuBtn');

  // Mobile / tablet menu
  function setMenu(open) {
    nav.classList.toggle('open', open);
    header.classList.toggle('menu-on', open);
    document.body.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  menuBtn.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); menuBtn.focus(); } });
  window.addEventListener('resize', function () { if (window.innerWidth > 1080) setMenu(false); });

  // Highlight the nav link for the section in view
  if ('IntersectionObserver' in window) {
    var links = Array.prototype.slice.call(nav.querySelectorAll('a:not(.btn)'));
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ['services', 'approach', 'industries', 'training', 'contact'].forEach(function (id) {
      var s = document.getElementById(id); if (s) spy.observe(s);
    });
  }

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Contact form
  var form = document.getElementById('contactForm');
  var status = document.getElementById('formStatus');
  if (!form) return;

  function setStatus(msg, kind) { status.textContent = msg; status.className = 'form-status ' + (kind || ''); }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var invalid = false;
    form.querySelectorAll('[required]').forEach(function (f) {
      var bad = !f.value.trim() || (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value));
      f.classList.toggle('invalid', bad);
      if (bad) invalid = true;
    });
    if (invalid) { setStatus('Please fill in your name, a valid email and a message.', 'err'); return; }

    var data = new FormData(form);
    if (data.get('_gotcha')) return; // spam bot

    // No form service configured yet: fall back to the visitor's email app
    if (form.action.indexOf('YOUR_FORM_ID') !== -1) {
      var body = 'Name: ' + data.get('name') + '\nCompany: ' + (data.get('company') || '') +
        '\nEmail: ' + data.get('email') + '\nPhone: ' + (data.get('phone') || '') +
        '\nService: ' + data.get('service') + '\n\n' + data.get('message');
      window.location.href = 'mailto:info@riggsafrica.com?subject=' +
        encodeURIComponent('Consultation request — ' + data.get('service')) + '&body=' + encodeURIComponent(body);
      setStatus('Opening your email app to send the enquiry…', 'ok');
      return;
    }

    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    setStatus('Sending…');
    fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
      .then(function (r) {
        if (!r.ok) throw new Error('bad status');
        form.reset();
        setStatus('Thank you — your enquiry has been sent. We will be in touch shortly.', 'ok');
      })
      .catch(function () {
        setStatus('Something went wrong. Please email info@riggsafrica.com directly.', 'err');
      })
      .then(function () { btn.disabled = false; });
  });
})();
