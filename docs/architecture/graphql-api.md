---
title: GraphQL API Design
category: reference
tags: [graphql, api, schema, query, mutation, subscription]
---

# GraphQL API Design

GraphQL is a query language and server-side runtime for APIs. Unlike REST where the server defines response structure, GraphQL lets the client specify exactly which fields to retrieve. A single endpoint handles all operations.

## Architecture

```php
Client -> GraphQL layer -> [Backend Service 1]
                        -> [Backend Service 2]
                        -> [Database]
                        -> [REST API]
```

GraphQL aggregates data from multiple sources behind a single endpoint, returning only requested fields. Protocol-agnostic, though HTTP POST is most common.

## Schema (SDL)

The schema is the contract between client and server. Clients can only request fields defined in the schema.

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

- `!` suffix = non-nullable field/argument
- `[Book!]` = list of non-null Book objects
- Fields can accept arguments: `book(id: Int!): Book`

## Three Operation Types

### 1. Query (Read)
```graphql
query {
  country(code: "ru") {
    name
    currency
    capital
  }
}
```

### 2. Mutation (Create/Update/Delete)
```graphql
mutation {
  createCountry(name: "Russia", currency: "RUB", capital: "Moscow") {
    name
  }
}
```

### 3. Subscription (Real-time)
Event-driven updates over persistent connections (typically WebSockets). Client subscribes; server pushes data when events fire.

## Resolvers

Functions that fetch data for each field. Each field has a resolver that can pull from different sources (databases, REST APIs, other services). This enables flexible data aggregation from heterogeneous backends.

## Advantages

- **No over/under-fetching** - client gets exactly what it requests
- **Single endpoint** - one URL for all operations
- **Strong type system** - schema enables IDE support, validation, refactoring
- **Team collaboration** - schema serves as shared contract
- **Evolvability** - add new services by updating resolvers without changing API surface

## Disadvantages

- **Caching difficulty** - flexible queries make HTTP caching harder
- **Security challenges** - flexible queries can expose sensitive data without proper auth
- **Large query performance** - combining many queries can create complex operations
- **Implementation complexity** - more setup overhead than REST for small projects

## When to Use

- Complex, evolving data requirements
- Multiple client platforms (web, mobile, desktop) with different needs
- Microservice architectures aggregating data from many services
- Mobile applications where bandwidth optimization matters

## When NOT to Use

- Simple CRUD APIs
- Small projects with minimal data complexity
- When HTTP caching is critical
- When team lacks GraphQL experience

## Gotchas

- **N+1 problem** - naive resolvers can make N+1 database queries. Use DataLoader for batching
- **Query depth attacks** - malicious clients can send deeply nested queries. Implement query depth/complexity limits
- **No built-in file upload** - requires multipart request spec or separate endpoint
- **Error handling** differs from REST - GraphQL returns 200 even for partial failures, with errors in response body

## See Also

- [[http-rest-fundamentals]] - REST API comparison
- [[grpc-api]] - Alternative high-performance API style
- [[api-documentation-specs]] - GraphQL schema as documentation
