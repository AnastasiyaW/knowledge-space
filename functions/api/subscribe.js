/**
 * Email subscription endpoint.
 * Stores emails in Cloudflare D1 database.
 * POST /api/subscribe { email: "user@example.com" }
 */

const CORS = {
  "Access-Control-Allow-Origin": "https://happyin.space",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json",
};

export async function onRequestOptions() {
  return new Response(null, { headers: CORS });
}

export async function onRequestPost(context) {
  try {
    const body = await context.request.json();
    const email = (body.email || "").trim().toLowerCase();

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return new Response(
        JSON.stringify({ error: "Invalid email address" }),
        { status: 400, headers: CORS }
      );
    }

    // Rate limit: check referer
    const referer = context.request.headers.get("Referer") || "";
    if (!referer.includes("happyin.space") && !referer.includes("localhost")) {
      return new Response(
        JSON.stringify({ error: "Forbidden" }),
        { status: 403, headers: CORS }
      );
    }

    // Generate unsubscribe token
    const token = crypto.randomUUID();
    const ip = context.request.headers.get("CF-Connecting-IP") || "";

    // Store in D1
    const db = context.env.DB;
    if (db) {
      await db
        .prepare(
          `INSERT OR IGNORE INTO subscribers (email, subscribed_at, ip_address, unsub_token, consent_text, status)
           VALUES (?, datetime('now'), ?, ?, 'v1', 'active')`
        )
        .bind(email, ip, token)
        .run();
    } else {
      // Fallback: log to console if D1 not configured yet
      console.log(`SUBSCRIBE: ${email} from ${ip} at ${new Date().toISOString()}`);
    }

    return new Response(
      JSON.stringify({ ok: true }),
      { status: 200, headers: CORS }
    );
  } catch (e) {
    return new Response(
      JSON.stringify({ error: "Server error" }),
      { status: 500, headers: CORS }
    );
  }
}
