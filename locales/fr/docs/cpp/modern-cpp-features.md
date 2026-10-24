---
title: "Fonctionnalités modernes de C++ (C++17/20/23)"
category: concepts
tags: [cpp, cpp17, cpp20, cpp23, structured-bindings, optional, variant, ranges, modules, coroutines]
level: 3
source_sha256: 1ab0b1e015abbd0b12f6f78ab1ff62d660ca528755a6f46e23c6449532ee2701
translation: machine
translated_at: '2026-10-24'
---
# Fonctionnalités modernes de C++ (C++17/20/23) {#modern-c-features-c172023}

Principales fonctionnalités des normes récentes qui changent la manière d'écrire du C++. L'accent est mis sur les ajouts les plus importants.

## Points clés - C++17 {#key-facts-c17}

- Liaisons structurées : `auto [key, value] = pair;`
- `std::optional<T>`, `std::variant<Ts...>`, `std::any`
- `if constexpr` - branchement à la compilation dans les templates
- Déduction des arguments de modèle de classe (CTAD) : `std::vector v{1,2,3};`
- `std::string_view` - référence de chaîne non propriétaire
- `<filesystem>` - opérations portables sur le système de fichiers
- Expressions de pliage : `(args + ...)`
- Espaces de noms imbriqués : `namespace A::B::C {}`
- Attributs `[[nodiscard]]`, `[[maybe_unused]]`, `[[fallthrough]]`
- `std::invoke` - invocation uniforme d'objets appelables

## Points clés - C++20 {#key-facts-c20}

- Concepts et contraintes
- Ranges et vues (`<ranges>`)
- Coroutines (`co_await`, `co_yield`, `co_return`)
- Modules (`import`, `export module`)
- `std::format` - formatage type-safe
- Opérateur de comparaison à trois voies `<=>`
- `std::span<T>` - vue contiguë non propriétaire
- `std::jthread` - thread à jointure automatique avec jeton d'arrêt
- `consteval`, `constinit`
- Expressions et clauses `requires`

## Points clés - C++23 {#key-facts-c23}

- `std::expected<T,E>` - valeur ou erreur
- `std::print` / `std::println` - sortie formatée
- `std::mdspan` - vue sur tableau multidimensionnel
- Déduction de `this` - paramètre d'objet explicite
- `std::generator` - générateur de coroutine synchrone
- `if consteval` - test de l'évaluation à la compilation
- `std::flat_map` / `std::flat_set` - conteneurs basés sur des vecteurs triés
- `std::stacktrace` - traces de pile programmatiques

## Schémas d'utilisation {#patterns}

### Liaisons structurées (C++17) {#structured-bindings-c17}

```cpp
// With pairs/tuples
auto [min_it, max_it] = std::minmax_element(v.begin(), v.end());

// With maps
std::map<std::string, int> scores;
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << '\n';
}

// With custom structs (public members or structured binding support)
struct Result { bool ok; std::string message; };
auto [ok, msg] = get_result();
if (ok) process(msg);

// With arrays
int arr[] = {1, 2, 3};
auto [a, b, c] = arr;
```

### std::variant et std::visit (C++17) {#stdvariant-and-stdvisit-c17}

```cpp
using Value = std::variant<int, double, std::string>;

Value v = 42;
v = "hello"s;

// Visit with overloaded lambdas
template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

auto result = std::visit(overloaded{
    [](int i)              { return std::to_string(i); },
    [](double d)           { return std::to_string(d); },
    [](const std::string& s) { return s; }
}, v);

// Check which type is active
if (std::holds_alternative<int>(v)) {
    int i = std::get<int>(v);
}

// Safe get
if (auto* p = std::get_if<std::string>(&v)) {
    process(*p);
}
```

### Ranges et vues (C++20) {#ranges-and-views-c20}

```cpp
#include <ranges>
namespace rv = std::views;

std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Pipeline
auto evens_squared = nums
    | rv::filter([](int n) { return n % 2 == 0; })
    | rv::transform([](int n) { return n * n; });

// Lazy evaluation - nothing computed until iterated
for (int n : evens_squared) { std::cout << n << ' '; }  // 4 16 36 64 100

// Range factories
for (int i : rv::iota(1, 11)) { /* 1..10 */ }
for (int i : rv::iota(0) | rv::take(5)) { /* 0..4 */ }

// String processing
std::string csv = "a,b,c,d";
for (auto word : csv | rv::split(',')) {
    // process each word
}
```

### std::span (C++20) {#stdspan-c20}

```cpp
#include <span>

// Non-owning view of contiguous data - replaces (T*, size_t) pairs
void process(std::span<const int> data) {
    for (int x : data) { /* ... */ }
    auto first3 = data.subspan(0, 3);
    auto last2 = data.last(2);
}

// Works with any contiguous container
std::vector<int> vec = {1, 2, 3};
std::array<int, 5> arr = {1, 2, 3, 4, 5};
int c_arr[] = {1, 2, 3, 4};

process(vec);
process(arr);
process(c_arr);
process({vec.data() + 1, 3});  // subview
```

### Déduction de this (C++23) {#deducing-this-c23}

```cpp
struct Widget {
    // Single implementation for const and non-const
    template<typename Self>
    auto&& value(this Self&& self) {
        return std::forward<Self>(self).value_;
    }

    // Recursive lambda (see also lambda-expressions)
    auto get_children(this const Widget& self) -> std::vector<Widget> {
        // can recurse: self.get_children()
    }

private:
    int value_;
};
```

### Modules (C++20) {#modules-c20}

```cpp
// mylib.cppm (module interface)
export module mylib;

export class Widget {
public:
    Widget(int val);
    int value() const;
private:
    int val_;
};

export int compute(int x);

// mylib.cpp (module implementation)
module mylib;

Widget::Widget(int val) : val_(val) {}
int Widget::value() const { return val_; }
int compute(int x) { return x * x; }

// main.cpp
import mylib;

int main() {
    Widget w(42);
    return compute(w.value());
}
```

## Pièges courants {#gotchas}

- **Problème :** `std::variant` construit par défaut sa première alternative - échoue si le premier type n'a pas de constructeur par défaut -> **Solution :** Placer en premier un type constructible par défaut, ou utiliser `std::monostate` comme premier type
- **Problème :** Les vues de ranges conservent des références vers la source - elles deviennent invalides si la source est temporaire -> **Solution :** Matérialiser les vues dans des conteneurs avant la destruction de la source. Ne pas renvoyer de vues sur des données locales.
- **Problème :** Le support des modules varie selon les compilateurs (partiel dans GCC/Clang en 2025) -> **Solution :** Consulter la matrice de support des compilateurs. Utiliser les headers en solution de repli, encapsulés dans un `#include`.
- **Problème :** `std::span` ne possède pas les données - mêmes risques d'invalidation que les pointeurs -> **Solution :** S'assurer que la source survit au span. Ne jamais renvoyer un span vers un conteneur local.

## Voir aussi {#see-also}

- [[stl-algorithms]]
- [[templates-and-concepts]]
- [[lambda-expressions]]
- [Gestion des erreurs - Exceptions et alternatives](error-handling.md)
- [[string-handling]]
