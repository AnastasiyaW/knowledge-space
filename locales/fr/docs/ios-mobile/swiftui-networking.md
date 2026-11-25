---
title: "Réseau SwiftUI et décodage JSON"
category: concepts
tags: [ios-mobile, swiftui, networking, async-await, json, codable, urlsession, asyncimage]
level: 3
source_sha256: 0beed9bbe339b2ca3ab6247ccf398e1047cc821c7976158b41d17284c94f3064
translation: machine
translated_at: '2026-10-24'
---
# Réseau SwiftUI et décodage JSON {#swiftui-networking-and-json-decoding}

Le réseau dans SwiftUI repose sur async/await de Swift avec URLSession pour les requêtes HTTP, et Codable/Decodable pour l'analyse du JSON. Cette entrée couvre le schéma complet, depuis les modèles de données jusqu'aux services de récupération et à l'intégration dans les vues.

## Points clés {#key-facts}

- `async`/`await` est le modèle de concurrence natif de Swift : aucun completion handler n'est nécessaire
- `URLSession.shared.data(from: url)` renvoie un tuple `(Data, URLResponse)`
- `JSONDecoder` avec `.convertFromSnakeCase` fait correspondre le snake_case du JSON au camelCase de Swift
- Le protocole `Decodable` permet l'analyse automatique du JSON vers une struct
- `AsyncImage` charge et affiche des images depuis des URL, avec un placeholder intégré
- Les vues sont synchrones : utilisez `.task` ou `Task { }` pour passer dans un contexte asynchrone
- Les propriétés optionnelles (`var death: Death?`) gèrent proprement les clés JSON absentes

## Schémas {#patterns}

### Modèles de données avec Decodable {#data-models-with-decodable}

```swift
struct Quote: Decodable {
    let quote: String
    let character: String
    let author: String
}

struct Character: Decodable {
    let name: String
    let birthday: String
    let occupations: [String]
    let images: [URL]           // JSONDecoder auto-converts URL strings
    let portrayedBy: String     // snake_case "portrayed_by" with .convertFromSnakeCase
    var death: Death?            // optional - nil if key absent
}
```

### Décodage JSON depuis le bundle (synchrone) {#json-decoding-from-bundle-synchronous}

```swift
if let url = Bundle.main.url(forResource: "jpapexpredators", withExtension: "json") {
    let data = try Data(contentsOf: url)
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    let results = try decoder.decode([ApexPredator].self, from: data)
}
```

Le force-try (`try!`) est acceptable lorsque : (1) le fichier est embarqué dans le bundle, (2) il a été vérifié au moment du développement, (3) un crash relève d'une erreur du programmeur.

### Service de récupération {#fetch-service}

```swift
struct FetchService {
    private enum FetchError: Error {
        case missingData
    }

    func fetchQuote(from show: String) async throws -> Quote {
        let urlString = "https://api.example.com/quotes/\(show.replacingOccurrences(of: " ", with: "%20"))"
        guard let url = URL(string: urlString) else { throw FetchError.missingData }

        let (data, response) = try await URLSession.shared.data(from: url)

        guard let response = response as? HTTPURLResponse,
              response.statusCode == 200 else {
            throw FetchError.missingData
        }

        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode([Quote].self, from: data).randomElement()!
    }
}
```

### Schéma async/await de base {#core-asyncawait-pattern}

```swift
// Fetch data from a URL
let (data, response) = try await URLSession.shared.data(from: url)

// Check HTTP status
guard let httpResponse = response as? HTTPURLResponse,
      httpResponse.statusCode == 200 else {
    throw SomeError.badResponse
}

// Decode JSON
let decoder = JSONDecoder()
decoder.keyDecodingStrategy = .convertFromSnakeCase
let result = try decoder.decode(MyType.self, from: data)
let array = try decoder.decode([MyType].self, from: data)
```

- `async` marque une fonction pouvant se suspendre
- `await` attend le résultat asynchrone sans bloquer le thread
- `throws`/`try` : propagation standard des erreurs en Swift

