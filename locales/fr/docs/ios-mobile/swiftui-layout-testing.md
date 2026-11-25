---
title: "Tests de layout SwiftUI"
description: "Fuzzing basé sur les propriétés pour vérifier les moteurs de layout personnalisés par rapport au rendu natif de SwiftUI d'Apple"
level: 3
source_sha256: a9fb215d86dc21a246310e7a348dcdcaf2dc4ca7fa37de3c61e60d7e13209b86
translation: machine
translated_at: '2026-10-24'
---
# Tests de layout SwiftUI {#swiftui-layout-testing}

Vérification automatisée des implémentations de layout SwiftUI personnalisées, par comparaison avec le rendu natif d'Apple, à l'aide de tests basés sur les propriétés (fuzzing).

## Approche {#approach}

Générer des configurations de vues aléatoires, les rendre à la fois avec votre moteur de layout personnalisé et avec SwiftUI, puis comparer les résultats :

1. Définir une énumération des configurations possibles des vues enfants
2. Générer aléatoirement des hiérarchies de vues
3. Mesurer les enfants avec votre implémentation
4. Mesurer les enfants avec SwiftUI (via `GeometryReader` + preferences)
5. Vérifier l'égalité

## Générer des configurations de vues aléatoires {#generating-random-view-configurations}

```swift
enum Frame: CustomStringConvertible {
    case flexible                     // no frame modifier
    case fixed(CGFloat)               // .frame(width: N)
    case min(CGFloat)                 // .frame(minWidth: N)
    case max(CGFloat)                 // .frame(maxWidth: N)
    case minMax(min: CGFloat, max: CGFloat)  // .frame(minWidth: N, maxWidth: M)

    static func random() -> Frame {
        let randomWidth = { CGFloat(Int.random(in: 0...100)) }
        switch Int.random(in: 0..<5) {
        case 0: return .flexible
        case 1: return .fixed(randomWidth())
        case 2: return .min(randomWidth())
        case 3: return .max(randomWidth())
        default:
            let maxW = randomWidth()
            let minW = CGFloat.random(in: 0...maxW).rounded()
            return .minMax(min: minW, max: maxW)
        }
    }

    var view: AnyView {
        let r = Rectangle()
        switch self {
        case .flexible: return AnyView(r)
        case .fixed(let w): return AnyView(r.frame(width: w))
        case .min(let w): return AnyView(r.frame(minWidth: w))
        case .max(let w): return AnyView(r.frame(maxWidth: w))
        case .minMax(let mn, let mx):
            return AnyView(r.frame(minWidth: mn, maxWidth: mx))
        }
    }
}
```

**Important :** pour `.minMax`, générez d'abord `max`, puis `min` dans `0...max`. Une génération indépendante produit des cadres invalides où `min > max`.

## Mesurer les vues SwiftUI {#measuring-swiftui-views}

Utilisez `PreferenceKey` pour remonter les tailles des enfants :

```swift
struct WidthKey: PreferenceKey {
    static var defaultValue: [CGFloat] = []
    static func reduce(value: inout [CGFloat], nextValue: () -> [CGFloat]) {
        value.append(contentsOf: nextValue())
    }
}

// Wrap each child with a GeometryReader overlay
ForEach(views.indices, id: \.self) { i in
    views[i]
        .overlay(GeometryReader { proxy in
            Color.clear.preference(key: WidthKey.self, value: [proxy.size.width])
        })
}
.onPreferenceChange(WidthKey.self) { widths in
    swiftUISizes = widths
}
```

Forcez le rendu avec `UIHostingController` :

```swift
let host = UIHostingController(rootView: swiftUIStack)
host.view.frame = CGRect(x: 0, y: 0, width: proposedWidth, height: 100)
_ = host.view.snapshotView(afterScreenUpdates: true)
```

## Boucle de test {#test-loop}

```swift
func testHStackLayout() {
    for _ in 0..<1000 {
        let frames = (1...Int.random(in: 1...10)).map { _ in Frame.random() }
        let proposedWidth = CGFloat.random(in: 0...500).rounded()

        // Custom implementation
        let customStack = HStack_(children: frames.map(\.view))
        customStack.layout(proposedSize: CGSize(width: proposedWidth, height: 100))
        let customWidths = customStack.sizes.map(\.width)

        // SwiftUI reference
        let swiftUIWidths = measureSwiftUI(frames: frames, proposedWidth: proposedWidth)

        // Compare
        XCTAssertEqual(customWidths, swiftUIWidths,
            "Mismatch for frames: \(frames), proposed: \(proposedWidth)")
    }
}
```

## Différences de plateforme {#platform-differences}

Exécutez les tests sur iOS, et non sur macOS. Problèmes connus sur macOS :

- Un `HStack` avec un contenu centré et des enfants surdimensionnés rend les sous-vues trop grandes et décentrées
- `GeometryReader` centre le contenu sur macOS, alors qu'il l'aligne en haut à gauche (top-leading) sur iOS

Configurez à la fois une cible de test macOS et une cible iOS, mais validez la justesse par rapport au comportement iOS.

## Pièges {#gotchas}

- **Perte de précision de `CGFloat.greatestFiniteMagnitude` :** lors de la comparaison des plages de flexibilité, `greatestFiniteMagnitude` (10^308) perd de la précision dans les chiffres fractionnaires. Deux vues de largeurs minimales différentes, mais de même largeur maximale égale à `greatestFiniteMagnitude`, calculeront des valeurs de flexibilité identiques. Utilisez plutôt une valeur sentinelle grande mais précise, comme `1e15`.
- **Erreurs d'arrondi :** le layout personnalisé et SwiftUI peuvent arrondir au pixel de manière différente. Utilisez le paramètre `accuracy` de `XCTAssertEqual` pour les comparaisons en virgule flottante, ou arrondissez les deux valeurs à la même précision avant la comparaison.
- **Journalisation en cas d'échec :** affichez le tableau `frames` et `proposedWidth` dans le message d'assertion. Sans cela, un échec de fuzzing fournit des tailles, mais aucun moyen de reproduire la configuration d'entrée.

## Voir aussi {#see-also}

- [[swiftui-views-and-modifiers]]
- [[swiftui-state-and-data-flow]]
- [[swift-phantom-types]]
