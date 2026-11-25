---
title: "SwiftUI-Views und Modifier"
category: concepts
tags: [ios-mobile, swiftui, views, modifiers, layout, text, image, button]
level: 3
source_sha256: f1f97ab71e205feb396860abad68185a3ca9588b9f61a85f55f951d46ba629f7
translation: machine
translated_at: '2026-10-24'
---
# SwiftUI-Views und Modifier {#swiftui-views-and-modifiers}

Jedes visuelle Element in SwiftUI ist eine View. Views sind Structs, die das `View`-Protokoll implementieren und deklarativ zusammengesetzt werden. Modifier werden an Views angehängt, um Erscheinungsbild und Verhalten zu ändern. Dieser Eintrag behandelt eingebaute Views, Layout-Container, die Verkettung von Modifiern und wiederverwendbare View-Muster.

## Wichtige Fakten {#key-facts}

- Jede eigene View ist ein `struct`, das `View` implementiert und eine verpflichtende berechnete Property `body` besitzt
- `some View` ist ein opaker Rückgabetyp – er verbirgt den genauen Typ, garantiert aber, dass dieser `View` konform ist
- Modifier werden per Punktsyntax verkettet; **die Reihenfolge ist wichtig** (padding vor background oder nach background)
- Layout-Container: `VStack` (vertikal), `HStack` (horizontal), `ZStack` (überlappend)
- `Spacer()` füllt in Stacks den verfügbaren Platz aus
- `GeometryReader` liefert die tatsächlichen Abmessungen des Containers für responsive Größen
- SF Symbols werden über `Image(systemName: "symbol.name")` eingebunden und reagieren auf den Modifier `.font()`

## Muster {#patterns}

### Grundstruktur einer View {#basic-view-structure}

```swift
struct ContentView: View {
    var body: some View {
        Text("Hello, world!")
    }
}
```

### Eingebaute View-Typen {#built-in-view-types}

| View | Verwendung |
|------|-------|
| `Text("string")` | Text anzeigen |
| `Image("name")` | Bild aus dem Asset-Katalog |
| `Image(systemName: "star")` | SF Symbol |
| `Button("label") { action }` | Antippbarer Button |
| `Circle()` | Kreisform |
| `RoundedRectangle(cornerRadius: 10)` | Abgerundetes Rechteck |
| `TextField("placeholder", text: $binding)` | Texteingabe |
| `Spacer()` | Flexibler Abstand |
| `Divider()` | Horizontale Linie |
| `ProgressView()` | Ladeanzeige |
| `EmptyView()` | Unsichtbarer Platzhalter |
| `Link("text", destination: URL)` | Link auf externe URL |

### Layout-Container {#layout-containers}

```swift
VStack { /* vertical stack */ }
HStack { /* horizontal stack */ }
ZStack { /* overlapping layers, last = top */ }

// With spacing and alignment
VStack(spacing: 20) { ... }
VStack(alignment: .leading) { ... }
HStack(alignment: .top) { ... }
ZStack(alignment: .bottomLeading) { ... }
```

### Verkettung von Modifiern (Reihenfolge ist wichtig) {#modifier-chaining-order-matters}

```swift
Text("Hello")
    .font(.largeTitle)
    .foregroundStyle(.white)
    .padding()
    .background(Color.blue)
    .clipShape(RoundedRectangle(cornerRadius: 15))
    .frame(width: 200, height: 50)
    .shadow(color: .black, radius: 7)
```

### Referenz häufiger Modifier {#common-modifiers-reference}

```swift
.padding()                          // default padding on all sides
.padding(.bottom, -5)               // negative padding = move closer
.padding(.horizontal, 20)           // only horizontal sides
.background(.black.opacity(0.5))    // semi-transparent background
.clipShape(.capsule)                // clip to capsule shape
.clipShape(.rect(cornerRadius: 15)) // clip to rounded rectangle
.foregroundStyle(.white)            // text/symbol color
.opacity(0.5)                       // 50% opacity
.ignoresSafeArea()                  // extend into safe areas
.border(.blue)                      // debug: show view bounds
.frame(width: 200, height: 50)     // explicit size
.frame(maxWidth: .infinity)         // fill width
.disabled(someCondition)            // prevent interaction
```

### Bild-Modifier {#image-modifiers}

```swift
Image(.backgroundParchment)    // asset catalog image
    .resizable()               // allows resizing (required before scaling)
    .scaledToFill()            // fill container, may crop
    .scaledToFit()             // fit container, maintains ratio
    .ignoresSafeArea()         // extend behind status bar
    .frame(height: 200)
    .scaleEffect(x: -1)       // flip horizontally

Image(systemName: "equal")    // SF Symbol
    .font(.largeTitle)         // SF Symbols respond to font modifier
    .symbolEffect(.pulse)      // animation effect (iOS 17+)
    .imageScale(.large)

// Pixel art (no blur)
AsyncImage(url: spriteURL) { image in
    image.interpolation(.none)  // sharp pixels
        .resizable()
        .scaledToFit()
}
```

