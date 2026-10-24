---
title: "Calculs Tableau"
category: tools
tags: [bi-analytics, tableau, calculated-fields, table-calculations, window-functions, parameters]
level: 3
source_sha256: 27314abcb76deaf17a5ca1a488b8e99e734a9a6e4edf64d191d3296e6822457f
translation: machine
translated_at: '2026-10-24'
---
# Calculs Tableau {#tableau-calculations}

Tableau propose plusieurs types de calculs qui opèrent à différents niveaux de granularité. Comprendre quand utiliser chaque type est essentiel pour construire des tableaux de bord précis et performants.

## Points clés {#key-facts}

- Six types de calculs : niveau ligne, agrégé, calcul de table rapide, calcul de table, calcul de fenêtre, LOD
- Les calculs au niveau ligne s'exécutent ligne par ligne ; les calculs agrégés nécessitent des fonctions d'agrégation
- Les calculs de table opèrent sur les valeurs visibles dans la vue courante
- Les calculs de fenêtre constituent un sous-type des calculs de table, opérant sur une fenêtre de valeurs visibles
- Les calculs de table rapides sont des enveloppes de fonctions de fenêtre appliquées en deux clics
- Les paramètres sont des variables contrôlées par l'utilisateur qui modifient le comportement du tableau de bord

## Modèles {#patterns}

### Vue d'ensemble des types de calculs {#calculation-types-overview}

| Type | Description | Exemple |
|------|-------------|---------|
| **Niveau ligne** | Par ligne (observation) | `[Price] * [Quantity]` |
| **Agrégé** | Utilise une fonction d'agrégation | `SUM([Sales]) / COUNT([Orders])` |
| **Calcul de table rapide** | Calculs de table intégrés (2 clics) | Total cumulé, Pourcentage du total |
| **Calcul de table** | Formule personnalisée sur les valeurs visibles | `INDEX()`, `RANK()`, `LOOKUP()` |
| **Calcul de fenêtre** | Sur une fenêtre de valeurs visibles | `WINDOW_AVG(SUM([Sales]), -2, 0)` |
| **LOD** | À un niveau de granularité spécifié | `{FIXED [Customer] : SUM([Sales])}` |

### Fonctions de date {#date-functions}

```sql
DATEPART('month', [Order Date])    -- extracts integer (3 for March)
DATETRUNC('month', [Order Date])   -- returns first date of period (2023-03-01)
DATEDIFF('day', [Order Date], TODAY())  -- difference between dates
DATENAME('weekday', [Order Date])  -- returns string ("Monday")
```

Remarque : Tableau encapsule DATETRUNC dans DATEBAR par défaut. Choisissez « exact date » dans le menu déroulant du champ pour afficher la date réelle.

### Fonctions de chaîne {#string-functions}

```sql
SPLIT([Product Name], '-', 1)      -- split by delimiter, first part
FIND([String], 'word')             -- position of substring
REPLACE([String], 'old', 'new')    -- replace substring
CONTAINS([String], 'word')         -- true/false
STARTSWITH([Category], 'word')     -- true/false (faster than CONTAINS)
REGEXP_MATCH / REGEXP_EXTRACT / REGEXP_REPLACE  -- regex
```

**Conseil de performance** : `STARTSWITH` est plus rapide que `CONTAINS` lorsque c'est possible.

### Calculs agrégés {#aggregated-calculations}

```sql
SUM([Sales])
AVG([Profit])
MEDIAN([Revenue])
COUNTD([User ID])               -- count distinct
ATTR([Region])                  -- checks if unique; marks * if multiple values
SUM([Revenue] - [Cost]) / SUM([Revenue])  -- margin calculation
```

### Calculs de table {#table-calculations}

**Indexation et classement :**
```sql
INDEX()                -- row number within partition (1, 2, 3...)
FIRST()                -- offset from first row (0 for first)
LAST()                 -- offset from last row (0 for last)
RANK(expression)       -- rank by value
RANK_UNIQUE(), RANK_DENSE(), RANK_PERCENTILE()
```

