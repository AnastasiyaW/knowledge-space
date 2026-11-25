---
level: 3
source_sha256: c73e84bf431e8eb45d7c197d2af41cfeab41a51a3ce68794196fc04bbaa5e3b5
translation: machine
translated_at: '2026-10-24'
---
# RunPod Serverless-Diagnose-Image: SSH, Filebrowser, TTY und pod-übergreifendes Log-Sharing {#runpod-serverless-diagnostic-image-ssh-filebrowser-tty-and-cross-pod-log-sharing}

Serverless-Worker sterben stillschweigend. Die RunPod Console erfasst nur, was der Prozess vor dem Beenden ausgibt, Log-Rotation kürzt die Logs, und sobald ein Container beendet ist, ist sein flüchtiges Dateisystem verloren. Dieser Artikel beschreibt eine mehrschichtige Diagnoseoberfläche, die den Tod eines Workers überdauert: pro Pod eine Log-Datei auf einem Network Volume, Observability-Dienste vor dem Handler (sshd, filebrowser, ttyd), ein Crash-Guard-Muster im Handler und eine Post-Mortem-Zustandsmaschine auf Basis von Marker-Dateien.

Begleitend zu: Ursachenanalyse für stille Abstürze, Python-Silent-Exit-Fallen.

---

## Semantik des geteilten Volumes über mehrere Pods {#volume-cross-pod-sharing-semantics}

RunPod Network Volumes sind gemeinsam genutzter Speicher im NFS-Stil. Mehrere Serverless-Worker können dasselbe Volume gleichzeitig einbinden (Einschränkung auf dasselbe Rechenzentrum, regionsgebunden). Die grundlegende Einschränkung: **`flock()` funktioniert auf NFS nicht zuverlässig, und `fcntl` ist ebenfalls unzuverlässig**. Gleichzeitige Schreibzugriffe auf dieselbe Datei beschädigen sie.

Architekturprinzip: **eine Datei pro Pod, das gemeinsame Volume als Speicher mit vielen Lesern**.

| Eigenschaft | Verhalten | Auswirkung |
|---|---|---|
| Gleichzeitige Lesezugriffe | Sicher | Jeder laufende Pod kann die Logs jedes abgestürzten Pods lesen |
| Gleichzeitige Schreibzugriffe auf unterschiedliche Dateien | Sicher | Pro-Pod-Benennung eliminiert Konkurrenz |
| Gleichzeitige Schreibzugriffe auf dieselbe Datei | Beschädigung | Für alle veränderlichen Zustände verboten |
| Anhängen per `O_APPEND` an JSONL | Relativ sicher bei Schreibvorgängen < 4 KB | Auf den meisten NFS-Implementierungen atomar |
| fsync-Garantie | Schwach | Explizites `os.fsync()` vor einem Absturz erforderlich |
| POSIX-Berechtigungen | Auf den meisten RunPod-Backends ignoriert | Keine Secrets in Dateien speichern |
| Same-DC-Einschränkung | Durchgesetzt | Regionsübergreifende Log-Aggregation erfordert einen externen Shipper |

**Mount-Pfade des Volumes**: `/runpod-volume` in Serverless; `/workspace` im Pod-Modus (Konvention über `OIS_VOLUME_ROOT=/workspace`).

**Dateilayout pro Pod**:

```text
/workspace/logs/
├── handler-${RUNPOD_POD_ID}.log         # full stdout+stderr from entrypoint start
├── handler-${RUNPOD_POD_ID}.traceback   # uncaught exception (sys.excepthook)
├── handler-${RUNPOD_POD_ID}.env         # startup env dump, secrets redacted
├── handler-${RUNPOD_POD_ID}.exit        # exit code + timestamp (bash EXIT trap)
├── handler-${RUNPOD_POD_ID}.atexit      # written by Python atexit; absence = crash/SIGKILL
├── heartbeat-${RUNPOD_POD_ID}           # unix timestamp, refreshed every 30s
└── _index.jsonl                         # append-only registry, one line per event
```

Die Datei `_index.jsonl` verwendet `O_APPEND`-Schreibvorgänge mit weniger als 4 KB pro Zeile. Sie ist kein Ersatz für eine Nachrichtenwarteschlange, sondern ein Diagnoseregister zur Korrelation von Ereignissen über mehrere Pods hinweg.

---

## Diagnose-Image: Dockerfile-Schicht {#diagnostic-image-dockerfile-layer}

