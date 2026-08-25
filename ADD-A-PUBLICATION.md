# How to publish an article (about 60 seconds)

You don't need to install anything or know Jekyll. You need write access to
this repository on GitHub — everything below works in the browser.

## 1. Create the file

On GitHub: **Add file → Create new file**, inside the `_publications`
folder. Name it with the publication date and a short slug:

```
_publications/2027-02-10-minimum-wage-virginia.md
```

The article's address becomes
`economicreview.github.io/publications/minimum-wage-virginia/` (the date
is stripped from the URL automatically).

## 2. Paste and fill this in

Complete worked example — replace every value with the real ones:

```yaml
---
title: "Minimum wage increases and teen employment in Virginia"
track: research
date: 2027-02-10
authors:
  - name: "Nicole Zajac"
    class_year: 2028
abstract: >-
  The full 150–250 word abstract the author submitted, pasted here as one
  block. It appears on the article page and in search results.
card_excerpt: "A one- or two-sentence editor-written summary. This is what shows on the homepage and archive cards."
volume: 1
issue: "Spring 2027"
keywords: ["minimum wage", "employment", "Virginia"]
jel_codes: ["J38"]
pdf_url: ""
featured: true
---

The full text of the article goes here, in Markdown. Paragraphs are blank-
line separated; `## Headings` make sections.
```

Rules that matter:

- `track:` is `research` or `perspectives` — nothing else.
- For a **Perspective**, delete the `abstract`, `volume`, `issue`, and
  `jel_codes` lines entirely.
- `card_excerpt` is required and is written by an editor — it is NOT the
  abstract.
- If the paper's PDF is in ScholarWorks, put that link in `pdf_url:` —
  then the body text is optional.
- `featured: true` puts the piece at the top of the homepage. Only one
  publication may have it: remove it from the previous one first.
- The field is called `card_excerpt`, never `excerpt` — `excerpt` breaks
  the site's safety checks.

## 3. Commit

Scroll down, write a short commit message ("Publish: minimum wage paper"),
and commit to the `main` branch. The live site rebuilds itself in about a
minute. That's it.

## If something looks wrong on the live site

A missing required field shows up as a red **MISSING …** marker on the
page — fix the front matter and commit again. If you have a computer with
Python handy, `python3 tools/validate-publications.py` checks every file
and tells you exactly what's missing before you commit. The full
maintainer's reference (including how to generate the social-media preview
image for an article) is in `CLAUDE.md`.
