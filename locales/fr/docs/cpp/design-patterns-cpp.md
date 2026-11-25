---
title: "Patrons de conception en C++ moderne"
category: patterns
tags: [cpp, design-patterns, singleton, factory, observer, strategy, crtp]
level: 3
source_sha256: 797da3e8f8f40e40083c30b993e8e59ebb2c7ea51e5b3eca47c58210c48c0c6f
translation: machine
translated_at: '2026-10-24'
---
# Patrons de conception en C++ moderne {#design-patterns-in-modern-c}

Patrons GoF classiques adaptés au C++ moderne, avec les templates, les pointeurs intelligents, les lambdas et la sémantique de valeur.

## Points clés {#key-facts}

- Création : Factory, Abstract Factory, Builder, Singleton, Prototype
- Structure : Adapter, Bridge, Composite, Decorator, Facade, Proxy
- Comportement : Observer, Strategy, Command, Iterator, State, Visitor
- Le C++ moderne remplace souvent les patrons par des constructions plus simples (lambdas pour Strategy, variants pour Visitor)
- Privilégier la composition à l'héritage : utiliser les templates et les lambdas
- CRTP (Curiously Recurring Template Pattern) : polymorphisme statique sans surcoût de vtable
- `std::variant` + `std::visit` remplace le patron Visitor classique
- Les pointeurs intelligents permettent des schémas de propriété sûrs (Singleton, Composite, Observer)
- Patron d'effacement de type : masquer l'implémentation derrière une interface à sémantique de valeur

## Patrons {#patterns}

### Singleton (thread-safe) {#singleton-thread-safe}

```cpp
class Logger {
public:
    static Logger& instance() {
        static Logger inst;  // C++11: thread-safe static init (Meyers' Singleton)
        return inst;
    }

    void log(std::string_view msg) {
        std::lock_guard lock(mtx_);
        std::cout << msg << '\n';
    }

    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

private:
    Logger() = default;
    std::mutex mtx_;
};
```

### Factory / Abstract Factory {#factory-abstract-factory}

```cpp
// Simple factory
class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;

    // Factory method
    static std::unique_ptr<Shape> create(std::string_view type, double param) {
        if (type == "circle") return std::make_unique<Circle>(param);
        if (type == "square") return std::make_unique<Square>(param);
        throw std::invalid_argument("Unknown shape type");
    }
};

// Registry-based factory (extensible)
class ShapeFactory {
    using Creator = std::function<std::unique_ptr<Shape>(double)>;
    std::unordered_map<std::string, Creator> registry_;
public:
    void register_type(std::string name, Creator creator) {
        registry_[std::move(name)] = std::move(creator);
    }

    std::unique_ptr<Shape> create(const std::string& type, double param) const {
        auto it = registry_.find(type);
        if (it == registry_.end()) throw std::runtime_error("Unknown: " + type);
        return it->second(param);
    }
};
```

### Strategy (basé sur les lambdas) {#strategy-lambda-based}

```cpp
// Modern: just use std::function or template parameter
class Sorter {
    std::function<bool(int, int)> compare_;
public:
    explicit Sorter(std::function<bool(int, int)> cmp = std::less<int>())
        : compare_(std::move(cmp)) {}

    void sort(std::vector<int>& data) {
        std::sort(data.begin(), data.end(), compare_);
    }
};

Sorter ascending;
Sorter descending([](int a, int b) { return a > b; });
```

### Observer {#observer}

```cpp
template<typename... Args>
class Signal {
    std::vector<std::function<void(Args...)>> slots_;
public:
    void connect(std::function<void(Args...)> slot) {
        slots_.push_back(std::move(slot));
    }

    void emit(Args... args) {
        for (auto& slot : slots_) {
            slot(args...);
        }
    }
};

// Usage
Signal<int, std::string> on_message;
on_message.connect([](int id, const std::string& msg) {
    std::cout << id << ": " << msg << '\n';
});
on_message.emit(1, "hello");
```

### CRTP - polymorphisme statique {#crtp-static-polymorphism}

```cpp
template<typename Derived>
class Printable {
public:
    void print() const {
        const auto& self = static_cast<const Derived&>(*this);
        std::cout << self.to_string() << '\n';
    }
};

class Name : public Printable<Name> {
    std::string name_;
public:
    explicit Name(std::string n) : name_(std::move(n)) {}
    std::string to_string() const { return name_; }
};

Name n("Alice");
n.print();  // no vtable, no virtual dispatch, fully inlined
```

### Visitor via std::variant (C++17) {#visitor-via-stdvariant-c17}

```cpp
using Shape = std::variant<Circle, Rectangle, Triangle>;

// Visit with overloaded lambdas
double area(const Shape& s) {
    return std::visit([](const auto& shape) { return shape.area(); }, s);
}

// Overload pattern helper
template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
template<class... Ts> overloaded(Ts...) -> overloaded<Ts...>;

std::string describe(const Shape& s) {
    return std::visit(overloaded{
        [](const Circle& c)    { return "circle r=" + std::to_string(c.radius); },
        [](const Rectangle& r) { return "rect " + std::to_string(r.w) + "x" + std::to_string(r.h); },
        [](const Triangle& t)  { return "triangle"; }
    }, s);
}
```

### Builder {#builder}

```cpp
class QueryBuilder {
    std::string table_;
    std::vector<std::string> conditions_;
    std::optional<int> limit_;
public:
    QueryBuilder& from(std::string table) { table_ = std::move(table); return *this; }
    QueryBuilder& where(std::string cond) { conditions_.push_back(std::move(cond)); return *this; }
    QueryBuilder& limit(int n) { limit_ = n; return *this; }

    std::string build() const {
        std::string q = "SELECT * FROM " + table_;
        if (!conditions_.empty()) {
            q += " WHERE " + conditions_[0];
            for (size_t i = 1; i < conditions_.size(); ++i)
                q += " AND " + conditions_[i];
        }
        if (limit_) q += " LIMIT " + std::to_string(*limit_);
        return q;
    }
};

auto query = QueryBuilder()
    .from("users")
    .where("age > 18")
    .where("active = true")
    .limit(10)
    .build();
```

## Pièges courants {#gotchas}

- **Problème :** Le Singleton classique avec pointeur brut fuit ou pose des problèmes d'ordre de destruction -> **Correctif :** Utiliser le Singleton de Meyers (static local à la fonction), garanti thread-safe en C++11
- **Problème :** Observer avec pointeurs bruts : pendant (dangling) lorsque l'observateur est détruit -> **Correctif :** Utiliser `weak_ptr` pour les observateurs, ou un désabonnement par jeton
- **Problème :** La base CRTP accède au dérivé avant la fin de la construction -> **Correctif :** Ne jamais appeler de méthodes dérivées dans le constructeur de la base CRTP
- **Problème :** Surcoût de `std::function` (allocation sur le tas, effacement de type) dans les chemins critiques -> **Correctif :** Utiliser un paramètre template pour Strategy dans le code sensible aux performances

## Voir aussi {#see-also}

- [[inheritance-and-polymorphism]]
- [[templates-and-concepts]]
- [[lambda-expressions]]
- [Gestion de la mémoire et pointeurs intelligents](smart-pointers.md)
