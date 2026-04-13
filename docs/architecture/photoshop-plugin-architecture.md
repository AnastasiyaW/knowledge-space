# Photoshop Plugin Architecture for ML Inference

Date: 2026-04-03
Context: Building cross-platform (Mac + Windows) C++ ML inference plugin for Photoshop and other photo editors. Covers plugin types, ONNX Runtime integration, IPC patterns, and 10 editors compared.

---

## Photoshop Plugin Types

### UXP Hybrid - PRIMARY CHOICE FOR ML

Available from PS v24.2.0 (Feb 2023), significantly enhanced in PS 2025 (v26, UXP v8.0).

**Architecture:**
- UXP (JavaScript/HTML for UI) + C++ native code in `.uxpaddon` file (renamed .dll/.dylib)
- Communication via Node.js N-API style API
- From PS 2025: **access to Photoshop C++ SDK from hybrid plugins** - filters, direct pixel data access

```
JavaScript (UXP) <--N-API--> C++ (.uxpaddon)
                                  |
                                  +-- ONNX Runtime
                                  +-- ML inference
                                  +-- Image processing
```

**Capabilities:**
- Arbitrary C++ code (ONNX Runtime, custom ML, etc.)
- JavaScript/HTML/CSS UI via UXP
- From PS 2025: PS C++ SDK access for filter creation + pixel data via C++ SDK
- Publish as single package via Adobe Marketplace

**Constraints:**
- Must support ALL platforms: Mac M1 (arm64), Mac Intel (x86_64), Windows x64
- Windows ARM not supported
- macOS: code signing + notarization required
- No Web Workers / POSIX threads inside UXP (C++ can create its own threads)
- Minimum: PS v24.2.0, UDT v1.7.0

### UXP (JS-only)

Basic platform. No native C++ code. ML inference only via subprocess or HTTP. Use only for simple UI plugins without heavy computation.

### CEP - DEPRECATED

CEP 12 = last major update. In PS 2025 (v26), legacy CEP extensions **no longer appear in UI**. On Apple Silicon without Rosetta: doesn't work. Do not use for new projects.

### C++ Filter Plugins (.8bf) - Legacy, Still Supported

- Files: `.8bf` (filters), `.8ba` (import), `.8be` (export), `.8bi` (file formats)
- Works in-process, direct pixel data access
- Requires PiPL resource
- For Apple Silicon: recompile as Universal Binary
- **Bonus:** Affinity Photo also supports 64-bit .8bf
- No modern UI framework (Win32/Cocoa only)

### Plugin Type Comparison

| Criterion | UXP Hybrid | UXP | .8bf Legacy | CEP |
|-----------|-----------|-----|-------------|-----|
| Status | Active | Active | Maintained | Deprecated |
| UI | HTML/CSS/JS | HTML/CSS/JS | Win32/Cocoa | HTML/CSS/JS |
| Native C++ | Yes (N-API) | No | Yes (full) | No |
| ML inference | Direct C++ call | Subprocess/HTTP | Direct | Subprocess |
| Marketplace | Yes | Yes | No | No (deprecated) |
| Apple Silicon | Native (Universal) | Native | Recompile needed | Rosetta only |
| Future | Long-term | Long-term | Unclear | Will be removed |

---

## Version Compatibility

| Feature | Min PS Version |
|---------|----------------|
| UXP basic | CC 2021 (v22.0) |
| **UXP Hybrid plugins** | **v24.2.0 (Feb 2023)** |
| UXP v8.0 features | PS 2025 (v26.0) |
| PS C++ SDK from Hybrid | PS 2025 (v26.0) |
| WebView in UXP | PS 2025 (v26.0) |
| CEP hidden from UI | PS 2025 (v26.0) |

```javascript
// Version detection from plugin
const app = require('photoshop').app;
const psVersion = app.version; // "26.0.0"
const platform = require('os').platform(); // "darwin" or "win32"
```

**Multi-version strategy:**
```json
// manifest.json
{"host": {"app": "PS", "minVersion": "24.2.0"}}
```
Feature-detect PS C++ SDK; fall back to JS imaging API if unavailable.

---

## Native Code Communication Options

### N-API (Hybrid Plugin) - Recommended

```
JS (UXP) <--N-API--> C++ (.uxpaddon)
```

Direct C++ function calls from JS. Pass ArrayBuffer/TypedArrays for pixel data. Sync and async calls. C++ can spawn its own threads for heavy computation.

```cpp
// Thread-safe callback from worker thread back to JS
napi_call_threadsafe_function(tsfn, data, napi_tsfn_blocking);
```

### WebAssembly

Compiled C/C++/Rust runs in UXP. No separate compilation per platform.
Performance: ~45-55% slower than native (USENIX research). No GPU access. PS 2025 has WASM crash bugs.

