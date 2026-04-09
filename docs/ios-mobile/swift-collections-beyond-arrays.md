---
title: "Swift Collections Beyond Arrays"
description: "Sets and Dictionaries in Swift with performance characteristics, set operations, and access patterns"
---

# Swift Collections Beyond Arrays

Arrays are the most common collection, but Swift provides Sets and Dictionaries for different access patterns. Choosing the right collection type directly impacts performance and correctness.

## Sets - Unordered Unique Elements

A Set stores unique elements with no defined order. Lookup, insertion, and deletion are O(1) average.

```swift
// Declaration
var numbers: Set<Int> = [1, 2, 3, 4, 5]

// Duplicates silently ignored
var withDupes: Set<Int> = [1, 2, 2, 3, 3, 3]
print(withDupes.count)  // 3

// Order is NOT guaranteed
print(numbers)  // could be {3, 1, 5, 2, 4} or any permutation
```

### Set Operations

```swift
let setA: Set<Int> = [1, 2, 3, 4]
let setB: Set<Int> = [3, 4, 5, 6]

setA.union(setB)           // {1, 2, 3, 4, 5, 6}
setA.intersection(setB)    // {3, 4}
setA.subtracting(setB)     // {1, 2}
setA.symmetricDifference(setB)  // {1, 2, 5, 6}

setA.isSubset(of: [1, 2, 3, 4, 5])   // true
setA.isDisjoint(with: [7, 8, 9])      // true (no common elements)
```

### Set API

```swift
var fruits: Set<String> = ["apple", "banana"]

fruits.insert("cherry")     // inserts, returns (inserted: true, ...)
fruits.insert("apple")      // no-op, returns (inserted: false, ...)
fruits.remove("banana")     // removes by VALUE (not index - sets have no indices)
fruits.contains("apple")    // true - O(1) lookup
fruits.count                // element count
fruits.isEmpty              // boolean check
```

### When to Use Sets

| Use Case | Array | Set |
|----------|-------|-----|
| Ordered data | Yes | No |
| Index-based access | Yes | No |
| Fast membership test | O(n) | O(1) |
| Guaranteed uniqueness | Manual | Automatic |
| Duplicates allowed | Yes | No |
| Mathematical operations | Manual | Built-in |

## Dictionaries - Key-Value Pairs

```swift
var user: [String: Any] = [
    "name": "Dmitry",
    "age": 25,
    "isPremium": true
]

// Access (returns Optional because key may not exist)
let name = user["name"]           // Optional("Dmitry")
let email = user["email"]         // nil

// Default value for missing keys
let email = user["email", default: "none"]  // "none"

// Modification
user["email"] = "dmitry@example.com"  // add
user["age"] = 26                      // update
user.removeValue(forKey: "isPremium") // remove
```

### Iterating Dictionaries

```swift
for (key, value) in user {
    print("\(key): \(value)")
}

// Keys and values as separate collections
let keys = Array(user.keys)
let values = Array(user.values)
```

## Higher-Order Functions on Collections

All Swift collections support `map`, `filter`, `reduce`, `compactMap`, `flatMap`:

### map - Transform Each Element

```swift
let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }        // [2, 4, 6, 8, 10]
let strings = numbers.map { String($0) }     // ["1", "2", "3", "4", "5"]

// map returns same-sized collection with potentially different type
let isEven = numbers.map { $0 % 2 == 0 }    // [false, true, false, true, false]
```

### filter - Select Elements

```swift
let evens = numbers.filter { $0 % 2 == 0 }  // [2, 4]
```

### reduce - Aggregate to Single Value

```swift
let sum = numbers.reduce(0, +)               // 15
let product = numbers.reduce(1, *)           // 120
```

### compactMap - Transform + Remove Nils

```swift
let strings = ["1", "two", "3", "four", "5"]
let ints = strings.compactMap { Int($0) }    // [1, 3, 5]
```

## String Interpolation

Swift uses `\()` syntax for embedding values in strings:

```swift
let name = "Anna"
let greeting = "Hello, \(name)!"          // "Hello, Anna!"
let calc = "2 * 5 = \(2 * 5)"            // "2 * 5 = 10"

// Works with any expression
let price = 9.99
let formatted = "Price: $\(price)"        // "Price: $9.99"
```

This is distinct from concatenation and avoids the spacing issues of passing multiple arguments to `print()`.

## Gotchas

- **Set elements must be Hashable.** Custom types need to conform to `Hashable` to be stored in a Set or used as Dictionary keys.
- **Dictionary access returns Optional.** Always unwrap safely: `if let value = dict["key"]` or use default values: `dict["key", default: 0]`.
- **Set order is random.** Do not rely on the iteration order of a Set - it may change between runs. If order matters, use an Array and manually ensure uniqueness.
- **`map` on Dictionary returns Array of tuples**, not a new Dictionary. To create a new dictionary from a transformation, use `Dictionary(uniqueKeysWithValues: dict.map { ... })` or `mapValues`.

## Cross-References

- [[swift-fundamentals]] - basic types, variables, constants
- [[swift-enums-and-optionals]] - Optional handling for dictionary access
- [[swift-generics]] - generic collection types
- [[swiftui-lists-and-grids]] - displaying collections in UI
