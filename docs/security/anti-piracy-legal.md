# Anti-Piracy Legal Framework: DMCA, Trade Secrets, EULA Design

Date: 2026-04-03
Context: Desktop ML inference product. Legal mechanisms for protecting software and model weights from unauthorized use and distribution.

---

## Trade Secrets Protection for ML Models

### What Qualifies as Trade Secret

Neural network weights are protectable as trade secrets when:
1. Commercial value derives from secrecy (competitors would benefit from access)
2. Reasonable measures taken to maintain secrecy
3. Not publicly disclosed

**DTSA (Defend Trade Secrets Act, US):** Federal civil remedy. Allows injunctive relief + damages for misappropriation.

**What "reasonable measures" means in practice:**
- Encrypt weights on disk and in transit (AES-256-GCM)
- Restrict access: server-side key material, device-bound licensing
- NDA for all employees/contractors with model access
- Mark model files/documentation as "Proprietary - Confidential"
- Audit logs showing who accessed model files

**What NOT to do:**
- Ship plaintext weights in application bundle (destroys trade secret claim)
- Allow unlimited offline access without any server verification
- Share raw weight files even under NDA without encryption

### ONNX/PyTorch Format = Not Copyrightable Structure

Model weights in ONNX/SafeTensors format: the file format is open, but the specific trained weight values are copyrightable as a "compilation" or protectable as trade secrets. The architecture (graph topology) is an idea, not copyrightable. The specific trained values are expression.

---

## DMCA Anti-Circumvention (17 U.S.C. § 1201)

### What It Covers

Prohibits circumventing "technological protection measures" (TPMs) that control access to copyrighted works.

**Applies to:**
- Encryption on model weights (the weights = copyrightable work + TPM = encryption)
- License verification systems that control access to software features
- DRM protecting activation codes

**Critical requirement:** the circumvented protection must actually control access to a copyrightable work. License check that returns true/false but doesn't cryptographically gate content = weaker DMCA argument. Encrypted model where key = function(license) = strong DMCA argument.

### Enforceability

**Strong cases (license-as-data architecture):**
- Model weights encrypted, key derived from valid license → circumvention clearly needed to access copyrighted weights
- ONNX Runtime `CreateSessionFromArray` with decryption → the TPM directly gates the copyrighted work

**Weak cases (boolean gate):**
- `if (isLicensed()) { run(); }` → patching the check is a gray area (some courts hold this is not "access control" for the underlying work)

**Practical enforcement:**
1. DMCA takedown to hosting provider (GitHub, RuTracker mirror hosts) - fast, requires minimal evidence
2. Cease-and-desist to identified individuals - effective for commercial piracy
3. Civil lawsuit - expensive, only for significant commercial infringement

### DMCA for Digital Watermarks

§ 1202: Prohibits removing or altering "copyright management information" (CMI). Watermarks embedded in output images = CMI if they identify the copyright owner and license.

**Watermark payload for DMCA support:**
```
bits 0-31: license_id hash (ties output to specific license)
bits 32-47: timestamp (days since epoch)
bits 48-55: app version
bits 56-63: CRC-8
```

With this payload, detecting watermark removal is possible. If pirated outputs appear without watermark → §1202 claim for intentional removal.

---

## EULA Design for Anti-Piracy Measures

### Mandatory Disclosures

Remote management and kill switch require EULA disclosure to be legally defensible:

```text
LICENSE COMPLIANCE AND REMOTE MANAGEMENT

The Software periodically communicates with our servers to:
(a) Verify your license status and activation count;
(b) Transmit a device identifier (hardware fingerprint) for license
    validation purposes;
(c) Deliver configuration updates and security parameters.

In cases of confirmed license violation, we may progressively limit
application functionality. Full functionality is restored immediately
upon valid license activation. We will not damage or delete your
personal data as part of any compliance action.

By installing or using the Software, you consent to this communication.
```

**Sony rootkit precedent (2005):** installed DRM rootkit without disclosure → $7.50/disc settlement + mandatory recall. Always disclose technical protection measures.

**WGA precedent (2006):** undisclosed daily phone-home → class action → Microsoft removed it. Must disclose phone-home behavior.

### Clickwrap vs Browse-wrap

**Clickwrap (required for enforceability):** user actively checks "I agree" checkbox + must scroll through EULA. Enforced in most US courts.

**Browse-wrap ("by using this software, you agree..."):** weak, often unenforceable against consumers. Use only as supplement to clickwrap.

