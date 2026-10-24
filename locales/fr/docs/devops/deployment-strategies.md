---
title: "Stratégies de déploiement"
category: concepts
tags: [devops, deployment, blue-green, canary, rolling-update, feature-flags, release-management]
level: 3
source_sha256: 97d120745594f5362e0120b2a5ac4687a5ffa52ebca3ea7f0518d7bd53410a4c
translation: machine
translated_at: '2026-10-24'
---
# Stratégies de déploiement {#deployment-strategies}

Les stratégies de déploiement déterminent la manière dont les nouvelles versions d'une application remplacent les anciennes. Le choix influe sur l'indisponibilité, la vitesse de retour arrière, le coût en ressources et le niveau de risque encouru.

## Rolling Update (valeur par défaut de Kubernetes) {#rolling-update-kubernetes-default}

Remplace progressivement les anciens pods par les nouveaux. Sans interruption de service si les health checks sont configurés.

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 25%         # max extra pods during update
    maxUnavailable: 25%   # max pods unavailable during update
```

```bash
kubectl set image deployment/app app=app:2.0
kubectl rollout status deployment/app
kubectl rollout undo deployment/app         # rollback
```

## Déploiement Blue-Green {#blue-green-deployment}

Deux environnements identiques. Déployer sur l'environnement inactif, puis basculer le trafic après validation.

- **Blue** = version stable actuelle
- **Green** = nouvelle version
- Retour arrière = rediriger le trafic vers l'environnement précédent
- Dans K8s : deux Deployments, le selector du Service bascule de l'un à l'autre

**Avantages** : retour arrière instantané, tests complets avant la bascule
**Inconvénients** : coût d'infrastructure doublé

## Déploiement Canary {#canary-deployment}

Diriger un faible pourcentage du trafic vers la nouvelle version. Surveiller, puis augmenter progressivement.

Avec Kubernetes + Istio :
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
spec:
  http:
  - route:
    - destination:
        host: app
        subset: v1
      weight: 90
    - destination:
        host: app
        subset: v2
      weight: 10
```

Sans service mesh : utiliser plusieurs Deployments avec des nombres de réplicas différents sous un même Service.

**Avantages** : risque faible, validation progressive
**Inconvénients** : nécessite une capacité de répartition du trafic

## Feature Flags {#feature-flags}

Déployer le code avec les fonctionnalités désactivées. Les activer progressivement par segment d'utilisateurs.

- Découpler le déploiement de la mise en production (release)
- Interrupteur d'arrêt d'urgence pour les fonctionnalités problématiques
- Déploiement progressif par segment d'utilisateurs
- Aucune infrastructure supplémentaire nécessaire

## Checklist de mise en production {#release-checklist}

- **Dimensionnement** : charge attendue, l'infrastructure peut-elle la supporter
- **Intégration** : load balancers configurés, supervision prête
- **Gestion des défaillances** : évaluation de l'impact par composant
- **Plan de retour arrière** : défini et testé
- **Communication** : information des parties prenantes, pages de statut

## Mise en production et budget d'erreur {#release-and-error-budget}

Du point de vue SRE :
- Budget d'erreur restant -> possibilité de déployer plus vite, de prendre plus de risques
- Budget d'erreur épuisé -> geler les mises en production, se concentrer sur la fiabilité
- Changements plus petits = risque moindre (rayon d'impact réduit)
- Mécanismes de retour arrière automatisés obligatoires

## Méthodologie cloud-native en 15 facteurs {#cloud-native-15-factor-methodology}

Extension de l'application 12-Factor pour les services cloud-native :

1. Une base de code par service
2. API First - contrat avant implémentation
3. Dépendances explicites (pom.xml, package.json)
4. Séparation stricte entre conception, build, release et exécution
5. Configuration externalisée (variables d'environnement, serveur de configuration)
6. Journaux comme flux d'événements (stdout)
7. Démarrage rapide, arrêt gracieux (jetabilité / Disposability)
8. Services de support traités comme des ressources attachées
9. Parité des environnements (dev ~ staging ~ prod)
10. Tâches d'administration comme tâches ponctuelles
11. Liaison de port pour l'exposition des services
12. Processus sans état (share-nothing)
13. Passage à l'échelle via le modèle de processus (concurrence)
14. Télémétrie (santé, performance, métriques métier)
15. Authentification/autorisation comme préoccupation de premier plan

## Pièges à éviter {#gotchas}

- Les mises à jour progressives peuvent provoquer un trafic mêlant plusieurs versions pendant la transition : assurer la rétrocompatibilité
- Le blue-green nécessite une stratégie de migration de base de données en cas de changement de schéma
- Le canary exige une bonne observabilité pour détecter les problèmes à faible pourcentage de trafic
- Les feature flags accumulent de la dette technique s'ils ne sont pas nettoyés après déploiement complet
- Le retour arrière de la configuration est aussi important que celui du code

## Voir aussi {#see-also}

- [[sre-principles]] - budgets d'erreur pilotant la vélocité des déploiements
- [[kubernetes-workloads]] - stratégies de déploiement K8s
- [[service-mesh-istio]] - répartition du trafic pour le canary
- [[helm-package-manager]] - versions de releases et retours arrière
- [[gitops-and-argocd]] - déploiements automatisés
