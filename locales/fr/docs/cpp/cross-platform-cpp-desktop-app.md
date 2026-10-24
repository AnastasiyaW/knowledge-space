---
level: 4
source_sha256: 4b779a2b8093160a248d164c83b55535a948b3e0461a681be4786f070a3cfab2
translation: machine
translated_at: '2026-10-24'
---
# Application C++ de bureau multiplateforme (Mac + Windows) {#cross-platform-c-desktop-application-mac-windows}

Référence des différences de plateforme pour la création d'applications de bureau C++ (avec inférence ML) destinées à Windows et macOS. Couvre le système de fichiers, le GPU, la sécurité, le système de build et le déploiement.

Voir [[cross-platform-ml-inference]] pour la sélection des execution providers d'ONNX Runtime.

## Différences du système de fichiers {#filesystem-differences}

### Répertoires standard des applications {#standard-app-directories}

| Usage | Windows | macOS |
|-------|---------|-------|
| Données utilisateur | `%APPDATA%` (`AppData\Roaming`) | `~/Library/Application Support/` |
| Cache local | `%LOCALAPPDATA%` | `~/Library/Caches/` |
| Fichiers temporaires | `%TEMP%` | `$TMPDIR` (`/var/folders/.../T/`) |
| Préférences | `%APPDATA%` (identique aux données) | `~/Library/Preferences/` |
| Journaux | `%LOCALAPPDATA%\MyApp\Logs` (aucun standard) | `~/Library/Logs/` |
| Installation | `C:\Program Files\` | `/Applications/` |

Utilisez `std::filesystem::path` : il gère automatiquement les séparateurs sur les deux plateformes.

### Comportement du verrouillage de fichiers {#file-locking-behavior}

| Aspect | Windows | macOS |
|--------|---------|-------|
| Type de verrou | **Obligatoire** : les autres processus ne peuvent pas ouvrir un fichier verrouillé | **Consultatif** : les autres processus peuvent ignorer le verrou |
| Supprimer un fichier ouvert | Impossible (fichier utilisé) | Possible (sémantique unlink d'Unix) |
| Renommer un fichier ouvert | Impossible | Possible |

Le verrouillage obligatoire de Windows complique les mises à jour automatiques : il faut un processus d'aide ou une mise à jour différée (écriture dans un fichier temporaire, puis renommage au lancement suivant).

### Attributs étendus / quarantaine {#extended-attributes-quarantine}

| Plateforme | Mécanisme | Indicateur de quarantaine |
|------------|-----------|---------------------------|
| Windows (NTFS) | Alternate Data Streams : `file.txt:Zone.Identifier` | `Zone.Id=3` |
| macOS (APFS) | xattr : `com.apple.quarantine` | Défini sur les fichiers téléchargés |

Les fichiers téléchargés (modèles, programmes de mise à jour) possèdent des attributs de quarantaine. Sur macOS, ceux-ci déclenchent Gatekeeper ; sous Windows, ils déclenchent SmartScreen.

### Limites de chemin {#path-limits}

- **Windows** : `MAX_PATH=260` par défaut. Activez les chemins longs via `longPathAware` dans le manifeste de l'application. `std::filesystem` utilise en interne le préfixe `\\?\`.
- **macOS** : pas de limite stricte (`PATH_MAX=1024` à titre indicatif).

## Signature de code {#code-signing}

### Windows (Authenticode + SmartScreen) {#windows-authenticode-smartscreen}

- Nécessite un certificat Authenticode (OV ou EV), environ 200 à 600 $ par an
- SmartScreen accumule une réputation au fil du temps : même les applications signées d'un nouvel éditeur affichent un avertissement
- Azure Trusted Signing disponible depuis octobre 2025 (États-Unis/Canada)

### macOS (Developer ID + notarisation) {#macos-developer-id-notarization}

**Obligatoire** pour une distribution en dehors du Mac App Store :

1. Signer le code avec le certificat Developer ID Application (99 $ par an)
2. Notariser : envoyer le binaire à Apple et récupérer le ticket
3. Agrafer : `xcrun stapler staple MyApp.app` — intègre le ticket pour une vérification Gatekeeper hors ligne

**Hardened Runtime** requis pour la notarisation :

```bash
# Entitlements for ML plugin:
com.apple.security.network.client           # for license checks
com.apple.security.files.user-selected.read-write  # for image import
com.apple.security.cs.allow-unsigned-executable-memory  # for GPU compute
```

Sans notarisation, l'application **ne se lancera pas** sur macOS 10.15 et versions ultérieures.

**Avantage anti-débogage** : Hardened Runtime désactive l'injection via `DYLD_INSERT_LIBRARIES` et interdit la désactivation de l'ASLR, ce qui constitue une protection intégrée contre la falsification.

## APIs GPU {#gpu-apis}

| API | Windows | macOS |
|-----|---------|-------|
| DirectX 12 / DirectML | API ML principale | N/A |
| Metal | N/A | API GPU principale |
| CoreML | N/A | Framework ML (GPU + Neural Engine) |
| CUDA | NVIDIA uniquement | N/A (Apple a abandonné NVIDIA) |
| Vulkan | Natif | Via MoltenVK (plus lent que Metal natif) |
| OpenCL | Support legacy | Déprécié depuis 10.14 |

### Apple Silicon : Neural Engine {#apple-silicon-neural-engine}

Accessible **uniquement via CoreML**, sans API bas niveau. Adapté aux CNN et aux modèles quantifiés. L'inférence de transformers est plus rapide sur le GPU Metal que sur le Neural Engine. La mémoire unifiée supprime le surcoût de copie CPU↔GPU : un modèle chargé en RAM est immédiatement accessible au GPU.

**Note de performance MoltenVK** : Metal natif surpasse MoltenVK sur GPU Apple, comme le confirment les benchmarks de llama.cpp. Utilisez MoltenVK uniquement lorsque macOS est une cible secondaire.

## Système de build {#build-system}

### Différences de compilateur {#compiler-differences}

| Aspect | MSVC (Windows) | Apple Clang (macOS) |
|--------|----------------|---------------------|
| ABI C++ | ABI Microsoft | ABI Itanium |
| Bibliothèque standard | MSVC STL | libc++ |
| C++20 | Complet (VS 2022 17.x) | Complet |
| Sanitizers | ASan | ASan, UBSan, TSan |

La disposition de `std::string` diffère (taille différente du tampon SSO). `wchar_t` fait 2 octets (UTF-16) sous Windows et 4 octets (UTF-32) sous macOS : ne sérialisez jamais de `wstring` entre plateformes.

### Configuration CMake multiplateforme {#cmake-cross-platform-setup}

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyMLApp LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

if(WIN32)
    add_definitions(-DUNICODE -D_UNICODE)
    # Static runtime: simpler deployment, avoids VC++ redist requirement
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
elseif(APPLE)
    # Universal Binary: supports Intel + Apple Silicon in one file
    set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64")
    set(CMAKE_OSX_DEPLOYMENT_TARGET "13.0")
endif()

find_package(onnxruntime REQUIRED)
target_link_libraries(myapp PRIVATE onnxruntime::onnxruntime)

if(WIN32)
    target_link_libraries(myapp PRIVATE DirectML)
elseif(APPLE)
    target_link_libraries(myapp PRIVATE
        "-framework CoreML" "-framework Metal" "-framework Foundation"
    )
endif()
```

