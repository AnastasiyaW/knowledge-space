---
title: "CMake und Build-Systeme"
category: tools
tags: [cpp, cmake, build, compilation, linking]
level: 3
source_sha256: 5019124803f77d7c89b0b8a7607397c4645a0617a4b2ed5a012de54c4aa4a8c1
translation: machine
translated_at: '2026-10-24'
---
# CMake und Build-Systeme {#cmake-and-build-systems}

CMake ist der де-facto-Standard zur Generierung von Build-Systemen für C++. Es definiert Targets, Abhängigkeiten und Compiler-Optionen in einer deklarativen `CMakeLists.txt`.

## Wichtigste Fakten {#key-facts}

- CMake erzeugt native Build-Dateien (Makefiles, Ninja, VS-Solutions, Xcode-Projekte)
- Modernes CMake (3.x) ist Target-basiert: `target_*`-Befehle ersetzen die globalen `include_directories`/`link_libraries`
- Targets: `add_executable`, `add_library` (STATIC, SHARED, INTERFACE, OBJECT)
- `target_link_libraries` überträgt Include-Verzeichnisse, Compile-Definitionen und Flags über `PUBLIC`/`PRIVATE`/`INTERFACE`
- `find_package` findet installierte Bibliotheken; `FetchContent` lädt Abhängigkeiten herunter und baut sie
- Generatorausdrücke: `$<BUILD_INTERFACE:...>` / `$<INSTALL_INTERFACE:...>` für kontextabhängige Einstellungen
- `CMAKE_CXX_STANDARD` legt die C++-Standardversion fest (17, 20, 23)
- Out-of-Source-Builds: `cmake -B build -S .` gefolgt von `cmake --build build`
- Presets (CMakePresets.json): vereinheitlichen Build-Konfigurationen im Team
- `ccache` / `sccache` für Compilation-Caching; `ninja` für schnellere Builds

## Muster {#patterns}

### Minimales Projekt {#minimal-project}

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(myapp src/main.cpp src/app.cpp)
target_include_directories(myapp PRIVATE ${CMAKE_SOURCE_DIR}/include)
```

### Bibliothek + Executable {#library-executable}

```cmake
# Library
add_library(mylib
    src/core.cpp
    src/utils.cpp
)
target_include_directories(mylib PUBLIC include)
target_compile_features(mylib PUBLIC cxx_std_20)

# Executable using the library
add_executable(myapp src/main.cpp)
target_link_libraries(myapp PRIVATE mylib)
```

### Abhängigkeiten finden {#finding-dependencies}

```cmake
# System-installed library
find_package(Threads REQUIRED)
find_package(Boost 1.80 REQUIRED COMPONENTS filesystem system)

target_link_libraries(myapp PRIVATE
    Threads::Threads
    Boost::filesystem
    Boost::system
)

# Download and build dependency (C++17)
include(FetchContent)
FetchContent_Declare(
    fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG 10.2.1
)
FetchContent_MakeAvailable(fmt)
target_link_libraries(myapp PRIVATE fmt::fmt)
```

### Testen mit CTest {#testing-with-ctest}

```cmake
enable_testing()

# With GoogleTest
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0
)
FetchContent_MakeAvailable(googletest)

add_executable(tests test/test_core.cpp)
target_link_libraries(tests PRIVATE mylib GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(tests)
```

### Compiler-Warnungen {#compiler-warnings}

```cmake
# Per-target warnings (modern approach)
target_compile_options(mylib PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic -Werror>
)
```

### Build-Befehle {#build-commands}

```bash
# Configure
cmake -B build -S . -G Ninja -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build --parallel $(nproc)

# Run tests
cd build && ctest --output-on-failure

# Install
cmake --install build --prefix /usr/local
```

### CMakePresets.json {#cmakepresetsjson}

```json
{
  "version": 6,
  "configurePresets": [
    {
      "name": "dev",
      "binaryDir": "build/dev",
      "generator": "Ninja",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_CXX_STANDARD": "20",
        "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
      }
    },
    {
      "name": "release",
      "binaryDir": "build/release",
      "generator": "Ninja",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    }
  ]
}
```

## Fallstricke {#gotchas}

- **Problem:** Verwendung von `include_directories` (global) statt `target_include_directories` -> verschmutzt alle Targets -> **Lösung:** Immer `target_*`-Befehle mit PRIVATE/PUBLIC/INTERFACE verwenden
- **Problem:** `find_package` schlägt fehl, weil die Bibliothek nicht in `CMAKE_PREFIX_PATH` liegt -> **Lösung:** `-DCMAKE_PREFIX_PATH=/path/to/lib` beim Konfigurieren setzen oder `FetchContent` für eigenständige Builds verwenden
- **Problem:** `CMAKE_CXX_STANDARD_REQUIRED ON` wird vergessen -> CMake fällt stillschweigend auf einen älteren Standard zurück -> **Lösung:** Immer sowohl `CMAKE_CXX_STANDARD` als auch `CMAKE_CXX_STANDARD_REQUIRED` setzen
- **Problem:** In-Source-Builds erzeugen ein Durcheinander generierter Dateien neben dem Quellcode -> **Lösung:** Immer Out-of-Source-Builds verwenden: `cmake -B build`

## Siehe auch {#see-also}

- [Performance-Optimierung](performance-optimization.md)
- [[const-and-type-safety]]
- [CMake-Dokumentation](https://cmake.org/cmake/help/latest/)
- [Modern-CMake-Leitfaden](https://cliutils.gitlab.io/modern-cmake/)
