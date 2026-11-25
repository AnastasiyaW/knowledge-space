---
level: 3
source_sha256: a254ce52685284720377d33e06206b473dac563a93d86929524eb446bc316827
translation: machine
translated_at: '2026-10-24'
---
# Système de build de conteneurs ComfyUI {#comfyui-container-build-system}

Modèles pour construire des images Docker ComfyUI de qualité production : résolution des conflits distutils, découpage des couches pour l'efficacité du cache, montages de cache pip BuildKit, builds multi-étapes et sélection de Flash Attention à l'exécution.

## Stack de build {#build-stack}

- **Image de base :** `nvidia/cuda:13.0.0-runtime-ubuntu22.04`
- **Python :** 3.12 via le PPA deadsnakes
- **PyTorch :** wheels cu130 depuis pytorch.org
- **Nœuds personnalisés :** `nodes.txt` avec des hashes de commit épinglés
- **Registre :** GHCR (`ghcr.io/org/comfyui`)
- **Runner de build :** GitHub Actions → VM éphémère (cx43, volume de 200 Go)

## Correctif du conflit distutils {#distutils-conflict-fix}

**Symptôme :**
```yaml
error: uninstall-distutils-installed-package
× Cannot uninstall blinker 1.4
╰─> It is a distutils installed project...
```

**Cause racine :** Ubuntu 22.04 installe via apt les paquets Python 3.10 avec des métadonnées distutils héritées (sans fichier `RECORD`). Lorsque pip tente de mettre à niveau ces paquets (par exemple `blinker>=1.9`, tiré de façon transitive), il ne peut pas supprimer l'ancienne version.

**Correctif — retirer `python3-pip` d'apt et amorcer via `ensurepip` :**

```dockerfile
FROM nvidia/cuda:13.0.0-runtime-ubuntu22.04

# Install Python 3.12 WITHOUT python3-pip (avoids system python3-* packages)
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    build-essential \
    # DO NOT install python3-pip — it pulls distutils-managed packages
    && rm -rf /var/lib/apt/lists/*

# Bootstrap pip cleanly via ensurepip
RUN python3.12 -m ensurepip --upgrade

# Defense in depth: remove known conflicting distutils packages if present
RUN dpkg -l python3-blinker python3-yaml 2>/dev/null | grep ^ii && \
    apt-get purge -y python3-blinker python3-yaml || true
```

**Complétez cette liste** dans `CONFLICTS.md` au fur et à mesure que de nouveaux conflits distutils apparaissent.

## Découpage en couches : stable/volatile {#layer-split-stablevolatile}

Un `nodes.txt` unique regroupant tous les nœuds personnalisés signifie que toute mise à jour d'un pin invalide la couche entière (reconstruction de plus de 10 minutes).

```text
nodes-stable.txt   ← core utilities, model loaders (change rarely)
nodes-volatile.txt ← custom/frequently-updated nodes
```

```dockerfile
# Stable nodes — cached layer, rarely invalidated
COPY nodes-stable.txt /tmp/nodes-stable.txt
COPY scripts/install_nodes.sh /tmp/install_nodes.sh
RUN cp /tmp/nodes-stable.txt /tmp/nodes.txt && /tmp/install_nodes.sh

# Volatile nodes — only this layer rebuilds on pin updates
COPY nodes-volatile.txt /tmp/nodes-volatile.txt
RUN cp /tmp/nodes-volatile.txt /tmp/nodes.txt && /tmp/install_nodes.sh
```

**Gain attendu :** reconstruction de 5 à 7 min au lieu de 15 min après la modification du pin d'un seul nœud.

## Montage de cache pip BuildKit {#buildkit-pip-cache-mount}

Sans montages de cache, chaque échec de cache impose le téléchargement complet des wheels (torch ~2 Go, tensorflow ~572 Mo).

```dockerfile
# syntax=docker/dockerfile:1

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /tmp/comfyui-requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
```

BuildKit conserve `/root/.cache/pip` entre les builds dans un volume. Les wheels sont réutilisées même lorsque le cache de couches échoue.

**Activer BuildKit :**
```bash
DOCKER_BUILDKIT=1 docker build .
# or in GitHub Actions:
# uses: docker/setup-buildx-action@v3
```

**Gain attendu :** -30 à -50 % sur la phase d'installation pip lorsque le cache de couches échoue.

## Build multi-étapes {#multi-stage-build}

Retire les outils de build de l'image finale (économie d'environ 500 Mo à 1 Go).

```dockerfile
# Stage 1: builder with full toolchain
FROM nvidia/cuda:13.0.0-devel-ubuntu22.04 AS builder
RUN apt-get install -y build-essential cmake python3.12-dev
# ... install all Python packages and compile extensions ...

# Stage 2: runtime — only what's needed to run
FROM nvidia/cuda:13.0.0-runtime-ubuntu22.04 AS runtime

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/dist-packages \
                    /usr/local/lib/python3.12/dist-packages
COPY --from=builder /app/ComfyUI /app/ComfyUI

# Minimal runtime deps only
RUN apt-get install -y python3.12 libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
```