### Subprocess (Out-of-Process Daemon)

```
JS (UXP) <--HTTP/WebSocket--> External Process (C++)
```

Full isolation, own address space, full GPU access. Pattern used by all major ML plugins (Topaz, Stable Diffusion plugins). IPC overhead for large image transfers.

---

## Process Architecture Patterns

### Pattern A: In-Process (UXP Hybrid)

```
[Photoshop Process]
  |
  +-- [UXP JS] <--N-API--> [C++ .uxpaddon]
                                  |
                                  +-- ONNX Runtime (CPU)
                                  +-- Image processing
```

Pros: minimum latency, shared address space, single package.
Cons: C++ crash = PS crash. Memory limited to PS process. GPU may conflict with PS usage.

### Pattern B: Out-of-Process Daemon

```
[Photoshop Process]               [ML Daemon Process]
  |                                     |
  +-- [UXP Plugin] <--localhost HTTP--> [HTTP Server]
                                             |
                                             +-- ONNX Runtime + GPU
                                             +-- Models in memory
```

Pros: full crash isolation, own address space, full GPU control, sharable between PS + LR + standalone.
Cons: IPC overhead, lifecycle management, firewall may block localhost.

### Pattern C: Hybrid - RECOMMENDED FOR ML

```
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

N-API for pixel transfer + subprocess for GPU inference.

### Real-World Pattern (Topaz, Nik, Luminar)

```
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

All major commercial ML plugins use this: standalone app + PS/LR integration.

---

## IPC Mechanisms

| Method | Latency | Throughput | Complexity | GPU Access |
|--------|---------|------------|-----------|------------|
| N-API (hybrid) | Low | High | Medium | Via C++ |
| WASM | Low | Medium | Low | None |
| localhost HTTP | Medium | Medium | Medium | Full |
| Named Pipes | Low | High | High | Full |
| Shared Memory | Minimal | Maximum | High | Full |
| gRPC | Medium | High | Medium | Full |

**Recommendations:**
- Light models (<100MB, CPU): N-API hybrid - minimum latency
- Heavy models (GPU): subprocess daemon + localhost HTTP/WebSocket - isolation + full GPU
- 4K/8K images: shared memory (zero-copy) + mmap

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

## ONNX Runtime Integration

### Execution Providers

| Provider | Platform | GPU | Notes |
|----------|---------|-----|-------|
| **DirectML** | Windows | All (AMD/Intel/NVIDIA/Qualcomm) | DX12, broadest compatibility |
| **CoreML** | macOS/iOS | Apple Neural Engine + GPU | Uses ANE on M-chips |
| **CUDA** | Win/Linux | NVIDIA only | Max NVIDIA performance |
| **CPU** | All | - | Always available fallback |
| **TensorRT** | Win/Linux | NVIDIA | Optimized inference |

**Recommended strategy:**
```
Windows: DirectML → CPU fallback
macOS:   CoreML  → CPU fallback
```

DirectML works with ANY DX12 GPU - no CUDA install required.
CoreML uses ANE on M-chips - best performance on Apple hardware.

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

### Memory Management for Large Images

Image buffer sizes (RGBA float32):
- 2K (2048×2048): ~64 MB
- 4K (4096×4096): ~256 MB
- 8K (8192×8192): ~1 GB
- 12K (12000×12000): ~2.2 GB

Strategies:
1. **Tiling:** 512×512 or 1024×1024 tiles with overlap for seamless joins
2. **Memory-mapped files:** mmap for data exceeding RAM
3. **Half-precision (fp16):** half memory for inference
4. **Progressive loading:** load on demand

### Thread Safety

```
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

**Rules:**
- NEVER block Photoshop UI thread
- Use N-API async workers for heavy operations
- C++ in .uxpaddon CAN create its own threads
- Callbacks to JS: only from main thread via `napi_call_threadsafe_function`

---

## Adobe Marketplace

### Publishing Requirements
- Publisher profile in Adobe Developer Console (one-time)
- Adobe review before publication
- **Required: support ALL platforms** (Mac M1, Mac Intel, Windows x64)
- macOS: Apple Developer Certificate + notarization mandatory
- Correct manifest.json with permissions

### Revenue Share
- Before August 2025: 90% developer / 10% Adobe
- From August 1, 2025: 87.4% developer / 12.6% Adobe
- Example: $5.00 plugin → developer receives $4.37

### Direct Distribution (No Marketplace)
Install `.ccx` file via Creative Cloud Desktop or UDT. No Adobe review, no revenue share. Use when: custom licensing system, pricing control, no marketplace discovery needed.

---

## Lightroom Integration

### Lightroom Classic - Lua SDK

**Language:** Lua (embedded interpreter). SDK version: 8.0.

SDK capabilities: export/publish destinations, custom metadata, menu items, UI via LrDialogs/LrView, HTTP via LrHttp, post-processing hooks, Develop settings.

**Limitations vs Photoshop:**

| Capability | LR Classic | PS UXP |
|-----------|-----------|-------|
| Pixel-level editing | No | Yes |
| Native C++ | No (Lua only) | Yes (Hybrid) |
| GPU inference | No | Yes (via C++) |
| External editor | Yes (round-trip) | N/A |

**External Editor Protocol (primary ML path for LR):**
1. LR sends photo to external editor (TIFF/PSD)
2. External app processes (your standalone app with ML backend)
3. File returns to LR catalog

This is how Topaz Photo AI, Nik Collection, Luminar Neo work in LR.

### Shared Codebase PS + LR

```
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

