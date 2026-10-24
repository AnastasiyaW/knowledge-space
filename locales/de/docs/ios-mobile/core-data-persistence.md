---
title: "Core Data Persistenz"
category: concepts
tags: [ios-mobile, swiftui, core-data, persistence, fetchrequest, nspredicate, nsmanagedobject]
level: 3
source_sha256: 7b17c53e8186655012604f8d1fb668d813d76c67b6d0aceb90230052ab7bb626
translation: machine
translated_at: '2026-10-24'
---
# Core Data Persistenz {#core-data-persistence}

Core Data ist Apples ausgereiftes Persistenz-Framework und auf allen iOS-Versionen verfügbar. SwiftData (iOS 17+) ist zwar einfacher, Core Data bleibt aber für Apps notwendig, die iOS 16 und älter unterstützen. Dieser Eintrag behandelt den vollständigen Core-Data-Stack mit SwiftUI-Integration.

## Wichtige Fakten {#key-facts}

- Core Data verwendet `NSManagedObject`-Unterklassen, die aus `.xcdatamodeld`-Dateien automatisch generiert werden
- `@FetchRequest` in Views ersetzt manuelle Fetch-Aufrufe und aktualisiert sich automatisch, wenn sich Daten ändern
- `NSPredicate` übernimmt die Filterung mit Format-Strings (groß-/kleinschreibungsunabhängig, zusammengesetzte Prädikate)
- `viewContext.save()` muss nach jeder Änderung explizit aufgerufen werden
- Der In-Memory-Store (`/dev/null`-URL) wird für Previews verwendet
- Erweiterungen von `NSManagedObject` fügen berechnete Eigenschaften hinzu, ohne den automatisch generierten Code zu verändern
- Das `PersistenceController`-Singleton-Muster verwaltet den Core-Data-Stack

## Muster {#patterns}

### Projekt-Setup {#project-setup}

1. Neues Projekt > "Use Core Data" aktivieren
2. Generiert: `Persistence.swift` + `YourApp.xcdatamodeld`
3. In der `.xcdatamodeld`: Entity hinzufügen, Attribute hinzufügen (Name, Typ)
4. Xcode generiert die NSManagedObject-Unterklassen beim Build automatisch

### Core-Data-Stack (Persistence.swift) {#core-data-stack-persistenceswift}

```swift
struct PersistenceController {
    static let shared = PersistenceController()

    static var preview: PersistenceController = {
        let result = PersistenceController(inMemory: true)
        let viewContext = result.container.viewContext
        let samplePokemon = Pokemon(context: viewContext)
        samplePokemon.id = 1
        samplePokemon.name = "bulbasaur"
        try? viewContext.save()
        return result
    }()

    let container: NSPersistentContainer

    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "Pokedex")
        if inMemory {
            container.persistentStoreDescriptions.first!.url =
                URL(fileURLWithPath: "/dev/null")
        }
        container.loadPersistentStores { _, error in
            if let error { fatalError("Core Data error: \(error)") }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
    }
}
```

### App-Einstiegspunkt {#app-entry-point}

```swift
@main
struct PokedexApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext,
                    persistenceController.container.viewContext)
        }
    }
}
```

### @FetchRequest in Views {#fetchrequest-in-views}

```swift
struct ContentView: View {
    @Environment(\.managedObjectContext) private var viewContext

    @FetchRequest<Pokemon>(
        sortDescriptors: [SortDescriptor(\Pokemon.id)],
        animation: .default
    ) private var pokedex: FetchedResults<Pokemon>

    var body: some View {
        List(pokedex) { pokemon in
            Text(pokemon.name ?? "Unknown")
        }
    }
}
```

### @FetchRequest mit statischem Prädikat {#fetchrequest-with-static-predicate}

```swift
@FetchRequest<Pokemon>(
    sortDescriptors: [SortDescriptor(\Pokemon.id)],
    predicate: NSPredicate(format: "favorite == true")
) private var favorites: FetchedResults<Pokemon>
```

### Dynamisches Prädikat (onChange-Muster) {#dynamic-predicate-onchange-pattern}

```swift
@FetchRequest<Pokemon>(sortDescriptors: [SortDescriptor(\Pokemon.id)])
private var pokedex: FetchedResults<Pokemon>

private var dynamicPredicate: NSPredicate {
    var predicates: [NSPredicate] = []

    if !searchText.isEmpty {
        predicates.append(
            NSPredicate(format: "name CONTAINS[c] %@", searchText)
        )
    }
    if filterByFavorites {
        predicates.append(
            NSPredicate(format: "favorite == %d", true)
        )
    }

    return NSCompoundPredicate(andPredicateWithSubpredicates: predicates)
}

var body: some View {
    List(pokedex) { ... }
    .searchable(text: $searchText)
    .onChange(of: searchText) { pokedex.nsPredicate = dynamicPredicate }
    .onChange(of: filterByFavorites) { pokedex.nsPredicate = dynamicPredicate }
}
```

