#!/usr/bin/env python3
"""Build the course catalogue, course pages and booking page from data/courses.json.

Run from the project root:  python3 tools/build.py
Outputs: courses/index.html, courses/<slug>.html, book.html, sitemap.xml, robots.txt
"""
import datetime as dt
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.riggsafrica.com"
WA = "254716845482"
LINKEDIN = "https://www.linkedin.com/in/joseph-reagan-barasa-mba-bcom-cpa-cisa-erm-irm-76575720/"

e = html.escape


def img(photo, w=900, q=72):
    return f"https://images.unsplash.com/{photo}?auto=format&fit=crop&w={w}&q={q}"


def add_workdays(start, days):
    d = start
    left = days - 1
    while left > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            left -= 1
    return d


def fmt_range(s, en):
    if s == en:
        return s.strftime("%-d %b %Y")
    if s.month == en.month:
        return f"{s.day}–{en.day} {s.strftime('%b %Y')}"
    return f"{s.strftime('%-d %b')} – {en.strftime('%-d %b %Y')}"


def load():
    with open(os.path.join(ROOT, "data", "courses.json"), encoding="utf-8") as f:
        data = json.load(f)
    cats = {c["id"]: c["name"] for c in data["categories"]}
    for c in data["courses"]:
        c["category_name"] = cats[c["category"]]
        out = []
        for s in c["sessions"]:
            start = dt.date.fromisoformat(s["start"])
            end = add_workdays(start, c["days"])
            out.append({
                "id": f"{c['slug']}-{s['start']}",
                "start": start, "end": end,
                "dates": fmt_range(start, end),
                "mode": s["mode"], "location": s["location"],
                "label": f"{fmt_range(start, end)} · {s['mode']} · {s['location']}",
            })
        out.sort(key=lambda x: x["start"])
        c["sessions_out"] = out
        c["duration"] = f"{c['days']} day" + ("s" if c["days"] > 1 else "")
    return data, cats


# ---------- shared chrome ----------

MEGA = [
    ("/#ways", "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z", "Governance, Risk &amp; Compliance", "ERM, board advisory, compliance, ESG risk"),
    ("/#ways", "M20 20l-4.5-4.5M11 5a6 6 0 100 12 6 6 0 000-12z", "Internal Audit &amp; Assurance", "Outsourced &amp; co-sourced audit, IT audits, fraud"),
    ("/#ways", "M4 19V9M10 19V5M16 19v-7M22 19H2", "Business Advisory", "Strategy, process improvement, operating models"),
    ("/#ways", "M3 7h18v12H3zM3 11h18", "Financial Advisory", "Budgeting, reporting, cash flow, CFO advisory"),
    ("/#ways", "M3 4h18v12H3zM8 20h8M12 16v4", "Technology &amp; Digital", "Digital strategy, IT governance, data, AI"),
    ("/courses", "M2 8l10-5 10 5-10 5zM6 10v5c3 2.5 9 2.5 12 0v-5", "Corporate Training", "14 courses · in-person, virtual &amp; in-house"),
]


