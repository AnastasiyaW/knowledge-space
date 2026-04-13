# Remote Kill Switch: Graduated Response for Desktop Applications

Date: 2026-04-03
Context: Desktop C++ retouching app (Mac + Windows). Targeted, operator-controlled response to confirmed piracy. 3 stages of graduated response. Ed25519-signed signals via 5 delivery mechanisms.

Related: [[licensing-implementation-cpp]], [[tamper-resistant-counters]], [[output-scrambling-antipiracy]]

---

## Concept

Kill switch differs from autonomous degradation timers:
- **Targeted** - activated for specific `device_fp` / `license_key`
- **Operator-controlled** - human decision on server, not algorithm
- **Reversible** - deactivatable per-user (purchase = instant recovery)
- **Graduated** - 3 response stages instead of binary block

---

## 3 Response Stages

### Stage 1: Stealth Latency (7-14 days)

Goal: pirate suspects a problem but cannot prove it.

```cpp
// Random delays in inference pipeline
// Normal distribution: mu=400ms, sigma=200ms
// NOT fixed delays - fixed delays look suspicious
double delay_ms = normal_dist(rng, 400.0, 200.0);
std::this_thread::sleep_for(std::chrono::milliseconds((int)delay_ms));
```

Gradual escalation: day 1 = 1.2× latency, day 3 = 2×, day 7 = 3-5×.

**Masking:** Attach delays to plausible compute events. Log entries that look legitimate:
```
[PERF] GPU memory fragmented, running defrag...
[WARN] ONNX session cache miss, rebuilding...
[INFO] Calibrating color space profile...
```

Insert delays in compute pipeline only, NOT UI thread (freeze = obvious).

Detectability thresholds:
- 1.5× - only power users notice via A/B comparison
- 2-3× - most professionals notice
- 5× - unacceptable for workflow

### Stage 2: Quality Degradation (14-21 days)

Goal: output becomes unsuitable for professional work, looks like "model bug."

Implementation (combine techniques):
1. **Micro-noise in skin tones** - Gaussian noise (sigma 2-5) in LAB a/b channels in skin regions
2. **Sharpness reduction** - Gaussian blur radius 0.3-0.5px on output (critical detail loss for retouching)
3. **Color shift** - white balance offset 200-500K warm. Looks like "model gives yellow cast"
4. **Banding artifacts** - posterization (reduce to 240-250 levels in shadows). Looks like "8-bit quantization"

**Calibration sweet spot:** artifacts visible at 100% zoom on retina display, invisible in preview. Professional notices within 1-3 work sessions.

**Escalation schedule:**
- Days 1-3: sharpness loss only
- Days 3-7: + color shift
- Days 7-14: + skin tone noise
- After 14: + banding; output unsuitable for client work

### Stage 3: Soft Block

Goal: app stops working but message doesn't say "blocked" or "pirated."

```
Acceptable messages:
- "Please update your application to continue. A critical update is required
   for your GPU configuration."
- "License validation failed. Please check your internet connection."
- "This version is no longer supported. Download the latest version."
```

Implementation: inference returns blank/black image with overlay message. "Retry" button triggers re-validation (instant recovery on license purchase). "Learn more" → pricing page.

### Timing Randomization (Anti-Pattern Detection)

Fixed timers allow pirates to document and share patterns.

```
base_delay_stage1 = 7 days  → actual: 5-9 days
base_delay_stage2 = 14 days → actual: 10-18 days
base_delay_stage3 = 21 days → actual: 15-27 days

actual_delay = base_delay * (1.0 + random(-0.3, 0.3))
```

**Bind randomization to device_fp, not wall clock:**
```cpp
// Deterministic per-device, unpredictable across devices
uint32_t device_hash = fnv1a(device_fp);
float jitter = (float)(device_hash & 0xFFFF) / 65535.0f * 0.6f - 0.3f;
```

Different devices get different timers → pirates can't collectively detect pattern via forums.

---

## 5 Delivery Mechanisms

### 1. Phone-Home Response (Primary)

```json
// Normal /heartbeat response
{"status": "ok", "counter": 42}

// Response with kill signal
{
  "status": "ok",
  "counter": 42,
  "config": {
    "perf_mode": 2,       // 0=normal, 1=stage1, 2=stage2, 3=stage3
    "perf_seed": 834729,  // seed for delay randomization
    "effective_after": "2026-04-10T00:00:00Z"
  }
}
```

