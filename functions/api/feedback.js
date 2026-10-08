/**
 * Agent feedback endpoint: what was missing, outdated or wrong, and which article helped.
 *
 *   GET  /api/feedback   -> this contract as JSON, so an agent can learn it without docs
 *   POST /api/feedback   -> stores one row in D1 (schema: migrations/0001_feedback.sql)
 *
 * Rows are research hints for the owner's pipeline (scripts/feedback_queue.py). They are
 * never shown on the site, so nothing a sender writes reaches another visitor.
 * No IP is stored: only sha256(ip|day|FEEDBACK_SALT), which changes every day.
 * Rows older than KEEP_DAYS are deleted on the next accepted report.
 */

const KINDS = {
  gap: "a topic you looked for and did not find (needs: topic)",
  outdated: "an article whose facts have moved on (needs: article, detail)",
  wrong: "an article that is incorrect (needs: article, detail)",
  helped: "an article that solved the task (needs: article)",
};
const LIMITS = { body: 8192, topic: 200, detail: 2000, source_url: 500, agent: 80 };
const PER_CLIENT_PER_DAY = 30;   // one busy agent session; more looks like a loop or spam
const ALL_PER_DAY = 3000;        // well above expected agent traffic; caps storage growth under a flood
const KEEP_DAYS = 365;           // retention promised in docs/privacy.md
const ARTICLE = /^[a-z0-9][a-z0-9-]*(\/[a-z0-9][a-z0-9-]*)+$/;

const HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json",
};

const CONTRACT = {
  endpoint: "POST https://happyin.space/api/feedback",
  content_type: "application/json",
  kinds: KINDS,
  fields: {
    kind: "required, one of: " + Object.keys(KINDS).join(", "),
    topic: `string <= ${LIMITS.topic} chars`,
    article: 'article path: "domain/slug", "docs/domain/slug.md" or its happyin.space URL',
    detail: `string <= ${LIMITS.detail} chars: what is missing or wrong, with versions`,
    source_url: "optional http(s) link to the evidence",
    agent: `optional client name <= ${LIMITS.agent} chars, e.g. "claude-code"`,
  },
  example: { kind: "gap", topic: "Kafka 4.0 share groups (KIP-932)", agent: "claude-code" },
  privacy: "https://happyin.space/privacy/",
};

const json = (status, body) => new Response(JSON.stringify(body), { status, headers: HEADERS });

export function normaliseArticle(value) {
  if (typeof value !== "string") return null;
  let path = value.trim().toLowerCase();
  path = path.replace(/^https?:\/\/(www\.)?happyin\.space\//, "");
  path = path.replace(/^docs\//, "").replace(/\.md$/, "").replace(/\/index$/, "");
  path = path.replace(/[?#].*$/, "").replace(/\/+$/, "");
  return ARTICLE.test(path) ? path : null;
}

function text(value, max) {
  if (value === undefined || value === null) return null;
  if (typeof value !== "string") throw new Error("must be a string");
  const trimmed = value.trim();
  if (trimmed.length > max) throw new Error(`longer than ${max} characters`);
  return trimmed || null;
}

export function validate(body) {
  if (!body || typeof body !== "object" || Array.isArray(body)) return { error: "body must be a JSON object" };
  if (!Object.hasOwn(KINDS, body.kind)) return { error: "kind must be one of: " + Object.keys(KINDS).join(", ") };
  const row = { kind: body.kind };
  for (const field of ["topic", "detail", "agent", "source_url"]) {
    try {
      row[field] = text(body[field], LIMITS[field]);
    } catch (e) {
      return { error: `${field} ${e.message}` };
    }
  }
  if (row.source_url && !/^https?:\/\/[^\s]+$/i.test(row.source_url)) return { error: "source_url must be an http(s) URL" };
  row.article = null;
  if (body.article !== undefined && body.article !== null && body.article !== "") {
    row.article = normaliseArticle(body.article);
    if (!row.article) return { error: 'article must look like "domain/slug"' };
  }
  if (row.kind === "gap" && !row.topic) return { error: "kind gap needs topic" };
  if (row.kind !== "gap" && !row.article) return { error: `kind ${row.kind} needs article` };
  if ((row.kind === "outdated" || row.kind === "wrong") && !row.detail) return { error: `kind ${row.kind} needs detail` };
  return { row };
}

async function clientHash(ip, day, salt) {
  const data = new TextEncoder().encode(`${ip}|${day}|${salt}`);
  const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", data));
  return [...digest.slice(0, 16)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export async function onRequestOptions() {
  return new Response(null, { headers: HEADERS });
}

export async function onRequestGet() {
  return json(200, CONTRACT);
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB;
  const salt = env.FEEDBACK_SALT;
  // Fail loud: a silently dropped report is worse than a visible 503.
  if (!db || !salt) return json(503, { error: "feedback storage is not configured" });

  const declared = Number(request.headers.get("Content-Length") || 0);
  if (declared > LIMITS.body) return json(413, { error: `body larger than ${LIMITS.body} bytes` });
  const raw = await request.text();   // still checked: Content-Length can be absent (chunked)
  if (raw.length > LIMITS.body) return json(413, { error: `body larger than ${LIMITS.body} bytes` });
  let body;
  try {
    body = JSON.parse(raw);
  } catch {
    return json(400, { error: "body must be JSON", contract: CONTRACT });
  }
  const { row, error } = validate(body);
  if (error) return json(400, { error, contract: CONTRACT });

  const now = new Date();
  const day = now.toISOString().slice(0, 10);
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  const client = await clientHash(ip, day, salt);

  // simplification: count-then-insert is not atomic, so a burst can pass a limit by a few rows,
  // and one sender rotating IPs can use up ALL_PER_DAY (reports then wait for tomorrow; nothing
  // stored is lost). A Durable Object counter or Turnstile would close both if abuse appears.
  const counts = await db
    .prepare(
      `SELECT
         (SELECT count(*) FROM feedback WHERE day = ?1) AS all_today,
         (SELECT count(*) FROM feedback WHERE day = ?1 AND client_hash = ?2) AS client_today,
         (SELECT count(*) FROM feedback WHERE day = ?1 AND client_hash = ?2 AND kind = ?3
            AND coalesce(topic, '') = coalesce(?4, '') AND coalesce(article, '') = coalesce(?5, '')) AS same`
    )
    .bind(day, client, row.kind, row.topic, row.article)
    .first();
  if (counts.same > 0) return json(200, { ok: true, duplicate: true });
  if (counts.client_today >= PER_CLIENT_PER_DAY || counts.all_today >= ALL_PER_DAY) {
    return json(429, { error: "daily feedback limit reached, try tomorrow" });
  }

  const result = await db
    .prepare(
      `INSERT INTO feedback (created_at, day, kind, topic, article, detail, source_url, agent, client_hash)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
    .bind(now.toISOString(), day, row.kind, row.topic, row.article, row.detail, row.source_url, row.agent, client)
    .run();
  const oldest = new Date(now.getTime() - KEEP_DAYS * 86400000).toISOString().slice(0, 10);
  await db.prepare("DELETE FROM feedback WHERE day < ?").bind(oldest).run();
  return json(201, { ok: true, id: result.meta.last_row_id, note: "Thank you. Gaps and corrections go to the research queue." });
}
