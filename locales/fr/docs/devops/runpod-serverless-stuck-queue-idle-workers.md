---
level: 3
source_sha256: 0bf41393becda79026b795e347908116d281ace304a52f708112bdd2856bf4d3
translation: machine
translated_at: '2026-10-24'
---
# RunPod Serverless : tâches bloquées en IN_QUEUE avec des workers prêts inactifs {#runpod-serverless-jobs-stuck-in_queue-with-idle-ready-workers}

Symptôme : l'endpoint `health` affiche `idle > 0` ou `ready > 0`, la profondeur de la file est positive, `inProgress = 0`, et `jobs.completed` n'augmente jamais. Ce cas se distingue des plantages de workers ou des paniques de handler : les workers sont actifs et enregistrés, mais le planificateur ne distribue simplement aucune tâche.

Deux causes racines indépendantes produisent des symptômes identiques. Établissez le diagnostic avant d'agir.

## Cause racine 1 : corruption de l'état de l'endpoint après des PATCH REST répétés {#root-cause-1-endpoint-state-corruption-after-repeated-rest-patches}

L'endpoint REST `PATCH /v1/endpoints/{id}` incrémente un champ interne `version` à chaque appel. Le planificateur RunPod maintient une correspondance worker↔endpoint dans son état interne. Après des PATCH répétés (version > ~10), cette correspondance peut entrer dans un état incohérent : le dispatcher considère les workers comme occupés ou mal étiquetés, alors que `health` les signale inactifs.

Signaux observables qui impliquent cette cause :
- Le champ `version` dans la réponse de `GET /v1/endpoints/{id}` est élevé (> 10).
- L'endpoint a été modifié fréquemment via PATCH REST, et non via GraphQL.
- `runsync` se bloque également (ce qui confirme un problème au niveau du planificateur, et non du handler).
- Un `running: 1` apparaît par intermittence pendant 30 à 60 s, puis retombe à 0 sans job terminé : affectation fantôme.
- `POST /v2/{id}/cancel/{job_id}` réussit (le plan de contrôle REST est opérationnel), mais le statut reste `IN_QUEUE`.
- La purge de la file résout le problème, mais les nouvelles soumissions rencontrent le même blocage.

Correctif confirmé par la communauté : **supprimer et recréer l'endpoint via un POST complet** (et non un PATCH).

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

Après la recréation, mettez à jour tous les identifiants d'endpoint codés en dur dans les services en aval (`wrangler.toml` du CF Worker, variables d'environnement, tableaux de bord).

### Définir `workersStandby` de manière fiable {#setting-workersstandby-reliably}

Le PATCH REST `PATCH /v1/endpoints/{id}` ignore silencieusement `workersStandby`. Utilisez plutôt la mutation GraphQL `saveEndpoint` (API GraphQL RunPod 2025) :

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

Endpoint GraphQL : `https://api.runpod.io/graphql`. Authentification : en-tête `Authorization: Bearer $RUNPOD_API_KEY`.

Référence du schéma : https://graphql-spec.runpod.io/ — le champ `workersStandby` y est documenté, ainsi que dans l'entrée `saveEndpoint`.

## Cause racine 2 : bug de routage vers un seul worker dans runpod-python 1.7.11 / 1.7.12 {#root-cause-2-runpod-python-1711-1712-single-worker-routing-bug}

Issue #432 de runpod-python sur GitHub (ouverte en juin 2025, toujours non résolue à la fin de 2025) : toutes les tâches entrantes sont routées vers un seul worker, même lorsque N workers sont inactifs. Si ce worker unique met du temps à acquitter ou se trouve dans un état bloquant, la file se fige alors que les autres workers sont complètement inactifs.

Concerne : les images construites avec `runpod==1.7.11` ou `runpod==1.7.12`. La version 1.7.12 était un correctif partiel de la 1.7.11 : elle fonctionne en local, mais reste défaillante en production Serverless.

**Recréer l'endpoint ne résoudra pas ce problème** : le bug se trouve dans l'image du conteneur.

Diagnostic : connectez-vous à un worker en cours d'exécution et vérifiez la version installée.

```bash
# Via RunPod Console → Pods → Worker UUID → Exec, or via SSH if openssh-server is baked in
pip show runpod | grep Version
```

Correctif : reconstruisez l'image avec la version épinglée.

```dockerfile
# Dockerfile — pin to last known-good SDK version
RUN pip install runpod==1.7.10
```

Reconstruire → pousser le nouveau tag → mettre à jour le template → ramener les workers à 0 puis les remonter pour vider le cache FlashBoot. Ne réutilisez pas le même tag d'image : FlashBoot de RunPod met en cache par digest, donc un nouveau tag garantit que le planificateur récupère l'image mise à jour.

