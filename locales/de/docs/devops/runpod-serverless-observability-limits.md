---
level: 3
source_sha256: 9be7fd85a4e59a5fb8509f2e624f544c7b933fc9e042ee3a98daa4064891fcc1
translation: machine
translated_at: '2026-10-24'
---
# RunPod Serverless Observability: Warum sie undurchsichtig ist und wie man damit arbeitet {#runpod-serverless-observability-why-its-opaque-and-how-to-work-around-it}

## Fünf architektonische Ursachen der Undurchsichtigkeit {#five-architectural-causes-of-opacity}

RunPod-Serverless-Worker sind schwer zu debuggen, nicht weil ein einzelnes Feature fehlt, sondern weil fünf voneinander unabhängige Architekturschichten jeweils eine Kategorie von Observability ausschließen.

**Ursache 1: Community-Cloud-Host-Modell.**
Worker laufen als gewöhnliche Docker-Container unter einem Standard-Docker-Daemon auf Peer-to-Peer-Hostrechnern von Drittanbietern. RunPod besitzt diese Maschinen nicht. Da sich auf jedem Host kein privilegierter Control-Plane-Agent garantiert betreiben lässt, können sie `docker exec`, `docker logs --follow` oder jeden anderen Exec-Kanal nicht sicher an Kunden weiterleiten. Modal besitzt seine gesamte Firecracker-microVM-Flotte, weshalb `modal shell <container-id>` funktioniert: Die API-Server fordern über den jailer/agent-ttrpc-Pfad einen Exec-Kanal in eine bestimmte microVM an. Das entsprechende Pfad-Gegenstück existiert bei RunPod nicht.

**Ursache 2: Keine eingehende Proxy-Identität für Serverless-Worker.**
Der Pod-Modus weist jedem Container eine routbare Identität zu: `https://[POD_ID]-[PORT].proxy.runpod.net` plus einer SSH-TCP-Zuordnung. Serverless-Worker haben in diesem Sinne keine `POD_ID`. Sie erhalten Arbeit ausschließlich aus der RunPod-Scheduler-Queue; eingehender Netzwerkverkehr von außerhalb dieses Schedulers wird nicht weitergeleitet. Eine Erweiterung des Pod-Proxys auf Serverless würde für jeden kurzlebigen Worker eine eindeutige routbare Identität und einen zustandsbehafteten Proxy-Eintrag erfordern, also eine Infrastrukturkost, die RunPod bisher nicht übernommen hat.

