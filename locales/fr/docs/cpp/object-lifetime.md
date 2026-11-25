---
title: "Durée de vie et construction des objets"
category: concepts
tags: [cpp, lifetime, constructor, destructor, initialization, copy-elision]
level: 4
source_sha256: 1c073217cf05f6e23fb5867a27fb03dd4e59307d1868b12ebe13d6a4f2e94d82
translation: machine
translated_at: '2026-10-24'
---
# Durée de vie et construction des objets {#object-lifetime-and-construction}

Construction et destruction des objets, formes d'initialisation et élision de copie. Comprendre la durée de vie est essentiel pour la correction et la performance.

## Points clés {#key-facts}

- Durée de vie d'un objet : construction -> utilisation -> destruction
- Ordre de construction : classes de base (de gauche à droite) -> membres (ordre de déclaration) -> corps du constructeur
- Ordre de destruction : inverse de l'ordre de construction
- Liste d'initialisation des membres : à privilégier par rapport à l'affectation dans le corps (construction directe, sans construction par défaut suivie d'une affectation)
- Constructeurs délégants (C++11) : `MyClass(int x) : MyClass(x, 0) {}`
- Mot-clé `explicit` : empêche les conversions implicites via un constructeur à un seul argument
- Élision de copie (RVO/NRVO) : le compilateur supprime la copie ou le déplacement lors du retour - obligatoire en C++17
- Initialisation d'agrégat : `Type{1, 2, 3}` pour les structures et tableaux sans constructeur défini par l'utilisateur
- Initialisateurs désignés (C++20) : `Point{.x=1, .y=2}`
- Variables locales statiques : initialisées une seule fois, thread-safe depuis C++11
- Extension de la durée de vie des temporaires : lier une rvalue à `const T&` prolonge sa durée de vie à celle de la portée de la référence

## Modèles {#patterns}

### Formes de constructeurs {#constructor-forms}

```cpp
class Widget {
    int id_;
    std::string name_;
    std::vector<int> data_;
public:
    // Default constructor
    Widget() : id_(0), name_("default") {}

    // Parameterized - use initializer list
    Widget(int id, std::string name)
        : id_(id), name_(std::move(name)) {}  // move string into member

    // Delegating constructor
    Widget(int id) : Widget(id, "unnamed") {}

    // Explicit - prevent implicit conversion from int
    explicit Widget(double d) : Widget(static_cast<int>(d)) {}

    // In-class member initializers (C++11)
    int priority_ = 0;              // default if not in init list
    bool active_ = true;
};
```

### Syntaxe d'initialisation {#initialization-syntax}

```cpp
// Direct initialization
int a(42);
std::string s("hello");

// Copy initialization
int b = 42;
std::string s2 = "hello";

// List initialization (C++11) - narrowing-safe
int c{42};
// int d{3.14};  // ERROR: narrowing from double to int

// Aggregate initialization
struct Point { double x, y, z; };
Point p1{1.0, 2.0, 3.0};
Point p2{.x = 1.0, .y = 2.0};  // C++20 designated initializers

// std::initializer_list
std::vector<int> v{1, 2, 3, 4, 5};

// Default initialization vs value initialization
int* a1 = new int;     // indeterminate value (default init)
int* a2 = new int();   // zero (value init)
int* a3 = new int{};   // zero (value init via list init)
```

### Règle du zéro / des cinq {#rule-of-zero-five}

```cpp
// Rule of Zero: let standard types manage resources
struct Employee {
    std::string name;
    std::vector<std::string> skills;
    std::unique_ptr<Address> address;
    // No special member functions needed - compiler generates correct ones
};

// Rule of Five: when managing a raw resource
class RawBuffer {
    size_t size_;
    char* data_;
public:
    explicit RawBuffer(size_t n) : size_(n), data_(new char[n]) {}

    ~RawBuffer() { delete[] data_; }

    RawBuffer(const RawBuffer& other)
        : size_(other.size_), data_(new char[other.size_]) {
        std::memcpy(data_, other.data_, size_);
    }

    RawBuffer& operator=(const RawBuffer& other) {
        if (this != &other) {
            auto tmp = RawBuffer(other);
            std::swap(size_, tmp.size_);
            std::swap(data_, tmp.data_);
        }
        return *this;
    }

    RawBuffer(RawBuffer&& other) noexcept
        : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }

    RawBuffer& operator=(RawBuffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }
};
```

### Élision de copie / RVO {#copy-elision-rvo}

```cpp
// Guaranteed copy elision (C++17) - no copy/move constructor needed
Widget create() {
    return Widget(42, "test");  // constructed directly in caller
}

// Named Return Value Optimization (NRVO) - not guaranteed but common
Widget build() {
    Widget w(1, "build");
    w.configure();
    return w;  // usually elided, otherwise moved
}

// Passing temporary to function
void consume(Widget w);
consume(Widget(42, "tmp"));  // elided: constructed directly in parameter
```

### Statique et thread-local {#static-and-thread-local}

```cpp
// Function-local static: initialized once, thread-safe (C++11)
Logger& get_logger() {
    static Logger instance;  // Meyers' Singleton
    return instance;
}

// Thread-local storage
thread_local int tls_counter = 0;
void per_thread_work() {
    ++tls_counter;  // each thread has its own copy
}
```

## Pièges {#gotchas}

- **Problème :** Most vexing parse : `Widget w();` déclare une fonction et non un objet -> **Correction :** Utiliser `Widget w{};` ou `Widget w;` pour une construction par défaut
- **Problème :** Les surprises de l'initialisation entre accolades avec une surcharge `std::initializer_list` : `vector<int>{10}` crée un vecteur d'un seul élément de valeur 10, et non un vecteur de 10 éléments -> **Correction :** Utiliser `vector<int>(10)` pour le constructeur basé sur le nombre d'éléments, et `vector<int>{10}` pour une liste à un seul élément
- **Problème :** L'ordre de la liste d'initialisation des membres ne correspond pas à l'ordre de déclaration -> les membres sont initialisés dans l'ordre de déclaration quoi qu'il arrive -> **Correction :** Toujours écrire la liste d'initialisation dans le même ordre que les déclarations des membres. Activer `-Wreorder`.
- **Problème :** Un temporaire lié à un paramètre `const T&` du constructeur, puis stocké comme membre -> référence pendante après le constructeur -> **Correction :** Prendre le paramètre par valeur puis le déplacer, ou le prendre par `string_view` et le copier dans le membre `string`

## Voir aussi {#see-also}

- [[raii-resource-management]]
- [[move-semantics]]
- [Pointeurs intelligents et gestion de la mémoire](smart-pointers.md)
- [[const-and-type-safety]]
