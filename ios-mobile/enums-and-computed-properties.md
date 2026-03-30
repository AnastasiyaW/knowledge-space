---
title: Enums and Computed Properties
category: ios-mobile/language
tags: [swift, enums, computed-properties, raw-values, switch, caseiterable]
---

# Enums and Computed Properties

## Key Facts

- Enums define a type with a fixed set of cases - instances must be one of the defined cases
- Each enum case can be thought of as a subtype of the enum type
- Raw values associate a constant value with each case: `enum Currency: Double { case penny = 0.01 }`
- Enums can conform to `CaseIterable` to get an `allCases` array for [[foreach-and-grids]] loops
- **Computed properties** calculate their value every time they are accessed - not stored, but computed on demand
- Computed properties must use `var` (never `let`) and must declare their type explicitly
- The `self` keyword inside an enum refers to whichever case the current instance is
- Switch statements on enums must be exhaustive - cover all cases or use `default`
- Enums can have multiple computed properties, each using `switch self` to return case-specific values
- Frameworks like SwiftUI must be imported (`import SwiftUI`) to use types like `ImageResource` inside enum files

## Patterns

```swift
import SwiftUI

enum Currency: Double, CaseIterable {
    case copperPenny = 640
    case silverPenny = 64
    case silverPiece = 16
    case goldPenny = 4
    case goldPiece = 1

    // Computed property - image for each case
    var image: ImageResource {
        switch self {
        case .copperPenny: .copperpenny
        case .silverPenny: .silverpenny
        case .silverPiece: .silverpiece
        case .goldPenny: .goldpenny
        case .goldPiece: .goldpiece
        }
    }

    // Computed property - display name
    var name: String {
        switch self {
        case .copperPenny: "Copper Penny"
        case .silverPenny: "Silver Penny"
        case .silverPiece: "Silver Piece"
        case .goldPenny: "Gold Penny"
        case .goldPiece: "Gold Piece"
        }
    }
}

// Usage
let currency = Currency.goldPenny
print(currency.rawValue) // 4.0
print(currency.name)     // "Gold Penny"

// Iterating all cases (CaseIterable)
for c in Currency.allCases {
    print("\(c.name): \(c.rawValue)")
}
```

## Gotchas

- Enum cases with raw values: the raw value type is declared after the colon on the enum name, not on each case
- `CaseIterable` conformance is required to iterate over all cases with `allCases`
- Computed properties re-compute every access - for expensive operations consider caching
- Switch on `self` in an enum does not need `default` if all cases are covered
- Xcode can auto-complete switch cases: type `switch self { }` and press Enter on the fix-it to insert all cases
- Don't confuse enum `case` with switch `case` - they share the keyword but serve different purposes
- When accessing enum cases in code, the dot syntax shorthand works when type is known: `.copperPenny` instead of `Currency.copperPenny`

## See Also

- [Enumerations](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/enumerations/)
- [[swift-fundamentals]]
- [[structs-and-classes]]
