---
title: "Concepts et contraintes en C++20"
description: "Exigences nommées sur les paramètres de template, remplaçant la SFINAE par des contraintes lisibles et vérifiées par le compilateur"
level: 3
source_sha256: 4ed180313d9aa555aa24173e0c6b4c22f59bb00783db110088c4c57c20905d6a
translation: machine
translated_at: '2026-10-24'
---
# Concepts et contraintes en C++20 {#c20-concepts-and-constraints}

Les concepts sont des ensembles nommés d'exigences portant sur les paramètres de template. Ils remplacent la SFINAE et les artifices `enable_if` par des contraintes lisibles, vérifiées par le compilateur, qui produisent des messages d'erreur clairs.

## Le problème que résolvent les concepts {#the-problem-concepts-solve}

Avant C++20, les erreurs de template étaient réputées très mauvaises. Si l'on passait un type incompatible à un template, le compilateur produisait des pages d'erreurs au cœur de l'implémentation du template. L'utilisateur n'avait aucun moyen de savoir ce que le template exigeait réellement sans lire son implémentation.

Les concepts font passer les exigences de « implicites dans l'implémentation » à « explicites dans la déclaration ».

## Utiliser les concepts standard {#using-standard-concepts}

Le header `<concepts>` fournit des concepts standard :

```cpp
#include <concepts>

// Constrained function template: T must be integral
template <std::integral T>
T double_it(T value) {
    return value * 2;
}

double_it(42);      // OK: int is integral
double_it(3.14);    // Compile error: double is not integral
// Error message: "constraints not satisfied" - clear and short
```

Concepts standard courants :

| Concept | Signification |
|---------|---------------|
| `std::integral` | Types entiers (int, long, char, etc.) |
| `std::floating_point` | float, double, long double |
| `std::signed_integral` | Types entiers signés |
| `std::unsigned_integral` | Types entiers non signés |
| `std::same_as<T, U>` | T et U sont le même type |
| `std::convertible_to<From, To>` | From se convertit implicitement en To |
| `std::derived_from<Derived, Base>` | Relation d'héritage |
| `std::equality_comparable` | Supporte == et != |
| `std::totally_ordered` | Supporte <, >, <=, >= |
| `std::movable` | Constructible par déplacement et assignable |
| `std::copyable` | Constructible par copie et assignable |

## Formes de syntaxe {#syntax-forms}

Trois façons équivalentes de contraindre un template :

```cpp
// 1. Requires clause
template <typename T>
    requires std::integral<T>
T add(T a, T b) { return a + b; }

// 2. Constrained template parameter
template <std::integral T>
T add(T a, T b) { return a + b; }

// 3. Trailing requires clause
template <typename T>
T add(T a, T b) requires std::integral<T> { return a + b; }
```

## Écrire des concepts personnalisés {#writing-custom-concepts}

Les concepts personnalisés combinent des concepts existants et des exigences ad hoc :

```cpp
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <typename T>
concept Printable = requires(T t) {
    { std::cout << t } -> std::same_as<std::ostream&>;
};

template <typename T>
concept Hashable = requires(T t) {
    { std::hash<T>{}(t) } -> std::convertible_to<std::size_t>;
};

// Combine multiple concepts
template <typename T>
concept PrintableNumeric = Numeric<T> && Printable<T>;
```

## Bénéfices pour les utilisateurs de templates {#benefits-for-template-users}

Avec les concepts, la déclaration d'un template suffit à tout expliquer :

```cpp
template <std::totally_ordered T>
T find_max(std::vector<T>& v);
// Reading this, you know: T must support comparison operators
// Look up std::totally_ordered on cppreference for details
```

Sans concepts (avant C++20) :
```cpp
template <typename T>
T find_max(std::vector<T>& v);
// What does T need to support? Must read implementation to find out.
```

## Bénéfices pour les auteurs de templates {#benefits-for-template-writers}

- L'autocomplétion de l'IDE sait quelles opérations sont disponibles selon le concept
- L'usage accidentel d'opérations absentes du concept est détecté au moment de la définition, et non de l'instanciation
- La résolution de surcharge peut utiliser les concepts pour sélectionner la surcharge la plus appropriée

## Stratégie d'adoption {#adoption-strategy}

1. Commencer par **utiliser** les concepts standard existants pour contraindre vos templates
2. Essayer ensuite de **combiner** les concepts existants avec `&&` et `||`
3. Ne **écrire des concepts personnalisés** que lorsque les concepts standard ne couvrent pas vos besoins
4. Écrire un concept personnalisé ne doit jamais être la première étape

## Pièges à éviter {#gotchas}

- **Les concepts ne restreignent pas l'implémentation.** Un concept dit « T doit supporter X », mais le corps du template peut toujours utiliser des opérations au-delà de ce qu'exige le concept. Le concept contraint les types qui peuvent être passés en argument, et non ce que le template fait avec eux.
- **Les règles de subsomption des concepts sont subtiles.** Lorsque deux surcharges ont des concepts différents, le compilateur choisit la « plus contrainte ». Les règles déterminant quel concept est « plus spécifique » peuvent ne pas être évidentes.
- **Les concepts standard se trouvent dans différents headers.** Tous les concepts ne sont pas dans `<concepts>` : certains se trouvent dans `<ranges>`, `<iterator>`, `<functional>`. Consultez cppreference pour connaître le bon include.
- **Le support par les compilateurs varie.** Les compilateurs plus anciens ou certains options de compilation peuvent ne pas supporter tous les concepts de C++20. Testez avec le compilateur cible.

## Références croisées {#cross-references}

- [[templates-and-concepts]] - fondements de la programmation générique
- [[modern-cpp-features]] - autres fonctionnalités de C++20
- [Gestion des erreurs - Exceptions et alternatives](error-handling.md) - les concepts améliorent les diagnostics d'erreur des templates
