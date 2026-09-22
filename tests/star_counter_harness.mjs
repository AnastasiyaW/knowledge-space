// Runs the star/return-counter script from overrides/main.html against fake browser
// globals and checks which counter files it requests. Exit 0 = every check passed.
// Usage: node tests/star_counter_harness.mjs overrides/main.html '<JSON list of counter names>'
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const html = readFileSync(process.argv[2], "utf8");
const expectedNames = process.argv[3] ? JSON.parse(process.argv[3]) : null;
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

function fakeElement() {
  const el = { textContent: "", innerHTML: "", disabled: false, shown: 0, setAttribute() {} };
  el.classList = { add(c) { if (c === "ks-copy-toast--visible") el.shown += 1; }, remove() {} };
  return el;
}

// Executes the script once, as one full page load on `day` (noon UTC, so the visitor's
// local calendar day is that date in every time zone from UTC-11 to UTC+11), and returns
// the counter names it requested, any request outside the contract, and the page it touched.
function load(src, { day, storage, nav = {}, win = {}, withSwitch = false }) {
  const RealDate = Date;
  const nowMs = RealDate.parse(`${day}T12:00:00Z`);
  class FakeDate extends RealDate {
    constructor(...args) { if (args.length) super(...args); else super(nowMs); }
    static now() { return nowMs; }
  }
  const requested = [];
  const unexpected = [];   // collected, not thrown: the script swallows fetch errors
  const listeners = {};
  const page = { state: fakeElement(), toggle: fakeElement(), created: [] };
  const fakeDocument = {
    addEventListener: (type, fn) => { listeners[type] = fn; },
    querySelector: (sel) => (!withSwitch ? null
      : sel === "[data-ks-counter-state]" ? page.state
      : sel === "[data-ks-counter-toggle]" ? page.toggle : null),
    getElementById: () => null,
    createElement: () => { const el = fakeElement(); page.created.push(el); return el; },
    body: { appendChild() {} },
  };
  const fakeFetch = (url, options) => {
    const m = /^\/ks\/hi\/([a-z0-9-]+)\.txt$/.exec(url);
    const o = options || {};
    if (m && o.referrerPolicy === "no-referrer" && o.credentials === "omit" && o.cache === "no-store") {
      requested.push(m[1]);
    } else {
      unexpected.push(`${url} ${JSON.stringify(o)}`);
    }
    return Promise.resolve({});
  };
  // Timers wait in a queue until the scenario calls flush(), so "during the wait" is testable.
  const timers = [];
  const queueTimer = (fn) => { timers.push(fn); return timers.length; };
  const flush = () => { while (timers.length) timers.shift()(); };
  // The body is this repository's own template script (trusted input); parameters
  // shadow the browser globals it touches, so nothing leaks into Node's globals.
  const run = new Function(
    "localStorage", "navigator", "window", "document", "fetch", "Date", "setTimeout", "clearTimeout",
    src,
  );
  run(storage, nav, win, fakeDocument, fakeFetch, FakeDate, queueTimer, () => {});
  return { requested, unexpected, listeners, page, flush };
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
  const seen = new Set();      // every counter name any scenario made the script request
  let loads = [];
  const L = (opts) => { const out = load(src, opts); loads.push(out); return out; };
  const check = (name, fn) => {
    loads = [];
    try {
      fn();
      for (const out of loads) {
        assert.deepEqual(out.unexpected, [], "request outside the contract (path or fetch options)");
        out.requested.forEach((n) => seen.add(n));
      }
      results.push([name, "PASS"]);
    } catch (e) { results.push([name, `FAIL: ${e.message}`]); }
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
      ["2026-03-05", ["reg-2-7d"]],
      ["2026-03-20", ["reg-8-30d"]],
    ];
    for (const [day, want] of seq) {
      assert.deepEqual(L({ day, storage }).requested, want, `on ${day}`);
    }
  });

  check("a visitor back after 31+ days on the second visit is ret-31d-plus", () => {
    const storage = makeStorage();
    L({ day: "2026-01-01", storage });
    assert.deepEqual(L({ day: "2026-03-01", storage }).requested, ["ret-31d-plus"]);
  });

  check("the record expires 13 months after the first visit", () => {
    const storage = makeStorage();
    L({ day: "2026-01-01", storage });
    L({ day: "2026-06-01", storage });
    assert.deepEqual(L({ day: "2027-02-15", storage }).requested, ["new"]);
  });

  check("Global Privacy Control: nothing is sent and the record is removed", () => {
    const storage = makeStorage();
    L({ day: "2026-01-01", storage });
    const out = L({ day: "2026-01-02", storage, nav: { globalPrivacyControl: true } });
    assert.deepEqual(out.requested, []);
    assert.equal(storage.getItem("ks_counter"), null);
  });

  check("Do Not Track and webdriver send nothing", () => {
    assert.deepEqual(L({ day: "2026-01-01", storage: makeStorage(), nav: { doNotTrack: "1" } }).requested, []);
    assert.deepEqual(L({ day: "2026-01-01", storage: makeStorage(), nav: { webdriver: true } }).requested, []);
  });

  check("the opt-out switch stops counting", () => {
    const storage = makeStorage();
    storage.setItem("ks_counter_off", "1");
    assert.deepEqual(L({ day: "2026-01-01", storage }).requested, []);
  });

  check("without storage: no visit, no star click, no notice, and the switch says so", () => {
    const storage = makeStorage({ broken: true });
    const out = L({ day: "2026-01-01", storage, withSwitch: true });
    clickOn(out.listeners, { "data-ks-star": "article" });
    clickOn(out.listeners, { "data-clipboard-target": "#__code_0 > code" });
    clickOn(out.listeners, { "data-clipboard-target": "#__code_1 > code" });
    out.flush();
    out.listeners.DOMContentLoaded();
    assert.deepEqual(out.requested, []);
    assert.equal(out.page.created.reduce((n, el) => n + el.shown, 0), 0, "copy notice shown without memory");
    assert.deepEqual(L({ day: "2026-01-01", storage }).requested, []);
    assert.match(out.page.state.textContent, /does not let the site store/);
    assert.equal(out.page.toggle.disabled, true);
  });

  check("the privacy switch turns counting off and back on", () => {
    const storage = makeStorage();
    const out = L({ day: "2026-01-01", storage, withSwitch: true });
    clickOn(out.listeners, { "data-ks-counter-toggle": "" });
    assert.equal(storage.getItem("ks_counter_off"), "1");
    assert.equal(storage.getItem("ks_counter"), null);
    assert.match(out.page.state.textContent, /You turned the return counter off/);
    clickOn(out.listeners, { "data-ks-star": "article" });     // off: not counted
    clickOn(out.listeners, { "data-ks-counter-toggle": "" });
    assert.equal(storage.getItem("ks_counter_off"), null);
    assert.match(out.page.state.textContent, /is on in this browser/);
    assert.deepEqual(out.requested, ["new"]);
  });

  check("a clock that moved backwards counts nothing", () => {
    const storage = makeStorage();
    L({ day: "2026-03-01", storage });
    const before = storage.getItem("ks_counter");
    assert.deepEqual(L({ day: "2026-02-01", storage }).requested, []);
    assert.equal(storage.getItem("ks_counter"), before);
  });

  check("a garbled record starts over as a new visit", () => {
    const storage = makeStorage();
    storage.setItem("ks_counter", "{not json");
    assert.deepEqual(L({ day: "2026-01-01", storage }).requested, ["new"]);
  });

  check("a code copy asks for a star once a week, and never after a star click", () => {
    const storage = makeStorage();
    const monday = L({ day: "2026-01-05", storage });
    clickOn(monday.listeners, { "data-clipboard-target": "#__code_0 > code" });
    clickOn(monday.listeners, { "data-clipboard-target": "#__code_1 > code" });
    monday.flush();
    assert.deepEqual(monday.requested, ["new", "toast-shown"]);
    const nextWeek = L({ day: "2026-01-13", storage });
    clickOn(nextWeek.listeners, { "data-clipboard-target": "#__code_0 > code" });
    nextWeek.flush();
    clickOn(nextWeek.listeners, { "data-ks-star": "toast" });
    assert.deepEqual(nextWeek.requested, ["ret-8-30d", "toast-shown", "star-toast"]);
    const later = L({ day: "2026-02-20", storage });
    clickOn(later.listeners, { "data-clipboard-target": "#__code_0 > code" });
    later.flush();
    assert.deepEqual(later.requested, ["ret-31d-plus"]);
  });

  check("a star click while the notice is pending cancels it", () => {
    const storage = makeStorage();
    const out = L({ day: "2026-01-05", storage });
    clickOn(out.listeners, { "data-clipboard-target": "#__code_0 > code" });
    clickOn(out.listeners, { "data-ks-star": "article" });
    out.flush();
    assert.deepEqual(out.requested, ["new", "star-article"]);
    assert.equal(out.page.created.reduce((n, el) => n + el.shown, 0), 0, "notice shown after a star click");
  });

  check("star clicks are counted by known placement only", () => {
    const storage = makeStorage();
    const page = L({ day: "2026-01-01", storage });
    // Unknown placements, including names every JS object inherits, request nothing.
    for (const where of ["topnav", "article", "footer", "constructor", "__proto__", "toString"]) {
      clickOn(page.listeners, { "data-ks-star": where });
    }
    assert.deepEqual(page.requested, ["new", "star-topnav", "star-article"]);
    assert.equal(storage.getItem("ks_star_clicked"), "2026-01-01");
  });

  if (expectedNames) {
    // Runs last: the union of everything requested above must be exactly the file list.
    results.push(["the script requests exactly the files the build writes",
      JSON.stringify([...seen].sort()) === JSON.stringify([...expectedNames].sort())
        ? "PASS" : `FAIL: requested ${JSON.stringify([...seen].sort())}`]);
  }
  return results;
}