### Exécuter des fonctions async dans les vues {#running-async-functions-in-views}

```swift
// Automatically on view appear (preferred)
.task {
    await vm.getData(for: show)
}

// In Button action
Button("Fetch") {
    Task {
        await vm.getData(for: show)   // Task bridges sync -> async
    }
}

// Auto-fetch with condition
.task {
    if pokedex.isEmpty {
        await getPokemon(from: 1)
    }
}
```

`.task` est annulée automatiquement lorsque la vue disparaît.

### AsyncImage {#asyncimage}

```swift
AsyncImage(url: character.images.first) { image in
    image
        .resizable()
        .scaledToFill()
} placeholder: {
    ProgressView()
}
.frame(width: 200, height: 250)
.clipShape(.rect(cornerRadius: 15))
```

Ne fonctionne que dans l'aperçu en direct ou dans le simulateur (pas en mode aperçu statique).

### Stratégies de décodage des clés de JSONDecoder {#jsondecoder-key-strategies}

```swift
let decoder = JSONDecoder()

// Default: exact match
decoder.keyDecodingStrategy = .useDefaultKeys

// Snake to camel (JSON "first_name" -> Swift "firstName")
decoder.keyDecodingStrategy = .convertFromSnakeCase
```

### CodingKeys personnalisées {#custom-codingkeys}

Redéfinissez la correspondance entre propriétés et clés JSON lorsque `.convertFromSnakeCase` ne suffit pas :

```swift
struct Character: Decodable {
    let name: String
    let portrayedBy: String

    enum CodingKeys: String, CodingKey {
        case name
        case portrayedBy = "portrayed_by"
    }
}
```

### Récupérer et stocker dans la persistance (exemple Core Data) {#fetch-and-store-in-persistence-core-data-example}

```swift
func getPokemon(from id: Int) async {
    for i in id...151 {
        let urlString = "https://pokeapi.co/api/v2/pokemon/\(i)"
        guard let url = URL(string: urlString) else { continue }

        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            let fetched = try decoder.decode(TempPokemon.self, from: data)

            let pokemon = Pokemon(context: viewContext)
            pokemon.id = Int16(fetched.id)
            pokemon.name = fetched.name
            try viewContext.save()
        } catch {
            print("Error fetching pokemon \(i): \(error)")
        }
    }
}
```

### Switch sur le statut pour des vues conditionnelles {#switch-on-status-for-conditional-views}

```swift
switch vm.status {
case .notStarted:
    EmptyView()
case .fetching:
    ProgressView()
case .success:
    Text("\"\(vm.quote.quote)\"")
case .failed(let error):
    Text(error.localizedDescription)
        .foregroundStyle(.red)
}
```

## Pièges {#gotchas}

- `URLSession.shared.data(from:)` exige un contexte `async` : on ne peut pas l'appeler directement depuis le corps synchrone d'une vue
- `guard let url = URL(string:)` peut échouer avec des caractères spéciaux : encodez d'abord les espaces et les symboles
- `.convertFromSnakeCase` ne gère que le snake_case standard ; les clés imbriquées ou les formes inhabituelles nécessitent des `CodingKeys` personnalisées
- `AsyncImage` effectue une nouvelle requête à chaque redessin de la vue : envisagez un cache pour les images fréquemment affichées
- `try!` sur les réponses réseau fait planter l'application : utilisez `do/catch` pour toutes les données distantes
- Les propriétés Decodable optionnelles (`var death: Death?`) deviennent silencieusement nil si la clé JSON est absente, mais provoquent une erreur si la clé existe avec un type incorrect

## Voir aussi {#see-also}

- [[swiftui-state-and-data-flow]] - ViewModel @Observable pour l'état réseau
- [[swiftdata-persistence]] - stocker les données récupérées avec SwiftData
- [[core-data-persistence]] - stocker les données récupérées avec Core Data
- [[swift-enums-and-optionals]] - enums d'erreurs, optionnels dans les modèles Decodable
