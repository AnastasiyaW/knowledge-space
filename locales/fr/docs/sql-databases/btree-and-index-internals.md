---
title: "Structure interne des B-Tree et des index"
category: concepts
tags: [sql-databases, btree, b-plus-tree, index, page-split, uuid, clustered-index, bloom-filter]
level: 4
source_sha256: ee9ffe01fa8a2ac979a8d55764686a31b5232f4b8eab8ab3bbdd5558d6759f20
translation: machine
translated_at: '2026-10-24'
---
# Structure interne des B-Tree et des index {#b-tree-and-index-internals}

Les B+Trees constituent la base de l'indexation dans tous les SGBDR majeurs. Comprendre leur structure explique pourquoi certaines requêtes sont rapides et d'autres non, et pourquoi le choix de la clé primaire est si déterminant.

## B-Tree vs B+Tree {#b-tree-vs-btree}

**B-Tree :** Les nœuds internes stockent à la fois les clés ET les valeurs (pointeurs vers les données). Les données peuvent être trouvées à n'importe quel niveau.

**B+Tree (utilisé par tous les SGBDR majeurs) :** Seuls les nœuds feuilles stockent les valeurs. Les nœuds internes ne contiennent que des clés pour la navigation. Les nœuds feuilles sont chaînés dans une liste doublement chaînée.

**Avantages des B+Trees :**
- Plus de clés par nœud interne (sans données) = arbre moins profond = moins d'E/S
- Requêtes par intervalle : parcours de la liste chaînée des feuilles (E/S séquentielles)
- Coût d'E/S prévisible : toutes les données sont à la même profondeur
- Meilleure utilisation du cache : les petits nœuds internes sont plus susceptibles d'être en cache

**Quantification :** une page de 8 Ko avec des clés de 100 octets donne environ 80 clés par nœud interne. Un B+Tree à 3 niveaux permet d'atteindre 80^3 = 512 000 pages feuilles en 3 E/S.

## Index clusterisés vs non clusterisés {#clustered-vs-non-clustered-indexes}

**MySQL InnoDB :** La clé primaire EST l'index clusterisé. Les données sont physiquement triées selon la PK. Les index secondaires stockent la valeur de la PK comme localisateur de ligne, ce qui impose un double parcours (index secondaire -> recherche de la PK -> index clusterisé -> ligne).

**PostgreSQL :** Pas d'index clusterisé par défaut. Tous les index pointent directement vers le `ctid` (page, décalage) dans le heap. Tout déplacement de tuple (UPDATE, VACUUM) invalide le ctid et impose une mise à jour de l'index.

**SQL Server :** Un seul index clusterisé par table (la PK par défaut). La feuille d'un index non clusterisé contient le RID pour les heaps, ou la clé clusterisée pour les tables clusterisées.

## Page splits {#page-splits}

Lors de l'insertion dans une page feuille pleine, un page split se produit : la page est divisée, les entrées sont redistribuées et les nœuds parents sont mis à jour. C'est l'opération d'index la plus coûteuse.

**Insertions séquentielles** (auto-incrément, UUID v7/ULID) : elles arrivent toujours dans la feuille la plus à droite. Peu de splits, E/S séquentielles, excellent taux de succès du cache.

**Insertions aléatoires** (UUID v4) : chaque insertion vise une page feuille aléatoire. Splits fréquents, E/S aléatoires, saturation (thrashing) du buffer pool.

## UUID v4 vs identifiants ordonnés {#uuid-v4-vs-ordered-ids}

Les UUID aléatoires entraînent :
- des page splits fréquents (les entrées se rajoutent rarement en fin d'index)
- des patterns d'E/S aléatoires (pages dispersées sur tout le disque)
- une saturation du buffer pool (pages évincées puis à nouveau nécessaires)
- une mauvaise utilisation du cache

**Étude de cas Shopify :** passage de l'UUID v4 à l'ULID. Les requêtes liées aux achats étant naturellement ordonnées dans le temps, les lectures comme les écritures se sont améliorées.

**Mise en garde MySQL :** TOUS les index secondaires stockent la PK. Une PK UUID aléatoire répand l'aléatoire sur chacun des index secondaires.

**Quand le caractère aléatoire ne pose pas de problème :** les tables heap de PostgreSQL sans index clusterisé, où les valeurs aléatoires se rajoutent simplement en fin de heap. Le problème se situe dans la maintenance des index.

## Filtres de Bloom {#bloom-filters}

Structure de données probabiliste : « peut-être présent » ou « certainement absent ». Aucun faux négatif, faux positifs possibles.

```php
Hash(value) % array_size = bit position
Bit = 0 -> definitely absent
Bit = 1 -> might exist (could be collision)
```

Cas d'usage : vérifier la disponibilité d'un nom d'utilisateur sans requête en base. Les faux positifs entraînent des recherches inutiles, mais n'affectent pas l'exactitude des résultats. Plusieurs fonctions de hachage réduisent le taux de faux positifs.

## Points clés {#key-facts}

- Facteur de branchement d'un B+Tree : taille de page 8 Ko / taille de clé = nombre de clés par nœud. Plus le facteur de branchement est élevé, moins l'arbre est profond
- PostgreSQL 13+ a ajouté la déduplication des index B-tree (plusieurs clés dupliquées dans une même feuille)
- Un fill factor < 100 % réserve de l'espace pour les insertions futures, ce qui réduit les splits
- `REINDEX CONCURRENTLY` reconstruit l'index sans bloquer les écritures
- La fragmentation des index causée par les page splits dégrade les performances : REBUILD ou REORGANIZE pour la corriger

## Pièges {#gotchas}

- Petites tables (< 1 page) : un parcours d'index est plus lent qu'un parcours séquentiel (surcoût de l'optimiseur)
- Les fonctions appliquées aux colonnes indexées empêchent l'utilisation de l'index : `WHERE YEAR(col) = 2024` ne peut pas utiliser l'index sur `col`
- UUID v4 comme PK InnoDB : pire cas pour l'index clusterisé comme pour tous les index secondaires
- Chemin rapide des verrous faibles de PostgreSQL : 16 emplacements par backend, les tables fortement partitionnées peuvent dépasser cette limite

## Voir aussi {#see-also}

- [[index-strategies]] - index composites, couvrants, partiels
- [[database-storage-internals]] - pages, heaps, E/S
- [[schema-design-normalization]] - choix de la stratégie de clé primaire
- [[query-optimization-explain]] - comment l'optimiseur choisit entre les types d'index
