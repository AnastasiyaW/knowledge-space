---
title: App Architecture Patterns (MVC, MVVM)
category: ios-mobile/architecture
tags: [architecture, mvc, mvvm, separation-of-concerns, dry, data-flow]
---

# App Architecture Patterns (MVC, MVVM)

## Key Facts

- Every iOS app has three main parts: **View** (what user sees), **Data** (resources/information), **Manipulation** (logic connecting data to views)
- **MVC** (Model-View-Controller): Apple's original recommended pattern - Controller mediates between Model and View
- **MVVM** (Model-View-ViewModel): modern preferred pattern for SwiftUI - ViewModel prepares data for the View
- Separation of concerns: each file/type should have a single responsibility
- DRY principle (Don't Repeat Yourself): never type the same code more than once - extract to reusable components
- Two perspectives to maintain: **developer** (code organization, naming, documentation) and **user** (UX, data presentation)
- Data questions to ask: what data is needed? where does it come from? what format? fetched or bundled?
- View questions: what data is shown? how is it laid out? one screen or multiple?
- [[state-and-data-flow]] connects the architecture layers in SwiftUI
- In SwiftUI MVVM: View observes ViewModel (@Observable), ViewModel transforms Model data

## Patterns

```
MVC Pattern:
  Model      - Data structures, business logic
  View       - SwiftUI views, UI code
  Controller - UIViewController (UIKit), less common in SwiftUI

MVVM Pattern (preferred for SwiftUI):
  Model      - Data structures (structs, enums)
  View       - SwiftUI views
  ViewModel  - @Observable class that prepares data for views

Project folder structure:
  Models/
    Currency.swift          // Enum with cases and computed properties
    ApexPredator.swift      // Data struct
  Views/
    ContentView.swift       // Main screen
    DetailView.swift        // Detail screen
    CurrencyIconView.swift  // Reusable component
  ViewModels/
    PredatorsViewModel.swift  // Data logic for views
```

```swift
// MVVM example

// Model
struct ApexPredator: Identifiable, Codable {
    let id: Int
    let name: String
    let type: PredatorType
}

// ViewModel
@Observable
class PredatorsViewModel {
    var predators: [ApexPredator] = []
    private var allPredators: [ApexPredator] = []

    init() { decode() }

    func filter(by type: PredatorType) { ... }
    func sort(by order: SortOrder) { ... }
    private func decode() { ... }
}

// View
struct PredatorListView: View {
    @State var viewModel = PredatorsViewModel()

    var body: some View {
        List(viewModel.predators) { predator in
            Text(predator.name)
        }
    }
}
```

```swift
// DRY: Extract reusable view component
struct CurrencyIcon: View {
    let currency: Currency

    var body: some View {
        ZStack {
            Image(currency.image)
                .resizable()
                .scaledToFit()
            Text(currency.name)
                .font(.caption)
        }
    }
}

// Use in ForEach - typed once, rendered many times
ForEach(Currency.allCases, id: \.self) { currency in
    CurrencyIcon(currency: currency)
}
```

## Gotchas

- Don't put all code in one file - split into Model, View, and ViewModel files for maintainability
- Apple's documentation and older tutorials use MVC, but MVVM is the modern SwiftUI approach
- The "manipulation" layer (Controller/ViewModel) should never directly reference specific views
- DRY doesn't mean over-abstracting - extract when you actually repeat code, not preemptively
- Consider Apple's App Store reviewer as a third perspective - code should be clean and understandable
- In MVVM, the View should not contain business logic - delegate filtering, sorting, formatting to the ViewModel
- When using `@Observable`, the view automatically re-renders when any observed property changes

## See Also

- [App Architecture Guide](https://developer.apple.com/documentation/swiftui/model-data)
- [[structs-and-classes]]
- [[state-and-data-flow]]
