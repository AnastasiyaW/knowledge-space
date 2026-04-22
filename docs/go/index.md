---
title: Go
description: Go language fundamentals, concurrency primitives (goroutines, channels), HTTP servers, modules, error-handling patterns, and production microservice idioms.
type: MOC
---

# Go

Go is a compiled systems language built for concurrent network services: fast compile times, a rich standard library, first-class goroutines and channels, and a minimal surface area. Articles cover the concurrency model (goroutines, channels, select, sync primitives), error-handling idioms that differ from exceptions, interface-driven composition, the net/http toolkit, and production patterns for microservices and database access. Each entry is copy-paste-ready code plus the gotcha you only learn after shipping.

## Fundamentals
- [[modules-packages]] - Go modules, packages, dependency management
- [[error-handling]] - Error handling patterns, wrapping, sentinel errors
- [[interfaces-composition]] - Interfaces, embedding, composition over inheritance

## Concurrency
- [[goroutines-channels]] - Goroutines, channels, select, sync primitives

## Web & Servers
- [[http-servers]] - HTTP servers, routing, middleware, net/http patterns
