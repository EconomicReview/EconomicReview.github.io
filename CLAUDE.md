# CLAUDE.md — maintainer's brief for The Economic Review at William & Mary

This file briefs a future Claude Code session (or a patient human) on how
this site works. Read it fully before changing anything. The site is built
so it can be ignored for two years and still work: GitHub Pages' native
Jekyll build, no Node, no npm, no GitHub Actions, no CI.

**Who maintains this:** the Editor-in-Chief of The Economic Review
(2026–27: Cooper Stillick), usually by opening a Claude Code session on
this repo rather than hand-editing.

---

## The iron rule: no placeholders, ever

Nothing on this site is invented. No "coming soon", no sample articles, no
fake authors, no stock photos, no invented statistics, no `href="#"`, no
guessed dates, no ISSN or DOI (the Review has neither — do not fabricate
one). If real content for a module doesn't exist, **the module doesn't
exist**. The empty-state designs are deliberate: with zero publications the
site leads with the call for submissions and neither archive appears in the
nav. Never "fill in" an empty state.

Internal paper IDs (`YYYY-F-##`) are internal — never display them on the
site.

## ⚠️ The auto-population trap (why the schema looks the way it does)

Jekyll silently fabricates three fields on every collection document:

- `title` — titleized from the filename (`missing-everything.md` renders
  as **"Missing Everything"**)
- `date` — parsed from the filename, else the build time
- `excerpt` — **auto-truncated from the body text**

So a Liquid guard like `{% unless page.title %}` NEVER fires, and a
forgotten excerpt silently ships body fragments. Two defenses, both
mandatory:

1. The card field is **`card_excerpt`**, never `excerpt`. Jekyll never
   auto-fills a non-reserved key. The validator rejects any file that uses
   `excerpt:`.
2. **`tools/validate-publications.py` must pass before every commit that
   touches `_publications/`.** It reads the raw front matter, so nothing
   Jekyll fabricates can hide a missing field. Templates also print loud
   red `MISSING <FIELD>` markers for fields Liquid *can* check.

## Adding a publication (the full flow)

1. Create `_publications/YYYY-MM-DD-kebab-slug.md` (date = publication
   date). The URL becomes `/publications/kebab-slug/` — the date prefix is
   stripped. Template:

```yaml
---
title:        "Sentence case, no trailing period"
track:        research            # research | perspectives
date:         2026-11-20
authors:
  - name: "Full Name"
    class_year: 2027              # optional
    # affiliation: "Other University"   # only for non-W&M co-authors
abstract: >-                      # research only; 150–250 words
  ...
card_excerpt: "One or two sentences, written by an editor, shown on cards."
volume:       1                   # research only
issue:        "Spring 2027"       # research only
keywords:     ["", ""]            # optional, 3–5
jel_codes:    ["O15"]             # optional, research only
pdf_url:      ""                  # ScholarWorks URL, or omit
featured:     false               # at most ONE publication may be true
---
Body in Markdown. Required if pdf_url is empty; optional otherwise.
```

2. `python3 tools/validate-publications.py` → must exit 0.
3. Render the OG card:
   `python3 tools/render-og.py _publications/<file>.md`
   then add the printed `image: /assets/og/<slug>.png` line to the front
   matter. (Needs a chromium binary plus `pip install pyyaml pillow`.
   If no chromium is available, skip — the site-wide card
   `/assets/og/default.png` is the fallback.)
4. Commit to `main`. GitHub Pages rebuilds in ~1 minute.

Conventions: `volume` is an integer (Volume 1 = 2026–27, one volume per
academic year). `issue` is `"Fall YYYY"` or `"Spring YYYY"`. Track values
are exactly `research` or `perspectives`. If a research paper's PDF lives
in ScholarWorks, set `pdf_url` and the body becomes optional; the article
page links out and explains the version of record. Citation name inversion
assumes "Given [Middle] Surname" — for suffixes ("Jr.") or multi-word
surnames, expect to correct the citation block by hand (or keep names
simple).