def header(active=""):
    mega = "".join(
        f'<a href="{h}"><span class="mi"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{p}"/></svg></span>'
        f'<span><strong>{t}</strong><em>{d}</em></span></a>' for h, p, t, d in MEGA)
    def a(href, label, key):
        cls = ' class="active" aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    return f'''  <a class="skip" href="#main">Skip to content</a>
  <header class="header" id="header">
    <div class="wrap header-inner">
      <a href="/" class="brand" aria-label="Riggs Africa home"><img src="/assets/img/logo-dark.png" alt="Riggs Africa" width="445" height="83"></a>
      <div class="mega">
        <button type="button" class="mega-btn" id="megaBtn" aria-expanded="false" aria-controls="megaPanel">Services <svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
        <div class="mega-panel" id="megaPanel" hidden>{mega}</div>
      </div>
      <nav class="nav" id="nav" aria-label="Main">
        {a("/courses", "Courses", "courses")}
        {a("/#ways", "Consulting", "consulting")}
        {a("/#industries", "Industries", "industries")}
        {a("/#about", "About", "about")}
        {a("/#callback", "Contact", "contact")}
        <a href="/book" class="btn btn-teal nav-cta">Book a course</a>
      </nav>
      <div class="header-tools">
        <button type="button" class="search-btn" id="searchBtn" aria-label="Search courses" aria-expanded="false" aria-controls="searchPanel"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/></svg></button>
        <a href="tel:+254716845482" class="v3-tel desk-only">+254 716 845 482</a>
        <a href="/book" class="btn btn-ink desk-only">Book a course</a>
        <button type="button" class="menu-btn" id="menuBtn" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
      </div>
    </div>
    <div class="search-panel" id="searchPanel" hidden>
      <div class="wrap">
        <form class="v3-search search-panel-form" role="search" action="/courses" method="get">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/></svg>
          <label for="siteQ" class="sr">Search courses</label>
          <input id="siteQ" name="q" type="search" placeholder="Search courses, e.g. ISO 31000" autocomplete="off">
          <button type="submit" class="btn btn-ink">Search</button>
        </form>
        <div class="v3-popular"><span>Popular:</span><a href="/courses?cat=risk">Enterprise risk</a><a href="/courses?cat=audit">Internal audit</a><a href="/courses/ai-for-business">AI for business</a><a href="/courses?cat=board">Board governance</a></div>
      </div>
    </div>
  </header>'''


FOOTER = f'''  <footer class="footer">
    <div class="wrap">
      <div class="foot-grid">
        <div class="foot-brand"><img src="/assets/img/logo-light.png" alt="Riggs Africa" width="445" height="83" loading="lazy"><p>Trusted advice, practical solutions and long-term partnerships.</p>
          <div class="socials">
            <a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true" class="fill"><path d="M4 9h3.5v11H4zM5.7 3.5a2 2 0 110 4 2 2 0 010-4zM10 9h3.4v1.6c.5-.9 1.7-1.9 3.6-1.9 3.8 0 4.5 2.4 4.5 5.6V20H18v-5c0-1.2 0-2.8-1.7-2.8s-2 1.3-2 2.7V20H10z"/></svg></a>
            <a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-4A8 8 0 1112 20a8 8 0 01-3.9-1z"/></svg></a>
          </div>
        </div>
        <div class="foot-col"><h4>Training</h4><a href="/courses">All courses</a><a href="/book">Book a course</a><a href="/courses#inhouse">In-house training</a></div>
        <div class="foot-col"><h4>Consulting</h4><a href="/#ways">Ways to work with us</a><a href="/#industries">Industries</a></div>
        <div class="foot-col"><h4>Riggs Africa</h4><a href="/#about">About</a><a href="/#about">Leadership</a><a href="/#callback">Contact</a></div>
        <div class="foot-col"><h4>Get in touch</h4><a href="mailto:info@riggsafrica.com">info@riggsafrica.com</a><a href="tel:+254716845482">+254 716 845 482</a><span>Nairobi, Kenya</span></div>
      </div>
      <div class="foot-bottom"><span>© <span id="year">2026</span> Riggs Africa Solutions Limited</span><span>Privacy policy · Terms</span></div>
    </div>
  </footer>'''


def page(title, desc, path, body, active="", scripts=("/assets/js/main.js",), extra_head=""):
    js = "\n".join(f'  <script src="{s}" defer></script>' for s in scripts)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="{SITE}{path}">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/icon-32.png">
  <link rel="apple-touch-icon" href="/assets/img/icon-180.png">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE}{path}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{SITE}/assets/img/og-image.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://images.unsplash.com">
  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css">
{extra_head}</head>
<body class="sub">
{header(active)}
  <main id="main">
{body}
  </main>
{FOOTER}
{js}
</body>
</html>
'''


ICON = {
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "level": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20v-5M10 20V10M16 20V6M22 20H2"/></svg>',
    "format": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="12" rx="2"/><path d="M8 21h8"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "cal": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    "check": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12l5 5L20 6"/></svg>',
    "user": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>',
}


def card(c):
    nxt = c["sessions_out"][0]["dates"] if c["sessions_out"] else "On request"
    fmts = " ".join(f.lower().replace("-", "") for f in c["formats"])
    return f'''<article class="ccard" data-cat="{c['category']}" data-formats="{fmts}" data-level="{e(c['level'].lower())}" data-text="{e((c['title'] + ' ' + c['summary'] + ' ' + c['category_name']).lower())}">
  <a class="ccard-img ph" href="/courses/{c['slug']}" tabindex="-1" aria-hidden="true"><img src="{img(c['image'], 700, 70)}" alt="" loading="lazy"><span class="badge">{e(c['category_name'])}</span></a>
  <div class="ccard-body">
    <h3><a href="/courses/{c['slug']}">{e(c['title'])}</a></h3>
    <p>{e(c['summary'])}</p>
    <ul class="meta"><li>{ICON['clock']}{c['duration']}</li><li>{ICON['level']}{e(c['level'])}</li><li>{ICON['format']}{e(' · '.join(c['formats']))}</li></ul>
    <div class="ccard-foot"><span class="next"><b>Next</b>{e(nxt)}</span><a class="btn btn-teal btn-sm" href="/book?course={c['slug']}">Book</a></div>
  </div>
</article>'''


