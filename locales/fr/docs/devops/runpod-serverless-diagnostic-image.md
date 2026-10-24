---
level: 3
source_sha256: c73e84bf431e8eb45d7c197d2af41cfeab41a51a3ce68794196fc04bbaa5e3b5
translation: machine
translated_at: '2026-10-24'
---
# Image de diagnostic RunPod Serverless : SSH, Filebrowser, TTY et partage de logs entre pods {#runpod-serverless-diagnostic-image-ssh-filebrowser-tty-and-cross-pod-log-sharing}

Les workers Serverless meurent silencieusement. La console RunPod ne capture que ce que le processus émet avant de se terminer, la rotation des logs les tronque, et une fois le conteneur arrêté, son système de fichiers éphémère disparaît. Cet article décrit une surface de diagnostic en couches qui survit à la mort du worker : fichiers de log par pod sur un Network Volume, services d'observabilité lancés avant le handler (sshd, filebrowser, ttyd), un motif de garde-fou contre les crashs dans le handler, et une machine d'état post-mortem basée sur des fichiers marqueurs.

Article complémentaire : analyse des causes racines des crashs silencieux, pièges de sortie silencieuse de Python.

---

## Sémantique du partage de Volume entre pods {#volume-cross-pod-sharing-semantics}

Les Network Volumes RunPod sont un stockage partagé de type NFS. Plusieurs workers Serverless peuvent monter le même Volume simultanément (contrainte de même datacenter, verrouillage par région). Limitation fondamentale : **flock() ne fonctionne pas de manière fiable sur NFS, et fcntl est peu fiable**. Des écritures concurrentes dans le même fichier le corrompront.

Principe d'architecture : **un fichier par pod, Volume partagé comme stockage en lecture massive**.

| Propriété | Comportement | Conséquence |
|---|---|---|
| Lectures concurrentes | Sûres | Tout pod vivant peut lire les logs d'un pod crashé |
| Écritures concurrentes dans des fichiers distincts | Sûres | Le nommage par pod élimine la contention |
| Écritures concurrentes dans le même fichier | Corruption | Interdit pour tout état mutable |
| Ajout via `O_APPEND` dans du JSONL | Relativement sûr si les écritures font < 4 Ko | Atomique sur la plupart des implémentations NFS |
| Garantie fsync | Faible | `os.fsync()` explicite requis avant un crash |
| Permissions POSIX | Ignorées sur la plupart des backends RunPod | Ne pas stocker de secrets dans les fichiers |
| Contrainte de même DC | Appliquée | L'agrégation de logs inter-régions nécessite un expéditeur externe |

**Chemins de montage du Volume** : `/runpod-volume` en Serverless ; `/workspace` en mode Pod (convention via `OIS_VOLUME_ROOT=/workspace`).

**Disposition des fichiers par pod** :

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

Le fichier `_index.jsonl` utilise des écritures `O_APPEND` de moins de 4 Ko par ligne. Ce n'est pas un substitut de file de messages : c'est un registre de diagnostic permettant de corréler les événements entre pods.

---

## Couche Dockerfile de l'image de diagnostic {#diagnostic-image-dockerfile-layer}

Ajoutez cette couche à la fin du Dockerfile de l'overlay de production, après `COPY handler.py`. Elle ajoute environ 80 à 120 Mo à une base de 23 Go, surcoût acceptable.

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

**Les `authorized_keys` SSH** sont chargées depuis le Volume à l'exécution, et non intégrées dans l'image : les clés peuvent être renouvelées sans reconstruction.

```bash
cp /workspace/authorized_keys /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
```

**Pourquoi un binaire unique plutôt qu'apt pour filebrowser/ttyd** : épinglage de version via `ARG`, aucune dépendance transitive, diffs de couches plus petits dans GHCR.

**Pourquoi pas supervisord** : supervisord relance automatiquement les processus crashés, ce qui signifie qu'un handler en boucle de crash ne remonte jamais `FAILED` au planificateur RunPod : la file d'attente se bloque. Il avale également les codes de sortie. Les processus d'arrière-plan bash avec `exec handler.py` (voir ci-dessous) transmettent correctement les codes de sortie.

---

## Entrypoint en trois étapes : l'observabilité avant le handler {#three-stage-entrypoint-observability-before-the-handler}

Le défaut critique des entrypoints naïfs : l'observabilité démarre **après** ComfyUI ou le handler. Si l'un des deux échoue au démarrage, les services de débogage ne se lancent jamais. Restructurez en trois étapes explicites.

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

`exec` remplace le processus shell par `handler.py`. Le handler devient un enfant direct de `tini`, reçoit correctement les signaux, et son code de sortie remonte au planificateur RunPod. Les processus de diagnostic en arrière-plan restent actifs jusqu'à la fin du conteneur, laissant au débogueur le temps de se connecter après un crash du handler.

---

## Garde-fou contre les crashs du handler : sys.excepthook + atexit + index O_APPEND {#handler-crash-guard-sysexcepthook-atexit-o_append-index}

