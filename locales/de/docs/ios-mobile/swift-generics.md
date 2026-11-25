---
title: "Swift-Generics"
description: "Typsichere, wiederverwendbare Funktionen und Typen mit generischen Parametern, Constraints und assoziierten Typen"
level: 3
source_sha256: fa019ab334b9865714d8ecd538cb990fa731042cc5edc0fa709cf2d4053ea7de
translation: machine
translated_at: '2026-10-24'
---
# Swift-Generics {#swift-generics}

Generics ermöglichen das Schreiben flexibler, wiederverwendbarer Funktionen und Typen, die mit beliebigen Datentypen arbeiten und dabei Typsicherheit wahren. Sie machen es überflüssig, identische Logik für unterschiedliche Typen mehrfach zu schreiben.

## Das Problem {#the-problem}

Ohne Generics benötigt man separate Funktionen für jeden Typ:

```swift
func getMiddleElement(from array: [Int]) -> Int {
    return array[array.count / 2]
}

func getMiddleElementString(from array: [String]) -> String {
    return array[array.count / 2]
}
// Duplicating logic for every type is unsustainable
```

## Generische Funktionen {#generic-functions}

Verwende einen Typplatzhalter (üblicherweise `T`) in spitzen Klammern:

```swift
func getMiddleElement<T>(from array: [T]) -> T {
    return array[array.count / 2]
}

let numbers = [1, 2, 3, 4, 5]
let texts = ["hello", "world", "swift"]

getMiddleElement(from: numbers)  // 3 (Int)
getMiddleElement(from: texts)    // "world" (String)
```

Swift leitet `T` aus dem Argumenttyp ab. An der Aufrufstelle ist keine explizite Typannotation nötig.

## Generische Typen {#generic-types}

Klassen, Structs und Enums können generisch sein:

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

## Typ-Constraints {#type-constraints}

Schränke generische Typen auf solche ein, die ein Protokoll konformieren:

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

Gängige Protokoll-Constraints:
- `Comparable` - unterstützt `<`, `>`, `<=`, `>=`
- `Equatable` - unterstützt `==`, `!=`
- `Hashable` - kann als Dictionary-Schlüssel oder in Sets verwendet werden
- `Codable` - JSON-Kodierung/-Dekodierung
- `CustomStringConvertible` - besitzt die Eigenschaft `description`

## Where-Klauseln {#where-clauses}

Für komplexere Constraints:

```swift
func allEqual<T: Equatable>(in array: [T]) -> Bool where T: Hashable {
    return Set(array).count <= 1
}

// Multiple generic types with relationships
func convert<Input, Output>(value: Input, using transform: (Input) -> Output) -> Output {
    return transform(value)
}
```

## Assoziierte Typen in Protokollen {#associated-types-in-protocols}

Protokolle können generisch-ähnliches Verhalten über assoziierte Typen besitzen:

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

## Praktische Anwendungen in der iOS-Entwicklung {#practical-uses-in-ios-development}

Generics sind in Swift und iOS allgegenwärtig:

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

## Fallstricke {#gotchas}

- **Typlöschung ist manchmal nötig.** Ein Protokoll mit assoziierten Typen kann nicht direkt als konkreter Typ verwendet werden (z. B. kompiliert `var container: Container` nicht). Verwende `any Container` (Swift 5.7+) oder typlöschende Wrapper.
- **Die generische Typinferenz kann bei komplexen Ausdrücken scheitern.** Wenn der Compiler `T` nicht ableiten kann, sind möglicherweise explizite Typannotationen nötig: `let result: MyType = genericFunction()`.
- **Generics werden zur Kompilierzeit aufgelöst.** Im Vergleich zum Schreiben typspezifischer Funktionen entsteht kein Laufzeit-Overhead. Der Compiler erzeugt für jeden verwendeten konkreten Typ spezialisierten Code.

## Querverweise {#cross-references}

- [[swift-fundamentals]] - grundlegende Swift-Syntax
- [[swift-structs-and-classes]] - generische Structs und Klassen
- [[swiftui-state-and-data-flow]] - generische Property Wrapper
- [[swiftui-networking]] - generische API-Clients
