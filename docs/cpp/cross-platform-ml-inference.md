---
title: Cross-Platform C++ for ML Inference
category: reference
tags: [cpp, cross-platform, onnx-runtime, directml, coreml, metal, windows, macos, apple-silicon, ml-inference]
aliases: ["Mac vs Windows ML", "Cross-Platform ONNX"]
---

# Cross-Platform C++ for ML Inference

Reference for building C++ desktop applications with ML inference that target both Windows and macOS. Covers ONNX Runtime execution providers, GPU API differences, filesystem quirks, build system setup, and deployment.

## GPU API Landscape

| API | Windows | macOS |
|-----|---------|-------|
| DirectX 12 / DirectML | Primary for ML | N/A |
| Metal | N/A | Primary GPU API |
| CoreML | N/A | ML framework (GPU + Neural Engine) |
| CUDA | NVIDIA only | N/A (Apple removed NVIDIA) |
| Vulkan | Native | Via MoltenVK (slower than native Metal) |
| OpenCL | NVIDIA/AMD/Intel | Deprecated since macOS 10.14 |
| OpenGL | Legacy | Deprecated, frozen at 4.1 |

## ONNX Runtime Execution Provider Selection

```cpp
Ort::SessionOptions session_options;

#ifdef _WIN32
  // Windows: CUDA > DirectML > CPU
  try {
    OrtCUDAProviderOptions cuda_opts{};
    session_options.AppendExecutionProvider_CUDA(cuda_opts);
  } catch (...) {
    OrtSessionOptionsAppendExecutionProvider_DML(session_options, 0);
  }
#elif defined(__APPLE__)
  // macOS: CoreML > CPU
  uint32_t coreml_flags = COREML_FLAG_ENABLE_ON_SUBGRAPH;
  OrtSessionOptionsAppendExecutionProvider_CoreML(session_options, coreml_flags);
#endif
```

**DirectML**: works with any DX12 GPU (NVIDIA, AMD, Intel). One binary for all vendors. In maintenance mode (2026) - stable, no new features. Falls back to shared system memory when VRAM exhausted.

**CoreML**: uses Metal GPU + Neural Engine on Apple Silicon. Neural Engine is optimal for CNNs, GPU via Metal is faster for transformer inference. Must be explicitly registered at session creation.

## Apple Silicon Specifics

```text
Unified Memory Architecture:
  - CPU and GPU share the SAME physical memory
  - No data copying between CPU/GPU - pointer passing
  - No separate VRAM - ML model and app share all RAM
  - Bandwidth: 200-800 GB/s (vs 32 GB/s PCIe 4.0)

Neural Engine:
  - Accessible ONLY through CoreML (no low-level API)
  - Optimal for: quantized models, convolutions, matrix ops
  - NOT optimal for: arbitrary compute, custom operators
  - CNN inference: NE faster; Transformer inference: Metal GPU faster

M1 8GB: ~5-6 GB available for ML (OS + apps take the rest)
```

**Rosetta 2 removal**: Apple announced removal in macOS 28 (2027). Native arm64 build is mandatory.

## Filesystem Differences

| Aspect | Windows | macOS |
|--------|---------|-------|
| Path separator | `\` (but `/` works in most APIs) | `/` |
| Max path | 260 chars (32,767 with `\\?\` prefix) | No hard limit |
| Case sensitivity | No (NTFS default) | No (APFS default) |
| File locking | **Mandatory** (cannot delete open files) | **Advisory** (can delete open files) |
| App data | `%APPDATA%` | `~/Library/Application Support/` |
| Cache | `%LOCALAPPDATA%\Temp\` | `~/Library/Caches/` |
| Config | `%APPDATA%` | `~/Library/Preferences/` |

```cpp
// Always use std::filesystem::path - handles separators automatically
namespace fs = std::filesystem;
fs::path config = get_app_data_dir() / "MyApp" / "config.json";
// NEVER concatenate strings with "/" or "\\"
```

**MAX_PATH fix**: enable `longPathAware` in application manifest, or use `\\?\` prefix for Win32 API. `std::filesystem` handles this automatically on newer SDKs.

**Library**: [PlatformFolders](https://github.com/sago007/PlatformFolders) abstracts standard directories cross-platform.

## DLL/dylib Loading

**Windows search order**: EXE dir > System32 > Windows dir > CWD (dangerous!) > PATH. Fix: `SetDllDirectory("")` removes CWD from search.

**macOS search**: `@executable_path` > `@loader_path` > `@rpath` > `DYLD_LIBRARY_PATH` (disabled in Hardened Runtime!). Use `@rpath` and set via CMake:

```cmake
set_target_properties(target PROPERTIES
    INSTALL_RPATH "@executable_path/../Frameworks")
