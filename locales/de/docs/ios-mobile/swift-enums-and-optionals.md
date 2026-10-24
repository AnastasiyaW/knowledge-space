---
title: "Swift-Enums und Optionals"
category: concepts
tags: [ios-mobile, swift, enums, optionals, switch, pattern-matching, codable]
level: 3
source_sha256: c1745156be4ce47fae5ab9fec094b5e023753b1360d449de21d36b7cad1e8938
translation: machine
translated_at: '2026-10-24'
---
# Swift-Enums und Optionals {#swift-enums-and-optionals}

Enums definieren eine endliche Menge benannter Fälle. Optionals repräsentieren Werte, die vorhanden sein können oder auch nicht. Zusammen mit `switch`-Anweisungen bilden sie das leistungsfähige Pattern-Matching-System von Swift, das in SwiftUI umfassend für Zustandsverwaltung und Datenverarbeitung eingesetzt wird.

## Wichtige Fakten {#key-facts}

- Enums können Raw Values (String, Int, Double) und berechnete Eigenschaften haben
- Die Konformität zu `CaseIterable` stellt das Array `.allCases` zur Iteration bereit
- Optionals werden mit dem Suffix `?` deklariert: `var death: Death?`
- `nil` repräsentiert das Fehlen eines Wertes
- Ein `switch` in Swift muss erschöpfend sein: Entweder alle Fälle abdecken oder `default` verwenden
- `guard let` wird für frühe Ausstiege bevorzugt, `if let` für bedingte Blöcke
- Der Force-Unwrap `!` sollte nur verwendet werden, wenn `nil` einen Programmierfehler darstellt

## Muster {#patterns}

### Enum mit Raw Values {#enum-with-raw-values}

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

### Berechnete Eigenschaften auf Enums {#computed-properties-on-enums}

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

### Methoden auf Enums über eine Extension {#methods-on-enums-via-extension}

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

### Enum zur Zustandsverfolgung {#enum-for-state-tracking}

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

### Switch-Anweisung {#switch-statement}

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

Ein `switch` muss erschöpfend sein: Entweder alle Fälle abdecken oder `default` verwenden.

### Optionals {#optionals}

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

### Optionals in Codable-Modellen {#optionals-in-codable-models}

```swift
struct Character: Decodable {
    let name: String
    var death: Death?          // optional - nil if key absent in JSON
}
```

`JSONDecoder` belässt optionale Eigenschaften als `nil`, wenn der Schlüssel in den JSON-Daten fehlt.

## Fallstricke {#gotchas}

- Ein Force-Unwrap (`!`) auf einen `nil`-Wert führt zur Laufzeit zum Absturz der App; nur verwenden, wenn der Wert garantiert vorhanden ist
- `guard let` muss den umgebenden Scope verlassen (`return`, `break`, `continue`, `throw`)
- Raw Values von Enums müssen eindeutig und vom selben Typ sein
- `ForEach` in SwiftUI akzeptiert nur halboffene Bereiche (`0..<5`), nicht geschlossene Bereiche (`0...4`)
- Optionale Vergleiche: `nil == nil` ist `true`, aber `nil < 0` lässt sich ohne explizite Typangabe nicht kompilieren
- Bei der Verwendung von Enums mit `Picker` den optionalen Typ umschließen: `Text("All").tag(APType?.none)` für den `nil`-Fall

## Siehe auch {#see-also}

- [[swift-fundamentals]] - Variablen, Typen, Kontrollfluss
- [[swift-structs-and-classes]] - Protokolle, berechnete Eigenschaften
- [[swiftui-networking]] - Enums zur Verfolgung des Abrufstatus
- [[swiftui-state-and-data-flow]] - Verwendung von Enums mit `@State`
