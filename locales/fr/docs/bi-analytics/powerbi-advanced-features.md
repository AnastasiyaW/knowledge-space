---
title: "Fonctionnalités avancées de Power BI"
category: tools
tags: [bi-analytics, power-bi, dax, bookmarks, drill-through, what-if, custom-visuals]
level: 4
source_sha256: bad9228921d5c64b5a152a7d81ba5bdad861912fa71052818112bbde75eee413
translation: machine
translated_at: '2026-10-24'
---
# Fonctionnalités avancées de Power BI {#power-bi-advanced-features}

Fonctionnalités avancées de Power BI, notamment les thèmes personnalisés, les visuels provenant d'AppSource, les paramètres What-If pour l'analyse de scénarios, la navigation par analyse détaillée (drill-through), les signets pour la mise en récit, et les modèles DAX avancés.

## Points clés {#key-facts}

- Thèmes personnalisés via des fichiers JSON pour le respect de la charte graphique et l'accessibilité
- Visuels personnalisés provenant de la place de marché AppSource (format `.pbiviz`)
- Les paramètres What-If créent une analyse de scénarios pilotée par des segments (slicers)
- L'analyse détaillée (drill-through) permet de passer d'une vue synthétique à une vue détaillée via le clic droit
- Les signets capturent l'état du rapport (filtres, page, visibilité) pour la navigation et la mise en récit
- Performance Analyzer identifie les visuels lents

## Modèles {#patterns}

### Thèmes personnalisés {#custom-themes}

```json
{
  "name": "MyTheme",
  "dataColors": ["#118DFF", "#12239E", "..."],
  "background": "#FFFFFF",
  "foreground": "#252423",
  "tableAccent": "#118DFF"
}
```

Application : Affichage -> Thèmes -> Parcourir les thèmes (fichier JSON) ou sélectionner dans la galerie. Des générateurs de thèmes sont disponibles sous forme d'outils web.

### Paramètres What-If {#what-if-parameters}

Création : Modélisation -> Nouveau paramètre -> définir le nom, le type de données, le minimum, le maximum, l'incrément et la valeur par défaut.

Création automatique : une nouvelle table à colonne unique contenant la plage de valeurs, un segment et une mesure pour la valeur sélectionnée.

```dax
-- Auto-created
Discount Rate = SELECTEDVALUE('Discount'[Discount], 0)

-- User-created measure using the parameter
Revenue After Discount = [Total Revenue] * (1 - [Discount Rate])
```

**Modèle de sélecteur de mesure** (choisir la mesure à afficher via un segment) :
```dax
Selected Metric =
SWITCH(
    SELECTEDVALUE('Metric Selector'[Metric]),
    "Revenue", [Total Revenue],
    "Profit", [Total Profit],
    "Orders", [Order Count]
)
```

### Analyse détaillée (drill-through) {#drill-through}

Configuration :
1. Créer la page de détail
2. Glisser le champ de dimension dans la section « Analyse détaillée » du volet Filtres
3. Sur les pages de synthèse : clic droit sur le point de données -> Analyse détaillée -> [nom de la page]

Le filtre est transmis automatiquement. Un bouton « Retour » apparaît sur la page de détail.

Cas d'usage : totaux par région -> clic sur une région -> affichage de toutes les transactions de cette région.

### Signets {#bookmarks}

Capturent : la page courante, les filtres, les valeurs des segments, la visibilité des visuels.

Création : Affichage -> volet Signets -> Ajouter un signet.

Modèles courants :
- **Mise en récit** : une séquence de signets formant un récit guidé
- **Navigation personnalisée** : des boutons avec l'action « Signet » remplacent les onglets de page par défaut
- **Navigation conditionnelle** : un bouton affiche une page différente selon la valeur d'un segment
- **Bascule de type de visuel** : afficher un graphique OU un tableau des mêmes données via un signet et la visibilité de la sélection
- **Info-bulles enrichies** : créer des info-bulles au survol à l'aide d'images SVG

Actions de bouton : Signet, Navigation vers une page, Q&R, Analyse détaillée, URL web.

### DAX avancé {#advanced-dax}

**Fonction FORMAT** :
```dax
Sales Label = FORMAT([Total Sales], "$#,##0.00")
Month Name = FORMAT(Date[Date], "MMMM YYYY")
```

**Mise en forme conditionnelle via DAX** :
```dax
KPI Color = IF([Actual] >= [Target], "#28A745", "#DC3545")
```

Application : Visualisations -> champ Valeur -> Mise en forme conditionnelle -> Valeur du champ.

**Tables calculées** :
```dax
Date Table = CALENDAR(DATE(2020,1,1), DATE(2025,12,31))
Top 10 Customers = TOPN(10, Customers, [Total Revenue], DESC)
```

### Optimisation des performances {#performance-optimization}

Utiliser Performance Analyzer : Affichage -> Performance Analyzer.

Techniques d'optimisation :
- Privilégier le mode Import plutôt que DirectQuery pour les gros agrégats
- Réduire la cardinalité des colonnes (supprimer les colonnes inutilisées)
- Pré-agréger dans Power Query avant le chargement
- Utiliser des clés de substitution entières dans les relations plutôt que des clés textuelles
- Éviter les relations bidirectionnelles sauf si nécessaire
- Déplacer les calculs complexes vers Power Query (M) plutôt que vers des mesures DAX

## Pièges courants {#gotchas}

- Les visuels personnalisés d'AppSource peuvent ne pas prendre en charge toutes les options de mise en forme, ou se comporter différemment dans Power BI Service et dans Desktop
- Les paramètres What-If créent de véritables tables dans le modèle : beaucoup de paramètres entraînent un alourdissement du modèle
- Les signets capturent la visibilité des visuels, ce qui peut casser la navigation si vous ajoutez ou supprimez des visuels après leur création
- L'analyse détaillée ne fonctionne que sur les points de données correspondant à la dimension de filtre de l'analyse détaillée
- Les mesures de Performance Analyzer peuvent varier entre Desktop et Service en raison de moteurs de requête différents

## Voir aussi {#see-also}

- [[powerbi-fundamentals]] - Bases de DAX, modèle de données, Power Query
- [[bi-tools-comparison]] - Comparaison des fonctionnalités Power BI et Tableau
- [[dashboard-design-patterns]] - Principes de conception pour la navigation
- [[color-theory-visualization]] - Thèmes et bonnes pratiques en matière de couleurs
