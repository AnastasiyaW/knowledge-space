---
title: Lists, Navigation, and Search
category: ios-mobile/ui
tags: [swiftui, list, navigationstack, navigationlink, searchable, sorting, filtering]
---

# Lists, Navigation, and Search

## Key Facts

- `List` is a scrollable container that automatically handles row layout, separators, and swipe actions
- `List` is inherently lazy - it only loads visible rows (unlike `VStack`)
- `NavigationStack` wraps views to enable push/pop navigation with a navigation bar
- `NavigationLink` creates tappable rows that push a destination view onto the navigation stack
- `.navigationTitle("Title")` sets the navigation bar title - must be inside a `NavigationStack`
- `.searchable(text: $searchText)` adds a search bar - requires a `@State` string binding
- Sorting with `.sorted(by:)` returns a new sorted array; `.sort(by:)` sorts in-place
- Filtering with `.filter { }` returns a new array of matching elements - does NOT modify the original
- When filtering, maintain a **master list** (`allItems`) that never changes + a **display list** (`items`) that gets filtered
- `.animation()` modifier adds smooth transitions when list content changes due to sort/filter
- [[state-and-data-flow]] drives list updates - when filtered data changes, the List re-renders

## Patterns

```swift
struct ContentView: View {
    @State var predators = Predators()
    @State var searchText = ""
    @State var currentSelection = PredatorType.all

    var filteredPredators: [ApexPredator] {
        predators.apexPredators.filter { predator in
            searchText.isEmpty ||
            predator.name.localizedCaseInsensitiveContains(searchText)
        }
    }

    var body: some View {
        NavigationStack {
            List(filteredPredators) { predator in
                NavigationLink {
                    // Destination view
                    PredatorDetail(predator: predator)
                } label: {
                    // Row content
                    PredatorRow(predator: predator)
                }
            }
            .navigationTitle("Apex Predators")
            .searchable(text: $searchText)
            .toolbar {
                // Sort button
                Button {
                    predators.sort(by: .alphabetical)
                } label: {
                    Image(systemName: "arrow.up.arrow.down")
                }

                // Filter menu
                Menu {
                    Picker("Filter", selection: $currentSelection) {
                        ForEach(PredatorType.allCases, id: \.self) { type in
                            Label(type.name, systemImage: type.icon)
                        }
                    }
                } label: {
                    Image(systemName: "slider.horizontal.3")
                }
            }
            .onChange(of: currentSelection) {
                predators.filter(by: currentSelection)
            }
        }
    }
}
```

```swift
// Filter pattern: master list + display list
@Observable
class Predators {
    var allApexPredators: [ApexPredator] = []  // Never changes
    var apexPredators: [ApexPredator] = []     // Filtered/sorted

    func filter(by type: PredatorType) {
        if type == .all {
            apexPredators = allApexPredators
        } else {
            apexPredators = allApexPredators.filter {
                $0.type == type
            }
        }
    }

    func sort(by order: SortOrder) {
        switch order {
        case .alphabetical:
            apexPredators.sort { $0.name < $1.name }
        case .original:
            apexPredators.sort { $0.id < $1.id }
        }
    }
}
```

## Gotchas

- Filtering a list and assigning back to the same property destroys data permanently - always filter from a master/backup list
- `.sort()` is in-place (mutates array); `.sorted()` returns a new array - choose based on whether you need the original
- `.searchable()` must be inside a `NavigationStack` or `NavigationView` to display properly
- Search + filter work independently - searching only filters the already-filtered list unless you reset the filter first
- `NavigationLink` destination views are lazy - they are not created until the user taps the link
- `.navigationTitle()` must be placed on a view INSIDE the NavigationStack, not on the NavigationStack itself
- Animation on list changes: apply `.animation(.default, value: currentSelection)` on the List or its container

## See Also

- [List Documentation](https://developer.apple.com/documentation/swiftui/list)
- [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack)
- [[state-and-data-flow]]
- [[app-architecture-patterns]]
