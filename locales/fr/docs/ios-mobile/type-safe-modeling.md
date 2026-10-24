---
title: "Modélisation de domaine type-safe en Swift"
description: "Utiliser les enums, les structs et les generics pour éliminer les états impossibles et rendre les API auto-documentées"
level: 3
source_sha256: 941317ef4a5fd5a070f382a95d8ba495ee52e250979f3f16dd387d1fdbed7112
translation: machine
translated_at: '2026-10-24'
---
# Modélisation de domaine type-safe en Swift {#type-safe-domain-modeling-in-swift}

Bien choisir la représentation des types permet d'éliminer les états impossibles, de réduire les bugs et de rendre les API auto-documentées. Le système de types de Swift (enums, structs, optionnels, generics) permet une modélisation précise, au-delà de ce qu'expriment les langages qui ne disposent que de classes.

## Le problème des optionnels {#the-problem-with-optionals}

Plusieurs paramètres optionnels créent une explosion des états possibles, dont la plupart sont invalides :

```swift
// URLSession completion handler: 3 optionals = 8 possible combinations
(Data?, URLResponse?, Error?) -> Void
```

La plupart des combinaisons n'ont aucun sens : des données sans réponse, une erreur accompagnée de données, tout à `nil`. Le système de types n'empêche rien de tout cela.

**Une meilleure représentation avec un enum :**

```swift
enum NetworkResult {
    case success(data: Data, response: URLResponse)
    case failure(Error)
}
```

Seuls 2 états valides existent désormais. Le compilateur impose un traitement exhaustif des cas.

## Quand les enums sont préférables aux structs {#when-enums-beat-structs}

Utilisez un enum lorsque :
- les états sont **mutuellement exclusifs** (connecté OU déconnecté, jamais les deux)
- les différents états portent des **données associées différentes**
- vous voulez que le compilateur impose un **traitement exhaustif**

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

## Quand une struct avec optionnels est préférable aux enums {#when-structs-optionals-beat-enums}

Si plusieurs cas d'un enum partagent la même valeur associée, une struct avec un optionnel peut être plus simple :

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

Accéder à `user` ne nécessite aucun `switch` : il suffit d'un chaînage optionnel sur la session elle-même.

## Conception du type de retour d'une fonction {#function-return-type-design}

Même une fonction simple comme « lire des fichiers » admet de nombreuses signatures de types valides :

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

Choisissez en fonction de ce dont l'appelant a besoin :
- **Récupération d'erreur par fichier** -> option 3 ou 5
- **Tout ou rien** -> option 4
- **Cas simple** -> option 1

## Compromis sur les entiers non signés {#unsigned-integer-trade-off}

La bibliothèque standard de Swift utilise `Int` (et non `UInt`) pour `Array.count` et les indices de subscript, alors que les valeurs négatives n'ont aucun sens. Il s'agit d'un compromis délibéré :

- **Précision :** `UInt` élimine les valeurs négatives
- **Ergonomie :** toute opération arithmétique avec `Int` nécessite une conversion

Apple a privilégié l'ergonomie. Leçon à retenir : **la précision maximale du type n'est pas toujours la meilleure conception.**

## Tests basés sur les propriétés pour les invariants de types {#property-based-testing-for-type-invariants}

Lorsque les types ne peuvent pas imposer pleinement certaines contraintes (par exemple « la longueur du tableau de sortie est égale à celle du tableau d'entrée »), utilisez des tests basés sur les propriétés :

```swift
func testReadFilesPreservesLength() {
    for _ in 0..<1000 {
        let names = (0..<Int.random(in: 1...20)).map { "file\($0).txt" }
        let results = readFiles(names)
        XCTAssertEqual(results.count, names.count)
    }
}
```

## Liste de contrôle pour la conception des types {#type-design-checklist}

1. **Listez tous les états possibles** dans lesquels vos données peuvent se trouver
2. **Identifiez les combinaisons invalides** qui ne devraient jamais se produire
3. **Choisissez des types qui éliminent les états invalides :**
   - enum pour les états mutuellement exclusifs
   - propriétés non optionnelles pour les données toujours présentes
   - types fantômes (phantom types) pour les machines à états vérifiées à la compilation
4. **Vérifiez :** peut-on construire une valeur de ce type qui représente quelque chose de dénué de sens ? Si oui, resserrez le type.

## Pièges à éviter {#gotchas}

- **Types trop précis :** imposer chaque contrainte au niveau du type peut rendre les API pénibles à utiliser. `UInt` pour les indices de tableaux est techniquement plus correct, mais impose une charge de conversion partout. Trouvez le juste équilibre entre précision et ergonomie.
- **Explosion du nombre de cas d'un enum :** si vous avez 4 champs optionnels dont les 16 combinaisons sont valides, un enum à 16 cas est moins bon que 4 optionnels. Les enums brillent lorsque la plupart des combinaisons sont **invalides**.
- **Difficulté de migration :** passer d'une struct à un enum (ou l'inverse) constitue un changement cassant pour l'API. Réfléchissez attentivement au choix de votre type avant de publier une API publique.

## Voir aussi {#see-also}

- [[swift-enums-and-optionals]]
- [[swift-structs-and-classes]]
- [[swift-phantom-types]]
- [[swift-generics]]
