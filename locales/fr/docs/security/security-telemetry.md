---
level: 3
source_sha256: c6f501fadc0b2afc725473a3cd9a5914298134d2e64f7e5b4edd60eecc8d69ae
translation: machine
translated_at: '2026-10-24'
---
# Télémétrie de sécurité : détection du piratage et analytique des anomalies {#security-telemetry-piracy-detection-and-anomaly-analytics}

Date : 2026-04-03
Contexte : Application de bureau avec serveur de licences en ligne. Détection des copies pirates, du partage d'identifiants et de la distribution de versions crackées par analyse comportementale.

---

## Données à collecter {#what-to-collect}

Télémétrie minimale pour la détection du piratage (préservant la vie privée) :

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

**Ne jamais collecter :** images réelles, noms de fichiers, contenu utilisateur. Collecter uniquement des métadonnées comportementales.

RGPD : la télémétrie destinée à l'application des licences relève de l'« intérêt légitime » (art. 6, paragraphe 1, point f). Elle doit être mentionnée dans la politique de confidentialité. Droit à l'effacement : supprimer toute la télémétrie associée à un hachage d'empreinte d'appareil.

---

## Signaux de détection d'anomalies {#anomaly-detection-signals}

### Sessions simultanées {#simultaneous-sessions}

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

**Seuils :**
- Plus de 2 appareils simultanés : signaler pour examen
- Plus de 5 appareils simultanés : révoquer automatiquement la clé et notifier le support
- Plus de 20 appareils en un mois : révocation automatique immédiate et alerte par e-mail

### Anomalies géographiques {#geographic-anomalies}

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

### Empreinte de distribution des versions {#version-distribution-fingerprint}

Schéma de diffusion d'une version piratée : les utilisateurs légitimes se mettent à jour progressivement. Une version crackée se traduit par une hausse soudaine de l'usage d'une ancienne version.

```python
def detect_version_spike(version: str, count_today: int,
                         avg_last_7d: float) -> bool:
    # Spike detection: 3× normal rate for specific old version
    return (count_today > avg_last_7d * 3.0 and
            version != CURRENT_VERSION)
```

En cas de détection : le numéro de la version crackée est connu → activer le signal de désactivation progressive pour cette version.

---

## Anomalies de l'empreinte d'appareil {#device-fingerprint-anomalies}

### Détection de machines virtuelles {#vm-detection}

Les machines virtuelles présentent des empreintes matérielles caractéristiques :
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

VM = +10 au score de risque (pas de blocage à elle seule, car les développeurs légitimes testent dans des VM). VM + autres signaux = suspicion accrue.

### Détection de débogueur {#debugger-detection}

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

Débogueur = +20 au score de risque. Réagir discrètement : ne pas planter ni afficher d'erreur, se contenter d'incrémenter le score de risque et d'ajouter de la latence.

### Vérification de l'intégrité du binaire {#binary-integrity-check}

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

Binaire modifié = +40 au score de risque. Ne pas générer d'erreur immédiatement : activer le kill switch après un délai aléatoire.

---

## Chaîne de renseignement sur le piratage {#piracy-intelligence-pipeline}

### Surveillance des canaux de distribution {#monitoring-distribution-channels}

**Analyse automatisée :**
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

**Éléments à rechercher :**
- Numéros de versions crackées (par ex. « 2.1.3 crack », qui indique la version visée)
- Disponibilité de keygens (signifie que l'algorithme de licence a été rétro-ingénierié)
- Discussions sur les forums contenant des instructions de contournement
- Dépôts GitHub contenant des scripts de patch

**Lorsqu'un crack est trouvé :**
1. Identifier la version crackée à partir du rapport
2. Activer le kill switch pour les appareils de cette version présentant des schémas d'anomalies
3. Préparer une mise à jour modifiant le mécanisme de protection
4. Publier la mise à jour dans un délai de 2 à 4 semaines (une cadence de mise à jour rapide constitue en soi une couche de protection)

### Criminalistique du filigrane {#watermark-forensics}

Lorsqu'une sortie piratée apparaît en ligne (plainte d'un utilisateur, surveillance DMCA) :
```bash
# Batch watermark extraction on suspected images
hmod_watermark_check --input /path/to/suspected_images/ \
    --output report.json --threshold 0.85

# Cross-reference with license database
python analyze_report.py report.json --db licenses.db
```

La sortie identifie l'ID de licence et l'horodatage → compte ayant généré l'image → éléments de preuve pour l'application des droits.

---

## Architecture de notation des risques {#risk-scoring-architecture}

Score de risque central par couple `{device_fp_hash, license_id}`, persisté côté serveur :

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

Le score persiste entre les sessions. Il décroît avec le temps pour les utilisateurs légitimes (par ex. une VM provoque une hausse temporaire du score, qui revient à la normale après 30 jours de comportement sans anomalie).

---

## Collecte conforme à la vie privée {#privacy-compliant-collection}

**Minimiser les identifiants :** hacher toutes les données rattachables à un utilisateur avec un SALT propre à chaque installation. Le serveur ne peut pas relier la télémétrie à un utilisateur réel sans le SALT.

**Durées de conservation :**
- Télémétrie de session : 90 jours
- Rapports d'anomalies agrégés : 1 an
- Hachages d'appareils connus pour piratage : jusqu'à révocation de la clé + 30 jours

**Demande d'accès RGPD :** renvoyer tous les enregistrements correspondant à `device_fp_hash` fourni par l'utilisateur. Effacement = supprimer tous les enregistrements de ce hachage, pour toutes les périodes de conservation.

---

## Pièges à éviter {#gotchas}

- **La détection de VM produit de faux positifs chez les développeurs.** Les développeurs logiciels professionnels exécutent souvent leurs environnements de test dans des VM. La VM seule ajoute +10 au score de risque, sans bloquer. VM + autres signaux = escalade.
- **L'attaque par timing RDTSC n'est pas fiable sur le matériel moderne.** La mise à l'échelle de fréquence du processeur, le turbo boost et la falsification du temps par l'hyperviseur provoquent de faux positifs avec la détection de débogueur fondée sur le timing. Privilégier `IsDebuggerPresent` et `CheckRemoteDebuggerPresent` comme signaux principaux.
- **La télémétrie doit être mentionnée dans la politique de confidentialité.** Même les empreintes d'appareils hachées sont des données personnelles au sens du RGPD (ré-identifiables par le contexte). Indiquer explicitement la finalité : « validation de licence et lutte contre le piratage ».
- **Les anomalies géographiques liées à l'usage de VPN sont courantes.** Les utilisateurs légitimes utilisent des VPN. Pondérer l'anomalie géographique à 35 points, et non comme déclencheur autonome. Exiger plusieurs signaux concordants.
- **L'outil d'extraction de filigrane doit rester interne.** Si un décodeur de filigrane est livré dans le client, les attaquants l'utiliseront pour vérifier qu'ils ont bien supprimé le filigrane. Conserver le décodeur uniquement côté serveur.
- **Le score doit persister au redémarrage.** Si le score de risque est remis à zéro au redémarrage de l'application, le pirate n'a qu'à redémarrer pour effacer le score accumulé. Stocker la contribution au risque chiffrée dans le stockage de compteurs à 4 couches.

## Voir aussi {#see-also}
- [[remote-kill-switch]]
- [[tamper-resistant-counters]]
- [[watermarking-encrypted-models]]
- [[adobe-piracy-patterns]]
