---
title: "REST-API Fortgeschritten - Performance, Versionierung, Caching"
category: reference
tags: [rest, api, caching, rate-limiting, versioning, retry]
level: 4
source_sha256: 790494f424d524b0887feaf883ea33ecef1ec7bc20c15dbe117686dbca3d7dc8
translation: machine
translated_at: '2026-10-24'
---
# REST-API Fortgeschritten - Performance, Versionierung, Caching {#rest-api-advanced-performance-versioning-caching}

Die Performance einer API hängt von Geschwindigkeit, Datenvolumen und Aufrufhäufigkeit ab. Faktoren wie mobile Datenkosten, Akkuverbrauch auf Geräten und die Abrechnung bei Serverless-Architekturen machen Effizienz entscheidend.

## Rate Limiting und Throttling {#rate-limiting-and-throttling}

### Rate Limiting auf Anfrageebene {#request-level-rate-limiting}
Anfragen pro Zeitfenster begrenzen, nach IP-Adresse, API-Schlüssel oder Benutzer. Bei Überschreitung:
- **HTTP 429 Too Many Requests**
- `X-Rate-Limit-Limit` - erlaubte Anfragen im aktuellen Zeitraum
- `X-Rate-Limit-Remaining` - verbleibende Anfragen
- `X-Rate-Limit-Reset` - Sekunden bis zum Zurücksetzen des Zeitraums

### Algorithmen für Rate Limiting {#rate-limiting-algorithms}
- **Fixed Window** - einfacher Zähler pro Zeitfenster
- **Sliding Window** - genauer, verhindert Lastspitzen an der Fenstergrenze
- **Token Bucket** - erlaubt kurze Lastspitzen bei gleichbleibender Durchschnittsrate (am gebräuchlichsten)
- **Leaky Bucket** - gleichmäßige Ausgaberate, unabhängig von der Eingaberate

### Throttling auf Anwendungsebene {#application-level-throttling}
Interner Schutz vor Lastspitzen. Priorisiert dringende Anfragen. Umgesetzt über Verzögerungen oder Batch-Verarbeitung.

## HTTP-Caching-Strategien {#http-caching-strategies}

### Vier Caching-Ansätze {#four-caching-approaches}

| Strategie | Header | Anwendungsfall |
|----------|--------|----------------|
| **Kein Cache** | `Cache-Control: private, no-cache, no-store` | Vertrauliche/dynamische Daten |
| **Zeitbasiert** | `Cache-Control: max-age=3600, must-revalidate` | Bekanntes Änderungsintervall |
| **Validierungsbasiert** | `Cache-Control: no-cache` + `ETag` | Unbekanntes Änderungsintervall |
| **Unbegrenzt cachen** | `Cache-Control: max-age=31536000, public, immutable` | Unveränderliche Inhalte |

### Validierungsablauf (ETag) {#validation-flow-etag}
```rust
1. Server responds with: ETag: "abc123"
2. Client conditional request: If-None-Match: "abc123"
3. Server responds: 304 Not Modified (use cache)
   OR sends new data with new ETag
```

### Cache-Verwaltung {#cache-management}
- Dateien unbegrenzt cachen, mit versionierten Namen (`style1a.css`)
- Bei Aktualisierung umbenennen zu `style2b.css` - der Browser behandelt sie als neue Ressource
- Vollständige Invalidierung: `Clear-Site-Data: "cache", "cookies", "storage"`

## Komprimierung {#compression}

Keine Änderung am API-Design nötig:
```yaml
# Client
Accept-Encoding: gzip, deflate, br

# Server
Content-Encoding: gzip
```

## Batch-Anfragen {#batch-requests}

Mehrere API-Operationen zu einer zusammenfassen. Reduziert Latenz und spart Bandbreite. Alle Teilanfragen werden in einer einzigen Anfrage gebündelt; die Antworten werden gemeinsam zurückgegeben. Als Referenz dient das Batch-Format der Google Drive API.

