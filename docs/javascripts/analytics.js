/*
 * Consent prompt, consent changes and aggregate product events for Happyin Knowledge Space.
 *
 * The Google tag itself and the Consent Mode v2 defaults are set in <head> by
 * overrides/partials/consent-bootstrap.html (denied in the EEA/UK/CH, granted elsewhere,
 * denied everywhere under Global Privacy Control / Do Not Track). This file:
 *   - shows the prompt to visitors in a consent region who have not chosen yet;
 *   - lets every visitor change or withdraw the choice ("Privacy choices");
 *   - sends a fixed set of aggregate events.
 * Never put search text, prompts, email addresses, feedback text, URL query strings or
 * affiliate identifiers in events.
 */
(function (root) {
  "use strict";

  var CONSENT_KEY = "ks_consent_v2";
  var REGION_KEY = "ks_consent_region_v1";
  var MEASUREMENT_ID_PATTERN = /^G-[A-Z0-9]{6,}$/i;
  var ALLOWED_EVENTS = {
    article_view: true,
    code_copy: true,
    github_star_click: true,
    knowledge_search: true,
    newsletter_subscribe: true,
    page_view: true,
    recommendation_click: true,
    search_result_open: true
  };
  var ALLOWED_ACTIONS = {
    github_star: "github_star_click",
    recommendation: "recommendation_click"
  };
  // First-party cookies of Google Analytics and AdSense on this domain.
  var GOOGLE_COOKIE = /^(_ga|_ga_.+|__gads|__gpi|__eoi)$/;
  var lastPageLocation = "";
  var preferencesOpen = false;
  // null = not known yet; the prompt stays hidden until the region answer arrives.
  var regionRequired = null;

  function readStorage(store, key) {
    try { return root[store].getItem(key); } catch (error) { return null; }
  }

  function writeStorage(store, key, value) {
    try { root[store].setItem(key, value); return true; } catch (error) { return false; }
  }

  function metaContent(name) {
    var meta = root.document.querySelector('meta[name="' + name + '"]');
    var value = meta && meta.getAttribute("content");
    return value ? value.trim() : "";
  }

  function measurementId() {
    var value = metaContent("happyin-ga4-id");
    return MEASUREMENT_ID_PATTERN.test(value) ? value : "";
  }

  function adsConfigured() {
    return /^ca-pub-\d+$/.test(metaContent("google-adsense-account"));
  }

  function configured() {
    return !!measurementId() || adsConfigured();
  }

  function privacySignal() {
    var navigator = root.navigator || {};
    return navigator.globalPrivacyControl === true || navigator.doNotTrack === "1" || root.doNotTrack === "1";
  }

  function consent() {
    if (privacySignal()) return "blocked";
    var value = readStorage("localStorage", CONSENT_KEY);
    return value === "granted" || value === "denied" ? value : "";
  }

  function pageLocation() {
    return root.location.origin + root.location.pathname;
  }

  function contentArea() {
    var parts = root.location.pathname.split("/");
    return parts.length > 1 && parts[1] ? parts[1].replace(/[^a-z0-9-]/gi, "").slice(0, 40) : "home";
  }

  function safePlacement(value) {
    return /^[a-z0-9_-]{1,32}$/i.test(value || "") ? value : "";
  }

  function gtag() {
    if (typeof root.gtag === "function") root.gtag.apply(root, arguments);
  }

  function removeGoogleCookies() {
    if (typeof root.document.cookie !== "string" || !root.document.cookie) return;
    var host = root.location.hostname || "";
    var parent = host.split(".").slice(-2).join(".");
    root.document.cookie.split(";").map(function (entry) {
      return entry.trim().split("=")[0];
    }).filter(function (name) {
      return GOOGLE_COOKIE.test(name);
    }).forEach(function (name) {
      var expired = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax";
      root.document.cookie = expired;
      if (host) root.document.cookie = expired + "; domain=" + host;
      if (parent && parent !== host) root.document.cookie = expired + "; domain=." + parent;
    });
  }

  // Events go through the tag the head bootstrap loaded; under a privacy signal it never
  // loads, and after a refusal nothing is sent at all.
  function send(name, parameters) {
    var value = consent();
    if (!ALLOWED_EVENTS[name] || !measurementId() || value === "blocked" || value === "denied") return false;
    if (typeof root.gtag !== "function") return false;
    root.gtag("event", name, parameters || {});
    return true;
  }

  function track(name, parameters) {
    if (!ALLOWED_EVENTS[name]) return false;
    var payload = { content_area: contentArea() };
    if (parameters && safePlacement(parameters.placement)) payload.placement = parameters.placement;
    return send(name, payload);
  }

  function trackPageView() {
    var location = pageLocation();
    if (location === lastPageLocation) return false;
    // Instant navigation changes the address without reloading the head bootstrap: keep
    // every later hit on the query-free address too (?h=<search terms> from search results).
    if (measurementId() && consent() !== "blocked" && consent() !== "denied") {
      var referrer = lastPageLocation || String(root.document.referrer || "").split("#")[0].split("?")[0];
      gtag("set", { page_location: location, page_referrer: referrer });
    }
    if (!send("page_view", { content_area: contentArea(), page_location: location })) return false;
    lastPageLocation = location;
    if (root.document.querySelector("[data-ks-article]")) track("article_view");
    return true;
  }

  function text(key, fallback) {
    var holder = root.document.getElementById("ks-analytics-consent");
    var value = holder && holder.getAttribute("data-" + key);
    return value || fallback;
  }

  function statusText(isConfigured, value) {
    if (!isConfigured) return text("state-off", "Google Analytics and Google ads are not enabled on this site.");
    if (value === "blocked") return text("state-signal", "Google cookies are off: your browser sends Global Privacy Control or Do Not Track.");
    if (value === "granted") return text("state-granted", "You allowed Google cookies in this browser.");
    if (value === "denied") return text("state-denied", "You turned Google cookies off in this browser.");
    return text("state-default", "You have not made a choice in this browser yet.");
  }

  function updateControls() {
    var isConfigured = configured();
    var value = consent();
    var banner = root.document.getElementById("ks-analytics-consent");
    var states = root.document.querySelectorAll("[data-ks-analytics-state]");
    var manage = root.document.querySelectorAll("[data-ks-analytics-preferences]");
    var i;
    for (i = 0; i < states.length; i++) states[i].textContent = statusText(isConfigured, value);
    for (i = 0; i < manage.length; i++) manage[i].hidden = !isConfigured || value === "blocked";
    if (banner) {
      var ask = value === "" && regionRequired === true;
      banner.hidden = !isConfigured || value === "blocked" || !(preferencesOpen || ask);
    }
  }

  function setConsent(value) {
    if ((value !== "granted" && value !== "denied") || !configured() || privacySignal()) return false;
    if (!writeStorage("localStorage", CONSENT_KEY, value)) return false;
    preferencesOpen = false;
    if (value === "granted") {
      // In a consent region this prompt grants analytics only; advertising consent there is
      // collected by Google's certified consent message once ads are enabled.
      if (regionRequired === false) {
        gtag("consent", "update", { ad_storage: "granted", ad_user_data: "granted", ad_personalization: "granted", analytics_storage: "granted" });
      } else {
        gtag("consent", "update", { analytics_storage: "granted" });
      }
      lastPageLocation = "";
      trackPageView();
    } else {
      gtag("consent", "update", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied" });
      removeGoogleCookies();
    }
    updateControls();
    return true;
  }

  // True while any consent question is, or may soon be, on screen: ours, ours still waiting
  // for the region answer, or Google's own consent message (Funding Choices, .fc-consent-root).
  // Other dialogs (the newsletter prompt) wait while this is true.
  function promptVisible() {
    var banner = root.document.getElementById("ks-analytics-consent");
    if (banner && !banner.hidden) return true;
    if (configured() && consent() === "" && regionRequired === null) return true;
    var google = root.document.querySelector(".fc-consent-root");
    return !!(google && google.offsetParent !== null);
  }

  // Unknown answer (network error, bad reply) counts as a consent region.
  function resolveRegion() {
    if (!configured() || consent() === "blocked") { regionRequired = false; return; }
    var cached = readStorage("sessionStorage", REGION_KEY);
    if (cached === "1" || cached === "0") {
      regionRequired = cached === "1";
      updateControls();
      return;
    }
    var fail = function () { regionRequired = true; updateControls(); };
    if (typeof root.fetch !== "function") { fail(); return; }
    try {
      root.fetch("/api/consent-region", { credentials: "omit" })
        .then(function (response) { return response.ok ? response.json() : null; })
        .then(function (data) {
          if (!data || typeof data.consent_required !== "boolean") { fail(); return; }
          regionRequired = data.consent_required;
          writeStorage("sessionStorage", REGION_KEY, regionRequired ? "1" : "0");
          updateControls();
        }, fail);
    } catch (error) {
      fail();
    }
  }

  function bindActions() {
    root.document.addEventListener("click", function (event) {
      var target = event.target;
      if (!target || !target.closest) return;

      if (target.closest("[data-ks-analytics-accept]")) {
        setConsent("granted");
        return;
      }
      if (target.closest("[data-ks-analytics-reject]")) {
        setConsent("denied");
        return;
      }
      if (target.closest("[data-ks-analytics-preferences]")) {
        preferencesOpen = true;
        updateControls();
        var banner = root.document.getElementById("ks-analytics-consent");
        var first = banner && banner.querySelector("button");
        if (first && first.focus) first.focus();
        return;
      }

      var action = target.closest("[data-ks-analytics]");
      if (action) {
        var name = ALLOWED_ACTIONS[action.getAttribute("data-ks-analytics")];
        if (name) track(name, { placement: action.getAttribute("data-ks-placement") });
      }

      if (target.closest("[data-clipboard-target]")) track("code_copy");
      if (target.closest(".md-search-result a")) track("search_result_open");
    }, true);

    root.document.addEventListener("submit", function (event) {
      var form = event.target;
      if (form && form.matches && form.matches('form[name="search"]')) track("knowledge_search");
    }, true);
  }

  function bindNavigation() {
    var onPage = function () {
      updateControls();
      trackPageView();
    };
    if (root.document$ && root.document$.subscribe) root.document$.subscribe(onPage);
    else root.document.addEventListener("DOMContentLoaded", onPage);
  }

  root.HappyinAnalytics = {
    getConsent: consent,
    isConfigured: configured,
    promptVisible: promptVisible,
    setConsent: setConsent,
    track: track
  };

  // The consent key of the opt-in-only release (PR #578); its value meant a different scope.
  try { root.localStorage.removeItem("ks_ga4_consent_v1"); } catch (error) {}
  // A privacy signal also clears Google cookies left from visits before it was turned on.
  if (configured() && privacySignal()) removeGoogleCookies();

  bindActions();
  bindNavigation();
  resolveRegion();
  updateControls();
})(window);
