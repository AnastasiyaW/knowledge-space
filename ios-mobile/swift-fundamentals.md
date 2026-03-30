---
title: Swift Language Fundamentals
category: ios-mobile/language
tags: [swift, variables, types, optionals, control-flow, swift-6]
---

# Swift Language Fundamentals

## Key Facts

- Swift is Apple's programming language for all platforms: iOS, iPadOS, macOS, watchOS, tvOS, visionOS
- Swift 6 introduced strict concurrency checking - new projects default to Swift 5, must manually change to Swift 6 in Build Settings
- Variables declared with `var` (mutable) or `let` (immutable/constant)
- Swift is type-safe: types include `String`, `Int`, `Double`, `Bool`, `Float`
- Type inference allows omitting type annotations when value is provided
- String interpolation uses `\(expression)` syntax inside double quotes
- [[swiftui-views]] use Swift properties extensively via `@State` and `@Binding` wrappers
- The underscore `_` is used as a placeholder when a value exists but is not needed (e.g., in [[foreach-and-grids]] loops: `_ in`)
- Ranges: `0..<5` is a half-open range (0 to 4), `0...4` is a closed range - ForEach requires half-open ranges
- Programmers count from 0 for historical efficiency reasons; arrays and ranges are zero-indexed

## Patterns

```swift
// Variable declaration
var name: String = "Swift"
let version: Int = 6
var score = 95.5  // Type inferred as Double

// String interpolation
let message = "Welcome to Swift \(version)"
let result = "Score: \(score)"

// Conditionals - if statement
if score > 90 {
    print("Excellent")
} else if score > 70 {
    print("Good")
} else {
    print("Needs work")
}

// Switch statement - must be exhaustive
switch version {
case 5:
    print("Legacy")
case 6:
    print("Current")
default:
    print("Unknown")
}

// Range examples
for i in 0..<5 { print(i) }  // 0,1,2,3,4
for i in 1...5 { print(i) }  // 1,2,3,4,5
```

## Gotchas

- `let` vs `var`: use `let` by default, `var` only when value must change - Xcode warns on unused `var`
- Double equals `==` checks equality; single `=` assigns value - mixing them up is a common beginner mistake
- Switch statements must be **exhaustive** - cover all cases or include `default`
- Swift 6 strict concurrency: enabling it in existing projects breaks code that was fine under Swift 5
- String comparison is case-sensitive by default
- Integer division truncates: `7 / 2` equals `3`, not `3.5` - use `Double` for decimal results

## See Also

- [The Swift Programming Language](https://docs.swift.org/swift-book/)
- [Swift.org Documentation](https://www.swift.org/documentation/)
- [[structs-and-classes]]
- [[enums-and-computed-properties]]