## Sondes de diagnostic {#diagnostic-probes}

Exécutez-les dans l'ordre pour identifier la cause racine active avant de toucher à la configuration de production.

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

## Procédure de récupération (par ordre de priorité) {#recovery-procedure-priority-order}

| Étape | Action | Durée | Corrige |
|---|---|---|---|
| 1 | Supprimer et recréer l'endpoint via un POST complet | 5–10 min | Cause racine 1 |
| 2 | Arrêter les workers individuellement via `DELETE /v1/pods/{podId}` | 2 min | Cause racine 1 (partiel) |
| 3 | Reconstruire l'image avec `runpod==1.7.10`, nouveau tag | 15–30 min + CI | Cause racine 2 |
| 4 | Migrer toutes les modifications vers la mutation GraphQL `saveEndpoint` | En continu | Prévient la récidive |
| 5 | Ouvrir un ticket auprès du support RunPod avec l'identifiant de l'endpoint et les horodatages | — | Réinitialisation du planificateur au niveau infrastructure |

Pour l'étape 5 : canal Discord `#serverless-help` ou support@runpod.io. Fournissez l'instantané JSON de `GET /health`, l'identifiant de l'endpoint et la plage horaire approximative. L'équipe d'ingénierie RunPod peut réinitialiser l'état du planificateur d'un endpoint précis sans nécessiter de recréation.

**Références :** issue #432 de runpod-python (bug de routage vers un seul worker) — https://github.com/runpod/runpod-python/issues/432 ; issue #250 (condition de concurrence sur `progress_update`, plus ancienne) — https://github.com/runpod/runpod-python/issues/250 ; documentation de configuration des endpoints — https://docs.runpod.io/serverless/references/endpoint-configurations ; états des jobs — https://docs.runpod.io/serverless/references/job-states ; gestion des endpoints via GraphQL — https://docs.runpod.io/sdks/graphql/manage-endpoints.

## Pièges courants {#gotchas}

- **Problème :** un `PATCH /v1/endpoints/{id}` avec un corps partiel efface silencieusement les champs absents de la charge utile. Il ne s'agit pas d'une fusion, mais d'un remplacement. **Correction :** envoyez toujours le corps complet de l'endpoint lors d'une modification, ou passez toutes les modifications à la mutation GraphQL `saveEndpoint`, qui prend en charge les mises à jour partielles sans perte de champs.

- **Problème :** `workersStandby` défini via PATCH REST semble réussir (HTTP 200), mais la valeur du champ ne change pas dans les GET suivants. **Correction :** utilisez la mutation GraphQL `saveEndpoint` avec `workersStandby` dans l'entrée ; c'est la seule voie fiable pour ce champ.

- **Problème :** ramener les workers à 0 puis les remonter ne force pas le téléchargement d'une nouvelle image : FlashBoot de RunPod met en cache par digest de manifeste. Reconstruire sous le même tag laisse les workers exécuter l'ancienne image. **Correction :** poussez chaque reconstruction sous un tag unique et nouveau (par exemple en incluant le SHA court de git) ; modifiez le template pour pointer vers le nouveau tag avant de cycler les workers.

- **Problème :** après une recréation de l'endpoint, tout service qui code en dur l'identifiant de l'endpoint (`wrangler.toml` du CF Worker, variables d'environnement, tableaux de bord de supervision) envoie silencieusement ses requêtes vers un endpoint supprimé et reçoit des 404. **Correction :** stockez toujours l'identifiant de l'endpoint à un seul endroit (par exemple un gestionnaire de secrets ou le bloc de variables de `wrangler.toml`), mettez-le à jour immédiatement après la recréation, puis redéployez les services dépendants avant de rétablir le trafic.

- **Problème :** `runsync` et `/run` asynchrone peuvent se comporter différemment sous la cause racine 1 : `runsync` peut parfois aboutir alors que `/run` reste bloqué. Ne concluez pas que l'endpoint est sain sur la base d'un seul `runsync` réussi. **Correction :** testez les deux ; vérifiez également que `jobs.completed` augmente sur une fenêtre de 5 minutes sous charge soutenue.

- **Problème :** la page d'état publique de RunPod (status.runpod.io) ne publie pas d'entrées pour les problèmes plus subtils au niveau du planificateur, seulement pour les pannes d'infrastructure franches. Une file bloquée pendant une période sans entrée sur la page d'état n'exclut pas une cause côté plateforme. **Correction :** croisez l'historique StatusGator de la région de datacenter concernée avec vos propres données de télémétrie avant de conclure que la cause racine est locale.

## Voir aussi {#see-also}

- [[runpod-production]]
- [[runpod-flash-gpu-serverless]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-serverless-silent-worker-crashes-on-task-pickup]]
