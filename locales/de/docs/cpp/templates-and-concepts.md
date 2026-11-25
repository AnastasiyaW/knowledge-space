---
title: "Templates und Concepts"
category: concepts
tags: [cpp, templates, concepts, generic, metaprogramming, cpp20]
level: 3
source_sha256: 79fa6d4cd9ee28575c2e8ca643b2738fc718396d9f2ba3c3c82cb6b71d0559ac
translation: machine
translated_at: '2026-10-24'
---
# Templates und Concepts {#templates-and-concepts}

Generische Programmierung durch Parametrisierung von Typen zur Kompilierzeit. Concepts (C++20) beschränken Templates mit lesbaren Anforderungen.

## Wichtige Fakten {#key-facts}

- Funktionstemplates: Der Compiler erzeugt Code für jede verwendete Typinstanziierung
- Klassentemplates: Parametrisieren ganze Klassen über Typen bzw. Werte
- Die Template-Instanziierung erfolgt zur Kompilierzeit, ohne Laufzeitaufwand
- SFINAE (Substitution Failure Is Not An Error): Eine fehlgeschlagene Substitution entfernt die Überladung aus der Kandidatenmenge
- `if constexpr` (C++17): Eliminierung von Zweigen zur Kompilierzeit innerhalb von Templates
- Concepts (C++20): benannte Anforderungen, die Template-Parameter beschränken
- `auto` in Funktionsparametern (C++20): abgekürzte Funktionstemplates
- Variadische Templates: `template<typename... Args>`, Parameterpakete mit beliebiger Anzahl
- Nicht-Typ-Template-Parameter: `template<int N>`, Konstanten zur Kompilierzeit
- Template-Spezialisierung: Bereitstellung einer spezifischen Implementierung für bestimmte Typen
- Zweiphasige Namenssuche: Namen werden sowohl zur Definitions- als auch zur Instanziierungszeit geprüft

## Muster {#patterns}

### Funktionstemplates {#function-templates}

```cpp
template<typename T>
T max_val(T a, T b) {
    return (a > b) ? a : b;
}

// Explicit instantiation
int m1 = max_val<int>(3, 7);

// Implicit deduction
double m2 = max_val(3.14, 2.71);

// Multiple type parameters
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

// C++20: auto parameters = abbreviated template
auto add_modern(auto a, auto b) {
    return a + b;
}
```

### Klassentemplates {#class-templates}

```cpp
template<typename T, size_t N>
class StaticArray {
    T data_[N];
public:
    T& operator[](size_t i) { return data_[i]; }
    const T& operator[](size_t i) const { return data_[i]; }
    constexpr size_t size() const { return N; }

    auto begin() { return std::begin(data_); }
    auto end() { return std::end(data_); }
};

StaticArray<int, 10> arr;
arr[0] = 42;
```

### Concepts (C++20) {#concepts-c20}

```cpp
// Define a concept
template<typename T>
concept Numeric = std::is_arithmetic_v<T>;

template<typename T>
concept Sortable = requires(T t) {
    { t.begin() } -> std::input_iterator;
    { t.end() } -> std::input_iterator;
    { t.size() } -> std::convertible_to<size_t>;
};

template<typename T>
concept Printable = requires(std::ostream& os, T val) {
    { os << val } -> std::same_as<std::ostream&>;
};

// Use concepts - four equivalent syntaxes
template<Numeric T>
T square(T x) { return x * x; }

auto square2(Numeric auto x) { return x * x; }

template<typename T> requires Numeric<T>
T square3(T x) { return x * x; }

template<typename T>
T square4(T x) requires Numeric<T> { return x * x; }
```

### Variadische Templates {#variadic-templates}

```cpp
// Base case
void print() {}

// Recursive case
template<typename T, typename... Rest>
void print(T first, Rest... rest) {
    std::cout << first;
    if constexpr (sizeof...(rest) > 0) {
        std::cout << ", ";
        print(rest...);
    }
}

// C++17 fold expressions
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);  // unary right fold
}

template<typename... Args>
void print_all(Args&&... args) {
    ((std::cout << args << ' '), ...);  // comma fold
}
```

### Template-Spezialisierung {#template-specialization}

```cpp
// Primary template
template<typename T>
struct Serializer {
    static std::string serialize(const T& val) {
        return std::to_string(val);
    }
};

// Full specialization for std::string
template<>
struct Serializer<std::string> {
    static std::string serialize(const std::string& val) {
        return '"' + val + '"';
    }
};

// Partial specialization for pointers
template<typename T>
struct Serializer<T*> {
    static std::string serialize(T* val) {
        return val ? Serializer<T>::serialize(*val) : "null";
    }
};
```

### if constexpr (C++17) {#if-constexpr-c17}

```cpp
template<typename T>
auto process(T val) {
    if constexpr (std::is_integral_v<T>) {
        return val * 2;
    } else if constexpr (std::is_floating_point_v<T>) {
        return val * 2.0;
    } else if constexpr (std::is_same_v<T, std::string>) {
        return val + val;
    } else {
        static_assert(false, "Unsupported type");  // C++23
    }
}
```

## Stolperfallen {#gotchas}

- **Problem:** Template-Definitionen in `.cpp`-Dateien verursachen Linker-Fehler -> **Lösung:** Templates müssen in Header-Dateien stehen (oder explizite Instanziierung in der `.cpp`-Datei verwenden)
- **Problem:** Abhängige Namen benötigen das Schlüsselwort `typename` in Templates -> **Lösung:** `typename Container::value_type` statt `Container::value_type` innerhalb eines Templates
- **Problem:** SFINAE-Fehler erzeugen schwer lesbare Fehlermeldungen -> **Lösung:** Concepts (C++20) für klare Meldungen bei Verletzung von Constraints verwenden
- **Problem:** Template-Code-Aufblähung: Jede Instanziierung erzeugt eigenen Maschinencode -> **Lösung:** Typunabhängigen Code in eine nicht-template Basisklasse auslagern und dünne Template-Wrapper verwenden
- **Problem:** Zweiphasige Namenssuche: Nicht qualifizierte Namen werden in einer abhängigen Basisklasse nicht gefunden -> **Lösung:** `this->member` oder `Base<T>::member` verwenden, um auf Member der Basisklasse zuzugreifen

## Siehe auch {#see-also}

- [[stl-containers]]
- [[stl-algorithms]]
- [[lambda-expressions]]
- [cppreference: Concepts](https://en.cppreference.com/w/cpp/language/constraints)
