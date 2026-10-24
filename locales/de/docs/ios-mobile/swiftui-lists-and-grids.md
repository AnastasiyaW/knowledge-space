---
title: "SwiftUI-Listen und Raster"
category: concepts
tags: [ios-mobile, swiftui, list, foreach, lazyvgrid, scrollview, identifiable]
level: 3
source_sha256: 3f10656a019b46b0df2f609e5202e62159c8f0761ccf8b8bc3379df2788614fd
translation: machine
translated_at: '2026-10-24'
---
# SwiftUI-Listen und Raster {#swiftui-lists-and-grids}

List, ForEach, LazyVGrid und ScrollView sind die wichtigsten Container zur Darstellung von Datensammlungen in SwiftUI. Dieser Eintrag behandelt dynamische Listen, Rasterlayouts, Wischen-zum-Löschen sowie die Unterschiede zwischen scrollbaren Containern.

## Wichtige Fakten {#key-facts}

- `List` zeigt scrollbare Zeilen mit integrierten Trennlinien und Wischen-zum-Löschen
- `ForEach` erzeugt Views aus einer Sammlung, ist aber allein nicht scrollbar
- Elemente in `ForEach`/`List` müssen `Identifiable` entsprechen oder einen `id:`-Parameter bereitstellen
- `LazyVGrid` erzeugt scrollbare Rasterlayouts mit flexiblen oder festen Spalten
- `ScrollView` bietet ein benutzerdefiniertes scrollbares Layout ohne die integrierten Funktionen von List
- Bereichssyntax in `ForEach`: nur halboffene Bereiche (`0..<5`), keine geschlossenen Bereiche (`0...4`)

## Muster {#patterns}

### Statische Liste {#static-list}

```swift
List {
    Text("Hello")
    Circle().frame(height: 40)
    Text("Hi")
}
```

### Dynamische Liste aus einem Array {#dynamic-list-from-array}

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

`id: \.self` verwendet den Wert selbst als Identifier. Funktioniert für String, Int usw.

### Liste mit Identifiable-Modell {#list-with-identifiable-model}

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

Die Konformität zu `Identifiable` stellt eine automatisch generierte `id`-Eigenschaft bereit.

### ForEach innerhalb von List (mit onDelete) {#foreach-inside-list-with-ondelete}

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

### ForEach-Varianten {#foreach-variants}

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

### LazyVGrid {#lazyvgrid}

```swift
let columns = [GridItem(), GridItem(), GridItem()]   // 3 flexible columns

LazyVGrid(columns: columns) {
    ForEach(currencies, id: \.self) { currency in
        CurrencyIcon(currency: currency)
    }
}
.padding()
```

Spaltentypen:
- `GridItem()` - flexibel (Standard), füllt den verfügbaren Platz
- `GridItem(.fixed(100))` - feste Breite
- Spaltenanzahl = Anzahl der `GridItem` im Array

### ScrollView vs. List {#scrollview-vs-list}

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

Der Inhalt einer ScrollView beginnt oben. Verwende ScrollView für vollständig benutzerdefinierte Layouts; verwende List für Standardzeilen.

### ScrollViewReader (programmatisches Scrollen) {#scrollviewreader-programmatic-scrolling}

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

### Muster für Sortieren, Filtern und Suchen {#sort-filter-and-search-pattern}

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

**Kritisch**: Filtere immer aus `allApexPredators` (der Hauptliste) und nicht aus der bereits gefilterten `apexPredators`. Andernfalls liefert das Anwenden eines zweiten Filters leere Ergebnisse.

### Animieren von Listenänderungen {#animating-list-changes}

```swift
List { ... }
    .animation(.default, value: predators.apexPredators)
```

### Liste mit Section-Footer {#list-with-section-footer}

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

## Fallstricke {#gotchas}

- `ForEach` akzeptiert nur halboffene Bereiche (`0..<5`), keine geschlossenen Bereiche (`0...4`)
- `id: \.self` funktioniert, wenn die Werte eindeutig sind; doppelte Werte führen zu undefiniertem Verhalten
- `List` bietet automatisch ein `Identifiable`-ähnliches Verhalten, verlangt aber dennoch die Konformität bei Modelltypen
- Beim Filtern immer aus der ursprünglichen Hauptliste filtern, nicht aus einer bereits gefilterten Kopie
- `LazyVGrid` rendert Zellen verzögert (nur wenn sichtbar) – gut für die Performance bei großen Datenmengen
- `ScrollView` füllt standardmäßig den gesamten verfügbaren Platz, anders als `VStack`, der nur den benötigten Platz einnimmt
- `.onDelete` funktioniert nur mit `ForEach` innerhalb einer `List`, nicht direkt mit `List(items)`

## Siehe auch {#see-also}

- [[swiftui-navigation]] - NavigationLink innerhalb von List-Zeilen
- [[swiftui-views-and-modifiers]] - Modifier-Referenz für die Gestaltung von Listeninhalten
- [[swiftui-forms-and-input]] - Form als spezialisierter listenähnlicher Container
- [[swiftdata-persistence]] - @Query zum Befüllen von Listen aus der Datenbank
