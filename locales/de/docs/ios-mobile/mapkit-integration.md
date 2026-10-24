---
title: "MapKit-Integration"
category: concepts
tags: [ios-mobile, swiftui, mapkit, maps, annotations, location, mapcamera]
level: 3
source_sha256: 3c486995d42cd76b5fecc8b24b405176a2d916dfba0914b7933ae24f8b35eabf
translation: machine
translated_at: '2026-10-24'
---
# MapKit-Integration {#mapkit-integration}

Die MapKit-Integration in SwiftUI bietet native Kartenansichten mit Annotationen, Kamerasteuerung, Umschaltung zwischen Standard- und Satellitenansicht sowie Standortkoordinaten. Verfügbar ab iOS 17+ mit der modernen Map-API.

## Wichtige Fakten {#key-facts}

- `import MapKit` ist erforderlich; `CLLocationCoordinate2D` repräsentiert Breiten- und Längengrad
- Die `Map`-Ansicht akzeptiert eine Kameraposition und Annotationsinhalte
- `MapCamera` steuert Zentrum, Distanz (Meter), Richtung (Kompass) und Neigung (Kippwinkel)
- `Annotation` platziert benutzerdefinierte SwiftUI-Ansichten auf der Karte
- `.mapStyle()` wechselt zwischen `.standard` und `.imagery` (Satellit)
- Kartenansichten funktionieren innerhalb von NavigationLink mit Zoom-Übergängen

## Muster {#patterns}

### Einfache Karte mit Annotation {#basic-map-with-annotation}

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

### MapCamera-Parameter {#mapcamera-parameters}

```swift
MapCamera(
    centerCoordinate: predator.location,
    distance: 1000,      // meters from center
    heading: 250,        // compass direction (0=north, 90=east)
    pitch: 80            // tilt angle (0=overhead, 90=horizontal)
)
```

### CLLocationCoordinate2D {#cllocationcoordinate2d}

```swift
// As a computed property on a model
var location: CLLocationCoordinate2D {
    CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
}
```

### Vollbildkarte mit mehreren Annotationen {#full-screen-map-with-multiple-annotations}

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

### Karte in der Detailansicht mit Zoom-Übergang {#map-in-detail-view-with-zoom-transition}

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

### Optionen für den Kartenstil {#map-style-options}

```swift
.mapStyle(.standard)                           // default road map
.mapStyle(.standard(elevation: .realistic))    // with terrain
.mapStyle(.imagery)                            // satellite
.mapStyle(.imagery(elevation: .realistic))     // satellite with 3D terrain
.mapStyle(.hybrid)                             // satellite + labels
```

## Stolpersteine {#gotchas}

- `Map(position:)` erfordert ein `Binding<MapCameraPosition>` – verwende `.constant()` für statische Positionen
- `Annotation`-Ansichten sind SwiftUI-Ansichten, keine standardmäßigen Kartennadeln – sie können beliebige Ansichten enthalten
- Karteninteraktionen (Zoomen, Verschieben) erfordern, dass die Ansicht nicht in einem deaktivierten oder nicht interaktiven Kontext liegt
- `.toolbarBackground(.automatic)` kann nötig sein, damit die Werkzeugleiste über Karteninhalten sichtbar bleibt
- Die Distanz wird in Metern angegeben – 1000 entspricht ungefähr Nachbarschaftsebene, 30000 Stadtebene
- Richtung 0 = Norden, 90 = Osten, 180 = Süden, 270 = Westen

## Siehe auch {#see-also}

- [[swiftui-navigation]] – Zoom-Übergänge mit @Namespace
- [[swiftui-views-and-modifiers]] – overlay und clipShape für die Gestaltung der Karte
- [[swiftui-networking]] – Laden von Standortdaten aus JSON/API
