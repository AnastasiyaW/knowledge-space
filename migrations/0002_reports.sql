-- Agent contact v2: reports gain kind 'finding', the channel (post / get), a coarse client family
-- for the agent funnel, and an owner-written public title for /api/wanted. SQLite cannot widen a
-- CHECK in place, so this is a new table; rows of 0001's `feedback` are copied, the old table is
-- left untouched (remove it only by an explicit owner decision). Copied rows get new ids unless
-- reports is empty, so a row the old code wrote during the deploy cannot collide with a new one;
-- run it again after the deploy to pick such rows up.
-- Apply: wrangler d1 execute happyin-subscribers --remote --file migrations/0002_reports.sql
CREATE TABLE IF NOT EXISTS reports (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at   TEXT NOT NULL,                    -- ISO 8601 UTC
  day          TEXT NOT NULL,                    -- YYYY-MM-DD UTC, for daily limits
  kind         TEXT NOT NULL CHECK (kind IN ('gap', 'outdated', 'wrong', 'helped', 'finding')),
  topic        TEXT,                             -- sender text: what was searched for / missing
  article      TEXT,                             -- normalised "domain/slug"
  detail       TEXT,
  source_url   TEXT,                             -- evidence offered by the sender
  agent        TEXT,                             -- self-declared client name, unverified
  client_hash  TEXT NOT NULL,                    -- sha256(ip|day|salt), rotates daily; no IP stored
  channel      TEXT NOT NULL DEFAULT 'post' CHECK (channel IN ('post', 'get')),
  ua_family    TEXT,                             -- coarse family from the User-Agent; full UA not stored
  status       TEXT NOT NULL DEFAULT 'new'
               CHECK (status IN ('new', 'accepted', 'rejected', 'done')),
  public_title TEXT,                             -- owner-written at triage; the only text /api/wanted shows
  triage_note  TEXT,
  result_url   TEXT,                             -- PR or article that closed it
  triaged_at   TEXT
);
CREATE INDEX IF NOT EXISTS reports_status ON reports (status, created_at);
CREATE INDEX IF NOT EXISTS reports_client_day ON reports (client_hash, day);
CREATE INDEX IF NOT EXISTS reports_day ON reports (day);

INSERT INTO reports (created_at, day, kind, topic, article, detail, source_url, agent, client_hash,
                     status, triage_note, result_url, triaged_at)
SELECT f.created_at, f.day, f.kind, f.topic, f.article, f.detail, f.source_url, f.agent, f.client_hash,
       f.status, f.triage_note, f.result_url, f.triaged_at
  FROM feedback f
 WHERE NOT EXISTS (SELECT 1 FROM reports r
                    WHERE r.created_at = f.created_at AND r.client_hash = f.client_hash AND r.kind = f.kind)
 ORDER BY f.id;
