# Cross-Platform C++ Desktop Application (Mac + Windows)

Reference for platform differences when building C++ desktop apps (with ML inference) targeting both Windows and macOS. Covers filesystem, GPU, security, build system, deployment.

See [[cross-platform-ml-inference]] for ONNX Runtime execution provider selection.

## Filesystem Differences

### Standard App Directories

| Purpose | Windows | macOS |
|---------|---------|-------|
| User data | `%APPDATA%` (`AppData\Roaming`) | `~/Library/Application Support/` |
| Local cache | `%LOCALAPPDATA%` | `~/Library/Caches/` |
| Temp files | `%TEMP%` | `$TMPDIR` (`/var/folders/.../T/`) |
| Preferences | `%APPDATA%` (same as data) | `~/Library/Preferences/` |
| Logs | `%LOCALAPPDATA%\MyApp\Logs` (no standard) | `~/Library/Logs/` |
| Install | `C:\Program Files\` | `/Applications/` |

Use `std::filesystem::path` — handles separators automatically on both platforms.

### File Locking Behavior

| Aspect | Windows | macOS |
|--------|---------|-------|
| Lock type | **Mandatory** — other processes cannot open locked file | **Advisory** — other processes can ignore lock |
| Delete open file | Impossible (file is in use) | Possible (Unix unlink semantics) |
| Rename open file | Impossible | Possible |

Windows mandatory locking complicates auto-updaters: need helper process or staged update (write to temp, rename on next launch).

### Extended Attributes / Quarantine

| Platform | Mechanism | Quarantine flag |
|----------|-----------|----------------|
| Windows (NTFS) | Alternate Data Streams: `file.txt:Zone.Identifier` | `Zone.Id=3` |
| macOS (APFS) | xattr: `com.apple.quarantine` | Set on downloaded files |

Downloaded files (models, updaters) will have quarantine attributes. On macOS this triggers Gatekeeper; on Windows triggers SmartScreen.

### Path Limits

- **Windows**: `MAX_PATH=260` by default. Enable long paths via `longPathAware` in app manifest. `std::filesystem` uses `\\?\` prefix internally.
- **macOS**: no hard limit (`PATH_MAX=1024` advisory).

## Code Signing

### Windows (Authenticode + SmartScreen)

- Requires Authenticode certificate (OV or EV), ~$200-600/year
- SmartScreen accumulates reputation over time — even signed apps from new publishers show warning
- Azure Trusted Signing available since October 2025 (US/Canada)

### macOS (Developer ID + Notarization)

**Required** for distribution outside Mac App Store:

1. Code sign with Developer ID Application certificate (`$99/year`)
2. Notarize: upload binary to Apple, get ticket back
3. Staple: `xcrun stapler staple MyApp.app` — embeds ticket for offline Gatekeeper

**Hardened Runtime** required for notarization:

```bash
# Entitlements for ML plugin:
com.apple.security.network.client           # for license checks
com.apple.security.files.user-selected.read-write  # for image import
com.apple.security.cs.allow-unsigned-executable-memory  # for GPU compute
```

Without notarization, app **will not launch** on macOS 10.15+.

**Anti-debug benefit**: Hardened Runtime disables `DYLD_INSERT_LIBRARIES` injection and prohibits disabling ASLR — acts as built-in anti-tamper measure.

## GPU APIs

| API | Windows | macOS |
|-----|---------|-------|
| DirectX 12 / DirectML | Primary ML API | N/A |
| Metal | N/A | Primary GPU API |
| CoreML | N/A | ML framework (GPU + Neural Engine) |
| CUDA | NVIDIA only | N/A (Apple removed NVIDIA) |
| Vulkan | Native | Via MoltenVK (slower than native Metal) |
| OpenCL | Legacy support | Deprecated since 10.14 |

### Apple Silicon: Neural Engine

Accessible **only via CoreML** — no low-level API. Best for CNNs and quantized models. Transformer inference is faster on Metal GPU than Neural Engine. Unified Memory means no CPU↔GPU copy overhead; model loaded in RAM is instantly accessible to GPU.

**MoltenVK performance note:** native Metal outperforms MoltenVK on Apple GPU — confirmed by llama.cpp benchmarks. Use MoltenVK only when macOS is a secondary target.

## Build System

### Compiler Differences

| Aspect | MSVC (Windows) | Apple Clang (macOS) |
|--------|----------------|---------------------|
| C++ ABI | Microsoft ABI | Itanium ABI |
| stdlib | MSVC STL | libc++ |
| C++20 | Full (VS 2022 17.x) | Full |
| Sanitizers | ASan | ASan, UBSan, TSan |

`std::string` layout differs (different SSO buffer size). `wchar_t` is 2 bytes (UTF-16) on Windows, 4 bytes (UTF-32) on macOS — never serialize `wstring` across platforms.

### CMake Cross-Platform Setup

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyMLApp LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

if(WIN32)
    add_definitions(-DUNICODE -D_UNICODE)
    # Static runtime: simpler deployment, avoids VC++ redist requirement
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
elseif(APPLE)
    # Universal Binary: supports Intel + Apple Silicon in one file
    set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64")
    set(CMAKE_OSX_DEPLOYMENT_TARGET "13.0")
endif()

find_package(onnxruntime REQUIRED)
target_link_libraries(myapp PRIVATE onnxruntime::onnxruntime)

if(WIN32)
    target_link_libraries(myapp PRIVATE DirectML)
elseif(APPLE)
    target_link_libraries(myapp PRIVATE
        "-framework CoreML" "-framework Metal" "-framework Foundation"
    )
endif()
```

