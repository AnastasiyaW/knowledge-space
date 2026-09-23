# Site SEO, page head and layout: what not to break

Every point below was a live defect found by the SEO audit of 2026-09-23. Each one names the
check that guards it. Run both after touching hooks, templates or site CSS:

```bash
python -m pytest tests -q
python -m mkdocs build --strict
```

## Meta descriptions (`hooks/description.py`)
- A front matter `description:` wins.
- Otherwise the description is the first prose paragraph after the H1. These are skipped:
  - headings, lists, tables, code and admonitions;
  - the news pipeline's metadata lines: `**Development line:**`, `**Last event:**`,
    `**Events:**`, `**Last researched:**`, `**Freshness check:**`;
  - the `**Scope checked: …**` label.
- Hub `index.md` pages without prose get "Title: N articles on Section, Section, …".
- `"` becomes `'`. Templates render without autoescape, and one double quote cut 15
  descriptions short, leaving stray attributes behind.
- `hooks/generate_llms_txt.py` carries the same `_METADATA_LINE`, and
  `tests/test_description_hook.py` keeps the two equal. A new pipeline label goes into both.
- Read `page.file.src_uri`, never `src_path`. On Windows `src_path` has backslashes, so local
  builds silently differ from CI. The tests fake a Windows `src_path` to catch this.

## Home page description (`mkdocs.yml`, `site_description`)
- Keep the form "NNNN+ curated articles across NN domains", with no thousands separator.
  `scripts/sync_stats.py` keeps both numbers current only in that form. "1,287+" would become
  "1,1287+", and "and 21 more domains" went stale because no script reached it.

## Structured data and preview images
- **BreadcrumbList** is `overrides/partials/breadcrumb-jsonld.html`.
  - Google requires `item` on every level but the last.
  - Each level links to its section's index page (the hub) and takes that page's title.
  - The Material blog index appears once.
  - `tests/test_breadcrumb_jsonld.py` covers this.
- **Preview image** is `overrides/partials/og-image.html`.
  - It uses `og-<domain>.png` only for domains where `hooks/og_image.py` found that file; every other page uses `og-image.png`.
  - To give a domain its own image, add `docs/assets/og-<domain>.png`.
  - `TechArticle.image` uses the same URL.
- **No `hreflang`.** The `llms-*.txt` files are not translations of a page. llms.txt is advertised by the `Link` header in `_headers` and by one `<link rel="alternate" type="text/plain">`.

## Page weight
- **three.js** is loaded by `docs/javascripts/graph.js`, and only when `#knowledge-graph`
  exists (the home page). Do not put it back into `extra_javascript`: that cost every
  article 166 KB and seconds of mobile main-thread time.
- **`navigation.instant.prefetch` stays off.** It re-read the 174 KB `sitemap.xml` up to 8 times per page.
- **The fonts.googleapis.com `preconnect`** lives in `{% block fonts %}`, before `{{ super() }}`, so it precedes the font stylesheet. In `extrahead` it would come too late to help.

## Sidebar and the phone menu (`docs/stylesheets/graph.css`)
- **All widths:** `.md-sidebar--primary` is a flex column. The site's buttons
  (`.ks-sidebar-buttons`, added by `overrides/main.html`) sit on top and the navigation fills the rest.
- **Desktop only (≥ 76.25em):** sticky and full height, the `[hidden]` rule, and the fade bands.
- **Below 76.25em** Material turns the sidebar into a fixed drawer. Three things have broken it:
  - making it sticky pinned it into the page and squeezed articles into a narrow column;
  - hiding `[hidden]` there removed the home page's menu;
  - a scroll wrapper without the flex height left the opened menu empty.
- **After any sidebar CSS change,** open the drawer at 375, 1024 and 1280 px, on an article and on the home page.
