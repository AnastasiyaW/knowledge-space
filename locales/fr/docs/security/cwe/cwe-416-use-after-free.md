---
description: "CWE-416 : Utilisation après libération (Use After Free) - l'accès à de la mémoire libérée permet l'exécution de code à distance, la divulgation d'informations et le déni de service. Pointeurs pendants, double libération, invalidation d'itérateurs, conditions de course libération/utilisation."
date: 2026-04-16
tags: [security, cwe, memory-corruption, use-after-free, c, cpp, rust]
level: Advanced
source_sha256: 7e5d04770fa0794fc1e05ca2ad28e1d119a9de7162e2d01984516a42cbcfdef8
translation: machine
translated_at: '2026-10-24'
---
# CWE-416 : Utilisation après libération (Use After Free) {#cwe-416-use-after-free}

**Rang dans le CWE Top 25 :** 8 (2024). Dans le top 10 de façon constante depuis 2019.
**Gravité :** CVSS 7,0 à 10,0. La plupart des RCE dans les navigateurs (V8, WebKit, Firefox) sont des exploitations de UAF.
**Mécanisme racine :** le gestionnaire de mémoire réutilise une allocation libérée ; le programme accède à un pointeur périmé ; une allocation contrôlée par l'attaquant occupe d'abord la zone libérée.

---

## Sémantique fonctionnelle {#functional-semantics}

Après `free(ptr)`, l'allocateur restitue la mémoire au tas. L'allocateur peut réutiliser immédiatement cette zone pour un appel ultérieur à `malloc()`. Si le programme conserve encore un pointeur vers la zone libérée et y accède :

- **Lecture :** renvoie des données influencées par l'attaquant si l'allocateur a réutilisé la zone.
- **Écriture :** écrase une allocation contrôlée par l'attaquant avec des données du programme.
- **Exécution (pointeur de fonction / vtable) :** saute vers une adresse contrôlée par l'attaquant.

**Heap grooming / attaque par confusion de types :**
```text
free(victim_object)      → allocator marks region free
malloc(attacker_size)    → if sizes match, region is reused for attacker allocation
attacker writes          → fills region with crafted data (fake vtable, fake object)
program uses victim_ptr  → reads/calls attacker's data as if it were victim_object
```

Les allocateurs modernes (tcmalloc, jemalloc, PartitionAlloc) séparent les allocations par classe de taille et ajoutent des mécanismes de durcissement, mais l'exploitation de UAF reste possible via des séquences d'allocations contrôlées.

---

## Causes racines {#root-causes}

### 1. Pointeur pendant après libération {#1-dangling-pointer-after-free}

```c
// VULNERABLE: pointer not nulled after free
typedef struct { char name[32]; void (*callback)(void); } Handler;

void cleanup(Handler *h) {
    free(h);
    // h is now dangling - caller still holds the original pointer
}

void process_event(Handler *h, int event) {
    cleanup(h);
    if (event == RETRY) {
        h->callback();   // UAF: h was freed above; h->callback reads freed memory
    }
}
```

```c
// FIXED: null the pointer after free; check before use
void cleanup(Handler **h) {
    free(*h);
    *h = NULL;   // caller's pointer is nulled
}

void process_event(Handler **h, int event) {
    cleanup(h);
    if (event == RETRY && *h != NULL) {   // null check prevents UAF
        (*h)->callback();
    }
}
```

**Remarque :** annuler le pointeur empêche l'UAF via ce pointeur précis, mais pas via des *alias* (d'autres pointeurs référençant la même allocation). Les alias constituent le cas difficile.

### 2. Double libération {#2-double-free}

```c
// VULNERABLE: error path frees twice
int parse_message(Message *msg) {
    char *buf = malloc(msg->len);
    if (!buf) return -1;

    if (read_data(buf, msg->len) < 0) {
        free(buf);    // free on error
        return -1;
    }

    int result = process(buf);
    free(buf);        // free on success
    if (result < 0) {
        free(buf);    // BUG: double-free if process() returned error after buf was freed
    }
    return result;
}
```