### Lightroom CC (Cloud)

**Does NOT support third-party plugins.** No SDK, no API. Community has been requesting since 2021. As of April 2026 - unchanged. Only integration path: round-trip through Photoshop.

---

## Other Photo Editors

| Editor | Plugin SDK | Native C++ | Recommended Approach | Market |
|--------|-----------|-----------|---------------------|--------|
| **Photoshop** | UXP Hybrid | Yes (N-API) | UXP Hybrid plugin | ~33% (leader) |
| **Lightroom Classic** | Lua SDK | No | External Editor + standalone | Significant |
| **Lightroom CC** | None | - | Not supported | Growing |
| **Capture One** | Limited | No | External Editor | Top-10 |
| **Affinity Photo** | .8bf only | Yes (.8bf) | .8bf filter | Growing |
| **GIMP** | Full (3.0+) | Yes (C plugins) | C plugin | ~10% |
| **DxO PhotoLab** | None | - | External Editor | Niche |
| **Darktable** | Lua | No | Lua + external process | Growing (Linux) |
| **Pixelmator Pro** | Core Image | No (Swift) | Core Image Unit | macOS only |
| **Luminar Neo** | None | - | Not supported | Growing |
| **ON1 Photo RAW** | None | - | Not supported | Niche |

**Key notes:**
- **Affinity Photo** supports 64-bit .8bf - free compatibility if you already build .8bf for PS
- **GIMP 3.0** (2025): major rewrite; old plugins require porting. C plugin + ONNX Runtime works.
- **Capture One** AppleScript API = macOS only. No scripting API on Windows.
- **Pixelmator Pro** macOS only; Core Image Units are Apple framework filters

---

## Development Tooling

**Bolt UXP** (github.com/hyperbrew/bolt-uxp): React/Svelte/Vue + TypeScript + Vite boilerplate. Hot reload.

**UDT (UXP Developer Tool):** Official Adobe debug tool for UXP plugins. Min version 1.7.0 for hybrid plugins.

**Reference implementations:**
- `AdobeDocs/photoshop-cpp-sdk` - official PS C++ SDK
- `tpl-photoshop-plugin` (javier-games) - C++ PS plugin template with Adobe SDK 2024
- `WasmUXP` (michelerenzullo) - WebAssembly in UXP plugins
- Auto-Photoshop-StableDiffusion-Plugin - open-source example: UXP + localhost HTTP to ML backend

---

## Gotchas

- **UXP Hybrid != Photoshop .8bf C++ plugin.** Hybrid uses N-API JS↔C++ bridge. From PS 2025 you can also call PS C++ SDK from inside the hybrid addon, but they are distinct entry points.
- **Partial platform support is rejected by Adobe Marketplace.** You must support Mac M1, Mac Intel, AND Windows x64. Windows ARM is not yet required but expect it in future reviews.
- **CEP extensions no longer appear in PS 2025 UI** even if installed. Users on PS 2025+ won't see them. Any active CEP plugin must migrate to UXP.
- **`CreateSessionFromArray` in ONNX Runtime** loads model from RAM buffer - critical for loading from encrypted .hmod without writing decrypted weights to disk.
- **DirectML doesn't support all ONNX operators.** Test your specific model. Fall back to CPU for unsupported ops or use `OrtSessionOptionsSetExecutionMode` to partition graph.
- **Firewall may block localhost** in restricted corporate environments. Shared memory IPC or named pipes avoid this for out-of-process daemon communication.
- **In-process crash protection:** if C++ addon crashes, it takes Photoshop down. Use out-of-process daemon for heavy inference. N-API is best for fast pixel transfer only.
- **UXP has no Web Workers or POSIX threads.** All threading for heavy work must be in C++ (.uxpaddon) using platform threads, results returned via N-API threadsafe callback.
- **Lightroom CC has zero plugin support.** Don't invest in LR CC integration until Adobe adds SDK support.
- **macOS notarization is required** for any plugin distributed outside Mac App Store. This means Apple-signed Developer ID certificate + submission to Apple notary service + stapling. Without this, Gatekeeper blocks the plugin on modern macOS.
