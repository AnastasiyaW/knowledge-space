---
level: 5
source_sha256: a910e6ea66878fce5f65abbaa0ecb60deb510c24d83d9b35d222165768e88473
translation: machine
translated_at: '2026-10-24'
---
# Architecture de plugins Photoshop pour l'inférence ML {#photoshop-plugin-architecture-for-ml-inference}

Date : 2026-04-03
Contexte : Développement d'un plugin d'inférence ML en C++ multiplateforme (Mac + Windows) pour Photoshop et d'autres éditeurs photo. Couvre les types de plugins, l'intégration d'ONNX Runtime, les schémas IPC et la comparaison de 10 éditeurs.

---

## Types de plugins Photoshop {#photoshop-plugin-types}

### UXP Hybride - CHOIX PRINCIPAL POUR LE ML {#uxp-hybrid-primary-choice-for-ml}

Disponible à partir de PS v24.2.0 (février 2023), considérablement amélioré dans PS 2025 (v26, UXP v8.0).

**Architecture :**
- UXP (JavaScript/HTML pour l'interface) + code natif C++ dans un fichier `.uxpaddon` (renommé .dll/.dylib)
- Communication via une API de style Node.js N-API
- À partir de PS 2025 : **accès au SDK C++ de Photoshop depuis les plugins hybrides**, avec filtres et accès direct aux données de pixels

```php
JavaScript (UXP) <--N-API--> C++ (.uxpaddon)
                                  |
                                  +-- ONNX Runtime
                                  +-- ML inference
                                  +-- Image processing
```

**Capacités :**
- Code C++ arbitraire (ONNX Runtime, ML personnalisé, etc.)
- Interface JavaScript/HTML/CSS via UXP
- À partir de PS 2025 : accès au SDK C++ de PS pour la création de filtres et l'accès aux pixels via le SDK C++
- Publication en un seul paquet via Adobe Marketplace

**Contraintes :**
- Doit prendre en charge TOUTES les plateformes : Mac M1 (arm64), Mac Intel (x86_64), Windows x64
- Windows ARM non pris en charge
- macOS : signature de code et notarisation obligatoires
- Pas de Web Workers ni de POSIX threads dans UXP (le C++ peut créer ses propres threads)
- Minimum : PS v24.2.0, UDT v1.7.0

### UXP (JS uniquement) {#uxp-js-only}

Plateforme de base. Pas de code natif C++. L'inférence ML n'est possible que via un sous-processus ou HTTP. À utiliser uniquement pour des plugins d'interface simples, sans calcul intensif.

### CEP - OBSOLÈTE {#cep-deprecated}

CEP 12 est la dernière mise à jour majeure. Dans PS 2025 (v26), les extensions CEP héritées **n'apparaissent plus dans l'interface**. Sur Apple Silicon sans Rosetta, elles ne fonctionnent pas. Ne pas utiliser pour de nouveaux projets.

### Plugins de filtre C++ (.8bf) - Hérité, toujours pris en charge {#c-filter-plugins-8bf-legacy-still-supported}

- Fichiers : `.8bf` (filtres), `.8ba` (import), `.8be` (export), `.8bi` (formats de fichiers)
- Fonctionne dans le même processus, accès direct aux données de pixels
- Nécessite une ressource PiPL
- Pour Apple Silicon : recompiler en Universal Binary
- **Bonus :** Affinity Photo prend aussi en charge les .8bf 64 bits
- Pas de framework d'interface moderne (Win32/Cocoa uniquement)

### Comparaison des types de plugins {#plugin-type-comparison}

| Critère | UXP Hybride | UXP | .8bf hérité | CEP |
|-----------|-----------|-----|-------------|-----|
| Statut | Actif | Actif | Maintenu | Obsolète |
| Interface | HTML/CSS/JS | HTML/CSS/JS | Win32/Cocoa | HTML/CSS/JS |
| C++ natif | Oui (N-API) | Non | Oui (complet) | Non |
| Inférence ML | Appel C++ direct | Sous-processus/HTTP | Direct | Sous-processus |
| Marketplace | Oui | Oui | Non | Non (obsolète) |
| Apple Silicon | Natif (Universal) | Natif | Recompilation nécessaire | Rosetta uniquement |
| Avenir | À long terme | À long terme | Incertain | Sera supprimé |

---

## Compatibilité des versions {#version-compatibility}

| Fonctionnalité | Version minimale de PS |
|---------------|----------------|
| UXP de base | CC 2021 (v22.0) |
| **Plugins UXP hybrides** | **v24.2.0 (février 2023)** |
| Fonctionnalités UXP v8.0 | PS 2025 (v26.0) |
| SDK C++ de PS depuis un hybride | PS 2025 (v26.0) |
| WebView dans UXP | PS 2025 (v26.0) |
| CEP masqué de l'interface | PS 2025 (v26.0) |

```javascript
// Version detection from plugin
const app = require('photoshop').app;
const psVersion = app.version; // "26.0.0"
const platform = require('os').platform(); // "darwin" or "win32"
```

**Stratégie multiversion :**
```json
// manifest.json
{"host": {"app": "PS", "minVersion": "24.2.0"}}
```
Détecter la présence du SDK C++ de PS ; à défaut, revenir à l'API d'imagerie JS.

---

## Options de communication avec le code natif {#native-code-communication-options}

### N-API (plugin hybride) - Recommandé {#n-api-hybrid-plugin-recommended}

```php
JS (UXP) <--N-API--> C++ (.uxpaddon)
```

Appels directs de fonctions C++ depuis JS. Transmission d'ArrayBuffer/TypedArrays pour les données de pixels. Appels synchrones et asynchrones. Le C++ peut lancer ses propres threads pour les calculs lourds.

```cpp
// Thread-safe callback from worker thread back to JS
napi_call_threadsafe_function(tsfn, data, napi_tsfn_blocking);
```

### WebAssembly {#webassembly}

Le C/C++/Rust compilé s'exécute dans UXP. Pas de compilation distincte par plateforme.
Performance : environ 45 à 55 % plus lent que le natif (recherche USENIX). Pas d'accès au GPU. PS 2025 présente des bugs de plantage avec WASM.

### Sous-processus (démon hors processus) {#subprocess-out-of-process-daemon}

```php
JS (UXP) <--HTTP/WebSocket--> External Process (C++)
```

Isolation complète, espace d'adressage propre, accès complet au GPU. Modèle utilisé par tous les grands plugins ML (Topaz, plugins Stable Diffusion). Surcoût IPC pour le transfert de grandes images.

---

## Schémas d'architecture de processus {#process-architecture-patterns}

### Schéma A : Dans le processus (UXP Hybride) {#pattern-a-in-process-uxp-hybrid}

```php
[Photoshop Process]
  |
  +-- [UXP JS] <--N-API--> [C++ .uxpaddon]
                                  |
                                  +-- ONNX Runtime (CPU)
                                  +-- Image processing
```

Avantages : latence minimale, espace d'adressage partagé, paquet unique.
Inconvénients : un crash C++ = un crash de PS. Mémoire limitée au processus PS. Le GPU peut entrer en conflit avec l'utilisation de PS.

### Schéma B : Démon hors processus {#pattern-b-out-of-process-daemon}

```bash
[Photoshop Process]               [ML Daemon Process]
  |                                     |
  +-- [UXP Plugin] <--localhost HTTP--> [HTTP Server]
                                             |
                                             +-- ONNX Runtime + GPU
                                             +-- Models in memory
```

Avantages : isolation complète des crashs, espace d'adressage propre, contrôle total du GPU, partageable entre PS, LR et l'application autonome.
Inconvénients : surcoût IPC, gestion du cycle de vie, le pare-feu peut bloquer localhost.

### Schéma C : Hybride - RECOMMANDÉ POUR LE ML {#pattern-c-hybrid-recommended-for-ml}

```bash
[Photoshop]
  |
  +-- [UXP Hybrid Plugin]
        |
        +-- [C++ .uxpaddon] -- light ops (resize, color convert, pixel transfer)
        |       |
        |       +-- IPC to daemon
        |
        +-- [ML Daemon] -- heavy GPU inference
                |
                +-- ONNX Runtime + GPU
                +-- Models in memory between calls
```

N-API pour le transfert de pixels + sous-processus pour l'inférence GPU.

### Schéma réel (Topaz, Nik, Luminar) {#real-world-pattern-topaz-nik-luminar}

```text
[Photoshop/LR Filter Call]
     |
     v
[.8bf / UXP Plugin]
     |
     +-- [Standalone Application]  ← same C++ codebase
          |
          +-- ML inference engine
          |
     [Returns result as new layer]
```

Tous les grands plugins ML commerciaux utilisent ce schéma : application autonome + intégration PS/LR.

---

## Mécanismes IPC {#ipc-mechanisms}

| Méthode | Latence | Débit | Complexité | Accès GPU |
|--------|---------|------------|-----------|------------|
| N-API (hybride) | Faible | Élevé | Moyenne | Via C++ |
| WASM | Faible | Moyen | Faible | Aucun |
| HTTP localhost | Moyenne | Moyen | Moyenne | Complet |
| Named Pipes | Faible | Élevé | Élevée | Complet |
| Mémoire partagée | Minimale | Maximal | Élevée | Complet |
| gRPC | Moyenne | Élevé | Moyenne | Complet |

**Recommandations :**
- Modèles légers (<100 Mo, CPU) : N-API hybride - latence minimale
- Modèles lourds (GPU) : démon en sous-processus + HTTP/WebSocket localhost - isolation + GPU complet
- Images 4K/8K : mémoire partagée (zéro copie) + mmap

```cpp
// IPC method selection by platform
#ifdef _WIN32
    // Named pipe: \\.\pipe\my-ml-plugin
    HANDLE hPipe = CreateNamedPipeW(L"\\\\.\\pipe\\my-ml-plugin", ...);
#else
    // Unix domain socket: /tmp/my-ml-plugin.sock
    int sock = socket(AF_UNIX, SOCK_STREAM, 0);
#endif
```

---

## Intégration d'ONNX Runtime {#onnx-runtime-integration}

### Execution Providers {#execution-providers}

| Provider | Plateforme | GPU | Remarques |
|----------|---------|-----|-------|
| **DirectML** | Windows | Tous (AMD/Intel/NVIDIA/Qualcomm) | DX12, compatibilité maximale |
| **CoreML** | macOS/iOS | Neural Engine d'Apple + GPU | Utilise l'ANE sur les puces M |
| **CUDA** | Win/Linux | NVIDIA uniquement | Performance NVIDIA maximale |
| **CPU** | Toutes | - | Repli toujours disponible |
| **TensorRT** | Win/Linux | NVIDIA | Inférence optimisée |

**Stratégie recommandée :**
```yaml
Windows: DirectML → CPU fallback
macOS:   CoreML  → CPU fallback
```

DirectML fonctionne avec TOUT GPU DX12, sans installation de CUDA.
CoreML utilise l'ANE sur les puces M : meilleures performances sur le matériel Apple.

```cpp
#include <onnxruntime_cxx_api.h>

Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "MLPlugin");
Ort::SessionOptions session_options;

#ifdef _WIN32
    OrtSessionOptionsAppendExecutionProvider_DML(session_options, 0);
#elif __APPLE__
    OrtSessionOptionsAppendExecutionProvider_CoreML(session_options, 0);
#endif
// CPU fallback is automatic

// Load from memory buffer (no plaintext model on disk)
Ort::Session session(env,
    model_bytes.data(), model_bytes.size(),  // in-memory load
    session_options);
```

### Gestion de la mémoire pour les grandes images {#memory-management-for-large-images}

Tailles des tampons d'image (RGBA float32) :
- 2K (2048×2048) : ~64 Mo
- 4K (4096×4096) : ~256 Mo
- 8K (8192×8192) : ~1 Go
- 12K (12000×12000) : ~2,2 Go

Stratégies :
1. **Découpage en tuiles :** tuiles de 512×512 ou 1024×1024 avec recouvrement pour des jonctions sans couture
2. **Fichiers mappés en mémoire :** mmap pour les données dépassant la RAM
3. **Demi-précision (fp16) :** moitié moins de mémoire pour l'inférence
4. **Chargement progressif :** chargement à la demande

### Sécurité des threads {#thread-safety}

```sql
JS: call startInference(imageData, callback)
 |
 +-> C++ (N-API): receive data, create worker thread
       |
       +-> Worker thread: ML inference (1-30 seconds)
             |
             +-> threadsafe callback: return result to JS
                   |
                   +-> JS: update UI, write result to PS
```

**Règles :**
- NE JAMAIS bloquer le thread d'interface de Photoshop
- Utiliser des workers asynchrones N-API pour les opérations lourdes
- Le C++ dans .uxpaddon PEUT créer ses propres threads
- Callbacks vers JS : uniquement depuis le thread principal, via `napi_call_threadsafe_function`

---

## Adobe Marketplace {#adobe-marketplace}

### Exigences de publication {#publishing-requirements}
- Profil d'éditeur dans Adobe Developer Console (une seule fois)
- Validation par Adobe avant publication
- **Obligatoire : prise en charge de TOUTES les plateformes** (Mac M1, Mac Intel, Windows x64)
- macOS : certificat Apple Developer et notarisation obligatoires
- manifest.json correct avec les permissions

### Partage des revenus {#revenue-share}
- Avant août 2025 : 90 % pour le développeur / 10 % pour Adobe
- À partir du 1er août 2025 : 87,4 % pour le développeur / 12,6 % pour Adobe
- Exemple : plugin à 5,00 $ → le développeur reçoit 4,37 $

### Distribution directe (sans Marketplace) {#direct-distribution-no-marketplace}
Installation du fichier `.ccx` via Creative Cloud Desktop ou UDT. Pas de validation par Adobe, pas de partage des revenus. À utiliser lorsqu'on dispose d'un système de licences personnalisé, d'un contrôle des prix, et qu'aucune découverte via la marketplace n'est nécessaire.

---

## Intégration Lightroom {#lightroom-integration}

### Lightroom Classic - SDK Lua {#lightroom-classic-lua-sdk}

**Langage :** Lua (interpréteur embarqué). Version du SDK : 8.0.

Capacités du SDK : destinations d'export/publication, métadonnées personnalisées, éléments de menu, interface via LrDialogs/LrView, HTTP via LrHttp, hooks de post-traitement, réglages du module Développement.

**Limitations par rapport à Photoshop :**

| Capacité | LR Classic | PS UXP |
|-----------|-----------|-------|
| Édition au niveau des pixels | Non | Oui |
| C++ natif | Non (Lua uniquement) | Oui (Hybride) |
| Inférence GPU | Non | Oui (via C++) |
| Éditeur externe | Oui (aller-retour) | N/A |

**Protocole d'éditeur externe (principale voie ML pour LR) :**
1. LR envoie la photo à un éditeur externe (TIFF/PSD)
2. L'application externe traite l'image (votre application autonome avec backend ML)
3. Le fichier revient dans le catalogue LR

C'est ainsi que Topaz Photo AI, Nik Collection et Luminar Neo fonctionnent dans LR.

### Base de code partagée PS + LR {#shared-codebase-ps-lr}

```bash
C++ backend ──── common (core ML inference)
                      |
           ┌──────────┴──────────┐
    PS frontend              LR frontend
    (UXP Hybrid Plugin)      (Lua plugin → calls standalone)
    (.uxpaddon calls backend)  (External Editor protocol)
                      |
              Standalone App
              (same C++ backend + own GUI via Qt/Dear ImGui)
```

### Lightroom CC (Cloud) {#lightroom-cc-cloud}

**Ne prend PAS en charge les plugins tiers.** Aucun SDK, aucune API. La communauté le demande depuis 2021. En avril 2026, la situation n'a pas changé. La seule voie d'intégration consiste à passer par un aller-retour avec Photoshop.

---

## Autres éditeurs photo {#other-photo-editors}

| Éditeur | SDK de plugins | C++ natif | Approche recommandée | Marché |
|--------|-----------|-----------|---------------------|--------|
| **Photoshop** | UXP Hybride | Oui (N-API) | Plugin UXP Hybride | ~33 % (leader) |
| **Lightroom Classic** | SDK Lua | Non | Éditeur externe + application autonome | Significatif |
| **Lightroom CC** | Aucun | - | Non pris en charge | En croissance |
| **Capture One** | Limité | Non | Éditeur externe | Top 10 |
| **Affinity Photo** | .8bf uniquement | Oui (.8bf) | Filtre .8bf | En croissance |
| **GIMP** | Complet (3.0+) | Oui (plugins C) | Plugin C | ~10 % |
| **DxO PhotoLab** | Aucun | - | Éditeur externe | Niche |
| **Darktable** | Lua | Non | Lua + processus externe | En croissance (Linux) |
| **Pixelmator Pro** | Core Image | Non (Swift) | Core Image Unit | macOS uniquement |
| **Luminar Neo** | Aucun | - | Non pris en charge | En croissance |
| **ON1 Photo RAW** | Aucun | - | Non pris en charge | Niche |

**Remarques clés :**
- **Affinity Photo** prend en charge les .8bf 64 bits : compatibilité gratuite si vous compilez déjà des .8bf pour PS
- **GIMP 3.0** (2025) : réécriture majeure ; les anciens plugins doivent être portés. Un plugin C + ONNX Runtime fonctionne.
- **API AppleScript de Capture One** : macOS uniquement. Pas d'API de script sous Windows.
- **Pixelmator Pro** : macOS uniquement ; les Core Image Units sont des filtres du framework Apple

---

## Outillage de développement {#development-tooling}

**Bolt UXP** (github.com/hyperbrew/bolt-uxp) : modèle de départ React/Svelte/Vue + TypeScript + Vite. Rechargement à chaud.

**UDT (UXP Developer Tool) :** outil de débogage officiel d'Adobe pour les plugins UXP. Version minimale 1.7.0 pour les plugins hybrides.

**Implémentations de référence :**
- `AdobeDocs/photoshop-cpp-sdk` - SDK C++ officiel de PS
- `tpl-photoshop-plugin` (javier-games) - modèle de plugin C++ pour PS avec le SDK Adobe 2024
- `WasmUXP` (michelerenzullo) - WebAssembly dans les plugins UXP
- Auto-Photoshop-StableDiffusion-Plugin - exemple open source : UXP + HTTP localhost vers un backend ML

---

## Pièges à éviter {#gotchas}

- **UXP Hybride != plugin C++ .8bf de Photoshop.** L'hybride utilise le pont N-API JS↔C++. Depuis PS 2025, on peut aussi appeler le SDK C++ de PS depuis l'addon hybride, mais ce sont deux points d'entrée distincts.
- **Une prise en charge partielle des plateformes est refusée par Adobe Marketplace.** Vous devez prendre en charge Mac M1, Mac Intel ET Windows x64. Windows ARM n'est pas encore exigé, mais attendez-vous à ce qu'il le soit lors des prochaines validations.
- **Les extensions CEP n'apparaissent plus dans l'interface de PS 2025**, même si elles sont installées. Les utilisateurs de PS 2025+ ne les verront pas. Tout plugin CEP actif doit migrer vers UXP.
- **`CreateSessionFromArray` dans ONNX Runtime** charge le modèle depuis un tampon en RAM : essentiel pour charger un .hmod chiffré sans écrire les poids déchiffrés sur le disque.
- **DirectML ne prend pas en charge tous les opérateurs ONNX.** Testez votre modèle spécifique. Repliez-vous sur le CPU pour les opérateurs non pris en charge, ou utilisez `OrtSessionOptionsSetExecutionMode` pour partitionner le graphe.
- **Le pare-feu peut bloquer localhost** dans les environnements d'entreprise restreints. La mémoire partagée ou les named pipes évitent ce problème pour la communication avec un démon hors processus.
- **Protection contre les crashs dans le processus :** si l'addon C++ plante, Photoshop plante avec lui. Utilisez un démon hors processus pour l'inférence lourde. N-API convient uniquement au transfert rapide de pixels.
- **UXP ne dispose ni de Web Workers ni de POSIX threads.** Tout le multithreading des tâches lourdes doit se trouver en C++ (.uxpaddon), avec des threads de la plateforme, et les résultats renvoyés via le callback thread-safe de N-API.
- **Lightroom CC n'a aucune prise en charge des plugins.** N'investissez pas dans une intégration LR CC tant qu'Adobe n'ajoute pas de SDK.
- **La notarisation macOS est obligatoire** pour tout plugin distribué en dehors du Mac App Store. Cela implique un certificat Developer ID signé par Apple, une soumission au service de notarisation d'Apple et le « stapling ». Sans cela, Gatekeeper bloque le plugin sur les versions récentes de macOS.
