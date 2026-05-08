# RunPod Serverless Diagnostic Image: SSH, Filebrowser, TTY, and Cross-Pod Log Sharing

Serverless workers die silently. RunPod Console captures only what the process emits before exit, rotation truncates logs, and once a container terminates its ephemeral filesystem is gone. This article describes a layered diagnostic surface that persists across worker death: per-pod log files on a Network Volume, pre-handler observability services (sshd, filebrowser, ttyd), a crash-guard pattern in the handler, and a post-mortem state machine via marker files.

Companion to: silent crash root-cause analysis, Python silent-exit traps.

---

## Volume Cross-Pod Sharing Semantics

RunPod Network Volumes are NFS-style shared storage. Multiple Serverless workers can mount the same Volume simultaneously (same datacenter constraint — region-locked). The fundamental limitation: **flock() does not work reliably on NFS, and fcntl is unreliable**. Concurrent writes to the same file will corrupt it.

Architecture principle: **one file per pod, shared Volume as read-many store**.

| Property | Behavior | Implication |
|---|---|---|
| Concurrent reads | Safe | Any live pod can read any crashed pod's logs |
| Concurrent writes to distinct files | Safe | Per-pod naming eliminates contention |
| Concurrent writes to the same file | Corruption | Forbidden for all mutable state |
| Append via `O_APPEND` to JSONL | Relatively safe if writes < 4 KB | Atomic on most NFS implementations |
| fsync guarantee | Weak | Explicit `os.fsync()` required before crash |
| POSIX permissions | Ignored on most RunPod backends | Do not store secrets in files |
| Same-DC constraint | Enforced | Cross-region log aggregation requires external shipper |

**Volume mount paths**: `/runpod-volume` in Serverless; `/workspace` in Pod mode (convention via `OIS_VOLUME_ROOT=/workspace`).

**Per-pod file layout**:

```
/workspace/logs/
├── handler-${RUNPOD_POD_ID}.log         # full stdout+stderr from entrypoint start
├── handler-${RUNPOD_POD_ID}.traceback   # uncaught exception (sys.excepthook)
├── handler-${RUNPOD_POD_ID}.env         # startup env dump, secrets redacted
├── handler-${RUNPOD_POD_ID}.exit        # exit code + timestamp (bash EXIT trap)
├── handler-${RUNPOD_POD_ID}.atexit      # written by Python atexit; absence = crash/SIGKILL
├── heartbeat-${RUNPOD_POD_ID}           # unix timestamp, refreshed every 30s
└── _index.jsonl                         # append-only registry, one line per event
```

The `_index.jsonl` uses `O_APPEND` writes under 4 KB per line. This is not a message queue substitute — it is a diagnostic registry for correlating events across pods.

---

## Diagnostic Image Dockerfile Layer

Add this layer at the end of the production overlay Dockerfile, after `COPY handler.py`. It adds approximately 80-120 MB to a 23 GB base — acceptable overhead.

```dockerfile
# Diagnostic tools layer (~80-120 MB)
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server openssh-client \
    iproute2 net-tools iputils-ping dnsutils \
    vim nano less \
    htop atop iotop \
    tmux screen \
    rsync \
    inotify-tools \
    strace lsof psmisc \
    file tree jq \
    unzip zip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && ssh-keygen -A \
    && mkdir -p /run/sshd /root/.ssh \
    && chmod 700 /root/.ssh \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config \
    && echo "AcceptEnv RUNPOD_*" >> /etc/ssh/sshd_config

# Single-binary services: version-pinned, no package manager at runtime
ARG FILEBROWSER_VERSION=2.32.0
ARG TTYD_VERSION=1.7.7
RUN curl -fsSL \
        https://github.com/filebrowser/filebrowser/releases/download/v${FILEBROWSER_VERSION}/linux-amd64-filebrowser.tar.gz \
        | tar -xz -C /usr/local/bin filebrowser \
    && curl -fsSL -o /usr/local/bin/ttyd \
        https://github.com/tsl0922/ttyd/releases/download/${TTYD_VERSION}/ttyd.x86_64 \
    && chmod +x /usr/local/bin/ttyd /usr/local/bin/filebrowser

EXPOSE 22 7681 8080 8188
```

**SSH authorized_keys** are loaded from the Volume at runtime, not baked into the image — keys can be rotated without rebuild:

```bash
cp /workspace/authorized_keys /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
```

**Why single-binary over apt for filebrowser/ttyd**: version pinning via `ARG`, no transitive deps, smaller layer diffs in GHCR.

