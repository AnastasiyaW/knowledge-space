---
title: "Principes fondamentaux du langage Swift"
category: concepts
tags: [ios-mobile, swift, variables, types, functions, control-flow]
level: 3
source_sha256: 2889b62110918fcee9fdbd3757935084666837d1789d8d4130d4a7d0d37b7187
translation: machine
translated_at: '2026-10-24'
---
# Principes fondamentaux du langage Swift {#swift-language-fundamentals}

Les constructions de base du langage Swift : variables, constantes, types, opérateurs, structures de contrôle, fonctions et manipulation de chaînes. Ce sont les briques de base utilisées dans tous les projets Swift et SwiftUI.

## Points clés {#key-facts}

- Swift est fortement typé avec inférence de types : une fois le type défini, il ne peut plus changer
- `var` déclare des variables mutables, `let` déclare des constantes immuables
- Utilisez `let` par défaut ; passez à `var` uniquement lorsque la mutabilité est nécessaire
- L'interpolation de chaînes utilise la syntaxe `\(expression)` à l'intérieur de guillemets doubles
- Swift utilise des paramètres nommés dans les appels de fonction par défaut
- Commentaires : `//` pour une ligne, `/* */` pour plusieurs lignes, `Cmd+/` pour basculer dans Xcode
- Swift Playgrounds (Fichier > Nouveau > Playground) fournit un environnement similaire à un REPL pour l'expérimentation

## Modèles {#patterns}

### Variables et constantes {#variables-and-constants}

```swift
// var = mutable
var age = 34
age = 35           // OK
age += 1           // shorthand: age = age + 1

// let = immutable
let kilosToPounds = 2.2
// kilosToPounds = 2.5  // ERROR: cannot change constant
```

Noms de variables : camelCase, sans espaces, sensibles à la casse.

### Système de types {#type-system}

```swift
var age: Int = 34          // whole number
var price: Double = 2.99   // decimal number
var name: String = "Nick"  // text (always double quotes)
var isHot: Bool = true     // true or false only
```

Les incompatibilités de types sont des erreurs de compilation : `age = 4.5` échoue si `age` est un `Int`.

### Interpolation de chaînes et méthodes {#string-interpolation-and-methods}

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

### Structures de contrôle {#control-flow}

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

### Tableaux {#arrays}

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

### Boucles for {#for-loops}

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

### Fonctions {#functions}

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

### Opérateurs mathématiques {#math-operators}

```swift
+  -  *  /  %       // basic arithmetic
+=  -=  *=  /=      // compound assignment
```

### Contrôle d'accès {#access-control}

```swift
private var secret = "hidden"              // only this file
private(set) var count = 0                 // readable anywhere, writable only in this type
internal var normal = "default"            // same module (default)
public var exposed = "visible"             // any module
```

### Extensions {#extensions}

Ajoutez des fonctionnalités à des types existants sans les modifier :

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

Règle : les extensions ne peuvent contenir que des propriétés calculées et des fonctions, pas de propriétés stockées.

### Gestion des dates {#date-handling}

```swift
var date = Date()              // current date/time
date.formatted()               // localized string
date.formatted(date: .long, time: .omitted)  // "April 1, 2025"
```

## Pièges courants {#gotchas}

- `let` et `var` avec des types référence : `let myCar = Car()` permet toujours de modifier les propriétés de l'instance de classe ; `let` empêche uniquement de réassigner la référence elle-même
- Les propriétés `.first` et `.last` d'un tableau renvoient des optionnels, et non la valeur brute
- L'interpolation de chaînes évalue les expressions : `"Result: \(2 + 3)"` produit `"Result: 5"`
- La division de deux `Int` donne un résultat `Int` : `7 / 2` vaut `3`, et non `3.5`
- `.capitalized` est une propriété (sans parenthèses), tandis que `.uppercased()` et `.lowercased()` sont des méthodes
- La sortie de `print()` va dans la console Xcode : utile pour le débogage, mais non visible dans l'interface de l'application

## Voir aussi {#see-also}

- [[swift-enums-and-optionals]] - énumérations, switch, optionnels, filtrage par motif
- [[swift-structs-and-classes]] - types valeur et types référence, méthodes, protocoles
- [[swiftui-views-and-modifiers]] - utilisation de Swift dans les vues SwiftUI
