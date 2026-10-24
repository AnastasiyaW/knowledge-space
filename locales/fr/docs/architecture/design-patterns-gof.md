---
title: "Patrons de conception (GoF)"
category: concepts
tags: [design-patterns, gof, solid, oop, creational, structural, behavioral]
level: 3
source_sha256: c5f21df0168cad8898eba79991de8205e8af63b286a8e77b371610a877b781f8
translation: machine
translated_at: '2026-10-24'
---
# Patrons de conception (GoF) {#design-patterns-gof}

Patrons de conception classiques issus du Gang of Four. Un patron décrit un concept général pour résoudre un problème courant - à utiliser uniquement lorsque c'est nécessaire, car les patrons superflus ajoutent de la complexité.

## Principes SOLID {#solid-principles}

| Principe | Règle | Signe de violation |
|-----------|------|----------------|
| **S**ingle Responsibility | Une classe = une seule raison de changer | La classe gère les logs ET la logique métier |
| **O**pen/Closed | Ouvert à l'extension, fermé à la modification | Modifier une classe existante pour un nouveau comportement |
| **L**iskov Substitution | Les sous-types sont substituables à leurs types de base | Une surcharge casse le contrat de la classe de base |
| **I**nterface Segregation | Plusieurs interfaces spécifiques > une interface générale | Implémenter des méthodes inutilisées |
| **D**ependency Inversion | Dépendre d'abstractions, pas d'implémentations | Instanciation directe des dépendances |

**Méta-principes :** privilégier la composition à l'héritage ; programmer vers des interfaces, pas vers des implémentations.

## Patrons créationnels {#creational-patterns}

| Patron | Objectif | Quand l'utiliser |
|---------|---------|-------------|
| **Factory Method** | Interface de création d'objets, les sous-classes décident du type | Types inconnus à l'avance, besoin d'un point d'extension |
| **Abstract Factory** | Créer des familles d'objets apparentés | Plusieurs familles de produits |
| **Builder** | Construire des objets complexes étape par étape | Nombreux paramètres optionnels, représentations différentes |
| **Prototype** | Créer par clonage d'objets existants | Construction coûteuse, éviter la sous-classification |
| **Singleton** | Exactement une instance, accès global | Pool de connexions BD, configuration. Attention : viole SRP, masque les dépendances |

## Patrons structurels {#structural-patterns}

| Patron | Objectif | Quand l'utiliser |
|---------|---------|-------------|
| **Adapter** | Convertir une interface incompatible | Intégration legacy/tiers |
| **Bridge** | Séparer l'abstraction de l'implémentation | Plusieurs dimensions orthogonales, changement à l'exécution |
| **Composite** | Structures arborescentes, traitement uniforme | Hiérarchies tout-partie (système de fichiers, UI, organigramme) |
| **Decorator** | Attacher un comportement dynamiquement par enveloppement | Ajouter des responsabilités sans sous-classification |
| **Facade** | Interface simplifiée d'un sous-système complexe | Réduire le couplage, valeurs par défaut pratiques |
| **Flyweight** | Partager un état commun entre de nombreux objets | Nombre énorme d'objets similaires consommant de la mémoire |
| **Proxy** | Substitut contrôlant l'accès | Chargement paresseux, contrôle d'accès, mise en cache, journalisation |

## Patrons comportementaux {#behavioral-patterns}

| Patron | Objectif | Quand l'utiliser |
|---------|---------|-------------|
| **Chain of Responsibility** | Transmettre la requête le long d'une chaîne de gestionnaires | Plusieurs gestionnaires, ordre variable, chaîne définie à l'exécution |
| **Command** | Encapsuler une requête dans un objet | Annulation, mise en file d'attente, journalisation des opérations |
| **Iterator** | Parcourir une collection sans exposer ses détails internes | Structures complexes (arbre, graphe) nécessitant un accès séquentiel |
| **Mediator** | Centraliser la communication | Nombreuses interdépendances entre composants |
| **Memento** | Capturer/restaurer un état sans violer l'encapsulation | Annulation/rétablissement, instantanés (historique d'éditeur, sauvegardes de jeu) |
| **Observer** | Notification d'événements par abonnement | Des changements dans un objet nécessitent la mise à jour d'autres objets |
| **State** | Le comportement change selon l'état interne | Nombreuses conditions basées sur l'état |
| **Strategy** | Algorithmes interchangeables | Changer d'algorithme à l'exécution, nombreuses variantes |
| **Template Method** | Squelette d'algorithme, les sous-classes redéfinissent les étapes | Structure commune, étapes spécifiques différentes |
| **Visitor** | Nouvelles opérations sans modifier les classes | Opérations qui changent souvent, structure stable |

## Guide de sélection des patrons {#pattern-selection-guide}

```yaml
Creating objects:
  One type           -> Factory Method
  Family of types    -> Abstract Factory
  Complex build      -> Builder
  Clone existing     -> Prototype

Structuring:
  Incompatible APIs  -> Adapter
  Dynamic behavior   -> Decorator
  Tree structures    -> Composite
  Simplify complex   -> Facade

Communication:
  Event notification -> Observer
  Centralized comms  -> Mediator
  Sequential handling -> Chain of Responsibility
  Encapsulated ops   -> Command

Algorithm variation:
  Interchangeable    -> Strategy
  Skeleton + hooks   -> Template Method
  State-dependent    -> State
```

## Relations POO {#oop-relationships}

| Relation | Signification | Force |
|-------------|---------|----------|
| **Dependency** | Utilise temporairement | La plus faible |
| **Association** | Utilise (possède une référence) | Faible |
| **Aggregation** | Possède, peut exister indépendamment | Moyenne |
| **Composition** | Possède, dépend du cycle de vie | Forte |
| **Inheritance** | Est-un | La plus forte |
| **Implementation** | Réalise une interface | - |

## Pièges courants {#gotchas}

- **Singleton** est le patron le plus mal utilisé - souvent employé là où une simple injection de dépendances suffit
- **Surutilisation des patrons** ajoute de la complexité. Si le code fonctionne proprement sans patron, ne pas en forcer un
- **Decorator vs Inheritance** - le décorateur est plus flexible mais crée de nombreux petits objets. L'héritage est plus simple lorsque la hiérarchie est stable
- **Fuites mémoire avec Observer** - les abonnements oubliés maintiennent les objets en vie. Toujours se désabonner
- **Strategy vs State** - avec Strategy, c'est le client qui choisit l'algorithme ; avec State, les transitions se font en interne

## Voir aussi {#see-also}

- [[architectural-styles]] - Patrons au niveau architectural
- [[microservices-communication]] - Patrons des systèmes distribués
- [[enterprise-integration]] - Patrons d'intégration d'entreprise (EIP)
