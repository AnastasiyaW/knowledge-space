---
title: "HTTP- und REST-API-Grundlagen"
category: reference
tags: [http, rest, api, web-services, protocol]
level: 2
source_sha256: f90ebbe43261a72beddd0205bab71e1e58ba4f970a48e8298b79d4f2a1f27fc7
translation: machine
translated_at: '2026-10-24'
---
# HTTP- und REST-API-Grundlagen {#http-and-rest-api-fundamentals}

REST (Representational State Transfer) ist ein Architekturstil für verteilte Systeme und kein Protokoll. Er passt zur Architektur des Internets und nutzt die vorhandene HTTP-Infrastruktur. REST ist der meistverbreitete API-Stil für öffentliche APIs.

## HTTP-Protokoll {#http-protocol}

### Aufbau von Request und Response {#requestresponse-structure}

```html
# Request
<METHOD> <URI> HTTP/<VERSION>
<Headers>
<Empty line>
<Body>

# Response
HTTP/<VERSION> <STATUS_CODE> <REASON>
<Headers>
<Empty line>
<Body>
```

### HTTP-Methoden {#http-methods}

| Methode | CRUD | Idempotent | Sicher | Hat Body |
|---------|------|------------|--------|----------|
| GET | Lesen | Ja | Ja | Nein |
| POST | Erstellen | Nein | Nein | Ja |
| PUT | Vollständiges Aktualisieren/Erstellen | Ja | Nein | Ja |
| PATCH | Teilweises Aktualisieren | Nein* | Nein | Ja |
| DELETE | Löschen | Ja | Nein | Optional |
| HEAD | Header lesen | Ja | Ja | Nein |
| OPTIONS | Fähigkeiten abfragen | Ja | Ja | Nein |

*PATCH kann durch eine geeignete Implementierung idempotent gemacht werden.

**Idempotent** = Mehrfach identisch ausgeführte Requests erzeugen dasselbe Ergebnis. **Sicher** = Verändert den Serverzustand nicht.

### Statuscodes {#status-codes}

| Bereich | Bedeutung | Wichtige Codes |
|---------|-----------|----------------|
| 2xx | Erfolg | 200 OK, 201 Created, 204 No Content |
| 3xx | Weiterleitung | 301 Moved Permanently, 304 Not Modified |
| 4xx | Client-Fehler | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| 5xx | Server-Fehler | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

### Wichtige Header {#key-headers}

**Request:** `Host` (in HTTP/1.1 erforderlich), `Content-Type`, `Accept`, `Authorization`, `Cache-Control`, `User-Agent`

**Response:** `Content-Type`, `Content-Length`, `Cache-Control`, `ETag`, `Last-Modified`, `Set-Cookie`

### HTTP-Versionen {#http-versions}

| Version | Wichtige Merkmale |
|---------|-------------------|
| HTTP/1.0 | Ein Request pro TCP-Verbindung |
| HTTP/1.1 | Persistente Verbindungen, Host-Header, Chunked Transfer, Pipelining |
| HTTP/2 | Binäres Framing, Multiplexing, Header-Kompression (HPACK), Server Push |
| HTTP/3 | Basiert auf QUIC (UDP), geringere Latenz, bessere Performance im Mobilfunk |

## Die sechs REST-Constraints {#rest-six-constraints}

1. **Client-Server** - Trennung der Belange von UI und Datenspeicherung
2. **Zustandslos (Stateless)** - Jeder Request enthält alle Informationen, die zu seiner Verarbeitung nötig sind
3. **Cacheable** - Antworten deklarieren, ob sie cachebar sind oder nicht
4. **Einheitliche Schnittstelle (Uniform Interface)** - Ressourcenidentifikation über URIs, Manipulation über Repräsentationen, selbstbeschreibende Nachrichten, HATEOAS
5. **Geschichtetes System (Layered System)** - Der Client kann nicht erkennen, ob er direkt mit dem Server oder über einen Intermediär verbunden ist
6. **Code on Demand** (optional) - Der Server kann ausführbaren Code (JavaScript) übertragen

## Ressourcenbasiertes URL-Design {#resource-based-url-design}

