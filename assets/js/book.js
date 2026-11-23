/* Booking page: course + session picker, live summary, validation and sending */
(function () {
  var form = document.getElementById('bookForm');
  if (!form) return;
  var data = JSON.parse(document.getElementById('courseData').textContent);
  var bySlug = {};
  data.courses.forEach(function (c) { bySlug[c.slug] = c; });

  var $ = function (id) { return document.getElementById(id); };
  var sel = $('bCourse'), sessBox = $('bSess'), people = $('bPeople'), as = $('bAs');
  var status = $('bStatus');

  function esc(s) { return String(s).replace(/[&<>"]/g, function (ch) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]; }); }

  function renderSessions(slug, wanted) {
    var c = bySlug[slug], html = '';
    if (!slug) { sessBox.innerHTML = '<p class="muted">Choose a course to see dates.</p>'; return; }
    var list = c ? c.sessions : [];
    list.forEach(function (s) {
      html += '<label class="sess"><input type="radio" name="session" value="' + esc(s.id) + '" data-label="' + esc(s.label) + '"><span class="sess-box"><span class="sess-date">' + esc(s.dates) + '</span><span class="sess-meta">' + esc(s.mode) + ' · ' + esc(s.location) + '</span></span></label>';
    });
    html += '<label class="sess"><input type="radio" name="session" value="inhouse" data-label="In-house / custom dates"><span class="sess-box"><span class="sess-date">In-house for my team</span><span class="sess-meta">Your dates · your venue or online</span></span></label>';
    sessBox.innerHTML = html;
    var radios = sessBox.querySelectorAll('input');
    var pick = Array.prototype.find.call(radios, function (r) { return r.value === wanted; }) || radios[0];
    if (pick) pick.checked = true;
  }

  function current() {
    var r = sessBox.querySelector('input:checked');
    return { course: bySlug[sel.value], slug: sel.value, sessionId: r ? r.value : '', sessionLabel: r ? r.dataset.label : '' };
  }

  function summary() {
    var cur = current();
    $('sumTitle').textContent = cur.course ? cur.course.title : (cur.slug === 'custom' ? 'Tailored / in-house programme' : 'Choose a course');
    $('sumSess').textContent = cur.sessionLabel || '—';
    $('sumPeople').textContent = people.value || '1';
    $('sumAs').textContent = as.value || '—';
    var img = $('sumImg');
    img.innerHTML = cur.course ? '<img src="' + esc(cur.course.image) + '" alt="">' : '';
    var im = img.querySelector('img');
    if (im) im.addEventListener('error', function () { im.remove(); });
    var steps = document.querySelectorAll('.steps-mini li');
    if (steps.length) { steps[0].classList.add('on'); steps[1].classList.toggle('on', !!(cur.slug && as.value)); }
  }

  // Pre-fill from ?course=&session=
  var p = new URLSearchParams(location.search);
  if (p.get('course') && (bySlug[p.get('course')] || p.get('course') === 'custom')) sel.value = p.get('course');
  renderSessions(sel.value, p.get('session'));
  summary();

  sel.addEventListener('change', function () { renderSessions(sel.value); summary(); });
  sessBox.addEventListener('change', summary);
  as.addEventListener('change', summary);
  people.addEventListener('input', summary);
  $('pMinus').addEventListener('click', function () { people.value = Math.max(1, (+people.value || 1) - 1); summary(); });
  $('pPlus').addEventListener('click', function () { people.value = Math.min(200, (+people.value || 1) + 1); summary(); });

  function setStatus(msg, kind) { status.textContent = msg; status.className = 'form-status ' + (kind || ''); }

  // Clear a field's error as soon as it is fixed
  function clearErr(e) {
    var t = e.target;
    if (t.classList.contains('invalid')) t.classList.remove('invalid');
    if (t.name === 'session') sessBox.classList.remove('invalid');
    if (!form.querySelector('.invalid') && !sessBox.classList.contains('invalid')) setStatus('');
  }
  form.addEventListener('input', clearErr);
  form.addEventListener('change', clearErr);

  function reference() {
    var d = new Date(), pad = function (n) { return (n < 10 ? '0' : '') + n; };
    return 'RA-' + String(d.getFullYear()).slice(2) + pad(d.getMonth() + 1) + pad(d.getDate()) + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var bad = [];
    form.querySelectorAll('[required]').forEach(function (f) {
      var b = f.type === 'checkbox' ? !f.checked : (!f.value.trim() || (f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value)));
      f.classList.toggle('invalid', b);
      if (b) bad.push(f);
    });
    if (!sessBox.querySelector('input:checked')) { bad.push(sessBox); sessBox.classList.add('invalid'); } else sessBox.classList.remove('invalid');
    if (bad.length) {
      setStatus('Please complete the highlighted fields.', 'err');
      var first = bad[0]; if (first.focus) first.focus();
      return;
    }
    var cur = current(), ref = reference();
    $('bRef').value = ref;
    $('bSessLabel').value = cur.sessionLabel;
    var fd = new FormData(form);
    if (fd.get('_gotcha')) return;

    var title = cur.course ? cur.course.title : 'Tailored / in-house programme';
    var lines = [
      'Booking reference: ' + ref,
      'Course: ' + title,
      'Session: ' + cur.sessionLabel,
      'Participants: ' + fd.get('participants'),
      'Booking as: ' + fd.get('booking_as'),
      '',
      'Name: ' + fd.get('name'),
      'Job title: ' + (fd.get('job_title') || ''),
      'Organisation: ' + (fd.get('organisation') || ''),
      'Email: ' + fd.get('email'),
      'Phone: ' + fd.get('phone'),
      'Contact by: ' + fd.get('contact_by'),
      '',
      'Participants: ' + (fd.get('participant_names') || '—'),
      'Notes: ' + (fd.get('notes') || '—')
    ];
    var text = lines.join('\n');
    var waText = 'Hello Riggs Africa, I have just sent a booking request (' + ref + ') for ' + title + ' — ' + cur.sessionLabel + ', ' + fd.get('participants') + ' participant(s).';

    function done(how) {
      form.hidden = true;
      $('bSum').hidden = true;
      var box = $('bDone');
      $('doneRef').textContent = ref;
      $('doneHow').textContent = how;
      $('doneWa').href = 'https://wa.me/254716845482?text=' + encodeURIComponent(waText);
      box.hidden = false;
      var steps = document.querySelectorAll('.steps-mini li');
      steps.forEach(function (s) { s.classList.add('on'); });
      box.focus();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    if (form.action.indexOf('YOUR_FORM_ID') !== -1) {
      // No form service connected yet: hand the booking to the visitor's email app
      window.location.href = 'mailto:info@riggsafrica.com?subject=' + encodeURIComponent('Course booking ' + ref + ' — ' + title) + '&body=' + encodeURIComponent(text);
      done('Your email app should open with the booking filled in — please press Send. If it did not open, send it on WhatsApp below.');
      return;
    }
    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true; setStatus('Sending…');
    fetch(form.action, { method: 'POST', body: fd, headers: { Accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(); done('We have received it and sent a copy to our team.'); })
      .catch(function () { setStatus('Something went wrong. Please call +254 716 845 482 or send your booking on WhatsApp.', 'err'); })
      .then(function () { btn.disabled = false; });
  });
})();
