#!/usr/bin/env python3
"""
Fails if any page references a local asset that GitHub Pages can't serve.

Windows treats "photo1.JPG" and "photo1.jpg" as the same file. GitHub Pages
does not. That mismatch is invisible locally and shows up as a broken image
on the live site, so this check compares every reference against the exact
filenames git has recorded -- not against the local filesystem, which would
happily report a match on Windows.

Two failure kinds:
    CASE     the file exists, but the reference spells it differently
    MISSING  no file by that name at any casing

References inside HTML comments are ignored, so commented-out templates and
"here's how to add one" examples don't fail the build.

    python3 _tools/check_assets.py

Exits 0 when clean, 1 on any problem. Run by .github/workflows/check-assets.yml
on every push and pull request.
"""

import io, os, re, subprocess, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSET_EXT = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".avif",
    ".ico", ".mp4", ".webm", ".mov", ".pdf",
)

# Intentional gaps: referenced on purpose, with an onerror placeholder in the
# page, until the real file exists. Delete an entry once you commit the file.
ALLOW_MISSING = {
    "images/kyoko.jpg",   # About page -- falls back to "Photo coming soon"
}

# src="...", href="...", poster="...", content="..."  or  url(...)
REF = re.compile(
    r"""(?:src|href|poster|content)\s*=\s*["']([^"']+)["']"""
    r"""|url\(\s*["']?([^"')]+)["']?\s*\)""",
    re.I,
)
COMMENT = re.compile(r"<!--.*?-->", re.S)
SCRIPT = re.compile(r"<script\b.*?</script>", re.S | re.I)


def tracked_files():
    """Exact filenames as git records them -- what Pages actually serves."""
    try:
        out = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.exit("check_assets: not a git checkout, or git is unavailable.")
    return {p.strip() for p in out.splitlines() if p.strip()}


def main():
    tracked = tracked_files()
    lower = {p.lower(): p for p in tracked}
    pages = sorted(p for p in tracked if p.endswith(".html"))

    problems = []
    allowed = []
    checked = 0

    for page in pages:
        raw = io.open(
            os.path.join(ROOT, page), encoding="utf-8", errors="surrogateescape"
        ).read()
        # Strip comments and inline JS: neither ships a real asset reference.
        text = SCRIPT.sub("", COMMENT.sub("", raw))
        page_dir = os.path.dirname(page)

        for match in REF.finditer(text):
            ref = (match.group(1) or match.group(2) or "").strip()
            if not ref or ref.startswith(
                ("http", "//", "data:", "mailto:", "tel:", "#", "javascript:")
            ):
                continue
            if not ref.lower().endswith(ASSET_EXT):
                continue

            clean = urllib.parse.unquote(ref.split("?")[0].split("#")[0])
            base = "" if clean.startswith("/") else page_dir
            target = os.path.normpath(
                os.path.join(base, clean.lstrip("/"))
            ).replace(os.sep, "/")
            checked += 1

            if target in tracked:
                continue
            actual = lower.get(target.lower())
            if actual:
                problems.append(("CASE", page, ref, actual))
            elif target not in ALLOW_MISSING:
                problems.append(("MISSING", page, ref, None))
            else:
                allowed.append((page, target))

    for page, target in allowed:
        print(f"check_assets: allowed gap -- {target} (referenced by {page})")

    if not problems:
        print(f"check_assets: OK -- {checked} references across {len(pages)} pages.")
        return 0

    print(f"check_assets: {len(problems)} broken reference(s).\n")
    for kind, page, ref, actual in problems:
        if kind == "CASE":
            print(f"  CASE     {page}")
            print(f"           references  {ref}")
            print(f"           actual file {actual}")
        else:
            print(f"  MISSING  {page}")
            print(f"           references  {ref}  (no such file, any casing)")
    print(
        "\nThese resolve on Windows but 404 on GitHub Pages. Fix the reference to "
        "match the committed filename exactly, or commit the missing file."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
