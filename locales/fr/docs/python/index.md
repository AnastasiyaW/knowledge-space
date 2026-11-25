---
title: "Python"
type: MOC
level: 3
source_sha256: cd2f0ba21a39ac66f5d30521f6a696ca3fcefd88a7ae33ddb5c55c948d32bbec
translation: machine
translated_at: '2026-10-24'
---
# Python {#python}

## Fondamentaux du langage {#language-fundamentals}

- [[variables-types-operators]] - types, nombres, opérateurs, variables, sémantique des références
- [[strings-and-text]] - méthodes de chaînes, formatage, encodage, bytes, validation des entrées
- [[data-structures]] - listes, tuples, ensembles, dictionnaires, compréhensions, Counter, defaultdict
- [[control-flow]] - conditionnelles, boucles for/while, compréhensions, expressions génératrices

## Fonctions et programmation fonctionnelle {#functions-and-functional-programming}

- [[functions]] - paramètres, portée (LEGB), fermetures, lambdas, map/filter, fonctions intégrées
- [[decorators]] - décorateurs de fonctions et de classes, fabriques de décorateurs, functools.wraps, patterns pratiques

## Programmation orientée objet {#object-oriented-programming}

- [[oop-fundamentals]] - classes, héritage, propriétés, encapsulation, super(), MRO
- [[oop-advanced]] - ABC, descripteurs, métaclasses, dataclasses, __slots__, __init_subclass__
- [[magic-methods]] - méthodes dunder, surcharge d'opérateurs, protocoles de conteneur, itérateur et gestionnaire de contexte

## Gestion des erreurs et E/S {#error-handling-and-io}

- [Gestion des erreurs et gestionnaires de contexte](error-handling.md) - try/except, gestionnaires de contexte, exceptions personnalisées, EAFP
- [[file-io]] - lecture/écriture, CSV, JSON, pathlib, os.path, encodage
- [[regular-expressions]] - module re, syntaxe des motifs, findall/sub/split, groupes, drapeaux

## Bibliothèque standard {#standard-library}

- [[standard-library]] - collections, datetime, timedelta, random, functools
- [[iterators-and-generators]] - protocole d'itération, yield, yield from, itertools, pipelines

## Fonctionnalités avancées du langage {#advanced-language-features}

- [[type-hints]] - annotations, génériques, Protocol, mypy, TypeVar, Literal
- [[async-programming]] - asyncio, async/await, gather, TaskGroup, aiohttp/httpx
- [Concurrence - Threading et multiprocessing](concurrency.md) - threading, multiprocessing, GIL, ThreadPoolExecutor, ProcessPoolExecutor
- [[memory-and-internals]] - CPython, comptage de références, GC, weakref, bytecode

## Performance et qualité {#performance-and-quality}

- [[profiling-and-optimization]] - cProfile, line_profiler, mise en cache, conseils de performance
- [[recursion-and-algorithms]] - récursivité, Big O, memoization, recherche dichotomique, tri
- [[testing-with-pytest]] - pytest, fixtures, parametrize, couverture, tests FastAPI
- [[project-setup-and-tooling]] - pip, venv, PEP 8, poetry, IDE

## Stack FastAPI {#fastapi-stack}

- [[fastapi-fundamentals]] - routage, paramètres de chemin/requête, Depends, routeurs, structure de projet
- [[fastapi-pydantic-validation]] - schémas, view models, validation de champs, conversion ORM
- [[fastapi-database-layer]] - SQLAlchemy 2.0, sessions asynchrones, migrations Alembic, pattern DAO
- [[fastapi-auth-and-security]] - JWT, bcrypt, cookies, connexion/déconnexion, dépendance à l'utilisateur courant
- [[fastapi-deployment]] - Docker, Nginx, Gunicorn, SSL, supervision, versionnement de l'API
- [[fastapi-caching-and-tasks]] - mise en cache avec Redis, Celery, BackgroundTasks, files de tâches

## Écosystème {#ecosystem}

- [[web-frameworks-comparison]] - Django vs Flask vs FastAPI
- [[data-analysis-basics]] - Pandas, Matplotlib, Seaborn, NumPy

## Références complémentaires {#additional-references}

- [[django-rest-framework]] - patterns de sérialiseurs Django REST Framework, gestion des relations, validation et ORM avancé
- [[stdlib-patterns]] - structures de données de la bibliothèque standard Python et outils de programmation fonctionnelle - module collections
- [[web-scraping]] - patterns de web scraping avec BeautifulSoup - méthodes de recherche d'éléments, extraction de données, pagination, tableaux
