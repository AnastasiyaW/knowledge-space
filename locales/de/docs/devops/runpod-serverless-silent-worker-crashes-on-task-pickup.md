---
level: 3
source_sha256: a1f7a9d5fbe626e027ba107264acfcce5e00ddf4ba3fdde55765186d1d8d209e
translation: machine
translated_at: '2026-10-24'
---
Hmm, I need to be careful: the YAML block's title and description values must be translated, and I must not add commentary. Let me redo this properly.

---
title: RunPod Serverless: Stille Worker-Abstürze bei der Task-Übernahme
description: Ursachen und Gegenmaßnahmen für Worker, die nach dem Start kommentarlos beenden, bevor sie einen Task abschließen.
---

Hmm — the input front matter block is not present in the source; the source begins directly with the heading after no YAML. Actually, the input shown has no YAML block at the top, so I should not invent one. Here is the correct output:

# RunPod Serverless: Stille Worker-Abstürze bei der Task-Übernahme {#runpod-serverless-silent-worker-crashes-on-task-pickup}

Worker in einer Serverless-Umgebung können als „Ready“ starten, einen Task übernehmen und dann innerhalb von 30–60 Sekunden lautlos sterben. In diesem Zustand erhöhen sich die Zähler `failed` und `completed` nicht, wohl aber der Zähler `unhealthy`, da der Worker-Prozess verschwindet. Dieses Verhalten deutet typischerweise auf einen Fehler im Container-Lebenszyklus oder in der internen Ergebnisbehandlung des `runpod-python`-SDKs hin.

## Primäre Fehlermechanismen {#primary-failure-mechanisms}

Die Stille dieser Abstürze entsteht meist dadurch, dass der Worker-Prozess endet, bevor das RunPod-Framework einen Fehler registrieren kann, oder während einer kritischen Übergabephase.

### Fehler beim Import auf Modulebene {#module-level-import-failures}
Wenn `handler.py` oder ein importiertes benutzerdefiniertes Modul auf oberster Ebene (Modulebene) abstürzt, beendet sich der Prozess, bevor `runpod.serverless.start()` erreicht wird. Da der Handler nie registriert wurde, kann der RunPod-Scheduler die Ausnahme nicht abfangen, was zum Status „unhealthy“ führt, weil der Container unerwartet stoppt.

Zur Diagnose das Container-Image lokal starten, um die Imports zu prüfen:
```bash
docker run --rm -it --gpus all \
  -e RUNPOD_DEBUG=1 \
  --entrypoint python \
  your-registry/image-name:tag \
  -c "import handler"
```

### Regressionen in SDK-Versionen (1.7.11+) {#sdk-version-regressions-1711}
Die Versionen des `runpod-python`-SDKs von 1.7.11 bis 1.8.x enthalten mehrere ungelöste Regressionen, die stille Beendigungen verursachen:
- **Issue #309:** Die interne Funktion `_handle_result` meldet das Ergebnis nicht an den Scheduler zurück, der Prozess endet dennoch, sodass der Zähler `failed` nicht erhöht wird.
- **Issue #458:** TypeErrors durch `current_concurrency: None` führen zu 2–3 Minuten langen Hängern, gefolgt von Container-Neustarts.
- **Issue #432:** Routing-Fehler, bei denen alle Anfragen an einen einzelnen Worker gesendet werden.

Die empfohlene stabile Version ist `runpod==1.7.10`.

### Race Conditions bei Geschwisterprozessen {#sibling-process-race-conditions}
Bei ComfyUI oder ähnlichen Stacks, in denen Handler und Anwendungsserver als Geschwisterprozesse laufen, versucht der Handler unter Umständen, mit dem Server zu kommunizieren, bevor dieser vollständig lauscht (z. B. auf Port 8188). Wirft der Handler einen `ConnectionRefusedError` und ist die Ausnahmebehandlung des SDKs umgangen oder fehlerhaft, beendet sich der Container lautlos.

## Implementierung geschützter Handler {#implementation-of-guarded-handlers}

Um stille Abstürze zu verhindern, einen defensiven Wrapper im Handler implementieren und für Geschwisterprozesse synchrone Prüfungen verwenden.

### Muster für geschützte Handler {#guarded-handler-pattern}
`raise` für erwartbare Fehler vermeiden; stattdessen ein Dictionary mit einem Schlüssel `error` zurückgeben. So stellt das SDK sicher, dass der Fehler an den RunPod-Scheduler gemeldet wird.

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

## Validierung von Infrastruktur und Ressourcen {#infrastructure-and-resource-validation}

### Beschränkungen des Festplattenspeichers {#disk-space-constraints}
Serverless-Templates mit `containerDiskInGb` auf dem Standardwert (oft 20–30 GB) stoßen während der Task-Ausführung häufig auf `ENOSPC` („No space left on device“), wenn das Basis-Image groß ist (z. B. 20 GB+). Dies führt dazu, dass der Kernel den Prozess beendet oder das Dateisystem blockiert, was einen stillen Absturz zur Folge hat.
- **Abhilfe:** Sicherstellen, dass `containerDiskInGb` mindestens das Zweifache der unkomprimierten Image-Größe beträgt. Für ComfyUI-Stacks wird als Mindestwert 60 GB empfohlen.

### Synchrones Testen (runsync) {#synchronous-testing-runsync}
Um die asynchrone Warteschlange zu umgehen und die Fehlermeldungen direkt in der API-Antwort zu sehen, den Endpunkt `/runsync` statt `/run` verwenden.
```bash
curl -X POST https://api.runpod.ai/v2/{endpoint_id}/runsync \
     -H "Authorization: Bearer {api_key}" \
     -H "Content-Type: application/json" \
     -d '{"input": {"test": "data"}}'
```

## Fallstricke {#gotchas}
- **Problem:** SDK-Versionen 1.7.11 und höher haben dokumentierte Regressionen, die die Fehlermeldung unterbrechen. → **Lösung:** `runpod==1.7.10` in das Dockerfile fest eintragen.
- **Problem:** Die Rückgabe eines leeren Dictionaries `{}` aus einem Handler führt in einigen Versionen innerhalb des SDK-Frameworks zu einem `KeyError: 'output'`. → **Lösung:** Immer ein nicht leeres Dictionary mit mindestens einem Status- oder Fehlerschlüssel zurückgeben.
- **Problem:** Durch den Linux-Kernel verursachte Out-of-Memory-(OOM-)Abbrüche erzeugen keine Python-Tracebacks. → **Lösung:** In den RunPod-Konsolenprotokollen nach der Zeichenkette „Killed“ suchen und GPU- oder System-RAM erhöhen.
- **Problem:** Uploads zu Wasabi S3 oder anderen externen Speichern können den Handler blockieren, wenn die Region nicht explizit angegeben ist, was zu einem Timeout-Abbruch führt. → **Lösung:** `region_name` explizit an den boto3-Client übergeben.

## Siehe auch {#see-also}
- [[runpod-production]]
- [[runpod-serverless-python-silent-exit-1]]
- [[runpod-flash-gpu-serverless]]
- [[comfyui-container-build]]
- [[docker-for-ml]]
