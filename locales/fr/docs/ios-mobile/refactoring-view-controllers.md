---
title: "Refactorisation des grands view controllers"
description: "Décomposition systématique de view controllers volumineux en composants testables à l'aide de patterns d'extraction"
level: 3
source_sha256: 2b53e2d90ce3956fbe525b417403e5402523b6c118c1eb71a7a708cce89b201b
translation: machine
translated_at: '2026-10-24'
---
# Refactorisation des grands view controllers {#refactoring-large-view-controllers}

Techniques systématiques pour décomposer des view controllers volumineux (1000+ lignes) en composants testables et maintenables. S'applique aussi bien aux bases de code UIKit qu'aux bases hybrides UIKit/SwiftUI.

## Extraire les fonctions pures {#extract-pure-functions}

La refactorisation la plus simple : identifier les méthodes qui n'accèdent pas aux propriétés de `self` et les extraire sous forme de fonctions libres ou d'extensions de types.

**Signal de détection :** une méthode reçoit toutes ses entrées en paramètres et retourne une valeur sans lire ni écrire d'état d'instance.

```swift
// Before: method inside PlacesViewController (2700 lines)
func isDistanceSignificant(_ region1: MKCoordinateRegion,
                           _ region2: MKCoordinateRegion) -> Bool {
    // pure computation using only parameters
}

// After: extension on MKCoordinateRegion
extension MKCoordinateRegion {
    func isSignificantlyDifferent(from other: MKCoordinateRegion) -> Bool {
        let widthDelta = abs(self.span.longitudeDelta - other.span.longitudeDelta)
        let heightDelta = abs(self.span.latitudeDelta - other.span.latitudeDelta)
        let centerDelta = self.center.latitude.distance(to: other.center.latitude)
        return widthDelta > 0.001 || heightDelta > 0.001 || centerDelta > 0.001
    }
}
```

**Avantages :**
- Prouve que le code est indépendant de l'état du view controller
- Facile à tester : pas besoin d'instancier le view controller
- Réduit le nombre de lignes du view controller

## Séparer le calcul des effets de bord {#separate-computation-from-side-effects}

Lorsqu'une méthode à la fois calcule une valeur et l'applique (par exemple, calcule un frame puis le définit), la scinder en deux :

```swift
// Step 1: Extract computation
func computePopoverLayout(
    popoverSize: CGSize,
    viewSize: CGSize,
    annotationFrame: CGRect,
    overlayFrame: CGRect?,
    extendedNavbarHeight: CGFloat
) -> CGRect {
    // Pure geometry computation
    let center = CGPoint(x: annotationFrame.midX, y: annotationFrame.midY)
    // ... frame math ...
    return computedFrame
}

// Step 2: Keep side effect in view controller
func adjustPopoverLayout(_ popover: UIViewController) {
    let annotationFrame = view.convert(annotationView.frame, from: mapView)
    let overlayFrame: CGRect? = isViewModeOverlay
        ? searchOverlayContainerView.frame : nil

    let frame = computePopoverLayout(
        popoverSize: popover.preferredContentSize,
        viewSize: view.bounds.size,
        annotationFrame: annotationFrame,
        overlayFrame: overlayFrame,
        extendedNavbarHeight: navigationBar.extendedHeight
    )
    popover.view.frame = frame
}
```

**Principe clé :** convertir les objets UIKit (vues, annotation views) en types valeur (CGRect, CGSize, CGPoint) à la frontière, puis ne passer que des valeurs à la fonction de calcul.

## Conversion de coordonnées aux frontières {#coordinate-conversion-at-boundaries}

Lors de l'extraction de code qui utilise `view.convert(_:from:)`, effectuer la conversion au point d'appel :

```swift
// Bad: computation function accesses UIKit views
func compute(annotationView: MKAnnotationView, mapView: MKMapView) -> CGRect {
    let frame = mapView.convert(annotationView.frame, to: self.view) // needs self
    // ...
}

// Good: convert at boundary, pass values
let convertedFrame = view.convert(annotationView.frame, from: mapView)
let result = computeLayout(annotationFrame: convertedFrame, viewSize: view.bounds.size)
```

## Extraire les child view controllers {#extract-child-view-controllers}

Lorsqu'une section du view controller gère une région d'interface distincte avec son propre cycle de vie :

```swift
// Create a dedicated child
class SearchOverlayViewController: UIViewController {
    // Owns search bar, results table, filter controls
}

// In parent
func addSearchOverlay() {
    let search = SearchOverlayViewController()
    addChild(search)
    view.addSubview(search.view)
    search.didMove(toParent: self)
}
```

**Utiliser des child view controllers lorsque :**
- La région possède sa propre source de données
- La région gère ses propres transitions d'état
- La région pourrait être réutilisée ailleurs

## Extraire les data sources {#extract-data-sources}

Les data sources des table views et collection views sont des cibles d'extraction privilégiées :

```swift
class PlacesDataSource: NSObject, UITableViewDataSource {
    var places: [Place] = []

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        places.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        // cell configuration
    }
}
```

## Ordre de refactorisation {#refactoring-order}

Commencer par les gains les plus faciles pour gagner en confiance :

1. **Fonctions utilitaires pures** : risque nul, bénéfice immédiat
2. **Définitions d'enums et de constantes** : déplacer les types imbriqués dans leurs propres fichiers
3. **Extraction des data sources** : frontières claires
4. **Séparation calcul/effets de bord** : nécessite de comprendre les dépendances
5. **Child view controllers** : le plus invasif, à faire en dernier

## Tester après l'extraction {#testing-after-extraction}

Les fonctions pures extraites des view controllers sont triviales à tester :

```swift
func testDistanceSignificant() {
    let region1 = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 52.5, longitude: 13.4),
        span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
    )
    let region2 = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 52.6, longitude: 13.4),
        span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
    )
    XCTAssertTrue(region1.isSignificantlyDifferent(from: region2))
}
```

Pas de configuration du view controller, pas de chargement de storyboard, pas de hiérarchie de fenêtres.

## Pièges à éviter {#gotchas}

- **Dépendances cachées sur `self` :** lorsqu'on sort une méthode d'un view controller, les erreurs du compilateur révèlent les propriétés auxquelles elle accédait. C'est un avantage : cela montre la surface de dépendance réelle. Si la méthode compile immédiatement en fonction libre, c'est qu'elle était déjà pure.
- **Systèmes de coordonnées :** les calculs de frame à l'intérieur d'un view controller utilisent souvent `view.convert(_:from:)` de manière implicite. Lors de l'extraction, il faut convertir à la frontière et passer les valeurs converties. Un oubli provoque des bugs de mise en page qui n'apparaissent que sur iPad ou avec des safe area insets différents.
- **Explosion des conformités aux délégués :** un view controller qui se conforme à 8 protocoles de délégation ou plus est un signal fort de la nécessité de le décomposer. Chaque protocole de délégation suggère une préoccupation séparable.

## Voir aussi {#see-also}

- [[swiftui-state-and-data-flow]]
- [[swift-structs-and-classes]]
- [[core-data-persistence]]