`pokedex.nsPredicate = newPredicate` aktualisiert den Fetch-Request live.

### NSPredicate-Format-Strings {#nspredicate-format-strings}

| Format | Zweck |
|--------|---------|
| `"name CONTAINS[c] %@"` | Enthält-Prüfung ohne Berücksichtigung der Groß-/Kleinschreibung (String) |
| `"favorite == %d"` | Vergleich für Boolean/Int |
| `"id == %d"` | Exakte Übereinstimmung |
| `NSCompoundPredicate(andPredicateWithSubpredicates:)` | Mehrere Prädikate kombinieren |

### CRUD-Operationen {#crud-operations}

```swift
// Create
let newPokemon = Pokemon(context: viewContext)
newPokemon.id = 1
newPokemon.name = "bulbasaur"

// Save (required after every change)
do {
    try viewContext.save()
} catch {
    print("Save error: \(error)")
}

// Update
pokemon.favorite.toggle()
try? viewContext.save()

// Delete
viewContext.delete(pokemon)
try? viewContext.save()
```

### Abruf eines einzelnen Objekts (für Previews) {#fetching-a-single-object-for-previews}

```swift
func fetchPokemon(id: Int, context: NSManagedObjectContext) -> Pokemon {
    let fetchRequest: NSFetchRequest<Pokemon> = Pokemon.fetchRequest()
    fetchRequest.fetchLimit = 1
    fetchRequest.predicate = NSPredicate(format: "id == %d", id)
    let results = try! context.fetch(fetchRequest)
    return results.first!
}
```

### NSManagedObject-Unterklassen erweitern {#extending-nsmanagedobject-subclasses}

```swift
extension Pokemon {
    var background: ImageResource {
        switch types?.first ?? "" {
        case "fire", "dragon": return .fireDragon
        case "water": return .water
        default: return .normalGrassElectricPoisonFairy
        }
    }

    var typeColor: Color {
        Color((types?.first ?? "normal").capitalized)
    }

    var stats: [Stat] {
        [
            Stat(id: 1, name: "HP", value: hp),
            Stat(id: 2, name: "Attack", value: attack),
            // ...
        ]
    }
}
```

Regel: keine gespeicherten Eigenschaften in Erweiterungen, nur berechnete Eigenschaften und Funktionen.

### Swift Charts mit Core Data {#swift-charts-with-core-data}

```swift
import Charts

Chart(pokemon.stats) { stat in
    BarMark(
        x: .value("Value", stat.value),
        y: .value("Stat", stat.name)
    )
    .annotation(position: .trailing) {
        Text("\(stat.value)")
    }
}
.frame(height: 200)
.foregroundStyle(pokemon.typeColor)
.chartXScale(domain: 0...(pokemon.highestStat.value + 10))
```

### NavigationDestination mit Core Data {#navigationdestination-with-core-data}

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

## Stolperfallen {#gotchas}

- Core-Data-Änderungen werden erst mit `viewContext.save()` persistiert. Wer den Aufruf vergisst, verliert Daten.
- Automatisch generierte NSManagedObject-Eigenschaften sind Optionals (`name: String?`) und sollten mit dem Nil-Coalescing-Operator behandelt werden.
- `fallbackToDestructiveMigration()` löscht bei einer Schemaänderung alle Daten. Für Produktivsysteme sollte stattdessen `addMigrations()` mit ALTER TABLE verwendet werden.
- `automaticallyMergesChangesFromParent = true` ist nötig, damit Änderungen aus Hintergrundkontexten in der UI erscheinen.
- NSPredicate-Format-Strings sind nicht typsicher. Formatfehler führen zur Laufzeit zu Abstürzen.
- Beim Abrufen von einer API und Speichern in Core Data sollte vor dem Einfügen auf Duplikate geprüft werden.

## Siehe auch {#see-also}

- [[swiftdata-persistence]] - moderne Alternative für iOS 17+
- [[swiftui-networking]] - Abruf entfernter Daten zur Speicherung in Core Data
- [[swiftui-lists-and-grids]] - Anzeige abgerufener Ergebnisse in Listen
- [[swiftui-forms-and-input]] - Erstellen- und Bearbeiten-Formulare mit Core Data
