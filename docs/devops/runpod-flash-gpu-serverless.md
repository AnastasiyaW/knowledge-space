# RunPod Flash GPU Serverless

RunPod Flash is an open-source Python SDK (MIT license, v1.16.0) that enables the deployment of GPU-accelerated serverless functions via a decorator-based interface. It automates worker provisioning, environment setup, and dependency management, eliminating the need for manual Dockerfile creation and container registry maintenance.

## Core Architecture and Implementation
Flash functions are defined using the `@Endpoint` decorator, which specifies hardware requirements and software dependencies. The SDK handles the cross-platform build process, allowing developers on macOS (M-series) or Linux to target remote x86_64 GPU environments.

### Serverless Function Definition
```python
from runpod_flash import Endpoint, GpuType

@Endpoint(
    name="tensor-processor",
    gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,
    workers=(0, 10), # scale-to-zero to 10 max workers
    dependencies=["torch>=2.4.0", "numpy", "pillow"]
)
async def process_data(payload):
    # Logic executes on remote RunPod Serverless infrastructure
    import torch
    return {"device": str(torch.cuda.get_device_name(0))}
```

### Deployment Workflow
The CLI manages authentication and endpoint lifecycle:
```bash
pip install runpod-flash
flash login   # OAuth browser flow
flash deploy  # Provisions infrastructure and uploads code
```

## Resource Management and Hardware Selection
The SDK uses typed enums for precise hardware targeting and flexible scaling configurations.

- **GPU Types:** Selection via `GpuType` for specific models (e.g., `NVIDIA_A100_80GB_PCIe`, `NVIDIA_GEFORCE_RTX_4090`).
- **GPU Groups:** Use of `GpuGroup` (e.g., `GpuGroup.AMPERE_80`, `GpuGroup.ANY`) to allow the provisioner to select the first available compatible node.
- **Worker Scaling:** The `workers=(min, max)` parameter enables scale-to-zero logic to eliminate idle costs.
- **Storage:** Integration with `NetworkVolume` provides persistent, cross-data-center storage for model weights or datasets.
- **Environment Variables:** Flash excludes environment variable values from the configuration hash, ensuring that secret rotation or configuration changes do not trigger an image rebuild.

## Deployment Patterns
1. **Queue-based (Async):** Standard pattern for batch processing jobs triggered via the SDK's async API.
2. **Load-balanced API:** HTTP-accessible routes that share a common pool of scaling workers.
3. **Custom Docker Orchestration:** Integration of existing pre-built images (e.g., vLLM, TensorRT-LLM, ComfyUI) into the Flash orchestration layer.
4. **Development Mode:** Ephemeral worker provisioning via `flash dev --auto-provision` for local debugging against remote GPU resources.

## Operational Constraints
- **Package Limits:** Total deployment size (code + local dependencies) is capped at 500 MB.
- **Runtime Support:** Limited to Python 3.10, 3.11, and 3.12.
- **Cold Starts:** Heavy dependency stacks (e.g., `torch` + `diffusers`) can result in cold starts lasting several minutes.
- **Host Requirements:** The local development CLI requires macOS or Linux; Windows environments are supported only via WSL2.

## Gotchas
- **Issue:** Large dependency overhead triggers 500 MB deployment limit or slow cold starts. → **Fix:** Move large static assets and model weights to a `NetworkVolume` and mount it to the worker instead of bundling them in the deployment package.
- **Issue:** Standard pip installs in the decorator fail for private or complex packages. → **Fix:** Use the `Custom Docker` pattern (Pattern 3) to provide a pre-built environment while still using Flash for orchestration.
- **Issue:** Local execution on Windows fails to initialize the Flash CLI. → **Fix:** Use a Linux-based development container or WSL2, as the native Windows shell is not supported for local builds.

## See Also
- [[runpod-production]]
- [[docker-for-ml]]
- [[deployment-strategies]]
- [[kubernetes-resource-management]]

