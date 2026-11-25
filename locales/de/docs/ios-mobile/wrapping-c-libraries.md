---
title: "C-Bibliotheken in Swift kapseln"
description: "C-Funktionen mit Typsicherheit in Swift einbinden, automatische Speicherverwaltung über deinit und Fehlerbehandlung"
level: 3
source_sha256: fbe3d709d2e9795b3452adc121d8ab1c2dd00851d2a025d808bd955f7ac09788
translation: machine
translated_at: '2026-10-24'
---
# C-Bibliotheken in Swift kapseln {#wrapping-c-libraries-in-swift}

Swift kann C-Funktionen über Bridging Headers direkt aufrufen. Wenn man C-Bibliotheken (libgit2, libpq, SQLite usw.) in Swift-Idiomen kapselt, erhält man Typsicherheit, automatische Speicherverwaltung über `deinit` und eine übersichtlichere Fehlerbehandlung.

## Einrichtung des Bridging Headers {#bridging-header-setup}

Einen Bridging Header anlegen und in den Build-Einstellungen konfigurieren:

```c
// ProjectName-Bridging-Header.h
#include "../libgit2/include/git2.h"
```

In den Build Settings die Option **Objective-C Bridging Header** auf den Pfad des Headers setzen. Danach sind alle C-Funktionen in Swift global verfügbar.

## C-Zeigertypen in Swift {#c-pointer-types-in-swift}

C-Zeiger werden auf Swift-Typen abgebildet:

| C-Typ | Swift-Typ | Anmerkungen |
|--------|-----------|-------------|
| `const char *` | `UnsafePointer<Int8>` | Swift konvertiert `String` automatisch |
| `void *` | `OpaquePointer` | Undurchsichtige Struct-Zeiger |
| `git_error *` | `UnsafePointer<git_error>` | Bekannte Struct-Zeiger |
| `T **` (Out-Parameter) | `UnsafeMutablePointer<OpaquePointer?>` | Als `&var` übergeben |

**Implizite Konvertierungen:** Swift wandelt `String` beim Aufruf automatisch in `UnsafePointer<Int8>` (C-String) um. Eine manuelle Konvertierung ist nicht nötig.

## Grundlegendes Aufrufmuster {#basic-call-pattern}

Die meisten C-Bibliotheken folgen diesem Ablauf: Funktion aufrufen -> Fehlercode prüfen -> Ergebnis verwenden -> Ergebnis freigeben.

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

Die Syntax `&pointer` erzeugt einen `UnsafeMutablePointer` auf die Variable, sodass C in sie schreiben kann.

## Wrapper für die Fehlerbehandlung {#error-handling-wrapper}

Das wiederkehrende Muster der Fehlercodes wird in eine werfende Funktion gekapselt:

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

`pointee` greift auf den Wert hinter einem `UnsafePointer` zu. Das funktioniert nur bei nicht undurchsichtigen Zeigern, bei denen Swift das Struct-Layout kennt.

## Klassen-Wrapper für die Speicherverwaltung {#class-wrapper-for-memory-management}

Die Lebensdauer der C-Ressource wird über `deinit` an eine Swift-Klasseninstanz gebunden:

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

Die Speicherverwaltung läuft nun automatisch: Wird die `Repository`-Instanz freigegeben, wird auch die C-Ressource freigegeben. An den Aufrufstellen ist kein manuelles `defer` nötig.

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

**Die Verwendung wird idiomatisches Swift:**

```swift
do {
    let repo = try Repository(open: "/path/to/repo")
    let ref = try Reference(repository: repo, dwim: "master")
    print(ref.name)  // refs/heads/master
} catch {
    print(error)
}
```

## Datenbankbeispiel: libpq (PostgreSQL) {#database-example-libpq-postgresql}

Dasselbe Muster gilt für Datenbankverbindungen:

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

Result-Wrapper mit Subscript-Zugriff:

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

## Einbinden von C-Bibliotheken {#linking-c-libraries}

Im Xcode-Projekt:

1. Das Xcode-Projekt der C-Bibliothek als Unterprojekt hinzufügen
2. Unter **Build Phases** -> **Target Dependencies** das Bibliotheks-Target hinzufügen
3. Unter **Link Binary with Libraries** die statische Bibliothek `.a` hinzufügen
4. Systemabhängigkeiten ergänzen (libz, libcurl, libiconv je nach Bedarf)

Bei statischen Bibliotheken `BUILD_SHARED_LIBS=OFF` setzen, wenn man mit CMake baut:

```bash
mkdir build && cd build
cmake -G Xcode -DBUILD_SHARED_LIBS=OFF ..
```

## Stolperfallen {#gotchas}

- **Initialisierung der Bibliothek:** Viele C-Bibliotheken verlangen einen globalen Init-Aufruf (z. B. `git_libgit2_init()`), bevor eine andere Funktion verwendet wird. Fehlt dieser Aufruf, führt das zu kryptischen Abstürzen statt zu verständlichen Fehlermeldungen. Die Dokumentation der Bibliothek sollte immer auf erforderliche Initialisierungen geprüft werden.
- **App Sandbox:** macOS-Apps mit aktivierter App Sandbox können nicht auf beliebige Dateisystempfade zugreifen. Öffnet die C-Bibliothek Dateien, sollte die Sandbox während der Entwicklung deaktiviert oder die Entitlements korrekt konfiguriert werden. Der Fehler sieht nach einem Bibliotheksfehler aus, nicht nach einem Sandbox-Fehler.
- **Implizit ausgepackte Optionals:** C-Funktionen, die Zeiger zurückgeben, werden als `OpaquePointer!` (implizit ausgepackt) importiert. Man sollte immer in der Dokumentation prüfen, ob `nil` ein gültiger Rückgabewert ist. Ein Force-Unwrap ohne diese Prüfung führt zu stillen Abstürzen.
- **Lebensdauer von Strings:** Wird ein Swift-`String` als `UnsafePointer<Int8>` an eine C-Funktion übergeben, ist der C-String nur für die Dauer des Aufrufs gültig. Der Zeiger darf nicht für eine spätere Verwendung gespeichert werden.

## Siehe auch {#see-also}

- [[swift-fundamentals]]
- [[swift-structs-and-classes]]