**Compromis :** la base devel du builder fait ~3,5 Go, contre ~2 Go pour la base runtime. L'image finale contient la base runtime et les paquets installés, sans compilateurs.

## Flash Attention : sélection du GPU à l'exécution {#flash-attention-runtime-gpu-selection}

Palette de GPU cibles : A100 (sm_80) + H100 (sm_90) + H200 (sm_90).

```python
# entrypoint.py or model init
import torch
from kernels import get_kernel

def load_flash_attention():
    cap = torch.cuda.get_device_capability()
    arch = f"sm_{cap[0]}{cap[1]}"
    
    if cap[0] >= 9:
        # H100, H200 → Flash Attention 3 (30-50% faster than FA2)
        return get_kernel("kernels-community/vllm-flash-attn3", arch=arch)
    else:
        # A100, A40, RTX 4090 → Flash Attention 2
        return get_kernel("kernels-community/flash-attn2", arch=arch)
```

**Registre HF Kernels :**
- `kernels-community/flash-attn2` — sm_80+ (A100, H100, H200)
- `kernels-community/vllm-flash-attn3` — sm_90 uniquement (H100, H200)
- `kernels-community/sgl-flash-attn3` — implémentation alternative pour H100+

**Vérifier d'abord si FA est nécessaire :**
```bash
docker run --rm IMAGE python -c "import flash_attn; print(flash_attn.__version__)"
# If ImportError → custom nodes don't require FA → skip optimization
```

## Configuration du cache de registre {#registry-cache-config}

```yaml
# GitHub Actions build step
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: |
      ghcr.io/org/comfyui:${{ github.sha }}
      ghcr.io/org/comfyui:latest
    cache-from: type=registry,ref=ghcr.io/org/comfyui:buildcache
    cache-to: type=registry,ref=ghcr.io/org/comfyui:buildcache,mode=max
```

Le cache de couches est stocké dans GHCR sous forme d'image OCI distincte. `mode=max` met en cache les couches intermédiaires, et pas seulement la couche finale.

## Objectifs de temps de build {#build-time-targets}

| Phase | Build à froid | Avec cache de couches | Avec montage de cache pip |
|-------|-----------|-----------------|---------------------|
| Dépendances système | ~2 min | ~0 (en cache) | — |
| Installation de PyTorch | ~5 min | ~0 (en cache) | ~2 min (wheels en cache) |
| ComfyUI + nœuds stables | ~8 min | ~0 (en cache) | ~4 min |
| Nœuds volatils uniquement | ~3 min | ~3 min (toujours exécuté) | ~1 min |
| **Reconstruction totale (changement de pin)** | ~18 min | ~6 min | ~3 min |

## Pièges {#gotchas}

- **Problème :** `python3-pip` laissé dans les dépendances apt → installe les paquets système `python3-*` avec des métadonnées distutils → la mise à niveau de pip échoue sur `blinker`, `yaml`, `requests` ou similaire. -> **Correctif :** retirer `python3-pip` d'apt entièrement. Amorcer avec `python3.12 -m ensurepip`. Ajouter un `apt purge` défensif pour les paquets connus pour créer des conflits.
- **Problème :** les 28 nœuds personnalisés dans un seul `nodes.txt` → un seul changement de pin provoque la reconstruction complète de tous les nœuds (plus de 10 min). -> **Correctif :** séparer en `nodes-stable.txt` (rarement modifié) et `nodes-volatile.txt` (mis à jour fréquemment). Utiliser des couches `RUN` distinctes pour chacun.
- **Problème :** des modèles GGUF intégrés à l'image la font grossir à 30-60 Go, ce qui rend le pull des couches depuis GHCR long de 10 à 20 min. -> **Correctif :** utiliser des Network Volumes pour tous les modèles de plus de 1 Go. Les monter à l'exécution. Utiliser le fichier sentinelle `.models_provisioned` pour éviter un nouveau téléchargement.
- **Problème :** le cache pip BuildKit n'est pas conservé entre les exécutions GitHub Actions (runners éphémères). -> **Correctif :** utiliser `actions/cache` pour conserver `/root/.cache/pip` entre les exécutions, ou utiliser un runner auto-hébergé avec un volume de cache persistant.
- **Problème :** l'appel `get_kernel()` à l'exécution échoue au premier import si HF Kernels n'est pas installé. -> **Correctif :** l'encadrer dans un try/except et revenir à `torch.nn.functional.scaled_dot_product_attention` (intégré à PyTorch, sans FA). Ne préférer FA que là où l'écart de débit compte.

## Voir aussi {#see-also}

- [[docker-for-ml]]
- [[runpod-production]]
- [[dockerfile-and-image-building]]
- [[container-registries]]
