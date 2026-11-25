---
title: "Const-Korrektheit und Typsicherheit"
category: concepts
tags: [cpp, const, constexpr, type-safety, auto, casting]
level: 3
source_sha256: e2f2a4507c14ef466e7bf62e38ec506e8dbe290545a042c4f64a19aacc9092ea
translation: machine
translated_at: '2026-10-24'
---
# Const-Korrektheit und Typsicherheit {#const-correctness-and-type-safety}

`const` drückt die Absicht aus, verhindert versehentliche Änderungen und ermöglicht Compileroptimierungen. Moderne C++-Typsicherheit eliminiert ganze Fehlerkategorien.

## Wichtige Fakten {#key-facts}

- `const int* p` = Zeiger auf const int (über p kann nicht verändert werden, p kann neu zugewiesen werden)
- `int* const p` = const-Zeiger auf int (über p kann verändert werden, p kann nicht neu zugewiesen werden)
- `const int* const p` = const-Zeiger auf const int
- Deklarationen von rechts nach links lesen: `int const* p` = „p ist ein Zeiger auf const int“
- `const`-Memberfunktion: `void foo() const` - verspricht, den Objektzustand nicht zu verändern
- `mutable`-Member: kann auch im const-Kontext verändert werden (Caches, Mutexe)
- `constexpr` (C++11): wird nach Möglichkeit zur Compilezeit ausgewertet; `consteval` (C++20): muss zur Compilezeit ausgewertet werden
- `auto` leitet den Typ aus dem Initialisierer ab - entfernt das oberste `const` und Referenzen
- `decltype(expr)` leitet den Typ ab und erhält dabei die Qualifizierer
- C++-Casts: `static_cast`, `dynamic_cast`, `const_cast`, `reinterpret_cast`
- `static_cast` für sichere Konvertierungen; `dynamic_cast` für zur Laufzeit geprüfte Downcasts
- `const_cast` zum Entfernen von const - nur sicher, wenn das ursprüngliche Objekt nicht const war
- `std::string_view` (C++17): nicht besitzende Sicht, ersetzt `const std::string&`-Parameter

## Muster {#patterns}

### Const-Korrektheit {#const-correctness}

```cpp
class Matrix {
    std::vector<double> data_;
    size_t rows_, cols_;
public:
    // const accessor - can call on const Matrix
    double at(size_t r, size_t c) const {
        return data_[r * cols_ + c];
    }

    // non-const accessor - modifiable
    double& at(size_t r, size_t c) {
        return data_[r * cols_ + c];
    }

    // const-qualified getters
    size_t rows() const { return rows_; }
    size_t cols() const { return cols_; }

    // mutable for caching
    mutable std::optional<double> cached_det_;
    double determinant() const {
        if (!cached_det_) {
            cached_det_ = compute_determinant();
        }
        return *cached_det_;
    }
};

// Function parameter const correctness
void process(const Matrix& m);       // won't modify m
void transform(Matrix& m);           // may modify m
void consume(Matrix m);              // takes copy
```

### constexpr {#constexpr}

```cpp
// Compile-time function
constexpr int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

constexpr int f5 = factorial(5);  // computed at compile time
static_assert(f5 == 120);

// constexpr class
class Point {
    double x_, y_;
public:
    constexpr Point(double x, double y) : x_(x), y_(y) {}
    constexpr double distance_sq(Point other) const {
        double dx = x_ - other.x_;
        double dy = y_ - other.y_;
        return dx*dx + dy*dy;
    }
};

constexpr Point p1(0, 0), p2(3, 4);
constexpr double d = p1.distance_sq(p2);  // 25.0 at compile time

// C++20: consteval - MUST be compile-time
consteval int must_be_compiletime(int x) { return x * x; }

// C++20: constinit - compile-time initialization, runtime mutability
constinit int global = factorial(5);  // init at compile time
```

### auto und decltype {#auto-and-decltype}

```cpp
// auto deduction
auto x = 42;                  // int
auto& r = x;                  // int&
const auto& cr = x;           // const int&
auto* p = &x;                 // int*

// auto with containers
std::map<std::string, std::vector<int>> data;
for (const auto& [key, values] : data) {   // structured bindings C++17
    for (auto val : values) { /* ... */ }
}

// decltype preserves qualifiers
int i = 0;
decltype(i) j = i;            // int
decltype((i)) k = i;          // int& (expression in parens = lvalue)

// Trailing return type
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}
```

### Sicheres Casting {#safe-casting}

```cpp
// static_cast: compile-time checked, common conversions
double d = 3.14;
int i = static_cast<int>(d);              // 3, explicit truncation
Base* bp = static_cast<Base*>(derived_ptr); // upcast (always safe)

// dynamic_cast: runtime-checked downcast (needs RTTI + virtual)
if (auto* dp = dynamic_cast<Derived*>(base_ptr)) {
    dp->derived_method();
}

// const_cast: remove const (danger zone)
void legacy_api(char* s);
const char* str = "hello";
legacy_api(const_cast<char*>(str));  // OK only if legacy_api doesn't write

// reinterpret_cast: type punning (last resort)
uintptr_t addr = reinterpret_cast<uintptr_t>(ptr);
```

### string_view (C++17) {#string_view-c17}

```cpp
// Efficient string parameter - no allocation
void process(std::string_view sv) {
    // sv.data(), sv.size(), sv.substr(), sv.find()
    // Supports string literals, std::string, char*, with/without length
}

process("hello");           // no allocation
process(std::string("hi")); // no copy
process(sv.substr(1, 3));   // no allocation (just pointer + length)
```

## Fallstricke {#gotchas}

- **Problem:** `auto` entfernt const- und Referenzqualifizierer -> **Lösung:** `const auto&` verwenden, wenn eine const-Referenz gewünscht ist
- **Problem:** `string_view` kann ins Leere zeigen (dangling), wenn der zugrunde liegende String zerstört wird -> **Lösung:** Ein `string_view` niemals länger speichern, als die Quelle des Strings existiert. Kein `string_view` auf eine lokale Variable zurückgeben.
- **Problem:** `const_cast` auf ein tatsächlich const-Objekt mit anschließendem Schreibzugriff = UB -> **Lösung:** `const_cast` nur verwenden, wenn bekannt ist, dass das ursprüngliche Objekt nicht const ist
- **Problem:** `constexpr`-Funktion wird nicht zur Compilezeit ausgewertet, wenn die Argumente Laufzeitwerte sind -> **Lösung:** `consteval` (C++20) verwenden, wenn eine garantierte Auswertung zur Compilezeit nötig ist

## Siehe auch {#see-also}

- [[templates-and-concepts]]
- [[string-handling]]
- [Performance Optimization](performance-optimization.md)
- [cppreference: const](https://en.cppreference.com/w/cpp/language/cv)
