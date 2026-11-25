---
title: "C++20-Konzepte und Constraints"
description: "Benannte Anforderungen an Template-Parameter, die SFINAE durch lesbare, vom Compiler erzwungene Constraints ersetzen"
level: 3
source_sha256: 4ed180313d9aa555aa24173e0c6b4c22f59bb00783db110088c4c57c20905d6a
translation: machine
translated_at: '2026-10-24'
---
# C++20-Konzepte und Constraints {#c20-concepts-and-constraints}

Konzepte sind benannte Mengen von Anforderungen an Template-Parameter. Sie ersetzen SFINAE- und `enable_if`-Konstrukte durch lesbare, vom Compiler erzwungene Constraints, die klare Fehlermeldungen erzeugen.

## Das Problem, das Konzepte lösen {#the-problem-concepts-solve}

Vor C++20 waren Template-Fehlermeldungen berüchtigt schlecht. Wurde einem Template ein inkompatibler Typ übergeben, erzeugte der Compiler seitenweise Fehler tief in der Template-Implementierung. Der Anwender hatte keine Möglichkeit zu erfahren, was das Template tatsächlich voraussetzt, ohne die Implementierung zu lesen.

Konzepte verschieben Anforderungen von „implizit in der Implementierung“ zu „explizit in der Deklaration“.

## Standardkonzepte verwenden {#using-standard-concepts}

Der Header `<concepts>` stellt Standardkonzepte bereit:

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

Gängige Standardkonzepte:

| Konzept | Bedeutung |
|---------|-----------|
| `std::integral` | Ganzzahlige Typen (int, long, char usw.) |
| `std::floating_point` | float, double, long double |
| `std::signed_integral` | Vorzeichenbehaftete Ganzzahltypen |
| `std::unsigned_integral` | Vorzeichenlose Ganzzahltypen |
| `std::same_as<T, U>` | T und U sind derselbe Typ |
| `std::convertible_to<From, To>` | From wird implizit nach To konvertiert |
| `std::derived_from<Derived, Base>` | Vererbungsbeziehung |
| `std::equality_comparable` | Unterstützt == und != |
| `std::totally_ordered` | Unterstützt <, >, <=, >= |
| `std::movable` | Move-konstruierbar und move-zuweisbar |
| `std::copyable` | Copy-konstruierbar und copy-zuweisbar |

## Syntaxformen {#syntax-forms}

Drei gleichwertige Möglichkeiten, ein Template zu constrainen:

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

## Eigene Konzepte schreiben {#writing-custom-concepts}

Eigene Konzepte kombinieren bestehende Konzepte und ad-hoc-Anforderungen:

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

## Nutzen für Template-Anwender {#benefits-for-template-users}

Mit Konzepten verrät die Template-Deklaration alles Wesentliche:

```cpp
template <std::totally_ordered T>
T find_max(std::vector<T>& v);
// Reading this, you know: T must support comparison operators
// Look up std::totally_ordered on cppreference for details
```

Ohne Konzepte (vor C++20):
```cpp
template <typename T>
T find_max(std::vector<T>& v);
// What does T need to support? Must read implementation to find out.
```

## Nutzen für Template-Autoren {#benefits-for-template-writers}

- IDE-Autovervollständigung kennt die verfügbaren Operationen anhand des Konzepts
- Versehentliche Verwendung von Operationen, die nicht im Konzept enthalten sind, wird zur Definitionszeit statt zur Instanziierungszeit erkannt
- Überladungsauflösung kann Konzepte nutzen, um die passendste Überladung auszuwählen

## Einführungsstrategie {#adoption-strategy}

1. Beginnen Sie damit, **bestehende Standardkonzepte** zur Constraint-Formulierung Ihrer Templates zu **verwenden**
2. Kombinieren Sie danach bestehende Konzepte mit `&&` und `||`
3. **Schreiben Sie eigene Konzepte** nur dann, wenn die Standardkonzepte Ihre Anforderungen nicht abdecken
4. Das Schreiben eines eigenen Konzepts sollte niemals der erste Schritt sein

## Fallstricke {#gotchas}

- **Konzepte beschränken nicht die Implementierung.** Ein Konzept besagt „T muss X unterstützen“, aber der Template-Rumpf kann dennoch Operationen verwenden, die über das hinausgehen, was das Konzept verlangt. Das Konzept beschränkt, welche Typen übergeben werden können, nicht, was das Template mit ihnen tut.
- **Die Regeln zur Konzept-Subsumption sind subtil.** Wenn zwei Überladungen unterschiedliche Konzepte haben, wählt der Compiler die „most constrained“-Überladung. Die Regeln, welches Konzept als „spezifischer“ gilt, können unintuitiv sein.
- **Standardkonzepte liegen in verschiedenen Headern.** Nicht alle Konzepte stammen aus `<concepts>` – einige befinden sich in `<ranges>`, `<iterator>` oder `<functional>`. Die passende Include-Datei finden Sie auf cppreference.
- **Die Compiler-Unterstützung variiert.** Ältere Compiler oder bestimmte Flags unterstützen möglicherweise nicht alle C++20-Konzepte. Testen Sie mit Ihrem Ziel-Compiler.

## Querverweise {#cross-references}

- [[templates-and-concepts]] - Grundlagen der generischen Programmierung
- [[modern-cpp-features]] - weitere C++20-Funktionen
- [Fehlerbehandlung - Exceptions und Alternativen](error-handling.md) - Konzepte verbessern die Diagnose von Template-Fehlern
