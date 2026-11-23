# Riggs Africa — website

Static one-page site (HTML + CSS + vanilla JS). No build step.

```
index.html
assets/css/styles.css
assets/js/main.js
assets/img/   logos, Africa map, favicons, social image
vercel.json   clean URLs, caching and security headers
```

## Run locally
```bash
npx serve .        # or: python3 -m http.server 8000
```

## Deploy to Vercel
1. Push this folder to a GitHub repo.
2. In Vercel: **Add New → Project → Import** the repo.
3. Framework preset: **Other**. Leave build command and output directory empty.
4. Deploy, then add the domain (e.g. `riggsafrica.com`) under **Settings → Domains**.

Or from the CLI: `npx vercel` (preview) and `npx vercel --prod`.

## Contact form
Until a form service is set up, **Send enquiry** opens the visitor's email app addressed to info@riggsafrica.com.

To receive submissions directly:
1. Create a free form at https://formspree.io and copy its ID.
2. In `index.html`, replace `YOUR_FORM_ID` in the form's `action` with that ID.

## Before launch — content to fill in
- Case study results: the `[+X%]`, `[X wks]`, `[X→Y]` and `[Sector]` placeholders (client-approved only).
- Privacy and Terms links in the footer.
- The hero dashboard is labelled "Illustrative" — keep that label or replace it with real data.

## Breakpoints
- Laptop/desktop: above 1080px
- Tablet: 721–1080px (menu button, two-column grids)
- Mobile: 720px and below (single column)

## Courses and booking

```
data/courses.json        all course content: modules, outcomes, audience, session dates
tools/build.py           turns courses.json into the pages below
courses/index.html       catalogue with search and filters   -> /courses
courses/<slug>.html      one page per course                 -> /courses/<slug>
book.html                booking form                        -> /book
sitemap.xml, robots.txt  for Google
```

### Edit a course, add dates or add a new course
1. Edit `data/courses.json` (dates are `YYYY-MM-DD`; `days` sets the session length, weekends are skipped).
2. Run `python3 tools/build.py` from the project root. It also refreshes the six
   "Programmes in demand" cards on the home page (list in `FEATURED` inside `tools/build.py`).
3. Commit the changed files and push.

Do not hand-edit the generated files above; they are overwritten on every build.

### Bookings
- Prices are not shown: fees are quoted after booking, based on organisation type and group size.
- Until a form service is connected, "Send booking request" opens the visitor's email app with the booking
  filled in (to info@riggsafrica.com), shows a reference number, and offers WhatsApp as a backup.
- To receive bookings directly, create a Formspree form and replace `YOUR_FORM_ID` in `tools/build.py`
  (booking form) and in `index.html` (call-back form), then rebuild.

### Run locally
`npx serve .` gives the same clean URLs as Vercel (`/courses`, `/book`).
