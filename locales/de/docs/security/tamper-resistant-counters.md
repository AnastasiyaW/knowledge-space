---
level: 4
source_sha256: bb68a26417ef43baec838bab6bd61d65ef85052d2b177c42954f41dece77d280
translation: machine
translated_at: '2026-10-24'
---
# Manipulationssichere monotone Zähler für Desktop-Apps {#tamper-resistant-monotonic-counters-for-desktop-apps}

Datum: 2026-04-03
Kontext: C++, Windows + macOS. Schutz einer Testphase über einen nur steigenden Zähler. 4 Speicherschichten; aktueller Wert = max() aller vier.

---

## Architektur: Speicherung in 4 Schichten {#architecture-4-layer-storage}

```bash
Layer 1: OS credential store (Windows Credential Manager / macOS Keychain)
Layer 2: Registry (Windows) / plist + xattr (macOS) - disguised
Layer 3: Hidden file + NTFS ADS (Windows) / extended attributes (macOS)
Layer 4: Server backend (source of truth)

Current counter = max(layer1, layer2, layer3, layer4)
```

Der Verlust einer einzelnen Schicht ist unkritisch. Ein Angreifer muss alle vier gleichzeitig überwinden.

---

## Schicht 1: OS-Credential-Store {#layer-1-os-credential-store}

### Windows Credential Manager {#windows-credential-manager}

```cpp
#include <windows.h>
#include <wincred.h>
#pragma comment(lib, "advapi32.lib")

// Disguise as system component
static const wchar_t* CRED_TARGET = L"Microsoft.Windows.Security.TokenBroker.Cache.v2";

bool WriteCounter(uint64_t counter) {
    CREDENTIALW cred = {};
    cred.Type = CRED_TYPE_GENERIC;
    cred.TargetName = const_cast<LPWSTR>(CRED_TARGET);
    cred.CredentialBlobSize = sizeof(uint64_t);
    cred.CredentialBlob = reinterpret_cast<LPBYTE>(&counter);
    cred.Persist = CRED_PERSIST_LOCAL_MACHINE; // survives logoff
    cred.UserName = const_cast<LPWSTR>(L"WindowsSecurityService");
    return CredWriteW(&cred, 0) == TRUE;
}

bool ReadCounter(uint64_t& counter) {
    PCREDENTIALW pCred = nullptr;
    if (!CredReadW(CRED_TARGET, CRED_TYPE_GENERIC, 0, &pCred))
        return false;
    if (pCred->CredentialBlobSize >= sizeof(uint64_t))
        memcpy(&counter, pCred->CredentialBlob, sizeof(uint64_t));
    CredFree(pCred);
    return true;
}
```

**Grenzen:** Maximale Blob-Größe 2560 Byte (Win7+). CRED_PERSIST_LOCAL_MACHINE = überlebt die Anmeldesitzung.

**Schwachstellen:**
- Sichtbar unter Systemsteuerung > Anmeldeinformationsverwaltung > Generische Anmeldeinformationen
- `cmdkey /delete:TargetName` entfernt den Eintrag
- Andere Apps desselben Benutzers können lesen und schreiben (keine Isolation zwischen Apps)
- Gespeichert als verschlüsselte .vcrd-Dateien in `%LOCALAPPDATA%\Microsoft\Vault\` über DPAPI

**Gegenmaßnahme:** Verschlüsselten Wert zusammen mit einem HMAC speichern, damit der rohe Blob nicht verrät, dass es sich um einen Zähler handelt.

### macOS Keychain {#macos-keychain}

```objc
#import <Security/Security.h>

static NSString* const kServiceName = @"com.apple.security.analytics.cache";
static NSString* const kAccountName = @"device-state-v2";

