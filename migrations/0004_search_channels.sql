-- Preserve report IDs (public status URLs), all triage data and the AUTOINCREMENT
-- high-water mark while widening SQLite's channel CHECK. Apply once via D1 migrations.
CREATE TABLE reports_search_channels (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  day TEXT NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('gap', 'outdated', 'wrong', 'helped', 'finding')),
  topic TEXT,
  article TEXT,
  detail TEXT,
  source_url TEXT,
  agent TEXT,
  client_hash TEXT NOT NULL,
  channel TEXT NOT NULL DEFAULT 'post' CHECK (channel IN ('post', 'get', 'search', 'mcp-search')),
  ua_family TEXT,
  status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'accepted', 'rejected', 'done')),
  public_title TEXT,
  triage_note TEXT,
  result_url TEXT,
  triaged_at TEXT
);
INSERT INTO reports_search_channels SELECT * FROM reports;
UPDATE sqlite_sequence SET seq = max(seq, coalesce((SELECT seq FROM sqlite_sequence WHERE name = 'reports'), 0))
 WHERE name = 'reports_search_channels';
DROP TABLE reports;
ALTER TABLE reports_search_channels RENAME TO reports;
CREATE INDEX reports_status ON reports (status, created_at);
CREATE INDEX reports_client_day ON reports (client_hash, day);
CREATE INDEX reports_day ON reports (day);
