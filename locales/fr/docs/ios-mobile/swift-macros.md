---
title: "Macros Swift"
description: "Génération de code à la compilation via des macros attachées et autonomes, reposant sur la transformation d'AST en Swift 5.9+"
level: 3
source_sha256: 0bf8ef706588814eada3532ad488ee2256e7159c918009b9ad41dc0291a0b044
translation: machine
translated_at: '2026-10-24'
---
# Macros Swift {#swift-macros}

Les macros Swift (5.9+) génèrent du code répétitif à la compilation en transformant l'arbre syntaxique abstrait (AST). Elles opèrent au niveau syntaxique, et non sémantique : elles voient des tokens et une structure, et non des types résolus.

## Rôles des macros {#macro-roles}

| Rôle | Décorateur | Finalité |
|------|-----------|---------|
| `@attached(member)` | `@MyMacro` sur un type | Ajoute des membres (propriétés, méthodes, initialiseurs) |
| `@attached(extension)` | `@MyMacro` sur un type | Ajoute des conformances à des protocoles |
| `@attached(peer)` | `@MyMacro` sur une déclaration | Crée des déclarations soeurs |
| `@attached(accessor)` | `@MyMacro` sur une propriété | Ajoute get/set/willSet/didSet |
| `@freestanding(expression)` | `#myMacro(...)` | Produit une expression |
| `@freestanding(declaration)` | `#myMacro(...)` | Produit des déclarations |

## Exemple de programmation structurelle {#structural-programming-example}

Une macro qui génère automatiquement des représentations structurelles pour des types, permettant le parcours générique, la sérialisation et la génération d'interfaces :

```swift
@attached(member, names: named(Structure), named(structure), named(init(structure:)))
@attached(extension, conformances: Structural)
public macro AddStructural() = #externalMacro(
    module: "StructuralMacros",
    type: "AddStructuralMacro"
)
```

**Utilisation :**

```swift
@AddStructural
struct User {
    var name: String
    var age: Int
}
```

**Code généré :**

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

## Prise en charge des enums {#enum-support}

Étendre les macros aux enums nécessite une représentation structurelle différente :

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

Pour un enum avec les cas `paperback` et `hardcover(title: String)` :

```swift
typealias Structure = Enum<Choice<Empty, Choice<List<Property<String>, Empty>, Nothing>>>
```

## Implémentation de la macro {#macro-implementation}

Les implémentations de macros opèrent sur les types de `SwiftSyntax` :

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

### Extraction des propriétés des structs {#extracting-properties-from-structs}

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

### Extraction des cas d'un enum {#extracting-enum-cases}

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

### Génération d'alias de types avec reduce {#generating-type-aliases-with-reduce}

Construire des types imbriqués de l'intérieur vers l'extérieur en utilisant `reversed().reduce()` :

```swift
let typeDecl: DeclSyntax = storedProperties.reversed().reduce("Empty" as TypeSyntax) {
    result, property in
    "List<Property<\(property.type)>, \(result)>"
}
```

## Débogage des macros {#debugging-macros}

Utilisez la fonction **Expand Macro** de Xcode (clic droit sur `@AddStructural`) pour voir le code généré en ligne.

**Cycle de travail :**
1. Modifier l'implémentation de la macro
2. Nettoyer le dossier de build (Cmd+Maj+K)
3. Recompiler
4. Développer la macro pour vérifier

Xcode met parfois en cache les expansions de macros. Si le code développé ne se met pas à jour après une modification du source de la macro, nettoyez et recompilez.

## Pièges courants {#gotchas}

- **Syntaxe uniquement :** les macros ne peuvent pas résoudre les types, vérifier les conformances ni rechercher des déclarations. Elles voient uniquement des tokens syntaxiques bruts. Si vous avez besoin que `MKCoordinateRegion` existe, vous ne pouvez pas le vérifier : vous générez du code qui le référence et laissez le compilateur contrôler.
- **Interpolation de chaînes dans le code généré :** utilisez `\(raw:)` pour les identifiants et `\(literal:)` pour les littéraux de chaînes dans les chaînes `DeclSyntax` générées. Une mauvaise interpolation provoque des erreurs de compilation difficiles à déboguer dans le code généré.
- **Cache de Xcode :** modifier le code source de la macro ne déclenche pas toujours une nouvelle expansion. Nettoyez toujours le dossier de build lorsque vous itérez sur l'implémentation d'une macro. C'est particulièrement pénible pendant le développement.
- **Surface de l'API SwiftSyntax :** l'arbre syntaxique possède une API très vaste. Utilisez [Swift AST Explorer](https://swift-ast-explorer.com) pour découvrir les types de nœuds et les noms de propriétés plutôt que de deviner.

## Voir aussi {#see-also}

- [[swift-generics]]
- [[swift-enums-and-optionals]]
