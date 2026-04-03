---
title: SwiftUI State and Data Flow
category: concepts
tags: [ios-mobile, swiftui, state, binding, observable, environment, property-wrappers]
---

# SwiftUI State and Data Flow

SwiftUI views are structs (immutable by default). Property wrappers like `@State`, `@Binding`, and `@Observable` enable mutable state that triggers view re-renders. This entry covers the complete data flow system from local state to app-wide shared state.

## Key Facts

- `@State` - view-local mutable property that triggers re-render on change
- `$` prefix creates a binding (two-way communication) for use in controls like `TextField`
- `@Binding` - property owned by another view, passed in for two-way access
- `@Observable` (iOS 17+) - replaces `ObservableObject` + `@Published` with simpler syntax
- `@Environment(\.dismiss)` - access environment values like dismiss action
- `@EnvironmentObject` - legacy pattern for sharing `ObservableObject` across view hierarchy
- `@FocusState` - tracks which text field has keyboard focus
- Without `@State`, changing a property inside a struct body gives: `Self is immutable`

## Patterns

### @State for View-Local State

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

Rule: use `@State` for any `var` in a SwiftUI view that should refresh the UI when changed.

### @Binding (Two-Way Communication)

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

`@State` = property is owned here; `@Binding` = property owned elsewhere, passed in.

### @Observable Macro (iOS 17+)

Replaces `ObservableObject` + `@Published`:

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

All stored properties are automatically observable - no `@Published` needed.

### @Observable ViewModel with Status Tracking

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

`private(set)` = external code can read but not write.

### @FocusState for Keyboard Tracking

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

### onChange Modifier

Observe property changes and run code:

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

### @Environment for System Values

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

### @EnvironmentObject (Legacy, pre-@Observable)

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

Requires `ObservableObject` conformance. Use `@Observable` (iOS 17+) for new code.

### @StateObject (Legacy)

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

### Passing Data to Child Views

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

## Gotchas

- Without `@State`, attempting to modify a property in a SwiftUI view struct body causes compile error: `Self is immutable`
- `$` prefix is required for two-way binding in `TextField`, `Slider`, `Toggle`, etc. - using the property directly is read-only
- `@Observable` makes ALL stored properties observable - to exclude a property, use `@ObservationIgnored`
- `@EnvironmentObject` crashes at runtime if the object is not provided in the ancestor view hierarchy
- `@FocusState` values are `Bool` by default but can also be enums for multi-field focus tracking
- `onChange` fires when the observed value actually changes, not on every re-render

## See Also

- [[swift-structs-and-classes]] - why views are structs and need @State for mutation
- [[swiftui-views-and-modifiers]] - building the UI that state drives
- [[swiftui-navigation]] - sheets and navigation use @State for presentation
- [[swiftui-networking]] - async data loading with @Observable ViewModel
