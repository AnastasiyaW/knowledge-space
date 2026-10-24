---
title: "Typsichere Domänenmodellierung in Swift"
description: "Enums, Structs und Generics einsetzen, um unmögliche Zustände zu eliminieren und APIs selbstdokumentierend zu machen"
level: 3
source_sha256: 941317ef4a5fd5a070f382a95d8ba495ee52e250979f3f16dd387d1fdbed7112
translation: machine
translated_at: '2026-10-24'
---
# Typsichere Domänenmodellierung in Swift {#type-safe-domain-modeling-in-swift}

Die Wahl der richtigen Typrepräsentation eliminiert unmögliche Zustände, reduziert Fehler und macht APIs selbstdokumentierend. Das Typsystem von Swift (Enums, Structs, Optionals, Generics) erlaubt eine präzise Modellierung, die über das hinausgeht, was Sprachen mit ausschließlich Klassen ausdrücken können.

## Das Problem mit Optionals {#the-problem-with-optionals}

Mehrere optionale Parameter erzeugen eine Explosion möglicher Zustände, von denen die meisten ungültig sind:

```swift
// URLSession completion handler: 3 optionals = 8 possible combinations
(Data?, URLResponse?, Error?) -> Void
```

Die meisten Kombinationen sind unsinnig: Daten ohne Antwort, Fehler mit Daten, alles nil. Das Typsystem verhindert dies nicht.

**Bessere Repräsentation mit einem Enum:**

```swift
enum NetworkResult {
    case success(data: Data, response: URLResponse)
    case failure(Error)
}
```

Jetzt existieren nur noch 2 gültige Zustände. Der Compiler erzwingt eine erschöpfende Behandlung.

## Wann Enums Structs schlagen {#when-enums-beat-structs}

Verwende Enums, wenn:
- Zustände **sich gegenseitig ausschließen** (angemeldet ODER abgemeldet, niemals beides)
- verschiedene Zustände **unterschiedliche zugehörige Daten** tragen
- du möchtest, dass der Compiler **erschöpfende Behandlung** erzwingt

```swift
// Struct: 4 possible states (user present/absent x expired true/false)
struct Session {
    var user: User?      // nil = not registered
    var expired: Bool     // only meaningful when user exists
}

// Enum: 3 valid states only
enum SessionState {
    case notRegistered
    case loggedIn(User)
    case expired(User)
}
```

## Wann Structs + Optionals Enums schlagen {#when-structs-optionals-beat-enums}

Wenn mehrere Enum-Fälle denselben zugehörigen Wert teilen, kann eine optionale Struct einfacher sein:

```swift
// Enum with duplicated user in two cases
enum SessionState {
    case loggedIn(User)
    case expired(User)    // same User type
    case notRegistered
}

// Simpler: struct + optional
struct Session {
    var user: User        // non-optional
    var expired: Bool
}
var currentSession: Session?  // nil = not registered
```

Der Zugriff auf `user` erfordert kein Switch – lediglich optional Chaining auf der Session selbst.

## Entwurf von Rückgabetypen bei Funktionen {#function-return-type-design}

Selbst eine einfache Funktion wie „Dateien lesen“ hat viele gültige Typsignaturen:

```swift
// Option 1: Lose information about which files failed
func readFiles(_ names: [String]) -> [Data]

// Option 2: Track which files failed (nil = failure)
func readFiles(_ names: [String]) -> [Data?]

// Option 3: Pair each result with its filename
func readFiles(_ names: [String]) -> [(String, Data?)]

// Option 4: All-or-nothing
func readFiles(_ names: [String]) -> [Data]?

// Option 5: Rich error per file
func readFiles(_ names: [String]) -> [Result<Data, FileError>]
```

Wähle abhängig davon, was der Aufrufer benötigt:
- **Fehlerbehandlung pro Datei** -> Option 3 oder 5
- **Alles-oder-nichts** -> Option 4
- **Einfacher Fall** -> Option 1

## Trade-off bei vorzeichenlosen Ganzzahlen {#unsigned-integer-trade-off}

Die Swift-Standardbibliothek verwendet `Int` (nicht `UInt`) für `Array.count` und Subscript-Indizes, obwohl negative Werte bedeutungslos sind. Dies ist ein bewusster Trade-off:

- **Präzision:** `UInt` eliminiert negative Werte
- **Ergonomie:** Jede Arithmetikoperation mit `Int` erfordert eine Konvertierung

Apple hat sich für Ergonomie entschieden. Die Lehre daraus: **Maximale Typpräzision ist nicht immer das beste Design.**

## Property-Based Testing für Typinvarianten {#property-based-testing-for-type-invariants}

Wenn Typen Einschränkungen nicht vollständig erzwingen können (z. B. „Länge des Ausgabe-Arrays entspricht der Länge des Eingabe-Arrays“), verwende Property-Based Tests:

```swift
func testReadFilesPreservesLength() {
    for _ in 0..<1000 {
        let names = (0..<Int.random(in: 1...20)).map { "file\($0).txt" }
        let results = readFiles(names)
        XCTAssertEqual(results.count, names.count)
    }
}
```

## Checkliste für den Typentwurf {#type-design-checklist}

1. **Liste alle möglichen Zustände** auf, in denen sich deine Daten befinden können
2. **Identifiziere ungültige Kombinationen**, die niemals auftreten sollten
3. **Wähle Typen, die ungültige Zustände eliminieren:**
   - Enum für sich gegenseitig ausschließende Zustände
   - Nicht-optionale Properties für immer vorhandene Daten
   - Phantomtypen für Zustandsautomaten zur Compilezeit
4. **Prüfe:** Kannst du einen Wert deines Typs konstruieren, der etwas Bedeutungsloses darstellt? Falls ja, verschärfe den Typ.

## Fallstricke {#gotchas}

- **Übermäßig präzise Typen:** Wenn jede Einschränkung als Prüfung auf Typebene umgesetzt wird, können APIs unangenehm zu verwenden sein. `UInt` für Array-Indizes ist technisch korrekter, erzeugt aber überall Konvertierungsaufwand. Finde den richtigen Mittelweg zwischen Präzision und Ergonomie.
- **Explosion der Enum-Fälle:** Wenn du 4 optionale Felder hast, bei denen alle 16 Kombinationen gültig sind, ist ein Enum mit 16 Fällen schlechter als 4 Optionals. Enums glänzen, wenn die meisten Kombinationen **ungültig** sind.
- **Migrationsaufwand:** Das Umwandeln einer Struct in ein Enum (oder umgekehrt) ist eine inkompatible API-Änderung. Denke sorgfältig über deine Typwahl nach, bevor du eine öffentliche API veröffentlichst.

## Siehe auch {#see-also}

- [[swift-enums-and-optionals]]
- [[swift-structs-and-classes]]
- [[swift-phantom-types]]
- [[swift-generics]]