**Ursache 3: Der Log-Shipper wird erst nach dem Status „ready“ angebunden.**
Die Log-Pipeline sieht so aus: Worker-stdout → Docker-JSON-Log-Datei auf dem Host → ein promtail-artiger Shipper, der auf diesem Host läuft → zentraler Log-Speicher → Console UI über eine interne Admin-API. Der Shipper hängt sich erst an einen Container, nachdem dieser in den Status `ready` übergegangen ist. Ein Worker, der während des Modulimports abstürzt, bevor `runpod.serverless.start()` zurückkehrt, erreicht `ready` nie, daher wird der Shipper nie angebunden. Dieser Worker erzeugt somit keine einzige Logzeile, die in der Console UI oder über eine API sichtbar wäre. Das wurde empirisch bestätigt (AnswerOverflow [#1295692391411355668](https://www.answeroverflow.com/m/1295692391411355668)) sowie im runpod-python-Issue [#29](https://github.com/runpod/runpodctl/issues/29).

**Ursache 4: `PYTHONUNBUFFERED` ist in Basis-Images nicht gesetzt.**
Python puffert stdout standardmäßig in Blöcken von etwa 4 KB. Bei einem `SIGKILL` (OOM-Kill, Scheduler-Timeout) geht der noch nicht geschriebene Puffer verloren: Der Prozess wird beendet, bevor `sys.stdout.flush()` ausgeführt wird. Selbst wenn der Log-Shipper angebunden ist, erhält er unter Umständen nie den letzten Traceback. Wer mit `-u` (`python -u handler.py`) arbeitet oder `ENV PYTHONUNBUFFERED=1` im Dockerfile setzt, sorgt dafür, dass jeder `write()`-Systemaufruf sofort in die Docker-JSON-Log-Datei geschrieben wird. Der Shipper hat dadurch die Chance, die Absturzmeldung zu erfassen, bevor der Prozess verschwindet.

**Ursache 5: Die Log-API ist eine bestätigte Lücke, keine Dokumentationslücke.**
Eine systematische Prüfung aller kundenzugänglichen API-Oberflächen bestätigt, dass kein Log-Abruf-Endpunkt existiert:

| Oberfläche | Ergebnis |
|---|---|
| [GraphQL-Public-Spec](https://graphql-spec.runpod.io/) | Keine Log-Abfragen; nur `cpuTypes`, `gpuTypes`, `myself`, `pod` (GPU-Telemetrie) |
| REST-API (`rest.runpod.io/v1`) | Endpoints, Templates, Volumes, GPU-Typen; keine Log-Ressourcen |
| Serverless-API (`api.runpod.ai/v2/<id>/`) | `run`, `runsync`, `status`, `cancel`, `health`; keine Log-Ressourcen |
| `runpodctl`-CLI ([vollständige Befehlsreferenz](https://github.com/runpod/runpodctl/blob/main/docs/runpodctl.md)) | `pod`, `serverless`, `template`, `model`, `network-volume`, `registry`, `ssh`, `send`, `receive`, `doctor`; keine Subcommands `logs`, `exec`, `shell` oder `attach` |
| runpod-python-SDK-Quellcode | Kein clientseitiges Log-Streaming |
| [runpod-python-Issue #400](https://github.com/runpod/runpod-python/issues/400) | Seit 2024 offen, keine Antwort des RunPod-Teams, kein Assignee, kein PR |
| [runpodctl-Issue #29](https://github.com/runpod/runpodctl/issues/29) | Seit März 2023 offen, seit 3 Jahren keine Aktivität von Maintainern |

Der Workers-Tab der Console UI lädt Logs von einem internen Admin-Endpunkt (vermutlich `wss://api.runpod.io/ws/workers/<uuid>/logs` oder ähnlich), der ein Admin-JWT erfordert, das Kunden nicht ausgestellt wird. Dabei handelt es sich nicht um einen versteckten, undokumentierten Pfad, sondern um reine Admin-Infrastruktur.

---

## Plattformvergleich {#platform-comparison}

| Fähigkeit | RunPod Serverless | Modal | Replicate (Cog) | Beam | AWS Lambda |
|---|---|---|---|---|---|
| Live-Shell in laufenden Worker | Nein | `modal shell <id>` | Nein (nur Self-Hosting) | Eingeschränkt | Nein |
| Live-Container-Exec | Nein | `modal container exec <id> <cmd>` | Nein | Eingeschränkt | Nein |
| Echtzeit-Log-Stream über API | Nein | `modal logs --follow` | Streaming-HTTP-API | Über Beam Cloud | CloudWatch |
| Programmatischer Log-Abruf | **Keine API** (Issue #400) | `modal app logs --app-id` | REST + WebSocket | Ja | CloudWatch `GetLogEvents` |
| Interaktiver Breakpoint / IPython | Nein | `--interactive`-Flag | Nein | Nein | Nein |
| Vorinstallierte Debug-Tools | Nein | vim, strace, py-spy im Basis-Image | Nein | Nein | Nein |
| Log-Aufbewahrung | 90 Tage Endpoint-Ereignisse, flüchtige Worker-stdout | 30 Tage (Standard) | API-gespeichert | 7–30 Tage | CloudWatch-Aufbewahrungsrichtlinie |

**Warum Modal das kann:** Modal besitzt seine gesamte Firecracker-microVM-Flotte und betreibt in jeder microVM einen privilegierten Control-Plane-Agenten. Shell-Zugriff, Exec und Log-Streaming sind Kernfunktionen des Produkts, keine Nebeneffekte der Architektur.

**Warum RunPod das nicht kann:** Die Kombination aus Drittanbieter-Hosts der Community Cloud, fehlendem Exec-Kanal vom Control Plane zum Host und einer Log-Pipeline, die nie nach außen freigegeben wird, bedeutet, dass interaktives Debugging architektonisch blockiert ist und nicht bloß nicht implementiert wurde.

---

## Bestätigte Sackgassen {#confirmed-dead-ends}

Diese Ansätze sollte man nicht weiterverfolgen:

- `runpodctl logs` / `runpodctl exec`: Die Subcommands existieren im Binary nicht.
- GraphQL-Log-Abfrage: Nicht im öffentlichen Schema enthalten.
- Direkter Docker-Daemon-Zugriff auf dem Host: Durch die Nutzungsbedingungen der Community Cloud untersagt.
- SSH in einen Serverless-Worker: Keine Proxy-Infrastruktur vorhanden.
- `docker exec` über die Container-ID: Keine kundenseitige API-Oberfläche.
- PATCH auf `rest.runpod.io/v1/endpoints/<id>` mit partiellem Body: Löscht die Konfiguration stillschweigend (nur vollständiges POST-Neuanlegen oder PATCH auf Templates verwenden).

---

## Funktionierende Workarounds {#working-workarounds}

### Fix 1: Dockerfile-Basis mit zwei Umgebungsvariablen {#fix-1-dockerfile-baseline-two-environment-variables}

Jedes Serverless-Image sollte diese beiden Zeilen enthalten. Sie stellen die minimal sinnvolle Verbesserung der Observability dar:

```dockerfile
ENV PYTHONUNBUFFERED=1
ENV RUNPOD_DEBUG_LEVEL=DEBUG
```

`PYTHONUNBUFFERED=1` leert stdout bei jedem Schreibvorgang, sodass der letzte Traceback einen `SIGKILL` überlebt. `RUNPOD_DEBUG_LEVEL=DEBUG` veranlasst das `runpod-python`-SDK, interne Zustandsübergänge, Zeitmessungen und Ausnahmekontext nach stderr auszugeben. Beides greift der Log-Shipper auf, sobald er angebunden ist (also bei Abstürzen nach `ready`), und beim Volume-Tee-Workaround für Abstürze vor `ready`.

### Fix 2: Lokaler FastAPI-Modus mit `--rp_serve_api` {#fix-2-rp_serve_api-local-fastapi-mode}

Das `runpod-python`-SDK bringt einen Entwicklungsserver mit, der die Endpunkte `/run` und `/runsync` lokal nachbildet. Damit lassen sich Abstürze zur Laufzeit des Handlers (falsche Feldnamen in der Workflow-Ausgabe, SDK-Versionskonflikte, Importfehler in Custom Nodes) in Sekunden finden, statt erst nach einem vollständigen CI-Deployment-Zyklus.

```bash
docker run --rm -d --name rp-local-test \
  --gpus all \
  -p 8000:8000 \
  -v /tmp/test-volume:/runpod-volume \
  -e PYTHONUNBUFFERED=1 \
  -e RUNPOD_DEBUG_LEVEL=DEBUG \
  ghcr.io/your-org/your-image:tag \
  python /handler.py --rp_serve_api --rp_api_port 8000 --rp_log_level DEBUG --rp_debugger

# Wait for ready
until curl -s http://localhost:8000/docs >/dev/null; do sleep 1; done

# Submit a test job and stream the result
curl -s -X POST http://localhost:8000/runsync \
  -H "Content-Type: application/json" \
  -d @tests/sample-job.json | jq .

# Tail full stdout including tracebacks
docker logs -f rp-local-test
```

Einschränkung: Die GPU muss lokal oder per SSH-Forward verfügbar sein. Das Network Volume muss nach `/runpod-volume` eingebunden (Bind-Mount) werden. Dies bildet keine RunPod-spezifischen Scheduling-Eigenheiten nach, sondern nur das Verhalten des Handler-Codes.

### Fix 3: Volume-Log-Tee im Entrypoint {#fix-3-volume-log-tee-in-entrypoint}

Füge im Container-Entrypoint einen Tee auf den persistenten Network-Volume-Speicher hinzu. Dies erfasst Abstürze vor `ready`, die der Log-Shipper nie sieht:

```bash
#!/bin/bash
VOLUME_LOG="/runpod-volume/logs/worker-$(hostname).log"
mkdir -p "$(dirname "$VOLUME_LOG")"

# Redirect all stdout and stderr through tee to volume
exec > >(tee -a "$VOLUME_LOG") 2>&1

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] entrypoint starting"
exec python -u /handler.py "$@"
```

Logs aus einem Debug-Pod auf demselben Volume lesen:

```bash
# In a debug Pod (paper-hopper or equivalent) mounted to the same volume:
tail -f /runpod-volume/logs/worker-*.log
```

Für die Live-Überwachung, während neue Abstürze auftreten:

```bash
inotifywait -m /runpod-volume/logs -e create -e modify \
  --format '%w%f %e' | \
  while read filepath event; do
    [[ "$filepath" == *.traceback ]] && \
      echo "=== CRASH: $filepath ===" && \
      head -40 "$filepath"
  done
```

### Fix 4: `--rp_debugger`-Flag über Umgebungsvariable {#fix-4-rp_debugger-flag-via-environment-variable}

Ist `RUNPOD_DEBUG_LEVEL=DEBUG` gesetzt (oder wird der Handler mit `--rp_debugger` gestartet), fügt das SDK jeder Job-Antwort diagnostische Metadaten unter dem Schlüssel `debug` hinzu: Zustandsübergänge, Zeiten pro Stufe, Speicher-Snapshots und Ausnahmekontext. Bei `FAILED`-Jobs erscheint dies im Status-Response und ist über `api.runpod.ai/v2/<endpoint-id>/status/<job-id>` abrufbar:

```bash
curl -s \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  "https://api.runpod.ai/v2/<endpoint-id>/status/<job-id>" | \
  jq '.output.debug // .error'
```

Das funktioniert bei Abstürzen nach `ready`. Abstürze vor `ready` erzeugen keine Job-ID.

### Fix 5: Debug-Pod auf demselben Network Volume {#fix-5-debug-pair-pod-on-same-network-volume}

Wenn Serverless-Worker still abstürzen, starte einen Pod mit demselben Image auf demselben Network Volume (gleiches Rechenzentrum erforderlich):

```bash
# Via RunPod REST API
curl -s -X POST "https://rest.runpod.io/v1/pods" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "debug-pair",
    "imageName": "ghcr.io/your-org/your-image:tag",
    "gpuTypeId": "NVIDIA H100 80GB HBM3",
    "networkVolumeId": "<volume-id>",
    "dataCenterId": "US-KS-2",
    "containerDiskInGb": 60,
    "dockerStartCmd": "bash -c \"apt-get install -y inotify-tools && sleep infinity\""
  }'
```

Der Pod ist per SSH über `runpodctl ssh info <pod-id>` erreichbar. Die Logs abgestürzter Worker liest man über den gemeinsam genutzten Volume-Mount unter `/runpod-volume/logs/`.

---

## Worker-Zustände und Log-Verfügbarkeit {#worker-states-and-log-availability}

| Worker-Zustand | Log-Shipper angebunden? | Logs in der Console UI sichtbar? | Logs über API abrufbar? |
|---|---|---|---|
| `initializing` | Nein | Teilweise (nur Startphase) | Nein |
| `ready` / `idle` | Ja | Ja | Nein |
| `running` | Ja | Ja (Echtzeit, etwa 1000–2000 Zeilen Scrollback) | Nein |
| `unhealthy` (Absturz nach ready) | War angebunden; nach dem Absturz flüchtig | Etwa 10 Min. Aufbewahrung | Nein |
| `unhealthy` (Absturz vor ready) | Nie angebunden | **Keine** | Nein |
| `throttled` | Nein | Nein | Nein |

Log-Drosselung: RunPod verwirft stdout stillschweigend, wenn die Ausgaberate übermäßig hoch ist. Eine dokumentierte Grenze in MB/s oder Zeilen/s existiert nicht. Verwende für umfangreiches Logging `runpod.RunPodLogger` statt `print()`, um das Drosselungsrisiko zu verringern.

---

## Stolpersteine {#gotchas}

- **Problem:** Der Worker zeigt `unhealthy` mit `[error] worker exited with exit code 1` und ohne jeden Traceback in der Console UI. **Lösung:** Der Absturz ereignete sich, bevor der Log-Shipper angebunden war (Absturz vor ready). Füge den Volume-Tee-Workaround in deinen Entrypoint ein und prüfe `/runpod-volume/logs/`. Die häufigste Ursache ist ein Python-`ImportError` beim Laden des Moduls. Teste zuerst mit `--rp_serve_api` lokal.

- **Problem:** `ENV PYTHONUNBUFFERED=1` ist gesetzt, aber bei einem Absturz fehlen trotzdem Logs. **Lösung:** Prüfe, ob der Entrypoint Python tatsächlich mit `exec python -u` aufruft (das Flag `-u` überschreibt jede Container-Umgebung, die die Pufferung zurücksetzt). Prüfe außerdem, ob der Entrypoint Python nicht in eine Shell einhüllt, die puffert: `bash -c "python handler.py"` ohne `exec` und ohne `-u` fügt eine zusätzliche Shell-Pufferebene hinzu.

- **Problem:** Der Debug-Pod sieht die Logs abgestürzter Worker auf dem gemeinsamen Volume nicht. **Lösung:** Pods und Serverless-Worker müssen im selben Rechenzentrum liegen, um ein Network Volume zu teilen. Volume-IDs sind regional gebunden: `nrdo9nagku` ist US-KS-2, `zex70m9p9s` ist EU-RO-1. Prüfe die Übereinstimmung des Rechenzentrums, bevor du den Debug-Pod startest.

- **Problem:** Der Aufruf von `runpodctl logs <id>` oder `runpodctl exec <id> <cmd>` liefert eine Fehlermeldung über ein unbekanntes Subcommand. **Lösung:** Diese Subcommands existieren nicht. Siehe runpodctl-Issue [#29](https://github.com/runpod/runpodctl/issues/29) (seit März 2023 offen). Verwende stattdessen den Volume-Tee oder den lokalen Modus `--rp_serve_api`.

- **Problem:** `RUNPOD_DEBUG_LEVEL=DEBUG` erzeugt bei Abstürzen vor ready keine Ausgabe. **Lösung:** Die Debug-Ausgabe des SDK wird innerhalb von `runpod.serverless.start()` erzeugt. Wird dieser Aufruf nie ausgeführt (Absturz beim Import), entsteht keine Debug-Ausgabe. Die Umgebungsvariable hilft nur bei Fehlern nach der Initialisierung.

- **Problem:** stdout erscheint in der Console UI, aber die letzten 4 KB (der Traceback) fehlen. **Lösung:** Der Python-stdout-Puffer wurde vor dem `SIGKILL` nicht geleert. Stelle sicher, dass sowohl `PYTHONUNBUFFERED=1` im Dockerfile als auch `exec python -u` im Entrypoint gesetzt sind. Zusammen garantieren sie, dass jeder `print()`-Aufruf ein synchroner `write()`-Systemaufruf ist.

---

## Siehe auch {#see-also}

- [[runpod-serverless-silent-worker-crashes-on-task-pickup]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-production]]
- [[runpod-flash-gpu-serverless]]
- [[monitoring-and-observability]]
