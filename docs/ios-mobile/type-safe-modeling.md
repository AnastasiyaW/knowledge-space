---
title: "Type-Safe Domain Modeling in Swift"
description: "Using enums, structs, and generics to eliminate impossible states and make APIs self-documenting"
---

# Type-Safe Domain Modeling in Swift

Choosing the right type representation eliminates impossible states, reduces bugs, and makes APIs self-documenting. Swift's type system (enums, structs, optionals, generics) allows precise modeling that goes beyond what languages with only classes can express.

## The Problem with Optionals

Multiple optional parameters create an explosion of possible states, most of which are invalid:

```swift
// URLSession completion handler: 3 optionals = 8 possible combinations
(Data?, URLResponse?, Error?) -> Void
```

Most combinations are nonsensical: data without a response, error with data, all nil. The type system does not prevent these.

**Better representation with an enum:**

```swift
enum NetworkResult {
    case success(data: Data, response: URLResponse)
    case failure(Error)
}
```

Now only 2 valid states exist. The compiler enforces exhaustive handling.

## When Enums Beat Structs

Use enums when:
- States are **mutually exclusive** (logged in OR logged out, never both)
- Different states carry **different associated data**
- You want the compiler to enforce **exhaustive handling**

```swift
// Struct: 4 possible states (user present/absent x expired true/false)
struct Session {
    var user: User?      // nil = not registered
    var expired: Bool     // only meaningful when user exists
}

// Enum: 3 valid states only
enum SessionState {
    case notRegistered
    case loggedIn(User)
    case expired(User)
}
```

## When Structs + Optionals Beat Enums

If multiple enum cases share the same associated value, an optional struct may be simpler:

```swift
// Enum with duplicated user in two cases
enum SessionState {
    case loggedIn(User)
    case expired(User)    // same User type
    case notRegistered
}

// Simpler: struct + optional
struct Session {
    var user: User        // non-optional
    var expired: Bool
}
var currentSession: Session?  // nil = not registered
```

Accessing `user` requires no switching - just optional chaining on the session itself.

## Function Return Type Design

Even a simple function like "read files" has many valid type signatures:

```swift
// Option 1: Lose information about which files failed
func readFiles(_ names: [String]) -> [Data]

// Option 2: Track which files failed (nil = failure)
func readFiles(_ names: [String]) -> [Data?]

// Option 3: Pair each result with its filename
func readFiles(_ names: [String]) -> [(String, Data?)]

// Option 4: All-or-nothing
func readFiles(_ names: [String]) -> [Data]?

// Option 5: Rich error per file
func readFiles(_ names: [String]) -> [Result<Data, FileError>]
```

Choose based on what the caller needs:
- **Error recovery per file** -> Option 3 or 5
- **All-or-nothing** -> Option 4
- **Simple case** -> Option 1

## Unsigned Integer Trade-off

The Swift standard library uses `Int` (not `UInt`) for `Array.count` and subscript indices, even though negative values are meaningless. This is a deliberate trade-off:

- **Precision:** `UInt` eliminates negative values
- **Ergonomics:** Every arithmetic operation with `Int` requires conversion

Apple chose ergonomics. Lesson: **maximum type precision is not always the best design.**

## Property-Based Testing for Type Invariants

When types cannot fully enforce constraints (e.g., "output array length equals input array length"), use property-based tests:

```swift
func testReadFilesPreservesLength() {
    for _ in 0..<1000 {
        let names = (0..<Int.random(in: 1...20)).map { "file\($0).txt" }
        let results = readFiles(names)
        XCTAssertEqual(results.count, names.count)
    }
}
```

## Type Design Checklist

1. **List all possible states** your data can be in
2. **Identify invalid combinations** that should never occur
3. **Choose types that eliminate invalid states:**
   - Enum for mutually exclusive states
   - Non-optional properties for always-present data
   - Phantom types for compile-time state machines
4. **Verify:** can you construct a value of your type that represents something meaningless? If yes, tighten the type.

## Gotchas

- **Over-precise types:** Making every constraint a type-level check can make APIs painful to use. `UInt` for array indices is technically more correct but creates conversion burden everywhere. Find the sweet spot between precision and ergonomics.
- **Enum case explosion:** If you have 4 optional fields where all 16 combinations are valid, an enum with 16 cases is worse than 4 optionals. Enums shine when most combinations are **invalid**.
- **Migration difficulty:** Changing a struct to an enum (or vice versa) is a breaking API change. Think carefully about your type choice before shipping a public API.

## See Also

- [[swift-enums-and-optionals]]
- [[swift-structs-and-classes]]
- [[swift-phantom-types]]
- [[swift-generics]]
