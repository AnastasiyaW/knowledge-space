---
title: "StoreKit 2 In-App-Käufe"
category: concepts
tags: [ios-mobile, swiftui, storekit, iap, in-app-purchases, monetization]
level: 3
source_sha256: 2238f63a6b3f0562b0069240af9861c657d7184ee89e378c8dd24f716e0aac76
translation: machine
translated_at: '2026-10-24'
---
# StoreKit 2 In-App-Käufe {#storekit-2-in-app-purchases}

StoreKit 2 ist Apples moderne API für In-App-Käufe. Sie verwendet async/await, bietet eine integrierte Belegprüfung und vereinfacht den Kaufablauf im Vergleich zu StoreKit 1. Dieser Eintrag behandelt Non-Consumable-Käufe und das Testen über StoreKit-Konfigurationsdateien.

## Key Facts {#key-facts}

- StoreKit 2 verwendet `Product.products(for:)`, um verfügbare Produkte abzurufen
- `product.purchase()` öffnet das systemseitige Kaufblatt
- `Transaction.updates` überwacht Käufe, die außerhalb der App getätigt werden
- Kaufergebnisse umfassen die Fälle `.success`, `.userCancelled` und `.pending`
- Verifizierte Transaktionen enthalten `signedType.productID`, um zu erfassen, was gekauft wurde
- Die StoreKit-Konfigurationsdatei (`.storekit`) ermöglicht Tests ohne App Store Connect
- Non-Consumable = einmal kaufen, dauerhaft gültig; Consumable = wiederholt kaufbar; Abonnement = wiederkehrend

## Patterns {#patterns}

### Setup: StoreKit-Konfigurationsdatei {#setup-storekit-configuration-file}

1. Neue Datei > StoreKit-Konfigurationsdatei
2. Auf `+` klicken > Non-Consumable In-App-Kauf hinzufügen
3. Reference Name (z. B. `HP4`), Product ID (z. B. `hp4`) und Preis festlegen
4. Display Name und Beschreibung hinzufügen
5. Produkt > Schema > Schema bearbeiten > StoreKit-Konfiguration: die Datei auswählen

### Store-Klasse {#store-class}

```swift
import StoreKit

@MainActor
class Store: ObservableObject {
    @Published var books: [BookStatus] = [
        .active, .active, .inactive,
        .locked, .locked, .locked, .locked
    ]
    @Published var products: [Product] = []
    @Published var purchasedIDs = Set<String>()

    private let productIDs = ["hp4", "hp5", "hp6", "hp7"]
    private var updates: Task<Void, Never>? = nil

    init() {
        updates = watchForUpdates()
    }

    func loadProducts() async {
        do {
            products = try await Product.products(for: productIDs)
        } catch {
            print("Couldn't fetch products: \(error)")
        }
    }

    func purchase(_ product: Product) async {
        do {
            let result = try await product.purchase()

            switch result {
            case .success(let verificationResult):
                switch verificationResult {
                case .unverified(_, let error):
                    print("Purchase unverified: \(error)")
                case .verified(let signedType):
                    purchasedIDs.insert(signedType.productID)
                @unknown default:
                    break
                }
            case .userCancelled:
                break
            case .pending:
                break   // waiting for parent approval
            @unknown default:
                break
            }
        } catch {
            print("Couldn't purchase: \(error)")
        }
    }

    func checkPurchased() async {
        for product in products {
            guard let state = await product.currentEntitlement else { return }

            switch state {
            case .unverified(_, let error):
                print("Error: \(error)")
            case .verified(let signedType):
                if signedType.revocationDate == nil {
                    purchasedIDs.insert(signedType.productID)
                } else {
                    purchasedIDs.remove(signedType.productID)
                }
            @unknown default:
                break
            }
        }
    }

    private func watchForUpdates() -> Task<Void, Never> {
        Task(priority: .background) {
            for await _ in Transaction.updates {
                await checkPurchased()
            }
        }
    }
}
```

### Store über EnvironmentObject injizieren {#injecting-store-via-environmentobject}

```swift
@main
struct HPTriviaApp: App {
    @StateObject private var store = Store()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(store)
        }
    }
}

// In any child view
struct SettingsView: View {
    @EnvironmentObject var store: Store

    var body: some View {
        ForEach(0..<7) { i in
            if store.books[i] == .active { ... }
            else if store.books[i] == .locked { ... }
        }
    }
}
```

### Produkte beim Erscheinen der View laden {#loading-products-on-view-appear}

```swift
.task {
    await store.loadProducts()
    await store.checkPurchased()
}
```

### IAP-Typen {#iap-types}

| Typ | Kauf | Anwendungsfall |
|------|----------|---------|
| Non-consumable | Einmalig, dauerhaft | Funktionen/Inhalte freischalten |
| Consumable | Wiederholt kaufbar | Spielwährung, Leben |
| Nicht verlängerbares Abonnement | Manuelle Verlängerung | Saisonaler Zugang |
| Automatisch verlängerbares Abonnement | Automatische Abrechnung | Laufender Dienst |

### Zusammenfassung des Kaufablaufs {#purchase-flow-summary}

1. `.storekit`-Konfigurationsdatei mit Product IDs erstellen
2. Schema so einstellen, dass es diese Konfigurationsdatei für Tests verwendet
3. `Product.products(for: productIDs)` - Metadaten abrufen
4. `product.purchase()` - Kaufblatt öffnen
5. Ergebnis auswerten: `.success` > `.verified(signedType)` > `productID` zu `purchasedIDs` hinzufügen
6. `product.currentEntitlement` - bestehende Käufe prüfen (beim Start und nach Updates)
7. `Transaction.updates` - auf externe Käufe achten

### Enum für den Sperrstatus von Inhalten {#enum-for-content-lock-status}

```swift
enum BookStatus {
    case active    // selected
    case inactive  // unselected
    case locked    // locked behind IAP
}
```

## Gotchas {#gotchas}

- Die `.storekit`-Konfigurationsdatei muss im Schema ausgewählt sein, damit Tests funktionieren
- `@MainActor` ist für die Store-Klasse erforderlich, da sie `@Published`-Eigenschaften aktualisiert
- `Transaction.updates` muss kontinuierlich laufen – den Task speichern, damit er nicht abgebrochen wird
- `revocationDate != nil` bedeutet, dass der Kauf erstattet wurde – aus `purchasedIDs` entfernen
- Der Status `pending` tritt auf, wenn Ask to Buy aktiviert ist (Kindersicherung)
- Das StoreKit-Testen in Xcode verwendet die Konfigurationsdatei; Tests im echten App Store erfordern TestFlight oder Sandbox-Konten
- `Set<String>` für `purchasedIDs` verhindert doppelte Einträge bei der Prüfung von Berechtigungen

## See Also {#see-also}

- [[swiftui-state-and-data-flow]] - @EnvironmentObject für die Store-Injektion
- [[swiftui-navigation]] - Anzeige der Kauf-UI in Sheets
- [[swift-enums-and-optionals]] - BookStatus-Enum-Muster
