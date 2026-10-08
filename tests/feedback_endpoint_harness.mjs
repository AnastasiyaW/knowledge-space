// Runs functions/api/feedback.js against a real SQLite database built from
// migrations/0001_feedback.sql, behind a minimal D1-shaped adapter. Exit 0 = every check passed.
// Usage: node tests/feedback_endpoint_harness.mjs
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const mod = await import(new URL("../functions/api/feedback.js", import.meta.url));

function d1() {
  const sqlite = new DatabaseSync(":memory:");
  sqlite.exec(readFileSync(root + "migrations/0001_feedback.sql", "utf8"));
  const db = {
    sqlite,
    prepare(sql) {
      const stmt = sqlite.prepare(sql);
      let args = [];
      const bound = {
        bind(...values) { args = values; return bound; },
        async first() { return stmt.get(...args) ?? null; },
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

async function post(env, body, ip = "203.0.113.7") {
  const request = new Request("https://happyin.space/api/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json", "CF-Connecting-IP": ip },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
  const res = await mod.onRequestPost({ request, env });
  return { status: res.status, body: await res.json() };
}

const env = { DB: d1(), FEEDBACK_SALT: "test-salt" };

// Contract is discoverable.
const contract = await (await mod.onRequestGet()).json();
assert.deepEqual(Object.keys(contract.kinds), ["gap", "outdated", "wrong", "helped"]);

// Fail loud without storage or salt (negative control: no silent drop).
assert.equal((await post({ DB: env.DB }, { kind: "gap", topic: "x y z" })).status, 503);
assert.equal((await post({ FEEDBACK_SALT: "s" }, { kind: "gap", topic: "x y z" })).status, 503);

// Valid rows land, with article normalised and no IP stored.
let r = await post(env, { kind: "gap", topic: "Kafka share groups", agent: "claude-code" });
assert.equal(r.status, 201, JSON.stringify(r.body));
r = await post(env, { kind: "outdated", article: "https://happyin.space/kafka/consumer-groups/", detail: "KIP-848 is GA in 4.0" });
assert.equal(r.status, 201, JSON.stringify(r.body));
r = await post(env, { kind: "helped", article: "docs/python/asyncio-basics.md" });
assert.equal(r.status, 201);
const rows = env.DB.sqlite.prepare("SELECT * FROM feedback ORDER BY id").all();
assert.deepEqual(rows.map((x) => x.article), [null, "kafka/consumer-groups", "python/asyncio-basics"]);
assert.ok(rows.every((x) => x.status === "new" && /^[0-9a-f]{32}$/.test(x.client_hash)));
assert.ok(!JSON.stringify(rows).includes("203.0.113.7"), "raw IP must not be stored");

// Same report twice in a day is a duplicate, not a second row.
r = await post(env, { kind: "gap", topic: "Kafka share groups" });
assert.deepEqual(r.body, { ok: true, duplicate: true });
assert.equal(env.DB.sqlite.prepare("SELECT count(*) AS n FROM feedback").get().n, 3);

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
];
for (const body of bad) assert.equal((await post(env, body)).status, 400, JSON.stringify(body));
assert.equal((await post(env, JSON.stringify({ kind: "gap", topic: "x".repeat(9000) }))).status, 413);

// Per-client daily limit.
const flood = { DB: d1(), FEEDBACK_SALT: "s" };
for (let i = 0; i < 30; i++) assert.equal((await post(flood, { kind: "gap", topic: `topic ${i}` })).status, 201);
assert.equal((await post(flood, { kind: "gap", topic: "one more" })).status, 429);
assert.equal((await post(flood, { kind: "gap", topic: "other client" }, "198.51.100.9")).status, 201);

console.log("feedback endpoint: all checks passed");
