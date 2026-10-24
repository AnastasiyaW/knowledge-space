---
title: "Swift Phantom Types"
description: "Nur zur Kompilierzeit existierende Typparameter zur Durchsetzung von Zustandsautomaten, Einheitensicherheit und Domänenbeschränkungen"
level: 3
source_sha256: 3af7aca12554057d8b2281168e46b58cda931598829ec36843e5c1366febd6ad
translation: machine
translated_at: '2026-10-24'
---
# Swift Phantom Types {#swift-phantom-types}

Phantom Types verwenden generische Typparameter, die nur zur Kompilierzeit existieren. Sie erscheinen in der Typsignatur, werden aber nie als Werte gespeichert. Dadurch werden Übergänge von Zustandsautomaten, Einheitensicherheit und Domänenbeschränkungen bereits zur Kompilierzeit erzwungen.

## Kernkonzept {#core-concept}

Ein Phantom-Typparameter ist ein Parameter, der in keiner gespeicherten Eigenschaft und in keinem Konstruktorargument vorkommt:

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

`FileType` hat keine entsprechende gespeicherte Eigenschaft. Er existiert rein als Marker zur Kompilierzeit.

## Marker-Typen {#marker-types}

Definiere nicht instanziierbare Enums (ohne Fälle) als Marker. Sie können zur Laufzeit nicht instanziiert werden:

```swift
enum File {}
enum Directory {}
```

Ein `enum` ohne Fälle garantiert keinen Laufzeit-Overhead, denn ein Wert dieses Typs kann niemals existieren.

## Eingeschränkte Extensions {#constrained-extensions}

Wende Operationen selektiv anhand des Phantom-Typs an:

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

Der Initializer befindet sich in der auf `Directory` eingeschränkten Extension. Daher liefert `Path(directoryComponents:)` immer `Path<Directory>` zurück.

## Durchsetzung zur Kompilierzeit {#compile-time-enforcement}

```swift
let dir = Path<Directory>(directoryComponents: ["Users", "chris"])
let docs = dir.appending(directory: "Documents")  // Path<Directory>
let file = docs.appending(file: "readme.md")       // Path<File>

// Compile error: Path<File> has no appending methods
// file.appending(file: "other.txt")  // won't compile
```

Der Zustandsautomat wird vom Typsystem durchgesetzt:
- `Path<Directory>` -> kann ein Verzeichnis oder eine Datei anhängen
- `Path<File>` -> Endzustand, kein weiteres Anhängen möglich

## Praktische Anwendungen {#practical-applications}

### Währungssicherheit {#currency-safety}

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

### Validierte vs. unvalidierte Eingaben {#validated-vs-unvalidated-input}

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

### UIKit-Layout-Anker {#uikit-layout-anchors}

Apple verwendet Phantom Types in Auto Layout. `NSLayoutAnchor<AnchorType>` verhindert, dass ein horizontaler Anker mit einem vertikalen Anker verknüpft wird:

```swift
// Works: both horizontal
view.leadingAnchor.constraint(equalTo: other.trailingAnchor)

// Compile error: NSLayoutXAxisAnchor vs NSLayoutYAxisAnchor
// view.leadingAnchor.constraint(equalTo: other.topAnchor)
```

## Mehrere Phantom-Parameter {#multiple-phantom-parameters}

Erweitere das Konzept auf mehrere Dimensionen, z. B. absolute vs. relative Pfade:

```swift
enum Absolute {}
enum Relative {}

struct FilePath<Location, Kind> {
    private var components: [String]
}
```

Jetzt sind `FilePath<Absolute, Directory>` und `FilePath<Relative, File>` voneinander verschiedene Typen. Du kannst verhindern, dass an absolute Pfade etwas vorangestellt wird, bzw. dass relative Pfade ohne Basispfad aufgelöst werden.

## Wann einsetzen {#when-to-use}

- **Zustandsautomaten** mit wenigen Zuständen und Übergängen
- **Einheitentypen** (Währung, Maßeinheiten), bei denen Vermischung ein Fehler wäre
- **Workflow-Stufen** (Entwurf -> validiert -> veröffentlicht)
- **Domänenbeschränkungen**, die unter keinen Umständen verletzt werden dürfen

## Wann nicht einsetzen {#when-not-to-use}

- Viele Zustände (>5): Die Enum-Explosion macht die API unübersichtlich
- Zustände, die nur zur Laufzeit bekannt sind: Phantom Types existieren nur zur Kompilierzeit
- Einfache validierte Wrapper, für die ein `struct` mit Validierung genügt

## Fallstricke {#gotchas}

- **Keine Laufzeit-Reflexion:** `FileType` kann zur Laufzeit nicht untersucht werden, weil kein Wert dieses Typs existiert. Wenn du zur Laufzeit verzweigen musst, verwende stattdessen ein reguläres `enum`.
- **Fehlermeldungen sind unzureichend:** Schlägt eine Phantom-Typ-Beschränkung fehl, können Swifts Fehlermeldungen kryptisch ausfallen (z. B. „ambiguous reference to member“). Vergib eindeutige Methodennamen, um aussagekräftigere Diagnosen zu erhalten.
- **Präzision bei 32-Bit-CGFloat:** Bei numerischen Berechnungen mit Phantom Types verliert `CGFloat.greatestFiniteMagnitude` bei großen Exponenten an Genauigkeit. Verwende einen kleineren Sentinel-Wert (z. B. `1e15`), um fehlerhafte Gleichheitsvergleiche zu vermeiden.

## Siehe auch {#see-also}

- [[swift-generics]]
- [[swift-enums-and-optionals]]
- [[swift-structs-and-classes]]
