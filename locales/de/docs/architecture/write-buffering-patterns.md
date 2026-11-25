---
title: "Muster für Write-Buffering"
category: reference
tags: [write-buffer, durable-objects, d1, queues, event-sourcing, offline-first, batch-insert, dirty-flag]
level: 3
source_sha256: 20db2d98bcda5cec989511218257c3dedabb820013881982068e7809c5354545
translation: machine
translated_at: '2026-10-24'
---
# Write-Buffering-Muster {#write-buffering-patterns}

Muster für Dauerhaftigkeit und Durchsatz, um hochfrequente Schreibvorgänge vor einem langsamen oder ratenbegrenzten kanonischen Datenspeicher abzufangen. Behandelt die Auswahl von Mustern, Koordination mit einem einzigen Schreiber, Constraint-Tabellen und konkrete Mechanismen im Edge-Stack.

## Wichtige Fakten {#key-facts}

- D1 (SQLite am Edge) Schreiblatenz: **200-300 ms** (Routing zum globalen Primary, SQLite mit einzelnem Schreiber); Lese-P99 ~8 ms. Quelle: Produktions-Post-Mortems, 2026.
- D1 `.batch()`-Benchmark: 5 000 Zeilen in **14 ms** gebatcht vs. **78 ms** sequenziell. Quelle: rxliuli.com, D1-Optimierungsstudie.
- D1-Harte Obergrenze: **10 GB** pro Datenbank. Migrationen rechtzeitig planen, bevor dieses Limit erreicht wird.
- D1-Batch-Constraint: **maximal 100 gebundene Parameter pro Statement**; bei 10 Spalten → 10 Zeilen pro Statement → entsprechend aufteilen.
- [[caching-and-performance]] behandelt Write-Through/Write-Behind auf konzeptioneller Ebene; dieser Artikel konzentriert sich auf Dauerhaftigkeitsmechanismen und Koordinationsprimitive.
- Cloudflare KV Eventual-Consistency-Fenster: **60 s** globale Propagation; Ratenlimit **1 Schreibvorgang/s** pro Schlüssel; Read-your-own-write nur innerhalb eines einzelnen PoP.
- Durable Object (DO) Schreiben im Speicher: **< 1 ms**; ~500-1 000 Anfragen/s pro Instanz bei moderater Logik; Instanzen sind am selben PoP wie der Routing-Worker co-lokalisiert.
- Cloudflare Queues: `max_batch_size` 1-100 (Standard 10), `max_batch_timeout` 0-60 s (Standard 5 s); At-least-once-Zustellung; 1 M Operationen/Monat inklusive, danach 0,40 $/M. Quelle: [Cloudflare Queues docs](https://developers.cloudflare.com/queues/configuration/batching-retries/).
- DO-Preise: 0,15 $/M Anfragen, 50 M geschriebene Zeilen/Monat inklusive, danach 1,00 $/M. Quelle: [Cloudflare DO pricing](https://developers.cloudflare.com/durable-objects/platform/pricing/).
- Batch-Größe für Offline-First-Synchronisation: **50 Elemente pro Chunk** ist ein empirisch validierter Sweet Spot, der Anfragegröße und Wiederherstellung bei Teilfehlern ausbalanciert.

## Musterkatalog {#pattern-catalog}

### Write-Through {#write-through}
Jeder Schreibvorgang trifft **sowohl** den schnellen Speicher (Cache/Buffer) **als auch** den kanonischen Datenspeicher synchron, bevor der Client eine ACK erhält.

- **Latenz:** volle Round-Trip-Zeit des Datenspeichers ist für den Client sichtbar (z. B. 200-300 ms bei D1)
- **Dauerhaftigkeit:** stark - kein separater Flush nötig
- **Wann verwenden:** Schreibvorgänge mit geringem Volumen, bei denen Konsistenz wichtiger ist als Geschwindigkeit; Finanzbuchungen; Operationen, die sofort von anderen Diensten lesbar sein müssen

### Write-Back (Write-Behind) {#write-back-write-behind}
Der Client schreibt in einen schnellen Buffer; ein asynchroner Prozess schreibt angesammelte Einträge gebündelt in den kanonischen Speicher.

- **Latenz für den Client:** unter einer Millisekunde (nur Schreiben in den Buffer)
- **Dauerhaftigkeitsrisiko:** Verlust des Buffers zwischen Schreibvorgang und Flush
- **Vorteil durch Zusammenführung (Coalescing):** 100 Updates auf denselben Schlüssel = 1 Schreibvorgang im Datenspeicher
- **Wann verwenden:** hochfrequente Nutzerzustände (Fortschritt, Einstellungen, Zähler); Spielzustand; jeder Workload, bei dem die DB-Latenz pro Operation nicht akzeptabel ist
- Minderung des Verlustrisikos: Buffer sofort nach Empfang in dauerhaftem Speicher ablegen (DO Storage / Redis); die In-Memory-Kopie bedient Lesezugriffe, die dauerhafte Kopie überlebt die Auslagerung

### Dirty-Flag (Tick-Muster von Game-Servern) {#dirty-flag-game-server-tick-pattern}
Der Server hält ein veränderbares In-Memory-Zustandsobjekt. Felder werden bei Mutation als dirty markiert. Ein periodischer Flush („Tick“) schreibt nur dirty Felder in den Datenspeicher und setzt die Flags zurück.

- **Granularität:** auf Feldebene, nicht auf Operationsebene - reduziert die Schreibverstärkung (Write Amplification)
- **Konfliktauflösung:** Last-Write-Wins (LWW) anhand des Zeitstempels ist die Standardstrategie, wenn mehrere Clients dasselbe Feld unabhängig voneinander aktualisieren können
- **Wann verwenden:** Entitätszustände, die sich zwischen zwei Persistierungen viele Male ändern (Lernstatus von Wörtern, Position einer Spielentität, Formularentwürfe); Synchronisation über mehrere Geräte, wenn pro Entität ein einziger kanonischer Feldwert akzeptabel ist

```javascript
// Conceptual dirty-flag flush inside a single-writer coordinator
class EntityBuffer {
  state = {};    // { fieldName: { value, ts, dirty } }

  mutate(field, value, ts) {
    const current = this.state[field];
    if (!current || ts > current.ts) {
      this.state[field] = { value, ts, dirty: true };
    }
  }

  dirtyFields() {
    return Object.entries(this.state)
      .filter(([, v]) => v.dirty)
      .map(([k, v]) => ({ field: k, value: v.value, ts: v.ts }));
  }

  markClean() {
    for (const k of Object.keys(this.state)) this.state[k].dirty = false;
  }
}
```

### Batch-Flush {#batch-flush}
Schreibvorgänge in einem Buffer sammeln (In-Memory oder dauerhafte Queue) und bei einem Zeit- oder Größenauslöser in einer einzigen transaktionalen Charge in den Datenspeicher leeren.

- **Auslöseoptionen:** verstrichene Zeit (Alarm/Cron), Schwellenwert der Buffergröße, expliziertes Signal des Clients (Navigation, Schließen des Tabs, Wiederverbindung)
- **Atomarität:** DB-seitige Batch-/Transaktionsmechanismen verwenden, damit Teilfehler keinen halb geschriebenen Zustand hinterlassen; idempotente Inserts (`INSERT OR REPLACE` / `ON CONFLICT DO UPDATE`) schützen vor erneuter Zustellung bei At-least-once
- **Wann verwenden:** jede Write-Back-Implementierung; Queue-Consumer, der in die DB schreibt; ETL-Micro-Batches; Synchronisation bei Wiederverbindung für Offline-Clients

```sql
-- LWW upsert: newer timestamp wins, avoids overwriting fresher data
INSERT INTO entity_state (user_id, key, value, updated_at)
VALUES (?, ?, ?, ?)
ON CONFLICT(user_id, key)
DO UPDATE SET
  value      = CASE WHEN excluded.updated_at > entity_state.updated_at
                    THEN excluded.value ELSE entity_state.value END,
  updated_at = MAX(excluded.updated_at, entity_state.updated_at);
```

### Event Sourcing für Nutzerzustände {#event-sourcing-for-user-state}
Append-only-Ereignislog; der aktuelle Zustand wird durch Wiedergabe oder Kompaktierung des Logs abgeleitet. Periodische Snapshots begrenzen die Kosten der Wiedergabe.

- **Schreibpfad:** jede Zustandsänderung ist ein unveränderliches Anhängen (z. B. `{userId, event: "saved", wordId, ts}`) - niemals ein Update an Ort und Stelle
- **Lesepfad:** Wiedergabe ab dem letzten Snapshot plus nachfolgende Ereignisse oder Abfrage einer materialisierten Sicht
- **Zusammenführung durch Log-Kompaktierung:** „Nutzer hat Wort X gespeichert“, danach „Nutzer hat Wort X ignoriert“ → die Kompaktierung behält nur das letztere; reduziert die Größe des kanonischen Speichers
- **Passung für Offline-First:** Der Client sammelt Ereignisse im lokalen Speicher (IndexedDB / SQLite) und synchronisiert den gesamten Ereignisstapel bei Wiederverbindung; der Server führt anhand des Zeitstempels zusammen
- **Wann verwenden:** Anforderungen an Audit-Trails; Konfliktauflösung über mehrere Geräte, wenn die vollständige Historie wichtig ist; Workloads, bei denen das Wiedergeben von Ereignissen akzeptabel ist gegenüber der Pflege einer veränderbaren Zustandstabelle
- **Wann NICHT verwenden:** einfacher CRUD-Zustand ohne Historienwert; Zähler mit hohem Volumen, bei denen der Kompaktierungsaufwand den Nutzen übersteigt

### Queues vs. Koordinator mit einem einzigen Schreiber {#queues-vs-single-writer-coordinator}

| Dimension | Message Queue (z. B. CF Queues) | Koordinator im DO-Stil |
|---|---|---|
| Zustellgarantie | At-least-once | Exactly-once (einzelner Schreiber) |
| Client-ACK | Fire-and-forget; keine Garantie für Read-after-Write | Synchrone ACK; Client kann eigene Schreibvorgänge lesen |
| Reihenfolge | FIFO pro Nachricht innerhalb der Queue; keine Reihenfolge auf Entitätsebene | Serialisiert pro Entität (eine Instanz = eine Entität) |
| Zusammenführung | Keine - jede Nachricht ist diskret | Vollständige Zusammenführung im In-Memory-Buffer |
| Kosten bei 750 K Schreibvorgängen/Tag | ~0,50 $/Monat (nach Free Tier) | ~3 $/Monat (Anfragekosten) |
| Geeignet für | Einseitige Pipelines, Analytik, Audit-Logs, wenn At-least-once akzeptabel ist | Interaktive Schreibvorgänge, Nutzerzustände, wenn Read-after-Write erforderlich ist |

## Buffering mit einem einzigen Schreiber – Durable-Object-Koordinator {#single-writer-buffering-durable-object-coordinator}

Eine einzelne DO-Instanz pro Entität (Nutzer, Session, Spielentität) serialisiert alle Schreibvorgänge, hält einen In-Memory-Buffer und verwendet einen geplanten Alarm, um in den kanonischen Speicher zu flushen.

### Warum der einzelne Schreiber wichtig ist {#why-single-writer-matters}
SQLite und ähnliche Speicher mit einem einzigen Schreiber serialisieren gleichzeitige Schreibvorgänge intern, was unter Last zu Warteschlangen führt. Die Vorserialisierung auf der Koordinatorebene wandelt N gleichzeitige Client-Schreibvorgänge in einen einzigen geplanten Batch um und beseitigt Konkurrenz.

### Alarm-Flush-Muster {#alarm-flush-pattern}

```javascript
// Cloudflare Durable Object - UserStateBuffer
export class UserStateBuffer extends DurableObject {
  buffer = [];  // in-memory; fast, lost on eviction

  async sync(payload) {
    // Persist to DO Storage first for durability across evictions
    const id = crypto.randomUUID();
    this.ctx.storage.sql.exec(
      'INSERT INTO pending (id, data) VALUES (?, ?)',
      id, JSON.stringify(payload)
    );
    this.buffer.push({ id, ...payload });

    // Schedule flush only if no alarm is already set
    if (!(await this.ctx.storage.getAlarm())) {
      await this.ctx.storage.setAlarm(Date.now() + 30_000); // 30 s window
    }
    return { ok: true };  // client ACK before D1 write
  }

  async alarm() {
    // Drain DO Storage (covers eviction scenario where in-memory buffer was lost)
    const rows = [...this.ctx.storage.sql.exec('SELECT id, data FROM pending').results];
    if (rows.length === 0) return;

    const stmts = rows.flatMap(r => buildD1Statements(JSON.parse(r.data)));
    await this.env.DB.batch(stmts);

    // Remove flushed entries
    const ids = rows.map(r => r.id);
    for (const id of ids) {
      this.ctx.storage.sql.exec('DELETE FROM pending WHERE id = ?', id);
    }
    this.buffer = this.buffer.filter(b => !ids.includes(b.id));

    // Reschedule if new writes arrived during flush
    if (this.buffer.length > 0) {
      await this.ctx.storage.setAlarm(Date.now() + 5_000);
    }
  }
}
```

```javascript
// Worker: route to per-user DO
async function handleSync(request, env) {
  const { userId, ...payload } = await request.json();
  const stub = env.USER_BUFFER.get(env.USER_BUFFER.idFromName(userId));
  return Response.json(await stub.sync(payload));
}
```

```javascript
// Helper: chunk rows respecting D1's 100 bound-parameter limit
function buildD1Statements(payload) {
  const stmts = [];
  if (payload.words) {
    for (const chunk of chunkArray(payload.words, 10)) { // 10 rows × 10 cols = 100 params
      stmts.push(buildUpsert('entity_state', chunk));
    }
  }
  return stmts;
}

function chunkArray(arr, size) {
  const out = [];
  for (let i = 0; i < arr.length; i += size) out.push(arr.slice(i, i + size));
  return out;
}
```

### Output Gates und Sichtbarkeit {#output-gates-and-visibility}
DO-Storage-Schreibvorgänge ohne dazwischenliegendes `await` werden automatisch zu einer einzigen impliziten Transaktion zusammengeführt (Cloudflare Write Coalescing). Die Client-ACK kommt vor dem D1-Commit zurück, daher müssen optimistische UI-Aktualisierungen bei Wiederverbindung anhand von Server-Zeitstempeln abgeglichen werden.

## Constraint-Tabelle {#constraints-table}

| Speicher | Schreiblatenz | Größenobergrenze | Konsistenzfenster | Ratenlimit |
|---|---|---|---|---|
| D1 (SQLite am Edge) | 200-300 ms (globales Primary) | 10 GB hart | Stark (einzelner Schreiber) | Konkurrenz bei gleichzeitigen Schreibvorgängen |
| DO Storage (SQLite) | < 5 ms (lokal zum PoP) | 1 GB pro Instanz | Stark (lokal) | ~500-1 000 Anfragen/s pro Instanz |
| Cloudflare KV | 5-10 ms Schreiben | Keine harte Obergrenze | 60 s eventuell global | 1 Schreibvorgang/s pro Schlüssel |
| Cloudflare Queues | 5-10 ms Enqueue | Limits pro Queue | At-least-once; kein Read-after-Write | 400 Nachrichten/s Standard |
| Redis (selbst gehostet) | < 1 ms | RAM-begrenzt | Konfigurierbar (AOF/RDB) | Abhängig von der Instanz |

## Offline-First-Synchronisations-Batch {#offline-first-sync-batch}

Der Client sammelt Schreibvorgänge lokal (IndexedDB für PWA, SQLite für native Mobile-Apps) und spielt den Batch bei Wiederverbindung oder Navigationsereignissen ab.

```typescript
// Client-side sync trigger
async function syncPendingWrites() {
  const pending = await localDb.getAll('pending_writes'); // IndexedDB
  if (pending.length === 0) return;

  // Chunk to 50 items per request to limit payload and enable partial retry
  for (const chunk of chunkArray(pending, 50)) {
    const res = await fetch('/api/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ client_ts: Date.now(), items: chunk }),
    });
    if (res.ok) {
      const ids = chunk.map(w => w.id);
      await localDb.deleteBatch('pending_writes', ids);
    }
    // On failure: leave chunk in local store, retry on next sync cycle
  }
}

// Trigger points
window.addEventListener('online', syncPendingWrites);
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') syncPendingWrites();
});
```

**Konfliktauflösung:** LWW anhand von `client_ts` ist ausreichend für unabhängigen Zustand pro Nutzer (Vokabular, Einstellungen). Für kollaborative Entitäten sind Vektoruhren oder Operational Transforms vorzuziehen (siehe [[distributed-systems-fundamentals]]).

## Stolperfallen {#gotchas}

- **Problem:** DO wird aus dem Speicher entfernt, bevor der Alarm auslöst; der In-Memory-Buffer geht verloren, Schreibvorgänge werden stillschweigend verworfen. -> **Lösung:** Beim Empfang immer in DO Storage (dauerhaftes SQLite) schreiben; die In-Memory-Kopie nur als Leseoptimierung behalten. `alarm()` leert den Storage, nicht `this.buffer`. Prüfen: die DO neu starten (60 s im Leerlauf lassen) und bestätigen, dass der Storage noch die ausstehenden Zeilen enthält.

- **Problem:** KV wird als Schreib-Queue verwendet; bei Spitzenlast (> 1 Schreibvorgang/s pro Schlüssel) löst das Ratenlimit 429-Fehler aus; das 60-s-Eventual-Consistency-Fenster bricht Annahmen über Read-after-Write (Client schreibt, liest sofort und erhält einen veralteten Wert von einem anderen PoP). -> **Lösung:** KV nicht als veränderbare Schreib-Queue verwenden. Stattdessen Queues (einseitige Pipeline, kein Read-after-Write) oder DO (serialisiert pro Entität mit sofortigem lokalen Lesen) verwenden. KV eignet sich für grobkörnige gemeinsame Konfiguration, nicht für veränderlichen Zustand pro Nutzer.

- **Problem:** Die harte Obergrenze von D1 von 10 GB wird ohne Warnung erreicht; alle Schreibvorgänge schlagen fehl. -> **Lösung:** Metrik `d1_storage_bytes` überwachen; Sharding planen oder rechtzeitig vor etwa 8 GB zu Postgres/Hyperdrive migrieren. D1 eignet sich für Anwendungen mit begrenzten oder archivierbaren Datensätzen; Tabellen mit stark wachsendem Nutzerzustand benötigen von Anfang an einen definierten Migrationspfad.

- **Problem:** At-least-once-Zustellung der Queue führt zu doppelten Zeilen, wenn der Consumer mitten im Batch abstürzt. Idempotenz ist nicht implementiert, daher entstehen Phantomduplikate. -> **Lösung:** `INSERT OR REPLACE` / `ON CONFLICT DO UPDATE` auf einem stabilen zusammengesetzten Schlüssel `(entity_id, event_ts)` verwenden. Für Schreibvorgänge aus Queues niemals ein einfaches `INSERT` verwenden.

- **Problem:** Der D1-Batch wird stillschweigend abgeschnitten, wenn ein einzelnes Statement 100 gebundene Parameter überschreitet (z. B. Bulk-Insert von 15 Zeilen mit 10 Spalten = 150 Parameter). Der Batch wird für andere Statements ausgeführt, das übergroße Statement wird aber verworfen. -> **Lösung:** Eingabe vor dem Erstellen des Batches auf `floor(100 / Spaltenanzahl)` Zeilen pro Statement aufteilen. Dies in der Hilfsfunktion erzwingen, die D1-Statements erstellt, nicht an der Aufrufstelle.

## Siehe auch {#see-also}

- [[caching-and-performance]] — konzeptionelle Definitionen von Write-Through/Write-Behind; Cache-Hierarchie und Invalidierungsstrategien
- [[async-event-apis]] — Zustellungssemantik (At-least-once, Webhooks, Polling); hier nicht behandelt
- [[message-broker-patterns]] — Kafka-Log-Kompaktierung, Event Sourcing im großen Maßstab, Koordination von Consumer-Gruppen
- [[distributed-systems-fundamentals]] — Vektoruhren, LWW und Uhrenabweichung, Replikationsverzögerung
- [[database-selection]] — wann von D1/SQLite zu Postgres oder einem verteilten Speicher migriert werden sollte
- [[quality-attributes-reliability]] — SLOs für Dauerhaftigkeit, Recovery Time Objectives
- [[queueing-theory]] — warum Latenz bei Schreibspitzen nichtlinear ist; Littles Gesetz angewendet auf die Dimensionierung von Batch-Flushes

**Quellenrecherche:**
- [Cloudflare DO: Rules of Durable Objects](https://developers.cloudflare.com/durable-objects/best-practices/rules-of-durable-objects/)
- [Cloudflare Blog: SQLite in every Durable Object](https://blog.cloudflare.com/sqlite-in-durable-objects/)
- [Cloudflare D1 Limits](https://developers.cloudflare.com/d1/platform/limits/)
- [Cloudflare Queues: Batching and Retries](https://developers.cloudflare.com/queues/configuration/batching-retries/)
- [Cloudflare KV: How KV Works](https://developers.cloudflare.com/kv/concepts/how-kv-works/)
- [Microsoft Azure: Event Sourcing Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [AWS: Database Caching Strategies Using Redis](https://docs.aws.amazon.com/whitepapers/latest/database-caching-strategies-using-redis/caching-patterns.html)
