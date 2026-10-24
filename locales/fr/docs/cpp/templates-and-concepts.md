---
title: "Modèles et concepts"
category: concepts
tags: [cpp, templates, concepts, generic, metaprogramming, cpp20]
level: 3
source_sha256: 79fa6d4cd9ee28575c2e8ca643b2738fc718396d9f2ba3c3c82cb6b71d0559ac
translation: machine
translated_at: '2026-10-24'
---
# Modèles et concepts {#templates-and-concepts}

Programmation générique par paramétrage de types à la compilation. Les concepts (C++20) contraignent les templates à l'aide d'exigences lisibles.

## Points clés {#key-facts}

- Templates de fonctions : le compilateur génère le code pour chaque instanciation de type utilisée
- Templates de classes : paramétrage de classes entières par des types ou des valeurs
- L'instanciation des templates a lieu à la compilation, sans surcoût à l'exécution
- SFINAE (Substitution Failure Is Not An Error) : un échec de substitution retire la surcharge de l'ensemble des candidats
- `if constexpr` (C++17) : élimination de branches à la compilation à l'intérieur des templates
- Concepts (C++20) : exigences nommées qui contraignent les paramètres de template
- `auto` dans les paramètres de fonction (C++20) : templates de fonctions abrégés
- Templates variadiques : `template<typename... Args>` : packs de paramètres de nombre quelconque
- Paramètres de template non typés : `template<int N>` : constantes de compilation
- Spécialisation de template : fournir une implémentation spécifique pour des types particuliers
- Recherche en deux phases : les noms sont vérifiés à la définition et à l'instanciation

## Patterns {#patterns}

### Templates de fonctions {#function-templates}

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

### Templates de classes {#class-templates}

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

### Templates variadiques {#variadic-templates}

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

### Spécialisation de template {#template-specialization}

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

## Pièges {#gotchas}

- **Problème :** Les définitions de templates dans des fichiers `.cpp` provoquent des erreurs d'édition de liens -> **Solution :** Les templates doivent être placés dans des fichiers d'en-tête (ou utiliser une instanciation explicite dans le `.cpp`)
- **Problème :** Les noms dépendants nécessitent le mot-clé `typename` dans les templates -> **Solution :** `typename Container::value_type` et non `Container::value_type` à l'intérieur d'un template
- **Problème :** Les erreurs SFINAE produisent des messages d'erreur illisibles -> **Solution :** Utiliser les Concepts (C++20) pour obtenir des messages clairs sur la violation des contraintes
- **Problème :** Gonflement du code des templates : chaque instanciation génère un code machine distinct -> **Solution :** Factoriser le code indépendant du type dans une base non template, et utiliser de fines enveloppes templates
- **Problème :** Recherche en deux phases : les noms non qualifiés ne sont pas trouvés dans une base dépendante -> **Solution :** Utiliser `this->member` ou `Base<T>::member` pour accéder aux membres de la classe de base

## Voir aussi {#see-also}

- [[stl-containers]]
- [[stl-algorithms]]
- [[lambda-expressions]]
- [cppreference: Concepts](https://en.cppreference.com/w/cpp/language/constraints)
