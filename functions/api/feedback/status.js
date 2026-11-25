/**
 * GET /api/feedback/status?id=N - what happened to a report. Never returns sender text: only the
 * kind, the day, the triage state, the owner-written title and the PR or article that closed it.
 */
import { json } from "../../_feedback_core.js";

const MEANING = {
  new: "received, waiting for triage",
  accepted: "accepted: it will be researched from primary sources",
  rejected: "not taken (off-topic, duplicate, or not something this knowledge base covers)",
  done: "done: see result_url",
};

export async function onRequestGet(context) {
  const { request, env } = context;
  if (!env.DB) return json(503, { error: "feedback storage is not configured" });
  const id = Number(new URL(request.url).searchParams.get("id"));
  if (!Number.isInteger(id) || id < 1) return json(400, { error: "id must be a positive integer" });
  const row = await env.DB
    .prepare("SELECT id, kind, day, status, public_title, result_url FROM reports WHERE id = ?")
    .bind(id)
    .first();
  if (!row) return json(404, { error: "no such report (reports are kept for 12 months)" });
  return json(200, { ...row, meaning: MEANING[row.status] });
}
