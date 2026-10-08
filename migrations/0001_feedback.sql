-- Agent feedback: research hints for the knowledge base. Written by functions/api/feedback.js,
-- read and triaged by scripts/feedback_queue.py. Never rendered on the site.
-- Apply: wrangler d1 execute happyin-subscribers --remote --file migrations/0001_feedback.sql
CREATE TABLE IF NOT EXISTS feedback (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at  TEXT NOT NULL,                     -- ISO 8601 UTC
  day         TEXT NOT NULL,                     -- YYYY-MM-DD UTC, for daily limits
  kind        TEXT NOT NULL CHECK (kind IN ('gap', 'outdated', 'wrong', 'helped')),
  topic       TEXT,                              -- what was searched for / missing
  article     TEXT,                              -- normalised "domain/slug"
  detail      TEXT,
  source_url  TEXT,                              -- evidence offered by the sender
  agent       TEXT,                              -- self-declared client name, unverified
  client_hash TEXT NOT NULL,                     -- sha256(ip|day|salt), rotates daily; no IP stored
  status      TEXT NOT NULL DEFAULT 'new'
              CHECK (status IN ('new', 'accepted', 'rejected', 'done')),
  triage_note TEXT,
  result_url  TEXT,                              -- PR or article that closed it
  triaged_at  TEXT
);
CREATE INDEX IF NOT EXISTS feedback_status ON feedback (status, created_at);
CREATE INDEX IF NOT EXISTS feedback_client_day ON feedback (client_hash, day);
CREATE INDEX IF NOT EXISTS feedback_day ON feedback (day);
