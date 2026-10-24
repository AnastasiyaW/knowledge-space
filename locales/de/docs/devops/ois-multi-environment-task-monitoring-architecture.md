---
level: 2
source_sha256: 64f5a98626c89e7aa3b1118807baa79542f52fccbc1d48436125f18f8c96ab18
translation: machine
translated_at: '2026-10-24'
---
# OIS-Architektur für die Aufgabenüberwachung über mehrere Umgebungen {#ois-multi-environment-task-monitoring-architecture}

Die OIS-Infrastruktur nutzt ein einheitliches Monorepo-Deployment über Staging- und Produktionsumgebungen (RU und EN). Die Code-Pfade sind identisch, die Umgebungen sind jedoch durch eigene Datenbank-Hosts, S3-Zugangsdaten und Redis-Instanzen voneinander getrennt. Für die Überwachung von Aufgaben über diese Umgebungen müssen Daten aus zwei getrennten Zustandsspeichern aggregiert werden: PostgreSQL für die Persistenz und Redis für den Live-Ausführungszustand.

## Datenquellen und Parität der Umgebungen {#data-sources-and-environment-parity}
Jede Umgebung betreibt dieselben Service-Images (`oisgold/<service>`). Unterschiede zwischen den Umgebungen beruhen ausschließlich auf der Konfiguration (Umgebungsvariablen).

- **Datenbankpersistenz:** PostgreSQL speichert die Aufgabenmetadaten in der Tabelle `chat_message`.
- **Live-Queue-Zustand:** Redis BullMQ verwaltet den Ausführungszyklus von Jobs über fünf Prioritätsstufen.
- **Admin-API:** Eingehängt unter `/api/chat/admin/` und geschützt durch die Middleware `checkAdmin`, die einen JWT oder ein Session-Cookie mit `role: 'admin'` voraussetzt.

## Persistenz des Zustands auf Nachrichtenbasis in PostgreSQL {#postgresql-message-based-state-persistence}
Das System verwendet keine eigene Tabelle `tasks`. Stattdessen sind Aufgaben spezielle Zeilen der Tabelle `chat_message`, die über einen JSON-Blob im Feld `text` identifiziert werden.

### Erkennung von Aufgaben und Ableitung des Status {#task-detection-and-status-derivation}
Eine Zeile gilt als Aufgabe, wenn das Feld `text` ein JSON-Objekt mit einem Array `items` ist. Der Status wird nicht als Spalte gespeichert, sondern dynamisch aus JSON-Eigenschaften abgeleitet: `done`, `stopped`, `canceled` und `items[].output`.

```sql
-- Query to identify active (not-done) tasks across all environments
SELECT id, chat_id, created_at, text
FROM chat_message
WHERE text LIKE '{%' 
  AND text::jsonb ? 'items'
  AND coalesce((text::jsonb->>'done')::boolean, false) = false
  AND coalesce((text::jsonb->>'stopped')::boolean, false) = false
  AND coalesce((text::jsonb->>'canceled')::boolean, false) = false
ORDER BY created_at DESC;
```

## Verwaltung der Redis-BullMQ-Queues {#redis-bullmq-queue-management}
Live-Zustände von Jobs (`waiting`, `active`, `delayed`, `paused`, `failed`) liegen in BullMQ. OIS verwendet fünf spezifische Queues für unterschiedliche Prioritätsstufen und Systemaufgaben.

| Queue | Prioritätsstufe | Zielnutzer / Anwendungsfall |
|---|---|---|
| `image-high` | Hoch | Enterprise- und Corporate-Tarife |
| `image-medium` | Mittel | Standard- und Pro-Nutzer |
| `image-low` | Niedrig | Nutzer des kostenlosen Plans |
| `main` | System | Abrechnung, Webhooks und E-Mail-Versand |
| `dead-letter` | k. A. | Wiederholte Jobs (10 Versuche, exponentielles Backoff) |

