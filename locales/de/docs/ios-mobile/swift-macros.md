---
title: "Swift-Makros"
description: "Codegenerierung zur Kompilierzeit über angehängte und freistehende Makros mit AST-Transformation in Swift 5.9+"
level: 3
source_sha256: 0bf8ef706588814eada3532ad488ee2256e7159c918009b9ad41dc0291a0b044
translation: machine
translated_at: '2026-10-24'
---
# Swift-Makros {#swift-macros}

Swift-Makros (5.9+) erzeugen zur Kompilierzeit Boilerplate-Code, indem sie den abstrakten Syntaxbaum transformieren. Sie arbeiten auf Syntaxebene, nicht auf semantischer Ebene: Sie sehen Tokens und Struktur, nicht aufgelöste Typen.

## Makro-Rollen {#macro-roles}

| Rolle | Dekorator | Zweck |
|-------|-----------|-------|
| `@attached(member)` | `@MyMacro` auf Typ | Fügt Member hinzu (Properties, Methoden, Initializer) |
| `@attached(extension)` | `@MyMacro` auf Typ | Fügt Protokollkonformitäten hinzu |
| `@attached(peer)` | `@MyMacro` auf Deklaration | Erzeugt Geschwisterdeklarationen |
| `@attached(accessor)` | `@MyMacro` auf Property | Fügt get/set/willSet/didSet hinzu |
| `@freestanding(expression)` | `#myMacro(...)` | Erzeugt einen Ausdruck |
| `@freestanding(declaration)` | `#myMacro(...)` | Erzeugt Deklarationen |

## Beispiel für strukturelle Programmierung {#structural-programming-example}

Ein Makro, das strukturelle Repräsentationen für Typen automatisch generiert und damit generische Traversierung, Serialisierung und UI-Erzeugung ermöglicht:

```swift
@attached(member, names: named(Structure), named(structure), named(init(structure:)))
@attached(extension, conformances: Structural)
public macro AddStructural() = #externalMacro(
    module: "StructuralMacros",
    type: "AddStructuralMacro"
)
```

**Verwendung:**

```swift
@AddStructural
struct User {
    var name: String
    var age: Int
}
```

**Generierter Code:**

```swift
extension User: Structural {
    typealias Structure = Struct<List<Property<String>, List<Property<Int>, Empty>>>

    var structure: Structure {
        Struct(name: "User", properties:
            List(head: Property(name: "name", value: name),
                 tail: List(head: Property(name: "age", value: age),
                            tail: Empty())))
    }

    init(structure s: Structure) {
        self.name = s.properties.head.value
        self.age = s.properties.tail.head.value
    }
}
```

## Unterstützung für Enums {#enum-support}

Die Erweiterung von Makros auf Enums erfordert eine andere strukturelle Repräsentation:

```swift
// Choice type for enum cases (like Either)
public enum Choice<First, Second> {
    case first(First)
    case second(Second)
}

// Nothing type - uninhabited, used as the terminal case
public enum Nothing {}

// Enum wrapper (like Struct but for enums)
public struct Enum<Cases> {
    public let name: String
    public let cases: Cases
}
```

Für ein Enum mit den Fällen `paperback` und `hardcover(title: String)`:

```swift
typealias Structure = Enum<Choice<Empty, Choice<List<Property<String>, Empty>, Nothing>>>
```

## Makro-Implementierung {#macro-implementation}

Makro-Implementierungen arbeiten auf `SwiftSyntax`-Typen:

```swift
struct AddStructuralMacro: MemberMacro {
    static func expansion(
        of node: AttributeSyntax,
        providingMembersOf declaration: some DeclGroupSyntax,
        in context: some MacroExpansionContext
    ) throws -> [DeclSyntax] {
        if let structDecl = declaration.as(StructDeclSyntax.self) {
            return try structExpansion(of: structDecl, in: context)
        } else if let enumDecl = declaration.as(EnumDeclSyntax.self) {
            return try enumExpansion(of: enumDecl, in: context)
        } else {
            throw MacroError("Only works on structs and enums")
        }
    }
}
```

### Properties aus Structs extrahieren {#extracting-properties-from-structs}

```swift
func asStoredProperty(_ member: MemberBlockItemSyntax)
    -> (identifier: TokenSyntax, type: TypeSyntax)? {
    guard let varDecl = member.decl.as(VariableDeclSyntax.self),
          let binding = varDecl.bindings.first,
          let identifier = binding.pattern.as(IdentifierPatternSyntax.self),
          let type = binding.typeAnnotation?.type
    else { return nil }
    return (identifier.identifier, type)
}
```

### Enum-Fälle extrahieren {#extracting-enum-cases}

```swift
func asEnumCase(_ member: MemberBlockItemSyntax)
    -> (identifier: TokenSyntax, parameters: [(TokenSyntax?, TypeSyntax)])? {
    guard let caseDecl = member.decl.as(EnumCaseDeclSyntax.self),
          let element = caseDecl.elements.first
    else { return nil }
    let params = element.parameterClause?.parameters.map { p in
        (p.firstName, p.type)
    } ?? []
    return (element.name, params)
}
```

### Typaliasse mit reduce erzeugen {#generating-type-aliases-with-reduce}

Verschachtelte Typen von innen nach außen aufbauen, indem `reversed().reduce()` verwendet wird:

```swift
let typeDecl: DeclSyntax = storedProperties.reversed().reduce("Empty" as TypeSyntax) {
    result, property in
    "List<Property<\(property.type)>, \(result)>"
}
```

## Makros debuggen {#debugging-macros}

Verwende die Xcode-Funktion **Makro expandieren** (Rechtsklick auf `@AddStructural`), um den generierten Code direkt inline anzuzeigen.

**Iterationsablauf:**
1. Makro-Implementierung ändern
2. Build-Ordner bereinigen (Cmd+Shift+K)
3. Neu bauen
4. Makro expandieren, um das Ergebnis zu prüfen

Xcode speichert Makroexpansionen manchmal im Cache. Wenn sich der expandierte Code nach einer Änderung am Makro-Quellcode nicht aktualisiert, bereinige den Build-Ordner und baue neu.

## Stolperfallen {#gotchas}

- **Nur Syntaxebene:** Makros können Typen nicht auflösen, Konformitäten nicht prüfen und keine Deklarationen nachschlagen. Sie sehen nur rohe Syntax-Tokens. Wenn `MKCoordinateRegion` existieren muss, kannst du das nicht verifizieren. Du erzeugst stattdessen Code, der darauf verweist, und überlässt die Prüfung dem Compiler.
- **String-Interpolation im generierten Code:** Verwende `\(raw:)` für Bezeichner und `\(literal:)` für String-Literale innerhalb der generierten `DeclSyntax`-Strings. Falsche Interpolation führt zu schwer nachvollziehbaren Kompilierfehlern im generierten Code.
- **Xcode-Caching:** Änderungen am Makro-Quellcode lösen nicht immer eine erneute Expansion aus. Bereinige beim Iterieren an Makro-Implementierungen immer den Build-Ordner. Das ist während der Entwicklung besonders mühsam.
- **Umfang der SwiftSyntax-API:** Der Syntaxbaum hat eine enorme API-Oberfläche. Verwende den [Swift AST Explorer](https://swift-ast-explorer.com), um Knotentypen und Property-Namen zu finden, anstatt sie zu raten.

## Siehe auch {#see-also}

- [[swift-generics]]
- [[swift-enums-and-optionals]]
