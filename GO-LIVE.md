# ABC英会話 / Bridgeway ABC — status & remaining work

**Status: LIVE at https://abc-eikaiwa.com as of 2026-08-18.**

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
Update the website URL; it still points at the dead address. For a local school
the map pack likely drives more enrollment than organic search, so this is worth
more than everything else on this list combined.

While in there: confirm the category is 英会話教室 / Language school, check hours,
and add recent photos.

### 2. Google Search Console
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

## Open questions / judgement calls

- [ ] **Verify the 1998 founding year.** Currently in the meta description, the
      hero, and the schema's `foundingDate`. It came from a Google summary of the
      old site, not a primary source. 2012 was definitely wrong (ruled out: Alex
      started 2019, predecessor was there ~10 years, and others came before).
      Confirm against old materials if possible. Fix location: `_tools/seo.py`
      plus two spots in `index.html`.
- [ ] **`/school-information` redirect target.** Points at `about.html`
      ("Meet the Teachers"). If the old page was more about fees, schedule or
      access, retarget in `_tools/redirects.py` — `course-books.html` or
      `index.html#about` may fit better. This is the most valuable redirect
      after the homepage.
- [ ] **Lesson days and times** — needed to add `openingHoursSpecification` to
      the schema, which is what makes hours appear in Google's local panel.

---

## Content issues noticed but not changed

- **Hero undersells the age range.** It says lessons run "from kindergarten
  through junior high" and the badge reads 🎓 〜中学生, but the courses section
  offers English Firsthand for 中学生・高校生 *and* an adult class. The first
  thing visitors read is narrower than what's actually offered.
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
