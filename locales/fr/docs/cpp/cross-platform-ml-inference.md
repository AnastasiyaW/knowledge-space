---
title: "C++ multiplateforme pour l'inférence ML"
category: reference
tags: [cpp, cross-platform, onnx-runtime, directml, coreml, metal, windows, macos, apple-silicon, ml-inference]
aliases: ["Mac vs Windows ML", "Cross-Platform ONNX"]
level: 4
source_sha256: b3282f5d497c9689a178e074c4d4a2c3cdd7da58e39e027d3c487d67c7ff20ea
translation: machine
translated_at: '2026-10-24'
---
# C++ multiplateforme pour l'inférence ML {#cross-platform-c-for-ml-inference}

Référence pour le développement d'applications de bureau C++ avec inférence ML ciblant à la fois Windows et macOS. Couvre les Execution Providers ONNX Runtime, les différences entre API GPU, les particularités du système de fichiers, la configuration du système de build et le déploiement.

## Panorama des API GPU {#gpu-api-landscape}

| API | Windows | macOS |
|-----|---------|-------|
| DirectX 12 / DirectML | Principale pour le ML | N/A |
| Metal | N/A | API GPU principale |
| CoreML | N/A | Framework ML (GPU + Neural Engine) |
| CUDA | NVIDIA uniquement | N/A (Apple a retiré NVIDIA) |
| Vulkan | Natif | Via MoltenVK (plus lent que Metal natif) |
| OpenCL | NVIDIA/AMD/Intel | Déprécié depuis macOS 10.14 |
| OpenGL | Ancien | Déprécié, figé à 4.1 |

## Sélection des Execution Providers ONNX Runtime {#onnx-runtime-execution-provider-selection}

```cpp
Ort::SessionOptions session_options;

#ifdef _WIN32
  // Windows: CUDA > DirectML > CPU
  try {
    OrtCUDAProviderOptions cuda_opts{};
    session_options.AppendExecutionProvider_CUDA(cuda_opts);
  } catch (...) {
    OrtSessionOptionsAppendExecutionProvider_DML(session_options, 0);
  }
#elif defined(__APPLE__)
  // macOS: CoreML > CPU
  uint32_t coreml_flags = COREML_FLAG_ENABLE_ON_SUBGRAPH;
  OrtSessionOptionsAppendExecutionProvider_CoreML(session_options, coreml_flags);
#endif
```

**DirectML** : fonctionne avec tout GPU DX12 (NVIDIA, AMD, Intel). Un seul binaire pour tous les fabricants. En mode maintenance (2026) : stable, sans nouvelles fonctionnalités. Bascule sur la mémoire système partagée lorsque la VRAM est épuisée.

**CoreML** : utilise le GPU Metal et le Neural Engine sur Apple Silicon. Le Neural Engine est optimal pour les CNN, tandis que le GPU via Metal est plus rapide pour l'inférence de transformers. Doit être enregistré explicitement à la création de la session.

## Spécificités Apple Silicon {#apple-silicon-specifics}

```text
Unified Memory Architecture:
  - CPU and GPU share the SAME physical memory
  - No data copying between CPU/GPU - pointer passing
  - No separate VRAM - ML model and app share all RAM
  - Bandwidth: 200-800 GB/s (vs 32 GB/s PCIe 4.0)

Neural Engine:
  - Accessible ONLY through CoreML (no low-level API)
  - Optimal for: quantized models, convolutions, matrix ops
  - NOT optimal for: arbitrary compute, custom operators
  - CNN inference: NE faster; Transformer inference: Metal GPU faster

M1 8GB: ~5-6 GB available for ML (OS + apps take the rest)
```

**Retrait de Rosetta 2** : Apple a annoncé son retrait dans macOS 28 (2027). Un build natif arm64 est obligatoire.

## Différences de système de fichiers {#filesystem-differences}

| Aspect | Windows | macOS |
|--------|---------|-------|
| Séparateur de chemin | `\` (mais `/` fonctionne dans la plupart des API) | `/` |
| Longueur max. du chemin | 260 caractères (32 767 avec le préfixe `\\?\`) | Pas de limite stricte |
| Sensibilité à la casse | Non (par défaut NTFS) | Non (par défaut APFS) |
| Verrouillage de fichiers | **Obligatoire** (impossible de supprimer des fichiers ouverts) | **Consultatif** (suppression de fichiers ouverts possible) |
| Données d'application | `%APPDATA%` | `~/Library/Application Support/` |
| Cache | `%LOCALAPPDATA%\Temp\` | `~/Library/Caches/` |
| Configuration | `%APPDATA%` | `~/Library/Preferences/` |

```cpp
// Always use std::filesystem::path - handles separators automatically
namespace fs = std::filesystem;
fs::path config = get_app_data_dir() / "MyApp" / "config.json";
// NEVER concatenate strings with "/" or "\\"
```

**Correctif MAX_PATH** : activer `longPathAware` dans le manifeste de l'application, ou utiliser le préfixe `\\?\` pour l'API Win32. `std::filesystem` gère cela automatiquement avec les SDK récents.

**Bibliothèque** : [PlatformFolders](https://github.com/sago007/PlatformFolders) abstrait les répertoires standard de manière multiplateforme.

## Chargement des DLL/dylib {#dlldylib-loading}

**Ordre de recherche Windows** : répertoire de l'EXE > System32 > répertoire Windows > CWD (dangereux !) > PATH. Correctif : `SetDllDirectory("")` retire le CWD de la recherche.

**Recherche macOS** : `@executable_path` > `@loader_path` > `@rpath` > `DYLD_LIBRARY_PATH` (désactivé avec le Hardened Runtime !). Utiliser `@rpath` et le définir via CMake :

```cmake
set_target_properties(target PROPERTIES
    INSTALL_RPATH "@executable_path/../Frameworks")
