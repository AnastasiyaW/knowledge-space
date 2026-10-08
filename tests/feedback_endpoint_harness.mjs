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

console.log("agent contact endpoints: all checks passed");