```c
// FIXED: single ownership, one free path
int parse_message(Message *msg) {
    char *buf = malloc(msg->len);
    if (!buf) return -1;

    int result = -1;
    if (read_data(buf, msg->len) >= 0) {
        result = process(buf);
    }
    free(buf);   // single free, always executed
    return result;
}
```

Dans les allocateurs modernes dotés de la détection de double libération de tcache, l'opération peut interrompre le programme avec le message « double free detected in tcache 2 ». Dans les anciens allocateurs ou avec des techniques de contournement, il s'agit d'une corruption de tas exploitable.

### 3. Invalidation d'itérateurs en C++ {#3-c-iterator-invalidation}

```cpp
// VULNERABLE: modifying container while iterating invalidates iterators
void remove_inactive(std::vector<Session*>& sessions) {
    for (auto it = sessions.begin(); it != sessions.end(); ++it) {
        if ((*it)->is_inactive()) {
            delete *it;           // frees the Session object
            sessions.erase(it);   // invalidates it AND all iterators after it
            // ++it in loop increment now dereferences invalid iterator: UB/crash
        }
    }
}
```

```cpp
// FIXED: erase returns valid next iterator; or use remove_if
void remove_inactive(std::vector<Session*>& sessions) {
    for (auto it = sessions.begin(); it != sessions.end(); ) {
        if ((*it)->is_inactive()) {
            delete *it;
            it = sessions.erase(it);   // erase returns next valid iterator
        } else {
            ++it;
        }
    }
    // Or idiomatically:
    // sessions.erase(
    //     std::remove_if(sessions.begin(), sessions.end(),
    //         [](Session* s) { bool r = s->is_inactive(); if(r) delete s; return r; }),
    //     sessions.end());
}
```

**Conteneurs STL qui invalident les itérateurs lors d'une modification :**
- `std::vector` : insert/erase/push_back (réallocation) invalide tous les itérateurs
- `std::deque` : insert/erase au milieu invalide tous les itérateurs ; les extrémités en invalident certains
- `std::unordered_map`/`unordered_set` : le rehachage invalide tous les itérateurs
- `std::list`/`std::map`/`std::set` : seuls les itérateurs vers les éléments effacés sont invalidés

### 4. Gestionnaire d'événements / callback accédant à un objet libéré {#4-event-handler-callback-accessing-freed-object}

```javascript
// JavaScript - conceptually UAF via closure (garbage-collected, but logic error pattern)
// In C++ event systems this is real UAF:

// C++ example
class Widget {
    ~Widget() { event_bus.unsubscribe(this); }  // MISSING: destructor doesn't unsubscribe
    void on_data(DataEvent& e) { this->process(e.data); }  // accesses this
};

// Elsewhere:
Widget *w = new Widget();
event_bus.subscribe("data", [w](DataEvent& e) { w->on_data(e); });
delete w;  // w freed but lambda still holds stale pointer in event_bus
// Next data event: lambda calls w->on_data() → UAF
```

```cpp
// FIXED: unsubscribe in destructor
class Widget {
    EventToken token_;
public:
    Widget() { token_ = event_bus.subscribe("data", [this](DataEvent& e) { on_data(e); }); }
    ~Widget() { event_bus.unsubscribe(token_); }  // explicit unsubscription
    void on_data(DataEvent& e) { process(e.data); }
};
```

### 5. Condition de course : libération dans un thread, utilisation dans un autre {#5-race-condition-free-in-one-thread-use-in-another}

```c
// VULNERABLE: connection object freed in cleanup thread while worker uses it
typedef struct { int fd; char *buf; } Conn;

void *worker(void *arg) {
    Conn *c = (Conn *)arg;
    // ... uses c->buf, c->fd
    read(c->fd, c->buf, BUF_SIZE);   // race: c may be freed by cleanup thread
    return NULL;
}

void cleanup_thread(Conn *c) {
    free(c->buf);
    free(c);   // if worker is still running, UAF in worker
}
```

