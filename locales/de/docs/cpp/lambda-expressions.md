---
title: "Lambda-Ausdrücke"
category: concepts
tags: [cpp, lambda, closures, functional, cpp11, cpp14, cpp20]
level: 4
source_sha256: 0cd923aebac4f40ff1aa03f84d3a407fdfd56555118a50bf288ef9a59454c976
translation: machine
translated_at: '2026-10-24'
---
# Lambda-Ausdrücke {#lambda-expressions}

Anonyme Funktionsobjekte mit Capture-Semantik. Zentrales Werkzeug für Callbacks, Algorithmen und funktionale Muster.

## Key Facts {#key-facts}

- Syntax: `[capture](params) -> return_type { body }`
- `[=]` erfasst alle lokalen Variablen per Wert, `[&]` erfasst alle per Referenz
- `[x]` Erfassung per Wert, `[&x]` Erfassung per Referenz, `[x = std::move(y)]` Init-Capture (C++14)
- Lambdas sind syntaktischer Zucker für vom Compiler erzeugte Closure-Typen (unbenannte `struct` mit `operator()`)
- Jede Lambda hat einen eindeutigen Typ – zum Speichern `std::function<>` oder `auto` verwenden
- `auto`-Parameter in Lambdas (C++14) ergeben generische/polymorphe Lambdas
- Das Schlüsselwort `mutable` erlaubt das Ändern von per Wert erfassten Variablen
- `constexpr`-Lambdas (C++17) – verwendbar in Kontexten zur Compile-Zeit
- Template-Lambdas (C++20): `[]<typename T>(T x) { ... }`
- Lambdas ohne Capture können in einen Funktionszeiger konvertiert werden
- Lambda bevorzugen gegenüber `std::bind` – klarer, effizienter, besser optimiert

## Patterns {#patterns}

### Capture-Modi {#capture-modes}

```cpp
int x = 10;
std::string name = "test";

auto by_val   = [x]() { return x; };            // copy of x
auto by_ref   = [&x]() { return x; };           // reference to x
auto all_val  = [=]() { return x + name.size(); }; // all by value
auto all_ref  = [&]() { x++; };                 // all by reference
auto mixed    = [&x, name]() { x += name.size(); }; // mix

// Init capture (C++14) - move into lambda
auto moved = [s = std::move(name)]() { return s.size(); };

// Capture this
struct Widget {
    int value_ = 42;
    auto get_printer() {
        return [this]() { std::cout << value_; };     // captures this ptr
        // return [*this]() { std::cout << value_; };  // C++17: copies *this
    }
};
```

### Generische Lambdas {#generic-lambdas}

```cpp
// C++14: auto parameters
auto add = [](auto a, auto b) { return a + b; };
add(1, 2);       // int
add(1.5, 2.5);   // double
add("a"s, "b"s); // string

// C++20: template syntax for constraints
auto print = []<typename T>(const std::vector<T>& v) {
    for (const auto& x : v) std::cout << x << ' ';
};
```

### Mit STL-Algorithmen {#with-stl-algorithms}

```cpp
std::vector<int> v = {5, 3, 1, 4, 2};

// Sort with custom comparator
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });

// Find first matching
auto it = std::find_if(v.begin(), v.end(), [](int x) { return x > 3; });

// Transform
std::vector<std::string> result;
std::transform(v.begin(), v.end(), std::back_inserter(result),
    [](int x) { return std::to_string(x); });

// Accumulate with lambda
auto product = std::accumulate(v.begin(), v.end(), 1,
    [](int acc, int x) { return acc * x; });
```

### Sofort aufgerufene Lambda (IIFE) {#immediately-invoked-lambda-iife}

```cpp
// Complex initialization
const auto config = [&] {
    Config c;
    c.width = parse_int(args[1]);
    c.height = parse_int(args[2]);
    c.title = args[3];
    return c;
}();  // note: immediately invoked

// Conditional const initialization
const int value = [&] {
    if (mode == Mode::Fast) return compute_fast();
    else return compute_accurate();
}();
```

### Rekursive Lambda {#recursive-lambda}

```cpp
// C++23: deducing this for recursion
auto fib = [](this auto self, int n) -> int {
    if (n <= 1) return n;
    return self(n-1) + self(n-2);
};

// Pre-C++23: use std::function
std::function<int(int)> fib = [&fib](int n) -> int {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
};
```

## Gotchas {#gotchas}

- **Issue:** Lokale Variable per Referenz erfasst, Lambda überlebt die Variable -> hängende Referenz, UB -> **Fix:** Per Wert erfassen, oder Init-Capture verwenden, um den Besitz in die Lambda zu verschieben
- **Issue:** `[=]` erfasst den `this`-Zeiger per Wert (den Zeiger, nicht das Objekt) -> weiterhin hängend, wenn das Objekt zerstört wurde -> **Fix:** `[*this]` (C++17) verwenden, um eine Kopie des Objekts zu erfassen, oder die Lebensdauer sicherstellen
- **Issue:** `std::function<>` hat Overhead (Type Erasure, Heap-Allokation) -> **Fix:** Wenn möglich `auto` verwenden; `std::function` nur, wenn typ-gelöschte Speicherung nötig ist
- **Issue:** Lambda, das eine per Wert erfasste Variable ändert, kompiliert nicht -> **Fix:** `mutable` ergänzen: `[x]() mutable { x++; }`

## See Also {#see-also}

- [[stl-algorithms]]
- [[templates-and-concepts]]
- [[move-semantics]]
- [cppreference: Lambda](https://en.cppreference.com/w/cpp/language/lambda)
