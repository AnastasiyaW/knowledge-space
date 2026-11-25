---
level: 3
source_sha256: 0bf41393becda79026b795e347908116d281ace304a52f708112bdd2856bf4d3
translation: machine
translated_at: '2026-10-24'
---
# RunPod Serverless: Jobs hängen in `IN_QUEUE` bei untätigen Ready-Workern {#runpod-serverless-jobs-stuck-in_queue-with-idle-ready-workers}

Symptom: Der `health`-Endpunkt zeigt `idle > 0` oder `ready > 0`, die Warteschlange hat eine positive Tiefe, `inProgress = 0`, und `jobs.completed` wird nie erhöht. Dies unterscheidet sich von Worker-Abstürzen oder Handler-Panics: Die Worker laufen und sind registriert, der Scheduler verteilt die Jobs jedoch schlicht nicht.

Zwei voneinander unabhängige Grundursachen führen zu identischen Symptomen. Diagnostizieren Sie, bevor Sie handeln.

## Grundursache 1: Zustandsverfälschung des Endpunkts nach wiederholten REST-PATCHes {#root-cause-1-endpoint-state-corruption-after-repeated-rest-patches}

Der REST-Endpunkt `PATCH /v1/endpoints/{id}` erhöht bei jedem Aufruf ein internes Feld `version`. Der RunPod-Scheduler pflegt im internen Zustand eine Zuordnung zwischen Workern und Endpunkt. Nach wiederholten PATCHes (version > ~10) kann diese Zuordnung in einen inkonsistenten Zustand geraten, in dem der Dispatcher Worker für beschäftigt oder falsch markiert hält, obwohl `health` sie als untätig meldet.

Beobachtbare Anzeichen, die auf diese Ursache hindeuten:
- Das Feld `version` in der Antwort von `GET /v1/endpoints/{id}` ist hoch (>10).
- Der Endpunkt wurde häufig per REST-PATCH statt per GraphQL geändert.
- `runsync` hängt ebenfalls (bestätigt ein Problem auf Scheduler-Ebene, nicht im Handler).
- Gelegentlich erscheint `running: 1` für 30–60 s und fällt dann ohne abgeschlossenen Job wieder auf 0 zurück: eine Geisterzuweisung.
- `POST /v2/{id}/cancel/{job_id}` gelingt (die REST-Steuerungsebene ist erreichbar), aber der Status bleibt `IN_QUEUE`.
- Das Leeren der Warteschlange behebt das Problem kurzzeitig, aber neue Aufträge laufen in denselben Stillstand.

Von der Community bestätigte Abhilfe: **Endpunkt löschen und per vollständigem POST neu anlegen** (nicht per PATCH).

```bash
# Step 1: capture current config
curl -s "https://rest.runpod.io/v1/endpoints/{ENDPOINT_ID}" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" > /tmp/ep_backup.json

# Step 2: purge pending jobs (optional — skip if queue is already empty)
curl -s -X POST "https://api.runpod.ai/v2/{ENDPOINT_ID}/purge-queue" \
  -H "Authorization: Bearer $RUNPOD_API_KEY"

# Step 3: delete
curl -s -X DELETE "https://rest.runpod.io/v1/endpoints/{ENDPOINT_ID}" \
  -H "Authorization: Bearer $RUNPOD_API_KEY"

# Step 4: recreate with FULL body (missing fields are wiped, not defaulted)
curl -s -X POST "https://rest.runpod.io/v1/endpoints" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-endpoint-v2",
    "templateId": "YOUR_TEMPLATE_ID",
    "gpuTypeIds": ["NVIDIA H100 PCIe", "NVIDIA H100 80GB HBM3"],
    "networkVolumeId": "YOUR_VOLUME_ID",
    "dataCenterIds": ["US-KS-2"],
    "workersMin": 0,
    "workersMax": 2,
    "idleTimeout": 300,
    "flashboot": true,
    "scalerType": "QUEUE_DELAY",
    "scalerValue": 4,
    "gpuCount": 1,
    "computeType": "GPU"
  }'
```

Nach der Neuanlage aktualisieren Sie alle fest kodierten Endpunkt-IDs in nachgelagerten Diensten (CF Worker `wrangler.toml`, Umgebungsvariablen, Dashboards).

### `workersStandby` zuverlässig setzen {#setting-workersstandby-reliably}

REST-`PATCH /v1/endpoints/{id}` ignoriert `workersStandby` stillschweigend. Verwenden Sie stattdessen die GraphQL-Mutation `saveEndpoint` (RunPod GraphQL API 2025):

