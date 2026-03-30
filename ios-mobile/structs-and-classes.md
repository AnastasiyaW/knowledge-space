---
title: Structs and Classes in Swift
category: ios-mobile/language
tags: [swift, structs, classes, value-types, reference-types, instances, properties]
---

# Structs and Classes in Swift

## Key Facts

- Both structs and classes are blueprints for creating instances with properties and methods
- **Structs** are value types (copied on assignment); **classes** are reference types (shared on assignment)
- SwiftUI views are always structs (`struct ContentView: View { ... }`)
- Naming convention: types (struct/class) use `PascalCase`, variables use `camelCase`
- Structs get a free **memberwise initializer** - classes do not (must write `init` manually)
- Properties inside a struct/class are called **stored properties** when they hold a value directly
- [[enums-and-computed-properties]] can also be used inside structs and classes
- The `self` keyword refers to the current instance - every instance has its own implicit `self`
- Prefer structs in Swift unless you specifically need class features (inheritance, reference semantics)
- When a struct is used in [[swiftui-views]], it conforms to the `View` protocol and requires a `body` property

## Patterns

```swift
// Struct with memberwise initializer (automatic)
struct Dog {
    var name: String
    var age: Int
    var furColor: String
}

// Creating instances - struct memberwise init
let fido = Dog(name: "Fido", age: 7, furColor: "brown")
let poodles = Dog(name: "Poodles", age: 3, furColor: "white")

// Accessing properties
print(fido.name)   // "Fido"
print(poodles.age) // 3

// Class - requires manual property initialization
class Car {
    var year: Int = 0
    var color: String = ""
}

let myCar = Car()
myCar.year = 1992
myCar.color = "red"

// Struct as SwiftUI view
struct ContentView: View {
    @State var userText = ""

    var body: some View {
        Text(userText)
    }
}
```

```swift
// Value type (struct) vs Reference type (class)

// Struct - copy on assign
var dog1 = Dog(name: "Rex", age: 5, furColor: "black")
var dog2 = dog1       // dog2 is a COPY
dog2.name = "Max"     // Only dog2 changes
print(dog1.name)      // "Rex" (unchanged)

// Class - share on assign
let car1 = Car()
car1.color = "blue"
let car2 = car1       // car2 points to SAME object
car2.color = "red"
print(car1.color)     // "red" (changed!)
```

## Gotchas

- Changing `class` to `struct` (or vice versa) often compiles but introduces subtle behavioral differences due to value vs reference semantics
- Structs can use `let` for the instance if no properties need to change; classes can always mutate properties even with `let` instance
- `mutating` keyword is required on struct methods that modify properties; not needed for class methods
- SwiftUI views must be structs - using a class will cause compilation errors
- In Swift 6 with strict concurrency, class instances shared across threads require `@Sendable` conformance or actor isolation
- Class instances use `===` for identity comparison (same object) vs `==` for equality

## See Also

- [Structures and Classes](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/classesandstructures/)
- [[swift-fundamentals]]
- [[enums-and-computed-properties]]
