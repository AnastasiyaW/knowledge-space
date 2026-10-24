---
title: "Sémantique de déplacement et transfert parfait"
category: concepts
tags: [cpp, move, rvalue, forwarding, cpp11, performance]
level: 3
source_sha256: bd516295bc8fffdb79458998c5d3dc4d2c34eaae01c25e09bf0e76aac6e2d35d
translation: machine
translated_at: '2026-10-24'
---
# Sémantique de déplacement et transfert parfait {#move-semantics-and-perfect-forwarding}

Transférer les ressources au lieu de les copier. Les références rvalue (`T&&`) permettent les constructeurs de déplacement et l'affectation par déplacement, ce qui élimine les copies profondes inutiles.

## Points clés {#key-facts}

- lvalue = possède une identité, on peut en prendre l'adresse ; rvalue = temporaire, sur le point d'être détruit
- `T&&` est une référence rvalue : elle se lie aux temporaires
- `std::move(x)` est simplement un cast vers `T&&` : il ne déplace rien, il permet seulement le déplacement
- Après `std::move`, la source est dans un état valide mais non spécifié : ne pas la lire
- Constructeur de déplacement : `Widget(Widget&& other) noexcept`
- Affectation par déplacement : `Widget& operator=(Widget&& other) noexcept`
- Marquer les opérations de déplacement `noexcept` : les conteneurs de la STL utilisent `std::move_if_noexcept` pour garantir une forte garantie d'exception
- Rule of Five : si vous définissez l'un parmi destructeur, constructeur de copie, affectation par copie, constructeur de déplacement et affectation par déplacement, définissez les cinq
- Rule of Zero : privilégier les classes qui n'ont besoin d'aucun des cinq (utiliser des pointeurs intelligents et des conteneurs standard)
- `std::forward<T>(arg)` préserve la catégorie de valeur dans le code template : c'est la base du transfert parfait
- Le compilateur génère implicitement les déplacements s'il n'y a ni opération de copie, ni opération de déplacement, ni destructeur déclarés par l'utilisateur

## Patrons {#patterns}

### Constructeur et affectation par déplacement {#move-constructor-and-assignment}

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

### Transfert parfait {#perfect-forwarding}

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

### Optimisation de la valeur de retour (RVO/NRVO) {#return-value-optimization-rvonrvo}

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

### Paramètres « sink » {#sink-parameters}

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

## Pièges {#gotchas}

- **Problème :** utiliser un objet après `std::move` conduit à lire un état déplacé → **Correction :** n'affecter ou ne détruire les objets déplacés, sans jamais lire leur valeur
- **Problème :** un constructeur de déplacement sans `noexcept` fait que la réallocation de `std::vector` revient à une copie → **Correction :** marquer systématiquement `noexcept` les opérations de déplacement qui ne peuvent pas lever d'exception
- **Problème :** `std::move` sur un objet `const` appelle silencieusement le constructeur de copie → **Correction :** ne jamais déplacer depuis un objet `const` : le `const` empêche le déplacement
- **Problème :** `return std::move(local)` empêche la NRVO → **Correction :** écrire simplement `return local;` : le compilateur applique la NRVO ou le déplacement implicite
- **Problème :** la référence de transfert `T&&` est confondue avec une référence rvalue → **Correction :** `T&&` n'est une référence de transfert que lorsque `T` est un paramètre template déduit. `Widget&&` est toujours une référence rvalue.

## Voir aussi {#see-also}

- [Pointeurs intelligents et gestion de la mémoire](smart-pointers.md)
- [[raii-resource-management]]
- [[templates-and-concepts]]
- [cppreference : move](https://en.cppreference.com/w/cpp/utility/move)