```graphql
mutation {
  saveEndpoint(input: {
    id: "YOUR_ENDPOINT_ID"
    workersStandby: 0
  }) {
    id
    workersStandby
  }
}
```

GraphQL-Endpunkt: `https://api.runpod.io/graphql`. Authentifizierung: Header `Authorization: Bearer $RUNPOD_API_KEY`.

Schemareferenz: https://graphql-spec.runpod.io/ – das Feld `workersStandby` ist dort sowie unter der Eingabe von `saveEndpoint` dokumentiert.

## Grundursache 2: Routing-Fehler mit einzelnem Worker in runpod-python 1.7.11 / 1.7.12 {#root-cause-2-runpod-python-1711-1712-single-worker-routing-bug}

runpod-python GitHub-Issue #432 (eröffnet im Juni 2025, Stand Ende 2025 ungelöst): Alle eingehenden Jobs werden an einen einzigen Worker geleitet, selbst wenn N Worker untätig sind. Reagiert dieser eine Worker langsam oder befindet er sich in einem blockierenden Zustand, stockt die Warteschlange, während die übrigen Worker vollständig untätig sind.

Betroffen sind Images, die mit `runpod==1.7.11` oder `runpod==1.7.12` gebaut wurden. Version 1.7.12 war eine teilweise Korrektur von 1.7.11, die lokal funktioniert, in der produktiven Serverless-Umgebung aber weiterhin fehlerhaft ist.

**Die Neuanlage des Endpunkts behebt dieses Problem nicht**, denn der Fehler steckt im Container-Image.

Diagnose: Verbinden Sie sich per exec mit einem laufenden Worker und prüfen Sie die installierte Version.

```bash
# Via RunPod Console → Pods → Worker UUID → Exec, or via SSH if openssh-server is baked in
pip show runpod | grep Version
```

Abhilfe: Bauen Sie das Image mit der fixierten Version neu.

```dockerfile
# Dockerfile — pin to last known-good SDK version
RUN pip install runpod==1.7.10
```

Neu bauen → neuen Tag pushen → Template aktualisieren → Worker auf 0 skalieren und danach wieder hochfahren, um den FlashBoot-Cache zu leeren. Verwenden Sie denselben Image-Tag nicht erneut: RunPod cached FlashBoot anhand des Digests, sodass ein neuer Tag garantiert, dass der Scheduler das aktualisierte Image lädt.

## Diagnoseprüfungen {#diagnostic-probes}

Führen Sie diese Prüfungen in der angegebenen Reihenfolge aus, um zu ermitteln, welche Grundursache aktiv ist, bevor Sie die Produktionskonfiguration ändern.

```bash
# 1. Endpoint metadata — check version field and current config
curl -s "https://rest.runpod.io/v1/endpoints/{ENDPOINT_ID}" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" | python -m json.tool | grep -E '"version"|"workersStandby"|"workersMin"|"workersMax"'

# 2. Health snapshot
curl -s "https://api.runpod.ai/v2/{ENDPOINT_ID}/health" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" | python -m json.tool

# 3. Submit runsync — blocks until completion or timeout; exposes raw errors
# If runsync also hangs: confirms scheduler issue (Root Cause 1)
# If runsync completes but async /run jobs queue forever: async dispatcher bug specifically
curl -s -X POST "https://api.runpod.ai/v2/{ENDPOINT_ID}/runsync" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {}}' \
  --max-time 120

# 4. Force-kill one specific worker to trigger respawn (sometimes unsticks without full recreate)
# Requires GET /v1/endpoints/{id}?includeWorkers=true to get pod IDs first
curl -s "https://rest.runpod.io/v1/endpoints/{ENDPOINT_ID}?includeWorkers=true" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" | python -m json.tool | grep podId

curl -s -X DELETE "https://rest.runpod.io/v1/pods/{POD_ID}" \
  -H "Authorization: Bearer $RUNPOD_API_KEY"
```

## Wiederherstellungsverfahren (in Prioritätsreihenfolge) {#recovery-procedure-priority-order}

| Schritt | Aktion | Dauer | Behebt |
|---|---|---|---|
| 1 | Endpunkt löschen und per vollständigem POST neu anlegen | 5–10 min | Grundursache 1 |
| 2 | Einzelne Worker über `DELETE /v1/pods/{podId}` beenden | 2 min | Grundursache 1 (teilweise) |
| 3 | Image mit `runpod==1.7.10` und neuem Tag neu bauen | 15–30 min + CI | Grundursache 2 |
| 4 | Alle Änderungen auf GraphQL `saveEndpoint` umstellen | Laufend | Verhindert Wiederauftreten |
| 5 | RunPod-Support-Ticket mit Endpunkt-ID und Zeitstempeln eröffnen | — | Zurücksetzen des Schedulers auf Infrastrukturebene |

