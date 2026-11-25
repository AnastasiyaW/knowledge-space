/**
 * GET /ads.txt - the AdSense seller line, derived from the built site so the publisher id
 * has one source: extra.ads.client in mkdocs.yml, which every page publishes as
 * <meta name="google-adsense-account" content="ca-pub-…">. Without that meta on the home
 * page the file does not exist (404): nothing is declared before AdSense is configured.
 * f08c47fec0942fa0 is Google's certification authority id, the fourth field of the line
 * AdSense publishes for every account (IAB ads.txt 1.1).
 */
// The minify plugin drops attribute quotes (measured: <meta name=google-adsense-account
// content=ca-pub-…>), so quotes are optional.
const META = /<meta\s+name=["']?google-adsense-account["']?\s+content=["']?ca-pub-(\d{10,20})["'\s>\/]/;

export async function onRequestGet({ request, env }) {
  let html = "";
  try {
    const home = await env.ASSETS.fetch(new URL("/", request.url));
    if (home.ok) html = await home.text();
  } catch (e) {
    html = "";
  }
  const match = META.exec(html);
  if (!match) {
    return new Response("Not found\n", {
      status: 404,
      headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=300" },
    });
  }
  return new Response(`google.com, pub-${match[1]}, DIRECT, f08c47fec0942fa0\n`, {
    headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "public, max-age=3600" },
  });
}
