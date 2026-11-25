---
title: "Injection de dépendances et couplage"
category: concepts
tags: [nodejs, dependency-injection, coupling, modules, layer-isolation, di]
level: 2
source_sha256: 333d88eefe170443e5788bd980aa8bb8e91d0b57fccd22d66364a188d1598228
translation: machine
translated_at: '2026-10-24'
---
# Injection de dépendances et couplage {#dependency-injection-and-coupling}

Il y a couplage dès qu'un module appelle des méthodes d'un autre module, crée des instances de ses entités ou lit/écrit leurs propriétés. En JavaScript, de nombreux patrons d'injection de dépendances traditionnels peuvent être remplacés par le système de modules lui-même. L'isolation des couches, grâce à des interfaces sûres et à une communication unidirectionnelle, empêche le couplage de devenir ingérable.

## Points clés {#key-facts}

- **Couplage** : il y a couplage lorsqu'un module appelle une méthode d'un autre, crée une instance d'un autre, ou lit/écrit les propriétés d'un autre
- Le cache de modules JavaScript garantit une seule instance par `require()`/`import` : c'est un singleton intégré
- Chaque dépendance (import, require, appel d'API) augmente le couplage : il faut les réduire au minimum
- Règle empirique : ne pas faire de métaprogrammation en TypeScript ; écrire les bibliothèques très orientées métaprogrammation en JS et fournir des déclarations `.d.ts`

## Le système de modules comme DI {#module-system-as-di}

| DI traditionnelle | Équivalent avec les modules JS |
|-------------------|--------------------------------|
| Conteneur singleton | Cache de modules (`require()` renvoie la même instance) |
| Injection de stratégie | Objets ou Maps exportés par les modules |
| Injection de configuration | Exporter un objet de configuration, l'importer là où il est nécessaire |
| Injection de fabrique | Exporter des fonctions de fabrique |
| Injection par constructeur | Passer des références de modules en paramètres du constructeur |

## Patrons {#patterns}

### Isolation des couches {#layer-isolation}

Les couches doivent interagir à travers des interfaces sûres (contrats) :
- **Unidirectionnelle :** la couche A appelle la couche B, mais pas l'inverse
- **Bidirectionnelle :** les deux couches s'appellent mutuellement (utiliser des événements ou des callbacks pour éviter les dépendances circulaires)

Patrons structurels pour l'isolation : [Patrons de conception (GoF) en JavaScript](design-patterns-gof.md) (adapter les interfaces), Proxy (contrôler l'accès), Facade (simplifier un sous-système), Composite (parcours uniforme d'une arborescence).

### Abstraction de la plateforme {#platform-abstraction}

Abstraire les API spécifiques à la plateforme afin que les implémentations soient interchangeables :

```js
// Storage abstraction - works on server and browser
const createStorage = (backend) => ({
  async read(key) { return backend.get(key); },
  async write(key, value) { return backend.set(key, value); },
});

// Server: filesystem or S3
const serverStorage = createStorage(new S3Backend(config));
// Browser: OPFS, IndexedDB, or Cache API
const browserStorage = createStorage(new OPFSBackend());
```

À abstraire : protocoles réseau (HTTP, WebSocket, gRPC), bases de données (PostgreSQL, MongoDB), fournisseurs de cryptographie, stockage de fichiers (local, S3, OPFS, IndexedDB), services de notification.

### Développement piloté par les schémas {#schema-driven-development}

Définir les schémas en premier, puis tout générer à partir d'eux :
- Tables de base de données
- Validateurs d'API
- Types TypeScript
- Documentation
- SDK clients

Les schémas, source unique de vérité, empêchent la divergence entre les couches.

## Pièges {#gotchas}

- Les singletons issus du cache de modules signifient que les mutations d'objets exportés sont visibles partout : cela peut être une fonctionnalité ou un bogue
- Les dépendances circulaires fonctionnent en CJS (le module partiellement chargé est renvoyé), mais provoquent des problèmes d'initialisation subtils
- Sur-ingénierie de la DI en JavaScript : cela mène à un code standard à la Java sans en avoir les bénéfices. Il faut d'abord utiliser les modules, et ne recourir aux conteneurs DI que lorsque le système de modules ne suffit plus

## Voir aussi {#see-also}

- [[modules-and-packages]] - CommonJS vs ESM, comportement du cache de modules
- [[application-architecture]] - comment la DI s'intègre à une architecture serveur en couches
- [[solid-and-grasp]] - Principe d'inversion de dépendances
- [[data-access-patterns]] - injection des repositories
