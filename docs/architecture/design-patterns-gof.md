---
title: Design Patterns (GoF)
category: concepts
tags: [design-patterns, gof, solid, oop, creational, structural, behavioral]
---

# Design Patterns (GoF)

Classic design patterns from the Gang of Four. A pattern describes a general concept for solving a common problem - use only when necessary, unnecessary patterns add complexity.

## SOLID Principles

| Principle | Rule | Violation Sign |
|-----------|------|----------------|
| **S**ingle Responsibility | One class = one reason to change | Class does logging AND business logic |
| **O**pen/Closed | Open for extension, closed for modification | Modifying existing class for new behavior |
| **L**iskov Substitution | Subtypes substitutable for base types | Override breaks base class contract |
| **I**nterface Segregation | Many specific interfaces > one general | Implementing unused methods |
| **D**ependency Inversion | Depend on abstractions, not implementations | Direct instantiation of dependencies |

**Meta-principles:** favor composition over inheritance; program to interfaces, not implementations.

## Creational Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Factory Method** | Interface for creating objects, subclasses decide type | Don't know types in advance, need extension point |
| **Abstract Factory** | Create families of related objects | Multiple families of products |
| **Builder** | Construct complex objects step by step | Many optional parameters, different representations |
| **Prototype** | Create by cloning existing objects | Expensive construction, avoid subclassing |
| **Singleton** | Exactly one instance, global access | DB pool, config. Warning: violates SRP, hides dependencies |

## Structural Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Adapter** | Convert incompatible interface | Legacy/third-party integration |
| **Bridge** | Separate abstraction from implementation | Multiple orthogonal dimensions, runtime switch |
| **Composite** | Tree structures, uniform treatment | Part-whole hierarchies (file system, UI, org chart) |
| **Decorator** | Attach behavior dynamically via wrapping | Add responsibilities without subclassing |
| **Facade** | Simplified interface to complex subsystem | Reduce coupling, convenient defaults |
| **Flyweight** | Share common state between many objects | Huge number of similar objects eating memory |
| **Proxy** | Surrogate controlling access | Lazy loading, access control, caching, logging |

## Behavioral Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Chain of Responsibility** | Pass request along handler chain | Multiple handlers, varying order, runtime chain |
| **Command** | Encapsulate request as object | Undo, queueing, logging of operations |
| **Iterator** | Traverse collection without exposing internals | Complex structures (tree, graph) needing sequential access |
| **Mediator** | Centralize communication | Many interdependencies between components |
| **Memento** | Capture/restore state without violating encapsulation | Undo/redo, snapshots (editor history, game saves) |
| **Observer** | Subscription-based event notification | Changes in one object require updating others |
| **State** | Behavior changes based on internal state | Many conditionals based on state |
| **Strategy** | Interchangeable algorithms | Switch algorithms at runtime, many variants |
| **Template Method** | Algorithm skeleton, subclasses override steps | Shared structure, different specific steps |
| **Visitor** | New operations without modifying classes | Operations change frequently, structure is stable |

## Pattern Selection Guide

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

## OOP Relationships

| Relationship | Meaning | Strength |
|-------------|---------|----------|
| **Dependency** | Temporarily uses | Weakest |
| **Association** | Uses (has reference) | Weak |
| **Aggregation** | Has, can exist independently | Medium |
| **Composition** | Owns, lifecycle dependent | Strong |
| **Inheritance** | Is-a | Strongest |
| **Implementation** | Realizes interface | - |

## Gotchas

- **Singleton** is the most misused pattern - often used where simple dependency injection suffices
- **Pattern overuse** adds complexity. If code works cleanly without a pattern, don't force one
- **Decorator vs Inheritance** - decorator is more flexible but creates many small objects. Inheritance is simpler when hierarchy is stable
- **Observer memory leaks** - forgotten subscriptions keep objects alive. Always unsubscribe
- **Strategy vs State** - Strategy client chooses algorithm; State transitions happen internally

## See Also

- [[architectural-styles]] - Architectural-level patterns
- [[microservices-communication]] - Distributed system patterns
- [[enterprise-integration]] - Enterprise integration patterns (EIP)
