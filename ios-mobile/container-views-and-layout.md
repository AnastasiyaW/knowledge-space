---
title: Container Views and Layout
category: ios-mobile/ui
tags: [swiftui, vstack, hstack, zstack, layout, container-views]
---

# Container Views and Layout

## Key Facts

- Container views hold and arrange child views: `VStack` (vertical), `HStack` (horizontal), `ZStack` (layered/depth)
- `VStack`: first view appears in the middle, additional views push it up
- `HStack`: arranges children left to right
- `ZStack`: layers views on top of each other (back to front in code order)
- Lazy variants (`LazyVStack`, `LazyHStack`) only load visible items - critical for performance with large lists
- `LazyVGrid` and `LazyHGrid` arrange items in grid patterns using `GridItem` columns/rows
- There is no non-lazy `VGrid` - grids are always lazy in SwiftUI
- Container views can be nested: an HStack inside a VStack, a VStack inside a ZStack, etc.
- Spacing between items can be customized: `VStack(spacing: 20) { ... }`
- [[swiftui-views]] modifiers like `.padding()` affect the entire container and its children
- [[foreach-and-grids]] loops are commonly placed inside containers to generate repeated content

## Patterns

```swift
// Basic stacks
VStack(alignment: .leading, spacing: 10) {
    Text("Title")
        .font(.title)
    Text("Subtitle")
        .font(.subheadline)
}

HStack(spacing: 16) {
    Image(systemName: "star.fill")
    Text("Favorites")
    Spacer()  // Pushes remaining content to the right
}

// ZStack for layering (background + content)
ZStack {
    Image(.background)
        .resizable()
        .ignoresSafeArea()
    VStack {
        Text("Overlay Text")
            .foregroundStyle(.white)
    }
}

// Grid layout with 3 columns
let columns = [
    GridItem(),
    GridItem(),
    GridItem()
]

LazyVGrid(columns: columns) {
    ForEach(0..<10) { index in
        Text("Item \(index)")
    }
}
```

## Gotchas

- Regular stacks load all children immediately; use `Lazy` variants for hundreds/thousands of items
- `Spacer()` inside an HStack pushes items apart; inside a VStack pushes items vertically
- Grid columns are defined by the number of `GridItem()` entries in the array - more items = more columns
- Too many GridItems can cause overlap if content is too wide for the screen
- ZStack alignment defaults to `.center` - use `.topLeading`, `.bottomTrailing`, etc. for other positions
- Maximum 10 direct children in a container without using `Group` or `ForEach`

## See Also

- [Layout Documentation](https://developer.apple.com/documentation/swiftui/layout-fundamentals)
- [[foreach-and-grids]]
- [[lists-and-navigation]]
