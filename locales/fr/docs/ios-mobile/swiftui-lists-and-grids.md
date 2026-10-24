---
title: "Listes et grilles en SwiftUI"
category: concepts
tags: [ios-mobile, swiftui, list, foreach, lazyvgrid, scrollview, identifiable]
level: 3
source_sha256: 3f10656a019b46b0df2f609e5202e62159c8f0761ccf8b8bc3379df2788614fd
translation: machine
translated_at: '2026-10-24'
---
# Listes et grilles en SwiftUI {#swiftui-lists-and-grids}

List, ForEach, LazyVGrid et ScrollView sont les conteneurs principaux pour afficher des collections de données dans SwiftUI. Cette entrée couvre les listes dynamiques, les mises en page en grille, la suppression par glissement (swipe-to-delete) et les différences entre les conteneurs défilants.

## Points clés {#key-facts}

- `List` affiche des lignes défilantes avec des séparateurs intégrés et la suppression par glissement
- `ForEach` génère des vues à partir d'une collection mais n'est pas défilant par lui-même
- Les éléments de `ForEach`/`List` doivent implémenter `Identifiable` ou fournir le paramètre `id:`
- `LazyVGrid` crée des mises en page en grille défilantes avec des colonnes flexibles ou fixes
- `ScrollView` fournit une mise en page défilante personnalisée, sans les fonctionnalités intégrées de List
- Syntaxe des intervalles dans `ForEach` : seuls les intervalles semi-ouverts (`0..<5`) sont acceptés, pas les intervalles fermés (`0...4`)

## Patrons {#patterns}

### Liste statique {#static-list}

```swift
List {
    Text("Hello")
    Circle().frame(height: 40)
    Text("Hi")
}
```

### Liste dynamique à partir d'un tableau {#dynamic-list-from-array}

```swift
struct ContentView: View {
    var dogs = ["Fido", "Sarah", "Billy"]

    var body: some View {
        List(dogs, id: \.self) { dog in
            Text(dog)
        }
    }
}
```

`id: \.self` utilise la valeur elle-même comme identifiant. Fonctionne pour String, Int, etc.

### Liste avec un modèle Identifiable {#list-with-identifiable-model}

```swift
class JournalEntry: Identifiable {
    var id = UUID()
    var title: String
    var text: String
}

List(journalEntries) { entry in
    Text(entry.title)
}
```

La conformité à `Identifiable` fournit une propriété `id` générée automatiquement.

### ForEach dans une List (avec onDelete) {#foreach-inside-list-with-ondelete}

```swift
List {
    ForEach(entries) { entry in
        Text(entry.title)
    }
    .onDelete { indices in
        entries.remove(atOffsets: indices)
    }
}
```

### Variantes de ForEach {#foreach-variants}

```swift
// Range-based (underscore when not using index)
ForEach(0..<5) { _ in
    CurrencyIcon(currency: .copperPenny)
}

// Named index
ForEach(0..<5) { index in
    Text("Row \(index)")
}

// Collection-based with Identifiable
ForEach(journalEntries) { entry in
    Text(entry.title)
}

// Non-Identifiable with id parameter
ForEach(predator.movies, id: \.self) { movie in
    Text(movie)
}

// Enum cases
ForEach(Currency.allCases, id: \.self) { currency in
    CurrencyIcon(currency: currency)
}
```

### LazyVGrid {#lazyvgrid}

```swift
let columns = [GridItem(), GridItem(), GridItem()]   // 3 flexible columns

LazyVGrid(columns: columns) {
    ForEach(currencies, id: \.self) { currency in
        CurrencyIcon(currency: currency)
    }
}
.padding()
```

Types de colonnes :
- `GridItem()` - flexible (par défaut), occupe l'espace disponible
- `GridItem(.fixed(100))` - largeur fixe
- Nombre de colonnes = nombre de `GridItem` dans le tableau

### ScrollView ou List {#scrollview-vs-list}

```swift
// List - built-in rows, separators, swipe-to-delete, selection
List(items) { item in Text(item.name) }

// ScrollView - custom layout, no separators
ScrollView {
    VStack {
        ForEach(items) { item in Text(item.name) }
    }
}
```

Le contenu de ScrollView commence en haut. Utilisez ScrollView pour une mise en page entièrement personnalisée ; utilisez List pour des lignes standard.

### ScrollViewReader (défilement programmatique) {#scrollviewreader-programmatic-scrolling}

```swift
ScrollViewReader { proxy in
    ScrollView {
        ForEach(items) { item in
            Text(item.name).id(item.id)
        }
    }
    Button("Scroll to last") {
        proxy.scrollTo(items.last?.id, anchor: .bottom)
    }
}
```

### Patron de tri, filtrage et recherche {#sort-filter-and-search-pattern}

```swift
@Observable
class Predators {
    var apexPredators: [ApexPredator] = []
    var allApexPredators: [ApexPredator] = []   // master list, never modified

    func sortByName(alphabetical: Bool) {
        apexPredators.sort { pred1, pred2 in
            alphabetical ? pred1.name < pred2.name : pred1.id < pred2.id
        }
    }

    func filterBy(_ type: APType?) {
        if let type {
            apexPredators = allApexPredators.filter { $0.type == type }
        } else {
            apexPredators = allApexPredators
        }
    }

    func search(for text: String) -> [ApexPredator] {
        if text.isEmpty {
            return apexPredators
        } else {
            return apexPredators.filter {
                $0.name.localizedCaseInsensitiveContains(text)
            }
        }
    }
}
```

**Critique** : filtrez toujours à partir de `allApexPredators` (liste principale), et non à partir de `apexPredators` déjà filtrée. Sinon, l'application d'un second filtre produit des résultats vides.

### Animation des modifications de liste {#animating-list-changes}

```swift
List { ... }
    .animation(.default, value: predators.apexPredators)
```

### Liste avec pied de section {#list-with-section-footer}

```swift
List {
    Section {
        ForEach(pokedex) { pokemon in ... }
    } footer: {
        if pokedex.count < 151 {
            ContentUnavailableView { ... }
        }
    }
}
```

## Pièges courants {#gotchas}

- `ForEach` n'accepte que les intervalles semi-ouverts (`0..<5`), pas les intervalles fermés (`0...4`)
- `id: \.self` fonctionne lorsque les valeurs sont uniques ; des valeurs dupliquées entraînent un comportement indéfini
- `List` fournit automatiquement un comportement semblable à `Identifiable`, mais les types de modèle doivent tout de même le implémenter explicitement
- Lors d'un filtrage, filtrez toujours à partir de la liste principale d'origine, et non à partir d'une copie déjà filtrée
- `LazyVGrid` rend les cellules de manière paresseuse (uniquement lorsqu'elles sont visibles) : c'est avantageux pour les performances avec de grands jeux de données
- `ScrollView` occupe par défaut tout l'espace disponible, contrairement à `VStack` qui n'utilise que l'espace nécessaire
- `.onDelete` ne fonctionne qu'avec `ForEach` à l'intérieur d'une `List`, et non directement avec `List(items)`

## Voir aussi {#see-also}

- [[swiftui-navigation]] - NavigationLink dans les lignes de List
- [[swiftui-views-and-modifiers]] - référence des modificateurs pour la mise en forme du contenu des listes
- [[swiftui-forms-and-input]] - Form comme conteneur spécialisé de type liste
- [[swiftdata-persistence]] - @Query pour alimenter les listes depuis la base de données
