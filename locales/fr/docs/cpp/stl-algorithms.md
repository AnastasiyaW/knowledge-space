---
title: "Algorithmes STL et Ranges"
category: concepts
tags: [cpp, stl, algorithms, ranges, sort, transform, cpp20]
level: 3
source_sha256: ea084749ae48f1700dc2203c1b11d19a203cf48e04e71774eb0b53c2431c8f7e
translation: machine
translated_at: '2026-10-24'
---
# Algorithmes STL et Ranges {#stl-algorithms-and-ranges}

`<algorithm>` fournit plus de 100 algorithmes génériques qui fonctionnent avec des itérateurs. Les Ranges de C++20 ajoutent une syntaxe de pipeline composable et paresseuse.

## Points clés {#key-facts}

- Les algorithmes opèrent sur des paires d'itérateurs `[begin, end)` : intervalle semi-ouvert
- Sans modification : `find`, `count`, `all_of`, `any_of`, `none_of`, `for_each`, `accumulate`
- Avec modification : `transform`, `copy`, `fill`, `replace`, `remove`, `reverse`, `rotate`
- Tri : `sort`, `stable_sort`, `partial_sort`, `nth_element`
- Recherche : `binary_search`, `lower_bound`, `upper_bound`, `equal_range`
- `std::sort` est un introsort (quicksort + heapsort + tri par insertion) : complexité O(n log n) garantie
- `std::stable_sort` préserve l'ordre relatif des éléments égaux
- `remove` / `remove_if` ne suppriment pas réellement les éléments : ils décalent les éléments et renvoient la nouvelle fin
- C++17 : politiques d'exécution parallèle, `std::execution::par`, `seq`, `par_unseq`
- C++20 : Ranges (`<ranges>`) : les algorithmes prennent directement des conteneurs, et les vues se composent de manière paresseuse
- `std::ranges::sort(vec)` à la place de `std::sort(vec.begin(), vec.end())`

## Modèles {#patterns}

### Algorithmes courants {#common-algorithms}

```cpp
std::vector<int> v = {5, 3, 1, 4, 2};

// Sort
std::sort(v.begin(), v.end());
std::sort(v.begin(), v.end(), std::greater<>());  // descending

// Find
auto it = std::find(v.begin(), v.end(), 3);
auto it2 = std::find_if(v.begin(), v.end(), [](int x) { return x > 3; });

// Transform
std::vector<int> squared;
std::transform(v.begin(), v.end(), std::back_inserter(squared),
    [](int x) { return x * x; });

// Accumulate (in <numeric>)
int sum = std::accumulate(v.begin(), v.end(), 0);

// Count
int evens = std::count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });

// All/Any/None
bool all_pos = std::all_of(v.begin(), v.end(), [](int x) { return x > 0; });
```

### Idiome erase-remove {#erase-remove-idiom}

```cpp
std::vector<int> v = {1, 2, 3, 2, 4, 2, 5};

// Classic (pre C++20)
v.erase(std::remove(v.begin(), v.end(), 2), v.end());

// With predicate
v.erase(std::remove_if(v.begin(), v.end(),
    [](int x) { return x < 3; }), v.end());

// C++20: much cleaner
std::erase(v, 2);
std::erase_if(v, [](int x) { return x < 3; });
```

### Ranges de C++20 {#c20-ranges}

```cpp
#include <ranges>
namespace rv = std::views;

std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Ranges algorithms - take containers directly
std::ranges::sort(v);
auto it = std::ranges::find(v, 5);

// Views - lazy, composable pipelines
auto result = v
    | rv::filter([](int x) { return x % 2 == 0; })   // even numbers
    | rv::transform([](int x) { return x * x; })       // square them
    | rv::take(3);                                       // first 3

for (int x : result) { std::cout << x << ' '; }  // 4 16 36

// Collect into vector (C++23: ranges::to)
auto collected = result | std::ranges::to<std::vector>();  // C++23

// Pre-C++23: manual collection
std::vector<int> out;
std::ranges::copy(result, std::back_inserter(out));
```

### Algorithmes parallèles (C++17) {#parallel-algorithms-c17}

```cpp
#include <execution>

std::vector<int> v(1'000'000);
std::iota(v.begin(), v.end(), 0);

// Parallel sort
std::sort(std::execution::par, v.begin(), v.end());

// Parallel transform-reduce
int sum = std::transform_reduce(std::execution::par,
    v.begin(), v.end(), 0, std::plus<>(),
    [](int x) { return x * x; });
```

### Recherche binaire (sur des données triées) {#binary-search-on-sorted-data}

```cpp
std::vector<int> v = {1, 3, 5, 7, 9, 11};

bool found = std::binary_search(v.begin(), v.end(), 5);       // true
auto lb = std::lower_bound(v.begin(), v.end(), 5);            // -> 5
auto ub = std::upper_bound(v.begin(), v.end(), 5);            // -> 7
auto [lo, hi] = std::equal_range(v.begin(), v.end(), 5);      // range of 5s
```

## Pièges {#gotchas}

- **Problème :** `remove` ne modifie pas la taille du conteneur : il déplace seulement les éléments -> **Correction :** toujours l'associer à `erase` (idiome erase-remove), ou utiliser `std::erase` / `std::erase_if` de C++20
- **Problème :** utiliser `sort` sur une `list` coûte un espace supplémentaire O(n log n) à cause des itérateurs à accès aléatoire -> **Correction :** utiliser la fonction membre `list::sort()`, qui a une complexité O(n log n) avec un espace O(1)
- **Problème :** les vues des Ranges sont paresseuses : elles ne s'exécutent qu'au moment de l'itération. Risque de références pendantes si la source est détruite -> **Correction :** matérialiser les vues avant que la source ne sorte de sa portée
- **Problème :** les algorithmes parallèles exigent que les éléments puissent être traités indépendamment : risque de data races sur un état partagé -> **Correction :** utiliser `std::atomic` ou revoir la conception pour éviter un état mutable partagé

## Voir aussi {#see-also}

- [[stl-containers]]
- [[lambda-expressions]]
- [[templates-and-concepts]]
- [cppreference : Algorithmes](https://en.cppreference.com/w/cpp/algorithm)
