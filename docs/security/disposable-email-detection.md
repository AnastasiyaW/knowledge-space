---
title: Disposable Email Detection
category: concepts
tags: [security, anti-fraud, email, disposable, multi-account, normalization]
---

# Disposable Email Detection

Backend reference for detecting throwaway email addresses and multi-account abuse at registration. Covers blocklists, DNS checks, address normalization, and account-linking signals.

## Key Facts

- Static blocklists catch 60-80% of obvious disposable signups at zero cost; layering curated + auto-generated lists raises coverage to 85-90% — see [[anti-fraud-behavioral-analysis]] for how email signals combine with behavioral ones
- Gmail dot-trick and plus-addressing are NOT in disposable-domain lists; they require normalization at write time
- Privacy aliasing services (`*@privaterelay.appleid.com`, `*.mozmail.com`, `*.simplelogin.co`) are legitimate inboxes — hard-blocking them loses high-LTV privacy-conscious users; soft-block only
- MX absence is a reliable hard-fail signal; MX presence is NOT a reliable pass (catch-all domains accept any address)
- `disposable-email-domains/disposable-email-domains` (npm: `disposable-email-domains`) — community-curated, ~3k entries, low false-positive rate; update cadence: manual
- `disposable/disposable` (GitHub) — auto-generated daily, ~100k+ domains, higher false-positive rate; use as secondary overlay
- Device fingerprinting for multi-account linking requires GDPR consent under EDPB Guidelines 2/2023 (Art. 5(3) ePrivacy) — see [[compliance-and-regulations]]
- Hashing emails (SHA-256 of canonical form) before storing satisfies GDPR data-minimisation; MaxMind minFraud accepts pre-hashed email natively

## Detection Signals

### 1. Domain blocklist check

Layer curated list (hard-block) over auto-generated list (soft-block). Load both into memory at startup; refresh auto-generated list every 24 h via cron.

```python
import hashlib
import json
import re
from pathlib import Path
from typing import Literal

# Load curated list (npm package ships JSON; or use python equivalent)
# pip install disposable-email-domains  (Python port: pyIsEmail / disposable-email-domains)
# For the auto-generated list, fetch:
# https://raw.githubusercontent.com/disposable/disposable/master/domains.json

CURATED: set[str] = set()   # populated from disposable-email-domains
AUTO_GEN: set[str] = set()  # populated from disposable/disposable daily

def load_lists(curated_path: str, autogen_path: str) -> None:
    global CURATED, AUTO_GEN
    with open(curated_path) as f:
        CURATED = set(json.load(f))
    with open(autogen_path) as f:
        AUTO_GEN = set(json.load(f))

def check_domain(domain: str) -> Literal["block", "softblock", "pass"]:
    d = domain.lower()
    if d in CURATED:
        return "block"
    if d in AUTO_GEN:
        return "softblock"
    return "pass"
```

### 2. Address normalization (Gmail, googlemail)

Normalize at write time and store both canonical hash and raw hash. Look up by canonical hash on login to detect same-person duplicates.

```python
def canonicalize_email(email: str) -> str:
    """
    Canonical form used ONLY for dedup lookups, never shown to user.
    Covers: gmail.com, googlemail.com (dots + plus-addressing).
    Other providers (Yahoo, Outlook) do NOT strip dots — do not generalize.
    """
    local, _, domain = email.lower().strip().partition("@")
    domain = domain.strip()

    # googlemail.com is an alias for gmail.com
    if domain == "googlemail.com":
        domain = "gmail.com"

    if domain == "gmail.com":
        # Strip plus-suffix: john+anything@gmail.com -> john@gmail.com
        local = local.split("+")[0]
        # Remove dots: j.o.h.n -> john
        local = local.replace(".", "")

    return f"{local}@{domain}"

def email_hashes(raw_email: str) -> dict[str, str]:
    canonical = canonicalize_email(raw_email)
    return {
        "raw_hash": hashlib.sha256(raw_email.lower().encode()).hexdigest(),
        "canonical_hash": hashlib.sha256(canonical.encode()).hexdigest(),
        "canonical": canonical,  # store temporarily for dedup query; discard after
    }
```

