---
level: 5
source_sha256: a910e6ea66878fce5f65abbaa0ecb60deb510c24d83d9b35d222165768e88473
translation: machine
translated_at: '2026-10-24'
---
# Photoshop-Plugin-Architektur für ML-Inferenz {#photoshop-plugin-architecture-for-ml-inference}

Datum: 2026-04-03
Kontext: Entwicklung eines plattformübergreifenden (Mac + Windows) C++-ML-Inferenz-Plugins für Photoshop und andere Fotobearbeitungsprogramme. Behandelt Plugin-Typen, ONNX-Runtime-Integration, IPC-Muster und einen Vergleich von 10 Editoren.

---

## Photoshop-Plugin-Typen {#photoshop-plugin-types}

### UXP Hybrid - BEVORZUGTE WAHL FÜR ML {#uxp-hybrid-primary-choice-for-ml}

Verfügbar ab PS v24.2.0 (Feb. 2023), deutlich erweitert in PS 2025 (v26, UXP v8.0).

**Architektur:**
- UXP (JavaScript/HTML für die UI) + C++-Nativcode in einer `.uxpaddon`-Datei (umbenannte .dll/.dylib)
- Kommunikation über eine Node.js-N-API-artige Schnittstelle
- Ab PS 2025: **Zugriff auf das Photoshop C++ SDK aus Hybrid-Plugins** - Filter, direkter Pixelzugriff

```php
JavaScript (UXP) <--N-API--> C++ (.uxpaddon)
                                  |
                                  +-- ONNX Runtime
                                  +-- ML inference
                                  +-- Image processing
```

**Fähigkeiten:**
- Beliebiger C++-Code (ONNX Runtime, eigene ML-Implementierungen usw.)
- JavaScript/HTML/CSS-UI über UXP
- Ab PS 2025: Zugriff auf das PS C++ SDK zur Filtererstellung sowie Pixeldaten über das C++ SDK
- Veröffentlichung als einzelnes Paket über den Adobe Marketplace

**Einschränkungen:**
- Muss ALLE Plattformen unterstützen: Mac M1 (arm64), Mac Intel (x86_64), Windows x64
- Windows ARM wird nicht unterstützt
- macOS: Code-Signierung und Notarisierung erforderlich
- Keine Web Workers oder POSIX-Threads innerhalb von UXP (C++ kann eigene Threads erzeugen)
- Mindestversion: PS v24.2.0, UDT v1.7.0

### UXP (nur JS) {#uxp-js-only}

Grundlegende Plattform. Kein nativer C++-Code. ML-Inferenz nur über Subprozess oder HTTP. Nur für einfache UI-Plugins ohne aufwendige Berechnungen verwenden.

### CEP - VERALTET {#cep-deprecated}

CEP 12 ist das letzte größere Update. In PS 2025 (v26) erscheinen ältere CEP-Erweiterungen **nicht mehr in der Oberfläche**. Auf Apple Silicon ohne Rosetta funktioniert CEP nicht. Nicht für neue Projekte verwenden.

### C++-Filter-Plugins (.8bf) - Legacy, weiterhin unterstützt {#c-filter-plugins-8bf-legacy-still-supported}

- Dateien: `.8bf` (Filter), `.8ba` (Import), `.8be` (Export), `.8bi` (Dateiformate)
- Läuft im selben Prozess, direkter Zugriff auf Pixeldaten
- Benötigt eine PiPL-Ressource
- Für Apple Silicon: als Universal Binary neu kompilieren
- **Bonus:** Affinity Photo unterstützt ebenfalls 64-Bit-.8bf
- Kein moderner UI-Framework-Support (nur Win32/Cocoa)

### Vergleich der Plugin-Typen {#plugin-type-comparison}

| Kriterium | UXP Hybrid | UXP | .8bf Legacy | CEP |
|-----------|-----------|-----|-------------|-----|
| Status | Aktiv | Aktiv | Gepflegt | Veraltet |
| UI | HTML/CSS/JS | HTML/CSS/JS | Win32/Cocoa | HTML/CSS/JS |
| Nativer C++-Code | Ja (N-API) | Nein | Ja (vollständig) | Nein |
| ML-Inferenz | Direkter C++-Aufruf | Subprozess/HTTP | Direkt | Subprozess |
| Marketplace | Ja | Ja | Nein | Nein (veraltet) |
| Apple Silicon | Nativ (Universal) | Nativ | Neukompilierung nötig | Nur Rosetta |
| Zukunft | Langfristig | Langfristig | Unklar | Wird entfernt |

