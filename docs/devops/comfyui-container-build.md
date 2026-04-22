# ComfyUI Container Build System

Patterns for building production-grade ComfyUI Docker images: distutils conflict resolution, layer split for cache efficiency, BuildKit pip cache mounts, multi-stage builds, and Flash Attention runtime selection.

## Build Stack

- **Base image:** `nvidia/cuda:13.0.0-runtime-ubuntu22.04`
- **Python:** 3.12 via deadsnakes PPA
- **PyTorch:** cu130 wheels from pytorch.org
- **Custom nodes:** `nodes.txt` with pinned commit hashes
- **Registry:** GHCR (`ghcr.io/org/comfyui`)
- **Build runner:** GitHub Actions → ephemeral VM (cx43, 200 GB volume)

## Distutils Conflict Fix

**Symptom:**
```yaml
error: uninstall-distutils-installed-package
× Cannot uninstall blinker 1.4
╰─> It is a distutils installed project...
```

**Root cause:** Ubuntu 22.04 installs Python 3.10 packages via apt using legacy distutils metadata (no `RECORD` file). When pip tries to upgrade those packages (e.g., `blinker>=1.9` pulled transitively), it cannot remove the old version.

**Fix — remove `python3-pip` from apt, bootstrap via `ensurepip`:**

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

**Extend this list** in `CONFLICTS.md` as new distutils conflicts surface.

## Layer Split: stable/volatile

Single `nodes.txt` with all custom nodes → any pin update invalidates the entire layer (10+ minute rebuild).

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

**Expected speedup:** 5-7 min rebuild instead of 15 min after single node pin change.

## BuildKit Pip Cache Mount

Without cache mounts, every cache miss forces full wheel download (torch ~2 GB, tensorflow ~572 MB).

```dockerfile
# syntax=docker/dockerfile:1

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /tmp/comfyui-requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
```

BuildKit persists `/root/.cache/pip` across builds in a volume. Wheels are reused even when the layer cache misses.

**Enable BuildKit:**
```bash
DOCKER_BUILDKIT=1 docker build .
# or in GitHub Actions:
# uses: docker/setup-buildx-action@v3
```

**Expected speedup:** -30-50% on pip install phase when layer cache misses.

## Multi-Stage Build

Removes build tools from final image (~500 MB - 1 GB savings).

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

**Trade-off:** devel base in builder ~3.5 GB vs runtime base ~2 GB. Final image: runtime base + installed packages, no compilers.

## Flash Attention: Runtime GPU Selection

Target GPU palette: A100 (sm_80) + H100 (sm_90) + H200 (sm_90).

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

**HF Kernels registry:**
- `kernels-community/flash-attn2` — sm_80+ (A100, H100, H200)
- `kernels-community/vllm-flash-attn3` — sm_90 only (H100, H200)
- `kernels-community/sgl-flash-attn3` — alternative H100+ implementation

**First check if FA is needed:**
```bash
docker run --rm IMAGE python -c "import flash_attn; print(flash_attn.__version__)"
# If ImportError → custom nodes don't require FA → skip optimization
```

## Registry Cache Config

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

Layer cache lives in GHCR as separate OCI image. `mode=max` caches intermediate layers, not just final.

## Build Time Targets

| Phase | Cold build | With layer cache | With pip cache mount |
|-------|-----------|-----------------|---------------------|
| System deps | ~2 min | ~0 (cached) | — |
| PyTorch install | ~5 min | ~0 (cached) | ~2 min (wheels cached) |
| ComfyUI + stable nodes | ~8 min | ~0 (cached) | ~4 min |
| Volatile nodes only | ~3 min | ~3 min (always runs) | ~1 min |
| **Total rebuild (pin change)** | ~18 min | ~6 min | ~3 min |

## Gotchas

- **Issue:** `python3-pip` left in apt dependencies → installs system `python3-*` packages with distutils metadata → pip upgrade fails on `blinker`, `yaml`, `requests`, or similar. -> **Fix:** Remove `python3-pip` from apt entirely. Bootstrap with `python3.12 -m ensurepip`. Add defensive `apt purge` for known conflicters.
- **Issue:** All 28 custom nodes in one `nodes.txt` → single pin change causes complete rebuild of all nodes (~10+ min). -> **Fix:** Split into `nodes-stable.txt` (rarely changed) and `nodes-volatile.txt` (frequently updated). Separate `RUN` layers for each.
- **Issue:** GGUF models baked into image inflate image size to 30-60 GB, making layer pulls from GHCR 10-20 min. -> **Fix:** Use Network Volumes for all models >1 GB. Mount at runtime. Use sentinel file `.models_provisioned` to avoid re-download.
- **Issue:** BuildKit pip cache not persisted between GitHub Actions runs (ephemeral runners). -> **Fix:** Use `actions/cache` to persist `/root/.cache/pip` between runs, or use a self-hosted runner with persistent cache volume.
- **Issue:** Runtime-selection `get_kernel()` call fails on first import if HF Kernels not installed. -> **Fix:** Wrap in try/except, fall back to `torch.nn.functional.scaled_dot_product_attention` (PyTorch built-in, no FA). Only prefer FA where throughput gap matters.

## See Also

- [[docker-for-ml]]
- [[runpod-production]]
- [[dockerfile-and-image-building]]
- [[container-registries]]
