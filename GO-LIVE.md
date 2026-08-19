# ABC英会話 / Bridgeway ABC — status & remaining work

**Status: LIVE at https://abc-eikaiwa.com as of 2026-08-18.**

Last content pass: **2026-08-19** (see "Done 2026-08-19" below).

Verified serving: homepage, `sitemap.xml`, `robots.txt`, the `/school-information`
redirect, and `www` → apex. HTTPS works on both hostnames.

---

## Reference

| | |
|---|---|
| Live site | `https://abc-eikaiwa.com` |
| Repo | `github.com/yoshi80085/bridgeway-abc`, publishing from `main` / root |
| abc-eikaiwa.com | Squarespace/Tucows registrar. Auto-renews **2027-06-03**. DNS points at GitHub Pages. |
| bridgewayabc.com | Namecheap. Auto-renews **2027-05-02**. 301-redirects to abc-eikaiwa.com. |
| Old Squarespace site | Expired, content gone. Not needed — all old URLs already mapped. |

**Tooling** — both are idempotent, safe to re-run:

- `python3 _tools/seo.py` — regenerates titles, meta descriptions, canonicals, OG
  tags, schema, `sitemap.xml`, `robots.txt`. Domain is the `SITE` constant at the top.
- `python3 _tools/redirects.py` — regenerates the ten old-Squarespace URL stubs.

---

## Remaining work

### 1. Google Business Profile ← highest value
*Still outstanding as of 2026-08-19.*
Update the website URL; it still points at the dead address. For a local school
the map pack likely drives more enrollment than organic search, so this is worth
more than everything else on this list combined.

While in there: confirm the category is 英会話教室 / Language school, check hours,
and add recent photos.

### 2. Google Search Console
*Still outstanding as of 2026-08-19. Add `/school-information/` to the list of
URLs to request indexing for — it's a brand-new page on an old, trusted URL.*
- Add `abc-eikaiwa.com` as a property (DNS TXT verification, added in Squarespace DNS)
- Submit `https://abc-eikaiwa.com/sitemap.xml`
- URL Inspection → `https://abc-eikaiwa.com/` → **Request Indexing**. Repeat for
  `/about.html` and `/course-books.html`.
- If an old property for this domain exists, keep it — the history is useful.

### 3. Update the other links pointing at the old address
- Instagram bio (`@abc_eikaiwa`)
- Facebook page (`facebook.com/ABCenglish123`) website field

### 4. Enforce HTTPS
Settings → Pages. Was showing "certificate has not yet been issued" while DNS was
still propagating, even though HTTPS already worked. Tick it once available. If
still greyed out after a day: Remove the custom domain, retype it, Save — then
`git pull`, because that rewrites the `CNAME` file.

---

### 5. ⚠️ Track down the forgotten third-party deployment

As of 2026-08-18, `https://bridgewayabc.com` was still serving a **live, older
copy of the site** over HTTPS, while `http://bridgewayabc.com` correctly
redirected to abc-eikaiwa.com. Most likely DNS mid-propagation, with different
resolvers giving different answers.

**The old copy is not on GitHub Pages.** Its links are extensionless
(`/about`, `/course-books`, `/halloween` — no `.html`), which is Netlify, Vercel
or Cloudflare Pages behaviour, not GitHub's. So there's a forgotten deployment
somewhere with bridgewayabc.com attached to it.

It's an outdated snapshot: calendar reads April–May 2026, the junior-high course
is described as "First Hand Access / My Next Grammar" instead of English
Firsthand, and there's no Summer 2026 album. A visitor landing there gets wrong
information, and as a duplicate it can split search signals.

**Update, later same day:** it was Netlify, and DNS has since moved —
`bridgewayabc.com` stopped serving the old copy. But Netlify team `yoshi6000` has
a project that published minutes after a `git push`, so it's connected to the
repo and mirroring the live site at some `*.netlify.app` URL. Alex has used
Netlify under **several different email addresses**, so the stale snapshot was
probably served by a *different* project under another login.

Dating the stale copy: it contained "My Next Grammar", removed from the repo in
commit `9397b77`, and lacked the Summer 2026 album added in `4d3866c`. So it was
a snapshot from before both. It did **not** come from the `New ABC Website`
folder — that string never existed there.

Not urgent: every page carries an absolute canonical to `abc-eikaiwa.com`, so any
mirror of the current site tells Google where the real one is.

To do:
- [ ] Netlify → Projects: how many exist? Check other email logins too.
- [ ] Each project → Domain management: detach `bridgewayabc.com` if attached.
- [ ] Active project → Site configuration → Build & deploy → Repository: confirm
      whether it's linked to `yoshi80085/bridgeway-abc`.
- [ ] Delete, or keep one deliberately as a staging preview — just with no
      custom domain pointed at it.

---

## Done 2026-08-19