Für Schritt 5: Discord `#serverless-help` oder support@runpod.io. Stellen Sie den Snapshot-JSON von `GET /health`, die Endpunkt-ID und einen ungefähren Zeitraum bereit. Das RunPod-Engineering kann den Scheduler-Zustand für einen bestimmten Endpunkt zurücksetzen, ohne dass eine Neuanlage nötig ist.

**Referenzen:** runpod-python Issue #432 (Routing-Fehler mit einzelnem Worker) – https://github.com/runpod/runpod-python/issues/432; Issue #250 (`progress_update`-Race Condition, älter) – https://github.com/runpod/runpod-python/issues/250; Dokumentation zur Endpunktkonfiguration – https://docs.runpod.io/serverless/references/endpoint-configurations; Jobstatus – https://docs.runpod.io/serverless/references/job-states; GraphQL-Endpunktverwaltung – https://docs.runpod.io/sdks/graphql/manage-endpoints.

## Stolperfallen {#gotchas}

- **Problem:** `PATCH /v1/endpoints/{id}` mit einem partiellen Body löscht stillschweigend alle Felder, die nicht im Payload enthalten sind. Es handelt sich nicht um ein Zusammenführen, sondern um ein vollständiges Ersetzen. **Abhilfe:** Senden Sie beim Bearbeiten immer den vollständigen Endpunkt-Body, oder stellen Sie alle Änderungen auf GraphQL `saveEndpoint` um, das partielle Aktualisierungen ohne Feldverlust unterstützt.

- **Problem:** `workersStandby`, gesetzt per REST-PATCH, scheint erfolgreich zu sein (HTTP 200), der Feldwert ändert sich in anschließenden GET-Abfragen jedoch nicht. **Abhilfe:** Verwenden Sie die GraphQL-Mutation `saveEndpoint` mit `workersStandby` in der Eingabe; dies ist der einzig zuverlässige Weg für dieses Feld.

- **Problem:** Das Skalieren der Worker auf 0 und danach wieder nach oben erzwingt keinen neuen Image-Pull, denn RunPod cached FlashBoot anhand des Manifest-Digests. Ein Neubau unter demselben Tag lässt Worker das alte Image weiterverwenden. **Abhilfe:** Pushen Sie jeden Neubau unter einem neuen, eindeutigen Tag (z. B. mit dem kurzen Git-SHA); passen Sie das Template auf den neuen Tag an, bevor Sie die Worker neu starten.

- **Problem:** Nach der Neuanlage des Endpunkts sendet jeder Dienst, der die Endpunkt-ID fest kodiert hat (CF Worker `wrangler.toml`, Umgebungsvariablen, Monitoring-Dashboards), stillschweigend an einen gelöschten Endpunkt und erhält 404. **Abhilfe:** Speichern Sie die Endpunkt-ID immer an einer zentralen Stelle (z. B. in einem Secrets-Manager oder im Block `vars` von `wrangler.toml`), aktualisieren Sie sie unmittelbar nach der Neuanlage und deployen Sie abhängige Dienste neu, bevor Sie den Traffic wieder freigeben.

- **Problem:** `runsync` und das asynchrone `/run` können sich unter Grundursache 1 unterschiedlich verhalten: `runsync` kann gelegentlich erfolgreich abschließen, während `/run` stockt. Schließen Sie nicht aus einem einzelnen erfolgreichen `runsync` auf einen gesunden Endpunkt. **Abhilfe:** Prüfen Sie beide Pfade; verifizieren Sie außerdem, dass `jobs.completed` bei anhaltender Last über ein Fenster von 5 Minuten steigt.

- **Problem:** Die öffentliche Statusseite von RunPod (status.runpod.io) veröffentlicht keine Einträge für subtile Probleme auf Scheduler-Ebene, sondern nur für harte Infrastrukturausfälle. Eine feststeckende Warteschlange in einem Zeitraum ohne Statusseiten-Eintrag schließt plattformseitige Ursachen nicht aus. **Abhilfe:** Gleichen Sie den StatusGator-Verlauf für die betreffende Rechenzentrumsregion mit Ihrer eigenen Endpunkt-Telemetrie ab, bevor Sie die Ursache als lokal einstufen.

## Siehe auch {#see-also}

- [[runpod-production]]
- [[runpod-flash-gpu-serverless]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-serverless-silent-worker-crashes-on-task-pickup]]
