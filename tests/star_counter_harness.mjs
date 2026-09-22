// Runs the star/return-counter script from overrides/main.html against fake browser
// globals and checks which counter files it requests. Exit 0 = every check passed.
// Usage: node tests/star_counter_harness.mjs overrides/main.html
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const html = readFileSync(process.argv[2], "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
const source = scripts.find((s) => s.includes("ks_counter"));
assert.ok(source, "no <script> block with the counter found in the template");
assert.ok(!source.includes("{{") && !source.includes("{%"), "counter script must not depend on template syntax");

function makeStorage({ broken = false } = {}) {
  const data = new Map();
  return {
    data,
    getItem: (k) => (data.has(k) ? data.get(k) : null),
    setItem: (k, v) => { if (broken) throw new Error("QuotaExceededError"); data.set(k, String(v)); },
    removeItem: (k) => { data.delete(k); },
  };
}

// Executes the script once, as one full page load on `day` (UTC), and returns the
// counter names it requested plus the captured document click listener.
function load(src, { day, storage, nav = {}, win = {} }) {
  const RealDate = Date;
  const nowMs = RealDate.parse(`${day}T12:00:00Z`);
  class FakeDate extends RealDate {
    constructor(...args) { if (args.length) super(...args); else super(nowMs); }
    static now() { return nowMs; }
  }
  const requested = [];
  const listeners = {};
  const fakeDocument = {
    addEventListener: (type, fn) => { listeners[type] = fn; },
    querySelector: () => null,
    getElementById: () => null,
    createElement: () => ({ classList: { add() {}, remove() {} }, setAttribute() {} }),
    body: { appendChild() {} },
  };
  const fakeFetch = (url) => {
    const m = /^\/ks\/hi\/([a-z0-9-]+)\.txt$/.exec(url);
    assert.ok(m, `unexpected request ${url}`);
    requested.push(m[1]);
    return Promise.resolve({});
  };
  // The body is this repository's own template script (trusted input); parameters
  // shadow the browser globals it touches, so nothing leaks into Node's globals.
  const run = new Function(
    "localStorage", "navigator", "window", "document", "fetch", "Date", "setTimeout", "clearTimeout",
    src,
  );
  run(storage, nav, win, fakeDocument, fakeFetch, FakeDate, () => 0, () => {});
  return { requested, listeners };
}

function clickOn(listeners, attrs) {
  const target = {
    closest: (sel) => {
      const m = /^\[([a-z-]+)\]$/.exec(sel);
      return m && m[1] in attrs ? { getAttribute: (a) => attrs[a] } : null;
    },
  };
  listeners.click({ target });
}

function scenarios(src) {
  const results = [];
  const check = (name, fn) => {
    try { fn(); results.push([name, "PASS"]); }
    catch (e) { results.push([name, `FAIL: ${e.message}`]); }
  };

  check("returning visits walk through the day buckets", () => {
    const storage = makeStorage();
    const seq = [
      ["2026-01-01", ["new"]],
      ["2026-01-01", []],               // same day: already counted
      ["2026-01-02", ["ret-1d"]],
      ["2026-01-05", ["ret-2-7d"]],
      ["2026-01-20", ["ret-8-30d"]],
      ["2026-03-01", ["reg-31d-plus"]], // fifth distinct day turns ret- into reg-
      ["2026-03-02", ["reg-1d"]],
    ];
    for (const [day, want] of seq) {
      assert.deepEqual(load(src, { day, storage }).requested, want, `on ${day}`);
    }
  });

  check("the record expires 13 months after the first visit", () => {
    const storage = makeStorage();
    load(src, { day: "2026-01-01", storage });
    load(src, { day: "2026-06-01", storage });
    assert.deepEqual(load(src, { day: "2027-02-15", storage }).requested, ["new"]);
  });

  check("Global Privacy Control: nothing is sent and the record is removed", () => {
    const storage = makeStorage();
    load(src, { day: "2026-01-01", storage });
    const out = load(src, { day: "2026-01-02", storage, nav: { globalPrivacyControl: true } });
    assert.deepEqual(out.requested, []);
    assert.equal(storage.getItem("ks_counter"), null);
  });

  check("Do Not Track and webdriver send nothing", () => {
    assert.deepEqual(load(src, { day: "2026-01-01", storage: makeStorage(), nav: { doNotTrack: "1" } }).requested, []);
    assert.deepEqual(load(src, { day: "2026-01-01", storage: makeStorage(), nav: { webdriver: true } }).requested, []);
  });

  check("the opt-out switch stops counting", () => {
    const storage = makeStorage();
    storage.setItem("ks_counter_off", "1");
    assert.deepEqual(load(src, { day: "2026-01-01", storage }).requested, []);
  });

  check("broken storage counts nothing instead of a new visit on every page", () => {
    const storage = makeStorage({ broken: true });
    assert.deepEqual(load(src, { day: "2026-01-01", storage }).requested, []);
    assert.deepEqual(load(src, { day: "2026-01-01", storage }).requested, []);
  });

  check("a clock that moved backwards counts nothing", () => {
    const storage = makeStorage();
    load(src, { day: "2026-03-01", storage });
    const before = storage.getItem("ks_counter");
    assert.deepEqual(load(src, { day: "2026-02-01", storage }).requested, []);
    assert.equal(storage.getItem("ks_counter"), before);
  });

  check("a garbled record starts over as a new visit", () => {
    const storage = makeStorage();
    storage.setItem("ks_counter", "{not json");
    assert.deepEqual(load(src, { day: "2026-01-01", storage }).requested, ["new"]);
  });

  check("a code copy asks for a star once a week, and never after a star click", () => {
    const storage = makeStorage();
    const monday = load(src, { day: "2026-01-05", storage });
    clickOn(monday.listeners, { "data-clipboard-target": "#__code_0 > code" });
    clickOn(monday.listeners, { "data-clipboard-target": "#__code_1 > code" });
    assert.deepEqual(monday.requested, ["new", "toast-shown"]);
    const nextWeek = load(src, { day: "2026-01-13", storage });
    clickOn(nextWeek.listeners, { "data-clipboard-target": "#__code_0 > code" });
    assert.deepEqual(nextWeek.requested, ["ret-8-30d", "toast-shown"]);
    clickOn(nextWeek.listeners, { "data-ks-star": "toast" });
    const later = load(src, { day: "2026-02-20", storage });
    clickOn(later.listeners, { "data-clipboard-target": "#__code_0 > code" });
    assert.deepEqual(later.requested, ["ret-31d-plus"]);
  });

  check("star clicks are counted by known placement only", () => {
    const storage = makeStorage();
    const page = load(src, { day: "2026-01-01", storage });
    clickOn(page.listeners, { "data-ks-star": "article" });
    clickOn(page.listeners, { "data-ks-star": "footer" });   // unknown placement: no request
    assert.deepEqual(page.requested, ["new", "star-article"]);
    assert.equal(storage.getItem("ks_star_clicked"), "2026-01-01");
  });

  return results;
}

let failed = 0;
for (const [name, verdict] of scenarios(source)) {
  console.log(`${verdict === "PASS" ? "PASS" : "FAIL"}  ${name}${verdict === "PASS" ? "" : ` - ${verdict}`}`);
  if (verdict !== "PASS") failed += 1;
}

// Negative control: a script that requests the wrong file must make the harness red.
const sabotaged = source.replace("hi('new')", "hi('old')");
assert.notEqual(sabotaged, source, "negative control could not find hi('new') to sabotage");
const control = scenarios(sabotaged).filter(([, v]) => v !== "PASS");
if (control.length === 0) {
  console.log("FAIL  negative control: a sabotaged script still passed every scenario");
  failed += 1;
} else {
  console.log(`PASS  negative control: sabotaged script failed ${control.length} scenario(s)`);
}

process.exit(failed ? 1 : 0);
