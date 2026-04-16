# Security Telemetry: Piracy Detection and Anomaly Analytics

Date: 2026-04-03
Context: Desktop application with online license server. Detecting pirated copies, credential sharing, and distribution of cracked versions via behavioral analytics.

---

## What to Collect

Minimum telemetry for piracy detection (privacy-preserving):

```json
{
  "session_id": "uuid-per-launch",
  "device_fp_hash": "sha256(device_fp + SALT)",
  "license_id_hash": "sha256(license_key)",
  "app_version": "2.1.3",
  "model_version": "5",
  "os_type": "win11",
  "inference_count": 42,
  "launch_timestamp": 1712188800,
  "country_code": "US",
  "timezone_offset": -5
}
```

**Never collect:** actual images, filenames, user content. Collect only behavioral metadata.

GDPR: telemetry for license enforcement = "legitimate interest" (Art. 6(1)(f)). Must be disclosed in Privacy Policy. Right to Erasure: delete all telemetry for a device fingerprint hash.

---

## Anomaly Detection Signals

### Simultaneous Sessions

```sql
-- Detect same license used on multiple devices concurrently
SELECT license_id_hash, COUNT(DISTINCT device_fp_hash) as device_count,
       MIN(launch_timestamp) as window_start
FROM sessions
WHERE launch_timestamp > (UNIX_TIMESTAMP() - 3600)  -- last hour
GROUP BY license_id_hash
HAVING device_count > 2
ORDER BY device_count DESC;
```

**Thresholds:**
- >2 simultaneous devices: flag for review
- >5 simultaneous devices: auto-revoke key, notify support
- >20 devices in a month: immediate auto-revoke + email alert

### Geographic Anomalies

```python
def detect_geo_anomaly(device_sessions: list[dict]) -> float:
    """Returns risk score 0-100"""
    countries = {s['country_code'] for s in device_sessions}
    timezones = {s['timezone_offset'] for s in device_sessions}
    
    score = 0
    if len(countries) > 3:  # active in >3 countries in 30 days
        score += 40
    if len(timezones) > 5:  # >5 timezone offsets = likely sharing
        score += 30
    # Impossible travel: same license active in US + EU simultaneously
    if _has_simultaneous_distant_sessions(device_sessions, max_km=5000):
        score += 50
    return min(score, 100)
```

### Version Distribution Fingerprint

Piracy release pattern: legitimate users update gradually. Cracked release = spike in old version usage.

```python
def detect_version_spike(version: str, count_today: int,
                         avg_last_7d: float) -> bool:
    # Spike detection: 3× normal rate for specific old version
    return (count_today > avg_last_7d * 3.0 and
            version != CURRENT_VERSION)
```

When detected: the cracked version number is known → activate graduated kill signal for that version.

---

## Device Fingerprint Anomalies

### VM Detection

VMs have characteristic hardware fingerprints:
```cpp
bool detect_vm() {
    bool indicators = false;
    
    // Windows: check CPUID hypervisor bit
    int cpu_info[4];
    __cpuid(cpu_info, 1);
    if (cpu_info[2] & (1 << 31)) indicators = true; // hypervisor present
    
    // Check for VM-specific hardware IDs
    const char* vm_vendors[] = {
        "VMware", "VBOX", "QEMU", "Virtual", "Hyper-V", "KVM", nullptr
    };
    std::string bios = get_bios_string();
    for (int i = 0; vm_vendors[i]; i++)
        if (bios.find(vm_vendors[i]) != std::string::npos) indicators = true;
    
    // MAC address OUI check
    if (is_vm_mac_oui(get_primary_mac())) indicators = true;
    
    return indicators;
}
```

VM = +10 risk score (not blocking alone - legitimate developers test in VMs). VM + other signals = elevated suspicion.

### Debugger Detection

```cpp
bool detect_debugger() {
#ifdef _WIN32
    if (IsDebuggerPresent()) return true;
    
    BOOL remote_debug = FALSE;
    CheckRemoteDebuggerPresent(GetCurrentProcess(), &remote_debug);
    if (remote_debug) return true;
    
    // NtQueryInformationProcess timing attack
    DWORD64 t1 = __rdtsc();
    // trivial operation
    DWORD64 t2 = __rdtsc();
    if (t2 - t1 > 1000) return true; // debugger slows RDTSC
#else // macOS
    int mib[] = {CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()};
    struct kinfo_proc info = {};
    size_t size = sizeof(info);
    if (sysctl(mib, 4, &info, &size, nullptr, 0) == 0)
        return info.kp_proc.p_flag & P_TRACED;
#endif
    return false;
}
```

Debugger = +20 risk score. Respond with stealth: don't crash/error, just increment risk score and add latency.

