---
title: "Python"
type: MOC
level: 3
source_sha256: cd2f0ba21a39ac66f5d30521f6a696ca3fcefd88a7ae33ddb5c55c948d32bbec
translation: machine
translated_at: '2026-10-24'
---
# Python {#python}

## Sprachgrundlagen {#language-fundamentals}

- [[variables-types-operators]] - Typen, Zahlen, Operatoren, Variablen, Referenzsemantik
- [[strings-and-text]] - String-Methoden, Formatierung, Kodierung, Bytes, Eingabevalidierung
- [[data-structures]] - Listen, Tupel, Mengen, Dicts, Comprehensions, Counter, defaultdict
- [[control-flow]] - Bedingungen, for-/while-Schleifen, Comprehensions, Generatorausdrücke

## Funktionen und funktionale Programmierung {#functions-and-functional-programming}

- [[functions]] - Parameter, Scope (LEGB), Closures, Lambdas, map/filter, eingebaute Funktionen
- [[decorators]] - Funktions- und Klassen-Decorators, Decorator-Factories, functools.wraps, praktische Muster

## Objektorientierte Programmierung {#object-oriented-programming}

- [[oop-fundamentals]] - Klassen, Vererbung, Properties, Kapselung, super(), MRO
- [[oop-advanced]] - ABC, Descriptors, Metaklassen, Dataclasses, __slots__, __init_subclass__
- [[magic-methods]] - Dunder-Methoden, Operatorüberladung, Container-, Iterator- und Context-Protokolle

## Fehlerbehandlung und I/O {#error-handling-and-io}

- [Fehlerbehandlung und Context Manager](error-handling.md) - try/except, Context Manager, eigene Exceptions, EAFP
- [[file-io]] - Lesen/Schreiben, CSV, JSON, pathlib, os.path, Kodierung
- [[regular-expressions]] - re-Modul, Mustersyntax, findall/sub/split, Gruppen, Flags

## Standardbibliothek {#standard-library}

- [[standard-library]] - collections, datetime, timedelta, random, functools
- [[iterators-and-generators]] - Iterator-Protokoll, yield, yield from, itertools, Pipelines

## Erweiterte Sprachfeatures {#advanced-language-features}

- [[type-hints]] - Annotationen, Generics, Protocol, mypy, TypeVar, Literal
- [[async-programming]] - asyncio, async/await, gather, TaskGroup, aiohttp/httpx
- [Nebenläufigkeit - Threading und Multiprocessing](concurrency.md) - threading, multiprocessing, GIL, ThreadPoolExecutor, ProcessPoolExecutor
- [[memory-and-internals]] - CPython, Referenzzählung, GC, weakref, Bytecode

## Performance und Qualität {#performance-and-quality}

- [[profiling-and-optimization]] - cProfile, line_profiler, Caching, Performance-Tipps
- [[recursion-and-algorithms]] - Rekursion, Big O, Memoization, binäre Suche, Sortierung
- [[testing-with-pytest]] - pytest, Fixtures, parametrize, Coverage, FastAPI-Tests
- [[project-setup-and-tooling]] - pip, venv, PEP 8, poetry, IDEs

## FastAPI-Stack {#fastapi-stack}

- [[fastapi-fundamentals]] - Routing, Path-/Query-Parameter, Depends, Router, Projektstruktur
- [[fastapi-pydantic-validation]] - Schemas, View Models, Feldvalidierung, ORM-Konvertierung
- [[fastapi-database-layer]] - SQLAlchemy 2.0, async Sessions, Alembic-Migrationen, DAO-Muster
- [[fastapi-auth-and-security]] - JWT, bcrypt, Cookies, Login/Logout, Dependency für den aktuellen Benutzer
- [[fastapi-deployment]] - Docker, Nginx, Gunicorn, SSL, Monitoring, API-Versionierung
- [[fastapi-caching-and-tasks]] - Redis-Caching, Celery, BackgroundTasks, Task-Queues

## Ökosystem {#ecosystem}

- [[web-frameworks-comparison]] - Django vs. Flask vs. FastAPI
- [[data-analysis-basics]] - Pandas, Matplotlib, Seaborn, NumPy

## Weiterführende Referenzen {#additional-references}

- [[django-rest-framework]] - Serializer-Muster, Behandlung von Beziehungen, Validierung und fortgeschrittenes ORM im Django REST Framework
- [[stdlib-patterns]] - Datenstrukturen der Python-Standardbibliothek und Werkzeuge für funktionale Programmierung - collections-Modul
- [[web-scraping]] - Web-Scraping-Muster mit BeautifulSoup - Methoden zur Elementsuche, Datenextraktion, Paginierung, Tabellen
