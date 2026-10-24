---
title: "Documentation d'architecture"
category: concepts
tags: [architecture, documentation, c4-model, adr, uml, diagrams]
level: 3
source_sha256: 8f98448ff3296ec91aa4d0e9b7164eb8ec55f66af0e9e4cad0e0d065423f89c3
translation: machine
translated_at: '2026-10-24'
---
# Documentation d'architecture {#architecture-documentation}

La documentation d'architecture doit être pragmatique, pas exhaustive. Le Manifeste Agile privilégie le logiciel qui fonctionne à une documentation complète - mais la documentation reste précieuse. Concentrez-vous sur ce qui aide les équipes à prendre des décisions et à comprendre le système.

## Méthodes de documentation {#documentation-methods}

- **Diagrammes** - libres (flexibles, nécessitent une légende) ou notations formelles (UML, ArchiMate, C4, BPMN)
- **ADR** - Architecture Decision Records, RFC
- **Tableaux** - comparaison structurée des options
- **Code** - ArchUnit pour les tests automatisés de conformité architecturale
- **Checklists** - critères de validation

## Document d'architecture minimal viable {#minimum-viable-architecture-document}

En l'absence de standard organisationnel, documentez au minimum :

1. **Décisions et principes architecturaux clés** - décisions qui façonnent la structure globale
2. **Composants importants et leurs interactions** - flux de données et de travail à travers le système
3. **Choix technologiques et justifications** - pourquoi chaque outil a été retenu
4. **Schémas de données et relations** - modèles de données, relations entre entités

## Modèle de vues architecturales 4+1 (Kruchten) {#41-architectural-view-model-kruchten}

| Vue | Montre | Diagrammes |
|------|-------|----------|
| **Logique** | Fonctionnalités pour les utilisateurs finaux | Diagrammes de classes, de séquence |
| **Processus** | Concurrence, synchronisation, performance | Diagrammes d'activité, d'états |
| **Composants** | Structure logicielle pour les développeurs | Diagrammes de composants, de paquets |
| **Physique** | Infrastructure et matériel | Diagrammes de déploiement |
| **Scénarios (+1)** | Cas d'utilisation reliant toutes les vues | Diagrammes de cas d'utilisation |

Chaque scénario parcourt les quatre autres vues, validant ainsi l'architecture.

## Modèle C4 {#c4-model}

Alternative pragmatique à UML complet, avec quatre niveaux d'abstraction :

### Niveau 1 : Contexte système {#level-1-system-context}
Niveau le plus élevé. Le système représenté comme une boîte entourée d'utilisateurs et de systèmes externes. Répond à : qu'est-ce que le système, qui l'utilise, avec quoi s'intègre-t-il ?

### Niveau 2 : Conteneur {#level-2-container}
Zoom sur le système. Montre les applications, bases de données, brokers de messages, systèmes de fichiers. Chaque conteneur est une unité déployable séparément.

### Niveau 3 : Composant {#level-3-component}
Zoom sur un conteneur. Montre les composants internes (contrôleurs, services, repositories) et leurs interactions.

### Niveau 4 : Code {#level-4-code}
Diagrammes au niveau des classes. Rarement dessinés par les architectes - générés automatiquement ou pour les modules critiques uniquement.

## Architecture Decision Records (ADR) {#architecture-decision-records-adr}

Documentation légère des décisions individuelles :

```markdown
# ADR-001: Use PostgreSQL for primary data storage

## Status: Accepted
## Date: 2024-01-15

## Context
We need a database for our order processing service.

## Decision
Use PostgreSQL 15.

## Rationale
- Team expertise in PostgreSQL
- ACID compliance required for financial data
- JSON support covers semi-structured data needs
- Cost-effective

## Alternatives Considered
- MongoDB: rejected due to ACID requirements
- MySQL: rejected due to limited JSON support

## Consequences
- Need DBA expertise for optimization
- Must plan for read replicas as load grows
```

## Diagrammes UML pour architectes {#uml-diagrams-for-architects}

### Structurels (les plus utilisés) {#structural-most-used}
- **Diagramme de composants** - composants et interfaces du système
- **Diagramme de déploiement** - cartographie de l'infrastructure physique

### Comportementaux (les plus utilisés) {#behavioral-most-used}
- **Diagramme de séquence** - interactions entre composants dans le temps (essentiel pour la conception d'API)
- **Diagramme d'activité** - flux de travail et de processus à travers les systèmes

## Attribute-Driven Design (ADD) {#attribute-driven-design-add}

Processus de conception itératif issu du SEI de la CMU :

1. **S'assurer que les exigences sont collectées** - cas d'utilisation, contraintes, scénarios d'attributs de qualité
2. **Sélectionner l'élément à affiner** - système entier ou module spécifique
3. **Identifier le driver architectural** - utiliser l'arbre d'utilité pour prioriser (importance métier élevée/moyenne x difficulté technique)
4. **Choisir le concept de conception** - patrons, tactiques, architectures de référence, frameworks, COTS
5. **Instancier les éléments et assigner les responsabilités**
6. **Définir les interfaces** - contrats entre les éléments
7. **Vérifier et raffiner** - contrôler que la décomposition satisfait les drivers

**Fin du processus :** lorsque les risques critiques sont atténués, que tous les drivers sont traités ou que le temps de conception alloué est écoulé.

## Séquence de livraison de la documentation {#documentation-delivery-sequence}

1. Vue d'ensemble de l'architecture - contexte système et diagrammes de composants
2. Spécifications d'API - OpenAPI pour REST, WSDL pour SOAP, AsyncAPI pour l'événementiel
3. Documentation du modèle de données - diagrammes ER, définitions de schémas
4. Spécifications d'intégration - connexions aux services externes
5. Guide de déploiement - prérequis d'infrastructure, configuration
6. Runbook - procédures opérationnelles, supervision, gestion des incidents

## Principes architecturaux à établir {#architectural-principles-to-establish}

1. **Séparation des responsabilités** - chaque composant a une responsabilité délimitée
2. **DRY** - source unique de vérité pour les données et la logique
3. **KISS** - la solution la plus simple qui répond aux exigences
4. **YAGNI** - ne pas construire ce dont on n'a pas encore besoin
5. **Fail Fast** - détecter et signaler les erreurs immédiatement
6. **Concevoir pour la défaillance** - supposer que les composants vont tomber en panne
7. **Configuration plutôt que code** - externaliser les paramètres propres à chaque environnement
8. **API First** - concevoir les interfaces avant l'implémentation

## Pièges à éviter {#gotchas}

- **Ne pas choisir des frameworks par effet de mode** - tenir compte des connaissances de l'équipe, de la courbe d'apprentissage, de la maturité du produit, des types de licences
- **Concevoir en vase clos** peut produire des solutions qui supportent mal les attributs de qualité critiques
- **Une matrice de fonctionnalités aide** - associer les décisions aux attributs de qualité lors de l'évaluation des alternatives
- **Les attributs de qualité sont en conflit** - améliorer l'un peut dégrader un autre ; documentez le compromis
- **Les SAD complets** peuvent faire la taille d'un livre - demandez d'abord quels standards de documentation existent

## Voir aussi {#see-also}

- [[solution-architecture-process]] - Collecte des exigences et résolution des compromis
- [[api-documentation-specs]] - Spécifications OpenAPI, WSDL, AsyncAPI, OpenRPC
- [[architectural-styles]] - Du monolithe aux microservices