Alex supplied the old Squarespace 教室案内 copy verbatim, which settled every
open question from the previous pass.

- **Founding year confirmed: 1998年4月.** The old 教室の概要 states it outright.
  `foundingDate: "1998-04"` was right; nothing to change.
- **`/school-information` is no longer a redirect — it's a real page again.**
  Google's index still carries it as 教室案内, and the old page was fees, hours,
  access and teachers, not "Meet the Teachers". Rather than dissipate its
  ranking onto another URL, the page was rebuilt at that exact path:
  `school-information/index.html`. Carries 教育理念, lesson hours, the full fee
  table, 教室の概要, teacher summaries, the map, and an FAQ — Japanese-first,
  which the rest of the site is thin on. Linked from the homepage nav and
  footer, and from about.html / course-books.html.
- **`openingHoursSpecification` added** — Mo–Fr 16:30–20:30. This is what puts
  hours in Google's local panel. The JSON-LD block now also renders on
  `/school-information/` with the same `@id`, so Google reads one entity
  described twice.
- **Hero age range widened.** "kindergarten through junior high" → age 3 through
  high school plus adults; the 🎓 〜中学生 badge → 〜高校生・大人; the courses
  intro and the enquiry form's age dropdown (高校生 was missing) match too.
- **`course-books.html` price cards said "月1回50分レッスン"** — once a month, for
  ¥7,000. Now "50分レッスン・年間42回". This was on all four cards and would have
  read as either absurdly expensive or a typo to every parent who saw it.
- **`course-books.html` still called the junior-high course "First Hand
  Access"** while index.html and first-hand.html said English Firsthand.
  Unified on English Firsthand; age chip 12〜15歳 → 中学生・高校生.
- **`course-books.html#adult` was a dead anchor** — no `id="adult"` existed on
  the page. Added, along with `id="junior"`.
- **Student private-lesson price (¥22,500) was missing** from the adult card.
- **`/new-page-1` redirect added.** Google still has the old "Portal access"
  page indexed; it had no stub. → homepage.
- **`_tools/seo.py` now handles directory-index pages** (`url_for`, discovery,
  and a `LD_PAGES` set). Re-running it is still idempotent.

### Second pass, same day

- **FAQPage schema on `/school-information/`.** Generated *from* the page's
  `.faq-item` blocks by `seo.py`, so editing the FAQ and re-running keeps the
  two in sync — it can't drift. Five Q&As. This is the cheapest route to a
  richer-looking result in Google.
- **NAP made consistent across all 36 pages.** It wasn't: the footer said
  "ABC Bridgeway English School" on 16 pages and "Bridgeway ABC English School"
  on one, the nav wordmark had four different spellings, and no footer carried
  the postcode or the Japanese name at all. Now every page reads
  `ABC英会話｜Bridgeway ABC English School` and
  `〒990-2447 山形県山形市元木2-2-17 ｜ TEL 023-641-3059`. Address notation is
  `元木2-2-17` everywhere (23 occurrences, no variants).
  This matters because the map pack cross-references the site against
  directory listings, and mismatched strings weaken the match.
- **Nav sub-line now reads `ABC英会話 · 山形市元木`** instead of "English School",
  so the two keywords that matter appear on every page. Cosmetic change —
  revert in the `nav-logo-text` markup if you don't like it.
- **Japanese teacher bios added to `about.html`.** The page was entirely in
  English under `lang="ja"`; good credentials that no Japanese search could
  find. Both bios now have a Japanese version, and the page intro leads in
  Japanese.
- **Five more old Squarespace URLs got redirect stubs**: `/new-page`,
  `/new-page-2`, `/little-hands-1`, `/little-hands-2`, `/hh1-u13`. All still
  in Google's index, none had a stub. 15 stubs total now.

---

## Local citations — the actual path to the map pack

Researched 2026-08-19. Blunt finding: **there is essentially no citation
footprint.** Searching the phone number, the address and the brand name across
Japanese directories turned up exactly one third-party listing.

Also worth knowing: the discovery query 山形市 英会話教室 子ども おすすめ is
dominated by affiliate listicles (English Hub, プロリア英会話, コドモブースター,
コトスタキッズ) and chains. You don't outrank those with your own site — you get
*listed in* them, and you win on the map pack and on longer, more specific
queries instead.

### The one listing that exists

**コドモブースター** — https://kodomo-booster.com/schools/s16218
Listed as `ABC英会話教室 山形市元木英会話教室`, rated 4.0 (2 reviews, from families
who joined in 2013 and 2019). Phone: **blank.** Website: **blank.** 料金: blank.
対象年齢: 調査中. Flagged as not accepting enquiries. It is unclaimed.

