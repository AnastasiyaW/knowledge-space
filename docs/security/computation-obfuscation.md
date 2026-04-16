# Computation Obfuscation: Split Inference and Converter Architectures

Date: 2026-04-03
Context: Desktop ML inference product. Protecting model IP by making the raw weights insufficient for piracy - output requires a separate transformation to be usable.

---

## Core Problem

Encrypting weights prevents extraction, but once decrypted for inference the model runs in the attacker's process. Computation obfuscation approaches make the output of the model itself unusable without a second component the attacker does not control.

---

## Variant A: Local Converter Service

The model's final layer outputs a non-RGB encoded tensor (scrambled channels, affine transform, XOR'd with a key). A separate signed process converts it to a usable image.

**Architecture:**
```
ONNX model -> encoded_tensor (not RGB) -> Converter.exe -> JPEG/PNG
```

**Converter binary characteristics:**
- Separate process, separate signature (Authenticode on Windows, notarized on macOS)
- Contains the decoding transform, obfuscated (LLVM passes, string encryption)
- Validates license server periodically; stops converting on failure
- Checks own integrity and detects debuggers

**Obfuscation stack (C++):**
```
LLVM passes:
  - Control Flow Flattening (CFF): state machine replaces conditional branches
  - Bogus Control Flow: dead code inserted with opaque predicates
  - String Encryption: all plaintext constants encrypted, decrypted at runtime
  
Binary protection (post-compile):
  - VMProtect / Themida: wraps critical functions in VM bytecode
  - Custom packer: compresses + encrypts PE/Mach-O sections
  - Anti-debug: TLS callbacks fire before main(), detect and exit
```

**Effectiveness: 5/10.** Once an attacker reverse-engineers the transform from one binary version, all previous and current copies are broken. The transform is fixed per model version. Delays casual piracy by weeks to months; motivated attackers with reverse engineering skills will extract it.

**Model versioning creates natural re-protection:**
- Each model update changes output format → forces new converter
- Old converter stops working with new model binary
- Cracked version becomes stale after update cycle (2-4 weeks)

---

## Variant B: Split Inference (Server-Side Layers)

Critical layers run on a remote server. Client cannot complete inference without server participation.

**Split strategies:**

| Strategy | Local | Server | Intermediate tensor size | Latency overhead |
|----------|-------|--------|--------------------------|------------------|
| Early split | encoder only | main processing | Large (uncompressed feature map) | 200-500ms |
| Late split | 95% of layers | 1-2 finalization layers | Small (bottleneck) | 50-150ms |
| Middle split | pre + post | bottleneck layer | Minimal | 50-100ms |

**Late split is preferred** for desktop products: most computation stays local (leveraging user GPU), minimal data transmitted, server handles only finalization.

```
Client GPU: layers 0..N-2 -> intermediate_tensor [B, C, H/8, W/8]
HTTP POST /finalize:
  body: {tensor: base64(gzip(intermediate_tensor)), license_token: ...}
  response: {output_tensor: ...}
Client: postprocess + decode output
```

**Strengths:**
- Server-side layers are physically absent from the client - not "bypassable", literally missing
- Server can be updated independently of client distribution
- Server-side usage logging enables anomaly detection

**Weaknesses:**
- **Requires internet.** Photographers in field, offline workflows, China/Russia/corporate proxy: all blocked.
- Latency: 50-200ms per inference is perceptible for interactive tools.
- Infrastructure cost: server-side GPU inference.
- Single point of failure.

**Effectiveness: 8/10 protection, 4/10 UX** for a desktop-first "works on weak GPU" product.

---

## Variant C: Hybrid - "Server Enhancement" Model

Full model runs locally at standard quality. 1-2 enhancement layers on server produce premium quality. Free tier = local only. Paid tier = local + server enhancement.

```
Local inference -> "good" output (usable, watermarked)
         +
Server enhancement request (paid, requires active license)
         -> "premium" output (higher PSNR, finer detail, no visible watermark)
```