bool WriteCounterToKeychain(uint64_t counter) {
    NSData* data = [NSData dataWithBytes:&counter length:sizeof(counter)];
    NSDictionary* query = @{
        (__bridge id)kSecClass: (__bridge id)kSecClassGenericPassword,
        (__bridge id)kSecAttrService: kServiceName,
        (__bridge id)kSecAttrAccount: kAccountName,
    };
    NSDictionary* update = @{ (__bridge id)kSecValueData: data };
    OSStatus status = SecItemUpdate((__bridge CFDictionaryRef)query,
                                    (__bridge CFDictionaryRef)update);
    if (status == errSecItemNotFound) {
        NSMutableDictionary* addQuery = [query mutableCopy];
        addQuery[(__bridge id)kSecValueData] = data;
        addQuery[(__bridge id)kSecAttrAccessible] =
            (__bridge id)kSecAttrAccessibleAfterFirstUnlock;
        status = SecItemAdd((__bridge CFDictionaryRef)addQuery, NULL);
    }
    return status == errSecSuccess;
}
```

**Überlebensmatrix des Keychains:**

| Speicher | App-Deinstallation | "Einstellungen zurücksetzen" | OS-Neuinstallation |
|----------|--------------------|------------------------------|--------------------|
| ~/Library/Preferences/*.plist | Überlebt (macOS) | Gelöscht | Gelöscht |
| Keychain-Eintrag | Überlebt | Überlebt | Gelöscht |
| iCloud-Schlüsselbund-Sync | Überlebt | Überlebt | **Überlebt (!)**|
| xattr auf ~/Library/ | Überlebt | Überlebt | Gelöscht |

**macOS-Schwachstellen:** `Keychain Access.app` zeigt alle generischen Passwörter an. `security find-generic-password -s "ServiceName"` und `security delete-generic-password` funktionieren von der CLI aus.

**Secure Enclave auf Apple Silicon:** Die SE speichert nur P256-Privatschlüssel. Workaround:
1. SE-gebundenen Schlüssel mit `kSecAttrTokenIDSecureEnclave` erzeugen
2. `{counter_value, device_id, timestamp}` mit dem SE-Schlüssel signieren (ECDSA)
3. Signierte Struktur im Keychain speichern
4. Beim Lesen die SE-Signatur prüfen. Ungültige Signatur = Manipulation erkannt
5. Der Schlüssel ist gerätegebunden (nicht exportierbar). Neuer Mac = neuer Schlüssel, die Server-Schicht stellt den Wert wieder her.

Hinweis: SE-Counter-Lockboxes (8-Bit, 8-Bit maximale Versuche) sind über die öffentliche API **nicht** zugänglich. Sie dienen ausschließlich dem Passcode-Schutz.

---

## Schicht 2: Getarnte Registry / Plist {#layer-2-disguised-registry-plist}

### Versteckte Registry-Orte unter Windows {#windows-registry-hidden-locations}

```cpp
// HKCU keys (no admin required) disguised as system components
const wchar_t* locations[] = {
    L"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\SessionInfo\\{random-GUID}",
    L"Software\\Microsoft\\CTF\\Assemblies\\{random-GUID}",
    L"Software\\Microsoft\\InputMethod\\Settings\\{random-GUID}",
    L"Software\\Classes\\CLSID\\{random-GUID}\\InprocServer32",
    L"Software\\Wow6432Node\\Microsoft\\Cryptography\\Providers\\{random-GUID}",
};

