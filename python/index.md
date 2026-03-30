---
title: Python & FastAPI
type: MOC
---

# Python & FastAPI

## Core Language

- [[decorators-and-closures]] - Closures, function/class decorators, parametrized decorators, functools.wraps
- [[generators-and-iterators]] - Iterator protocol, yield, yield from, generator pipelines, itertools
- [[context-managers]] - with statement, __enter__/__exit__, contextlib, ExitStack, async context managers
- [[magic-methods]] - Dunder methods, operator overloading, __slots__, __repr__/__str__, container protocol
- [[error-handling-and-logging]] - Exception hierarchy, chaining, custom exceptions, logging, structlog

## OOP and Type System

- [[oop-inheritance-and-mro]] - MRO, C3 linearization, super(), ABC, Protocol, mixins, __init_subclass__
- [[metaclasses-and-descriptors]] - Metaclass __new__/__prepare__, data/non-data descriptors, __set_name__
- [[type-hints-and-generics]] - Modern annotations (3.10+), TypeVar, Generic, Annotated, ParamSpec, TypeGuard
- [[dataclasses-and-pydantic]] - @dataclass, frozen, __post_init__, Pydantic v2 BaseModel, validation, settings

## Concurrency

- [[async-programming]] - asyncio, async/await, TaskGroup, Semaphore, async generators, producer-consumer
- [[concurrency-and-parallelism]] - GIL, threading, multiprocessing, concurrent.futures, asyncio.to_thread

## FastAPI Stack

- [[fastapi-fundamentals]] - Routing, APIRouter, middleware, lifespan, OpenAPI docs, response models
- [[fastapi-dependency-injection]] - Depends, yield dependencies, Annotated, service layer, testing overrides
- [[fastapi-authentication]] - JWT, OAuth2, bcrypt, role-based access, API keys, refresh tokens
- [[sqlalchemy-and-alembic]] - SQLAlchemy 2.0 models, async sessions, queries, Alembic migrations

## Engineering Practices

- [[testing-with-pytest]] - Fixtures, parametrize, mocking, monkeypatch, conftest.py, TestClient
- [[design-patterns]] - Repository, Strategy, Factory, Observer, Unit of Work, Pythonic adaptations
- [[packaging-and-project-structure]] - pyproject.toml, src-layout, virtual environments, uv/poetry, CLI
- [[docker-deployment]] - Multi-stage Dockerfile, Gunicorn+Uvicorn, docker compose, health checks
