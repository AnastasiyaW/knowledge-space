---
title: "Modélisation des données et normalisation"
category: concepts
tags: [data-engineering, data-modeling, normalization, er-diagrams, database-design]
level: 3
source_sha256: 55bdbef0054455a51335da394b93e9fc7fe2cfec73ee5d7a9c2fbf0980e89ec5
translation: machine
translated_at: '2026-10-24'
---
# Modélisation des données et normalisation {#data-modeling-and-normalization}

La modélisation des données est le processus consistant à analyser les besoins et à créer des structures de données. Trois niveaux : conceptuel (entités métier), logique (diagrammes ER avec attributs et clés), physique (scripts DDL avec index et partitions). La normalisation élimine la redondance grâce aux dépendances fonctionnelles.

## Formes normales {#normal-forms}

**Mnémotechnique :** « Les données dépendent de la clé [1NF], de la clé entière [2NF] et de rien d'autre que la clé [3NF]. »

### Première forme normale (1NF) {#first-normal-form-1nf}
- Toutes les valeurs sont **atomiques** (pas de tableaux, pas de valeurs composites)
- Pas de lignes en double
- Possède une clé primaire

### Deuxième forme normale (2NF) {#second-normal-form-2nf}
- Respecte la 1NF
- Chaque attribut non clé dépend de la **totalité** de la clé primaire
- Ne concerne que les clés composites : si la PK est simple, la 2NF est automatiquement satisfaite

### Troisième forme normale (3NF) {#third-normal-form-3nf}
- Respecte la 2NF
- Aucune **dépendance transitive** : un attribut non clé A dépend d'un attribut non clé B, lui-même dépendant de la PK
- **Correction :** extraire le groupe transitivement dépendant dans une table séparée

### Au-delà de la 3NF {#beyond-3nf}
- **BCNF, 4NF, 5NF** : rarement nécessaires en pratique
- **6NF** : décomposition extrême, un attribut par table. Utilisée dans la [[data-vault#anchor-modeling|modélisation par ancres]]

## Dépendances fonctionnelles {#functional-dependencies}

`{X} -> {Y}` signifie : si deux tuples ont la même valeur pour X, ils doivent avoir la même valeur pour Y. Chaque valeur de X détermine exactement une valeur de Y.

### Anomalies (lorsque la normalisation ne suffit pas) {#anomalies-when-normalization-is-insufficient}

| Anomalie | Problème |
|----------|----------|
| **Mise à jour** | Modifier une information impose de mettre à jour TOUTES les lignes contenant cette entité |
| **Suppression** | Supprimer la dernière ligne liée fait perdre entièrement les données de l'entité |
| **Insertion** | Impossible d'insérer une entité qui n'a pas encore d'enregistrements liés |

## Clés {#keys}

| Type de clé | Définition |
|-------------|------------|
| **Clé candidate** | Sous-ensemble d'attributs unique et irréductible |
| **Clé primaire** | Clé candidate retenue |
| **Clé alternative** | Clés candidates non retenues |
| **Clé de substitution** | Identifiant généré par le système (auto-incrément, UUID) |
| **Clé naturelle** | Attribut métier (courriel, numéro de sécurité sociale) |
| **Clé composite** | Plusieurs attributs formant une clé candidate |

**Privilégier les clés de substitution** lorsque plusieurs candidates existent ou que la clé naturelle est susceptible de changer.

## Diagrammes ER {#er-diagrams}

### Types de cardinalité {#cardinality-types}

| Type | Implémentation |
|------|----------------|
| **1:1** | FK avec contrainte UNIQUE |
| **1:N** | FK dans la table « plusieurs » |
| **M:N** | Table de jonction avec des FK vers les deux tables |

### Notations {#notations}

**Martin (patte de corbeau, *Crow's Foot*)** : la plus pratique, attendue en entretien :
- Rectangles = entités, avec leurs attributs listés à l'intérieur
- Patte de corbeau (fourche) = « plusieurs », trait simple = « un »
- Cercle = « zéro » (optionnel), tiret = « un » (obligatoire)

**Notation de Chen** : académique. Rectangles (entités), losanges (relations), ovales (attributs)

## Normalisation et dénormalisation {#normalization-vs-denormalization}

| Critère | Normalisé (3NF) | Dénormalisé |
|---------|-----------------|-------------|
| Intégrité des données | Meilleure (pas d'anomalies) | Moins bonne |
| INSERT/UPDATE/DELETE | Plus rapide (tables plus petites) | Plus lent |
| SELECT (lectures) | Plus lent (nombreuses jointures) | Plus rapide (tables larges) |
| Usage privilégié | OLTP (intégrité en écriture) | OLAP (vitesse de lecture, data marts) |

## Schémas de déduplication {#deduplication-patterns}

```sql
-- Method 1: CTE + ROW_NUMBER (most common)
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY key_col1, key_col2
        ORDER BY load_date DESC
    ) AS rn
    FROM source_table
)
SELECT * FROM ranked WHERE rn = 1;

-- Method 2: QUALIFY (Snowflake, BigQuery, DuckDB)
SELECT * FROM source_table
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY key_col1, key_col2
    ORDER BY load_date DESC
) = 1;

-- Method 3: DISTINCT ON (PostgreSQL only)
SELECT DISTINCT ON (key_col1, key_col2) *
FROM source_table
ORDER BY key_col1, key_col2, load_date DESC;
```

## Pièges à éviter {#gotchas}
- Les relations (au sens mathématique) ne contiennent ni tuples en double ni ordre. Les tables (physiques) peuvent enfreindre ces deux principes
- Une relation est automatiquement en 1NF par définition (théorie des ensembles). Les tables nécessitent une vérification explicite
- Dans un DWH, les contraintes (PK, FK) sont souvent désactivées pour accélérer les chargements en masse
- La plupart des DWH en production sont hybrides : Data Vault ou 3NF au cœur, modélisation dimensionnelle dans les data marts

## Voir aussi {#see-also}
- [[dimensional-modeling]] - schémas en étoile et en flocon
- [[data-vault]] - méthodologie Hub/Link/Satellite
- [[dwh-architecture]] - où les modèles sont appliqués
- [[sql-for-de]] - implémentation SQL des modèles
