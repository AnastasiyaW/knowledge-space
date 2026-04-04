---
title: File I/O and Streams
category: concepts
tags: [cpp, file-io, streams, fstream, filesystem]
---

# File I/O and Streams

Stream-based I/O (`<fstream>`, `<iostream>`) and filesystem operations (`<filesystem>`). RAII-managed file handles with automatic cleanup.

## Key Facts

- `std::ifstream` - input file stream (reading)
- `std::ofstream` - output file stream (writing)
- `std::fstream` - bidirectional file stream
- Streams are RAII - file closed automatically in destructor
- Check state: `if (stream)` or `stream.good()`, `stream.fail()`, `stream.eof()`
- `std::getline(stream, string)` reads entire line
- `stream >> var` extracts formatted data, skips whitespace
- Binary I/O: `stream.read()`, `stream.write()` with `std::ios::binary` flag
- `<filesystem>` (C++17): path manipulation, directory iteration, file operations
- `std::filesystem::path` handles OS-specific path separators
- Prefer `<filesystem>` over C-style `fopen`/`fclose` or OS-specific APIs

## Patterns

### Reading Files

```cpp
#include <fstream>

// Read entire file to string
std::string read_file(const std::string& path) {
    std::ifstream file(path);
    if (!file) throw std::runtime_error("Cannot open: " + path);
    return std::string(std::istreambuf_iterator<char>(file),
                       std::istreambuf_iterator<char>());
}

// Read line by line
void process_lines(const std::string& path) {
    std::ifstream file(path);
    std::string line;
    while (std::getline(file, line)) {
        // process line
    }
}

// Read structured data
struct Record { std::string name; int age; double score; };

std::vector<Record> read_csv(const std::string& path) {
    std::ifstream file(path);
    std::vector<Record> records;
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        Record r;
        char comma;
        if (iss >> r.name >> comma >> r.age >> comma >> r.score) {
            records.push_back(r);
        }
    }
    return records;
}
```

### Writing Files

```cpp
// Text output
void write_report(const std::string& path,
                  const std::vector<Record>& data) {
    std::ofstream file(path);
    if (!file) throw std::runtime_error("Cannot create: " + path);

    file << "Name,Age,Score\n";
    for (const auto& r : data) {
        file << r.name << ',' << r.age << ',' << r.score << '\n';
    }
    // file closed automatically
}

// Append mode
std::ofstream log("app.log", std::ios::app);
log << "Event occurred\n";

// Truncate (default for ofstream)
std::ofstream fresh("data.txt", std::ios::trunc);
```

### Binary I/O

```cpp
// Write binary
void save_binary(const std::string& path, const std::vector<float>& data) {
    std::ofstream file(path, std::ios::binary);
    size_t count = data.size();
    file.write(reinterpret_cast<const char*>(&count), sizeof(count));
    file.write(reinterpret_cast<const char*>(data.data()),
               count * sizeof(float));
}

// Read binary
std::vector<float> load_binary(const std::string& path) {
    std::ifstream file(path, std::ios::binary);
    size_t count;
    file.read(reinterpret_cast<char*>(&count), sizeof(count));
    std::vector<float> data(count);
    file.read(reinterpret_cast<char*>(data.data()),
              count * sizeof(float));
    return data;
}
```

### Filesystem (C++17)

```cpp
#include <filesystem>
namespace fs = std::filesystem;

// Path operations
fs::path p = "/home/user/docs/file.txt";
p.filename();     // "file.txt"
p.stem();         // "file"
p.extension();    // ".txt"
p.parent_path();  // "/home/user/docs"
p / "subdir";     // "/home/user/docs/file.txt/subdir"

// File operations
bool exists = fs::exists(p);
auto size = fs::file_size(p);         // bytes
auto time = fs::last_write_time(p);

fs::copy("src.txt", "dst.txt");
fs::rename("old.txt", "new.txt");
fs::remove("temp.txt");
fs::create_directories("a/b/c");      // creates all intermediate

// Directory iteration
for (const auto& entry : fs::directory_iterator("/path")) {
    if (entry.is_regular_file()) {
        std::cout << entry.path() << " : " << entry.file_size() << '\n';
    }
}

// Recursive iteration
for (const auto& entry : fs::recursive_directory_iterator("/path")) {
    if (entry.path().extension() == ".cpp") {
        process(entry.path());
    }
}
```

### Console Input (cin)

`std::cin` is an input stream, counterpart to `std::cout`. The `>>` operator extracts formatted input, skipping whitespace.

```cpp
#include <iostream>
#include <string>

// Basic input
std::string name;
std::cout << "Enter name: ";
std::cin >> name;  // reads until whitespace
std::cout << "Hello, " << name << '\n';

// Multiple values
int age;
double height;
std::cin >> age >> height;  // space/newline separated

// Full line input (including spaces)
std::string full_name;
std::cout << "Enter full name: ";
std::getline(std::cin, full_name);
```

**Input direction**: `cin >> variable` - data flows FROM stream TO variable (arrows point right). Contrast with `cout << value` - data flows TO stream (arrows point left).

**Input validation**:

```cpp
int value;
while (!(std::cin >> value)) {
    std::cin.clear();   // clear error flags
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::cout << "Invalid input. Try again: ";
}
```

### Locale and Encoding

Console encoding issues are common with non-ASCII text. Standard C++ locale controls formatting/encoding:

```cpp
#include <locale>

// Set locale for the program
std::setlocale(LC_ALL, "");  // use system locale

// C++ locale on streams
std::cout.imbue(std::locale(""));  // system default
```

On Windows, console encoding is often incompatible with string literals. Non-ASCII console output is unreliable across platforms - stick to ASCII for console I/O in portable code. For file I/O, explicitly use UTF-8 encoding.

## Gotchas

- **Issue:** Not checking if file opened successfully -> silent failure, empty reads -> **Fix:** Always check `if (!file)` after construction or use exceptions: `file.exceptions(std::ios::failbit)`
- **Issue:** Mixing `>>` and `getline` - `>>` leaves `\n` in buffer, next `getline` reads empty -> **Fix:** Call `std::cin.ignore()` or `getline` to consume the newline before switching modes
- **Issue:** `fs::remove_all` can follow symlinks on some platforms -> **Fix:** Check with `fs::is_symlink` before recursive delete
- **Issue:** Text mode on Windows adds `\r\n` - corrupts binary data -> **Fix:** Always use `std::ios::binary` for non-text files
- **Issue:** Non-ASCII text in console garbled on Windows -> **Fix:** Use ASCII for console, UTF-8 for files. Don't rely on `setlocale` for cross-platform console encoding
- **Issue:** `cin >> string_var` only reads until first whitespace -> **Fix:** Use `std::getline(std::cin, var)` for full-line input

## See Also

- [[string-handling]]
- [[raii-resource-management]]
- [[error-handling]]
- [cppreference: filesystem](https://en.cppreference.com/w/cpp/filesystem)
