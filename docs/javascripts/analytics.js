/*
 * Optional GA4 measurement for Happyin Knowledge Space.
 *
 * The tag is deliberately absent until all three conditions hold: a valid public
 * Measurement ID is configured, the visitor explicitly opts in, and the browser
 * does not send a privacy signal. Do not put search text, prompts, email addresses,
 * feedback text, URL query strings, or affiliate identifiers in events.
 */
(function (root) {
  "use strict";

  var CONSENT_KEY = "ks_ga4_consent_v1";
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
  var tagLoaded = false;
  var lastPageLocation = "";
  var preferencesOpen = false;

  function readStorage(key) {
    try { return root.localStorage.getItem(key); } catch (error) { return null; }
  }

  function writeStorage(key, value) {
    try { root.localStorage.setItem(key, value); return true; } catch (error) { return false; }
  }

  function measurementId() {
    var meta = root.document.querySelector('meta[name="happyin-ga4-id"]');
    var value = meta && meta.getAttribute("content");
    value = value ? value.trim() : "";
    return MEASUREMENT_ID_PATTERN.test(value) ? value : "";
  }

  function privacySignal() {
    var navigator = root.navigator || {};
    return navigator.globalPrivacyControl === true || navigator.doNotTrack === "1" || root.doNotTrack === "1";
  }

  function consent() {
    if (privacySignal()) return "blocked";
    var value = readStorage(CONSENT_KEY);
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

  function loadTag() {
    var id = measurementId();
    if (!id || tagLoaded || consent() !== "granted") return false;

    root.dataLayer = root.dataLayer || [];
    root.gtag = root.gtag || function () { root.dataLayer.push(arguments); };

    // The default exists before the tag loads. Advertising and personalization
    // stay disabled even after a visitor permits aggregate analytics.
    root.gtag("consent", "default", {
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      analytics_storage: "denied"
    });
    root.gtag("consent", "update", {
      analytics_storage: "granted"
    });
    root.gtag("js", new Date());
    root.gtag("config", id, {
      allow_ad_personalization_signals: false,
      allow_google_signals: false,
      send_page_view: false
    });

    var script = root.document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    var firstScript = root.document.querySelector("script");
    if (firstScript && firstScript.parentNode) firstScript.parentNode.insertBefore(script, firstScript);
    else root.document.head.appendChild(script);
    tagLoaded = true;
    return true;
  }

  function removeAnalyticsCookies() {
    if (typeof root.document.cookie !== "string" || !root.document.cookie) return;
    var names = root.document.cookie.split(";").map(function (entry) {
      return entry.trim().split("=")[0];
    }).filter(function (name) {
      return name === "_ga" || name.indexOf("_ga_") === 0;
    });
    names.forEach(function (name) {
      var expired = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax";
      root.document.cookie = expired;
      if (root.location.hostname) root.document.cookie = expired + "; domain=" + root.location.hostname;
    });
  }

  function send(name, parameters) {
    if (!ALLOWED_EVENTS[name] || consent() !== "granted") return false;
    loadTag();
    if (!root.gtag) return false;
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
    if (consent() !== "granted") return false;
    var location = pageLocation();
    if (location === lastPageLocation) return false;
    lastPageLocation = location;
    send("page_view", { content_area: contentArea(), page_location: location });
    if (root.document.querySelector(".md-content__inner article")) track("article_view");
    return true;
  }

  function statusText(configured, value) {
    if (!configured) return "Optional Google Analytics is not enabled for this release.";
    if (value === "blocked") return "Analytics is off because your browser sent a privacy signal.";
    if (value === "granted") return "You allowed anonymous product analytics in this browser.";
    if (value === "denied") return "Analytics is off in this browser.";
    return "Choose whether to allow optional Google Analytics in this browser.";
  }

  function updateControls() {
    var configured = !!measurementId();
    var value = consent();
    var banner = root.document.getElementById("ks-analytics-consent");
    var state = root.document.querySelector("[data-ks-analytics-state]");
    var manage = root.document.querySelector("[data-ks-analytics-preferences]");
    if (state) state.textContent = statusText(configured, value);
    if (manage) manage.hidden = !configured || value === "blocked";
    if (banner) banner.hidden = !configured || value === "blocked" || (value !== "" && !preferencesOpen);
  }

  function setConsent(value) {
    if ((value !== "granted" && value !== "denied") || !measurementId() || privacySignal()) return false;
    if (!writeStorage(CONSENT_KEY, value)) return false;
    preferencesOpen = false;
    if (value === "granted") {
      lastPageLocation = "";
      loadTag();
      trackPageView();
    } else {
      if (root.gtag) root.gtag("consent", "update", { analytics_storage: "denied" });
      removeAnalyticsCookies();
      lastPageLocation = "";
    }
    updateControls();
    return true;
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
    if (root.document$ && root.document$.subscribe) {
      root.document$.subscribe(function () {
        updateControls();
        trackPageView();
      });
    } else {
      root.document.addEventListener("DOMContentLoaded", function () {
        updateControls();
        trackPageView();
      });
    }
  }

  var api = {
    getConsent: consent,
    isConfigured: function () { return !!measurementId(); },
    setConsent: setConsent,
    track: track
  };
  root.HappyinAnalytics = api;

  bindActions();
  bindNavigation();
  updateControls();
  if (consent() === "granted") {
    loadTag();
    trackPageView();
  }
})(window);
