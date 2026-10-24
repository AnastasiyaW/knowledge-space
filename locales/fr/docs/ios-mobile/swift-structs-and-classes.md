---
title: "Structs et classes Swift"
category: concepts
tags: [ios-mobile, swift, structs, classes, protocols, value-types, reference-types]
level: 3
source_sha256: c4a8f0a4d6ba7c90e214518a671f94eb7d4cb68b556c281862951d188c918593
translation: machine
translated_at: '2026-10-24'
---
# Structs et classes Swift {#swift-structs-and-classes}

Les structs et les classes sont des modèles pour définir des types personnalisés en Swift. Apple recommande d'utiliser les structs par défaut. Les classes sont nécessaires pour la sémantique par référence, l'héritage, ou lorsqu'elles sont utilisées avec des frameworks qui les exigent (Core Data, @Observable).

## Points clés {#key-facts}

- Les structs sont des types valeur (copiés lors de l'affectation), les classes sont des types référence (partagés)
- Apple recommande le struct par défaut, sauf si des fonctionnalités propres aux classes sont nécessaires
- Le mot-clé `mutating` est requis pour les méthodes de struct qui modifient des propriétés
- Chaque vue SwiftUI est un struct qui adopte le protocole `View`
- Une classe `final` ne peut pas être sous-classée (exigence de `@Model` de SwiftData)
- Les structs reçoivent gratuitement un initialiseur memberwise ; les classes nécessitent un `init` explicite
- `self` désigne l'instance courante à l'intérieur des méthodes

## Modèles {#patterns}

### Définition d'un struct {#struct-definition}

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

### Méthodes sur les structs {#methods-on-structs}

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

### Définition d'une classe {#class-definition}

```swift
class Car {
    var year: Int = 2020
    var color: String = "red"
}

let myCar = Car()
myCar.color = "blue"   // OK: let prevents reassignment, not property changes
```

### Propriétés stockées et propriétés calculées {#stored-vs-computed-properties}

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

### Protocoles {#protocols}

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

### Conformité via une extension {#conforming-via-extension}

```swift
extension Character: Identifiable {
    var id: String { name }
}
```

### Type valeur ou type référence {#value-type-vs-reference-type}

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

## Pièges {#gotchas}

- Oublier `mutating` sur une méthode de struct qui modifie des propriétés provoque une erreur de compilation
- `let` sur une instance de struct empêche TOUTE modification de propriété ; `let` sur une instance de classe empêche seulement la réaffectation
- Les vues SwiftUI sont des structs, donc leurs propriétés ne peuvent pas changer sans `@State` ou d'autres property wrappers
- Les extensions ne peuvent pas ajouter de propriétés stockées, seulement des propriétés calculées et des méthodes
- `some View` est un type de retour opaque qui masque le type exact de la vue tout en se conformant à `View`

## Voir aussi {#see-also}

- [[swift-fundamentals]] - variables, types, fonctions
- [[swift-enums-and-optionals]] - enums, optionnels, switch
- [[swiftui-state-and-data-flow]] - @State permet la mutation dans les vues basées sur des structs
