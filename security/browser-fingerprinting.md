---
title: Browser Fingerprinting
category: identification
tags: [fingerprinting, anti-fraud, browser, tracking, privacy]
---

# Browser Fingerprinting

## Key Facts

- Browser fingerprinting identifies users by collecting unique browser and device attributes without cookies
- Combines Canvas fingerprint, WebGL fingerprint, AudioContext fingerprint, font enumeration, plugin list, and timezone into a composite identifier
- Canvas fingerprint renders hidden graphics elements; differences in GPU/driver produce unique pixel-level output
- Unlike cookies, fingerprints cannot be deleted by users - they are computed from environment characteristics
- Anti-detect browsers (Multilogin, GoLogin, Dolphin{anty}) attempt to spoof fingerprint parameters
- [[network-identifiers]] complement browser fingerprints at the network layer
- [[anti-fraud-systems]] use fingerprinting as one identification vector among many

## Patterns

```javascript
// Basic canvas fingerprinting detection
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
ctx.textBaseline = 'top';
ctx.font = '14px Arial';
ctx.fillText('fingerprint test', 2, 2);
const hash = canvas.toDataURL().hashCode();
// Each browser/GPU/driver combo produces different hash

// WebGL fingerprint extraction
const gl = canvas.getContext('webgl');
const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
```

```python
# Server-side fingerprint comparison
def fingerprint_similarity(fp1: dict, fp2: dict) -> float:
    """Compare two browser fingerprints, return similarity 0.0-1.0"""
    weights = {
        'canvas_hash': 0.25,
        'webgl_hash': 0.20,
        'audio_hash': 0.15,
        'fonts': 0.15,
        'screen_res': 0.10,
        'timezone': 0.10,
        'language': 0.05,
    }
    score = sum(
        w for key, w in weights.items()
        if fp1.get(key) == fp2.get(key)
    )
    return score
```

## Gotchas

- Canvas fingerprint alone is NOT unique per user - it identifies GPU/driver/OS combination; millions share the same hash
- Chrome's unique internal identifier (not Canvas) is per-installation and tracked across all Google ecosystem sites
- Deleting browser profile and creating a new one resets Chrome's internal identifier
- Anti-detect browsers often fail to spoof Chrome's internal identifiers visible to Google services
- `navigator.hardwareConcurrency`, `navigator.deviceMemory` and screen resolution are trivially spoofable but still used by many systems
- Tor Browser standardizes fingerprint parameters to make all users look identical - the approach of uniformity vs randomization

## See Also

- [EFF Panopticlick / Cover Your Tracks](https://coveryourtracks.eff.org/)
- [AmIUnique](https://amiunique.org/)
- [Fingerprint.js open source library](https://github.com/nicornot/fingerprintjs)
- NIST SP 800-63B (Digital Identity Guidelines) - addresses device binding
