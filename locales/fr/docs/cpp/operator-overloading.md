---
title: "Surcharge d'opérateurs"
category: concepts
tags: [cpp, operators, overloading, comparison, streams]
level: 3
source_sha256: 29f1b2486cf6c3c44a68929e2513f31e40ad625760479b9c9d525ccd6758d1a9
translation: machine
translated_at: '2026-10-24'
---
# Surcharge d'opérateurs {#operator-overloading}

Définir un comportement personnalisé pour les opérateurs sur les types définis par l'utilisateur. Permet une syntaxe naturelle pour les types mathématiques, les conteneurs et les E/S.

## Points clés {#key-facts}

- Surchargeables : `+` `-` `*` `/` `%` `==` `!=` `<` `>` `<=` `>=` `<<` `>>` `[]` `()` `->` `++` `--` `<=>` et d'autres
- Non surchargeables : `::` `.` `.*` `?:` `sizeof` `typeid`
- Fonction membre ou libre : les opérateurs binaires sont généralement libres (symétriques), les opérateurs unaires sont généralement membres
- `operator<<` / `operator>>` pour les E/S sur flux doivent être des fonctions libres (l'opérande de gauche est un `ostream`/`istream`)
- `operator<=>` (C++20) : opérateur vaisseau spatial (spaceship) — une seule fonction génère les 6 comparaisons
- `operator()` rend l'objet appelable (foncteur)
- `operator[]` pour l'indexation : retourner une référence pour permettre l'affectation
- L'affectation composée (`+=`) devrait être membre ; le binaire (`+`) libre, défini en fonction de `+=`
- `explicit operator bool()` empêche la conversion implicite en bool dans des contextes indésirables
- Les opérateurs d'affectation par copie et par déplacement sont des fonctions membres spéciales (voir [[move-semantics]])

## Modèles {#patterns}

### Opérateurs arithmétiques {#arithmetic-operators}

```cpp
class Vec2 {
    double x_, y_;
public:
    Vec2(double x, double y) : x_(x), y_(y) {}

    // Compound assignment as member
    Vec2& operator+=(const Vec2& rhs) {
        x_ += rhs.x_;
        y_ += rhs.y_;
        return *this;
    }

    Vec2& operator*=(double s) {
        x_ *= s;
        y_ *= s;
        return *this;
    }

    Vec2 operator-() const { return {-x_, -y_}; }  // unary minus

    double x() const { return x_; }
    double y() const { return y_; }
};

// Binary as free function (using compound)
Vec2 operator+(Vec2 lhs, const Vec2& rhs) {
    return lhs += rhs;  // lhs is copy, modify and return
}

Vec2 operator*(Vec2 v, double s) { return v *= s; }
Vec2 operator*(double s, Vec2 v) { return v *= s; }  // commutative
```

### Opérateurs de comparaison (C++20 vaisseau spatial) {#comparison-operators-c20-spaceship}

```cpp
#include <compare>

class Version {
    int major_, minor_, patch_;
public:
    Version(int ma, int mi, int pa) : major_(ma), minor_(mi), patch_(pa) {}

    // Single operator generates ==, !=, <, >, <=, >=
    auto operator<=>(const Version&) const = default;
};

// Custom comparison logic
class CaseInsensitiveString {
    std::string str_;
public:
    std::strong_ordering operator<=>(const CaseInsensitiveString& other) const {
        // custom case-insensitive comparison
        auto a = to_lower(str_);
        auto b = to_lower(other.str_);
        return a <=> b;
    }
    bool operator==(const CaseInsensitiveString& other) const {
        return (*this <=> other) == 0;
    }
};
```

### Opérateurs d'E/S sur flux {#stream-io-operators}

```cpp
class Complex {
    double real_, imag_;
public:
    Complex(double r, double i) : real_(r), imag_(i) {}

    // Must be free function (ostream is left operand)
    friend std::ostream& operator<<(std::ostream& os, const Complex& c) {
        return os << c.real_ << "+" << c.imag_ << "i";
    }

    friend std::istream& operator>>(std::istream& is, Complex& c) {
        return is >> c.real_ >> c.imag_;
    }
};

Complex c(3, 4);
std::cout << c;  // prints: 3+4i
```

### Indexation et appel de fonction {#subscript-and-function-call}

```cpp
class Matrix {
    std::vector<double> data_;
    size_t cols_;
public:
    // Subscript (C++23: multidimensional)
    double& operator[](size_t r, size_t c) {  // C++23
        return data_[r * cols_ + c];
    }

    // Pre-C++23: proxy pattern
    struct Row {
        double* data;
        double& operator[](size_t c) { return data[c]; }
    };
    Row operator[](size_t r) { return {data_.data() + r * cols_}; }
};

// Functor - callable object
class Multiplier {
    int factor_;
public:
    explicit Multiplier(int f) : factor_(f) {}
    int operator()(int x) const { return x * factor_; }
};

Multiplier times3(3);
int result = times3(7);  // 21
```

### Opérateurs de conversion {#conversion-operators}

```cpp
class Rational {
    int num_, den_;
public:
    // Explicit conversion to double
    explicit operator double() const {
        return static_cast<double>(num_) / den_;
    }

    // Explicit conversion to bool (for if-statements)
    explicit operator bool() const {
        return num_ != 0;
    }
};

Rational r(3, 4);
double d = static_cast<double>(r);  // explicit required
if (r) { /* OK: explicit bool in boolean context */ }
// double d2 = r;  // ERROR: implicit conversion blocked by explicit
```

## Pièges {#gotchas}

- **Problème :** Implémenter `operator+` comme membre le rend asymétrique (pas de conversion implicite de l'opérande de gauche) -> **Solution :** L'implémenter comme fonction libre prenant les deux opérandes par valeur ou par référence constante
- **Problème :** Absence de `explicit` sur un constructeur à un argument ou sur un opérateur de conversion -> conversions implicites indésirables et silencieuses -> **Solution :** Toujours utiliser `explicit` sur les constructeurs à un argument et les opérateurs de conversion
- **Problème :** `operator<<` a besoin d'accéder aux membres privés -> **Solution :** Le déclarer `friend` à l'intérieur de la classe
- **Problème :** Avant C++20 : implémenter manuellement les 6 opérateurs de comparaison -> **Solution :** Utiliser `operator<=>` (C++20), qui génère les six à partir d'une seule déclaration

## Voir aussi {#see-also}

- [[inheritance-and-polymorphism]]
- [[move-semantics]]
- [[const-and-type-safety]]
- [cppreference : surcharge d'opérateurs](https://en.cppreference.com/w/cpp/language/operators)
