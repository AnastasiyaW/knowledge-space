---
title: "Swift Macros"
description: "Compile-time code generation via attached and freestanding macros using AST transformation in Swift 5.9+"
---

# Swift Macros

Swift macros (5.9+) generate boilerplate code at compile time by transforming the abstract syntax tree. They operate at the syntax level, not semantic level - they see tokens and structure, not resolved types.

## Macro Roles

| Role | Decorator | Purpose |
|------|-----------|---------|
| `@attached(member)` | `@MyMacro` on type | Adds members (properties, methods, initializers) |
| `@attached(extension)` | `@MyMacro` on type | Adds protocol conformances |
| `@attached(peer)` | `@MyMacro` on declaration | Creates sibling declarations |
| `@attached(accessor)` | `@MyMacro` on property | Adds get/set/willSet/didSet |
| `@freestanding(expression)` | `#myMacro(...)` | Produces an expression |
| `@freestanding(declaration)` | `#myMacro(...)` | Produces declarations |

## Structural Programming Example

A macro that auto-generates structural representations for types - enabling generic traversal, serialization, and UI generation:

```swift
@attached(member, names: named(Structure), named(structure), named(init(structure:)))
@attached(extension, conformances: Structural)
public macro AddStructural() = #externalMacro(
    module: "StructuralMacros",
    type: "AddStructuralMacro"
)
```

**Usage:**

```swift
@AddStructural
struct User {
    var name: String
    var age: Int
}
```

**Generated code:**

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

## Enum Support

Extending macros to handle enums requires a different structural representation:

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

For an enum with cases `paperback` and `hardcover(title: String)`:

```swift
typealias Structure = Enum<Choice<Empty, Choice<List<Property<String>, Empty>, Nothing>>>
```

## Macro Implementation

Macro implementations operate on `SwiftSyntax` types:

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

### Extracting Properties from Structs

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

### Extracting Enum Cases

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

### Generating Type Aliases with Reduce

Build nested types from inside out using `reversed().reduce()`:

```swift
let typeDecl: DeclSyntax = storedProperties.reversed().reduce("Empty" as TypeSyntax) {
    result, property in
    "List<Property<\(property.type)>, \(result)>"
}
```

## Debugging Macros

Use Xcode's **Expand Macro** feature (right-click on `@AddStructural`) to see generated code inline.

**Iteration workflow:**
1. Change the macro implementation
2. Clean build folder (Cmd+Shift+K)
3. Rebuild
4. Expand macro to verify

Xcode sometimes caches macro expansions. If the expanded code doesn't update after changing the macro source, clean and rebuild.

## Gotchas

- **Syntax-level only:** Macros cannot resolve types, check conformances, or look up declarations. They see raw syntax tokens. If you need `MKCoordinateRegion` to exist, you cannot verify it - you generate code that references it and let the compiler check.
- **String interpolation in generated code:** Use `\(raw:)` for identifiers and `\(literal:)` for string literals inside the generated `DeclSyntax` strings. Incorrect interpolation causes hard-to-debug compile errors in generated code.
- **Xcode caching:** Changing macro source code does not always trigger re-expansion. Always clean build folder when iterating on macro implementations. This is especially painful during development.
- **SwiftSyntax API surface:** The syntax tree has an enormous API surface. Use the [Swift AST Explorer](https://swift-ast-explorer.com) to discover node types and property names rather than guessing.

## See Also

- [[swift-generics]]
- [[swift-enums-and-optionals]]
