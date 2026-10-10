// Runs the agent contact endpoints (functions/api/feedback.js, feedback/report.js,
// feedback/status.js, wanted.js) against a real SQLite database built from every file in
// migrations/, behind a minimal D1-shaped adapter. Exit 0 = every check passed.
// Usage: node tests/feedback_endpoint_harness.mjs
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const load = (p) => import(new URL(`../functions/${p}`, import.meta.url));
const mod = await load("api/feedback.js");
const report = await load("api/feedback/report.js");
const status = await load("api/feedback/status.js");
const wanted = await load("api/wanted.js");
const search = await load("api/search.js");
const mcpGap = await load("api/feedback/internal/mcp-gap.js");

function d1() {
  const sqlite = new DatabaseSync(":memory:");
  for (const f of readdirSync(root + "migrations").filter((n) => n.endsWith(".sql")).sort()) {
    sqlite.exec(readFileSync(root + "migrations/" + f, "utf8"));
  }
  const db = {
    sqlite,
    prepare(sql) {
      const stmt = sqlite.prepare(sql);
      let args = [];
      const bound = {
        bind(...values) { args = values; return bound; },
        async first() { return stmt.get(...args) ?? null; },
        async all() { return { results: stmt.all(...args) }; },
        async run() {
          const r = stmt.run(...args);
          return { meta: { last_row_id: Number(r.lastInsertRowid), changes: r.changes } };
        },
      };
      return bound;
    },
  };
  return db;
}

async function post(env, body, ip = "203.0.113.7", ua = "curl/8.5.0") {
  const request = new Request("https://happyin.space/api/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json", "CF-Connecting-IP": ip, "User-Agent": ua },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
  const res = await mod.onRequestPost({ request, env });
  return { status: res.status, body: await res.json() };
}

async function get(handler, env, query, ip = "203.0.113.7", ua = "Mozilla/5.0 (compatible; Claude-User/1.0)") {
  const request = new Request(`https://happyin.space/x?${query}`, { headers: { "CF-Connecting-IP": ip, "User-Agent": ua } });
  const res = await handler.onRequestGet({ request, env });
  const type = res.headers.get("Content-Type") || "";
  return { status: res.status, type, body: type.startsWith("application/json") ? await res.json() : await res.text(), res };
}

const env = { DB: d1(), FEEDBACK_SALT: "test-salt" };

// Contract is discoverable.
const contract = await (await mod.onRequestGet()).json();
assert.deepEqual(Object.keys(contract.kinds), ["gap", "outdated", "wrong", "helped", "finding"]);
assert.ok(contract.get.includes("/api/feedback/report") && contract.wanted.includes("/api/wanted"));

// Migration 0002 copies the rows of 0001's table.
{
  const m = new DatabaseSync(":memory:");
  m.exec(readFileSync(root + "migrations/0001_feedback.sql", "utf8"));
  m.prepare("INSERT INTO feedback (created_at, day, kind, topic, client_hash, status) VALUES ('t', '2026-10-08', 'gap', 'old row', 'h', 'rejected')").run();
  m.exec(readFileSync(root + "migrations/0002_reports.sql", "utf8"));
  m.exec(readFileSync(root + "migrations/0002_reports.sql", "utf8"));   // re-run is harmless
  assert.deepEqual(m.prepare("SELECT id, topic, status, channel FROM reports").all().map((x) => ({ ...x })),
                   [{ id: 1, topic: "old row", status: "rejected", channel: "post" }]);
  // The new code writes id 2; the old code, still live during the deploy, also writes its id 2.
  m.prepare("INSERT INTO reports (created_at, day, kind, topic, client_hash) VALUES ('t2', '2026-10-08', 'gap', 'new code', 'n')").run();
  m.prepare("INSERT INTO feedback (created_at, day, kind, topic, client_hash) VALUES ('t3', '2026-10-08', 'gap', 'old code', 'o')").run();
  m.exec(readFileSync(root + "migrations/0002_reports.sql", "utf8"));
  assert.deepEqual(m.prepare("SELECT topic FROM reports ORDER BY id").all().map((x) => x.topic), ["old row", "new code", "old code"]);
}

// Fail loud without storage or salt (negative control: no silent drop).
assert.equal((await post({ DB: env.DB }, { kind: "gap", topic: "x y z" })).status, 503);
assert.equal((await post({ FEEDBACK_SALT: "s" }, { kind: "gap", topic: "x y z" })).status, 503);
assert.equal((await get(report, { DB: env.DB }, "kind=gap&topic=x")).status, 503);

