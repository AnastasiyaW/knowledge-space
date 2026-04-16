# Neural Network Output Scrambling: Anti-Piracy for Inference Engines

Date: 2026-04-03
Context: Desktop C++ app with ONNX inference. Model outputs scrambled tensor; separate obfuscated converter process applies secret session-key-derived formula to produce normal image.

---

## Training Approach

### Approach A: Bake Scramble into Training

Loss = MSE(model_output, scramble(ground_truth)). Model learns to predict scrambled representation.

**Pros:** Normal image never exists in GPU memory (not even transiently).
**Cons:** Requires retraining. Scramble function must be differentiable:
- Channel/spatial permutation: differentiable (index reorder)
- XOR with key: NOT differentiable directly (use straight-through estimator)
- LUTs: NOT differentiable
- Quality loss 1-3% PSNR for nonlinear scramble

### Approach B: Post-processing (no retraining) - RECOMMENDED

Normal training. Add scramble as ONNX custom operator (last node in graph). Scramble executes on GPU, output already scrambled when copied to CPU.

```cpp
// Register ONNX Runtime custom op
struct ScrambleOp : Ort::CustomOpBase<ScrambleOp, ScrambleKernel> {
    const char* GetName() const { return "Scramble"; }
    size_t GetInputTypeCount() const { return 2; } // tensor + key
    size_t GetOutputTypeCount() const { return 1; }
    ONNXTensorElementDataType GetInputType(size_t) const {
        return ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT;
    }
    ONNXTensorElementDataType GetOutputType(size_t) const {
        return ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT;
    }
};
```

Insert scramble node into existing exported model via ONNX Graph Surgery (no retraining required).
Performance overhead: ~0.1-0.5ms additional CUDA kernel. Negligible vs 50-200ms inference.

---

## Scrambling Techniques

### Channel Permutation

For RGB (3 channels): only 3! = 6 permutations. Brute-forced in microseconds.

**Solution:** Permute intermediate channels (64ch in penultimate layer). 64! ~ 10^89 variants. Implement by permuting rows/columns of last conv weight matrix - no model changes needed.

### Spatial Scrambling

| Level | Search Space | Jigsaw Attack Resistance | Overhead |
|-------|-------------|--------------------------|---------|
| Block-level (16x16) | (64×64)! ~ 10^9000+ | **Low** - jigsaw solver recovers via block boundary matching | Minimal |
| Pixel-level | (1024×1024)! | **Medium** - histogram preserved within channels | Medium |
| Pixel-level + channel mix | Astronomical | **High** - destroys spatial AND color correlations | Medium |
| DCT-domain | Implementation-dependent | **High** - destroys spatial coherence | Significant |

**Recommendation: pixel-level permutation + channel mixing.** Block-level is vulnerable to jigsaw attacks (see arxiv:2308.02227, arxiv:2211.02369).

### Value Transformations

**Affine (y = w*x + b):** Only 2 parameters per channel. Broken with 2 known pairs. Too weak as primary defense.

**LUT per channel (8-bit):** 256! ~ 10^507 possible tables. Broken with 1 known (scrambled, original) pair if position-independent. Strengthen with position-dependent LUT (PDLUT): `out[i] = LUT[x,y][in[i]]`.

**Polynomial (session-key derived):**
```sql
y = a0 + a1*x + a2*x^2 + ... + an*x^n  (n=4-8)
Coefficients derived from session_key via HKDF
```
Needs n+1 known pairs to break - but coefficients rotate with session.

**Key-dependent color matrix:**
```text
[R', G', B'] = M(key) × [R, G, B]
```
M derived from session_key via HMAC/KDF. Linear - vulnerable to statistical analysis.

### Recommended Multi-Layer Stack

```bash
Input tensor (HWC, float32)
  ↓
[1] Channel permutation on intermediate channels (64ch)
  ↓
[2] Custom conv layer (scrambled weights from session_key)
  ↓
[3] Pixel-level spatial permutation (seed = HMAC(session_key, "spatial"))
  ↓
[4] Position-dependent polynomial transform (coefficients from session_key)
  ↓
[5] XOR with key-derived pseudorandom stream (AES-CTR)
  ↓
Scrambled output (HWC, float32)
```

