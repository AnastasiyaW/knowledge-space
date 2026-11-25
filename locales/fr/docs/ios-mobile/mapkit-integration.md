---
title: "Intégration de MapKit"
category: concepts
tags: [ios-mobile, swiftui, mapkit, maps, annotations, location, mapcamera]
level: 3
source_sha256: 3c486995d42cd76b5fecc8b24b405176a2d916dfba0914b7933ae24f8b35eabf
translation: machine
translated_at: '2026-10-24'
---
# Intégration de MapKit {#mapkit-integration}

L'intégration de MapKit dans SwiftUI fournit des vues de carte natives avec des annotations, le contrôle de la caméra, un basculement entre les vues standard et satellite, et les coordonnées géographiques. Disponible à partir d'iOS 17+ avec la nouvelle API Map.

## Points clés {#key-facts}

- `import MapKit` requis ; `CLLocationCoordinate2D` représente la latitude et la longitude
- La vue `Map` accepte une position de caméra et un contenu d'annotations
- `MapCamera` contrôle le centre, la distance (en mètres), le cap (boussole) et l'inclinaison (pitch)
- `Annotation` place des vues SwiftUI personnalisées sur la carte
- `.mapStyle()` permet de basculer entre `.standard` et `.imagery` (satellite)
- Les vues de carte fonctionnent à l'intérieur de NavigationLink avec des transitions de zoom

## Modèles {#patterns}

### Carte de base avec annotation {#basic-map-with-annotation}

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

### Paramètres de MapCamera {#mapcamera-parameters}

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

### Carte plein écran avec plusieurs annotations {#full-screen-map-with-multiple-annotations}

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

### Carte dans une vue de détail avec transition de zoom {#map-in-detail-view-with-zoom-transition}

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

### Options de style de carte {#map-style-options}

```swift
.mapStyle(.standard)                           // default road map
.mapStyle(.standard(elevation: .realistic))    // with terrain
.mapStyle(.imagery)                            // satellite
.mapStyle(.imagery(elevation: .realistic))     // satellite with 3D terrain
.mapStyle(.hybrid)                             // satellite + labels
```

## Pièges à éviter {#gotchas}

- `Map(position:)` nécessite un `Binding<MapCameraPosition>` - utilisez `.constant()` pour des positions statiques
- Les `Annotation` sont des vues SwiftUI, et non des épingles de carte standard - elles peuvent contenir n'importe quelle vue
- Les interactions avec la carte (zoom, déplacement) nécessitent que la vue ne se trouve pas dans un contexte désactivé ou non interactif
- `.toolbarBackground(.automatic)` peut être nécessaire pour garantir la visibilité de la barre d'outils au-dessus du contenu de la carte
- La distance est exprimée en mètres - 1000 correspond à peu près à l'échelle du quartier, 30000 à l'échelle de la ville
- Cap 0 = nord, 90 = est, 180 = sud, 270 = ouest

## Voir aussi {#see-also}

- [[swiftui-navigation]] - transitions de zoom avec @Namespace
- [[swiftui-views-and-modifiers]] - overlay et clipShape pour le style de la carte
- [[swiftui-networking]] - chargement des données de localisation depuis JSON/API
