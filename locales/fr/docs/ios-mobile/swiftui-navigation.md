---
title: "Navigation SwiftUI"
category: concepts
tags: [ios-mobile, swiftui, navigation, navigationstack, sheets, tabview, toolbar]
level: 3
source_sha256: 9d11c26505bc796ddb98c50bef5b8d9649429e70dab7b61fc574416e3d3fda5e
translation: machine
translated_at: '2026-10-24'
---
# Navigation SwiftUI {#swiftui-navigation}

SwiftUI fournit `NavigationStack` pour la navigation hiérarchique par empilement et dépilement (push/pop), les sheets pour la présentation modale et `TabView` pour les applications à onglets. Cette entrée couvre les patterns de navigation, les barres d'outils et les flux de présentation.

## Points clés {#key-facts}

- `NavigationStack` permet la navigation par empilement avec bouton de retour automatique
- `NavigationLink` empile une vue de destination sur la pile de navigation
- `.navigationTitle()` doit être placé sur le contenu **à l'intérieur** de la pile, et non sur la pile elle-même
- Les sheets sont des superpositions modales fermées par un balayage ou programmatiquement via `dismiss()`
- `TabView` affiche une barre d'onglets en bas de l'écran ; chaque onglet conserve un état indépendant
- `.toolbar` ajoute des boutons à la barre de navigation
- `@Environment(\.dismiss)` fonctionne à la fois pour fermer une sheet et pour revenir en arrière dans la navigation

## Patterns {#patterns}

### NavigationStack avec NavigationLink {#navigationstack-with-navigationlink}

```swift
NavigationStack {
    List(journalEntries) { entry in
        NavigationLink(destination: JournalDetailView(entry: entry)) {
            Text(entry.title)
        }
    }
    .navigationTitle("\(journalEntries.count) Journal Entries")
}
```

Les liens de navigation affichent automatiquement les chevrons de disclosure.

### NavigationDestination (iOS 16+, à privilégier) {#navigationdestination-ios-16-preferred}

Sépare le lien de sa destination :

```swift
List(pokedex) { pokemon in
    NavigationLink(value: pokemon) {
        PokemonRow(pokemon: pokemon)
    }
}
.navigationDestination(for: Pokemon.self) { pokemon in
    PokemonDetail(pokemon: pokemon)
}
```

À privilégier par rapport à `NavigationLink(destination:)` lorsqu'on utilise `NavigationStack`.

### Présentation en sheet {#sheet-presentation}

```swift
struct ContentView: View {
    @State var showCreateView = false

    var body: some View {
        NavigationStack {
            List { ... }
            .toolbar {
                Button {
                    showCreateView = true
                } label: {
                    Image(systemName: "plus")
                }
            }
            .sheet(isPresented: $showCreateView) {
                CreateEntryView()
            }
        }
    }
}
```

La sheet peut être placée sur n'importe quelle vue de la hiérarchie : elle est pilotée par le binding `isPresented`, et non par la vue à laquelle elle est attachée.

### Fermer la sheet ou revenir en arrière dans la navigation {#dismiss-sheet-or-pop-navigation}

```swift
struct CreateEntryView: View {
    @Environment(\.dismiss) var dismiss

    var body: some View {
        NavigationStack {
            Form { ... }
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        // save data
                        dismiss()    // closes sheet after save
                    }
                    .bold()
                }
            }
        }
    }
}
```

### Sheet ou NavigationLink {#sheet-vs-navigationlink}

| Caractéristique | NavigationLink | Sheet |
|---------|---------------|-------|
| Fait partie de la pile de navigation | Oui | Non |
| Bouton de retour | Automatique | Aucun (balayage ou dismiss()) |
| Animation | Glissement depuis la droite | Remontée depuis le bas |
| Cas d'usage | Détail en navigation hiérarchique | Formulaires de création/édition, informations |

### TabView {#tabview}

