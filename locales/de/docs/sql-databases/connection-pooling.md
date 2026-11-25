---
title: "Connection Pooling"
category: concepts
tags: [sql-databases, connection-pooling, pgbouncer, proxysql, pool-sizing, postgresql, mysql]
level: 4
source_sha256: 250497c67ec869000630c23a5666cb5ab88222fa5e29cfb09c420225e8fce096
translation: machine
translated_at: '2026-10-24'
---
# Connection Pooling {#connection-pooling}

Jede Datenbankverbindung ist teuer: TCP-Handshake, TLS-Aushandlung, Authentifizierung sowie der Start eines Backend-Prozesses (PostgreSQL) bzw. die Zuweisung eines Threads (MySQL). Connection Pooling verwendet bereits aufgebaute Verbindungen über mehrere Anwendungsanfragen hinweg wieder.

## Warum Pooling {#why-pool}

- PostgreSQL: jede Verbindung = ein eigener Betriebssystemprozess (fork)
- MySQL: jede Verbindung = ein Thread
- Öffnen und Schließen pro Anfrage verschwendet Ressourcen und erhöht die Latenz
- 10 App-Instanzen x 20 Verbindungen je Instanz = 200 DB-Verbindungen ohne externen Pooler

## PgBouncer (PostgreSQL) {#pgbouncer-postgresql}

Leichtgewichtiger Proxy zwischen Anwendung und PostgreSQL.

### Pooling-Modi {#pooling-modes}

| Modus | Verhalten | Kompatibilität |
|-------|-----------|----------------|
| **Session** | Verbindung wird für die gesamte Client-Sitzung gehalten | Vollständig - alle Funktionen funktionieren |
| **Transaction** | Verbindung wird nach jeder Transaktion zurückgegeben | Keine Prepared Statements, kein SET auf Sitzungsebene, kein LISTEN/NOTIFY |
| **Statement** | Verbindung wird nach jedem Statement zurückgegeben | Bricht Multi-Statement-Transaktionen |

Der Transaction-Modus wird für die meisten Produktionsumgebungen empfohlen, da er das beste Verhältnis aus Pooling-Effizienz und Kompatibilität bietet.

### Formel zur Pool-Dimensionierung {#pool-sizing-formula}

```toml
connections = (cpu_cores * 2) + effective_spindle_count
```

Bei SSD mit 4 Kernen: ca. 9-10 Verbindungen. Mehr Verbindungen bedeuten nicht mehr Durchsatz (Overhead durch Kontextwechsel und Lock-Konkurrenz).

PgBouncer `default_pool_size = 20` pro Benutzer/Datenbank-Paar.

## ProxySQL (MySQL) {#proxysql-mysql}

Verbindungs-Multiplexing, Query-Routing, Read/Write-Splitting, Query-Caching. Der Funktionsumfang ist im MySQL-Umfeld umfangreicher als bei den entsprechenden PgBouncer-Funktionen.

## Pooling auf Anwendungsebene {#application-level-pooling}

```javascript
// Node.js with pg (node-postgres)
const { Pool } = require('pg');
const pool = new Pool({
  connectionString: 'postgresql://user:pass@host:5432/db',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

// Transaction pattern
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('INSERT INTO orders ...');
  await client.query('UPDATE inventory ...');
  await client.query('COMMIT');
} catch (e) {
  await client.query('ROLLBACK');
  throw e;
} finally {
  client.release();
}
```

## Wichtige Fakten {#key-facts}

- PgBouncer ist single-threaded (für hohen Durchsatz mehrere Instanzen einsetzen)
- Odyssey (Yandex) ist eine multi-threaded Alternative zu PgBouncer
- pgcat ist ein neuerer, in Rust geschriebener Pooler mit Sharding-Unterstützung
- Zu kleiner Connection Pool: Anfragen warten in der Warteschlange auf freie Verbindungen
- Zu großer Connection Pool: Datenbank überlastet, Overhead durch Kontextwechsel

## Fallstricke {#gotchas}

- **Prepared Statements** funktionieren im PgBouncer-Transaction-Modus nicht (Verbindung wird wiederverwendet, das Prepared Statement ist nicht mehr vorhanden)
- **SET-Befehle** gehen verloren, sobald die Verbindung in den Pool zurückgegeben wird (Sitzungseinstellungen werden zurückgesetzt)
- **Advisory Session Locks** werden freigegeben, sobald PgBouncer im Transaction-Modus die Verbindung neu zuweist
- **Lange Transaktionen** blockieren Verbindungen und verhungern andere Anfragen
- **Verbindungslecks** entstehen, wenn Verbindungen vergessen werden, an den Pool zurückgegeben zu werden
- **LISTEN/NOTIFY** erfordert Pooling im Session-Modus (persistente Verbindung)

## Siehe auch {#see-also}

- [[postgresql-configuration-tuning]] - max_connections-Einstellung
- [[postgresql-ha-patroni]] - HAProxy für das Verbindungs-Routing
- [[transactions-and-acid]] - Transaktionsverhalten mit Poolern
- [[concurrency-and-locking]] - Sperrverhalten über gepoolte Verbindungen hinweg
