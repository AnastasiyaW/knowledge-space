---
title: "Java et Spring"
type: MOC
level: 2
source_sha256: 23831c844d9dfeb03fe0e840aabcb561c395ca3e4b8e53d808a04bd84afe4b0e
translation: machine
translated_at: '2026-10-24'
---
# Java et Spring {#java-spring}

## Langage Java et Kotlin {#java-kotlin-language}
- [[java-type-system-fundamentals]] - Types primitifs, chaînes, génériques, exceptions, BigDecimal
- [[kotlin-language-features]] - Sécurité des nulls, data/sealed classes, fonctions d'extension, syntaxe d'expression
- [[java-collections-streams]] - Hiérarchie des collections, API Stream, fonctions de collection Kotlin
- [[java-concurrency]] - Threads, synchronisation, ExecutorService, CompletableFuture
- [[algorithms-data-structures]] - Tri, recherche, arbres, Big O, schémas d'entretien

## Spring Framework {#spring-framework}
- [[spring-ioc-beans]] - Conteneur IoC, injection de dépendances, portées des beans, cycle de vie, beans conditionnels
- [[spring-boot-configuration]] - Initialisation du projet, propriétés de l'application, couches de l'architecture propre
- [[spring-mvc-rest]] - Contrôleurs, templates Thymeleaf, i18n, portée de session
- [[spring-validation]] - Annotations de validation des DTO, BindingResult, affichage des erreurs
- [[spring-security]] - BCrypt, SecurityFilterChain, accès basé sur les rôles, authentification par session

## Spring Data & Persistance {#spring-data-persistence}
- [[spring-data-access-evolution]] - JDBC -> JdbcTemplate -> NamedParameter -> JOOQ -> CrudRepository
- [[spring-data-jpa-hibernate]] - Entités JPA, relations, héritage, transactions, mise en cache
- [[database-migrations]] - Flyway (basé sur SQL) et Liquibase (multi-format) pour la gestion du schéma
- [[spring-nosql-databases]] - Cassandra, MongoDB, Redis, Neo4j avec Spring Data

## Développement Android {#android-development}
- [[android-fundamentals-ui]] - Structure du projet, layouts XML, Views, ViewGroups
- [[android-activity-lifecycle]] - Cycle de vie des Activity, Intents, navigation entre écrans
- [[android-recyclerview]] - RecyclerView, Adapter/ViewHolder, DiffUtil, vues personnalisées
- [[android-fragments-navigation]] - Fragments, Navigation Component, Safe Args, View Binding
- [[android-architecture-mvvm]] - MVP vs MVVM, ViewModel, LiveData, pattern Repository
- [[android-data-storage]] - SharedPreferences, SQLite, ORM Room, Content Providers
- [[android-networking-retrofit]] - Retrofit, OkHttp, Gson, pagination, chargement d'images
- [[android-jetpack-compose]] - UI déclarative, gestion de l'état, LazyColumn, navigation Compose
- [[kotlin-coroutines]] - Fonctions suspend, Flow, StateFlow, Dispatchers, concurrence structurée
- [[android-firebase]] - Firebase Auth, Cloud Firestore, Cloud Storage, écouteurs en temps réel
- [[android-dependency-injection]] - Framework Hilt DI, modules, scopes, parallèles avec Spring IoC
