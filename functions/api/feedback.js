/**
 * Agent feedback endpoint (core and the other contact endpoints: functions/_feedback_core.js).
 *
 *   GET  /api/feedback   -> the contract as JSON, so an agent can learn it without docs
 *   POST /api/feedback   -> stores one report
 */
import { CONTRACT, HEADERS, LIMITS, json, storeReport } from "../_feedback_core.js";

export { normaliseArticle, validate } from "../_feedback_core.js";

export async function onRequestOptions() {
  return new Response(null, { headers: HEADERS });
}

export async function onRequestGet() {
  return json(200, CONTRACT);
}

export async function onRequestPost(context) {
  const { request, env } = context;
  if (!env.DB || !env.FEEDBACK_SALT) return json(503, { error: "feedback storage is not configured" });
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
  const { status, body: reply } = await storeReport(env, request, body, "post");
  return json(status, reply);
}
