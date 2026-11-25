---
title: "Swift-Structs und Klassen"
category: concepts
tags: [ios-mobile, swift, structs, classes, protocols, value-types, reference-types]
level: 3
source_sha256: c4a8f0a4d6ba7c90e214518a671f94eb7d4cb68b556c281862951d188c918593
translation: machine
translated_at: '2026-10-24'
---
# Swift-Structs und Klassen {#swift-structs-and-classes}

Structs und Klassen sind Baupläne für benutzerdefinierte Typen in Swift. Apple empfiehlt, standardmäßig Structs zu verwenden. Klassen werden für Referenzsemantik, Vererbung oder bei der Verwendung mit Frameworks benötigt, die sie voraussetzen (Core Data, @Observable).

## Wichtige Fakten {#key-facts}

- Structs sind Wertetypen (werden bei der Zuweisung kopiert), Klassen sind Referenztypen (werden geteilt)
- Apple empfiehlt, standardmäßig Structs zu verwenden, sofern keine klassenspezifischen Funktionen benötigt werden
- Das Schlüsselwort `mutating` ist für Struct-Methoden erforderlich, die Eigenschaften verändern
- Jede SwiftUI-View ist ein Struct, das dem Protokoll `View` entspricht
- Eine `final`-Klasse kann nicht unterklassifiziert werden (erforderlich für `@Model` von SwiftData)
- Structs erhalten einen kostenlosen memberweisen Initialisierer; Klassen erfordern einen expliziten `init`
- `self` verweist innerhalb von Methoden auf die aktuelle Instanz

## Muster {#patterns}

### Struct-Definition {#struct-definition}

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

### Methoden auf Structs {#methods-on-structs}

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

### Klassendefinition {#class-definition}

```swift
class Car {
    var year: Int = 2020
    var color: String = "red"
}

let myCar = Car()
myCar.color = "blue"   // OK: let prevents reassignment, not property changes
```

### Gespeicherte vs. berechnete Eigenschaften {#stored-vs-computed-properties}

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

### Protokolle {#protocols}

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

### Konformität über Extension {#conforming-via-extension}

```swift
extension Character: Identifiable {
    var id: String { name }
}
```

### Wertetyp vs. Referenztyp {#value-type-vs-reference-type}

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

## Stolperfallen {#gotchas}

- Das Vergessen von `mutating` bei Struct-Methoden, die Eigenschaften ändern, führt zu einem Kompilierfehler
- `let` bei einer Struct-Instanz verhindert ALLE Eigenschaftsänderungen; `let` bei einer Klasseninstanz verhindert nur die Neuzuweisung
- SwiftUI-Views sind Structs, daher können Eigenschaften ohne `@State` oder andere Property-Wrapper nicht geändert werden
- Extensions können keine gespeicherten Eigenschaften hinzufügen – nur berechnete Eigenschaften und Methoden
- `some View` ist ein undurchsichtiger Rückgabetyp, der den genauen View-Typ verbirgt, während er dem Protokoll `View` entspricht

## Siehe auch {#see-also}

- [[swift-fundamentals]] - Variablen, Typen, Funktionen
- [[swift-enums-and-optionals]] - Enums, Optionals, switch
- [[swiftui-state-and-data-flow]] - @State ermöglicht Mutation in Struct-basierten Views
