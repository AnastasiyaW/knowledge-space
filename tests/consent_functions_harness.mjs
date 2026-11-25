// Checks functions/api/consent-region.js and functions/ads.txt.js. Exit 0 = every check passed.
// Usage: node tests/consent_functions_harness.mjs
import assert from "node:assert/strict";

const region = await import(new URL("../functions/api/consent-region.js", import.meta.url));
const adsTxt = await import(new URL("../functions/ads.txt.js", import.meta.url));

async function regionFor(country) {
  const request = { url: "https://happyin.space/api/consent-region", cf: country === undefined ? undefined : { country } };
  const response = region.onRequestGet({ request });
  assert.match(response.headers.get("Cache-Control"), /^private\b/, "the answer must never sit in a shared cache");
  const body = await response.json();
  assert.deepEqual(Object.keys(body), ["consent_required"], "the country itself is never echoed back");
  return body.consent_required;
}

for (const code of ["DE", "FR", "GB", "CH", "NO", "IS", "LI", "de"]) {
  assert.equal(await regionFor(code), true, `${code} needs the prompt`);
}
for (const code of ["US", "RU", "CN", "BR", "JP"]) {
  assert.equal(await regionFor(code), false, `${code} does not need the prompt`);
}
for (const code of [undefined, "", "XX", "T1"]) {
  assert.equal(await regionFor(code), true, `unknown country ${JSON.stringify(code)} fails safe to the prompt`);
}

function assets(html, ok = true) {
  return { ASSETS: { fetch: async () => ({ ok, text: async () => html }) } };
}
const request = { url: "https://happyin.space/ads.txt" };

{
  const response = await adsTxt.onRequestGet({ request, env: assets("<html><head></head></html>") });
  assert.equal(response.status, 404, "no publisher id -> no ads.txt");
}
{
  const html = '<head><meta name="google-adsense-account" content="ca-pub-1234567890123456"></head>';
  const response = await adsTxt.onRequestGet({ request, env: assets(html) });
  assert.equal(response.status, 200);
  assert.equal(await response.text(), "google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0\n");
  assert.match(response.headers.get("Content-Type"), /^text\/plain/);
}
{
  // The form the minified build actually ships.
  const html = "<head><meta name=google-adsense-account content=ca-pub-0000000000000000><meta charset=utf-8>";
  const response = await adsTxt.onRequestGet({ request, env: assets(html) });
  assert.equal(await response.text(), "google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n");
}
{
  const html = '<meta name="google-adsense-account" content="ca-pub-12345678901234567890123">';
  const response = await adsTxt.onRequestGet({ request, env: assets(html) });
  assert.equal(response.status, 404, "an over-long id is not truncated into a valid-looking one");
}
{
  const html = '<meta name="google-adsense-account" content="ca-pub-<script>">';
  const response = await adsTxt.onRequestGet({ request, env: assets(html) });
  assert.equal(response.status, 404, "a malformed id is not published");
}
{
  const response = await adsTxt.onRequestGet({ request, env: { ASSETS: { fetch: async () => { throw new Error("down"); } } } });
  assert.equal(response.status, 404, "an asset error yields no ads.txt, not a crash");
}

console.log("PASS consent and ads.txt functions");