### 3. MX record validation

```python
import dns.asyncresolver  # dnspython >= 2.0

async def has_mx(domain: str) -> bool:
    """No MX -> hard-block. MX present -> not sufficient (catch-all passes). Cache 24 h."""
    try:
        answers = await dns.asyncresolver.resolve(domain, "MX")
        return len(answers) > 0
    except Exception:
        return False
# Node: dns.promises.resolveMx(domain) -> records.length > 0
```

### 4. Paid reputation API (MaxMind minFraud)

Single call covers `email.is_disposable`, IP risk, proxy/VPN detection. Call only after free gates pass.

```python
# pip install minfraud
from minfraud import AsyncClient

async def minfraud_score(email_sha256: str, ip: str, fp: str | None, acct: int, key: str) -> dict:
    async with AsyncClient(account_id=acct, license_key=key) as c:
        req = {"device": {"ip_address": ip}, "email": {"address": email_sha256, "hash_address": True}}
        if fp:
            req["device"]["fingerprint"] = fp
        r = await c.score(req)
        return {
            "risk_score": r.risk_score,           # 0-100
            "is_disposable": r.email.is_disposable if r.email else None,
            "is_anonymous": r.ip_address.traits.is_anonymous if r.ip_address else None,
        }
```

## Multi-Account Linking

### Normalized-email hashing

```sql
-- Store at registration; look up on new signup
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    email_raw_hash       TEXT NOT NULL,       -- SHA-256(raw_input.lower())
    email_canonical_hash TEXT NOT NULL,       -- SHA-256(canonicalize(email))
    created_at  TIMESTAMPTZ DEFAULT now()
);
CREATE UNIQUE INDEX idx_users_canonical ON users(email_canonical_hash);

-- Signup dedup query (before INSERT):
-- SELECT id FROM users WHERE email_canonical_hash = $1 LIMIT 1;
-- Match -> same person or abuse -> block with "account already exists, try logging in"
```

### Device fingerprint velocity

Device fingerprinting libraries: ThumbmarkJS (MIT, ~80% accuracy OSS mode; Pro API upgrades to ~99%), FingerprintJS Pro (99.5%, $99+/mo). See [[browser-and-device-fingerprinting]] for signal internals.

```python
# Redis sorted-set velocity check (Python/redis-py)
import redis.asyncio as redis
import time

r = redis.Redis()

async def fingerprint_signup_count_30d(fp: str) -> int:
    key = f"fp_signups:{fp}"
    now = time.time()
    cutoff = now - 30 * 86400
    # Remove entries older than 30 days
    await r.zremrangebyscore(key, "-inf", cutoff)
    count = await r.zcard(key)
    # Record this signup attempt
    await r.zadd(key, {str(now): now})
    await r.expire(key, 31 * 86400)
    return count

# Thresholds (tune via shadow-mode data before enforcing):
# count > 3 in 30d -> soft-block (require phone verify)
# count > 10 in 30d -> hard-block
```

### Audit log table

```sql
CREATE TABLE signup_audit_log (
    id                   BIGSERIAL PRIMARY KEY,
    ts                   TIMESTAMPTZ DEFAULT now(),
    email_canonical_hash TEXT NOT NULL,
    email_raw_hash       TEXT NOT NULL,
    ip                   INET NOT NULL,
    fingerprint          TEXT,
    action               TEXT NOT NULL,   -- allow | softblock | block
    reason               TEXT NOT NULL,
    score                INT,
    signals_json         JSONB            -- full minFraud response
);
CREATE INDEX idx_audit_canonical ON signup_audit_log(email_canonical_hash);
CREATE INDEX idx_audit_fp        ON signup_audit_log(fingerprint);
CREATE INDEX idx_audit_ip        ON signup_audit_log(ip);
CREATE INDEX idx_audit_ts        ON signup_audit_log(ts);
```

## Implementation

