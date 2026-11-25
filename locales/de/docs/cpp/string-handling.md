---
title: "String-Verarbeitung"
category: concepts
tags: [cpp, string, string_view, formatting, regex]
level: 3
source_sha256: e39dafec5fbfae60a809d072d330641b650e159c855ad0a1535a885241ec6d36
translation: machine
translated_at: '2026-10-24'
---
# String-Verarbeitung {#string-handling}

`std::string`, `std::string_view`, Formatierung, Konvertierung und Suche. Modernes C++ bietet effiziente und sichere String-Operationen.

## Wichtige Fakten {#key-facts}

- `std::string` - Heap-allokiert, besitzend, veränderlich, in einigen Implementierungen referenzgezählt
- Small String Optimization (SSO): Strings mit <~22 Zeichen werden inline gespeichert, ohne Heap-Allokation
- `std::string_view` (C++17) - nicht besitzend, schreibgeschützte Sicht; Teilstrings ohne Kopie
- `std::format` (C++20) - typsicheres Formatieren, vergleichbar mit Python-f-Strings
- `std::to_string(x)` / `std::stoi`, `std::stod` usw. für numerische Konvertierung
- `std::from_chars` / `std::to_chars` (C++17) - schnellste numerische Konvertierung, ohne Allokation
- `string_view` für Funktionsparameter bevorzugen, wenn kein Besitz benötigt wird
- String-Verkettung: `+` erzeugt temporäre Objekte; `append()` oder `+=` zum Aufbauen von Strings verwenden
- `std::ostringstream` für komplexen String-Aufbau
- C++23: `std::print` für formatierte Ausgabe (ersetzt `printf` und `cout <<`)

## Muster {#patterns}

### Grundlegende String-Operationen {#basic-string-operations}

```cpp
std::string s = "Hello, World!";

// Searching
size_t pos = s.find("World");       // 7
size_t pos2 = s.find('!');          // 12
bool found = s.contains("World");   // C++23: true

// Substrings
std::string sub = s.substr(7, 5);   // "World"

// Modification
s.replace(7, 5, "C++");             // "Hello, C++!"
s.erase(5, 2);                      // "HelloC++!"
s.insert(5, ", ");                   // "Hello, C++!"

// Comparison
bool eq = (s == "Hello, C++!");     // true
auto cmp = s <=> "Hello"s;          // C++20

// Case check / conversion (per-char)
std::transform(s.begin(), s.end(), s.begin(), ::tolower);
```

### string_view - ohne Kopie {#string_view-zero-copy}

```cpp
// Function parameter - accepts string, literal, string_view
void process(std::string_view sv) {
    auto first_word = sv.substr(0, sv.find(' '));  // no allocation!
    bool starts = sv.starts_with("Hello");          // C++20
    bool ends = sv.ends_with("!");                   // C++20
    sv.remove_prefix(1);  // advance start
    sv.remove_suffix(1);  // shrink end
}

process("Hello World");            // no allocation
process(std::string("Hello"));     // no copy
```

### Numerische Konvertierung {#numeric-conversion}

```cpp
// Simple (may throw, allocates)
int i = std::stoi("42");
double d = std::stod("3.14");
std::string s = std::to_string(42);

// Fast, no-throw (C++17)
#include <charconv>
std::string_view sv = "12345";
int value;
auto [ptr, ec] = std::from_chars(sv.data(), sv.data() + sv.size(), value);
if (ec == std::errc()) {
    // success: value = 12345
}

// to_chars
char buf[20];
auto [end, ec2] = std::to_chars(buf, buf + sizeof(buf), 42);
std::string_view result(buf, end - buf);  // "42"
```

### Formatierung (C++20/23) {#formatting-c2023}

```cpp
#include <format>

// std::format - type-safe, Python-like
std::string msg = std::format("Hello, {}! You are {} years old.", name, age);
std::string hex = std::format("{:#x}", 255);         // "0xff"
std::string pad = std::format("{:>10}", "right");     // "     right"
std::string flt = std::format("{:.2f}", 3.14159);     // "3.14"

// C++23: std::print (direct to stdout)
std::print("Value: {}\n", 42);
std::println("Formatted: {:06.2f}", 3.14);
```

### String-Aufbau {#string-building}

```cpp
// For many concatenations, use ostringstream or reserve
std::string build_csv(const std::vector<int>& data) {
    std::ostringstream oss;
    for (size_t i = 0; i < data.size(); ++i) {
        if (i > 0) oss << ',';
        oss << data[i];
    }
    return oss.str();
}

// Or pre-reserve
std::string result;
result.reserve(1024);
for (const auto& part : parts) {
    result += part;
    result += ',';
}
```

### Strings aufteilen {#splitting-strings}

```cpp
// C++20 ranges split
#include <ranges>
std::string csv = "one,two,three";
for (auto word : csv | std::views::split(',')) {
    std::string_view sv(word.begin(), word.end());
    // process sv
}

// Manual split
std::vector<std::string> split(const std::string& s, char delim) {
    std::vector<std::string> tokens;
    std::istringstream iss(s);
    std::string token;
    while (std::getline(iss, token, delim)) {
        tokens.push_back(token);
    }
    return tokens;
}
```

## Fallstricke {#gotchas}

- **Problem:** `string_view` hängt ins Leere (dangling), wenn der zugrunde liegende String zerstört wird -> **Lösung:** `string_view` niemals über die Lebensdauer der Quelle hinaus speichern. Niemals ein `string_view` auf einen lokalen String zurückgeben.
- **Problem:** `s[s.size()]` ist gültig (liefert `'\0'` in C++11), `s[s.size()+1]` ist undefiniertes Verhalten -> **Lösung:** `.at()` für Bereichsprüfung verwenden oder den Index validieren
- **Problem:** Verkettung von `const char*` mit `+` funktioniert nicht: `"a" + "b"` ist Zeigerarithmetik -> **Lösung:** `"a"s + "b"` (String-Literal-Operator) oder `std::string("a") + "b"` verwenden
- **Problem:** `std::stoi` wirft bei ungültiger Eingabe eine Exception, `from_chars` nicht -> **Lösung:** `from_chars` zum Parsen nicht vertrauenswürdiger Eingaben verwenden und den `errc`-Rückgabewert prüfen

## Siehe auch {#see-also}

- [[const-and-type-safety]]
- [[file-io-streams]]
- [[stl-algorithms]]
- [cppreference: string](https://en.cppreference.com/w/cpp/string/basic_string)