HOW = '''<ol class="how">
  <li><b>1</b><div><h3>Choose a course &amp; date</h3><p>Pick a public session, or ask for in-house dates for your team.</p></div></li>
  <li><b>2</b><div><h3>Send your booking</h3><p>Tell us who is attending. It takes about two minutes.</p></div></li>
  <li><b>3</b><div><h3>We confirm &amp; share fees</h3><p>We confirm your place and send you the fees and joining details.</p></div></li>
  <li><b>4</b><div><h3>Attend &amp; apply</h3><p>Practical sessions, templates to take home and a Riggs Africa certificate of completion.</p></div></li>
</ol>'''


def catalogue(data, cats):
    counts = {k: 0 for k in cats}
    for c in data["courses"]:
        counts[c["category"]] += 1
    chips = '<button type="button" class="chip-f on" data-cat="all">All courses <span>' + str(len(data["courses"])) + '</span></button>' + "".join(
        f'<button type="button" class="chip-f" data-cat="{k}">{e(v)} <span>{counts[k]}</span></button>' for k, v in cats.items())
    cards = "\n".join(card(c) for c in data["courses"])
    body = f'''    <section class="page-hero">
      <img class="hero-map" src="/assets/img/africa-map.svg" alt="" aria-hidden="true">
      <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>Courses</span></nav>
        <span class="eyebrow">Corporate training</span>
        <h1>Practical courses in risk, audit, governance &amp; technology</h1>
        <p class="lead">{len(data['courses'])} programmes your team can apply the next morning — in Nairobi, live online or in-house at your organisation.</p>
        <div class="search">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/></svg>
          <label class="sr" for="q">Search courses</label>
          <input id="q" type="search" placeholder="Search courses, e.g. audit, ISO 31000, AI" autocomplete="off">
        </div>
      </div>
    </section>

    <section class="catalog wrap">
      <div class="filters" role="group" aria-label="Filter by category">{chips}</div>
      <div class="filters2">
        <label>Format <select id="fFormat"><option value="">Any format</option><option value="inperson">In-person</option><option value="virtual">Virtual</option><option value="inhouse">In-house</option></select></label>
        <label>Level <select id="fLevel"><option value="">Any level</option><option>foundation</option><option>intermediate</option><option>advanced</option><option>executive</option><option>all levels</option></select></label>
        <p class="result-count" id="count" aria-live="polite">{len(data['courses'])} courses</p>
      </div>
      <div class="cgrid" id="grid">
{cards}
      </div>
      <p class="empty" id="empty" hidden>No courses match. Try another search, or <a href="/book?course=custom">ask us for a tailored programme</a>.</p>
    </section>

    <section class="section section-soft">
      <div class="wrap">
        <div class="sec-head"><div><span class="eyebrow">Booking</span><h2>How booking works</h2></div><a class="btn btn-teal" href="/book">Book a course <span aria-hidden="true">→</span></a></div>
        {HOW}
      </div>
    </section>

    <section class="section" id="inhouse">
      <div class="wrap">
        <div class="inhouse">
          <div>
            <span class="eyebrow eyebrow-copper">In-house training</span>
            <h2>Train your whole team, on your dates</h2>
            <p>Any course can be delivered at your premises or online for your team only, tailored to your sector, policies and real risks. Ideal for 8 or more participants.</p>
            <ul class="ticks"><li>{ICON['check']}Content tailored to your organisation</li><li>{ICON['check']}Dates and venue that suit you</li><li>{ICON['check']}Workshops on your own risks and processes</li></ul>
          </div>
          <div class="inhouse-cta">
            <a class="btn btn-teal" href="/book?course=custom">Request in-house training <span aria-hidden="true">→</span></a>
            <a class="btn btn-outline" href="https://wa.me/{WA}?text={e('Hello Riggs Africa, I would like to ask about in-house training.')}" target="_blank" rel="noopener">Ask on WhatsApp</a>
          </div>
        </div>
      </div>
    </section>'''
    return page("Courses | Riggs Africa Solutions",
                f"{len(data['courses'])} practical courses in enterprise risk management, internal audit, ISO 31000, COSO, IT audit, fraud, AI and board governance — in Nairobi, online or in-house.",
                "/courses", body, "courses", ("/assets/js/main.js", "/assets/js/courses.js"))