Attacker must break ALL layers in correct order.

---

## Session-Key Dependent Formula

### Parameterized Inversion (RECOMMENDED)

```text
session_key → HKDF-SHA256 → scramble parameters:
  - spatial_permutation_seed  (32 bytes)
  - channel_permutation_seed  (32 bytes)
  - polynomial_coefficients   (N * float64)
  - xor_stream_key            (32 bytes)
  - affine_scale              (per channel)
  - affine_offset             (per channel)
```

Server issues `session_key` at authentication (ECDH key exchange). Key rotates every 1h-1d. Converter derives same parameters and computes inverse.

Security: even if attacker extracts converter binary, without session_key the formula is useless. Compromise = only one session exposed.

### XOR Stream (AES-CTR CSPRNG)

```cpp
void generate_scramble_stream(const uint8_t* session_key, size_t key_len,
                              float* stream, size_t num_pixels) {
    AES_CTR_Context ctx;
    aes_ctr_init(&ctx, session_key, initial_counter);
    for (size_t i = 0; i < num_pixels * 3; i++) {
        uint32_t rand_bits;
        aes_ctr_next(&ctx, &rand_bits, 4);
        stream[i] = (float)(rand_bits) / UINT32_MAX * 2.0f - 1.0f;
    }
}
// Scramble: output[i] = clamp(model_output[i] + stream[i] * strength)
// Unscramble: original[i] = output[i] - stream[i] * strength
```

Pure additive stream is weak alone - trivially inverted with one known pair. Use only as Layer 5 on top of nonlinear scramble.

---

## Converter Binary Obfuscation

The converter is the critical attack target. If broken, entire scheme is compromised.

### LLVM Obfuscation (Baseline - Required)

Tools: Obfuscator-LLVM (o-LLVM), Hikari (o-LLVM fork), commercial: IRDETO Cloakware, Arxan, Promon.

Techniques:
1. **Control Flow Flattening (CFF)** - all basic blocks in one switch inside loop; state variable controls order
2. **Bogus Control Flow** - fake branches with opaque predicates (always true/false, hard to analyze statically)
3. **Instruction Substitution** - `a+b` → `a-(-b)`, `x^y` → `(x&~y)|(~x&y)`
4. **String Encryption** - decrypt strings at runtime
5. **Constant Encoding** - replace numeric constants with computed equivalents

Against this: SATURN (LLVM IR deobfuscation), Triton (symbolic execution). CFF is not a silver bullet.

### VM Protection (for Critical Functions)

VMProtect / Themida: critical function compiled to custom bytecode for custom interpreter. Attacker sees only interpreter + bytecode blob. Current state (2025-2026): no public universal devirtualizer for recent VMProtect. Takes weeks-months for qualified reverser.

**Recommended stack:**
```text
Required (baseline):
├── LLVM obfuscation (CFF + bogus flow + string encryption)
├── Anti-debug checks (IsDebuggerPresent, ptrace, timing)
├── Integrity checks (code signing + self-checksumming)
└── Stripped symbols

Recommended (serious protection):
├── VMProtect for inverse-scramble function
├── White-box crypto for key derivation
└── Junk/dead code injection

Optional (maximum):
├── NN as one unscramble layer
├── Split into 2 processes (GPU unscramble + CPU finalize)
└── Custom VM for key management
```

**White-box crypto reality:** White-box AES broken multiple times academically (DCA - Differential Computation Analysis). Commercial WBC implementations hold better via security-through-obscurity. Useful as **one layer**, not sole defense.

### Process Split

```text
Process A: inverse_step_1(scrambled) → intermediate_1
Process B: inverse_step_2(intermediate_1) → normal_image
```

Max 2 processes - IPC overhead and complexity grow fast.

---

## IPC Security (Engine → Converter)

### Shared Memory + Encryption (RECOMMENDED)

