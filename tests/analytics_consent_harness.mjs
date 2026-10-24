// Exercises the privacy boundary in docs/javascripts/analytics.js without a browser.
// The tag and the Consent Mode defaults come from overrides/partials/consent-bootstrap.html;
// here window.gtag stands in for that bootstrap.
// Usage: node tests/analytics_consent_harness.mjs
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const root = fileURLToPath(new URL("..", import.meta.url));
const source = fs.readFileSync(path.join(root, "docs", "javascripts", "analytics.js"), "utf8");

function storage(initial = {}) {
  const values = new Map(Object.entries(initial));
  return {
    getItem(key) { return values.has(key) ? values.get(key) : null; },
    setItem(key, value) { values.set(key, String(value)); }
  };
}

async function run({ measurementId = "", adsClient = "", stored = {}, privacySignal = false, cookies = "", region = true, regionFails = false } = {}) {
  const calls = [];
  const fetched = [];
  const listeners = {};
  const cookieWrites = [];
  let cookieValue = cookies;
  const banner = { hidden: true, getAttribute() { return null; }, querySelector() { return null; } };
  const meta = {
    "happyin-ga4-id": measurementId,
    "google-adsense-account": adsClient
  };
  const doc = {
    head: { appendChild() {} },
    addEventListener(type, handler) { listeners[type] = handler; },
    createElement(tag) { return { tagName: tag.toUpperCase() }; },
    getElementById(id) { return id === "ks-analytics-consent" ? banner : null; },
    querySelectorAll() { return []; },
    querySelector(selector) {
      const match = /^meta\[name="([^"]+)"\]$/.exec(selector);
      if (match) return meta[match[1]] ? { getAttribute() { return meta[match[1]]; } } : null;
      if (selector === "[data-ks-article]") return {};
      return null;
    }
  };
  Object.defineProperty(doc, "cookie", {
    get() { return cookieValue; },
    set(value) { cookieWrites.push(value); cookieValue = value; }
  });
  const window = {
    document: doc,
    localStorage: storage(stored),
    sessionStorage: storage(),
    location: { origin: "https://happyin.space", hostname: "happyin.space", pathname: "/llm-agents/test/", search: "?h=kafka+secret+terms" },
    navigator: privacySignal ? { globalPrivacyControl: true } : {},
    fetch(url) {
      fetched.push(url);
      if (regionFails) return Promise.reject(new Error("offline"));
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ consent_required: region }) });
    }
  };
  // The head bootstrap defines gtag; under a privacy signal it still defines it (for the
  // denied defaults) but never loads the tag, so events must be refused by analytics.js.
  window.gtag = function () { calls.push(Array.from(arguments)); };
  vm.runInNewContext(source, { window, Date, encodeURIComponent, setTimeout, clearTimeout, Promise });
  if (listeners.DOMContentLoaded) listeners.DOMContentLoaded();
  await new Promise((resolve) => setTimeout(resolve, 0));
  return { banner, calls, cookieWrites, fetched, window };
}

const events = (calls) => calls.filter((c) => c[0] === "event");
const updates = (calls) => calls.filter((c) => c[0] === "consent" && c[1] === "update");

{
  const { banner, calls, fetched, window } = await run();
  assert.equal(window.HappyinAnalytics.isConfigured(), false, "blank configuration must disable Google");
  assert.equal(fetched.length, 0, "blank configuration must not even ask for the region");
  assert.equal(banner.hidden, true, "blank configuration must not show a prompt");
  assert.equal(window.HappyinAnalytics.setConsent("granted"), false, "nothing to consent to without configuration");
  assert.equal(calls.length, 0);
}

