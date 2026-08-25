# The Economic Review at William & Mary — website

The public site of The Economic Review, the undergraduate economics
journal of William & Mary. Live at **https://economicreview.github.io**
(deployed from the `EconomicReview.github.io` repo via GitHub Pages'
native Jekyll build — no Node, no Actions, no CI).

- **Publish an article:** see `ADD-A-PUBLICATION.md` (60-second browser
  flow).
- **Everything else** (schema, config constraints, design tokens, testing):
  see `CLAUDE.md`.

## Preview locally

```
bundle install
bundle exec jekyll serve      # → http://localhost:4000
```

Requires Ruby 3.x. One `GitHub Metadata` warning during build is normal.
Before committing publication changes, run
`python3 tools/validate-publications.py`.
