---
title: "Plattformübergreifendes C++ für ML-Inference"
category: reference
tags: [cpp, cross-platform, onnx-runtime, directml, coreml, metal, windows, macos, apple-silicon, ml-inference]
aliases: ["Mac vs Windows ML", "Cross-Platform ONNX"]
level: 4
source_sha256: b3282f5d497c9689a178e074c4d4a2c3cdd7da58e39e027d3c487d67c7ff20ea
translation: machine
translated_at: '2026-10-24'
---
# Plattformübergreifendes C++ für ML-Inference {#cross-platform-c-for-ml-inference}

Referenz für den Bau von C++-Desktopanwendungen mit ML-Inference für Windows und macOS. Behandelt ONNX-Runtime-Execution-Provider, Unterschiede der GPU-APIs, Eigenheiten des Dateisystems, Einrichtung des Build-Systems und Deployment.

## Landschaft der GPU-APIs {#gpu-api-landscape}

| API | Windows | macOS |
|-----|---------|-------|
| DirectX 12 / DirectML | Primär für ML | N/A |
| Metal | N/A | Primäre GPU-API |
| CoreML | N/A | ML-Framework (GPU + Neural Engine) |
| CUDA | Nur NVIDIA | N/A (Apple hat NVIDIA entfernt) |
| Vulkan | Nativ | Über MoltenVK (langsamer als natives Metal) |
| OpenCL | NVIDIA/AMD/Intel | Seit macOS 10.14 veraltet |
| OpenGL | Legacy | Veraltet, eingefroren bei 4.1 |

## Auswahl des ONNX-Runtime-Execution-Providers {#onnx-runtime-execution-provider-selection}

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

**DirectML**: funktioniert mit jeder DX12-GPU (NVIDIA, AMD, Intel). Ein Binary für alle Hersteller. Befindet sich 2026 im Wartungsmodus – stabil, keine neuen Features. Weicht auf gemeinsamen Systemspeicher aus, wenn der VRAM erschöpft ist.

**CoreML**: nutzt auf Apple Silicon die Metal-GPU und die Neural Engine. Die Neural Engine ist optimal für CNNs, für Transformer-Inference ist die GPU über Metal schneller. Muss bei der Session-Erstellung explizit registriert werden.

## Besonderheiten von Apple Silicon {#apple-silicon-specifics}

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

**Entfernung von Rosetta 2**: Apple hat die Entfernung in macOS 28 (2027) angekündigt. Ein nativer arm64-Build ist zwingend erforderlich.

## Unterschiede im Dateisystem {#filesystem-differences}

| Aspekt | Windows | macOS |
|--------|---------|-------|
| Pfadtrennzeichen | `\` (`/` funktioniert aber in den meisten APIs) | `/` |
| Maximale Pfadlänge | 260 Zeichen (32.767 mit `\\?\`-Präfix) | Keine feste Grenze |
| Groß-/Kleinschreibung | Nicht unterschieden (NTFS-Standard) | Nicht unterschieden (APFS-Standard) |
| Dateisperren | **Verbindlich** (geöffnete Dateien können nicht gelöscht werden) | **Empfehlend** (geöffnete Dateien können gelöscht werden) |
| App-Daten | `%APPDATA%` | `~/Library/Application Support/` |
| Cache | `%LOCALAPPDATA%\Temp\` | `~/Library/Caches/` |
| Konfiguration | `%APPDATA%` | `~/Library/Preferences/` |

```cpp
// Always use std::filesystem::path - handles separators automatically
namespace fs = std::filesystem;
fs::path config = get_app_data_dir() / "MyApp" / "config.json";
// NEVER concatenate strings with "/" or "\\"
```

**Fix für MAX_PATH**: `longPathAware` im Application-Manifest aktivieren oder das `\\?\`-Präfix für die Win32-API verwenden. `std::filesystem` übernimmt dies auf neueren SDKs automatisch.

**Bibliothek**: [PlatformFolders](https://github.com/sago007/PlatformFolders) abstrahiert Standardverzeichnisse plattformübergreifend.

## Laden von DLL/dylib {#dlldylib-loading}

**Suchreihenfolge unter Windows**: EXE-Verzeichnis > System32 > Windows-Verzeichnis > CWD (gefährlich!) > PATH. Fix: `SetDllDirectory("")` entfernt das CWD aus der Suche.

**Suche unter macOS**: `@executable_path` > `@loader_path` > `@rpath` > `DYLD_LIBRARY_PATH` (in der Hardened Runtime deaktiviert!). `@rpath` verwenden und über CMake setzen:

```cmake
set_target_properties(target PROPERTIES
    INSTALL_RPATH "@executable_path/../Frameworks")