```

## Signature de code et distribution {#code-signing-and-distribution}

**Windows (Authenticode + SmartScreen) :**

- Certificat OV ou EV (environ 200 à 600 $/an)
- Un certificat EV ne donne plus une confiance SmartScreen immédiate (depuis août 2024)
- SmartScreen construit sa réputation au fil du temps : les nouveaux éditeurs reçoivent toujours des avertissements
- Azure Trusted Signing disponible pour les États-Unis et le Canada (depuis octobre 2025)

**macOS (codesign + notarisation + Gatekeeper) :**

- Developer ID via l'Apple Developer Program (99 $/an)
- Hardened Runtime **obligatoire** pour la notarisation
- Notarisation : envoi à Apple pour une analyse automatisée, réception d'un ticket
- Sans notarisation, l'application **ne se lance pas** (macOS 10.15+)
- Le Hardened Runtime bloque l'injection `DYLD_INSERT_LIBRARIES` et désactive la surcharge d'ASLR

## Système de build (CMake) {#build-system-cmake}

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyMLApp LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

if(WIN32)
    add_definitions(-DUNICODE -D_UNICODE)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
elseif(APPLE)
    set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64")  # Universal Binary
    set(CMAKE_OSX_DEPLOYMENT_TARGET "13.0")
endif()

find_package(onnxruntime REQUIRED)
target_link_libraries(myapp PRIVATE onnxruntime::onnxruntime)

if(WIN32)
    target_link_libraries(myapp PRIVATE DirectML)
elseif(APPLE)
    target_link_libraries(myapp PRIVATE
        "-framework CoreML" "-framework Metal" "-framework Foundation")
endif()
```

**Pièges des Universal Binary** : toutes les dépendances doivent également être universelles. Utiliser `lipo` pour combiner des bibliothèques mono-architecture. Vérifier qu'ONNX Runtime fournit un build universel de son API C.

## Différences entre compilateurs {#compiler-differences}

| Aspect | MSVC (Windows) | Apple Clang (macOS) |
|--------|----------------|---------------------|
| ABI C++ | ABI Microsoft | ABI Itanium |
| Bibliothèque standard | Microsoft STL | libc++ (LLVM) |
| Avertissements | `/W4` | `-Wall -Wextra` |
| Sanitizers | ASan | ASan, UBSan, TSan |
| Gestion des exceptions | SEH | DWARF/zero-cost |
| Symboles de débogage | PDB | dSYM (DWARF) |

**Édition de liens** : statique pour les dépendances C++ (onnxruntime, curl), dynamique pour les frameworks système et le runtime GPU (CUDA, DirectML, CoreML).

## Gestion de l'Unicode {#unicode-handling}

```cpp
// Internal: UTF-8 everywhere (std::string)
// Windows API boundary: convert to UTF-16
#ifdef _WIN32
std::wstring utf8_to_wide(const std::string& utf8) {
    int len = MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, nullptr, 0);
    std::wstring wide(len - 1, 0);
    MultiByteToWideChar(CP_UTF8, 0, utf8.c_str(), -1, &wide[0], len);
    return wide;
}
// Use wide API: CreateFileW, LoadLibraryW
#endif
```

`wchar_t` fait 2 octets sous Windows (UTF-16) et 4 octets sous macOS (UTF-32). **Ne jamais transférer de `wstring` entre plateformes via IPC ou fichiers.**

