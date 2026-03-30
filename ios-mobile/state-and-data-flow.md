---
title: State and Data Flow in SwiftUI
category: ios-mobile/data
tags: [swiftui, state, binding, environment, observable, property-wrappers, data-flow]
---

# State and Data Flow in SwiftUI

## Key Facts

- `@State` marks a property that SwiftUI manages and watches for changes - view re-renders when it changes
- `@State` properties should be `private` and belong to a single view
- `$` prefix creates a `Binding` - enables two-way communication between views (e.g., `$showSheet`)
- `@Binding` lets a child view read and write a parent's `@State` property
- `@Environment` exposes built-in SwiftUI functionality (e.g., `.dismiss` action)
- `@Environment` properties must use `var` (never `let`) because their values can change
- `@Observable` (iOS 17+) replaces `@ObservableObject` for model classes - simpler and more performant
- When an `@State` property changes, SwiftUI automatically re-evaluates the `body` and updates the UI
- Bindings are required for interactive controls: `TextField`, `Toggle`, `Picker`, `Slider`
- The `.sheet()` modifier watches a `Bool` binding and presents/dismisses a view when it changes

## Patterns

```swift
struct ContentView: View {
    @State private var showExchangeInfo = false
    @State private var leftAmount = ""
    @State private var rightAmount = ""

    var body: some View {
        VStack {
            // TextField requires $binding for two-way data flow
            TextField("Amount", text: $leftAmount)

            // Button toggles state
            Button("Show Info") {
                showExchangeInfo.toggle()
            }
        }
        // Sheet watches the boolean - presents when true
        .sheet(isPresented: $showExchangeInfo) {
            ExchangeInfoView()
        }
    }
}
```

```swift
// @Environment for dismiss action
struct ExchangeInfoView: View {
    @Environment(\.dismiss) var dismiss

    var body: some View {
        Button("Done") {
            dismiss()  // Parentheses trigger the action
        }
    }
}
```

```swift
// @Observable model (iOS 17+)
@Observable
class Predators {
    var apexPredators: [ApexPredator] = []
    var allApexPredators: [ApexPredator] = []

    func filter(by type: PredatorType) {
        if type == .all {
            apexPredators = allApexPredators
        } else {
            apexPredators = allApexPredators.filter {
                $0.type == type
            }
        }
    }
}
```

## Gotchas

- `@State` should only be used for simple value types owned by one view - for shared data use `@Observable` or `@Environment`
- `dismiss` without parentheses just references the property value; `dismiss()` with parentheses actually triggers the dismiss action
- `.sheet()` can be attached to ANY view within the parent view - it does not have to be on the button that triggers it
- Forgetting the `$` prefix on bindings causes compile errors about type mismatches
- `@Environment(\.dismiss)` must use `var`, not `let`, even though you never manually reassign it
- Preview cannot test sheet dismiss - sheets only dismiss properly on simulator or device
- Changing `@State` properties triggers view re-renders, which re-runs functions that depend on those properties

## See Also

- [Managing Model Data](https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app)
- [Property Wrappers](https://developer.apple.com/documentation/swiftui/state-and-data-flow)
- [[swiftui-views]]
- [[lists-and-navigation]]
