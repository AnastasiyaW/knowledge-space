# RunPod Serverless: Silent Worker Crashes on Task Pickup

Workers in a serverless environment may spawn as "Ready," pick up a task, and then die silently within 30-60 seconds. In this state, the `failed` and `completed` counters do not increment, but the `unhealthy` counter increases as the worker process disappears. This behavior typically indicates a failure within the container lifecycle or the `runpod-python` SDK's internal result handling.

## Primary Failure Mechanisms

The silent nature of these crashes usually stems from the worker process exiting before the RunPod framework can register a failure or during a critical handover period.

### Module-Level Import Failures
If the `handler.py` or any imported custom modules crash at the top-level (module scope), the process exits before `runpod.serverless.start()` is ever reached. Because the handler was never registered, the RunPod scheduler cannot catch the exception, leading to an "unhealthy" status as the container stops unexpectedly.

To diagnose, run the container image locally to verify imports:
```bash
docker run --rm -it --gpus all \
  -e RUNPOD_DEBUG=1 \
  --entrypoint python \
  your-registry/image-name:tag \
  -c "import handler"
```

### SDK Version Regressions (1.7.11+)
Versions of the `runpod-python` SDK from 1.7.11 to 1.8.x contain several unresolved regressions that cause silent exits:
- **Issue #309:** The internal `_handle_result` function fails to post back to the scheduler but the process exits, preventing the `failed` counter from incrementing.
- **Issue #458:** `current_concurrency: None` TypeErrors cause 2-3 minute hangs followed by container restarts.
- **Issue #432:** Routing bugs where all requests are sent to a single worker.

The recommended stable version is `runpod==1.7.10`.

### Sibling Process Race Conditions
In ComfyUI or similar stacks where the handler and the application server run as sibling processes, the handler may attempt to communicate with the server before the server is fully listening (e.g., on port 8188). If the handler raises a `ConnectionRefusedError` and the SDK's exception handling is bypassed or broken, the container exits silently.

## Implementation of Guarded Handlers

To prevent silent crashes, implement a defensive wrapper within the handler and use synchronous checks for sibling processes.

### Guarded Handler Pattern
Avoid using `raise` for expected errors; instead, return a dictionary containing an `error` key. This ensures the SDK successfully posts the failure back to the RunPod scheduler.

```python
import sys, traceback, runpod, requests, time

def _wait_for_server(url="http://127.0.0.1:8188/", timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        try:
            if requests.get(url, timeout=5).status_code == 200:
                return True
        except requests.RequestException:
            time.sleep(1)
    return False

def handler(job):
    try:
        if not _wait_for_server():
            return {"error": "Application server failed to start in time"}
        
        # Core logic
        result = {"output": "success"} 
        
        # Ensure result is not an empty dict
        if not result:
            return {"error": "Empty result produced"}
            
        return result
    except Exception as e:
        # Capture traceback to stderr for Console UI visibility
        error_info = traceback.format_exc()
        print(error_info, file=sys.stderr)
        return {"error": str(e), "traceback": error_info}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
```

## Infrastructure and Resource Validation

### Disk Space Constraints
Serverless templates with `containerDiskInGb` set to the default (often 20-30GB) frequently hit `ENOSPC` (No space left on device) during task execution if the base image is large (e.g., 20GB+). This causes the kernel to kill the process or the filesystem to lock up, resulting in a silent crash.
- **Remedy:** Ensure `containerDiskInGb` is at least 2x the uncompressed image size. For ComfyUI stacks, 60GB is the recommended minimum.

### Synchronous Testing (runsync)
To bypass the async queue and see raw error messages directly in the API response, use the `/runsync` endpoint instead of `/run`.
```bash
curl -X POST https://api.runpod.ai/v2/{endpoint_id}/runsync \
     -H "Authorization: Bearer {api_key}" \
     -H "Content-Type: application/json" \
     -d '{"input": {"test": "data"}}'
```

## Gotchas
- **Issue:** SDK versions 1.7.11 and higher have documented regressions that break the failure reporting loop. → **Fix:** Pin `runpod==1.7.10` in your Dockerfile.
- **Issue:** Returning an empty dictionary `{}` from a handler causes a `KeyError: 'output'` within the SDK framework in some versions. → **Fix:** Always return a non-empty dictionary with at least one status or error key.
- **Issue:** Out-of-memory (OOM) kills by the Linux kernel do not produce Python tracebacks. → **Fix:** Monitor the "Killed" string in the RunPod Console logs and increase GPU or System RAM.
- **Issue:** Wasabi S3 or other external storage uploads can hang the handler if the region is not explicitly defined, leading to a timeout kill. → **Fix:** Pass `region_name` explicitly to the boto3 client.

## See Also
- [[runpod-production]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-flash-gpu-serverless]]
- [[comfyui-container-build]]
- [[docker-for-ml]]

