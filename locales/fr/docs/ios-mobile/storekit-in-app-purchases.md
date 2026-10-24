---
title: "Achats in-app avec StoreKit 2"
category: concepts
tags: [ios-mobile, swiftui, storekit, iap, in-app-purchases, monetization]
level: 3
source_sha256: 2238f63a6b3f0562b0069240af9861c657d7184ee89e378c8dd24f716e0aac76
translation: machine
translated_at: '2026-10-24'
---
# Achats in-app avec StoreKit 2 {#storekit-2-in-app-purchases}

StoreKit 2 est l'API moderne d'Apple pour les achats in-app. Elle repose sur async/await, fournit une vérification des reçus intégrée et simplifie le parcours d'achat par rapport à StoreKit 1. Cette entrée couvre les achats non consommables, avec des tests réalisés à l'aide de fichiers de configuration StoreKit.

## Points clés {#key-facts}

- StoreKit 2 utilise `Product.products(for:)` pour récupérer les produits disponibles
- `product.purchase()` affiche la feuille d'achat du système
- `Transaction.updates` surveille les achats effectués en dehors de l'application
- Les résultats d'achat incluent les cas `.success`, `.userCancelled` et `.pending`
- Les transactions vérifiées incluent `signedType.productID` pour suivre ce qui a été acheté
- Le fichier de configuration StoreKit (`.storekit`) permet de tester sans App Store Connect
- Non consommable = achat unique et permanent ; consommable = rachetable ; abonnement = récurrent

## Patrons {#patterns}

### Mise en place : fichier de configuration StoreKit {#setup-storekit-configuration-file}

1. New File > StoreKit Configuration File
2. Cliquer sur `+` > Add Non-Consumable In-App Purchase
3. Renseigner le Reference Name (par exemple `HP4`), le Product ID (par exemple `hp4`) et le prix
4. Ajouter le Display Name et la Description
5. Product > Scheme > Edit Scheme > StoreKit Configuration : sélectionner le fichier

### Classe Store {#store-class}

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

### Injection du Store via EnvironmentObject {#injecting-store-via-environmentobject}

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

### Chargement des produits à l'apparition de la vue {#loading-products-on-view-appear}

```swift
.task {
    await store.loadProducts()
    await store.checkPurchased()
}
```

### Types d'achats intégrés {#iap-types}

| Type | Achat | Cas d'usage |
|------|-------|-------------|
| Non consommable | Unique, permanent | Déverrouiller des fonctionnalités ou du contenu |
| Consommable | Renouvelable | Monnaie in-game, vies |
| Abonnement non renouvelable | Renouvellement manuel | Accès saisonnier |
| Abonnement à renouvellement automatique | Facturation automatique | Service continu |

### Résumé du parcours d'achat {#purchase-flow-summary}

1. Créer le fichier de configuration `.storekit` avec les identifiants produits
2. Configurer le scheme pour utiliser ce fichier lors des tests
3. `Product.products(for: productIDs)` : récupérer les métadonnées
4. `product.purchase()` : afficher la feuille d'achat
5. Traiter le résultat : `.success` > `.verified(signedType)` > ajouter `productID` à `purchasedIDs`
6. `product.currentEntitlement` : vérifier les achats existants (au lancement et après les mises à jour)
7. `Transaction.updates` : surveiller les achats externes

### Énumération pour l'état de verrouillage du contenu {#enum-for-content-lock-status}

```swift
enum BookStatus {
    case active    // selected
    case inactive  // unselected
    case locked    // locked behind IAP
}
```

## Pièges {#gotchas}

- Le fichier de configuration `.storekit` doit être sélectionné dans le scheme pour que les tests fonctionnent
- `@MainActor` est requis sur la classe Store, car elle met à jour des propriétés `@Published`
- `Transaction.updates` doit s'exécuter en continu : conserver la Task pour l'empêcher d'être annulée
- `revocationDate != nil` signifie que l'achat a été remboursé : le retirer de purchasedIDs
- L'état `pending` apparaît lorsque Ask to Buy est activé (contrôle parental)
- Les tests StoreKit dans Xcode utilisent le fichier de configuration ; les tests sur l'App Store réel nécessitent TestFlight ou des comptes sandbox
- `Set<String>` pour purchasedIDs évite les doublons lors de la vérification des droits

## Voir aussi {#see-also}

- [[swiftui-state-and-data-flow]] - @EnvironmentObject pour l'injection du Store
- [[swiftui-navigation]] - présenter l'interface d'achat dans des feuilles (sheets)
- [[swift-enums-and-optionals]] - le patron de l'énumération BookStatus
