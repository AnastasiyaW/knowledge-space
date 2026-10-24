// Countries where Google cookies stay off until the visitor allows them: the EEA, the UK
// and Switzerland (network policy, happyin-sites-network docs/analytics-and-ads.md).
// overrides/partials/consent-bootstrap.html carries the same list for gtag's region
// parameter; tests/test_ads_and_consent.py keeps the two equal.
export const CONSENT_REGIONS = [
  "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IS", "IE", "IT",
  "LV", "LI", "LT", "LU", "MT", "NL", "NO", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "GB", "CH",
  // EU outermost regions and Aland have their own ISO 3166-1 codes in Cloudflare geolocation.
  "AX", "GF", "GP", "MQ", "RE", "YT", "MF",
];

// An unknown or anonymised country (missing, "XX", Tor's "T1") counts as a consent region:
// asking one extra visitor is harmless, not asking a European one is not.
export function consentRequired(country) {
  const code = String(country || "").toUpperCase();
  if (!/^[A-Z]{2}$/.test(code) || code === "XX") return true;
  return CONSENT_REGIONS.includes(code);
}
