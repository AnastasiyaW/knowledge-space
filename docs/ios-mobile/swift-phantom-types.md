---
title: "Swift Phantom Types"
description: "Compile-time-only type parameters for enforcing state machines, unit safety, and domain constraints"
---

# Swift Phantom Types

Phantom types use generic type parameters that exist only at compile time - they appear in the type signature but are never stored as values. This enforces state machine transitions, unit safety, and domain constraints at compile time.

## Core Concept

A phantom type parameter is one that does not appear in any stored property or constructor argument:

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

`FileType` has no corresponding stored property - it exists purely as a compile-time marker.

## Marker Types

Define uninhabited enums (no cases) as markers - they cannot be instantiated at runtime:

```swift
enum File {}
enum Directory {}
```

Using `enum` with no cases guarantees zero runtime overhead - no value of this type can ever exist.

## Constrained Extensions

Apply operations selectively based on the phantom type:

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

The initializer lives in the `Directory`-constrained extension, so `Path(directoryComponents:)` always returns `Path<Directory>`.

## Compile-Time Enforcement

```swift
let dir = Path<Directory>(directoryComponents: ["Users", "chris"])
let docs = dir.appending(directory: "Documents")  // Path<Directory>
let file = docs.appending(file: "readme.md")       // Path<File>

// Compile error: Path<File> has no appending methods
// file.appending(file: "other.txt")  // won't compile
```

The state machine is enforced by the type system:
- `Path<Directory>` -> can append directory or file
- `Path<File>` -> terminal state, no further appending

## Practical Applications

### Currency Safety

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

### Validated vs Unvalidated Input

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

### UIKit Layout Anchors

Apple uses phantom types in Auto Layout - `NSLayoutAnchor<AnchorType>` prevents constraining a horizontal anchor to a vertical one:

```swift
// Works: both horizontal
view.leadingAnchor.constraint(equalTo: other.trailingAnchor)

// Compile error: NSLayoutXAxisAnchor vs NSLayoutYAxisAnchor
// view.leadingAnchor.constraint(equalTo: other.topAnchor)
```

## Multiple Phantom Parameters

Extend to multiple dimensions - e.g., absolute vs relative paths:

```swift
enum Absolute {}
enum Relative {}

struct FilePath<Location, Kind> {
    private var components: [String]
}
```

Now `FilePath<Absolute, Directory>` and `FilePath<Relative, File>` are distinct types. You can prevent prepending to absolute paths or resolving relative paths without a base.

## When to Use

- **State machines** with a small number of states and transitions
- **Unit types** (currency, measurements) where mixing is a bug
- **Workflow stages** (draft -> validated -> published)
- **Domain constraints** that should be impossible to violate

## When NOT to Use

- Many states (>5) - enum explosion makes the API unwieldy
- States known only at runtime - phantom types are compile-time only
- Simple validated wrappers where a `struct` with validation suffices

## Gotchas

- **No runtime reflection:** You cannot inspect `FileType` at runtime since no value of that type exists. If you need runtime branching, use a regular enum instead.
- **Error messages are poor:** When a phantom-type constraint fails, Swift's error messages can be cryptic (e.g., "ambiguous reference to member"). Give methods distinct names to get clearer diagnostics.
- **32-bit CGFloat precision:** When using phantom types with numeric computations, `CGFloat.greatestFiniteMagnitude` loses precision on large exponents. Use a smaller sentinel value (e.g., `1e15`) to avoid incorrect equality comparisons.

## See Also

- [[swift-generics]]
- [[swift-enums-and-optionals]]
- [[swift-structs-and-classes]]