---

## Versionskompatibilität {#version-compatibility}

| Funktion | Min. PS-Version |
|----------|-----------------|
| UXP Grundfunktionen | CC 2021 (v22.0) |
| **UXP-Hybrid-Plugins** | **v24.2.0 (Feb. 2023)** |
| UXP-v8.0-Funktionen | PS 2025 (v26.0) |
| PS C++ SDK aus Hybrid | PS 2025 (v26.0) |
| WebView in UXP | PS 2025 (v26.0) |
| CEP in der UI ausgeblendet | PS 2025 (v26.0) |

```javascript
// Version detection from plugin
const app = require('photoshop').app;
const psVersion = app.version; // "26.0.0"
const platform = require('os').platform(); // "darwin" or "win32"
```

**Strategie für mehrere Versionen:**
```json
// manifest.json
{"host": {"app": "PS", "minVersion": "24.2.0"}}
```
Funktionserkennung für das PS C++ SDK durchführen; falls nicht verfügbar, auf die JS-Imaging-API zurückfallen.

---

## Optionen für die Kommunikation mit Nativcode {#native-code-communication-options}

### N-API (Hybrid-Plugin) - Empfohlen {#n-api-hybrid-plugin-recommended}

```php
JS (UXP) <--N-API--> C++ (.uxpaddon)
```

Direkte C++-Funktionsaufrufe aus JS. ArrayBuffer/TypedArrays für Pixeldaten übergeben. Synchrone und asynchrone Aufrufe. C++ kann für rechenintensive Aufgaben eigene Threads starten.

```cpp
// Thread-safe callback from worker thread back to JS
napi_call_threadsafe_function(tsfn, data, napi_tsfn_blocking);
```

### WebAssembly {#webassembly}

Kompiliertes C/C++/Rust läuft in UXP. Keine separate Kompilierung pro Plattform nötig.
Leistung: ca. 45-55 % langsamer als nativ (USENIX-Forschung). Kein GPU-Zugriff. PS 2025 hat WASM-Absturzfehler.

### Subprozess (Out-of-Process-Daemon) {#subprocess-out-of-process-daemon}

```php
JS (UXP) <--HTTP/WebSocket--> External Process (C++)
```

Vollständige Isolation, eigener Adressraum, voller GPU-Zugriff. Muster, das von allen großen ML-Plugins verwendet wird (Topaz, Stable-Diffusion-Plugins). IPC-Overhead bei großen Bildübertragungen.

---

## Prozessarchitektur-Muster {#process-architecture-patterns}

### Muster A: In-Process (UXP Hybrid) {#pattern-a-in-process-uxp-hybrid}

```php
[Photoshop Process]
  |
  +-- [UXP JS] <--N-API--> [C++ .uxpaddon]
                                  |
                                  +-- ONNX Runtime (CPU)
                                  +-- Image processing
```

Vorteile: minimale Latenz, gemeinsamer Adressraum, ein einziges Paket.
Nachteile: Absturz des C++-Codes = Absturz von PS. Speicher auf den PS-Prozess begrenzt. GPU kann mit der GPU-Nutzung von PS in Konflikt geraten.

### Muster B: Out-of-Process-Daemon {#pattern-b-out-of-process-daemon}

```bash
[Photoshop Process]               [ML Daemon Process]
  |                                     |
  +-- [UXP Plugin] <--localhost HTTP--> [HTTP Server]
                                             |
                                             +-- ONNX Runtime + GPU
                                             +-- Models in memory
```

Vorteile: vollständige Absturzisolation, eigener Adressraum, volle GPU-Kontrolle, gemeinsam nutzbar für PS, LR und eigenständige Anwendungen.
Nachteile: IPC-Overhead, Lebenszyklusverwaltung, Firewall kann localhost blockieren.

### Muster C: Hybrid - FÜR ML EMPFOHLEN {#pattern-c-hybrid-recommended-for-ml}

```bash
[Photoshop]
  |
  +-- [UXP Hybrid Plugin]
        |
        +-- [C++ .uxpaddon] -- light ops (resize, color convert, pixel transfer)
        |       |
        |       +-- IPC to daemon
        |
        +-- [ML Daemon] -- heavy GPU inference
                |
                +-- ONNX Runtime + GPU
                +-- Models in memory between calls
```

N-API für die Pixelübertragung + Subprozess für die GPU-Inferenz.

### Praxismuster (Topaz, Nik, Luminar) {#real-world-pattern-topaz-nik-luminar}

