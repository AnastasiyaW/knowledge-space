# RunPod Production Patterns

Reference for deploying GPU workloads on RunPod: deploy type selection, image strategy tiers, serverless worker architecture, secrets management, and common failure modes.

## Deploy Type Selection

| Use case | Deploy type | Billing |
|----------|------------|---------|
| Training / fine-tuning (hours/days) | **Pod** | Per-hour, idle included |
| Debugging, interactive ComfyUI | **Pod** | Per-hour, idle included |
| Production inference API | **Serverless** | Per-second active only |
| Uneven traffic (peak + idle) | **Serverless** | 60-70% savings vs always-on |
| Hybrid: serverless front + long tasks | **Instant Clusters** | Mixed |

**Decision rule:** Constant load → Pod. Uneven / API endpoint → Serverless.

## Image Strategy (3 Tiers)

### Tier 1 — RunPod-cached (10-60 sec pull)
```text
runpod/pytorch:2.11.0-cuda13.0-cudnn9-devel
runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
runpod/worker-comfyui:<version>-base
runpod/worker-comfyui:<version>-flux1-dev
runpod/base:0.6.x-cuda...
```
Cached on Secure Cloud nodes. Community cloud not guaranteed.

### Tier 2 — Popular Docker Hub (1-5 min pull)
```text
pytorch/pytorch:2.11.0-cuda13.0-cudnn9-devel
nvidia/cuda:*  (sometimes cached, sometimes not)
```

### Tier 3 — Custom images (3-10 min or STUCK)
```text
ghcr.io/your-org/your-image:tag
nvidia/cuda:13.0.0-devel-ubuntu22.04  ← confirmed stuck on 4/4 pods (2026-04-17)
```

**Rule:** Always try Tier 1 first. If CUDA/PyTorch version matches Tier 1, use it.  
Custom images (Tier 3) go to `ghcr.io` as overlay on Tier 2 base, not bare `nvidia/cuda`.

## FlashBoot

Free cold-start optimization, enabled by default.

- 48% of cold starts complete in <200ms
- Typical: 1-2 sec cold start
- ComfyUI: 50-80% faster cold starts with FlashBoot
- Mechanism: more frequent calls → RunPod keeps workers "warm" on host

**Active worker count ≥ 1** reduces cold start to ~0ms (pay always-on price).

## Network Volumes (Model Storage)

```bash
# Create volume in RunPod Console → pick region closest to traffic source
# Mount volume in pod/worker:
# /opt/ComfyUI/models → Network Volume path

# Pre-load models via cheap CPU pod:
rsync -av ./models/ /workspace/models/
# Or: aws s3 sync s3://your-bucket/models /workspace/models/
```

**Pricing:** $0.07/GB/month first TB, $0.05/GB thereafter.  
**Use when:** Models >10 GB, updated frequently, shared across multiple pods.  
**Baked-in images:** Only for stable models ≤10 GB that rarely change.

## worker-comfyui Pattern

Official serverless pattern (`github.com/runpod-workers/worker-comfyui`).

### Request Format

```json
{
  "input": {
    "workflow": {},
    "images": [{"name": "input.png", "image": "<base64>"}],
    "api_key_override": ""
  },
  "webhook": "https://your-endpoint/callback"
}
```

### Response Format (v5.0.0+)

```json
{
  "output": {
    "images": [
      {"filename": "out.png", "type": "base64", "data": "..."}
    ],
    "errors": []
  }
}
```

### Endpoints
- `/run` — async, up to 10 MB payload
- `/runsync` — sync, up to 20 MB payload
- `/health` — status check

### SSH Debug Access
```bash
# Set env var in pod template:
PUBLIC_KEY=<your-ssh-public-key>
# Opens port 22 for SSH access into worker
```

## Secrets Management

```bash
# In RunPod Console → Account → Secrets → create named secret
# Reference in template env vars:
RUNPOD_SECRET_WASABI_ACCESS_KEY=my-wasabi-key-name
RUNPOD_SECRET_WASABI_SECRET_KEY=my-wasabi-secret-name
# Runtime substitutes encrypted value → plain env var inside container
```

