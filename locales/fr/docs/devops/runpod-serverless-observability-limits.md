---
level: 3
source_sha256: 9be7fd85a4e59a5fb8509f2e624f544c7b933fc9e042ee3a98daa4064891fcc1
translation: machine
translated_at: '2026-10-24'
---
# Observabilité de RunPod Serverless : pourquoi elle est opaque et comment la contourner {#runpod-serverless-observability-why-its-opaque-and-how-to-work-around-it}

## Cinq causes architecturales de l'opacité {#five-architectural-causes-of-opacity}

Les workers RunPod Serverless sont difficiles à déboguer non pas à cause d'une fonctionnalité manquante, mais parce que cinq couches architecturales indépendantes suppriment chacune une catégorie d'observabilité.

**Cause 1 : modèle d'hôte Community Cloud.**
Les workers s'exécutent comme de simples conteneurs Docker sous un daemon Docker standard, sur des machines hôtes pair-à-pair appartenant à des tiers. RunPod ne possède pas ces machines. Comme elles ne peuvent pas garantir la présence d'un agent de plan de contrôle privilégié sur chaque hôte, RunPod ne peut pas transmettre de manière sûre `docker exec`, `docker logs --follow` ni aucun canal d'exécution aux clients. Modal possède l'intégralité de sa flotte de microVM Firecracker, c'est pourquoi `modal shell <container-id>` fonctionne : leur serveur d'API demande un canal d'exécution vers une microVM précise via le chemin jailer/agent ttrpc. L'équivalent chez RunPod n'existe pas.

**Cause 2 : absence d'identité proxy entrante pour les workers Serverless.**
Le mode Pod attribue à chaque conteneur une identité routable : `https://[POD_ID]-[PORT].proxy.runpod.net`, ainsi qu'une correspondance TCP SSH. Les workers Serverless n'ont pas de `POD_ID` au sens propre. Ils ne reçoivent du travail que depuis la file d'attente du scheduler RunPod ; le trafic réseau entrant depuis l'extérieur de ce scheduler n'est pas routé. Étendre le proxy des Pods aux workers Serverless nécessiterait une identité routable unique et une entrée de proxy avec état pour chaque worker éphémère, un coût d'infrastructure que RunPod n'a pas pris en charge.