### Universal Binary (macOS)

One binary containing both `arm64` and `x86_64`. All dependencies must also be universal.

```bash
# Combine separate arch builds:
lipo -create arm64/libfoo.dylib x86_64/libfoo.dylib -output libfoo.dylib
```

**Rosetta 2 removal**: Apple announced removal in macOS 28 (2027). Native `arm64` build is mandatory, not optional.

### DLL/dylib Search Order

**Windows DLL search** (simplified):
1. EXE directory
2. System32
3. Current working directory (**dangerous** — DLL hijacking)
4. PATH entries

Mitigate: `SetDllDirectory("")` removes CWD from search.

**macOS dylib** uses `@rpath`:
```cmake
set_target_properties(target PROPERTIES
    INSTALL_RPATH "@executable_path/../Frameworks"
)
```

## Unicode Handling

**Key difference**: Windows API is UTF-16; macOS/POSIX is UTF-8.

```cpp
// Keep all internal strings as UTF-8 (std::string)
// Convert at Windows API boundary:
#ifdef _WIN32
std::wstring utf8_to_wide(const std::string& utf8) {
    int len = MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, nullptr, 0);
    std::wstring wide(len - 1, 0);
    MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, &wide[0], len);
    return wide;
}
// Use wide API variants: CreateFileW, LoadLibraryW, etc.
#endif
```

Use Boost.Nowide to transparently handle UTF-8 on Windows (`std::fstream`, `std::cout`).

## Security / Credential Storage

| Platform | API | Notes |
|----------|-----|-------|
| Windows | DPAPI + Credential Manager (`CredWrite`/`CredRead`) | Any app of same user can read — no ACL per item |
| macOS | Keychain (`SecItemAdd`/`SecItemCopyMatching`) | Per-item ACL, prompts on foreign app access |

Cross-platform wrapper: `keychain` C++ library (GitHub: hrantzsch/keychain) abstracts both.

**For license keys**: store via platform credential API + encrypt the data additionally (defense in depth).

## Installation / Distribution

### Installer Formats

**Windows:**

| Format | Use Case |
|--------|----------|
| WiX (MSI) | Corporate / GPO deployment — IT prefers MSI |
| NSIS / Inno Setup | Simpler EXE installer, broad adoption |
| MSIX | Modern sandbox, auto-update, requires cert |

**macOS:**
- DMG with drag-to-Applications is user expectation
- `.pkg` inside DMG if system-level file placement needed

### Auto-Update

| Component | Windows | macOS |
|-----------|---------|-------|
| Framework | WinSparkle | Sparkle |
| Format | Appcast XML | Appcast XML |
| Signature check | Authenticode | Apple codesign |
| Restart | Needs helper (mandatory file locking) | Can update in-place |

### Crash Reporting: Crashpad + Sentry

Crashpad (Google, open-source) handles crash capture on both platforms. Sentry accepts Minidump + PDB/dSYM for symbolication:

```bash
# CI: upload debug symbols
sentry-cli debug-files upload --include-sources ./build/Release/*.pdb    # Windows
sentry-cli debug-files upload --include-sources ./build/Release/*.dSYM   # macOS
```

## Testing Matrix

### Minimum Matrix

