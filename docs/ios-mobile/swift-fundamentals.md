---
title: Swift Language Fundamentals
category: concepts
tags: [ios-mobile, swift, variables, types, functions, control-flow]
---

# Swift Language Fundamentals

Core Swift language constructs: variables, constants, types, operators, control flow, functions, and string handling. These are the building blocks used in every Swift and SwiftUI project.

## Key Facts

- Swift is strongly typed with type inference - once a type is set, it cannot change
- `var` declares mutable variables, `let` declares immutable constants
- Use `let` by default; switch to `var` only when mutability is needed
- String interpolation uses `\(expression)` syntax inside double quotes
- Swift uses named parameters in function calls by default
- Comments: `//` single-line, `/* */` multi-line, `Cmd+/` to toggle in Xcode
- Swift Playgrounds (File > New > Playground) provide a REPL-like environment for experimentation

## Patterns

### Variables and Constants

```swift
// var = mutable
var age = 34
age = 35           // OK
age += 1           // shorthand: age = age + 1

// let = immutable
let kilosToPounds = 2.2
// kilosToPounds = 2.5  // ERROR: cannot change constant
```

Variable names: camelCase, no spaces, case-sensitive.

### Type System

```swift
var age: Int = 34          // whole number
var price: Double = 2.99   // decimal number
var name: String = "Nick"  // text (always double quotes)
var isHot: Bool = true     // true or false only
```

Type mismatches are compile-time errors: `age = 4.5` fails if age is Int.

### String Interpolation and Methods

```swift
var count = 5
var message = "There are \(count) people"  // "There are 5 people"

// String methods
let text = "hello world"
text.uppercased()        // "HELLO WORLD"
text.lowercased()        // "hello world"
text.capitalized         // "Hello World" (property, not method)

// Type conversion
let numStr = String(count)   // explicit Int -> String
```

### Control Flow

```swift
if age > 18 {
    print("Adult")
} else if age > 12 {
    print("Teenager")
} else {
    print("Child")
}

// Comparisons produce Booleans
let isAdult = age > 18     // Bool
let isNick = name == "Nick"
```

### Arrays

```swift
var favCandy = ["FunDip", "Snickers", "HiChew"]
let nums: [Int] = [4, 7, 22, 98]

// Access (zero-indexed)
favCandy[0]        // "FunDip"
favCandy.first     // Optional("FunDip")
favCandy.last      // Optional("HiChew")
favCandy.count     // 3

// Mutation (requires var)
favCandy.append("Smarties")
favCandy.insert("M&Ms", at: 1)
favCandy.remove(at: 0)

// Empty arrays
var numbers = [Int]()
var strings: [String] = []
```

### For Loops

```swift
for candy in favCandy {
    print(candy)
}

for i in 0..<5 {  // half-open range: 0, 1, 2, 3, 4
    print(i)
}

for i in 0...4 {  // closed range: 0, 1, 2, 3, 4
    print(i)
}
```

### Functions

```swift
func greet(name: String) -> String {
    return "Hello, \(name)!"
}
let result = greet(name: "Nick")

// Multiple parameters with external/internal names
func add(_ a: Int, to b: Int) -> Int {
    return a + b
}
add(3, to: 5)  // _ suppresses external name for first param

// No return value
func printHello() {
    print("Hello")
}

// Single-expression (implicit return)
func double(_ n: Int) -> Int { n * 2 }
```

### Math Operators

```swift
+  -  *  /  %       // basic arithmetic
+=  -=  *=  /=      // compound assignment
```

### Access Control

```swift
private var secret = "hidden"              // only this file
private(set) var count = 0                 // readable anywhere, writable only in this type
internal var normal = "default"            // same module (default)
public var exposed = "visible"             // any module
```

### Extensions

Add functionality to existing types without modifying them:

```swift
extension String {
    var noSpaces: String {
        replacingOccurrences(of: " ", with: "")
    }
}
"Breaking Bad".noSpaces   // "BreakingBad"

// Conform a type to a protocol via extension
extension Character: Identifiable {
    var id: String { name }
}
```

Rule: extensions can only have computed properties and functions, no stored properties.

### Date Handling

```swift
var date = Date()              // current date/time
date.formatted()               // localized string
date.formatted(date: .long, time: .omitted)  // "April 1, 2025"
```

## Gotchas

- `let` vs `var` with reference types: `let myCar = Car()` still allows property changes on the class instance - `let` only prevents reassigning the reference itself
- Array `.first` and `.last` return optionals, not the raw value
- String interpolation evaluates expressions: `"Result: \(2 + 3)"` produces `"Result: 5"`
- Division of two Ints gives Int result: `7 / 2` equals `3`, not `3.5`
- `.capitalized` is a property (no parentheses), while `.uppercased()` and `.lowercased()` are methods
- `print()` output goes to Xcode console - useful for debugging but not visible in the app UI

## See Also

- [[swift-enums-and-optionals]] - enums, switch, optionals, pattern matching
- [[swift-structs-and-classes]] - value types vs reference types, methods, protocols
- [[swiftui-views-and-modifiers]] - using Swift within SwiftUI views