`featured: true` drives the homepage lead. Moving it: remove it from the
old file, add it to the new one, never two at once (validator enforces).

## Where things live

| What | Where | When it changes |
|---|---|---|
| Deadlines & calendar | `_data/dates.yml` | each semester, when the board sets dates |
| Masthead & adviser | `_data/masthead.yml` | every April after elections |
| Contact email, socials, volume, academic year | `_data/journal.yml` | rarely; volume + academic_year roll over each fall |
| Nav (with per-track gating) | `_data/nav.yml` | rarely |
| Track descriptions | `_data/tracks.yml` | rarely |
| All styling | `assets/css/main.css` (plain CSS, no Sass — see below) | as needed |

Dates in `_data/dates.yml` carry a machine `date` (sorting/expiry), a
`datetime` (for `<time>`; month precision like `"2027-04"` is valid for
fuzzy dates), and a `display` string readers see. The "next deadline"
is picked server-side at build AND re-checked in the browser
(`assets/js/main.js`), because GitHub Pages only rebuilds on push — that's
the stale-date protection. Rolling `academic_year`/`current_volume` in
`journal.yml` each fall is manual.

## Config keys you must never remove

`_config.yml` — six keys each fix a verified failure:

1. `url` + 2. `baseurl: ""` — user site at the domain root.
3. `theme: null` — otherwise the github-pages gem injects
   jekyll-theme-primer layouts and a stray stylesheet.
4. `future: true` — GitHub's production builder forces future=true; local
   defaults to false, so future-dated publications would build no HTML
   locally (every listing link 404s) while appearing to work in
   production. This makes the two match.
5. `timezone: America/New_York` — otherwise deadline comparisons run in
   UTC and flip a day early.
6. `repository` — jekyll-github-metadata aborts fresh local builds
   without it.

Also load-bearing: the `exclude:` list (jekyll-optional-front-matter is
always on, so any root-level `.md` NOT excluded — this file included —
would publish as a live page and land in sitemap.xml), the `collections`
block (`permalink: /:collection/:title/` — `:title` strips the filename
date; `:name` would leave it in the URL), and the `defaults` block
(without it, publications render as raw unwrapped HTML).

## Hard constraints of the stack

- **GitHub Pages native build**: Jekyll 3.10, kramdown, Liquid — that's
  it. **Never add npm, GitHub Actions, a CI step, or any plugin that is
  not on GitHub's whitelist** — non-whitelisted plugins are *silently
  ignored* in production; the build won't error, the site will just be
  wrong. Currently enabled (all whitelisted): jekyll-feed, jekyll-seo-tag,
  jekyll-sitemap, jekyll-redirect-from, jekyll-include-cache.
- **No Sass.** The bundled jekyll-sass-converter is ancient. All styling
  is plain CSS in `assets/css/main.css`, which has NO front matter so
  Jekyll copies it byte-identical. Keep it that way.
- **`jekyll-paginate` can't paginate collections** — the archives are
  volume/issue (research) and year (perspectives) groupings on single
  pages, on purpose. Don't add pagination.
- JavaScript is progressive enhancement only (theme toggle, deadline
  freshness, copy buttons). Everything must work with JS disabled. Keep
  `main.js` dependency-free and under 5 KB.
- Fonts are self-hosted woff2 in `assets/fonts/` (Newsreader variable
  roman+italic, Inter variable, IBM Plex Mono 400/500 — all subset to
  Latin). There is no network at deploy time; never switch to a CDN or
  the Google Fonts CSS API (it also serves static instances that break
  optical sizing).
- `/feed.xml` in the repo root is a hand-written publications feed that
  EXISTS TO BLOCK jekyll-feed's default (a posts feed that would be valid
  but permanently empty — this site has no `_posts`). The configured
  collection feed is `/feed/publications.xml`. Don't delete either.
- `robots.txt` is committed by hand because jekyll-sitemap's generated one
  has no `User-agent` line.
