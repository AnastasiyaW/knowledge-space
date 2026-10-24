---
title: "Portée et durée de vie des variables en C++"
description: "Règles de portée au niveau des blocs, masquage de noms et ordre de destruction déterministe, prérequis du RAII"
level: 4
source_sha256: cc71320356236c667198f8b1cb0ab13afa2bf1ae3baae1deff7395656012e1e1
translation: machine
translated_at: '2026-10-24'
---
# Portée et durée de vie des variables en C++ {#variable-scope-and-lifetime-in-c}

C++ applique une portée au niveau des blocs, avec des règles strictes sur la visibilité des variables et le moment de leur destruction. Comprendre la portée permet d'éviter les bugs de masquage de noms, et c'est un prérequis pour [[raii-resource-management]].

## Niveaux de portée {#scope-levels}

C++ prend en charge trois niveaux de portée :

1. **Portée globale** : déclarée en dehors de toutes les fonctions, accessible partout
2. **Portée de fonction / locale** : déclarée à l'intérieur d'une fonction, accessible dans cette fonction
3. **Portée de bloc** : déclarée à l'intérieur de `{}`, accessible uniquement dans ce bloc

```cpp
int x = 10;  // global scope

int main() {
    int x = 20;  // local scope (shadows global x)

    {
        int x = 30;  // block scope (shadows local x)
        std::cout << x;  // prints 30 (nearest scope)
    }

    std::cout << x;  // prints 20 (block x is gone)

    // Access global x despite local shadow:
    std::cout << ::x;  // prints 10 (scope resolution operator)
}
```

## Règles de recherche de noms {#name-lookup-rules}

Lorsqu'un nom est utilisé, le compilateur le recherche depuis la portée la plus interne vers l'extérieur :
1. Bloc courant
2. Blocs englobants
3. Portée de la fonction
4. Portée de l'espace de noms
5. Portée globale

La **première correspondance l'emporte**. Les déclarations internes masquent les déclarations externes.

## Opérateur de résolution de portée {#scope-resolution-operator}

L'opérateur `::` accède à une portée précise :

```cpp
int x = 10;  // global

int main() {
    int x = 20;  // local shadows global
    std::cout << x;    // 20 (local)
    std::cout << ::x;  // 10 (global, bypassing shadow)
}
```

Il sert aussi à accéder aux membres d'un espace de noms ou d'une classe : `std::cout`, `MyClass::method`.

## Durée de stockage {#storage-duration}

| Durée | Création | Destruction | Exemple |
|-------|----------|-------------|---------|
| Automatique | Entrée dans le bloc | Sortie du bloc | Variables locales |
| Statique | Démarrage du programme | Fin du programme | Variables locales `static`, globales |
| Dynamique | `new` | `delete` | Allocation sur le tas |
| Thread | Démarrage du thread | Fin du thread | `thread_local` |

## `const` comme documentation {#const-as-documentation}

Déclarer des variables `const` documente leur portée et leur usage :

```cpp
void process() {
    const int max_retries = 3;  // documents: this will not change
    int attempts = 0;           // documents: this WILL change

    // Technique for exploring unfamiliar code:
    // 1. Mark everything const
    // 2. Compile
    // 3. Remove const where compiler complains
    // Result: map of which variables actually vary
}
```

Règles pour `const` :
- Doit être initialisée à la déclaration (pas de « on la rendra const plus tard »)
- Le compilateur l'impose : toute tentative de modification produit une erreur de compilation
- Exprime l'intention aux autres développeurs qui lisent le code

## Variables globales {#global-variables}

Les variables globales :
- Sont créées au démarrage du programme et détruites à sa fin
- Ne sont ni sur la pile ni sur le tas (elles occupent un segment mémoire dédié)
- Sont accessibles depuis n'importe quelle fonction (néfaste pour l'encapsulation)
- Ont un ordre d'initialisation **indéfini** entre unités de traduction (Static Initialization Order Fiasco)

**Règle générale** : évitez l'état global modifiable. Utilisez des globales `const`/`constexpr` pour les vraies constantes, et passez l'état par paramètres pour tout le reste.

## Pièges courants {#gotchas}

- **Le masquage est silencieux par défaut.** Déclarer une variable de même nom dans une portée interne est du C++ valide et ne produit aucun avertissement, sauf si vous activez `-Wshadow`. Compilez toujours avec les avertissements activés.
- **Les variables déclarées dans l'initialisation d'un `for` sont limitées à la boucle.** Dans `for (int i = 0; ...)`, `i` n'existe plus après le corps de la boucle.
- **Les instructions d'initialisation de `if` (C++17) sont limitées au bloc.** Dans `if (auto it = map.find(key); it != map.end())`, `it` n'existe qu'à l'intérieur du `if`/`else`.
- **Les variables locales `static` sont initialisées une seule fois**, lors du premier appel de la fonction, puis persistent. Elles ne sont **pas** réinitialisées aux appels suivants, ce qui est utile pour les schémas d'initialisation paresseuse.

## Références croisées {#cross-references}

- [[raii-resource-management]] : lier le nettoyage à la sortie de portée
- [[object-lifetime]] : ordre de construction et de destruction
- [[const-and-type-safety]] : exactitude de `const`
- [Pointeurs intelligents et gestion de la mémoire](smart-pointers.md) : gestion mémoire basée sur la portée
