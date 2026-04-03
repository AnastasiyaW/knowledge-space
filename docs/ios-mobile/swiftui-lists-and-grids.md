---
title: SwiftUI Lists and Grids
category: concepts
tags: [ios-mobile, swiftui, list, foreach, lazyvgrid, scrollview, identifiable]
---

# SwiftUI Lists and Grids

List, ForEach, LazyVGrid, and ScrollView are the primary containers for displaying collections of data in SwiftUI. This entry covers dynamic lists, grid layouts, swipe-to-delete, and the differences between scrollable containers.

## Key Facts

- `List` displays scrollable rows with built-in separators and swipe-to-delete
- `ForEach` generates views from a collection but is not scrollable by itself
- Items in `ForEach`/`List` must conform to `Identifiable` or provide `id:` parameter
- `LazyVGrid` creates scrollable grid layouts with flexible or fixed columns
- `ScrollView` provides custom scrollable layout without List's built-in features
- Range syntax in `ForEach`: only half-open ranges (`0..<5`), not closed ranges (`0...4`)

## Patterns

### Static List

```swift
List {
    Text("Hello")
    Circle().frame(height: 40)
    Text("Hi")
}
```

### Dynamic List from Array

```swift
struct ContentView: View {
    var dogs = ["Fido", "Sarah", "Billy"]

    var body: some View {
        List(dogs, id: \.self) { dog in
            Text(dog)
        }
    }
}
```

`id: \.self` uses the value itself as identifier. Works for String, Int, etc.

### List with Identifiable Model

```swift
class JournalEntry: Identifiable {
    var id = UUID()
    var title: String
    var text: String
}

List(journalEntries) { entry in
    Text(entry.title)
}
```

`Identifiable` conformance provides auto-generated `id` property.

### ForEach Inside List (with onDelete)

```swift
List {
    ForEach(entries) { entry in
        Text(entry.title)
    }
    .onDelete { indices in
        entries.remove(atOffsets: indices)
    }
}
```

### ForEach Variants

```swift
// Range-based (underscore when not using index)
ForEach(0..<5) { _ in
    CurrencyIcon(currency: .copperPenny)
}

// Named index
ForEach(0..<5) { index in
    Text("Row \(index)")
}

// Collection-based with Identifiable
ForEach(journalEntries) { entry in
    Text(entry.title)
}

// Non-Identifiable with id parameter
ForEach(predator.movies, id: \.self) { movie in
    Text(movie)
}

// Enum cases
ForEach(Currency.allCases, id: \.self) { currency in
    CurrencyIcon(currency: currency)
}
```

### LazyVGrid

```swift
let columns = [GridItem(), GridItem(), GridItem()]   // 3 flexible columns

LazyVGrid(columns: columns) {
    ForEach(currencies, id: \.self) { currency in
        CurrencyIcon(currency: currency)
    }
}
.padding()
```

Column types:
- `GridItem()` - flexible (default), fills available space
- `GridItem(.fixed(100))` - fixed width
- Column count = number of `GridItem` in array

### ScrollView vs List

```swift
// List - built-in rows, separators, swipe-to-delete, selection
List(items) { item in Text(item.name) }

// ScrollView - custom layout, no separators
ScrollView {
    VStack {
        ForEach(items) { item in Text(item.name) }
    }
}
```

ScrollView content starts at top. Use ScrollView for full custom layout; use List for standard rows.

### ScrollViewReader (Programmatic Scrolling)

```swift
ScrollViewReader { proxy in
    ScrollView {
        ForEach(items) { item in
            Text(item.name).id(item.id)
        }
    }
    Button("Scroll to last") {
        proxy.scrollTo(items.last?.id, anchor: .bottom)
    }
}
```

### Sort, Filter, and Search Pattern

```swift
@Observable
class Predators {
    var apexPredators: [ApexPredator] = []
    var allApexPredators: [ApexPredator] = []   // master list, never modified

    func sortByName(alphabetical: Bool) {
        apexPredators.sort { pred1, pred2 in
            alphabetical ? pred1.name < pred2.name : pred1.id < pred2.id
        }
    }

    func filterBy(_ type: APType?) {
        if let type {
            apexPredators = allApexPredators.filter { $0.type == type }
        } else {
            apexPredators = allApexPredators
        }
    }

    func search(for text: String) -> [ApexPredator] {
        if text.isEmpty {
            return apexPredators
        } else {
            return apexPredators.filter {
                $0.name.localizedCaseInsensitiveContains(text)
            }
        }
    }
}
```

**Critical**: always filter from `allApexPredators` (master list), not from the already-filtered `apexPredators`. Otherwise, applying a second filter produces empty results.

### Animating List Changes

```swift
List { ... }
    .animation(.default, value: predators.apexPredators)
```

### List with Section Footer

```swift
List {
    Section {
        ForEach(pokedex) { pokemon in ... }
    } footer: {
        if pokedex.count < 151 {
            ContentUnavailableView { ... }
        }
    }
}
```

## Gotchas

- `ForEach` only accepts half-open ranges (`0..<5`), not closed ranges (`0...4`)
- `id: \.self` works when values are unique - duplicate values cause undefined behavior
- `List` automatically provides `Identifiable`-like behavior but still requires conformance on model types
- When filtering, always filter from the original master list, not from an already-filtered copy
- `LazyVGrid` renders cells lazily (only when visible) - good for performance with large datasets
- `ScrollView` fills all available space by default, unlike `VStack` which only takes needed space
- `.onDelete` only works with `ForEach` inside a `List`, not with `List(items)` directly

## See Also

- [[swiftui-navigation]] - NavigationLink inside List rows
- [[swiftui-views-and-modifiers]] - modifier reference for styling list content
- [[swiftui-forms-and-input]] - Form as a specialized list-like container
- [[swiftdata-persistence]] - @Query to populate lists from database
