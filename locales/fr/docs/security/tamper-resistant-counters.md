---
level: 4
source_sha256: bb68a26417ef43baec838bab6bd61d65ef85052d2b177c42954f41dece77d280
translation: machine
translated_at: '2026-10-24'
---
# Compteurs monotones résistants à la falsification pour applications de bureau {#tamper-resistant-monotonic-counters-for-desktop-apps}

Date : 2026-04-03
Contexte : C++, Windows + macOS. Protection de la période d'essai par un compteur à incrémentation seule. 4 couches de stockage ; valeur actuelle = max() des quatre.

---

## Architecture : stockage en 4 couches {#architecture-4-layer-storage}

```bash
Layer 1: OS credential store (Windows Credential Manager / macOS Keychain)
Layer 2: Registry (Windows) / plist + xattr (macOS) - disguised
Layer 3: Hidden file + NTFS ADS (Windows) / extended attributes (macOS)
Layer 4: Server backend (source of truth)

Current counter = max(layer1, layer2, layer3, layer4)
```

La perte d'une couche isolée n'est pas critique. L'attaquant doit contourner les quatre simultanément.

---

## Couche 1 : magasin d'identifiants du système d'exploitation {#layer-1-os-credential-store}

### Gestionnaire d'identifiants Windows {#windows-credential-manager}

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

**Limites :** blob maximal de 2560 octets (Win7+). CRED_PERSIST_LOCAL_MACHINE = survit à la session d'ouverture de session.

