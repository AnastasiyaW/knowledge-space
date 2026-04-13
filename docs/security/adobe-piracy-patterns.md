# Adobe Piracy Patterns: Attack Categories and Lessons for ML Protection

Date: 2026-04-03
Context: Defensive security research. Understanding Adobe attack patterns to architect better ML product protection.

---

## Adobe Genuine Software (AGS) Architecture

AGS = background service checking authenticity of installed Adobe apps.

**What it checks:**
- Serial number / license type
- Binary integrity (hashes of executables)
- Activation validity via server

**Weaknesses:**
- Separate process - can be killed/blocked
- Periodic checks, not continuous
- Server communication blockable via hosts file
- Vulnerable to DLL substitution

**License data location:** `<user>/AppData/Roaming/Adobe/`

**Key endpoints:**
- `lcs-cops.adobe.io` - Feature Restricted Licensing
- `lm.licenses.adobe.com` - license validation
- `activate.adobe.com` - activation

**Offline grace period:**
- Annual subscription: 99 days offline
- Monthly subscription: 30 days
- **Critical weakness:** 99-day grace period means one successful activation = app works offline long enough to apply permanent patches

**Most effective Adobe protection:** Firefly (AI features) runs server-side. Cannot pirate server-side computation. This is the architectural lesson.

---

## Attack Category 1: DLL Replacement

**Mechanism:** Replace `amtlib.dll` (license DLL) with modified version that returns "license valid" on all queries.

**AMTEmu (2013-2019) attack path:**
1. Find `amtlib.dll` in app directory
2. Replace with patched DLL
3. Patched DLL returns true to all license checks
4. Result: permanent activation

**Why it worked for years:**
- Single DLL responsible for all licensing logic
- Boolean gate - DLL returned true/false, always returning true bypassed everything
- Adobe didn't change architecture for years

**Lesson:** NEVER concentrate licensing logic in one module. Distribute checks across dozens of locations. Inline checks, not calls to a separate "license" function.

---

## Attack Category 2: Hosts File Modification

```
127.0.0.1 lcs-cops.adobe.io
127.0.0.1 lm.licenses.adobe.com
127.0.0.1 activate.adobe.com
127.0.0.1 genuine.adobe.com
# ... dozens more Adobe domains
```

GitHub repos maintain updated Adobe host block lists. Blocks all server communication.

**Lessons:**
- Don't rely on DNS names alone; use certificate pinning
- Detect hosts file modification (compare DNS resolution to known IP)
- Use IP fallback in addition to DNS
- Use steganographic communication (kill signal in CDN headers/weights)
- Don't be overly aggressive - corporate firewalls affect legitimate users

---

## Attack Category 3: Binary Patching

**Mechanism:**
1. Disassemble binary (IDA Pro, Ghidra, OllyDbg)
2. Find conditional branch after license check
3. Replace `JNZ` → `JMP` (unconditional) or NOP the call

```asm
; Original
call license_check
test eax, eax
jnz  failure_path    ; jump if license invalid

; Patched
call license_check
test eax, eax
nop                  ; always falls through to success
nop
```

**Techniques:**
- NOP injection
- Conditional branch inversion
- Comparison result forcing
- IAT hooking (Import Address Table address substitution)

**GenP (2019-present):** open-source AutoIt patcher, community-maintained. Pattern-scans for characteristic license check byte sequences across updates.

Why GenP keeps working despite updates: license check logic structure doesn't change fundamentally. `if (license_valid) { run } else { block }` - still one bit. GenP finds new patterns for each version.

**Fundamental "boolean gate" problem:**
```c
if (isLicensed()) {
    enableFeatures();
}
```
Regardless of isLicensed() complexity, result = 1 bit (true/false). One patched instruction bypasses everything.

**Lesson: License must be DATA, not boolean:**
- License key contains parameters required for algorithm operation
- Without correct key → algorithm produces garbage, not "blocked"
- No single `if (licensed)` to patch
- Example: HKDF-derived model weights ([[hkdf-personalized-weights]]), encrypted model ([[watermarking-encrypted-models]])

---

## Attack Category 4: Fake Local License Server

**Mechanism:** Local server emulates Adobe server responses. Pirate intercepts via hosts file or proxy, sends fake "license valid" responses.

**Advantage over binary patching:** doesn't modify files on disk - harder to detect.

**Lessons:**
- Server responses must be cryptographically signed (Ed25519)
- Mutual TLS
- Response must contain DATA needed for computation (not just "OK")
- Even with fake server, attacker can't forge Ed25519-signed key material

---

## Attack Category 5: Pre-patched Installers (Repacks)

**Mechanism:** Modified installers with patches pre-applied. No Creative Cloud required.