```text
[Photoshop/LR Filter Call]
     |
     v
[.8bf / UXP Plugin]
     |
     +-- [Standalone Application]  ← same C++ codebase
          |
          +-- ML inference engine
          |
     [Returns result as new layer]
```

Alle großen kommerziellen ML-Plugins nutzen dieses Muster: eigenständige Anwendung + Integration in PS/LR.

---

## IPC-Mechanismen {#ipc-mechanisms}

| Methode | Latenz | Durchsatz | Komplexität | GPU-Zugriff |
|---------|--------|-----------|-------------|-------------|
| N-API (Hybrid) | Niedrig | Hoch | Mittel | Über C++ |
| WASM | Niedrig | Mittel | Niedrig | Keiner |
| localhost-HTTP | Mittel | Mittel | Mittel | Voll |
| Named Pipes | Niedrig | Hoch | Hoch | Voll |
| Shared Memory | Minimal | Maximal | Hoch | Voll |
| gRPC | Mittel | Hoch | Mittel | Voll |

**Empfehlungen:**
- Leichte Modelle (<100 MB, CPU): N-API-Hybrid - minimale Latenz
- Schwere Modelle (GPU): Subprozess-Daemon + localhost-HTTP/WebSocket - Isolation + volle GPU-Nutzung
- 4K/8K-Bilder: Shared Memory (Zero-Copy) + mmap

```cpp
// IPC method selection by platform
#ifdef _WIN32
    // Named pipe: \\.\pipe\my-ml-plugin
    HANDLE hPipe = CreateNamedPipeW(L"\\\\.\\pipe\\my-ml-plugin", ...);
#else
    // Unix domain socket: /tmp/my-ml-plugin.sock
    int sock = socket(AF_UNIX, SOCK_STREAM, 0);
#endif
```

---

## ONNX-Runtime-Integration {#onnx-runtime-integration}

### Execution Provider {#execution-providers}

| Provider | Plattform | GPU | Hinweise |
|----------|-----------|-----|----------|
| **DirectML** | Windows | Alle (AMD/Intel/NVIDIA/Qualcomm) | DX12, breiteste Kompatibilität |
| **CoreML** | macOS/iOS | Apple Neural Engine + GPU | Nutzt die ANE auf M-Chips |
| **CUDA** | Win/Linux | Nur NVIDIA | Maximale NVIDIA-Leistung |
| **CPU** | Alle | - | Immer verfügbarer Fallback |
| **TensorRT** | Win/Linux | NVIDIA | Optimierte Inferenz |

**Empfohlene Strategie:**
```yaml
Windows: DirectML → CPU fallback
macOS:   CoreML  → CPU fallback
```

DirectML funktioniert mit JEDER DX12-GPU - keine CUDA-Installation erforderlich.
CoreML nutzt die ANE auf M-Chips - beste Leistung auf Apple-Hardware.

```cpp
#include <onnxruntime_cxx_api.h>

Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "MLPlugin");
Ort::SessionOptions session_options;

#ifdef _WIN32
    OrtSessionOptionsAppendExecutionProvider_DML(session_options, 0);
#elif __APPLE__
    OrtSessionOptionsAppendExecutionProvider_CoreML(session_options, 0);
#endif
// CPU fallback is automatic

// Load from memory buffer (no plaintext model on disk)
Ort::Session session(env,
    model_bytes.data(), model_bytes.size(),  // in-memory load
    session_options);
```

### Speicherverwaltung für große Bilder {#memory-management-for-large-images}

Puffergrößen für Bilder (RGBA float32):
- 2K (2048×2048): ca. 64 MB
- 4K (4096×4096): ca. 256 MB
- 8K (8192×8192): ca. 1 GB
- 12K (12000×12000): ca. 2,2 GB

Strategien:
1. **Kachelung:** 512×512- oder 1024×1024-Kacheln mit Überlappung für nahtlose Übergänge
2. **Speicherabbildungsdateien:** mmap für Daten, die den RAM übersteigen
3. **Halbe Genauigkeit (fp16):** halber Speicherbedarf für die Inferenz
4. **Progressives Laden:** Laden bei Bedarf

### Thread-Sicherheit {#thread-safety}

```sql
JS: call startInference(imageData, callback)
 |
 +-> C++ (N-API): receive data, create worker thread
       |
       +-> Worker thread: ML inference (1-30 seconds)
             |
             +-> threadsafe callback: return result to JS
                   |
                   +-> JS: update UI, write result to PS
```

