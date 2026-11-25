---
title: "Conception d'API GraphQL"
category: reference
tags: [graphql, api, schema, query, mutation, subscription]
level: 2
source_sha256: 957489e0b3f5a9f101ca3c21bdce7ee72e5647ac78ee4f97deb76135973503d5
translation: machine
translated_at: '2026-10-24'
---
# Conception d'API GraphQL {#graphql-api-design}

GraphQL est un langage de requête et un runtime côté serveur pour les API. Contrairement à REST, où le serveur définit la structure de la réponse, GraphQL permet au client de spécifier exactement les champs à récupérer. Un point de terminaison unique gère l'ensemble des opérations.

## Architecture {#architecture}

```php
Client -> GraphQL layer -> [Backend Service 1]
                        -> [Backend Service 2]
                        -> [Database]
                        -> [REST API]
```

GraphQL agrège des données provenant de plusieurs sources derrière un point de terminaison unique, en ne renvoyant que les champs demandés. Indépendant du protocole, même si HTTP POST est le plus courant.

## Schéma (SDL) {#schema-sdl}

Le schéma est le contrat entre le client et le serveur. Les clients ne peuvent demander que les champs définis dans le schéma.

```graphql
type Book {
  id: Int!
  title: String!
  pages: Int
  chapters: Int
}

type Query {
  books: [Book!]
  book(id: Int!): Book
}

type Mutation {
  createBook(title: String!, pages: Int, chapters: Int): Book!
  updateBook(id: Int!, title: String, pages: Int, chapters: Int): Book!
  deleteBook(id: Int!): Boolean!
}
```

- Le suffixe `!` = champ ou argument non nullable
- `[Book!]` = liste d'objets Book non nullables
- Les champs peuvent accepter des arguments : `book(id: Int!): Book`

## Trois types d'opérations {#three-operation-types}

### 1. Query (lecture) {#1-query-read}
```graphql
query {
  country(code: "ru") {
    name
    currency
    capital
  }
}
```

### 2. Mutation (création/mise à jour/suppression) {#2-mutation-createupdatedelete}
```graphql
mutation {
  createCountry(name: "Russia", currency: "RUB", capital: "Moscow") {
    name
  }
}
```

### 3. Subscription (temps réel) {#3-subscription-real-time}
Mises à jour pilotées par les événements sur des connexions persistantes (généralement WebSockets). Le client s'abonne ; le serveur envoie les données lorsque les événements se produisent.

## Resolvers {#resolvers}

Fonctions qui récupèrent les données pour chaque champ. Chaque champ dispose d'un resolver pouvant puiser dans différentes sources (bases de données, API REST, autres services). Cela permet une agrégation de données flexible à partir de backends hétérogènes.

## Avantages {#advantages}

- **Pas de sur-récupération ni de sous-récupération** - le client obtient exactement ce qu'il demande
- **Point de terminaison unique** - une seule URL pour toutes les opérations
- **Système de types strict** - le schéma permet le support IDE, la validation et le refactoring
- **Collaboration en équipe** - le schéma sert de contrat partagé
- **Évolutivité** - ajouter de nouveaux services en mettant à jour les resolvers sans modifier la surface de l'API

## Inconvénients {#disadvantages}

- **Difficulté de mise en cache** - des requêtes flexibles compliquent la mise en cache HTTP
- **Défis de sécurité** - des requêtes flexibles peuvent exposer des données sensibles sans authentification appropriée
- **Performance des grosses requêtes** - combiner de nombreuses requêtes peut créer des opérations complexes
- **Complexité d'implémentation** - plus de mise en place qu'avec REST pour les petits projets

## Quand l'utiliser {#when-to-use}

- Besoins de données complexes et en évolution
- Plusieurs plateformes clientes (web, mobile, desktop) aux besoins différents
- Architectures microservices agrégeant des données de nombreux services
- Applications mobiles où l'optimisation de la bande passante est importante

## Quand ne PAS l'utiliser {#when-not-to-use}

- API CRUD simples
- Petits projets à la complexité de données minimale
- Lorsque la mise en cache HTTP est critique
- Lorsque l'équipe n'a pas d'expérience de GraphQL

## Pièges courants {#gotchas}

- **Problème N+1** - des resolvers naïfs peuvent générer N+1 requêtes en base de données. Utilisez DataLoader pour le regroupement des requêtes
- **Attaques par profondeur de requête** - des clients malveillants peuvent envoyer des requêtes profondément imbriquées. Mettez en place des limites de profondeur/complexité des requêtes
- **Pas d'upload de fichiers intégré** - nécessite la spécification multipart request ou un point de terminaison séparé
- **La gestion des erreurs** diffère de REST - GraphQL renvoie 200 même en cas d'échecs partiels, avec les erreurs dans le corps de la réponse

## Voir aussi {#see-also}

- [[http-rest-fundamentals]] - comparaison avec REST
- [[grpc-api]] - style d'API alternatif haute performance
- [[api-documentation-specs]] - le schéma GraphQL comme documentation
