---
title: "SwiftUI-Layout-Tests"
description: "Property-based Fuzzing zur Verifikation eigener Layout-Engines gegen das native SwiftUI-Rendering von Apple"
level: 3
source_sha256: a9fb215d86dc21a246310e7a348dcdcaf2dc4ca7fa37de3c61e60d7e13209b86
translation: machine
translated_at: '2026-10-24'
---
# SwiftUI-Layout-Tests {#swiftui-layout-testing}

Automatisierte Verifikation eigener SwiftUI-Layout-Implementierungen durch Vergleich mit dem nativen Rendering von Apple, mittels Property-based Testing (Fuzzing).

## Vorgehen {#approach}

Zufällige View-Konfigurationen erzeugen, mit der eigenen Layout-Engine und mit SwiftUI rendern und anschließend die Ergebnisse vergleichen:

1. Ein Enum mit den möglichen Konfigurationen der Child-Views definieren
2. Zufällig View-Hierarchien generieren
3. Child-Views mit der eigenen Implementierung messen
4. Child-Views mit SwiftUI messen (über `GeometryReader` + Preferences)
5. Gleichheit prüfen

## Zufällige View-Konfigurationen erzeugen {#generating-random-view-configurations}

```swift
enum Frame: CustomStringConvertible {
    case flexible                     // no frame modifier
    case fixed(CGFloat)               // .frame(width: N)
    case min(CGFloat)                 // .frame(minWidth: N)
    case max(CGFloat)                 // .frame(maxWidth: N)
    case minMax(min: CGFloat, max: CGFloat)  // .frame(minWidth: N, maxWidth: M)

    static func random() -> Frame {
        let randomWidth = { CGFloat(Int.random(in: 0...100)) }
        switch Int.random(in: 0..<5) {
        case 0: return .flexible
        case 1: return .fixed(randomWidth())
        case 2: return .min(randomWidth())
        case 3: return .max(randomWidth())
        default:
            let maxW = randomWidth()
            let minW = CGFloat.random(in: 0...maxW).rounded()
            return .minMax(min: minW, max: maxW)
        }
    }

    var view: AnyView {
        let r = Rectangle()
        switch self {
        case .flexible: return AnyView(r)
        case .fixed(let w): return AnyView(r.frame(width: w))
        case .min(let w): return AnyView(r.frame(minWidth: w))
        case .max(let w): return AnyView(r.frame(maxWidth: w))
        case .minMax(let mn, let mx):
            return AnyView(r.frame(minWidth: mn, maxWidth: mx))
        }
    }
}
```

**Wichtig:** Für `.minMax` zuerst `max` erzeugen und danach `min` in `0...max`. Werden beide unabhängig voneinander erzeugt, entstehen ungültige Frames mit `min > max`.

## SwiftUI-Views messen {#measuring-swiftui-views}

`PreferenceKey` verwenden, um die Größen der Child-Views nach oben weiterzureichen:

```swift
struct WidthKey: PreferenceKey {
    static var defaultValue: [CGFloat] = []
    static func reduce(value: inout [CGFloat], nextValue: () -> [CGFloat]) {
        value.append(contentsOf: nextValue())
    }
}

// Wrap each child with a GeometryReader overlay
ForEach(views.indices, id: \.self) { i in
    views[i]
        .overlay(GeometryReader { proxy in
            Color.clear.preference(key: WidthKey.self, value: [proxy.size.width])
        })
}
.onPreferenceChange(WidthKey.self) { widths in
    swiftUISizes = widths
}
```

Das Rendering mit `UIHostingController` erzwingen:

```swift
let host = UIHostingController(rootView: swiftUIStack)
host.view.frame = CGRect(x: 0, y: 0, width: proposedWidth, height: 100)
_ = host.view.snapshotView(afterScreenUpdates: true)
```

## Testschleife {#test-loop}

```swift
func testHStackLayout() {
    for _ in 0..<1000 {
        let frames = (1...Int.random(in: 1...10)).map { _ in Frame.random() }
        let proposedWidth = CGFloat.random(in: 0...500).rounded()

        // Custom implementation
        let customStack = HStack_(children: frames.map(\.view))
        customStack.layout(proposedSize: CGSize(width: proposedWidth, height: 100))
        let customWidths = customStack.sizes.map(\.width)

        // SwiftUI reference
        let swiftUIWidths = measureSwiftUI(frames: frames, proposedWidth: proposedWidth)

        // Compare
        XCTAssertEqual(customWidths, swiftUIWidths,
            "Mismatch for frames: \(frames), proposed: \(proposedWidth)")
    }
}
```

## Plattformunterschiede {#platform-differences}

Tests auf iOS ausführen, nicht auf macOS. Bekannte Probleme unter macOS:

- HStack mit zentriertem Inhalt und übergroßen Child-Views rendert die Subviews zu groß und nicht zentriert
- GeometryReader zentriert den Inhalt unter macOS, unter iOS dagegen oben-links ausgerichtet

Sowohl ein macOS- als auch ein iOS-Testtarget einrichten, die Korrektheit aber gegen das iOS-Verhalten prüfen.

## Stolperfallen {#gotchas}

- **Präzisionsverlust bei `CGFloat.greatestFiniteMagnitude`:** Beim Vergleichen von Flexibilitätsbereichen verliert `greatestFiniteMagnitude` (10^308) die Genauigkeit in den Nachkommastellen. Zwei Views mit unterschiedlichen Mindestbreiten, aber derselben Maximalbreite `greatestFiniteMagnitude`, berechnen daher identische Flexibilitätswerte. Stattdessen einen großen, aber präzisen Platzhalter wie `1e15` verwenden.
- **Rundungsfehler:** Eigenes Layout und SwiftUI können auf Pixel unterschiedlich runden. Für Vergleiche von Fließkommazahlen den Parameter `accuracy` in `XCTAssertEqual` verwenden oder beide Seiten vor dem Vergleich auf dieselbe Genauigkeit runden.
- **Logging bei Fehlschlägen:** `frames`-Array und `proposedWidth` in die Assertion-Meldung aufnehmen. Ohne diese Angaben liefert ein Fuzzing-Fehler zwar Größen, aber keine Möglichkeit, die auslösende Konfiguration zu reproduzieren.

## Siehe auch {#see-also}

- [[swiftui-views-and-modifiers]]
- [[swiftui-state-and-data-flow]]
- [[swift-phantom-types]]
