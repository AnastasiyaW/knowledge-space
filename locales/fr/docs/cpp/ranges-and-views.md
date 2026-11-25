---
title: "Intervalles et vues en C++20"
description: "Pipelines paresseux et composables pour le traitement de séquences avec l'opérateur pipe et les adaptateurs d'intervalles"
level: 3
source_sha256: 94b917c8683ffd5d90dc1737024a26f008700e48d2119b97f6df3cc2f18ae3a4
translation: machine
translated_at: '2026-10-24'
---
# Intervalles et vues en C++20 {#c20-ranges-and-views}

Les intervalles (ranges) de C++20 offrent une manière composable, paresseuse et orientée pipeline de manipuler des séquences. Ils remplacent les schémas verbeux à base de paires d'itérateurs par une syntaxe plus claire et permettent souvent de meilleures performances grâce à l'évaluation paresseuse.

## Concepts fondamentaux {#core-concepts}

**Range** : tout type qui fournit `begin()` et `end()`. Tous les conteneurs standard sont des ranges.

**View** : un adaptateur d'intervalle léger, non propriétaire et paresseux. Les vues ne copient pas les données : elles décrivent une transformation évaluée à la demande lors de l'itération.

**Algorithmes sur intervalles** : remplacements directs des fonctions de `<algorithm>` qui acceptent un conteneur complet au lieu de paires d'itérateurs.

```cpp
#include <ranges>
#include <vector>
#include <algorithm>

std::vector<int> nums = {32, 1, 26, 7, 10, 21};

// Old way: iterator pair
std::sort(nums.begin(), nums.end());

// C++20 ranges: pass entire container
std::ranges::sort(nums);
```

## Pipeline de vues (opérateur pipe) {#view-pipeline-pipe-operator}

Les vues se composent à l'aide de l'opérateur `|`, à la manière des tubes Unix. Chaque étape produit une vue paresseuse : aucune copie, aucune allocation et aucun calcul avant le début de l'itération.

```cpp
#include <ranges>
#include <vector>

struct PossibleValue {
    bool flag;
    int value;
};

std::vector<PossibleValue> values = {
    {true, 1}, {true, 2}, {false, 3}, {true, 4}, {false, 5}
};

auto flagged = [](const PossibleValue& pv) { return pv.flag; };

auto result = values
    | std::views::filter(flagged)           // keep only flagged
    | std::views::transform([](const PossibleValue& pv) { return pv.value; })  // extract int
    | std::views::reverse                   // reverse order
    | std::views::drop(1);                  // skip first element

// result is a lazy view: {4, 2} -> drop 1 -> {2}
// Nothing computed until iteration:
for (int v : result) {
    std::cout << v << " ";
}
```

Propriété clé : l'ensemble du pipeline est **évalué paresseusement**. Aucun cycle CPU n'est consommé pour évaluer la lambda ou effectuer le filtrage tant que le résultat n'est pas itéré. C'est à la fois plus simple et plus rapide que la boucle impérative équivalente.

## Adaptateurs de vues courants {#common-view-adaptors}

| Adaptateur | Rôle |
|------------|------|
| `std::views::filter(pred)` | Conserve les éléments satisfaisant le prédicat |
| `std::views::transform(fn)` | Applique une fonction à chaque élément |
| `std::views::take(n)` | Les n premiers éléments |
| `std::views::drop(n)` | Ignore les n premiers éléments |
| `std::views::reverse` | Inverse l'ordre d'itération |
| `std::views::keys` / `std::views::values` | Pour les intervalles de type map |
| `std::views::split(delim)` | Découpe selon un délimiteur |
| `std::views::join` | Aplatit des intervalles imbriqués |

## Tri et recherche avec les intervalles {#ranges-sorting-and-finding}

```cpp
#include <ranges>
#include <algorithm>
#include <vector>

std::vector<int> v = {5, 3, 8, 1, 9};

// Sort with ranges
std::ranges::sort(v);

// Find with ranges
auto it = std::ranges::find(v, 8);

// Find with predicate
auto it2 = std::ranges::find_if(v, [](int x) { return x > 6; });

// Partial sort: nth_element
// Puts the correct element at position n, partitions rest
std::ranges::nth_element(v, v.begin() + 2);
// v[2] is now what would be at index 2 if fully sorted
// Elements before are <= v[2], elements after are >= v[2]
// Neither half is necessarily sorted - faster than partial_sort
```

## Conventions de nommage des algorithmes {#algorithm-naming-conventions}

L'en-tête `<algorithm>` suit des conventions cohérentes qui allègent l'effort de mémorisation :

- Les paramètres suivent toujours le même ordre : begin avant end, source avant destination
- Le suffixe `_if` désigne la version à prédicat : `find` et `find_if`, `count` et `count_if`
- Le suffixe `_copy` indique que le résultat est écrit dans un itérateur de sortie
- Le suffixe `_n` indique que l'opération porte sur un nombre d'éléments plutôt que sur un intervalle
- Les versions `ranges::` acceptent un conteneur complet, tandis que les versions `std::` prennent des paires d'itérateurs

## Prise en charge par les compilateurs {#compiler-support}

Tous les compilateurs ne prennent pas entièrement en charge les intervalles de C++20. Vous pourriez avoir besoin :
- de la dernière version du compilateur ;
- de l'option explicite `-std=c++20` ou `/std:c++latest` ;
- de compilateurs en ligne (Compiler Explorer) pour tester la disponibilité de la fonctionnalité.

## Pièges à éviter {#gotchas}

- **Les vues ne possèdent pas les données.** Si le conteneur sous-jacent est détruit ou modifié, la vue devient pendante. Ne stockez jamais une vue qui survit à sa source.
- **Le support du débogueur est limité.** La plupart des débogueurs (en 2024) n'affichent pas bien le contenu des vues. Pour inspecter les valeurs pendant le débogage, utilisez une boucle qui les convertit en chaîne.
- **Toutes les combinaisons de vues ne compilent pas.** Certains pipelines exigent que l'intervalle sous-jacent satisfasse des concepts précis (par exemple, `reverse` nécessite un intervalle bidirectionnel). Les messages d'erreur peuvent être obscurs.
- **`nth_element` n'est PAS un tri partiel.** Il partitionne correctement mais ne trie pas les éléments « retenus » : utilisez-le lorsque vous voulez les N premiers sans vous soucier de leur ordre (plus rapide que `partial_sort`).

## Références croisées {#cross-references}

- [[stl-algorithms]] - schémas d'algorithmes traditionnels
- [[stl-containers]] - types de conteneurs compatibles avec les intervalles
- [[lambda-expressions]] - écriture de prédicats pour filter/transform
- [Performance Optimization](performance-optimization.md) - bénéfices de l'évaluation paresseuse
