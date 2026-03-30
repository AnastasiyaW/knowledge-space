---
title: SwiftUI Views and Modifiers
category: ios-mobile/ui
tags: [swiftui, views, modifiers, text, image, button, swiftui-6]
---

# SwiftUI Views and Modifiers

## Key Facts

- SwiftUI is Apple's declarative UI framework - describes **what** the UI should look like, not **how** to build it
- Every SwiftUI view is a `struct` conforming to the `View` protocol with a required `body` computed property
- Views are composed by nesting - a view can contain other views ("Viewception")
- Modifiers are chained with dot syntax and return new modified views: `.padding()`, `.foregroundStyle()`, `.font()`
- Visual modifiers change appearance; functional modifiers add behavior (e.g., `.sheet()`, `.searchable()`)
- SwiftUI automatically handles view updates when [[state-and-data-flow]] properties change
- The `import SwiftUI` statement must be at the top of every SwiftUI file
- Preview code at the bottom of a file (`#Preview { }`) tells Xcode to show a live preview
- Previews are limited - they only render what's in the preview body, not the full app navigation

## Patterns

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            // Image from asset catalog
            Image(.backgroundImage)
                .resizable()
                .scaledToFit()
                .padding()

            // Text with modifiers
            Text("Hello, SwiftUI!")
                .font(.title)
                .foregroundStyle(.blue)
                .bold()

            // Button with action
            Button("Tap Me") {
                print("Button tapped")
            }
            .buttonStyle(.borderedProminent)
        }
    }
}

#Preview {
    ContentView()
}
```

```swift
// Image from SF Symbols (system icons)
Image(systemName: "star.fill")
    .font(.largeTitle)
    .foregroundStyle(.yellow)

// TextField for user input
@State private var userInput = ""
TextField("Enter text", text: $userInput)
    .textFieldStyle(.roundedBorder)
```

## Gotchas

- Modifier order matters: `.padding().background(.blue)` differs from `.background(.blue).padding()`
- Preview does not behave like a real device - sheet dismiss, navigation, and some interactions only work on simulator/device
- `Image` initializer differs: `Image(.assetName)` for asset catalog vs `Image(systemName:)` for SF Symbols
- Container views (VStack, HStack, ZStack) have a 10-child limit without `Group` or `ForEach`
- `.foregroundStyle()` replaced `.foregroundColor()` in newer SwiftUI versions
- Preview pauses sometimes - click the refresh/play button to restart it

## See Also

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [[container-views-and-layout]]
- [[state-and-data-flow]]
