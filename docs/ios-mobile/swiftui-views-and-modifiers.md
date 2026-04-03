---
title: SwiftUI Views and Modifiers
category: concepts
tags: [ios-mobile, swiftui, views, modifiers, layout, text, image, button]
---

# SwiftUI Views and Modifiers

Every visual element in SwiftUI is a View. Views are structs conforming to the `View` protocol, composed using declarative syntax. Modifiers chain onto views to change appearance and behavior. This entry covers built-in views, layout containers, modifier chaining, and reusable view patterns.

## Key Facts

- Every custom view is a `struct` conforming to `View` with a required `body` computed property
- `some View` is an opaque return type - hides the exact type while guaranteeing it conforms to `View`
- Modifiers chain using dot syntax; **order matters** (padding before background vs after)
- Layout containers: `VStack` (vertical), `HStack` (horizontal), `ZStack` (overlapping)
- `Spacer()` expands to fill available space in stacks
- `GeometryReader` provides actual container dimensions for responsive sizing
- SF Symbols are used via `Image(systemName: "symbol.name")` and respond to `.font()` modifier

## Patterns

### Basic View Structure

```swift
struct ContentView: View {
    var body: some View {
        Text("Hello, world!")
    }
}
```

### Built-in View Types

| View | Usage |
|------|-------|
| `Text("string")` | Display text |
| `Image("name")` | Asset catalog image |
| `Image(systemName: "star")` | SF Symbol |
| `Button("label") { action }` | Tappable button |
| `Circle()` | Circle shape |
| `RoundedRectangle(cornerRadius: 10)` | Rounded rect shape |
| `TextField("placeholder", text: $binding)` | Text input |
| `Spacer()` | Flexible space |
| `Divider()` | Horizontal line |
| `ProgressView()` | Loading spinner |
| `EmptyView()` | Invisible placeholder |
| `Link("text", destination: URL)` | External URL link |

### Layout Containers

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

### Modifier Chaining (Order Matters)

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

### Common Modifiers Reference

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

### Image Modifiers

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

### Button Styles

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

### Reusable Views with Parameters

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

### GeometryReader for Responsive Layout

```swift
GeometryReader { geo in
    Image(predator.type.rawValue)
        .resizable()
        .frame(width: geo.size.width)

    Text("Title")
        .offset(x: geo.size.width / 2.3)
}
```

`geo.size.width` / `geo.size.height` = actual rendered size of the container. Adapts to screen size and device.

### LinearGradient Overlay

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

### Custom Colors (Assets Catalog)

1. In Assets.xcassets, press `+` > Color Set
2. Name it (e.g., "BreakingBadButton")
3. Set color via hex value

```swift
// Dot notation (static):
.background(.breakingBadButton)

// Dynamic using string:
Color(show.replacingOccurrences(of: " ", with: "") + "Button")
```

### Accent Color for Navigation

In Assets.xcassets, set Accent Color with Any (Light) and Dark appearances. Applies to all navigation back buttons and toolbar buttons automatically.

### Dark Mode

```swift
// Force dark mode for whole stack
NavigationStack { ... }
    .preferredColorScheme(.dark)

// Override system color for specific content
ScrollView { VStack { /* text views */ } }
    .foregroundStyle(.black)
```

### minimumScaleFactor

```swift
Text(longQuote)
    .minimumScaleFactor(0.5)   // text can shrink to 50% to fit
```

Prevents text truncation at the cost of smaller font size.

## Gotchas

- `.resizable()` must come before `.scaledToFit()`/`.scaledToFill()` or sizing has no effect
- Modifier order matters: `.padding().background(.blue)` puts padding inside the blue area; `.background(.blue).padding()` puts padding outside
- `ZStack` layers: first child is bottommost, last child is topmost
- `Spacer()` behaves differently in `VStack` (vertical space) vs `HStack` (horizontal space)
- `GeometryReader` fills all available space and aligns content to top-leading by default
- `ScrollView` content starts at top, unlike `VStack` which centers by default
- Force unwrap on `URL(string:)!` is only safe for compile-time known valid strings

## See Also

- [[swiftui-state-and-data-flow]] - @State, @Binding for interactive views
- [[swiftui-navigation]] - NavigationStack, sheets, tabs
- [[swiftui-lists-and-grids]] - List, ForEach, LazyVGrid
- [[swiftui-animations]] - withAnimation, transitions, matchedGeometryEffect
