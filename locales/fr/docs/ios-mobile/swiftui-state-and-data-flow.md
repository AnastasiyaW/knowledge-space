---
title: "État et flux de données dans SwiftUI"
category: concepts
tags: [ios-mobile, swiftui, state, binding, observable, environment, property-wrappers]
level: 3
source_sha256: 30eda23a90e70c962b04ceca506507cd4a80f39b9ae642c287487142f0788970
translation: machine
translated_at: '2026-10-24'
---
# État et flux de données dans SwiftUI {#swiftui-state-and-data-flow}

Les vues SwiftUI sont des structs (immuables par défaut). Les property wrappers comme `@State`, `@Binding` et `@Observable` permettent d'avoir un état mutable qui déclenche le re-rendu des vues. Cette entrée couvre l'ensemble du système de flux de données, depuis l'état local jusqu'à l'état partagé à l'échelle de l'application.

## Points clés {#key-facts}

- `@State` - propriété mutable locale à la vue, qui déclenche un re-rendu à chaque modification
- Le préfixe `$` crée un binding (communication bidirectionnelle) à utiliser avec des contrôles comme `TextField`
- `@Binding` - propriété possédée par une autre vue, transmise pour un accès bidirectionnel
- `@Observable` (iOS 17+) - remplace `ObservableObject` + `@Published` avec une syntaxe plus simple
- `@Environment(\.dismiss)` - accès aux valeurs d'environnement, comme l'action dismiss
- `@EnvironmentObject` - ancien modèle pour partager un `ObservableObject` dans la hiérarchie des vues
- `@FocusState` - suit le champ de texte qui détient le focus clavier
- Sans `@State`, modifier une propriété dans le corps d'un struct produit l'erreur : `Self is immutable`

## Patterns {#patterns}

### @State pour l'état local à la vue {#state-for-view-local-state}

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

Règle : utiliser `@State` pour toute `var` d'une vue SwiftUI qui doit rafraîchir l'interface lorsqu'elle change.

### @Binding (communication bidirectionnelle) {#binding-two-way-communication}

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

`@State` = la propriété appartient à cette vue ; `@Binding` = la propriété appartient à une autre vue et est transmise.

### Macro @Observable (iOS 17+) {#observable-macro-ios-17}

Remplace `ObservableObject` + `@Published` :

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

Toutes les propriétés stockées sont automatiquement observables : aucun `@Published` n'est nécessaire.

### ViewModel @Observable avec suivi de statut {#observable-viewmodel-with-status-tracking}

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

`private(set)` = le code externe peut lire la propriété mais ne peut pas l'écrire.

### @FocusState pour le suivi du clavier {#focusstate-for-keyboard-tracking}

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

### Modificateur onChange {#onchange-modifier}

Observer les changements d'une propriété et exécuter du code :

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

### @Environment pour les valeurs système {#environment-for-system-values}

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

### @EnvironmentObject (ancien modèle, avant @Observable) {#environmentobject-legacy-pre-observable}

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

Nécessite que `ObservableObject` soit implémenté. Utiliser `@Observable` (iOS 17+) pour le nouveau code.

### @StateObject (ancien modèle) {#stateobject-legacy}

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

### Transmettre des données aux vues enfants {#passing-data-to-child-views}

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

## Pièges à éviter {#gotchas}

- Sans `@State`, tenter de modifier une propriété dans le corps d'une struct de vue SwiftUI provoque une erreur de compilation : `Self is immutable`
- Le préfixe `$` est requis pour le binding bidirectionnel dans `TextField`, `Slider`, `Toggle`, etc. : utiliser la propriété directement ne donne qu'un accès en lecture seule
- `@Observable` rend observables TOUTES les propriétés stockées ; pour exclure une propriété, utiliser `@ObservationIgnored`
- `@EnvironmentObject` provoque un crash à l'exécution si l'objet n'est pas fourni dans la hiérarchie des vues ancêtres
- `@FocusState` vaut par défaut un `Bool`, mais peut aussi être un enum pour suivre le focus entre plusieurs champs
- `onChange` se déclenche lorsque la valeur observée change réellement, et non à chaque re-rendu

## Voir aussi {#see-also}

- [[swift-structs-and-classes]] - pourquoi les vues sont des structs et ont besoin de `@State` pour être modifiées
- [[swiftui-views-and-modifiers]] - construction de l'interface pilotée par l'état
- [[swiftui-navigation]] - les sheets et la navigation utilisent `@State` pour la présentation
- [[swiftui-networking]] - chargement asynchrone de données avec un ViewModel `@Observable`
