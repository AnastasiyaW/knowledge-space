---
title: "Inférence causale"
category: techniques
tags: [data-science, statistics, causality, quasi-experiments, observational]
level: 2
source_sha256: 87d6b3471645eb3bd5dc40fa6f00eb9cfc1755f1cf344287ceed2d6c5611821f
translation: machine
translated_at: '2026-10-24'
---
# Inférence causale {#causal-inference}

Déterminer une relation de cause à effet à partir de données. La corrélation n'implique pas la causalité, mais avec les bonnes méthodes, on peut se rapprocher de conclusions causales même sans expériences randomisées.

## Hiérarchie des méthodes (par niveau de rigueur) {#methods-hierarchy-by-strength}

1. **Tests A/B randomisés** - référence absolue
2. **Quasi-expériences** - affectation naturelle aux groupes
3. **Analyse contrefactuelle** - pas de groupe de contrôle

## DAG (graphes orientés acycliques) {#dags-directed-acyclic-graphs}

Visualiser les relations causales. Identifier les facteurs de confusion, les médiateurs et les collisionneurs.

- **Facteur de confusion** : affecte à la fois le traitement et le résultat (il faut le contrôler)
- **Médiateur** : situé sur le chemin causal entre le traitement et le résultat
- **Collisionneur** : causé à la fois par le traitement et par le résultat (ne pas le contrôler)

Exemple : moyenne scolaire -> admission à l'université, mais motivation, revenus et qualité de l'établissement sont tous interdépendants.

## Différence de différences (DiD) {#difference-in-differences-did}

Comparer les groupes de traitement et de contrôle avant et après l'intervention.

**Effet = (traitement_après - traitement_avant) - (contrôle_après - contrôle_avant)**

**Prérequis** : hypothèse des tendances parallèles - les groupes auraient suivi la même tendance sans l'intervention.

## Appariement par score de propension (PSM) {#propensity-score-matching-psm}

Lorsque les groupes ne sont pas affectés aléatoirement :
1. Estimer la probabilité de recevoir le traitement pour chaque unité (score de propension)
2. Apparier les unités traitées avec des unités de contrôle ayant des scores de propension similaires
3. Comparer les résultats entre les paires appariées

**Validation** : vérifier que les distributions des covariables deviennent similaires après appariement.

## Contrôle synthétique {#synthetic-control}

Lorsqu'il est impossible de diviser les utilisateurs :
1. Déployer la fonctionnalité dans la région de traitement
2. Construire un modèle prédisant la métrique de la région de traitement à partir des régions de contrôle
3. Comparer la valeur réelle à la référence prédite
4. La différence correspond à l'effet estimé

**Limite** : nécessite des régions de contrôle et reste fragile face aux événements extraordinaires.

## Variables instrumentales (IV) {#instrumental-variables-iv}

Lorsque l'affectation au traitement est confondue :
- Trouver une variable (l'instrument) qui affecte le traitement sans affecter directement le résultat
- Utiliser l'instrument pour isoler la variation causale du traitement
- Exemple classique : la distance au collège comme instrument pour l'effet de l'éducation sur les revenus

## Régression par discontinuité (RDD) {#regression-discontinuity-rdd}

Lorsque le traitement est attribué selon un seuil (score à un test, âge, niveau de revenu) :
- Comparer les unités juste au-dessus et juste en dessous du seuil
- Elles sont en pratique affectées aléatoirement à proximité du seuil
- Estimer l'effet du traitement au niveau de la discontinuité

## Pièges à éviter {#gotchas}
- **Biais de variable omise** : les facteurs de confusion manquants invalident les conclusions causales
- L'hypothèse des tendances parallèles de la DiD n'est pas testable (on ne peut vérifier que la période précédant l'intervention)
- Le PSM ne contrôle que les facteurs de confusion observés : les facteurs cachés demeurent
- Le contrôle synthétique est fragile lorsque le nombre d'unités de contrôle est faible
- Ne pas confondre modèles prédictifs et modèles causaux : une variable peut bien prédire sans être causale
- Les « expériences naturelles » ne valent que par la solidité de l'argument d'exogénéité

## Voir aussi {#see-also}
- [[hypothesis-testing]] - les tests A/B comme expérience randomisée
- [[descriptive-statistics]] - comprendre les données avant l'analyse causale
- [[bi-dashboards]] - présenter les résultats de l'analyse causale
