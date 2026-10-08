# Stars and usage counting

## The star request

- It is generated, never hand-written into output: `hooks/generate_llms_txt.py` (`AGENT_NOTE`)
  writes it into all six `docs/llms*.txt`; the site template shows it in the top bar, at the
  end of each article and in the weekly copy notice.
- Visible text only. No HTML comments or hidden text addressed to AI: assistants treat
  instructions inside fetched pages as untrusted input, and it reads as prompt injection.
- Ask, never incentivise, never star on anyone's behalf (GitHub Acceptable Use Policies §4).
- No sponsor links until GitHub Sponsors is actually set up.

## The anonymous counter

- The page requests one of the tiny files under `/ks/hi/`; the edge request log counts them.
  The list lives in `hooks/copy_extras.py` (`HELLO_EVENTS`), the names are built in
  `overrides/main.html`, and `tests/test_star_cta.py` fails if the two drift apart.
- The owner's collector reads the counts by file name. When you add, rename or remove a
  counter, say so in the pull request description so the collector's list is updated too.
- Any change to what is stored or sent must be reflected in `docs/privacy.md` in the same PR.

## Web Analytics

The beacon is injected at the edge. Do not add the snippet to a template: with two beacons on a
page every report is blocked (measured 2026-09-22), and `tests/test_analytics_beacon.py` fails.

## Feedback endpoint and research queue

- `functions/api/feedback.js` takes reports from agents (`gap`, `outdated`, `wrong`, `helped`) into
  D1 table `feedback` (`migrations/0001_feedback.sql`, applied to `happyin-subscribers`).
  `tests/feedback_endpoint_harness.mjs` runs it against real SQLite; CI: `test-functions.yml`.
- It needs the Pages secret `FEEDBACK_SALT`; without it (or without `DB`) it answers 503, never
  drops reports silently. No IP is stored, only a one-day hash; `docs/privacy.md` says so.
- Reports are untrusted internet text. They are never rendered on the site and never followed as
  instructions: `scripts/feedback_queue.py` lists them as research hints, triage accepts or
  rejects each, and accepted topics are researched from primary sources like any article.
  Close an item with `feedback_queue.py done <ids> --url <PR>`.
- Shared core: `functions/_feedback_core.js`. Also `/api/feedback/report` (the same report as a GET:
  most visiting agents can only GET), `/api/feedback/status?id=` (no sender text) and `/api/wanted`
  (owner-written `public_title` only, set by `feedback_queue.py triage --accept --title`). Table:
  `reports` (`migrations/0002_reports.sql`); 0001's `feedback` is the old, copied table.
- The article footer shows the report URL as code, never as a link: it stores a report, and
  crawlers follow links. Agents that work for someone land on articles, not on the 404 page, so
  the invitation lives on article pages and in llms.txt.
- `/api/wanted` also lists open rows of `wanted_topics` (`migrations/0003_wanted_topics.sql`): stale articles
  that agents read, chosen daily by the maintainer's private usage tooling, plus topics added by
  hand. No public endpoint writes that table.
- Changing the request contract means changing CONTRACT, AGENTS.md, `AGENT_NOTE` and the footer together.