### Binary Integrity Check

```cpp
bool verify_self_integrity() {
    // Hash own binary
    uint8_t current_hash[32];
    hash_file(get_own_executable_path(), current_hash);
    
    // Compare against build-time embedded hash (obfuscated in binary)
    uint8_t* expected = get_obfuscated_expected_hash();
    return crypto_memcmp(current_hash, expected, 32) == 0;
}
```

Modified binary = +40 risk score. Don't error immediately - activate kill switch after random delay.

---

## Piracy Intelligence Pipeline

### Monitoring Distribution Channels

**Automated scanning:**
```python
import requests
from datetime import datetime

SEARCH_TARGETS = [
    "site:rutracker.org {product_name} crack",
    "site:github.com {product_name} crack license",
    "{product_name} keygen 2026",
]

def scan_for_cracks(product_name: str) -> list[dict]:
    findings = []
    for query_template in SEARCH_TARGETS:
        query = query_template.format(product_name=product_name)
        # Use web search API (Bing/Google)
        results = search_api(query)
        for r in results:
            findings.append({
                'url': r['url'],
                'title': r['title'],
                'query': query,
                'detected_at': datetime.utcnow().isoformat(),
            })
    return findings
```

**What to look for:**
- Cracked version numbers (e.g., "2.1.3 crack" - tells you which version was targeted)
- Keygen availability (means license algorithm was reverse-engineered)
- Forum discussions with bypass instructions
- GitHub repos with patch scripts

**When crack is found:**
1. Identify cracked version from report
2. Activate kill switch for devices on that version + anomaly patterns
3. Prepare update that changes protection mechanism
4. Ship update within 2-4 weeks (fast update cadence is itself a protection layer)

### Watermark Forensics

When pirated output appears online (user complaint, DMCA monitoring):
```bash
# Batch watermark extraction on suspected images
hmod_watermark_check --input /path/to/suspected_images/ \
    --output report.json --threshold 0.85

# Cross-reference with license database
python analyze_report.py report.json --db licenses.db
```

Output identifies license ID + timestamp → account that generated the image → evidence for enforcement.

---

## Risk Scoring Architecture

Central risk score per `{device_fp_hash, license_id}` pair, persisted server-side:

```python
RISK_FACTORS = {
    'debugger_detected': 20,
    'binary_modified': 40,
    'known_cracked_key': 50,
    'excess_simultaneous_devices': 30,
    'vm_environment': 10,
    'clock_rollback': 25,
    'geo_anomaly': 35,
    'version_spike_pattern': 45,
}

THRESHOLDS = {
    'stage1_latency': 30,    # +latency
    'stage2_artifacts': 60,  # +quality degradation
    'stage3_softblock': 100, # soft block
    'alert_human': 50,       # flag for manual review
}
```

Score persists across sessions. Decays over time for legitimate users (e.g., VM = temporary elevated score, clears after 30 days of clean behavior).

---

## Privacy-Compliant Collection

**Minimize identifiers:** hash all user-attributable data with per-install SALT. Server cannot link telemetry to real user without the SALT.

**Data retention:**
- Session telemetry: 90 days
- Aggregated anomaly reports: 1 year
- Known-pirated device hashes: until key revoked + 30 days

**GDPR data subject request:** return all records matching device_fp_hash provided by user. Erasure = delete all records for that hash from all retention periods.

---

## Gotchas

- **VM detection = false positives for developers.** Professional software developers run test environments in VMs. VM alone is +10 risk score, not a block. VM + other signals = escalate.
- **RDTSC timing attack unreliable on modern hardware.** CPU frequency scaling, turbo boost, and hypervisor time spoofing make timing-based debugger detection produce false positives. Prefer `IsDebuggerPresent` + `CheckRemoteDebuggerPresent` as primary signals.
- **Telemetry collection requires Privacy Policy disclosure.** Even hashed device fingerprints are personal data under GDPR (re-identifiable via context). Disclose purpose explicitly: "license validation and anti-piracy."
- **Geographic anomaly from VPN use is common.** Legitimate users use VPNs. Weight geo anomaly at 35 points, not as a standalone trigger. Require multiple corroborating signals.
- **Watermark extraction tool should be internal-only.** If you ship a watermark decoder in the client, attackers will use it to verify they successfully removed the watermark. Keep decoder server-side only.
- **Score must persist across restarts.** If risk score resets on app restart, pirate simply restarts to clear accumulated score. Store encrypted risk contribution in 4-layer counter storage.

## See Also
- [[remote-kill-switch]]
- [[tamper-resistant-counters]]
- [[watermarking-encrypted-models]]
- [[adobe-piracy-patterns]]
