---
level: 4
source_sha256: 4b779a2b8093160a248d164c83b55535a948b3e0461a681be4786f070a3cfab2
translation: machine
translated_at: '2026-10-24'
---
# Plattformübergreifende C++-Desktopanwendung (Mac + Windows) {#cross-platform-c-desktop-application-mac-windows}

Referenz für Plattformunterschiede beim Erstellen von C++-Desktopanwendungen (mit ML-Inferenz) für Windows und macOS. Behandelt Dateisystem, GPU, Sicherheit, Build-System und Deployment.

Siehe [[cross-platform-ml-inference]] zur Auswahl des ONNX-Runtime-Execution-Providers.

## Unterschiede im Dateisystem {#filesystem-differences}

### Standard-App-Verzeichnisse {#standard-app-directories}

| Zweck | Windows | macOS |
|-------|---------|-------|
| Benutzerdaten | `%APPDATA%` (`AppData\Roaming`) | `~/Library/Application Support/` |
| Lokaler Cache | `%LOCALAPPDATA%` | `~/Library/Caches/` |
| Temporäre Dateien | `%TEMP%` | `$TMPDIR` (`/var/folders/.../T/`) |
| Einstellungen | `%APPDATA%` (wie Daten) | `~/Library/Preferences/` |
| Protokolle | `%LOCALAPPDATA%\MyApp\Logs` (kein Standard) | `~/Library/Logs/` |
| Installation | `C:\Program Files\` | `/Applications/` |

`std::filesystem::path` verwenden – es behandelt Trennzeichen auf beiden Plattformen automatisch.

### Dateisperren-Verhalten {#file-locking-behavior}

| Aspekt | Windows | macOS |
|--------|---------|-------|
| Sperrtyp | **Obligatorisch** – andere Prozesse können eine gesperrte Datei nicht öffnen | **Advisory** – andere Prozesse können die Sperre ignorieren |
| Geöffnete Datei löschen | Nicht möglich (Datei wird verwendet) | Möglich (Unix-unlink-Semantik) |
| Geöffnete Datei umbenennen | Nicht möglich | Möglich |

Die obligatorische Sperrung unter Windows erschwert Auto-Updater: Erforderlich sind ein Hilfsprozess oder ein gestuftes Update (in eine temporäre Datei schreiben, beim nächsten Start umbenennen).

### Erweiterte Attribute / Quarantäne {#extended-attributes-quarantine}

| Plattform | Mechanismus | Quarantäne-Flag |
|-----------|-------------|-----------------|
| Windows (NTFS) | Alternate Data Streams: `file.txt:Zone.Identifier` | `Zone.Id=3` |
| macOS (APFS) | xattr: `com.apple.quarantine` | Bei heruntergeladenen Dateien gesetzt |

Heruntergeladene Dateien (Modelle, Updater) tragen Quarantäne-Attribute. Unter macOS löst dies Gatekeeper aus, unter Windows SmartScreen.

### Pfadlängen {#path-limits}

- **Windows**: `MAX_PATH=260` standardmäßig. Lange Pfade werden über `longPathAware` im App-Manifest aktiviert. `std::filesystem` verwendet intern das Präfix `\\?\`.
- **macOS**: keine harte Grenze (`PATH_MAX=1024` als Richtwert).

## Code-Signierung {#code-signing}

### Windows (Authenticode + SmartScreen) {#windows-authenticode-smartscreen}

- Erfordert ein Authenticode-Zertifikat (OV oder EV), ca. 200–600 $ pro Jahr
- SmartScreen baut Reputation über die Zeit auf – auch signierte Apps neuer Herausgeber zeigen eine Warnung
- Azure Trusted Signing seit Oktober 2025 verfügbar (USA/Kanada)

### macOS (Developer ID + Notarisierung) {#macos-developer-id-notarization}

**Erforderlich** für die Verteilung außerhalb des Mac App Store:

1. Mit einem Developer-ID-Application-Zertifikat signieren (`$99/year`)
2. Notarisieren: Binary an Apple hochladen und Ticket zurückerhalten
3. Stapeln: `xcrun stapler staple MyApp.app` – bettet das Ticket für Offline-Gatekeeper ein

**Hardened Runtime** ist für die Notarisierung erforderlich:

```bash
# Entitlements for ML plugin:
com.apple.security.network.client           # for license checks
com.apple.security.files.user-selected.read-write  # for image import
com.apple.security.cs.allow-unsigned-executable-memory  # for GPU compute
```

Ohne Notarisierung **startet die App nicht** unter macOS 10.15+.

**Schutz gegen Debugging**: Die Hardened Runtime deaktiviert die Injektion über `DYLD_INSERT_LIBRARIES` und untersagt das Abschalten von ASLR. Sie wirkt damit als eingebaute Schutzmaßnahme gegen Manipulation.

## GPU-APIs {#gpu-apis}

| API | Windows | macOS |
|-----|---------|-------|
| DirectX 12 / DirectML | Primäre ML-API | N/A |
| Metal | N/A | Primäre GPU-API |
| CoreML | N/A | ML-Framework (GPU + Neural Engine) |
| CUDA | Nur NVIDIA | N/A (Apple hat NVIDIA entfernt) |
| Vulkan | Nativ | Über MoltenVK (langsamer als natives Metal) |
| OpenCL | Legacy-Unterstützung | Seit 10.14 veraltet |

### Apple Silicon: Neural Engine {#apple-silicon-neural-engine}

Zugänglich **nur über CoreML** – es gibt keine Low-Level-API. Am besten geeignet für CNNs und quantisierte Modelle. Transformer-Inferenz ist auf der Metal-GPU schneller als auf der Neural Engine. Unified Memory bedeutet keinen Overhead durch CPU↔GPU-Kopien; im RAM geladene Modelle sind sofort für die GPU zugänglich.

**Hinweis zur MoltenVK-Performance:** Natives Metal übertrifft MoltenVK auf Apple-GPUs, bestätigt durch llama.cpp-Benchmarks. MoltenVK nur verwenden, wenn macOS ein sekundäres Ziel ist.

## Build-System {#build-system}

### Compiler-Unterschiede {#compiler-differences}

| Aspekt | MSVC (Windows) | Apple Clang (macOS) |
|--------|----------------|---------------------|
| C++-ABI | Microsoft-ABI | Itanium-ABI |
| Stdlib | MSVC STL | libc++ |
| C++20 | Vollständig (VS 2022 17.x) | Vollständig |
| Sanitizer | ASan | ASan, UBSan, TSan |

Das Layout von `std::string` unterscheidet sich (andere SSO-Puffergröße). `wchar_t` ist unter Windows 2 Byte groß (UTF-16), unter macOS 4 Byte (UTF-32). `wstring` niemals plattformübergreifend serialisieren.

### CMake-Setup für mehrere Plattformen {#cmake-cross-platform-setup}

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

### Universal Binary (macOS) {#universal-binary-macos}

Ein Binary, das sowohl `arm64` als auch `x86_64` enthält. Alle Abhängigkeiten müssen ebenfalls universal sein.

```bash
# Combine separate arch builds:
lipo -create arm64/libfoo.dylib x86_64/libfoo.dylib -output libfoo.dylib
```

**Entfernung von Rosetta 2**: Apple hat die Entfernung in macOS 28 (2027) angekündigt. Ein natives `arm64`-Build ist verpflichtend, nicht optional.

### Suchreihenfolge für DLL/dylib {#dlldylib-search-order}

**DLL-Suche unter Windows** (vereinfacht):
1. EXE-Verzeichnis
2. System32
3. Aktuelles Arbeitsverzeichnis (**gefährlich** – DLL-Hijacking)
4. PATH-Einträge

Abhilfe: `SetDllDirectory("")` entfernt das aktuelle Verzeichnis aus der Suche.

**macOS-dylib** verwendet `@rpath`:

```cmake
set_target_properties(target PROPERTIES
    INSTALL_RPATH "@executable_path/../Frameworks"
)
```

## Unicode-Behandlung {#unicode-handling}

**Wesentlicher Unterschied**: Die Windows-API arbeitet mit UTF-16, macOS/POSIX mit UTF-8.

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

Boost.Nowide verwenden, um UTF-8 unter Windows transparent zu behandeln (`std::fstream`, `std::cout`).

## Sicherheit / Speicherung von Zugangsdaten {#security-credential-storage}

| Plattform | API | Hinweise |
|-----------|-----|----------|
| Windows | DPAPI + Credential Manager (`CredWrite`/`CredRead`) | Jede App desselben Benutzers kann lesen – keine ACL pro Eintrag |
| macOS | Keychain (`SecItemAdd`/`SecItemCopyMatching`) | ACL pro Eintrag, fragt bei Zugriff durch fremde Apps nach |

Plattformübergreifender Wrapper: Die C++-Bibliothek `keychain` (GitHub: hrantzsch/keychain) abstrahiert beide.

**Für Lizenzschlüssel**: über die plattformeigene Credential-API speichern und die Daten zusätzlich verschlüsseln (Defense in Depth).

## Installation / Distribution {#installation-distribution}

### Installer-Formate {#installer-formats}

**Windows:**

| Format | Anwendungsfall |
|--------|----------------|
| WiX (MSI) | Unternehmens-/GPO-Deployment – IT bevorzugt MSI |
| NSIS / Inno Setup | Einfacherer EXE-Installer, weit verbreitet |
| MSIX | Moderne Sandbox, Auto-Update, erfordert Zertifikat |

**macOS:**
- DMG mit Drag-to-Applications entspricht der Erwartung der Nutzer
- `.pkg` im DMG, falls Dateien auf Systemebene platziert werden müssen

### Auto-Update {#auto-update}

| Komponente | Windows | macOS |
|------------|---------|-------|
| Framework | WinSparkle | Sparkle |
| Format | Appcast XML | Appcast XML |
| Signaturprüfung | Authenticode | Apple codesign |
| Neustart | Benötigt Hilfsprozess (obligatorische Sperrung) | Kann in place aktualisieren |

### Crash-Reporting: Crashpad + Sentry {#crash-reporting-crashpad-sentry}

Crashpad (Google, Open Source) übernimmt die Absturzerfassung auf beiden Plattformen. Sentry akzeptiert Minidump + PDB/dSYM zur Symbolisierung:

```bash
# CI: upload debug symbols
sentry-cli debug-files upload --include-sources ./build/Release/*.pdb    # Windows
sentry-cli debug-files upload --include-sources ./build/Release/*.dSYM   # macOS
```

## Testmatrix {#testing-matrix}

### Mindestmatrix {#minimum-matrix}

| Betriebssystem | Architektur | GPU | Priorität |
|----------------|-------------|-----|-----------|
| Windows 10 22H2 | x64 | NVIDIA (CUDA + DirectML) | P0 |
| Windows 10 22H2 | x64 | AMD (nur DirectML) | P0 |
| Windows 10 22H2 | x64 | Intel iGPU (DirectML) | P1 |
| Windows 11 24H2 | x64 | NVIDIA | P1 |
| macOS 14 Sonoma | arm64 (M1–M3) | Apple GPU (CoreML) | P0 |
| macOS 15 Sequoia | arm64 (M1–M4) | Apple GPU | P1 |
| macOS 14 Sonoma | x86_64 Intel | AMD/Intel GPU | P2 |

### Plattformspezifische kritische Testfälle {#platform-specific-critical-test-cases}

| Test | Windows | macOS |
|------|---------|-------|
| Erster Start | SmartScreen-Warnung | Gatekeeper + Prüfung des Quarantäne-xattr |
| GPU-Inferenz | DirectML-Fallback, wenn kein CUDA | CoreML + Neural Engine vs. CPU |
| VRAM-OOM | DirectML-OOM → CPU-Fallback | Unified Memory – kein OOM, aber Swapping |
| Installer | Lange Pfade (kyrillischer Benutzername = Grenzfall) | DMG per Drag-to-Apps; Prüfung der Notarisierung |
| Update | Hilfsprozess für den Dateiaustausch | Austausch der Datei in place möglich |
| Unternehmensproxy | SSL-Inspection über den Windows-Zertifikatspeicher | SSL-Inspection über den System-Schlüsselbund |
| Ruhezustand/Aufwachen | GPU-Gerät nach dem Aufwachen verloren | Metal-Gerät bleibt erhalten |

## Zusammenfassung: Plattform-Kurzreferenz {#summary-platform-quick-reference}

| Komponente | Windows | macOS Intel | macOS Apple Silicon |
|------------|---------|-------------|---------------------|
| GPU-Inferenz | CUDA oder DirectML | Nur CPU | CoreML + Neural Engine |
| Code-Signierung | Authenticode | Developer ID + Notarisierung | Developer ID + Notarisierung |
| Dateisperren | Obligatorisch | Advisory | Advisory |
| Unicode | UTF-16 an der API-Grenze | UTF-8 durchgehend | UTF-8 durchgehend |
| Installer | MSI / NSIS / MSIX | DMG + pkg | DMG (Universal Binary) |
| Crash-Symbole | PDB + WER/Crashpad | dSYM + Crashpad | dSYM + Crashpad |
| Auto-Update | WinSparkle | Sparkle | Sparkle |
| Speicherung von Zugangsdaten | DPAPI / Credential Manager | Keychain | Keychain + Secure Enclave |
| C++-Stdlib | MSVC STL | libc++ | libc++ |
| ARM nativ | Minimal (Win ARM ist eine Nische) | N/A | **Erforderlich** (Rosetta entfällt 2027) |

## Stolperfallen {#gotchas}

- **Obligatorische Sperrung blockiert Auto-Update unter Windows**: DLL- und Modelldateien können im geladenen Zustand nicht ersetzt werden. Muster: in eine temporäre Datei `*.new` schreiben, beim nächsten Start über einen Hilfsprozess umbenennen. Unterbleibt dies, kommt es beim Update zu „file is in use“-Fehlern.
- **Entfernung von Rosetta 2 im Jahr 2027 (macOS)**: Ein natives `arm64`-Build auf Apple Silicon ist verpflichtend. Apps, die nur x86_64 über Rosetta ausliefern, funktionieren nicht mehr. Das Universal Binary (`x86_64;arm64`) ist die sichere Standardwahl.
- **Unterschiedliche `wchar_t`-Größe**: 2 Byte unter Windows (UTF-16), 4 Byte unter macOS (UTF-32). `std::wstring` niemals in Dateien oder IPC-Kanäle serialisieren, die plattformübergreifend genutzt werden. Interne Strings in `std::string` (UTF-8) halten und an API-Grenzen konvertieren.
- **Verzögerung des SmartScreen-Reputationsaufbaus unter Windows**: Selbst ein korrekt signiertes Binary eines neuen Herausgebers zeigt „Windows hat Ihren PC geschützt“ für Wochen oder Monate, bis die Download-Anzahl Reputation aufgebaut hat. EV-Zertifikate gewährten früher sofortige Reputation; seit August 2024 hat Microsoft OV und EV gleichgestellt.
- **macOS ohne Notarisierung = nicht startbar**: `xcrun notarytool` und `xcrun stapler` sind für macOS 10.15+ verpflichtende Schritte in der Release-Pipeline. Nicht gestapelte Apps schlagen auch auf Rechnern ohne Internetzugang fehl, da Gatekeeper nicht online prüfen kann.
- **`Sleep(1)` unter Windows = ca. 15,6 ms**: Die Timer-Auflösung von Windows beträgt standardmäßig 15,6 ms. `timeBeginPeriod(1)` aufrufen, um ca. 1 ms Auflösung zu erhalten – dies erhöht jedoch den systemweiten Stromverbrauch. `std::this_thread::sleep_for` verwenden, das auf QPC aufsetzt und dieselbe Auflösung erbt.
- **Fehler beim Dezimaltrennzeichen (Locale)**: `atof("1.5")` liefert 1, wenn die Systemlocale das Komma als Dezimaltrennzeichen verwendet. Vor jedem numerischen Parsen immer `setlocale(LC_NUMERIC, "C")` oder `std::locale::global(std::locale::classic())` setzen.
- **CEP-Erweiterungen in PS 2025 entfernt**: Photoshop 2025 (v26) zeigt veraltete CEP-Erweiterungen nicht mehr in der Oberfläche an. Apple Silicon hat CEP nie unterstützt, da es Rosetta erfordert. Neue Plugins müssen UXP oder UXP Hybrid verwenden.

## Siehe auch {#see-also}

- [[cross-platform-ml-inference]] – Auswahl des ONNX-Runtime-Execution-Providers (DirectML, CoreML, CUDA)
- [[photoshop-plugin-architecture]] – UXP-Hybrid-Plugin, C++ .uxpaddon, Lightroom SDK
