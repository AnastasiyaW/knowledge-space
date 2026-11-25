---
title: "Collections Swift au-delà des tableaux"
description: "Set et Dictionary en Swift : caractéristiques de performance, opérations ensemblistes et modes d'accès"
level: 3
source_sha256: 945ba8a0368acbb4760a10fb652393d143d0cc93a3659964371df1b94541b7b2
translation: machine
translated_at: '2026-10-24'
---
# Collections Swift au-delà des tableaux {#swift-collections-beyond-arrays}

Les tableaux sont la collection la plus courante, mais Swift fournit les Set et les Dictionary pour d'autres modes d'accès. Le choix du type de collection a un impact direct sur les performances et la justesse du code.

## Set - Éléments uniques non ordonnés {#sets-unordered-unique-elements}

Un Set stocke des éléments uniques sans ordre défini. La recherche, l'insertion et la suppression sont en O(1) en moyenne.

```swift
// Declaration
var numbers: Set<Int> = [1, 2, 3, 4, 5]

// Duplicates silently ignored
var withDupes: Set<Int> = [1, 2, 2, 3, 3, 3]
print(withDupes.count)  // 3

// Order is NOT guaranteed
print(numbers)  // could be {3, 1, 5, 2, 4} or any permutation
```

### Opérations sur les Set {#set-operations}

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

### API des Set {#set-api}

```swift
var fruits: Set<String> = ["apple", "banana"]

fruits.insert("cherry")     // inserts, returns (inserted: true, ...)
fruits.insert("apple")      // no-op, returns (inserted: false, ...)
fruits.remove("banana")     // removes by VALUE (not index - sets have no indices)
fruits.contains("apple")    // true - O(1) lookup
fruits.count                // element count
fruits.isEmpty              // boolean check
```

### Quand utiliser un Set {#when-to-use-sets}

| Cas d'usage | Array | Set |
|-------------|-------|-----|
| Données ordonnées | Oui | Non |
| Accès par index | Oui | Non |
| Test d'appartenance rapide | O(n) | O(1) |
| Unicité garantie | Manuel | Automatique |
| Doublons autorisés | Oui | Non |
| Opérations mathématiques | Manuel | Intégré |

## Dictionary - Paires clé-valeur {#dictionaries-key-value-pairs}

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

### Parcourir un Dictionary {#iterating-dictionaries}

```swift
for (key, value) in user {
    print("\(key): \(value)")
}

// Keys and values as separate collections
let keys = Array(user.keys)
let values = Array(user.values)
```

## Fonctions d'ordre supérieur sur les collections {#higher-order-functions-on-collections}

Toutes les collections Swift prennent en charge `map`, `filter`, `reduce`, `compactMap`, `flatMap` :

### map - Transformer chaque élément {#map-transform-each-element}

```swift
let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }        // [2, 4, 6, 8, 10]
let strings = numbers.map { String($0) }     // ["1", "2", "3", "4", "5"]

// map returns same-sized collection with potentially different type
let isEven = numbers.map { $0 % 2 == 0 }    // [false, true, false, true, false]
```

### filter - Sélectionner des éléments {#filter-select-elements}

```swift
let evens = numbers.filter { $0 % 2 == 0 }  // [2, 4]
```

### reduce - Agréger en une seule valeur {#reduce-aggregate-to-single-value}

```swift
let sum = numbers.reduce(0, +)               // 15
let product = numbers.reduce(1, *)           // 120
```

### compactMap - Transformer et retirer les nil {#compactmap-transform-remove-nils}

```swift
let strings = ["1", "two", "3", "four", "5"]
let ints = strings.compactMap { Int($0) }    // [1, 3, 5]
```

## Interpolation de chaînes {#string-interpolation}

Swift utilise la syntaxe `\()` pour intégrer des valeurs dans les chaînes :

```swift
let name = "Anna"
let greeting = "Hello, \(name)!"          // "Hello, Anna!"
let calc = "2 * 5 = \(2 * 5)"            // "2 * 5 = 10"

// Works with any expression
let price = 9.99
let formatted = "Price: $\(price)"        // "Price: $9.99"
```

Cette approche se distingue de la concaténation et évite les problèmes d'espacement liés au passage de plusieurs arguments à `print()`.

## Pièges courants {#gotchas}

- **Les éléments d'un Set doivent être Hashable.** Les types personnalisés doivent se conformer à `Hashable` pour être stockés dans un Set ou utilisés comme clés de Dictionary.
- **L'accès à un Dictionary renvoie un Optional.** Déballez toujours la valeur de manière sûre : `if let value = dict["key"]`, ou utilisez une valeur par défaut : `dict["key", default: 0]`.
- **L'ordre de parcours d'un Set est aléatoire.** Ne vous fiez pas à l'ordre d'itération d'un Set : il peut changer d'une exécution à l'autre. Si l'ordre compte, utilisez un Array et garantissez manuellement l'unicité.
- **`map` sur un Dictionary renvoie un Array de tuples**, et non un nouveau Dictionary. Pour créer un nouveau dictionnaire à partir d'une transformation, utilisez `Dictionary(uniqueKeysWithValues: dict.map { ... })` ou `mapValues`.

## Références croisées {#cross-references}

- [[swift-fundamentals]] - types de base, variables, constantes
- [[swift-enums-and-optionals]] - gestion des Optional pour l'accès aux dictionnaires
- [[swift-generics]] - types de collections génériques
- [[swiftui-lists-and-grids]] - affichage de collections dans l'interface utilisateur
