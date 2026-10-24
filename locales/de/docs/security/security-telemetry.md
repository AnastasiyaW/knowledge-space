---
level: 3
source_sha256: c6f501fadc0b2afc725473a3cd9a5914298134d2e64f7e5b4edd60eecc8d69ae
translation: machine
translated_at: '2026-10-24'
---
# Sicherheits-Telemetrie: Piraterie-Erkennung und Anomalie-Analyse {#security-telemetry-piracy-detection-and-anomaly-analytics}

Datum: 2026-04-03
Kontext: Desktop-Anwendung mit Online-Lizenzserver. Erkennung von Raubkopien, Lizenzteilung und Verbreitung gecrackter Versionen mittels Verhaltensanalyse.

---

## Was erfasst wird {#what-to-collect}

Minimale Telemetrie für die Piraterie-Erkennung (datenschutzfreundlich):

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

**Niemals erfassen:** tatsächliche Bilder, Dateinamen, Nutzerinhalte. Es werden ausschließlich Verhaltens-Metadaten erfasst.

DSGVO: Telemetrie zur Lizenzdurchsetzung = „berechtigtes Interesse" (Art. 6 Abs. 1 lit. f). Muss in der Datenschutzerklärung offengelegt werden. Recht auf Löschung: Alle Telemetriedaten zu einem Geräte-Fingerprint-Hash löschen.

---

## Signale zur Anomalie-Erkennung {#anomaly-detection-signals}

### Gleichzeitige Sitzungen {#simultaneous-sessions}

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

**Schwellenwerte:**
- >2 gleichzeitige Geräte: zur Prüfung markieren
- >5 gleichzeitige Geräte: Schlüssel automatisch widerrufen, Support benachrichtigen
- >20 Geräte innerhalb eines Monats: sofortiger automatischer Widerruf + E-Mail-Warnung

### Geografische Anomalien {#geographic-anomalies}

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

### Versionsverteilungs-Fingerprint {#version-distribution-fingerprint}

Muster bei Piraterie-Veröffentlichungen: Legitime Nutzer aktualisieren schrittweise. Eine gecrackte Version zeigt sich als Anstieg der Nutzung alter Versionen.

```python
def detect_version_spike(version: str, count_today: int,
                         avg_last_7d: float) -> bool:
    # Spike detection: 3× normal rate for specific old version
    return (count_today > avg_last_7d * 3.0 and
            version != CURRENT_VERSION)
```

Bei Erkennung: Ist die Nummer der gecrackten Version bekannt, wird ein abgestuftes Kill-Signal für genau diese Version aktiviert.

---

## Anomalien beim Geräte-Fingerprint {#device-fingerprint-anomalies}

### VM-Erkennung {#vm-detection}

Virtuelle Maschinen weisen charakteristische Hardware-Fingerprints auf:
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

VM = +10 Risiko-Score (nicht allein blockierend, da Entwickler Tests in VMs durchführen). VM zusammen mit weiteren Signalen = erhöhter Verdacht.

### Debugger-Erkennung {#debugger-detection}

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

Debugger = +20 Risiko-Score. Reaktion unauffällig gestalten: nicht abstürzen oder Fehler melden, sondern nur den Risiko-Score erhöhen und Latenz hinzufügen.

### Prüfung der Binärintegrität {#binary-integrity-check}

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

Veränderte Binärdatei = +40 Risiko-Score. Nicht sofort mit einem Fehler reagieren, sondern den Kill-Switch nach einer zufälligen Verzögerung aktivieren.

---

## Piraterie-Aufklärung {#piracy-intelligence-pipeline}

### Überwachung der Verbreitungskanäle {#monitoring-distribution-channels}

**Automatisiertes Scannen:**
```python
import requests
from datetime import datetime

SEARCH_TARGETS = [
    "site:rutracker.org {product_name} crack",
    "site:github.com {product_name} crack license",
    "{product_name} keygen 2026"]

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

**Worauf zu achten ist:**
- Nummern gecrackter Versionen (z. B. „2.1.3 crack“ – zeigt, welche Version angegriffen wurde)
- Verfügbarkeit von Keygens (bedeutet, dass der Lizenzalgorithmus reverse-engineert wurde)
- Foren-Diskussionen mit Anleitungen zur Umgehung
- GitHub-Repositories mit Patch-Skripten

**Wenn ein Crack gefunden wird:**
1. Gecrackte Version aus dem Bericht ermitteln
2. Kill-Switch für Geräte mit dieser Version und Anomalie-Mustern aktivieren
3. Update vorbereiten, das den Schutzmechanismus ändert
4. Update innerhalb von 2–4 Wochen ausliefern (ein schneller Update-Rhythmus ist selbst eine Schutzebene)

### Wasserzeichen-Forensik {#watermark-forensics}

Wenn gepiratete Ausgaben online auftauchen (Nutzerbeschwerde, DMCA-Monitoring):
```bash
# Batch watermark extraction on suspected images
hmod_watermark_check --input /path/to/suspected_images/ \
    --output report.json --threshold 0.85

