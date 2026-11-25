---
title: "Enums et optionnels en Swift"
category: concepts
tags: [ios-mobile, swift, enums, optionals, switch, pattern-matching, codable]
level: 3
source_sha256: c1745156be4ce47fae5ab9fec094b5e023753b1360d449de21d36b7cad1e8938
translation: machine
translated_at: '2026-10-24'
---
# Enums et optionnels en Swift {#swift-enums-and-optionals}

Les enums définissent un ensemble fini de cas nommés. Les optionnels représentent des valeurs qui peuvent exister ou non. Associés aux instructions `switch`, ils forment le système de pattern matching puissant de Swift, largement utilisé dans SwiftUI pour la gestion d'état et le traitement des données.

## Points clés {#key-facts}

- Les enums peuvent avoir des valeurs brutes (String, Int, Double) et des propriétés calculées
- La conformité à `CaseIterable` fournit le tableau `.allCases` pour l'itération
- Les optionnels se déclarent avec le suffixe `?` : `var death: Death?`
- `nil` représente l'absence de valeur
- Le `switch` de Swift doit être exhaustif : couvrir tous les cas ou utiliser `default`
- `guard let` est préféré pour les sorties anticipées ; `if let` pour les blocs conditionnels
- Le force unwrap `!` ne doit être utilisé que lorsque `nil` constitue une erreur de programmation

## Modèles {#patterns}

### Enum avec valeurs brutes {#enum-with-raw-values}

```swift
enum Currency: Double, CaseIterable {
    case copperPenny = 0.01
    case silverPenny = 0.1
    case silverSickle = 1.0
    case goldSickle = 10.0
    case goldGalleon = 100.0
}

// Access raw value
Currency.goldGalleon.rawValue  // 100.0

// Iterate all cases
for currency in Currency.allCases {
    print(currency)
}
```

### Propriétés calculées sur les enums {#computed-properties-on-enums}

```swift
enum APType: String, Decodable, CaseIterable {
    case land
    case air
    case sea
}

enum Currency: Double {
    case copperPenny = 0.01
    // ...

    var name: String {
        switch self {
        case .copperPenny: return "Copper Penny"
        case .silverPenny: return "Silver Penny"
        // ... etc
        }
    }

    var image: Image {
        switch self {
        case .copperPenny: return Image(.copperPenny)
        // ... etc
        }
    }
}
```

### Méthodes sur les enums via une extension {#methods-on-enums-via-extension}

```swift
extension Currency {
    func convert(_ amountString: String, to currency: Currency) -> String {
        guard let doubleAmount = Double(amountString) else { return "" }
        let convertedAmount = (doubleAmount / self.rawValue) * currency.rawValue
        return String(convertedAmount)
    }
}

// Usage
leftCurrency.convert(leftAmount, to: rightCurrency)
```

### Enum pour le suivi d'état {#enum-for-state-tracking}

```swift
enum FetchStatus {
    case notStarted
    case fetching
    case success
    case failed(error: Error)    // associated value
}

enum BookStatus {
    case active
    case inactive
    case locked
}
```

### Instruction switch {#switch-statement}

```swift
switch vm.status {
case .notStarted:
    EmptyView()
case .fetching:
    ProgressView()
case .success:
    Text("Data loaded")
case .failed(let error):         // extract associated value
    Text(error.localizedDescription)
}
```

Le `switch` doit être exhaustif : couvrir tous les cas ou utiliser `default`.

### Optionnels {#optionals}

```swift
var death: Death? = nil      // optional Death - no value yet

// 1. if let (safe unwrap)
if let death = character.death {
    Text(death.cause)        // only runs if death is not nil
}

// 2. guard let (early exit)
guard let url = URL(string: urlString) else { return nil }

// 3. nil coalescing
let name = character.death?.responsible ?? "Unknown"

// 4. Optional chaining
let responsible = character.death?.responsible   // nil if death is nil

// 5. Force unwrap (!) - only when certain non-nil
URL(string: "https://apple.com")!
```

### Optionnels dans les modèles Codable {#optionals-in-codable-models}

```swift
struct Character: Decodable {
    let name: String
    var death: Death?          // optional - nil if key absent in JSON
}
```

`JSONDecoder` laisse les propriétés optionnelles à `nil` lorsque la clé est absente des données JSON.

## Pièges {#gotchas}

- Le force unwrap (`!`) d'une valeur `nil` fait planter l'application à l'exécution : à utiliser uniquement lorsque la valeur est garantie
- `guard let` doit quitter la portée englobante (return, break, continue, throw)
- Les valeurs brutes d'un enum doivent être uniques et du même type
- `ForEach` dans SwiftUI n'accepte que les intervalles semi-ouverts (`0..<5`), et non les intervalles fermés (`0...4`)
- Comparaisons d'optionnels : `nil == nil` vaut `true`, mais `nil < 0` ne compile pas sans typage explicite
- Lors de l'utilisation d'enums avec `Picker`, encapsuler le type optionnel : `Text("All").tag(APType?.none)` pour le cas `nil`

## Voir aussi {#see-also}

- [[swift-fundamentals]] - variables, types, structures de contrôle
- [[swift-structs-and-classes]] - protocoles, propriétés calculées
- [[swiftui-networking]] - enums pour le suivi du statut des requêtes
- [[swiftui-state-and-data-flow]] - utilisation des enums avec @State
