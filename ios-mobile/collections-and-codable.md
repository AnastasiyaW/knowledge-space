---
title: Collections, Arrays, and Codable
category: ios-mobile/data
tags: [swift, arrays, collections, codable, json, decoding, identifiable]
---

# Collections, Arrays, and Codable

## Key Facts

- Arrays are ordered collections of the same type: `[String]`, `[Int]`, `[ApexPredator]`
- Empty array initialization: `var items: [String] = []` or `var items = [String]()`
- Arrays are zero-indexed: first element is `items[0]`, last is `items[items.count - 1]`
- `Codable` protocol (`Encodable` + `Decodable`) enables JSON serialization/deserialization
- `JSONDecoder` converts JSON data to Swift types; `JSONEncoder` converts Swift types to JSON
- `Identifiable` protocol requires an `id` property - used by SwiftUI [[foreach-and-grids]] and [[lists-and-navigation]]
- `CaseIterable` on enums auto-generates `allCases` array of all enum cases
- Common array operations: `.filter {}`, `.sorted {}`, `.map {}`, `.contains {}`, `.count`, `.append()`
- `.filter()` creates a NEW array - does not modify the original; `.sort()` sorts IN-PLACE
- Decoding JSON from app bundle: `Bundle.main.url(forResource:)` + `Data(contentsOf:)` + `JSONDecoder`

## Patterns

```swift
// Array basics
var names: [String] = ["Alice", "Bob", "Charlie"]
names.append("Diana")
let first = names[0]     // "Alice"
let count = names.count   // 4

// Struct with Codable + Identifiable
struct ApexPredator: Codable, Identifiable {
    let id: Int
    let name: String
    let type: String
    let latitude: Double
    let longitude: Double
    let movies: [String]
}

// Decode JSON from bundle
func decode() -> [ApexPredator] {
    guard let url = Bundle.main.url(
        forResource: "jpapexpredators",
        withExtension: "json"
    ) else {
        fatalError("Missing data file")
    }

    do {
        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode([ApexPredator].self, from: data)
    } catch {
        fatalError("Failed to decode: \(error)")
    }
}
```

```swift
// Array operations
let predators: [ApexPredator] = decode()

// Filter - returns new array
let airPredators = predators.filter { $0.type == "air" }

// Sort - in place (mutating)
var sorted = predators
sorted.sort { $0.name < $1.name }

// Sorted - returns new array (non-mutating)
let alphabetical = predators.sorted { $0.name < $1.name }

// Map - transform elements
let names = predators.map { $0.name }

// Contains
let hasTRex = predators.contains { $0.name == "Tyrannosaurus Rex" }
```

## Gotchas

- JSON property names must match struct property names exactly, or use `CodingKeys` enum for mapping
- `.convertFromSnakeCase` decoder strategy auto-converts `snake_case` JSON keys to `camelCase` Swift properties
- `fatalError()` crashes the app intentionally - use for truly unrecoverable situations only
- `.filter()` returns a new array without modifying the original - if you assign back to the same variable, you lose the original data permanently
- Always keep a master copy of data before filtering (see [[lists-and-navigation]] filter pattern)
- Array index out of bounds causes a runtime crash - always check `.count` or use `.first` / `.last` (which return optionals)
- `$0` is shorthand for the first parameter in a closure - `$1` for second, etc.
- When conforming to `Codable`, all properties must also be `Codable`

## See Also

- [Codable Documentation](https://developer.apple.com/documentation/swift/codable)
- [JSONDecoder](https://developer.apple.com/documentation/foundation/jsondecoder)
- [[swift-fundamentals]]
- [[lists-and-navigation]]
