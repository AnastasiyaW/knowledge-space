---
title: MapKit Integration
category: concepts
tags: [ios-mobile, swiftui, mapkit, maps, annotations, location, mapcamera]
---

# MapKit Integration

SwiftUI's MapKit integration provides native map views with annotations, camera control, satellite/standard toggle, and location coordinates. Available from iOS 17+ with the modern Map API.

## Key Facts

- `import MapKit` required; `CLLocationCoordinate2D` represents lat/long
- `Map` view accepts a camera position and annotation content
- `MapCamera` controls center, distance (meters), heading (compass), and pitch (tilt)
- `Annotation` places custom SwiftUI views on the map
- `.mapStyle()` switches between `.standard` and `.imagery` (satellite)
- Map views work inside NavigationLink with zoom transitions

## Patterns

### Basic Map with Annotation

```swift
import MapKit

struct MapView: View {
    let predator: ApexPredator

    var body: some View {
        Map(position: .constant(
            .camera(MapCamera(
                centerCoordinate: predator.location,
                distance: 1000
            ))
        )) {
            Annotation(predator.name, coordinate: predator.location) {
                predator.image
                    .resizable()
                    .scaledToFit()
                    .frame(height: 100)
                    .shadow(color: .white, radius: 3)
                    .scaleEffect(x: -1)
            }
        }
    }
}
```

### MapCamera Parameters

```swift
MapCamera(
    centerCoordinate: predator.location,
    distance: 1000,      // meters from center
    heading: 250,        // compass direction (0=north, 90=east)
    pitch: 80            // tilt angle (0=overhead, 90=horizontal)
)
```

### CLLocationCoordinate2D

```swift
// As a computed property on a model
var location: CLLocationCoordinate2D {
    CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
}
```

### Full-Screen Map with Multiple Annotations

```swift
struct PredatorMap: View {
    @State var satellite = false
    var position: MapCameraPosition

    var body: some View {
        Map(position: .constant(position)) {
            ForEach(Predators().apexPredators) { predator in
                Annotation(predator.name, coordinate: predator.location) {
                    predator.image
                        .resizable()
                        .scaledToFit()
                        .frame(height: 100)
                        .shadow(color: .white, radius: 3)
                        .scaleEffect(x: -1)
                }
            }
        }
        .mapStyle(satellite
            ? .imagery(elevation: .realistic)
            : .standard(elevation: .realistic))
        .overlay(alignment: .bottomTrailing) {
            Button {
                satellite.toggle()
            } label: {
                Image(systemName: satellite
                    ? "globe.americas.fill" : "globe.americas")
                    .font(.largeTitle)
                    .imageScale(.large)
                    .padding(3)
                    .background(.ultraThinMaterial)
                    .clipShape(.rect(cornerRadius: 7))
                    .shadow(radius: 3)
                    .padding()
            }
        }
        .toolbarBackground(.automatic)
    }
}
```

### Map in Detail View with Zoom Transition

```swift
struct PredatorDetail: View {
    let predator: ApexPredator
    @Namespace var namespace

    var body: some View {
        NavigationLink {
            PredatorMap(position: .camera(
                MapCamera(
                    centerCoordinate: predator.location,
                    distance: 1000, heading: 250, pitch: 80
                )
            ))
            .navigationTransition(.zoom(sourceID: 1, in: namespace))
        } label: {
            MapView(predator: predator)
                .frame(height: 125)
                .clipShape(.rect(cornerRadius: 15))
                .overlay(alignment: .topLeading) {
                    Text("Current Location")
                        .font(.caption)
                        .padding(5)
                }
        }
        .matchedTransitionSource(id: 1, in: namespace)
    }
}
```

### Map Style Options

```swift
.mapStyle(.standard)                           // default road map
.mapStyle(.standard(elevation: .realistic))    // with terrain
.mapStyle(.imagery)                            // satellite
.mapStyle(.imagery(elevation: .realistic))     // satellite with 3D terrain
.mapStyle(.hybrid)                             // satellite + labels
```

## Gotchas

- `Map(position:)` requires a `Binding<MapCameraPosition>` - use `.constant()` for static positions
- `Annotation` views are SwiftUI views, not standard map pins - they can contain any view
- Map interactions (zoom, pan) require the view to not be inside a disabled or non-interactive context
- `.toolbarBackground(.automatic)` may be needed to ensure toolbar visibility over map content
- Distance is in meters - 1000 = roughly neighborhood level, 30000 = city level
- Heading 0 = north, 90 = east, 180 = south, 270 = west

## See Also

- [[swiftui-navigation]] - zoom transitions with @Namespace
- [[swiftui-views-and-modifiers]] - overlay and clipShape for map styling
- [[swiftui-networking]] - loading location data from JSON/API
