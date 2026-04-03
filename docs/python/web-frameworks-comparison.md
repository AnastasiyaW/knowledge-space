---
title: Python Web Frameworks Comparison
category: frameworks
tags: [python, django, flask, fastapi, web-frameworks, comparison]
---

# Python Web Frameworks Comparison

Python has three major web frameworks: Django (batteries-included, 2005), Flask (micro-framework, 2010), and FastAPI (modern async-first, 2018). Each serves different use cases and team preferences.

## Key Facts

- Django: built-in ORM, admin panel, auth, templates, DRF for REST APIs
- Flask: minimal core, choose your own ORM/auth/etc via extensions
- FastAPI: native async, auto-generated docs, Pydantic validation, highest performance
- FastAPI increasingly appears in job postings for new projects; Django dominates legacy
- Microservices trend favors FastAPI/Flask; monolith approach favors Django

## Comparison

| Feature | Django | Flask | FastAPI |
|---------|--------|-------|---------|
| Year | 2005 | 2010 | 2018 |
| Philosophy | Batteries-included | Micro, freedom | Modern, async-first |
| Async | Limited (3.1+) | No (needs extensions) | Native |
| ORM | Built-in | Choose your own | Choose your own |
| Admin panel | Built-in | Flask-Admin | None built-in |
| API docs | Manual / DRF | Manual | Auto-generated (OpenAPI) |
| Validation | Manual / DRF | Manual | Pydantic (built-in) |
| Performance | Lower | Medium | Highest |
| Best use | Full web apps | Small APIs | Modern APIs, microservices |

## When to Choose

### Django
- Full-featured web applications with admin interface
- Rapid prototyping with built-in tools
- Teams that prefer convention over configuration
- Projects needing built-in auth, ORM, templating out of the box

### Flask
- Small to medium APIs
- Developers wanting full control over architecture
- Learning web development basics
- Lightweight services where batteries-included is overkill

### FastAPI
- REST APIs and microservices
- High-performance async backends
- New projects prioritizing modern tooling
- Teams already using type hints and Pydantic

## Django ORM vs SQLAlchemy

| Feature | SQLAlchemy | Django ORM |
|---------|-----------|------------|
| Queries | `select(Model).where(...)` | `Model.objects.filter(...)` |
| Session | Manual management | Auto (request lifecycle) |
| Migrations | Alembic (separate) | Built-in `makemigrations` |
| Async | Full (asyncpg) | Limited |
| Lazy loading | selectinload/joinedload | select_related/prefetch_related |

## See Also

- [[fastapi-fundamentals]] - FastAPI in depth
- [[fastapi-deployment]] - production deployment patterns
- [[architecture/index]] - monolith vs microservices decisions
