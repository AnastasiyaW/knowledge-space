---
title: "Caching-Strategien und Performance"
category: reference
tags: [caching, redis, memcached, cdn, performance, load-balancing]
level: 4
source_sha256: d7ce41e232514e94c8a4f6afcc746d2b125a435000b8fc1c658af62aacfd9cc0
translation: machine
translated_at: '2026-10-24'
---
# Caching-Strategien und Performance {#caching-strategies-and-performance}

Caching ist eine der wirksamsten Performance-Optimierungen. Das Verständnis von Cache-Mustern, Invalidierung und der gesamten Caching-Hierarchie ist für Architekturentscheidungen entscheidend.

## Cache-Hierarchie {#cache-hierarchy}

| Schicht | Latenz | Geltungsbereich | Beispiel |
|---------|--------|-----------------|----------|
| L1/L2/L3-CPU-Cache | 1-10 ns | Einzelner Kern/CPU | Hardware |
| In-Process-Cache | ~100 ns | Einzelne Instanz | HashMap, Guava, Caffeine |
| Verteilter Cache | ~1 ms | Dienstübergreifend | Redis, Memcached |
| CDN-Cache | 1-50 ms | Globaler Edge | CloudFlare, CloudFront |
| Datenbank-Cache | 1-10 ms | Einzelne DB | Materialized Views |

## Cache-Muster {#cache-patterns}

### Cache-Aside (Lazy Loading) - Das gebräuchlichste {#cache-aside-lazy-loading-most-common}
Die Anwendung prüft zuerst den Cache. Bei einem Miss liest sie aus der DB und füllt den Cache.
- **Pro:** einfach, die Anwendung steuert die Caching-Logik
- **Contra:** veraltete Daten bis zum TTL-Ablauf oder zur expliziten Invalidierung; Cache-Miss = langsame erste Anfrage

### Read-Through {#read-through}
Der Cache liegt zwischen Anwendung und DB. Bei einem Miss lädt der **Cache selbst** die Daten aus der DB.
- **Pro:** einfacherer Anwendungscode
- **Contra:** der Cache muss die Datenquelle kennen

### Write-Through {#write-through}
Jeder Schreibvorgang geht synchron sowohl in den Cache als auch in die DB.
- **Pro:** starke Konsistenz, keine veralteten Daten
- **Contra:** höhere Schreiblatenz

### Write-Behind (Write-Back) {#write-behind-write-back}
Schreibvorgänge gehen sofort in den Cache und werden asynchron in die DB geschrieben.
- **Pro:** geringste Schreiblatenz
- **Contra:** Datenverlust-Risiko, wenn der Cache vor dem Flush ausfällt

### Refresh-Ahead {#refresh-ahead}
Einträge werden vor Ablauf proaktiv aktualisiert. Reduziert die Cache-Miss-Latenz für häufig genutzte Daten. Erfordert eine Vorhersage des Zugriffsmusters.

## Strategien zur Cache-Invalidierung {#cache-invalidation-strategies}

| Strategie | Mechanismus | Abwägung |
|-----------|-------------|----------|
| **TTL** | Einträge verfallen nach fester Dauer | Einfach, liefert aber innerhalb des Zeitfensters veraltete Daten |
| **Ereignisgesteuert** | Invalidierung bei Datenänderung (Events, CDC) | Aktuelle Daten, aber komplexer |
| **Versionierte Schlüssel** | Version im Schlüssel enthalten (`user:123:v5`) | Keine explizite Invalidierung, alte Einträge verfallen |

### Verhinderung von Cache-Stampedes {#cache-stampede-prevention}
Wenn ein beliebter Schlüssel abläuft, treffen viele Anfragen gleichzeitig auf die DB.
- **Sperren (Locking)** - nur eine Anfrage aktualisiert, die anderen warten
- **Probabilistisches frühzeitiges Verfallen** - Jitter einbauen, damit Schlüssel zu unterschiedlichen Zeitpunkten verfallen
- **Vorberechnung** - Aktualisierung vor Ablauf

## Redis vs. Memcached {#redis-vs-memcached}

