---
title: iOS & Mobile Development
type: MOC
---

# iOS & Mobile Development

Reference knowledge base for iOS and Android mobile app development. Covers Swift language, SwiftUI framework, persistence (SwiftData + Core Data), networking, animations, MapKit, StoreKit, and Android development with Kotlin.

## Swift Language

- [[swift-fundamentals]] - Variables, types, functions, arrays, control flow, extensions
- [[swift-structs-and-classes]] - Value vs reference types, protocols, methods, computed properties
- [[swift-enums-and-optionals]] - Enums with raw values, optionals, switch, pattern matching

## SwiftUI Framework

- [[swiftui-views-and-modifiers]] - Views, layout containers, modifier chaining, images, buttons, GeometryReader
- [[swiftui-state-and-data-flow]] - @State, @Binding, @Observable, @Environment, @FocusState, onChange
- [[swiftui-navigation]] - NavigationStack, NavigationLink, sheets, TabView, toolbar, searchable
- [[swiftui-lists-and-grids]] - List, ForEach, LazyVGrid, ScrollView, sort/filter/search patterns
- [[swiftui-forms-and-input]] - TextField, TextEditor, DatePicker, Slider, Form, create/edit patterns
- [[swiftui-animations]] - withAnimation, transitions, matchedGeometryEffect, @Namespace, looping

## Data & Networking

- [[swiftui-networking]] - async/await, URLSession, JSONDecoder, Codable, AsyncImage, fetch services
- [[swiftdata-persistence]] - @Model, @Query, modelContainer, CRUD operations (iOS 17+)
- [[core-data-persistence]] - NSManagedObject, @FetchRequest, NSPredicate, PersistenceController

## Apple Frameworks

- [[mapkit-integration]] - Map view, annotations, MapCamera, satellite/standard toggle
- [[storekit-in-app-purchases]] - StoreKit 2, purchase flow, product management, entitlements
- [[avkit-audio-and-haptics]] - AVAudioPlayer, background music, sound effects, haptic feedback

## Tooling

- [[xcode-project-setup]] - Project creation, previews, file organization, version control

## Android (Kotlin)

- [[kotlin-android-fundamentals]] - Kotlin basics, project structure, Fragments, RecyclerView, navigation
- [[android-mvvm-architecture]] - ViewModel, LiveData, coroutines, Repository pattern, Services
- [[android-room-database]] - Entity, DAO, Database singleton, LiveData queries
- [[android-retrofit-networking]] - REST API interfaces, Gson, OkHttp, annotations
- [[android-dagger-dependency-injection]] - Modules, Components, @Provides, @Singleton, @Inject

## Additional References

- [[android-sparkle-filter]] - Implementing realtime sparkle/glitter effects on clothing in live camera preview on Android
- [[graph-algorithms-swift]] - Adjacency list graphs, BFS/DFS traversal, and shortest path algorithms with mapping examples
- [[refactoring-view-controllers]] - Systematic decomposition of massive view controllers into testable components using extraction
- [[swift-collections-beyond-arrays]] - Sets and Dictionaries in Swift with performance characteristics, set operations, and access patterns
- [[swift-generics]] - Type-safe reusable functions and types with generic parameters, constraints, and associated types
- [[swift-macros]] - Compile-time code generation via attached and freestanding macros using AST transformation in Swift
- [[swift-phantom-types]] - Compile-time-only type parameters for enforcing state machines, unit safety, and domain constraints
- [[swiftui-layout-testing]] - Property-based fuzzing to verify custom layout engines against Apple's native SwiftUI rendering
- [[type-safe-modeling]] - Using enums, structs, and generics to eliminate impossible states and make APIs self-documenting
- [[wrapping-c-libraries]] - Bridging C functions into Swift with type safety, automatic memory management via deinit, and error