Pros: simple, existing channel. Cons: hosts-file blocking defeats it.
Counter: without phone-home, CORELOCKER doesn't deliver key_weights → model degrades automatically (separate defense layer).

### 2. Update Check (Secondary)

```json
// Update manifest on CDN
{
  "version": "2.1.3",
  "url": "https://cdn.example.com/update.zip",
  "signature": "...",
  "device_config": "base64(AES-GCM encrypted config blob)"
}
```

Config blob after decryption:
```json
{
  "rules": [
    {"fp_prefix": "a3f2", "action": 1, "seed": 123},
    {"fp_hash": "sha256:deadbeef...", "action": 3}
  ],
  "default": 0
}
```

Can use different CDN/domain than main API. Pirates must block both.

### 3. CDN Response Headers (Covert Channel)

```
HTTP/1.1 200 OK
Content-Type: image/png
X-App-Config: eyJwZXJmX21vZGUiOjJ9   // base64 JSON kill signal
ETag: "abc123-sig-deadbeef"            // ETag encodes signature
Cache-Control: no-cache
```

**Enhanced targeting:** Send `device_fp` in query string or cookie; CDN edge function returns personalized header.

Pros: pirate doesn't suspect image resources carry kill signal.
Cons: CDN may cache headers; not targeted without edge function.

### 4. DNS TXT Record (High Resistance)

```
_config.example.com. 300 IN TXT "v=appconf1 p=2 s=834729 t=1712188800"
// v=version, p=perf_mode, s=seed, t=timestamp (Unix)
```

**Targeted via device fp:**
```
App queries: {hash(device_fp)[0:8]}._config.example.com
// E.g.: a3f2b8c1._config.example.com
// DNS server creates TXT record only for targeted hashes
```

Pros: DNS practically impossible to fully block; cached by OS; looks like normal SPF/DKIM traffic.
Cons: 255-byte TXT limit (sufficient for signed signal); TTL 60-300s minimum.
Cost: Cloudflare Workers / Route53 - $0-5/month at this scale.

### 5. Steganographic: Kill Signal in Key Weights

The subtlest approach: encode kill signal in model weights delivered via CORELOCKER.

```
clean   weights neuron[42] = [0.1523, -0.3847, 0.9812, ...]
kill    weights neuron[42] = [0.1524, -0.3847, 0.9812, ...]
                                  ^
                         LSB difference = kill signal bit
```

Server holds "clean" and "kill" key_weights. Kill weights have subtle modifications in specific neurons encoding signal bits. Client checks "watermark" in received weights → triggers stage if detected.

**Advantage:** kill signal is inseparable from key weights. Blocking signal delivery = losing key weights = model degrades via CORELOCKER. Cannot be blocked independently.

### Mechanism Comparison

| Mechanism | Block Resistance | Targeting | Stealth | Complexity | Use |
|-----------|-----------------|-----------|---------|------------|-----|
| Phone-home | Low | High | Medium | Low | Primary |
| Update check | Medium | High | High | Low | Secondary |
| CDN headers | Medium | Medium | High | Medium | Secondary |
| DNS TXT | High | High | High | Medium | Backup |
| Key weights | Very high | Per-user | Very high | High | Optional |

**Principle:** implement 2-3 mechanisms. Pirate must find and block ALL channels.

---

## Cryptographic Protection

### Ed25519 Signal Signature

Kill signal MUST be signed. Unsigned signals allow:
- Fake kill signals to block legitimate users (DoS)
- Fake "all clear" to unblock pirated copies

```
Server: Ed25519 private key (on VPS, never in client)
Client: Ed25519 public key (embedded in binary, obfuscated)

signal = {
  "target": "sha256(device_fp + SALT)",
  "action": 2,
  "seed": 834729,
  "issued_at": 1712188800,
  "expires_at": 1712793600,
  "nonce": "random_16_bytes"
}

signature = Ed25519.sign(private_key, canonical_json(signal))
```

Signature = 64 bytes (fits in DNS TXT record).

### Client Verification

