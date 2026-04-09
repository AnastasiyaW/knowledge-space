---
title: "SwiftUI Layout Testing"
description: "Property-based fuzzing to verify custom layout engines against Apple's native SwiftUI rendering"
---

# SwiftUI Layout Testing

Automated verification of custom SwiftUI layout implementations by comparing against Apple's native rendering using property-based testing (fuzzing).

## Approach

Generate random view configurations, render with both your custom layout engine and SwiftUI, then compare results:

1. Define an enum of possible child view configurations
2. Randomly generate view hierarchies
3. Measure children using your implementation
4. Measure children using SwiftUI (via `GeometryReader` + preferences)
5. Assert equality

## Generating Random View Configurations

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

**Important:** For `.minMax`, generate `max` first, then `min` in `0...max`. Generating independently produces invalid frames where `min > max`.

## Measuring SwiftUI Views

Use `PreferenceKey` to propagate child sizes up:

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

Force rendering with `UIHostingController`:

```swift
let host = UIHostingController(rootView: swiftUIStack)
host.view.frame = CGRect(x: 0, y: 0, width: proposedWidth, height: 100)
_ = host.view.snapshotView(afterScreenUpdates: true)
```

## Test Loop

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

## Platform Differences

Run tests on iOS, not macOS. Known macOS issues:

- HStack with centered content and oversized children renders subviews too large and off-center
- GeometryReader centers content on macOS but top-leading aligns on iOS

Set up both a macOS and iOS test target, but validate against iOS behavior for correctness.

## Gotchas

- **`CGFloat.greatestFiniteMagnitude` precision loss:** When comparing flexibility ranges, `greatestFiniteMagnitude` (10^308) loses precision in the fractional digits. Two views with different min-widths but the same max-width of `greatestFiniteMagnitude` will compute identical flexibility values. Use a large-but-precise sentinel like `1e15` instead.
- **Rounding errors:** Custom layout and SwiftUI may round to pixels differently. Use `accuracy` parameter in `XCTAssertEqual` for floating-point comparisons, or round both sides to the same precision before comparing.
- **Logging on failure:** Print the `frames` array and `proposedWidth` in the assertion message. Without this, a fuzzing failure gives you sizes but no way to reproduce the input configuration.

## See Also

- [[swiftui-views-and-modifiers]]
- [[swiftui-state-and-data-flow]]
- [[swift-phantom-types]]