# Cross-reference with license database
python analyze_report.py report.json --db licenses.db
```

Die Ausgabe enthält Lizenz-ID und Zeitstempel → Zuordnung zum Konto, das die Datei erzeugt hat → Beweismittel für Rechtsdurchsetzung.

---

## Architektur des Risiko-Scorings {#risk-scoring-architecture}

Zentraler Risiko-Score pro Paar `{device_fp_hash, license_id}`, serverseitig persistiert:

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

Der Score bleibt über Sitzungen hinweg erhalten. Bei legitimen Nutzern klingt er mit der Zeit ab (z. B. VM = vorübergehend erhöhter Score, der nach 30 Tagen unauffälligen Verhaltens wieder zurückgesetzt wird).

---

## Datenschutzkonforme Erfassung {#privacy-compliant-collection}

**Identifikatoren minimieren:** Alle nutzerbezogenen Daten werden mit einem geräteindividuellen SALT gehasht. Ohne den SALT kann der Server die Telemetrie nicht einem realen Nutzer zuordnen.

**Aufbewahrungsfristen:**
- Sitzungstelemetrie: 90 Tage
- Aggregierte Anomaliberichte: 1 Jahr
- Bekannte Hashes gepirateter Geräte: bis zum Widerruf des Schlüssels + 30 Tage

**Auskunftsersuchen nach DSGVO:** Alle Datensätze zurückgeben, die dem vom Nutzer angegebenen device_fp_hash entsprechen. Löschung = Entfernen aller Datensätze zu diesem Hash aus allen Aufbewahrungsfristen.

---

## Stolperfallen {#gotchas}

- **VM-Erkennung führt bei Entwicklern zu Fehlalarmen.** Professionelle Softwareentwickler betreiben Testumgebungen in VMs. Eine VM allein ergibt +10 Risiko-Score, keine Sperrung. VM zusammen mit weiteren Signalen = Eskalation.
- **RDTSC-Timing-Angriff ist auf moderner Hardware unzuverlässig.** CPU-Frequenzskalierung, Turbo Boost und Zeitmanipulation durch den Hypervisor führen bei zeitbasierter Debugger-Erkennung zu Fehlalarmen. Vorzugsweise `IsDebuggerPresent` + `CheckRemoteDebuggerPresent` als primäre Signale verwenden.
- **Die Erfassung von Telemetrie erfordert Offenlegung in der Datenschutzerklärung.** Auch gehashte Geräte-Fingerprints sind nach DSGVO personenbezogene Daten (über den Kontext re-identifizierbar). Zweck ausdrücklich benennen: „Lizenzvalidierung und Schutz vor Piraterie.“
- **Geografische Anomalien durch VPN-Nutzung sind häufig.** Legitime Nutzer verwenden VPNs. Geo-Anomalie mit 35 Punkten gewichten, nicht als alleinigen Auslöser. Mehrere bestätigende Signale verlangen.
- **Das Werkzeug zur Wasserzeichen-Extraktion sollte nur intern verfügbar sein.** Wird ein Wasserzeichen-Decoder im Client ausgeliefert, nutzen Angreifer ihn, um zu prüfen, ob sie das Wasserzeichen erfolgreich entfernt haben. Decoder ausschließlich serverseitig betreiben.
- **Der Score muss Neustarts überstehen.** Wird der Risiko-Score beim Neustart der App zurückgesetzt, startet der Pirat die App einfach neu, um den angesammelten Score zu löschen. Den verschlüsselten Risikobeitrag im 4-Ebenen-Zählerspeicher ablegen.

## Siehe auch {#see-also}
- [[remote-kill-switch]]
- [[tamper-resistant-counters]]
- [[watermarking-encrypted-models]]
- [[adobe-piracy-patterns]]
