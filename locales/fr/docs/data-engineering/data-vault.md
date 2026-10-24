---
title: "Data Vault 2.0"
category: concepts
tags: [data-engineering, data-vault, data-modeling, dwh, scd2]
level: 3
source_sha256: e29b457acb016e4270303529de477eb3cf5d96a9447ee8ef06dbf3d7b78ef0d8
translation: machine
translated_at: '2026-10-24'
---
# Data Vault 2.0 {#data-vault-20}

Data Vault est une méthodologie de modélisation de données conçue pour les environnements DWH agiles, comportant de nombreuses sources, des évolutions fréquentes de schéma et des exigences d'audit. Elle résout la rigidité de la 3NF et les problèmes de duplication propres à la modélisation dimensionnelle.

## Types de tables principaux {#core-table-types}

| Table | Rôle | Champs clés |
|-------|------|-------------|
| **Hub** | Entités métier (client, produit) | Clé de hachage, clé métier, horodatage de chargement, code source |
| **Link** | Relations/transactions entre 2 hubs ou plus | Clé de hachage, clés étrangères vers les hubs, horodatage de chargement, source |
| **Satellite** | Attributs descriptifs avec historique SCD2 | Clé de hachage du hub/link, attributs, valid_from, valid_to, source |

## Principes clés {#key-principles}
- Les données entrent telles quelles depuis les sources (aucune transformation métier dans le cœur)
- Les règles métier ne sont appliquées que dans la couche mart
- Toutes les tables sont **en ajout seul (append-only)** : l'historique est tracé via SCD2 dans les satellites
- **Clés de hachage** pour les jointures (déterministes, sans séquences)
- Sépare la structure (hubs/links) du contenu (satellites)

## Avantages {#advantages}
- Ajout facile de nouvelles sources (il suffit d'ajouter des satellites)
- Auditabilité complète (chaque modification est tracée avec horodatages et codes source)
- Chargement parallélisable (hubs, links et satellites se chargent indépendamment)
- Gère de nombreuses sources aux schémas différents
- Résilient aux évolutions des sources

## Inconvénients {#disadvantages}
- Complexe à interroger directement (nécessite des jointures hub + satellite + link)
- Alimente généralement des marts dimensionnels pour la BI
- Les jointures SCD2 entre satellites aux fréquences de changement différentes ajoutent de la complexité

## SCD2 (Slowly Changing Dimension de type 2) {#scd2-slowly-changing-dimension-type-2}

Suit les changements historiques en ajoutant de nouvelles lignes avec des dates de validité :

```sql
customer_id | name    | valid_from | valid_to   | is_current
1           | Alice   | 2023-01-01 | 2023-06-15 | false
1           | Alice B | 2023-06-15 | 9999-12-31 | true
```

Lorsqu'on joint des satellites provenant de hubs/links différents, les intervalles de dates doivent se chevaucher, ce qui peut provoquer une explosion cartésienne.

## Anchor Modeling {#anchor-modeling}

Forme extrême de Data Vault où chaque attribut possède sa propre table (à la manière de la 6NF) :

| Composant | Équivalent | Description |
|-----------|------------|-------------|
| **Anchor** | Hub | Entité identifiée par un identifiant de substitution |
| **Attribute** | Satellite | Un seul attribut par table, avec horodatage |
| **Tie** | Link | Relation entre anchors |
| **Knot** | Référence | Données de référence partagées (énumérations, tables de correspondance) |

### Différences clés avec Data Vault {#key-differences-from-data-vault}
- Plus granulaire : un attribut = une table (contre des satellites regroupant plusieurs attributs)
- Évolution du schéma facilitée (ajouter un attribut = ajouter une table, sans ALTER)
- Aboutit à un grand nombre de tables et de jointures
- Mieux adapté aux environnements aux schémas fréquemment modifiés

## Choisir une méthodologie {#choosing-a-methodology}

| Méthodologie | Idéale pour | Compromis |
|--------------|-------------|-----------|
| **3NF (Inmon)** | Couche cœur d'un DWH d'entreprise | Complexe à interroger, bonne pour l'intégration |
| **Dimensionnelle (Kimball)** | Marts, BI, requêtes rapides | Dénormalisée, plus difficile à maintenir |
| **Data Vault** | DWH agile, sources multiples, audit | Complexe à interroger, nécessite des marts en aval |
| **Anchor** | Schémas fréquemment modifiés | Très nombreuses tables, nombreuses jointures |

## Pièges à éviter {#gotchas}
- Data Vault ajoute de nombreuses jointures : la couche mart doit pré-joindre les données pour des performances acceptables
- Les jointures sur intervalles de dates SCD2 entre satellites différents peuvent produire des produits cartésiens inattendus
- Les clés de hachage doivent utiliser un hachage cohérent dans tous les processus de chargement
- Sans couche mart adéquate, les analystes ne peuvent pas interroger Data Vault directement

## Voir aussi {#see-also}
- [[data-modeling]] - principes fondamentaux de la normalisation
- [[dimensional-modeling]] - schémas en étoile et en flocon pour les marts
- [[scd-patterns]] - techniques de dimensions à évolution lente
- [[dwh-architecture]] - contexte architectural
