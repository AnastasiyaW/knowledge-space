---
title: "SwiftUI State und Datenfluss"
category: concepts
tags: [ios-mobile, swiftui, state, binding, observable, environment, property-wrappers]
level: 3
source_sha256: 30eda23a90e70c962b04ceca506507cd4a80f39b9ae642c287487142f0788970
translation: machine
translated_at: '2026-10-24'
---
# SwiftUI State und Datenfluss {#swiftui-state-and-data-flow}

SwiftUI-Views sind Structs (standardmäßig unveränderlich). Property Wrapper wie `@State`, `@Binding` und `@Observable` ermöglichen veränderlichen Zustand, der ein Neuzeichnen der View auslöst. Dieser Eintrag behandelt das vollständige Datenflusssystem, vom lokalen Zustand bis zum app-weit geteilten Zustand.

## Wichtige Fakten {#key-facts}

- `@State` - view-lokale veränderliche Property, die bei Änderung ein Neuzeichnen auslöst
- Das `$`-Präfix erzeugt ein Binding (bidirektionale Kommunikation) für Steuerelemente wie `TextField`
- `@Binding` - Property, die einer anderen View gehört und zum bidirektionalen Zugriff übergeben wird
- `@Observable` (iOS 17+) - ersetzt `ObservableObject` + `@Published` durch eine einfachere Syntax
- `@Environment(\.dismiss)` - Zugriff auf Environment-Werte wie die Dismiss-Aktion
- `@EnvironmentObject` - veraltetes Muster zum Teilen eines `ObservableObject` über die View-Hierarchie
- `@FocusState` - verfolgt, welches Textfeld den Tastaturfokus hat
- Ohne `@State` führt eine Änderung einer Property im Body eines Structs zu: `Self is immutable`

## Muster {#patterns}

### @State für view-lokalen Zustand {#state-for-view-local-state}

```swift
struct ContentView: View {
    @State var count = 0
    @State var showExchangeInfo = false
    @State var leftAmount = ""

    var body: some View {
        VStack {
            Text("Count: \(count)")
                .font(.largeTitle)
            Button("Add") {
                count += 1
            }
        }
    }
}
```

Regel: Verwende `@State` für jede `var` in einer SwiftUI-View, die die UI bei Änderung aktualisieren soll.

### @Binding (bidirektionale Kommunikation) {#binding-two-way-communication}

```swift
// $ prefix creates a binding
TextField("Amount", text: $leftAmount)
// Without $: text: leftAmount  -> ERROR: expects Binding<String>

// @Binding in child view
struct ChildView: View {
    @Binding var isActive: Bool  // owned by parent, passed in

    var body: some View {
        Toggle("Active", isOn: $isActive)
    }
}

// Parent passes binding with $
ChildView(isActive: $showExchangeInfo)
```

`@State` = Property gehört hier; `@Binding` = Property gehört woanders und wird übergeben.

### @Observable-Makro (iOS 17+) {#observable-macro-ios-17}

Ersetzt `ObservableObject` + `@Published`:

```swift
@Observable
class CurrencyViewModel {
    var leftAmount = ""
    var rightAmount = ""
    var leftCurrency: Currency = .silverPenny
    var rightCurrency: Currency = .goldGalleon
}

// In view - no @StateObject or @ObservedObject needed
struct ContentView: View {
    var vm = CurrencyViewModel()

    var body: some View {
        TextField("Amount", text: $vm.leftAmount)
    }
}
```

Alle gespeicherten Properties sind automatisch beobachtbar - `@Published` ist nicht nötig.

### @Observable-ViewModel mit Statusverfolgung {#observable-viewmodel-with-status-tracking}

```swift
enum FetchStatus {
    case notStarted
    case fetching
    case success
    case failed(error: Error)
}

@Observable
class ViewModel {
    private(set) var status: FetchStatus = .notStarted
    var quote: Quote
    var character: Character

    func getData(for show: String) async {
        status = .fetching
        do {
            quote = try await fetcher.fetchQuote(from: show)
            character = try await fetcher.fetchCharacter(quote.character)
            status = .success
        } catch {
            status = .failed(error: error)
        }
    }
}
```

