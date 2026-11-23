/* Course page: expand/collapse modules, mobile booking bar */
(function () {
  var btn = document.getElementById('toggleMods');
  var mods = Array.prototype.slice.call(document.querySelectorAll('.mod'));
  if (btn && mods.length) {
    function sync() { var all = mods.every(function (m) { return m.open; }); btn.textContent = all ? 'Collapse all' : 'Expand all'; }
    btn.addEventListener('click', function () {
      var open = !mods.every(function (m) { return m.open; });
      mods.forEach(function (m) { m.open = open; });
      sync();
    });
    mods.forEach(function (m) { m.addEventListener('toggle', sync); });
    sync();
  }

  /* Keep the mobile "Book" bar in step with the chosen session, and hide it over the booking card */
  var bar = document.querySelector('.mobile-book'), side = document.getElementById('sessions');
  if (bar && side) {
    var link = bar.querySelector('a'), label = bar.querySelector('span');
    side.addEventListener('change', function (e) {
      if (e.target.name !== 'session') return;
      var u = new URL(link.href, location.href);
      u.searchParams.set('session', e.target.value);
      link.href = u.pathname + u.search;
      var d = e.target.closest('label').querySelector('.sess-date');
      if (d) label.textContent = d.textContent;
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { bar.classList.toggle('hide', en[0].isIntersecting); }, { threshold: 0.1 }).observe(side);
    }
  }
})();
