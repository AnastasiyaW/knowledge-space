---
level: 3
source_sha256: a254ce52685284720377d33e06206b473dac563a93d86929524eb446bc316827
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Container Build System {#comfyui-container-build-system}

Muster für den Bau produktionstauglicher ComfyUI-Docker-Images: Auflösung von distutils-Konflikten, Layer-Aufteilung für Cache-Effizienz, BuildKit-Pip-Cache-Mounts, Multi-Stage-Builds und Laufzeitauswahl für Flash Attention.

## Build-Stack {#build-stack}

- **Basis-Image:** `nvidia/cuda:13.0.0-runtime-ubuntu22.04`
- **Python:** 3.12 über das deadsnakes-PPA
- **PyTorch:** cu130-Wheels von pytorch.org
- **Custom Nodes:** `nodes.txt` mit festgepinnten Commit-Hashes
- **Registry:** GHCR (`ghcr.io/org/comfyui`)
- **Build-Runner:** GitHub Actions → ephemere VM (cx43, 200-GB-Volume)

## Behebung des distutils-Konflikts {#distutils-conflict-fix}

**Symptom:**
```yaml
error: uninstall-distutils-installed-package
× Cannot uninstall blinker 1.4
╰─> It is a distutils installed project...
```

**Ursache:** Ubuntu 22.04 installiert Python-3.10-Pakete über apt mit altmodischen distutils-Metadaten (ohne `RECORD`-Datei). Wenn pip versucht, diese Pakete zu aktualisieren (z. B. `blinker>=1.9`, transitiv angefordert), kann die alte Version nicht entfernt werden.

**Lösung: `python3-pip` aus apt entfernen und pip über `ensurepip` bereitstellen:**

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

**Diese Liste** in `CONFLICTS.md` erweitern, sobald neue distutils-Konflikte auftreten.

## Layer-Aufteilung: stable/volatile {#layer-split-stablevolatile}

Eine einzige `nodes.txt` mit allen Custom Nodes → jede Pin-Aktualisierung invalidiert die gesamte Layer (Neuaufbau über 10 Minuten).

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

**Erwartete Beschleunigung:** Neuaufbau in 5–7 Minuten statt 15 Minuten nach einer einzelnen Pin-Änderung bei einem Node.

## BuildKit-Pip-Cache-Mount {#buildkit-pip-cache-mount}

Ohne Cache-Mounts erzwingt jeder Cache-Miss einen vollständigen Download der Wheels (torch ca. 2 GB, tensorflow ca. 572 MB).

```dockerfile
# syntax=docker/dockerfile:1

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /tmp/comfyui-requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
```

BuildKit hält `/root/.cache/pip` in einem Volume über Builds hinweg vor. Wheels werden wiederverwendet, auch wenn der Layer-Cache verfehlt wird.

**BuildKit aktivieren:**
```bash
DOCKER_BUILDKIT=1 docker build .
# or in GitHub Actions:
# uses: docker/setup-buildx-action@v3
```

**Erwartete Beschleunigung:** -30–50 % in der pip-install-Phase bei einem Layer-Cache-Miss.

## Multi-Stage-Build {#multi-stage-build}

Entfernt Build-Werkzeuge aus dem finalen Image (Einsparung ca. 500 MB – 1 GB).

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

**Abwägung:** Das devel-Basis-Image im Builder umfasst ca. 3,5 GB, das runtime-Basis-Image ca. 2 GB. Das finale Image besteht aus dem runtime-Basis-Image plus den installierten Paketen, ohne Compiler.

## Flash Attention: Auswahl der GPU zur Laufzeit {#flash-attention-runtime-gpu-selection}

Zielpalette der GPUs: A100 (sm_80) + H100 (sm_90) + H200 (sm_90).

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

**HF-Kernels-Registry:**
- `kernels-community/flash-attn2` — sm_80+ (A100, H100, H200)
- `kernels-community/vllm-flash-attn3` — nur sm_90 (H100, H200)
- `kernels-community/sgl-flash-attn3` — alternative Implementierung für H100+

**Zuerst prüfen, ob FA überhaupt benötigt wird:**
```bash
docker run --rm IMAGE python -c "import flash_attn; print(flash_attn.__version__)"
# If ImportError → custom nodes don't require FA → skip optimization
```

## Konfiguration des Registry-Caches {#registry-cache-config}

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

Der Layer-Cache liegt in GHCR als separates OCI-Image. `mode=max` cacht auch Zwischen-Layer, nicht nur das finale Ergebnis.

## Zielwerte für die Build-Zeit {#build-time-targets}

| Phase | Kaltstart | Mit Layer-Cache | Mit pip-Cache-Mount |
|-------|-----------|-----------------|---------------------|
| Systemabhängigkeiten | ~2 min | ~0 (gecacht) | — |
| PyTorch-Installation | ~5 min | ~0 (gecacht) | ~2 min (Wheels gecacht) |
| ComfyUI + stabile Nodes | ~8 min | ~0 (gecacht) | ~4 min |
| Nur volatile Nodes | ~3 min | ~3 min (läuft immer) | ~1 min |
| **Gesamter Neuaufbau (Pin-Änderung)** | ~18 min | ~6 min | ~3 min |

## Fallstricke {#gotchas}

- **Problem:** `python3-pip` bleibt in den apt-Abhängigkeiten → installiert System-Pakete `python3-*` mit distutils-Metadaten → pip-Upgrade schlägt bei `blinker`, `yaml`, `requests` o. Ä. fehl. → **Lösung:** `python3-pip` vollständig aus apt entfernen. Mit `python3.12 -m ensurepip` bootstrappen. Defensives `apt purge` für bekannte Konfliktpakete ergänzen.
- **Problem:** Alle 28 Custom Nodes in einer `nodes.txt` → eine einzelne Pin-Änderung löst den vollständigen Neuaufbau aller Nodes aus (über 10 Min). → **Lösung:** Aufteilen in `nodes-stable.txt` (selten geändert) und `nodes-volatile.txt` (häufig aktualisiert). Für jede Datei eine eigene `RUN`-Layer.
- **Problem:** GGUF-Modelle im Image lassen dieses auf 30–60 GB anwachsen, sodass das Pullen der Layer aus GHCR 10–20 Min dauert. → **Lösung:** Network Volumes für alle Modelle über 1 GB verwenden. Zur Laufzeit einhängen. Sentinel-Datei `.models_provisioned` nutzen, um erneute Downloads zu vermeiden.
- **Problem:** Der pip-Cache von BuildKit wird zwischen GitHub-Actions-Läufen nicht persistiert (ephemere Runner). → **Lösung:** `actions/cache` nutzen, um `/root/.cache/pip` zwischen Läufen zu erhalten, oder einen selbst gehosteten Runner mit persistentem Cache-Volume verwenden.
- **Problem:** Der `get_kernel()`-Aufruf zur Laufzeit-Auswahl schlägt beim ersten Import fehl, wenn HF Kernels nicht installiert ist. → **Lösung:** In try/except kapseln und auf `torch.nn.functional.scaled_dot_product_attention` (PyTorch-eigen, ohne FA) zurückfallen. FA nur dort bevorzugen, wo der Durchsatzunterschied relevant ist.

## Siehe auch {#see-also}

- [[docker-for-ml]]
- [[runpod-production]]
- [[dockerfile-and-image-building]]
- [[container-registries]]
