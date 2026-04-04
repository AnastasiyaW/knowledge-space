---
title: String Handling
category: concepts
tags: [cpp, string, string_view, formatting, regex]
---

# String Handling

`std::string`, `std::string_view`, formatting, conversion, and searching. Modern C++ offers efficient, safe string operations.

## Key Facts

- `std::string` - heap-allocated, owning, mutable, reference-counted in some implementations
- Small String Optimization (SSO): strings <~22 chars stored inline, no heap allocation
- `std::string_view` (C++17) - non-owning, read-only view; zero-copy substrings
- `std::format` (C++20) - type-safe formatting, similar to Python f-strings
- `std::to_string(x)` / `std::stoi`, `std::stod` etc. for numeric conversion
- `std::from_chars` / `std::to_chars` (C++17) - fastest numeric conversion, no allocation
- Prefer `string_view` for function parameters when no ownership needed
- String concatenation: `+` creates temporaries; `append()` or `+=` for building strings
- `std::ostringstream` for complex string building
- C++23: `std::print` for formatted output (replaces `printf` and `cout <<`)

## Patterns

### Basic String Operations

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

### string_view - Zero-Copy

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

### Numeric Conversion

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

### Formatting (C++20/23)

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

### String Building

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

### Splitting Strings

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

## Gotchas

- **Issue:** `string_view` dangling when underlying string destroyed -> **Fix:** Never store `string_view` beyond source lifetime. Never return `string_view` to local string.
- **Issue:** `s[s.size()]` is valid (returns `'\0'` in C++11), but `s[s.size()+1]` is UB -> **Fix:** Use `.at()` for bounds checking or validate index
- **Issue:** Concatenating `const char*` with `+` doesn't work: `"a" + "b"` is pointer arithmetic -> **Fix:** Use `"a"s + "b"` (string literal operator) or `std::string("a") + "b"`
- **Issue:** `std::stoi` throws on invalid input, `from_chars` does not -> **Fix:** Use `from_chars` for parsing untrusted input, check `errc` return

## See Also

- [[const-and-type-safety]]
- [[file-io-streams]]
- [[stl-algorithms]]
- [cppreference: string](https://en.cppreference.com/w/cpp/string/basic_string)