bool WriteCounterToRegistry(const wchar_t* subkey, const wchar_t* valueName,
                            uint64_t counter) {
    HKEY hKey;
    LONG result = RegCreateKeyExW(HKEY_CURRENT_USER, subkey, 0, NULL,
                                   REG_OPTION_NON_VOLATILE, KEY_WRITE,
                                   NULL, &hKey, NULL);
    if (result != ERROR_SUCCESS) return false;
    uint64_t obfuscated = counter ^ GetMachineFingerprint(); // XOR with HW fp
    result = RegSetValueExW(hKey, valueName, 0, REG_BINARY,
                            reinterpret_cast<const BYTE*>(&obfuscated),
                            sizeof(obfuscated));
    RegCloseKey(hKey);
    return result == ERROR_SUCCESS;
}
```

**Was Registry-Cleaner löschen:**

| Kategorie | CCleaner | Revo Uninstaller |
|-----------|----------|------------------|
| HKCU\Software\{AppName} | Ja (nach Deinstallation) | Ja (aggressiv) |
| Verwaiste COM-CLSID | Teilweise | Teilweise |
| Zufällige GUID in Systemunterschlüsseln | **Nein** | **Nein** |
| HKCU\Software\Microsoft\* | **Nein** (zu riskant) | **Nein** |

---

## Schicht 3: Versteckte Dateien {#layer-3-hidden-files}

### Windows: NTFS Alternate Data Streams (ADS) {#windows-ntfs-alternate-data-streams-ads}

Stärkster versteckter Kanal unter Windows. Unsichtbar für den Explorer und den Befehl `dir`.

```cpp
bool WriteCounterADS(const wchar_t* hostFile, uint64_t counter) {
    // hostFile:streamName syntax
    std::wstring adsPath = std::wstring(hostFile) + L":SysCache.dat";
    HANDLE hFile = CreateFileW(adsPath.c_str(), GENERIC_WRITE, 0, NULL,
                                CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) return false;
    DWORD written;
    uint64_t encrypted = EncryptCounter(counter);
    WriteFile(hFile, &encrypted, sizeof(encrypted), &written, NULL);
    CloseHandle(hFile);
    return written == sizeof(encrypted);
}

bool ReadCounterADS(const wchar_t* hostFile, uint64_t& counter) {
    std::wstring adsPath = std::wstring(hostFile) + L":SysCache.dat";
    HANDLE hFile = CreateFileW(adsPath.c_str(), GENERIC_READ, FILE_SHARE_READ,
                                NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) return false;
    uint64_t encrypted; DWORD read;
    ReadFile(hFile, &encrypted, sizeof(encrypted), &read, NULL);
    CloseHandle(hFile);
    if (read == sizeof(encrypted)) { counter = DecryptCounter(encrypted); return true; }
    return false;
}
```

**ADS-Eigenschaften:**
- Unsichtbar im Explorer (Win10+: `dir /r` zeigt sie an)
- Keine sichtbare Änderung der Dateigröße
- **Beim Kopieren auf FAT32/exFAT gelöscht** (nur NTFS)
- Antivirensoftware KANN sie scannen (MITRE ATT&CK T1564.004)
- Process Monitor sieht Zugriffe auf ADS

**Geeignete Host-Datei:** `%APPDATA%\Microsoft\` oder `%LOCALAPPDATA%\Microsoft\Windows\Caches\`

**Dateisystem-Zeitstempel als verdeckter Speicher:**
```cpp
// Encode counter in file modification timestamp
FILETIME ft;
uint64_t encoded = EncodeCounterAsTimestamp(counter); // 16-bit days fits fine
ft.dwLowDateTime = (DWORD)encoded;
ft.dwHighDateTime = (DWORD)(encoded >> 32);
SetFileTime(hFile, NULL, NULL, &ft);
```

### macOS: Extended Attributes (xattr) {#macos-extended-attributes-xattr}

```cpp
#include <sys/xattr.h>

bool WriteCounterXattr(const char* filePath, uint64_t counter) {
    const char* attrName = "com.apple.metadata.kMDItemFinderComment";
    uint64_t encrypted = EncryptCounter(counter);
    return setxattr(filePath, attrName, &encrypted, sizeof(encrypted), 0, 0) == 0;
}

