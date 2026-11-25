---
title: "Gestion manuelle de la mémoire en C++"
description: "new/delete bruts, pile et tas, et les trois modes de défaillance qui motivent les pointeurs intelligents et le RAII"
level: 3
source_sha256: fe1a627336ab59da854461b93a8bd897a1a05a88c7301ebab7d0610c2462524e
translation: machine
translated_at: '2026-10-24'
---
# Gestion manuelle de la mémoire en C++ {#manual-memory-management-in-c}

Comprendre les `new`/`delete` bruts est indispensable pour saisir pourquoi les [Pointeurs intelligents et gestion de la mémoire](smart-pointers.md) et [[raii-resource-management]] existent. La gestion manuelle de la mémoire est sujette aux erreurs et doit être évitée en C++ moderne, mais connaître ses modes de défaillance est essentiel.

## Pile vs tas (magasin libre) {#stack-vs-heap-free-store}

**Pile** : stockage automatique. Les objets sont créés à l'entrée d'une portée et détruits à sa sortie. Aucune gestion manuelle n'est nécessaire.

**Tas (magasin libre)** : stockage dynamique. Les objets sont créés avec `new` et persistent jusqu'à leur destruction explicite avec `delete`. Le programmeur est entièrement responsable de la durée de vie.

```cpp
void example() {
    Resource local("local");     // stack: automatic cleanup at }

    Resource* p = new Resource("heap");  // heap: manual cleanup
    p->getName();
    delete p;                    // must explicitly destroy
}  // local destroyed here automatically, p's memory was freed above
```

## Trois modes de défaillance {#three-failure-modes}

### 1. Utilisation après delete (pointeur pendant) {#1-use-after-delete-dangling-pointer}

```cpp
Resource* p = new Resource("data");
delete p;
p->getName();  // UNDEFINED BEHAVIOR: p points to freed memory
// Crash, garbage data, or silent corruption
```

### 2. Double delete {#2-double-delete}

```cpp
Resource* p = new Resource("data");
Resource* p2 = p;    // copy the pointer, not the object
delete p2;           // frees the memory
delete p;            // CRASH: same memory freed twice
```

Copier des pointeurs bruts est dangereux, car plusieurs pointeurs vers le même objet créent une ambiguïté quant à celui qui est responsable de la libération.

### 3. Fuite mémoire {#3-memory-leak}

```cpp
Resource* p = new Resource("data");
if (someCondition) {
    return;  // early return: delete never reached
}
delete p;    // never executes when condition is true
```

La règle « chaque `new` doit avoir exactement un `delete` » semble simple, mais elle se brise avec :
- les retours anticipés ;
- les exceptions levées entre `new` et `delete` ;
- les flots de contrôle complexes ;
- les copies de pointeurs créant une ambiguïté de propriété.

## Surcharge de new et delete {#overloading-new-and-delete}

`new` et `delete` sont des opérateurs qui peuvent être surchargés pour un comportement personnalisé. La surcharge n'affecte que la partie allocation/désallocation de la mémoire : la construction et la destruction restent inchangées.

```cpp
#include <cstdlib>
#include <cstddef>

// Track allocations globally
static std::size_t allocated_mem = 0;

void* operator new(std::size_t size) {
    allocated_mem += size;
    std::cout << "Allocating " << size << " bytes\n";
    return std::malloc(size);
}

void operator delete(void* ptr, std::size_t size) noexcept {
    allocated_mem -= size;
    std::cout << "Deallocating " << size << " bytes\n";
    std::free(ptr);
}

// At program end: if allocated_mem != 0, there is a leak
```

Cas d'usage de la surcharge :
- **Détection personnalisée de fuites mémoire** : suivre l'équilibre allocations/désallocations ;
- **Pooling mémoire** : pré-allouer de grands blocs et regrouper les objets pour réduire la fragmentation ;
- **Systèmes embarqués** : implémenter un tas personnalisé lorsque le système d'exploitation n'en fournit pas ;
- **Profilage de performance** : représenter graphiquement les schémas d'allocation au fil du temps ;
- **Surcharges spécifiques à une classe** : optimiser l'allocation pour une classe donnée.

## Surcharges globales vs surcharges limitées à une classe {#global-vs-class-scoped-overloads}

```cpp
// Global: affects ALL allocations in the program
void* operator new(std::size_t size) { /* ... */ }

// Class-scoped: affects only this class
class MyObject {
    static void* operator new(std::size_t size) { /* ... */ }
    static void operator delete(void* ptr) { /* ... */ }
};
```

## Vector : taille vs capacité {#vector-size-vs-capacity}

Comprendre comment `std::vector` gère la mémoire en interne :

```cpp
std::vector<Subject> v;
// size=0, capacity=0

v.reserve(3);
// size=0, capacity=3 (memory allocated, no objects constructed)

v.emplace_back("Math", 95);
// size=1, capacity=3 (one object constructed in-place)

v.push_back(Subject("History", 80));
// size=2, capacity=3 (temporary created then moved)

v.clear();
// size=0, capacity=3 (objects destroyed but memory NOT freed)
```

Distinctions essentielles :
- `reserve(n)` : alloue la capacité sans construire d'objets ;
- `resize(n)` : modifie la taille, construit/détruit des objets au besoin ;
- `emplace_back(args...)` : construit l'objet en place (sans temporaire, sans déplacement) ;
- `push_back(obj)` : copie/déplace un objet existant dans le vecteur ;
- `clear()` : détruit tous les objets mais ne réduit PAS la capacité ;
- `shrink_to_fit()` : demande une réduction de capacité (non contraignante).

**Préférer `emplace_back` à `push_back`** lors de la construction de nouveaux objets : cela élimine le temporaire et le surcoût du constructeur de déplacement.

## La réponse du C++ moderne {#the-modern-c-answer}

L'ensemble des bogues de gestion manuelle de la mémoire est résolu par :
1. **RAII** : lier la durée de vie de la ressource à la portée de l'objet ;
2. **`std::unique_ptr`** : propriété exclusive, sans surcoût ;
3. **`std::shared_ptr`** : propriété partagée avec comptage de références ;
4. ne jamais utiliser `new`/`delete` bruts dans le code applicatif.

## Pièges à éviter {#gotchas}

- **`delete` sur un pointeur nul est sans danger** (aucune opération, selon la norme), mais `delete` sur un pointeur déjà libéré est un comportement indéfini.
- **`clear()` ne libère pas la mémoire du vecteur.** Seuls le destructeur ou `shrink_to_fit()` peuvent réduire la capacité. C'est un choix délibéré pour des raisons de performance : on évite des réallocations si l'on remplit à nouveau le vecteur.
- **Les surcharges globales de `operator new` affectent l'ensemble du programme**, y compris le code des bibliothèques. Utiliser des surcharges limitées à une classe pour un comportement ciblé.
- **`malloc`/`free` n'appellent PAS les constructeurs/destructeurs.** Ne les utiliser qu'à l'intérieur des surcharges de `operator new`/`operator delete`, jamais directement dans du code C++.

## Références croisées {#cross-references}

- [Pointeurs intelligents et gestion de la mémoire](smart-pointers.md) : `unique_ptr`, `shared_ptr`, `weak_ptr`
- [[raii-resource-management]] : le motif qui remplace la gestion manuelle
- [[object-lifetime]] : portée, durée de stockage, ordre de destruction
- [[move-semantics]] : transfert efficace des ressources