**Vulnérabilités :**
- Visible dans Panneau de configuration > Gestionnaire d'identifiants > Identifiants génériques
- `cmdkey /delete:TargetName` le supprime
- Les autres applications du même utilisateur peuvent lire et écrire (pas d'isolation entre applications)
- Stocké sous forme de fichiers .vcrd chiffrés dans `%LOCALAPPDATA%\Microsoft\Vault\` via DPAPI

**Atténuation :** stocker la valeur chiffrée et un HMAC afin que le blob brut ne révèle pas qu'il s'agit d'un compteur.

### Trousseau macOS {#macos-keychain}

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

**Matrice de survie du trousseau :**

| Stockage | Désinstallation de l'application | « Réinitialiser les réglages » | Réinstallation de l'OS |
|---------|---------------|------------------|--------------|
| ~/Library/Preferences/*.plist | Survit (macOS) | Supprimé | Supprimé |
| Entrée de trousseau | Survit | Survit | Supprimé |
| Synchronisation iCloud Keychain | Survit | Survit | **Survit (!)**|
| xattr sur ~/Library/ | Survit | Survit | Supprimé |

**Vulnérabilités macOS :** `Keychain Access.app` affiche tous les mots de passe génériques. `security find-generic-password -s "ServiceName"` et `security delete-generic-password` fonctionnent en ligne de commande.

**Secure Enclave sur Apple Silicon :** le SE ne stocke que des clés privées P256. Contournement :
1. Créer une clé liée au SE avec `kSecAttrTokenIDSecureEnclave`
2. Signer `{counter_value, device_id, timestamp}` avec la clé SE (ECDSA)
3. Stocker la structure signée dans le trousseau
4. À la lecture : vérifier la signature SE. Signature invalide = falsification détectée
5. La clé est liée à l'appareil (non exportable). Nouveau Mac = nouvelle clé, la couche serveur assure la récupération.

Remarque : les verrous de tentatives du SE (8 bits, 8 bits de tentatives maximales) ne sont **pas accessibles** via l'API publique ; ils ne servent qu'à la protection par code d'accès.

---

## Couche 2 : registre / plist dissimulé {#layer-2-disguised-registry-plist}

### Emplacements cachés du registre Windows {#windows-registry-hidden-locations}

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

**Ce que suppriment les nettoyeurs de registre :**

| Catégorie | CCleaner | Revo Uninstaller |
|----------|----------|------------------|
| HKCU\Software\{AppName} | Oui (après désinstallation) | Oui (agressif) |
| CLSID COM orphelins | Partiellement | Partiellement |
| GUID aléatoire dans des sous-clés système | **Non** | **Non** |
| HKCU\Software\Microsoft\* | **Non** (trop risqué) | **Non** |

---

## Couche 3 : fichiers cachés {#layer-3-hidden-files}

### Windows : flux de données alternatifs NTFS (ADS) {#windows-ntfs-alternate-data-streams-ads}

Le canal caché le plus robuste sous Windows, invisible pour l'Explorateur et la commande `dir`.

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

**Propriétés des ADS :**
- Invisibles dans l'Explorateur (Win10+ : `dir /r` les affiche)
- Aucune modification visible de la taille du fichier
- **Supprimés lors de la copie vers FAT32/exFAT** : NTFS uniquement
- L'antivirus PEUT les analyser (MITRE ATT&CK T1564.004)
- Process Monitor voit les accès aux ADS

**Fichier hôte à privilégier :** `%APPDATA%\Microsoft\` ou `%LOCALAPPDATA%\Microsoft\Windows\Caches\`

**Horodatages du système de fichiers comme stockage couvert :**
```cpp
// Encode counter in file modification timestamp
FILETIME ft;
uint64_t encoded = EncodeCounterAsTimestamp(counter); // 16-bit days fits fine
ft.dwLowDateTime = (DWORD)encoded;
ft.dwHighDateTime = (DWORD)(encoded >> 32);
SetFileTime(hFile, NULL, NULL, &ft);
```

### macOS : attributs étendus (xattr) {#macos-extended-attributes-xattr}

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

**Les xattr survivent :** à la désinstallation de l'application et à la restauration Time Machine. Les rattacher au répertoire `~/Library/` ou à des fichiers créés par le système qui ne seront pas supprimés.

---

## Couche 4 : compteurs NV TPM 2.0 {#layer-4-tpm-20-nv-counters}

Compteur monotone garanti par le matériel. Il ne peut pas être décrémenté, même avec un accès complet au système d'exploitation.

| Propriété | Valeur |
|----------|-------|
| Taille du compteur | 64 bits |
| Opérations | Define, Increment, Read (pas de Decrement/Write) |
| Mémoire NV minimale | 3834 octets, >=68 index |
| **Écritures à vie** | **~100 Ko au total (!!)** |
| Limitation de débit | `TPM_RC_NV_RATE` en cas d'écritures à haute fréquence |

**Calcul du budget à vie :** 100 Ko / 8 octets = ~12 500 écritures. À 1 écriture par jour : ~34 ans. À 1 écriture par lancement d'application chez des utilisateurs fréquents : épuisement possible en un an.

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

**Verdict sur le TPM :**
- Survit à la réinstallation de l'OS et au formatage du disque
- Lent (~100 ms par incrément)
- Pas de TPM sur macOS
- Un utilisateur disposant des droits d'administrateur peut effacer le TPM via Paramètres > Sécurité > TPM > Effacer le TPM
- Le service TBS (`tbs`) est parfois absent sur Win11 malgré un matériel TPM 2.0. Vérifier : `sc query tbs`

---

## Détection de retour arrière de l'horloge {#clock-rollback-detection}

### Méthode 1 : dernière heure connue (principale) {#method-1-last-known-time-primary}

```cpp
bool DetectClockRollback() {
    uint64_t lastKnownTime = ReadLastKnownTime(); // from all 4 layers, take max
    uint64_t currentTime = GetCurrentUnixTime();
    if (currentTime < lastKnownTime) return true; // rollback detected
    WriteLastKnownTime(currentTime);
    return false;
}
```

### Méthode 2 : mtime d'un fichier sentinelle {#method-2-sentinel-file-mtime}

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

### Méthode 3 : horodatages des certificats TLS {#method-3-tls-certificate-timestamps}

L'en-tête HTTP Date de toute requête HTTPS (CDN Google/Cloudflare) fournit une référence temporelle authentifiée. Difficile à falsifier sans contrôler le serveur distant.

### Méthode 4 : ancrage à la compilation {#method-4-compile-time-anchor}

```cpp
constexpr time_t BUILD_TIME = __TIME_UNIX__; // GCC/Clang
bool DetectRollbackVsBuildTime() {
    return time(NULL) < BUILD_TIME;
}
```

### Méthode 5 : comparaison de plusieurs sources {#method-5-multiple-source-comparison}

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

**Google Roughtime :** protocole de temps authentifié avec signatures Ed25519. Attaque de type MITM impossible. Précision d'environ 1 s, suffisante.

---

## Matrice de survie {#survival-matrix}

| Stockage | Désinstallation de l'application | Nettoyeur (CCleaner) | Réinstallation de l'OS | Retour à un instantané de VM |
|---------|--------------|-------------------|--------------|----------------------|
| Gestionnaire d'identifiants (Win) | Survit | Survit | Supprimé | Restauré à l'ancienne valeur |
| Trousseau (macOS) | Survit | Survit | Supprimé | Restauré à l'ancienne valeur |
| iCloud Keychain | Survit | Survit | **Survit** | **Survit** |
| Registre (GUID dissimulé) | Survit | Survit | Supprimé | Restauré à l'ancienne valeur |
| ADS NTFS | Survit | Survit | Supprimé | Restauré à l'ancienne valeur |
| xattr (macOS) | Survit | Survit | Supprimé | Restauré à l'ancienne valeur |
| TPM NV | Survit | Survit | **Survit** | **Survit** |
| Backend serveur | Survit | Survit | Survit | Survit |

Le retour à un instantané de VM contourne toutes les couches locales. Le backend serveur et le TPM sont la seule défense réelle.

---

## Implémentation de référence : Adobe CC {#adobe-cc-reference-implementation}

Adobe Creative Cloud utilise exactement cette approche en 4 couches :
- Gestionnaire d'identifiants Windows (clés dissimulées `Microsoft_Genuine_Preference_*`)
- Registre (`HKCU\Software\Adobe\*` avec noms de valeurs obfusqués)
- Fichiers (`.operatingconfig` dans `%APPDATA%\Adobe\` avec encodage binaire)
- Serveurs Adobe (faisant autorité au prochain lancement de CC Desktop App)

**Antimodèle JetBrains (à éviter) :**
Les compteurs d'essai de JetBrains utilisaient des noms de fichiers et des chemins de registre prévisibles, ce qui a donné naissance à des scripts de réinitialisation maintenus par la communauté (suppression du fichier `.ideLicense`, clés de registre spécifiques). Obfusquer les noms de stockage est essentiel. Ne JAMAIS nommer les fichiers ou clés d'après votre produit.

## Défense contre les instantanés de VM {#vm-snapshot-defense}

Les instantanés de VM restaurent TOUTES les couches locales simultanément. Options de défense :

| Couche | Résistante aux instantanés ? | Remarques |
|-------|--------------------|-|
| Gestionnaire d'identifiants (Win) | Non : restaurée | |
| Trousseau (macOS) | Non : restauré | |
| iCloud Keychain | **Oui** : la synchronisation cloud survit | Nécessite une connexion iCloud de l'utilisateur |
| ADS NTFS / xattr | Non : restaurés | |
| Compteur NV TPM | **Oui** : le matériel survit | L'état du TPM est indépendant du disque |
| Backend serveur | **Oui** : hors de contrôle de la VM | |

Stratégie : exiger une synchronisation serveur lors de la première utilisation de chaque session. Instantané de VM → réinitialisation hors ligne du compteur → l'application est forcée en ligne pour la vérification serveur → le serveur rejette le retour en arrière.

## Conformité RGPD pour le stockage du compteur {#gdpr-compliance-for-counter-storage}

Le stockage d'un compteur d'essai dans des emplacements cachés relève de l'intérêt légitime (RGPD, art. 6, par. 1, point f) lorsque :
1. La finalité est divulguée dans la politique de confidentialité
2. En cas de demande d'effacement, les 4 couches de stockage doivent être supprimées
3. Aucune donnée personnelle n'est stockée, uniquement l'état de l'appareil ou un compteur d'usage

Implémenter un point de terminaison d'effacement : `DELETE /api/device/{fp}` supprime le compteur serveur. Après effacement, l'application cliente reçoit au premier lancement un compteur neuf depuis le serveur (initialisé à zéro).

## Pièges {#gotchas}

- **L'écriture NV du TPM est limitée à environ 12 500 opérations.** Ne jamais incrémenter à chaque lancement de l'application. Utiliser un incrément paresseux : n'écrire que lors du franchissement d'une limite de jour ou de session.
- **CRED_PERSIST_LOCAL_MACHINE vs CRED_PERSIST_SESSION** : les identifiants limités à la session disparaissent à la déconnexion. Toujours utiliser LOCAL_MACHINE pour la persistance.
- **Les ADS sont supprimés lors d'une copie vers FAT32/exFAT.** Ne pas s'appuyer sur les ADS pour le stockage principal ; les utiliser comme l'une des 4 couches.
- **Le comportement des xattr dépend de l'outil de copie.** `cp` les conserve ; de nombreux outils de compression et de synchronisation cloud ne le font pas. Ne pas s'appuyer uniquement sur les xattr.
- **Sandbox macOS (applications du Mac App Store) :** l'accès au trousseau est isolé par application ; lors de la désinstallation, le conteneur et ses entrées de trousseau SONT supprimés. Pour les applications hors App Store, le trousseau survit à la désinstallation.
- **Service TBS absent sur Win11** malgré la présence d'un TPM 2.0. Toujours vérifier le code de retour de `Tbsi_Context_Create` et gérer l'erreur proprement.
- **Format de clé GUID du registre :** stocker le compteur en REG_BINARY, combiné par XOR à l'empreinte de la machine, afin que le navigateur `regedit` affiche des octets illisibles plutôt qu'un nombre lisible.
- **Le compteur serveur n'est pas toujours disponible hors ligne.** Les couches locales doivent contenir un état suffisant pour les périodes hors ligne. N'accepter la valeur serveur comme faisant autorité que lorsque la connectivité est confirmée.
- **Des noms de stockage prévisibles entraînent des scripts de réinitialisation de masse.** JetBrains a subi des scripts communautaires supprimant leurs fichiers d'essai par nom connu. Toujours dissimuler les identifiants de stockage.
- **Incrémenter le compteur à chaque lancement consomme la durée de vie du TPM.** À usage quotidien : 365 incréments par an. À chaque lancement (5 fois par jour) : 1 825 par an, soit un épuisement en environ 7 ans. Utiliser les limites de session plutôt que les événements de lancement.

## Voir aussi {#see-also}
- [[remote-kill-switch]]
- [[licensing-implementation-cpp]]
- [[adobe-piracy-patterns]]
