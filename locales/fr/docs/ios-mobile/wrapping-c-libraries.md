---
title: "Encapsuler des bibliothèques C en Swift"
description: "Interfacer des fonctions C avec Swift en garantissant la sûreté des types, la gestion automatique de la mémoire via deinit, et la gestion des erreurs"
level: 3
source_sha256: fbe3d709d2e9795b3452adc121d8ab1c2dd00851d2a025d808bd955f7ac09788
translation: machine
translated_at: '2026-10-24'
---
# Encapsuler des bibliothèques C en Swift {#wrapping-c-libraries-in-swift}

Swift peut appeler directement des fonctions C via des en-têtes de pontage (bridging headers). Encapsuler des bibliothèques C (libgit2, libpq, SQLite, etc.) dans les idiomes Swift apporte la sûreté des types, la gestion automatique de la mémoire via `deinit`, et une gestion des erreurs plus claire.

## Configuration de l'en-tête de pontage {#bridging-header-setup}

Créez un en-tête de pontage et configurez-le dans les réglages de build :

```c
// ProjectName-Bridging-Header.h
#include "../libgit2/include/git2.h"
```

Dans Build Settings, définissez **Objective-C Bridging Header** avec le chemin de l'en-tête. Toutes les fonctions C deviennent alors globalement accessibles en Swift.

## Types de pointeurs C en Swift {#c-pointer-types-in-swift}

Les pointeurs C correspondent à des types Swift :

| Type C | Type Swift | Remarques |
|--------|-----------|-----------|
| `const char *` | `UnsafePointer<Int8>` | Swift convertit automatiquement `String` |
| `void *` | `OpaquePointer` | Pointeurs vers des structures opaques |
| `git_error *` | `UnsafePointer<git_error>` | Pointeurs vers des structures connues |
| `T **` (paramètre de sortie) | `UnsafeMutablePointer<OpaquePointer?>` | À passer sous la forme `&var` |

**Conversions implicites :** Swift convertit automatiquement un `String` en `UnsafePointer<Int8>` (chaîne C) au moment de l'appel. Aucune conversion manuelle n'est nécessaire.

## Schéma d'appel de base {#basic-call-pattern}

La plupart des bibliothèques C suivent ce schéma : appeler la fonction -> vérifier le code d'erreur -> utiliser le résultat -> libérer le résultat.

```swift
// C: int git_repository_open(git_repository **out, const char *path)
var pointer: OpaquePointer? = nil
let result = git_repository_open(&pointer, "/path/to/repo")
guard result == 0 else {
    fatalError("Failed to open repository")
}
// use pointer...
git_repository_free(pointer)
```

La syntaxe `&pointer` crée un `UnsafeMutablePointer` vers la variable, ce qui permet à C d'y écrire.

## Wrapper de gestion des erreurs {#error-handling-wrapper}

Regroupez le motif répétitif de vérification des codes d'erreur dans une fonction qui lève des exceptions :

```swift
struct GitError: Error {
    let message: String
}

func gitCall(_ body: () -> Int32) throws {
    let result = body()
    guard result == 0 else {
        let error = git_error_last()
        let message = error?.pointee.message
            .flatMap { String(cString: $0) } ?? "Unknown git error"
        throw GitError(message: message)
    }
}

// Usage
try gitCall { git_repository_open(&pointer, path) }
```

`pointee` accède à la valeur pointée par un `UnsafePointer`. Il n'est disponible que pour les pointeurs non opaques, lorsque Swift connaît la disposition de la structure.

## Wrapper de classe pour la gestion de la mémoire {#class-wrapper-for-memory-management}

Liez la durée de vie de la ressource C à une instance de classe Swift via `deinit` :

```swift
final class Repository {
    let pointer: OpaquePointer

    init(open path: String) throws {
        var ptr: OpaquePointer? = nil
        try gitCall { git_repository_open(&ptr, path) }
        self.pointer = ptr!
    }

    deinit {
        git_repository_free(pointer)
    }
}
```

La gestion de la mémoire est désormais automatique : lorsque l'instance `Repository` est désallouée, la ressource C est libérée. Aucun `defer` manuel n'est nécessaire aux sites d'appel.