```swift
struct ContentView: View {
    var body: some View {
        TabView {
            QuoteView(show: "Breaking Bad")
                .tabItem {
                    Label("Breaking Bad", systemImage: "tortoise")
                }

            QuoteView(show: "Better Call Saul")
                .tabItem {
                    Label("Better Call Saul", systemImage: "briefcase")
                }
        }
        .toolbarBackground(.visible, for: .tabBar)
        .toolbarBackground(.black, for: .tabBar)
    }
}
```

### Toolbar {#toolbar}

```swift
.toolbar {
    ToolbarItem(placement: .navigationBarTrailing) {
        Button("Add") { ... }
    }
    ToolbarItem(placement: .navigationBarLeading) {
        EditButton()
    }
    ToolbarItem(placement: .topBarLeading) {
        Button { alphabetical.toggle() } label: {
            Image(systemName: alphabetical ? "film" : "textformat")
        }
    }
}
```

### .searchable {#searchable}

```swift
NavigationStack {
    List(filteredItems) { item in ... }
    .searchable(text: $searchText)
    .navigationTitle("Items")
}
```

Ajoute une barre de recherche à NavigationStack ; le binding se met à jour au fur et à mesure que l'utilisateur tape.

### Menu dans la toolbar (sélecteur de filtre) {#menu-in-toolbar-filter-picker}

```swift
ToolbarItem(placement: .topBarTrailing) {
    Menu {
        Picker("Filter", selection: $currentFilter) {
            Text("All").tag(APType?.none)
            ForEach(APType.allCases, id: \.self) { type in
                Text(type.rawValue.capitalized).tag(APType?.some(type))
            }
        }
    } label: {
        Image(systemName: "slider.horizontal.3")
    }
}
```

### Transition de navigation zoom (iOS 18+) {#zoom-navigation-transition-ios-18}

```swift
struct PredatorDetail: View {
    @Namespace var namespace

    var body: some View {
        NavigationLink {
            PredatorMap(position: position)
                .navigationTransition(.zoom(sourceID: 1, in: namespace))
        } label: {
            MapView(predator: predator)
        }
        .matchedTransitionSource(id: 1, in: namespace)
    }
}
```

- `@Namespace` déclare un groupe nommé pour les animations connectées
- `.navigationTransition(.zoom(...))` sur la vue de destination
- `.matchedTransitionSource(id:in:)` sur le NavigationLink (et non sur son label)

### ContentUnavailableView (état vide) {#contentunavailableview-empty-state}

```swift
if pokedex.isEmpty {
    ContentUnavailableView {
        Label("No Pokemon", image: .noPokemon)
    } description: {
        Text("There aren't any Pokemon yet.\nFetch some to get started.")
    } actions: {
        Button("Fetch Pokemon", systemImage: "antenna.radiowaves.left.and.right") {
            Task { await getPokemon(from: 1) }
        }
        .buttonStyle(.borderedProminent)
    }
}
```

## Pièges {#gotchas}

- `.navigationTitle()` placé sur le `NavigationStack` lui-même n'a aucun effet : il doit être sur le contenu interne
- L'état de présentation de la sheet (`@State var show = false`) revient à `false` lorsque la sheet est fermée par balayage
- Un `NavigationLink` dans une `List` affiche automatiquement les chevrons de disclosure ; en dehors d'une liste, ce n'est pas le cas
- Un `NavigationStack` imbriqué dans une sheet crée une hiérarchie de navigation distincte : c'est le comportement attendu
- `.toolbarBackground(.visible)` est nécessaire lorsque le contenu s'étend derrière la barre d'onglets (arrière-plans plein écran)
- Lorsqu'on utilise un `Picker` avec des types enum optionnels, étiqueter le cas nil/tout avec `APType?.none`

## Voir aussi {#see-also}

- [[swiftui-state-and-data-flow]] - @State pilote la présentation des sheets et de la navigation
- [[swiftui-lists-and-grids]] - contenu de List à l'intérieur d'un NavigationStack
- [[swiftui-forms-and-input]] - vues de création/édition basées sur des formulaires présentées dans des sheets
- [[swiftui-animations]] - transitions de navigation et effets de zoom