Full Python pipeline combining blocklist refresh + normalization + decision:

```python
import asyncio
import hashlib
import json
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Literal

import aiohttp
import dns.asyncresolver
import redis.asyncio as aioredis

CURATED_URL = "https://cdn.jsdelivr.net/npm/disposable-email-domains@latest/disposable_email_blocklist.conf"
AUTOGEN_URL = "https://raw.githubusercontent.com/disposable/disposable/master/domains.json"

_curated: set[str] = set()
_autogen: set[str] = set()
_redis: aioredis.Redis | None = None


async def refresh_lists(session: aiohttp.ClientSession) -> None:
    global _curated, _autogen
    async with session.get(CURATED_URL) as r:
        text = await r.text()
        _curated = {line.strip() for line in text.splitlines() if line.strip()}
    async with session.get(AUTOGEN_URL) as r:
        _autogen = set(await r.json())


def canonicalize(email: str) -> str:
    local, _, domain = email.lower().strip().partition("@")
    if domain == "googlemail.com":
        domain = "gmail.com"
    if domain == "gmail.com":
        local = local.split("+")[0].replace(".", "")
    return f"{local}@{domain}"


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


async def mx_ok(domain: str, r: aioredis.Redis) -> bool:
    cache_key = f"mx:{domain}"
    cached = await r.get(cache_key)
    if cached is not None:
        return cached == b"1"
    try:
        answers = await dns.asyncresolver.resolve(domain, "MX")
        result = len(answers) > 0
    except Exception:
        result = False
    await r.setex(cache_key, 86400, b"1" if result else b"0")
    return result


@dataclass
class Decision:
    action: Literal["allow", "softblock", "block"]
    reason: str
    score: int


async def evaluate(
    raw_email: str,
    ip: str,
    fingerprint: str | None,
    r: aioredis.Redis,
) -> Decision:
    domain = raw_email.lower().split("@")[-1]

    # Blocklist
    if domain in _curated:
        return Decision("block", "disposable_curated", 100)
    if domain in _autogen:
        return Decision("softblock", "disposable_autogen", 70)

    # MX
    if not await mx_ok(domain, r):
        return Decision("block", "no_mx", 100)

    # Canonical dedup (pseudo — implement with real DB)
    canonical = canonicalize(raw_email)
    # exists = await db.fetchval("SELECT 1 FROM users WHERE email_canonical_hash=$1", sha256(canonical))
    # if exists: return Decision("block", "canonical_duplicate", 100)

    # Fingerprint velocity
    if fingerprint:
        key = f"fp:{fingerprint}"
        now = time.time()
        await r.zremrangebyscore(key, "-inf", now - 30 * 86400)
        count = await r.zcard(key)
        await r.zadd(key, {str(now): now})
        await r.expire(key, 31 * 86400)
        if count > 10:
            return Decision("block", "fp_velocity", 90)
        if count > 3:
            return Decision("softblock", "fp_velocity_warn", 65)

    # IP velocity
    ip_key = f"ip_h:{ip}"
    ip_count = int(await r.incr(ip_key))
    if ip_count == 1:
        await r.expire(ip_key, 3600)
    if ip_count > 5:
        return Decision("softblock", "ip_velocity", 60)

    return Decision("allow", "clean", 0)


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        await refresh_lists(session)

    r = aioredis.Redis()
    result = await evaluate("john.doe+test@gmail.com", "1.2.3.4", "fp-abc123", r)
    print(result)  # Decision(action='allow', reason='clean', score=0)
    # canonical: johndoe@gmail.com — dots and suffix stripped


if __name__ == "__main__":
    asyncio.run(main())
```

Refresh blocklists daily via cron (`curl -sS <AUTOGEN_URL> -o domains.json && systemctl reload app`) or as a background asyncio task at startup.

## Gotchas

