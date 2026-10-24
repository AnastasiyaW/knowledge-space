---
title: "Gestion des chaînes"
category: concepts
tags: [cpp, string, string_view, formatting, regex]
level: 3
source_sha256: e39dafec5fbfae60a809d072d330641b650e159c855ad0a1535a885241ec6d36
translation: machine
translated_at: '2026-10-24'
---
# Gestion des chaînes {#string-handling}

`std::string`, `std::string_view`, le formatage, la conversion et la recherche. C++ moderne offre des opérations sur les chaînes efficaces et sûres.

## Points clés {#key-facts}

- `std::string` - alloué sur le tas, propriétaire, modifiable, à comptage de références dans certaines implémentations
- Small String Optimization (SSO) : les chaînes de moins de ~22 caractères sont stockées en ligne, sans allocation sur le tas
- `std::string_view` (C++17) - vue non propriétaire et en lecture seule ; sous-chaînes sans copie
- `std::format` (C++20) - formatage type-safe, similaire aux f-strings de Python
- `std::to_string(x)` / `std::stoi`, `std::stod`, etc. pour la conversion numérique
- `std::from_chars` / `std::to_chars` (C++17) - conversion numérique la plus rapide, sans allocation
- Privilégier `string_view` pour les paramètres de fonction lorsqu'aucune propriété n'est nécessaire
- Concaténation de chaînes : `+` crée des temporaires ; utiliser `append()` ou `+=` pour construire des chaînes
- `std::ostringstream` pour la construction de chaînes complexes
- C++23 : `std::print` pour la sortie formatée (remplace `printf` et `cout <<`)

## Patrons {#patterns}

### Opérations de base sur les chaînes {#basic-string-operations}

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

### string_view - sans copie {#string_view-zero-copy}

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

### Conversion numérique {#numeric-conversion}

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

### Formatage (C++20/23) {#formatting-c2023}

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

### Construction de chaînes {#string-building}

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

### Découpage de chaînes {#splitting-strings}

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

## Pièges {#gotchas}

- **Problème :** `string_view` devient pendante lorsque la chaîne sous-jacente est détruite -> **Correction :** ne jamais conserver une `string_view` au-delà de la durée de vie de sa source. Ne jamais retourner une `string_view` pointant vers une chaîne locale.
- **Problème :** `s[s.size()]` est valide (retourne `'\0'` en C++11), mais `s[s.size()+1]` est un comportement indéfini -> **Correction :** utiliser `.at()` pour la vérification des bornes, ou valider l'indice
- **Problème :** la concaténation d'un `const char*` avec `+` ne fonctionne pas : `"a" + "b"` est une arithmétique de pointeurs -> **Correction :** utiliser `"a"s + "b"` (opérateur de littéral de chaîne) ou `std::string("a") + "b"`
- **Problème :** `std::stoi` lève une exception sur une entrée invalide, contrairement à `from_chars` -> **Correction :** utiliser `from_chars` pour analyser des entrées non fiables, et vérifier la valeur `errc` retournée

## Voir aussi {#see-also}

- [[const-and-type-safety]]
- [[file-io-streams]]
- [[stl-algorithms]]
- [cppreference: string](https://en.cppreference.com/w/cpp/string/basic_string)
