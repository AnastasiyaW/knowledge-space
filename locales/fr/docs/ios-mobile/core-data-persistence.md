---
title: "Persistance des données avec Core Data"
category: concepts
tags: [ios-mobile, swiftui, core-data, persistence, fetchrequest, nspredicate, nsmanagedobject]
level: 3
source_sha256: 7b17c53e8186655012604f8d1fb668d813d76c67b6d0aceb90230052ab7bb626
translation: machine
translated_at: '2026-10-24'
---
# Persistance des données avec Core Data {#core-data-persistence}

Core Data est le framework de persistance mature d'Apple, disponible sur toutes les versions d'iOS. Bien que SwiftData (iOS 17+) soit plus simple, Core Data reste nécessaire pour les applications qui prennent en charge iOS 16 et les versions antérieures. Cette entrée couvre l'ensemble de la pile Core Data avec l'intégration SwiftUI.

## Points clés {#key-facts}

- Core Data utilise des sous-classes de `NSManagedObject` générées automatiquement à partir des fichiers `.xcdatamodeld`
- `@FetchRequest` dans les vues remplace les appels de récupération manuels : les mises à jour se font automatiquement lorsque les données changent
- `NSPredicate` gère le filtrage avec des chaînes de format (insensible à la casse, prédicats composés)
- `viewContext.save()` doit être appelé explicitement après chaque modification
- Le magasin en mémoire (URL `/dev/null`) est utilisé pour les aperçus
- Les extensions de `NSManagedObject` ajoutent des propriétés calculées sans modifier le code généré automatiquement
- Le motif singleton `PersistenceController` gère la pile Core Data

## Motifs {#patterns}

### Configuration du projet {#project-setup}

1. Nouveau projet > cocher « Use Core Data »
2. Générés : `Persistence.swift` + `YourApp.xcdatamodeld`
3. Dans `.xcdatamodeld` : ajouter une Entity, ajouter des Attributes (nom, type)
4. Xcode génère automatiquement les sous-classes NSManagedObject lors de la compilation

### Pile Core Data (Persistence.swift) {#core-data-stack-persistenceswift}

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

### Point d'entrée de l'application {#app-entry-point}

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

### @FetchRequest dans les vues {#fetchrequest-in-views}

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

### @FetchRequest avec prédicat statique {#fetchrequest-with-static-predicate}

```swift
@FetchRequest<Pokemon>(
    sortDescriptors: [SortDescriptor(\Pokemon.id)],
    predicate: NSPredicate(format: "favorite == true")
) private var favorites: FetchedResults<Pokemon>
```

### Prédicat dynamique (motif onChange) {#dynamic-predicate-onchange-pattern}

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

`pokedex.nsPredicate = newPredicate` met à jour la requête de récupération en direct.

### Chaînes de format NSPredicate {#nspredicate-format-strings}

| Format | Utilisation |
|--------|-------------|
| `"name CONTAINS[c] %@"` | Contient, insensible à la casse (chaîne) |
| `"favorite == %d"` | Comparaison booléenne/entière |
| `"id == %d"` | Correspondance exacte |
| `NSCompoundPredicate(andPredicateWithSubpredicates:)` | Combiner plusieurs prédicats |

### Opérations CRUD {#crud-operations}

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

### Récupération d'un objet unique (pour les aperçus) {#fetching-a-single-object-for-previews}

```swift
func fetchPokemon(id: Int, context: NSManagedObjectContext) -> Pokemon {
    let fetchRequest: NSFetchRequest<Pokemon> = Pokemon.fetchRequest()
    fetchRequest.fetchLimit = 1
    fetchRequest.predicate = NSPredicate(format: "id == %d", id)
    let results = try! context.fetch(fetchRequest)
    return results.first!
}
```

### Étendre les sous-classes NSManagedObject {#extending-nsmanagedobject-subclasses}

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

Règle : pas de propriétés stockées dans les extensions, uniquement des propriétés calculées et des fonctions.

### Swift Charts avec Core Data {#swift-charts-with-core-data}

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

### NavigationDestination avec Core Data {#navigationdestination-with-core-data}

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

## Pièges à éviter {#gotchas}

- Les modifications Core Data ne sont PAS persistées tant que `viewContext.save()` n'est pas appelé : oublier cet appel entraîne une perte de données
- Les propriétés générées automatiquement des NSManagedObject sont des optionnels (`name: String?`) : les gérer avec l'opérateur de coalescence nulle (`??`)
- `fallbackToDestructiveMigration()` supprime toutes les données lors d'un changement de schéma : en production, utiliser `addMigrations()` avec ALTER TABLE
- `automaticallyMergesChangesFromParent = true` est nécessaire pour que les modifications des contextes en arrière-plan apparaissent dans l'interface
- Les chaînes de format NSPredicate ne sont pas typées : les erreurs de format provoquent des plantages à l'exécution
- Lors de la récupération depuis une API et du stockage dans Core Data, vérifier l'existence de doublons avant l'insertion

## Voir aussi {#see-also}

- [[swiftdata-persistence]] - alternative moderne pour iOS 17+
- [[swiftui-networking]] - récupération de données distantes à stocker dans Core Data
- [[swiftui-lists-and-grids]] - affichage des résultats récupérés dans des listes
- [[swiftui-forms-and-input]] - formulaires de création/modification avec Core Data
