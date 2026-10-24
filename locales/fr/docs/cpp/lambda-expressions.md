---
title: "Expressions lambda"
category: concepts
tags: [cpp, lambda, closures, functional, cpp11, cpp14, cpp20]
level: 4
source_sha256: 0cd923aebac4f40ff1aa03f84d3a407fdfd56555118a50bf288ef9a59454c976
translation: machine
translated_at: '2026-10-24'
---
# Expressions lambda {#lambda-expressions}

Objets fonctions anonymes à sémantique de capture. Outil central pour les callbacks, les algorithmes et les patrons fonctionnels.

## Points clés {#key-facts}

- Syntaxe : `[capture](params) -> return_type { body }`
- `[=]` capture toutes les variables locales par valeur, `[&]` les capture toutes par référence
- `[x]` capture par valeur, `[&x]` capture par référence, `[x = std::move(y)]` capture avec initialisation (C++14)
- Les lambdas sont du sucre syntaxique pour des types de fermeture générés par le compilateur (un `struct` sans nom disposant d'un `operator()`)
- Chaque lambda possède un type unique : utiliser `std::function<>` ou `auto` pour la stocker
- Les paramètres `auto` des lambdas (C++14) permettent de créer des lambdas génériques/polymorphes
- Le mot-clé `mutable` permet de modifier les variables capturées par valeur
- Les lambdas `constexpr` (C++17) sont utilisables dans des contextes de compilation
- Lambdas template (C++20) : `[]<typename T>(T x) { ... }`
- Les lambdas sans capture peuvent être converties en pointeur de fonction
- Préférer une lambda à `std::bind` : plus claire, plus efficace, mieux optimisée

## Patrons {#patterns}

### Modes de capture {#capture-modes}

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

### Lambdas génériques {#generic-lambdas}

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

### Avec les algorithmes de la STL {#with-stl-algorithms}

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

### Lambda invoquée immédiatement (IIFE) {#immediately-invoked-lambda-iife}

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

### Lambda récursive {#recursive-lambda}

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

## Pièges {#gotchas}

- **Problème :** capturer une variable locale par référence alors que la lambda lui survit : référence pendante, comportement indéfini -> **Solution :** capturer par valeur, ou utiliser une capture avec initialisation pour transférer la propriété dans la lambda
- **Problème :** `[=]` capture le pointeur `this` par valeur (le pointeur, pas l'objet) : toujours pendant si l'objet est détruit -> **Solution :** utiliser `[*this]` (C++17) pour capturer une copie de l'objet, ou s'assurer de la durée de vie de celui-ci
- **Problème :** `std::function<>` a un coût (effacement de type, allocation sur le tas) -> **Solution :** utiliser `auto` lorsque c'est possible ; n'utiliser `std::function` que lorsqu'un stockage à type effacé est nécessaire
- **Problème :** une lambda modifiant une variable capturée par valeur ne compile pas -> **Solution :** ajouter `mutable` : `[x]() mutable { x++; }`

## Voir aussi {#see-also}

- [[stl-algorithms]]
- [[templates-and-concepts]]
- [[move-semantics]]
- [cppreference : Lambda](https://en.cppreference.com/w/cpp/language/lambda)