### Binaire universel (macOS) {#universal-binary-macos}

Un seul binaire contenant `arm64` et `x86_64`. Toutes les dépendances doivent également être universelles.

```bash
# Combine separate arch builds:
lipo -create arm64/libfoo.dylib x86_64/libfoo.dylib -output libfoo.dylib
```

**Suppression de Rosetta 2** : Apple a annoncé sa suppression dans macOS 28 (2027). Un build `arm64` natif est obligatoire, et non facultatif.

### Ordre de recherche des DLL/dylib {#dlldylib-search-order}

**Recherche des DLL Windows** (simplifiée) :
1. Répertoire de l'EXE
2. System32
3. Répertoire de travail courant (**dangereux** : détournement de DLL)
4. Entrées du PATH

Atténuation : `SetDllDirectory("")` retire le répertoire courant de la recherche.

**Les dylib macOS** utilisent `@rpath` :

```cmake
set_target_properties(target PROPERTIES
    INSTALL_RPATH "@executable_path/../Frameworks"
)
```

## Gestion de l'Unicode {#unicode-handling}

**Différence essentielle** : l'API Windows utilise UTF-16, tandis que macOS/POSIX utilise UTF-8.

```cpp
// Keep all internal strings as UTF-8 (std::string)
// Convert at Windows API boundary:
#ifdef _WIN32
std::wstring utf8_to_wide(const std::string& utf8) {
    int len = MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, nullptr, 0);
    std::wstring wide(len - 1, 0);
    MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, &wide[0], len);
    return wide;
}
// Use wide API variants: CreateFileW, LoadLibraryW, etc.
#endif
```

