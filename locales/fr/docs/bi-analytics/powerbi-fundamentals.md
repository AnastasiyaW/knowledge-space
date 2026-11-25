---
title: "Fondamentaux de Power BI"
category: tools
tags: [bi-analytics, power-bi, dax, power-query, data-model, microsoft]
level: 2
source_sha256: 2b42c6be1f15d2b8242dcf311133a460bc9686c954ef459e87f3dc8759cd79ca
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de Power BI {#power-bi-fundamentals}

Power BI est la plateforme BI de Microsoft (Desktop + Cloud), étroitement intégrée à l'écosystème Microsoft, avec une offre gratuite généreuse et le moteur de calcul DAX. Il excelle dans les organisations qui utilisent déjà Azure, Excel, Teams et SharePoint.

## Points clés {#key-facts}

- Trois vues de l'espace de travail : Report View (canevas), Data View (inspection des tables), Model View (relations)
- Deux modes de connexion : Import (données chargées dans le moteur en mémoire) et DirectQuery (requêtes en direct vers la source)
- Schéma en étoile recommandé : table de faits au centre, tables de dimensions autour
- DAX (Data Analysis Expressions) = langage de formules pour les colonnes calculées et les mesures
- Power Query Editor = outil ETL intégré utilisant le langage M
- Prend en charge plus de 100 sources de données : Excel, CSV, JSON, PDF, SQL Server, PostgreSQL, MySQL, Azure, SharePoint, Web, OData

## Modèles d'utilisation {#patterns}

### Flux de connexion {#connection-workflow}

1. Home -> Get Data -> sélectionner le type de source
2. Saisir les paramètres de connexion / parcourir jusqu'au fichier
3. Navigator : sélectionner les tables/feuilles à charger
4. Transform Data (ouvre Power Query) ou Load directement

**Mode Import** : données chargées dans le fichier `.pbix`, toujours rapide, mais obsolète jusqu'à l'actualisation.
**DirectQuery** : requêtes en direct à chaque interaction, toujours à jour, mais plus lent.

### Transformations Power Query (langage M) {#power-query-m-language-transformations}

| Opération | Équivalent SQL |
|-----------|---------------|
| Modifier le type de données | CAST |
| Supprimer des lignes | WHERE + DELETE |
| Filtrer des lignes | WHERE |
| Fractionner une colonne | SUBSTRING / SPLIT |
| Fusionner des colonnes | CONCAT |
| Ajouter une colonne personnalisée | Colonne calculée |
| Pivoter/Dépivoter | PIVOT / UNPIVOT |
| Fusionner des requêtes | JOIN |
| Ajouter des requêtes | UNION |

Panneau Applied Steps : chaque transformation est enregistrée sous forme d'étape réversible. Le code M sous-jacent est visible dans Advanced Editor.

### Modèle de données : relations {#data-model-relationships}

Propriétés d'une relation :
- **Cardinalité** : One-to-Many (la plus courante), Many-to-Many, One-to-One
- **Direction du filtre croisé** : Single (de 1 vers Many), Both (bidirectionnel)
- **Actif/Inactif** : une seule relation active par paire de tables

Création : glisser un champ d'une table vers le champ correspondant d'une autre table dans Model View.

### Bases de DAX {#dax-basics}

**Colonne calculée** - calculée au chargement des données, stockée par ligne :
```dax
Full Name = Customers[First Name] & " " & Customers[Last Name]
Profit = Sales[Revenue] - Sales[Cost]
```

**Mesure** - calculée au moment de la requête, en fonction du contexte de filtre :
```dax
Total Sales = SUM(Sales[Revenue])
Average Order = AVERAGE(Sales[OrderValue])
Num Customers = DISTINCTCOUNT(Sales[CustomerID])
Sales LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Date[Date]))
YoY Growth % = DIVIDE([Total Sales] - [Sales LY], [Sales LY])
```

### Fonctions DAX essentielles {#key-dax-functions}

| Fonction | Rôle |
|----------|---------|
| `SUM()` | Somme agrégée |
| `AVERAGE()` | Moyenne agrégée |
| `COUNT()` / `COUNTA()` | Compter les lignes / les valeurs non vides |
| `DISTINCTCOUNT()` | Compter les valeurs uniques |
| `CALCULATE()` | Modifier le contexte de filtre |
| `FILTER()` | Renvoyer une table filtrée |
| `ALL()` | Supprimer les filtres d'une colonne ou d'une table |
| `RELATED()` | Obtenir une valeur d'une table liée |
| `DIVIDE(num, den)` | Division sécurisée (BLANK en cas de division par zéro) |
| `IF(cond, true, false)` | Logique conditionnelle |
| `SWITCH()` | Conditions multiples |
| `SAMEPERIODLASTYEAR()` | Intelligence temporelle - même période de l'année précédente |
| `DATEADD()` | Intelligence temporelle - décalage de dates |

**Contexte de filtre** : les mesures respectent automatiquement les segments (slicers), les filtres de page et les filtres de visuel actifs. `CALCULATE` modifie ce contexte.

### Types de filtres (par priorité) {#filter-types-by-precedence}

1. **Niveau visuel** - s'applique à un seul graphique
2. **Niveau page** - s'applique à tous les visuels de la page
3. **Niveau rapport** - s'applique à toutes les pages
4. **Drillthrough** - transmis automatiquement lors de l'exploration détaillée

Le visuel Slicer = widget de filtre interactif. Types : liste, liste déroulante, entre (plage de dates), date relative.

### Visualisations courantes {#common-visualizations}

- Graphique à barres/colonnes - comparaison de catégories
- Graphique en courbes - tendances temporelles
- Secteurs/Anneau - partie d'un tout (5 segments maximum)
- Matrice - tableau croisé
- Carte - indicateur KPI unique
- Table - données brutes
- Treemap - comparaison hiérarchique de tailles
- Carte/Carte remplie - données géographiques
- Jauge - progression vers un objectif

## Pièges {#gotchas}

- DAX est un paradigme puissant mais distinct de SQL : la courbe d'apprentissage est raide
- Les colonnes calculées augmentent la taille du fichier (stockées par ligne) ; privilégier les mesures lorsque c'est possible
- Les relations bidirectionnelles peuvent provoquer une propagation de filtres inattendue : à éviter sauf nécessité
- Les fichiers `.pbix` sont binaires et peu adaptés à git ; utiliser Azure DevOps pour le contrôle de version
- Les fichiers `.pbix` en mode Import peuvent devenir très volumineux avec de grands jeux de données : envisager DirectQuery ou des agrégations

## Voir aussi {#see-also}

- [[powerbi-advanced-features]] - thèmes, signets, exploration détaillée (drill-through), DAX avancé
- [[bi-tools-comparison]] - Power BI vs Tableau vs alternatives
- [[dashboard-design-patterns]] - principes de conception applicables à tous les outils
- [[sql-for-analytics]] - bases SQL pour les utilisateurs de DAX
