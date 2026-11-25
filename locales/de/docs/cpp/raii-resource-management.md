---
title: "RAII und Ressourcenverwaltung"
category: concepts
tags: [cpp, raii, memory, lifetime, resource, destructor]
level: 4
source_sha256: 1304dbda07d26b10ab48e97136da1929eb9c552631d97256fb7ef3c48a5a8190
translation: machine
translated_at: '2026-10-24'
---
# RAII und Ressourcenverwaltung {#raii-and-resource-management}

Resource Acquisition Is Initialization: Die Lebensdauer einer Ressource wird an die Lebensdauer eines Objekts gebunden. Der Konstruktor erwirbt die Ressource, der Destruktor gibt sie frei. Das wichtigste C++-Idiom überhaupt.

## Wichtige Fakten {#key-facts}

- RAII garantiert die Bereinigung über den Destruktor, auch bei Exceptions (Stack-Unwinding)
- Jede Ressource (Speicher, Dateien, Locks, Sockets, Handles) sollte von einem RAII-Wrapper verwaltet werden
- Auf dem Stack angelegte RAII-Objekte werden in umgekehrter Reihenfolge ihrer Konstruktion zerstört
- Ein Destruktor darf keine Exceptions werfen. Tut er es während des Stack-Unwindings, wird `std::terminate` aufgerufen
- Standard-RAII-Wrapper: `unique_ptr`, `shared_ptr`, `lock_guard`, `unique_lock`, `fstream`, `string`, `vector`
- Rohes `new`/`delete` sollte in modernem C++ praktisch nie vorkommen. Stattdessen [Smart Pointers und Speicherverwaltung](smart-pointers.md) oder Container verwenden
- Kopiersemantik: tiefe Kopie oder Kopieren deaktivieren (`= delete`)
- Move-Semantik: Eigentum günstig übertragen, siehe [[move-semantics]]
- Rule of Zero > Rule of Five > manuelle Verwaltung

## Muster {#patterns}

### Einfacher RAII-Wrapper {#basic-raii-wrapper}

```cpp
class FileHandle {
    FILE* fp_;
public:
    explicit FileHandle(const char* path, const char* mode)
        : fp_(fopen(path, mode)) {
        if (!fp_) throw std::runtime_error("Cannot open file");
    }

    ~FileHandle() {
        if (fp_) fclose(fp_);
    }

    // Non-copyable
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    // Movable
    FileHandle(FileHandle&& other) noexcept : fp_(other.fp_) {
        other.fp_ = nullptr;
    }
    FileHandle& operator=(FileHandle&& other) noexcept {
        if (this != &other) {
            if (fp_) fclose(fp_);
            fp_ = other.fp_;
            other.fp_ = nullptr;
        }
        return *this;
    }

    FILE* get() const { return fp_; }
};
```

### Lock-Guard-Muster {#lock-guard-pattern}

```cpp
std::mutex mtx;

void safe_operation() {
    std::lock_guard<std::mutex> lock(mtx);  // acquires lock
    // ... critical section ...
}  // lock released automatically, even if exception thrown

// C++17 CTAD
void modern() {
    std::lock_guard lock(mtx);   // template args deduced
}

// For more control, use unique_lock
void flexible() {
    std::unique_lock lock(mtx);
    // can unlock/relock, use with condition_variable
    lock.unlock();
    // ... non-critical work ...
    lock.lock();
}
```

### Scope Guard (generisches RAII) {#scope-guard-generic-raii}

```cpp
template<typename F>
class ScopeGuard {
    F cleanup_;
    bool active_ = true;
public:
    explicit ScopeGuard(F f) : cleanup_(std::move(f)) {}
    ~ScopeGuard() { if (active_) cleanup_(); }
    void dismiss() { active_ = false; }

    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
};

// Usage
void transactional_work() {
    begin_transaction();
    auto guard = ScopeGuard([] { rollback_transaction(); });

    do_step_1();
    do_step_2();
    commit_transaction();
    guard.dismiss();  // success - don't rollback
}
```

### Rule of Zero {#rule-of-zero}

```cpp
// Best practice: let compiler-generated defaults handle everything
class Person {
    std::string name_;                    // manages its own memory
    std::vector<std::string> aliases_;    // manages its own memory
    std::unique_ptr<Address> address_;    // manages its own memory

    // No destructor, no copy/move ops needed
    // Compiler generates correct versions automatically
};
```

### Reihenfolge von Konstruktor und Destruktor {#constructordestructor-order}

```cpp
class Base {
public:
    Base()  { std::cout << "Base ctor\n"; }
    ~Base() { std::cout << "Base dtor\n"; }
};

class Member {
public:
    Member()  { std::cout << "Member ctor\n"; }
    ~Member() { std::cout << "Member dtor\n"; }
};

class Derived : public Base {
    Member m_;
public:
    Derived()  { std::cout << "Derived ctor\n"; }
    ~Derived() { std::cout << "Derived dtor\n"; }
};

// Construction order:  Base -> Member -> Derived body
// Destruction order:   Derived body -> Member -> Base
```

## Fallstricke {#gotchas}

- **Problem:** Der Destruktor wirft während des Stack-Unwindings -> `std::terminate` wird aufgerufen -> **Lösung:** Destruktoren müssen `noexcept` sein (seit C++11 implizit). Exceptions innerhalb des Destruktors abfangen.
- **Problem:** Rohes `new` ohne passendes `delete`. Bei einer Exception zwischen Allokation und Zuweisung entsteht ein Speicherleck -> **Lösung:** `make_unique`/`make_shared` verwenden, niemals rohes `new`
- **Problem:** Virtueller Destruktor in einer polymorphen Basisklasse vergessen -> undefiniertes Verhalten beim Löschen eines abgeleiteten Objekts über einen Basiszeiger -> **Lösung:** Eine Basisklasse mit virtuellen Funktionen muss `virtual ~Base() = default;` deklarieren
- **Problem:** Member werden in der falschen Reihenfolge initialisiert (Reihenfolge in der Initialisierungsliste vs. Deklarationsreihenfolge) -> **Lösung:** Die Reihenfolge in der Member-Initialisierungsliste muss der Deklarationsreihenfolge entsprechen. Der Compiler warnt mit `-Wreorder`.

## Siehe auch {#see-also}

- [Smart Pointers und Speicherverwaltung](smart-pointers.md)
- [[move-semantics]]
- [Fehlerbehandlung - Exceptions und Alternativen](error-handling.md)
- [[object-lifetime]]
