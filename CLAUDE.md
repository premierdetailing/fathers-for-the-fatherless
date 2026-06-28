# Fathers For The Fatherless — Claude Code Instructions

You are helping run the public website for **Fathers For The Fatherless (FFTF)**, a
Christian nonprofit. This is a real, live site with real donors reading it. Read this whole
file before making any change. Be accurate, check spelling and links, and never invent
testimonials, statistics, or claims (e.g. tax-deductible status) that have not been
confirmed.

## What this project is
A **static website** — plain HTML, CSS, and JavaScript. There is **no build step**, no
framework, no `npm install`. You edit the files directly and those files *are* the website.

## How this site goes live (important)
The site is hosted on **Vercel**, connected to this GitHub repo
(`premierdetailing/fathers-for-the-fatherless`, private). **Pushing the `main` branch
auto-deploys to production in ~20 seconds.** Live URL:
https://fathers-for-the-fatherless.vercel.app

Two people edit this repo. To stay in sync and avoid conflicts, follow this every time:

1. **Pull first**, before you change anything:
   ```
   git pull
   ```
2. Make the requested edits.
3. **Preview locally** and confirm it looks right (see below).
4. **Publish** — do not ask, just commit and push:
   ```
   git add -A && git commit -m "<short summary of the change>" && git push
   ```
5. Confirm the live URL updated before reporting the work done.

You do NOT need any Vercel login or account to publish — pushing to `main` is all it takes.
The deploy happens automatically on the owner's Vercel.

## How to preview locally
From the repo root:
```
python3 -m http.server 8000
```
Then open http://localhost:8000 and check the page you changed. Stop the server with Ctrl+C.

## File structure
- `index.html` — the home page (long, single-file; most sections live here)
- `about.html`, `mission.html`, `give.html`, `updates.html`, `contact.html` — main pages
- `dental-care.html`, `education.html`, `health-care.html`, `mission-trips.html` — program pages
- `css/styles.css` — global styles
- `css/fftf-pages.css` — styles for the interior pages
- `js/fftf.js` — scripts
- `images/` — logos and graphics used on the site (emblem, full logo, light/dark SVGs)
- `robots.txt`, `sitemap.xml` — keep these consistent with the pages that exist

## Giving / donations
There is **no payment processor connected yet.** The donate flow and the give page
currently direct people to **email** the ministry to give. Do not wire up a fake or
placeholder checkout. When a real Donorbox (or similar) campaign exists, replace the email
fallback with the real embed — and only then.

## Working notes
- Keep the existing visual style and structure unless explicitly asked to change it.
- This is a faith-based ministry site; quotes used on the page are Scripture or clearly
  labeled commitment statements, not fabricated personal testimonials. Keep it that way.
- Small site, two editors — if you ever see a merge conflict, stop and ask the owner rather
  than guessing which version to keep.
