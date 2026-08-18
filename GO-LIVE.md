# SEO status & go-live plan — bridgeway-abc

_Updated 2026-08-18. Nothing here has been connected to a domain yet — that's on hold until you say go._

---

## Where things actually stand

| Thing | Status |
|---|---|
| **Site** | `yoshi80085.github.io/bridgeway-abc` — live, publishing from `main` |
| **abc-eikaiwa.com** | Yours. Squarespace/Tucows, auto-renews 2027-06-03. Resolves but serves nothing. |
| **bridgewayabc.com** | Yours. Namecheap, auto-renews 2027-05-02. Never connected to anything. |
| **Custom domain on GitHub** | Not configured — no CNAME file in the repo |

**This is why the site vanished from Google.** It isn't a rebrand penalty. The new
site was never attached to a domain at all. It's been sitting on a github.io
project URL that nothing links to, while both domains you pay for point nowhere.
Nothing is damaged — it just was never plugged in.

---

## What's been done (safe to ship now)

All of this is domain-independent and improves the site wherever it's served:

- `lang="en"` → `lang="ja"` on every page. You were telling Google these were
  English pages for English speakers.
- Japanese keyword-first titles carrying 英会話 / 山形市. Every title was
  previously English-only. Your old site ranked partly *because* its title read
  「ABC English School は、ずっと身につく英会話」.
- Meta descriptions on all 15 public pages. There were none.
- Canonical + Open Graph tags (currently pointing at the github.io URL — correct
  for today, one line to flip at launch).
- `LanguageSchool` JSON-LD with address, phone, geo, founding date.
- `sitemap.xml`, `robots.txt`, and a branded Japanese `404.html`.
- `noindex` on `thank-you`, `animal-race`, `hih-2 copy`, and **both** Summer 2026
  album pages.
- `.gitattributes` to stop the CRLF phantom diffs. Your working tree had drifted
  to CRLF while HEAD was LF, which is why a one-line edit showed up as
  "1468 insertions, 1468 deletions". The real diff for all this SEO work is
  303 insertions / 39 deletions.

Re-run any time with `python3 _tools/seo.py`. It's idempotent — verified stable
across three consecutive runs.

---

## Decide before launch: which domain

Both are yours and both are paid up, so this is purely a branding call.

- **abc-eikaiwa.com** — 7 years old, holds every backlink you've ever earned, has
  英会話 in the name, matches `@abc_eikaiwa` and what people actually search.
  Fastest recovery by a wide margin.
- **bridgewayabc.com** — clean brand match, but zero history and zero links.
  Starting from nothing.

Nothing stops you using abc-eikaiwa.com as the address while the school is
called Bridgeway ABC. You can also point bridgewayabc.com at the site as a
redirect so both work.

---

## When you say go — launch steps

### 1. Flip the domain in the script

In `_tools/seo.py`, change two lines:

```python
SITE = "https://abc-eikaiwa.com"
IS_APEX = True
```

Then `python3 _tools/seo.py`. That rewrites every canonical, og:url, the schema
URLs, and the sitemap in one pass.

### 2. Fix the root-relative links ⚠️

`index.html` and others contain `href="/"`, `href="/#about"`, `href="/#contact"`,
`href="/#courses"`. These are **currently broken** on the project URL — they jump
to `yoshi80085.github.io` instead of your site. They'll start working the moment
you're on an apex domain, so this fixes itself at launch. But if launch is more
than a few days out, say the word and I'll convert them to relative paths so the
live site's navigation works in the meantime.

### 3. Add the CNAME and set the custom domain

Create a `CNAME` file at the repo root containing just the domain, then:
GitHub repo → **Settings → Pages → Custom domain** → enter it → Save.
Leave **Enforce HTTPS** unticked until DNS resolves.

### 4. DNS

**For abc-eikaiwa.com** — Squarespace → Domains → DNS Settings. Remove the
existing Squarespace A record and `www` CNAME, then add:

| Type | Host | Value |
|---|---|---|
| A | @ | `185.199.108.153` |
| A | @ | `185.199.109.153` |
| A | @ | `185.199.110.153` |
| A | @ | `185.199.111.153` |
| CNAME | www | `yoshi80085.github.io` |

**For bridgewayabc.com** — same records at Namecheap (Advanced DNS), if you want
it pointing at the site too.

**Leave MX records alone** — those are email.

### 5. Then

- Tick **Enforce HTTPS** once the domain resolves (cert can take up to 24h).
- Search Console: add the property, submit `sitemap.xml`, request indexing on
  the homepage.
- Update the website URL on **Google Business Profile** (likely worth more than
  organic for a local school), Instagram bio, and the Facebook page.

---

## Old URL redirects — done

Recovered the full old URL list from the Wayback Machine and built stubs for all
ten. They're in the repo now and do nothing until abc-eikaiwa.com points here.
Regenerate with `python3 _tools/redirects.py`.

| Old Squarespace URL | Redirects to |
|---|---|
| `/` | homepage (automatic — no stub needed) |
| `/school-information` | `about.html` ⚠️ see below |
| `/access` | `index.html#contact` |
| `/contact-us` | `index.html#contact` |
| `/take-action` | `index.html#contact` |
| `/news` + 3 old posts | `index.html#instagram` |
| `/partners` | `index.html` |
| `/projects` | `index.html#events` |

⚠️ **One judgement call worth your eye:** `/school-information` was 教室案内 in
Google's index and is the most valuable redirect after the homepage. I pointed it
at `about.html`, but that page is "Meet the Teachers". If the old page was more
about fees, schedule or access, retarget it in `_tools/redirects.py` —
`course-books.html` or `index.html#about` may fit better. You'll remember what
was on it; I'm guessing from the title.

`/partners`, `/projects` and `/take-action` are stock Squarespace template page
names and were probably never used. Built anyway — costs nothing.

## Still needed from you

- [ ] **Confirm the schema email.** I used `abc-eikaiwa@outlook.com` from the old
      site. Fix it in `_tools/seo.py` if wrong.
- [ ] **Lesson days/hours** — so I can add `openingHoursSpecification`, which is
      what makes hours appear in Google's local panel.
- [ ] **Delete `hih-2 copy.html`** — stray duplicate, noindexed for now.

---

## Unrelated but worth knowing

`_ADD-REAL-PASSWORD.txt` is right: the Summer 2026 album passcode is client-side
only. The pages are noindexed and `/summer-2026/` is disallowed in robots.txt, so
they won't surface in search — but anyone with a direct image URL can still open
it, and "View Source" reveals the passcode. GitHub Pages can't fix that; it needs
a host that can authenticate before serving files. Worth addressing separately
since those are students' families.
