---
title: SwiftData Persistence
category: concepts
tags: [ios-mobile, swiftui, swiftdata, persistence, model, query, database]
---

# SwiftData Persistence

SwiftData (iOS 17+) is Apple's modern persistence framework built on top of Core Data. It uses Swift macros (`@Model`, `@Query`) for a dramatically simpler API compared to Core Data's NSManagedObject approach.

## Key Facts

- SwiftData requires iOS 17+ - use Core Data for iOS 16 and below
- `@Model` macro replaces `NSManagedObject` subclass + Xcode data model editor
- `@Query` replaces `@FetchRequest` - automatically updates views when data changes
- `modelContext.insert()` persists new objects; `modelContext.delete()` removes them
- `@Model` automatically provides `Identifiable` conformance
- `@Model` classes must be `final` (cannot be subclassed)
- `.modelContainer()` on the Scene provides the database to all child views

## Patterns

### @Model Definition

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

`@Model` automatically provides `Identifiable` - remove explicit conformance if present.

### modelContainer Setup (App Entry Point)

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

Add every new `@Model` class to the `Schema` array.

### @Query (Fetching Data)

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

`@Query` automatically updates the view when SwiftData changes.

### Sorting with @Query

```swift
@Query(sort: \JournalEntry.date, order: .reverse)
var journalEntries: [JournalEntry]
```

- `.forward` - ascending (default)
- `.reverse` - descending (most recent first)

### Insert and Delete

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

### Full List View with CRUD

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

### Adding SwiftData to Existing Project

1. Update model class:
```swift
import SwiftData
@Model
final class JournalEntry {  // remove Identifiable conformance
    // properties unchanged
}
```

2. Update app file with `.modelContainer(sharedModelContainer)`

3. Replace static arrays with `@Query`:
```swift
// Remove: var entries = [JournalEntry(), JournalEntry()]
// Add:
@Query var entries: [JournalEntry]
```

4. Update previews:
```swift
#Preview {
    JournalEntriesListView()
        .modelContainer(for: JournalEntry.self, inMemory: true)
}
```

### SwiftData vs Core Data

| Feature | SwiftData | Core Data |
|---------|-----------|-----------|
| Syntax | `@Model` macro | `NSManagedObject` subclass |
| Query | `@Query` property wrapper | `@FetchRequest` |
| Context | `@Environment(\.modelContext)` | `@Environment(\.managedObjectContext)` |
| Setup | `.modelContainer()` on Scene | `.environment(\.managedObjectContext, ...)` |
| iOS requirement | iOS 17+ | All iOS versions |
| Complexity | Simpler | More complex |

## Gotchas

- `@Model` classes are reference types - edits to properties propagate automatically (no explicit save needed for in-memory changes)
- `inMemory: true` in previews means data is lost on refresh - use the simulator to test real persistence
- Every `@Model` class must be added to the `Schema` array or it will not be persisted
- `@Model` requires `final` - the class cannot be subclassed
- SwiftData is built on Core Data internally - both can coexist in the same project if needed
- `modelContext.delete()` works immediately in the UI but the actual storage delete happens on the next autosave or explicit save

## See Also

- [[core-data-persistence]] - legacy persistence for iOS 16 and below
- [[swiftui-forms-and-input]] - create/edit forms that write to SwiftData
- [[swiftui-networking]] - fetching remote data to store in SwiftData
- [[swiftui-lists-and-grids]] - displaying @Query results in lists