**Regeln:**
- Den UI-Thread von Photoshop NIEMALS blockieren
- N-API-Async-Worker für aufwendige Operationen verwenden
- C++ in .uxpaddon KANN eigene Threads erzeugen
- Rückrufe an JS: nur aus dem Hauptthread über `napi_call_threadsafe_function`

---

## Adobe Marketplace {#adobe-marketplace}

### Veröffentlichungsvoraussetzungen {#publishing-requirements}
- Herausgeberprofil in der Adobe Developer Console (einmalig)
- Prüfung durch Adobe vor der Veröffentlichung
- **Pflicht: Unterstützung ALLER Plattformen** (Mac M1, Mac Intel, Windows x64)
- macOS: Apple-Developer-Zertifikat und Notarisierung zwingend erforderlich
- Korrekte manifest.json mit Berechtigungen

### Umsatzbeteiligung {#revenue-share}
- Vor August 2025: 90 % Entwickler / 10 % Adobe
- Ab 1. August 2025: 87,4 % Entwickler / 12,6 % Adobe
- Beispiel: Plugin für 5,00 $ → Entwickler erhält 4,37 $

### Direktvertrieb (ohne Marketplace) {#direct-distribution-no-marketplace}
Installation über die `.ccx`-Datei mit Creative Cloud Desktop oder UDT. Keine Prüfung durch Adobe, keine Umsatzbeteiligung. Geeignet, wenn ein eigenes Lizenzsystem, Preiskontrolle oder keine Marketplace-Auffindbarkeit benötigt wird.

---

## Lightroom-Integration {#lightroom-integration}

### Lightroom Classic - Lua SDK {#lightroom-classic-lua-sdk}

**Sprache:** Lua (eingebetteter Interpreter). SDK-Version: 8.0.

SDK-Funktionen: Export-/Veröffentlichungsziele, benutzerdefinierte Metadaten, Menüeinträge, UI über LrDialogs/LrView, HTTP über LrHttp, Nachbearbeitungs-Hooks, Develop-Einstellungen.

**Einschränkungen gegenüber Photoshop:**

| Fähigkeit | LR Classic | PS UXP |
|-----------|-----------|-------|
| Pixelbasierte Bearbeitung | Nein | Ja |
| Nativer C++-Code | Nein (nur Lua) | Ja (Hybrid) |
| GPU-Inferenz | Nein | Ja (über C++) |
| Externer Editor | Ja (Round-Trip) | N/A |

**Protokoll für externe Editoren (primärer ML-Weg für LR):**
1. LR sendet das Foto an einen externen Editor (TIFF/PSD)
2. Die externe App verarbeitet es (eigenständige Anwendung mit ML-Backend)
3. Die Datei kehrt in den LR-Katalog zurück

So funktionieren Topaz Photo AI, Nik Collection und Luminar Neo in LR.

### Gemeinsame Codebasis für PS + LR {#shared-codebase-ps-lr}

```bash
C++ backend ──── common (core ML inference)
                      |
           ┌──────────┴──────────┐
    PS frontend              LR frontend
    (UXP Hybrid Plugin)      (Lua plugin → calls standalone)
    (.uxpaddon calls backend)  (External Editor protocol)
                      |
              Standalone App
              (same C++ backend + own GUI via Qt/Dear ImGui)
```

### Lightroom CC (Cloud) {#lightroom-cc-cloud}

**Unterstützt KEINE Plugins von Drittanbietern.** Kein SDK, keine API. Die Community fordert dies seit 2021. Stand April 2026 - unverändert. Einziger Integrationsweg: Round-Trip über Photoshop.

---

## Andere Fotobearbeitungsprogramme {#other-photo-editors}

| Editor | Plugin-SDK | Nativer C++-Code | Empfohlener Ansatz | Marktanteil |
|--------|-----------|------------------|--------------------|-------------|
| **Photoshop** | UXP Hybrid | Ja (N-API) | UXP-Hybrid-Plugin | ca. 33 % (Marktführer) |
| **Lightroom Classic** | Lua SDK | Nein | Externer Editor + eigenständige Anwendung | Erheblich |
| **Lightroom CC** | Keines | - | Nicht unterstützt | Wachsend |
| **Capture One** | Eingeschränkt | Nein | Externer Editor | Top 10 |
| **Affinity Photo** | Nur .8bf | Ja (.8bf) | .8bf-Filter | Wachsend |
| **GIMP** | Vollständig (3.0+) | Ja (C-Plugins) | C-Plugin | ca. 10 % |
| **DxO PhotoLab** | Keines | - | Externer Editor | Nische |
| **Darktable** | Lua | Nein | Lua + externer Prozess | Wachsend (Linux) |
| **Pixelmator Pro** | Core Image | Nein (Swift) | Core Image Unit | Nur macOS |
| **Luminar Neo** | Keines | - | Nicht unterstützt | Wachsend |
| **ON1 Photo RAW** | Keines | - | Nicht unterstützt | Nische |

