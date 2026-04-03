---
title: Browser and Device Fingerprinting
category: concepts
tags: [security, fingerprinting, canvas, webgl, anti-fraud, tracking, privacy]
---

# Browser and Device Fingerprinting

Technical fingerprinting methods used by anti-fraud systems and tracking: canvas fingerprinting, WebGL, AudioContext, font enumeration, hardware signals, TCP/IP stack fingerprinting, WebRTC leaks, and persistent tracking mechanisms (evercookies).

## Key Facts
- Canvas fingerprinting exploits GPU + OS rendering differences invisible to the human eye
- WebGL exposes GPU model directly via `WEBGL_debug_renderer_info` extension
- AudioContext fingerprinting works through Web Audio API processing differences
- TCP/IP stack fingerprinting (p0f) detects OS even through VPN
- WebRTC STUN requests can leak real IP behind VPN
- Evercookies store identifiers in 10+ locations to survive clearing

## Canvas Fingerprinting
Browser renders text/graphics via `<canvas>` using GPU and OS rendering libraries. Different hardware + software combos produce pixel-level differences.

Process: force-render specific text + geometric shapes -> `toDataURL()` or `getImageData()` -> hash the pixel data.

Factors: GPU model, driver version, OS font rendering (DirectWrite/CoreText/FreeType), antialiasing, sub-pixel rendering.

Evasion: anti-detect browsers inject noise into pixel data. Consistent noise is critical - random noise per call looks suspicious.

## WebGL Fingerprinting
- `UNMASKED_VENDOR_WEBGL` and `UNMASKED_RENDERER_WEBGL` directly reveal GPU
- Additional parameters: max texture size, max viewport dimensions, shader precision, supported extensions
- Combined with 3D rendering tests for highly unique fingerprint

## AudioContext Fingerprinting
`OscillatorNode` -> `DynamicsCompressorNode` -> `AnalyserNode` -> extract processed audio buffer. Floating point differences in audio processing across platforms create unique signatures.

## Font Enumeration
- Side-channel: render text in candidate fonts vs fallback, measure width/height differences
- Font sets are highly indicative: Adobe Creative Suite fonts differ from default Windows
- Language-specific fonts reveal locale

## Hardware Signals
- `screen.width`, `screen.height`, `screen.colorDepth`, `devicePixelRatio`
- `navigator.hardwareConcurrency` (logical CPU cores)
- `navigator.deviceMemory` (approximate RAM in GB)
- Battery Status API (mostly deprecated/restricted)
- Sensor calibration offsets (accelerometer, gyroscope) are device-unique
- `navigator.mediaDevices.enumerateDevices()` returns audio/video device IDs

## OS-Level Device Identifiers
- **Windows**: Machine GUID (`HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid`), disk serial numbers, BIOS UUID
- **Linux**: `/etc/machine-id`, `/var/lib/dbus/machine-id`
- **MAC addresses**: easily spoofed but collected when available
- **TPM endorsement key**: hardware-bound, not spoofable

## TCP/IP Stack Fingerprinting
OS implementation details leak through packets:
- Initial TTL (Linux: 64, Windows: 128)
- TCP window size and options ordering
- IP ID sequence generation
- Don't Fragment bit behavior

Tool: `p0f` - passive OS detection. Works even through VPN because TCP parameters originate from source OS.

## WebRTC Leaks
ICE (Interactive Connectivity Establishment) gathers candidate IPs:
- Public IP via STUN server response
- Local/private IP from network interfaces
- Even behind VPN, may reveal real IP or local network range

Mitigation: disable WebRTC (`media.peerconnection.enabled = false` in Firefox), browser extensions.

## Persistent Tracking (Evercookies)
Store identifiers in multiple locations to survive clearing:
- HTTP cookies, Flash LSOs, Silverlight storage
- `localStorage`, `sessionStorage`, `IndexedDB`, Web SQL
- HTTP ETags (cache-based)
- HSTS supercookies (encoding bits per subdomain)
- `window.name`, favicon cache

On revisit: check all locations, if any survive, restore the others.

### Browser Storage
- `localStorage`: persists until explicitly cleared, 5-10MB per origin
- `sessionStorage`: per-tab, cleared on close
- `IndexedDB`: structured, large capacity
- Cache API / Service Workers: persists across sessions

### Cookie Syncing
Ad networks sync identifiers via redirect chains. ITP (Safari) and ETP (Firefox) progressively restrict this.

## Gotchas
- Anti-detect browsers can spoof most fingerprints but consistent spoofing across all vectors is extremely difficult
- Canvas noise injection that varies per call is more suspicious than a consistent fingerprint
- Private/incognito mode does NOT prevent fingerprinting - it only clears storage
- Multiple fingerprint vectors are combined - defeating one leaves dozens of others
- Tor Browser specifically targets fingerprint uniformity (all users look identical)

## See Also
- [[anti-fraud-behavioral-analysis]] - behavioral patterns complementing fingerprints
- [[tls-fingerprinting-and-network-identifiers]] - IP analysis, geolocation
- [[osint-and-reconnaissance]] - using fingerprint data for investigation
- [[web-application-security-fundamentals]] - CSP, cookies, storage
