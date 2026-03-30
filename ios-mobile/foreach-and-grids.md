---
title: ForEach Loops and Grids
category: ios-mobile/ui
tags: [swiftui, foreach, lazy-grids, iteration, identifiable, collections]
---

# ForEach Loops and Grids

## Key Facts

- `ForEach` is a SwiftUI view that generates views from a collection - typed once, rendered many times
- ForEach requires a **range** (`0..<5`) or a collection of **Identifiable** data
- Half-open range syntax: `0..<5` means 0,1,2,3,4 (five iterations) - closed ranges `0...4` do NOT work with ForEach
- `_ in` syntax: underscore discards the loop variable when it's not needed
- Named loop variable (e.g., `index in`) stores the current value for use inside the loop body
- `LazyVGrid` arranges items in a vertical grid - number of columns defined by array of `GridItem()`
- No non-lazy grid exists in SwiftUI - grids are always `LazyVGrid` or `LazyHGrid`
- Lazy loading: views are created only when they scroll into the visible area
- `Identifiable` protocol requires an `id` property - enables SwiftUI to track items for efficient updates
- ForEach works with [[enums-and-computed-properties]] that conform to `CaseIterable`

## Patterns

```swift
// ForEach with range - underscore discards index
LazyVGrid(columns: [GridItem(), GridItem(), GridItem()]) {
    ForEach(0..<5, id: \.self) { _ in
        Text("Item")
    }
}

// ForEach with named variable
ForEach(0..<10) { index in
    Text("Item \(index)")
}

// ForEach with Identifiable data
struct Dinosaur: Identifiable {
    let id = UUID()
    let name: String
    let type: PredatorType
}

ForEach(dinosaurs) { dino in
    Text(dino.name)
}

// ForEach with CaseIterable enum
enum Currency: CaseIterable {
    case copper, silver, gold
}

ForEach(Currency.allCases, id: \.self) { currency in
    Text(currency.name)
}

// Grid with custom column configuration
let columns = [
    GridItem(.flexible()),
    GridItem(.flexible()),
    GridItem(.flexible())
]

LazyVGrid(columns: columns, spacing: 16) {
    ForEach(items) { item in
        ItemView(item: item)
    }
}
```

## Gotchas

- ForEach requires half-open range (`0..<5`), NOT closed range (`0...4`) - closed range causes compile error: "cannot convert value of type ClosedRange<Int>"
- When using `ForEach` with a range, you must either provide `id: \.self` or use `_ in` / named variable
- If ForEach gives an error about "contextual type", you need to add `_ in` or a named parameter after the range
- Changing the number of `GridItem()` entries changes column count - too many columns cause items to overlap
- `Identifiable` conformance is preferred over `id: \.self` for real data models
- ForEach inside a container view (VStack, List, LazyVGrid) generates views as direct children of that container
- Lazy loading means items may briefly flicker or load late when scrolling fast through large collections

## See Also

- [ForEach Documentation](https://developer.apple.com/documentation/swiftui/foreach)
- [LazyVGrid](https://developer.apple.com/documentation/swiftui/lazyvgrid)
- [[container-views-and-layout]]
- [[lists-and-navigation]]