**Scoped API keys (2026):** Create per-endpoint keys with usage tracking. Principle of least privilege.

## GPU Selection Matrix

| GPU | Architecture | flash-attn2 | flash-attn3 | Notes |
|-----|-------------|-------------|-------------|-------|
| A100 | sm_80 | Yes | No | Standard, widely available |
| H100 | sm_90 | Yes | Yes (+30-50% vs FA2) | Best for HF/training |
| H200 | sm_90 | Yes | Yes | Latest, scarce |
| A40 | sm_86 | Yes | No | Budget training |
| RTX 4090 | sm_89 | Yes | No (sm_89 < sm_90) | Consumer, cheap |

**Flash Attention runtime selection:**
```python
import torch
cap = torch.cuda.get_device_capability()
if cap[0] >= 9:
    # H100, H200 → FA3 via HF Kernels
    from kernels import get_kernel
    fa = get_kernel("kernels-community/vllm-flash-attn3",
                    arch=f"sm_{cap[0]}{cap[1]}")
else:
    # A100 → FA2
    fa = get_kernel("kernels-community/flash-attn2",
                    arch=f"sm_{cap[0]}{cap[1]}")
```

## CI/CD Pattern

```yaml
# .github/workflows/deploy.yml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/org/image:${{ github.sha }},ghcr.io/org/image:latest
    cache-from: type=registry,ref=ghcr.io/org/image:buildcache
    cache-to: type=registry,ref=ghcr.io/org/image:buildcache,mode=max
```

**Immutable tags:** `:sha` never mutates. `:latest` is a moving pointer only.

## 8 Common Pitfalls

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| Image pull stuck indefinitely | Tier 3 image not cached by RunPod, Docker Hub rate-limit | Use Tier 1/2; push custom to ghcr.io as overlay |
| CUDA mismatch at runtime | Base image CUDA ≠ installed PyTorch CUDA | Match exactly: `cu130` wheels need CUDA 13.0 base |
| Zero GPU scaling stuck at 0 workers | Worker health check fails | Check `PUBLIC_KEY` for SSH debug; test `/health` endpoint |
| OOM on large models | Model loaded per-request instead of once | Load model in `handler.py` init, not inside `handler()` function |
| Idle pod cost accumulating | Pod left running after session | Use Serverless for production; set stop-idle for dev pods |
| Secrets not accessible | Referencing plain env var name instead of `RUNPOD_SECRET_*` | Use prefix `RUNPOD_SECRET_<secret-name>` in template |
| Community Cloud pods stuck | Image pull unreliable on community nodes | Use Secure Cloud for Tier 3 images |
| Blackwell GPU incompatibility | sm_100 wheels not yet available | Check wheel compatibility; use A100/H100 until support lands |

## Gotchas

- **Issue:** `nvidia/cuda:13.0.0-devel-ubuntu22.04` used directly as pod image → stuck on 4/4 consecutive pods across A5000/A40/L40S. -> **Fix:** Use `pytorch/pytorch:2.11.0-cuda13.0-cudnn9-devel` as base (same CUDA 13, same PyTorch 2.11, properly cached). Never use raw `nvidia/cuda` images as direct RunPod targets.
- **Issue:** Model downloaded to container local disk → lost when pod terminates. -> **Fix:** Always use Network Volumes for models >1 GB. Attach volume at `/workspace/models`. Use sentinel file `.models_provisioned` to skip re-download on restart.
- **Issue:** Serverless worker loads heavy model inside `handler()` function — 30-second cold start per request. -> **Fix:** Load model at module level (outside handler): `model = load_model()` executed once at worker init.
- **Issue:** `--resume` / `--continue` sessions with billing-related strings in history trigger cache invalidation bug (v2.1.100), inflating token costs 10-20x. -> **Fix:** Avoid `--resume` until bug is confirmed fixed; start fresh sessions for long workflows.

## See Also

- [[docker-for-ml]]
- [[container-registries]]
- [[dockerfile-and-image-building]]
- [[cicd-pipelines]]
