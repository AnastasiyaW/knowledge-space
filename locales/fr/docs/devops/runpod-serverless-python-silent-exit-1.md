---
level: 3
source_sha256: ab2aeb52398450d035b101ad83c46b20dcd41195dc310129fbe0211232d9fee2
translation: machine
translated_at: '2026-10-24'
---
# RunPod Serverless Python : sortie silencieuse avec code 1 {#runpod-serverless-python-silent-exit-1}

Analyse et atténuation des plantages silencieux de workers (code de sortie 1) lors de la prise en charge d'une tâche sur RunPod Serverless, en particulier lorsqu'on encapsule des sous-processus lourds comme ComfyUI.

## Classement diagnostique pour le code de sortie 1 {#diagnostic-ranking-for-exit-code-1}
Lorsqu'un worker RunPod se termine avec le code 1 sans traceback dans les logs, la cause est généralement liée à la gestion du cycle de vie des processus plutôt qu'à une simple exception Python.

### 1. Mort du sous-processus et retour gracieux du handler {#1-subprocess-death-and-handler-graceful-return}
Si un sous-processus (par exemple ComfyUI) meurt, le handler peut intercepter une `ConnectionError` ou une `TimeoutError`, la journaliser et renvoyer un statut « failed » au SDK. Cependant, si la boucle d'exécution principale `runpod.serverless.start()` retourne normalement, l'interpréteur Python démarre sa séquence d'arrêt.
- **Condition de concurrence :** les threads démons (comme les processus de vidage des logs Loki) ou les hooks `atexit` peuvent lever une exception pendant l'arrêt de l'interpréteur.
- **Résultat :** CPython se termine avec le code 1, mais comme le logger est déjà en cours d'arrêt, le traceback n'est jamais émis.

### 2. Mise en tampon de la sortie {#2-output-buffering}
Par défaut, Python met en tampon `stdout` et `stderr` lorsqu'ils sont redirigés vers un tube (situation courante dans les environnements conteneurisés).
- **Piège :** si un plantage survient, les derniers Ko de logs (y compris le traceback) peuvent encore se trouver dans le tampon mémoire et ne jamais atteindre les logs du conteneur.
- **Vérification :** si le log est tronqué ou totalement vide après l'initialisation, la mise en tampon est un facteur contributif.

### 3. Échec du script d'entrée {#3-entrypoint-script-failure}
Si `entrypoint.sh` utilise `set -e` et qu'une commande échoue avant `exec python handler.py`, le conteneur se termine immédiatement avec le code 1. Cela arrive souvent lorsque le script du worker tente de vérifier la disponibilité du sous-processus et échoue.

## Atténuation : terminaison forcée du processus {#mitigation-forced-process-termination}
Pour éviter les conditions de concurrence pendant l'arrêt de l'interpréteur (par exemple des threads démons bloqués), utilisez `os._exit(0)` afin de contourner `atexit` et les hooks de nettoyage une fois que le SDK RunPod a terminé.

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

## Atténuation : journalisation sans tampon et hooks d'exception {#mitigation-unbuffered-logging-and-exception-hooks}
Assurez-vous que les logs sont émis immédiatement et que les exceptions non interceptées dans le thread principal sont capturées avant la mort du processus.

### Options d'exécution {#execution-flags}
Modifiez le point d'entrée du conteneur pour forcer une sortie sans tampon.
```bash
export PYTHONUNBUFFERED=1
exec python -u handler.py
```

### Hook global d'exception {#global-exception-hook}
Implémentez un `sys.excepthook` pour écrire les erreurs fatales dans un volume persistant ou sur `stderr` immédiatement.
```python
import sys
import traceback

def fatal_error_hook(exc_type, exc_value, tb):
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, tb))
    sys.stderr.write(f"FATAL EXCEPTION: {error_msg}\n")
    sys.stderr.flush()

sys.excepthook = fatal_error_hook
```

## Vérifications de santé du sous-processus {#subprocess-health-checks}
Si vous encapsulez un outil basé sur une API comme ComfyUI, le handler doit vérifier que le PID est toujours actif. Un simple timeout de `requests.get` est insuffisant.

```python
import os

def is_subprocess_alive(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
```

## Pièges à éviter {#gotchas}
- **Problème :** confusion avec un OOM Kill → **Correction :** vérifiez le code de sortie. Un manque de mémoire (OOM) déclenche un `SIGKILL`, ce qui donne le code de sortie **137**. Le code de sortie **1** correspond à une erreur au niveau logiciel ou à un plantage de l'interpréteur.
- **Problème :** plantages des threads en arrière-plan → **Correction :** `sys.excepthook` de Python n'intercepte que les exceptions du thread principal. Pour les threads en arrière-plan (Python 3.8+), vous devez également définir `threading.excepthook`.
- **Problème :** perte de logs à la sortie → **Correction :** utilisez toujours `sys.stdout.flush()` avant tout appel à `exit()` ou `_exit()` dans un environnement conteneurisé.

## Voir aussi {#see-also}
- [[runpod-production]]
- [[monitoring-and-observability]]
- [[docker-for-ml]]
- [[runpod-flash-gpu-serverless]]
