---
title: "Types de graphiques Tableau et choix de visualisation"
category: tools
tags: [bi-analytics, tableau, chart-types, visualization, encoding, anscombes-quartet]
level: 3
source_sha256: e82f1bf28306a74fa9e1a12e437e32c5b8d7920f71d472bcfcf2a69c99c837d8
translation: machine
translated_at: '2026-10-24'
---
# Types de graphiques Tableau et choix de visualisation {#tableau-chart-types-visualization-selection}

Choisir le bon type de graphique est une compétence essentielle en BI. Chaque visualisation encode les attributs des données de manière différente, et le choix doit être guidé par la question précise à laquelle on cherche à répondre. Le quartet d'Anscombe l'illustre : quatre jeux de données aux statistiques identiques produisent des formes visuelles totalement différentes.

## Points clés {#key-facts}

- Visualisation = ensemble de méthodes d'encodage associées aux données
- Pour la précision (valeurs exactes) : utiliser la **longueur** et la **position sur les axes**
- Pour la séparation (regroupement) : utiliser la **couleur**, le **volume**, la **taille**
- Règle : comprendre la question que pose l'utilisateur, puis choisir le graphique qui y répond
- Visualisations maison = analyse interne (Jupyter, matplotlib) ; visualisations préfabriquées = communication aux utilisateurs (tableaux de bord, présentations)

## Schémas {#patterns}

### Attributs d'encodage des données {#data-encoding-attributes}

Principaux attributs d'encodage classés par précision :
1. **Position sur une échelle commune** (la plus précise)
2. **Longueur**
3. **Angle/pente**
4. **Surface**
5. **Intensité de couleur**
6. **Teinte** (la moins précise pour les données quantitatives)

### Guide de sélection des types de graphiques {#chart-type-selection-guide}

| Graphique | Usage recommandé | Remarques |
|-----------|------------------|-----------|
| **Barres/Colonnes** | Comparaisons entre catégories | Barres horizontales pour les libellés longs |
| **Courbe** | Tendances dans le temps | Relier uniquement des données continues |
| **Secteurs/Anneau** | Partie d'un tout | À utiliser avec parcimonie, 5 segments maximum |
| **Matrice/Tableau croisé** | Tableaux croisés | Lorsque les chiffres précis comptent |
| **Carte (Card)** | Indicateur KPI unique | Faits marquants en en-tête de tableau de bord |
| **Tableau** | Données tabulaires brutes | Exploration détaillée (drill-down) |
| **Treemap** | Partie d'un tout hiérarchique avec taille | Préférable aux secteurs pour de nombreuses catégories |
| **Carte géographique/Carte remplie** | Données géographiques | Vérifier l'interpolation des couleurs |
| **Jauge** | Progression vers un objectif | Suivi d'une cible sur une seule métrique |
| **Nuage de points** | Corrélation entre deux mesures | Ajouter une courbe de tendance pour plus de clarté |
| **Carte de chaleur (Heatmap)** | Densité de motifs selon deux dimensions | Échelle de couleurs séquentielle |

### Catégories de visualisations {#visualization-categories}

**Maison (pour l'analyse interne) :**
- Analytique métier : exploration rapide des données (Jupyter + matplotlib/seaborn)
- Visualisation scientifique : phénomènes physiques, 3D
- Visualisation de recherche/de concepts : relations et principes

**Préfabriquées (pour communiquer aux utilisateurs) :**
- Tableaux de bord et présentations : panneaux interactifs de performance métier
- Cartes d'entité / comptes personnels : vues de type bancaire (factoids KPI + sparklines)
- Outils d'analyse de données : l'utilisateur explore lui-même les données grâce à l'interactivité
- Infographies et journalisme : attractives, à forte dimension graphique

### Sparklines et factoids KPI {#sparklines-and-kpi-factoids}

- **Factoid KPI** : nombre unique accompagné d'un libellé, indiquant l'état actuel (par exemple « Ventes 5,7 M$ »)
- **Sparkline** : mini-graphique intégré, sans axes, qui montre la tendance et se place à côté du factoid
- Les deux éléments sont placés dans la zone supérieure gauche pour maximiser l'attention et permettre une évaluation rapide de l'état

### Actions de tableau de bord (interactivité) {#dashboard-actions-interactivity}

| Action | Description |
|--------|-------------|
| **Filtre** | Clic sur un élément -> filtre les autres graphiques (le plus courant) |
| **Surlignage** | Clic -> met en évidence les données liées sans les filtrer |
| **Paramètre** | Action de l'utilisateur -> modifie la valeur d'un paramètre |
| **Ensemble** | Action de l'utilisateur -> ajoute ou retire un élément d'un ensemble |
| **GoToSheet** | Navigation vers une autre feuille de calcul ou un autre tableau de bord |
| **URL** | Ouvre une URL avec des paramètres dynamiques |

Exemple d'action URL :
```text
https://crm.example.com/deal?object=<object_number>
```

## Pièges à éviter {#gotchas}

- Quartet d'Anscombe : toujours visualiser les données avant de se fier aux statistiques descriptives ; quatre jeux de données partageant la même moyenne, la même variance, la même corrélation et la même droite de régression peuvent avoir un aspect totalement différent
- Les graphiques en secteurs de plus de 5 segments deviennent illisibles : utiliser plutôt un graphique à barres ou un treemap
- Les grands objets colorés attirent l'attention quelle que soit leur position (le contraste l'emporte sur la lecture en F)
- Une interpolation de couleurs incorrecte dans les cartes de chaleur et les cartes géographiques rend les graphiques trompeurs : toujours la vérifier
- Chaque feuille de calcul génère une requête vers la source : plus de graphiques = plus de requêtes = tableau de bord plus lent

## Voir aussi {#see-also}

- [[dashboard-design-patterns]] - mise en page, lecture en F, principes de Gestalt
- [[color-theory-visualization]] - échelles de couleurs et accessibilité
- [[tableau-calculations]] - champs calculés pour les données des graphiques
- [[powerbi-fundamentals]] - types de visualisations Power BI
