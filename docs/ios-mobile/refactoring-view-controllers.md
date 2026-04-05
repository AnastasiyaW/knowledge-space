# Refactoring Large View Controllers

Systematic techniques for decomposing massive view controllers (1000+ lines) into testable, maintainable components. Applies to both UIKit and hybrid UIKit/SwiftUI codebases.

## Extract Pure Functions

The simplest refactoring: identify methods that don't access `self` properties and extract them as free functions or type extensions.

**Detection signal:** a method takes all its inputs as parameters and returns a value without reading/writing instance state.

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

**Benefits:**
- Proves the code is independent of view controller state
- Easy to test - no view controller instantiation needed
- Reduces view controller line count

## Separate Computation from Side Effects

When a method both computes a value and applies it (e.g., calculates a frame then sets it), split into two:

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

**Key principle:** convert UIKit objects (views, annotation views) into value types (CGRect, CGSize, CGPoint) at the boundary, then pass only values into the computation function.

## Coordinate Conversion at Boundaries

When extracting code that uses `view.convert(_:from:)`, perform the conversion at the call site:

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

## Extract Child View Controllers

When a section of the view controller manages a distinct UI region with its own lifecycle:

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

**Use child VCs when:**
- The region has its own data source
- The region manages its own state transitions
- The region could be reused elsewhere

## Extract Data Sources

Table/collection view data sources are prime extraction targets:

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

## Refactoring Order

Start with the easiest wins and build confidence:

1. **Pure helper functions** - zero risk, immediate payoff
2. **Enum/constant definitions** - move inner types to their own files
3. **Data source extraction** - clear boundaries
4. **Computation/side-effect split** - requires understanding dependencies
5. **Child view controllers** - most invasive, do last

## Testing After Extraction

Pure functions extracted from view controllers are trivially testable:

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

No view controller setup, no storyboard loading, no window hierarchy.

## Gotchas

- **Hidden dependencies on `self`:** When cutting a method out of a view controller, compiler errors reveal which properties it was accessing. This is a feature - it shows the true dependency surface. If it compiles immediately as a free function, the method was already pure.
- **Coordinate systems:** Frame-based calculations inside a view controller often use `view.convert(_:from:)` implicitly. When extracting, you must convert at the boundary and pass the converted values in. Missing this will cause layout bugs that only appear on iPad or with different safe area insets.
- **Delegate conformance explosion:** A view controller conforming to 8+ delegate protocols is a strong signal it needs decomposition. Each delegate protocol suggests a separable concern.

## See Also

- [[swiftui-state-and-data-flow]]
- [[swift-structs-and-classes]]
- [[core-data-persistence]]
