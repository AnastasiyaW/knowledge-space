---
title: "Fondamentaux de l'analyse produit"
category: concepts
tags: [bi-analytics, product-analytics, metrics, analyst-role]
level: 1
source_sha256: 2e899eef468aaac0730639c5f683b3fc078a3178f23a2311ab6428547de6916b
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de l'analyse produit {#product-analytics-fundamentals}

L'analyse produit est la discipline qui consiste à mesurer et comprendre le comportement des utilisateurs au sein d'un produit afin d'orienter les décisions business. Elle combine une réflexion analytique avec la mesure des données : savoir utiliser SQL ou Tableau est nécessaire mais insuffisant ; la compétence centrale consiste à comprendre ce qu'il faut mesurer et pourquoi.

## Points clés {#key-facts}

- L'analyse produit répond à : quel problème cherchons-nous à résoudre, qui est l'audience, comment résolvons-nous ce problème, que voulons-nous atteindre, et comment gagnons-nous de l'argent
- Un analyste produit définit les métriques clés, collecte les données, les analyse, mène des expérimentations (tests A/B) et met en œuvre les conclusions
- Le cycle en cinq étapes de l'analyste : définir les métriques -> collecter les données -> analyser -> expérimenter -> mettre en œuvre
- L'analyse doit être impliquée dès les premières phases de conception, et non ajoutée après le lancement
- Les recommandations doivent reposer sur des chiffres, et non sur des émotions
- La définition d'un « utilisateur actif » varie selon le produit et doit être explicitement définie pour chaque contexte

## Modèles {#patterns}

### Pyramide des métriques {#metrics-pyramid}

Un outil permettant de visualiser les processus et d'identifier les KPI. Structure : l'OBJECTIF business en haut, les métriques primaires au niveau 1, les métriques de décomposition/secondaires au niveau 2.

Erreurs courantes lors du choix des KPI :
- Choisir un indicateur unique (crée des angles morts)
- Choisir trop d'indicateurs (paralysie d'analyse)

La formulation de la tâche doit être précise : non pas « Analyser le trafic du site », mais « Étudier l'impact de la résolution des écrans sur le taux de conversion et formuler des recommandations ».

### Métriques de vanité vs métriques actionnables {#vanity-vs-actionable-metrics}

**Les métriques de vanité** ont une bonne apparence mais n'orientent pas les décisions :
- Nombre total d'utilisateurs inscrits (inclut les inactifs)
- Pages vues (sans contexte)
- Téléchargements (sans indication d'engagement)

**Les métriques actionnables** sont directement liées aux décisions business :
- DAU/MAU avec une définition précise de « actif »
- Taux de conversion des entonnoirs (étape par étape)
- Courbes de rétention (J1/J7/J30)
- Taux d'adoption des fonctionnalités
- Revenu par cohorte

### Métrique North Star {#north-star-metric}

Une métrique unique qui capture au mieux la valeur délivrée. Tout est mesuré par rapport à son impact sur cette métrique. Exemple : pour Spotify, « temps d'écoute par utilisateur ».

**Les métriques d'entrée** (leviers sur lesquels les équipes agissent) pilotent les **métriques de sortie** (résultats business) :
- Entrée : taux d'adoption des fonctionnalités → Sortie : rétention
- Entrée : taux de finalisation de l'onboarding → Sortie : rétention à J7
- Entrée : taux de réussite de la recherche → Sortie : conversion en achat

## Pièges {#gotchas}

- Variables propres à l'entreprise qui influencent la mise en place de l'analyse : taille et stade de l'entreprise, B2B ou B2C, structure des équipes, méthodologie (Scrum/Agile), outillage et niveau de maturité de la culture analytique
- L'analyse marketing et l'analyse produit répondent à des questions différentes : le marketing se concentre sur l'efficacité des canaux et l'allocation budgétaire, le produit sur le comportement des utilisateurs et la performance des fonctionnalités
- La pyramide des métriques doit être réévaluée à mesure que le produit évolue : les métriques adaptées à une startup diffèrent de celles d'un produit mature

## Voir aussi {#see-also}

- [[product-metrics-framework]] - définitions de DAU/MAU, stickiness et rétention
- [[funnel-analysis]] - concepts d'entonnoir de conversion et optimisation
- [[unit-economics]] - calculs de rentabilité par utilisateur
- [[bi-development-process]] - recueil des besoins et flux de travail des tableaux de bord
