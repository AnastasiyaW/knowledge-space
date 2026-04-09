---
title: "Wrapping C Libraries in Swift"
description: "Bridging C functions into Swift with type safety, automatic memory management via deinit, and error handling"
---

# Wrapping C Libraries in Swift

Swift can call C functions directly through bridging headers. Wrapping C libraries (libgit2, libpq, SQLite, etc.) in Swift idioms provides type safety, automatic memory management via `deinit`, and cleaner error handling.

## Bridging Header Setup

Create a bridging header and configure it in build settings:

```c
// ProjectName-Bridging-Header.h
#include "../libgit2/include/git2.h"
```

In Build Settings, set **Objective-C Bridging Header** to the header path. All C functions become globally available in Swift.

## C Pointer Types in Swift

C pointers map to Swift types:

| C Type | Swift Type | Notes |
|--------|-----------|-------|
| `const char *` | `UnsafePointer<Int8>` | Swift auto-bridges `String` |
| `void *` | `OpaquePointer` | Opaque struct pointers |
| `git_error *` | `UnsafePointer<git_error>` | Known struct pointers |
| `T **` (out param) | `UnsafeMutablePointer<OpaquePointer?>` | Pass as `&var` |

**Implicit conversions:** Swift automatically converts `String` to `UnsafePointer<Int8>` (C string) at call sites. No manual conversion needed.

## Basic Call Pattern

Most C libraries follow: call function -> check error code -> use result -> free result.

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

The `&pointer` syntax creates an `UnsafeMutablePointer` to the variable, letting C write into it.

## Error Handling Wrapper

Wrap the repeated error-code pattern into a throwing function:

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

`pointee` accesses the value behind an `UnsafePointer` - available only for non-opaque pointers where Swift knows the struct layout.

## Class Wrapper for Memory Management

Tie the C resource lifetime to a Swift class instance via `deinit`:

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

Now memory management is automatic - when the `Repository` instance is deallocated, the C resource is freed. No manual `defer` needed at call sites.

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

**Usage becomes idiomatic Swift:**

```swift
do {
    let repo = try Repository(open: "/path/to/repo")
    let ref = try Reference(repository: repo, dwim: "master")
    print(ref.name)  // refs/heads/master
} catch {
    print(error)
}
```

## Database Example: libpq (PostgreSQL)

Same pattern applies to database connections:

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

Result wrapper with subscript access:

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

## Linking C Libraries

In the Xcode project:

1. Add the C library Xcode project as a sub-project
2. In **Build Phases** -> **Target Dependencies**, add the library target
3. In **Link Binary with Libraries**, add the `.a` static library
4. Add system dependencies (libz, libcurl, libiconv as needed)

For static libraries, set `BUILD_SHARED_LIBS=OFF` when building with CMake:

```bash
mkdir build && cd build
cmake -G Xcode -DBUILD_SHARED_LIBS=OFF ..
```

## Gotchas

- **Library initialization:** Many C libraries require a global init call (e.g., `git_libgit2_init()`) before any other function. Missing this causes cryptic crashes, not clear error messages. Always check the library's documentation for required initialization.
- **App Sandbox:** macOS apps with App Sandbox enabled cannot access arbitrary file system paths. If your C library opens files, disable sandboxing during development or configure entitlements properly. The error looks like a library error, not a sandbox error.
- **Implicitly unwrapped optionals:** C functions returning pointers are imported as `OpaquePointer!` (implicitly unwrapped). Always check the documentation for whether `nil` is a valid return value - force-unwrapping without checking causes silent crashes.
- **String lifetime:** When passing Swift `String` to a C function as `UnsafePointer<Int8>`, the C string is only valid for the duration of the call. Do not store the pointer for later use.

## See Also

- [[swift-fundamentals]]
- [[swift-structs-and-classes]]
