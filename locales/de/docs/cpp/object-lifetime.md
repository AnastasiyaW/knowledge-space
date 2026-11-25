---
title: "Objektlebensdauer und Konstruktion"
category: concepts
tags: [cpp, lifetime, constructor, destructor, initialization, copy-elision]
level: 4
source_sha256: 1c073217cf05f6e23fb5867a27fb03dd4e59307d1868b12ebe13d6a4f2e94d82
translation: machine
translated_at: '2026-10-24'
---
# Objektlebensdauer und Konstruktion {#object-lifetime-and-construction}

Objektkonstruktion, Destruktion, Initialisierungsformen und Copy Elision. Das Verständnis der Lebensdauer ist sowohl für Korrektheit als auch für Performance unverzichtbar.

## Wichtige Fakten {#key-facts}

- Lebensdauer eines Objekts: Konstruktion -> Verwendung -> Destruktion
- Reihenfolge der Konstruktion: Basisklassen (von links nach rechts) -> Member (in Deklarationsreihenfolge) -> Konstruktorrumpf
- Reihenfolge der Destruktion: umgekehrt zur Konstruktion
- Member-Initialisierungsliste: wird gegenüber Zuweisung im Rumpf bevorzugt (konstruiert direkt, nicht Default-Konstruktion gefolgt von Zuweisung)
- Delegierende Konstruktoren (C++11): `MyClass(int x) : MyClass(x, 0) {}`
- `explicit`-Schlüsselwort: verhindert implizite Konvertierungen über Konstruktoren mit einem Argument
- Copy Elision (RVO/NRVO): der Compiler eliminiert Kopier- bzw. Verschiebeoperationen bei der Rückgabe – in C++17 verpflichtend
- Aggregat-Initialisierung: `Type{1, 2, 3}` für Structs und Arrays ohne benutzerdefinierte Konstruktoren
- Designierte Initialisierer (C++20): `Point{.x=1, .y=2}`
- Statische lokale Variablen: werden einmalig initialisiert, ab C++11 thread-sicher
- Verlängerung der Lebensdauer temporärer Objekte: Bindung eines rvalue an `const T&` verlängert die Lebensdauer bis zum Ende des Gültigkeitsbereichs der Referenz

## Muster {#patterns}

### Konstruktorformen {#constructor-forms}

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

### Initialisierungssyntax {#initialization-syntax}

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

### Rule of Zero / Five {#rule-of-zero-five}

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

### Copy Elision / RVO {#copy-elision-rvo}

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

### Statisch und Thread-Local {#static-and-thread-local}

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

## Fallstricke {#gotchas}

- **Problem:** Most Vexing Parse: `Widget w();` deklariert eine Funktion, kein Objekt -> **Lösung:** `Widget w{};` oder `Widget w;` für die Default-Konstruktion verwenden
- **Problem:** Überraschungen bei geschweifter Initialisierung mit Überladung für `std::initializer_list`: `vector<int>{10}` erzeugt einen Vektor mit einem Element (Wert 10), nicht einen Vektor mit 10 Elementen -> **Lösung:** `vector<int>(10)` für den Konstruktor mit Anzahl verwenden, `vector<int>{10}` für eine Liste mit einem einzelnen Element
- **Problem:** Reihenfolge in der Member-Initialisierungsliste stimmt nicht mit der Deklarationsreihenfolge überein -> Member werden unabhängig davon in Deklarationsreihenfolge initialisiert -> **Lösung:** Initialisierungsliste immer in derselben Reihenfolge wie die Member-Deklarationen schreiben. `-Wreorder` aktivieren.
- **Problem:** Temporäres Objekt, das an einen `const T&`-Parameter im Konstruktor gebunden und als Member gespeichert wird -> nach dem Konstruktor hängende Referenz -> **Lösung:** Per Wert übernehmen und verschieben, oder per `string_view` übernehmen und in den String-Member kopieren

## Siehe auch {#see-also}

- [[raii-resource-management]]
- [[move-semantics]]
- [Smart Pointers und Speicherverwaltung](smart-pointers.md)
- [[const-and-type-safety]]
