---
title: "Processus d'architecture de solution"
category: concepts
tags: [architecture, requirements, stakeholders, trade-offs, process]
level: 3
source_sha256: 4bcfcb8724331b10443a25cca390c34b2a86454845a6f951b4f202af4d900375
translation: machine
translated_at: '2026-10-24'
---
# Processus d'architecture de solution {#solution-architecture-process}

L'architecture de solution fait le lien entre les besoins métier et la mise en œuvre technologique. Le processus de l'architecte couvre la période allant de la collecte des exigences jusqu'au déploiement, en se concentrant sur la recherche et la résolution des compromis. Plus de 60 % de la réussite dépend des compétences relationnelles : les solutions sont conçues pour des personnes, par des personnes.

## Niveaux d'architecture et rôles {#architecture-levels-and-roles}

| Niveau | Périmètre | Focus |
|-------|-------|-----|
| **Architecture d'entreprise** | Ensemble de l'organisation | Stratégie métier, processus globaux |
| **Architecture de solution** | Problème métier spécifique | Intersection métier-technique, intégration de systèmes |
| **Architecture système/technique** | Système spécifique | Modules, code, processus atomiques |

| Rôle | Périmètre | Activité principale |
|------|-----------|-----------------|
| Ingénieur senior | Ses propres tâches/modules | Développement |
| Tech Lead | Ensemble de l'équipe | Développement + une part de conception |
| Architecte de solution | Plusieurs équipes | Conception + alignement métier |

Dans les petites organisations, une même personne cumule plusieurs rôles. L'autorité se gagne par l'expertise démontrée, et non par le titre.

## Pipeline des exigences {#requirements-pipeline}

```php
Business Architecture Study
  -> Stakeholder Identification
    -> Requirements Elicitation (WHY, WHO, HOW)
      -> NFR Definition (quantified with numbers)
        -> ASR Extraction
          -> Trade-off Identification
            -> Trade-off Resolution
              -> Ready for Solution Design
```

### Trois questions clés {#three-key-questions}

1. **POURQUOI** cette solution est-elle créée ? - Exigences métier, objectifs, valeur attendue
2. **QUI** l'utilisera ? - Tous les groupes d'utilisateurs (clients, personnel de support, administrateurs, partenaires, sécurité)
3. **COMMENT** l'utiliseront-ils ? - Scénarios d'utilisation comme fondement de la conception

**Principe :** N'inventez pas de réponses. Interagissez activement avec les parties prenantes. À ce stade, vous êtes un chercheur.

### Identification des parties prenantes {#stakeholder-identification}

Parties prenantes courantes : sponsors métier, utilisateurs finaux, développeurs/testeurs, support/exploitation, département sécurité, personnel de centre d'appels. Impliquez-les tôt pour instaurer la confiance. Utilisez le brainstorming, la cartographie des parties prenantes et l'analyse influence/intérêt.

## Exigences non fonctionnelles (ENF) {#non-functional-requirements-nfrs}

Sans ENF, vous construisez un système qui plante, perd des données ou ne répond qu'une fois par heure. Quantifiez toujours avec des chiffres.

| Catégorie | Ce qu'il faut définir | Exemple |
|----------|---------------|---------|
| **Performance** | Objectifs de temps de réponse | Le chatbot répond en < 3 secondes |
| **Disponibilité** | Exigences de disponibilité | SLA de 99,9 % |
| **Scalabilité** | Gestion de la croissance | Supporter une multiplication par 10 du nombre d'utilisateurs |
| **Sécurité** | Protection des données, conformité | Conformité à la réglementation sur les données personnelles |
| **Fiabilité** | Tolérance aux pannes, durabilité | Les données survivent aux défaillances |
| **Maintenabilité** | Facilité de mise à jour et de débogage | Supervision, journalisation structurée |

### Checklist d'estimation de charge {#load-estimation-checklist}

- Nombre d'utilisateurs simultanés attendus
- Requêtes par seconde (RPS)
- Volume de données et taux de croissance
- Ratio charge de pointe / charge moyenne
- Temps de réponse au P95/P99

## Exigences architecturalement significatives (ASR) {#architecturally-significant-requirements-asrs}

Signes d'une ASR fonctionnelle :
- Introduit une **nouvelle intégration** dans le système
- Impose un **nouveau mode d'interaction utilisateur**
- Paraît **complexe**, sans implémentation triviale et simple

**TOUTES les ENF sont architecturalement significatives** : elles influencent le choix de l'infrastructure, les patterns architecturaux, le choix des technologies et le coût de la solution.

## Compromis architecturaux {#architectural-trade-offs}

**Principe fondamental : l'architecture est l'art et la science de trouver et de résoudre des compromis.** Il n'existe pas de solution parfaite, seulement des compromis tranchés dans un sens ou dans l'autre.

| Compromis | Exemple de résolution |
|-----------|-------------------|
| Performance vs coût | Commencer par une solution abordable, la faire évoluer ensuite |
| Sécurité vs ergonomie | Éviter l'authentification complète pour le chatbot ; ne demander que le nom et l'e-mail |
| Scalabilité vs complexité | Commencer par un monolithe, concevoir pour des microservices à venir |
| Disponibilité vs coût | Accepter 99,9 % au lieu de 99,999 % |
| Fonctionnalités vs délai de mise sur le marché | MVP avec les fonctionnalités essentielles, itérations ensuite |

### Approches de résolution {#resolution-approaches}

1. **Prioriser avec les parties prenantes** : déterminer quelle caractéristique compte le plus
2. **Trouver un terrain d'entente** : satisfaire partiellement les deux parties

Documentez systématiquement : le compromis identifié, la décision prise, son motif et ce qui a été sacrifié.

## Repères sur les volumes de données {#data-volume-reference-points}

| Plage | Classification | Implications |
|---------------|---------------|-------------|
| < 100 Go | Petit | Machine unique, complexité minimale |
| < 2 To | Modéré | Grande machine unique, services managés |
| < 10-50 To | Important | Plusieurs machines, planification soignée |
| < 1 Po | Grand | Mise à l'échelle dynamique, effort significatif |
| > 100 Po | Extrême | Le remplacement de disques devient routinier |

## Pièges à éviter {#gotchas}

- **Ignorer la phase d'exigences** est la première cause d'échec de projet : chaque étape alimente la suivante
- **Les clients décrivent l'AS-IS mêlé au TO-BE** : l'architecte doit les séparer et demander « Pourquoi le métier investit-il ? »
- **Une ASR fonctionnelle manquée** ne nécessite généralement pas une reconstruction complète : elle se résout le plus souvent en ajoutant un nouveau service
- **Des tickets sans descriptions** : les équipes modernes attendent des ingénieurs qu'ils investiguent les exigences de manière autonome
- **Règle des trois options** : présentez systématiquement au minimum 3 approches pour chaque décision, même si deux d'entre elles sont manifestement mauvaises

## Voir aussi {#see-also}

- [[architecture-documentation]] - Modèle C4, ADR, vues 4+1
- [[architectural-styles]] - Du monolithe aux microservices
- [[quality-attributes-reliability]] - Métriques de disponibilité, tolérance aux pannes, capacité de reprise
- [[database-selection]] - Choix des bases de données selon le type de données et les exigences
