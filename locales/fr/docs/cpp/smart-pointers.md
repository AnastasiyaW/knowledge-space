---
title: "Pointeurs intelligents et gestion de la mémoire"
category: concepts
tags: [cpp, memory, raii, smart-pointers, cpp11, cpp14]
level: 3
source_sha256: 5e4fc8592d5e2172ec9a5ef181800bbaa017f4b673d6d2047a1034856a8d0d6e
translation: machine
translated_at: '2026-10-24'
---
# Pointeurs intelligents et gestion de la mémoire {#smart-pointers-and-memory-management}

Gestion de la mémoire fondée sur la propriété, avec `unique_ptr`, `shared_ptr` et `weak_ptr`. C'est le mécanisme central pour éliminer les `new`/`delete` manuels et prévenir les fuites.

## Points clés {#key-facts}

- Les pointeurs intelligents sont définis dans l'en-tête `<memory>`
- `std::unique_ptr` - propriété exclusive, aucun surcoût par rapport à un pointeur brut, non copiable, déplaçable
- `std::shared_ptr` - propriété partagée par comptage de références, compteur de références thread-safe, taille d'environ 2 fois celle d'un pointeur (bloc de contrôle)
- `std::weak_ptr` - observateur sans propriété d'un `shared_ptr`, permet de rompre les références circulaires
- Toujours privilégier `std::make_unique` (C++14) et `std::make_shared` (C++11) plutôt que `new` direct
- `make_shared` alloue l'objet et le bloc de contrôle en une seule allocation (favorable au cache)
- `unique_ptr` peut contenir des tableaux : `std::unique_ptr<int[]> arr(new int[10]);`
- Déleteurs personnalisés : `unique_ptr<FILE, decltype(&fclose)> f(fopen("x","r"), &fclose);`
- Le constructeur d'alias (aliasing constructor) de `shared_ptr` permet de pointer vers des sous-objets tout en partageant la propriété de l'objet parent
- [[raii-resource-management]] est la base : les pointeurs intelligents sont du RAII pour la mémoire sur le tas

## Patterns {#patterns}

### unique_ptr - Choix par défaut {#unique_ptr-default-choice}

```cpp
// Creation - always use make_unique
auto widget = std::make_unique<Widget>(42, "hello");

// Transfer ownership
auto other = std::move(widget);  // widget is now nullptr

// Factory pattern - return unique_ptr
std::unique_ptr<Base> create(int type) {
    switch (type) {
        case 1: return std::make_unique<DerivedA>();
        case 2: return std::make_unique<DerivedB>();
        default: return nullptr;
    }
}

// Pass to sink (transfers ownership)
void consume(std::unique_ptr<Widget> w);

// Pass for use (no ownership transfer)
void use(Widget& w);           // preferred
void use(Widget* w);           // if nullable
```

### shared_ptr - Propriété partagée {#shared_ptr-shared-ownership}

```cpp
auto sp = std::make_shared<Widget>(42);
auto sp2 = sp;  // ref count = 2

// Get ref count (debugging only, not for logic)
std::cout << sp.use_count();  // 2

// Custom deleter
auto sp3 = std::shared_ptr<Widget>(new Widget(1),
    [](Widget* w) {
        log("deleting widget");
        delete w;
    });

// Aliasing constructor - share ownership of parent, point to member
struct Node { int value; };
auto node = std::make_shared<Node>();
std::shared_ptr<int> val(node, &node->value);
```

### weak_ptr - Rupture des cycles {#weak_ptr-breaking-cycles}

```cpp
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;    // weak to break cycle
};

// Using weak_ptr
std::weak_ptr<Widget> wp = sp;
if (auto locked = wp.lock()) {  // returns shared_ptr or nullptr
    locked->doSomething();
}
// Or check without locking
if (!wp.expired()) { /* might still expire before use */ }
```

### unique_ptr avec déleteur personnalisé {#unique_ptr-with-custom-deleter}

```cpp
// C-style resource management
auto file = std::unique_ptr<FILE, decltype(&fclose)>(
    fopen("data.txt", "r"), &fclose);

// SDL example
auto window = std::unique_ptr<SDL_Window, decltype(&SDL_DestroyWindow)>(
    SDL_CreateWindow("App", 0, 0, 800, 600, 0),
    &SDL_DestroyWindow);

// Lambda deleter (note: changes unique_ptr size)
auto p = std::unique_ptr<int, std::function<void(int*)>>(
    new int(42),
    [](int* p) { std::cout << "deleting\n"; delete p; });
```

## Pièges {#gotchas}

- **Problème :** Passer `this` à un `shared_ptr` crée un bloc de contrôle distinct, d'où une double libération à la destruction -> **Correction :** Hériter de `std::enable_shared_from_this<T>` et utiliser la méthode `shared_from_this()`
- **Problème :** `make_shared` retarde la libération lorsqu'un `weak_ptr` existe : le bloc de contrôle maintient la mémoire en vie même après la destruction de tous les `shared_ptr` -> **Correction :** Pour les gros objets avec des observateurs de longue durée, utiliser `shared_ptr(new T(...))` à la place
- **Problème :** Les références `shared_ptr` circulaires provoquent des fuites mémoire (le compteur de références n'atteint jamais 0) -> **Correction :** Utiliser `weak_ptr` pour les références arrière et les pointeurs vers le parent
- **Problème :** Un `shared_ptr<T>` vers un tableau, avant C++17, nécessite un déleteur personnalisé -> **Correction :** Utiliser `shared_ptr<T[]>` (C++17), `unique_ptr<T[]>` ou simplement `std::vector<T>`
- **Problème :** Construire plusieurs `shared_ptr` à partir du même pointeur brut -> **Correction :** Ne jamais créer deux `shared_ptr` à partir du même pointeur brut. Utiliser `make_shared` ou transmettre un `shared_ptr` existant
- **Problème :** Utiliser `get()` et conserver le pointeur brut au-delà de la durée de vie du pointeur intelligent -> **Correction :** N'utiliser `get()` que pour un accès transitoire, ne jamais stocker le résultat

## Voir aussi {#see-also}

- [[raii-resource-management]]
- [[move-semantics]]
- [[object-lifetime]]
- [cppreference : unique_ptr](https://en.cppreference.com/w/cpp/memory/unique_ptr)
- [cppreference : shared_ptr](https://en.cppreference.com/w/cpp/memory/shared_ptr)