**Implementation:** show EULA at first launch with explicit "I Accept" button. Store acceptance timestamp + EULA version hash in persistent storage. On update, show again if EULA changed.

### Jurisdiction Considerations

**EU - Consumer Protection:**
- Digital Content Directive (2019/770) Art. 14(2): allows termination for contract violation with "reasonable" notice
- Unfair Commercial Practices Directive: undisclosed degradation = potentially unfair practice
- GDPR: device fingerprint + usage data = personal data → Privacy Policy + lawful basis (legitimate interest)

**Russia/CIS - Limited Enforceability:**
- Software licensing enforcement practically limited for individual users
- Enterprise/commercial enforcement possible via Russian courts
- Practical strategy: graduated response (degrade quality) rather than legal action

**China - Separate Enforcement Regime:**
- Copyright law exists but practical enforcement for foreign software companies is difficult
- Consider China-specific pricing and local payment methods to reduce economic incentive for piracy
- Weibo/WeChat distribution channels harder to police than open web

---

## Copyright Registration

Register copyright in software + model weights to establish:
- Statutory damages ($750-30,000 per work; up to $150,000 willful infringement)
- Attorney's fees eligibility
- Presumption of validity

**What to register:**
- Software binary (as "computer program")
- Model weights (as "compilation" or "architectural work")
- Register before infringement for statutory damages eligibility

**US copyright registration fee:** $45-65 per work online. File within 3 months of publication for full damages option.

---

## Evidence Preservation for Enforcement

### Watermark Chain of Custody

```python
# When pirated output detected: preserve evidence
evidence_record = {
    'detected_at': datetime.utcnow().isoformat(),
    'image_hash': sha256(image_bytes).hex(),
    'watermark_payload': decoded_payload,
    'license_id': lookup_license(decoded_payload['license_id_hash']),
    'original_activation': get_activation_record(license_id),
    'detection_confidence': confidence,
    'detection_threshold': 0.85,
    'detector_version': '2.1.0',
    'source_url': piracy_url,
}
# Store immutably with timestamp server signature
```

Chain of custody requirements for litigation:
- Timestamped server logs (use append-only log storage)
- Cryptographically signed detection records
- Preserving original infringing URLs/content (screenshots + HTTP response captures)
- Activation records linking license_id to purchase

### BSA Audit Preparation

For commercial/enterprise piracy enforcement via BSA:
1. Document: activation count per license, activation device fingerprints, dates
2. Evidence: server logs showing device using licensed software → watermarked outputs found online
3. BSA engagement: BSA has delegated authority from member companies; refer commercial piracy cases

---

## Practical Enforcement Tiers

| Infringement type | Response | Mechanism |
|-------------------|----------|-----------|
| Individual personal use | Tolerate or graduated kill | Kill switch stage 1-2 |
| Commercial freelancer using pirated copy | DMCA takedown to output hosting + kill switch | Watermark detection |
| Business/enterprise use | BSA audit referral + C&D letter | License count anomaly |
| Cracked version redistributor | DMCA takedown to host | URL monitoring |
| Crack developer (GitHub) | DMCA + C&D | GitHub DMCA process |

---

## Gotchas

- **Boolean gate without encryption = weak DMCA claim.** Courts are split on whether patching a boolean license check circumvents a "TPM" protecting the copyrighted work. License-as-data (encrypted weights decrypted with license-derived key) = unambiguous DMCA TPM.
- **Kill switch without EULA disclosure = unfair practice (EU).** Cannot activate remote degradation without disclosed basis. Sony rootkit ($7.50/disc) and WGA lawsuit set clear precedent.
- **Trade secret requires actual secrecy measures.** Shipping unencrypted weights in app bundle = trade secret status destroyed. Must encrypt + restrict + NDA.
- **Statutory damages require timely registration.** Copyright registered after infringement discovery: only actual damages (hard to prove). Register before shipping for statutory damages option.
- **Chinese enforcement is practically limited.** Even valid copyright/trade secret claims may not result in enforcement action. Pricing strategy and watermarking are more practical in Chinese market than legal enforcement.
- **GDPR Right to Erasure applies to telemetry.** If you hash device fingerprints for piracy detection, a GDPR erasure request for that device must delete all telemetry records. Implement erasure endpoint.

## See Also
- [[remote-kill-switch]]
- [[watermarking-encrypted-models]]
- [[adobe-piracy-patterns]]
- [[piracy-economics]]
