// Exercises the privacy boundary in docs/javascripts/analytics.js without a browser.
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

function run({ measurementId = "", stored = {}, privacySignal = false, cookies = "" } = {}) {
  const scripts = [];
  const listeners = {};
  const cookieWrites = [];
  let cookieValue = cookies;
  const meta = { getAttribute() { return measurementId; } };
  const doc = {
    head: { appendChild(node) { scripts.push(node); node.parentNode = this; } },
    addEventListener(type, handler) { listeners[type] = handler; },
    createElement(tag) { return { tagName: tag.toUpperCase() }; },
    getElementById() { return null; },
    querySelector(selector) {
      if (selector === 'meta[name="happyin-ga4-id"]') return meta;
      if (selector === ".md-content__inner article") return {};
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
    location: { origin: "https://happyin.space", hostname: "happyin.space", pathname: "/llm-agents/test/", search: "?private=never-send" },
    navigator: privacySignal ? { globalPrivacyControl: true } : {},
    setTimeout,
    clearTimeout
  };
  vm.runInNewContext(source, { window, Date, encodeURIComponent, setTimeout, clearTimeout });
  return { cookieWrites, listeners, scripts, window };
}

function events(window) {
  return (window.dataLayer || []).map((entry) => Array.from(entry));
}

{
  const { scripts, window } = run();
  assert.equal(window.HappyinAnalytics.isConfigured(), false, "blank public configuration must disable GA");
  assert.equal(scripts.length, 0, "blank configuration must not load Google");
}

{
  const { scripts, window } = run({ measurementId: "G-TEST1234" });
  assert.equal(window.HappyinAnalytics.getConsent(), "", "GA must start without consent");
  assert.equal(scripts.length, 0, "GA must not load before consent");
  assert.equal(window.HappyinAnalytics.setConsent("granted"), true, "explicit approval must be recorded");
  assert.equal(scripts.length, 1, "approval must load exactly one tag");
  assert.match(scripts[0].src, /googletagmanager\.com\/gtag\/js\?id=G-TEST1234$/);
  const sent = events(window);
  const config = sent.find((entry) => entry[0] === "config");
  assert.equal(config[2].send_page_view, false, "page views are sent explicitly to avoid SPA duplicates");
  const pageView = sent.find((entry) => entry[0] === "event" && entry[1] === "page_view");
  assert.equal(pageView[2].page_location, "https://happyin.space/llm-agents/test/", "query strings must not reach GA");
  assert.equal(JSON.stringify(pageView).includes("private=never-send"), false, "a private query must never reach GA");
  window.HappyinAnalytics.track("newsletter_subscribe", { email: "not-for-analytics@example.test" });
  const newsletter = events(window).find((entry) => entry[0] === "event" && entry[1] === "newsletter_subscribe");
  assert.equal(JSON.stringify(newsletter).includes("email"), false, "caller data must not leak into GA events");
}

{
  const { cookieWrites, window } = run({ measurementId: "G-TEST1234", cookies: "_ga=old; _ga_TEST1234=old; keep=1" });
  window.HappyinAnalytics.setConsent("granted");
  window.HappyinAnalytics.setConsent("denied");
  assert.equal(cookieWrites.some((value) => value.startsWith("_ga=")), true, "withdrawal must expire the base GA cookie");
  assert.equal(cookieWrites.some((value) => value.startsWith("_ga_TEST1234=")), true, "withdrawal must expire the stream GA cookie");
}

{
  const { scripts, window } = run({ measurementId: "G-TEST1234" });
  assert.equal(window.HappyinAnalytics.setConsent("denied"), true, "a refusal must be recorded");
  assert.equal(scripts.length, 0, "a refusal must not load Google");
  assert.equal(window.HappyinAnalytics.track("knowledge_search"), false, "a refusal must suppress events");
}

{
  const { scripts, window } = run({ measurementId: "G-TEST1234", stored: { ks_ga4_consent_v1: "granted" }, privacySignal: true });
  assert.equal(window.HappyinAnalytics.getConsent(), "blocked", "GPC overrides stored consent");
  assert.equal(scripts.length, 0, "GPC must keep the Google tag unloaded");
}

console.log("PASS analytics consent harness");
