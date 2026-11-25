---
title: "Théorie des couleurs pour la visualisation de données"
category: concepts
tags: [bi-analytics, color, visualization, accessibility, palette, colorbrewer]
level: 3
source_sha256: 1efdcd80899fa0afa92f67ad75627755778d3d60e25dfc715def7f2c2c85b6fd
translation: machine
translated_at: '2026-10-24'
---
# Théorie des couleurs pour la visualisation de données {#color-theory-for-data-visualization}

La couleur est l'un des attributs d'encodage les plus puissants et les plus fréquemment mal utilisés en visualisation de données. Une utilisation appropriée des échelles de couleurs, la prise en compte de l'accessibilité et une sémantique des couleurs cohérente d'un tableau de bord à l'autre ont un impact significatif sur la lisibilité et la fiabilité perçue.

## Points clés {#key-facts}

- Trois types d'échelles de couleurs : catégorielle, séquentielle, divergente
- Maximum 5 à 7 couleurs par tableau de bord : au-delà, il devient impossible de mémoriser les associations
- Une couleur = une entité sur l'ensemble des graphiques d'un tableau de bord
- Le gris est la couleur de base par défaut ; n'ajouter de la couleur que là où elle aide l'utilisateur
- Choix sûr par défaut en cas de doute : le bleu, le gris et leurs nuances
- Nuances atténuées plutôt que vives : réduire la saturation et la luminosité
- Associations courantes : vert = bon, rouge = mauvais

## Modèles {#patterns}

### Types d'échelles de couleurs {#color-scale-types}

| Type | Cas d'usage | Règles |
|------|-------------|--------|
| **Catégorielle** | Grouper / séparer des catégories | Pas de notion d'ordre ; 5 à 7 couleurs maximum ; poids visuel identique pour toutes |
| **Séquentielle** | Encoder des valeurs numériques | Une couleur de base + dégradé ; clair = faible, foncé = élevé |
| **Divergente** | Montrer les écarts par rapport à 0 ou à la moyenne | Deux couleurs polaires ; dégradé passant par un gris neutre ; rouge-vert pour bon-mauvais, bleu-orange pour les écarts |

### Interpolation des couleurs {#color-interpolation}

L'interpolation consiste à associer des nuances de couleur à des valeurs numériques précises. Une interpolation incorrecte rend les graphiques trompeurs. Vérifiez toujours que les heatmaps et les cartes utilisent une interpolation correcte dans Tableau.

### Palette personnalisée dans Tableau {#custom-palette-in-tableau}

Ajouter dans : `My Tableau Repository/Preferences.tps`

Types de palettes :
- `regular` = palette catégorielle
- `sequential` = dégradé continu
- `diverging` = dégradé à deux pôles

### Ressources pour daltoniens {#color-blind-safe-resources}

- **ColorBrewer** (colorbrewer2.org) : la référence pour les palettes cartographiques et de données
- **DataColorPicker** : génère des palettes à uniformité perceptuelle
- **Coolors** : générateur de palettes avec tests d'accessibilité
- **Paletton** : conception de palettes basée sur la roue chromatique

### Liste de contrôle des couleurs {#color-checklist}

1. Préparer une palette de couleurs avant de commencer
2. Une couleur = une entité, de manière constante sur l'ensemble des graphiques
3. Le double encodage (couleur + taille) est acceptable mais souvent inutile
4. Pour les graphiques à grandes surfaces, utiliser des couleurs pastel (saturation plus faible)
5. Le gris comme couleur de base principale
6. Tester l'accessibilité pour les daltoniens
7. Texte foncé sur fond clair (vérifier le contraste)

### Couleur dans Power BI {#color-in-power-bi}

Les thèmes personnalisés permettent un contrôle complet des couleurs via JSON :
```json
{
  "name": "MyTheme",
  "dataColors": ["#118DFF", "#12239E", "..."],
  "background": "#FFFFFF",
  "foreground": "#252423",
  "tableAccent": "#118DFF"
}
```

Appliquer via : Affichage -> Thèmes -> Parcourir les thèmes.

### Couleur conditionnelle en DAX {#conditional-color-in-dax}

```dax
KPI Color =
IF([Actual] >= [Target], "#28A745", "#DC3545")
```

Appliquer dans : Visualisations -> Champ de valeur -> Mise en forme conditionnelle -> Valeur du champ.

## Pièges à éviter {#gotchas}

- La combinaison rouge-vert est la pire pour les daltoniens (8 % des hommes) : utiliser plutôt bleu-orange ou bleu-rouge
- Les échelles séquentielles aux nuances trop proches deviennent illisibles à l'impression
- Les couleurs vives et saturées provoquent une fatigue visuelle sur les tableaux de bord riches en données
- Une couleur qui « ressort » sur un écran peut paraître délavée lors d'une projection : tester dans l'environnement de présentation
- Utiliser la même couleur pour des entités différentes d'un graphique à l'autre casse le langage visuel du tableau de bord

## Voir aussi {#see-also}

- [[dashboard-design-patterns]] - mise en page et hiérarchie visuelle
- [[tableau-chart-types]] - attributs d'encodage et choix du type de graphique
- [[powerbi-advanced-features]] - thèmes Power BI et mise en forme conditionnelle
