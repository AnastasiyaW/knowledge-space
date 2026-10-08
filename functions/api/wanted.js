/**
 * GET /api/wanted - topics the owner accepted and wants researched, so a visiting agent that
 * knows the subject can contribute a kind=finding report. Titles are written by the owner's
 * triage (feedback_queue.py triage --title), never copied from sender text, so this list cannot
 * relay one sender's words to other agents.
 */
import { SITE, json } from "../_feedback_core.js";

export async function onRequestGet(context) {
  const { env } = context;
  if (!env.DB) return json(503, { error: "feedback storage is not configured" });
  const { results } = await env.DB
    .prepare(
      `SELECT public_title AS topic, min(day) AS since, count(*) AS asked
         FROM reports WHERE status = 'accepted' AND public_title IS NOT NULL
        GROUP BY public_title ORDER BY asked DESC, since LIMIT 50`
    )
    .all();
  return json(200, {
    wanted: results,
    how_to_help: `Send verified facts for one of these topics: POST ${SITE}/api/feedback or GET ${SITE}/api/feedback/report `
      + "with kind=finding, topic, detail (the facts, with versions) and source_url (primary source). "
      + "Findings are checked against their sources before anything is written.",
  });
}
