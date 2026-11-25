---
title: "CMake et systèmes de build"
category: tools
tags: [cpp, cmake, build, compilation, linking]
level: 3
source_sha256: 5019124803f77d7c89b0b8a7607397c4645a0617a4b2ed5a012de54c4aa4a8c1
translation: machine
translated_at: '2026-10-24'
---
# CMake et systèmes de build {#cmake-and-build-systems}

CMake est le générateur de systèmes de build C++ de facto. Il permet de définir les cibles, les dépendances et les options du compilateur de manière déclarative, dans un fichier `CMakeLists.txt`.

## Points clés {#key-facts}

- CMake génère les fichiers de build natifs (Makefiles, Ninja, solutions VS, projets Xcode)
- CMake moderne (3.x) est orienté cibles : les commandes `target_*` remplacent les commandes globales `include_directories`/`link_libraries`
- Cibles : `add_executable`, `add_library` (STATIC, SHARED, INTERFACE, OBJECT)
- `target_link_libraries` propage les répertoires d'inclusion, les définitions de compilation et les options via `PUBLIC`/`PRIVATE`/`INTERFACE`
- `find_package` localise les bibliothèques installées ; `FetchContent` télécharge et compile les dépendances
- Expressions de générateur : `$<BUILD_INTERFACE:...>` / `$<INSTALL_INTERFACE:...>` pour les paramètres dépendant du contexte
- `CMAKE_CXX_STANDARD` définit la version du standard C++ (17, 20, 23)
- Builds hors source : `cmake -B build -S .` puis `cmake --build build`
- Presets (CMakePresets.json) : standardisent les configurations de build au sein de l'équipe
- `ccache` / `sccache` pour la mise en cache de la compilation ; `ninja` pour des builds plus rapides

## Modèles {#patterns}

### Projet minimal {#minimal-project}

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(myapp src/main.cpp src/app.cpp)
target_include_directories(myapp PRIVATE ${CMAKE_SOURCE_DIR}/include)
```

### Bibliothèque + exécutable {#library-executable}

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

### Recherche des dépendances {#finding-dependencies}

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

### Tests avec CTest {#testing-with-ctest}

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

### Avertissements du compilateur {#compiler-warnings}

```cmake
# Per-target warnings (modern approach)
target_compile_options(mylib PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic -Werror>
)
```

### Commandes de build {#build-commands}

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

## Pièges {#gotchas}

- **Problème :** utiliser `include_directories` (global) au lieu de `target_include_directories` -> pollue toutes les cibles -> **Correction :** toujours utiliser les commandes `target_*` avec PRIVATE/PUBLIC/INTERFACE
- **Problème :** `find_package` échoue car la bibliothèque ne se trouve pas dans CMAKE_PREFIX_PATH -> **Correction :** définir `-DCMAKE_PREFIX_PATH=/path/to/lib` lors de la configuration, ou utiliser `FetchContent` pour des builds autonomes
- **Problème :** oublier `CMAKE_CXX_STANDARD_REQUIRED ON` -> CMake revient silencieusement à un standard antérieur -> **Correction :** toujours définir à la fois `CMAKE_CXX_STANDARD` et `CMAKE_CXX_STANDARD_REQUIRED`
- **Problème :** les builds dans les sources créent un désordre de fichiers générés à côté du code source -> **Correction :** toujours utiliser un build hors source : `cmake -B build`

## Voir aussi {#see-also}

- [Optimisation des performances](performance-optimization.md)
- [[const-and-type-safety]]
- [Documentation CMake](https://cmake.org/cmake/help/latest/)
- [Guide Modern CMake](https://cliutils.gitlab.io/modern-cmake/)
