# Email Reputation and Age Scoring for Anti-Fraud

Signal categories, vendor service tradeoffs, and a DIY MVP stack for blocking high-risk registrations based on email age and reputation signals.

## Key Facts

- Email age at registration is a strong fraud predictor: accounts with emails < 30 days old correlate with card fraud, chargebacks, and trial abuse
- No service knows the *true* mailbox creation date; signals are first-observed timestamps within the vendor's consortium, breach history, and domain WHOIS
- [[anti-fraud-behavioral-analysis]] covers behavioral signals (mouse, keystroke, session timing); this article covers static email signals applied at registration
- [[disposable-email-detection]] covers blocklist-based throwaway detection; this article covers reputation/age scoring from third-party APIs and DIY signal stacks
- Sending raw email addresses to third-party APIs triggers GDPR Article 4(1) obligations; always hash (SHA-256 or MD5) before transmission unless DPA explicitly permits raw
- Email validation services (SMTP-probe deliverability checks) are a **different product class** — they verify deliverability, not age or fraud risk
- Enterprise fraud platforms (bank-grade, $30k+/yr) are out of scope for SMB/SaaS; see [[threat-modeling]] for matching controls to risk levels

## Signal Categories

| Signal | What it indicates | Latency | Cost model | Privacy posture |
|---|---|---|---|---|
| **Consortium first-seen date** | Earliest timestamp the vendor's customer network queried this email; proxy for account age | 150-400ms | Per-call (PAYG or subscription) | Email hashed before send; GDPR-friendly if DPA in place |
| **Breach presence (HIBP-style)** | Email appeared in a known data breach; older breaches (2012-2019) imply account age 5-10+ years; absence is NOT a new-email signal | 100-300ms | Free tier available ($3.95–$275/mo for HIBP API) | MD5/SHA1 k-anonymity API; no raw email transmitted |
| **Digital footprint / social presence** | Accounts linked across 250+ social platforms; high footprint implies long-lived legitimate user | 1.4-5s (OSINT enrichment) | Subscription-heavy ($699/mo+) | OSINT-based; DPA complexity varies |
| **Domain WHOIS / registration age** | Domain of the email (not the mailbox) registered recently; catches newly-registered lookalike domains but irrelevant for gmail.com/hotmail.com | 200-500ms (RDAP) | Free (public RDAP) | Domain-level only; no PII |
| **Disposable/temporary domain list** | Email domain matches known throwaway provider | <50ms | Free (OSS blocklists) | No PII transmitted |
| **Fraud consortium score** | Aggregate score across email + IP + device signals from shared fraud network | 150-300ms | PAYG ($0.015–$025/call) | Email hashed; IP/device in payload |
| **Avatar/Gravatar presence** | Profile image registered against email hash; weak signal, skewed toward developer audiences | 200-400ms | Free (no key required) | MD5 hash only |

## Vendor Service Categories

Three tiers exist; the right tier depends on volume and fraud tolerance:

**Tier 1 — Fraud consortium APIs (email + IP + device combined)**
PAYG pricing, no subscription floor, returns email `first_seen`, `is_disposable`, `is_free`, and domain age alongside IP/device signals. Mature DPA programs. Email hashed (MD5) by default before transmission. Best suited for SMB-to-midmarket volumes where single API call should cover multiple signal types.
- Example capability: `email.first_seen`, `is_disposable`, domain age, IP geolocation, proxy/VPN detection in one response
- Latency: 150-300ms; Cost: ~$0.015-$0.025/call PAYG
- GDPR: US-based; DPA available on request; some EU privacy officers require review
- Key gotcha: `first_seen` records the vendor's first consortium sighting, not true mailbox birth date. New fraudsters queried for the first time receive a blank-slate timestamp — the signal sharpens as consortium coverage grows

**Tier 2 — Email-specific risk APIs (higher first_seen fidelity)**
Dedicated email reputation services with cleaner age signals (`first_seen: {human, timestamp, iso}`) and explicit abuse flags (`recent_abuse`, `frequent_complainer`, `leaked`). Generous free tiers (5k/mo+) suitable for validation and A/B testing. Domain-only age field (mailbox-level first_seen only where vendor has prior sighting).
- Latency: 200-400ms; Cost: Free tier + PAYG ~$0.001-$0.005
- GDPR: US-based, single datacenter; DPA on request
- Key gotcha: `first_seen` returns "just now" for any email the service has not previously seen — high false-positive rate if used as standalone threshold. Compound with `fraud_score`, `disposable`, `recent_abuse`