**Totaux cumulés :**
```sql
RUNNING_SUM(SUM([Sales]))
RUNNING_AVG(SUM([Profit]))
RUNNING_MAX(SUM([Revenue]))
```

**Recherche et référence :**
```sql
LOOKUP(SUM([Sales]), -1)       -- value from 1 row earlier
LOOKUP(SUM([Sales]), FIRST())  -- value from first row in partition
PREVIOUS_VALUE(0)              -- previous value or 0 if none
```

**Partition et adressage** : les paramètres « Compute Using » définissent la dimension à adresser (calcul le long de) et la dimension à partitionner (réinitialisation du calcul).

### Calculs de fenêtre {#window-calculations}

```sql
WINDOW_SUM(SUM([Sales]), -2, 0)    -- rolling 3-period sum
WINDOW_AVG(SUM([Sales]), -2, 0)    -- rolling 3-period average
WINDOW_MAX(SUM([Profit]))           -- max in entire window
WINDOW_MIN(SUM([Profit]))           -- min in entire window
WINDOW_STDEV(SUM([Sales]))         -- std deviation
```

Décalages : `FIRST()` = début, `LAST()` = fin, `0` = ligne courante. Les deuxième et troisième paramètres sont les bornes relatives de début et de fin.

### Calculs de table rapides {#quick-table-calculations}

Appliqués via un clic droit sur la mesure dans l'étagère, puis Calcul de table rapide :

| Fonction | Description |
|----------|-------------|
| Running Total | Somme cumulée |
| Difference | Différence avec la période précédente |
| Percent Difference | `(current - previous) / previous * 100%` |
| Percent of Total | Part dans le total global |
| Moving Average | Moyenne glissante sur N périodes |
| YTD Total | Total cumulé depuis le début de l'année |
| Compound Growth Rate | TCAC |
| Rank | Classement au sein de la partition |

Filtre pour afficher le dernier mois : `LAST() = 0` comme filtre de calcul de table.

### Paramètres {#parameters}

Création : clic droit sur le panneau de données, puis Create Parameter. Types : String, Integer, Float, Boolean, Date.

```ruby
IF [Sales] > [Parameter: Sales Threshold] THEN 'Above' ELSE 'Below' END
```

**Modèle de sélecteur de mesure** : paramètre combiné à IF/CASE pour afficher différentes mesures selon la sélection dans la liste déroulante.

### Fonctions logiques {#logical-functions}

```ruby
// IF
IF [Profit] > 0 THEN 'Profitable'
ELSEIF [Profit] = 0 THEN 'Break Even'
ELSE 'Loss'
END

// CASE (cleaner for multiple fixed values)
CASE [Region]
  WHEN 'North' THEN 'Northern Division'
  WHEN 'South' THEN 'Southern Division'
  ELSE 'Other'
END
```

## Pièges à éviter {#gotchas}

- Le sens d'agrégation compte : configurez si le calcul s'exécute à travers les colonnes ou le long des lignes dans le menu « Compute Using »
- Les calculs de table rapides sont en réalité des fonctions de fenêtre ; elles encapsulent les formules pour éviter de les écrire manuellement
- Mélanger des champs agrégés et non agrégés dans un calcul provoque des erreurs : tous les champs doivent être au même niveau
- Les opérations sur les chaînes de caractères sont les plus lentes ; privilégiez la hiérarchie des types : `String > Date > Numeric > Boolean`
- `DUPLICATE_AS_CROSSTAB` révèle la table de données sous-jacente à une visualisation, utile pour le débogage

## Voir aussi {#see-also}

- [[tableau-lod-expressions]] - FIXED/INCLUDE/EXCLUDE pour les niveaux de granularité croisés
- [[tableau-fundamentals]] - connexions aux données et ordre des filtres
- [[tableau-performance-optimization]] - optimisation des performances de calcul
- [[powerbi-fundamentals]] - équivalent des calculs en DAX
