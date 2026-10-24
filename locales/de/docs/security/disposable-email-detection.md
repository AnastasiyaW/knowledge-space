---
title: "Erkennung von Wegwerf-E-Mail-Adressen"
category: concepts
tags: [security, anti-fraud, email, disposable, multi-account, normalization]
level: 3
source_sha256: a77c7c4e4111eec988f792b0ef4ec9e459c2066123bf55d97f438b21ebca5827
translation: machine
translated_at: '2026-10-24'
---
# Erkennung von Wegwerf-E-Mail-Adressen {#disposable-email-detection}

Backend-Referenz zur Erkennung von Wegwerf-E-Mail-Adressen und Missbrauch durch Mehrfachkonten bei der Registrierung. Behandelt Blocklisten, DNS-Prüfungen, Adressnormalisierung und Signale zur Verknüpfung von Konten.

## Kernfakten {#key-facts}

- Statische Blocklisten erkennen 60–80 % der offensichtlichen Wegwerf-Registrierungen ohne Kosten; die Kombination kuratierter und automatisch generierter Listen erhöht die Abdeckung auf 85–90 %. Siehe [[anti-fraud-behavioral-analysis]], wie E-Mail-Signale mit Verhaltenssignalen zusammenwirken.
- Gmail-Punkt-Trick und Plus-Adressierung sind NICHT in Listen mit Wegwerf-Domains enthalten; sie erfordern eine Normalisierung zum Zeitpunkt des Schreibens.
- Dienste für Adressmaskierung im Datenschutz (`*@privaterelay.appleid.com`, `*.mozmail.com`, `*.simplelogin.co`) sind legitime Postfächer. Ein hartes Blockieren verliert wertvolle, datenschutzbewusste Nutzer; nur weich blockieren.
- Fehlende MX-Records sind ein verlässliches Signal für einen harten Fehlschlag; vorhandene MX-Records sind KEIN verlässlicher Erfolg (Catch-all-Domains akzeptieren jede Adresse).
- `disposable-email-domains/disposable-email-domains` (npm: `disposable-email-domains`) – von der Community kuratiert, ca. 3.000 Einträge, niedrige Falsch-Positiv-Rate; Aktualisierungsrhythmus: manuell.
- `disposable/disposable` (GitHub) – täglich automatisch generiert, ca. 100.000+ Domains, höhere Falsch-Positiv-Rate; als sekundäres Overlay verwenden.
- Geräte-Fingerprinting zur Verknüpfung von Mehrfachkonten erfordert eine DSGVO-Einwilligung gemäß EDPB-Leitlinien 2/2023 (Art. 5 Abs. 3 ePrivacy-Richtlinie). Siehe [[compliance-and-regulations]].
- Das Hashen von E-Mail-Adressen (SHA-256 der kanonischen Form) vor der Speicherung erfüllt den Grundsatz der Datenminimierung nach DSGVO; MaxMind minFraud akzeptiert vorgehashte E-Mail-Adressen nativ.

## Erkennungssignale {#detection-signals}

### 1. Prüfung gegen Domain-Blockliste {#1-domain-blocklist-check}

Kuratierte Liste (hart blockieren) über die automatisch generierte Liste (weich blockieren) legen. Beide Listen beim Start in den Speicher laden; die automatisch generierte Liste alle 24 h per Cron aktualisieren.

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

### 2. Adressnormalisierung (Gmail, googlemail) {#2-address-normalization-gmail-googlemail}

Beim Schreiben normalisieren und sowohl den kanonischen Hash als auch den Roh-Hash speichern. Beim Login nach dem kanonischen Hash suchen, um Duplikate derselben Person zu erkennen.

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

### 3. MX-Record-Validierung {#3-mx-record-validation}

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

### 4. Kostenpflichtige Reputations-API (MaxMind minFraud) {#4-paid-reputation-api-maxmind-minfraud}

Ein einziger Aufruf deckt `email.is_disposable`, IP-Risiko sowie Proxy- und VPN-Erkennung ab. Nur aufrufen, nachdem die kostenlosen Prüfungen bestanden wurden.

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

## Verknüpfung von Mehrfachkonten {#multi-account-linking}

### Hashing normalisierter E-Mail-Adressen {#normalized-email-hashing}

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

### Velocity des Geräte-Fingerprints {#device-fingerprint-velocity}

Bibliotheken für Geräte-Fingerprinting: ThumbmarkJS (MIT, ca. 80 % Genauigkeit im Open-Source-Modus; die Pro-API steigert sie auf ca. 99 %), FingerprintJS Pro (99,5 %, ab 99 $/Monat). Siehe [[browser-and-device-fingerprinting]] für die internen Signale.

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

### Audit-Log-Tabelle {#audit-log-table}

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

## Implementierung {#implementation}

Vollständige Python-Pipeline, die Aktualisierung der Blocklisten, Normalisierung und Entscheidung kombiniert:

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

Blocklisten täglich per Cron aktualisieren (`curl -sS <AUTOGEN_URL> -o domains.json && systemctl reload app`) oder beim Start als asynchronen Hintergrund-Task (asyncio) ausführen.

## Fallstricke {#gotchas}

- **Problem:** Blocklisten veralten – neue Wegwerfdienste (Klone von mailtm, Varianten von temp-mail) entstehen wöchentlich; die kuratierte Liste kann 3–7 Tage hinterherhinken, die automatisch generierte bis zu 24 h. -> **Lösung:** Beide Listen kombinieren; den GitHub-Releases-Feed von `disposable/disposable` abonnieren; einen täglichen Cron-Job in Betracht ziehen, der das JSON abruft und ohne Neustart in das In-Memory-Set der Anwendung nachlädt. Neue Domains (registriert vor weniger als 30 Tagen) per WHOIS markieren, als zusätzliches weiches Blockiersignal.