let failed = 0;
for (const [name, verdict] of scenarios(source)) {
  console.log(`${verdict === "PASS" ? "PASS" : "FAIL"}  ${name}${verdict === "PASS" ? "" : ` - ${verdict}`}`);
  if (verdict !== "PASS") failed += 1;
}

// Negative controls: each sabotaged copy of the script must turn at least one scenario red.
const sabotage = {
  "wrong file name": (s) => s.replace("hi('new')", "hi('old')"),
  "referrer sent again": (s) => s.replace("referrerPolicy: 'no-referrer', ", ""),
  "prototype names accepted": (s) => s.replace("Object.prototype.hasOwnProperty.call(PLACEMENTS, where)", "PLACEMENTS[where]"),
  "notice without memory": (s) => s.replace("if (!write(TOAST_AT, String(Date.now()))) return;", "write(TOAST_AT, String(Date.now()));"),
  "pending notice not cancelled": (s) => s.replace("if (read(STARRED)) return;   // a star click", "// a star click"),
};
for (const [label, mutate] of Object.entries(sabotage)) {
  const bad = mutate(source);
  assert.notEqual(bad, source, `negative control "${label}" found nothing to change`);
  const red = scenarios(bad).filter(([, v]) => v !== "PASS").length;
  if (red === 0) {
    console.log(`FAIL  negative control "${label}": the sabotaged script passed every scenario`);
    failed += 1;
  } else {
    console.log(`PASS  negative control "${label}": ${red} scenario(s) went red`);
  }
}

if (failed) process.exit(1);
if (!expectedNames) {
  // Not a pass: without the file list the one check that ties the script to the build is skipped.
  console.log("NOT CHECKED  file list: pass the counter names as the second argument (pytest does)");
  process.exit(2);
}
process.exit(0);