**Why not supervisord**: supervisord auto-restarts crashed processes, which means a handler in a crash loop never reports `FAILED` to the RunPod scheduler — the queue stalls. It also swallows exit codes. Bash background processes with `exec handler.py` (see below) forward exit codes correctly.

---

## Three-Stage Entrypoint: Observability Before the Handler

The critical flaw in naive entrypoints: observability starts **after** ComfyUI or the handler has already started. If either fails during startup, the debug services never launch. Restructure into three explicit stages.

```bash
#!/usr/bin/env bash
# NOTE: set -uo pipefail NOT -euo — -e would kill observability if any service fails to start
set -uo pipefail

# === STAGE 0: Volume sanity ===
VOLUME_LOG_DIR="${OIS_VOLUME_ROOT:-/workspace}/logs"
POD_ID="${RUNPOD_POD_ID:-pod-$(hostname)-$(date +%s)}"

mkdir -p "$VOLUME_LOG_DIR" 2>/dev/null || {
    echo "FATAL: Cannot create $VOLUME_LOG_DIR — Volume not mounted?" >&2
    exit 1
}

# === STAGE 1: Persistent log redirect — BEFORE any other output ===
VOLUME_LOG_FILE="$VOLUME_LOG_DIR/handler-${POD_ID}.log"
EXIT_FILE="$VOLUME_LOG_DIR/handler-${POD_ID}.exit"
ENV_FILE="$VOLUME_LOG_DIR/handler-${POD_ID}.env"

: > "$VOLUME_LOG_FILE"
exec > >(tee -a "$VOLUME_LOG_FILE") 2>&1

# Env dump with secrets redacted
env | grep -vE '(KEY|TOKEN|SECRET|PASSWORD|HASH)' | sort > "$ENV_FILE"

# Bash EXIT trap — writes exit code before container terminates
trap 'rc=$?; printf "{\"pod\":\"%s\",\"exit\":%d,\"ts\":\"%s\"}\n" \
    "'$POD_ID'" $rc "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "'$EXIT_FILE'"' EXIT

# === STAGE 2: Diagnostic services — BEFORE ComfyUI or handler ===
# Load SSH keys from Volume (rotatable without image rebuild)
if [ -f "${OIS_VOLUME_ROOT:-/workspace}/authorized_keys" ]; then
    cp "${OIS_VOLUME_ROOT:-/workspace}/authorized_keys" /root/.ssh/authorized_keys
    chmod 600 /root/.ssh/authorized_keys
fi

if command -v sshd >/dev/null 2>&1; then
    /usr/sbin/sshd -D > "$VOLUME_LOG_DIR/sshd-${POD_ID}.log" 2>&1 &
    echo "sshd PID=$! port=22"
fi

if command -v filebrowser >/dev/null 2>&1; then
    filebrowser --noauth --address 0.0.0.0 --port 8080 \
        --root /workspace --database /tmp/fb.db \
        > "$VOLUME_LOG_DIR/filebrowser-${POD_ID}.log" 2>&1 &
    echo "filebrowser PID=$! port=8080"
fi

if command -v ttyd >/dev/null 2>&1; then
    ttyd -p 7681 -W -t titleFixed="pod-${POD_ID}" bash \
        > "$VOLUME_LOG_DIR/ttyd-${POD_ID}.log" 2>&1 &
    echo "ttyd PID=$! port=7681"
fi

# Heartbeat loop — external observer detects live pods
(while true; do
    date -u +%s > "$VOLUME_LOG_DIR/heartbeat-${POD_ID}"
    sleep 30
done) &

# Log rotation — prevent Volume fill from crash loops
OIS_LOG_TTL_DAYS="${OIS_LOG_TTL_DAYS:-7}"
(while true; do
    sleep 21600  # 6h
    find "$VOLUME_LOG_DIR" -type f -mtime +"$OIS_LOG_TTL_DAYS" -delete 2>/dev/null || true
done) &

# === STAGE 3: Application (becomes container's exit-code authority) ===
exec python /opt/comfyui-api/handler.py
```

`exec` replaces the shell process with `handler.py`. The handler becomes a direct child of `tini`, receives signals correctly, and its exit code propagates to the RunPod scheduler. The diagnostic background processes remain running until the container terminates, giving a debugger time to connect after a handler crash.

---

## Handler Crash Guard: sys.excepthook + atexit + O_APPEND Index