def course_page(c, data):
    sessions = c["sessions_out"]
    sess_html = "".join(f'''<li><label class="sess"><input type="radio" name="session" value="{s['id']}"{' checked' if i == 0 else ''}><span class="sess-box"><span class="sess-date">{ICON['cal']}{e(s['dates'])}</span><span class="sess-meta">{e(s['mode'])} · {e(s['location'])}</span></span></label></li>''' for i, s in enumerate(sessions))
    first = sessions[0]["id"] if sessions else ""
    outcomes = "".join(f"<li>{ICON['check']}{e(o)}</li>" for o in c["outcomes"])
    audience = "".join(f"<span>{e(a)}</span>" for a in c["audience"])
    mods = "".join(f'''<details class="mod"{' open' if i == 0 else ''}><summary><b>{i+1:02d}</b><span>{e(m['title'])}</span><svg class="chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary><ul>{''.join(f'<li>{e(t)}</li>' for t in m['topics'])}</ul></details>''' for i, m in enumerate(c["modules"]))
    ntopics = sum(len(m["topics"]) for m in c["modules"])
    related = [x for x in data["courses"] if x["category"] == c["category"] and x["slug"] != c["slug"]]
    related += [x for x in data["courses"] if x["category"] != c["category"] and x not in related]
    rel = "\n".join(card(x) for x in related[:3])
    wa = e(f"Hello Riggs Africa, I have a question about the course: {c['title']}.")
    schema = {
        "@context": "https://schema.org", "@type": "Course", "name": c["title"], "description": c["summary"],
        "provider": {"@type": "Organization", "name": "Riggs Africa Solutions Limited", "sameAs": SITE},
        "hasCourseInstance": [{"@type": "CourseInstance", "courseMode": "online" if s["mode"] == "Virtual" else "onsite",
                               "startDate": s["start"].isoformat(), "endDate": s["end"].isoformat(),
                               "location": s["location"]} for s in sessions],
    }
    body = f'''    <section class="page-hero course-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/courses">Courses</a><span aria-hidden="true">/</span><span>{e(c['category_name'])}</span></nav>
        <div class="ch-grid">
          <div>
            <span class="eyebrow">{e(c['category_name'])}</span>
            <h1>{e(c['title'])}</h1>
            <p class="lead">{e(c['summary'])}</p>
            <ul class="meta meta-lg"><li>{ICON['clock']}{c['duration']}</li><li>{ICON['level']}{e(c['level'])}</li><li>{ICON['format']}{e(' · '.join(c['formats']))}</li><li>{ICON['user']}Max 20 per public session</li></ul>
            <div class="actions"><a class="btn btn-teal" href="#sessions">Book a slot <span aria-hidden="true">→</span></a><a class="btn btn-outline" href="#modules">See the {len(c['modules'])} modules</a></div>
          </div>
          <div class="ph ch-img"><img src="{img(c['image'], 1000, 75)}" alt=""></div>
        </div>
      </div>
    </section>

    <div class="wrap course-layout">
      <div class="course-main">
        <section class="block reveal" id="overview"><h2>Course overview</h2><p class="body-lg">{e(c['overview'])}</p></section>
        <section class="block reveal"><h2>What you'll be able to do</h2><ul class="ticks ticks-2">{outcomes}</ul></section>
        <section class="block reveal"><h2>Who should attend</h2><div class="pills pills-lg">{audience}</div></section>
        <section class="block reveal" id="modules">
          <div class="block-head"><h2>Course modules</h2><span class="muted">{len(c['modules'])} modules · {ntopics} topics</span><button type="button" class="link-btn" id="toggleMods">Expand all</button></div>
          <div class="mods">{mods}</div>
        </section>
        <section class="block reveal"><h2>How it's delivered</h2>
          <div class="deliver">
            <div>{ICON['user']}<h3>Interactive &amp; practical</h3><p>Short inputs, case studies, group exercises and work on your own organisation's examples.</p></div>
            <div>{ICON['format']}<h3>Materials to keep</h3><p>Slides, templates and checklists you can use straight away.</p></div>
            <div>{ICON['check']}<h3>Certificate</h3><p>A Riggs Africa certificate of completion for every participant who attends in full.</p></div>
          </div>
        </section>
        <section class="block reveal"><h2>Questions</h2>
          <details class="faq"><summary>How much does the course cost?</summary><p>Book a slot and we'll send you the fees when we confirm your booking. There's no payment at the booking stage.</p></details>
          <details class="faq"><summary>Can you run this course for our team only?</summary><p>Yes. Any course can be delivered in-house at your premises or online, on dates that suit you, and tailored to your sector. <a href="/book?course={c['slug']}&amp;session=inhouse">Request in-house dates</a>.</p></details>
          <details class="faq"><summary>Are the dates confirmed?</summary><p>Public session dates are provisional until we confirm your booking. If a session moves, we'll let you know and offer the next available date.</p></details>
          <details class="faq"><summary>What do participants need to bring?</summary><p>A notebook and an open mind. For practical sessions such as data analytics, please bring a laptop. Virtual sessions need a stable internet connection.</p></details>
        </section>
      </div>

      <aside class="course-side" id="sessions">
        <form class="book-card" action="/book" method="get">
          <input type="hidden" name="course" value="{c['slug']}">
          <h2>Upcoming sessions</h2>
          <p class="prov">Provisional dates · confirmed when you book</p>
          <ul class="sess-list">{sess_html}<li><label class="sess"><input type="radio" name="session" value="inhouse"{'' if sessions else ' checked'}><span class="sess-box"><span class="sess-date">{ICON['user']}In-house for my team</span><span class="sess-meta">Your dates · your venue or online</span></span></label></li></ul>
          <div class="fee"><b>Fees</b><span>Shared when we confirm your booking.</span></div>
          <button type="submit" class="btn btn-teal btn-block">Book a slot <span aria-hidden="true">→</span></button>
          <a class="btn btn-wa btn-block" href="https://wa.me/{WA}?text={wa}" target="_blank" rel="noopener">Ask a question on WhatsApp</a>
        </form>
      </aside>
    </div>

    <section class="section section-soft">
      <div class="wrap">
        <div class="sec-head"><div><span class="eyebrow">Keep learning</span><h2>Related courses</h2></div><a class="link" href="/courses">All courses →</a></div>
        <div class="cgrid cgrid-3">
{rel}
        </div>
      </div>
    </section>

    <div class="mobile-book"><div><b>{e(c['title'])}</b><span>{e(sessions[0]['dates'] if sessions else 'In-house on request')}</span></div><a class="btn btn-teal" href="/book?course={c['slug']}&amp;session={first or 'inhouse'}">Book</a></div>'''
    head = f'  <script type="application/ld+json">{json.dumps(schema)}</script>\n'
    return page(f"{c['title']} | Riggs Africa Training", c["summary"], f"/courses/{c['slug']}", body, "courses",
                ("/assets/js/main.js", "/assets/js/course.js"), head)


