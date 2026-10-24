---
title: "Große View Controller refaktorisieren"
description: "Systematische Zerlegung umfangreicher View Controller in testbare Komponenten mithilfe von Extraktionsmustern"
level: 3
source_sha256: 2b53e2d90ce3956fbe525b417403e5402523b6c118c1eb71a7a708cce89b201b
translation: machine
translated_at: '2026-10-24'
---
# Große View Controller refaktorisieren {#refactoring-large-view-controllers}

Systematische Techniken zur Zerlegung umfangreicher View Controller (1000+ Zeilen) in testbare, wartbare Komponenten. Anwendbar sowohl auf reine UIKit-Codebasen als auch auf hybride UIKit/SwiftUI-Codebasen.

## Reine Funktionen extrahieren {#extract-pure-functions}

Die einfachste Refaktorisierung: Methoden identifizieren, die nicht auf `self`-Properties zugreifen, und als freie Funktionen oder Typerweiterungen extrahieren.

**Erkennungsmerkmal:** Eine Methode erhält alle Eingaben als Parameter und gibt einen Wert zurück, ohne den Instanzzustand zu lesen oder zu schreiben.

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

**Vorteile:**
- Belegt, dass der Code unabhängig vom Zustand des View Controllers ist
- Einfach zu testen – keine Instanziierung des View Controllers nötig
- Reduziert die Zeilenzahl des View Controllers

## Berechnung von Seiteneffekten trennen {#separate-computation-from-side-effects}

Wenn eine Methode einen Wert sowohl berechnet als auch anwendet (z. B. einen Frame berechnet und ihn dann setzt), wird sie in zwei Methoden aufgeteilt:

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

**Zentrales Prinzip:** UIKit-Objekte (Views, Annotation Views) an der Grenze in Wertetypen (CGRect, CGSize, CGPoint) umwandeln und dann nur Werte an die Berechnungsfunktion übergeben.

## Koordinatenumrechnung an den Grenzen {#coordinate-conversion-at-boundaries}

Beim Extrahieren von Code, der `view.convert(_:from:)` verwendet, wird die Umrechnung an der Aufrufstelle durchgeführt:

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

## Child View Controller extrahieren {#extract-child-view-controllers}

Wenn ein Bereich des View Controllers eine eigenständige UI-Region mit eigenem Lebenszyklus verwaltet:

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

**Child View Controller verwenden, wenn:**
- die Region eine eigene Datenquelle besitzt
- die Region ihre Zustandsübergänge selbst verwaltet
- die Region an anderer Stelle wiederverwendet werden könnte

## Datenquellen extrahieren {#extract-data-sources}

Datenquellen von Table- und Collection Views sind ideale Kandidaten für eine Extraktion:

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

## Reihenfolge der Refaktorisierung {#refactoring-order}

Mit den einfachsten Gewinnen beginnen, um Vertrauen aufzubauen:

1. **Hilfsfunktionen ohne Seiteneffekte** – kein Risiko, sofortiger Nutzen
2. **Enum- und Konstantendefinitionen** – innere Typen in eigene Dateien verschieben
3. **Extraktion der Datenquellen** – klare Grenzen
4. **Trennung von Berechnung und Seiteneffekten** – erfordert Verständnis der Abhängigkeiten
5. **Child View Controller** – am invasivsten, daher zuletzt

## Testen nach der Extraktion {#testing-after-extraction}

Aus View Controllern extrahierte reine Funktionen sind trivial testbar:

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

Kein Setup des View Controllers, kein Laden von Storyboards, keine Window-Hierarchie.

## Fallstricke {#gotchas}

- **Versteckte Abhängigkeiten von `self`:** Beim Herauslösen einer Methode aus einem View Controller zeigen Compilerfehler, auf welche Properties sie zugreift. Das ist gewollt – es macht die tatsächliche Abhängigkeitsfläche sichtbar. Kompiliert die Methode sofort als freie Funktion, war sie bereits rein.
- **Koordinatensysteme:** Frame-basierte Berechnungen innerhalb eines View Controllers verwenden oft implizit `view.convert(_:from:)`. Beim Extrahieren muss an der Grenze umgerechnet und der umgerechnete Wert übergeben werden. Wird dies übersehen, entstehen Layoutfehler, die nur auf dem iPad oder bei abweichenden Safe-Area-Insets auftreten.
- **Explosion der Delegate-Konformitäten:** Ein View Controller, der 8 oder mehr Delegate-Protokolle implementiert, ist ein deutliches Signal für eine Zerlegung. Jedes Delegate-Protokoll deutet auf eine abtrennbare Verantwortlichkeit hin.

## Siehe auch {#see-also}

- [[swiftui-state-and-data-flow]]
- [[swift-structs-and-classes]]
- [[core-data-persistence]]