**Wichtige Hinweise:**
- **Affinity Photo** unterstützt 64-Bit-.8bf - kostenlose Kompatibilität, wenn bereits .8bf für PS gebaut wird
- **GIMP 3.0** (2025): grundlegende Überarbeitung; alte Plugins müssen portiert werden. C-Plugin + ONNX Runtime funktioniert.
- **Capture One**: AppleScript-API nur unter macOS. Unter Windows keine Scripting-API.
- **Pixelmator Pro** nur für macOS; Core-Image-Units sind Apple-Framework-Filter

---

## Entwicklungswerkzeuge {#development-tooling}

**Bolt UXP** (github.com/hyperbrew/bolt-uxp): Boilerplate für React/Svelte/Vue + TypeScript + Vite. Hot Reload.

**UDT (UXP Developer Tool):** Offizielles Debug-Werkzeug von Adobe für UXP-Plugins. Mindestversion 1.7.0 für Hybrid-Plugins.

**Referenzimplementierungen:**
- `AdobeDocs/photoshop-cpp-sdk` - offizielles PS C++ SDK
- `tpl-photoshop-plugin` (javier-games) - C++-PS-Plugin-Vorlage mit Adobe SDK 2024
- `WasmUXP` (michelerenzullo) - WebAssembly in UXP-Plugins
- Auto-Photoshop-StableDiffusion-Plugin - Open-Source-Beispiel: UXP + localhost-HTTP zum ML-Backend

---

## Stolperfallen {#gotchas}

- **UXP Hybrid ist nicht dasselbe wie ein C++-Plugin im Format Photoshop .8bf.** Hybrid nutzt die N-API-Brücke zwischen JS und C++. Ab PS 2025 kann das Hybrid-Addon zusätzlich das PS C++ SDK aufrufen, beide sind aber unterschiedliche Einstiegspunkte.
- **Eine unvollständige Plattformunterstützung wird vom Adobe Marketplace abgelehnt.** Mac M1, Mac Intel UND Windows x64 müssen unterstützt werden. Windows ARM ist noch nicht verpflichtend, dürfte aber in künftigen Prüfungen gefordert werden.
- **CEP-Erweiterungen erscheinen in der PS-2025-Oberfläche nicht mehr**, selbst wenn sie installiert sind. Nutzer ab PS 2025 sehen sie nicht. Jedes aktive CEP-Plugin muss auf UXP migriert werden.
- **`CreateSessionFromArray` in ONNX Runtime** lädt das Modell aus einem RAM-Puffer - entscheidend, um verschlüsselte .hmod-Dateien zu laden, ohne entschlüsselte Gewichte auf die Festplatte zu schreiben.
- **DirectML unterstützt nicht alle ONNX-Operatoren.** Das konkrete Modell testen. Für nicht unterstützte Operatoren auf die CPU zurückfallen oder `OrtSessionOptionsSetExecutionMode` verwenden, um den Graphen zu partitionieren.
- **Firewalls können localhost in restriktiven Unternehmensumgebungen blockieren.** Shared Memory oder Named Pipes umgehen dies für die Kommunikation mit einem Out-of-Process-Daemon.
- **Schutz vor In-Process-Abstürzen:** Stürzt das C++-Addon ab, reißt es Photoshop mit. Für aufwendige Inferenz einen Out-of-Process-Daemon verwenden. N-API eignet sich am besten nur für schnelle Pixelübertragung.
- **UXP hat keine Web Workers und keine POSIX-Threads.** Die gesamte Threadverarbeitung für aufwendige Aufgaben muss in C++ (.uxpaddon) mit plattformeigenen Threads erfolgen; Ergebnisse werden über den N-API-Threadsafe-Callback zurückgegeben.
- **Lightroom CC bietet keinerlei Plugin-Unterstützung.** Keine Investitionen in die LR-CC-Integration, bis Adobe ein SDK bereitstellt.
- **Die macOS-Notarisierung ist für jedes außerhalb des Mac App Store verteilte Plugin erforderlich.** Dazu gehören ein von Apple signiertes Developer-ID-Zertifikat, die Einreichung beim Apple-Notary-Service und das Stapling. Ohne dies blockiert Gatekeeper das Plugin auf aktuellen macOS-Versionen.