```swift
final class Reference {
    let pointer: OpaquePointer

    init(repository: Repository, dwim shorthand: String) throws {
        var ptr: OpaquePointer? = nil
        try gitCall {
            git_reference_dwim(&ptr, repository.pointer, shorthand)
        }
        self.pointer = ptr!
    }

    var name: String {
        String(cString: git_reference_name(pointer))
    }

    deinit {
        git_reference_free(pointer)
    }
}
```

**L'utilisation devient un Swift idiomatique :**

```swift
do {
    let repo = try Repository(open: "/path/to/repo")
    let ref = try Reference(repository: repo, dwim: "master")
    print(ref.name)  // refs/heads/master
} catch {
    print(error)
}
```

## Exemple de base de données : libpq (PostgreSQL) {#database-example-libpq-postgresql}

Le même motif s'applique aux connexions à une base de données :

```swift
final class PGConnection {
    private let conn: OpaquePointer

    init(connectionInfo: String) throws {
        conn = PQconnectdb(connectionInfo)
        guard PQstatus(conn) == CONNECTION_OK else {
            let msg = String(cString: PQerrorMessage(conn))
            PQfinish(conn)
            throw PostgresError(message: msg)
        }
    }

    @discardableResult
    func query(_ sql: String) throws -> PGResult? {
        let resultPtr = PQexec(conn, sql)!
        let status = PQresultStatus(resultPtr)

        if status == PGRES_TUPLES_OK {
            return PGResult(pointer: resultPtr)
        } else if status == PGRES_COMMAND_OK {
            PQclear(resultPtr)
            return nil
        } else {
            let msg = String(cString: PQresultErrorMessage(resultPtr))
            PQclear(resultPtr)
            throw PostgresError(message: msg)
        }
    }

    deinit {
        PQfinish(conn)
    }
}
```

Wrapper de résultat avec accès par subscript :

```swift
final class PGResult {
    private let result: OpaquePointer

    init(pointer: OpaquePointer) { self.result = pointer }

    var rowCount: Int32 { PQntuples(result) }
    var columnCount: Int32 { PQnfields(result) }

    subscript(row row: Int32, column column: Int32) -> String {
        String(cString: PQgetvalue(result, row, column))
    }

    deinit { PQclear(result) }
}
```

## Lier les bibliothèques C {#linking-c-libraries}

Dans le projet Xcode :

1. Ajoutez le projet Xcode de la bibliothèque C comme sous-projet
2. Dans **Build Phases** -> **Target Dependencies**, ajoutez la cible de la bibliothèque
3. Dans **Link Binary with Libraries**, ajoutez la bibliothèque statique `.a`
4. Ajoutez les dépendances système nécessaires (libz, libcurl, libiconv selon le besoin)

Pour les bibliothèques statiques, définissez `BUILD_SHARED_LIBS=OFF` lors de la compilation avec CMake :

```bash
mkdir build && cd build
cmake -G Xcode -DBUILD_SHARED_LIBS=OFF ..
```

## Pièges à éviter {#gotchas}

- **Initialisation de la bibliothèque :** De nombreuses bibliothèques C exigent un appel d'initialisation global (par exemple `git_libgit2_init()`) avant toute autre fonction. L'oubli de cet appel provoque des plantages obscurs, et non des messages d'erreur explicites. Vérifiez systématiquement la documentation de la bibliothèque pour les initialisations requises.
- **App Sandbox :** Les applications macOS dotées de l'App Sandbox ne peuvent pas accéder à des chemins arbitraires du système de fichiers. Si votre bibliothèque C ouvre des fichiers, désactivez le sandboxing pendant le développement ou configurez correctement les entitlements. L'erreur ressemble à une erreur de la bibliothèque, et non à une erreur de sandbox.
- **Optionnels implicitement déballés :** Les fonctions C qui renvoient des pointeurs sont importées sous la forme `OpaquePointer!` (optionnel implicitement déballé). Vérifiez toujours dans la documentation si `nil` est une valeur de retour valide : un déballage forcé sans vérification provoque des plantages silencieux.
- **Durée de vie des chaînes :** Lorsqu'un `String` Swift est passé à une fonction C sous la forme `UnsafePointer<Int8>`, la chaîne C n'est valide que pendant la durée de l'appel. Ne stockez pas ce pointeur pour un usage ultérieur.

## Voir aussi {#see-also}

- [[swift-fundamentals]]
- [[swift-structs-and-classes]]
