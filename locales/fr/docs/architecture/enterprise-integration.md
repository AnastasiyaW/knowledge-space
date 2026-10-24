---
title: "Intégration d'entreprise - ESB, styles, patterns"
category: concepts
tags: [integration, esb, eip, api-gateway, service-mesh, ipaas]
level: 3
source_sha256: d1df8f2a961e01e37d3544f46aa2175412051621ca735d6fb759064fad8a27c7
translation: machine
translated_at: '2026-10-24'
---
# Intégration d'entreprise - ESB, styles, patterns {#enterprise-integration-esb-styles-patterns}

Les systèmes modernes fonctionnent rarement de manière isolée. Une intégration bien conçue réduit la latence, améliore la maintenabilité, permet la scalabilité et garantit la sécurité.

## Styles d'intégration {#integration-styles}

| Style | Mécanisme | Couplage | Latence | Cas d'usage |
|-------|-----------|---------|---------|----------|
| **Transfert de fichiers** | Fichiers partagés (CSV, XML, JSON) | Faible | Élevée | Échange de données par lots |
| **Base de données partagée** | Plusieurs systèmes, même BD | Très élevé | Faible | À éviter dans les architectures modernes |
| **Appel de procédure distante (RPI)** | Appels REST, gRPC, SOAP | Moyen | Faible | Communication synchrone entre services |
| **Messagerie** | Broker de messages (Kafka, RabbitMQ) | Faible | Moyenne | Systèmes asynchrones et découplés |

## Enterprise Service Bus (ESB) {#enterprise-service-bus-esb}

Middleware assurant une intégration centralisée : routage, traduction de protocoles, transformation de messages, orchestration.

**Fonctionnalités principales :**
- **Routage** - basé sur le contenu, sur des règles, dynamique
- **Transformation** - XML vers JSON, mapping de schémas
- **Médiation de protocoles** - SOAP vers REST, JMS vers HTTP
- **Orchestration** - processus métier en plusieurs étapes
- **Virtualisation de services** - abstraction des emplacements et des versions
- **Supervision** - journalisation centralisée, métriques, audit

**Produits :** MuleSoft, IBM Integration Bus, Oracle Service Bus, WSO2, Microsoft BizTalk.

### Anti-pattern de l'ESB {#esb-anti-pattern}
Placer la logique métier dans l'ESB au lieu des services. L'ESB ne doit que router, transformer et assurer la médiation, sans contenir de logique métier. Cela crée un goulot d'étranglement monolithique.

## Alternatives modernes à l'ESB {#modern-alternatives-to-esb}

### API Gateway {#api-gateway}
Plus simple qu'un ESB, centrée sur la gestion des API. Limitation de débit, authentification, routage, transformation.
- Produits : Kong, AWS API Gateway, Apigee, nginx

### Architecture orientée événements {#event-driven-architecture}
Les services communiquent par événements. Un broker d'événements (Kafka) remplace le routage de l'ESB. Chaque service est propriétaire de sa logique.

### Service Mesh {#service-mesh}
Communication service à service au niveau de l'infrastructure. Motif de proxy sidecar.
- Fonctionnalités : mTLS, répartition de charge, coupure de circuit (circuit breaking), observabilité
- Produits : Istio/Envoy, Linkerd
- Aucune modification du code applicatif nécessaire

### iPaaS (Integration Platform as a Service) {#ipaas-integration-platform-as-a-service}
Intégration dans le cloud avec des connecteurs prêts à l'emploi pour les SaaS.
- Produits : MuleSoft Anypoint, Dell Boomi, Azure Integration Services

## Enterprise Integration Patterns (EIP) {#enterprise-integration-patterns-eip}

### Patterns de routage {#routing-patterns}
- **Content-Based Router** - routage selon le contenu du message
- **Message Filter** - suppression des messages indésirables
- **Splitter** - découpage d'un message composite en parties
- **Aggregator** - regroupement de messages liés
- **Scatter-Gather** - diffusion à plusieurs destinataires, puis agrégation des réponses
- **Routing Slip** - liste dynamique d'étapes de traitement

### Patterns de transformation {#transformation-patterns}
- **Envelope Wrapper** - encapsulation et désencapsulation des messages pour le transport
- **Content Enricher** - ajout de données provenant d'une source externe
- **Content Filter** - suppression des données inutiles
- **Normalizer** - conversion de formats différents vers une forme canonique

### Gestion des erreurs {#error-handling}
- **Dead Letter Channel** - messages non traitables
- **Invalid Message Channel** - messages mal formés
- **Retry with backoff** - nouvelles tentatives à délai exponentiel
- **Idempotent Receiver** - traitement sûr des messages dupliqués

## Modèle de données canonique {#canonical-data-model}

Format de données standard vers lequel et depuis lequel tous les systèmes effectuent une traduction. Il réduit les transformations N-à-N en transformations N-à-1.

```bash
System A -> [transform to canonical] -> Canonical Format
System B -> [transform to canonical] ->     |
System C -> [transform to canonical] ->     v
                                      [transform from canonical] -> Target
```

**Compromis :** surcharge de maintenance, mais l'ajout de nouveaux systèmes est simplifié.

## Processus de planification de l'intégration {#integration-planning-process}

```php
Gather requirements -> Model in UML -> Choose style -> Define formats ->
  Implement -> Test -> Deploy (return to any step for refinement)
```

**Liste de vérification des exigences :** systèmes concernés, flux de données (sens, volume, fréquence), besoins de transformation, gestion des erreurs, SLA (latence, disponibilité), sécurité (authentification, chiffrement, sensibilité des données).

## Idempotence dans l'intégration {#idempotency-in-integration}

Les opérations doivent pouvoir être rejouées sans risque, car les messages peuvent être livrés plus d'une fois. Utiliser des identifiants de message uniques, une vérification avant écriture et des opérations upsert.

## Pièges à éviter {#gotchas}

- **La base de données partagée** crée un couplage fort et de véritables cauchemars de coordination lors des changements de schéma : à éviter dans les architectures modernes
- **Le transfert de fichiers** semble simple, mais la gestion du polling, des conventions de nommage, des accès concurrents et des erreurs est complexe
- **Un ESB devient un goulot d'étranglement monolithique** s'il accumule de la logique métier
- **Le service mesh ajoute de la latence** à chaque saut (proxy sidecar) : mesurer avant d'adopter
- **Le surcoût du modèle canonique** : maintenir le format canonique devient un défi de gouvernance

## Voir aussi {#see-also}

- [[microservices-communication]] - API Gateway, BFF, patterns Saga
- [[message-broker-patterns]] - Pub/sub, files d'attente, garanties de livraison
- [[kafka-architecture]] - Streaming d'événements pour l'intégration
- [[distributed-systems-fundamentals]] - CAP, cohérence, réplication
