---
title: "iOS et développement mobile"
type: MOC
level: 1
source_sha256: 9465ac5c0cff4e7cb0bc2de19549f2b5f1027ad9b3c84c295f41269cea678915
translation: machine
translated_at: '2026-10-24'
---
# iOS et développement mobile {#ios-mobile-development}

Base de connaissances de référence pour le développement d'applications mobiles iOS et Android. Couvre le langage Swift, le framework SwiftUI, la persistance (SwiftData + Core Data), le réseau, les animations, MapKit, StoreKit et le développement Android avec Kotlin.

## Langage Swift {#swift-language}

- [[swift-fundamentals]] - Variables, types, fonctions, tableaux, structures de contrôle, extensions
- [[swift-structs-and-classes]] - Types valeur vs types référence, protocoles, méthodes, propriétés calculées
- [[swift-enums-and-optionals]] - Énumérations avec valeurs brutes, optionnels, switch, pattern matching

## Framework SwiftUI {#swiftui-framework}

- [[swiftui-views-and-modifiers]] - Vues, conteneurs de mise en page, chaînage de modificateurs, images, boutons, GeometryReader
- [[swiftui-state-and-data-flow]] - @State, @Binding, @Observable, @Environment, @FocusState, onChange
- [[swiftui-navigation]] - NavigationStack, NavigationLink, sheets, TabView, toolbar, searchable
- [[swiftui-lists-and-grids]] - List, ForEach, LazyVGrid, ScrollView, schémas de tri/filtrage/recherche
- [[swiftui-forms-and-input]] - TextField, TextEditor, DatePicker, Slider, Form, schémas de création/édition
- [[swiftui-animations]] - withAnimation, transitions, matchedGeometryEffect, @Namespace, animations en boucle

## Données et réseau {#data-networking}

- [[swiftui-networking]] - async/await, URLSession, JSONDecoder, Codable, AsyncImage, services de récupération de données
- [[swiftdata-persistence]] - @Model, @Query, modelContainer, opérations CRUD (iOS 17+)
- [[core-data-persistence]] - NSManagedObject, @FetchRequest, NSPredicate, PersistenceController

## Frameworks Apple {#apple-frameworks}

- [[mapkit-integration]] - Vue carte, annotations, MapCamera, bascule satellite/standard
- [[storekit-in-app-purchases]] - StoreKit 2, flux d'achat, gestion des produits, droits d'accès
- [[avkit-audio-and-haptics]] - AVAudioPlayer, musique de fond, effets sonores, retour haptique

## Outillage {#tooling}

- [[xcode-project-setup]] - Création de projet, aperçus, organisation des fichiers, gestion de versions

## Android (Kotlin) {#android-kotlin}

- [[kotlin-android-fundamentals]] - Bases de Kotlin, structure de projet, Fragments, RecyclerView, navigation
- [[android-mvvm-architecture]] - ViewModel, LiveData, coroutines, pattern Repository, Services
- [[android-room-database]] - Entity, DAO, singleton Database, requêtes LiveData
- [[android-retrofit-networking]] - Interfaces d'API REST, Gson, OkHttp, annotations
- [[android-dagger-dependency-injection]] - Modules, Components, @Provides, @Singleton, @Inject

## Références complémentaires {#additional-references}

- [[android-sparkle-filter]] - Implémentation d'effets de scintillement/paillettes en temps réel sur les vêtements dans un aperçu caméra en direct sous Android
- [[graph-algorithms-swift]] - Graphes à listes d'adjacence, parcours BFS/DFS et algorithmes de plus court chemin avec exemples de cartographie
- [[refactoring-view-controllers]] - Décomposition systématique de view controllers volumineux en composants testables par extraction
- [[swift-collections-beyond-arrays]] - Ensembles et dictionnaires en Swift, leurs caractéristiques de performance, opérations sur ensembles et modes d'accès
- [[swift-generics]] - Fonctions et types réutilisables et type-safe avec paramètres génériques, contraintes et types associés
- [[swift-macros]] - Génération de code à la compilation via des macros attachées et autonomes, reposant sur la transformation d'AST en Swift
- [[swift-phantom-types]] - Paramètres de type uniquement présents à la compilation, pour imposer des machines à états, la sécurité des unités et des contraintes métier
- [[swiftui-layout-testing]] - Fuzzing basé sur les propriétés pour vérifier des moteurs de mise en page personnalisés par rapport au rendu natif de SwiftUI d'Apple
- [[type-safe-modeling]] - Utilisation d'énumérations, de structs et de génériques pour éliminer les états impossibles et rendre les API auto-documentées
- [[wrapping-c-libraries]] - Interfaçage de fonctions C avec Swift en garantissant la sûreté de type, la gestion automatique de la mémoire via deinit, et la gestion des erreurs