```

## Code-Signing und Distribution {#code-signing-and-distribution}

**Windows (Authenticode + SmartScreen):**

- OV- oder EV-Zertifikat (ca. 200–600 $/Jahr)
- EV bringt seit August 2024 kein sofortiges SmartScreen-Vertrauen mehr
- SmartScreen baut Reputation über die Zeit auf – neue Publisher erhalten immer Warnungen
- Azure Trusted Signing verfügbar für USA/Kanada (seit Oktober 2025)

**macOS (codesign + Notarisierung + Gatekeeper):**

- Developer ID über das Apple Developer Program (99 $/Jahr)
- Hardened Runtime ist für die Notarisierung **erforderlich**
- Notarisierung: Upload zu Apple für automatisierten Scan, Empfang eines Tickets
- Ohne Notarisierung **startet die App nicht** (macOS 10.15+)
- Die Hardened Runtime blockiert `DYLD_INSERT_LIBRARIES`-Injection und deaktiviert das Überschreiben von ASLR

## Build-System (CMake) {#build-system-cmake}

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

**Stolperfallen bei Universal Binaries**: Alle Abhängigkeiten müssen ebenfalls universal sein. Single-Arch-Bibliotheken mit `lipo` zusammenführen. Prüfen, ob ONNX Runtime einen universellen C-API-Build bereitstellt.

## Unterschiede der Compiler {#compiler-differences}

| Aspekt | MSVC (Windows) | Apple Clang (macOS) |
|--------|----------------|---------------------|
| C++-ABI | Microsoft-ABI | Itanium-ABI |
| Standardbibliothek | Microsoft STL | libc++ (LLVM) |
| Warnungen | `/W4` | `-Wall -Wextra` |
| Sanitizer | ASan | ASan, UBSan, TSan |
| Exception-Handling | SEH | DWARF/Zero-Cost |
| Debug-Symbole | PDB | dSYM (DWARF) |

**Linken**: statisch für C++-Abhängigkeiten (onnxruntime, curl), dynamisch für System-Frameworks und GPU-Laufzeiten (CUDA, DirectML, CoreML).

## Unicode-Behandlung {#unicode-handling}

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

`wchar_t` ist unter Windows 2 Byte groß (UTF-16), unter macOS 4 Byte (UTF-32). **`wstring` niemals plattformübergreifend über IPC oder Dateien übertragen.**

Bibliothek: [Boost.Nowide](https://www.boost.org/libs/nowide/) – UTF-8-fähige I/O unter Windows.

## Speicherung von Zugangsdaten {#credential-storage}

| Aspekt | Windows | macOS |
|--------|---------|-------|
| System | DPAPI + Credential Manager | Keychain Services |
| ACL pro Eintrag | Nein – jede App desselben Benutzers kann lesen | Ja – Abfrage bei Zugriff durch fremde App |
| API | `CredWrite`/`CredRead` | `SecItemAdd`/`SecItemCopyMatching` |

Bibliothek: [keychain](https://github.com/hrantzsch/keychain) – plattformübergreifende C++-Abstraktion.

## Netzwerk (libcurl) {#networking-libcurl}

libcurl mit dem **nativen TLS-Backend** der jeweiligen Plattform verwenden:

- **Windows**: libcurl + Schannel – nutzt den Windows-Zertifikatspeicher
- **macOS**: libcurl + Secure Transport (oder OpenSSL mit gebündelten CA-Zertifikaten)

So funktioniert die SSL-Inspection von Unternehmens-Proxys transparent. Bei Certificate Pinning sollte bei Fehlschlägen der Verifikation ein Fallback auf den Systemspeicher ergänzt werden.

## Auto-Update {#auto-update}

| Komponente | Windows | macOS |
|-----------|---------|-------|
| Framework | WinSparkle (Sparkle-Portierung) | Sparkle |
| Update-Datei | Appcast XML | Appcast XML |
| Neustart | Helper-Prozess erforderlich (verbindliche Sperren) | Kann direkt an Ort und Stelle aktualisieren |

## Absturzberichte {#crash-reporting}

**Crashpad** (Google, plattformübergreifend) + **Sentry** (SaaS):

```bash
# Windows: upload PDB
sentry-cli debug-files upload --include-sources ./build/Release/*.pdb

# macOS: upload dSYM
sentry-cli debug-files upload --include-sources ./build/Release/*.dSYM
```

## Installer {#installers}

| Plattform | Empfohlen | Hinweise |
|----------|-----------|----------|
| Windows | WiX (MSI) oder NSIS (EXE) | MSI für Deployment per Unternehmens-GPO |
| macOS | DMG mit Drag-to-Applications | pkg innerhalb des DMG, falls Systemkomponenten benötigt werden |

## Plattformübergreifende Stolperfallen {#cross-platform-pitfalls}

| Stolperfalle | Details |
|-------------|---------|
| Zeilenenden | CR+LF (Win) vs. LF (Mac). `std::getline` lässt ein nachgestelltes `\r` stehen |
| Sleep-Genauigkeit | `Sleep(1)` = 15,6 ms unter Windows ohne `timeBeginPeriod(1)` |
| Locale-Dezimaltrennzeichen | `atof("1.5")` kann in einer Nicht-C-Locale als 1 geparst werden. `setlocale(LC_NUMERIC, "C")` erzwingen |
| Fenster schließen != Beenden | macOS: Das Schließen des letzten Fensters beendet die App NICHT |
| Quarantäne-Attribute | Heruntergeladene Dateien erhalten eine Quarantäne-Markierung: Zone.Identifier (Win) / com.apple.quarantine (Mac) |

## Testmatrix (Minimum) {#testing-matrix-minimum}

| OS | Architektur | GPU | Priorität |
|----|-------------|-----|-----------|
| Windows 10 22H2 | x64 | NVIDIA (CUDA+DirectML) | Primär |
| Windows 10 22H2 | x64 | AMD (DirectML) | Sekundär |
| Windows 10 22H2 | x64 | Intel iGPU (DirectML) | Randfall |
| Windows 11 24H2 | x64 | NVIDIA | Primär |
| macOS 14+ | arm64 (M1–M4) | CoreML/Metal | Primär (Mac) |
| macOS 14+ | x86_64 (Intel) | CPU | Legacy |

**Kritische Testfälle**: erster Start (SmartScreen/Gatekeeper), eleganter Fallback bei GPU-OOM, Unicode in Benutzerpfaden (kyrillisch), Recovery der GPU nach Sleep/Wake, Auswahl unter mehreren GPUs (dGPU vs. iGPU unter Windows).

## Stolperfallen (Gotchas) {#gotchas}

- **Verbindliche vs. empfehlende Dateisperren**: Unter Windows kann eine DLL/ein Modell, während es geladen ist, nicht aktualisiert werden. Lösung: Datei schließen, aktualisieren, erneut öffnen, oder ein gestaffeltes Update mit Umbenennen beim Neustart. macOS erlaubt das Ersetzen, der Prozess behält jedoch den alten Inode bis zum Schließen
- **DirectML befindet sich im Wartungsmodus (2026)**: stabile API, keine neuen Features. Produktionstauglich, aber es sind keine Performance-Verbesserungen zu erwarten
- **Apple-Silicon-Apps müssen nativ arm64 sein**: Die Entfernung von Rosetta 2 in macOS 28 (2027) bedeutet, dass reine x86_64-Binaries nicht mehr funktionieren. Jetzt ein Universal Binary bauen
- **Die CoreML-Konvertierung kann Genauigkeit verlieren**: Nicht alle ONNX-Operatoren werden von CoreML unterstützt. Manche Modelle benötigen statt der direkten CoreML-Konvertierung den ONNX-Runtime-CoreML-EP als Fallback
- **Die Größe des SSO-Puffers von `std::string` unterscheidet sich**: MSVC STL und libc++ implementieren die Small-String-Optimierung unterschiedlich. Das binäre Layout von `std::string` darf plattformübergreifend niemals vorausgesetzt werden

## Siehe auch {#see-also}

- [[cmake-build-systems]] – CMake-Konfigurationsmuster
- [Nebenläufigkeit - Threads, Async, Atomics](concurrency.md) – Unterschiede beim Threading zwischen Plattformen
- [Fehlerbehandlung - Exceptions und Alternativen](error-handling.md) – Exception-Handling über Compiler hinweg
- [[low-vram-inference-strategies]] – Techniken zur GPU-Speicheroptimierung