```c
// FIXED: reference counting with atomic ops
typedef struct { int fd; char *buf; _Atomic int refcount; } Conn;

Conn *conn_retain(Conn *c) { atomic_fetch_add(&c->refcount, 1); return c; }
void conn_release(Conn *c) {
    if (atomic_fetch_sub(&c->refcount, 1) == 1) {
        free(c->buf); free(c);
    }
}

void *worker(void *arg) {
    Conn *c = conn_retain((Conn *)arg);
    read(c->fd, c->buf, BUF_SIZE);
    conn_release(c);
    return NULL;
}
```

### 6. UAF dans du Rust `unsafe` {#6-rust-unsafe-uaf}

```rust
// VULNERABLE: raw pointer use after deallocation
unsafe fn dangerous() {
    let b = Box::new(42i32);
    let ptr: *const i32 = &*b as *const i32;
    drop(b);               // b freed here
    println!("{}", *ptr);  // UAF: reads freed memory
}
```

```rust
// FIXED: use lifetime-tracked references; raw pointer only within known live scope
fn safe_version() -> i32 {
    let b = Box::new(42i32);
    let val = *b;  // copy the value before drop
    val            // return copy, not reference to freed memory
}
```

---

## Écosystèmes concernés {#affected-ecosystems}

| Langage | Risque | Remarques |
|---------|--------|-----------|
| C | Critique | Gestion manuelle de la mémoire, aucun suivi de durée de vie |
| C++ | Critique | `delete` + pointeurs bruts ; les pointeurs intelligents atténuent le risque s'ils sont utilisés de façon cohérente |
| C++ (pointeurs intelligents) | Moyen | Les cycles de `shared_ptr` empêchent la libération ; un mauvais usage de `weak_ptr` → pendant |
| Rust (sûr) | Aucun | Le vérificateur d'emprunts empêche les UAF à la compilation |
| Rust (unsafe) | Élevé | Les opérations sur pointeurs bruts contournent le vérificateur d'emprunts |
| Go | Très faible | Le GC empêche les UAF sur les objets gérés par le GC ; `unsafe.Pointer` peut provoquer un UAF |
| Java/Python/JS | Très faible | Le GC empêche les UAF ; des erreurs logiques sont possibles, mais pas d'UAF au niveau mémoire |

---

## Heuristiques de détection {#detection-heuristics}

**En C/C++ :**

1. `free(ptr)` suivi de toute lecture/écriture/appel via `ptr` ou un alias quelconque, sans `ptr = NULL` intermédiaire.
2. Rechercher `free(ptr)` dans des fonctions qui renvoient `ptr` ou qui stockent `ptr` ailleurs avant de le libérer : plusieurs propriétaires.
3. Motifs de destructeurs où un pointeur est stocké dans plusieurs structures : `A.ptr = p; B.ptr = p; delete p;` - B.ptr est désormais pendant.
4. Motifs de système d'événements : `subscribe(lambda capturant un pointeur brut)` sans `unsubscribe` correspondant dans le destructeur de l'objet pointé.
5. Conteneurs modifiés pendant leur parcours : boucles range-for avec `erase`, `insert`, `push_back` sur le conteneur parcouru.
6. Code multithread : `free()` dans une fonction, utilisation dans une autre, sans synchronisation sur le pointeur.

**Outils d'analyse statique :**
- Clang `scan-build` avec `alpha.cplusplus.STLAlgorithmModeling`
- Cppcheck : `--enable=warning` signale les UAF évidents
- Coverity : le contrôleur « USE_AFTER_FREE »
- CodeQL : `cpp/use-after-free`
- Valgrind `memcheck` : détection à l'exécution avec historique du tas

**Détection dynamique :**
- `-fsanitize=address` (ASan) : détecte les UAF à l'exécution ; signale les emplacements exacts de l'allocation, de la libération et de l'utilisation
- libdislocator (AFL) : randomise les allocations pour rendre les UAF plus susceptibles de provoquer un plantage pendant le fuzzing

---

## Schémas d'exploitation {#exploitation-patterns}