Bibliothèque : [Boost.Nowide](https://www.boost.org/libs/nowide/) - E/S compatibles UTF-8 sous Windows.

## Stockage des identifiants {#credential-storage}

| Aspect | Windows | macOS |
|--------|---------|-------|
| Système | DPAPI + Credential Manager | Keychain Services |
| ACL par élément | Non - toute application du même utilisateur peut lire | Oui - demande de confirmation lors d'un accès par une application tierce |
| API | `CredWrite`/`CredRead` | `SecItemAdd`/`SecItemCopyMatching` |

Bibliothèque : [keychain](https://github.com/hrantzsch/keychain) - abstraction C++ multiplateforme.

## Réseau (libcurl) {#networking-libcurl}

Utiliser libcurl avec le **backend TLS natif** de chaque plateforme :

- **Windows** : libcurl + Schannel - utilise le magasin de certificats Windows
- **macOS** : libcurl + Secure Transport (ou OpenSSL avec une autorité de certification intégrée)

Cela permet à l'inspection SSL des proxys d'entreprise de fonctionner de manière transparente. En cas d'utilisation de l'épinglage de certificats, prévoir un repli sur le magasin système en cas d'échec de vérification.

## Mise à jour automatique {#auto-update}

| Composant | Windows | macOS |
|-----------|---------|-------|
| Framework | WinSparkle (portage de Sparkle) | Sparkle |
| Fichier de mise à jour | Appcast XML | Appcast XML |
| Redémarrage | Processus d'assistance nécessaire (verrouillage obligatoire) | Mise à jour en place possible |

## Rapports de plantage {#crash-reporting}

**Crashpad** (Google, multiplateforme) + **Sentry** (SaaS) :

```bash
# Windows: upload PDB
sentry-cli debug-files upload --include-sources ./build/Release/*.pdb

# macOS: upload dSYM
sentry-cli debug-files upload --include-sources ./build/Release/*.dSYM
```

## Programmes d'installation {#installers}

| Plateforme | Recommandé | Remarques |
|------------|------------|-----------|
| Windows | WiX (MSI) ou NSIS (EXE) | MSI pour le déploiement GPO en entreprise |
| macOS | DMG avec glisser-déposer vers Applications | pkg dans le DMG si des composants système sont nécessaires |

## Pièges multiplateformes {#cross-platform-pitfalls}

| Piège | Détails |
|-------|---------|
| Fins de ligne | CR+LF (Win) vs LF (Mac). `std::getline` laisse un `\r` résiduel en fin de ligne |
| Précision de Sleep | `Sleep(1)` = 15,6 ms sous Windows sans `timeBeginPeriod(1)` |
| Séparateur décimal (locale) | `atof("1.5")` peut être interprété comme 1 dans une locale non-C. Forcer `setlocale(LC_NUMERIC, "C")` |
| Fermer la fenêtre != quitter | macOS : fermer la dernière fenêtre ne quitte PAS l'application |
| Attributs de quarantaine | Les fichiers téléchargés reçoivent une marque de quarantaine : Zone.Identifier (Win) / com.apple.quarantine (Mac) |

## Matrice de tests (minimale) {#testing-matrix-minimum}

| OS | Architecture | GPU | Priorité |
|----|-------------|-----|----------|
| Windows 10 22H2 | x64 | NVIDIA (CUDA+DirectML) | Principale |
| Windows 10 22H2 | x64 | AMD (DirectML) | Secondaire |
| Windows 10 22H2 | x64 | Intel iGPU (DirectML) | Cas limite |
| Windows 11 24H2 | x64 | NVIDIA | Principale |
| macOS 14+ | arm64 (M1-M4) | CoreML/Metal | Mac principal |
| macOS 14+ | x86_64 (Intel) | CPU | Ancien |

**Cas de test critiques** : premier lancement (SmartScreen/Gatekeeper), repli gracieux en cas de OOM GPU, unicode dans les chemins utilisateur (cyrillique), reprise GPU après veille/réveil, sélection de plusieurs GPU (dGPU vs iGPU sous Windows).

## Pièges à éviter {#gotchas}

- **Verrouillage obligatoire vs consultatif** : sous Windows, il est impossible de mettre à jour une DLL ou un modèle pendant qu'il est chargé. Solutions : fermer le fichier, le mettre à jour puis le rouvrir, ou effectuer une mise à jour échelonnée avec renommage au redémarrage. macOS autorise le remplacement, mais le processus conserve l'ancien inode jusqu'à la fermeture
- **DirectML est en mode maintenance (2026)** : API stable, sans nouvelles fonctionnalités. Adapté à la production, mais aucune amélioration de performance n'est à prévoir
- **Les applications Apple Silicon doivent être natives arm64** : le retrait de Rosetta 2 dans macOS 28 (2027) signifie que les binaires x86_64 uniquement cesseront de fonctionner. Construire un Universal Binary dès maintenant
- **La conversion CoreML peut entraîner une perte de précision** : tous les opérateurs ONNX ne sont pas pris en charge par CoreML. Certains modèles nécessitent l'Execution Provider CoreML d'ONNX Runtime comme solution de repli au lieu d'une conversion directe vers CoreML
- **La taille du buffer SSO de `std::string` diffère** : la STL de MSVC et libc++ ont des implémentations différentes de l'optimisation des petites chaînes. Ne jamais supposer la disposition binaire de `std::string` d'une plateforme à l'autre

## Voir aussi {#see-also}

- [[cmake-build-systems]] - Modèles de configuration CMake
- [Concurrence - Threads, Async, Atomics](concurrency.md) - différences de threading selon les plateformes
- [Gestion des erreurs - Exceptions et alternatives](error-handling.md) - gestion des exceptions selon les compilateurs
- [[low-vram-inference-strategies]] - techniques d'optimisation de la mémoire GPU