def book(data, cats):
    payload = {
        "categories": cats,
        "courses": [{"slug": c["slug"], "title": c["title"], "category": c["category"], "duration": c["duration"],
                     "formats": c["formats"], "image": img(c["image"], 500, 65),
                     "sessions": [{"id": s["id"], "label": s["label"], "dates": s["dates"], "mode": s["mode"], "location": s["location"]} for s in c["sessions_out"]]}
                    for c in data["courses"]],
    }
    opts = ""
    for k, v in cats.items():
        items = "".join(f'<option value="{c["slug"]}">{e(c["title"])}</option>' for c in data["courses"] if c["category"] == k)
        opts += f'<optgroup label="{e(v)}">{items}</optgroup>'
    opts += '<optgroup label="Other"><option value="custom">Tailored / in-house programme</option></optgroup>'
    body = f'''    <section class="page-hero book-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/courses">Courses</a><span aria-hidden="true">/</span><span>Book</span></nav>
        <h1>Book a course</h1>
        <p class="lead">Reserve your place in about two minutes. No payment now — we'll confirm your booking and send you the fees.</p>
        <ol class="steps-mini"><li class="on"><b>1</b>Choose course</li><li><b>2</b>Your details</li><li><b>3</b>We confirm</li></ol>
      </div>
    </section>

    <div class="wrap book-layout">
      <form class="bform" id="bookForm" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate>
        <fieldset>
          <legend><b>1</b>Course &amp; session</legend>
          <label class="full">Course<select name="course" id="bCourse" required><option value="">Choose a course</option>{opts}</select></label>
          <div class="full"><span class="lbl" id="sessLbl">Session</span><div class="bsess" id="bSess" role="radiogroup" aria-labelledby="sessLbl"><p class="muted">Choose a course to see dates.</p></div></div>
          <label>Number of participants
            <span class="stepper"><button type="button" id="pMinus" aria-label="Fewer participants">−</button><input type="number" name="participants" id="bPeople" value="1" min="1" max="200" inputmode="numeric"><button type="button" id="pPlus" aria-label="More participants">+</button></span>
          </label>
          <label>Booking as
            <select name="booking_as" id="bAs" required><option value="">Select</option><option>Individual</option><option>Startup / SME</option><option>Corporate / private company</option><option>Public institution / government</option><option>NGO / development organisation</option><option>SACCO / microfinance</option></select>
          </label>
        </fieldset>
        <fieldset>
          <legend><b>2</b>Your details</legend>
          <label>Full name<input type="text" name="name" autocomplete="name" required></label>
          <label>Job title<input type="text" name="job_title" autocomplete="organization-title"></label>
          <label>Organisation<input type="text" name="organisation" autocomplete="organization"></label>
          <label>Email<input type="email" name="email" autocomplete="email" required></label>
          <label>Phone<input type="tel" name="phone" autocomplete="tel" placeholder="+254" required></label>
          <label>Best way to reach you<select name="contact_by"><option>Email</option><option>Phone call</option><option>WhatsApp</option></select></label>
          <label class="full"><span>Participants' names <span class="opt">(optional)</span></span><textarea name="participant_names" rows="3" placeholder="One per line, with job titles if you have them"></textarea></label>
          <label class="full"><span>Anything we should know? <span class="opt">(optional)</span></span><textarea name="notes" rows="3" placeholder="e.g. preferred in-house dates, accessibility needs, invoicing details"></textarea></label>
          <label class="check full"><input type="checkbox" name="consent" required> I agree that Riggs Africa may contact me about this booking.</label>
        </fieldset>
        <input type="hidden" name="reference" id="bRef">
        <input type="hidden" name="session_label" id="bSessLabel">
        <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <button type="submit" class="btn btn-teal btn-block btn-lg">Send booking request <span aria-hidden="true">→</span></button>
        <p class="form-status" id="bStatus" role="status" aria-live="polite"></p>
      </form>

      <aside class="bsum" id="bSum" aria-live="polite">
        <div class="ph bsum-img" id="sumImg"></div>
        <div class="bsum-body">
          <span class="k">Your booking</span>
          <h2 id="sumTitle">Choose a course</h2>
          <dl>
            <div><dt>Session</dt><dd id="sumSess">—</dd></div>
            <div><dt>Participants</dt><dd id="sumPeople">1</dd></div>
            <div><dt>Booking as</dt><dd id="sumAs">—</dd></div>
            <div><dt>Fees</dt><dd>Shared after booking</dd></div>
          </dl>
          <p class="bsum-note">No payment now. We'll confirm within one working day and send you the fees.</p>
        </div>
      </aside>

      <section class="bdone" id="bDone" hidden tabindex="-1">
        <div class="done-ic">{ICON['check']}</div>
        <h2>Booking request ready</h2>
        <p>Your reference is <b id="doneRef">—</b>. We'll confirm your place and send you the fees.</p>
        <p class="muted" id="doneHow"></p>
        <ol class="next-steps"><li>We check availability for your session.</li><li>We email or call you with the fees and joining details.</li><li>Your place is secured once you confirm.</li></ol>
        <div class="actions"><a class="btn btn-wa" id="doneWa" href="https://wa.me/{WA}" target="_blank" rel="noopener">Also send on WhatsApp</a><a class="btn btn-outline" href="/courses">Back to courses</a></div>
      </section>
    </div>
    <script type="application/json" id="courseData">{json.dumps(payload).replace("</", "<\\/")}</script>'''
    return page("Book a course | Riggs Africa Solutions", "Book a place on a Riggs Africa training course. No payment now — we confirm your booking and share the fees.",
                "/book", body, "", ("/assets/js/main.js", "/assets/js/book.js"))


