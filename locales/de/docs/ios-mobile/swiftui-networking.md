---
title: "SwiftUI-Netzwerkzugriff und JSON-Dekodierung"
category: concepts
tags: [ios-mobile, swiftui, networking, async-await, json, codable, urlsession, asyncimage]
level: 3
source_sha256: 0beed9bbe339b2ca3ab6247ccf398e1047cc821c7976158b41d17284c94f3064
translation: machine
translated_at: '2026-10-24'
---
# SwiftUI-Netzwerkzugriff und JSON-Dekodierung {#swiftui-networking-and-json-decoding}

Netzwerkzugriff in SwiftUI verwendet Swifts async/await mit URLSession für HTTP-Anfragen und Codable/Decodable für das JSON-Parsing. Dieser Eintrag beschreibt das vollständige Muster von den Datenmodellen über die Fetch-Services bis zur Integration in die Views.

## Wichtige Fakten {#key-facts}

- `async`/`await` ist Swifts natives Concurrency-Modell - keine Completion-Handler nötig
- `URLSession.shared.data(from: url)` gibt ein `(Data, URLResponse)`-Tupel zurück
- `JSONDecoder` mit `.convertFromSnakeCase` bildet JSON-snake_case auf Swift-camelCase ab
- Das `Decodable`-Protokoll ermöglicht das automatische Parsen von JSON in Structs
- `AsyncImage` lädt und zeigt Bilder von URLs an und bietet eine integrierte Platzhalter-Unterstützung
- Views sind synchron - `.task` oder `Task { }` verwenden, um in den asynchronen Kontext zu wechseln
- Optionale Properties (`var death: Death?`) behandeln fehlende JSON-Schlüssel robust

## Muster {#patterns}

### Datenmodelle mit Decodable {#data-models-with-decodable}

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

### JSON-Dekodierung aus dem Bundle (synchron) {#json-decoding-from-bundle-synchronous}

```swift
if let url = Bundle.main.url(forResource: "jpapexpredators", withExtension: "json") {
    let data = try Data(contentsOf: url)
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    let results = try decoder.decode([ApexPredator].self, from: data)
}
```

Force-try (`try!`) ist akzeptabel, wenn: (1) die Datei im Bundle enthalten ist, (2) sie zur Entwicklungszeit verifiziert wurde, (3) ein Absturz einen Programmierfehler darstellt.

### Fetch-Service {#fetch-service}

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

### Grundlegendes async/await-Muster {#core-asyncawait-pattern}

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

- `async` markiert eine Funktion, die suspendieren kann
- `await` wartet auf das asynchrone Ergebnis, ohne den Thread zu blockieren
- `throws`/`try` - standardmäßige Fehlerweitergabe in Swift

### Ausführung von async-Funktionen in Views {#running-async-functions-in-views}

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

`.task` wird automatisch abgebrochen, wenn die View verschwindet.

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

Funktioniert nur in der Live-Vorschau oder im Simulator (nicht im statischen Vorschau-Modus).

### JSONDecoder-Dekodierungsstrategien {#jsondecoder-key-strategies}

```swift
let decoder = JSONDecoder()

// Default: exact match
decoder.keyDecodingStrategy = .useDefaultKeys

// Snake to camel (JSON "first_name" -> Swift "firstName")
decoder.keyDecodingStrategy = .convertFromSnakeCase
```

### Benutzerdefinierte CodingKeys {#custom-codingkeys}

Die Zuordnung von Properties zu JSON-Schlüsseln überschreiben, wenn `.convertFromSnakeCase` nicht ausreicht:

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

### Abrufen und Speichern in der Persistenz (Core-Data-Beispiel) {#fetch-and-store-in-persistence-core-data-example}

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

### switch auf Status für bedingte Views {#switch-on-status-for-conditional-views}

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

## Fallstricke {#gotchas}

- `URLSession.shared.data(from:)` erfordert einen `async`-Kontext - kann nicht direkt aus einem synchronen View-Body aufgerufen werden
- `guard let url = URL(string:)` kann bei Sonderzeichen in Strings fehlschlagen - Leerzeichen und Symbole zuerst kodieren
- `.convertFromSnakeCase` unterstützt nur Standard-snake_case; verschachtelte Schlüssel oder ungewöhnliche Muster erfordern benutzerdefinierte `CodingKeys`
- `AsyncImage` stellt bei jedem Neuzeichnen der View eine neue Anfrage - bei häufig angezeigten Bildern Caching in Betracht ziehen
- `try!` bei Netzwerkantworten lässt die App abstürzen - für alle Remote-Daten `do/catch` verwenden
- Optionale Decodable-Properties (`var death: Death?`) werden stillschweigend zu nil, wenn der JSON-Schlüssel fehlt, führen aber zu einem Fehler, wenn der Schlüssel mit falschem Typ vorhanden ist

## Siehe auch {#see-also}

- [[swiftui-state-and-data-flow]] - @Observable-ViewModel für den Netzwerkzustand
- [[swiftdata-persistence]] - Speichern abgerufener Daten mit SwiftData
- [[core-data-persistence]] - Speichern abgerufener Daten mit Core Data
- [[swift-enums-and-optionals]] - Fehler-Enums, Optionals in Decodable-Modellen
