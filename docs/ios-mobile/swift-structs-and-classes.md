---
title: Swift Structs and Classes
category: concepts
tags: [ios-mobile, swift, structs, classes, protocols, value-types, reference-types]
---

# Swift Structs and Classes

Structs and classes are blueprints for custom types in Swift. Apple recommends using structs by default. Classes are needed for reference semantics, inheritance, or when used with frameworks that require them (Core Data, @Observable).

## Key Facts

- Structs are value types (copied on assignment), classes are reference types (shared)
- Apple recommends struct by default unless class-specific features are needed
- `mutating` keyword required for struct methods that modify properties
- Every SwiftUI view is a struct conforming to the `View` protocol
- `final` class cannot be subclassed (required by SwiftData's `@Model`)
- Structs get a free memberwise initializer; classes require explicit `init`
- `self` refers to the current instance inside methods

## Patterns

### Struct Definition

```swift
struct Dog {
    var name: String
    var age: Int
    var furColor: String
}

// Auto-generated memberwise initializer
var myDog = Dog(name: "Fido", age: 7, furColor: "brown")
myDog.age = 8       // update property (requires var)
```

### Methods on Structs

```swift
struct Puppy {
    var name: String
    var hunger: Int

    func bark() {
        print("\(name) says Woof!")
    }

    mutating func eat() {   // mutating required to change properties
        hunger -= 1
    }
}

var myPuppy = Puppy(name: "Fido", hunger: 5)
myPuppy.eat()    // hunger becomes 4
myPuppy.bark()   // "Fido says Woof!"
```

### Class Definition

```swift
class Car {
    var year: Int = 2020
    var color: String = "red"
}

let myCar = Car()
myCar.color = "blue"   // OK: let prevents reassignment, not property changes
```

### Stored vs Computed Properties

```swift
// Stored property - holds a value
var count = 0
let name = "Nick"

// Computed property - runs code to produce a value each time
var body: some View {    // required by View protocol
    Text("Hello")
}

// Computed property on custom type
var fullName: String {
    "\(firstName) \(lastName)"
}
```

### Protocols

```swift
// View protocol - every SwiftUI view conforms
struct ContentView: View {
    var body: some View {    // computed property required by protocol
        Text("Hello, world!")
    }
}

// Identifiable protocol - required for List/ForEach
class JournalEntry: Identifiable {
    var id = UUID()
    var title: String
    // ...
}

// CaseIterable protocol - provides .allCases array
enum APType: String, CaseIterable {
    case land, air, sea
}
APType.allCases  // [.land, .air, .sea]
```

### Conforming via Extension

```swift
extension Character: Identifiable {
    var id: String { name }
}
```

### Value Type vs Reference Type

```swift
// Struct (value type) - copies
var dog1 = Dog(name: "Fido", age: 3)
var dog2 = dog1       // dog2 is a COPY
dog2.name = "Buddy"   // dog1.name still "Fido"

// Class (reference type) - shared
let car1 = Car()
let car2 = car1       // car2 points to SAME object
car2.color = "blue"   // car1.color is also "blue"
```

## Gotchas

- Forgetting `mutating` on struct methods that change properties causes a compile error
- `let` on a struct instance prevents ALL property changes; `let` on a class instance only prevents reassignment
- SwiftUI views are structs, so properties cannot change without `@State` or other property wrappers
- Extensions cannot add stored properties - only computed properties and methods
- `some View` is an opaque return type that hides the exact view type while conforming to `View`

## See Also

- [[swift-fundamentals]] - variables, types, functions
- [[swift-enums-and-optionals]] - enums, optionals, switch
- [[swiftui-state-and-data-flow]] - @State enables mutation in struct-based views