**Tier 3 — Digital footprint / OSINT enrichment**
250+ platform presence checks (social media, forums, gaming, professional networks). Returns `minimum_age_months`, `earliest_profile_date`, consortium `first_seen`. Categorically stronger signal than Tier 1/2 for catching synthetic identities, but latency (1.4-5s) precludes synchronous blocking at signup. Starter pricing at $699+/mo minimum. Use for async post-signup enrichment with account suspension on threshold breach.
- Pattern: signup completes → async enrichment job → if score > threshold → suspend + require re-verify before first paid action
- Footprint coverage degrades as social platforms add anti-scraping; validate against your labeled fraud data

## DIY MVP Stack

Combines four free/cheap signals into a 0-100 risk score. No subscription required; ~$50-200/yr for HIBP API at low volumes.

```python
import hashlib
import httpx
import asyncio
from datetime import datetime, timezone

async def check_breach_presence(email: str, client: httpx.AsyncClient) -> dict:
    """HIBP k-anonymity API: no raw email transmitted."""
    sha1 = hashlib.sha1(email.lower().encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    resp = await client.get(
        f"https://api.pwnedpasswords.com/range/{prefix}",
        headers={"hibp-api-key": "YOUR_KEY"},  # required for email API; range API is free
    )
    # Range API returns hashes for breaches, not email-specific breach list.
    # For per-email breach metadata use /breachedaccount/{email} endpoint (paid).
    breaches_found = suffix in resp.text
    return {"breached": breaches_found, "signal_strength": "strong_if_true"}

async def check_gravatar(email: str, client: httpx.AsyncClient) -> dict:
    """Gravatar presence: weak signal, skewed to dev/designer audience."""
    md5 = hashlib.md5(email.strip().lower().encode()).hexdigest()
    try:
        resp = await client.get(
            f"https://www.gravatar.com/{md5}.json",
            timeout=2.0,
        )
        return {"gravatar_present": resp.status_code == 200}
    except httpx.TimeoutException:
        return {"gravatar_present": None, "error": "timeout"}

async def check_domain_age(domain: str, client: httpx.AsyncClient) -> dict:
    """RDAP domain age via IANA bootstrap. Freemail domains (gmail.com etc) skip."""
    FREEMAIL_SKIP = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"}
    if domain.lower() in FREEMAIL_SKIP:
        return {"domain_age_days": None, "is_freemail": True}
    try:
        bootstrap = await client.get(
            "https://data.iana.org/rdap/dns.json", timeout=3.0
        )
        # Simplified: use rdap.org as convenience resolver
        rdap = await client.get(
            f"https://rdap.org/domain/{domain}", timeout=3.0
        )
        if rdap.status_code != 200:
            return {"domain_age_days": None}
        data = rdap.json()
        for event in data.get("events", []):
            if event.get("eventAction") == "registration":
                reg_date = datetime.fromisoformat(
                    event["eventDate"].replace("Z", "+00:00")
                )
                age_days = (datetime.now(timezone.utc) - reg_date).days
                return {"domain_age_days": age_days}
        return {"domain_age_days": None}
    except Exception as e:
        return {"domain_age_days": None, "error": str(e)}

async def check_disposable(domain: str, client: httpx.AsyncClient) -> dict:
    """
    Check against open disposable domain list.
    Fetch once, cache in memory or Redis for 24h.
    Source: github.com/disposable-email-domains/disposable-email-domains
    """
    resp = await client.get(
        "https://raw.githubusercontent.com/disposable-email-domains/"
        "disposable-email-domains/master/disposable_email_blocklist.conf",
        timeout=5.0,
    )
    blocklist = set(resp.text.strip().splitlines())
    return {"is_disposable": domain.lower() in blocklist}

def compute_risk_score(signals: dict) -> dict:
    """
    Combine signals into 0-100 risk score.
    Higher score = higher risk.
    """
    score = 0
    reasons = []

    if signals.get("is_disposable"):
        score += 40
        reasons.append("disposable_domain")

    domain_age = signals.get("domain_age_days")
    if domain_age is not None and not signals.get("is_freemail"):
        if domain_age < 7:
            score += 35
            reasons.append("domain_registered_<7d")
        elif domain_age < 30:
            score += 20
            reasons.append("domain_registered_<30d")

    if not signals.get("breached"):
        # Absence of breach does NOT imply new account; only presence implies age
        pass
    else:
        score = max(0, score - 15)
        reasons.append("breach_presence_age_signal")

    if signals.get("gravatar_present") is True:
        score = max(0, score - 10)
        reasons.append("gravatar_present")

    return {
        "score": min(score, 100),
        "reasons": reasons,
        "action": "block" if score >= 70 else ("require_verify" if score >= 40 else "allow"),
    }

async def email_risk_check(email: str) -> dict:
    domain = email.split("@")[-1]
    async with httpx.AsyncClient() as client:
        breach, gravatar, domain_age, disposable = await asyncio.gather(
            check_breach_presence(email, client),
            check_gravatar(email, client),
            check_domain_age(domain, client),
            check_disposable(domain, client),
        )
    signals = {**breach, **gravatar, **domain_age, **disposable}
    result = compute_risk_score(signals)
    result["signals"] = signals
    return result
```

