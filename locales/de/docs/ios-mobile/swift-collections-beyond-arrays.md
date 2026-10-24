---
title: "Swift-Collections jenseits von Arrays"
description: "Sets und Dictionaries in Swift mit Leistungsmerkmalen, Mengenoperationen und Zugriffsmustern"
level: 3
source_sha256: 945ba8a0368acbb4760a10fb652393d143d0cc93a3659964371df1b94541b7b2
translation: machine
translated_at: '2026-10-24'
---
# Swift-Collections jenseits von Arrays {#swift-collections-beyond-arrays}

Arrays sind die gebräuchlichste Collection, aber Swift bietet mit Sets und Dictionaries Typen für unterschiedliche Zugriffsmuster. Die Wahl des passenden Collection-Typs beeinflusst direkt Leistung und Korrektheit.

## Sets - ungeordnete eindeutige Elemente {#sets-unordered-unique-elements}

Ein Set speichert eindeutige Elemente ohne definierte Reihenfolge. Suche, Einfügen und Löschen sind im Durchschnitt O(1).

```swift
// Declaration
var numbers: Set<Int> = [1, 2, 3, 4, 5]

// Duplicates silently ignored
var withDupes: Set<Int> = [1, 2, 2, 3, 3, 3]
print(withDupes.count)  // 3

// Order is NOT guaranteed
print(numbers)  // could be {3, 1, 5, 2, 4} or any permutation
```

### Set-Operationen {#set-operations}

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

### Set-API {#set-api}

```swift
var fruits: Set<String> = ["apple", "banana"]

fruits.insert("cherry")     // inserts, returns (inserted: true, ...)
fruits.insert("apple")      // no-op, returns (inserted: false, ...)
fruits.remove("banana")     // removes by VALUE (not index - sets have no indices)
fruits.contains("apple")    // true - O(1) lookup
fruits.count                // element count
fruits.isEmpty              // boolean check
```

### Wann Sets verwenden {#when-to-use-sets}

| Anwendungsfall | Array | Set |
|----------|-------|-----|
| Geordnete Daten | Ja | Nein |
| Indexbasierter Zugriff | Ja | Nein |
| Schnelle Mitgliedschaftsprüfung | O(n) | O(1) |
| Garantierte Eindeutigkeit | Manuell | Automatisch |
| Duplikate erlaubt | Ja | Nein |
| Mathematische Operationen | Manuell | Eingebaut |

## Dictionaries - Schlüssel-Wert-Paare {#dictionaries-key-value-pairs}

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

### Dictionaries iterieren {#iterating-dictionaries}

```swift
for (key, value) in user {
    print("\(key): \(value)")
}

// Keys and values as separate collections
let keys = Array(user.keys)
let values = Array(user.values)
```

## Higher-Order-Funktionen auf Collections {#higher-order-functions-on-collections}

Alle Swift-Collections unterstützen `map`, `filter`, `reduce`, `compactMap` und `flatMap`:

### map - jedes Element transformieren {#map-transform-each-element}

```swift
let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }        // [2, 4, 6, 8, 10]
let strings = numbers.map { String($0) }     // ["1", "2", "3", "4", "5"]

// map returns same-sized collection with potentially different type
let isEven = numbers.map { $0 % 2 == 0 }    // [false, true, false, true, false]
```

### filter - Elemente auswählen {#filter-select-elements}

```swift
let evens = numbers.filter { $0 % 2 == 0 }  // [2, 4]
```

### reduce - zu einem einzelnen Wert aggregieren {#reduce-aggregate-to-single-value}

```swift
let sum = numbers.reduce(0, +)               // 15
let product = numbers.reduce(1, *)           // 120
```

### compactMap - transformieren und nil entfernen {#compactmap-transform-remove-nils}

```swift
let strings = ["1", "two", "3", "four", "5"]
let ints = strings.compactMap { Int($0) }    // [1, 3, 5]
```

## Stringinterpolation {#string-interpolation}

Swift verwendet die Syntax `\()`, um Werte in Strings einzubetten:

```swift
let name = "Anna"
let greeting = "Hello, \(name)!"          // "Hello, Anna!"
let calc = "2 * 5 = \(2 * 5)"            // "2 * 5 = 10"

// Works with any expression
let price = 9.99
let formatted = "Price: $\(price)"        // "Price: $9.99"
```

Dies unterscheidet sich von der Verkettung und vermeidet die Probleme mit Leerzeichen, die beim Übergeben mehrerer Argumente an `print()` entstehen.

## Stolperfallen {#gotchas}

- **Set-Elemente müssen `Hashable` sein.** Eigene Typen müssen `Hashable` implementieren, um in einem Set gespeichert oder als Dictionary-Schlüssel verwendet zu werden.
- **Dictionary-Zugriff liefert ein Optional.** Immer sicher auspacken: `if let value = dict["key"]` oder Standardwerte verwenden: `dict["key", default: 0]`.
- **Die Reihenfolge eines Set ist zufällig.** Die Iterationsreihenfolge eines Set sollte nicht vorausgesetzt werden; sie kann sich zwischen Ausführungen ändern. Wenn die Reihenfolge wichtig ist, ein Array verwenden und die Eindeutigkeit manuell sicherstellen.
- **`map` auf einem Dictionary liefert ein Array von Tupeln**, kein neues Dictionary. Um aus einer Transformation ein neues Dictionary zu erzeugen, `Dictionary(uniqueKeysWithValues: dict.map { ... })` oder `mapValues` verwenden.

## Querverweise {#cross-references}

- [[swift-fundamentals]] - Grundtypen, Variablen, Konstanten
- [[swift-enums-and-optionals]] - Optional-Behandlung beim Dictionary-Zugriff
- [[swift-generics]] - generische Collection-Typen
- [[swiftui-lists-and-grids]] - Darstellung von Collections in der UI
