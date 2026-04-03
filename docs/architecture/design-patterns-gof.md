---
title: Design Patterns (GoF) and SOLID Principles
category: concepts
tags: [architecture, design-patterns, solid, oop, gof]
---

# Design Patterns (GoF) and SOLID Principles

The Gang of Four (GoF) design patterns are reusable solutions to common software design problems. Combined with SOLID principles, they form the foundation of maintainable object-oriented design.

## OOP Foundations

**Four pillars**: Abstraction (model relevant attributes only), Encapsulation (hide internals, expose interface), Inheritance (reuse code via hierarchy), Polymorphism (same interface, different behavior).

**Object relationships**: Association (uses), Aggregation (has, can exist independently), Composition (owns, lifecycle dependent), Dependency (temporarily uses), Inheritance (is-a), Implementation (realizes interface).

**Key principles**: Favor composition over inheritance. Program to interfaces, not implementations.

## SOLID Principles

- **S** - Single Responsibility: one class = one reason to change
- **O** - Open/Closed: open for extension, closed for modification
- **L** - Liskov Substitution: subtypes must be substitutable for base types without breaking behavior
- **I** - Interface Segregation: many specific interfaces > one general-purpose
- **D** - Dependency Inversion: depend on abstractions, not concrete implementations

## Creational Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Factory Method** | Interface for creating objects; subclasses decide which class | Class doesn't know in advance which objects to create |
| **Abstract Factory** | Create families of related objects without concrete classes | Code must work with various families of related products |
| **Builder** | Construct complex objects step by step | Object has many optional parameters; need different representations |
| **Prototype** | Create objects by cloning existing ones | Creating objects is costly; avoid subclassing for configurations |
| **Singleton** | Ensure one instance with global access | Need exactly one instance (DB pool, config). Warning: violates SRP, masks dependencies |

## Structural Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Adapter** | Convert incompatible interface to expected one | Integrating legacy code or third-party libraries |
| **Bridge** | Separate abstraction from implementation | Need to extend in multiple orthogonal dimensions |
| **Composite** | Tree structures, treat individual/composite uniformly | Part-whole hierarchies (file system, UI, org structures) |
| **Decorator** | Attach additional behavior dynamically by wrapping | Add responsibilities without subclassing; combine behaviors |
| **Facade** | Simplified interface to complex subsystem | Reduce coupling; provide convenient defaults |
| **Flyweight** | Share common state between many objects | Huge number of similar objects consuming too much memory |
| **Proxy** | Surrogate controlling access to another object | Lazy loading, access control, caching, logging transparently |

**Proxy types**: virtual (lazy loading), protection (access control), remote (network), caching, logging.

## Behavioral Patterns

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Chain of Responsibility** | Pass request along chain of handlers | Multiple handlers in varying order; set determined at runtime |
| **Command** | Encapsulate request as object | Parameterize actions, queue operations, support undo |
| **Iterator** | Traverse collection without exposing internals | Complex structure (tree, graph) needs sequential access |
| **Mediator** | Centralize communication between components | Components have many interdependencies |
| **Memento** | Capture and restore object state | Undo/redo; save snapshots (editor history, game saves) |
| **Observer** | Subscription mechanism for event notification | Changes in one object require updating others dynamically |
| **State** | Object behavior changes based on internal state | Object behavior depends on state; many state conditionals |
| **Strategy** | Family of interchangeable algorithms | Switch algorithms at runtime; many variants of same operation |
| **Template Method** | Algorithm skeleton in base class, subclasses override steps | Several classes share algorithm structure, differ in steps |
| **Visitor** | Add operations to class hierarchy without modifying classes | Operations change frequently but structure is stable |

## Pattern Selection Guide

- **Creating objects**: Factory Method (one type), Abstract Factory (family), Builder (complex construction), Prototype (cloning)
- **Structuring**: Adapter (incompatible interfaces), Decorator (dynamic behavior), Composite (trees), Facade (simplification)
- **Communication**: Observer (events), Mediator (centralized), Chain of Responsibility (sequential), Command (encapsulated operations)
- **Algorithm variation**: Strategy (interchangeable), Template Method (skeleton with hooks), State (behavior per state)

## Gotchas

- Use patterns only when necessary - unnecessary patterns add complexity
- Singleton is the most misused pattern - consider dependency injection instead
- Decorator chains can become hard to debug
- Observer can create memory leaks if subscriptions are not cleaned up
- Don't force a pattern where simple code would suffice

## See Also

- [[software-architecture-fundamentals]] - architectural principles
- [[microservices-patterns]] - distributed system patterns (Saga, CQRS, Circuit Breaker)
