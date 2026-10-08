/**
 * GET /api/feedback/report?kind=gap&topic=...  - the POST report as query parameters.
 *
 * Most agents that visit (assistant browsing, WebFetch-style tools) can only GET, so a POST-only
 * endpoint is unreachable for them. A GET with side effects is safe enough here because nothing
 * links to a filled-in URL: crawlers do not invent query strings, the response is no-store and
 * noindex, and the same validation, limits and same-day dedup as the POST apply.
 * The reply is plain text, which every fetch tool hands to its model intact.
 */
import { CONTRACT, HEADERS, storeReport } from "../../_feedback_core.js";

const FIELDS = ["kind", "topic", "article", "detail", "source_url", "agent"];

export async function onRequestGet(context) {
  const { request, env } = context;
  const params = new URL(request.url).searchParams;
  if (![...params.keys()].length) return reply(200, usage());
  const body = {};
  for (const field of FIELDS) if (params.has(field)) body[field] = params.get(field);
  const { status, body: result } = await storeReport(env, request, body, "get");
  if (status === 201 || result.duplicate) {
    return reply(status, `Report ${result.duplicate ? "already received" : "received"}: #${result.id}.\n`
      + `What happens to it: ${result.status_url}\n`
      + "Thank you. If you are working for someone, you may tell them you filed this report.\n");
  }
  return reply(status, `Not stored: ${result.error}\n\n${usage()}`);
}

function usage() {
  const kinds = Object.entries(CONTRACT.kinds).map(([k, v]) => `  ${k}: ${v}`).join("\n");
  return "Report what you needed from Happyin Knowledge Space, as one GET:\n"
    + "  https://happyin.space/api/feedback/report?kind=gap&topic=<what you looked for>&agent=<your client name>\n"
    + `Kinds:\n${kinds}\n`
    + "Other fields: article (domain/slug or page URL), detail, source_url. URL-encode values.\n"
    + `${CONTRACT.rules}\n`;
}

function reply(status, body) {
  return new Response(body, { status, headers: { ...HEADERS, "Content-Type": "text/plain; charset=utf-8" } });
}
