#!/usr/bin/env python3
"""
Regenerates the SEO <head> block on every page.

Safe to run repeatedly: it strips the previous MANAGED-SEO block before
writing a new one, so it never stacks up duplicate tags.

AT LAUNCH: change SITE to "https://abc-eikaiwa.com", set IS_APEX = True,
re-run, and commit. Nothing else needs to change.

    python3 _tools/seo.py
"""

import re, os, io, json, glob

# ---------------------------------------------------------------- config
# Live on the apex domain as of 2026-08-18.
# (Pre-launch value was "https://yoshi80085.github.io/bridgeway-abc")
SITE = "https://abc-eikaiwa.com"

# True once the site is served from the apex domain. Controls whether the
# sitemap and canonicals use a bare root path.
IS_APEX = True

OG_IMAGE = SITE + "/images/main2.jpg"

# ---------------------------------------------------------------- content
# filename -> (title, meta description)
PUBLIC = {
 "index.html": (
  "山形市の子ども英会話教室 ABC英会話｜幼児〜高校生・無料体験受付中",
  "山形市元木の英会話教室ABC英会話（Bridgeway ABC English School）。1998年開校、幼児から高校生・大人まで年間42回の少人数レッスン。ハロウィンやサマーキャンプなど楽しいイベントも充実。無料体験レッスン受付中／023-641-3059"),
 "about.html": (
  "講師紹介｜山形市の子ども英会話教室 ABC英会話",
  "ABC英会話（山形市元木）の講師をご紹介します。ネイティブ講師と日本人スタッフが、幼児から高校生まで一人ひとりに合わせて指導します。無料体験レッスン受付中。"),
 "course-books.html": (
  "コース・教材のご案内｜山形市の子ども英会話 ABC英会話",
  "ABC英会話（山形市）のコースと教材のご案内。Little Hands、Hand in Hand、English Firsthandなど、年齢と英語力に合わせたステップアップ式カリキュラムをご紹介します。"),
 "little-hands.html": (
  "Little Hands 幼児クラス｜山形市の子ども英会話 ABC英会話",
  "山形市の英会話教室ABC英会話の幼児クラス「Little Hands」。歌・絵本・遊びを通して、英語を楽しい体験として身につける未就学児向けレッスンです。無料体験受付中。"),
 "hih-starter.html": (
  "Hand in Hand Starter 小学生クラス｜山形市 ABC英会話",
  "ABC英会話（山形市）の小学生向けクラス「Hand in Hand Starter」。英語を初めて学ぶお子様が、フォニックスと基本表現から無理なくスタートできるコースです。"),
 "hih-1.html": (
  "Hand in Hand 1 小学生クラス｜山形市の子ども英会話 ABC英会話",
  "ABC英会話（山形市）の小学生クラス「Hand in Hand 1」。読み書きの基礎とやさしい会話表現を、少人数のレッスンで着実に積み上げていきます。"),
 "hih-2.html": (
  "Hand in Hand 2 小学生クラス｜山形市の子ども英会話 ABC英会話",
  "ABC英会話（山形市）の小学生クラス「Hand in Hand 2」。基本文型と語彙を広げ、自分のことを英語で伝えられる力を育てます。"),
 "hih-3.html": (
  "Hand in Hand 3 小学生クラス｜山形市の子ども英会話 ABC英会話",
  "ABC英会話（山形市）の小学生クラス「Hand in Hand 3」。時制や疑問文を使いこなし、まとまった会話ができる段階を目指します。"),
 "hih-4.html": (
  "Hand in Hand 4 小学生クラス｜山形市の子ども英会話 ABC英会話",
  "ABC英会話（山形市）の小学生クラス「Hand in Hand 4」。読解と作文にも取り組み、中学英語へ自然につながる土台をつくります。"),
 "hih-5.html": (
  "Hand in Hand 5 小学生クラス｜山形市の子ども英会話 ABC英会話",
  "ABC英会話（山形市）の小学生クラス「Hand in Hand 5」。長めの文章を読み、自分の考えを英語で表現する力を伸ばします。"),
 "hih-6.html": (
  "Hand in Hand 6 小学生クラス｜山形市の子ども英会話 ABC英会話",
  "ABC英会話（山形市）の小学生クラス「Hand in Hand 6」。小学生コースの仕上げとして、中学英語にスムーズに接続する総合力を養います。"),
 "first-hand.html": (
  "English Firsthand 中高生・大人クラス｜山形市 ABC英会話",
  "ABC英会話（山形市）の中学生・高校生・大人向けクラス「English Firsthand」。実際に使える会話力と、試験にも通用する確かな英語力を養います。"),
 "halloween.html": (
  "ハロウィンパーティー｜山形市の子ども英会話 ABC英会話",
  "ABC英会話（山形市）の毎年恒例ハロウィンパーティー。仮装してゲームやトリック・オア・トリートを楽しみながら、英語を本物の言葉として体験できる人気イベントです。"),
 "summer-camp.html": (
  "イングリッシュサマーキャンプ｜山形市 ABC英会話",
  "ABC英会話（山形市）のイングリッシュサマーキャンプ。英語だけで過ごすキャンプで、教室では味わえない自信と度胸が身につきます。過去の様子を写真でご紹介。"),
 # Directory-index page: keeps the original Squarespace URL
 # https://abc-eikaiwa.com/school-information , which is still in Google's
 # index and was the highest-value old URL after the homepage.
 "school-information/index.html": (
  "教室案内・受講料｜山形市の英会話教室 ABC英会話",
  "山形市元木のABC英会話（Bridgeway ABC English School）の教室案内。1998年開校、月〜金16:30〜20:30、未就学児から高校生・大人まで年間42回の少人数レッスン。受講料・アクセス・講師紹介・よくあるご質問はこちら。無料体験受付中／023-641-3059"),
 "tokyo-trip.html": (
  "東京研修旅行｜山形市の子ども英会話 ABC英会話",
  "ABC英会話（山形市）の東京研修旅行。学んだ英語を実際に使う機会として、外国人観光客との交流や現地体験を通して英語を「使える」力に変えます。"),
}

