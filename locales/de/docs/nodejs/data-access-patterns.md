---
title: "Data Access Patterns"
category: patterns
tags: [nodejs, repository, active-record, cursor, transaction, dal, orm]
level: 3
source_sha256: d060aced476d97051e3d32693217a65c422377dba0020d14df94da8897fdaa50
translation: machine
translated_at: '2026-10-24'
---
# Datenzugriffsmuster {#data-access-patterns}

Die Data-Access-Layer (DAL) trennt die Geschäftslogik von der physischen Speicherung und stellt abstrakte CRUD-Operationen, die Verwaltung von Connection Pools sowie sitzungsbezogene Verbindungen bereit. Node.js-Anwendungen profitieren von Repository-, Active-Record-, Cursor- und Transaction-Mustern sowohl für Datenbank- als auch für In-Memory-Daten.

## Wichtige Fakten {#key-facts}

- Geschäftslogik sollte NIEMALS rohe Datenbankabfragen enthalten
- Die DAL bietet: API-Funktionen, gecachte Schemas/Daten, Connection Pools, sitzungs-/benutzerbezogene Verbindungen
- Verschiedene Benutzer können unterschiedliche DB-Berechtigungen haben – Connection Pools müssen benutzerbezogene Verbindungen unterstützen
- **Repository** wird bei komplexen Domänen bevorzugt: mehrere Repositories pro Entität (User für Personalwesen, Abrechnung, Zugriffskontrolle)
- **Active Record** ist einfacher, vermischt jedoch Belange: Ein Objekt wird direkt auf eine DB-Zeile abgebildet, mit integriertem save/delete
- Cache in der DAO-Schicht, wenn er von Implementierungsdetails abhängt (Cache nach ID); Cache in der Service-Schicht, wenn er von der Geschäftslogik abhängt
- ORM-Kritik: TypeORM erzwingt unnötigen Boilerplate-Code; Prisma erzeugt typunsicheren Code (`any`-Rückgaben)

## Muster {#patterns}

### Repository-Muster {#repository-pattern}

```js
// Clean separation of domain and persistence
class UserRepository {
  #pool;
  constructor(pool) { this.#pool = pool; }

  async findById(id) {
    const { rows } = await this.#pool.query(
      'SELECT * FROM users WHERE id = $1', [id]
    );
    return rows[0] ? this.#toDomain(rows[0]) : null;
  }

  async save(user) {
    await this.#pool.query(
      'INSERT INTO users (id, name, email) VALUES ($1, $2, $3) ON CONFLICT (id) DO UPDATE SET name = $2, email = $3',
      [user.id, user.name, user.email]
    );
  }

  #toDomain(row) { return { id: row.id, name: row.name, email: row.email }; }
}
```

### In-Memory-Transaktionen {#in-memory-transactions}

```js
class Transaction {
  #operations = [];
  #committed = false;

  add(operation) { this.#operations.push(operation); }

  commit() {
    for (const op of this.#operations) op.execute();
    this.#committed = true;
  }

  rollback() {
    if (this.#committed) {
      for (const op of this.#operations.reverse()) op.undo();
    }
    this.#operations = [];
  }
}
```

Selbst reine JavaScript-Anwendungen profitieren von transaktionalen Mustern bei komplexen Zustandsänderungen.

### Template Method für Geschäftsoperationen {#template-method-for-business-operations}

```js
class MoneyTransfer {
  async process(request) {
    await this.validate(request);     // overridable
    await this.checkBalance(request); // overridable
    await this.execute(request);      // overridable
    await this.notify(request);       // overridable
  }
}

class InternationalTransfer extends MoneyTransfer {
  async validate(request) { /* compliance checks */ }
  async execute(request) { /* SWIFT/correspondent bank */ }
}
```

## Anti-Muster bei der Datenbankintegration {#database-integration-anti-patterns}

### Problem der gemeinsam genutzten Datenbank {#shared-database-problem}

Wenn mehrere Services in dieselbe Datenbank schreiben:
- Niemand weiß, welche Tabelle/Spalte zu welchem Service gehört
- Tabellen wachsen nur (niemand traut sich, unbekannte Spalten zu löschen)
- Innerhalb von 5 Jahren wird die Datenbank zur nicht mehr wartbaren Altlast

**Lösung:** Jeder Service besitzt seine Daten. Integration erfolgt über APIs/Events, nicht über gemeinsame Tabellen.

### PostgreSQL-Indizierung {#postgresql-indexing}

- Erzeugt NICHT automatisch zusammengesetzte Indizes
- Die Definition von 3 Feldern erzeugt NICHT alle möglichen Kombinationen
- Daten können zwischen Tabelle und Indizes dupliziert sein (by design)
- Der Query Planner wählt bei JOINs, ORDER BY und GROUP BY automatisch die Indizes aus

## Stolpersteine {#gotchas}

- Keine Metaprogrammierung in TypeScript – meta-lastige Bibliotheken in JS schreiben und mit `.d.ts` typisieren; 100 Zeilen JS ersetzen 500+ Zeilen TypeScript
- Connection Pools sind nötig, weil Node.js mehrere gleichzeitige Benutzer in einem Prozess bedient
- Die `save()`-Methode von Active Record vermischt Persistenz mit Domänenlogik, wodurch unklar wird, wo querschnittliche Belange untergebracht werden sollten

## Siehe auch {#see-also}

- [[application-architecture]] - wie sich die DAL in die Schichtenarchitektur einfügt
- [[dependency-injection]] - Repositories injizieren vs. Modul-Singletons verwenden
- [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) - Template Method, Repository als GoF-Anwendungen