The `runpod-python` SDK has documented bugs where raised exceptions are not reliably translated to `FAILED` job status (issues #309, #459). Wrap the handler with explicit hooks installed **before** risky imports.

```python
# /opt/comfyui-api/handler.py
import os
import sys
import traceback
import atexit
import json
import time
from pathlib import Path

POD_ID = os.environ.get("RUNPOD_POD_ID", f"pod-{os.uname().nodename}-{int(time.time())}")
VOLUME_LOG_DIR = Path(os.environ.get("OIS_VOLUME_ROOT", "/workspace")) / "logs"
TRACEBACK_FILE = VOLUME_LOG_DIR / f"handler-{POD_ID}.traceback"
ATEXIT_FILE    = VOLUME_LOG_DIR / f"handler-{POD_ID}.atexit"
INDEX_FILE     = VOLUME_LOG_DIR / "_index.jsonl"


def _write_traceback(exc_type, exc_value, exc_tb):
    """Persist traceback to Volume before process exits. Called from excepthook and catch-all."""
    try:
        VOLUME_LOG_DIR.mkdir(parents=True, exist_ok=True)
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        with open(TRACEBACK_FILE, "w") as f:
            f.write(f"=== {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} pod={POD_ID} ===\n")
            f.write(tb_str)
            f.flush()
            os.fsync(f.fileno())   # force write to NFS backend before crash
    except Exception as inner:
        print(f"FATAL: failed to write traceback: {inner}", file=sys.stderr)


def _excepthook(exc_type, exc_value, exc_tb):
    _write_traceback(exc_type, exc_value, exc_tb)
    sys.__excepthook__(exc_type, exc_value, exc_tb)  # also print to stderr


def _atexit_marker():
    """Clean exit marker. If .atexit absent and .exit non-zero: SIGKILL or OOM."""
    try:
        with open(ATEXIT_FILE, "w") as f:
            f.write(json.dumps({"pod": POD_ID, "ts": time.time(), "ok": True}))
    except Exception:
        pass


def _index_append(event: dict):
    """O_APPEND write to shared JSONL index. Safe for concurrent appends if line < 4 KB."""
    try:
        line = json.dumps({**event, "pod": POD_ID, "ts": time.time()}) + "\n"
        fd = os.open(str(INDEX_FILE), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
        os.write(fd, line.encode())
        os.close(fd)
    except Exception:
        pass


# Install hooks BEFORE any risky import
sys.excepthook = _excepthook
atexit.register(_atexit_marker)
_index_append({"event": "startup_begin"})

try:
    import runpod
    # ... other imports ...
except Exception as e:
    _write_traceback(type(e), e, e.__traceback__)
    _index_append({"event": "import_failed", "error": str(e)})
    raise  # excepthook fires, then process exits

_index_append({"event": "startup_done"})


def handler(job):
    try:
        _index_append({"event": "job_start", "job_id": job.get("id")})
        result = do_work(job)
        _index_append({"event": "job_done", "job_id": job.get("id")})
        return result
    except Exception as e:
        tb = traceback.format_exc()
        _write_traceback(type(e), e, e.__traceback__)
        _index_append({"event": "job_failed", "job_id": job.get("id"), "error": str(e)})
        # Return dict instead of raise — more reliable FAILED propagation (SDK bug #309)
        return {"error": str(e), "traceback": tb}


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
```

---

## Post-Mortem State Machine: Reading Marker Files

A debugger on any live pod sharing the same Volume can classify a crashed pod's failure mode from the marker files alone, without access to RunPod Console.

| `.log` | `.traceback` | `.atexit` | `.exit` rc | Diagnosis |
|---|---|---|---|---|
| Exists, non-empty | Empty | Absent | Non-zero | Entrypoint died at Stage 0-1 (before handler launched) |
| Exists | Non-empty | Absent | Non-zero | Handler raised uncaught exception (excepthook fired) |
| Exists | Empty | Absent | Non-zero | SIGKILL or OOM — no Python cleanup ran |
| Exists | Empty | Exists | 0 | Clean drain — worker exited normally |
| Absent | — | — | — | Volume not mounted, or Stage 0 mkdir failed |

**Debug session workflow** from any live pod on the same Volume:

```bash
# List all pods with log files
ls /workspace/logs/handler-*.log 2>/dev/null | head -20

# Find pods that crashed (non-empty traceback)
for tb in /workspace/logs/handler-*.traceback; do
    [ -s "$tb" ] && printf "\n=== %s ===\n" "$tb" && head -30 "$tb"
done

# Read full log of a specific pod
less /workspace/logs/handler-pod-XXXXX.log

# Check exit code
cat /workspace/logs/handler-pod-XXXXX.exit

# Check startup env
grep -v "^#" /workspace/logs/handler-pod-XXXXX.env

# Correlate event timeline across all pods
jq -r '[.ts, .pod, .event, .job_id, .error] | @tsv' /workspace/logs/_index.jsonl \
    | sort | tail -50

# Identify live pods via heartbeat freshness (stale if > 60s)
now=$(date +%s)
for hb in /workspace/logs/heartbeat-*; do
    ts=$(cat "$hb" 2>/dev/null)
    [ -n "$ts" ] && age=$((now - ts)) && echo "$age s  $hb"
done | sort -n
```

If the debug pod has filebrowser running, the entire `/workspace/logs/` tree is browsable via `https://<pod-id>-8080.proxy.runpod.net/` without SSH.

---

## Deployment Strategy: Debug vs Production Endpoints

Do not deploy the diagnostic image to the production endpoint — it adds 100 MB and slightly increases cold-start. Use one of:

1. **Separate debug endpoint** (`workersMin=0`, `idleTimeout=300`) with the debug image. Spin up on-demand during incident investigation; delete when done.
2. **Temporary template swap** on the production endpoint: patch `imageName` to the debug tag, wait for a worker to spawn, investigate, revert. Requires care — workers spawned during the swap window have the debug image.
3. **Pod-mode debug pod** on the same Volume: spin up a Pod (not Serverless) with the debug image and the same `networkVolumeId`. The Pod has persistent SSH/filebrowser/ttyd. Read crashed Serverless workers' logs from `/workspace/logs/`.

Option 3 is the safest for production: the debug pod is isolated from the job dispatch queue and can remain running as a standing debugger without affecting Serverless worker scaling.

**Example endpoint creation** (debug endpoint, not production):

```bash
curl -s -X POST "https://rest.runpod.io/v1/endpoints" \
  -H "Authorization: Bearer $RUNPOD_API_KEY_OIS" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ois-comfyui-debug",
    "templateId": "<debug-template-id>",
    "gpuTypeIds": ["NVIDIA H100 PCIe"],
    "networkVolumeId": "nrdo9nagku",
    "dataCenterIds": ["US-KS-2"],
    "workersMin": 0,
    "workersMax": 1,
    "idleTimeout": 300,
    "flashboot": false,
    "scalerType": "QUEUE_DELAY",
    "scalerValue": 4,
    "gpuCount": 1,
    "computeType": "GPU"
  }'
```

Delete the debug endpoint when the investigation is complete — idle Serverless endpoints with `workersMin=0` cost nothing, but leaving them clutters the dashboard and may confuse future sessions.

---

## Gotchas

- **Issue:** `set -euo pipefail` in the entrypoint kills observability if filebrowser or ttyd fails to start (binary missing or port conflict). → **Fix:** Use `set -uo pipefail` without `-e`; wrap each service start with `if command -v <binary> >/dev/null 2>&1; then ... fi` so failures are logged and skipped, not fatal.

- **Issue:** Concurrent writes to `_index.jsonl` from multiple pods corrupt data when any single write exceeds one NFS block (typically 4 KB). → **Fix:** Keep each `_index_append()` call's JSON payload under 500 bytes. Truncate `error` fields: `"error": str(e)[:200]`.

- **Issue:** The `handler-{pod_id}.atexit` marker is absent even on clean exits if `atexit.register()` is called after a module-level exception silently swallows the error. → **Fix:** Install `atexit.register(_atexit_marker)` and `sys.excepthook = _excepthook` as the very first lines of `handler.py`, before any import that could fail.

- **Issue:** SSH authorized_keys copied from Volume have wrong permissions if the Volume NFS backend strips `chmod 600`. The sshd refuses to start. → **Fix:** Always run `chmod 600 /root/.ssh/authorized_keys` explicitly after the `cp`; add `StrictModes no` to `sshd_config` as a fallback for permission-stripped NFS mounts.

- **Issue:** The heartbeat file becomes stale when the heartbeat loop's parent shell exits due to a signal, leaving the last timestamp frozen. External logic may conclude the pod is still alive. → **Fix:** Use the RunPod `/health` API endpoint as the authoritative liveness check; treat the heartbeat file as a secondary indicator only.

- **Issue:** Log files accumulate indefinitely on the Volume when workers crash-loop. At 1 MB/crash × 1000 crashes, the Volume fills before the TTL cleanup loop runs. → **Fix:** Set `OIS_LOG_TTL_DAYS=1` for crash-loop investigations; run `find /workspace/logs -type f -mtime +1 -delete` manually after a known bad deploy.

---

## See Also

- [[runpod-serverless-silent-worker-crashes-on-task-pickup]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-production]]
- [[comfyui-container-build]]
