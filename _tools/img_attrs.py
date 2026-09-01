#!/usr/bin/env python3
"""
Adds the three attributes every <img> on this site should carry, and nothing else.

    loading="lazy"    Below-the-fold images stop competing with the ones the
                      visitor can actually see. The first two images after
                      <body> -- the nav logo and whatever sits in the hero --
                      are deliberately left eager, because lazy-loading the
                      image that paints first makes the page measurably slower,
                      not faster.
    decoding="async"  Lets the browser decode off the main thread.
    width / height    Taken from the file itself. The browser can then reserve
                      the right space before the image arrives, so text stops
                      jumping down the page as photos load. That jump is
                      Cumulative Layout Shift, one of the three Core Web Vitals
                      Google measures.

Attributes already present are never overwritten, so this is safe to re-run
after adding new images. Images with a dynamic or missing src (the lightbox,
gallery slots filled in by script) are skipped -- there's no file to measure.

    python3 _tools/img_attrs.py --dry-run
    python3 _tools/img_attrs.py
"""

import os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "node_modules", "_tools"}

IMG = re.compile(r"<img\b[^>]*>", re.I)
COMMENT = re.compile(r"<!--.*?-->", re.S)
SRC = re.compile(r"""\bsrc\s*=\s*["']([^"']*)["']""", re.I)

EAGER_COUNT = 2          # nav logo + hero image stay eager


def comment_spans(text):
    return [(m.start(), m.end()) for m in COMMENT.finditer(text)]


def in_comment(pos, spans):
    return any(a <= pos < b for a, b in spans)


def dims(path):
    try:
        with Image.open(path) as im:
            return im.width, im.height
    except Exception:
        return None


def process(path, dry=False):
    text = open(path, encoding="utf-8", errors="ignore").read()
    spans = comment_spans(text)
    body = text.lower().find("<body")
    if body == -1:
        body = 0

    out = []
    last = 0
    seen = 0
    added = {"lazy": 0, "decoding": 0, "dims": 0}

    for m in IMG.finditer(text):
        if m.start() < body or in_comment(m.start(), spans):
            continue
        tag = m.group(0)
        seen += 1

        s = SRC.search(tag)
        src = s.group(1).strip() if s else ""
        if not src or src.startswith(("http", "//", "data:", "${", "{")):
            continue

        new = tag
        low = new.lower()

        if "loading=" not in low and seen > EAGER_COUNT:
            new = new[:-1].rstrip() + ' loading="lazy">'
            added["lazy"] += 1
            low = new.lower()

        if "decoding=" not in low:
            new = new[:-1].rstrip() + ' decoding="async">'
            added["decoding"] += 1
            low = new.lower()

        if "width=" not in low and "height=" not in low:
            local = os.path.normpath(
                os.path.join(
                    ROOT if src.startswith("/") else os.path.dirname(path),
                    src.lstrip("/").split("?")[0],
                )
            )
            d = dims(local) if os.path.isfile(local) else None
            if d:
                new = new[:-1].rstrip() + f' width="{d[0]}" height="{d[1]}">'
                added["dims"] += 1

        if new != tag:
            out.append(text[last:m.start()])
            out.append(new)
            last = m.end()

    if last == 0:
        return None
    out.append(text[last:])
    result = "".join(out)

    if not dry:
        open(path, "w", encoding="utf-8", newline="\n").write(result)
    return added


def main():
    dry = "--dry-run" in sys.argv
    total = {"lazy": 0, "decoding": 0, "dims": 0}
    files = 0
    for dirpath, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in sorted(names):
            if not n.endswith(".html"):
                continue
            p = os.path.join(dirpath, n)
            r = process(p, dry)
            if not r:
                continue
            files += 1
            for k in total:
                total[k] += r[k]
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            print(f"  {rel}: +{r['lazy']} lazy, +{r['decoding']} decoding, +{r['dims']} dims")
    print(f"\n{'DRY RUN -- nothing written' if dry else 'Done'} -- {files} pages")
    print(f"  loading=lazy    +{total['lazy']}")
    print(f"  decoding=async  +{total['decoding']}")
    print(f"  width/height    +{total['dims']}")


if __name__ == "__main__":
    main()
