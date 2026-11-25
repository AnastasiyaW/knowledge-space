---
title: "Algorithmes sur les graphes en Swift"
description: "Graphes en liste d'adjacence, parcours BFS/DFS et algorithmes de plus court chemin, avec exemples de cartographie"
level: 3
source_sha256: d750ecf2368d93bce6f2ba23077ea24c4129c35288a648ecf88a3f84896ff0d1
translation: machine
translated_at: '2026-10-24'
---
# Algorithmes sur les graphes en Swift {#graph-algorithms-in-swift}

Construction de structures de données de graphes et d'algorithmes de parcours en Swift, avec des exemples concrets issus d'applications géographiques et cartographiques.

## Structure de données de graphe {#graph-data-structure}

Une représentation par liste d'adjacence à l'aide d'un dictionnaire :

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

**Particularités de Swift utilisées :**
- `private(set)` - lecture externe, écriture uniquement en interne
- Subscript avec `default: []` - évite les vérifications de `nil` lors de l'ajout à des tableaux stockés dans le dictionnaire
- `mutating` - requis pour la modification d'un type valeur

## Construction de graphes à partir de tracés {#building-graphs-from-tracks}

Relier les points successifs d'un tracé en fermant la boucle :

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

Le motif `zip` + `dropFirst` évite la gestion manuelle des indices et les variables de suivi du point précédent.

## Exploration en largeur {#breadth-first-exploration}

Découvrir tous les sommets atteignables depuis un point de départ, en conservant les étapes pour la visualisation :

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

**Propriétés de l'algorithme :**
- Renvoie un tableau de tableaux : chaque tableau interne correspond à une étape du BFS
- L'ensemble `seen` empêche les boucles infinies dans les graphes cycliques
- Permet une animation pas à pas de l'exploration du graphe

## Visualisation animée sur MapKit {#animated-visualization-on-mapkit}

Afficher progressivement les étapes du BFS grâce à une distribution récursive :

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

Utiliser `ArraySlice` évite de copier le tableau à chaque appel récursif.

## Rendre les coordonnées hachables {#making-coordinates-hashable}

`CLLocationCoordinate2D` n'est pas `Hashable`. Il faut l'encapsuler :

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

## Considérations de performance {#performance-considerations}

| Opération | Liste d'adjacence | Matrice d'adjacence |
|-----------|-------------------|---------------------|
| Ajouter une arête | O(1) | O(1) |
| Vérifier l'existence d'une arête | O(degré) | O(1) |
| Tous les voisins | O(degré) | O(V) |
| Mémoire | O(V + E) | O(V^2) |

Pour les graphes géographiques peu denses (routes, sentiers), les listes d'adjacence sont largement préférables.

## Pièges à éviter {#gotchas}

- **Égalité de coordonnées en virgule flottante :** Deux points GPS censés correspondre au même lieu peuvent différer de quantités infimes. Lorsque l'on utilise des coordonnées comme clés de dictionnaire, il est conseillé d'arrondir à une précision fixe ou d'utiliser un index spatial plutôt qu'une égalité stricte.
- **Composantes déconnectées :** Construire un graphe à partir de tracés indépendants produit des sous-graphes déconnectés. Un BFS partant du sommet d'un tracé n'explorera que ce tracé. Il faut une logique explicite de fusion d'arêtes pour relier les tracés aux intersections, généralement en recherchant les points situés sous un seuil de distance.
- **Performance des superpositions MapKit :** Ajouter des milliers d'overlays `MKPolyline` à une vue de carte provoque de sérieuses chutes de fréquence d'images. Pour une visualisation de débogage, cela reste acceptable, mais le code de production doit utiliser un seul `MKMultiPolyline` ou un rendu de tuiles personnalisé.

## Voir aussi {#see-also}

- [[mapkit-integration]]
- [[swift-collections-beyond-arrays]]
- [[swift-structs-and-classes]]