```cpp
// Check targeting
std::string local_target = sha256(device_fp + SALT);
if (signal.target != local_target &&
    signal.target != "*" &&
    !signal.target.startswith("prefix:")) {
    return; // Not for this device
}

// Verify signature (libsodium)
if (crypto_sign_verify_detached(sig, msg, msg_len, pk) != 0) {
    return; // Invalid signature - fake signal
}

// Anti-replay
if (signal.expires_at < current_time) return; // expired
if (signal.issued_at < last_known_signal_time) return; // replay

// Apply (time-delayed, randomized)
schedule_action(signal.action, signal.seed, apply_after_random_delay());
```

**Wildcard targeting:**
```json
{"target": "*"}                      // all devices (use carefully)
{"target": "prefix:a3f2"}            // devices with fp starting a3f2
{"target": "license:CRACKED-KEY-123"} // all devices with specific cracked key
```

### Multiple Independent Handlers

Attacker finding and NOP-ing one kill signal handler must find all others:

```cpp
// Spread checks across unrelated code paths
// Image loader startup
void ImageLoader::init() {
    // ... real init code ...
    check_performance_config_1(); // disguised as "config check"
}

// GPU init
void GPUContext::create() {
    // ... real GPU code ...
    check_performance_config_2(); // disguised as "GPU calibration"
}

// Color conversion
void ColorConverter::process() {
    // ... real color code ...
    check_performance_config_3(); // disguised as "ICC profile check"
}
```

**Time-delayed application:** handler receives signal but applies it 2-7 days later (randomized). Makes it hard to identify which handler caused degradation.

---

## Legal Analysis

### EU Requirements

For kill switch to be legally defensible in EU:
1. **Disclosed in EULA** - clearly, not fine print
2. **Graduated response** - not instant block
3. **Recovery possible** - purchase restores functionality
4. **No user data damage** - only functionality affected

Relevant: Digital Content Directive (2019/770) Art. 14(2) allows service termination on contract violation with notice. Unfair Commercial Practices Directive (2005/29) - secret degradation can be unfair practice; must be in EULA.

Sony rootkit (2005): installed without disclosure → $7.50/disc settlement, product recall. Lesson: NEVER install without user knowledge.

WGA lawsuit (2006): undisclosed daily phone-home → Microsoft removed it. Lesson: disclose phone-home behavior.

### US Requirements

1. Clickwrap EULA with explicit disclosure
2. Phone-home disclosed in Privacy Policy
3. No damage to user data
4. Appeal/recovery process

Nintendo Switch 2 (2025): EULA explicitly allows remote disable for ToS violations. No legal challenges to date because it was disclosed.

### EULA Clause Template

```
LICENSE COMPLIANCE AND REMOTE MANAGEMENT

The Software periodically communicates with our servers to verify license
compliance and deliver updates. This includes:

(a) Transmission of a device identifier (hardware fingerprint) for
    license validation purposes;
(b) Verification of license status and activation count;
(c) Delivery of configuration updates including performance parameters.

In cases of confirmed license violation, we may progressively adjust
application performance. Full functionality is restored upon valid
license activation.
```

---

## Gotchas

- **Predictable timers are reverse-engineered quickly.** If degradation starts exactly on day 7 every time, pirates document it in hours. Always randomize timing based on device_fp hash.
- **Stage 1 latency in UI thread = obvious.** Sleep only in compute/inference pipeline. Users accept "processing..." delays; they don't accept UI freezes.
- **Stage 2 artifacts must survive professional review.** Test with actual retouching workflows at 100% zoom on retina displays, not just casual glance.
- **DNS TXT records have 255-byte limit per string** but can chain multiple strings in one record. Ed25519 signature (64 bytes base64 = ~88 chars) + metadata fits in single string.
- **Multiple handlers are useless if pattern is obvious.** Don't name functions `check_kill_switch()`. Embed checks in domain-appropriate code paths with domain-appropriate names.
- **Ed25519 public key in binary can be replaced.** Use obfuscation + make it participate in model key derivation (as in [[licensing-implementation-cpp]]) so replacing it = wrong model decryption key.
- **"All clear" signals need freshness check too.** Without expiry + sequence numbers, a cached "all clear" replay keeps the app un-degraded forever.
- **Stage 3 must convert, not just block.** Show a message + purchase button. Pure blocking with no CTA leaves revenue on the table. Some pirates will convert if given easy path.