Diese Schicht am Ende des Produktions-Overlay-Dockerfiles hinzufügen, nach `COPY handler.py`. Sie erhöht ein 23-GB-Basisimage um etwa 80–120 MB, was ein vertretbarer Aufwand ist.

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

**SSH-`authorized_keys`** werden zur Laufzeit vom Volume geladen und nicht ins Image eingebacken, sodass Schlüssel ohne Neubau rotiert werden können:

```bash
cp /workspace/authorized_keys /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
```

**Warum Einzelbinärdateien statt apt für filebrowser/ttyd**: Versionspinning über `ARG`, keine transitiven Abhängigkeiten, kleinere Layer-Differenzen in GHCR.

**Warum kein supervisord**: supervisord startet abgestürzte Prozesse automatisch neu. Ein Handler in einer Crash-Schleife meldet dem RunPod-Scheduler dadurch nie `FAILED`, und die Warteschlange stockt. Außerdem werden Exit-Codes verschluckt. Bash-Hintergrundprozesse mit `exec handler.py` (siehe unten) leiten Exit-Codes korrekt weiter.

---

## Dreistufiger Entrypoint: Observability vor dem Handler {#three-stage-entrypoint-observability-before-the-handler}

Der entscheidende Fehler naiver Entrypoints: Die Observability startet **nach** ComfyUI oder dem Handler. Scheitert einer von beiden beim Start, werden die Debug-Dienste nie gestartet. Deshalb wird der Ablauf in drei explizite Stufen aufgeteilt.

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

`exec` ersetzt den Shell-Prozess durch `handler.py`. Der Handler wird damit direktes Kindprozess von `tini`, empfängt Signale korrekt, und sein Exit-Code wird an den RunPod-Scheduler weitergegeben. Die diagnostischen Hintergrundprozesse laufen weiter, bis der Container beendet wird, sodass ein Debugger nach einem Handler-Absturz Zeit hat, sich zu verbinden.

---

## Crash-Guard im Handler: sys.excepthook + atexit + O_APPEND-Index {#handler-crash-guard-sysexcepthook-atexit-o_append-index}

