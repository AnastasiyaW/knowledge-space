---
title: "Stratégie de test et gestion de la qualité"
category: reference
tags: [testing, testing-pyramid, contract-testing, chaos-engineering, quality]
level: 3
source_sha256: 9d2c3cc4c08699af932114d202aeb3451e463534341fbccc70e82592ac91eb5f
translation: machine
translated_at: '2026-10-24'
---
# Stratégie de test et gestion de la qualité {#testing-strategy-and-quality-management}

La qualité et la vitesse de développement sont liées par la dette technique : qualité médiocre = développement lent. Une bonne infrastructure de test permet des déploiements plus rapides et plus sûrs.

## Pyramide de tests {#testing-pyramid}

```text
      /    E2E    \        <- Fewest, most expensive, slowest
     / Integration \       <- Middle layer
    /   Unit Tests  \      <- Most tests, cheapest, fastest
```

**Règle :** beaucoup de tests unitaires, environ 10 fois moins de tests d'intégration, environ 10 fois moins de tests E2E.

| Niveau | Périmètre | Coût | Vitesse |
|--------|-----------|------|---------|
| **Unitaire** | Fonctions individuelles | Faible | Rapide |
| **Intégration** | Interactions entre services | Modéré | Modérée |
| **E2E** | Parcours utilisateur complets | Élevé | Lent |

## Tests de contrat {#contract-testing}

Garantissent que deux services peuvent interagir correctement en vérifiant que les contrats d'API correspondent. Essentiel lorsque plusieurs équipes possèdent différents services. Évite les changements cassants lorsqu'une équipe modifie son API.

**Workflow :** le service A définit la requête/réponse attendue → le contrat est publié → le service B valide sa conformité au contrat → toute incohérence est signalée avant le déploiement.

## Chaos Engineering {#chaos-engineering}

Injecter volontairement des défaillances pour tester la résilience. Netflix Chaos Monkey arrête aléatoirement des services en production.

**Si vous n'êtes pas à l'échelle de Netflix ou Google, vous n'en avez pas besoin.** Pertinent uniquement pour les systèmes distribués de très grande taille, afin de vérifier la résilience face à des défaillances aléatoires.

**Types :** injection de fautes (erreurs), mise en forme du trafic (simulation de conditions).

## Techniques de conception de tests {#test-design-techniques}

Sélection stratégique des cas de test permettant de couvrir un maximum de fonctionnalités avec un minimum de tests :
- Partitionnement en classes d'équivalence (une valeur par classe d'entrée)
- Analyse des valeurs limites (bornes des plages valides)
- Tables de décision (combinaisons de conditions)
- Test des transitions d'état (changements d'état valides/invalides)

## Analyse d'impact {#impact-analysis}

Lors de modifications, les développeurs communiquent aux testeurs les zones affectées. La collaboration inter-équipes est essentielle : les testeurs doivent comprendre le rayon d'impact.

## Lien entre qualité et déploiement {#quality-deployment-connection}

Tests de contrat + stratégie de migration appropriée + portes de qualité = confiance pour déployer fréquemment.

Point moins évident : une bonne infrastructure de test **permet** des déploiements plus rapides et plus sûrs, et ne se limite pas à détecter des bugs.

## Pièges courants {#gotchas}

- **Inversion de la pyramide de tests** (beaucoup de E2E, peu de tests unitaires) = CI lente, fragile et coûteuse
- **Tests E2E pour chaque fonctionnalité** : seuls les parcours utilisateur critiques méritent des tests E2E. Utilisez des tests de contrat pour les frontières entre services
- **Chaos testing sans supervision** : injecter des défaillances sans observer les résultats revient simplement à casser des choses
- **Couverture de code à 100 %** ne garantit pas la qualité : on peut avoir une couverture complète et manquer des cas limites critiques

## Voir aussi {#see-also}

- [[devops-cicd]] - Étapes du pipeline CI/CD, stratégies de déploiement
- [[microservices-communication]] - Circuit breaker comme pattern de qualité à l'exécution
- [[quality-attributes-reliability]] - SLA, tests de disponibilité
