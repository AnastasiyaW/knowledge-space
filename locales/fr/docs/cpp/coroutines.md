---
title: "Coroutines C++20"
description: "Multitâche coopératif avec co_yield, co_return et co_await pour les générateurs paresseux et les E/S asynchrones"
level: 4
source_sha256: 58c633c9f018c9d0b963b088c0cb5a295b20091a0636f17c465bb2f04d2eef84
translation: machine
translated_at: '2026-10-24'
---
# Coroutines C++20 {#c20-coroutines}

Les coroutines apportent le multitâche coopératif en C++20 : une fonction capable de suspendre son exécution, de produire une valeur, puis de reprendre là où elle s'est arrêtée. Elles sont fondamentalement différentes des threads : il ne s'agit pas de parallélisme, mais d'entrelacer l'exécution sans bloquer.

## Modèle de base {#core-model}

Une fonction ordinaire possède une **frame de pile** créée à l'appel et détruite au retour. Une coroutine possède une **frame de coroutine** allouée sur le tas, qui persiste à travers les suspensions.

Différence essentielle avec les threads :
- **Threads** : multitâche préemptif, c'est le système d'exploitation qui décide quand basculer
- **Coroutines** : multitâche coopératif, la coroutine cède volontairement son tour

Lorsqu'une coroutine se suspend, elle signifie « j'ai effectué un peu de travail, je suis prête à laisser les autres s'exécuter ». À la reprise, l'exécution continue exactement là où elle s'était arrêtée, avec tout l'état local intact.

## Mots-clés {#keywords}

C++20 introduit trois mots-clés qui transforment une fonction en coroutine :

| Mot-clé | Rôle |
|---------|------|
| `co_yield expr` | Suspendre et produire une valeur |
| `co_return expr` | Retour final (la coroutine se termine) |
| `co_await expr` | Suspendre jusqu'à la fin d'un awaitable |

Toute fonction contenant l'un de ces mots-clés est automatiquement traitée comme une coroutine par le compilateur.

## Cas d'usage {#use-cases}

Les coroutines excellent dans les domaines suivants :
- **Générateurs paresseux** : produire les valeurs une à une sans calculer la séquence entière
- **E/S asynchrones** : lancer la lecture d'un fichier, céder le contrôle, reprendre quand les données sont disponibles
- **Traitement de flux** : traiter les éléments à mesure qu'ils arrivent, sans tout mettre en tampon
- **Pipelines** : enchaîner producteurs et consommateurs sans threads

Elles ne sont **pas** adaptées à :
- le parallélisme lié au CPU (utiliser plutôt des threads ou `std::async`)
- l'exécution simultanée de N tâches identiques (un pool de threads est préférable)

## Motif du générateur {#generator-pattern}

Le motif le plus courant : une fonction qui produit une séquence de valeurs de manière paresseuse.

```cpp
#include <coroutine>
#include <iostream>

// Simplified generator (real implementation needs promise_type, etc.)
Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}

// Usage: values computed on-demand
auto fib = fibonacci();
for (int i = 0; i < 10; ++i) {
    std::cout << fib.next() << " ";
}
// Output: 0 1 1 2 3 5 8 13 21 34
```

## Cycle de vie de la frame de coroutine {#coroutine-frame-lifecycle}

1. L'appelant invoque la fonction coroutine
2. La frame de coroutine est allouée (sur le tas, et non sur la pile)
3. Les paramètres sont copiés dans la frame
4. L'objet promise est construit
5. L'exécution commence
6. Sur `co_yield`/`co_await` : l'état est sauvegardé, le contrôle revient à l'appelant
7. À la reprise : l'exécution continue depuis le point de suspension
8. Sur `co_return` ou à la sortie de la fin de la fonction : la frame est détruite

## Relation avec les autres fonctionnalités de concurrence {#relationship-to-other-concurrency-features}

| Fonctionnalité | Modèle | Surcoût | Usage idéal |
|---------|-------|----------|----------|
| `std::thread` | Préemptif, géré par l'OS | Élevé (thread système) | Parallélisme CPU |
| `std::async` | Basé sur les tâches, peut utiliser un pool de threads | Moyen | Tâches lancées sans suivi |
| Coroutines | Coopératif, mono-thread | Faible (frame sur le tas) | E/S, générateurs, pipelines |

## Pièges {#gotchas}

- **Pas de type générateur dans la bibliothèque standard en C++20.** Il faut écrire son propre `Generator<T>` avec un `promise_type` correct, ou utiliser une bibliothèque. C++23 ajoute `std::generator`.
- **La frame de coroutine est allouée sur le tas.** Le compilateur peut éliminer cette allocation (HALO - Heap Allocation eLision Optimization), mais rien ne le garantit. Pour les boucles critiques en performance, mesurer.
- **Les références pendantes sont faciles à créer.** Si une coroutine capture une référence vers une variable locale de l'appelant, et que la portée de l'appelant se termine avant la reprise de la coroutine, on obtient un comportement indéfini.
- **Le débogage est difficile.** Parcourir pas à pas la suspension et la reprise d'une coroutine dans un débogueur n'est pas bien pris en charge par la plupart des IDE en 2024.

## Références croisées {#cross-references}

- [Concurrence - Threads, Async, Atomics](concurrency.md) - threads, mutex, opérations atomiques
- [[modern-cpp-features]] - autres ajouts de C++20
- [[lambda-expressions]] - souvent utilisées avec les coroutines pour les callbacks
