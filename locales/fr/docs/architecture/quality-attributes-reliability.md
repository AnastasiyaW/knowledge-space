---
title: "Attributs de qualité - Fiabilité et tolérance aux pannes"
category: concepts
tags: [reliability, availability, fault-tolerance, sla, chaos-engineering, recovery]
level: 4
source_sha256: e28fcb10ed3daf8a63278600bec02ec1f3203d96f005096220afddd6a9f3461f
translation: machine
translated_at: '2026-10-24'
---
# Attributs de qualité - Fiabilité et tolérance aux pannes {#quality-attributes-reliability-and-fault-tolerance}

Fiabilité = le système fonctionne correctement dans des conditions spécifiées, sur la durée, y compris la reprise après défaillance. Trois piliers : disponibilité, tolérance aux pannes, capacité de reprise.

## Disponibilité {#availability}

Pourcentage du temps pendant lequel le système est accessible. Temps de fonctionnement / durée totale d'observation.

| SLA | Indisponibilité/an | Classification |
|-----|--------------|----------------|
| 99.999% | ~5 min | Cinq neuf (idéal) |
| 99.99% | ~52 min | Quatre neuf |
| 99.9% | ~8,76 heures | Standard |
| 99% | ~3,65 jours | Basique |
| 95% | ~18,25 jours | Faible |

### Outils de disponibilité {#availability-tools}

| Outil | Rôle |
|------|---------|
| **Auto-scaling** | Ajouter/retirer dynamiquement des instances selon des métriques |
| **Load balancer** | Répartir le trafic entre les instances |
| **CDN** | Distribution géographique du contenu statique |
| **Caching** | Réduire la charge sur le backend |
| **Rate limiting** | Prévenir la surcharge |
| **Service discovery** | Détection automatique des services (Consul, etcd, ZooKeeper) |
| **Health checks** | Sondes actives ou heartbeats passifs |
| **Connection pooling** | Réutiliser des connexions préétablies |
| **Hot standby** | Sauvegarde synchronisée, bascule immédiate |
| **Cold standby** | Sauvegarde arrêtée, nécessite un temps de démarrage |

## Tolérance aux pannes {#fault-tolerance}

Le système continue de fonctionner lors de défaillances partielles.

### Métriques clés {#key-metrics}

| Métrique | Mesure | Idéal | Normal | Faible |
|--------|----------|-------|--------|------|
| **MTTF** | Temps entre deux pannes | 2 ans | 6 mois | 1 semaine |
| **MTTR** | Temps de restauration | 5 min | 30 min | 3 jours |

### Patterns de tolérance aux pannes {#fault-tolerance-patterns}

**Failover :**
- **Active-Passive** - une instance active, la secondaire attend
- **Active-Active** - toutes les instances traitent le trafic simultanément

**Bulkhead :** Isoler les ressources pour qu'une défaillance ne se propage pas en cascade. Isolation au niveau des threads ou des processus.

**Timeouts + Retries :** Backoff exponentiel avec jitter pour éviter le thundering herd.

**Graceful Degradation :** Désactiver les fonctionnalités non critiques. Si le service de recommandations est hors service, les achats fonctionnent toujours.

**Chaos Engineering :** Injecter volontairement des défaillances. Netflix Chaos Monkey tue aléatoirement des services en production pour vérifier l'auto-guérison.

### Pratiques organisationnelles {#organizational-practices}
- **Plans de reprise** - scénarios préparés à l'avance, testés régulièrement
- **Analyse post-mortem** - chronologie, cause racine, actions menées, efficacité de la communication

## Capacité de reprise {#recoverability}

Aptitude à revenir à un état opérationnel après une défaillance.

### Métriques clés {#key-metrics_1}

| Métrique | Mesure | Idéal | Normal | Faible |
|--------|----------|-------|--------|------|
| **RTO** | Indisponibilité maximale acceptable | 5 min | 1 heure | 3 jours |
| **RPO** | Perte de données maximale acceptable | 1 min | 15 min | 1 jour |

### Outils de reprise {#recovery-tools}

- **Reprise automatisée** - scripts + orchestration (Kubernetes redémarre automatiquement)
- **Rollback** - revenir rapidement à la version stable précédente
- **Database rollback** - mécanismes de annulation de transactions
- **Configuration management** - Ansible pour le versionnement de la configuration

**Principe clé :** la préparation est essentielle. Préparer à l'avance scripts et scénarios pour une reprise rapide.

## Correspondance problème-outil {#problem-to-tool-mapping}

| Problème | Solution |
|---------|----------|
| Serveur en panne, redémarrage manuel nécessaire | Health checks + redémarrage automatique |
| Pics de trafic provoquant une dégradation | Auto-scaling |
| Microservice hors service, impossible de trouver un standby | Service discovery |
| Toutes les requêtes atteignent un seul serveur | Load balancer |
| Latence élevée pour les utilisateurs distants | CDN + distribution géographique |
| Base de données surchargée par les requêtes | Caching |
| Un seul client inonde l'API | Rate limiting |
| Panne d'un serveur unique = indisponibilité totale | Hot/cold standby |

## Rôle de l'architecte {#architects-role}

La valeur de l'architecte réside dans une compréhension approfondie du domaine métier et des besoins, et non dans la connaissance de chaque détail technique. Question centrale : « quoi et pourquoi » - les détails d'implémentation sont délégués aux équipes de développement.

Les décisions techniques sont liées à la culture organisationnelle, à la stratégie métier et aux exigences réglementaires. Toutes les métriques de fiabilité varient selon le cas d'usage, la criticité du système et les exigences métier.

## Pièges à éviter {#gotchas}

- **Cinq neuf coûtent exponentiellement plus cher** que trois neuf - chaque neuf supplémentaire coûte environ 10 fois plus
- **Le MTTR compte plus que le MTTF** en pratique - les pannes sont inévitables, une reprise rapide est l'objectif
- **Hot standby non testé** - un standby jamais testé peut ne pas fonctionner au moment voulu. Tester la bascule régulièrement
- **Chaos engineering sans supervision** - injecter des pannes sans observer les résultats revient simplement à casser des choses
- **SLA != SLO != SLI** - le SLI mesure, le SLO fixe la cible, le SLA est le contrat avec ses conséquences

## Voir aussi {#see-also}

- [[distributed-systems-fundamentals]] - Théorème CAP, consensus, réplication
- [[microservices-communication]] - Circuit breaker, patterns bulkhead
- [[devops-cicd]] - Stratégies de déploiement, monitoring, observabilité
- [[security-architecture]] - La sécurité comme partie de la fiabilité