{
  const { banner, calls } = await run({ measurementId: "G-TEST1234", region: true });
  assert.equal(banner.hidden, false, "a consent-region visitor without a choice must see the prompt");
  const view = events(calls).find((c) => c[1] === "page_view");
  assert.ok(view, "the page view is sent; Consent Mode keeps it cookieless until consent");
  assert.equal(view[2].page_location, "https://happyin.space/llm-agents/test/", "query strings must not reach GA");
  assert.equal(JSON.stringify(calls).includes("h=kafka"), false, "a private query must never reach GA");
  const location = calls.find((c) => c[0] === "set" && c[1] && c[1].page_location);
  assert.ok(location, "later hits (code_copy, star clicks) must inherit a query-free page_location");
  assert.equal(location[1].page_location, "https://happyin.space/llm-agents/test/");
}

{
  const { banner } = await run({ measurementId: "G-TEST1234", region: false });
  assert.equal(banner.hidden, true, "outside the consent regions the prompt stays closed");
}

{
  const { banner } = await run({ measurementId: "G-TEST1234", regionFails: true });
  assert.equal(banner.hidden, false, "an unknown region must be treated as a consent region");
}

{
  const { banner, calls, window } = await run({ measurementId: "G-TEST1234", region: true });
  assert.equal(window.HappyinAnalytics.setConsent("granted"), true, "explicit approval must be recorded");
  const grant = updates(calls).at(-1)[2];
  assert.equal(JSON.stringify(grant), JSON.stringify({ analytics_storage: "granted" }), "in a consent region the prompt grants analytics only");
  assert.equal(banner.hidden, true, "the prompt closes after a choice");
  window.HappyinAnalytics.track("newsletter_subscribe", { email: "not-for-analytics@example.test" });
  const newsletter = events(calls).find((c) => c[1] === "newsletter_subscribe");
  assert.ok(newsletter);
  assert.equal(JSON.stringify(newsletter).includes("email"), false, "caller data must not leak into GA events");
}

{
  const { calls, window } = await run({ measurementId: "G-TEST1234", region: false, stored: { ks_consent_v2: "denied" } });
  assert.equal(events(calls).length, 0, "a stored refusal must suppress every event");
  window.HappyinAnalytics.setConsent("granted");
  const grant = updates(calls).at(-1)[2];
  assert.equal(grant.ad_storage, "granted", "outside consent regions allowing again restores every default");
}

{
  const { calls, cookieWrites, window } = await run({ measurementId: "G-TEST1234", region: false, cookies: "_ga=old; _ga_TEST1234=old; __gads=old; keep=1" });
  assert.equal(window.HappyinAnalytics.setConsent("denied"), true, "everyone can withdraw");
  const deny = updates(calls).at(-1)[2];
  assert.equal(JSON.stringify(deny), JSON.stringify({ ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied" }));
  for (const name of ["_ga=", "_ga_TEST1234=", "__gads="]) {
    assert.equal(cookieWrites.some((value) => value.startsWith(name)), true, `withdrawal must expire ${name}`);
  }
  assert.equal(cookieWrites.some((value) => value.startsWith("keep=")), false, "unrelated cookies stay");
  const before = events(calls).length;
  assert.equal(window.HappyinAnalytics.track("knowledge_search"), false, "a refusal must suppress events");
  assert.equal(events(calls).length, before);
}

{
  const { banner, calls, fetched, window } = await run({ measurementId: "G-TEST1234", stored: { ks_consent_v2: "granted" }, privacySignal: true });
  assert.equal(window.HappyinAnalytics.getConsent(), "blocked", "GPC overrides stored consent");
  assert.equal(window.HappyinAnalytics.track("article_view"), false, "GPC must keep events off");
  assert.equal(events(calls).length, 0, "GPC must keep every event off");
  assert.equal(banner.hidden, true, "GPC needs no prompt");
  assert.equal(fetched.length, 0, "GPC needs no region lookup");
}

{
  const { banner, window } = await run({ adsClient: "ca-pub-1234567890123456", region: true });
  assert.equal(window.HappyinAnalytics.isConfigured(), true, "ads alone also need the prompt");
  assert.equal(banner.hidden, false);
  assert.equal(window.HappyinAnalytics.track("article_view"), false, "no GA events without a Measurement ID");
}

console.log("PASS analytics consent harness");
