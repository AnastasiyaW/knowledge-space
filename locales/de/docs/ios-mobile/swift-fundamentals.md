---
title: "Swift-Sprachgrundlagen"
category: concepts
tags: [ios-mobile, swift, variables, types, functions, control-flow]
level: 3
source_sha256: 2889b62110918fcee9fdbd3757935084666837d1789d8d4130d4a7d0d37b7187
translation: machine
translated_at: '2026-10-24'
---
# Swift-Sprachgrundlagen {#swift-language-fundamentals}

Grundlegende Sprachkonstrukte von Swift: Variablen, Konstanten, Typen, Operatoren, Kontrollfluss, Funktionen und Stringverarbeitung. Diese Bausteine werden in jedem Swift- und SwiftUI-Projekt verwendet.

## Wichtige Fakten {#key-facts}

- Swift ist stark typisiert und nutzt Typinferenz: Sobald ein Typ festgelegt ist, kann er sich nicht mehr ändern
- `var` deklariert veränderliche Variablen, `let` deklariert unveränderliche Konstanten
- Verwende standardmäßig `let`; wechsle nur dann zu `var`, wenn Veränderlichkeit benötigt wird
- Stringinterpolation verwendet die Syntax `\(expression)` innerhalb von doppelten Anführungszeichen
- Swift verwendet bei Funktionsaufrufen standardmäßig benannte Parameter
- Kommentare: `//` für einzeilige, `/* */` für mehrzeilige Kommentare, `Cmd+/` zum Umschalten in Xcode
- Swift Playgrounds (Ablage > Neu > Playground) bieten eine REPL-ähnliche Umgebung zum Experimentieren

## Muster {#patterns}

### Variablen und Konstanten {#variables-and-constants}

```swift
// var = mutable
var age = 34
age = 35           // OK
age += 1           // shorthand: age = age + 1

// let = immutable
let kilosToPounds = 2.2
// kilosToPounds = 2.5  // ERROR: cannot change constant
```

Variablennamen: camelCase, ohne Leerzeichen, case-sensitiv.

### Typsystem {#type-system}

```swift
var age: Int = 34          // whole number
var price: Double = 2.99   // decimal number
var name: String = "Nick"  // text (always double quotes)
var isHot: Bool = true     // true or false only
```

Typkonflikte sind Fehler zur Kompilierzeit: `age = 4.5` schlägt fehl, wenn `age` vom Typ `Int` ist.

### Stringinterpolation und Methoden {#string-interpolation-and-methods}

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

### Kontrollfluss {#control-flow}

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

### Arrays {#arrays}

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

### For-Schleifen {#for-loops}

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

### Funktionen {#functions}

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

### Mathematische Operatoren {#math-operators}

```swift
+  -  *  /  %       // basic arithmetic
+=  -=  *=  /=      // compound assignment
```

### Zugriffskontrolle {#access-control}

```swift
private var secret = "hidden"              // only this file
private(set) var count = 0                 // readable anywhere, writable only in this type
internal var normal = "default"            // same module (default)
public var exposed = "visible"             // any module
```

### Extensions {#extensions}

Fügen Sie bestehenden Typen Funktionalität hinzu, ohne sie zu verändern:

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

Regel: Extensions können nur berechnete Eigenschaften und Funktionen enthalten, keine gespeicherten Eigenschaften.

### Datumsverarbeitung {#date-handling}

```swift
var date = Date()              // current date/time
date.formatted()               // localized string
date.formatted(date: .long, time: .omitted)  // "April 1, 2025"
```

## Stolperfallen {#gotchas}

- `let` vs. `var` bei Referenztypen: `let myCar = Car()` erlaubt weiterhin Änderungen an Eigenschaften der Klasseninstanz – `let` verhindert nur das Neuzuweisen der Referenz selbst
- Die Eigenschaften `.first` und `.last` von Arrays geben Optionals zurück, nicht den reinen Wert
- Stringinterpolation wertet Ausdrücke aus: `"Result: \(2 + 3)"` ergibt `"Result: 5"`
- Die Division zweier `Int`-Werte ergibt ein `Int`-Ergebnis: `7 / 2` ergibt `3`, nicht `3.5`
- `.capitalized` ist eine Eigenschaft (ohne Klammern), während `.uppercased()` und `.lowercased()` Methoden sind
- Die Ausgabe von `print()` erscheint in der Xcode-Konsole – nützlich zum Debuggen, aber nicht in der App-Oberfläche sichtbar

## Siehe auch {#see-also}

- [[swift-enums-and-optionals]] - Enums, switch, Optionals, Pattern Matching
- [[swift-structs-and-classes]] - Werttypen vs. Referenztypen, Methoden, Protokolle
- [[swiftui-views-and-modifiers]] - Verwendung von Swift in SwiftUI-Views