### Identifikation von Jobs {#job-identification}
BullMQ-Jobs enthalten in `job.data` eine Payload mit `{messageId, inputFileId}`. Diese Metadaten sind entscheidend, um Redis-Jobs mit PostgreSQL-Zeilen abzugleichen und „verwaiste“ Aufgaben zu erkennen, also Datenbankzeilen, die als eingereiht markiert sind, für die aber kein entsprechender Redis-Job existiert.

## Aggregationsstrategie: das Collector-Muster {#aggregation-strategy-the-collector-pattern}
Um eine einheitliche Sicht bereitzustellen, ohne die Produktionsdienste zu verändern, wird ein Aggregator im Pull-Modell (Collector) implementiert.

1. **Redis-Subscription:** Collectors verwenden BullMQ `QueueEvents`, um in Echtzeit auf die Ereignisse `waiting`, `active` und `completed` zu lauschen.
2. **PostgreSQL-Polling:** Ein periodischer Abruf (30–60 s) identifiziert verwaiste Aufgaben und aktualisiert den Zustand des einheitlichen Dashboards.
3. **Vertrauensgrenze intern:** Der Aggregator sollte idealerweise innerhalb der VPC laufen oder langlebige Service-JWTs verwenden, um die üblichen Anforderungen an Session-Cookies zu umgehen.

## Administrative Aktions-API {#administrative-action-api}
Operatoren verwalten hängende oder fehlgeschlagene Jobs über die Endpunkte unter `/api/chat/admin/tasks`.

### Neustart und Wiederherstellung {#restart-and-recovery}
- **Massen-Neustart:** `POST /tasks/restart` mit `messageIds[]` stellt alle unvollständigen Dateien bestimmter Nachrichten erneut in die Queue ein.
- **Gezielter Neustart:** `POST /tasks/restart-file` betrifft eine einzelne `inputFileId`.
- **Wiederherstellung aus der DLQ:** `POST /tasks/dlq/retry` entfernt die DLQ-Metadaten und gibt den Job an seine ursprüngliche Queue zurück.

### Stoppen und Drosseln {#stopping-and-throttling}
- **Aufgabe stoppen:** `POST /tasks/stop` markiert die DB-Zeile als `stopped=true` und entfernt den Job aus Redis, während vorhandene Ausgaben erhalten bleiben.
- **Queue pausieren:** `Queue.pause()` ist über die BullMQ-API verfügbar, erfordert aber einen eigenen Admin-Endpunkt, um die Ausführung für eine ganze Prioritätsstufe umzuschalten (z. B. das Pausieren von `image-low` bei Lastspitzen).

## Stolperfallen {#gotchas}
- **Problem:** Der Aufgabenstatus ist im JSON verborgen → **Lösung:** `jsonb`-Indizes oder eine PostgreSQL-View verwenden, um sequenzielle Scans beim Filtern von Tausenden Zeilen zu vermeiden.
- **Problem:** Redis-Ereignisse können während eines Ausfalls des Collectors verloren gehen → **Lösung:** Beim Start des Collectors immer einen vollständigen PostgreSQL-Snapshot erstellen und die Redis-Queues scannen (`getJobs`), um den Zustand neu zu synchronisieren.
- **Problem:** Das Pausieren einzelner Jobs wird in OIS nicht nativ unterstützt → **Lösung:** Den Endpunkt `/tasks/stop` verwenden; er hält die Arbeit effektiv an, indem der Job aus der Queue entfernt wird, und erlaubt ein späteres `restart`.
- **Problem:** Ablauf des Auth-Cookies → **Lösung:** Für lang laufende Monitore einen Bearer-JWT verwenden, der mit dem privaten Schlüssel der Umgebung signiert ist, statt das Session-Cookie eines menschlichen Operators zu nutzen.

## Siehe auch {#see-also}
- [[monitoring-and-observability]]
- [[docker-fundamentals]]
- [[microservices-patterns]]
- [[runpod-production]]
