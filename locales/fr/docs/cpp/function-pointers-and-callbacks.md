---
title: "Pointeurs de fonction et callbacks en C++"
description: "Pointeurs de fonction de style C, std::function et lambdas pour l'invocation indirecte et les patterns de callback"
level: 3
source_sha256: d96b61d5bb5f83c7e7079207a54517a928750a88c65c1de59ce5e9182e5415e2
translation: machine
translated_at: '2026-10-24'
---
# Pointeurs de fonction et callbacks en C++ {#function-pointers-and-callbacks-in-c}

Les fonctions en C++ ont des adresses en mémoire. Un pointeur de fonction contient l'adresse d'une fonction et peut l'invoquer indirectement. Le C++ moderne fournit `std::function` et les lambdas comme alternatives plus sûres et plus souples.

## Pointeurs de fonction hérités de style C {#legacy-c-style-function-pointers}

Chaque fonction est stockée en mémoire. Le nom de la fonction sans parenthèses s'évalue à son adresse :

```cpp
int sum(int a, int b) { return a + b; }

// Print function address
std::cout << reinterpret_cast<void*>(sum);  // some hex address

// Declare function pointer (C-style syntax)
int (*func_ptr)(int, int) = sum;

// Call through pointer
int result = func_ptr(3, 4);          // result = 7
int result2 = (*func_ptr)(3, 4);      // equivalent, explicit dereference
```

La syntaxe `int (*name)(int, int)` se lit ainsi : `name` est un pointeur vers une fonction prenant deux `int` et retournant un `int`.

## auto pour une syntaxe plus simple {#auto-for-simpler-syntax}

```cpp
auto* func_ptr = sum;   // compiler deduces the type
func_ptr(3, 4);         // works identically
```

## Fonctions en tant que paramètres {#functions-as-parameters}

La vraie puissance : passer un comportement en argument.

```cpp
// Legacy: function pointer parameter
int calculate(int* arr, int size, int (*operation)(int, int)) {
    int result = arr[0];
    for (int i = 1; i < size; ++i) {
        result = operation(result, arr[i]);
    }
    return result;
}

int sum(int a, int b) { return a + b; }
int product(int a, int b) { return a * b; }

int arr[] = {1, 2, 3, 4, 5};
calculate(arr, 5, sum);      // 15
calculate(arr, 5, product);  // 120
```

## Lambdas comme fonctions en ligne {#lambdas-as-inline-functions}

Plutôt que de définir des fonctions nommées pour des callbacks à usage unique, utilisez des lambdas :

```cpp
// Lambda: anonymous function
calculate(arr, 5, [](int a, int b) { return a + b; });
calculate(arr, 5, [](int a, int b) { return a * b; });
```

Les lambdas qui ne capturent rien (`[]` vide) peuvent se convertir implicitement en pointeurs de fonction de style C.

## std::function (C++ moderne) {#stdfunction-modern-c}

`std::function` de `<functional>` est un wrapper de fonction généraliste à effacement de type. Il fonctionne avec les pointeurs de fonction, les lambdas (y compris celles qui capturent) et les objets fonction.

```cpp
#include <functional>

// Accepts any callable with matching signature
int calculate(int* arr, int size, const std::function<int(int, int)>& op) {
    int result = arr[0];
    for (int i = 1; i < size; ++i) {
        result = op(result, arr[i]);
    }
    return result;
}

// Works with capturing lambda (function pointer cannot do this)
int offset = 10;
calculate(arr, 5, [offset](int a, int b) { return a + b + offset; });
```

## Quel mécanisme choisir {#when-to-use-which}

| Mécanisme | Surcoût | Captures | Effacement de type |
|-----------|---------|----------|-------------------|
| Pointeur de fonction C | Nul | Non | Non |
| `auto` + lambda | Nul (en ligne) | Oui | Non |
| `std::function` | Faible (allocation tas possible) | Oui | Oui |
| Paramètre template | Nul (à la compilation) | Oui | Non |

**Choix par défaut** : `std::function` pour les frontières d'API, les templates pour le code interne ou critique en performance. Les pointeurs de fonction bruts uniquement pour l'interopérabilité avec C.

```cpp
// Best for library APIs: flexible, clear interface
void register_callback(std::function<void(int)> cb);

// Best for hot paths: zero overhead, inlined
template <typename F>
void hot_loop(F&& callback) { /* ... */ }
```

## Pièges à éviter {#gotchas}

- **Les lambdas avec captures ne peuvent pas se convertir en pointeurs de fonction bruts.** Seules les lambdas sans capture (`[]`) sont convertibles. Utilisez `std::function` pour les lambdas avec captures.
- **`std::function` a un surcoût.** Il peut allouer sur le tas pour de grandes captures et utilise un dispatch virtuel en interne. Pour le code critique en performance dans des boucles serrées, privilégiez les paramètres template.
- **Passez `std::function` par `const&`**, et non par valeur, pour éviter des copies inutiles de l'objet appelable interne.
- **Appeler un `std::function` vide lève `std::bad_function_call`.** Vérifiez toujours `if (func)` avant l'appel si la fonction peut être vide.

## Références croisées {#cross-references}

- [[lambda-expressions]] - syntaxe des lambdas, captures, lambdas génériques
- [[templates-and-concepts]] - utiliser les templates pour des callbacks à coût nul
- [[design-patterns-cpp]] - le pattern Strategy utilise largement les objets fonction
- [[stl-algorithms]] - les algorithmes acceptent des appelables en paramètres