| OS | Arch | GPU | Priority |
|----|------|-----|----------|
| Windows 10 22H2 | x64 | NVIDIA (CUDA + DirectML) | P0 |
| Windows 10 22H2 | x64 | AMD (DirectML only) | P0 |
| Windows 10 22H2 | x64 | Intel iGPU (DirectML) | P1 |
| Windows 11 24H2 | x64 | NVIDIA | P1 |
| macOS 14 Sonoma | arm64 (M1-M3) | Apple GPU (CoreML) | P0 |
| macOS 15 Sequoia | arm64 (M1-M4) | Apple GPU | P1 |
| macOS 14 Sonoma | x86_64 Intel | AMD/Intel GPU | P2 |

### Platform-Specific Critical Test Cases

| Test | Windows | macOS |
|------|---------|-------|
| First launch | SmartScreen warning | Gatekeeper + quarantine xattr check |
| GPU inference | DirectML fallback if no CUDA | CoreML + Neural Engine vs CPU |
| VRAM OOM | DirectML OOM → CPU fallback | Unified memory — no OOM, but swap |
| Installer | Long paths (Cyrillic username = edge case) | DMG drag-to-Apps; notarization check |
| Update | Helper process for file replacement | In-place file replacement OK |
| Corporate proxy | SSL inspection via Windows cert store | SSL inspection via System Keychain |
| Sleep/wake | GPU device lost on wake | Metal device survives |

## Summary: Platform Quick Reference

| Component | Windows | macOS Intel | macOS Apple Silicon |
|-----------|---------|-------------|---------------------|
| GPU inference | CUDA or DirectML | CPU only | CoreML + Neural Engine |
| Code signing | Authenticode | Developer ID + Notarization | Developer ID + Notarization |
| File locking | Mandatory | Advisory | Advisory |
| Unicode | UTF-16 API boundary | UTF-8 everywhere | UTF-8 everywhere |
| Installer | MSI / NSIS / MSIX | DMG + pkg | DMG (Universal Binary) |
| Crash symbols | PDB + WER/Crashpad | dSYM + Crashpad | dSYM + Crashpad |
| Auto-update | WinSparkle | Sparkle | Sparkle |
| Credential storage | DPAPI / Credential Manager | Keychain | Keychain + Secure Enclave |
| C++ stdlib | MSVC STL | libc++ | libc++ |
| ARM native | Minimal (Win ARM is niche) | N/A | **Required** (Rosetta gone 2027) |

## Gotchas

- **Windows mandatory locking blocks auto-update**: DLL and model files cannot be replaced while loaded. Pattern: write to `*.new` temp file, rename on next launch via helper process. Failing to do this causes "file is in use" errors during update.
- **macOS Rosetta 2 removal in 2027**: Apple Silicon native `arm64` build is mandatory. Apps shipping x86_64-only via Rosetta will stop working. Universal Binary (`x86_64;arm64`) is the safe default.
- **`wchar_t` size mismatch**: 2 bytes on Windows (UTF-16), 4 bytes on macOS (UTF-32). Never serialize `std::wstring` to files or IPC channels intended for cross-platform use. Keep internal strings in `std::string` (UTF-8) and convert at API boundaries.
- **Windows SmartScreen reputation delay**: even a correctly signed binary from a new publisher shows "Windows protected your PC" for weeks/months until download count builds reputation. EV certificates used to grant instant reputation; since August 2024 Microsoft equalized OV and EV.
- **macOS without notarization = unlaunchable**: `xcrun notarytool` + `xcrun stapler` are mandatory steps in the release pipeline for macOS 10.15+. Apps not stapled also fail on hosts with no internet (Gatekeeper can't check online).
- **`Sleep(1)` on Windows = ~15.6ms**: Windows timer resolution defaults to 15.6ms. Call `timeBeginPeriod(1)` to get ~1ms resolution — but this increases system-wide power consumption. Use `std::this_thread::sleep_for` which wraps QPC; it inherits the same resolution.
- **Decimal separator locale bug**: `atof("1.5")` returns 1 when system locale uses comma as decimal separator. Always set `setlocale(LC_NUMERIC, "C")` or use `std::locale::global(std::locale::classic())` before any numeric parsing.
- **CEP extensions removed in PS 2025**: Photoshop 2025 (v26) no longer shows legacy CEP extensions in the UI. Apple Silicon never supported CEP (requires Rosetta). New plugins must use UXP or UXP Hybrid.

## See Also

- [[cross-platform-ml-inference]] - ONNX Runtime execution provider selection (DirectML, CoreML, CUDA)
- [[photoshop-plugin-architecture]] - UXP Hybrid plugin, C++ .uxpaddon, Lightroom SDK