`private(set)` = externer Code kann lesen, aber nicht schreiben.

### @FocusState für die Tastaturverfolgung {#focusstate-for-keyboard-tracking}

```swift
struct ContentView: View {
    @FocusState var leftTyping: Bool
    @FocusState var rightTyping: Bool

    var body: some View {
        TextField("Amount", text: $leftAmount)
            .focused($leftTyping)
        TextField("Amount", text: $rightAmount)
            .focused($rightTyping)
    }
}

// Dismiss keyboard on background tap
.onTapGesture { leftTyping = false; rightTyping = false }
```

### onChange-Modifier {#onchange-modifier}

Änderungen an Properties beobachten und Code ausführen:

```swift
.onChange(of: leftAmount) {
    if leftTyping {
        rightAmount = leftCurrency.convert(leftAmount, to: rightCurrency)
    }
}
.onChange(of: leftCurrency) {
    leftAmount = rightCurrency.convert(rightAmount, to: leftCurrency)
}
```

### @Environment für Systemwerte {#environment-for-system-values}

```swift
struct SheetView: View {
    @Environment(\.dismiss) var dismiss
    @Environment(\.modelContext) var modelContext  // SwiftData
    @Environment(\.managedObjectContext) var viewContext  // Core Data

    var body: some View {
        Button("Done") {
            dismiss()   // works for both sheets and navigation pop-back
        }
    }
}
```

### @EnvironmentObject (veraltet, vor @Observable) {#environmentobject-legacy-pre-observable}

```swift
// Pass into environment from parent
ContentView()
    .environmentObject(myObject)

// Access in any child view
struct ChildView: View {
    @EnvironmentObject var myObject: MyClass
    // ...
}
```

Erfordert die Konformität zu `ObservableObject`. Verwende für neuen Code `@Observable` (iOS 17+).

### @StateObject (veraltet) {#stateobject-legacy}

```swift
@main
struct HPTriviaApp: App {
    @StateObject private var store = Store()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(store)
        }
    }
}
```

### Daten an Child-Views übergeben {#passing-data-to-child-views}

```swift
struct JournalDetailView: View {
    var entry: JournalEntry   // no @State, no default = required parameter

    var body: some View {
        Text(entry.title).font(.title)
    }
}

// Preview requires sample data
#Preview {
    JournalDetailView(entry: JournalEntry(title: "Test", text: "Hello", rating: 4, date: Date()))
}
```

## Fallstricke {#gotchas}

- Ohne `@State` führt der Versuch, eine Property im Body einer SwiftUI-View-Struct zu ändern, zu einem Compilerfehler: `Self is immutable`
- Das `$`-Präfix ist für bidirektionale Bindings in `TextField`, `Slider`, `Toggle` usw. erforderlich - die direkte Verwendung der Property ist nur lesend
- `@Observable` macht ALLE gespeicherten Properties beobachtbar - um eine Property auszuschließen, verwende `@ObservationIgnored`
- `@EnvironmentObject` führt zur Laufzeit zum Absturz, wenn das Objekt in der übergeordneten View-Hierarchie nicht bereitgestellt wird
- `@FocusState`-Werte sind standardmäßig `Bool`, können aber für die Fokusverfolgung mehrerer Felder auch Enums sein
- `onChange` wird ausgelöst, wenn sich der beobachtete Wert tatsächlich ändert, nicht bei jedem Neuzeichnen

## Siehe auch {#see-also}

- [[swift-structs-and-classes]] - warum Views Structs sind und für Mutation `@State` benötigen
- [[swiftui-views-and-modifiers]] - der Aufbau der UI, die durch den Zustand gesteuert wird
- [[swiftui-navigation]] - Sheets und Navigation verwenden `@State` für die Präsentation
- [[swiftui-networking]] - asynchrones Laden von Daten mit einem `@Observable`-ViewModel
