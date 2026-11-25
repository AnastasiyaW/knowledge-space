---
title: "SwiftUI-Navigation"
category: concepts
tags: [ios-mobile, swiftui, navigation, navigationstack, sheets, tabview, toolbar]
level: 3
source_sha256: 9d11c26505bc796ddb98c50bef5b8d9649429e70dab7b61fc574416e3d3fda5e
translation: machine
translated_at: '2026-10-24'
---
# SwiftUI-Navigation {#swiftui-navigation}

SwiftUI bietet `NavigationStack` für hierarchische Push/Pop-Navigation, Sheets für modale Präsentation und `TabView` für tab-basierte Apps. Dieser Eintrag behandelt Navigationsmuster, Toolbars und Präsentationsabläufe.

## Wichtige Fakten {#key-facts}

- `NavigationStack` ermöglicht Push-Navigation mit automatischem Zurück-Button
- `NavigationLink` legt eine Zielansicht auf den Navigationsstack
- `.navigationTitle()` muss auf dem Inhalt **innerhalb** des Stacks platziert werden, nicht auf dem Stack selbst
- Sheets sind modale Overlays, die per Wischgeste oder programmatisch über `dismiss()` geschlossen werden
- `TabView` zeigt eine Tab-Leiste am unteren Rand; jeder Tab behält seinen eigenen Zustand bei
- `.toolbar` fügt Schaltflächen zur Navigationsleiste hinzu
- `@Environment(\.dismiss)` funktioniert sowohl zum Schließen von Sheets als auch zum Zurücknavigieren per Pop

## Muster {#patterns}

### NavigationStack mit NavigationLink {#navigationstack-with-navigationlink}

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

Navigationslinks zeigen automatisch Disclosure-Pfeile an.

### NavigationDestination (iOS 16+, bevorzugt) {#navigationdestination-ios-16-preferred}

Trennt den Link von seinem Ziel:

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

Bevorzugt gegenüber `NavigationLink(destination:)` bei Verwendung von `NavigationStack`.

### Sheet-Präsentation {#sheet-presentation}

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

Das Sheet kann auf jeder beliebigen Ansicht der Hierarchie platziert werden – es wird durch die `isPresented`-Bindung gesteuert, nicht durch die Ansicht, an der es angehängt ist.

### Sheet schließen oder Navigation zurücknavigieren {#dismiss-sheet-or-pop-navigation}

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

### Sheet vs. NavigationLink {#sheet-vs-navigationlink}

| Merkmal | NavigationLink | Sheet |
|---------|---------------|-------|
| Teil des Navigationsstacks | Ja | Nein |
| Zurück-Button | Automatisch | Keiner (Wischgeste oder dismiss()) |
| Animation | Push von rechts | Von unten nach oben einblenden |
| Anwendungsfall | Detailansicht in der Hierarchie | Erstellen/Bearbeiten von Formularen, Infos |

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

Fügt dem NavigationStack eine Suchleiste hinzu; die Bindung aktualisiert sich bei jeder Eingabe des Nutzers.

### Menü in der Toolbar (Filter-Picker) {#menu-in-toolbar-filter-picker}

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

### Zoom-Navigationsübergang (iOS 18+) {#zoom-navigation-transition-ios-18}

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

- `@Namespace` deklariert eine benannte Gruppe für verbundene Animationen
- `.navigationTransition(.zoom(...))` auf der Zielansicht
- `.matchedTransitionSource(id:in:)` auf dem NavigationLink (nicht auf dessen Label)

### ContentUnavailableView (Leerzustand) {#contentunavailableview-empty-state}

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

## Fallstricke {#gotchas}

- `.navigationTitle()` auf dem `NavigationStack` selbst hat keine Wirkung – es muss auf dem inneren Inhalt stehen
- Der Präsentationszustand des Sheets (`@State var show = false`) wird beim Schließen per Wischgeste auf `false` zurückgesetzt
- `NavigationLink` innerhalb einer `List` zeigt automatisch Disclosure-Pfeile an; außerhalb einer Liste nicht
- Ein verschachtelter `NavigationStack` innerhalb eines Sheets erzeugt eine eigene Navigationshierarchie – das ist korrekt so
- `.toolbarBackground(.visible)` ist nötig, wenn Inhalte hinter die Tab-Leiste reichen (Vollbild-Hintergründe)
- Bei Verwendung von `Picker` mit optionalen Enum-Typen wird der nil-/Alle-Fall mit `APType?.none` getaggt

## Siehe auch {#see-also}

- [[swiftui-state-and-data-flow]] - @State steuert Sheet- und Navigationspräsentation
- [[swiftui-lists-and-grids]] - List-Inhalte innerhalb des NavigationStack
- [[swiftui-forms-and-input]] - Formularbasierte Erstellen-/Bearbeiten-Ansichten in Sheets
- [[swiftui-animations]] - Navigationsübergänge und Zoom-Effekte
