---
title: "Smart Pointer und Speicherverwaltung"
category: concepts
tags: [cpp, memory, raii, smart-pointers, cpp11, cpp14]
level: 3
source_sha256: 5e4fc8592d5e2172ec9a5ef181800bbaa017f4b673d6d2047a1034856a8d0d6e
translation: machine
translated_at: '2026-10-24'
---
# Smart Pointer und Speicherverwaltung {#smart-pointers-and-memory-management}

Besitzbasierte Speicherverwaltung über `unique_ptr`, `shared_ptr` und `weak_ptr`. Zentraler Mechanismus, um manuelles `new`/`delete` zu vermeiden und Speicherlecks zu verhindern.

## Wichtige Fakten {#key-facts}

- Smart Pointer sind im Header `<memory>` definiert
- `std::unique_ptr` - alleiniges Eigentum, kein Mehraufwand gegenüber einem Rohzeiger, nicht kopierbar, verschiebbar
- `std::shared_ptr` - referenzgezählter geteilter Besitz, thread-sicherer Referenzzähler, ca. doppelte Zeigergröße (Control Block)
- `std::weak_ptr` - nicht besitzender Beobachter eines `shared_ptr`, durchbricht zirkuläre Referenzen
- Bevorzuge immer `std::make_unique` (C++14) und `std::make_shared` (C++11) gegenüber direktem `new`
- `make_shared` reserviert Objekt und Control Block in einer einzigen Allokation (cache-freundlich)
- `unique_ptr` kann Arrays halten: `std::unique_ptr<int[]> arr(new int[10]);`
- Benutzerdefinierte Deleter: `unique_ptr<FILE, decltype(&fclose)> f(fopen("x","r"), &fclose);`
- Der Aliasing-Konstruktor von `shared_ptr` erlaubt es, auf Unterobjekte zu zeigen und dabei das Eigentum am übergeordneten Objekt zu teilen
- [[raii-resource-management]] ist die Grundlage: Smart Pointer sind RAII für Heap-Speicher

## Muster {#patterns}

### unique_ptr - Standardwahl {#unique_ptr-default-choice}

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

### shared_ptr - Geteiltes Eigentum {#shared_ptr-shared-ownership}

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

### weak_ptr - Zyklen aufbrechen {#weak_ptr-breaking-cycles}

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

### unique_ptr mit benutzerdefiniertem Deleter {#unique_ptr-with-custom-deleter}

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

## Fallstricke {#gotchas}

- **Problem:** Übergabe von `this` an `shared_ptr` erzeugt einen separaten Control Block, was beim Zerstören zu einem Double-Free führt -> **Lösung:** Von `std::enable_shared_from_this<T>` erben und die Methode `shared_from_this()` verwenden
- **Problem:** `make_shared` verzögert die Freigabe, wenn ein `weak_ptr` existiert: Der Control Block hält den Speicher auch dann noch am Leben, wenn alle `shared_ptr` bereits zerstört sind -> **Lösung:** Bei großen Objekten mit langlebigen Beobachtern stattdessen `shared_ptr(new T(...))` verwenden
- **Problem:** Zirkuläre `shared_ptr`-Referenzen verursachen Speicherlecks (der Referenzzähler erreicht nie 0) -> **Lösung:** Für Rückreferenzen bzw. Elternzeiger `weak_ptr` verwenden
- **Problem:** `shared_ptr<T>` auf ein Array benötigt vor C++17 einen benutzerdefinierten Deleter -> **Lösung:** `shared_ptr<T[]>` (C++17), `unique_ptr<T[]>` oder einfach `std::vector<T>` verwenden
- **Problem:** Mehrere `shared_ptr` aus demselben Rohzeiger erzeugen -> **Lösung:** Niemals zwei `shared_ptr` aus demselben Rohzeiger erstellen. `make_shared` verwenden oder einen bestehenden `shared_ptr` übergeben
- **Problem:** Verwendung von `get()` und Speichern des Rohzeigers über die Lebensdauer des Smart Pointers hinaus -> **Lösung:** `get()` nur für kurzzeitigen Zugriff verwenden und das Ergebnis niemals speichern

## Siehe auch {#see-also}

- [[raii-resource-management]]
- [[move-semantics]]
- [[object-lifetime]]
- [cppreference: unique_ptr](https://en.cppreference.com/w/cpp/memory/unique_ptr)
- [cppreference: shared_ptr](https://en.cppreference.com/w/cpp/memory/shared_ptr)
