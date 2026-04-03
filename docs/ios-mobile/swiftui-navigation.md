---
title: SwiftUI Navigation
category: concepts
tags: [ios-mobile, swiftui, navigation, navigationstack, sheets, tabview, toolbar]
---

# SwiftUI Navigation

SwiftUI provides NavigationStack for hierarchical push/pop navigation, sheets for modal presentation, and TabView for tab-based apps. This entry covers navigation patterns, toolbars, and presentation flows.

## Key Facts

- `NavigationStack` enables push navigation with automatic back button
- `NavigationLink` pushes a destination view onto the navigation stack
- `.navigationTitle()` must be on content **inside** the stack, not on the stack itself
- Sheets are modal overlays dismissed by swipe or programmatically via `dismiss()`
- `TabView` shows a tab bar at bottom; each tab maintains independent state
- `.toolbar` adds buttons to the navigation bar
- `@Environment(\.dismiss)` works for both sheet dismiss and navigation pop-back

## Patterns

### NavigationStack with NavigationLink

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

Navigation links show disclosure arrows automatically.

### NavigationDestination (iOS 16+, preferred)

Separates the link from its destination:

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

Preferred over `NavigationLink(destination:)` when using `NavigationStack`.

### Sheet Presentation

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

Sheet can be placed on any view in the hierarchy - it is powered by the `isPresented` binding, not the view it is attached to.

### Dismiss Sheet or Pop Navigation

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

### Sheet vs NavigationLink

| Feature | NavigationLink | Sheet |
|---------|---------------|-------|
| Part of nav stack | Yes | No |
| Back button | Automatic | None (swipe or dismiss()) |
| Animation | Push from right | Slide up from bottom |
| Use case | Drill-down detail | Create/edit forms, info |

### TabView

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

### Toolbar

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

### .searchable

```swift
NavigationStack {
    List(filteredItems) { item in ... }
    .searchable(text: $searchText)
    .navigationTitle("Items")
}
```

Adds a search bar to NavigationStack; binding updates as user types.

### Menu in Toolbar (Filter Picker)

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

### Zoom Navigation Transition (iOS 18+)

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

- `@Namespace` declares a named group for connected animations
- `.navigationTransition(.zoom(...))` on the destination view
- `.matchedTransitionSource(id:in:)` on the NavigationLink (not its label)

### ContentUnavailableView (Empty State)

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

## Gotchas

- `.navigationTitle()` placed on the `NavigationStack` itself has no effect - must be on inner content
- Sheet presentation state (`@State var show = false`) resets to `false` when the sheet is dismissed via swipe
- `NavigationLink` inside a `List` automatically renders disclosure arrows; outside a list it does not
- Nested `NavigationStack` inside a sheet creates a separate navigation hierarchy - this is correct
- `.toolbarBackground(.visible)` is needed when content extends behind the tab bar (full-screen backgrounds)
- When using `Picker` with optional enum types, tag with `APType?.none` for the nil/all case

## See Also

- [[swiftui-state-and-data-flow]] - @State drives sheet and navigation presentation
- [[swiftui-lists-and-grids]] - List content inside NavigationStack
- [[swiftui-forms-and-input]] - Form-based create/edit views presented in sheets
- [[swiftui-animations]] - navigation transitions and zoom effects