// Valid rows land, with article normalised, channel and client family recorded, no IP stored.
let r = await post(env, { kind: "gap", topic: "Kafka share groups", agent: "claude-code" });
assert.equal(r.status, 201, JSON.stringify(r.body));
assert.equal(r.body.status_url, `https://happyin.space/api/feedback/status?id=${r.body.id}`);
r = await post(env, { kind: "outdated", article: "https://happyin.space/kafka/consumer-groups/", detail: "KIP-848 is GA in 4.0" });
assert.equal(r.status, 201, JSON.stringify(r.body));
r = await post(env, { kind: "helped", article: "docs/python/asyncio-basics.md" });
assert.equal(r.status, 201);
const rows = env.DB.sqlite.prepare("SELECT * FROM reports ORDER BY id").all();
assert.deepEqual(rows.map((x) => x.article), [null, "kafka/consumer-groups", "python/asyncio-basics"]);
assert.ok(rows.every((x) => x.status === "new" && x.channel === "post" && x.ua_family === "curl"
                     && /^[0-9a-f]{32}$/.test(x.client_hash)));
assert.ok(!JSON.stringify(rows).includes("203.0.113.7"), "raw IP must not be stored");

// Same report twice in a day is a duplicate that points at the first one.
r = await post(env, { kind: "gap", topic: "Kafka share groups" });
assert.equal(r.body.duplicate, true);
assert.equal(r.body.id, 1);
assert.equal(env.DB.sqlite.prepare("SELECT count(*) AS n FROM reports").get().n, 3);

// Rejections, each must be red.
const bad = [
  "not json",
  [1, 2],
  { kind: "spam" },
  { kind: "gap" },
  { kind: "helped" },
  { kind: "wrong", article: "kafka/x" },
  { kind: "outdated", article: "../../etc/passwd", detail: "d" },
  { kind: "gap", topic: "t".repeat(201) },
  { kind: "gap", topic: 42 },
  { kind: "gap", topic: "ok topic", source_url: "javascript:alert(1)" },
  { kind: "finding", topic: "t", detail: "d" },
  { kind: "finding", topic: "t", source_url: "https://example.org/a" },
  { kind: "gap", topic: "<what you looked for>" },
  { kind: "outdated", article: "kafka/consumer-groups", detail: "<what changed>" },
];
for (const body of bad) assert.equal((await post(env, body)).status, 400, JSON.stringify(body));
assert.equal((await post(env, JSON.stringify({ kind: "gap", topic: "x".repeat(9000) }))).status, 413);

// Content-Length over the limit is refused before the body is read.
{
  const request = new Request("https://happyin.space/api/feedback", {
    method: "POST", headers: { "Content-Type": "application/json", "Content-Length": "999999" },
    body: JSON.stringify({ kind: "gap", topic: "fine" }),
  });
  assert.equal((await mod.onRequestPost({ request, env })).status, 413);
}

// Same subject with a different detail is still one report per client per day.
r = await post(env, { kind: "outdated", article: "kafka/consumer-groups", detail: "another wording" });
assert.equal(r.body.duplicate, true);

// A finding with a source is accepted.
r = await post(env, { kind: "finding", topic: "Kafka share groups", detail: "GA in 4.1", source_url: "https://kafka.apache.org/" });
assert.equal(r.status, 201, JSON.stringify(r.body));