FEATURED = [  # shown on the home page under "Programmes in demand"
    "enterprise-risk-management-practical-approach",
    "risk-based-internal-auditing",
    "ai-for-business",
    "board-effectiveness-governance",
    "iso-31000-risk-management",
    "fraud-risk-management",
]

CAT_SHORT = {"risk": "Risk", "audit": "Audit", "tech": "Technology", "finance": "Finance", "board": "Boards", "health": "Healthcare"}
CAT_ICON = {
    "risk": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/>',
    "audit": '<path d="M9 5h10v14H5V9z"/><path d="M9 5v4H5"/><path d="M9 14l2 2 4-4"/>',
    "tech": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M10 2v4M14 2v4M10 18v4M14 18v4M2 10h4M2 14h4M18 10h4M18 14h4"/>',
    "finance": '<path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/>',
    "board": '<circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M3 20c0-3 2.5-5 5-5s5 2 5 5M11 20c0-3 2.5-5 5-5s5 2 5 5"/>',
    "health": '<path d="M12 20s-7-4.5-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.5-7 10-7 10z"/>',
}


def home_programmes(data):
    by = {c["slug"]: c for c in data["courses"]}
    out = []
    for slug in FEATURED:
        c = by[slug]
        s = c["sessions_out"][0] if c["sessions_out"] else None
        when = f"{s['dates']} · {s['location']}" if s else "Dates on request"
        out.append(f'''          <a class="v3-cc" data-cat="{c['category']}" href="/courses/{slug}">
            <div class="v3-cc-top"><span class="v3-cc-tag">{CAT_SHORT[c['category']]}</span><span class="v3-cc-ic"><svg viewBox="0 0 24 24" aria-hidden="true">{CAT_ICON[c['category']]}</svg></span></div>
            <div class="v3-cc-body"><h3>{e(c["title"])}</h3><p>{e(c["summary"])}</p>
              <ul class="v3-cc-meta"><li>{c['duration']}</li><li>{e(' · '.join(c['formats'][:2]))}</li><li>{e(c['level'])}</li></ul>
              <span class="v3-cc-next"><b>Next</b>{e(when)}</span></div>
          </a>''')
    return "\n".join(out)