Claim it (https://kodomo-booster.com/contacts), add the phone, add
`https://abc-eikaiwa.com`, fill in 対象年齢 and fees, enable trial applications.
Fastest single win on this page.

### Free registrations, in priority order

1. **iタウンページ** — https://itp.ne.jp/about-posted-application/ (feeds other aggregators)
2. **Yahoo!プレイス** — https://yplace.yahoo.co.jp/ (drives Yahoo!ロコ and Yahoo!マップ)
3. **エキテン 教室プラン** — https://www.owner.ekiten.jp/free-lesson01 (free plan includes 口コミ + website link)
4. **習い事スクスク** — https://sp-sukusuku.jp/
5. **子どもスクールナビ** — https://ksn-japan.net/ ／ **すたぽ** — https://sutapo.com/
6. **ジモティー** — https://jmty.jp/yamagata/les-eng (post 無料体験 recruitment, not just a listing)

Use the exact same NAP string every time — the one now in the site footer.

Skip まいぷれ: no 山形市 edition exists.

**Could not verify, needs a human:** Yahoo!ロコ (robots-blocked), NAVITIME (403),
iタウンページ presence, みんなの英語ひろば, and Google Business Profile itself.

### Note on the brand name

`abcenglish.velvet.jp` (Shiga) and `eikaiwa-abc.com` (Shizuoka) both compete for
the bare "ABC英会話" query. Register everywhere as **ABC英会話 山形** or
**ABC英会話（山形市元木）**, never bare "ABC".

---

## The content gap, measured

Direct local competitor ニコニコ英会話 (山形市松栄) has **153 URLs in its sitemap.
This site has 16.** Nearly all of their extra pages are ongoing Japanese-language
posts — news, blog, per-course pages, plus separate 料金 and アクセス pages.

They publish full fees openly (入会金10,000円, 幼児8,365円, 小学生8,365円〜, 大人
9,600円/月 年間42回). Worth knowing what you're priced against: ABC is
7,000–7,700円, i.e. meaningfully cheaper, which is an argument the site should
probably be making out loud.

The gap isn't design — the new 教室案内 page closes the 料金/アクセス/時間 hole.
What's left is that there's no stream of dated Japanese content. The Halloween,
summer-camp and Tokyo-trip pages already exist as one-offs; turning the
Instagram feed into dated Japanese posts would be the natural next move.

---

## Open questions / judgement calls

- [ ] **`images/kyoko.jpg` doesn't exist.** about.html falls back to a
      "Photo coming soon" placeholder, so nothing is visibly broken — but the
      Japanese-side teacher has no photo. Worth adding.
- [ ] **Little Hands price card reads `¥7,000 (¥5,500)`** with no explanation of
      what the bracketed figure is. The old site listed 未就学児7,000円 only.
      Either explain it or drop it.
- [ ] **`about.html` is entirely in English** under `lang="ja"`. The bios are
      good, but 山形市 英会話 講師 searches won't find them. Worth a Japanese
      version of each bio at some point.

---

## Content issues noticed but not changed

- **`images/calendar-June_July.jpg`** is now unreferenced. Harmless; delete whenever.
- **`C:\Users\ATBro\Documents\New ABC Website`** is the stale pre-git copy. It has
  a superseded-notice file in it. Safe to delete once you're confident nothing
  there is needed.

---

## Worth fixing properly at some point

**The Summer 2026 photo album isn't actually protected.** The passcode is
implemented in the page itself, so:

- anyone with a direct image URL (`/summer-2026/waterwars-3.webp`) sees the photo
  without ever hitting the passcode screen
- "View Source" reveals the passcode

The pages are `noindex` and `/summer-2026/` is disallowed in `robots.txt`, so they
won't surface in search — but that's obscurity, not protection. GitHub Pages
can't fix this; it serves static files with no way to authenticate first. Real
options are a host that can gate files (Cloudflare Access, Netlify password
protection) or a private album service. Worth addressing since those are
students' families.

See `_ADD-REAL-PASSWORD.txt` for the original note on this.

---

## What to check in 2–4 weeks

Recovery should be quick, since the domain is old and trusted rather than new.

- Search Console → Performance: impressions for 英会話 / 山形 queries starting to appear
- Search `site:abc-eikaiwa.com` — pages should be indexed
- Search 山形市 英会話 and see where you land
- Confirm branded searches (ABC英会話) still rank #1 — they should never have moved

If nothing is indexed after a month, check Search Console → Pages for crawl
errors before changing anything. Don't tinker with the setup in the meantime;
ranking recovery after a domain move is slow and steady, and churn makes it worse.

---

## Background — why the site vanished

Not a rebrand penalty. The site was **never connected to anything**. GitHub Pages
was disabled on the repo, so it wasn't even live at the github.io URL, while both
domains resolved nowhere. Meanwhile abc-eikaiwa.com's seven years of links sat
unused. The fix was connecting them, not undoing the rebrand.

Also fixed along the way: every page declared `lang="en"` over Japanese content,
no page had a meta description, titles carried no 英会話 or 山形市, and there was
no sitemap, robots.txt, or structured data.