// GET channel: the same report as query parameters, plain-text reply, recorded as channel get.
let g = await get(report, env, "kind=gap&topic=" + encodeURIComponent("Rust async traits") + "&agent=chatgpt");
assert.equal(g.status, 201, g.body);
assert.ok(g.type.startsWith("text/plain") && /Report received: #\d+/.test(g.body) && g.body.includes("/api/feedback/status?id="));
assert.equal(g.res.headers.get("Cache-Control"), "no-store");
assert.equal(g.res.headers.get("X-Robots-Tag"), "noindex");
const getRow = env.DB.sqlite.prepare("SELECT channel, ua_family FROM reports WHERE topic = 'Rust async traits'").get();
assert.deepEqual({ ...getRow }, { channel: "get", ua_family: "claude-user" });
g = await get(report, env, "kind=gap&topic=" + encodeURIComponent("Rust async traits"));
assert.ok(g.body.startsWith("Report already received"));
g = await get(report, env, "kind=nonsense");
assert.equal(g.status, 400);
assert.ok(g.body.startsWith("Not stored: kind must be"));
g = await get(report, env, "");                                  // bare URL: usage, nothing stored
assert.equal(g.status, 200);
assert.ok(g.body.includes("kind=gap&topic="));
const before = env.DB.sqlite.prepare("SELECT count(*) AS n FROM reports").get().n;
await get(report, env, "");
assert.equal(env.DB.sqlite.prepare("SELECT count(*) AS n FROM reports").get().n, before);

// Status: no sender text, ever.
g = await get(status, env, "id=1");
assert.equal(g.status, 200);
assert.deepEqual(Object.keys(g.body).sort(), ["day", "id", "kind", "meaning", "public_title", "result_url", "status"]);
assert.ok(!JSON.stringify(g.body).includes("Kafka share groups"));
assert.equal((await get(status, env, "id=999")).status, 404);
assert.equal((await get(status, env, "id=abc")).status, 400);

// Wanted lists only accepted rows with an owner-written title, never the sender's topic.
env.DB.sqlite.prepare("UPDATE reports SET status = 'accepted', public_title = 'Kafka 4 share groups' WHERE id = 1").run();
env.DB.sqlite.prepare("UPDATE reports SET status = 'accepted' WHERE topic = 'Rust async traits'").run();   // no title
g = await get(wanted, env, "");
assert.deepEqual(g.body.wanted.map((w) => w.topic), ["Kafka 4 share groups"]);
assert.ok(!JSON.stringify(g.body).includes("Kafka share groups"));

// Maintainer topics come first; closed and dropped ones are not listed.
{
  const ins = env.DB.sqlite.prepare(
    `INSERT INTO wanted_topics (key, title, domain, article, why, source, added_at, updated_at, status)
     VALUES (?, ?, ?, ?, ?, 'demand', '2026-10-08T00:00:00Z', '2026-10-08T00:00:00Z', ?)`);
  ins.run("llm-agents/telegram-managed-bots", "Refresh: Telegram managed bots", "llm-agents",
          "llm-agents/telegram-managed-bots", "fixture reason", "open");
  ins.run("x/closed", "Closed topic", "x", null, null, "closed");
  ins.run("x/dropped", "Dropped topic", "x", null, null, "dropped");
  g = await get(wanted, env, "");
  assert.deepEqual(g.body.wanted.map((w) => w.topic), ["Refresh: Telegram managed bots", "Kafka 4 share groups"]);
  assert.equal(g.body.wanted[0].article, "https://happyin.space/llm-agents/telegram-managed-bots/");
  assert.equal(g.body.wanted[0].since, "2026-10-08");
  env.DB.sqlite.exec("ALTER TABLE wanted_topics RENAME TO wanted_topics_gone");
  g = await get(wanted, env, "");
  assert.equal(g.status, 503);
  env.DB.sqlite.exec("ALTER TABLE wanted_topics_gone RENAME TO wanted_topics");
}

// Retention: a row older than a year goes on the next accepted report.
env.DB.sqlite.prepare("INSERT INTO reports (created_at, day, kind, topic, client_hash) VALUES ('2020-01-01T00:00:00Z', '2020-01-01', 'gap', 'old', 'x')").run();
assert.equal((await post(env, { kind: "gap", topic: "fresh topic" })).status, 201);
assert.equal(env.DB.sqlite.prepare("SELECT count(*) AS n FROM reports WHERE day = '2020-01-01'").get().n, 0);

// GET answers cross-origin too.
assert.equal((await mod.onRequestGet()).headers.get("Access-Control-Allow-Origin"), "*");

// Global daily cap.
{
  const capped = { DB: d1(), FEEDBACK_SALT: "s" };
  const today = new Date().toISOString().slice(0, 10);
  const ins = capped.DB.sqlite.prepare("INSERT INTO reports (created_at, day, kind, topic, client_hash) VALUES (?, ?, 'gap', ?, ?)");
  for (let i = 0; i < 3000; i++) ins.run(`${today}T00:00:00Z`, today, `t${i}`, `c${i}`);
  assert.equal((await post(capped, { kind: "gap", topic: "over the cap" })).status, 429);
  assert.equal((await get(report, capped, "kind=gap&topic=over")).status, 429);
}

// Per-client daily limit.
const flood = { DB: d1(), FEEDBACK_SALT: "s" };
for (let i = 0; i < 30; i++) assert.equal((await post(flood, { kind: "gap", topic: `topic ${i}` })).status, 201);
assert.equal((await post(flood, { kind: "gap", topic: "one more" })).status, 429);
assert.equal((await post(flood, { kind: "gap", topic: "other client" }, "198.51.100.9")).status, 201);

// Search uses deployed assets; only a successful zero-result search records a gap.
{
  const index = { docs: [
    { location: "kafka/groups/", title: "Kafka groups", text: "Consumer coordination" },
    { location: "kafka/groups/#share", title: "Share groups", text: "Kafka consumer coordination" },
    { location: "https://evil.example/a/b/", title: "Kafka", text: "coordination" },
  ] };
  const e = { DB: d1(), FEEDBACK_SALT: "s", ASSETS: { async fetch(url) {
    assert.equal(new URL(url).pathname, "/search/search_index.json");
    return Response.json(index);
  } } };
  let found = await get(search, e, "q=Kafka+coordination");
  assert.equal(found.status, 200);
  assert.equal(found.body.total, 1);
  assert.equal(e.DB.sqlite.prepare("SELECT count(*) AS n FROM reports").get().n, 0);
  for (const q of ["", "q=+++", "q=%21%21", "q=" + "a".repeat(201)]) {
    assert.equal((await get(search, e, q)).status, 400);
  }
  found = await get(search, e, "q=missing+topic&channel=mcp-search");
  assert.equal(found.status, 200);
  assert.equal(found.body.gap.recorded, true);
  const id = found.body.gap.id;
  assert.equal(e.DB.sqlite.prepare("SELECT channel FROM reports WHERE id=?").get(id).channel, "search");
  assert.equal((await get(search, e, "q=missing+topic")).body.gap.id, id);
  assert.equal(e.DB.sqlite.prepare("SELECT count(*) AS n FROM reports").get().n, 1);
  assert.equal((await get(search, { ...e, FEEDBACK_SALT: undefined }, "q=another+gap")).status, 503);
  const broken = { ...e, ASSETS: { async fetch() { return new Response("missing", { status: 404 }); } } };
  assert.equal((await get(search, broken, "q=unavailable")).status, 503);
  broken.ASSETS.fetch = async () => Response.json({ docs: [] });
  assert.equal((await get(search, broken, "q=unavailable")).status, 503);
  assert.equal(e.DB.sqlite.prepare("SELECT count(*) AS n FROM reports").get().n, 1);
}

// Widening channel CHECK preserves all fields, indexes and deleted-ID high water.
for (const empty of [false, true]) {
  const m = new DatabaseSync(":memory:");
  for (const file of ["0001_feedback.sql", "0002_reports.sql", "0003_wanted_topics.sql"]) {
    m.exec(readFileSync(root + "migrations/" + file, "utf8"));
  }
  m.exec("INSERT INTO reports(id,created_at,day,kind,topic,client_hash,status,public_title,result_url) VALUES(91,'t','d','gap','topic','hash','done','Reviewed','https://happyin.space/kafka/groups/'); INSERT INTO reports(id,created_at,day,kind,client_hash) VALUES(100,'t','d','gap','h'); DELETE FROM reports WHERE id=100;");
  if (empty) m.exec("DELETE FROM reports");
  const before = m.prepare("SELECT * FROM reports").all();
  m.exec(readFileSync(root + "migrations/0004_search_channels.sql", "utf8"));
  assert.deepEqual(m.prepare("SELECT * FROM reports").all(), before);
  assert.deepEqual(m.prepare("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='reports' ORDER BY name").all().map(r => r.name), ["reports_client_day", "reports_day", "reports_status"]);
  const insert = m.prepare("INSERT INTO reports(created_at,day,kind,client_hash,channel) VALUES('t','d','gap','h',?)");
  assert.ok(Number(insert.run("search").lastInsertRowid) > 100);
  insert.run("mcp-search");
  assert.throws(() => insert.run("untrusted"));
}

// MCP provenance is authenticated and cannot be selected by a public caller.
{
  const e = { DB: d1(), FEEDBACK_SALT: "s", MCP_GAP_INGEST_SECRET: "test-only-secret" };
  const send = async (auth, body, target = e) => mcpGap.onRequestPost({ env: target, request: new Request(
    "https://happyin.space/api/feedback/internal/mcp-gap", { method: "POST",
      headers: { Authorization: auth, "Content-Type": "application/json" }, body: JSON.stringify(body) }) });
  assert.equal((await send("", { topic: "missing" })).status, 401);
  assert.equal((await send("Bearer wrong", { topic: "missing" })).status, 401);
  assert.equal((await send("Bearer test-only-secret", { topic: "missing", channel: "post" })).status, 400);
  assert.equal((await send("Bearer test-only-secret", { topic: "missing" }, { ...e, MCP_GAP_INGEST_SECRET: undefined })).status, 503);
  assert.equal(e.DB.sqlite.prepare("SELECT count(*) AS n FROM reports").get().n, 0);
  assert.equal((await send("Bearer test-only-secret", { topic: "missing" })).status, 201);
  assert.equal((await send("Bearer test-only-secret", { topic: "missing" })).status, 200);
  assert.deepEqual({ ...e.DB.sqlite.prepare("SELECT channel,agent FROM reports").get() },
    { channel: "mcp-search", agent: "diffusion-love-mcp" });
  assert.equal(mcpGap.onRequest().status, 405);
}

console.log("agent contact and search endpoints: all checks passed");
