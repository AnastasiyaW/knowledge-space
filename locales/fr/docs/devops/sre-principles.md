---
title: "Principes et culture SRE"
category: concepts
tags: [devops, sre, reliability, error-budget, toil, culture, blameless]
level: 3
source_sha256: 6093815966eb46f4dbde65349266fec1a85e1d781163c9b0b111669b3fbbc124
translation: machine
translated_at: '2026-10-24'
---
# Principes et culture SRE {#sre-principles-and-culture}

Site Reliability Engineering (SRE) est un ensemble de techniques d'ingénierie pour concevoir et maintenir des systèmes fiables. Née chez Google (2003, Ben Treynor). « SRE est ce qui se produit lorsqu'un ingénieur logiciel se voit confier ce qu'on appelait autrefois l'exploitation. »

## SRE vs DevOps {#sre-vs-devops}

- **DevOps** définit CE QUI doit être fait (mouvement culturel, pratiques larges)
- **SRE** définit COMMENT mettre en œuvre la fiabilité (prescriptif, orienté ingénierie)
- SRE met en œuvre les principes DevOps. SRE inclut le développement : 50 % d'exploitation, 50 % de projets d'ingénierie

## Principes clés {#key-principles}

1. **L'exploitation est un problème logiciel** - le résoudre par l'ingénierie
2. **Piloter par les SLO** - et non par une « fiabilité maximale »
3. **Budgets d'erreur** - indisponibilité acceptable quantifiée
4. **Réduction du toil** - automatiser le travail manuel répétitif
5. **Responsabilité partagée** - les SRE co-possèdent la production avec les développeurs
6. **Post-mortems sans blâme** - se concentrer sur les correctifs systémiques

## Piliers de la culture {#culture-pillars}

### Culture d'ingénierie {#engineering-culture}
- Libre échange d'idées. Aucune conséquence organisationnelle pour les problèmes (si le SLO est respecté)
- « Tous dans le même bateau » - responsabilité partagée
- Sans blâme : le blâme relève de la neurophysiologie - bâtir une culture qui le surmonte

### Tout mesurer (observabilité) {#measure-everything-observability}
- Connaître son système : où regarder, ce qui se passe, rapidement
- Simple en apparence, mais complexe et coûteux à mettre en œuvre

### Post-mortems sans blâme {#blameless-postmortems}
- Chercher des coupables est contre-productif
- Culture ouverte pour discuter des problèmes au moment où ils surviennent

### Gestion des incidents {#incident-management}
- Les défaillances surviennent toujours. Runbooks, échelles d'escalade, classification
- Des incidents bien classés, avec des procédures connues, mènent à des systèmes auto-réparateurs
- Exemple le plus simple : les health checks avec redémarrage automatique

## Métriques clés {#key-metrics}

| Métrique | Description |
|--------|-------------|
| Deploy Frequency | Fréquence de mise en production du nouveau code. En baisse = problème de pipeline |
| MTTC | Mean Time To Commit - du commit à la production |
| Change Failure Rate | Proportion de changements provoquant une défaillance |
| MTTA | Mean Time To Acknowledge (~5 min, standard du secteur) |
| MTTR | Mean Time To Resolve (~1 heure, standard du secteur) |

## Budget d'erreur {#error-budget}

`100% - SLO = budget d'erreur`

- SLO 99,9 % = budget de 0,1 % = 43,2 min/mois
- Budget épuisé -> geler les mises en production de fonctionnalités, se concentrer sur la fiabilité
- Budget restant -> déployer plus vite, prendre plus de risques
- Le burn rate du budget d'erreur suit la vitesse de consommation
- La politique de budget d'erreur définit les actions à chaque seuil

## Toil {#toil}

Travail manuel répétitif qui peut être automatisé. Caractéristiques : manuel, automatisable, tactique, sans valeur durable, croît linéairement avec la croissance.

`Toil / Toutes les tâches` = ratio de toil. Cible : inférieur à 50 %.

### Niveaux de maturité de l'automatisation {#automation-maturity-levels}

1. **Aucune automatisation** - entièrement manuel
2. **Scripts spécifiques au système** - administrateurs individuels
3. **Automatisation générique partagée** - outils partagés
4. **Automatisation intégrée** - le système s'auto-gère
5. **Systèmes autonomes** - auto-réparateurs, à mise à l'échelle automatique

## Modèles d'équipes SRE {#sre-team-models}

| Modèle | Description |
|-------|-------------|
| **Infrastructure SRE** | Équipe plateforme partagée. Approche unifiée. Risque : déconnectée du produit |
| **Product SRE** | Intégrée à l'équipe produit. Connaissance approfondie. Risque : pratiques cloisonnées |
| **Consulting SRE** | Mission temporaire. Aide les équipes à s'améliorer. Part lorsque le SLO est atteint |

### Quand le SRE n'est PAS nécessaire {#when-sre-is-not-needed}

- Le service fonctionne déjà bien
- Le service n'est pas important
- Le service est un héritage en cours de mise hors service

## Anti-patterns {#anti-patterns}

- « Le SRE résout tous les problèmes » - le SRE est un ensemble de techniques ; ce sont les personnes qui résolvent les problèmes
- « Le SRE est une solution miracle » - ne fonctionne qu'avec certains systèmes, à certaines étapes du cycle de vie
- « Le SRE fait partie de l'équipe DevOps » - les objectifs diffèrent, la subordination pose problème
- Lancer le SRE sans l'engagement de TOUS les départements

## Pièges {#gotchas}

- Une fiabilité excessive est un gaspillage - le SRE vise une fiabilité « suffisante » pour le métier
- Le SRE exige l'engagement de tous les départements, pas seulement de l'ingénierie
- Cycles Know-Do-Learn : le changement constant est la nouvelle réalité

## Voir aussi {#see-also}

- [[monitoring-and-observability]] - mesure SLI/SLO/SLA
- [[sre-incident-management]] - astreinte, post-mortems, escalade
- [[deployment-strategies]] - gestion des mises en production et budgets d'erreur
- [[chaos-engineering-and-testing]] - tests de fiabilité
- [[sre-automation-and-toil]] - outils et pratiques d'automatisation
