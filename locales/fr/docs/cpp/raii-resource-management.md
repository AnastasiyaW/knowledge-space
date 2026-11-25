---
title: "RAII et gestion des ressources"
category: concepts
tags: [cpp, raii, memory, lifetime, resource, destructor]
level: 4
source_sha256: 1304dbda07d26b10ab48e97136da1929eb9c552631d97256fb7ef3c48a5a8190
translation: machine
translated_at: '2026-10-24'
---
# RAII et gestion des ressources {#raii-and-resource-management}

Resource Acquisition Is Initialization : lier la durée de vie d'une ressource à celle d'un objet. Le constructeur acquiert la ressource, le destructeur la libère. C'est l'idiome C++ le plus important.

## Points clés {#key-facts}

- RAII garantit le nettoyage via le destructeur, même en cas d'exception (déroulement de la pile)
- Chaque ressource (mémoire, fichiers, verrous, sockets, handles) doit être possédée par un wrapper RAII
- Les objets RAII alloués sur la pile sont détruits dans l'ordre inverse de leur construction
- Le destructeur ne doit pas lever d'exception : si c'est le cas pendant un déroulement de pile, `std::terminate` est appelée
- Wrappers RAII standard : `unique_ptr`, `shared_ptr`, `lock_guard`, `unique_lock`, `fstream`, `string`, `vector`
- Les `new`/`delete` bruts ne devraient presque jamais apparaître en C++ moderne : utilisez [Pointeurs intelligents et gestion de la mémoire](smart-pointers.md) ou des conteneurs
- Sémantique de copie : copie profonde ou désactivation de la copie (`= delete`)
- Sémantique de déplacement : transférer la propriété à moindre coût, voir [[move-semantics]]
- Rule of Zero > Rule of Five > gestion manuelle

## Patrons {#patterns}

### Wrapper RAII de base {#basic-raii-wrapper}

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

### Patron Lock Guard {#lock-guard-pattern}

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

### Scope Guard (RAII générique) {#scope-guard-generic-raii}

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

### Ordre constructeur/destructeur {#constructordestructor-order}

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

## Pièges courants {#gotchas}

- **Problème :** le destructeur lève une exception pendant le déroulement de la pile -> `std::terminate` est appelée -> **Correction :** les destructeurs doivent être `noexcept` (implicite depuis C++11). Interceptez les exceptions à l'intérieur du destructeur.
- **Problème :** `new` brut sans `delete` correspondant - fuite en cas d'exception entre l'allocation et l'affectation -> **Correction :** utilisez `make_unique`/`make_shared`, jamais `new` brut
- **Problème :** oubli du destructeur virtuel dans une classe de base polymorphe -> comportement indéfini lors de la suppression d'un objet dérivé via un pointeur de base -> **Correction :** une classe de base possédant des fonctions virtuelles doit déclarer `virtual ~Base() = default;`
- **Problème :** membres initialisés dans le mauvais ordre (ordre de la liste d'initialisation par rapport à l'ordre de déclaration) -> **Correction :** l'ordre de la liste d'initialisation des membres doit correspondre à l'ordre de déclaration. Le compilateur émet un avertissement avec `-Wreorder`.

## Voir aussi {#see-also}

- [Pointeurs intelligents et gestion de la mémoire](smart-pointers.md)
- [[move-semantics]]
- [Gestion des erreurs - exceptions et alternatives](error-handling.md)
- [[object-lifetime]]
