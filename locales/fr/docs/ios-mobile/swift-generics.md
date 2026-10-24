---
title: "Génériques en Swift"
description: "Fonctions et types réutilisables et sûrs au niveau des types, avec paramètres génériques, contraintes et types associés"
level: 3
source_sha256: fa019ab334b9865714d8ecd538cb990fa731042cc5edc0fa709cf2d4053ea7de
translation: machine
translated_at: '2026-10-24'
---
# Génériques en Swift {#swift-generics}

Les génériques permettent d'écrire des fonctions et des types flexibles et réutilisables qui fonctionnent avec n'importe quel type de données tout en préservant la sûreté des types. Ils évitent d'avoir à écrire la même logique pour différents types.

## Le problème {#the-problem}

Sans génériques, il faut des fonctions séparées pour chaque type :

```swift
func getMiddleElement(from array: [Int]) -> Int {
    return array[array.count / 2]
}

func getMiddleElementString(from array: [String]) -> String {
    return array[array.count / 2]
}
// Duplicating logic for every type is unsustainable
```

## Fonctions génériques {#generic-functions}

Utilisez un paramètre de type (par convention `T`) entre chevrons :

```swift
func getMiddleElement<T>(from array: [T]) -> T {
    return array[array.count / 2]
}

let numbers = [1, 2, 3, 4, 5]
let texts = ["hello", "world", "swift"]

getMiddleElement(from: numbers)  // 3 (Int)
getMiddleElement(from: texts)    // "world" (String)
```

Swift déduit `T` à partir du type de l'argument. Aucune annotation de type explicite n'est nécessaire à l'appel.

## Types génériques {#generic-types}

Les classes, les structures et les énumérations peuvent être génériques :

```swift
struct Stack<Element> {
    private var items: [Element] = []

    mutating func push(_ item: Element) {
        items.append(item)
    }

    mutating func pop() -> Element? {
        return items.popLast()
    }

    var top: Element? {
        return items.last
    }

    var isEmpty: Bool {
        return items.isEmpty
    }
}

var intStack = Stack<Int>()
intStack.push(1)
intStack.push(2)

var stringStack = Stack<String>()
stringStack.push("hello")
```

## Contraintes de type {#type-constraints}

Restreignez les types génériques à ceux qui se conforment à un protocole :

```swift
// T must be Comparable
func findMax<T: Comparable>(in array: [T]) -> T? {
    guard var maxValue = array.first else { return nil }
    for item in array {
        if item > maxValue {
            maxValue = item
        }
    }
    return maxValue
}

findMax(in: [3, 1, 4, 1, 5])   // 5
findMax(in: ["b", "a", "c"])    // "c"
```

Contraintes de protocole courantes :
- `Comparable` - prend en charge `<`, `>`, `<=`, `>=`
- `Equatable` - prend en charge `==`, `!=`
- `Hashable` - peut être utilisé comme clé de dictionnaire ou dans des ensembles
- `Codable` - encodage/décodage JSON
- `CustomStringConvertible` - possède la propriété description

## Clauses where {#where-clauses}

Pour des contraintes plus complexes :

```swift
func allEqual<T: Equatable>(in array: [T]) -> Bool where T: Hashable {
    return Set(array).count <= 1
}

// Multiple generic types with relationships
func convert<Input, Output>(value: Input, using transform: (Input) -> Output) -> Output {
    return transform(value)
}
```

## Types associés dans les protocoles {#associated-types-in-protocols}

Les protocoles peuvent avoir un comportement de type générique grâce aux types associés :

```swift
protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
    var count: Int { get }
    subscript(i: Int) -> Item { get }
}

struct IntArray: Container {
    typealias Item = Int  // Swift can usually infer this
    var items: [Int] = []

    mutating func append(_ item: Int) {
        items.append(item)
    }
    var count: Int { items.count }
    subscript(i: Int) -> Int { items[i] }
}
```

## Utilisations pratiques dans le développement iOS {#practical-uses-in-ios-development}

Les génériques sont omniprésents en Swift et sur iOS :

```swift
// Networking: generic response parsing
func fetchData<T: Decodable>(from url: URL) async throws -> T {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(T.self, from: data)
}

let user: User = try await fetchData(from: userURL)
let posts: [Post] = try await fetchData(from: postsURL)

// SwiftUI: generic view builders
struct CardView<Content: View>: View {
    let content: Content

    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }

    var body: some View {
        VStack {
            content
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .shadow(radius: 4)
    }
}
```

## Pièges à éviter {#gotchas}

- **L'effacement de type est parfois nécessaire.** Vous ne pouvez pas utiliser directement un protocole comportant des types associés comme type concret (par exemple, `var container: Container` ne compile pas). Utilisez `any Container` (Swift 5.7+) ou des wrappers à effacement de type.
- **L'inférence de type générique peut échouer avec des expressions complexes.** Si le compilateur ne parvient pas à déduire `T`, vous devrez peut-être ajouter une annotation de type explicite : `let result: MyType = genericFunction()`.
- **Les génériques sont résolus à la compilation.** Il n'y a aucun surcoût à l'exécution par rapport à l'écriture de fonctions spécifiques à chaque type. Le compilateur génère du code spécialisé pour chaque type concret utilisé.

## Références croisées {#cross-references}

- [[swift-fundamentals]] - syntaxe de base de Swift
- [[swift-structs-and-classes]] - structures et classes génériques
- [[swiftui-state-and-data-flow]] - wrappers de propriétés génériques
- [[swiftui-networking]] - clients d'API génériques
