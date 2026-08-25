#!/usr/bin/env python3
"""Validate the front matter of every file in _publications/.

Jekyll will NOT catch these problems — it silently invents a title from the
filename, a date from the filename or build time, and an excerpt from the
body (see CLAUDE.md, "The auto-population trap"). This script reads the RAW
front matter, so nothing Jekyll fabricates can hide a missing field.

Run it before every commit that touches _publications/:

    python3 tools/validate-publications.py            # full check
    python3 tools/validate-publications.py --offline  # skip pdf_url HTTP checks

Exits 0 when everything passes; 1 when anything fails. Warnings don't fail
the run but should be read.
"""

import re
import sys
import urllib.request
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(
        "PyYAML is required: python3 -m pip install pyyaml\n"
        "(The site builds without it; only this validator needs it.)"
    )

ROOT = Path(__file__).resolve().parent.parent
PUB_DIR = ROOT / "_publications"

REQUIRED = ["title", "track", "date", "authors", "card_excerpt"]
TRACKS = {"research", "perspectives"}
RESEARCH_REQUIRED = ["volume", "issue", "abstract"]
FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*\.md$")

errors: list[str] = []
warnings: list[str] = []


def err(f: Path, msg: str) -> None:
    errors.append(f"{f.name}: {msg}")


def warn(f: Path, msg: str) -> None:
    warnings.append(f"{f.name}: {msg}")


def split_front_matter(text: str):
    """Return (front_matter_str, body_str) or (None, None)."""
    if not text.startswith("---"):
        return None, None
    parts = text.split("\n---", 2)
    if len(parts) < 2:
        return None, None
    fm = parts[0].lstrip("-\n")
    # find the closing delimiter properly
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def url_resolves(url: str) -> bool:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "wmer-validator"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status < 400
    except Exception:
        # Some hosts refuse HEAD; retry with GET before failing.
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "wmer-validator"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.status < 400
        except Exception:
            return False


def main() -> int:
    offline = "--offline" in sys.argv

    if not PUB_DIR.is_dir():
        print("OK: _publications/ does not exist yet (no publications).")
        return 0

    files = sorted(p for p in PUB_DIR.glob("*.md"))
    featured_files = []

    for f in files:
        if not FILENAME_RE.match(f.name):
            err(f, "filename must be YYYY-MM-DD-kebab-slug.md")

        fm_text, body = split_front_matter(f.read_text(encoding="utf-8"))
        if fm_text is None:
            err(f, "no YAML front matter found (file must start with ---)")
            continue
        try:
            fm = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError as e:
            err(f, f"front matter is not valid YAML: {e}")
            continue

        # The reserved-key trap: `excerpt` is auto-populated by Jekyll, so a
        # guard on it never fires. The schema uses card_excerpt instead.
        if "excerpt" in fm:
            err(f, "uses `excerpt:` — forbidden. Use `card_excerpt:` "
                   "(Jekyll auto-fills `excerpt` from the body, which defeats "
                   "every missing-field guard)")

        for key in REQUIRED:
            if key not in fm or fm[key] in (None, "", []):
                err(f, f"missing required field `{key}`")

        track = fm.get("track")
        if track is not None and track not in TRACKS:
            err(f, f"unknown track `{track}` (must be research or perspectives)")

        if track == "research":
            for key in RESEARCH_REQUIRED:
                if key not in fm or fm[key] in (None, "", []):
                    err(f, f"research publication missing `{key}`")
            abstract = fm.get("abstract")
            if isinstance(abstract, str):
                n = len(abstract.split())
                if not 150 <= n <= 250:
                    warn(f, f"abstract is {n} words (house style is 150–250)")

        # date sanity: must be a real date matching the filename prefix
        d = fm.get("date")
        if isinstance(d, datetime):
            d = d.date()
        if d is not None and not isinstance(d, date):
            try:
                d = datetime.strptime(str(d)[:10], "%Y-%m-%d").date()
            except ValueError:
                err(f, f"date `{fm.get('date')}` is not a valid YYYY-MM-DD date")
                d = None
        if isinstance(d, date):
            prefix = f.name[:10]
            if d.isoformat() != prefix:
                warn(f, f"date {d.isoformat()} differs from filename prefix "
                        f"{prefix} — the URL slug and sort order come from the "
                        f"front matter date; keep them in sync")

        authors = fm.get("authors")
        if isinstance(authors, list):
            for i, a in enumerate(authors, 1):
                if not isinstance(a, dict) or not a.get("name"):
                    err(f, f"author #{i} has no `name`")
        elif authors is not None:
            err(f, "`authors` must be a list of {name: ...} entries")

        if fm.get("featured") is True:
            featured_files.append(f.name)

        pdf_url = fm.get("pdf_url")
        if pdf_url:
            if pdf_url.startswith("/"):
                local = ROOT / pdf_url.lstrip("/")
                if not local.exists():
                    err(f, f"pdf_url `{pdf_url}` does not exist in the repo")
            elif pdf_url.startswith("http"):
                if offline:
                    warn(f, f"pdf_url not checked (--offline): {pdf_url}")
                elif not url_resolves(pdf_url):
                    err(f, f"pdf_url does not resolve: {pdf_url}")
            else:
                err(f, f"pdf_url `{pdf_url}` must be an absolute URL or a "
                       f"site-root path starting with /")
        else:
            if not (body or "").strip():
                err(f, "has neither body text nor pdf_url — one is required")

    if len(featured_files) > 1:
        errors.append(
            "more than one publication has featured: true "
            f"({', '.join(featured_files)}) — at most one at a time"
        )

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\nChecked {len(files)} publication(s): "
          f"{len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