- **Problem:** Übermäßiges Blockieren legitimer Adressmaskierung im Datenschutz. Firefox Relay (`*.mozmail.com`), Apple Hide My Email (`*@privaterelay.appleid.com`), SimpleLogin und Addy.io tauchen in einigen automatisch generierten Listen auf – ein hartes Blockieren weist wertvolle Nutzer ab. Bleeping Computer dokumentierte 2022 den Protest der Community, als Firefox Relay in `disposable-email-domains` aufgenommen wurde. -> **Lösung:** Eine explizite Allowlist für Domains von Datenschutz-Relays pflegen; immer weich blockieren (Telefonverifizierung oder zusätzliche Bestätigung verlangen) statt hart zu blockieren; diese Domains niemals in die kuratierte Liste für hartes Blockieren aufnehmen.

- **Problem:** Gmail-Kanonisierung wird auf Nicht-Gmail-Anbieter angewendet. Yahoo und Outlook entfernen Punkte NICHT (`j.o.h.n@yahoo.com` und `john@yahoo.com` sind verschiedene Postfächer). Eine globale Anwendung der Gmail-Normalisierung erzeugt Falsch-Positiv-Duplikate für Yahoo- und Outlook-Nutzer. -> **Lösung:** Das Entfernen von Punkten auf `gmail.com` und `googlemail.com` beschränken; bei Plus-Adressierung unterstützen Fastmail und andere Anbieter sie zwar, aber nur nach Prüfung des jeweiligen Anbieterverhaltens entfernen – oder nur bei Gmail, wo es dokumentiertes Verhalten ist.

- **Problem:** DSGVO-Risiko bei der Speicherung von E-Mail-Hashes, die mit Geräte-Fingerprints verknüpft sind. Gemäß EDPB-Leitlinien 2/2023 ist die Kombination aus gehashter E-Mail-Adresse, Geräte-Fingerprint und IP-Adresse ein Profiling mit hohem Risiko; Art. 35 DSGVO kann vor dem Einsatz eine Datenschutz-Folgenabschätzung (DSFA) erfordern. -> **Lösung:** Alle E-Mail-Adressen vor der Speicherung hashen (SHA-256 der kanonischen Kleinschreibung); Einträge in `fingerprint_aggregations` in einem rollierenden 30-Tage-Fenster löschen; Roh-IP-Adressen höchstens 90 Tage speichern; die Rechtsgrundlage des berechtigten Interesses (DSGVO, Erwägungsgrund 49) in der Datenschutzerklärung und einer Interessenabwägung (Legitimate Interest Assessment) dokumentieren. Details unter [[compliance-and-regulations]].

- **Problem:** Die MX-Validierung liefert bei Catch-all-Unternehmensdomains falsch-negative Ergebnisse. `random123@small-startup.io` ist unter Umständen kein echtes Postfach, doch die Catch-all-SMTP-Konfiguration der Domain liefert einen gültigen MX-Record und akzeptiert die SMTP-Verbindung. -> **Lösung:** Die MX-Prüfung nur als harten Fehlschlag verwenden (kein MX = sicher ungültig); für mehrdeutige Adressen das Vorhandensein eines MX-Records nicht als Erfolgssignal werten; zur SMTP-Zustellbarkeitsprüfung kostenpflichtige E-Mail-Verifizierungs-APIs ergänzen (IPQualityScore, MaxMind `is_disposable`).

## Siehe auch {#see-also}

- [[anti-fraud-behavioral-analysis]] – Verhaltenssignale (Velocity, Sitzungszeitpunkte), die E-Mail-Signale ergänzen
- [[browser-and-device-fingerprinting]] – interne Funktionsweise von Geräte-Fingerprints (Canvas, WebGL, AudioContext) bei der Verknüpfung von Mehrfachkonten
- [[authentication-and-authorization]] – Token- und Session-Architektur, die bestimmt, wie Daten zur Kontoverknüpfung nach der Registrierung weitergegeben werden
- [[compliance-and-regulations]] – DSGVO Art. 5 Abs. 3, ePrivacy-Richtlinie, DSFA-Anforderungen für Fingerprinting
- [[secure-backend-development]] – Muster für Rate-Limiting, Redis-Velocity-Prüfungen, Umgang mit Geheimnissen für API-Schlüssel (MaxMind, Turnstile)
- Quellen für Blocklisten: [disposable-email-domains/disposable-email-domains](https://github.com/disposable-email-domains/disposable-email-domains), [disposable/disposable](https://github.com/disposable/disposable), [amieiro/disposable-email-domains](https://github.com/amieiro/disposable-email-domains)
- Referenz zur E-Mail-Normalisierung: [UserCheck — How to Normalize Email Addresses](https://www.usercheck.com/guides/how-to-normalize-email-addresses)
- EDPB-Leitlinien 2/2023 zu Art. 5 Abs. 3 ePrivacy: [edpb.europa.eu](https://www.edpb.europa.eu/system/files/2024-10/edpb_guidelines_202302_technical_scope_art_53_eprivacydirective_v2_en_0.pdf)
- MaxMind minFraud API-Dokumentation: [dev.maxmind.com/minfraud](https://dev.maxmind.com/minfraud/)
- Cloudflare Turnstile (Bot-Filter, kostenlos, EU-konform): [cloudflare.com/products/turnstile](https://www.cloudflare.com/application-services/products/turnstile/)
