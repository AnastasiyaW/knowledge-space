---
title: Core Data Persistence
category: concepts
tags: [ios-mobile, swiftui, core-data, persistence, fetchrequest, nspredicate, nsmanagedobject]
---

# Core Data Persistence

Core Data is Apple's mature persistence framework, available on all iOS versions. While SwiftData (iOS 17+) is simpler, Core Data remains necessary for apps supporting iOS 16 and below. This entry covers the full Core Data stack with SwiftUI integration.

## Key Facts

- Core Data uses `NSManagedObject` subclasses auto-generated from `.xcdatamodeld` files
- `@FetchRequest` in views replaces manual fetch calls - updates automatically when data changes
- `NSPredicate` handles filtering with format strings (case-insensitive, compound predicates)
- `viewContext.save()` must be called explicitly after every change
- In-memory store (`/dev/null` URL) is used for previews
- Extensions on `NSManagedObject` add computed properties without modifying auto-generated code
- `PersistenceController` singleton pattern manages the Core Data stack

## Patterns

### Project Setup

1. New project > Check "Use Core Data"
2. Generated: `Persistence.swift` + `YourApp.xcdatamodeld`
3. In `.xcdatamodeld`: add Entity, add Attributes (name, type)
4. Xcode auto-generates NSManagedObject subclasses on build

### Core Data Stack (Persistence.swift)

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

### App Entry Point

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

### @FetchRequest in Views

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

### @FetchRequest with Static Predicate

```swift
@FetchRequest<Pokemon>(
    sortDescriptors: [SortDescriptor(\Pokemon.id)],
    predicate: NSPredicate(format: "favorite == true")
) private var favorites: FetchedResults<Pokemon>
```

### Dynamic Predicate (onChange Pattern)

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

`pokedex.nsPredicate = newPredicate` updates the fetch request live.

### NSPredicate Format Strings

| Format | Purpose |
|--------|---------|
| `"name CONTAINS[c] %@"` | Case-insensitive contains (string) |
| `"favorite == %d"` | Boolean/int comparison |
| `"id == %d"` | Exact match |
| `NSCompoundPredicate(andPredicateWithSubpredicates:)` | Combine multiple |

### CRUD Operations

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

### Fetching a Single Object (for Previews)

```swift
func fetchPokemon(id: Int, context: NSManagedObjectContext) -> Pokemon {
    let fetchRequest: NSFetchRequest<Pokemon> = Pokemon.fetchRequest()
    fetchRequest.fetchLimit = 1
    fetchRequest.predicate = NSPredicate(format: "id == %d", id)
    let results = try! context.fetch(fetchRequest)
    return results.first!
}
```

### Extending NSManagedObject Subclasses

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

Rule: no stored properties in extensions - only computed properties and functions.

### Swift Charts with Core Data

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

### NavigationDestination with Core Data

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

## Gotchas

- Core Data changes are NOT persisted until `viewContext.save()` is called - forgetting this loses data
- Auto-generated NSManagedObject properties are optionals (`name: String?`) - handle with nil coalescing
- `fallbackToDestructiveMigration()` deletes all data on schema change - for production, use `addMigrations()` with ALTER TABLE
- `automaticallyMergesChangesFromParent = true` is needed for background context changes to appear in UI
- NSPredicate format strings are not type-safe - runtime crashes on format errors
- When fetching from API and storing in Core Data, check for duplicates before inserting

## See Also

- [[swiftdata-persistence]] - modern alternative for iOS 17+
- [[swiftui-networking]] - fetching remote data to store in Core Data
- [[swiftui-lists-and-grids]] - displaying fetched results in lists
- [[swiftui-forms-and-input]] - create/edit forms with Core Data