```cpp
// Windows: random GUID segment name
std::wstring segName = L"Global\\" + generate_uuid();
HANDLE hMap = CreateFileMappingW(INVALID_HANDLE_VALUE, NULL,
    PAGE_READWRITE, 0, tensor_size, segName.c_str());
void* ptr = MapViewOfFile(hMap, FILE_MAP_ALL_ACCESS, 0, 0, tensor_size);
VirtualLock(ptr, tensor_size); // prevent swap to disk

// macOS/Linux: anonymous, unlinked immediately
int fd = shm_open("/tensor_temp", O_CREAT | O_RDWR, 0600);
ftruncate(fd, tensor_size);
void* ptr = mmap(NULL, tensor_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
shm_unlink("/tensor_temp"); // name removed, segment lives while fd open
```

Encrypt data in shared memory with ChaCha20-Poly1305 (~0.3ms for 12MB on modern CPU with SIMD). Random segment names per session.

**Named pipes:** ~5-15ms for 12MB - too slow. Debugger on converter still sees decrypted data.
**In-process DLL:** weakest - debugger on main process sees everything.

---

## Performance Benchmarks

**CPU (Intel i5-10400, 6-core, 2.9 GHz):**

| Operation | 1024×1024 | 2048×2048 | Parallelizable |
|-----------|-----------|-----------|----------------|
| Channel permutation (3ch) | ~0.01ms | ~0.04ms | Trivially (memcpy) |
| Channel permutation (64ch) | ~0.05ms | ~0.2ms | Per-channel |
| Spatial pixel permutation | ~0.5ms | ~2ms | Per-row |
| Affine transform (per-pixel) | ~0.1ms | ~0.4ms | SIMD AVX2 |
| Polynomial (degree 4) | ~0.3ms | ~1.2ms | SIMD AVX2 |
| LUT per channel | ~0.2ms | ~0.8ms | Cache-friendly |
| XOR key stream (AES-CTR) | ~0.3ms | ~1.2ms | AES-NI |
| **Full multi-layer scramble** | **~2-3ms** | **~8-12ms** | |

**GPU (CUDA):**

| Operation | 1024×1024 | 2048×2048 |
|-----------|-----------|-----------|
| Full scramble | ~0.1-0.3ms | ~0.3-0.8ms |
| + GPU→CPU copy | ~0.5ms | ~2ms |

Total overhead: ~3-5ms for typical 1024×1024. Against 50-200ms inference = <5%.

---

## Known Attacks

### Jigsaw Puzzle Solving
Block-level scrambling = jigsaw puzzle. Algorithms exploit block boundary statistics.
- 16×16 blocks: 70-90% order recovery with sufficient blocks
- 8×8 blocks: 40-60%
- **Pixel-level: immune** (no block boundaries)

### Known-Plaintext Attack (KPA) - Most Dangerous
Attacker obtains (scrambled_output, original_image) pair.

Research findings:
- All permutation-only ciphers broken from O(log2(N)) pairs (arxiv, 2017)
- Pixel permutation 1024×1024: ~20 pairs for full recovery
- Affine transform: 2 pairs per channel
- LUT (position-independent): 1 pair

**Critical: if session_key doesn't rotate between runs**, one intercepted pair may suffice for complete break.

### Statistical Analysis
- Channel permutation preserves histogram per channel
- Spatial permutation preserves global histogram
- **Defense:** nonlinear value transform (LUT/polynomial) changes histogram

---

## Gotchas

- **Permutation-only scramble breaks with 20 known-plaintext pairs** regardless of permutation size. Always combine with value transformation.
- **Session key must rotate per session** - not per user, not per day. One session = one key. Compromised key = one session exposed, not all.
- **AES-CTR stream by itself is trivially invertible** once attacker has one (scrambled, original) pair. Use only as final layer after nonlinear transforms.
- **GPU scramble in ONNX custom op** requires the op to be registered before session creation. If session is already created without the custom op, you must recreate it.
- **Block-level scramble is useless for anti-piracy** - modern jigsaw solvers (2022-2023) recover 70%+ of content from 16x16 blocks. Use pixel-level only.
- **Learned scramble heads (NN)** are theoretically elegant but lossy (~0.1-0.5 LSB errors) and vulnerable to approximation if attacker has enough pairs with known keys.
- **VMProtect significantly slows down the protected function** - 10-50x overhead. Profile before protecting hot paths.
