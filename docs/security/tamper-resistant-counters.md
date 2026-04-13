# Tamper-Resistant Monotonic Counters for Desktop Apps

Date: 2026-04-03
Context: C++, Windows + macOS. Trial period protection via increment-only counter. 4 storage layers; current value = max() of all four.

---

## Architecture: 4-Layer Storage

```
Layer 1: OS credential store (Windows Credential Manager / macOS Keychain)
Layer 2: Registry (Windows) / plist + xattr (macOS) - disguised
Layer 3: Hidden file + NTFS ADS (Windows) / extended attributes (macOS)
Layer 4: Server backend (source of truth)

Current counter = max(layer1, layer2, layer3, layer4)
```

Loss of any single layer is non-critical. Attacker must defeat all four simultaneously.

---

## Layer 1: OS Credential Store

### Windows Credential Manager

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

**Limits:** Max blob 2560 bytes (Win7+). CRED_PERSIST_LOCAL_MACHINE = survives logon session.

**Vulnerabilities:**
- Visible in Control Panel > Credential Manager > Generic Credentials
- `cmdkey /delete:TargetName` removes it
- Other apps of same user can read/write (no inter-app isolation)
- Stored as encrypted .vcrd files in `%LOCALAPPDATA%\Microsoft\Vault\` via DPAPI

**Mitigation:** Store encrypted value + HMAC so raw blob doesn't reveal it's a counter.

### macOS Keychain

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

**Keychain survival matrix:**

| Storage | App Uninstall | "Reset Settings" | OS Reinstall |
|---------|---------------|------------------|--------------|
| ~/Library/Preferences/*.plist | Survives (macOS) | Deleted | Deleted |
| Keychain entry | Survives | Survives | Deleted |
| iCloud Keychain sync | Survives | Survives | **Survives (!)**|
| xattr on ~/Library/ | Survives | Survives | Deleted |

**macOS vulnerabilities:** `Keychain Access.app` shows all generic passwords. `security find-generic-password -s "ServiceName"` / `security delete-generic-password` work from CLI.

**Secure Enclave on Apple Silicon:** SE stores only P256 private keys. Workaround:
1. Create SE-bound key with `kSecAttrTokenIDSecureEnclave`
2. Sign `{counter_value, device_id, timestamp}` with SE key (ECDSA)
3. Store signed struct in Keychain
4. On read: verify SE signature. Invalid signature = tamper detected
5. Key is device-bound (non-exportable). New Mac = new key, server layer recovers.

Note: SE counter lockboxes (8-bit, 8-bit max attempts) are **not accessible** via public API - used only for passcode protection.

---

## Layer 2: Disguised Registry / Plist

### Windows Registry Hidden Locations

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

**What registry cleaners delete:**

| Category | CCleaner | Revo Uninstaller |
|----------|----------|------------------|
| HKCU\Software\{AppName} | Yes (post-uninstall) | Yes (aggressive) |
| Orphaned COM CLSID | Partial | Partial |
| Random GUID in system subkeys | **No** | **No** |
| HKCU\Software\Microsoft\* | **No** (too risky) | **No** |

---

## Layer 3: Hidden Files

### Windows: NTFS Alternate Data Streams (ADS)

Strongest hidden channel on Windows - invisible to Explorer and `dir` command.

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

**ADS properties:**
- Invisible in Explorer (Win10+: `dir /r` shows them)
- No file size change visible
- **Deleted on FAT32/exFAT copy** - NTFS only
- Antivirus CAN scan (MITRE ATT&CK T1564.004)
- Process Monitor sees ADS access

**Best host file:** `%APPDATA%\Microsoft\` or `%LOCALAPPDATA%\Microsoft\Windows\Caches\`

**Filesystem timestamps as covert storage:**
```cpp
// Encode counter in file modification timestamp
FILETIME ft;
uint64_t encoded = EncodeCounterAsTimestamp(counter); // 16-bit days fits fine
ft.dwLowDateTime = (DWORD)encoded;
ft.dwHighDateTime = (DWORD)(encoded >> 32);
SetFileTime(hFile, NULL, NULL, &ft);
```

### macOS: Extended Attributes (xattr)

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

**xattr survives:** app uninstall, Time Machine restore. Attach to `~/Library/` directory or system-created files that won't be deleted.

---

## Layer 4: TPM 2.0 NV Counters

Hardware-guaranteed monotonic counter. Cannot decrement even with full OS access.

| Property | Value |
|----------|-------|
| Counter size | 64-bit |
| Operations | Define, Increment, Read (no Decrement/Write) |
| Min NV memory | 3834 bytes, >=68 indexes |
| **Lifetime writes** | **~100KB total (!!)** |
| Rate limiting | `TPM_RC_NV_RATE` on high-frequency writes |

**Lifetime budget math:** 100KB / 8 bytes = ~12,500 writes. At 1 write/day = ~34 years. At 1 write/app launch with frequent users = may exhaust in a year.

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

**TPM verdict:**
- Survives OS reinstall and disk format
- Slow (~100ms per increment)
- No TPM on macOS
- User with admin rights can clear TPM via Settings > Security > TPM > Clear TPM
- TBS service (`tbs`) sometimes missing on Win11 despite TPM 2.0 hardware. Check: `sc query tbs`

---

## Clock Rollback Detection

### Method 1: Last Known Time (Primary)

```cpp
bool DetectClockRollback() {
    uint64_t lastKnownTime = ReadLastKnownTime(); // from all 4 layers, take max
    uint64_t currentTime = GetCurrentUnixTime();
    if (currentTime < lastKnownTime) return true; // rollback detected
    WriteLastKnownTime(currentTime);
    return false;
}
```

### Method 2: Sentinel File mtime

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

### Method 3: TLS Certificate Timestamps

HTTP Date header from any HTTPS request (Google/Cloudflare CDN) provides authenticated time reference. Hard to fake without controlling the remote server.

### Method 4: Compile-Time Anchor

```cpp
constexpr time_t BUILD_TIME = __TIME_UNIX__; // GCC/Clang
bool DetectRollbackVsBuildTime() {
    return time(NULL) < BUILD_TIME;
}
```

### Method 5: Multiple Source Comparison

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

**Google Roughtime:** authenticated time protocol with Ed25519 signatures. MITM impossible. ~1s accuracy - sufficient.

---

## Survival Matrix

| Storage | App Uninstall | Cleaner (CCleaner) | OS Reinstall | VM Snapshot Rollback |
|---------|--------------|-------------------|--------------|----------------------|
| Cred Manager (Win) | Survives | Survives | Deleted | Rolled back |
| Keychain (macOS) | Survives | Survives | Deleted | Rolled back |
| iCloud Keychain | Survives | Survives | **Survives** | **Survives** |
| Registry (disguised GUID) | Survives | Survives | Deleted | Rolled back |
| NTFS ADS | Survives | Survives | Deleted | Rolled back |
| xattr (macOS) | Survives | Survives | Deleted | Rolled back |
| TPM NV | Survives | Survives | **Survives** | **Survives** |
| Server backend | Survives | Survives | Survives | Survives |

VM snapshot rollback defeats all local layers. Server backend + TPM are only real defense.

---

## Gotchas

- **TPM NV write lifetime is ~12,500 operations.** Never increment on every app launch. Use lazy increment: write only when crossing day/session boundaries.
- **CRED_PERSIST_LOCAL_MACHINE vs CRED_PERSIST_SESSION** - session-scoped credentials disappear at logoff. Always use LOCAL_MACHINE for persistence.
- **ADS are stripped on FAT32/exFAT copy.** Don't rely on ADS for the primary storage; use as one of 4 layers.
- **xattr behavior varies by copy tool.** `cp` preserves; many zip tools and cloud sync don't. Don't rely solely on xattr.
- **macOS sandbox (App Store apps):** Keychain access is app-sandboxed; on uninstall the container and its Keychain entries ARE deleted. For non-App-Store apps, Keychain survives uninstall.
- **TBS service missing on Win11** despite TPM 2.0 present. Always check `Tbsi_Context_Create` return code and handle gracefully.
- **Registry GUID key format:** store counter as REG_BINARY XOR'd with machine fingerprint so `regedit` browser shows unrecognizable bytes, not a readable number.
- **Server counter is not always available offline.** Local layers must hold sufficient state for offline periods. Accept server value as authoritative only when connectivity is confirmed.
