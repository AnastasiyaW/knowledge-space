---
title: SwiftUI Animations
category: concepts
tags: [ios-mobile, swiftui, animations, transitions, withAnimation, matchedGeometryEffect, namespace]
---

# SwiftUI Animations

SwiftUI animations are property-driven: toggle a Bool, attach modifiers that react to it, wrap the toggle in `withAnimation`. This entry covers animation triggers, transitions, matched geometry effects, and patterns for complex multi-step animations.

## Key Facts

- Animations are driven by `@State` Bool toggled inside `withAnimation { }` block
- Modifiers use ternary operator to switch between animated/default values
- `.transition()` controls how views enter/exit the hierarchy
- `matchedGeometryEffect` morphs between two views in different positions
- `@Namespace` groups connected animations together
- `.onAppear` with `withAnimation(.repeatForever())` creates looping animations
- Duration-0 trick: set `animateViewsIn ? duration : 0` to reset instantly

## Patterns

### Basic Property Animation

```swift
@State private var revealHint = false

image
    .rotation3DEffect(
        revealHint ? .degrees(1440) : .degrees(0),
        axis: (x: 0, y: 1, z: 0)
    )
    .scaleEffect(revealHint ? 5 : 1)
    .opacity(revealHint ? 0 : 1)
    .offset(x: revealHint ? geo.size.width / 2 : 0)
    .onTapGesture {
        withAnimation(.easeOut(duration: 1)) {
            revealHint = true
        }
    }
```

### Looping Animation on Appear

```swift
@State private var hintWiggle = false

.onAppear {
    withAnimation(
        .easeInOut(duration: 0.1)
        .repeatCount(9, autoreverses: true)
        .delay(5)
        .repeatForever()
    ) {
        hintWiggle = true
    }
}

// Apply to modifier
.rotationEffect(hintWiggle ? .degrees(-13) : .degrees(-17))
```

### View Transitions (Animate In/Out)

```swift
VStack {
    if animateViewsIn {
        Text(question)
            .transition(.scale)

        Text(answer)
            .transition(
                .scale.combined(
                    with: .offset(y: -geo.size.height / 2)
                )
            )
    }
}
.animation(
    .easeInOut(duration: 2).delay(0),
    value: animateViewsIn
)
```

### Instant Reset (Zero-Duration Trick)

When resetting views, use duration 0 so they disappear instantly:

```swift
.animation(
    .easeInOut(duration: animateViewsIn ? 2 : 0)
        .delay(animateViewsIn ? 1 : 0),
    value: animateViewsIn
)
```

Reset flow:
```swift
animateViewsIn = false          // views vanish instantly (duration 0)
tappedCorrectAnswer = false
revealHint = false

DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
    animateViewsIn = true       // views animate back in (duration 2)
}
```

### matchedGeometryEffect + @Namespace

Morph between two views in different positions:

```swift
struct GameplayView: View {
    @Namespace private var namespace

    var body: some View {
        // Small version in answer list
        if !tappedCorrectAnswer {
            Text(answer)
                .matchedGeometryEffect(id: "answer", in: namespace)
                .onTapGesture {
                    withAnimation(.easeOut(duration: 1)) {
                        tappedCorrectAnswer = true
                    }
                }
        }

        // Big version in celebration screen
        if tappedCorrectAnswer {
            Text(answer)
                .font(.largeTitle)
                .matchedGeometryEffect(id: "answer", in: namespace)
        }
    }
}
```

Rules:
- Same `id:` on both views marks them as the same logical view
- Both must share the same `@Namespace` instance
- When one disappears and the other appears, SwiftUI morphs between their frames

### Score Moving to Total Animation

```swift
@State private var movePointsToScore = false

Text("\(pointsEarned)")
    .offset(
        x: movePointsToScore ? geo.size.width / 2.3 : 0,
        y: movePointsToScore ? -geo.size.height / 13 : 0
    )
    .opacity(movePointsToScore ? 0 : 1)
    .onAppear {
        withAnimation(.easeInOut(duration: 1).delay(3)) {
            movePointsToScore = true
        }
    }
```

### DispatchQueue.main.asyncAfter

Delay state changes for animation sequencing:

```swift
DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
    animateViewsIn = true
}
```

### .animation on List Data Changes

```swift
List(predators.search(for: searchText)) { ... }
    .animation(.default, value: predators.apexPredators)
```

Animates row additions/removals/reordering when the list data changes.

## Gotchas

- `withAnimation` only animates changes made inside its closure - haptics and non-visual code should go outside
- `.transition()` only works when views are conditionally added/removed from the hierarchy (via `if`)
- `@Namespace` must be declared in the view that contains both matched views - passing it between views requires `@Namespace` binding
- `matchedGeometryEffect` views must both exist (briefly) for the morph to work - use if/else, not removal
- `.repeatForever()` animation cannot be stopped once started - toggle the triggering Bool back to reset
- `DispatchQueue.main.asyncAfter` is not cancellable - for cancellable delays, use `Task.sleep` with structured concurrency

## See Also

- [[swiftui-views-and-modifiers]] - modifiers that respond to animated state changes
- [[swiftui-state-and-data-flow]] - @State Bools that drive animations
- [[swiftui-navigation]] - zoom navigation transitions (iOS 18+)