- Never create a `.nojekyll` file. Never add a `CNAME` file until there's
  a real custom domain (see below).

## Color contrast ledger

Every pair below was computed (WCAG 2.1), not eyeballed. Re-verify with a
calculator before changing ANY color, especially gold.

| Pair | Ratio |
|---|---|
| `#14181A` ink on `#FBFAF7` paper | 17.12:1 |
| `#5A6165` muted on paper | 6.04:1 |
| `#004E38` green text/links on paper | 9.37:1 |
| `#846838` gold-text on paper | 5.01:1 |
| `#FBFAF7` on `#004E38` (featured block, research cover) | 9.37:1 |
| `#14181A` on `#B79257` (perspectives cover) | 6.18:1 |
| dark theme: `#EDEAE3` on `#0E1211` | 15.70:1 |
| dark: `#9BA3A0` muted | 7.31:1 |
| dark: `#76A190` patina links | 6.53:1 |
| dark: `#B79257` gold text | 6.52:1 |

⚠️ **Raw W&M Gold `#B79257` on light paper is 2.77:1 — it FAILS at every
size.** On light backgrounds gold is decorative only (rules, fills); any
gold *text* on light uses `--gold-text` `#846838`, W&M's own ADA web hex.
Gold-on-green is 3.38:1 — large/UI/decorative only. Covers use fixed
colors in both themes so "a cover never changes."

## Layout testing without fake articles

Never write plausible fake articles into `_publications/` to test layouts.
Use the fixtures overlay:

```
mkdir -p fixtures-workbench/_publications
# generate obviously-synthetic entries (FIXTURE-DO-NOT-SHIP titles,
# FIXTURE AUTHOR names) there, then:
bundle exec jekyll build --config _config.yml,_config.fixtures.yml
# output lands in _site-fixtures/ ; both dirs are git-ignored.
rm -rf fixtures-workbench _site-fixtures   # ALWAYS delete before commit
```

Check `git status` afterwards. The placeholder scan
(`grep -riE 'lorem|placeholder|coming soon|\bTBD\b|FIXTURE' _site/`)
must stay clean on the real build.

## Local preview

```
bundle install          # once; needs Ruby ~3.x
bundle exec jekyll serve
```
Expect exactly one warning — `GitHub Metadata: No GitHub API
authentication` — it's harmless. Zero warnings is not achievable on this
stack.

## Deploying / hosting

The production target is a **public** repo named exactly
`EconomicReview.github.io` (user site → serves at
https://economicreview.github.io with `baseurl: ""`). Settings → Pages →
Deploy from a branch → `main` / root. As of August 2026 the site was built
in the `economic-review-at-william-and-mary` repo and still needs to be
pushed to `EconomicReview.github.io` to go live.

**Custom domain, later:** when the Review buys a domain, add a `CNAME`
file containing just the bare domain, set the DNS (CNAME record →
`economicreview.github.io`), update `url:` in `_config.yml`, and update
the `Sitemap:` line in `robots.txt`. Until then, no CNAME file.

## OG images

GitHub Pages cannot rasterize at deploy time, so 1200×630 OG PNGs are
pre-rendered and committed to `assets/og/`. `default.png` is the site-wide
card; per-article cards come from `tools/render-og.py` (see the add-a-
publication flow). Headless-chromium quirk the script already handles: the
window reserves ~100px of UI height, so it renders tall and crops.

## Gotchas found the hard way

- Liquid here drops a conditional body that is ONLY whitespace
  (`{% unless x %} {% endunless %}` renders nothing) — joiner spaces in
  the citation builder use `&#32;` for this reason.
- Front matter is not Liquid-processed: you can't write
  `{{ site.data... }}` in a page's front matter (see `kicker_academic_year`
  in `_layouts/page.html`).
- An include file's trailing newline becomes output — includes that sit
  against punctuation (`next-deadline.html`) must not end with a newline.
- Headless-chromium screenshots below ~500px window width silently render
  at a larger size and crop — use Playwright with a real viewport for
  mobile screenshots.