# Pages that must never appear in search results.
# summer-2026*: private family photo album. thank-you: form confirmation.
# animal-race: in-class game. hih-2 copy: stray duplicate.
PRIVATE = {
 "thank-you.html":          "お問い合わせありがとうございます｜ABC英会話",
 "summer-2026.html":        None,
 "summer-2026-backup.html": None,
 "animal-race.html":        None,
 # "hih-2 copy.html" was a stray duplicate - deleted 2026-08-18.
}

# Leave this page's markup in English - it's an in-class game, not a public page.
KEEP_ENGLISH = {"animal-race.html"}

# Pages that carry the JSON-LD block. Same @id on both, so Google reads them
# as one entity described twice, not two schools.
LD_PAGES = {"index.html", "school-information/index.html"}

SCHEMA = {
 "@context": "https://schema.org",
 "@type": "LanguageSchool",
 "@id": SITE + "/#school",
 "name": "ABC英会話 / Bridgeway ABC English School",
 "alternateName": ["ABC English School", "Bridgeway ABC English School",
                   "ABC英会話", "エービーシー英会話"],
 "url": SITE + "/",
 "logo": SITE + "/logo.png",
 "image": OG_IMAGE,
 "telephone": "+81-23-641-3059",
 "email": "abc-eikaiwa@outlook.com",   # <- confirm this is current
 "foundingDate": "1998-04",
 "priceRange": "¥¥",
 # Mon-Fri 16:30-20:30. This is what puts hours in Google's local panel.
 "openingHoursSpecification": [{
   "@type": "OpeningHoursSpecification",
   "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
   "opens": "16:30", "closes": "20:30",
 }],
 "address": {
   "@type": "PostalAddress", "streetAddress": "元木2-2-17",
   "addressLocality": "山形市", "addressRegion": "山形県",
   "postalCode": "990-2447", "addressCountry": "JP",
 },
 "geo": {"@type": "GeoCoordinates", "latitude": 38.2242458, "longitude": 140.3185454},
 "areaServed": {"@type": "City", "name": "山形市"},
 "sameAs": ["https://www.instagram.com/abc_eikaiwa/",
            "https://www.facebook.com/ABCenglish123/"],
 "inLanguage": ["ja", "en"],
 "knowsLanguage": ["ja", "en"],
}

# ---------------------------------------------------------------- helpers
# These files are CRLF. Every pattern below has to tolerate \r or each run
# leaves an orphan carriage return behind and the file grows forever.
EOL = r'(?:\r?\n)?'
BLOCK   = re.compile(EOL + r'<!-- MANAGED-SEO -->.*?<!-- /MANAGED-SEO -->' + EOL, re.S)
LDBLOCK = re.compile(EOL + r'<!-- MANAGED-SEO-LD -->.*?<!-- /MANAGED-SEO-LD -->' + EOL, re.S)
VIEWPORT = re.compile(r'(<meta\s+name="viewport"[^>]*>)', re.I)
TITLE    = re.compile(r'<title>.*?</title>', re.I | re.S)
HTMLTAG  = re.compile(r'<html\s+lang="[^"]*"', re.I)
# Any robots/description tag the page already carried, so we don't end up
# with two of them fighting each other.
OLD_ROBOTS = re.compile(r'[ \t]*<meta\s+name="(?:robots|googlebot)"[^>]*>' + EOL, re.I)
OLD_DESC   = re.compile(r'[ \t]*<meta\s+name="description"[^>]*>' + EOL, re.I)


