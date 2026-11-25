---
title: "Exactitude de const et sûreté de type"
category: concepts
tags: [cpp, const, constexpr, type-safety, auto, casting]
level: 3
source_sha256: e2f2a4507c14ef466e7bf62e38ec506e8dbe290545a042c4f64a19aacc9092ea
translation: machine
translated_at: '2026-10-24'
---
# Exactitude de const et sûreté de type {#const-correctness-and-type-safety}

`const` exprime l'intention, empêche les modifications accidentelles et permet des optimisations du compilateur. La sûreté de type du C++ moderne élimine des catégories entières de bugs.

## Points clés {#key-facts}

- `const int* p` = pointeur vers un int constant (impossible de modifier via p, mais p peut être réaffecté)
- `int* const p` = pointeur constant vers un int (modification possible via p, mais p ne peut pas être réaffecté)
- `const int* const p` = pointeur constant vers un int constant
- Lire les déclarations de droite à gauche : `int const* p` = « p est un pointeur vers un int constant »
- Fonction membre `const` : `void foo() const` - s'engage à ne pas modifier l'état de l'objet
- Membre `mutable` : peut être modifié même dans un contexte `const` (caches, mutex)
- `constexpr` (C++11) : évalué à la compilation si possible ; `consteval` (C++20) : doit être évalué à la compilation
- `auto` déduit le type à partir de l'initialisation - supprime le `const` de premier niveau et les références
- `decltype(expr)` déduit le type en conservant les qualificateurs
- Casts C++ : `static_cast`, `dynamic_cast`, `const_cast`, `reinterpret_cast`
- `static_cast` pour les conversions sûres ; `dynamic_cast` pour un downcast vérifié à l'exécution
- `const_cast` pour retirer le `const` - sûr uniquement si l'objet d'origine n'était pas `const`
- `std::string_view` (C++17) : vue non propriétaire, remplace les paramètres `const std::string&`

## Motifs {#patterns}

### Exactitude de const {#const-correctness}

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

### auto et decltype {#auto-and-decltype}

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

### Conversions de type sûres {#safe-casting}

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

## Pièges {#gotchas}

- **Problème :** `auto` supprime les qualificateurs `const` et de référence -> **Correction :** Utiliser `const auto&` lorsqu'on veut une référence constante
- **Problème :** `string_view` peut devenir un pointeur pendant (dangling) si la chaîne sous-jacente est détruite -> **Correction :** Ne jamais conserver un `string_view` au-delà de la durée de vie de la chaîne source. Ne pas retourner de `string_view` vers une variable locale.
- **Problème :** `const_cast` sur un objet réellement `const` suivi d'une écriture = comportement indéfini (UB) -> **Correction :** Utiliser `const_cast` uniquement lorsqu'on sait que l'objet d'origine n'est pas `const`
- **Problème :** une fonction `constexpr` n'est pas évaluée à la compilation lorsque ses arguments sont des valeurs d'exécution -> **Correction :** Utiliser `consteval` (C++20) si une évaluation garantie à la compilation est nécessaire

## Voir aussi {#see-also}

- [[templates-and-concepts]]
- [[string-handling]]
- [Optimisation des performances](performance-optimization.md)
- [cppreference : const](https://en.cppreference.com/w/cpp/language/cv)
