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