bool ReadCounterXattr(const char* filePath, uint64_t& counter) {
    uint64_t encrypted;
    ssize_t size = getxattr(filePath, "com.apple.metadata.kMDItemFinderComment",
                            &encrypted, sizeof(encrypted), 0, 0);
    if (size == sizeof(encrypted)) {
        counter = DecryptCounter(encrypted);
        return true;
    }
    return false;
}
```

**xattr überlebt:** App-Deinstallation und Time-Machine-Wiederherstellung. Man hängt sie an das Verzeichnis `~/Library/` oder an systemerzeugte Dateien, die nicht gelöscht werden.

---

## Schicht 4: TPM 2.0 NV-Zähler {#layer-4-tpm-20-nv-counters}

Hardwaregarantierter monotoner Zähler. Er kann auch bei vollem OS-Zugriff nicht dekrementiert werden.

| Eigenschaft | Wert |
|-------------|------|
| Zählergröße | 64-Bit |
| Operationen | Define, Increment, Read (kein Decrement/Write) |
| Min. NV-Speicher | 3834 Byte, >=68 Indizes |
| **Lebenszeit-Schreibvorgänge** | **~100 KB gesamt (!!)** |
| Ratenbegrenzung | `TPM_RC_NV_RATE` bei häufigen Schreibvorgängen |

**Rechnung zum Lebenszeitbudget:** 100 KB / 8 Byte = ~12.500 Schreibvorgänge. Bei 1 Schreibvorgang pro Tag sind das ~34 Jahre. Bei 1 Schreibvorgang pro App-Start und häufig nutzenden Anwendern kann das Budget innerhalb eines Jahres erschöpft sein.

```cpp
#include <tss2/tss2_esys.h>

ESYS_CONTEXT *esysContext;
Esys_Initialize(&esysContext, NULL, NULL);

// Define NV counter space
TPM2B_NV_PUBLIC publicInfo = {
    .nvPublic = {
        .nvIndex = 0x01500000,    // user NV range
        .nameAlg = TPM2_ALG_SHA256,
        .attributes = (
            TPMA_NV_COUNTER |    // increment-only
            TPMA_NV_AUTHWRITE |
            TPMA_NV_AUTHREAD |
            TPMA_NV_NO_DA        // not DA lockout
        ),
        .dataSize = 8,           // 64-bit
    }
};

Esys_NV_DefineSpace(esysContext, ESYS_TR_RH_OWNER,
                    ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
                    &auth, &publicInfo, &nvHandle);

// Increment
Esys_NV_Increment(esysContext, nvHandle, nvHandle,
                  ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE);

// Read
TPM2B_MAX_NV_BUFFER *data;
Esys_NV_Read(esysContext, nvHandle, nvHandle,
             ESYS_TR_PASSWORD, ESYS_TR_NONE, ESYS_TR_NONE,
             8, 0, &data);
```

**TPM-Fazit:**
- Überlebt OS-Neuinstallation und Festplattenformatierung
- Langsam (~100 ms pro Increment)
- Unter macOS kein TPM
- Ein Benutzer mit Adminrechten kann das TPM über Einstellungen > Sicherheit > TPM > TPM löschen zurücksetzen
- Der Dienst TBS (`tbs`) fehlt unter Win11 manchmal trotz TPM-2.0-Hardware. Prüfen mit: `sc query tbs`

---

## Erkennung von Uhr-Rollbacks {#clock-rollback-detection}

### Methode 1: Letzte bekannte Zeit (primär) {#method-1-last-known-time-primary}

```cpp
bool DetectClockRollback() {
    uint64_t lastKnownTime = ReadLastKnownTime(); // from all 4 layers, take max
    uint64_t currentTime = GetCurrentUnixTime();
    if (currentTime < lastKnownTime) return true; // rollback detected
    WriteLastKnownTime(currentTime);
    return false;
}
```

### Methode 2: Mtime einer Sentinel-Datei {#method-2-sentinel-file-mtime}

```cpp
bool DetectRollbackViaFileTimestamps() {
    struct stat st;
    stat(SENTINEL_PATH, &st);
    time_t fileModTime = st.st_mtime;
    time_t currentTime = time(NULL);
    if (fileModTime > currentTime + 3600) return true; // 1h tolerance
    return false;
}
```

### Methode 3: TLS-Zertifikatszeitstempel {#method-3-tls-certificate-timestamps}

Der HTTP-Date-Header jeder HTTPS-Anfrage (Google/Cloudflare-CDN) liefert eine authentifizierte Zeitreferenz. Sie lässt sich schwer fälschen, solange man nicht den Remote-Server kontrolliert.

### Methode 4: Compile-Zeit-Anker {#method-4-compile-time-anchor}

```cpp
constexpr time_t BUILD_TIME = __TIME_UNIX__; // GCC/Clang
bool DetectRollbackVsBuildTime() {
    return time(NULL) < BUILD_TIME;
}
```

### Methode 5: Vergleich mehrerer Quellen {#method-5-multiple-source-comparison}

```cpp
struct TimeSource {
    time_t system_time;
    time_t file_mtime;    // sentinel file
    time_t last_known;    // from storage
    time_t build_time;    // __TIME__
    time_t ntp_time;      // if available
    time_t tls_time;      // from HTTPS header
};

