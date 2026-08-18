#!/usr/bin/env python3
"""
Builds redirect stubs for the old Squarespace URLs.

GitHub Pages can't do server-side 301s, so each old path gets a directory with
an index.html that does an instant meta-refresh plus a canonical tag pointing
at the new page. Google treats an instant (0-second) meta refresh as a
permanent redirect, so ranking transfers.

These files do nothing until abc-eikaiwa.com actually points at this repo.
Safe to commit ahead of the switch.

    python3 _tools/redirects.py
"""

import os, io

SITE = "https://abc-eikaiwa.com"

# old Squarespace path -> new target (relative to site root)
#
# Source: Wayback Machine index for abc-eikaiwa.com.
# "/" is intentionally absent - the homepage redirects itself the moment DNS
# points at this repo, and it carries most of the inbound links.
REDIRECTS = {
    # Highest value after the homepage. This was 教室案内 in Google's index.
    # JUDGEMENT CALL: about.html is "Meet the Teachers". If the old page was
    # more fees/schedule/access than people, retarget it at course-books.html
    # or index.html#about.
    "school-information": "about.html",

    # Address, map and phone all live in the homepage contact block now.
    "access":     "index.html#contact",
    "contact-us": "index.html#contact",
    "take-action": "index.html#contact",   # old CTA page - trial booking

    # The old blog. Nothing equivalent on the new site; day-to-day updates
    # moved to Instagram, which is embedded on the homepage.
    "news":                                  "index.html#instagram",
    "news/2014/1/23/get-out-there":          "index.html#instagram",
    "news/challenge-week-3":                 "index.html#instagram",
    "news/nv00pq0r7kabc8en0t2hro3lkan08h":   "index.html#instagram",

    # Stock Squarespace template pages - almost certainly unused, but free.
    "partners": "index.html",
    "projects": "index.html#events",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>移転しました｜ABC英会話</title>
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0; url={rel}">
</head>
<body>
<p>このページは移転しました。自動的に移動します。</p>
<p>This page has moved. <a href="{rel}">Continue to the new page</a>.</p>
<script>window.location.replace("{rel}");</script>
</body>
</html>
"""


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)

    for old, target in sorted(REDIRECTS.items()):
        os.makedirs(old, exist_ok=True)

        # Walk back up to the site root so the stub works whether it's served
        # from an apex domain or a /project-name/ subpath.
        depth = old.count("/") + 1
        rel = "../" * depth + target

        html = TEMPLATE.format(canonical=SITE + "/" + target, rel=rel)
        io.open(os.path.join(old, "index.html"), "w",
                encoding="utf-8", newline="").write(html)
        print("  /%-38s -> %s" % (old, target))

    print("\n%d redirect stubs written." % len(REDIRECTS))
    print("Inert until abc-eikaiwa.com points at this repo.")


if __name__ == "__main__":
    main()
