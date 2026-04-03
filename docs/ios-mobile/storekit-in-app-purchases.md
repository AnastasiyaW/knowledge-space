---
title: StoreKit 2 In-App Purchases
category: concepts
tags: [ios-mobile, swiftui, storekit, iap, in-app-purchases, monetization]
---

# StoreKit 2 In-App Purchases

StoreKit 2 is Apple's modern API for in-app purchases. It uses async/await, provides built-in receipt verification, and simplifies the purchase flow compared to StoreKit 1. This entry covers non-consumable purchases with testing via StoreKit configuration files.

## Key Facts

- StoreKit 2 uses `Product.products(for:)` to fetch available products
- `product.purchase()` triggers the system purchase sheet
- `Transaction.updates` watches for purchases made outside the app
- Purchase results include `.success`, `.userCancelled`, and `.pending` cases
- Verified transactions include `signedType.productID` to track what was purchased
- StoreKit Configuration File (`.storekit`) enables testing without App Store Connect
- Non-consumable = buy once permanently; consumable = repeatable; subscription = recurring

## Patterns

### Setup: StoreKit Configuration File

1. New File > StoreKit Configuration File
2. Click `+` > Add Non-Consumable In-App Purchase
3. Set Reference Name (e.g., `HP4`), Product ID (e.g., `hp4`), Price
4. Add Display Name and Description
5. Product > Scheme > Edit Scheme > StoreKit Configuration: select the file

### Store Class

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

### Injecting Store via EnvironmentObject

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

### Loading Products on View Appear

```swift
.task {
    await store.loadProducts()
    await store.checkPurchased()
}
```

### IAP Types

| Type | Purchase | Use Case |
|------|----------|---------|
| Non-consumable | Once, permanent | Unlock features/content |
| Consumable | Repeatable | In-game currency, lives |
| Non-renewing subscription | Manual renewal | Seasonal access |
| Auto-renewing subscription | Auto-billed | Ongoing service |

### Purchase Flow Summary

1. Create `.storekit` config file with product IDs
2. Set scheme to use that config file for testing
3. `Product.products(for: productIDs)` - fetch metadata
4. `product.purchase()` - trigger purchase sheet
5. Switch on result: `.success` > `.verified(signedType)` > add `productID` to `purchasedIDs`
6. `product.currentEntitlement` - check existing purchases (on launch + after updates)
7. `Transaction.updates` - watch for external purchases

### Enum for Content Lock Status

```swift
enum BookStatus {
    case active    // selected
    case inactive  // unselected
    case locked    // locked behind IAP
}
```

## Gotchas

- The `.storekit` config file must be selected in the scheme for testing to work
- `@MainActor` is required on the Store class because it updates `@Published` properties
- `Transaction.updates` must run continuously - store the Task to prevent it from being cancelled
- `revocationDate != nil` means the purchase was refunded - remove from purchasedIDs
- `pending` state occurs when Ask to Buy is enabled (parental controls)
- StoreKit testing in Xcode uses the config file; real App Store testing requires TestFlight or sandbox accounts
- `Set<String>` for purchasedIDs prevents duplicate entries when checking entitlements

## See Also

- [[swiftui-state-and-data-flow]] - @EnvironmentObject for Store injection
- [[swiftui-navigation]] - presenting purchase UI in sheets
- [[swift-enums-and-optionals]] - BookStatus enum pattern
