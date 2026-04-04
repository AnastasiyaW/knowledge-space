---
title: CMake and Build Systems
category: tools
tags: [cpp, cmake, build, compilation, linking]
---

# CMake and Build Systems

CMake is the de facto standard C++ build system generator. Defines targets, dependencies, and compiler options in a declarative `CMakeLists.txt`.

## Key Facts

- CMake generates native build files (Makefiles, Ninja, VS solutions, Xcode projects)
- Modern CMake (3.x) is target-based: `target_*` commands replace global `include_directories`/`link_libraries`
- Targets: `add_executable`, `add_library` (STATIC, SHARED, INTERFACE, OBJECT)
- `target_link_libraries` propagates include dirs, compile defs, and flags through `PUBLIC`/`PRIVATE`/`INTERFACE`
- `find_package` locates installed libraries; `FetchContent` downloads and builds dependencies
- Generator expressions: `$<BUILD_INTERFACE:...>` / `$<INSTALL_INTERFACE:...>` for context-dependent settings
- `CMAKE_CXX_STANDARD` sets C++ standard version (17, 20, 23)
- Out-of-source builds: `cmake -B build -S .` then `cmake --build build`
- Presets (CMakePresets.json): standardize build configurations across team
- `ccache` / `sccache` for compilation caching; `ninja` for faster builds

## Patterns

### Minimal Project

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(myapp src/main.cpp src/app.cpp)
target_include_directories(myapp PRIVATE ${CMAKE_SOURCE_DIR}/include)
```

### Library + Executable

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

### Finding Dependencies

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

### Testing with CTest

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

### Compiler Warnings

```cmake
# Per-target warnings (modern approach)
target_compile_options(mylib PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic -Werror>
)
```

### Build Commands

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

### CMakePresets.json

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

## Gotchas

- **Issue:** Using `include_directories` (global) instead of `target_include_directories` -> pollutes all targets -> **Fix:** Always use `target_*` commands with PRIVATE/PUBLIC/INTERFACE
- **Issue:** `find_package` fails because library not in CMAKE_PREFIX_PATH -> **Fix:** Set `-DCMAKE_PREFIX_PATH=/path/to/lib` at configure time or use `FetchContent` for self-contained builds
- **Issue:** Forgetting `CMAKE_CXX_STANDARD_REQUIRED ON` -> CMake silently falls back to older standard -> **Fix:** Always set both `CMAKE_CXX_STANDARD` and `CMAKE_CXX_STANDARD_REQUIRED`
- **Issue:** In-source builds create mess of generated files alongside source -> **Fix:** Always use out-of-source build: `cmake -B build`

## See Also

- [[performance-optimization]]
- [[const-and-type-safety]]
- [CMake documentation](https://cmake.org/cmake/help/latest/)
- [Modern CMake guide](https://cliutils.gitlab.io/modern-cmake/)
