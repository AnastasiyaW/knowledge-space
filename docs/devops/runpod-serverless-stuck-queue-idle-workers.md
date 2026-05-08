# RunPod Serverless: Jobs Stuck IN_QUEUE with Idle Ready Workers

Symptom: `health` endpoint shows `idle > 0` or `ready > 0`, queue depth is positive, `inProgress = 0`, and `jobs.completed` never increments. Distinct from worker crashes or handler panics — workers are up and registered, the scheduler simply does not dispatch.

Two independent root causes produce identical symptoms. Diagnose before acting.

## Root Cause 1: Endpoint State Corruption After Repeated REST PATCHes

The REST endpoint `PATCH /v1/endpoints/{id}` increments an internal `version` field on every call. The RunPod scheduler maintains a worker↔endpoint mapping in internal state. After repeated PATCHes (version > ~10), that mapping can enter an inconsistent state where the dispatcher believes workers are busy or mis-tagged even though `health` reports them idle.

Observable signals that implicate this cause:
- `version` field in `GET /v1/endpoints/{id}` response is high (>10).
- Endpoint was modified frequently via REST PATCH, not GraphQL.
- `runsync` also hangs (confirms scheduler-layer problem, not handler).
- Occasional `running: 1` appears for 30–60 s then collapses back to 0 without a completed job — ghost assignment.
- `POST /v2/{id}/cancel/{job_id}` succeeds (REST control plane alive), but status stays `IN_QUEUE`.
- Purging the queue clears it, but fresh submissions hit the same stall.

Community-confirmed fix: **delete and recreate the endpoint via full POST** (not PATCH).

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

After recreate: update any hardcoded endpoint IDs in downstream services (CF Worker `wrangler.toml`, environment variables, dashboards).

### Setting `workersStandby` Reliably

REST `PATCH /v1/endpoints/{id}` silently ignores `workersStandby`. Use GraphQL `saveEndpoint` mutation instead (RunPod GraphQL API 2025):

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

GraphQL endpoint: `https://api.runpod.io/graphql`. Auth: `Authorization: Bearer $RUNPOD_API_KEY` header.

Schema reference: https://graphql-spec.runpod.io/ — field `workersStandby` is documented there and under `saveEndpoint` input.

## Root Cause 2: runpod-python 1.7.11 / 1.7.12 Single-Worker Routing Bug

runpod-python GitHub issue #432 (opened June 2025, unresolved as of late 2025): all inbound jobs are routed to a single worker even when N workers are idle. If that one worker is slow to acknowledge or in a blocking state, the queue stalls with other workers fully idle.

Affects: images built with `runpod==1.7.11` or `runpod==1.7.12`. Version 1.7.12 was a partial fix to 1.7.11 that works locally but remains broken in production Serverless.

**Recreating the endpoint will not fix this** — the bug is inside the container image.

Diagnosis: exec into a running worker and check the installed version.

```bash
# Via RunPod Console → Pods → Worker UUID → Exec, or via SSH if openssh-server is baked in
pip show runpod | grep Version
```

Fix: rebuild the image with the pinned version.

```dockerfile
# Dockerfile — pin to last known-good SDK version
RUN pip install runpod==1.7.10
```

Rebuild → push new tag → update template → scale workers to 0 then back up to flush FlashBoot cache. Do not reuse the same image tag; RunPod's FlashBoot caches by digest, so a new tag guarantees the scheduler pulls the updated image.

## Diagnostic Probes

Run these in order to identify which root cause is active before touching production config.

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

## Recovery Procedure (Priority Order)

| Step | Action | Time | Fixes |
|---|---|---|---|
| 1 | Delete + recreate endpoint via full POST | 5–10 min | Root Cause 1 |
| 2 | Kill individual workers via `DELETE /v1/pods/{podId}` | 2 min | Root Cause 1 (partial) |
| 3 | Rebuild image with `runpod==1.7.10`, new tag | 15–30 min + CI | Root Cause 2 |
| 4 | Migrate all edits to GraphQL `saveEndpoint` | Ongoing | Prevents recurrence |
| 5 | Open RunPod support ticket with endpoint ID + timestamps | — | Infra-level scheduler reset |

For step 5: Discord `#serverless-help` or support@runpod.io. Provide `GET /health` snapshot JSON, endpoint ID, and approximate time range. RunPod engineering can reset scheduler state for a specific endpoint without requiring a recreate.

**References:** runpod-python issue #432 (single-worker routing bug) — https://github.com/runpod/runpod-python/issues/432; issue #250 (`progress_update` race, older) — https://github.com/runpod/runpod-python/issues/250; endpoint configuration docs — https://docs.runpod.io/serverless/references/endpoint-configurations; job states — https://docs.runpod.io/serverless/references/job-states; GraphQL manage-endpoints — https://docs.runpod.io/sdks/graphql/manage-endpoints.

## Gotchas

- **Issue:** `PATCH /v1/endpoints/{id}` with a partial body silently wipes fields not included in the payload — not a merge, a replace. **Fix:** always send the complete endpoint body on edit, or switch all edits to GraphQL `saveEndpoint` which supports partial updates without field loss.

- **Issue:** `workersStandby` set via REST PATCH appears to succeed (HTTP 200) but the field value does not change in subsequent GETs. **Fix:** use GraphQL `saveEndpoint` mutation with `workersStandby` in the input; this is the only reliable path for this field.

- **Issue:** Scaling workers to 0 then back up does not force a new image pull — RunPod FlashBoot caches by manifest digest. Rebuilding on the same tag leaves workers running the old image. **Fix:** push every rebuild under a new unique tag (e.g., include the git short SHA); patch the template to point at the new tag before cycling workers.

- **Issue:** After endpoint recreate, any service that hardcodes the endpoint ID (CF Worker `wrangler.toml`, env vars, monitoring dashboards) silently starts sending to a deleted endpoint returning 404. **Fix:** always store the endpoint ID in one place (e.g., a secrets manager or `wrangler.toml` vars block), update it immediately after recreate, and redeploy dependent services before re-enabling traffic.

- **Issue:** `runsync` and async `/run` can exhibit different behavior under Root Cause 1 — `runsync` may occasionally complete while `/run` stalls. Do not conclude the endpoint is healthy based on one successful `runsync` alone. **Fix:** check both; also verify `jobs.completed` increments over a 5-minute window under sustained load.

- **Issue:** RunPod public status page (status.runpod.io) does not post entries for subtle scheduler-layer issues, only hard infra outages. A stuck queue during a period with no status page entry does not rule out platform-side causes. **Fix:** cross-reference StatusGator history for the relevant datacenter region alongside your own endpoint telemetry before concluding the root cause is local.

## See Also

- [[runpod-production]]
- [[runpod-flash-gpu-serverless]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-serverless-silent-worker-crashes-on-task-pickup]]