- **Issue:** Blocklists go stale — new throwaway services (mailtm clones, temp-mail variants) launch weekly; curated list may lag 3-7 days, auto-generated up to 24 h. -> **Fix:** Layer both lists; subscribe to `disposable/disposable` GitHub releases feed; consider a daily cron that fetches the JSON and hot-reloads into the application's in-memory set without restart. Flag recent domains (registered < 30 days) via WHOIS as additional soft-block signal.

- **Issue:** Over-blocking legitimate privacy aliasing. Firefox Relay (`*.mozmail.com`), Apple Hide My Email (`*@privaterelay.appleid.com`), SimpleLogin, Addy.io appear in some auto-generated lists — hard-blocking them rejects high-LTV users. Bleeping Computer documented community backlash when Firefox Relay was added to `disposable-email-domains` in 2022. -> **Fix:** Maintain an explicit allowlist of privacy-relay domains; always soft-block (require phone verify or additional confirmation) rather than hard-block; never add these to the curated hard-block list.

- **Issue:** Gmail catch-all canonicalization applied to non-Gmail providers. Yahoo and Outlook do NOT strip dots (`j.o.h.n@yahoo.com` and `john@yahoo.com` are different inboxes). Applying Gmail normalization globally causes false-positive duplicates for Yahoo/Outlook users. -> **Fix:** Scope dot-removal to `gmail.com` and `googlemail.com` only; for plus-addressing, Fastmail and others do support it, but strip only after confirming the provider's behavior — or strip only for Gmail where it is documented behavior.

- **Issue:** GDPR exposure when storing email hashes linked to device fingerprints. Under EDPB Guidelines 2/2023, combining hashed email + device fingerprint + IP is high-risk profiling; Art. 35 GDPR may require a DPIA before deployment. -> **Fix:** Hash all emails (SHA-256 of canonical lowercase) before storage; purge `fingerprint_aggregations` entries on a 30-day rolling window; store raw IPs for ≤ 90 days max; document legitimate interest basis (GDPR Recital 49) in Privacy Policy and a Legitimate Interest Assessment — details in [[compliance-and-regulations]].

- **Issue:** MX validation returns false-negative for catch-all corporate domains. `random123@small-startup.io` may not be a real inbox but the domain's catch-all SMTP will return a valid MX record and accept the SMTP connection. -> **Fix:** Use MX check only as a hard-fail signal (no MX = definitely invalid); do not use MX presence as a pass signal for ambiguous addresses; supplement with paid email verification APIs (IPQualityScore, MaxMind `is_disposable`) for SMTP-level deliverability confirmation.

## See Also

- [[anti-fraud-behavioral-analysis]] — behavioral signals (velocity, session timing) that complement email-level signals
- [[browser-and-device-fingerprinting]] — device fingerprint internals (canvas, WebGL, AudioContext) used in multi-account linking
- [[authentication-and-authorization]] — token and session architecture that determines how account-linking data is propagated post-signup
- [[compliance-and-regulations]] — GDPR Art. 5(3), ePrivacy Directive, DPIA requirements for fingerprinting
- [[secure-backend-development]] — rate-limiting patterns, Redis velocity checks, secrets handling for API keys (MaxMind, Turnstile)
- Blocklist sources: [disposable-email-domains/disposable-email-domains](https://github.com/disposable-email-domains/disposable-email-domains), [disposable/disposable](https://github.com/disposable/disposable), [amieiro/disposable-email-domains](https://github.com/amieiro/disposable-email-domains)
- Email normalization reference: [UserCheck — How to Normalize Email Addresses](https://www.usercheck.com/guides/how-to-normalize-email-addresses)
- EDPB Guidelines 2/2023 on Art. 5(3) ePrivacy: [edpb.europa.eu](https://www.edpb.europa.eu/system/files/2024-10/edpb_guidelines_202302_technical_scope_art_53_eprivacydirective_v2_en_0.pdf)
- MaxMind minFraud API docs: [dev.maxmind.com/minfraud](https://dev.maxmind.com/minfraud/)
- Cloudflare Turnstile (bot filter, free, EU-compliant): [cloudflare.com/products/turnstile](https://www.cloudflare.com/application-services/products/turnstile/)
