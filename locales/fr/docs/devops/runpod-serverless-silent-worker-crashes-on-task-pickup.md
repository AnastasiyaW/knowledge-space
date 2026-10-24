---
level: 3
source_sha256: a1f7a9d5fbe626e027ba107264acfcce5e00ddf4ba3fdde55765186d1d8d209e
translation: machine
translated_at: '2026-10-24'
---
# RunPod Serverless : plantages silencieux des workers lors de la prise en charge d'une tâche {#runpod-serverless-silent-worker-crashes-on-task-pickup}

Dans un environnement serverless, des workers peuvent démarrer en état « Ready », prendre une tâche, puis mourir silencieusement dans les 30 à 60 secondes. Dans cet état, les compteurs `failed` et `completed` n'augmentent pas, mais le compteur `unhealthy` s'incrémente à mesure que le processus du worker disparaît. Ce comportement indique généralement une défaillance dans le cycle de vie du conteneur ou dans la gestion interne des résultats du SDK `runpod-python`.

## Mécanismes de défaillance principaux {#primary-failure-mechanisms}

Le caractère silencieux de ces plantages provient en général du fait que le processus du worker se termine avant que le framework RunPod ait pu enregistrer une erreur, ou pendant une phase critique de transfert.

### Échecs d'import au niveau du module {#module-level-import-failures}
Si `handler.py` ou l'un des modules personnalisés importés plante au niveau supérieur (portée du module), le processus se termine avant que `runpod.serverless.start()` ne soit atteint. Comme le handler n'a jamais été enregistré, le planificateur RunPod ne peut pas capturer l'exception, ce qui se traduit par un statut « unhealthy » lorsque le conteneur s'arrête de façon inattendue.

Pour diagnostiquer le problème, exécutez l'image du conteneur localement afin de vérifier les imports :
```bash
docker run --rm -it --gpus all \
  -e RUNPOD_DEBUG=1 \
  --entrypoint python \
  your-registry/image-name:tag \
  -c "import handler"
```

### Régressions des versions du SDK (1.7.11+) {#sdk-version-regressions-1711}
Les versions du SDK `runpod-python` comprises entre 1.7.11 et 1.8.x contiennent plusieurs régressions non résolues qui provoquent des sorties silencieuses :
- **Issue #309 :** la fonction interne `_handle_result` ne parvient pas à renvoyer le résultat au planificateur, mais le processus se termine, ce qui empêche l'incrémentation du compteur `failed`.
- **Issue #458 :** des erreurs TypeError liées à `current_concurrency: None` provoquent des blocages de 2 à 3 minutes, suivis de redémarrages du conteneur.
- **Issue #432 :** des bugs de routage envoient toutes les requêtes vers un seul worker.

La version stable recommandée est `runpod==1.7.10`.

### Conditions de concurrence entre processus frères {#sibling-process-race-conditions}
Dans ComfyUI ou des stacks similaires, où le handler et le serveur applicatif tournent comme processus frères, le handler peut tenter de communiquer avec le serveur avant que celui-ci ne soit pleinement à l'écoute (par exemple sur le port 8188). Si le handler lève une `ConnectionRefusedError` et que la gestion des exceptions du SDK est contournée ou défaillante, le conteneur se termine silencieusement.

## Mise en œuvre de handlers protégés {#implementation-of-guarded-handlers}

Pour éviter les plantages silencieux, implémentez un wrapper défensif dans le handler et utilisez des vérifications synchrones pour les processus frères.

### Modèle de handler protégé {#guarded-handler-pattern}
Évitez d'utiliser `raise` pour les erreurs attendues ; renvoyez plutôt un dictionnaire contenant une clé `error`. Cela garantit que le SDK transmet bien l'échec au planificateur RunPod.

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

## Validation de l'infrastructure et des ressources {#infrastructure-and-resource-validation}

### Contraintes d'espace disque {#disk-space-constraints}
Les templates serverless dont `containerDiskInGb` est laissé à la valeur par défaut (souvent 20 à 30 Go) rencontrent fréquemment l'erreur `ENOSPC` (No space left on device) pendant l'exécution des tâches lorsque l'image de base est volumineuse (par exemple 20 Go et plus). Le noyau tue alors le processus, ou le système de fichiers se bloque, ce qui entraîne un plantage silencieux.
- **Solution :** veillez à ce que `containerDiskInGb` soit au moins égal à deux fois la taille non compressée de l'image. Pour les stacks ComfyUI, 60 Go constituent le minimum recommandé.

### Test synchrone (runsync) {#synchronous-testing-runsync}
Pour contourner la file d'attente asynchrone et voir directement les messages d'erreur bruts dans la réponse de l'API, utilisez l'endpoint `/runsync` à la place de `/run`.
```bash
curl -X POST https://api.runpod.ai/v2/{endpoint_id}/runsync \
     -H "Authorization: Bearer {api_key}" \
     -H "Content-Type: application/json" \
     -d '{"input": {"test": "data"}}'
```

## Pièges courants {#gotchas}
- **Problème :** les versions 1.7.11 et supérieures du SDK présentent des régressions documentées qui cassent la boucle de remontée des erreurs. → **Correctif :** épinglez `runpod==1.7.10` dans votre Dockerfile.
- **Problème :** renvoyer un dictionnaire vide `{}` depuis un handler provoque une `KeyError: 'output'` dans le framework du SDK, selon les versions. → **Correctif :** renvoyez toujours un dictionnaire non vide contenant au moins une clé de statut ou d'erreur.
- **Problème :** les arrêts pour dépassement de mémoire (OOM) déclenchés par le noyau Linux ne produisent aucune trace Python. → **Correctif :** surveillez la chaîne « Killed » dans les logs de la RunPod Console et augmentez la RAM du GPU ou du système.
- **Problème :** les envois vers Wasabi S3 ou un autre stockage externe peuvent bloquer le handler si la région n'est pas explicitement définie, ce qui provoque un arrêt pour timeout. → **Correctif :** passez explicitement `region_name` au client boto3.

## Voir aussi {#see-also}
- [[runpod-production]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-flash-gpu-serverless]]
- [[comfyui-container-build]]
- [[docker-for-ml]]
