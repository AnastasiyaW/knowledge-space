---
title: "Moderne C++-Features (C++17/20/23)"
category: concepts
tags: [cpp, cpp17, cpp20, cpp23, structured-bindings, optional, variant, ranges, modules, coroutines]
level: 3
source_sha256: 1ab0b1e015abbd0b12f6f78ab1ff62d660ca528755a6f46e23c6449532ee2701
translation: machine
translated_at: '2026-10-24'
---
# Moderne C++-Features (C++17/20/23) {#modern-c-features-c172023}

Wichtige Neuerungen aus aktuellen Standards, die die Art verändern, wie C++ geschrieben wird. Der Fokus liegt auf den wirkungsvollsten Ergänzungen.

## Kernfakten - C++17 {#key-facts-c17}

- Structured Bindings: `auto [key, value] = pair;`
- `std::optional<T>`, `std::variant<Ts...>`, `std::any`
- `if constexpr` - Verzweigung zur Kompilierzeit in Templates
- Class Template Argument Deduction (CTAD): `std::vector v{1,2,3};`
- `std::string_view` - nicht besitzende Referenz auf einen String
- `<filesystem>` - portable Dateisystemoperationen
- Fold-Expressions: `(args + ...)`
- Verschachtelte Namespaces: `namespace A::B::C {}`
- `[[nodiscard]]`, `[[maybe_unused]]`, `[[fallthrough]]`-Attribute
- `std::invoke` - einheitlicher Aufruf von Callables

## Kernfakten - C++20 {#key-facts-c20}

- Concepts und Constraints
- Ranges und Views (`<ranges>`)
- Coroutines (`co_await`, `co_yield`, `co_return`)
- Modules (`import`, `export module`)
- `std::format` - typsichere Formatierung
- `<=>`-Spaceship-Operator
- `std::span<T>` - nicht besitzende, zusammenhängende Sicht auf Daten
- `std::jthread` - automatisch joinender Thread mit Stop-Token
- `consteval`, `constinit`
- `requires`-Ausdrücke und -Klauseln

## Kernfakten - C++23 {#key-facts-c23}

- `std::expected<T,E>` - Wert oder Fehler
- `std::print` / `std::println` - formatierte Ausgabe
- `std::mdspan` - Sicht auf mehrdimensionale Arrays
- Deducing `this` - expliziter Objektparameter
- `std::generator` - synchroner Coroutine-Generator
- `if consteval` - prüft, ob in einer konstanten Auswertung gearbeitet wird
- `std::flat_map` / `std::flat_set` - sortierte, vektorbasierte Container
- `std::stacktrace` - programmatische Stack-Traces

## Muster {#patterns}

### Structured Bindings (C++17) {#structured-bindings-c17}

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

### std::variant und std::visit (C++17) {#stdvariant-and-stdvisit-c17}

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

### Ranges und Views (C++20) {#ranges-and-views-c20}

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

### Deducing this (C++23) {#deducing-this-c23}

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

## Fallstricke {#gotchas}

- **Problem:** `std::variant` default-konstruiert die erste Alternative - schlägt fehl, wenn der erste Typ keinen Default-Konstruktor hat -> **Lösung:** Einen standardmäßig konstruierbaren Typ voranstellen oder `std::monostate` als ersten Typ verwenden
- **Problem:** Ranges-Views halten Referenzen auf die Quelle - hängen ins Leere, wenn die Quelle ein temporäres Objekt ist -> **Lösung:** Views vor der Zerstörung der Quelle in Container materialisieren. Keine Views auf lokale Daten zurückgeben.
- **Problem:** Die Unterstützung für Modules variiert zwischen den Compilern (Stand 2025 teilweise in GCC/Clang) -> **Lösung:** Die Compiler-Support-Matrix prüfen. Als Fallback Header mit einem `#include`-Wrapper verwenden.
- **Problem:** `std::span` besitzt die Daten nicht - dieselben Dangling-Risiken wie bei Zeigern -> **Lösung:** Sicherstellen, dass die Quelle den Span überdauert. Niemals einen Span auf einen lokalen Container zurückgeben.

## Siehe auch {#see-also}

- [[stl-algorithms]]
- [[templates-and-concepts]]
- [[lambda-expressions]]
- [Fehlerbehandlung - Exceptions und Alternativen](error-handling.md)
- [[string-handling]]
