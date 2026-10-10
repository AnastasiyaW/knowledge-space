import { HEADERS, LIMITS, json, storeReport } from "../../../_feedback_core.js";

// Service-only ingestion: provenance comes from a shared secret, never a public
// channel query parameter. Configure the same secret on the MCP Worker and Pages.
export async function onRequestPost({ request, env }) {
  const secret = env.MCP_GAP_INGEST_SECRET;
  if (!secret) return json(503, { error: "MCP gap ingestion is not configured" });
  const supplied = request.headers.get("Authorization") || "";
  const expected = `Bearer ${secret}`;
  // Hash both values first to compare fixed-length buffers without prefix timing.
  const hash = async (value) => new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value)));
  const [a, b] = await Promise.all([hash(supplied), hash(expected)]);
  let difference = 0;
  for (let i = 0; i < a.length; i++) difference |= a[i] ^ b[i];
  if (difference) return json(401, { error: "unauthorized" });
  if (!request.headers.get("Content-Type")?.toLowerCase().startsWith("application/json")) {
    return json(415, { error: "Content-Type must be application/json" });
  }
  if (Number(request.headers.get("Content-Length")) > LIMITS.body) return json(413, { error: "body too large" });
  const raw = await request.text();
  if (new TextEncoder().encode(raw).length > LIMITS.body) return json(413, { error: "body too large" });
  let body;
  try { body = JSON.parse(raw); } catch { return json(400, { error: "invalid JSON" }); }
  if (!body || Array.isArray(body) || typeof body !== "object" || Object.keys(body).some(k => k !== "topic")) {
    return json(400, { error: "body must contain only topic" });
  }
  try {
    const result = await storeReport(env, request, { kind: "gap", topic: body.topic, agent: "diffusion-love-mcp" }, "mcp-search");
    return json(result.status, result.body);
  } catch {
    return json(503, { error: "gap storage is unavailable" });
  }
}

export function onRequest() {
  return new Response(JSON.stringify({ error: "POST required" }), {
    status: 405, headers: { ...HEADERS, Allow: "POST" },
  });
}
