#!/usr/bin/env python3
"""
Shrinks oversized images in place, keeping every filename and format exactly
as it is. No page needs editing and no reference can break.

Why this exists: most photos here came straight off a phone at 4032x3024 and
2-4 MB each. Nothing on the site displays an image wider than about 1200 CSS
pixels, so every one of those bytes was downloaded and thrown away. The
homepage alone was pulling roughly 9 MB. Mobile page speed is a ranking
signal, and a parent on a phone leaves before a 9 MB page paints.

What it does, per format:

    JPEG   EXIF rotation baked in, resized to MAX_EDGE, re-saved progressive
           at QUALITY. Metadata dropped.
    PNG    Photographs saved as PNG (screenshots, video stills) are resized
           and reduced to a 256-colour palette. Graphics with real
           transparency keep their alpha and get the same palette treatment.
    WEBP   Only the unusually large ones; these were already reasonable.

Files already inside their budget are left untouched, so re-running is cheap
and safe. Originals stay recoverable from git history:

    git checkout HEAD~1 -- images/photo5.jpeg

Usage:
    python3 _tools/optimize_images.py --dry-run          # report only
    python3 _tools/optimize_images.py images tokyo-trip  # specific folders
    python3 _tools/optimize_images.py                    # every folder below
"""

import os, sys, shutil, tempfile
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FOLDERS = ["images", "tokyo-trip", "halloween", "summer-camp", "summer-2026"]

# Longest edge, in pixels, that any of these ever needs to be. The largest
# on-screen use is the full-screen lightbox.
MAX_EDGE = 1600
JPEG_QUALITY = 78

# Calendars are photographs of a printed month grid -- the text has to stay
# readable when a parent zooms in, so they keep more pixels and less
# compression than a snapshot of a classroom does.
CALENDAR_MAX_EDGE = 2200
CALENDAR_QUALITY = 88

PNG_MAX_EDGE = 1400          # PNGs here are screenshots and cover art
WEBP_MAX_EDGE = 1600
WEBP_QUALITY = 80

# Below this, a file is already small enough that re-encoding it risks more
# quality than it saves bytes.
SKIP_UNDER = 120_000
WEBP_SKIP_UNDER = 400_000    # the .webp files were already sensibly sized

# Never touch these: logos and UI marks, where palette reduction shows.
KEEP = {"abc-logo.png", "logo.png", "book.png", "bridge-bg.png"}


def is_calendar(path):
    return "calendar" in os.path.basename(path).lower()


def fit(im, max_edge):
    if max(im.size) <= max_edge:
        return im
    r = max_edge / max(im.size)
    return im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)


def has_alpha(im):
    if im.mode not in ("RGBA", "LA", "P"):
        return False
    im = im.convert("RGBA")
    return im.getchannel("A").getextrema()[0] < 255


def rewrite(path, dry_run=False):
    """Returns (before, after) bytes, or None if the file was left alone."""
    name = os.path.basename(path)
    ext = os.path.splitext(name)[1].lower()
    before = os.path.getsize(path)

    if name in KEEP:
        return None
    if ext == ".webp" and before < WEBP_SKIP_UNDER:
        return None
    if ext != ".webp" and before < SKIP_UNDER:
        return None

    try:
        im = ImageOps.exif_transpose(Image.open(path))
    except Exception as e:
        print(f"  ! unreadable, skipped: {path} ({e})")
        return None

    fd, tmp = tempfile.mkstemp(suffix=ext, dir=os.path.dirname(path))
    os.close(fd)
    try:
        if ext in (".jpg", ".jpeg"):
            edge = CALENDAR_MAX_EDGE if is_calendar(path) else MAX_EDGE
            q = CALENDAR_QUALITY if is_calendar(path) else JPEG_QUALITY
            fit(im.convert("RGB"), edge).save(
                tmp, "JPEG", quality=q, optimize=True, progressive=True
            )
        elif ext == ".png":
            small = fit(im, PNG_MAX_EDGE)
            if has_alpha(im):
                # FASTOCTREE is the one Pillow method that keeps alpha.
                small.convert("RGBA").quantize(
                    colors=256, method=Image.FASTOCTREE
                ).save(tmp, "PNG", optimize=True)
            else:
                small.convert("RGB").quantize(
                    colors=256, method=Image.MEDIANCUT,
                    dither=Image.FLOYDSTEINBERG,
                ).save(tmp, "PNG", optimize=True)
        elif ext == ".webp":
            fit(im, WEBP_MAX_EDGE).save(
                tmp, "WEBP", quality=WEBP_QUALITY, method=6
            )
        else:
            os.remove(tmp)
            return None

        after = os.path.getsize(tmp)
        # Never make a file bigger. If the re-encode didn't help, keep the
        # original -- some of these were already well optimised.
        if after >= before * 0.95:
            os.remove(tmp)
            return None
        if dry_run:
            os.remove(tmp)
        else:
            shutil.move(tmp, path)
        return before, after
    except Exception as e:
        if os.path.exists(tmp):
            os.remove(tmp)
        print(f"  ! failed, left as is: {path} ({e})")
        return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    dry = "--dry-run" in sys.argv
    folders = args or FOLDERS

    total_before = total_after = 0
    changed = skipped = 0

    for folder in folders:
        d = os.path.join(ROOT, folder)
        if not os.path.isdir(d):
            print(f"no such folder: {folder}")
            continue
        print(f"\n{folder}/")
        for dirpath, _, files in os.walk(d):
            for f in sorted(files):
                if not f.lower().endswith(
                    (".jpg", ".jpeg", ".png", ".webp")
                ):
                    continue
                p = os.path.join(dirpath, f)
                r = rewrite(p, dry)
                if r is None:
                    skipped += 1
                    continue
                b, a = r
                changed += 1
                total_before += b
                total_after += a
                rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
                print(f"  {b/1e6:6.2f} -> {a/1e6:5.2f} MB  {rel}")

    print(f"\n{'DRY RUN -- nothing written' if dry else 'Done'}")
    print(f"  rewritten : {changed}")
    print(f"  untouched : {skipped}")
    if total_before:
        print(
            f"  {total_before/1e6:.1f} MB -> {total_after/1e6:.1f} MB "
            f"({100 - 100*total_after/total_before:.0f}% smaller)"
        )


if __name__ == "__main__":
    main()