**Why it's hard to prevent:** if app can run standalone without server binding, repacks are inevitable.

**Lessons:** Server-dependent architecture is the only reliable defense against repacks. If core functionality requires live server validation that returns cryptographic material, repacked installers are useless.

---

## Attack Category 6: Grace Period Exploitation

**Mechanism:** Activate legitimately → wait for grace period → patch binary → keep working forever (grace period cached license works offline indefinitely after patch).

**Lessons for offline ML apps:**
- Model encrypted; decryption key = function of hardware ID + license + timestamps
- Without server verification, model doesn't decrypt
- Even cached license requires periodic re-derivation of encryption key

---

## Adobe's Effective Defenses (to Copy)

### Multiple Independent Verification Points
AGS (background service) + in-app checks + CC Desktop App checks. Even if one bypassed, others continue working.

For ML products: distribute checks across code. Not one `if (licensed)`, but dozens of check points in different modules.

### Server-Side Feature Gating
Generative AI (Firefly) runs ONLY on Adobe servers. Impossible to pirate server-side computation. Generates Generative Credits - server-side accounting, cannot be forged.

For ML products: full server-side is best but not always viable. Hybrid: key decryption material comes from server, stored model is useless without it.

### Continuous Updates Breaking Old Cracks
Every update potentially breaks current patches. Creates windows where pirated version doesn't work. Forces pirates to constantly update cracks.

### Subscription + Cloud Features as Value-Add
Cloud storage, fonts, libraries, collaboration work only with active subscription. Pirated version = crippled version. Revenue grew $4.2B → $21.5B (2011-2024). 37M CC subscribers.

### Graduated Response vs Hard Block
Adobe's response to GenP 3.x: warnings, feature degradation, targeted blocks. Not bricking every patched installation (that would drive casual users away).

---

## Adobe's Ineffective Defenses (to Avoid)

### Single DLL for All Licensing (amtlib.dll)
One replacement = full bypass. Fixed now but the lesson: never centralize.

### Predictable DNS Names
Block 20 domains in hosts file = done. Use pinning + steganographic channels + IP fallback.

### Boolean Gate Everywhere
Pattern: `if (isLicensed())` → always crackable by NOP. Fix: license = decryption ingredient.

### Long Offline Grace Period
99-day grace = 99 days for pirates to apply permanent patches. For ML products: periodic re-derivation of keys from server data.

---

## Photoshop Plugin Attack Surface

**CEP extensions (deprecated):** JavaScript minification = no real protection. Minified JS easily deobfuscated.

**UXP plugins:** Code reviewed by Adobe before marketplace publication, but direct install (`.ccx`) bypasses review.

**Plugin license verification:** typically an HTTP request to vendor server at startup (~0.3s check). Easily bypassed by returning fake "OK" from local proxy if response is not cryptographically signed.

**Lesson for plugin developers:** response signing is mandatory. If license response contains only `{"valid": true}`, local fake server trivially emulates it.

---

## Enforcement Strategy

**BSA (Business Software Alliance) + Adobe:**
- Audit demand letters sent to companies
- Self-audit declaration required
- Settlements: $100K+ typical for commercial use
- Company must purchase licenses + destroy unlicensed copies + agree to future audits

**"Piracy tolerance" strategy:**
- Students pirating → learning → get jobs → company buys corporate licenses
- Individual users mostly left alone (they stay in ecosystem)
- Commercial/enterprise piracy pursued aggressively
- Redistributors get takedowns

**Timeline:**
- 1990s: SafeDisc/SecuROM (cracked in ~1 week)
- 2013: CC subscription launch; first cracks appeared 2 DAYS later
- 2019+: AGS + cloud-gated features
- 2022: GenP pattern detection in CC 23.x
- 2024+: Neural Filters/Firefly moved to server-side

---

## Gotchas

- **Revenue grew 5× despite (or because of) piracy.** Adobe's "piracy tolerance" strategy is deliberate - free exposure to students creates future paying customers. Not all piracy is pure loss.
- **Even after architecture improvements, GenP keeps working.** Community-updated pattern scanner adapts to new binary patterns. Only server-side functionality is truly piracy-resistant.
- **Grace period cannot be zero for UX.** 99 days is extreme; 7-30 days is the right balance between user experience (travel, network issues) and security.
- **Aggressive anti-piracy hurts legitimate users first.** Corporate firewalls block phone-home → support tickets. Design graceful degradation, not hard blocks, for network failures.
- **Signed responses are non-negotiable.** Fake server attack (Category 4) makes all unsigned server responses pointless. Ed25519 verification must be part of any license check that involves server communication.
- **GenP source code released in 2023.** Open-source community continues maintaining forks. "Security through obscurity" of binary patterns has finite lifespan; architectural defense (license = data) is permanent.
