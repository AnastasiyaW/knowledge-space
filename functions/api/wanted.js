/**
 * GET /api/wanted - what the maintainer wants researched, so a visiting agent that knows the
 * subject can contribute a kind=finding report. Two sources, both worded by the maintainer:
 *   - wanted_topics: articles agents read that have gone stale, and topics added by hand
 *     (migrations/0003_wanted_topics.sql; filled by the maintainer's daily tooling)
 *   - reports accepted at triage, under the title written then (feedback_queue.py --title)
 * Sender text never appears here, so this list cannot relay one sender's words to other agents.
 */
import { SITE, json } from "../_feedback_core.js";

export async function onRequestGet(context) {
  const { env } = context;
  if (!env.DB) return json(503, { error: "feedback storage is not configured" });
  try {
    return json(200, await listWanted(env.DB));
  } catch (e) {
    // A missing table (migration not applied) is a deploy error: say so, never an empty list.
    return json(503, { error: "wanted list unavailable", detail: String(e.message || e).slice(0, 200) });
  }
}

async function listWanted(db) {
  const topics = await db
    .prepare(
      `SELECT title AS topic, domain, article, why, substr(added_at, 1, 10) AS since
         FROM wanted_topics WHERE status = 'open' ORDER BY added_at, id LIMIT 50`
    )
    .all();
  const asked = await db
    .prepare(
      `SELECT public_title AS topic, min(day) AS since, count(*) AS asked
         FROM reports WHERE status = 'accepted' AND public_title IS NOT NULL
        GROUP BY public_title ORDER BY asked DESC, since LIMIT 50`
    )
    .all();
  const wanted = [
    ...topics.results.map((t) => ({
      topic: t.topic, since: t.since, why: t.why,
      ...(t.article ? { article: `${SITE}/${t.article}/` } : {}),
      ...(t.domain ? { domain: t.domain } : {}),
    })),
    ...asked.results.map((t) => ({ topic: t.topic, since: t.since, asked: t.asked })),
  ];
  return {
    wanted,
    how_to_help: `Send verified facts for one of these topics: POST ${SITE}/api/feedback or GET ${SITE}/api/feedback/report `
      + "with kind=finding, topic, detail (the facts, with versions and dates) and source_url (primary source). "
      + "For an existing article, also pass article. Findings are checked against their sources before anything is written.",
  };
}
