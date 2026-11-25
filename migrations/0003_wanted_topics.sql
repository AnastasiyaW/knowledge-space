-- Topics the maintainer wants researched, listed at /api/wanted next to accepted agent reports.
-- Written only by the maintainer's own tooling (the daily selection from agent demand and article
-- age, or by hand); never by a public endpoint, so every word here is ours.
-- Apply: wrangler d1 execute happyin-subscribers --remote --file migrations/0003_wanted_topics.sql
CREATE TABLE IF NOT EXISTS wanted_topics (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  key         TEXT NOT NULL UNIQUE,             -- article path "domain/slug" or a slug for a new topic
  title       TEXT NOT NULL,
  domain      TEXT,
  article     TEXT,                             -- existing article to refresh, if any
  why         TEXT,                             -- e.g. how often agents read it and when it was last updated
  source      TEXT NOT NULL CHECK (source IN ('demand', 'owner')),
  added_at    TEXT NOT NULL,
  updated_at  TEXT NOT NULL,
  status      TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'closed', 'dropped')),
  closed_url  TEXT                              -- the refreshed article or PR
);
CREATE INDEX IF NOT EXISTS wanted_topics_status ON wanted_topics (status, added_at);
