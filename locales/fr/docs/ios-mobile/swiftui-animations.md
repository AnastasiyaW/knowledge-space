---
title: "Animations SwiftUI"
category: concepts
tags: [ios-mobile, swiftui, animations, transitions, withAnimation, matchedGeometryEffect, namespace]
level: 3
source_sha256: f6edc2e29c48a013d2f747c1104ba50f9629b72d8b2a9b8225079d1544986d6e
translation: machine
translated_at: '2026-10-24'
---
# Animations SwiftUI {#swiftui-animations}

Les animations SwiftUI sont pilotées par les propriétés : on bascule un Bool, on attache des modificateurs qui réagissent à cette valeur, puis on enveloppe le basculement dans `withAnimation`. Cette entrée couvre les déclencheurs d'animation, les transitions, les effets de géométrie appariée (matched geometry effects) et les schémas pour les animations complexes en plusieurs étapes.

## Points clés {#key-facts}

- Les animations sont pilotées par un `@State` Bool basculé à l'intérieur d'un bloc `withAnimation { }`
- Les modificateurs utilisent l'opérateur ternaire pour alterner entre valeurs animées et valeurs par défaut
- `.transition()` contrôle la manière dont les vues entrent dans la hiérarchie et en sortent
- `matchedGeometryEffect` effectue une transformation morphologique entre deux vues situées à des positions différentes
- `@Namespace` regroupe les animations liées entre elles
- `.onAppear` avec `withAnimation(.repeatForever())` crée des animations en boucle
- Astuce de durée nulle : définir `animateViewsIn ? duration : 0` pour réinitialiser instantanément

## Patrons {#patterns}

### Animation de propriété de base {#basic-property-animation}

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

### Animation en boucle à l'apparition {#looping-animation-on-appear}

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

### Transitions de vues (animer l'entrée et la sortie) {#view-transitions-animate-inout}

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

### Réinitialisation instantanée (astuce de durée nulle) {#instant-reset-zero-duration-trick}

Lors de la réinitialisation des vues, utiliser une durée de 0 pour qu'elles disparaissent instantanément :

```swift
.animation(
    .easeInOut(duration: animateViewsIn ? 2 : 0)
        .delay(animateViewsIn ? 1 : 0),
    value: animateViewsIn
)
```

Déroulement de la réinitialisation :
```swift
animateViewsIn = false          // views vanish instantly (duration 0)
tappedCorrectAnswer = false
revealHint = false

DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
    animateViewsIn = true       // views animate back in (duration 2)
}
```

### matchedGeometryEffect + @Namespace {#matchedgeometryeffect-namespace}

Transformation morphologique entre deux vues situées à des positions différentes :

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

Règles :
- Le même `id:` sur les deux vues les identifie comme une seule et même vue logique
- Les deux vues doivent partager la même instance de `@Namespace`
- Lorsque l'une disparaît et que l'autre apparaît, SwiftUI effectue la transformation entre leurs cadres

### Animation de déplacement du score vers le total {#score-moving-to-total-animation}

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

Retarder les changements d'état pour séquencer les animations :

```swift
DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
    animateViewsIn = true
}
```

### .animation sur les changements de données d'une liste {#animation-on-list-data-changes}

```swift
List(predators.search(for: searchText)) { ... }
    .animation(.default, value: predators.apexPredators)
```

Anime les ajouts, suppressions et réordonnancements de lignes lorsque les données de la liste changent.

## Pièges courants {#gotchas}

- `withAnimation` ne anime que les modifications effectuées à l'intérieur de sa closure ; le code haptique et le code non visuel doivent être placés à l'extérieur
- `.transition()` ne fonctionne que lorsque les vues sont ajoutées ou retirées conditionnellement de la hiérarchie (via `if`)
- `@Namespace` doit être déclaré dans la vue qui contient les deux vues appariées ; le transmettre entre vues nécessite une liaison `@Namespace`
- Les vues de `matchedGeometryEffect` doivent exister toutes les deux (brièvement) pour que la transformation fonctionne ; utiliser if/else, et non une suppression
- Une animation `.repeatForever()` ne peut pas être arrêtée une fois lancée ; pour la réinitialiser, rebasculer le Bool déclencheur
- `DispatchQueue.main.asyncAfter` ne peut pas être annulé ; pour des délais annulables, utiliser `Task.sleep` avec la concurrence structurée

## Voir aussi {#see-also}

- [[swiftui-views-and-modifiers]] - modificateurs qui réagissent aux changements d'état animés
- [[swiftui-state-and-data-flow]] - Bools `@State` qui pilotent les animations
- [[swiftui-navigation]] - transitions de navigation par zoom (iOS 18+)
