---
title: "Culture DevOps et SDLC"
category: concepts
tags: [devops, culture, sdlc, agile, automation, collaboration]
level: 2
source_sha256: c0c98a89f04ae9386f2fcc550b6872422eb352a0b2b9406a72fd1b5dd47ed332
translation: machine
translated_at: '2026-10-24'
---
# Culture DevOps et SDLC {#devops-culture-and-sdlc}

DevOps est un ensemble de pratiques, d'outils et de philosophies culturelles visant à automatiser et à intégrer les processus entre le développement logiciel et les opérations informatiques. Il met l'accent sur la collaboration, la responsabilité partagée et l'amélioration continue.

## Le problème traditionnel {#the-traditional-problem}

- Équipes de développement : focus sur les fonctionnalités, la vitesse, « jeter le code par-dessus le mur »
- Équipes d'exploitation : focus sur la stabilité, résistance aux changements, déploiements manuels
- Résultat : frictions, retards, recherche de coupables, mise sur le marché plus lente

## Principes DevOps {#devops-principles}

1. **Collaboration** - objectifs communs entre développement et exploitation
2. **Automatisation** - pipelines CI/CD, IaC, tests automatisés
3. **Amélioration continue** - boucles de rétroaction, raffinement itératif
4. **Orientation client** - livraison rapide de valeur, réponse rapide

## SDLC (Software Development Life Cycle) {#sdlc-software-development-life-cycle}

```php
Plan -> Code -> Build -> Test -> Release -> Deploy -> Operate -> Monitor -> (back to Plan)
```

DevOps automatise les étapes de Build à Deploy, supervise Operate et réinjecte les retours dans la planification.

## Panorama des outils {#tools-landscape}

| Catégorie | Outils |
|----------|-------|
| Gestion de sources | Git, GitHub, GitLab, Bitbucket |
| CI/CD | Jenkins, GitLab CI, GitHub Actions, Azure DevOps |
| Conteneurisation | Docker, containerd |
| Orchestration | Kubernetes, Docker Swarm |
| IaC | Terraform, Ansible, CloudFormation, Pulumi |
| Supervision | Prometheus, Grafana, ELK, Datadog |
| Cloud | AWS, Azure, GCP |
| Dépôt d'artefacts | Nexus, JFrog Artifactory, Docker Hub |

## Agile et Scrum {#agile-and-scrum}

- **Sprints** - itérations de 2 semaines
- **Rôles** - Product Owner, Scrum Master, équipe de développement
- **Cérémonies** - Sprint Planning, Daily Standup, Review, Retrospective
- **Tableau** - To Do -> In Progress -> In Review -> Done

## Étapes de déploiement {#deployment-stages}

| Étape | Objectif | Accès |
|-------|---------|--------|
| Development | Codage local, tests | Développeurs |
| Testing/QA | Tests d'intégration | Équipe QA |
| Staging | Validation préproduction | Interne |
| Production | Trafic utilisateurs réels | Public |

## Versionnage sémantique {#semantic-versioning}

Format : `MAJOR.MINOR.PATCH` (par exemple, 2.1.3)
- MAJOR : changements non rétrocompatibles
- MINOR : nouvelles fonctionnalités, rétrocompatibles
- PATCH : corrections de bogues

## Fondamentaux de sécurité {#security-fundamentals}

- Clés SSH plutôt que mots de passe
- Règles de pare-feu (moindre privilège)
- Secrets dans des variables d'environnement, pas dans le code
- HTTPS/TLS pour les communications externes
- Maintenir les logiciels à jour

## Voir aussi {#see-also}

- [[sre-principles]] - ingénierie de la fiabilité prolongeant DevOps
- [[cicd-pipelines]] - automatisation du pipeline
- [[git-version-control]] - fondation de la gestion de sources
- [[monitoring-and-observability]] - boucle de rétroaction
