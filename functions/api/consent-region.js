/**
 * GET /api/consent-region -> {"consent_required": true|false}
 * Tells the page whether to show the cookie prompt. The country comes from Cloudflare's
 * request.cf and is neither stored nor echoed back; "private" keeps the answer out of
 * shared caches, so one visitor's answer is never served to another.
 */
import { consentRequired } from "../_consent_regions.js";

export function onRequestGet({ request }) {
  const country = request.cf && request.cf.country;
  return new Response(JSON.stringify({ consent_required: consentRequired(country) }), {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "private, max-age=3600",
      "X-Robots-Tag": "noindex",
    },
  });
}