Utilisez Boost.Nowide pour gérer de manière transparente l'UTF-8 sous Windows (`std::fstream`, `std::cout`).

## Sécurité / stockage des identifiants {#security-credential-storage}

| Plateforme | API | Remarques |
|------------|-----|-----------|
| Windows | DPAPI + Gestionnaire d'identifiants (`CredWrite`/`CredRead`) | Toute application du même utilisateur peut lire les données : pas d'ACL par élément |
| macOS | Trousseau (`SecItemAdd`/`SecItemCopyMatching`) | ACL par élément, demande de confirmation en cas d'accès par une application tierce |

Wrapper multiplateforme : la bibliothèque C++ `keychain` (GitHub : hrantzsch/keychain) abstrait les deux.

**Pour les clés de licence** : stockez-les via l'API d'identifiants de la plateforme et chiffrez en plus les données (défense en profondeur).

## Installation / distribution {#installation-distribution}

### Formats d'installateur {#installer-formats}

**Windows :**

| Format | Cas d'usage |
|--------|-------------|
| WiX (MSI) | Déploiement en entreprise / GPO : les services IT préfèrent MSI |
| NSIS / Inno Setup | Installateur EXE plus simple, large adoption |
| MSIX | Sandbox moderne, mise à jour automatique, nécessite un certificat |

**macOS :**
- Un DMG avec glisser-déposer vers Applications correspond aux attentes des utilisateurs
- `.pkg` dans le DMG si un placement de fichiers au niveau système est nécessaire

### Mise à jour automatique {#auto-update}

| Composant | Windows | macOS |
|-----------|---------|-------|
| Framework | WinSparkle | Sparkle |
| Format | Appcast XML | Appcast XML |
| Vérification de signature | Authenticode | codesign Apple |
| Redémarrage | Nécessite un processus d'aide (verrouillage obligatoire) | Mise à jour en place possible |

### Rapports de plantage : Crashpad + Sentry {#crash-reporting-crashpad-sentry}

Crashpad (Google, open source) gère la capture des plantages sur les deux plateformes. Sentry accepte les Minidump + PDB/dSYM pour la symbolication :

```bash
# CI: upload debug symbols
sentry-cli debug-files upload --include-sources ./build/Release/*.pdb    # Windows
sentry-cli debug-files upload --include-sources ./build/Release/*.dSYM   # macOS
```

## Matrice de tests {#testing-matrix}

### Matrice minimale {#minimum-matrix}

| OS | Architecture | GPU | Priorité |
|----|--------------|-----|----------|
| Windows 10 22H2 | x64 | NVIDIA (CUDA + DirectML) | P0 |
| Windows 10 22H2 | x64 | AMD (DirectML uniquement) | P0 |
| Windows 10 22H2 | x64 | iGPU Intel (DirectML) | P1 |
| Windows 11 24H2 | x64 | NVIDIA | P1 |
| macOS 14 Sonoma | arm64 (M1-M3) | GPU Apple (CoreML) | P0 |
| macOS 15 Sequoia | arm64 (M1-M4) | GPU Apple | P1 |
| macOS 14 Sonoma | x86_64 Intel | GPU AMD/Intel | P2 |

### Cas de test critiques par plateforme {#platform-specific-critical-test-cases}