Das `runpod-python`-SDK weist dokumentierte Fehler auf, bei denen ausgelöste Exceptions nicht zuverlässig in den Job-Status `FAILED` übersetzt werden (Issues #309, #459). Den Handler daher mit expliziten Hooks umschließen, die **vor** riskanten Imports installiert werden.

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

## Post-Mortem-Zustandsmaschine: Marker-Dateien lesen {#post-mortem-state-machine-reading-marker-files}

Ein Debugger auf einem laufenden Pod, der dasselbe Volume nutzt, kann den Fehlermodus eines abgestürzten Pods allein anhand der Marker-Dateien klassifizieren, ohne Zugriff auf die RunPod Console.

| `.log` | `.traceback` | `.atexit` | `.exit`-rc | Diagnose |
|---|---|---|---|---|
| Vorhanden, nicht leer | Leer | Fehlt | Ungleich null | Entrypoint ist in Stufe 0–1 beendet worden (bevor der Handler gestartet wurde) |
| Vorhanden | Nicht leer | Fehlt | Ungleich null | Handler hat eine nicht abgefangene Exception ausgelöst (excepthook hat gegriffen) |
| Vorhanden | Leer | Fehlt | Ungleich null | SIGKILL oder OOM — keine Python-Bereinigung ausgeführt |
| Vorhanden | Leer | Vorhanden | 0 | Sauberes Abarbeiten — Worker wurde regulär beendet |
| Fehlt | — | — | — | Volume nicht eingebunden oder mkdir in Stufe 0 fehlgeschlagen |

**Debug-Sitzung** von einem laufenden Pod auf demselben Volume aus:

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

Wenn auf dem Debug-Pod filebrowser läuft, ist der gesamte Verzeichnisbaum `/workspace/logs/` über `https://<pod-id>-8080.proxy.runpod.net/` ohne SSH durchsuchbar.

---

## Deployment-Strategie: Debug- vs. Produktions-Endpoints {#deployment-strategy-debug-vs-production-endpoints}

Das Diagnose-Image nicht auf dem Produktions-Endpoint deployen: Es fügt 100 MB hinzu und verlängert den Kaltstart leicht. Stattdessen eine der folgenden Optionen verwenden:

1. **Separater Debug-Endpoint** (`workersMin=0`, `idleTimeout=300`) mit dem Debug-Image. Bei Bedarf während einer Incident-Untersuchung hochfahren; danach löschen.
2. **Temporärer Template-Tausch** auf dem Produktions-Endpoint: `imageName` auf den Debug-Tag patchen, warten, bis ein Worker startet, untersuchen, zurücksetzen. Erfordert Sorgfalt, denn Worker, die während des Tauschfensters gestartet werden, laufen mit dem Debug-Image.
3. **Debug-Pod im Pod-Modus** auf demselben Volume: einen Pod (nicht Serverless) mit dem Debug-Image und derselben `networkVolumeId` starten. Der Pod bietet dauerhaft SSH/filebrowser/ttyd. Die Logs abgestürzter Serverless-Worker werden aus `/workspace/logs/` gelesen.

Option 3 ist für die Produktion am sichersten: Der Debug-Pod ist von der Job-Dispatch-Warteschlange isoliert und kann als dauerhafter Debugger laufen, ohne die Skalierung der Serverless-Worker zu beeinflussen.

**Beispiel für die Erstellung eines Endpoints** (Debug-Endpoint, nicht Produktion):

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

Den Debug-Endpoint nach Abschluss der Untersuchung löschen. Inaktive Serverless-Endpoints mit `workersMin=0` kosten zwar nichts, belegen aber das Dashboard und können künftige Sitzungen verwirren.

---

## Stolperfallen {#gotchas}

- **Problem:** `set -euo pipefail` im Entrypoint beendet die Observability, wenn filebrowser oder ttyd nicht starten (Binary fehlt oder Portkonflikt). → **Lösung:** `set -uo pipefail` ohne `-e` verwenden; jeden Dienststart mit `if command -v <binary> >/dev/null 2>&1; then ... fi` umschließen, damit Fehler protokolliert und übersprungen werden, statt fatal zu sein.

- **Problem:** Gleichzeitige Schreibzugriffe von mehreren Pods auf `_index.jsonl` beschädigen Daten, sobald ein einzelner Schreibvorgang einen NFS-Block überschreitet (typischerweise 4 KB). → **Lösung:** Die JSON-Nutzlast jedes Aufrufs von `_index_append()` unter 500 Byte halten. Felder `error` kürzen: `"error": str(e)[:200]`.

- **Problem:** Der Marker `handler-{pod_id}.atexit` fehlt auch bei sauberen Beendigungen, wenn `atexit.register()` erst aufgerufen wird, nachdem ein Fehler auf Modulebene den Fehler stillschweigend verschluckt hat. → **Lösung:** `atexit.register(_atexit_marker)` und `sys.excepthook = _excepthook` als allererste Zeilen in `handler.py` installieren, vor jedem Import, der fehlschlagen könnte.

- **Problem:** Vom Volume kopierte SSH-`authorized_keys` haben falsche Berechtigungen, wenn das NFS-Backend `chmod 600` entfernt. sshd weigert sich zu starten. → **Lösung:** Nach dem `cp` immer explizit `chmod 600 /root/.ssh/authorized_keys` ausführen; als Fallback für NFS-Mounts, die Berechtigungen entfernen, `StrictModes no` in `sshd_config` setzen.

- **Problem:** Die Heartbeat-Datei wird veraltet, wenn die Shell der Heartbeat-Schleife durch ein Signal beendet wird, und der letzte Zeitstempel bleibt eingefroren. Externe Logik könnte daraus schließen, dass der Pod noch lebt. → **Lösung:** Den RunPod-API-Endpoint `/health` als maßgebliche Liveness-Prüfung verwenden; die Heartbeat-Datei nur als sekundären Indikator behandeln.

- **Problem:** Log-Dateien sammeln sich auf dem Volume unbegrenzt an, wenn Worker in Crash-Schleifen geraten. Bei 1 MB pro Absturz × 1000 Abstürze ist das Volume voll, bevor die TTL-Bereinigungsschleife läuft. → **Lösung:** Für Untersuchungen von Crash-Schleifen `OIS_LOG_TTL_DAYS=1` setzen; nach einem bekannten fehlerhaften Deployment manuell `find /workspace/logs -type f -mtime +1 -delete` ausführen.

---

## Siehe auch {#see-also}

- [[runpod-serverless-silent-worker-crashes-on-task-pickup]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-production]]
- [[comfyui-container-build]]