```

## Code Signing and Distribution

**Windows (Authenticode + SmartScreen):**

- OV or EV certificate (~$200-600/year)
- EV no longer gives instant SmartScreen trust (since Aug 2024)
- SmartScreen builds reputation over time - new publishers always get warnings
- Azure Trusted Signing available for US/Canada (since Oct 2025)

**macOS (codesign + notarization + Gatekeeper):**

- Developer ID via Apple Developer Program ($99/year)
- Hardened Runtime **required** for notarization
- Notarization: upload to Apple for automated scan, receive ticket
- Without notarization, app **will not launch** (macOS 10.15+)
- Hardened Runtime blocks `DYLD_INSERT_LIBRARIES` injection, disables ASLR override

## Build System (CMake)

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyMLApp LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

if(WIN32)
    add_definitions(-DUNICODE -D_UNICODE)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
elseif(APPLE)
    set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64")  # Universal Binary
    set(CMAKE_OSX_DEPLOYMENT_TARGET "13.0")
endif()

find_package(onnxruntime REQUIRED)
target_link_libraries(myapp PRIVATE onnxruntime::onnxruntime)

if(WIN32)
    target_link_libraries(myapp PRIVATE DirectML)
elseif(APPLE)
    target_link_libraries(myapp PRIVATE
        "-framework CoreML" "-framework Metal" "-framework Foundation")
endif()
```

**Universal Binary pitfalls**: all dependencies must also be universal. Use `lipo` to combine single-arch libraries. Check ONNX Runtime provides universal C API build.

## Compiler Differences

| Aspect | MSVC (Windows) | Apple Clang (macOS) |
|--------|----------------|---------------------|
| C++ ABI | Microsoft ABI | Itanium ABI |
| stdlib | Microsoft STL | libc++ (LLVM) |
| Warnings | `/W4` | `-Wall -Wextra` |
| Sanitizers | ASan | ASan, UBSan, TSan |
| Exception handling | SEH | DWARF/zero-cost |
| Debug symbols | PDB | dSYM (DWARF) |

**Linking**: static for C++ deps (onnxruntime, curl), dynamic for system frameworks and GPU runtime (CUDA, DirectML, CoreML).

## Unicode Handling

```cpp
// Internal: UTF-8 everywhere (std::string)
// Windows API boundary: convert to UTF-16
#ifdef _WIN32
std::wstring utf8_to_wide(const std::string& utf8) {
    int len = MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, nullptr, 0);
    std::wstring wide(len - 1, 0);
    MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, &wide[0], len);
    return wide;
}
// Use wide API: CreateFileW, LoadLibraryW
#endif
```

`wchar_t` is 2 bytes on Windows (UTF-16), 4 bytes on macOS (UTF-32). **Never transfer wstring across platforms via IPC/files.**

