---
title: "SwiftUI-Animationen"
category: concepts
tags: [ios-mobile, swiftui, animations, transitions, withAnimation, matchedGeometryEffect, namespace]
level: 3
source_sha256: f6edc2e29c48a013d2f747c1104ba50f9629b72d8b2a9b8225079d1544986d6e
translation: machine
translated_at: '2026-10-24'
---
# SwiftUI-Animationen {#swiftui-animations}

SwiftUI-Animationen sind property-gesteuert: Man schaltet einen Bool um, hängt Modifier an, die darauf reagieren, und umschließt das Umschalten mit `withAnimation`. Dieser Eintrag behandelt Animationsauslöser, Transitionen, matched geometry effects und Muster für komplexe mehrstufige Animationen.

## Zentrale Fakten {#key-facts}

- Animationen werden durch einen `@State`-Bool gesteuert, der innerhalb eines `withAnimation { }`-Blocks umgeschaltet wird
- Modifier verwenden den ternären Operator, um zwischen animierten und Standardwerten zu wechseln
- `.transition()` steuert, wie Views in die Hierarchie ein- und aus ihr austreten
- `matchedGeometryEffect` überführt fließend zwischen zwei Views an unterschiedlichen Positionen
- `@Namespace` gruppiert zusammengehörige Animationen
- `.onAppear` mit `withAnimation(.repeatForever())` erzeugt Endlosanimationen
- Null-Dauer-Trick: `animateViewsIn ? duration : 0` setzt sofort zurück

## Muster {#patterns}

### Einfache Property-Animation {#basic-property-animation}

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

### Endlosanimation beim Erscheinen {#looping-animation-on-appear}

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

### View-Transitionen (Ein- und Ausblenden) {#view-transitions-animate-inout}

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

### Sofortiges Zurücksetzen (Null-Dauer-Trick) {#instant-reset-zero-duration-trick}

Beim Zurücksetzen von Views verwendet man die Dauer 0, damit sie sofort verschwinden:

```swift
.animation(
    .easeInOut(duration: animateViewsIn ? 2 : 0)
        .delay(animateViewsIn ? 1 : 0),
    value: animateViewsIn
)
```

Ablauf beim Zurücksetzen:
```swift
animateViewsIn = false          // views vanish instantly (duration 0)
tappedCorrectAnswer = false
revealHint = false

DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
    animateViewsIn = true       // views animate back in (duration 2)
}
```

### matchedGeometryEffect + @Namespace {#matchedgeometryeffect-namespace}

Überführung zwischen zwei Views an unterschiedlichen Positionen:

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

Regeln:
- Dieselbe `id:` an beiden Views kennzeichnet sie als dieselbe logische View
- Beide müssen dieselbe `@Namespace`-Instanz teilen
- Wenn die eine View verschwindet und die andere erscheint, überführt SwiftUI zwischen deren Frames

### Animation: Score wird zur Summe verschoben {#score-moving-to-total-animation}

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

### DispatchQueue.main.asyncAfter {#dispatchqueuemainasyncafter}

Zustandsänderungen für die Abfolge von Animationen verzögern:

```swift
DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
    animateViewsIn = true
}
```

### .animation bei Änderungen von Listendaten {#animation-on-list-data-changes}

```swift
List(predators.search(for: searchText)) { ... }
    .animation(.default, value: predators.apexPredators)
```

Animiert das Hinzufügen, Entfernen und Umordnen von Zeilen, wenn sich die Listendaten ändern.

## Fallstricke {#gotchas}

- `withAnimation` animiert nur Änderungen innerhalb seines Closures; Haptik und nicht visueller Code sollten außerhalb stehen
- `.transition()` funktioniert nur, wenn Views bedingt zur Hierarchie hinzugefügt oder daraus entfernt werden (über `if`)
- `@Namespace` muss in der View deklariert werden, die beide gematchten Views enthält; wird es zwischen Views weitergereicht, ist ein `@Namespace`-Binding nötig
- `matchedGeometryEffect`-Views müssen beide (kurzzeitig) existieren, damit die Überführung funktioniert; also if/else verwenden, nicht Entfernen
- Eine `.repeatForever()`-Animation lässt sich nach dem Start nicht mehr anhalten; zum Zurücksetzen den auslösenden Bool zurückschalten
- `DispatchQueue.main.asyncAfter` ist nicht abbrechbar; für abbrechbare Verzögerungen `Task.sleep` mit Structured Concurrency verwenden

## Siehe auch {#see-also}

- [[swiftui-views-and-modifiers]] - Modifier, die auf animierte Zustandsänderungen reagieren
- [[swiftui-state-and-data-flow]] - @State-Bools, die Animationen steuern
- [[swiftui-navigation]] - Zoom-Navigationstransitionen (iOS 18+)
