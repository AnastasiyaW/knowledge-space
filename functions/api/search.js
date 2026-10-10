import { json, LIMITS, SITE, storeReport } from "../_feedback_core.js";

// Uses the same deployed MkDocs index as the site's browser search. No remote URL
// or channel supplied by the caller is used to select storage or fetch a resource.
export async function onRequestGet({ request, env }) {
  const query = (new URL(request.url).searchParams.get("q") || "").trim();
  const terms = [...new Set(query.toLowerCase().match(/[\p{L}\p{N}]+/gu) || [])];
  if (!terms.length || query.length > LIMITS.topic) {
    return json(400, { error: `q must contain searchable text, at most ${LIMITS.topic} characters` });
  }
  let results;
  try {
    const response = await env.ASSETS.fetch(new URL("/search/search_index.json", request.url));
    if (!response.ok) throw new Error("index unavailable");
    const index = await response.json();
    if (!Array.isArray(index.docs) || !index.docs.length) throw new Error("index missing documents");
    results = searchDocuments(index.docs, terms);
  } catch {
    return json(503, { error: "search index is unavailable; no gap was recorded" });
  }
  const body = { query, total: results.length, results: results.slice(0, 10) };
  if (results.length) return json(200, body);
  try {
    const saved = await storeReport(env, request, { kind: "gap", topic: query }, "search");
    if (saved.status >= 400) return json(saved.status, { ...body, gap: { recorded: false, error: saved.body.error } });
    return json(200, { ...body, gap: { recorded: true, id: saved.body.id, status_url: saved.body.status_url } });
  } catch {
    return json(503, { ...body, gap: { recorded: false, error: "gap storage is unavailable" } });
  }
}

export function searchDocuments(docs, terms) {
  const articles = new Map();
  for (const doc of docs) {
    if (typeof doc.location !== "string" || typeof doc.title !== "string" || typeof doc.text !== "string") {
      throw new Error("invalid search document");
    }
    const url = new URL(doc.location, SITE + "/");
    if (url.origin !== SITE || !/^\/[a-z0-9-]+\/[a-z0-9-]+\/$/.test(url.pathname)) continue;
    const title = doc.title.toLowerCase();
    const text = doc.text.toLowerCase();
    if (!terms.every((term) => title.includes(term) || text.includes(term))) continue;
    const score = terms.reduce((sum, term) => sum + (title.includes(term) ? 2 : 1), 0);
    const hit = { title: doc.title, url: url.href, excerpt: doc.text.replace(/\s+/g, " ").slice(0, 300), score };
    if (!articles.has(url.pathname) || articles.get(url.pathname).score < score) articles.set(url.pathname, hit);
  }
  return [...articles.values()].sort((a, b) => b.score - a.score || a.url.localeCompare(b.url));
}
