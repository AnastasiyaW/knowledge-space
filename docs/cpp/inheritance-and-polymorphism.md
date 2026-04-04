---
title: Inheritance and Polymorphism
category: concepts
tags: [cpp, oop, inheritance, polymorphism, virtual, abstract]
---

# Inheritance and Polymorphism

Runtime polymorphism via virtual functions and inheritance hierarchies. Base class pointers/references invoke derived behavior through vtable dispatch.

## Key Facts

- Three access specifiers: `public`, `protected`, `private`
- `public` inheritance = IS-A relationship (most common)
- `protected` inheritance = implemented-in-terms-of (rare)
- `private` inheritance = implemented-in-terms-of (prefer composition)
- Constructor order: base -> members -> derived body. Destructor: reverse
- `virtual` function: dispatched via vtable at runtime. Overhead: one pointer per object + indirect call
- `override` keyword (C++11): compiler checks that function actually overrides base virtual
- `final` keyword: prevents further overriding or derivation
- Pure virtual `= 0`: makes class abstract, cannot instantiate
- Virtual destructor required in any class used as polymorphic base
- Multiple inheritance: supported but use with caution; virtual inheritance solves diamond problem
- `dynamic_cast<Derived*>(base_ptr)`: safe downcast, returns nullptr on failure (RTTI)

## Patterns

### Basic Inheritance

```cpp
class Shape {
protected:
    double x_, y_;  // position
public:
    Shape(double x, double y) : x_(x), y_(y) {}
    virtual ~Shape() = default;  // ALWAYS virtual dtor for base

    virtual double area() const = 0;         // pure virtual
    virtual double perimeter() const = 0;    // pure virtual
    virtual void draw() const { /* default impl */ }

    double x() const { return x_; }
    double y() const { return y_; }
};

class Circle : public Shape {
    double radius_;
public:
    Circle(double x, double y, double r) : Shape(x, y), radius_(r) {}

    double area() const override { return 3.14159 * radius_ * radius_; }
    double perimeter() const override { return 2 * 3.14159 * radius_; }
};

class Rectangle : public Shape {
    double w_, h_;
public:
    Rectangle(double x, double y, double w, double h)
        : Shape(x, y), w_(w), h_(h) {}

    double area() const override { return w_ * h_; }
    double perimeter() const override { return 2 * (w_ + h_); }
};
```

### Polymorphic Usage

```cpp
void print_info(const Shape& s) {
    std::cout << "Area: " << s.area()
              << " Perimeter: " << s.perimeter() << '\n';
}

// Polymorphism through base pointer/reference
std::vector<std::unique_ptr<Shape>> shapes;
shapes.push_back(std::make_unique<Circle>(0, 0, 5));
shapes.push_back(std::make_unique<Rectangle>(0, 0, 4, 6));

for (const auto& s : shapes) {
    print_info(*s);  // dispatches to correct area()/perimeter()
}
```

### Access Specifiers in Inheritance

```cpp
class Base {
private:   int priv_;    // only Base
protected: int prot_;    // Base + derived
public:    int pub_;     // everyone
};

class Derived : public Base {
    void foo() {
        // priv_ = 1;   // ERROR: private in Base
        prot_ = 2;      // OK: protected accessible in derived
        pub_ = 3;       // OK: public
    }
};

// public inheritance: public stays public, protected stays protected
// protected inheritance: public+protected become protected
// private inheritance: everything becomes private
```

### Interface Pattern (Abstract Base)

```cpp
class ILogger {
public:
    virtual ~ILogger() = default;
    virtual void log(std::string_view msg) = 0;
    virtual void flush() = 0;
};

class FileLogger : public ILogger {
    std::ofstream file_;
public:
    explicit FileLogger(const std::string& path) : file_(path) {}
    void log(std::string_view msg) override { file_ << msg << '\n'; }
    void flush() override { file_.flush(); }
};

class ConsoleLogger : public ILogger {
public:
    void log(std::string_view msg) override { std::cout << msg << '\n'; }
    void flush() override { std::cout.flush(); }
};
```

### Multiple Inheritance and Diamond

```cpp
// Diamond problem
class A { public: int val; };
class B : virtual public A {};  // virtual inheritance
class C : virtual public A {};  // virtual inheritance
class D : public B, public C {};

D d;
d.val = 42;  // unambiguous: single A sub-object
```

### override and final

```cpp
class Base {
public:
    virtual void process() const;
    virtual void update();
};

class Derived : public Base {
public:
    void process() const override;       // OK: overrides Base::process
    // void process() override;           // ERROR: signature mismatch (missing const)
    void update() override final;        // overrides AND prevents further override
};

class Final final : public Derived {     // cannot derive from Final
    // void update() override;            // ERROR: update() is final
};
```

### Method Overloading vs Overriding

**Overloading**: same name, different parameter types/count. Compile-time resolution (no `virtual` needed):

```cpp
class Calculator {
public:
    int add(int a, int b) { return a + b; }
    double add(double a, double b) { return a + b; }
    int add(int a, int b, int c) { return a + b + c; }
};
```

**Overriding**: same name AND signature in derived class. Runtime resolution via vtable. Requires `virtual` in base.

Key difference: overloading = compile-time polymorphism, overriding = runtime polymorphism. Don't confuse hiding (non-virtual same-name function in derived) with either.

### Constructor Chaining in Inheritance

Constructors execute in order: base -> members -> derived body. Each derived constructor must call a base constructor (implicitly default or explicitly):

```cpp
class Animal {
protected:
    std::string name_;
    int age_;
public:
    Animal(std::string name, int age) : name_(std::move(name)), age_(age) {}
};

class Dog : public Animal {
    std::string breed_;
public:
    // Must explicitly call base constructor - no default Animal()
    Dog(std::string name, int age, std::string breed)
        : Animal(std::move(name), age), breed_(std::move(breed)) {}
};
```

Destructors execute in reverse: derived -> members -> base. This is why base destructors must be `virtual` - ensures derived destructor runs when deleting through base pointer.

## Gotchas

- **Issue:** Missing `virtual` destructor in base class -> UB when deleting derived through base pointer -> **Fix:** Any class with virtual functions must have `virtual ~Base() = default;`
- **Issue:** Calling virtual function in constructor/destructor -> calls base version, not derived -> **Fix:** Don't call virtual functions in ctor/dtor. Use post-construction init or CRTP pattern.
- **Issue:** Forgetting `override` keyword -> silent bug if base signature changes -> **Fix:** Always use `override` on every overriding function
- **Issue:** Object slicing - assigning derived to base by value loses derived data -> **Fix:** Use references or pointers for polymorphism, never value semantics
- **Issue:** Name hiding - derived non-virtual function with same name as base hides ALL base overloads -> **Fix:** Use `using Base::func;` in derived class to bring base overloads into scope

## See Also

- [[design-patterns-cpp]]
- [[smart-pointers]]
- [[raii-resource-management]]
- [[operator-overloading]]
