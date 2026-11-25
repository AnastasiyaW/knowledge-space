---
title: "Graph-Algorithmen in Swift"
description: "Adjazenzlisten-Graphen, BFS/DFS-Traversierung und Algorithmen für kürzeste Wege mit Kartenbeispielen"
level: 3
source_sha256: d750ecf2368d93bce6f2ba23077ea24c4129c35288a648ecf88a3f84896ff0d1
translation: machine
translated_at: '2026-10-24'
---
# Graph-Algorithmen in Swift {#graph-algorithms-in-swift}

Aufbau von Graphstrukturen und Traversierungsalgorithmen in Swift, mit praxisnahen Beispielen aus Geo- und Kartenanwendungen.

## Graph-Datenstruktur {#graph-data-structure}

Eine Adjazenzlisten-Darstellung mit einem Dictionary:

```swift
struct Graph {
    struct Destination {
        let coordinate: Coordinate
        let distance: CLLocationDistance
    }

    private(set) var edges: [Coordinate: [Destination]] = [:]

    mutating func addEdge(from: Coordinate, to: Coordinate) {
        let distance = from.distance(to: to)
        edges[from, default: []].append(
            Destination(coordinate: to, distance: distance)
        )
    }
}
```

**Verwendete Swift-Muster:**
- `private(set)` - extern lesbar, nur intern schreibbar
- `default: []`-Subskript - vermeidet Nil-Prüfungen beim Anhängen an Arrays im Dictionary
- `mutating` - erforderlich für die Mutation von Value-Types

## Graphen aus Tracks aufbauen {#building-graphs-from-tracks}

Aufeinanderfolgende Punkte eines Tracks verbinden und die Schleife schließen:

```swift
func buildGraph(from tracks: [Track]) -> Graph {
    var result = Graph()
    for track in tracks {
        let coords = track.coordinates.map(\.coordinate)
        // zip pairs each point with the next; append first to close the loop
        let pairs = zip(coords, coords.dropFirst() + [coords[0]])
        for (from, to) in pairs {
            result.addEdge(from: from, to: to)
        }
    }
    return result
}
```

Das Muster `zip` + `dropFirst` kommt ohne manuelle Indexverwaltung und ohne Variablen zur Verfolgung des vorherigen Punktes aus.

## Exploration per Breitensuche {#breadth-first-exploration}

Alle erreichbaren Knoten ausgehend von einem Startpunkt ermitteln und die Schritte für die Visualisierung festhalten:

```swift
extension Graph {
    func connectedVertices(from start: Coordinate) -> [[(Coordinate, Coordinate)]] {
        var result: [[(Coordinate, Coordinate)]] = [[]]
        var seen: Set<Coordinate> = [start]
        var sourcePoints: [Coordinate] = [start]

        while !sourcePoints.isEmpty {
            var newSourcePoints: [Coordinate] = []

            for source in sourcePoints {
                for edge in edges[source] ?? [] {
                    let dest = edge.coordinate
                    result[result.endIndex - 1].append((source, dest))
                    if !seen.contains(dest) {
                        newSourcePoints.append(dest)
                    }
                }
                seen.insert(source)
            }

            newSourcePoints = newSourcePoints.filter { !seen.contains($0) }
            sourcePoints = newSourcePoints
            result.append([])
        }

        return result
    }
}
```

**Eigenschaften des Algorithmus:**
- Gibt ein Array von Arrays zurück - jedes innere Array ist ein BFS-„Schritt“
- Die `seen`-Menge verhindert Endlosschleifen in zyklischen Graphen
- Ermöglicht eine schrittweise Animation der Graph-Exploration

## Animierte Visualisierung mit MapKit {#animated-visualization-on-mapkit}

BFS-Schritte mithilfe rekursiver Dispatch-Aufrufe nacheinander darstellen:

```swift
func drawStep(_ remainder: ArraySlice<[(Coordinate, Coordinate)]>) {
    guard let step = remainder.first else { return }

    for edge in step {
        let coords = [
            CLLocationCoordinate2D(edge.0),
            CLLocationCoordinate2D(edge.1)
        ]
        let polyline = MKPolyline(coordinates: coords, count: 2)
        mapView.addOverlay(polyline)
    }

    DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
        drawStep(remainder.dropFirst())
    }
}

// Start animation
let steps = graph.connectedVertices(from: graph.edges.keys.randomElement()!)
drawStep(steps[steps.startIndex...])
```

Die Verwendung von `ArraySlice` vermeidet das Kopieren des Arrays bei jedem rekursiven Schritt.

## Koordinaten hashbar machen {#making-coordinates-hashable}

`CLLocationCoordinate2D` ist nicht `Hashable`. Daher wird es in einen Wrapper gekapselt:

```swift
struct Coordinate: Hashable {
    let latitude: Double
    let longitude: Double

    init(_ coord: CLLocationCoordinate2D) {
        self.latitude = coord.latitude
        self.longitude = coord.longitude
    }

    func distance(to other: Coordinate) -> CLLocationDistance {
        let loc1 = CLLocation(latitude: latitude, longitude: longitude)
        let loc2 = CLLocation(latitude: other.latitude, longitude: other.longitude)
        return loc1.distance(from: loc2)
    }
}
```

## Überlegungen zur Performance {#performance-considerations}

| Operation | Adjazenzliste | Adjazenzmatrix |
|-----------|---------------|-----------------|
| Kante hinzufügen | O(1) | O(1) |
| Prüfen, ob Kante existiert | O(degree) | O(1) |
| Alle Nachbarn | O(degree) | O(V) |
| Speicher | O(V + E) | O(V^2) |

Für dünn besetzte Geodaten-Graphen (Straßen, Wege) sind Adjazenzlisten deutlich vorzuziehen.

## Fallstricke {#gotchas}

- **Gleitkomma-Gleichheit bei Koordinaten:** Zwei GPS-Punkte, die denselben Ort darstellen sollten, können sich um winzige Beträge unterscheiden. Werden Koordinaten als Dictionary-Schlüssel verwendet, sollte man auf eine feste Rundungsgenauigkeit runden oder einen räumlichen Index verwenden, statt exakte Gleichheit zu prüfen.
- **Getrennte Komponenten:** Wird ein Graph aus unabhängigen Tracks aufgebaut, entstehen getrennte Teilgraphen. Eine BFS ab dem Knoten eines Tracks erkundet nur diesen Track. Um Tracks an Schnittpunkten zu verbinden, ist explizite Logik zum Zusammenführen von Kanten nötig, typischerweise durch das Finden von Punkten innerhalb eines Abstandsschwellenwerts.
- **Performance von MapKit-Overlays:** Das Hinzufügen Tausender `MKPolyline`-Overlays zu einer Kartenansicht führt zu starken Einbrüchen der Bildrate. Für Debugging-Visualisierungen ist das akzeptabel, Produktivcode sollte jedoch ein einzelnes `MKMultiPolyline` oder ein eigenes Kachel-Rendering verwenden.

## Siehe auch {#see-also}

- [[mapkit-integration]]
- [[swift-collections-beyond-arrays]]
- [[swift-structs-and-classes]]
