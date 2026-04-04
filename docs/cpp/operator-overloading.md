---
title: Operator Overloading
category: concepts
tags: [cpp, operators, overloading, comparison, streams]
---

# Operator Overloading

Define custom behavior for operators on user-defined types. Enables natural syntax for mathematical types, containers, and I/O.

## Key Facts

- Overloadable: `+` `-` `*` `/` `%` `==` `!=` `<` `>` `<=` `>=` `<<` `>>` `[]` `()` `->` `++` `--` `<=>` and more
- Not overloadable: `::` `.` `.*` `?:` `sizeof` `typeid`
- Member vs free function: binary ops usually free (symmetric), unary ops usually member
- `operator<<` / `operator>>` for stream I/O must be free function (left operand is `ostream`/`istream`)
- `operator<=>` (C++20): spaceship operator - single function generates all 6 comparisons
- `operator()` makes object callable (functor)
- `operator[]` for subscript - return reference for assignment
- Compound assignment (`+=`) should be member; binary (`+`) free in terms of `+=`
- `explicit operator bool()` prevents implicit conversion to bool in unwanted contexts
- Copy/move assignment operators are special member functions (see [[move-semantics]])

## Patterns

### Arithmetic Operators

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

### Comparison Operators (C++20 Spaceship)

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

### Stream I/O Operators

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

### Subscript and Function Call

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

### Conversion Operators

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

## Gotchas

- **Issue:** Implementing `operator+` as member makes it asymmetric (no implicit conversion of left operand) -> **Fix:** Implement as free function taking both by value/const ref
- **Issue:** Missing `explicit` on single-arg constructor or conversion operator -> silent unwanted conversions -> **Fix:** Always use `explicit` on single-arg constructors and conversion operators
- **Issue:** `operator<<` needs access to private members -> **Fix:** Declare as `friend` inside class
- **Issue:** Pre-C++20: implementing all 6 comparison operators manually -> **Fix:** Use `operator<=>` (C++20) which generates all six from one declaration

## See Also

- [[inheritance-and-polymorphism]]
- [[move-semantics]]
- [[const-and-type-safety]]
- [cppreference: operator overloading](https://en.cppreference.com/w/cpp/language/operators)
