# RunPod Serverless Python Silent Exit 1

Analysis and mitigation of silent worker crashes (exit code 1) during task pickup on RunPod Serverless, specifically when wrapping heavy subprocesses like ComfyUI.

## Diagnostic Ranking for Exit Code 1
When a RunPod worker exits with code 1 without a traceback in the logs, the cause is typically related to process lifecycle management rather than a simple Python exception.

### 1. Subprocess Death and Handler Graceful Return
If a subprocess (e.g., ComfyUI) dies, the handler may catch a `ConnectionError` or `TimeoutError`, log it, and return a "failed" status to the SDK. However, if the main execution loop `runpod.serverless.start()` returns normally, the Python interpreter begins its shutdown sequence.
- **Race Condition:** Daemon threads (like Loki logging flushers) or `atexit` hooks may raise an exception during interpreter shutdown.
- **Result:** CPython exits with code 1, but since the logger is already shutting down, the traceback is never emitted.

### 2. Output Buffering
By default, Python buffers `stdout` and `stderr` when redirected to a pipe (common in containerized environments).
- **Pitfall:** If a crash occurs, the last few KB of logs (including the traceback) may still be in the memory buffer and never reach the container logs.
- **Verification:** If the log is truncated or completely empty after initialization, buffering is a contributing factor.

### 3. Entrypoint Script Failure
If `entrypoint.sh` uses `set -e` and a command fails before `exec python handler.py`, the container exits immediately with code 1. This often happens if the worker script tries to verify the subprocess availability and fails.

## Mitigation: Forced Process Termination
To prevent race conditions during interpreter shutdown (e.g., hanging daemon threads), use `os._exit(0)` to bypass `atexit` and cleanup hooks after the RunPod SDK finishes.

```python
import sys
import os
import runpod

def handler(job):
    # ... logic ...
    return {"status": "success"}

if __name__ == "__main__":
    try:
        runpod.serverless.start({"handler": handler})
    finally:
        # Force flush and hard exit to avoid exit 1 race conditions
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(0)
```

## Mitigation: Unbuffered Logging and Exception Hooks
Ensure logs are emitted immediately and uncaught exceptions in the main thread are captured before the process dies.

### Execution Flags
Modify the container entrypoint to force unbuffered output.
```bash
export PYTHONUNBUFFERED=1
exec python -u handler.py
```

### Global Exception Hook
Implement a `sys.excepthook` to write fatal errors to a persistent volume or `stderr` immediately.
```python
import sys
import traceback

def fatal_error_hook(exc_type, exc_value, tb):
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, tb))
    sys.stderr.write(f"FATAL EXCEPTION: {error_msg}\n")
    sys.stderr.flush()

sys.excepthook = fatal_error_hook
```

## Subprocess Health Checks
If wrapping an API-based tool like ComfyUI, the handler must verify the PID is still alive. A simple `requests.get` timeout is insufficient.

```python
import os

def is_subprocess_alive(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
```

## Gotchas
- **Issue:** OOM Kill confusion → **Fix:** Check the exit code. Out of Memory (OOM) triggers `SIGKILL`, resulting in exit code **137**. Exit code **1** is a software-level error or interpreter crash.
- **Issue:** Background thread crashes → **Fix:** Python's `sys.excepthook` only catches exceptions in the main thread. For background threads (Python 3.8+), you must also set `threading.excepthook`.
- **Issue:** Log loss on exit → **Fix:** Always use `sys.stdout.flush()` before any `exit()` or `_exit()` call in a container environment.

## See Also
- [[runpod-production]]
- [[monitoring-and-observability]]
- [[docker-for-ml]]
- [[runpod-flash-gpu-serverless]]

