#!/usr/bin/env python3
"""Render a 1200×630 Open Graph card for one publication.

GitHub Pages cannot rasterize anything at deploy time (no network, no Node),
so OG images are pre-rendered in the authoring session and committed.

Usage:
    python3 tools/render-og.py _publications/2026-11-20-example-slug.md

Writes assets/og/<slug>.png (slug = filename minus the date prefix) and
prints the front-matter line to add. Requires a Chromium/Chrome binary —
pass --chromium /path/to/chrome if it isn't found automatically — and the
committed fonts in assets/fonts/.
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: python3 -m pip install pyyaml")

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python3 -m pip install pillow")

ROOT = Path(__file__).resolve().parent.parent

CHROMIUM_CANDIDATES = [
    "chromium", "chromium-browser", "google-chrome", "chrome",
    "/opt/pw-browsers/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

TRACK_COLORS = {
    # field background, text color — same pairs as the site's cover tokens,
    # both verified ≥4.5:1 (see CLAUDE.md contrast ledger)
    "research": ("#004E38", "#FBFAF7"),
    "perspectives": ("#B79257", "#14181A"),
}

HTML = """<!doctype html><meta charset="utf-8">
<style>
@font-face{{font-family:Newsreader;src:url("file://{fonts}/newsreader-var.woff2") format("woff2");font-weight:200 800}}
@font-face{{font-family:Inter;src:url("file://{fonts}/inter-var.woff2") format("woff2");font-weight:100 900}}
@font-face{{font-family:"IBM Plex Mono";src:url("file://{fonts}/plexmono-medium.woff2") format("woff2");font-weight:500}}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{background:{bg};color:{fg};position:relative;box-sizing:border-box}}
.top{{position:absolute;left:72px;right:72px;top:60px;max-height:380px;overflow:hidden}}
.kicker{{font:500 22px "IBM Plex Mono",monospace;text-transform:uppercase;letter-spacing:.12em;opacity:.85;margin:0}}
h1{{font-family:Newsreader,serif;font-optical-sizing:auto;font-weight:500;
  font-size:{title_size}px;line-height:1.12;margin:24px 0 0;max-width:1020px}}
.byline{{font:450 26px/1.35 Inter,sans-serif;opacity:.92;max-width:700px}}
.foot{{position:absolute;left:72px;right:72px;top:488px;display:flex;
  justify-content:space-between;align-items:flex-start;gap:40px}}
.journal{{font:600 24px/1.3 Inter,sans-serif;letter-spacing:.01em;text-align:right;flex:none}}
</style><body>
<div class="top"><p class="kicker">{kicker}</p><h1>{title}</h1></div>
<div class="foot"><span class="byline">{byline}</span>
<span class="journal">The Economic Review<br>at William &amp; Mary</span></div>
</body>"""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pub", help="path to a _publications/*.md file")
    ap.add_argument("--chromium", help="path to a chromium/chrome binary")
    args = ap.parse_args()

    pub = Path(args.pub)
    if not pub.exists():
        sys.exit(f"not found: {pub}")

    m = re.match(r"^---\s*\n(.*?)\n---", pub.read_text(encoding="utf-8"), re.DOTALL)
    if not m:
        sys.exit("no front matter found")
    fm = yaml.safe_load(m.group(1))

    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", pub.stem)
    track = fm.get("track", "research")
    bg, fg = TRACK_COLORS.get(track, TRACK_COLORS["research"])

    if track == "research" and fm.get("volume"):
        kicker = f"WMER · Vol. {fm['volume']}"
        if fm.get("issue"):
            kicker += f" · {fm['issue']}"
    else:
        kicker = f"WMER · {track.capitalize()}"

    authors = fm.get("authors") or []
    names = [a.get("name", "") for a in authors if isinstance(a, dict)]
    byline = ", ".join(n for n in names if n)

    title = fm.get("title", "")
    title_size = 72 if len(title) <= 60 else (58 if len(title) <= 110 else 46)

    chromium = args.chromium or next(
        (c for c in CHROMIUM_CANDIDATES if shutil.which(c) or Path(c).exists()), None)
    if not chromium:
        sys.exit("no chromium/chrome binary found — pass --chromium PATH")

    out = ROOT / "assets" / "og" / f"{slug}.png"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(HTML.format(fonts=ROOT / "assets" / "fonts", bg=bg, fg=fg,
                            kicker=esc(kicker), title=esc(title),
                            byline=esc(byline), title_size=title_size))
        tmp = f.name

    # Headless chromium reserves ~100px of the window for UI, so a
    # window-size=1200,630 screenshot silently clips the card's bottom.
    # Render tall, then crop to exactly 1200×630.
    subprocess.run(
        [chromium, "--headless", "--no-sandbox", "--disable-gpu",
         f"--screenshot={out}", "--window-size=1200,830", f"file://{tmp}"],
        check=True, capture_output=True)
    Image.open(out).convert("RGB").crop((0, 0, 1200, 630)).save(out)
    print(f"wrote {out.relative_to(ROOT)}")
    print(f"now add to the front matter of {pub.name}:")
    print(f"  image: /assets/og/{slug}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