```sql
# Resources are nouns, not verbs
/users            # collection
/users/123        # specific resource
/users/123/orders # nested resource

# Actions via HTTP methods, not URL
DELETE /users/123          # correct
POST /users/123/delete     # wrong

# Naming conventions
/order-items     # hyphens for multi-word
/users/123       # plurals
                 # lowercase, no trailing slashes, no file extensions
```

## REST-Ressourcentypen {#rest-resource-types}

| Typ | Beschreibung | ID-Quelle |
|-----|--------------|-----------|
| **Object** | Einzelne Ressource mit eindeutiger ID | - |
| **Collection** | Vom Server verwalteter Katalog | Server generiert IDs |
| **Store** | Vom Client verwalteter Speicher | Client vergibt IDs |
| **Controller** | Aktion/Funktion (RPC-ähnlich) | POST-basiert |

## Filtern, Paginierung, Suche {#filtering-pagination-search}

### Paginierungsansätze {#pagination-approaches}

| Ansatz | Beispiel | Vor-/Nachteile |
|--------|----------|----------------|
| **Offset-basiert** | `?offset=20&limit=10` | Einfach, erlaubt Sprünge; inkonsistent bei Live-Daten |
| **Cursor-basiert** | `?cursor=abc123&limit=10` | Stabil bei Live-Daten; kein Sprung auf beliebige Seiten |
| **Keyset-basiert** | `?after_id=100&limit=20` | Sehr performant bei indizierten Spalten |

### Filtern und Sortieren {#filtering-and-sorting}

```bash
?status=active&created_after=2024-01-01    # filtering
?sort=created_at&order=desc                # sorting
?q=search+term                             # full-text search
```

## Dateiübertragung {#file-transfer}

```yaml
# Client request
Accept: image/png

# Server response
Content-Type: image/png
Content-Disposition: attachment; filename="file.png"
Content-Length: 12345

# Large files
Transfer-Encoding: chunked
```

## CORS (Cross-Origin Resource Sharing) {#cors-cross-origin-resource-sharing}

Sicherheitsmechanismus des Browsers. Der Server deklariert erlaubte Origins:
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`

Für nicht einfache Requests werden Preflight-Anfragen (OPTIONS) gesendet. Entscheidend für die Integration von Frontend und Backend.

## Vergleich der API-Stile {#api-style-comparison}

| Aspekt | REST | JSON-RPC | GraphQL | gRPC |
|--------|------|----------|---------|------|
| Paradigma | Ressourcenorientiert | Funktionsorientiert | Abfrageorientiert | Funktionsorientiert |
| Transport | HTTP | HTTP/TCP/WS | HTTP | HTTP/2 |
| Format | JSON/XML | JSON | JSON-ähnlich | Protobuf (binär) |
| Caching | Nativ über HTTP | Schwierig | Schwierig | Schwierig |
| Typisierung | Schwach (OpenAPI) | Schwach | Stark (Schema) | Stark (Proto) |
| Geeignet für | Öffentliche APIs, CRUD | Einfache interne APIs | Komplexe Abfragen | Microservices |

## Stolperfallen {#gotchas}

- **PUT ersetzt vollständig** - Es muss die gesamte Ressource gesendet werden, nicht nur Teile. Für partielle Updates PATCH verwenden
- **POST ist nicht idempotent** - Mehrfach identische Aufrufe erzeugen Duplikate, sofern keine Deduplizierung implementiert ist
- **HTTP 200 bei SOAP-Fehlern** - SOAP liefert für Fachfehler 200, nur für Protokollfehler 4xx
- **HATEOAS** ist Bestandteil der REST-Spezifikation, wird in der Praxis aber selten umgesetzt
- **URL-Versionierung** (`/api/v1/users`) ist am gebräuchlichsten; maximal 2 aktive Versionen beibehalten

## Siehe auch {#see-also}

- [[rest-api-advanced]] - Rate Limiting, Caching-Strategien, Batch-Requests, Retry-Muster
- [[api-authentication-security]] - OAuth 2.0, JWT, mTLS, CORS im Detail
- [[graphql-api]] - Abfragesprache für flexibles Laden von Daten
- [[grpc-api]] - Hochperformantes binäres RPC-Framework
