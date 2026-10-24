---
title: "Gestion des erreurs - Exceptions et alternatives"
category: concepts
tags: [cpp, exceptions, error-handling, optional, expected, noexcept]
level: 3
source_sha256: 55c74201a5bf79c855baa767c32524cc276671dd8ad9dc7d740b046ad54a2c8f
translation: machine
translated_at: '2026-10-24'
---
# Gestion des erreurs - Exceptions et alternatives {#error-handling-exceptions-and-alternatives}

C++ prend en charge les exceptions, les codes d'erreur, `std::optional` et `std::expected` (C++23). Choisissez le mécanisme adapté au contexte.

## Points clés {#key-facts}

- Exceptions : pour les erreurs exceptionnelles ou inattendues. Coût nul lorsqu'aucune exception n'est levée (déroulement basé sur des tables)
- Spécificateur `noexcept` : la fonction promet de ne pas lever d'exception. Permet des optimisations (déplacement dans `vector`)
- Codes d'erreur : pour les échecs attendus (fichier introuvable, entrée invalide). Pas de surcoût, flux de contrôle explicite
- `std::optional<T>` (C++17) : valeur ou absence de valeur. Pour les fonctions pouvant ne pas produire de résultat
- `std::expected<T,E>` (C++23) : valeur ou erreur. Alternative typée aux exceptions
- Hiérarchie standard des exceptions : `std::exception` -> `runtime_error`, `logic_error`, etc.
- Capturer par référence `const` : `catch (const std::exception& e)`
- Déroulement de la pile lors d'une exception : tous les objets RAII locaux sont détruits (voir [[raii-resource-management]])
- `throw;` relève l'exception courante (en préservant son type). `throw e;` tranche vers `std::exception`
- Ne jamais lever d'exception depuis un destructeur (cela termine le programme pendant le déroulement de la pile)
- Les spécifications d'exception ont été supprimées en C++17, à l'exception de `noexcept`

## Patterns {#patterns}

### Gestion des exceptions {#exception-handling}

```cpp
#include <stdexcept>

// Throwing
void parse(const std::string& input) {
    if (input.empty())
        throw std::invalid_argument("Input cannot be empty");
    if (input.size() > 1024)
        throw std::length_error("Input too long");
    // parse...
}

// Catching
try {
    parse(user_input);
} catch (const std::invalid_argument& e) {
    std::cerr << "Invalid: " << e.what() << '\n';
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << '\n';
} catch (...) {
    std::cerr << "Unknown error\n";
    throw;  // re-throw
}
```

### Exceptions personnalisées {#custom-exceptions}

```cpp
class AppError : public std::runtime_error {
    int code_;
public:
    AppError(int code, const std::string& msg)
        : std::runtime_error(msg), code_(code) {}
    int code() const { return code_; }
};

class NetworkError : public AppError {
public:
    NetworkError(const std::string& msg)
        : AppError(1001, msg) {}
};

// Usage
throw NetworkError("Connection refused");
```

### std::optional (C++17) {#stdoptional-c17}

```cpp
#include <optional>

std::optional<int> find_index(const std::vector<int>& v, int target) {
    for (size_t i = 0; i < v.size(); ++i) {
        if (v[i] == target) return static_cast<int>(i);
    }
    return std::nullopt;
}

// Usage
if (auto idx = find_index(vec, 42)) {
    std::cout << "Found at index " << *idx << '\n';
} else {
    std::cout << "Not found\n";
}

// Value-or-default
int idx = find_index(vec, 42).value_or(-1);
```

### std::expected (C++23) {#stdexpected-c23}

```cpp
#include <expected>

enum class ParseError { empty_input, invalid_format, overflow };

std::expected<int, ParseError> parse_int(std::string_view sv) {
    if (sv.empty())
        return std::unexpected(ParseError::empty_input);
    // parse logic...
    return 42;
}

// Usage
auto result = parse_int("123");
if (result) {
    use(*result);
} else {
    handle_error(result.error());
}

// Monadic operations (C++23)
auto final_result = parse_int(input)
    .transform([](int x) { return x * 2; })
    .or_else([](ParseError e) -> std::expected<int, ParseError> {
        log_error(e);
        return 0;  // default value
    });
```

### Gestion de plusieurs exceptions {#multiple-exception-handling}

L'ordre compte : capturez les types dérivés avant les types de base. Du plus spécifique au plus général :

```cpp
try {
    open_file(path);
    parse_data(content);
    write_results(output_path);
} catch (const std::ios_base::failure& e) {
    // File I/O specific errors
    std::cerr << "I/O error: " << e.what() << '\n';
} catch (const std::invalid_argument& e) {
    // Parse errors
    std::cerr << "Invalid data: " << e.what() << '\n';
} catch (const std::runtime_error& e) {
    // Generic runtime errors
    std::cerr << "Runtime error: " << e.what() << '\n';
} catch (const std::exception& e) {
    // Catch-all for standard exceptions
    std::cerr << "Error: " << e.what() << '\n';
} catch (...) {
    // Non-standard exceptions (rare, e.g. from C libraries)
    std::cerr << "Unknown error\n";
    throw;  // re-throw - don't swallow unknown exceptions
}
```

**Pattern pratique** : enveloppez la logique principale dans un bloc `try`, traitez les erreurs spécifiques récupérables, et laissez remonter celles qui ne le sont pas :

```cpp
int main() {
    try {
        run_application();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Fatal: " << e.what() << '\n';
        return 1;
    } catch (...) {
        std::cerr << "Unknown fatal error\n";
        return 2;
    }
}
```

### noexcept {#noexcept}

```cpp
// Mark functions that won't throw
void swap(Widget& a, Widget& b) noexcept {
    std::swap(a.data_, b.data_);
}

// Conditional noexcept
template<typename T>
void safe_swap(T& a, T& b) noexcept(noexcept(std::swap(a, b))) {
    std::swap(a, b);
}

// Move operations MUST be noexcept for vector optimization
Widget(Widget&& other) noexcept;
Widget& operator=(Widget&& other) noexcept;
```

## Pièges {#gotchas}

- **Problème :** capturer une exception par valeur tranche le type dérivé -> **Correction :** capturez toujours par référence `const` : `catch (const std::exception& e)`
- **Problème :** `throw e;` dans un `catch` relève une copie tranchée -> **Correction :** utilisez `throw;` pour relever l'exception en préservant son type d'origine
- **Problème :** exception dans un destructeur pendant le déroulement de la pile -> `std::terminate` -> **Correction :** ne levez jamais d'exception depuis un destructeur. Capturez et journalisez-la à l'intérieur du destructeur.
- **Problème :** `optional.value()` lève `bad_optional_access` si l'objet est vide -> **Correction :** vérifiez avec `has_value()` / `if (opt)` ou utilisez `value_or(default)`
- **Problème :** l'absence de `noexcept` sur le constructeur de déplacement fait copier au lieu de déplacer `vector` lors de la réallocation -> **Correction :** marquez toujours les opérations de déplacement `noexcept`

## Voir aussi {#see-also}

- [[raii-resource-management]]
- [[move-semantics]]
- [[const-and-type-safety]]
- [cppreference : Exceptions](https://en.cppreference.com/w/cpp/error/exception)
