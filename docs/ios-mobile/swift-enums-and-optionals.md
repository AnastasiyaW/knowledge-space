---
title: Swift Enums and Optionals
category: concepts
tags: [ios-mobile, swift, enums, optionals, switch, pattern-matching, codable]
---

# Swift Enums and Optionals

Enums define a finite set of named cases. Optionals represent values that may or may not exist. Together with switch statements, they form Swift's powerful pattern matching system used extensively in SwiftUI for state management and data handling.

## Key Facts

- Enums can have raw values (String, Int, Double) and computed properties
- `CaseIterable` conformance provides `.allCases` array for iteration
- Optionals are declared with `?` suffix: `var death: Death?`
- `nil` represents the absence of a value
- Swift's switch must be exhaustive - cover all cases or use `default`
- `guard let` is preferred for early exits; `if let` for conditional blocks
- Force unwrap `!` should only be used when nil is a programmer error

## Patterns

### Enum with Raw Values

```swift
enum Currency: Double, CaseIterable {
    case copperPenny = 0.01
    case silverPenny = 0.1
    case silverSickle = 1.0
    case goldSickle = 10.0
    case goldGalleon = 100.0
}

// Access raw value
Currency.goldGalleon.rawValue  // 100.0

// Iterate all cases
for currency in Currency.allCases {
    print(currency)
}
```

### Computed Properties on Enums

```swift
enum APType: String, Decodable, CaseIterable {
    case land
    case air
    case sea
}

enum Currency: Double {
    case copperPenny = 0.01
    // ...

    var name: String {
        switch self {
        case .copperPenny: return "Copper Penny"
        case .silverPenny: return "Silver Penny"
        // ... etc
        }
    }

    var image: Image {
        switch self {
        case .copperPenny: return Image(.copperPenny)
        // ... etc
        }
    }
}
```

### Methods on Enums via Extension

```swift
extension Currency {
    func convert(_ amountString: String, to currency: Currency) -> String {
        guard let doubleAmount = Double(amountString) else { return "" }
        let convertedAmount = (doubleAmount / self.rawValue) * currency.rawValue
        return String(convertedAmount)
    }
}

// Usage
leftCurrency.convert(leftAmount, to: rightCurrency)
```

### Enum for State Tracking

```swift
enum FetchStatus {
    case notStarted
    case fetching
    case success
    case failed(error: Error)    // associated value
}

enum BookStatus {
    case active
    case inactive
    case locked
}
```

### Switch Statement

```swift
switch vm.status {
case .notStarted:
    EmptyView()
case .fetching:
    ProgressView()
case .success:
    Text("Data loaded")
case .failed(let error):         // extract associated value
    Text(error.localizedDescription)
}
```

Switch must be exhaustive - cover all cases or use `default`.

### Optionals

```swift
var death: Death? = nil      // optional Death - no value yet

// 1. if let (safe unwrap)
if let death = character.death {
    Text(death.cause)        // only runs if death is not nil
}

// 2. guard let (early exit)
guard let url = URL(string: urlString) else { return nil }

// 3. nil coalescing
let name = character.death?.responsible ?? "Unknown"

// 4. Optional chaining
let responsible = character.death?.responsible   // nil if death is nil

// 5. Force unwrap (!) - only when certain non-nil
URL(string: "https://apple.com")!
```

### Optionals in Codable Models

```swift
struct Character: Decodable {
    let name: String
    var death: Death?          // optional - nil if key absent in JSON
}
```

`JSONDecoder` leaves optional properties as `nil` when the key is missing from JSON data.

## Gotchas

- Force unwrapping (`!`) a nil value crashes the app at runtime - use only when the value is guaranteed
- `guard let` must exit the enclosing scope (return, break, continue, throw)
- Enum raw values must be unique and of the same type
- `ForEach` in SwiftUI only accepts half-open ranges (`0..<5`), not closed ranges (`0...4`)
- Optional comparisons: `nil == nil` is `true`, but `nil < 0` does not compile without explicit typing
- When using enums with `Picker`, wrap the optional type: `Text("All").tag(APType?.none)` for the nil case

## See Also

- [[swift-fundamentals]] - variables, types, control flow
- [[swift-structs-and-classes]] - protocols, computed properties
- [[swiftui-networking]] - enums for fetch status tracking
- [[swiftui-state-and-data-flow]] - using enums with @State
