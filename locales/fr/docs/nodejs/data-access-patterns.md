---
title: "Patrons d'accès aux données"
category: patterns
tags: [nodejs, repository, active-record, cursor, transaction, dal, orm]
level: 3
source_sha256: d060aced476d97051e3d32693217a65c422377dba0020d14df94da8897fdaa50
translation: machine
translated_at: '2026-10-24'
---
# Patrons d'accès aux données {#data-access-patterns}

La couche d'accès aux données (DAL) sépare la logique métier du stockage physique. Elle fournit des opérations CRUD abstraites, la gestion des pools de connexions et des connexions liées à la session. Les applications Node.js bénéficient des patrons Repository, Active Record, Cursor et Transaction, aussi bien pour les données en base que pour les données en mémoire.

## Points clés {#key-facts}

- La logique métier ne doit JAMAIS contenir de requêtes SQL brutes
- La DAL fournit : des fonctions d'API, des schémas et données en cache, des pools de connexions, des connexions liées à la session ou à l'utilisateur
- Différents utilisateurs peuvent avoir des permissions différentes sur la base : les pools de connexions doivent donc supporter des connexions liées à l'utilisateur
- **Repository** est préféré pour les domaines complexes : plusieurs repositories par entité (User pour les RH, la facturation et le contrôle d'accès)
- **Active Record** est plus simple mais mélange les responsabilités : l'objet correspond directement à une ligne de la base, avec `save` et `delete` intégrés
- Mettre en cache dans la couche DAO si le cache dépend de détails d'implémentation (cache par ID) ; le mettre en cache dans la couche service s'il dépend de la logique métier
- Critiques sur les ORM : TypeORM impose du code superflu ; Prisma génère du code non typé en sécurité (retours de type `any`)

## Patrons {#patterns}

### Patron Repository {#repository-pattern}

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

### Transactions en mémoire {#in-memory-transactions}

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

Même les applications en JavaScript pur tirent profit de patrons transactionnels pour les mutations d'état complexes.

### Template Method pour les opérations métier {#template-method-for-business-operations}

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

## Anti-patrons d'intégration avec la base de données {#database-integration-anti-patterns}

### Problème de la base de données partagée {#shared-database-problem}

Lorsque plusieurs services écrivent dans la même base :
- Personne ne sait quelle table ou colonne appartient à quel service
- Les tables ne font que grandir (personne n'ose supprimer des colonnes inconnues)
- Au bout de 5 ans, la base devient un héritage ingérable

**Solution :** chaque service possède ses propres données. L'intégration passe par des API ou des événements, pas par des tables partagées.

### Indexation dans PostgreSQL {#postgresql-indexing}

- Ne crée PAS automatiquement d'index composites
- Définir 3 champs NE crée PAS toutes les combinaisons possibles
- Les données peuvent être dupliquées entre la table et les index (par conception)
- Le planificateur de requêtes choisit automatiquement les index à utiliser pour les JOIN, ORDER BY et GROUP BY

## Pièges courants {#gotchas}

- Évitez la métaprogrammation en TypeScript : écrivez les bibliothèques très méta en JS et typez-les avec des `.d.ts` ; 100 lignes de JS remplacent plus de 500 lignes de TypeScript
- Les pools de connexions sont nécessaires car Node.js sert plusieurs utilisateurs concurrents dans un même processus
- La méthode `save()` d'Active Record mélange persistance et logique métier, ce qui rend peu clair l'endroit où placer les préoccupations transversales

## Voir aussi {#see-also}

- [[application-architecture]] - comment la DAL s'intègre dans une architecture en couches
- [[dependency-injection]] - injecter des repositories ou utiliser des singletons de module
- [Design Patterns (GoF) en JavaScript](design-patterns-gof.md) - Template Method, Repository comme applications des patrons GoF