**Freemium via quality delta:**
- Pirates use the local version - receive "good" output with visible watermark
- Paying users get server-enhanced output - measurably better, no overlay
- Server endpoint is not accessible without valid license token
- Pirated copies cannot access the premium endpoint even if they crack local binary

**Quality delta requirement:** if the difference between local and server-enhanced is not visible in professional output, there is no purchase incentive. Target: 2-3 dB PSNR improvement, or a visible detail difference at 100% zoom on print-size images.

**Effectiveness: 7/10.** Doesn't block piracy entirely but makes paying the rational choice. Offline always works. Server failure degrades to "good" rather than total failure.

---

## Recommendation Matrix

| Scenario | Recommended variant |
|----------|---------------------|
| Desktop-first, offline required, low server cost tolerance | A (converter) + C (freemium quality) |
| Cloud-first or API product, latency acceptable | B (split inference) |
| SaaS with premium tier | C (hybrid enhancement) |
| Maximum IP protection regardless of UX | B (split inference) |

**Practical combination for desktop product:** Variant A as a cheap first layer (delays 80% of casual pirates), Variant C to monetize the remaining users who pirate but would pay for quality.

---

## Binary Hardening Reference

### LLVM Obfuscation (Ollvm / Hikari / O-MVLL)

```cmake
# CMake: add obfuscation passes via Clang plugin
target_compile_options(converter PRIVATE
  -mllvm -fla          # Control Flow Flattening
  -mllvm -bcf          # Bogus Control Flow
  -mllvm -sub          # Instruction Substitution
  -mllvm -sobf         # String Obfuscation
)
```

**O-MVLL** (commercial, supports Android NDK, iOS, macOS, Windows):
- VM-based protection: wraps hot functions in interpreted bytecode
- Trampolines defeat symbol resolution
- Constant obfuscation: constants split and reconstructed at runtime

### Anti-Debug in TLS Callback (Windows)

```cpp
// Fires before main() - attacker cannot skip
void NTAPI tls_callback(PVOID, DWORD reason, PVOID) {
    if (reason == DLL_PROCESS_ATTACH) {
        if (IsDebuggerPresent()) ExitProcess(0);
        BOOL remote = FALSE;
        CheckRemoteDebuggerPresent(GetCurrentProcess(), &remote);
        if (remote) ExitProcess(0);
    }
}
#pragma comment(linker, "/INCLUDE:_tls_used")
#pragma data_seg(".CRT$XLB")
PIMAGE_TLS_CALLBACK p_tls_callback = tls_callback;
#pragma data_seg()
```

---

## Gotchas

- **Converter cracking is one-time amortized.** Once a cracker reverse-engineers the output transform from version 2.1.3, that transform is public. Unlike encryption (per-user key), the converter transform is shared across all copies. The only defense is model updates that change the format.
- **VMProtect/Themida add startup latency.** VM-protected initialization can add 0.5-3 seconds at first launch. Users notice and report it. Profile and protect only the minimum: the license check and key extraction, not the entire binary.
- **Offline mandatory for professional photo tools.** Variant B (split inference) fundamentally contradicts offline use. If your target user is a wedding photographer on location with no cell signal, Variant B is a non-starter regardless of protection strength.
- **Split inference endpoint can be replayed.** If the intermediate tensor is not bound to a session token or nonce, an attacker can capture it and replay it against the server. Bind each inference request to a signed session token with expiry.
- **Antivirus false positives from heavy obfuscation.** Control flow flattening + string encryption + packer triggers heuristic detections in Windows Defender, Kaspersky, BitDefender. Submit to antivirus vendors before shipping, or use code signing with Extended Validation cert to reduce FP rate.

## See Also
- [[output-scrambling-antipiracy]]
- [[remote-kill-switch]]
- [[watermarking-encrypted-models]]
- [[model-weight-encryption]]
- [[licensing-implementation-cpp]]