| Merkmal | Redis | Memcached |
|---------|-------|-----------|
| Datentypen | Strings, Hashes, Listen, Sets, Sorted Sets, Streams | Nur Key-Value |
| Persistenz | RDB-Snapshots, AOF-Log | Keine |
| Clustering | Ja | Consistent Hashing |
| Pub/Sub | Ja | Nein |
| Threading | Single-threaded (ab 7.0 mehrere Threads) | Multi-threaded |
| Geeignet für | Komplexe Daten, Persistenz, Pub/Sub | Einfaches Caching, große Werte |

**Typische Redis-Einsatzzwecke:** Session-Store, Rate Limiting, Leaderboards, Echtzeit-Analysen.

## Caching auf verschiedenen Ebenen {#caching-at-different-layers}

- **CDN** - statische Assets (Bilder, CSS, JS), Cache-Control-Header, ETags
- **API-Gateway** - Caching von API-Antworten, TTL pro Endpunkt
- **Anwendung** - Objekt-Caching, Caching von Abfrageergebnissen
- **Seite/Fragment** - gerenderter HTML-Code für CMS, Produktseiten

## Lastverteilung {#load-balancing}

### Algorithmen {#algorithms}
- **Round Robin** / **Weighted Round Robin** - gleichmäßige oder proportionale Verteilung
- **Least Connections** - Anfrage an den am wenigsten ausgelasteten Server
- **IP Hash** - Sticky Sessions (gleicher Client, gleicher Server)
- **Consistent Hashing** - zur Verteilung von Cache-Daten

### L4 vs. L7 {#l4-vs-l7}

| Schicht | Ebene | Funktionen |
|---------|-------|-----------|
| **L4** | TCP/UDP | Schneller, keine Inhaltsprüfung |
| **L7** | HTTP | Inhaltsbasiertes Routing, SSL-Terminierung, Caching |

### Health Checks {#health-checks}
- **Aktiv** - Backend in regelmäßigen Abständen prüfen
- **Passiv** - echte Verkehrsfehler überwachen
- Fehlerhafte Backends aus dem Pool entfernen

### Session-Affinität {#session-affinity}
Sticky Sessions vereinfachen zustandsbehaftete Anwendungen, verringern aber die gleichmäßige Verteilung. **Zustandslose Backends mit externem Session-Store (Redis) bevorzugen.**

## Checkliste zur Performance-Optimierung {#performance-optimization-checklist}

1. **Zuerst profilieren** - messen, Engpässe identifizieren, die größte Wirkung zuerst optimieren
2. **Datenbank** - Indizierung, EXPLAIN ANALYZE, Auflösung von N+1-Problemen, Connection Pooling, Read Replicas
3. **Connection Pooling** - DB- und HTTP-Verbindungen wiederverwenden, Pool-Größe an die Nebenläufigkeit anpassen
4. **Komprimierung** - gzip/Brotli für Textinhalte (JSON, HTML, CSS, JS)
5. **Asynchrone Verarbeitung** - aufwendige Arbeit in Hintergrundwarteschlangen auslagern, sofort eine Job-ID zurückgeben

## Stolperfallen {#gotchas}

- **Cache-Invalidierung** gehört zu den zwei schwierigsten Problemen der Informatik (neben dem Benennen von Dingen)
- **Veralteter Cache nach einem Deployment** - neuer Code liest Daten im neuen Format, der Cache enthält das alte Format. Cache beim Deployment leeren oder versionierte Schlüssel verwenden
- **Cache-Warming** - ein kalter Cache nach einem Neustart bedeutet, dass alle Anfragen die DB treffen. Kritische Schlüssel vorab befüllen
- **Netzwerklatenz verteilter Caches** - 1 ms pro Redis-Aufruf summiert sich. Operationen mit Pipelines bündeln
- **CDN-Cache-Poisoning** - das Caching von Fehlerantworten liefert Fehler an alle Nutzer. Für Fehlerantworten `Cache-Control: no-store` setzen

## Siehe auch {#see-also}

- [[distributed-systems-fundamentals]] - Latenzwerte, Replikation
- [[queueing-theory]] - Warum Last zu nichtlinearer Verschlechterung führt
- [[rest-api-advanced]] - HTTP-Caching-Header, ETag, Cache-Control
- [[quality-attributes-reliability]] - Verfügbarkeitswerkzeuge einschließlich Auto-Scaling
