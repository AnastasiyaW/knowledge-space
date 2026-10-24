---
title: "BI & Analytics"
type: MOC
level: 2
source_sha256: d2e42a4acbdc0c0d35ed1b63ed7dde8e44aabca448395b7bfa3c805530dccd7e
translation: machine
translated_at: '2026-10-24'
---
# BI & Analytics {#bi-analytics}

## Analytique produit et métriques {#product-analytics-metrics}
- [[product-analytics-fundamentals]] - rôle de l'analyste, pyramide des métriques, métrique North Star, métriques de vanité vs métriques actionnables
- [[product-metrics-framework]] - DAU/MAU/WAU, stickiness, types de rétention, étapes du cycle de vie utilisateur
- [[unit-economics]] - formules CPA/LTV/ARPU, leviers de croissance, délai de récupération (payback period), segmentation RFM
- [[funnel-analysis]] - entonnoirs de conversion, processus d'optimisation, cartes d'événements, patterns SQL pour les entonnoirs
- [[cohort-retention-analysis]] - types de cohortes, SQL de rétention, cohortes LOD dans Tableau, analyse comportementale

## Tableau {#tableau}
- [[tableau-fundamentals]] - connexions aux données, live vs extract, jointures/unions/relations/blending, ordre des filtres, RLS
- [[tableau-calculations]] - calculs au niveau ligne, agrégés, calculs de table, calculs de fenêtre, paramètres, fonctions logiques
- [[tableau-lod-expressions]] - FIXED/INCLUDE/EXCLUDE, interaction avec l'ordre des filtres, implications sur les performances
- [[tableau-chart-types]] - attributs d'encodage, guide de choix des graphiques, actions, sparklines, KPI factoids
- [[tableau-performance-optimization]] - enregistreur de performances, optimisation au niveau serveur, données, calcul et vue

## Power BI {#power-bi}
- [[powerbi-fundamentals]] - interface, Power Query (M), bases de DAX, modèle de données, relations, filtres
- [[powerbi-advanced-features]] - thèmes, visuels personnalisés, paramètres what-if, drill-through, signets, DAX avancé

## Conception de tableaux de bord {#dashboard-design}
- [[dashboard-design-patterns]] - motif en F, disposition modulaire, principes de Gestalt, lois UX, storytelling
- [[color-theory-visualization]] - échelles catégorielles/séquentielles/divergentes, accessibilité, palettes personnalisées
- [[bi-development-process]] - collecte des exigences, carte des tableaux de bord, registre des métriques, communication avec les parties prenantes

## Panorama des outils BI {#bi-tool-landscape}
- [[bi-tools-comparison]] - Tableau vs Power BI vs Superset vs DataLens, cadre de sélection

## Analyse de données (SQL et Python) {#data-analysis-sql-python}
- [[sql-for-analytics]] - SELECT, JOINs, fonctions de fenêtrage, CTE, patterns de requêtes spécifiques à l'analytique
- [[pandas-data-analysis]] - opérations sur DataFrame, nettoyage, groupby, tableaux croisés dynamiques, fusion, visualisation
- [[python-for-analytics]] - bases de Python, NumPy, workflow Jupyter pour les analystes

## Analytique mobile et web {#mobile-web-analytics}
- [[web-marketing-analytics]] - GA, Yandex Metrica, GTM, tags UTM, modèles d'attribution, analytique multicanal
- [[mobile-analytics-platforms]] - Firebase, AppMetrica, intégration et reporting du SDK Amplitude
- [[mobile-attribution-fraud]] - attribution AppsFlyer, deep links, détection de fraude Protect360
- [[app-store-optimization]] - facteurs de classement ASO, recherche de mots-clés, optimisation de la conversion, stratégie de notation