def home_next(data):
    today = dt.date.today()
    best = None
    for c in data["courses"]:
        for s in c["sessions_out"]:
            if s["start"] >= today and (best is None or s["start"] < best[1]["start"]):
                best = (c, s)
    if not best:
        return '          <a class="v3-next" href="/courses"><span class="v3-next-k">Training</span><strong>14 courses in 6 fields</strong><span class="v3-next-go">Browse courses →</span></a>'
    c, s = best
    return (f'          <a class="v3-next" href="/courses/{c["slug"]}"><span class="v3-next-k">Next intake</span>'
            f'<strong>{e(c["title"])}</strong><span class="v3-next-d">{e(s["dates"])} · {e(s["location"])}</span>'
            f'<span class="v3-next-go">Reserve a seat →</span></a>')


def _splice(s, start, end, body):
    a = s.index(start)
    a = s.index("-->", a) + 3
    b = s.index(end)
    return s[:a] + "\n" + body + "\n" + s[b:]


def patch_home(data):
    path = os.path.join(ROOT, "index.html")
    with open(path, encoding="utf-8") as f:
        s = f.read()
    s = _splice(s, "<!-- PROGRAMMES:START", "<!-- PROGRAMMES:END -->", home_programmes(data))
    if "<!-- NEXT:START" in s:
        s = _splice(s, "<!-- NEXT:START", "<!-- NEXT:END -->", home_next(data))
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


def main():
    data, cats = load()
    patch_home(data)
    os.makedirs(os.path.join(ROOT, "courses"), exist_ok=True)
    written = []
    def w(rel, text):
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
            f.write(text)
        written.append(rel)
    w("courses/index.html", catalogue(data, cats))
    for c in data["courses"]:
        w(f"courses/{c['slug']}.html", course_page(c, data))
    w("book.html", book(data, cats))
    urls = ["/", "/courses", "/book"] + [f"/courses/{c['slug']}" for c in data["courses"]]
    today = dt.date.today().isoformat()
    w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Built {len(written)} files:", ", ".join(written[:4]), "…")


if __name__ == "__main__":
    main()