def eol_of(s):
    """Preserve whatever line ending the file already uses."""
    return "\r\n" if "\r\n" in s else "\n"


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def url_for(fn):
    if fn == "index.html":
        return SITE + "/"
    if fn.endswith("/index.html"):          # directory-index page
        return SITE + "/" + fn[:-len("index.html")]
    return SITE + "/" + fn.replace(" ", "%20")


def build_block(fn, eol="\n"):
    out = ["<!-- MANAGED-SEO -->"]
    if fn in PRIVATE:
        out.append('<meta name="robots" content="noindex, nofollow, noarchive, noimageindex">')
        out.append('<meta name="googlebot" content="noindex, nofollow, noimageindex">')
    else:
        title, desc = PUBLIC[fn]
        u = url_for(fn)
        out += [
          '<meta name="description" content="%s">' % esc(desc),
          '<meta name="robots" content="index, follow, max-image-preview:large">',
          '<link rel="canonical" href="%s">' % u,
          '<meta property="og:type" content="website">',
          '<meta property="og:site_name" content="ABC英会話 / Bridgeway ABC English School">',
          '<meta property="og:locale" content="ja_JP">',
          '<meta property="og:title" content="%s">' % esc(title),
          '<meta property="og:description" content="%s">' % esc(desc),
          '<meta property="og:url" content="%s">' % u,
          '<meta property="og:image" content="%s">' % OG_IMAGE,
          '<meta name="twitter:card" content="summary_large_image">',
        ]
    out.append("<!-- /MANAGED-SEO -->")
    return eol + eol.join(out)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)

    known = set(PUBLIC) | set(PRIVATE)
    found = (set(glob.glob("*.html")) - {"404.html"}) | {
        p for p in known if "/" in p and os.path.exists(p)}

    for extra in sorted(found - known):
        print("  !! UNKNOWN PAGE (skipped, add it to the script):", extra)
    for missing in sorted(known - found):
        print("  !! LISTED BUT MISSING:", missing)

    done = 0
    for fn in sorted(found & known):
        s = io.open(fn, encoding="utf-8", newline="").read()
        eol = eol_of(s)

        s = BLOCK.sub(eol, s)
        # The LD block carries its own leading AND trailing newline, so strip
        # to nothing here - substituting eol would leave one behind per run.
        s = LDBLOCK.sub("", s)
        s = OLD_ROBOTS.sub("", s)
        s = OLD_DESC.sub("", s)

        if fn not in KEEP_ENGLISH:
            s = HTMLTAG.sub('<html lang="ja"', s, count=1)

        title = PUBLIC[fn][0] if fn in PUBLIC else PRIVATE.get(fn)
        if title:
            s = TITLE.sub("<title>" + title + "</title>", s, count=1)

        if not VIEWPORT.search(s):
            print("  !! no viewport meta, skipped:", fn)
            continue
        s = VIEWPORT.sub(lambda m: m.group(1) + build_block(fn, eol), s, count=1)

        if fn in LD_PAGES:
            ld = eol.join(["", "<!-- MANAGED-SEO-LD -->",
                           '<script type="application/ld+json">',
                           json.dumps(SCHEMA, ensure_ascii=False, indent=2).replace("\n", eol),
                           "</script>", "<!-- /MANAGED-SEO-LD -->", ""])
            s = s.replace("</head>", ld + "</head>", 1)

        io.open(fn, "w", encoding="utf-8", newline="").write(s)
        done += 1

    # ---- sitemap ----
    urls = [url_for(f) for f in PUBLIC if f in found]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(urls, key=lambda x: (x.count("/"), x)):
        pri = "1.0" if u.rstrip("/") == SITE else "0.7"
        sm += ["  <url>", "    <loc>%s</loc>" % u,
               "    <priority>%s</priority>" % pri, "  </url>"]
    sm.append("</urlset>")
    io.open("sitemap.xml", "w", encoding="utf-8", newline="").write("\n".join(sm) + "\n")

    # ---- robots ----
    # summer-2026*.html are deliberately NOT disallowed: Google has to be able
    # to crawl them to see the noindex tag. Only the image folder is blocked.
    io.open("robots.txt", "w", encoding="utf-8", newline="").write(
        "User-agent: *\nAllow: /\n\n"
        "Disallow: /summer-2026/\n\n"
        "Sitemap: %s/sitemap.xml\n" % SITE)

    print("\nSITE = %s  (IS_APEX=%s)" % (SITE, IS_APEX))
    print("updated %d pages, %d sitemap urls" % (done, len(urls)))


if __name__ == "__main__":
    main()
