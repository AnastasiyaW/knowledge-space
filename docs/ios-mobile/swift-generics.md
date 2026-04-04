# Swift Generics

Generics enable writing flexible, reusable functions and types that work with any data type while maintaining type safety. They eliminate the need to write identical logic for different types.

## The Problem

Without generics, you need separate functions for each type:

```swift
func getMiddleElement(from array: [Int]) -> Int {
    return array[array.count / 2]
}

func getMiddleElementString(from array: [String]) -> String {
    return array[array.count / 2]
}
// Duplicating logic for every type is unsustainable
```

## Generic Functions

Use a type placeholder (conventionally `T`) in angle brackets:

```swift
func getMiddleElement<T>(from array: [T]) -> T {
    return array[array.count / 2]
}

let numbers = [1, 2, 3, 4, 5]
let texts = ["hello", "world", "swift"]

getMiddleElement(from: numbers)  // 3 (Int)
getMiddleElement(from: texts)    // "world" (String)
```

Swift infers `T` from the argument type. No explicit type annotation needed at the call site.

## Generic Types

Classes, structs, and enums can be generic:

```swift
struct Stack<Element> {
    private var items: [Element] = []

    mutating func push(_ item: Element) {
        items.append(item)
    }

    mutating func pop() -> Element? {
        return items.popLast()
    }

    var top: Element? {
        return items.last
    }

    var isEmpty: Bool {
        return items.isEmpty
    }
}

var intStack = Stack<Int>()
intStack.push(1)
intStack.push(2)

var stringStack = Stack<String>()
stringStack.push("hello")
```

## Type Constraints

Restrict generic types to those conforming to a protocol:

```swift
// T must be Comparable
func findMax<T: Comparable>(in array: [T]) -> T? {
    guard var maxValue = array.first else { return nil }
    for item in array {
        if item > maxValue {
            maxValue = item
        }
    }
    return maxValue
}

findMax(in: [3, 1, 4, 1, 5])   // 5
findMax(in: ["b", "a", "c"])    // "c"
```

Common protocol constraints:
- `Comparable` - supports `<`, `>`, `<=`, `>=`
- `Equatable` - supports `==`, `!=`
- `Hashable` - can be used as dictionary key or in sets
- `Codable` - JSON encoding/decoding
- `CustomStringConvertible` - has description property

## Where Clauses

For more complex constraints:

```swift
func allEqual<T: Equatable>(in array: [T]) -> Bool where T: Hashable {
    return Set(array).count <= 1
}

// Multiple generic types with relationships
func convert<Input, Output>(value: Input, using transform: (Input) -> Output) -> Output {
    return transform(value)
}
```

## Associated Types in Protocols

Protocols can have generic-like behavior via associated types:

```swift
protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
    var count: Int { get }
    subscript(i: Int) -> Item { get }
}

struct IntArray: Container {
    typealias Item = Int  // Swift can usually infer this
    var items: [Int] = []

    mutating func append(_ item: Int) {
        items.append(item)
    }
    var count: Int { items.count }
    subscript(i: Int) -> Int { items[i] }
}
```

## Practical Uses in iOS Development

Generics are ubiquitous in Swift and iOS:

```swift
// Networking: generic response parsing
func fetchData<T: Decodable>(from url: URL) async throws -> T {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(T.self, from: data)
}

let user: User = try await fetchData(from: userURL)
let posts: [Post] = try await fetchData(from: postsURL)

// SwiftUI: generic view builders
struct CardView<Content: View>: View {
    let content: Content

    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }

    var body: some View {
        VStack {
            content
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .shadow(radius: 4)
    }
}
```

## Gotchas

- **Type erasure is sometimes needed.** You cannot use a protocol with associated types as a concrete type directly (e.g., `var container: Container` does not compile). Use `any Container` (Swift 5.7+) or type-erased wrappers.
- **Generic type inference can fail with complex expressions.** If the compiler cannot infer `T`, you may need explicit type annotations: `let result: MyType = genericFunction()`.
- **Generics are resolved at compile time.** There is zero runtime overhead compared to writing type-specific functions. The compiler generates specialized code for each concrete type used.

## Cross-References

- [[swift-fundamentals]] - basic Swift syntax
- [[swift-structs-and-classes]] - generic structs and classes
- [[swiftui-state-and-data-flow]] - generic property wrappers
- [[swiftui-networking]] - generic API clients
