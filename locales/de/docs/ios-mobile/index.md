---
title: "iOS & Mobile-Entwicklung"
type: MOC
level: 1
source_sha256: 9465ac5c0cff4e7cb0bc2de19549f2b5f1027ad9b3c84c295f41269cea678915
translation: machine
translated_at: '2026-10-24'
---
# iOS & Mobile-Entwicklung {#ios-mobile-development}

Referenz-Wissensdatenbank für die Entwicklung von iOS- und Android-Apps. Behandelt die Programmiersprache Swift, das SwiftUI-Framework, Persistenz (SwiftData + Core Data), Netzwerkkommunikation, Animationen, MapKit, StoreKit sowie die Android-Entwicklung mit Kotlin.

## Swift-Sprache {#swift-language}

- [[swift-fundamentals]] - Variablen, Typen, Funktionen, Arrays, Kontrollfluss, Extensions
- [[swift-structs-and-classes]] - Value- vs. Referenztypen, Protokolle, Methoden, berechnete Eigenschaften
- [[swift-enums-and-optionals]] - Enums mit Raw Values, Optionals, switch, Pattern Matching

## SwiftUI-Framework {#swiftui-framework}

- [[swiftui-views-and-modifiers]] - Views, Layout-Container, Modifier-Verkettung, Bilder, Buttons, GeometryReader
- [[swiftui-state-and-data-flow]] - @State, @Binding, @Observable, @Environment, @FocusState, onChange
- [[swiftui-navigation]] - NavigationStack, NavigationLink, Sheets, TabView, Toolbar, searchable
- [[swiftui-lists-and-grids]] - List, ForEach, LazyVGrid, ScrollView, Sortier-, Filter- und Suchmuster
- [[swiftui-forms-and-input]] - TextField, TextEditor, DatePicker, Slider, Form, Erstellen- und Bearbeiten-Muster
- [[swiftui-animations]] - withAnimation, Transitions, matchedGeometryEffect, @Namespace, Endlosschleifen

## Daten & Netzwerkkommunikation {#data-networking}

- [[swiftui-networking]] - async/await, URLSession, JSONDecoder, Codable, AsyncImage, Fetch-Services
- [[swiftdata-persistence]] - @Model, @Query, modelContainer, CRUD-Operationen (iOS 17+)
- [[core-data-persistence]] - NSManagedObject, @FetchRequest, NSPredicate, PersistenceController

## Apple-Frameworks {#apple-frameworks}

- [[mapkit-integration]] - Kartenansicht, Annotationen, MapCamera, Umschaltung zwischen Satellit und Standard
- [[storekit-in-app-purchases]] - StoreKit 2, Kaufablauf, Produktverwaltung, Berechtigungen (Entitlements)
- [[avkit-audio-and-haptics]] - AVAudioPlayer, Hintergrundmusik, Soundeffekte, haptisches Feedback

## Tooling {#tooling}

- [[xcode-project-setup]] - Projekterstellung, Previews, Dateiorganisation, Versionskontrolle

## Android (Kotlin) {#android-kotlin}

- [[kotlin-android-fundamentals]] - Kotlin-Grundlagen, Projektstruktur, Fragments, RecyclerView, Navigation
- [[android-mvvm-architecture]] - ViewModel, LiveData, Coroutines, Repository-Muster, Services
- [[android-room-database]] - Entity, DAO, Database-Singleton, LiveData-Abfragen
- [[android-retrofit-networking]] - REST-API-Schnittstellen, Gson, OkHttp, Annotationen
- [[android-dagger-dependency-injection]] - Module, Komponenten, @Provides, @Singleton, @Inject

## Weiterführende Referenzen {#additional-references}

- [[android-sparkle-filter]] - Implementierung von Echtzeit-Glitzer-/Funkeleffekten auf Kleidung in der Live-Kameravorschau unter Android
- [[graph-algorithms-swift]] - Graphen mit Adjazenzlisten, BFS/DFS-Traversierung und Algorithmen für kürzeste Pfade mit Kartenbeispielen
- [[refactoring-view-controllers]] - Systematische Zerlegung übergroßer View Controller in testbare Komponenten durch Extraktion
- [[swift-collections-beyond-arrays]] - Sets und Dictionaries in Swift mit Performance-Eigenschaften, Mengenoperationen und Zugriffsmustern
- [[swift-generics]] - Typsichere, wiederverwendbare Funktionen und Typen mit generischen Parametern, Constraints und assoziierten Typen
- [[swift-macros]] - Codegenerierung zur Compilezeit über attached und freestanding Macros mit AST-Transformation in Swift
- [[swift-phantom-types]] - Nur zur Compilezeit existierende Typparameter zur Durchsetzung von Zustandsautomaten, Einheitensicherheit und Domänenbeschränkungen
- [[swiftui-layout-testing]] - Property-based Fuzzing zur Verifikation eigener Layout-Engines gegen das native SwiftUI-Rendering von Apple
- [[type-safe-modeling]] - Enums, Structs und Generics, um unmögliche Zustände zu eliminieren und APIs selbstdokumentierend zu gestalten
- [[wrapping-c-libraries]] - Anbindung von C-Bibliotheken an Swift mit Typsicherheit, automatischer Speicherverwaltung über deinit und Fehlerbehandlung
