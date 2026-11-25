---
title: "Modèles de conception de tableaux de bord"
category: concepts
tags: [bi-analytics, dashboard, design, ux, layout, gestalt, f-pattern, storytelling]
level: 3
source_sha256: 9ad5648f8b9e75bacd3f2be18295db0aa348688f52cec7a8ab37ba1d12971667
translation: machine
translated_at: '2026-10-24'
---
# Modèles de conception de tableaux de bord {#dashboard-design-patterns}

La conception de tableaux de bord combine design de l'information, design graphique, UX et storytelling. Une bonne conception s'appuie sur des modèles établis concernant le sens de lecture, la hiérarchie visuelle et les principes cognitifs, afin que les utilisateurs puissent rapidement trouver les informations pertinentes et agir en conséquence.

## Points clés {#key-facts}

- Les utilisateurs lisent de gauche à droite et de haut en bas (motif en F pour les publics européens)
- Zone de forte attention : coin supérieur gauche ; zone de faible attention : coin inférieur droit
- Le contraste prime sur le motif en F : les grands objets colorés attirent l'attention quelle que soit leur position
- Les factoids KPI et les sparklines se placent en haut à gauche pour un impact maximal
- Structure du tableau de bord : synthèse -> tendance -> ventilation -> détail (du général au spécifique)
- 5 à 7 couleurs maximum par tableau de bord ; codage couleur cohérent entre les graphiques
- Chaque graphique doit répondre à une seule question de l'utilisateur

## Modèles {#patterns}

### Structure du tableau de bord (du général au spécifique) {#dashboard-structure-general-to-specific}

```text
Level 1: KPI summary (total state, one number per metric)
Level 2: Trend over time (is it improving or declining?)
Level 3: Breakdown by dimension (which segment drives the trend?)
Level 4: Detail/drill-down (individual records, anomalies)
```

Disposition visuelle :
```text
Header (title)
+-- KPI factoids + sparklines (upper area, high attention)
+-- Trend charts (middle area)
+-- Detail table (lower area)
```

### Disposition modulaire {#modular-layout}

Divisez le tableau de bord en blocs rectangulaires invisibles (comme les colonnes d'un journal) :
- Utilisez des conteneurs Tiled (un seul Tiled externe, puis vertical/horizontal à l'intérieur)
- Pas d'éléments flottants (ils cassent le dimensionnement adaptatif)

Modes de dimensionnement du tableau de bord :
- **Fixe** : conserve la taille exacte spécifiée
- **Plage** : plage min/max de largeur/hauteur (recommandé)
- **Automatique** : s'adapte à l'écran, mais les éléments peuvent se déplacer

Règle : planifiez d'abord la structure, puis créez les conteneurs. Vertical à l'extérieur, horizontaux à l'intérieur, puis verticaux dans les horizontaux.

### Principes UX {#ux-principles}

**Loi de Fitts** : les éléments nécessitant des interactions fréquentes doivent être plus grands et plus proches du centre.

**Loi de Hick** : plus il y a de choix, plus la décision prend du temps. Réduisez autant que possible le nombre d'options de filtre.

Placement des filtres : à proximité des graphiques qu'ils contrôlent. UX = habitudes des utilisateurs + bon sens.

### Principes de Gestalt {#gestalt-principles}

- **Proximité** : les objets proches sont perçus comme liés ; utilisez des marges pour regrouper les graphiques associés
- **Zone délimitée** : les objets à l'intérieur d'un conteneur visible sont perçus comme un seul groupe
- **Similarité/contraste** : les éléments d'apparence similaire sont regroupés ; ceux d'apparence différente sont séparés

### Storytelling et tableaux de bord opérationnels {#storytelling-vs-operational-dashboards}

**Storytelling** = données + visuel + récit. Utilisé dans les présentations, pas dans les tableaux de bord opérationnels. Ajoutez des annotations, des titres et des lignes de contexte pour guider l'utilisateur dans la compréhension de l'information.

**Tableaux de bord opérationnels** = conçus pour un usage répété, une exploration en libre-service et un récit minimal.

### Liste de contrôle de visualisation {#visualization-checklist}

Avant de finaliser un tableau de bord :
- [ ] Factoids KPI en haut à gauche (zone de forte attention)
- [ ] Hiérarchie des graphiques : synthèse -> tendance -> ventilation -> détail
- [ ] 5 à 7 couleurs maximum ; codage couleur cohérent entre les graphiques
- [ ] Chaque graphique répond à une seule question de l'utilisateur
- [ ] Libellés de filtre clairs ; positions des filtres proches des graphiques concernés
- [ ] Lignes de contexte et annotations lorsque c'est pertinent
- [ ] Performance : chargement initial < 10 secondes
- [ ] Disposition mobile prise en compte si nécessaire
- [ ] Testé avec les parties prenantes réelles dans un groupe de test

### Principes de storytelling pour les rapports {#report-storytelling-principles}

- Une seule question claire à laquelle répond chaque page
- Le titre énonce l'insight, pas seulement le sujet (« Les ventes ont progressé de 23 % par rapport à N-1 » plutôt que « Analyse des ventes »)
- Codage couleur cohérent (rouge = mauvais, vert = bon)
- Annotations sur les événements clés dans les séries temporelles
- Contexte : ajoutez les périodes de comparaison, les objectifs et les références

## Pièges {#gotchas}

- Construire dans son coin sans points d'étape avec les parties prenantes est l'anti-modèle n° 1 : montrez une maquette avant de construire, montrez une version provisoire à 50 %
- Une grande carte placée en bas à droite détournera l'attention des KPI situés en haut à gauche à cause de l'effet de contraste
- Plus de 6 feuilles par classeur dégradent les performances : envisagez de les répartir dans plusieurs tableaux de bord
- La disposition mobile est une conception distincte dans Tableau, elle n'est pas automatique : prévoyez-la explicitement si nécessaire
- Les demandes du type « construis-moi quelque chose » entraînent des reprises : investissez 2 jours dans la collecte des besoins pour éviter 2 semaines de reconstruction

## Voir aussi {#see-also}

- [[color-theory-visualization]] - échelles de couleurs et accessibilité
- [[tableau-chart-types]] - choix et encodage des graphiques
- [[bi-development-process]] - collecte des besoins avant la conception
- [[powerbi-advanced-features]] - signets et exploration détaillée (drill-through) pour la navigation