```python
# Cache results in Postgres or Redis to avoid redundant API calls
# Cache TTL: 30 days for allow/block decisions; 1 day for require_verify
# Key: SHA-256(email) — never cache by raw email

import hashlib

def cache_key(email: str) -> str:
    return "email_risk:" + hashlib.sha256(email.lower().encode()).hexdigest()
```

## Integration Pattern

**Primary: Fraud consortium API (Tier 1)**
Single call at registration covering email age, disposable flag, IP signals. PAYG, no subscription minimum. Hash email (MD5) before transmission. Log full API response for audit and threshold tuning.

**Secondary: DIY stack**
Run in parallel or as fallback when Tier 1 API is unavailable. Cache results 30 days. Use as signal correlation baseline for 60-day chargeback analysis before committing to Tier 1 subscription.

**Escalation: Digital footprint API (Tier 3)**
Async only — never block signup synchronously on 1.4-5s enrichment. Pattern:

```text
POST /register
  ↓
[synchronous] disposable check (<50ms) → block if hit
[synchronous] Tier 1 consortium API (~200ms) → block/phone-gate on score
  ↓ signup completes
[async job queue] Tier 3 enrichment (1.4-5s) → suspend if score > threshold
  ↓
Log full response → audit table
  ↓
Monthly: correlate signal thresholds vs confirmed fraud / chargebacks → tune
```

**Environment variables for kill-switch operation:**

```bash
EMAIL_RISK_THRESHOLD_BLOCK=75       # score >= this → reject registration
EMAIL_RISK_THRESHOLD_VERIFY=50      # score >= this → require phone/card verify
EMAIL_RISK_DISABLE=false            # kill-switch; set true to bypass all checks
```

## Gotchas

- **Issue:** Sending raw email addresses to Tier 1/2 APIs violates GDPR Article 4(1) for EU users — email is personal data. -> **Fix:** Hash email with MD5 (Tier 1 default) or SHA-256 before transmission. Confirm with vendor DPA that hashed-only mode is supported. Update Privacy Policy to mention third-party email risk scoring.

- **Issue:** `first_seen` timestamp from consortium APIs returns "just now" for any email the vendor has never seen — common for niche SaaS where user base differs from vendor's existing customers. Thresholding on `first_seen` alone produces high false-positive rates. -> **Fix:** Never use `first_seen` as a standalone gate. Compound with `is_disposable`, explicit `fraud_score`, `recent_abuse` flags, and domain WHOIS age. Use breach presence as a corroborating age signal (presence = old; absence = unknown).

- **Issue:** Digital footprint enrichment (Tier 3) takes 1.4-5 seconds — blocking signup synchronously on this signal destroys conversion. -> **Fix:** Run enrichment asynchronously post-registration. Gate the first paid action (export, purchase, API key creation) rather than account creation. Implement account suspension flow: create account → enrichment job → if threshold breached, send email "verify identity to continue".

- **Issue:** Privacy-conscious users — those using unique email aliases, no Gravatar, no social media presence, VPN — score artificially high on DIY stacks even though they are legitimate. -> **Fix:** Set DIY thresholds conservatively (require_verify at 60+, block at 85+). Provide clear human-review path for false positives. Monitor false-positive rate monthly; if >2% of real users hit require_verify, lower thresholds or add a redemption flow.

## See Also

- [[anti-fraud-behavioral-analysis]] — behavioral signals (mouse, keystroke, session timing) complementary to static email checks
- [[browser-and-device-fingerprinting]] — device-level signals to combine with email scoring at registration
- [[disposable-email-detection]] — blocklist-based throwaway detection; use as first-pass before calling reputation APIs
- [[authentication-and-authorization]] — registration flow architecture, phone/SMS verification fallback
- [[secure-backend-development]] — secure handling of third-party API credentials and PII in audit logs
- [[compliance-and-regulations]] — GDPR Article 4/6/9 obligations when scoring EU registrations; DPA requirements
- [[threat-modeling]] — matching fraud control tier (DIY vs Tier 1 vs Tier 3) to actual risk and scale

**Source data:**
- MaxMind minFraud API docs: https://dev.maxmind.com/minfraud/api-documentation/requests/
- IPQS Email Validation API: https://www.ipqualityscore.com/documentation/email-validation-api/overview
- SEON Email API: https://docs.seon.io/api-reference/email-api
- HIBP API subscription: https://haveibeenpwned.com/API/v3
- Disposable email blocklist: https://github.com/disposable-email-domains/disposable-email-domains
- RDAP bootstrap: https://data.iana.org/rdap/dns.json