Library: [Boost.Nowide](https://www.boost.org/libs/nowide/) - UTF-8 aware I/O on Windows.

## Credential Storage

| Aspect | Windows | macOS |
|--------|---------|-------|
| System | DPAPI + Credential Manager | Keychain Services |
| ACL per item | No - any app of same user can read | Yes - prompt on foreign app access |
| API | `CredWrite`/`CredRead` | `SecItemAdd`/`SecItemCopyMatching` |

Library: [keychain](https://github.com/hrantzsch/keychain) - cross-platform C++ abstraction.

## Networking (libcurl)

Use libcurl with **native TLS backend** per platform:

- **Windows**: libcurl + Schannel - uses Windows Certificate Store
- **macOS**: libcurl + Secure Transport (or OpenSSL with bundled CA)

This allows corporate proxy SSL inspection to work transparently. If using certificate pinning, add fallback to system store on verification failure.

## Auto-Update

| Component | Windows | macOS |
|-----------|---------|-------|
| Framework | WinSparkle (Sparkle port) | Sparkle |
| Update file | Appcast XML | Appcast XML |
| Restart | Helper process needed (mandatory locking) | Can update in place |

## Crash Reporting

**Crashpad** (Google, cross-platform) + **Sentry** (SaaS):

```bash
# Windows: upload PDB
sentry-cli debug-files upload --include-sources ./build/Release/*.pdb

# macOS: upload dSYM
sentry-cli debug-files upload --include-sources ./build/Release/*.dSYM
```

## Installers

| Platform | Recommended | Notes |
|----------|-------------|-------|
| Windows | WiX (MSI) or NSIS (EXE) | MSI for corporate GPO deployment |
| macOS | DMG with drag-to-Applications | pkg inside DMG if system components needed |

## Cross-Platform Pitfalls

| Pitfall | Details |
|---------|---------|
| Line endings | CR+LF (Win) vs LF (Mac). `std::getline` leaves trailing `\r` |
| Sleep precision | `Sleep(1)` = 15.6ms on Windows without `timeBeginPeriod(1)` |
| Locale decimal | `atof("1.5")` may parse as 1 in non-C locale. Force `setlocale(LC_NUMERIC, "C")` |
| Close window != quit | macOS: closing last window does NOT quit the app |
| Quarantine attrs | Downloaded files get quarantine mark: Zone.Identifier (Win) / com.apple.quarantine (Mac) |

## Testing Matrix (Minimum)

| OS | Architecture | GPU | Priority |
|----|-------------|-----|----------|
| Windows 10 22H2 | x64 | NVIDIA (CUDA+DirectML) | Primary |
| Windows 10 22H2 | x64 | AMD (DirectML) | Secondary |
| Windows 10 22H2 | x64 | Intel iGPU (DirectML) | Edge case |
| Windows 11 24H2 | x64 | NVIDIA | Primary |
| macOS 14+ | arm64 (M1-M4) | CoreML/Metal | Primary Mac |
| macOS 14+ | x86_64 (Intel) | CPU | Legacy |

**Critical test cases**: first launch (SmartScreen/Gatekeeper), GPU OOM graceful fallback, unicode in user paths (Cyrillic), sleep/wake GPU recovery, multiple GPU selection (dGPU vs iGPU on Windows).

## Gotchas

- **Mandatory vs advisory file locking**: on Windows, you cannot update a DLL/model while it is loaded. Need: close file, update, reopen, or staged update with rename on restart. macOS allows replacement but process keeps old inode until close
- **DirectML is in maintenance mode (2026)**: stable API, no new features. Production-safe but no performance improvements coming
- **Apple Silicon apps must be arm64 native**: Rosetta 2 removal in macOS 28 (2027) means x86_64-only binaries stop working. Build Universal Binary now
- **CoreML conversion can lose precision**: not all ONNX ops supported in CoreML. Some models need the ONNX Runtime CoreML EP as fallback instead of direct CoreML conversion
- **`std::string` SSO buffer size differs**: MSVC STL and libc++ have different small string optimization implementations. Never assume binary layout of std::string across platforms

## See Also

- [[cmake-build-systems]] - CMake configuration patterns
- [[concurrency]] - platform threading differences
- [[error-handling]] - exception handling across compilers
- [[low-vram-inference-strategies]] - GPU memory optimization techniques
