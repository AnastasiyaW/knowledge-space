---
title: "SwiftData-Persistenz"
category: concepts
tags: [ios-mobile, swiftui, swiftdata, persistence, model, query, database]
level: 3
source_sha256: 540790694eca27502ff1dbfcadaf43b19fc77535314ffd59c5e2e714c2ac4d2c
translation: machine
translated_at: '2026-10-24'
---
# SwiftData-Persistenz {#swiftdata-persistence}

SwiftData (iOS 17+) ist Apples moderne Persistenz-Framework, das auf Core Data aufbaut. Es verwendet Swift-Makros (`@Model`, `@Query`) für eine deutlich einfachere API im Vergleich zum NSManagedObject-Ansatz von Core Data.

## Wichtige Fakten {#key-facts}

- SwiftData erfordert iOS 17+ - für iOS 16 und älter Core Data verwenden
- Das `@Model`-Makro ersetzt die `NSManagedObject`-Unterklasse und den Datenmodell-Editor in Xcode
- `@Query` ersetzt `@FetchRequest` - Views werden automatisch aktualisiert, wenn sich Daten ändern
- `modelContext.insert()` persistiert neue Objekte; `modelContext.delete()` entfernt sie
- `@Model` stellt automatisch die `Identifiable`-Konformität bereit
- `@Model`-Klassen müssen `final` sein (sie können nicht subklassiert werden)
- `.modelContainer()` auf der Scene stellt die Datenbank allen untergeordneten Views zur Verfügung

## Muster {#patterns}

### @Model-Definition {#model-definition}

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

`@Model` stellt automatisch `Identifiable` bereit - explizite Konformität entfernen, falls vorhanden.

### modelContainer-Einrichtung (App-Einstiegspunkt) {#modelcontainer-setup-app-entry-point}

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

Jede neue `@Model`-Klasse zum `Schema`-Array hinzufügen.

### @Query (Daten abrufen) {#query-fetching-data}

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

`@Query` aktualisiert die View automatisch, wenn sich Daten in SwiftData ändern.

### Sortierung mit @Query {#sorting-with-query}

```swift
@Query(sort: \JournalEntry.date, order: .reverse)
var journalEntries: [JournalEntry]
```

- `.forward` - aufsteigend (Standard)
- `.reverse` - absteigend (neueste zuerst)

### Einfügen und Löschen {#insert-and-delete}

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

### Vollständige Listenansicht mit CRUD {#full-list-view-with-crud}

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

### SwiftData zu einem bestehenden Projekt hinzufügen {#adding-swiftdata-to-existing-project}

1. Modellklasse aktualisieren:
```swift
import SwiftData
@Model
final class JournalEntry {  // remove Identifiable conformance
    // properties unchanged
}
```

2. App-Datei mit `.modelContainer(sharedModelContainer)` aktualisieren

3. Statische Arrays durch `@Query` ersetzen:
```swift
// Remove: var entries = [JournalEntry(), JournalEntry()]
// Add:
@Query var entries: [JournalEntry]
```

4. Previews aktualisieren:
```swift
#Preview {
    JournalEntriesListView()
        .modelContainer(for: JournalEntry.self, inMemory: true)
}
```

### SwiftData vs. Core Data {#swiftdata-vs-core-data}

| Merkmal | SwiftData | Core Data |
|---------|-----------|-----------|
| Syntax | `@Model`-Makro | `NSManagedObject`-Unterklasse |
| Abfrage | `@Query`-Property-Wrapper | `@FetchRequest` |
| Kontext | `@Environment(\.modelContext)` | `@Environment(\.managedObjectContext)` |
| Einrichtung | `.modelContainer()` auf Scene | `.environment(\.managedObjectContext, ...)` |
| iOS-Anforderung | iOS 17+ | Alle iOS-Versionen |
| Komplexität | Einfacher | Komplexer |

## Stolperfallen {#gotchas}

- `@Model`-Klassen sind Referenztypen - Änderungen an Eigenschaften werden automatisch übernommen (kein explizites Speichern nötig für In-Memory-Änderungen)
- `inMemory: true` in Previews bedeutet, dass Daten bei einem Refresh verloren gehen - im Simulator testen, um die echte Persistenz zu prüfen
- Jede `@Model`-Klasse muss zum `Schema`-Array hinzugefügt werden, sonst wird sie nicht persistiert
- `@Model` erfordert `final` - die Klasse kann nicht subklassiert werden
- SwiftData basiert intern auf Core Data - beide können bei Bedarf im selben Projekt koexistieren
- `modelContext.delete()` wirkt in der UI sofort, die eigentliche Löschung im Speicher erfolgt jedoch erst beim nächsten Autosave oder expliziten Speichern

## Siehe auch {#see-also}

- [[core-data-persistence]] - Legacy-Persistenz für iOS 16 und älter
- [[swiftui-forms-and-input]] - Formulare zum Erstellen/Bearbeiten, die in SwiftData schreiben
- [[swiftui-networking]] - Abruf von Remote-Daten zur Speicherung in SwiftData
- [[swiftui-lists-and-grids]] - Anzeige von @Query-Ergebnissen in Listen