**Cause 3 : le log shipper s'attache après que le worker a signalé son état prêt.**
Le pipeline de logs est le suivant : stdout du worker → fichier JSON-log Docker sur l'hôte → shipper de type promtail s'exécutant sur cet hôte → magasin de logs centralisé → Console UI via une API d'administration interne. Le shipper ne s'attache à un conteneur qu'après sa transition vers l'état `ready`. Un worker qui plante lors de l'import d'un module, avant que `runpod.serverless.start()` ne retourne, n'atteint jamais `ready` ; le shipper ne s'attache donc jamais. Ce worker ne produit aucune ligne de log visible dans la Console UI ni via une API. Ce comportement est confirmé empiriquement (AnswerOverflow [#1295692391411355668](https://www.answeroverflow.com/m/1295692391411355668)) ainsi que dans le ticket runpod-python [#29](https://github.com/runpod/runpodctl/issues/29).

**Cause 4 : `PYTHONUNBUFFERED` non défini dans les images de base.**
Par défaut, Python met en tampon la sortie stdout par blocs d'environ 4 Ko. En cas de `SIGKILL` (kill par OOM, timeout du scheduler), le tampon en cours est perdu : le processus est terminé avant l'exécution de `sys.stdout.flush()`. Même si le log shipper est attaché, il peut ne jamais recevoir la dernière traceback. Exécuter avec `-u` (`python -u handler.py`) ou définir `ENV PYTHONUNBUFFERED=1` dans le Dockerfile fait en sorte que chaque appel système `write()` soit immédiatement vidé vers le fichier JSON-log Docker, donnant au shipper une chance de capturer le message de crash avant la disparition du processus.

**Cause 5 : l'absence d'API de logs est une lacune confirmée, et non un manque de documentation.**
Une recherche systématique sur toutes les surfaces d'API accessibles aux clients confirme qu'aucun endpoint de récupération de logs n'existe :

| Surface | Résultat |
|---|---|
| [Spécification GraphQL publique](https://graphql-spec.runpod.io/) | Aucune requête de logs ; uniquement `cpuTypes`, `gpuTypes`, `myself`, `pod` (télémétrie GPU) |
| API REST (`rest.runpod.io/v1`) | Endpoints, templates, volumes, types de GPU : aucune ressource de logs |
| API Serverless (`api.runpod.ai/v2/<id>/`) | `run`, `runsync`, `status`, `cancel`, `health` : aucune ressource de logs |
| CLI `runpodctl` ([référence complète des commandes](https://github.com/runpod/runpodctl/blob/main/docs/runpodctl.md)) | `pod`, `serverless`, `template`, `model`, `network-volume`, `registry`, `ssh`, `send`, `receive`, `doctor` : aucune sous-commande `logs`, `exec`, `shell` ou `attach` |
| Code source du SDK runpod-python | Aucun streaming de logs côté client |
| [runpod-python issue #400](https://github.com/runpod/runpod-python/issues/400) | Ouvert depuis 2024, sans réponse de l'équipe RunPod, sans assigné, sans PR |
| [runpodctl issue #29](https://github.com/runpod/runpodctl/issues/29) | Ouvert depuis mars 2023, aucune activité de mainteneur depuis 3 ans |

L'onglet Workers de la Console UI récupère les logs depuis un endpoint d'administration interne (probablement `wss://api.runpod.io/ws/workers/<uuid>/logs` ou équivalent) qui exige un JWT d'administrateur non délivré aux clients. Il ne s'agit pas d'un chemin caché et non documenté, mais d'une infrastructure réservée aux administrateurs.

---

## Comparaison des plateformes {#platform-comparison}

| Capacité | RunPod Serverless | Modal | Replicate (Cog) | Beam | AWS Lambda |
|---|---|---|---|---|---|
| Shell interactif dans un worker en cours d'exécution | Non | `modal shell <id>` | Non (auto-hébergement uniquement) | Limité | Non |
| Exécution de commandes dans le conteneur | Non | `modal container exec <id> <cmd>` | Non | Limité | Non |
| Flux de logs en temps réel via API | Non | `modal logs --follow` | API HTTP en streaming | Via Beam Cloud | CloudWatch |
| Récupération programmatique des logs | **Aucune API** (issue #400) | `modal app logs --app-id` | REST + WebSocket | Oui | `GetLogEvents` de CloudWatch |
| Point d'arrêt interactif / IPython | Non | Option `--interactive` | Non | Non | Non |
| Outils de débogage préinstallés | Non | vim, strace, py-spy dans l'image de base | Non | Non | Non |
| Rétention des logs | 90d pour les événements d'endpoint, stdout des workers éphémères | 30d par défaut | Persistés via l'API | 7–30d | Politique de rétention CloudWatch |

**Pourquoi Modal peut le faire :** Modal possède l'intégralité de sa flotte de microVM Firecracker et dispose d'un agent de plan de contrôle privilégié dans chaque microVM. L'accès shell, l'exécution de commandes et le streaming de logs sont des fonctionnalités produit de base, et non des effets secondaires de l'architecture.

**Pourquoi RunPod ne le peut pas :** La combinaison d'hôtes Community Cloud tiers, de l'absence de canal d'exécution du plan de contrôle vers l'hôte et d'un pipeline de logs jamais exposé à l'extérieur signifie que le débogage interactif est bloqué par l'architecture, et non simplement non implémenté.

---

## Impasses confirmées {#confirmed-dead-ends}

Inutile de perdre du temps à tenter ces opérations :

- `runpodctl logs` / `runpodctl exec` : ces sous-commandes n'existent pas dans le binaire
- Requête GraphQL de logs : absente du schéma public
- Accès direct au daemon Docker sur l'hôte : interdit par les conditions d'utilisation du Community Cloud
- SSH vers un worker Serverless : pas d'infrastructure de proxy
- `docker exec` via l'ID du conteneur : aucune surface d'API accessible aux clients
- PATCH sur `rest.runpod.io/v1/endpoints/<id>` avec un corps partiel : efface silencieusement la configuration (utiliser une recréation complète par POST, ou un PATCH sur les templates uniquement)

---

## Solutions de contournement {#working-workarounds}

### Correctif 1 : base du Dockerfile, deux variables d'environnement {#fix-1-dockerfile-baseline-two-environment-variables}

Chaque image Serverless devrait inclure ces deux lignes. Elles constituent l'amélioration minimale et viable de l'observabilité :

```dockerfile
ENV PYTHONUNBUFFERED=1
ENV RUNPOD_DEBUG_LEVEL=DEBUG
```

`PYTHONUNBUFFERED=1` vide stdout à chaque écriture, ce qui garantit que la dernière traceback survit à un `SIGKILL`. `RUNPOD_DEBUG_LEVEL=DEBUG` amène le SDK `runpod-python` à émettre dans stderr les transitions de sa machine à états, les temps d'exécution et le contexte des exceptions. Ces deux éléments sont pris en compte par le log shipper lorsqu'il est attaché (c'est-à-dire pour les crashs après `ready`), ainsi que par le contournement par tee vers un Volume pour les crashs avant `ready`.

### Correctif 2 : mode local FastAPI avec `--rp_serve_api` {#fix-2-rp_serve_api-local-fastapi-mode}

Le SDK `runpod-python` fournit un serveur de développement qui imite localement les endpoints `/run` et `/runsync`. Cela permet de détecter en quelques secondes les crashs à l'exécution du handler (mauvais noms de champs dans la sortie de workflow, incompatibilités de version du SDK, erreurs d'import de custom nodes), au lieu d'attendre un cycle complet de déploiement CI.

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

Limitation : le GPU doit être disponible localement ou via un transfert SSH. Le Network Volume doit être monté en bind sur `/runpod-volume`. Cela ne reproduit pas les particularités d'ordonnancement propres à RunPod, seulement le comportement du code du handler.

### Correctif 3 : tee des logs vers un Volume dans l'entrypoint {#fix-3-volume-log-tee-in-entrypoint}

Ajoutez un tee vers le stockage persistant du Network Volume dans l'entrypoint du conteneur. Cela permet de capturer les crashs survenant avant `ready`, que le log shipper ne voit jamais :

```bash
#!/bin/bash
VOLUME_LOG="/runpod-volume/logs/worker-$(hostname).log"
mkdir -p "$(dirname "$VOLUME_LOG")"

# Redirect all stdout and stderr through tee to volume
exec > >(tee -a "$VOLUME_LOG") 2>&1

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] entrypoint starting"
exec python -u /handler.py "$@"
```

Lisez les logs depuis un Pod de débogage monté sur le même Volume :

```bash
# In a debug Pod (paper-hopper or equivalent) mounted to the same volume:
tail -f /runpod-volume/logs/worker-*.log
```

Pour un suivi en direct à mesure que de nouveaux crashs apparaissent :

```bash
inotifywait -m /runpod-volume/logs -e create -e modify \
  --format '%w%f %e' | \
  while read filepath event; do
    [[ "$filepath" == *.traceback ]] && \
      echo "=== CRASH: $filepath ===" && \
      head -40 "$filepath"
  done
```

### Correctif 4 : flag `--rp_debugger` via variable d'environnement {#fix-4-rp_debugger-flag-via-environment-variable}

Lorsque `RUNPOD_DEBUG_LEVEL=DEBUG` est défini (ou que le handler est lancé avec `--rp_debugger`), le SDK inclut des métadonnées de diagnostic dans chaque payload de réponse de job, sous une clé `debug` : transitions de la machine à états, temps par étape, instantanés mémoire et contexte des exceptions. Pour les jobs en `FAILED`, ces informations apparaissent dans la réponse de statut et sont récupérables via `api.runpod.ai/v2/<endpoint-id>/status/<job-id>` :

```bash
curl -s \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  "https://api.runpod.ai/v2/<endpoint-id>/status/<job-id>" | \
  jq '.output.debug // .error'
```

Cela fonctionne pour les crashs survenant après `ready`. Les crashs survenant avant `ready` ne produisent aucun ID de job.

### Correctif 5 : Pod de débogage sur le même Network Volume {#fix-5-debug-pair-pod-on-same-network-volume}

Lorsque des workers Serverless crashent silencieusement, lancez un Pod utilisant la même image sur le même Network Volume (même datacenter requis) :

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

Le Pod est accessible en SSH via `runpodctl ssh info <pod-id>`. Lisez les logs des workers crashés via le point de montage partagé du Volume, dans `/runpod-volume/logs/`.

---

## États des workers et disponibilité des logs {#worker-states-and-log-availability}

| État du worker | Log shipper attaché ? | Logs visibles dans la Console UI ? | Logs accessibles via API ? |
|---|---|---|---|
| `initializing` | Non | Partiellement (démarrage uniquement) | Non |
| `ready` / `idle` | Oui | Oui | Non |
| `running` | Oui | Oui (temps réel, ~1000–2000 lignes d'historique) | Non |
| `unhealthy` (crash après ready) | Attaché, puis éphémère après le crash | Rétention d'environ 10 min | Non |
| `unhealthy` (crash avant ready) | Jamais attaché | **Aucun** | Non |
| `throttled` | Non | Non | Non |

Limitation de débit des logs : RunPod supprime silencieusement stdout si le débit de sortie est excessif. Aucun seuil en Mo/s ou en lignes/s n'est documenté. Utilisez `runpod.RunPodLogger` plutôt que `print()` pour les journaux à fort volume afin de réduire le risque de limitation.

---

## Pièges à éviter {#gotchas}

- **Problème :** le worker affiche `unhealthy` avec `[error] worker exited with exit code 1` et aucune traceback dans la Console UI. **Correctif :** le crash s'est produit avant l'attachement du log shipper (crash avant ready). Ajoutez le contournement par tee vers le Volume dans votre entrypoint et consultez `/runpod-volume/logs/`. La cause la plus fréquente est une `ImportError` Python au chargement du module ; testez d'abord avec `--rp_serve_api` en local.

- **Problème :** `ENV PYTHONUNBUFFERED=1` est défini, mais des logs manquent encore lors d'un crash. **Correctif :** vérifiez que votre entrypoint lance Python avec `exec python -u` (le flag `-u` outrepasse tout environnement de conteneur qui réinitialiserait la mise en tampon). Vérifiez également que l'entrypoint n'encapsule pas Python dans un shell qui mettrait en tampon : `bash -c "python handler.py"` sans `exec` et sans `-u` ajoute une couche de tampon supplémentaire.

- **Problème :** le Pod de débogage ne voit pas les logs des workers crashés sur le Volume partagé. **Correctif :** les Pods et les workers Serverless doivent être dans le même datacenter pour partager un Network Volume. Les ID de Volume sont liés à une région : `nrdo9nagku` correspond à US-KS-2, `zex70m9p9s` à EU-RO-1. Vérifiez la correspondance de datacenter avant de lancer le Pod de débogage.

- **Problème :** l'exécution de `runpodctl logs <id>` ou `runpodctl exec <id> <cmd>` renvoie une erreur de sous-commande inconnue. **Correctif :** ces sous-commandes n'existent pas. Voir l'issue runpodctl [#29](https://github.com/runpod/runpodctl/issues/29) (ouvert depuis mars 2023). Utilisez plutôt le tee vers le Volume ou le mode local `--rp_serve_api`.

- **Problème :** `RUNPOD_DEBUG_LEVEL=DEBUG` ne produit aucune sortie pour les crashs avant ready. **Correctif :** la sortie de débogage du SDK est émise depuis `runpod.serverless.start()`. Si cet appel ne s'exécute jamais (crash à l'import), aucune sortie de débogage n'est produite. La variable d'environnement n'aide que pour les échecs survenant après l'initialisation.

- **Problème :** stdout apparaît dans la Console UI, mais les 4 Ko finaux (la traceback) sont tronqués. **Correctif :** il s'agit du tampon stdout de Python non vidé avant le `SIGKILL`. Assurez-vous d'avoir à la fois `PYTHONUNBUFFERED=1` dans le Dockerfile et `exec python -u` dans l'entrypoint. Ensemble, ils garantissent que chaque appel à `print()` est un appel système `write()` synchrone.

---

## Voir aussi {#see-also}

- [[runpod-serverless-silent-worker-crashes-on-task-pickup]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-production]]
- [[runpod-flash-gpu-serverless]]
- [[monitoring-and-observability]]