| Test | Windows | macOS |
|------|---------|-------|
| Premier lancement | Avertissement SmartScreen | Gatekeeper + vérification de l'xattr de quarantaine |
| Inférence GPU | Repli sur DirectML si pas de CUDA | CoreML + Neural Engine vs CPU |
| OOM VRAM | OOM DirectML → repli sur CPU | Mémoire unifiée : pas d'OOM, mais swap |
| Installateur | Chemins longs (nom d'utilisateur cyrillique = cas limite) | DMG glisser-déposer vers Applications ; vérification de la notarisation |
| Mise à jour | Processus d'aide pour le remplacement des fichiers | Remplacement de fichiers en place OK |
| Proxy d'entreprise | Inspection SSL via le magasin de certificats Windows | Inspection SSL via le Trousseau système |
| Veille / reprise | Périphérique GPU perdu à la reprise | Périphérique Metal préservé |

## Résumé : référence rapide des plateformes {#summary-platform-quick-reference}

| Composant | Windows | macOS Intel | macOS Apple Silicon |
|-----------|---------|-------------|---------------------|
| Inférence GPU | CUDA ou DirectML | CPU uniquement | CoreML + Neural Engine |
| Signature de code | Authenticode | Developer ID + notarisation | Developer ID + notarisation |
| Verrouillage de fichiers | Obligatoire | Consultatif | Consultatif |
| Unicode | API en UTF-16 à la frontière | UTF-8 partout | UTF-8 partout |
| Installateur | MSI / NSIS / MSIX | DMG + pkg | DMG (binaire universel) |
| Symboles de plantage | PDB + WER/Crashpad | dSYM + Crashpad | dSYM + Crashpad |
| Mise à jour automatique | WinSparkle | Sparkle | Sparkle |
| Stockage des identifiants | DPAPI / Gestionnaire d'identifiants | Trousseau | Trousseau + Secure Enclave |
| Bibliothèque standard C++ | MSVC STL | libc++ | libc++ |
| ARM natif | Minimal (Win ARM est de niche) | N/A | **Obligatoire** (Rosetta supprimé en 2027) |

## Pièges à éviter {#gotchas}

- **Le verrouillage obligatoire de Windows bloque la mise à jour automatique** : les fichiers DLL et de modèles ne peuvent pas être remplacés pendant leur chargement. Schéma à adopter : écrire dans un fichier temporaire `*.new`, puis le renommer au lancement suivant via un processus d'aide. Sans cela, des erreurs « fichier utilisé » surviennent pendant la mise à jour.
- **Suppression de Rosetta 2 en 2027 sous macOS** : un build `arm64` natif pour Apple Silicon est obligatoire. Les applications livrées uniquement en x86_64 via Rosetta cesseront de fonctionner. Le binaire universel (`x86_64;arm64`) constitue la valeur par défaut sûre.
- **Différence de taille de `wchar_t`** : 2 octets sous Windows (UTF-16), 4 octets sous macOS (UTF-32). Ne sérialisez jamais `std::wstring` dans des fichiers ou des canaux IPC destinés à un usage multiplateforme. Conservez les chaînes internes en `std::string` (UTF-8) et convertissez-les aux frontières des API.
- **Délai de réputation de SmartScreen sous Windows** : même un binaire correctement signé, émis par un nouvel éditeur, affiche « Windows a protégé votre PC » pendant des semaines, voire des mois, jusqu'à ce que le nombre de téléchargements construise la réputation. Les certificats EV accordaient autrefois une réputation immédiate ; depuis août 2024, Microsoft a aligné OV et EV.
- **macOS sans notarisation = application impossible à lancer** : `xcrun notarytool` et `xcrun stapler` sont des étapes obligatoires du pipeline de publication pour macOS 10.15 et versions ultérieures. Les applications non agrafées échouent également sur les machines sans accès Internet (Gatekeeper ne peut pas vérifier en ligne).
- **`Sleep(1)` sous Windows = environ 15,6 ms** : la résolution du minuteur Windows est par défaut de 15,6 ms. Appelez `timeBeginPeriod(1)` pour obtenir une résolution d'environ 1 ms, mais cela augmente la consommation électrique à l'échelle du système. Utilisez `std::this_thread::sleep_for`, qui s'appuie sur QPC et hérite donc de la même résolution.
- **Bug de séparateur décimal lié à la locale** : `atof("1.5")` renvoie 1 lorsque la locale système utilise la virgule comme séparateur décimal. Appelez toujours `setlocale(LC_NUMERIC, "C")` ou `std::locale::global(std::locale::classic())` avant tout parsing numérique.
- **Extensions CEP supprimées dans PS 2025** : Photoshop 2025 (v26) n'affiche plus les extensions CEP héritées dans l'interface. Apple Silicon n'a jamais pris en charge CEP (nécessite Rosetta). Les nouveaux plugins doivent utiliser UXP ou UXP Hybrid.

## Voir aussi {#see-also}

- [[cross-platform-ml-inference]] - Sélection des execution providers d'ONNX Runtime (DirectML, CoreML, CUDA)
- [[photoshop-plugin-architecture]] - Plugin UXP Hybrid, `.uxpaddon` en C++, SDK Lightroom