bool IsTimeConsistent(TimeSource& ts) {
    time_t max_known = std::max({ts.last_known, ts.build_time});
    return ts.system_time >= max_known - 86400; // 1-day tolerance
}
```

**Google Roughtime:** authentifiziertes Zeitprotokoll mit Ed25519-Signaturen. MITM ist unmöglich. ~1 s Genauigkeit, das reicht.

---

## Überlebensmatrix {#survival-matrix}

| Speicher | App-Deinstallation | Reiniger (CCleaner) | OS-Neuinstallation | VM-Snapshot-Rollback |
|----------|--------------------|---------------------|--------------------|----------------------|
| Cred Manager (Win) | Überlebt | Überlebt | Gelöscht | Zurückgesetzt |
| Keychain (macOS) | Überlebt | Überlebt | Gelöscht | Zurückgesetzt |
| iCloud Keychain | Überlebt | Überlebt | **Überlebt** | **Überlebt** |
| Registry (getarnte GUID) | Überlebt | Überlebt | Gelöscht | Zurückgesetzt |
| NTFS ADS | Überlebt | Überlebt | Gelöscht | Zurückgesetzt |
| xattr (macOS) | Überlebt | Überlebt | Gelöscht | Zurückgesetzt |
| TPM NV | Überlebt | Überlebt | **Überlebt** | **Überlebt** |
| Server-Backend | Überlebt | Überlebt | Überlebt | Überlebt |

Ein VM-Snapshot-Rollback umgeht alle lokalen Schichten. Nur Server-Backend und TPM bieten echten Schutz.

---

## Adobe-CC-Referenzimplementierung {#adobe-cc-reference-implementation}

Adobe Creative Cloud nutzt genau diesen 4-Schicht-Ansatz:
- Windows Credential Manager (getarnte Schlüssel `Microsoft_Genuine_Preference_*`)
- Registry (`HKCU\Software\Adobe\*` mit verschleierten Wertenamen)
- Dateien (`.operatingconfig` in `%APPDATA%\Adobe\` mit Binärkodierung)
- Adobe-Server (maßgeblich beim nächsten Start der CC-Desktop-App)

**JetBrains-Antimuster (zu vermeiden):**
Die Testzähler von JetBrains verwendeten vorhersehbare Dateinamen und Registry-Pfade. Die Folge waren von der Community gepflegte Reset-Skripte (Löschen der Datei `.ideLicense`, bestimmte Registry-Schlüssel). Das Verschleiern der Speichernamen ist entscheidend. Dateien und Schlüssel dürfen NICHT nach dem eigenen Produkt benannt werden.

## VM-Snapshot-Abwehr {#vm-snapshot-defense}

VM-Snapshots setzen ALLE lokalen Schichten gleichzeitig zurück. Abwehroptionen:

| Schicht | Snapshot-resistent? | Hinweise |
|---------|---------------------|-|
| Credential Manager (Win) | Nein, zurückgesetzt | |
| Keychain (macOS) | Nein, zurückgesetzt | |
| iCloud Keychain | **Ja**, Cloud-Sync überlebt | Erfordert iCloud-Anmeldung des Benutzers |
| NTFS ADS / xattr | Nein, zurückgesetzt | |
| TPM NV-Zähler | **Ja**, Hardware überlebt | TPM-Zustand unabhängig vom Datenträger |
| Server-Backend | **Ja**, außerhalb der VM-Kontrolle | |

Strategie: Server-Synchronisation bei der ersten Nutzung pro Sitzung erzwingen. VM-Snapshot → Offline-Zähler wird zurückgesetzt → App wird für die Server-Verifikation online gezwungen → Server weist den Rollback ab.

## DSGVO-Konformität bei der Zählerspeicherung {#gdpr-compliance-for-counter-storage}

Die Speicherung eines Testzählers an versteckten Orten gilt als berechtigtes Interesse (DSGVO Art. 6 Abs. 1 lit. f), wenn:
1. Der Zweck in der Datenschutzerklärung offengelegt ist
2. Bei einem Löschersuchen (Recht auf Löschung) alle 4 Speicherschichten gelöscht werden
3. Keine personenbezogenen Daten gespeichert werden, nur Gerätezustand bzw. ein Nutzungszähler

Löschendpunkt implementieren: `DELETE /api/device/{fp}` löscht den Server-Zähler. Die Client-App erhält beim ersten Start nach der Löschung vom Server einen neuen Zähler (mit null initialisiert).

## Stolperfallen (Gotchas) {#gotchas}

- **Die Schreiblebensdauer des TPM-NV liegt bei ~12.500 Operationen.** Niemals bei jedem App-Start inkrementieren. Lazy Increment verwenden: nur schreiben, wenn Tages- oder Sitzungsgrenzen überschritten werden.
- **CRED_PERSIST_LOCAL_MACHINE vs. CRED_PERSIST_SESSION:** Sitzungsgebundene Anmeldeinformationen verschwinden beim Abmelden. Für Persistenz immer LOCAL_MACHINE verwenden.
- **ADS werden beim Kopieren auf FAT32/exFAT entfernt.** Nicht auf ADS als primären Speicher verlassen; sie sind eine von 4 Schichten.
- **Das xattr-Verhalten hängt vom Kopierwerkzeug ab.** `cp` erhält sie; viele ZIP-Tools und Cloud-Sync-Dienste nicht. Nicht allein auf xattr verlassen.
- **macOS-Sandbox (App-Store-Apps):** Der Keychain-Zugriff ist app-sandboxed. Bei der Deinstallation werden der Container und seine Keychain-Einträge GELÖSCHT. Bei Apps außerhalb des App Stores überlebt der Keychain die Deinstallation.
- **Der Dienst TBS fehlt unter Win11** trotz vorhandenem TPM 2.0. Den Rückgabecode von `Tbsi_Context_Create` immer prüfen und den Fehlerfall sauber behandeln.
- **Format des Registry-GUID-Schlüssels:** Den Zähler als REG_BINARY speichern, per XOR mit dem Geräte-Fingerabdruck verknüpft, damit der `regedit`-Browser unlesbare Bytes statt einer lesbaren Zahl zeigt.
- **Der Serverzähler ist offline nicht immer verfügbar.** Lokale Schichten müssen für Offline-Zeiten genügend Zustand halten. Den Serverwert nur dann als maßgeblich akzeptieren, wenn die Verbindung bestätigt ist.
- **Vorhersehbare Speichernamen ergeben Massen-Reset-Skripte.** JetBrains hatte von der Community gepflegte Skripte, die Testdateien anhand bekannter Namen löschten. Speicherkennungen immer tarnen.
- **Zählererhöhung bei jedem Start verbraucht die TPM-Lebensdauer.** Bei täglicher Nutzung sind das 365 Inkremente pro Jahr. Bei jedem Start (5×/Tag) sind es 1.825 pro Jahr, das Budget ist also in ~7 Jahren erschöpft. Sitzungsgrenzen statt Startereignisse verwenden.

## Siehe auch {#see-also}
- [[remote-kill-switch]]
- [[licensing-implementation-cpp]]
- [[adobe-piracy-patterns]]
