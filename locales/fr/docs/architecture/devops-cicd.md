---
title: "DevOps et CI/CD"
category: reference
tags: [devops, cicd, docker, kubernetes, iac, deployment, monitoring]
level: 3
source_sha256: 2e0938b6eb8f14c1494a80775a7ed93ac048416452a0117640af96f8de4ff8f5
translation: machine
translated_at: '2026-10-24'
---
# DevOps et CI/CD {#devops-and-cicd}

DevOps fait le lien entre développement et exploitation grâce à la culture, l'automatisation et l'amélioration continue des processus. Ce n'est pas un outil : c'est une méthodologie combinant des pratiques culturelles, organisationnelles et techniques.

## Pipeline CI/CD {#cicd-pipeline}

```bash
Source (commit) -> Build (compile) -> Test (unit, integration, e2e) ->
  Security scan -> Artifact creation -> Deploy staging -> Acceptance tests ->
  Deploy production -> Smoke tests
```

| Pratique | Description |
|----------|-------------|
| **CI** | Fusions fréquentes (quotidiennes ou plus), build et tests automatisés, détection précoce des bugs |
| **Continuous Delivery** | Livraison automatiquement préparée pour la mise en production, déploiement soumis à approbation manuelle |
| **Continuous Deployment** | Déploiement automatique dès que les tests passent, sans étape manuelle |

## Infrastructure as Code (IaC) {#infrastructure-as-code-iac}

Gérer l'infrastructure au travers de fichiers de configuration versionnés.

| Outil | Approche | Idéal pour |
|-------|----------|------------|
| **Terraform** | Déclaratif, indépendant du cloud | Provisionnement multi-cloud |
| **CloudFormation** | Déclaratif, spécifique à AWS | Environnements exclusivement AWS |
| **Pulumi** | Langages de programmation généralistes | Développeurs préférant le code |
| **Ansible** | Gestion de configuration | Configuration de serveurs, orchestration |

**Infrastructure immuable :** créer de nouvelles instances avec la configuration mise à jour, puis remplacer les anciennes. Élimine la dérive de configuration. Fonctionne avec les conteneurs et les déploiements blue-green.

## Conteneurisation {#containerization}

**Docker :** empaqueter l'application et ses dépendances dans des conteneurs portables.
- Le Dockerfile définit les étapes de build
- docker-compose pour les applications multi-conteneurs
- Bonnes pratiques : images de base légères (Alpine, distroless), builds multi-étapes, utilisateur non-root, health checks, limites de ressources

**Kubernetes (K8s) :** orchestration de conteneurs.
- Concepts clés : Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, Namespaces
- Déploiement automatisé, mise à l'échelle et gestion des applications conteneurisées

## Stratégies de déploiement {#deployment-strategies}

| Stratégie | Mécanisme | Retour arrière | Risque |
|-----------|-----------|----------------|--------|
| **Blue-Green** | Deux environnements identiques, bascule du trafic | Instantané (bascule inverse) | Coût d'infrastructure doublé |
| **Canary** | Déploiement progressif, d'abord sur un petit sous-ensemble | Suppression du canary | Faible : rayon d'impact réduit |
| **Rolling** | Remplacement progressif des instances | Retour arrière en cours | Coexistence brève de versions différentes |
| **Feature flags** | Déploiement avec fonctionnalités derrière des interrupteurs | Désactivation de l'interrupteur | Complexité du code |

## Migrations de base de données sans interruption {#zero-downtime-database-migrations}

**Pattern Expand-Contract :**
1. **Expand** : ajouter la nouvelle colonne ou table à côté de l'ancienne. Les deux fonctionnent
2. **Migrate data** : copier et transformer les données de l'ancienne vers la nouvelle structure
3. **Switch** : mettre à jour l'application pour utiliser la nouvelle structure
4. **Contract** : supprimer l'ancienne structure après une période de vérification

**Principes de migration :**
- Uniquement en avant (ne jamais modifier les scripts existants)
- Versionnées (Git)
- Idempotentes (sûres à exécuter plusieurs fois)
- Plan de retour arrière pour chaque migration

## Supervision et observabilité {#monitoring-and-observability}

### Les trois piliers {#three-pillars}

| Pilier | Contenu | Outils |
|--------|---------|--------|
| **Metrics** | Valeurs numériques dans le temps (latence, débit, erreurs) | Prometheus + Grafana |
| **Logs** | Enregistrements d'événements | ELK Stack, Loki |
| **Traces** | Parcours des requêtes entre services | Jaeger, Zipkin |

**Solutions tout-en-un :** Datadog, New Relic.

### Métriques clés {#key-metrics}
- Latence : p50, p95, p99
- Débit : requêtes par seconde
- Taux d'erreur
- Saturation : taux d'utilisation des ressources
- SLI/SLO/SLA

**Alerting :** alerter sur les symptômes (impact utilisateur) et non sur les causes. Réduire la fatigue liée aux alertes. Disposer d'un runbook pour chaque alerte. PagerDuty et OpsGenie pour la gestion des incidents.

## Méthodologie 12-Factor App {#12-factor-app-methodology}

1. **Codebase** : un dépôt par application
2. **Dependencies** : les déclarer explicitement
3. **Config** : stockée dans les variables d'environnement
4. **Backing services** : traités comme des ressources attachées
5. **Build, release, run** : séparation stricte
6. **Processes** : sans état, sans partage
7. **Port binding** : autonome
8. **Concurrency** : mise à l'échelle par les processus
9. **Disposability** : démarrage rapide, arrêt gracieux
10. **Dev/prod parity** : environnements aussi proches que possible
11. **Logs** : traités comme des flux d'événements
12. **Admin** : processus ponctuels

## Concevoir pour l'exploitation {#design-for-operations}

- Endpoints de santé, arrêt gracieux
- Journalisation structurée, identifiants de corrélation entre services
- Externalisation de la configuration
- Migrations de base de données rétrocompatibles
- Versionnement des API, feature flags
- Métriques métier en complément des métriques techniques

## Pièges à éviter {#gotchas}

- **CI sans tests** : ce n'est qu'un « build continu ». Les tests automatisés sont le cœur de la démarche
- **Blue-green et bases de données** : les deux versions doivent fonctionner avec le même schéma de base de données pendant la transition
- **Nettoyage des feature flags** : les flags obsolètes s'accumulent. Planifier leur suppression après le déploiement
- **Supervision sans alerting** : des tableaux de bord que personne ne consulte ne servent à rien
- **DevSecOps** : intégrer la sécurité à chaque étape, et non en fin de parcours

## Voir aussi {#see-also}

- [[quality-attributes-reliability]] - Disponibilité, tolérance aux pannes, mise à l'échelle automatique
- [[security-architecture]] - Intégration du DevSecOps
- [[microservices-communication]] - Patterns d'architecture de services
- [[database-selection]] - ORM, migrations, patterns sans interruption