### Button-Styles {#button-styles}

```swift
// Simple label
Button("Tap me") { doSomething() }

// Custom label (image + text)
Button {
    showExchangeInfo = true
} label: {
    Image(systemName: "info.circle.fill")
        .font(.largeTitle)
        .foregroundStyle(.white)
}

// Button extension for reusable styling
extension Button {
    func doneButton() -> some View {
        self
            .font(.largeTitle)
            .padding()
            .buttonStyle(.borderedProminent)
            .tint(.brown)
            .foregroundStyle(.white)
    }
}

Button("Done") { dismiss() }
    .doneButton()
```

### Wiederverwendbare Views mit Parametern {#reusable-views-with-parameters}

```swift
struct CustomButtonView: View {
    var title: String
    var color: Color

    var body: some View {
        Text(title)
            .foregroundStyle(.white)
            .padding()
            .background(color)
            .clipShape(RoundedRectangle(cornerRadius: 15))
    }
}

// Usage
CustomButtonView(title: "Tap Me", color: .blue)
```

### GeometryReader für responsives Layout {#geometryreader-for-responsive-layout}

```swift
GeometryReader { geo in
    Image(predator.type.rawValue)
        .resizable()
        .frame(width: geo.size.width)

    Text("Title")
        .offset(x: geo.size.width / 2.3)
}
```

`geo.size.width` / `geo.size.height` = tatsächlich gerenderte Größe des Containers. Passt sich an Bildschirmgröße und Gerät an.

### LinearGradient-Overlay {#lineargradient-overlay}

```swift
Image(predator.type.rawValue)
    .overlay {
        LinearGradient(
            stops: [
                .init(color: .clear, location: 0.5),
                .init(color: .black, location: 1.0)
            ],
            startPoint: .top,
            endPoint: .bottom
        )
    }
```

### Eigene Farben (Asset-Katalog) {#custom-colors-assets-catalog}

1. In Assets.xcassets `+` > Color Set auswählen
2. Einen Namen vergeben (z. B. "BreakingBadButton")
3. Farbe über den Hex-Wert festlegen

```swift
// Dot notation (static):
.background(.breakingBadButton)

// Dynamic using string:
Color(show.replacingOccurrences(of: " ", with: "") + "Button")
```

### Akzentfarbe für die Navigation {#accent-color-for-navigation}

In Assets.xcassets die Akzentfarbe („Accent Color") mit den Erscheinungsbildern Any (Light) und Dark festlegen. Sie gilt automatisch für alle Zurück-Buttons der Navigation und für Toolbar-Buttons.

### Dark Mode {#dark-mode}

```swift
// Force dark mode for whole stack
NavigationStack { ... }
    .preferredColorScheme(.dark)

// Override system color for specific content
ScrollView { VStack { /* text views */ } }
    .foregroundStyle(.black)
```

### minimumScaleFactor {#minimumscalefactor}

```swift
Text(longQuote)
    .minimumScaleFactor(0.5)   // text can shrink to 50% to fit
```

Verhindert das Abschneiden von Text, allerdings auf Kosten einer kleineren Schriftgröße.

## Stolperfallen {#gotchas}

- `.resizable()` muss vor `.scaledToFit()`/`.scaledToFill()` stehen, sonst hat die Größenanpassung keine Wirkung
- Die Reihenfolge der Modifier ist wichtig: `.padding().background(.blue)` platziert das Padding innerhalb der blauen Fläche; `.background(.blue).padding()` platziert es außerhalb
- `ZStack`-Ebenen: das erste Kind liegt ganz unten, das letzte ganz oben
- `Spacer()` verhält sich in `VStack` (vertikaler Abstand) anders als in `HStack` (horizontaler Abstand)
- `GeometryReader` füllt den gesamten verfügbaren Platz und richtet Inhalte standardmäßig oben-führend (top-leading) aus
- Der Inhalt einer `ScrollView` beginnt oben, während `VStack` standardmäßig zentriert
- Das Force-Unwrap `URL(string:)!` ist nur bei zur Kompilierzeit bekannten, gültigen Strings sicher

## Siehe auch {#see-also}

- [[swiftui-state-and-data-flow]] - @State, @Binding für interaktive Views
- [[swiftui-navigation]] - NavigationStack, Sheets, Tabs
- [[swiftui-lists-and-grids]] - List, ForEach, LazyVGrid
- [[swiftui-animations]] - withAnimation, Übergänge, matchedGeometryEffect
