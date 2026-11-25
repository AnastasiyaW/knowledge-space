---
title: "Vues et modificateurs SwiftUI"
category: concepts
tags: [ios-mobile, swiftui, views, modifiers, layout, text, image, button]
level: 3
source_sha256: f1f97ab71e205feb396860abad68185a3ca9588b9f61a85f55f951d46ba629f7
translation: machine
translated_at: '2026-10-24'
---
# Vues et modificateurs SwiftUI {#swiftui-views-and-modifiers}

Chaque élément visuel de SwiftUI est une View. Les views sont des structs conformes au protocole `View`, composées avec une syntaxe déclarative. Les modificateurs s'enchaînent sur les views pour modifier l'apparence et le comportement. Cette entrée couvre les vues intégrées, les conteneurs de mise en page, l'enchaînement de modificateurs et les patterns de vues réutilisables.

## Points clés {#key-facts}

- Chaque vue personnalisée est une `struct` conforme à `View`, avec une propriété calculée `body` obligatoire
- `some View` est un type de retour opaque : il masque le type exact tout en garantissant la conformité à `View`
- Les modificateurs s'enchaînent avec la syntaxe pointée ; **l'ordre compte** (padding avant ou après background)
- Conteneurs de mise en page : `VStack` (vertical), `HStack` (horizontal), `ZStack` (superposition)
- `Spacer()` occupe tout l'espace disponible dans les stacks
- `GeometryReader` fournit les dimensions réelles du conteneur pour un dimensionnement adaptatif
- Les SF Symbols s'utilisent via `Image(systemName: "symbol.name")` et répondent au modificateur `.font()`

## Patterns {#patterns}

### Structure de base d'une vue {#basic-view-structure}

```swift
struct ContentView: View {
    var body: some View {
        Text("Hello, world!")
    }
}
```

### Types de vues intégrés {#built-in-view-types}

| View | Usage |
|------|-------|
| `Text("string")` | Afficher du texte |
| `Image("name")` | Image du catalogue d'assets |
| `Image(systemName: "star")` | SF Symbol |
| `Button("label") { action }` | Bouton cliquable |
| `Circle()` | Forme cercle |
| `RoundedRectangle(cornerRadius: 10)` | Forme rectangle arrondi |
| `TextField("placeholder", text: $binding)` | Saisie de texte |
| `Spacer()` | Espace flexible |
| `Divider()` | Ligne horizontale |
| `ProgressView()` | Indicateur de chargement |
| `EmptyView()` | Placeholder invisible |
| `Link("text", destination: URL)` | Lien vers une URL externe |

### Conteneurs de mise en page {#layout-containers}

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

### Enchaînement de modificateurs (l'ordre compte) {#modifier-chaining-order-matters}

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

### Référence des modificateurs courants {#common-modifiers-reference}

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

### Modificateurs d'image {#image-modifiers}

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

### Styles de boutons {#button-styles}

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

### Vues réutilisables avec paramètres {#reusable-views-with-parameters}

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

### GeometryReader pour une mise en page adaptative {#geometryreader-for-responsive-layout}

```swift
GeometryReader { geo in
    Image(predator.type.rawValue)
        .resizable()
        .frame(width: geo.size.width)

    Text("Title")
        .offset(x: geo.size.width / 2.3)
}
```

`geo.size.width` / `geo.size.height` = taille réelle rendue du conteneur. S'adapte à la taille de l'écran et à l'appareil.

### Superposition avec LinearGradient {#lineargradient-overlay}

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

### Couleurs personnalisées (catalogue d'assets) {#custom-colors-assets-catalog}

1. Dans Assets.xcassets, appuyez sur `+` > Color Set
2. Nommez-le (par exemple « BreakingBadButton »)
3. Définissez la couleur via une valeur hexadécimale

```swift
// Dot notation (static):
.background(.breakingBadButton)

// Dynamic using string:
Color(show.replacingOccurrences(of: " ", with: "") + "Button")
```

### Couleur d'accent pour la navigation {#accent-color-for-navigation}

Dans Assets.xcassets, définissez la couleur d'accent avec les apparences Any (Light) et Dark. Elle s'applique automatiquement à tous les boutons de retour de navigation et aux boutons de la barre d'outils.

### Mode sombre {#dark-mode}

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

Évite la troncature du texte au prix d'une taille de police réduite.

## Pièges {#gotchas}

- `.resizable()` doit précéder `.scaledToFit()`/`.scaledToFill()`, sinon le dimensionnement n'a aucun effet
- L'ordre des modificateurs compte : `.padding().background(.blue)` place le padding à l'intérieur de la zone bleue ; `.background(.blue).padding()` place le padding à l'extérieur
- Les couches de `ZStack` : le premier enfant est le plus bas, le dernier est le plus haut
- `Spacer()` se comporte différemment dans `VStack` (espace vertical) et dans `HStack` (espace horizontal)
- `GeometryReader` occupe tout l'espace disponible et aligne le contenu en haut-début par défaut
- Le contenu d'une `ScrollView` commence en haut, contrairement à `VStack` qui centre par défaut
- Le force unwrap sur `URL(string:)!` n'est sûr que pour des chaînes valides connues à la compilation

## Voir aussi {#see-also}

- [[swiftui-state-and-data-flow]] - @State, @Binding pour les vues interactives
- [[swiftui-navigation]] - NavigationStack, sheets, tabs
- [[swiftui-lists-and-grids]] - List, ForEach, LazyVGrid
- [[swiftui-animations]] - withAnimation, transitions, matchedGeometryEffect