## API-Versionierung {#api-versioning}

### Warum versionieren {#why-version}
- Abwärtskompatibilität für bestehende Clients sicherstellen
- Klare Kommunikation der verfügbaren Funktionen
- Clients ermöglichen, in ihrem eigenen Tempo zu migrieren

### Semantische Versionierung {#semantic-versioning}
- **Nicht breaking** (neue Endpunkte, neue optionale Felder, neue Antwortfelder): Minor-Erhöhung (1.0 -> 1.1)
- **Breaking** (entfernte Endpunkte, geänderte Pflichtfelder, geänderte Fehlercodes): Major-Erhöhung (1.x -> 2.0)
- Maximal 2 aktive Versionen parallel betreiben; Clients über die Abkündigung informieren

### Versionierungsansätze {#versioning-approaches}

| Ansatz | Beispiel | Hinweise |
|--------|----------|----------|
| **URL-Pfad** | `/api/v1/users` | Am gebräuchlichsten, explizit |
| **Query-Parameter** | `/api/users?version=1` | Einfach, aber unübersichtlich |
| **Header** | `Accept: application/vnd.api.v1+json` | Sauberere URLs |

### Migration der API ohne Ausfallzeit {#zero-downtime-api-migration}
- Abkündigungen mit klarem Zeitplan ankündigen
- Nutzung alter Versionen vor der Entfernung überwachen
- Alte API-Versionen länger als erwartet bereitstellen, denn manche Clients rufen APIs nur einmal im Jahr auf
- Expand-Contract-Muster: Neues neben Altem bereitstellen, migrieren, Altes entfernen

## Retry-Muster {#retry-patterns}

### Exponentielles Backoff {#exponential-backoff}
Mit kurzer Verzögerung beginnen und exponentiell erhöhen: 5s -> 25s -> 125s

### Jitter {#jitter}
Zufällige Anteile zu den Wiederholungsverzögerungen hinzufügen, damit nicht viele Clients gleichzeitig wiederholen und eine Lawine (Thundering Herd) auslösen.

### Regeln für Wiederholungen {#retry-rules}
- Nur bei transienten Fehlern wiederholen (5xx, Netzwerk-Timeouts)
- Client-Fehler (4xx) nicht wiederholen, denn sie lösen sich nicht von selbst
- Maximale Anzahl an Wiederholungen festlegen
- Für dauerhafte Fehler einen Circuit Breaker in Betracht ziehen

## Format von Fehlerantworten {#error-response-format}

Einheitliches Format über alle APIs hinweg:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {"field": "email", "issue": "invalid format"}
    ]
  }
}
```

Interne Fehlerdetails (Stack-Traces, SQL-Abfragen) niemals in der Produktion offenlegen.

## Fallstricke {#gotchas}

- **Caching und Authentifizierung** - Antworten mit `Authorization`-Header niemals cachen, außer sie sind ausdrücklich `public`
- **429 ohne Header** - immer Rate-Limit-Header mitsenden, damit Clients sich selbst drosseln können
- **Wiederholung bei POST** - ohne Idempotenz-Schlüssel gefährlich, kann doppelte Ressourcen erzeugen
- **Cache Stampede** - läuft ein beliebter Schlüssel ab, treffen viele Anfragen gleichzeitig die Datenbank. Mit Sperren oder probabilistischem frühzeitigem Ablauf gegensteuern
- **CPU-Kosten der Komprimierung** - für Textinhalte (JSON, HTML) aktivieren, nicht aber für bereits komprimierte Inhalte (Bilder, Video)

## Siehe auch {#see-also}

- [[http-rest-fundamentals]] - HTTP-Protokoll, REST-Constraints, Ressourcendesign
- [[api-authentication-security]] - OAuth 2.0, JWT, TLS
- [[caching-and-performance]] - Caching-Muster auf Anwendungsebene
- [[api-documentation-specs]] - OpenAPI, Swagger, AsyncAPI