| Type d'exploitation | Mécanisme |
|---------------------|-----------|
| Confusion de types via UAF | Heap grooming : remplir la zone libérée avec un autre type ; le code d'origine la lit avec son type initial → valeurs de champs contrôlées |
| Écrasement de la table de fonctions virtuelles (vtable) | Objet avec vtable libéré ; nouvelle allocation placée à la même adresse ; l'attaquant contrôle le pointeur de vtable → appel virtuel arbitraire |
| Écrasement de pointeur de fonction | Libérer une structure contenant un pointeur de fonction ; la remplir avec une structure forgée ; le code appelle le pointeur de fonction → contrôle du PC |
| Fuite d'information via lecture UAF | Lire la zone libérée contenant des données sensibles d'une allocation adjacente |
| Double libération vers écriture arbitraire | Deux libérations → corruption des métadonnées du tas → valeur de retour de `malloc` contrôlée → primitive d'écriture |

---

## Schémas de correction {#fixing-patterns}

| Schéma | Application |
|--------|-------------|
| Annuler le pointeur après libération | `free(p); p = NULL;` - empêche l'utilisation via ce pointeur précis |
| `std::unique_ptr` / `std::shared_ptr` | La sémantique de propriété empêche la plupart des schémas d'UAF en C++ |
| Comptage de références | `shared_ptr`, compteur atomique personnalisé ; libération uniquement lorsque le compteur vaut 0 |
| RAII + durées de vie bornées à la portée | Durée de vie de la ressource liée à la portée ; pas de libération manuelle |
| `std::weak_ptr` pour les références arrière | Référence non propriétaire qui expire lorsque l'objet possédé est détruit |
| Récupération basée sur les époques (RCU) | Libération différée jusqu'à la fin de tous les lecteurs ; courant dans le code noyau et concurrent |
| Address Sanitizer en CI | Détecte les UAF à l'exécution ; indispensable pour les suites de tests C/C++ |
| Fuzzing avec ASan | AFL++/libFuzzer + ASan est la principale méthode de découverte des UAF dans les navigateurs et les analyseurs |

---

## Pièges - indicateurs de faux positifs {#gotchas-false-positive-indicators}

- **`free(p); p = malloc(new_size);`** - pointeur réutilisé pour une nouvelle allocation dans la même portée ; ce n'est pas un UAF s'il n'y a pas d'utilisation intermédiaire de l'ancienne valeur.
- **Extraction de pointeur brut à partir d'un pointeur intelligent pour interopérabilité :** `p.get()` passé à une API C qui ne prend pas la propriété - sûr tant que le propriétaire `unique_ptr`/`shared_ptr` survit à l'appel de l'API C.
- **`shared_ptr` passé à une lambda :** la lambda capture une copie du `shared_ptr`, ce qui prolonge la durée de vie ; l'objet pointé ne sera pas libéré avant la destruction de la lambda - pas d'UAF.
- **Allocateurs à pool :** `free` dans un contexte de pool restitue la mémoire au pool, pas au système d'exploitation ; une « utilisation » ultérieure lit une mémoire gérée par le pool qui n'a pas encore été écrasée par une autre allocation. Techniquement un UAF, mais souvent non exploitable sans grooming du pool.
- **Réallocation de `std::vector` :** `vec.push_back(x)` peut réallouer ; les références, itérateurs et pointeurs vers l'ancien stockage du vecteur sont invalidés, mais il s'agit d'une classe de bogue distincte (itérateur/référence pendant, et non UAF de pointeur au sens traditionnel).

---

## Voir aussi {#see-also}

- [[cwe-787-oob-write]] - souvent enchaînés : une lecture UAF divulgue une adresse, puis une écriture hors limites l'exploite
- CWE-125 : Lecture hors limites - erreur mémoire côté lecture ; la lecture UAF en est une sous-catégorie
- CWE-415 : Double libération - sous-type direct ; double libération → corruption du tas → impact équivalent à un UAF
- CWE-362 : Condition de course - cause racine concurrente d'un UAF
- CWE-672 : Opération sur une ressource après expiration - parent sémantique pour l'accès à une ressource expirée
