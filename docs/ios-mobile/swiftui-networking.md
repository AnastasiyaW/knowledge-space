---
title: SwiftUI Networking and JSON Decoding
category: concepts
tags: [ios-mobile, swiftui, networking, async-await, json, codable, urlsession, asyncimage]
---

# SwiftUI Networking and JSON Decoding

Networking in SwiftUI uses Swift's async/await with URLSession for HTTP requests and Codable/Decodable for JSON parsing. This entry covers the full pattern from data models through fetch services to view integration.

## Key Facts

- `async`/`await` is Swift's native concurrency model - no completion handlers needed
- `URLSession.shared.data(from: url)` returns `(Data, URLResponse)` tuple
- `JSONDecoder` with `.convertFromSnakeCase` maps JSON snake_case to Swift camelCase
- `Decodable` protocol enables automatic JSON-to-struct parsing
- `AsyncImage` loads and displays images from URLs with built-in placeholder support
- Views are synchronous - use `.task` or `Task { }` to bridge to async context
- Optional properties (`var death: Death?`) handle missing JSON keys gracefully

## Patterns

### Data Models with Decodable

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

### JSON Decoding from Bundle (Synchronous)

```swift
if let url = Bundle.main.url(forResource: "jpapexpredators", withExtension: "json") {
    let data = try Data(contentsOf: url)
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    let results = try decoder.decode([ApexPredator].self, from: data)
}
```

Force-try (`try!`) is acceptable when: (1) file is bundled, (2) verified at dev time, (3) crash = programmer error.

### Fetch Service

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

### Core async/await Pattern

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

- `async` marks a function that can suspend
- `await` waits for async result without blocking the thread
- `throws`/`try` - standard Swift error propagation

### Running async Functions in Views

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

`.task` cancels automatically when the view disappears.

### AsyncImage

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

Only works in live preview or simulator (not static preview mode).

### JSONDecoder Key Strategies

```swift
let decoder = JSONDecoder()

// Default: exact match
decoder.keyDecodingStrategy = .useDefaultKeys

// Snake to camel (JSON "first_name" -> Swift "firstName")
decoder.keyDecodingStrategy = .convertFromSnakeCase
```

### Custom CodingKeys

Override property-to-JSON key mapping when `.convertFromSnakeCase` is insufficient:

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

### Fetch and Store in Persistence (Core Data Example)

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

### Switch on Status for Conditional Views

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

## Gotchas

- `URLSession.shared.data(from:)` requires `async` context - cannot call from synchronous view body directly
- `guard let url = URL(string:)` can fail with special characters in strings - encode spaces and symbols first
- `.convertFromSnakeCase` only handles standard snake_case; nested keys or unusual patterns need custom `CodingKeys`
- `AsyncImage` makes a new request every time the view redraws - consider caching for frequently-displayed images
- `try!` on network responses crashes the app - use `do/catch` for all remote data
- Optional Decodable properties (`var death: Death?`) silently become nil if the JSON key is missing, but error if the key exists with wrong type

## See Also

- [[swiftui-state-and-data-flow]] - @Observable ViewModel for network state
- [[swiftdata-persistence]] - storing fetched data with SwiftData
- [[core-data-persistence]] - storing fetched data with Core Data
- [[swift-enums-and-optionals]] - error enums, optionals in Decodable models
