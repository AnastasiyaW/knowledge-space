---
title: "Persistance avec SwiftData"
category: concepts
tags: [ios-mobile, swiftui, swiftdata, persistence, model, query, database]
level: 3
source_sha256: 540790694eca27502ff1dbfcadaf43b19fc77535314ffd59c5e2e714c2ac4d2c
translation: machine
translated_at: '2026-10-24'
---
# Persistance avec SwiftData {#swiftdata-persistence}

SwiftData (iOS 17+) est le framework de persistance moderne d'Apple, construit au-dessus de Core Data. Il s'appuie sur des macros Swift (`@Model`, `@Query`) pour offrir une API nettement plus simple que l'approche NSManagedObject de Core Data.

## Points clés {#key-facts}

- SwiftData nécessite iOS 17+ - utilisez Core Data pour iOS 16 et les versions antérieures
- La macro `@Model` remplace la sous-classe `NSManagedObject` et l'éditeur de modèle de données Xcode
- `@Query` remplace `@FetchRequest` - il met automatiquement à jour les vues lorsque les données changent
- `modelContext.insert()` persiste les nouveaux objets ; `modelContext.delete()` les supprime
- `@Model` fournit automatiquement la conformité à `Identifiable`
- Les classes `@Model` doivent être `final` (elles ne peuvent pas être sous-classées)
- `.modelContainer()` appliqué à la Scene fournit la base de données à toutes les vues enfants

## Modèles {#patterns}

### Définition de @Model {#model-definition}

```swift
import Foundation
import SwiftData

@Model
final class JournalEntry {
    var title: String
    var text: String
    var rating: Double
    var date: Date

    init(title: String, text: String, rating: Double, date: Date) {
        self.title = title
        self.text = text
        self.rating = rating
        self.date = date
    }
}
```

`@Model` fournit automatiquement `Identifiable` - supprimez la conformité explicite si elle est présente.

### Configuration de modelContainer (point d'entrée de l'application) {#modelcontainer-setup-app-entry-point}

```swift
import SwiftUI
import SwiftData

@main
struct DayJournalApp: App {
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            JournalEntry.self,
            // add every @Model class here
        ])
        let modelConfiguration = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false
        )
        do {
            return try ModelContainer(
                for: schema,
                configurations: [modelConfiguration]
            )
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()

    var body: some Scene {
        WindowGroup {
            JournalEntriesListView()
        }
        .modelContainer(sharedModelContainer)
    }
}
```

Ajoutez chaque nouvelle classe `@Model` au tableau `Schema`.

### @Query (récupération des données) {#query-fetching-data}

```swift
import SwiftData

struct JournalEntriesListView: View {
    @Query var journalEntries: [JournalEntry]

    var body: some View {
        List(journalEntries) { entry in
            Text(entry.title)
        }
    }
}
```

`@Query` met automatiquement à jour la vue lorsque SwiftData change.

### Tri avec @Query {#sorting-with-query}

```swift
@Query(sort: \JournalEntry.date, order: .reverse)
var journalEntries: [JournalEntry]
```

- `.forward` - ordre croissant (par défaut)
- `.reverse` - ordre décroissant (le plus récent en premier)

### Insertion et suppression {#insert-and-delete}

```swift
struct JournalEntriesListView: View {
    @Environment(\.modelContext) var modelContext
    @Query var journalEntries: [JournalEntry]

    func addEntry() {
        let newEntry = JournalEntry(
            title: "Fun day",
            text: "Learning SwiftData!",
            rating: 4.0,
            date: Date()
        )
        modelContext.insert(newEntry)
    }

    func deleteEntry(entry: JournalEntry) {
        modelContext.delete(entry)
    }
}
```

### Vue de liste complète avec CRUD {#full-list-view-with-crud}

```swift
struct JournalEntriesListView: View {
    @Environment(\.modelContext) var modelContext
    @Query(sort: \JournalEntry.date, order: .reverse)
    var journalEntries: [JournalEntry]
    @State var showCreateView = false

    var body: some View {
        NavigationStack {
            List {
                ForEach(journalEntries) { entry in
                    NavigationLink(destination: EditJournalEntryView(editingEntry: entry)) {
                        JournalEntryRowView(entry: entry)
                    }
                }
                .onDelete { indices in
                    for index in indices {
                        modelContext.delete(journalEntries[index])
                    }
                }
            }
            .navigationTitle("\(journalEntries.count) Journal Entries")
            .toolbar {
                Button {
                    showCreateView = true
                } label: {
                    Image(systemName: "plus")
                }
            }
            .sheet(isPresented: $showCreateView) {
                CreateJournalEntryView()
            }
        }
    }
}
```

### Ajout de SwiftData à un projet existant {#adding-swiftdata-to-existing-project}

1. Mettre à jour la classe du modèle :
```swift
import SwiftData
@Model
final class JournalEntry {  // remove Identifiable conformance
    // properties unchanged
}
```

2. Mettre à jour le fichier de l'application avec `.modelContainer(sharedModelContainer)`

3. Remplacer les tableaux statiques par `@Query` :
```swift
// Remove: var entries = [JournalEntry(), JournalEntry()]
// Add:
@Query var entries: [JournalEntry]
```

4. Mettre à jour les previews :
```swift
#Preview {
    JournalEntriesListView()
        .modelContainer(for: JournalEntry.self, inMemory: true)
}
```

### SwiftData vs Core Data {#swiftdata-vs-core-data}

| Fonctionnalité | SwiftData | Core Data |
|----------------|-----------|-----------|
| Syntaxe | macro `@Model` | sous-classe `NSManagedObject` |
| Requête | wrapper de propriété `@Query` | `@FetchRequest` |
| Contexte | `@Environment(\.modelContext)` | `@Environment(\.managedObjectContext)` |
| Configuration | `.modelContainer()` sur la Scene | `.environment(\.managedObjectContext, ...)` |
| Exigence iOS | iOS 17+ | Toutes les versions d'iOS |
| Complexité | Plus simple | Plus complexe |

## Pièges à éviter {#gotchas}

- Les classes `@Model` sont des types référence - les modifications de propriétés se propagent automatiquement (aucune sauvegarde explicite n'est nécessaire pour les changements en mémoire)
- `inMemory: true` dans les previews signifie que les données sont perdues au rafraîchissement - utilisez le simulateur pour tester la persistance réelle
- Chaque classe `@Model` doit être ajoutée au tableau `Schema`, sinon elle ne sera pas persistée
- `@Model` exige `final` - la classe ne peut pas être sous-classée
- SwiftData est construit en interne sur Core Data - les deux peuvent coexister dans le même projet si nécessaire
- `modelContext.delete()` prend effet immédiatement dans l'interface, mais la suppression effective dans le stockage intervient lors de la prochaine sauvegarde automatique ou explicite

## Voir aussi {#see-also}

- [[core-data-persistence]] - persistance héritée pour iOS 16 et les versions antérieures
- [[swiftui-forms-and-input]] - formulaires de création/modification qui écrivent dans SwiftData
- [[swiftui-networking]] - récupération de données distantes à stocker dans SwiftData
- [[swiftui-lists-and-grids]] - affichage des résultats de @Query dans des listes
