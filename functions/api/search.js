import { json, LIMITS, SITE, storeReport } from "../_feedback_core.js";

// Static assets belong to a deployment. Share parsing across concurrent requests
// to the same binding, and evict failures so a transient read can be retried.
const indexes = new WeakMap();
function loadIndex(assets, origin) {
  if (!indexes.has(assets)) {
    const pending = (async () => {
      const response = await assets.fetch(new URL("/search/search_index.json", origin));
      if (!response.ok) throw new Error("index unavailable");
      const index = await response.json();
      if (!Array.isArray(index.docs) || !index.docs.length) throw new Error("index missing documents");
      return prepareDocuments(index.docs);
    })().catch(error => { indexes.delete(assets); throw error; });
    indexes.set(assets, pending);
  }
  return indexes.get(assets);
}

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
    results = searchPrepared(await loadIndex(env.ASSETS, request.url), terms);
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
  return searchPrepared(prepareDocuments(docs), terms);
}

function prepareDocuments(docs) {
  const prepared = [];
  for (const doc of docs) {
    if (typeof doc.location !== "string" || typeof doc.title !== "string" || typeof doc.text !== "string") {
      throw new Error("invalid search document");
    }
    const url = new URL(doc.location, SITE + "/");
    // The index is authoritative: article URLs include nested CWE paths, case
    // and plus signs. Do not invent a narrower slug grammar than the builder.
    if (url.origin !== SITE || url.pathname.split("/").filter(Boolean).length < 2) continue;
    prepared.push({ pathname: url.pathname, url: url.href, title: doc.title,
      lowerTitle: doc.title.toLowerCase(), text: doc.text.toLowerCase(),
      excerpt: doc.text.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim().slice(0, 300) });
  }
  return prepared;
}

function searchPrepared(docs, terms) {
  const articles = new Map();
  for (const doc of docs) {
    const title = doc.lowerTitle;
    const text = doc.text;
    const matched = terms.filter((term) => title.includes(term) || text.includes(term));
    if (!matched.length) continue;
    const score = matched.reduce((sum, term) => sum + (title.includes(term) ? 2 : 1), 0);
    const hit = { title: doc.title, url: doc.url, excerpt: doc.excerpt, score };
    const article = articles.get(doc.pathname) || { hit, matched: new Set() };
    for (const term of matched) article.matched.add(term);
    if (article.hit.score < score) article.hit = hit;
    articles.set(doc.pathname, article);
  }
  // MkDocs emits separate section documents. A query spanning two sections is
  // still covered by their article and must not create a research gap.
  return [...articles.values()].filter(a => a.matched.size === terms.length)
    .map(a => a.hit).sort((a, b) => b.score - a.score || a.url.localeCompare(b.url));
}
