---
title: "Move-Semantik und perfekte Weiterleitung"
category: concepts
tags: [cpp, move, rvalue, forwarding, cpp11, performance]
level: 3
source_sha256: bd516295bc8fffdb79458998c5d3dc4d2c34eaae01c25e09bf0e76aac6e2d35d
translation: machine
translated_at: '2026-10-24'
---
# Move-Semantik und perfekte Weiterleitung {#move-semantics-and-perfect-forwarding}

Ressourcen werden übertragen, statt sie zu kopieren. Rvalue-Referenzen (`T&&`) ermöglichen Move-Konstruktoren und Move-Zuweisungsoperatoren und vermeiden unnötige tiefe Kopien.

## Wichtige Fakten {#key-facts}

- lvalue = hat Identität, Adresse kann ermittelt werden; rvalue = temporäres Objekt, wird gleich zerstört
- `T&&` ist eine Rvalue-Referenz - bindet an temporäre Objekte
- `std::move(x)` ist nur ein Cast auf `T&&` - es verschiebt nichts, sondern ermöglicht nur das Verschieben
- Nach `std::move` befindet sich die Quelle in einem gültigen, aber unspezifizierten Zustand - nicht mehr lesen
- Move-Konstruktor: `Widget(Widget&& other) noexcept`
- Move-Zuweisungsoperator: `Widget& operator=(Widget&& other) noexcept`
- Move-Operationen mit `noexcept` markieren - STL-Container verwenden `std::move_if_noexcept` für die starke Ausnahmegarantie
- Rule of Five: Wenn du eines von Destruktor/Copy-Konstruktor/Copy-Zuweisung/Move-Konstruktor/Move-Zuweisung definierst, definiere alle fünf
- Rule of Zero: Klassen bevorzugen, die keine der fünf benötigen (Smart Pointer und Standardcontainer verwenden)
- `std::forward<T>(arg)` erhält die Wertkategorie in Template-Code - die Grundlage der perfekten Weiterleitung
- Der Compiler erzeugt Moves implizit, wenn keine benutzerdeklarierten Copy-Operationen, Move-Operationen oder kein Destruktor vorhanden sind

## Muster {#patterns}

### Move-Konstruktor und Move-Zuweisung {#move-constructor-and-assignment}

```cpp
class Buffer {
    size_t size_;
    int* data_;
public:
    // Move constructor - steal resources
    Buffer(Buffer&& other) noexcept
        : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;  // leave source in valid state
    }

    // Move assignment - release own, steal other's
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }

    // Copy-and-swap idiom handles both copy and move assignment
    // Buffer& operator=(Buffer other) { swap(*this, other); return *this; }
};
```

### Perfekte Weiterleitung {#perfect-forwarding}

```cpp
// Forward arguments preserving value category
template<typename T, typename... Args>
std::unique_ptr<T> make_unique_wrapper(Args&&... args) {
    return std::make_unique<T>(std::forward<Args>(args)...);
}

// Forwarding reference (T&& where T is deduced)
template<typename T>
void wrapper(T&& arg) {
    // If called with lvalue: T = Widget&, arg is Widget&
    // If called with rvalue: T = Widget, arg is Widget&&
    target(std::forward<T>(arg));
}
```

### Return Value Optimization (RVO/NRVO) {#return-value-optimization-rvonrvo}

```cpp
// Compiler elides copy/move entirely (mandatory in C++17)
Widget create() {
    Widget w(42);
    return w;  // NRVO: constructed directly in caller's space
}

// DON'T std::move the return value - it prevents NRVO
Widget bad_create() {
    Widget w(42);
    return std::move(w);  // WRONG: prevents NRVO
}
```

### Sink-Parameter {#sink-parameters}

```cpp
class Registry {
    std::vector<std::string> names_;
public:
    // By value + move: one interface for both lvalue and rvalue
    void add(std::string name) {
        names_.push_back(std::move(name));
    }
    // Called with lvalue: copy into param + move into vector
    // Called with rvalue: move into param + move into vector
};
```

## Fallstricke {#gotchas}

- **Problem:** Verwendung eines Objekts nach `std::move` führt zum Lesen des verschobenen Zustands -> **Lösung:** Verschobene Objekte nur neu zuweisen oder zerstören, niemals deren Wert lesen
- **Problem:** Move-Konstruktor ohne `noexcept` - beim Neuallokieren eines `std::vector` wird stattdessen kopiert -> **Lösung:** Move-Operationen immer mit `noexcept` markieren, wenn sie nicht werfen können
- **Problem:** `std::move` auf ein `const`-Objekt ruft stillschweigend den Kopierkonstruktor auf -> **Lösung:** Niemals aus `const`-Objekten verschieben - das `const` verhindert das Verschieben
- **Problem:** `return std::move(local)` verhindert NRVO -> **Lösung:** Einfach `return local;` schreiben - der Compiler wendet NRVO oder implizites Verschieben an
- **Problem:** Weiterleitungsreferenz `T&&` wird mit einer Rvalue-Referenz verwechselt -> **Lösung:** `T&&` ist nur dann eine Weiterleitungsreferenz, wenn `T` ein abgeleiteter Template-Parameter ist. `Widget&&` ist immer eine Rvalue-Referenz.

## Siehe auch {#see-also}

- [Smart Pointer und Speicherverwaltung](smart-pointers.md)
- [[raii-resource-management]]
- [[templates-and-concepts]]
- [cppreference: move](https://en.cppreference.com/w/cpp/utility/move)
