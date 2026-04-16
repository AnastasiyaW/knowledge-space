# ONNX Model Protection: Encrypted Loading and Architecture Obfuscation

Date: 2026-04-03
Context: Desktop C++ app (Mac + Windows), ONNX Runtime inference, protection of model weights from extraction.

---

## Encrypted Loading via CreateSessionFromArray

Microsoft officially does not plan built-in encryption support in ONNX Runtime (Issue #3556). Encryption is the developer's responsibility; ONNX Runtime provides the memory-load API.

```cpp
#include <onnxruntime_cxx_api.h>

std::vector<uint8_t> encrypted_data = read_file("model.onnx.enc");
std::vector<uint8_t> decrypted = decrypt_aes256_gcm(encrypted_data, key);

Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "app");
Ort::SessionOptions opts;
Ort::Session session(env, decrypted.data(), decrypted.size(), opts);

// Zero buffer immediately after session creation
sodium_memzero(decrypted.data(), decrypted.size());
```

```python
import onnxruntime as ort

with open("model.onnx.enc", "rb") as f:
    encrypted = f.read()
decrypted = decrypt_aes_gcm(encrypted, key, nonce)
session = ort.InferenceSession(decrypted)
# decrypted goes out of scope → GC (Python); explicitly zero in C++
```

### Memory Optimization for Large Models

`CreateSessionFromArray` doubles memory: buffer + parsed model. For 500 MB model = ~1 GB RAM during init (Issue #23775).

Options:
```cpp
// Use model bytes directly (no copy), buffer must stay alive for session lifetime
session_options.AddConfigEntry("session.use_ort_model_bytes_directly", "1");
// Initializers (weights) read from buffer directly
session_options.AddConfigEntry("session.use_ort_model_bytes_for_initializers", "1");
```

Both flags give maximum memory savings for `.ort` format models. Standard `.onnx` format: only partial benefit.

**Chunked decryption for large models (>1 GB):**
```cpp
constexpr size_t CHUNK = 64 * 1024;
std::vector<uint8_t> out;
out.reserve(file_size);
for (size_t off = 0; off < file_size; off += CHUNK) {
    size_t chunk_sz = std::min(CHUNK, file_size - off);
    auto chunk = decrypt_chunk(mapped_ptr + off, chunk_sz, &ctx);
    out.insert(out.end(), chunk.begin(), chunk.end());
}
// ONNX Runtime does NOT support streaming model load - full buffer required
```

---

## DirectML / WinML (Windows)

DirectML entered maintenance mode (2025). Microsoft recommends **Windows ML (WinML)** - abstraction layer over ONNX Runtime that auto-selects execution provider:
- NVIDIA RTX → TensorRT EP
- AMD GPU → DirectML EP
- Intel GPU/NPU → DirectML or Intel EP
- Qualcomm NPU → QNN EP
- Fallback → XNNPACK EP

```cpp
// Force DirectML EP
Ort::SessionOptions opts;
OrtSessionOptionsAppendExecutionProvider_DML(opts, 0); // device_id = 0

// Memory limits for weak GPUs
opts.SetGraphOptimizationLevel(ORT_ENABLE_ALL);
opts.SetExecutionMode(ORT_SEQUENTIAL); // less memory vs parallel
```

**GPU memory reality for weak hardware:**

| GPU | VRAM | UNet ~100MB | 1024×1024 FPS |
|-----|------|-------------|---------------|
| Intel UHD 630 | Shared 2-4 GB | Possible | 0.5-2 |
| Intel Iris Xe | Shared 4-8 GB | OK | 2-5 |
| NVIDIA GTX 1650 | 4 GB | OK | 5-15 |
| Intel Arc A380 | 6 GB | OK | 8-20 |

ONNX model 1.77 GB FP16 → ~2.5 GB VRAM at load time → 5 GB peak on first inference (intermediate buffers). 2 GB VRAM GPU: safe max model size ~300 MB.

**Fallback when VRAM exhausted:** DirectML uses shared system memory → 10-100x slowdown. Always check actual memory usage, not just model file size.

---

## CoreML Encryption (macOS)

Apple provides native CoreML model encryption with Secure Enclave integration.

```bash
# Generate key (coremltools)
python -c "import coremltools as ct; print(ct.models.utils.generate_model_encryption_key())"
```

```swift
// Encrypt at compile time
let key = try MLModelEncryptionKey(url: keyURL)
try MLModel.compileModel(at: modelURL, configuration: config, encryptionKey: key)

// Load encrypted (CoreML handles decryption transparently)
let model = try MLModel(contentsOf: compiledModelURL, configuration: config)
```

**Secure Enclave integration:** Encryption key never leaves SE. Decryption happens inside the chip. Key is device-bound (non-exportable).

**Protection strength:**
- Apple Silicon + SIP enabled + no jailbreak: **very strong**
- Intel Mac without SIP: **medium** (memory dump possible)
- Without SE (Hackintosh, VM): keys in software keychain → **weak**

**Known bypass:** `.mlmodelc` contains `model.espresso.weights` - if decrypted, easily parseable. On jailbroken device, intercept model in RAM after decryption.

---

## CoreML vs ONNX Runtime Performance (Mac)

| Model | CoreML (ANE) | CoreML (Metal) | ONNX CPU | ONNX+CoreML EP |
|-------|-------------|----------------|----------|----------------|
| MobileNetV2 (M1) | ~1.5 ms | ~5 ms | ~15 ms | ~6 ms |
| UNet 1024×1024 (M2) | ~30 ms | ~80 ms | ~300 ms | ~90 ms |
| ViT-Base (M3) | ~4 ms | ~12 ms | ~40 ms | ~15 ms |

Apple Neural Engine: 3-5x faster than Metal for compatible models.

**When to use each:**
- CoreML native: need ANE, need encryption, static shapes, Apple-only
- ONNX+CoreML EP: cross-platform code, dynamic shapes, complex ops not supported by CoreML

---

## Architecture Obfuscation via Custom Ops

Replace standard ops (Conv, MatMul) with custom ops having meaningless names. Netron and onnx-inspector cannot determine real architecture.

```cpp
struct HiddenConv2dOp : Ort::CustomOpBase<HiddenConv2dOp, HiddenConv2dKernel> {
    const char* GetName() const { return "XProcessor_v3"; } // obfuscated name
    size_t GetInputTypeCount() const { return 2; }
    size_t GetOutputTypeCount() const { return 1; }
    ONNXTensorElementDataType GetInputType(size_t) const {
        return ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT;
    }
    // ...
};

Ort::CustomOpDomain domain("com.myapp.internal");
domain.Add(&hiddenConvOp);
session_options.Add(domain);
```

**Limits of this approach:**
- Weights (initializers) still in protobuf - extractable even if op names are hidden
- Tensor shapes visible - architecture guessable from sizes
- Custom ops disable graph transformer optimizations (performance loss)

**Wrapper approach:** custom op that runs an encrypted inner session:
```cpp
struct EncryptedModelOp {
    void Compute(OrtKernelContext* context) {
        // inner_session_ holds real model, decrypted at init
        inner_session_->Run(run_options, names, tensors, ...);
    }
    std::unique_ptr<Ort::Session> inner_session_;
};
```

Outer `.onnx` file contains one custom op. Real model encrypted inside custom op binary.

---

## Model Export: Minimizing Metadata Leakage

```python
torch.onnx.export(
    model, dummy_input, "model.onnx",
    opset_version=17,
    strip_doc_string=True,    # removes Python stack traces
    do_constant_folding=True,
    input_names=["input"],    # anonymized names
    output_names=["output"],
)
```

**What remains in ONNX file after export:**
- Full computation graph (op names, connections)
- All weights as initializers (plaintext unless encrypted)
- Tensor shapes and dtypes
- Opset version

`strip_doc_string=True` removes Python source paths but not architecture. Encrypting the `.onnx` file is necessary to protect weights; op name obfuscation only protects architecture.

---

## Dual-Backend Recommendation (Desktop App)

```text
Mac:     CoreML native
         - Built-in encryption (Secure Enclave)
         - Apple Neural Engine performance
         - Compile: torch → coremltools → .mlpackage

Windows: ONNX Runtime + WinML
         - AES-256-GCM encrypted .onnx / .hmod
         - WinML auto-selects best EP
         - Compile: torch → torch.onnx.export → encrypt
```

Convert PyTorch model to both formats at build time. CoreML encryption via Apple API, ONNX via custom AES-256-GCM.

---

## Gotchas

- **`CreateSessionFromArray` doubles RAM.** 200 MB model needs ~400 MB during load. On 4 GB RAM machines with shared GPU: plan carefully.
- **ONNX Runtime has no streaming model load.** Full decrypted buffer must exist before `CreateSessionFromArray`. No way to feed it in chunks.
- **DirectML entered maintenance mode.** Use WinML API for new code. DirectML EP still works but no new features.
- **CoreML EP in ONNX Runtime silently converts to FP16.** Use native CoreML for precision-critical models. ONNX+CoreML EP may partition graph between CoreML and CPU, sometimes slower than pure CPU.
- **Custom op disables graph optimizations.** If a hot path is inside a custom op, ONNX Runtime cannot fuse it with adjacent ops. Profile before protecting hot paths.
- **Secure zero after decryption.** Use `sodium_memzero` or `SecureZeroMemory` - compiler may optimize away `memset(ptr, 0, ...)` as "unnecessary write."
- **AES-NI availability check required.** `crypto_aead_aes256gcm_is_available()` returns 0 on some ARM or older x86 without AES-NI. Fall back to ChaCha20-Poly1305.

## See Also
- [[watermarking-encrypted-models]]
- [[hkdf-personalized-weights]]
- [[output-scrambling-antipiracy]]
- [[licensing-implementation-cpp]]
