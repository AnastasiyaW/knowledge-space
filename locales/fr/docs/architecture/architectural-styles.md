---
title: "Styles architecturaux - du monolithe aux microservices"
category: concepts
tags: [architecture, monolith, microservices, soa, modular-monolith]
level: 4
source_sha256: 4bc8ced7702788b4cdbb33fb14e2a40aa9f59ac6a6b1653389ce617562e1e962
translation: machine
translated_at: '2026-10-24'
---
# Styles architecturaux - du monolithe aux microservices {#architectural-styles-monolith-to-microservices}

Le choix du style architectural est la première et la plus importante étape de conception. Il détermine la flexibilité, la scalabilité et les caractéristiques clés du système. L'architecture est un spectre, et non un choix binaire.

## Évolution des styles {#style-evolution}

```php
Monolith -> Modular Monolith -> SOA -> Microservices -> Microservices + Micro-Frontends
```

1. **Monolithe** - déploiement unique, fortement couplé. Tous les composants dans une seule base de code
2. **Monolithe modulaire** - frontières de modules claires au sein d'un déploiement unique, interfaces bien définies
3. **SOA** - services via un bus d'entreprise (ESB), base de données partagée possible
4. **Microservices** - services indépendants avec leurs propres bases de données, déploiement indépendant
5. **Microservices + Micro-frontends** - backend et frontend découpés en parties autonomes

## Quand choisir quoi {#when-to-choose-what}

### Commencer par un monolithe lorsque {#start-with-monolith-when}
- L'équipe est petite (< 5-7 développeurs)
- Le domaine est simple
- La rapidité du développement initial est importante
- Le domaine n'est pas encore bien compris
- La fréquence de changement est faible
- L'équipe ne dispose pas d'une maturité DevOps/infrastructure suffisante

### Migrer vers les microservices lorsque {#migrate-to-microservices-when}
- L'équipe grandit et a besoin de déploiements indépendants
- Les besoins de mise à l'échelle diffèrent selon le domaine
- Il faut une diversité technologique
- Des frontières de domaine claires ont été identifiées
- La complexité opérationnelle supplémentaire en vaut les bénéfices

### Arbre de décision {#decision-tree}

```php
Team size < 10?
  -> Monolith (or modular monolith)
Clear domain boundaries + independent deployment needed?
  -> Microservices
Unclear boundaries + fast iteration needed?
  -> Start monolith, extract later (Strangler Fig)
```

## Migration du monolithe vers les microservices {#monolith-to-microservices-migration}

### Motif Strangler Fig {#strangler-fig-pattern}
Remplacer progressivement les fonctionnalités du monolithe :
1. Les nouvelles fonctionnalités sont développées sous forme de microservices
2. Les fonctionnalités existantes sont extraites une à une
3. Le trafic passe par une façade qui décide entre monolithe et microservice
4. Le monolithe se réduit au fil du temps jusqu'à être entièrement remplacé

### Monolithe distribué (anti-pattern) {#distributed-monolith-anti-pattern}
Des services déployés séparément mais si fortement couplés qu'ils doivent être déployés ensemble. Le pire des deux mondes : la complexité distribuée sans les bénéfices de l'indépendance.

## Principes fondamentaux des microservices {#microservices-core-principles}

### Faible couplage {#low-coupling}
Le service A (création de commandes) ne connaît rien du paiement. Le service B (traitement des paiements) ne connaît rien de la création de commandes. Chaque service a un minimum de dépendances, ce qui permet un déploiement indépendant.

### Forte cohésion {#high-cohesion}
Le code d'un même domaine fonctionnel doit rester regroupé. Chaque microservice est responsable d'un seul et unique domaine fonctionnel.

### Bénéfices combinés {#benefits-of-both}
- Mise à l'échelle indépendante par service
- Déploiement indépendant (sans reconstruction complète)
- Chaque service reste simple
- Piles technologiques différentes par service
- Livraison accélérée du code en production

## Motifs de base de données pour les microservices {#microservices-database-patterns}

### Une base de données par service {#database-per-service}
Chaque microservice possède sa propre base de données. Pas de bases partagées. Les services communiquent via des API, et non par jointures. Cela permet la diversité technologique et la mise à l'échelle indépendante.

### Base de données partagée (anti-pattern) {#shared-database-anti-pattern}
Plusieurs services accédant à la même base créent un couplage fort. Acceptable uniquement pendant une migration transitoire du monolithe vers les microservices.

### Règles de propriété des données {#data-ownership-rules}
- Petits jeux de données provenant d'un autre service : cache local (le plus rapide mais nécessite une invalidation)
- Grands jeux de données partagés : cache distribué (Redis) accessible par les deux services
- Si les données étrangères mises en cache >> données propres : reconsidérer les frontières des services

## Découverte de services {#service-discovery}

Les services doivent se trouver mutuellement dans des environnements dynamiques (conteneurs, mise à l'échelle automatique).

- **Découverte côté client** - le client interroge le registre et se connecte directement
- **Découverte côté serveur** - le client envoie la requête à un load balancer qui interroge le registre

Outils : Consul, Eureka, etcd, Kubernetes DNS.

## Pièges à éviter {#gotchas}

- **Ne pas commencer par les microservices** - commencer par un monolithe bien structuré, et découper lorsque des points de douleur apparaissent
- **Loi de Conway** - la conception du système reflète la structure de communication de l'organisation
- **Microservices sans maturité DevOps** = cauchemar opérationnel
- **Le monolithe modulaire** est souvent le juste milieu - des frontières claires sans la complexité d'un système distribué
- **Les architectes semblent parfois peu performants** lorsqu'ils mènent des batailles organisationnelles (par exemple, attendre des mois une infrastructure)

## Voir aussi {#see-also}

- [[microservices-communication]] - Synchrone vs asynchrone, API gateway, BFF, CQRS
- [[distributed-systems-fundamentals]] - Théorème CAP, consensus, réplication
- [[enterprise-integration]] - ESB, styles d'intégration, alternatives modernes
- [[microfrontends]] - Stratégies de découpage du frontend
