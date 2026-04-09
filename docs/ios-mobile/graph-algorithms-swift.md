---
title: "Graph Algorithms in Swift"
description: "Adjacency list graphs, BFS/DFS traversal, and shortest path algorithms with mapping examples"
---

# Graph Algorithms in Swift

Building graph data structures and traversal algorithms in Swift, with practical examples from geographic/mapping applications.

## Graph Data Structure

An adjacency list representation using a dictionary:

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

**Key Swift patterns used:**
- `private(set)` - read externally, write only internally
- `default: []` subscript - avoids nil checks when appending to dictionary arrays
- `mutating` - required for value-type mutation

## Building Graphs from Tracks

Connect sequential points in a track, closing the loop:

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

The `zip` + `dropFirst` pattern avoids manual index management and previous-point tracking variables.

## Breadth-First Exploration

Discover all reachable vertices from a starting point, tracking steps for visualization:

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

**Algorithm properties:**
- Returns array of arrays - each inner array is one BFS "step"
- `seen` set prevents infinite loops in cyclic graphs
- Enables step-by-step animation of graph exploration

## Animated Visualization on MapKit

Render BFS steps progressively using recursive dispatch:

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

Using `ArraySlice` avoids copying the array at each recursive step.

## Making Coordinates Hashable

`CLLocationCoordinate2D` is not `Hashable`. Wrap it:

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

## Performance Considerations

| Operation | Adjacency List | Adjacency Matrix |
|-----------|---------------|-----------------|
| Add edge | O(1) | O(1) |
| Check edge exists | O(degree) | O(1) |
| All neighbors | O(degree) | O(V) |
| Memory | O(V + E) | O(V^2) |

For sparse geographic graphs (roads, trails), adjacency lists are strongly preferred.

## Gotchas

- **Floating-point coordinate equality:** Two GPS points that should be the same location may differ by tiny amounts. When using coordinates as dictionary keys, consider rounding to a fixed precision or using a spatial index instead of exact equality.
- **Disconnected components:** Building a graph from independent tracks produces disconnected subgraphs. BFS from one track's vertex will only explore that track. You need explicit edge-merging logic to connect tracks at intersections, typically by finding points within a distance threshold.
- **MapKit overlay performance:** Adding thousands of `MKPolyline` overlays to a map view causes severe frame drops. For debugging visualization this is acceptable, but production code should use a single `MKMultiPolyline` or custom tile rendering.

## See Also

- [[mapkit-integration]]
- [[swift-collections-beyond-arrays]]
- [[swift-structs-and-classes]]