Le SDK `runpod-python` présente des bugs documentés où les exceptions levées ne sont pas traduites de manière fiable en statut de job `FAILED` (issues #309, #459). Enveloppez le handler avec des hooks explicites installés **avant** les imports risqués.

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

## Post-mortem : lecture des fichiers marqueurs {#post-mortem-state-machine-reading-marker-files}

Un débogueur sur n'importe quel pod vivant partageant le même Volume peut classifier le mode de défaillance d'un pod crashé à partir des seuls fichiers marqueurs, sans accès à la console RunPod.

| `.log` | `.traceback` | `.atexit` | Code retour `.exit` | Diagnostic |
|---|---|---|---|---|
| Existe, non vide | Vide | Absent | Non nul | L'entrypoint est mort aux étapes 0-1 (avant le lancement du handler) |
| Existe | Non vide | Absent | Non nul | Le handler a levé une exception non interceptée (excepthook déclenché) |
| Existe | Vide | Absent | Non nul | SIGKILL ou OOM : aucun nettoyage Python n'a été exécuté |
| Existe | Vide | Existe | 0 | Vidange propre : le worker s'est terminé normalement |
| Absent | — | — | — | Volume non monté, ou échec du `mkdir` de l'étape 0 |

**Workflow de session de débogage** depuis tout pod vivant sur le même Volume :

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

Si le pod de débogage exécute filebrowser, l'arborescence complète `/workspace/logs/` est consultable via `https://<pod-id>-8080.proxy.runpod.net/` sans SSH.

---

## Stratégie de déploiement : endpoints de débogage et de production {#deployment-strategy-debug-vs-production-endpoints}

Ne déployez pas l'image de diagnostic sur l'endpoint de production : elle ajoute 100 Mo et augmente légèrement le démarrage à froid. Utilisez l'une des options suivantes :

1. **Endpoint de débogage séparé** (`workersMin=0`, `idleTimeout=300`) avec l'image de débogage. Lancez-le à la demande pendant une investigation d'incident, supprimez-le une fois terminé.
2. **Remplacement temporaire du template** sur l'endpoint de production : modifiez `imageName` pour pointer vers le tag de débogage, attendez qu'un worker apparaisse, investiguez, puis revenez en arrière. Nécessite de la prudence : les workers créés pendant la fenêtre de remplacement utilisent l'image de débogage.
3. **Pod de débogage en mode Pod** sur le même Volume : lancez un Pod (et non un Serverless) avec l'image de débogage et le même `networkVolumeId`. Le Pod dispose d'SSH, filebrowser et ttyd persistants. Lisez les logs des workers Serverless crashés depuis `/workspace/logs/`.

L'option 3 est la plus sûre pour la production : le pod de débogage est isolé de la file de dispatch des jobs et peut rester actif comme débogueur permanent sans affecter la mise à l'échelle des workers Serverless.

**Exemple de création d'endpoint** (endpoint de débogage, pas de production) :

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

Supprimez l'endpoint de débogage une fois l'investigation terminée : les endpoints Serverless inactifs avec `workersMin=0` ne coûtent rien, mais les laisser encombre le tableau de bord et peut troubler les sessions suivantes.

---

## Pièges courants {#gotchas}

- **Problème :** `set -euo pipefail` dans l'entrypoint tue l'observabilité si filebrowser ou ttyd ne démarre pas (binaire manquant ou conflit de port). → **Correctif :** Utilisez `set -uo pipefail` sans `-e` ; encadrez chaque démarrage de service avec `if command -v <binary> >/dev/null 2>&1; then ... fi` afin que les échecs soient journalisés et ignorés, non fatals.

- **Problème :** Les écritures concurrentes dans `_index.jsonl` depuis plusieurs pods corrompent les données dès qu'une écriture unique dépasse un bloc NFS (généralement 4 Ko). → **Correctif :** Limitez la charge JSON de chaque appel `_index_append()` à 500 octets. Tronquez les champs `error` : `"error": str(e)[:200]`.

- **Problème :** Le marqueur `handler-{pod_id}.atexit` est absent même lors de sorties propres si `atexit.register()` est appelé après qu'une exception au niveau du module a silencieusement avalé l'erreur. → **Correctif :** Installez `atexit.register(_atexit_marker)` et `sys.excepthook = _excepthook` comme toutes premières lignes de `handler.py`, avant tout import susceptible d'échouer.

- **Problème :** Les `authorized_keys` SSH copiées depuis le Volume ont de mauvaises permissions si le backend NFS du Volume retire `chmod 600`. sshd refuse de démarrer. → **Correctif :** Exécutez toujours explicitement `chmod 600 /root/.ssh/authorized_keys` après le `cp` ; ajoutez `StrictModes no` dans `sshd_config` comme solution de repli pour les montages NFS dont les permissions sont retirées.

- **Problème :** Le fichier de heartbeat devient obsolète lorsque le shell parent de la boucle de heartbeat se termine à cause d'un signal, figeant le dernier horodatage. Une logique externe peut conclure à tort que le pod est encore vivant. → **Correctif :** Utilisez l'endpoint d'API `/health` de RunPod comme vérification de vie de référence ; ne considérez le fichier de heartbeat que comme indicateur secondaire.

- **Problème :** Les fichiers de log s'accumulent indéfiniment sur le Volume lorsque les workers entrent en boucle de crash. À 1 Mo par crash × 1000 crashs, le Volume se remplit avant l'exécution de la boucle de nettoyage TTL. → **Correctif :** Définissez `OIS_LOG_TTL_DAYS=1` pour les investigations de boucles de crash ; exécutez manuellement `find /workspace/logs -type f -mtime +1 -delete` après un déploiement défectueux connu.

---

## Voir aussi {#see-also}

- [[runpod-serverless-silent-worker-crashes-on-task-pickup]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-production]]
- [[comfyui-container-build]]
