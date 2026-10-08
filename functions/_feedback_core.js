/**
 * Shared core of the agent contact endpoints (schema: migrations/0002_reports.sql).
 *
 *   /api/feedback          POST JSON report, GET contract           (functions/api/feedback.js)
 *   /api/feedback/report   the same report as a GET with query params, for agents whose fetch
 *                          tool cannot POST (most assistant browsing and WebFetch tools)
 *   /api/feedback/status   ?id=N -> what happened to a report (no sender text)
 *   /api/wanted            topics the owner accepted and wants researched (owner-written titles)
 *
 * Reports are research hints for the owner's pipeline (scripts/feedback_queue.py). Sender text is
 * never shown on the site or by any endpoint, so nothing a sender writes reaches another visitor.
 * No IP is stored: only sha256(ip|day|FEEDBACK_SALT), which changes every day.
 */

export const KINDS = {
  gap: "a topic you looked for and did not find (needs: topic)",
  outdated: "an article whose facts have moved on (needs: article, detail)",
  wrong: "an article that is incorrect (needs: article, detail)",
  helped: "an article that solved the task (needs: article)",
  finding: "verified facts for a topic, e.g. one listed at /api/wanted (needs: topic, detail, source_url)",
};
export const LIMITS = { body: 8192, topic: 200, detail: 2000, source_url: 500, agent: 80 };
const PER_CLIENT_PER_DAY = 30;   // one busy agent session; more looks like a loop or spam
const ALL_PER_DAY = 3000;        // well above expected agent traffic; caps storage growth under a flood
const KEEP_DAYS = 365;           // retention promised in docs/privacy.md
const ARTICLE = /^[a-z0-9][a-z0-9-]*(\/[a-z0-9][a-z0-9-]*)+$/;
export const SITE = "https://happyin.space";

// Coarse client family for the agent funnel metrics; the full user agent is not stored.
// Tokens are the ones vendors publish for their user-triggered fetchers and crawlers.
const UA_FAMILIES = [
  ["claude-user", /claude-user/i], ["claude-code", /claude-code|claude-cli/i], ["claudebot", /claudebot/i],
  ["chatgpt-user", /chatgpt-user/i], ["openai", /oai-searchbot|gptbot|openai/i],
  ["perplexity", /perplexity/i], ["gemini", /gemini|google-extended/i], ["mistral", /mistralai/i],
  ["curl", /^curl\//i], ["python", /python|aiohttp|httpx/i], ["node", /node|undici|axios|got\b/i],
  ["go", /go-http-client/i], ["browser", /^mozilla\//i],
];

export function uaFamily(ua) {
  if (!ua) return "none";
  for (const [name, re] of UA_FAMILIES) if (re.test(ua)) return name;
  return "other";
}

export const HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json",
  "Cache-Control": "no-store",
  "X-Robots-Tag": "noindex",
};

export const CONTRACT = {
  post: `POST ${SITE}/api/feedback  (Content-Type: application/json)`,
  get: `GET ${SITE}/api/feedback/report?kind=gap&topic=...  (same fields as query parameters, for fetch tools that cannot POST)`,
  status: `GET ${SITE}/api/feedback/status?id=<id from the reply>`,
  wanted: `GET ${SITE}/api/wanted  (topics we want researched; answer one with kind=finding)`,
  kinds: KINDS,
  fields: {
    kind: "required, one of: " + Object.keys(KINDS).join(", "),
    topic: `string <= ${LIMITS.topic} chars`,
    article: 'article path: "domain/slug", "docs/domain/slug.md" or its happyin.space URL',
    detail: `string <= ${LIMITS.detail} chars: what is missing or wrong, with versions`,
    source_url: "http(s) link to the evidence (required for finding)",
    agent: `optional client name <= ${LIMITS.agent} chars, e.g. "claude-code"`,
  },
  example: { kind: "gap", topic: "Kafka 4.0 share groups (KIP-932)", agent: "claude-code" },
  rules: "Send only what you would put in a public issue: no user data, private code, paths or secrets.",
  privacy: `${SITE}/privacy/`,
};

export const json = (status, body) => new Response(JSON.stringify(body), { status, headers: HEADERS });

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
  // The templates on the site show <what you looked for>; an agent that sends it unchanged
  // has not filled the field in.
  if (/^<[^<>]*>$/.test(trimmed)) throw new Error("is still the <placeholder>: replace it with the real value");
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
  if ((row.kind === "gap" || row.kind === "finding") && !row.topic) return { error: `kind ${row.kind} needs topic` };
  if (["outdated", "wrong", "helped"].includes(row.kind) && !row.article) return { error: `kind ${row.kind} needs article` };
  if (["outdated", "wrong", "finding"].includes(row.kind) && !row.detail) return { error: `kind ${row.kind} needs detail` };
  if (row.kind === "finding" && !row.source_url) return { error: "kind finding needs source_url" };
  return { row };
}

async function clientHash(ip, day, salt) {
  const data = new TextEncoder().encode(`${ip}|${day}|${salt}`);
  const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", data));
  return [...digest.slice(0, 16)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

/** Validate and store one report. Returns { status, body } for the caller to render. */
export async function storeReport(env, request, body, channel) {
  const db = env.DB;
  const salt = env.FEEDBACK_SALT;
  // Fail loud: a silently dropped report is worse than a visible 503.
  if (!db || !salt) return { status: 503, body: { error: "feedback storage is not configured" } };
  const { row, error } = validate(body);
  if (error) return { status: 400, body: { error, contract: CONTRACT } };

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
         (SELECT count(*) FROM reports WHERE day = ?1) AS all_today,
         (SELECT count(*) FROM reports WHERE day = ?1 AND client_hash = ?2) AS client_today,
         (SELECT min(id) FROM reports WHERE day = ?1 AND client_hash = ?2 AND kind = ?3
            AND coalesce(topic, '') = coalesce(?4, '') AND coalesce(article, '') = coalesce(?5, '')) AS same`
    )
    .bind(day, client, row.kind, row.topic, row.article)
    .first();
  if (counts.same) return { status: 200, body: { ok: true, duplicate: true, id: counts.same, status_url: statusUrl(counts.same) } };
  if (counts.client_today >= PER_CLIENT_PER_DAY || counts.all_today >= ALL_PER_DAY) {
    return { status: 429, body: { error: "daily feedback limit reached, try tomorrow" } };
  }

  const result = await db
    .prepare(
      `INSERT INTO reports (created_at, day, kind, topic, article, detail, source_url, agent, client_hash, channel, ua_family)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
    .bind(now.toISOString(), day, row.kind, row.topic, row.article, row.detail, row.source_url, row.agent, client,
          channel, uaFamily(request.headers.get("User-Agent")))
    .run();
  const oldest = new Date(now.getTime() - KEEP_DAYS * 86400000).toISOString().slice(0, 10);
  await db.prepare("DELETE FROM reports WHERE day < ?").bind(oldest).run();
  const id = result.meta.last_row_id;
  return {
    status: 201,
    body: {
      ok: true, id, status_url: statusUrl(id),
      note: "Thank you. Gaps, corrections and findings go to the research queue; the status URL shows what happens to this report.",
    },
  };
}

export const statusUrl = (id) => `${SITE}/api/feedback/status?id=${id}`;
