---
title: "Überladen von Operatoren"
category: concepts
tags: [cpp, operators, overloading, comparison, streams]
level: 3
source_sha256: 29f1b2486cf6c3c44a68929e2513f31e40ad625760479b9c9d525ccd6758d1a9
translation: machine
translated_at: '2026-10-24'
---
# Überladen von Operatoren {#operator-overloading}

Definiert benutzerspezifisches Verhalten für Operatoren auf benutzerdefinierten Typen. Ermöglicht eine natürliche Syntax für mathematische Typen, Container und Ein-/Ausgabe.

## Wichtige Fakten {#key-facts}

- Überladbar: `+` `-` `*` `/` `%` `==` `!=` `<` `>` `<=` `>=` `<<` `>>` `[]` `()` `->` `++` `--` `<=>` und weitere
- Nicht überladbar: `::` `.` `.*` `?:` `sizeof` `typeid`
- Member- vs. freie Funktion: binäre Operatoren meist als freie Funktionen (symmetrisch), unäre Operatoren meist als Member
- `operator<<` / `operator>>` für Stream-I/O müssen eine freie Funktion sein (der linke Operand ist `ostream`/`istream`)
- `operator<=>` (C++20): Spaceship-Operator – eine einzige Funktion erzeugt alle 6 Vergleiche
- `operator()` macht ein Objekt aufrufbar (Functor)
- `operator[]` für den Index-Zugriff – für Zuweisungen eine Referenz zurückgeben
- Zusammengesetzte Zuweisung (`+=`) sollte als Member implementiert werden; der binäre Operator (`+`) als freie Funktion auf Basis von `+=`
- `explicit operator bool()` verhindert ungewollte implizite Konvertierung nach bool in unpassenden Kontexten
- Kopier- und Verschiebe-Zuweisungsoperatoren sind spezielle Member-Funktionen (siehe [[move-semantics]])

## Muster {#patterns}

### Arithmetische Operatoren {#arithmetic-operators}

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

### Vergleichsoperatoren (C++20 Spaceship) {#comparison-operators-c20-spaceship}

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

### Stream-I/O-Operatoren {#stream-io-operators}

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

### Index- und Funktionsaufruf {#subscript-and-function-call}

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

### Konvertierungsoperatoren {#conversion-operators}

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

## Fallstricke {#gotchas}

- **Problem:** Implementierung von `operator+` als Member macht ihn asymmetrisch (keine implizite Konvertierung des linken Operanden) -> **Lösung:** Als freie Funktion implementieren, die beide Operanden per Wert bzw. const-Referenz entgegennimmt
- **Problem:** Fehlendes `explicit` bei einem Konstruktor mit einem Argument oder bei einem Konvertierungsoperator -> stille, ungewollte Konvertierungen -> **Lösung:** Bei Konstruktoren mit einem Argument und Konvertierungsoperatoren immer `explicit` verwenden
- **Problem:** `operator<<` benötigt Zugriff auf private Member -> **Lösung:** Innerhalb der Klasse als `friend` deklarieren
- **Problem:** Vor C++20: alle 6 Vergleichsoperatoren manuell implementieren -> **Lösung:** `operator<=>` (C++20) verwenden, das alle sechs aus einer Deklaration erzeugt

## Siehe auch {#see-also}

- [[inheritance-and-polymorphism]]
- [[move-semantics]]
- [[const-and-type-safety]]
- [cppreference: operator overloading](https://en.cppreference.com/w/cpp/language/operators)
