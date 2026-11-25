---
title: "Types fantômes en Swift"
description: "Paramètres de type existant uniquement à la compilation pour imposer des machines à états, la sécurité des unités et des contraintes de domaine"
level: 3
source_sha256: 3af7aca12554057d8b2281168e46b58cda931598829ec36843e5c1366febd6ad
translation: machine
translated_at: '2026-10-24'
---
# Types fantômes en Swift {#swift-phantom-types}

Les types fantômes utilisent des paramètres de type génériques qui n'existent qu'à la compilation : ils apparaissent dans la signature de type, mais ne sont jamais stockés sous forme de valeurs. Cela permet d'imposer à la compilation les transitions d'une machine à états, la sécurité des unités et des contraintes de domaine.

## Concept de base {#core-concept}

Un paramètre de type fantôme est un paramètre qui n'apparaît dans aucune propriété stockée ni dans aucun argument de constructeur :

```swift
struct Path<FileType> {
    private var components: [String]

    private init(components: [String]) {
        self.components = components
    }

    var rendered: String {
        "/" + components.joined(separator: "/")
    }
}
```

`FileType` ne correspond à aucune propriété stockée : il existe uniquement comme marqueur à la compilation.

## Types marqueurs {#marker-types}

Définissez des `enum` sans cas (non instanciables) comme marqueurs : ils ne peuvent pas être instanciés à l'exécution :

```swift
enum File {}
enum Directory {}
```

Utiliser un `enum` sans cas garantit un surcoût nul à l'exécution : aucune valeur de ce type ne peut jamais exister.

## Extensions contraintes {#constrained-extensions}

Appliquez des opérations de manière sélective en fonction du type fantôme :

```swift
extension Path where FileType == Directory {
    init(directoryComponents: [String]) {
        self.init(components: directoryComponents)
    }

    func appending(directory component: String) -> Path<Directory> {
        Path<Directory>(components: components + [component])
    }

    func appending(file component: String) -> Path<File> {
        Path<File>(components: components + [component])
    }
}
```

L'initialiseur se trouve dans l'extension contrainte à `Directory`, donc `Path(directoryComponents:)` renvoie toujours `Path<Directory>`.

## Application à la compilation {#compile-time-enforcement}

```swift
let dir = Path<Directory>(directoryComponents: ["Users", "chris"])
let docs = dir.appending(directory: "Documents")  // Path<Directory>
let file = docs.appending(file: "readme.md")       // Path<File>

// Compile error: Path<File> has no appending methods
// file.appending(file: "other.txt")  // won't compile
```

La machine à états est imposée par le système de types :
- `Path<Directory>` -> peut ajouter un répertoire ou un fichier
- `Path<File>` -> état terminal, aucun ajout supplémentaire possible

## Applications pratiques {#practical-applications}

### Sécurité des devises {#currency-safety}

```swift
enum USD {}
enum EUR {}

struct Money<Currency> {
    let amount: Decimal
}

func convert(_ money: Money<USD>) -> Money<EUR> {
    Money<EUR>(amount: money.amount * 0.92)
}

let dollars = Money<USD>(amount: 100)
let euros = convert(dollars)
// convert(euros) -> compile error: Money<EUR> != Money<USD>
```

### Entrées validées et non validées {#validated-vs-unvalidated-input}

```swift
enum Validated {}
enum Unvalidated {}

struct Email<State> {
    let address: String
}

func validate(_ email: Email<Unvalidated>) -> Email<Validated>? {
    guard email.address.contains("@") else { return nil }
    return Email<Validated>(address: email.address)
}

func send(to email: Email<Validated>) {
    // Only accepts validated emails
}
```

### Ancres de mise en page UIKit {#uikit-layout-anchors}

Apple utilise des types fantômes dans Auto Layout : `NSLayoutAnchor<AnchorType>` empêche de contraindre une ancre horizontale à une ancre verticale :

```swift
// Works: both horizontal
view.leadingAnchor.constraint(equalTo: other.trailingAnchor)

// Compile error: NSLayoutXAxisAnchor vs NSLayoutYAxisAnchor
// view.leadingAnchor.constraint(equalTo: other.topAnchor)
```

## Plusieurs paramètres fantômes {#multiple-phantom-parameters}

Étendez le concept à plusieurs dimensions, par exemple chemins absolus et relatifs :

```swift
enum Absolute {}
enum Relative {}

struct FilePath<Location, Kind> {
    private var components: [String]
}
```

Désormais, `FilePath<Absolute, Directory>` et `FilePath<Relative, File>` sont des types distincts. Vous pouvez interdire d'ajouter un préfixe à un chemin absolu ou de résoudre un chemin relatif sans base.

## Quand les utiliser {#when-to-use}

- **Machines à états** avec un nombre restreint d'états et de transitions
- **Types d'unités** (devises, mesures) où le mélange constitue un bogue
- **Étapes de workflow** (brouillon -> validé -> publié)
- **Contraintes de domaine** qui doivent être impossibles à violer

## Quand ne pas les utiliser {#when-not-to-use}

- Nombreux états (>5) : l'explosion combinatoire des `enum` rend l'API difficile à manier
- États connus uniquement à l'exécution : les types fantômes n'existent qu'à la compilation
- Simples wrappers validés pour lesquels une `struct` avec validation suffit

## Pièges à éviter {#gotchas}

- **Pas de réflexion à l'exécution :** vous ne pouvez pas inspecter `FileType` à l'exécution, car aucune valeur de ce type n'existe. Si vous avez besoin d'un branchement à l'exécution, utilisez plutôt un `enum` classique.
- **Messages d'erreur peu clairs :** lorsqu'une contrainte de type fantôme n'est pas respectée, les messages d'erreur de Swift peuvent être obscurs (par exemple « ambiguous reference to member »). Donnez des noms distincts aux méthodes pour obtenir des diagnostics plus clairs.
- **Précision de CGFloat en 32 bits :** lorsque vous utilisez des types fantômes dans des calculs numériques, `CGFloat.greatestFiniteMagnitude` perd en précision avec les exposants élevés. Utilisez une valeur sentinelle plus petite (par exemple `1e15`) pour éviter des comparaisons d'égalité incorrectes.

## Voir aussi {#see-also}

- [[swift-generics]]
- [[swift-enums-and-optionals]]
- [[swift-structs-and-classes]]
