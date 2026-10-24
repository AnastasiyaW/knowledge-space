---
title: "Expressions LOD dans Tableau"
category: tools
tags: [bi-analytics, tableau, lod, fixed, include, exclude, level-of-detail]
level: 3
source_sha256: 6519159ce39d66df75b9560b6a0f8efa685339c5488cc81b627068c9fc40dfc4
translation: machine
translated_at: '2026-10-24'
---
# Expressions LOD dans Tableau {#tableau-lod-expressions}

Les expressions Level of Detail (LOD) calculent des agrégations à un niveau de granularité différent de celui affiché dans la vue courante. Elles créent des sous-requêtes indépendantes du contexte de la vue, ce qui permet d'effectuer des analyses multi-granularités sans contournements complexes.

## Points clés {#key-facts}

- Trois types de LOD : FIXED, INCLUDE, EXCLUDE
- Une LOD crée des sous-requêtes indépendantes de la vue courante
- FIXED ignore totalement la vue ; INCLUDE ajoute de la granularité ; EXCLUDE retire de la granularité
- Une LOD FIXED est évaluée au niveau des filtres de contexte (étape 4 de l'ordre des filtres)
- Une LOD INCLUDE/EXCLUDE est évaluée au niveau des filtres de dimension (étape 5)
- Une LOD imbriquée dans des calculs complexes entraîne des problèmes de performance (JOIN supplémentaires)

## Modèles {#patterns}

### LOD FIXED {#fixed-lod}

Calcule au niveau de la ou des dimensions spécifiées, en ignorant complètement la vue :

```sql
{FIXED [Customer ID] : SUM([Sales])}
-- Total sales per customer, regardless of view

{FIXED [Region], [Year] : AVG([Revenue])}
-- Average revenue per region per year

{FIXED [User ID] : MIN([Event Date])}
-- First event date per user (for cohort analysis)
```

Cas d'usage : analyse de cohortes, valeur vie client (LTV), recherche de la date du premier/dernier achat, totaux par entité affichés dans n'importe quel contexte de vue.

### LOD INCLUDE {#include-lod}

Calcule à une granularité plus fine que la vue (ajoute des dimensions) :

```sql
{INCLUDE [Order ID] : SUM([Quantity])}
-- Per-order sum while viewing by month
```

La vue peut afficher des agrégats mensuels, mais INCLUDE calcule d'abord au niveau de la commande, puis agrège vers le haut.

**Note de performance** : INCLUDE ajoute 2 JOIN lorsqu'il est utilisé dans un calcul complexe.

### LOD EXCLUDE {#exclude-lod}

Calcule à une granularité plus grossière (retire des dimensions du contexte) :

```sql
{EXCLUDE [Region] : SUM([Sales])}
-- Total ignoring region, while view shows by region
```

Cas d'usage : afficher le pourcentage du total général tout en ventilant par sous-catégorie.

### Modèle classique : pourcentage du total {#classic-pattern-percent-of-total}

```sql
SUM([Sales]) / {FIXED : SUM([Sales])} * 100
```

L'expression `{FIXED : SUM([Sales])}` sans dimension calcule le total général, indépendamment de toute dimension présente dans la vue.

### LOD dans l'ordre des filtres {#lod-in-filter-order}

Pour comprendre où se situe la LOD dans l'ordre d'exécution des filtres :

1. Filtres d'extraction
2. Filtres de la source de données
3. Filtres de contexte
4. **LOD FIXED** évaluée ici (avec les filtres de dimension)
5. **LOD INCLUDE/EXCLUDE** évaluée ici (avec les filtres de mesure)
6. Filtres de calcul de tableau

Cela signifie qu'une LOD FIXED est affectée par les filtres de contexte mais PAS par les filtres de dimension, tandis qu'une LOD INCLUDE/EXCLUDE est affectée par les deux.

### Analyse de cohortes avec LOD {#cohort-analysis-with-lod}

```sql
-- Cohort month (first activity)
{FIXED [User ID] : MIN(DATETRUNC('month', [Event Date]))}

-- Period since first activity
DATEDIFF('month',
    {FIXED [User ID] : MIN([Event Date])},
    [Event Date])
```

### LOD imbriquée {#nested-lod}

Une LOD à l'intérieur d'une autre LOD est possible, mais à utiliser avec précaution en raison de l'impact sur les performances. Chaque niveau d'imbrication ajoute des JOIN à la requête générée.

## Pièges à éviter {#gotchas}

- Éviter les LOD dans des calculs imbriqués complexes : chaque LOD ajoute des JOIN :
```bash
  -- Slow (3+ JOINs):
  SUM({FIXED DATEPART('year', [Order Date]) : SUM([Sales])})

  -- Better: pre-aggregate in data source or use table calculation
  ```
- Une LOD FIXED n'est pas affectée par les filtres de dimension de la vue : cela peut prêter à confusion lorsqu'un filtre semble ne pas fonctionner sur un calcul FIXED
- Les filtres de contexte affectent bien les LOD FIXED : promouvez un filtre en filtre de contexte si vous voulez que la LOD FIXED en tienne compte
- INCLUDE/EXCLUDE sont plus intuitives mais plus lentes que FIXED dans la plupart des cas
- Lorsque c'est possible, matérialisez les champs calculés dans l'extraction avant publication plutôt que de calculer la LOD au moment de la requête

## Voir aussi {#see-also}

- [[tableau-calculations]] - calculs au niveau ligne, agrégés et calculs de tableau
- [[tableau-fundamentals]] - ordre des opérations de filtrage, connexions aux données
- [[tableau-performance-optimization]] - optimisation des performances des LOD
- [[cohort-retention-analysis]] - modèles d'analyse de cohortes utilisant les LOD
