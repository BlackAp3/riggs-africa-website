/* Course catalogue: search, category chips, format and level filters */
(function () {
  var grid = document.getElementById('grid');
  if (!grid) return;
  var cards = Array.prototype.slice.call(grid.children);
  var q = document.getElementById('q'), fFormat = document.getElementById('fFormat'), fLevel = document.getElementById('fLevel');
  var count = document.getElementById('count'), empty = document.getElementById('empty');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip-f'));
  var cat = 'all';

  var params = new URLSearchParams(location.search);
  if (params.get('cat')) cat = params.get('cat');
  if (params.get('q')) q.value = params.get('q');

  function apply() {
    var term = q.value.trim().toLowerCase(), fm = fFormat.value, lv = fLevel.value, shown = 0;
    cards.forEach(function (c) {
      var ok = (cat === 'all' || c.dataset.cat === cat) &&
        (!fm || c.dataset.formats.indexOf(fm) !== -1) &&
        (!lv || c.dataset.level === lv) &&
        (!term || term.split(/\s+/).every(function (w) { return c.dataset.text.indexOf(w) !== -1; }));
      c.hidden = !ok;
      if (ok) shown++;
    });
    chips.forEach(function (ch) { var on = ch.dataset.cat === cat; ch.classList.toggle('on', on); ch.setAttribute('aria-pressed', String(on)); });
    count.textContent = shown + (shown === 1 ? ' course' : ' courses');
    empty.hidden = shown !== 0;
  }
  chips.forEach(function (ch) { ch.addEventListener('click', function () { cat = ch.dataset.cat; apply(); }); });
  q.addEventListener('input', apply);
  fFormat.addEventListener('change', apply);
  fLevel.addEventListener('change', apply);
  apply();
})();
