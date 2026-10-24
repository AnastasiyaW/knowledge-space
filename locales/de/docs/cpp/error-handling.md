---
title: "Fehlerbehandlung - Exceptions und Alternativen"
category: concepts
tags: [cpp, exceptions, error-handling, optional, expected, noexcept]
level: 3
source_sha256: 55c74201a5bf79c855baa767c32524cc276671dd8ad9dc7d740b046ad54a2c8f
translation: machine
translated_at: '2026-10-24'
---
# Fehlerbehandlung - Exceptions und Alternativen {#error-handling-exceptions-and-alternatives}

C++ unterstützt Exceptions, Fehlercodes, `std::optional` und `std::expected` (C++23). Wähle den passenden Mechanismus für den jeweiligen Kontext.

## Wichtige Fakten {#key-facts}

- Exceptions: für außergewöhnliche/unerwartete Fehler. Keine Laufzeitkosten, solange nicht geworfen wird (tabellenbasiertes Unwinding)
- `noexcept`-Spezifizierer: Funktion verspricht, nicht zu werfen. Ermöglicht Optimierungen (Verschieben in `vector`)
- Fehlercodes: für erwartbare Fehler (Datei nicht gefunden, ungültige Eingabe). Kein Overhead, explizite Kontrollflusssteuerung
- `std::optional<T>` (C++17): Wert oder nichts. Für Funktionen, die möglicherweise kein Ergebnis liefern
- `std::expected<T,E>` (C++23): Wert oder Fehler. Typsichere Alternative zu Exceptions
- Standard-Exception-Hierarchie: `std::exception` -> `runtime_error`, `logic_error`, usw.
- Mit `const`-Referenz fangen: `catch (const std::exception& e)`
- Stack-Unwinding bei Exception: alle lokalen RAII-Objekte werden destruiert (siehe [[raii-resource-management]])
- `throw;` wirft die aktuelle Exception erneut (Typ bleibt erhalten). `throw e;` schneidet auf `std::exception` ab (Slicing)
- Niemals aus einem Destruktor werfen (führt während des Stack-Unwindings zu `std::terminate`)
- Exception-Spezifikationen wurden in C++17 entfernt, außer `noexcept`

## Muster {#patterns}

### Exception-Behandlung {#exception-handling}

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

### Eigene Exceptions {#custom-exceptions}

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

### Behandlung mehrerer Exceptions {#multiple-exception-handling}

Die Reihenfolge ist wichtig: abgeleitete Typen vor Basistypen fangen. Die spezifischsten zuerst:

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

**Praxismuster**: Die Hauptlogik in `try` einschließen, spezifische behebbare Fehler behandeln und nicht behebbare nach oben weiterreichen:

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

## Fallstricke {#gotchas}

- **Problem:** Exception per Wert fangen schneidet den abgeleiteten Typ ab (Slicing) -> **Lösung:** Immer mit `const`-Referenz fangen: `catch (const std::exception& e)`
- **Problem:** `throw e;` innerhalb von `catch` wirft eine abgeschnittene Kopie erneut -> **Lösung:** `throw;` verwenden, um die Exception mit ihrem ursprünglichen Typ erneut zu werfen
- **Problem:** Exception im Destruktor während des Stack-Unwindings -> `std::terminate` -> **Lösung:** Niemals aus Destruktoren werfen. Im Destruktor abfangen und protokollieren.
- **Problem:** `optional.value()` wirft `bad_optional_access`, wenn leer -> **Lösung:** Mit `has_value()` / `if (opt)` prüfen oder `value_or(default)` verwenden
- **Problem:** Fehlendes `noexcept` am Move-Konstruktor führt dazu, dass `vector` bei der Neuallokation kopiert statt zu verschieben -> **Lösung:** Move-Operationen immer als `noexcept` markieren

## Siehe auch {#see-also}

- [[raii-resource-management]]
- [[move-semantics]]
- [[const-and-type-safety]]
- [cppreference: Exceptions](https://en.cppreference.com/w/cpp/error/exception)
