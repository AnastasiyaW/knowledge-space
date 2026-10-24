---
title: "Gestion des incidents SRE"
category: concepts
tags: [devops, sre, on-call, postmortems, incident-response, escalation]
level: 3
source_sha256: 0cceaf0ca9634eadf53daebe4ad0360824750df6c6e35200bfbd6b1cdc9a4eeb
translation: machine
translated_at: '2026-10-24'
---
# Gestion des incidents SRE {#sre-incident-management}

La gestion des incidents couvre la structure des astreintes, l'escalade, l'atténuation et les postmortems sans recherche de responsabilité. L'objectif est de minimiser le MTTR tout en maintenant des pratiques d'astreinte soutenables.

## Structure des astreintes {#on-call-structure}

- Rotation principale + secondaire
- Durée : 1 à 2 semaines en général
- Maximum : 2 incidents par poste de 12 heures (rythme soutenable)
- Follow-the-sun pour les équipes réparties à l'échelle mondiale
- Outils : PagerDuty, Opsgenie, VictorOps

## Responsabilités de l'astreinte {#on-call-responsibilities}

1. **Acquitter** l'alerte dans le délai du SLA (par ex. 5 min pour P1)
2. **Trier** - évaluer la gravité, déterminer si une escalade est nécessaire
3. **Atténuer** - réduire l'impact utilisateur (sans chercher encore la cause racine)
4. **Communiquer** - mettre à jour la page de statut, prévenir les parties prenantes
5. **Résoudre** - remédiation complète
6. **Passer la main** - documenter pour le poste suivant, rédiger le postmortem

## Connaissances essentielles pour l'astreinte {#essential-on-call-knowledge}

1. **Lecture des traces** - comment déboguer des systèmes distribués
2. **Bascule de secours** - mécanismes de repli existants, procédures manuelles
3. **Rollback de déploiement** - revenir en arrière sur les déploiements et configurations défectueux
4. **Limitation de débit** - gérer les DoS malveillants et les auto-DoS accidentels
5. **Limitation de l'impact** - contenir l'impact des composants défaillants sur l'ensemble du système

**Principe clé** : la cause première de tous les problèmes est quelqu'un qui a mal configuré quelque chose. Le rollback de déploiement et de configuration doit être documenté et pratiqué.

## Escalade {#escalation}

| Gravité | Délai de réponse | Action |
|----------|---------------|--------|
| P1 (service arrêté) | Alerte immédiate | War room sous 15 min |
| P2 (dégradé) | Alerte, 30 min | Investigation ciblée |
| P3 (impact mineur) | Ticket | Jour ouvré suivant |

En cas de doute, escaladez.

## Rôles clés lors d'un incident {#key-incident-roles}

### IMOC (Incident Manager On-Call) {#imoc-incident-manager-on-call}

- Dirige et coordonne la résolution des SEV
- Axé sur le TTR (time to recovery), cible : SEV-0 en 15 min
- Point unique de responsabilité
- Garde l'équipe calme, gère la communication vers la direction
- Les ingénieurs se concentrent sur le travail technique et rapportent leur état à l'IMOC

### TLOC (Technical Lead On-Call) {#tloc-technical-lead-on-call}

- Expert technique pour le diagnostic et l'atténuation
- Rapporte son état à l'IMOC
- Après un SEV : travaille sur la cause racine, dirige les expériences de chaos

## Postmortems {#postmortems}

### Principes {#principles}

1. **Sans recherche de coupable** - « qu'est-ce, dans le système, a rendu l'erreur possible ? »
2. **Document écrit** - trace permanente et partagée
3. **Actions avec responsables** - assignées, suivies, priorisées
4. **Diffusion large** - apprentissage à l'échelle de l'organisation

### Modèle {#template}

```markdown
## Incident: [Title]
**Date**: YYYY-MM-DD | **Severity**: P1 | **Duration**: 2h 15m

## Summary
2-3 sentences of what happened.

## Impact
- Users affected: X
- Revenue impact: $Y
- SLO burn: Z%

## Timeline
- HH:MM - Alert fired
- HH:MM - On-call acknowledged
- HH:MM - Root cause identified
- HH:MM - Mitigation applied
- HH:MM - Full resolution

## Root Cause Analysis (5 Whys)
1. Why did the service fail? -> OOM kill
2. Why was memory exhausted? -> Memory leak in handler
...

## What Went Well
- Detection was fast (< 2 min)
- Runbook was accurate

## What Went Wrong
- Monitoring gap: no alert on memory trend
- Rollback took 20 min (should be < 5)

## Action Items
| Action | Owner | Priority | Deadline | Status |
|--------|-------|----------|----------|--------|
| Add memory trend alert | @eng | P1 | 2026-04-10 | TODO |
| Automate rollback | @sre | P2 | 2026-04-17 | TODO |

## Lessons Learned
```

### Critères de déclenchement {#trigger-criteria}

Rédiger un postmortem lorsque : impact visible par les utilisateurs, budget d'erreur consommé, perte de données, intervention manuelle nécessaire, lacune de supervision découverte, escalade de l'astreinte.

## Méthodologie de diagnostic {#diagnostics-methodology}

1. **Observer** - quels symptômes ? Depuis quand ? Qu'est-ce qui a changé ?
2. **Formuler des hypothèses** - causes possibles au regard des symptômes
3. **Tester** - vérifier ou éliminer avec des données
4. **Corriger** - appliquer la remédiation
5. **Prévenir** - ajouter supervision, tests, automatisation

### Dimensions de débogage courantes {#common-debugging-dimensions}

- **Corrélation temporelle** : déploiement ? Changement de configuration ? Variation de trafic ?
- **Périmètre** : un hôte ? Une AZ ? Un service ? Tous les utilisateurs ou une partie ?
- **Graphe de dépendances** : services amont/aval ?
- **Épuisement des ressources** : CPU, mémoire, disque, descripteurs de fichiers, connexions ?

### Hiérarchie des outils {#tools-hierarchy}

Tableaux de bord (Grafana) -> Journaux (Loki/ELK) -> Traces (Jaeger/Tempo) -> Profilage (pprof) -> Core dumps. Commencez large, puis resserrez.

## Partage des connaissances {#knowledge-sharing}

- Documenter les procédures de diagnostic
- Faire de l'astreinte en observation (shadowing) pour se former
- Wheel of Misfortune (incidents simulés)
- Game days (exercices de fiabilité planifiés)

## Pièges à éviter {#gotchas}

- Un postmortem sans suivi des actions est sans valeur
- La reconstitution de la chronologie est critique : à quel moment exact chaque événement s'est produit
- Les runbooks doivent être mis à jour après chaque incident
- « Une seule personne sait comment basculer » est un risque critique : documenter et faire monter en compétence d'autres personnes
- Le coordinateur d'incident communique l'état, il ne débogue PAS

## Voir aussi {#see-also}

- [[sre-principles]] - culture SRE et budgets d'erreur
- [[monitoring-and-observability]] - alerting et SLI/SLO
- [[chaos-engineering-and-testing]] - tests de fiabilité proactifs
- [[deployment-strategies]] - stratégies de rollback
