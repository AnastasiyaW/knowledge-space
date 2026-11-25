---
level: 3
source_sha256: 232647fc555ee120803bc81f920355994d1b3880a848943c33850ae9ce7611f7
translation: machine
translated_at: '2026-10-24'
---
# RunPod Production Patterns {#runpod-production-patterns}

Referenz für das Deployment von GPU-Workloads auf RunPod: Auswahl des Deploy-Typs, Image-Strategie in drei Stufen, Architektur der Serverless-Worker, Secrets-Management und typische Fehlerbilder.

## Auswahl des Deploy-Typs {#deploy-type-selection}

| Anwendungsfall | Deploy-Typ | Abrechnung |
|----------------|------------|------------|
| Training / Fine-Tuning (Stunden/Tage) | **Pod** | Pro Stunde, Leerlaufzeit inklusive |
| Debugging, interaktives ComfyUI | **Pod** | Pro Stunde, Leerlaufzeit inklusive |
| Produktive Inferenz-API | **Serverless** | Nur aktive Sekunden |
| Ungleichmäßiger Traffic (Spitzen + Leerlauf) | **Serverless** | 60–70 % Ersparnis gegenüber Dauerbetrieb |
| Hybrid: Serverless-Frontend + lange Tasks | **Instant Clusters** | Gemischt |

**Entscheidungsregel:** Konstante Last → Pod. Ungleichmäßig / API-Endpoint → Serverless.

## Image-Strategie (3 Stufen) {#image-strategy-3-tiers}

### Stufe 1 — RunPod-gecacht (Pull 10–60 Sek.) {#tier-1-runpod-cached-10-60-sec-pull}
```text
runpod/pytorch:2.11.0-cuda13.0-cudnn9-devel
runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
runpod/worker-comfyui:<version>-base
runpod/worker-comfyui:<version>-flux1-dev
runpod/base:0.6.x-cuda...
```
Auf Secure-Cloud-Nodes gecacht. Für die Community Cloud nicht garantiert.

### Stufe 2 — Beliebte Docker-Hub-Images (Pull 1–5 Min.) {#tier-2-popular-docker-hub-1-5-min-pull}
```text
pytorch/pytorch:2.11.0-cuda13.0-cudnn9-devel
nvidia/cuda:*  (sometimes cached, sometimes not)
```

### Stufe 3 — Eigene Images (3–10 Min. oder HÄNGT) {#tier-3-custom-images-3-10-min-or-stuck}
```text
ghcr.io/your-org/your-image:tag
nvidia/cuda:13.0.0-devel-ubuntu22.04  ← confirmed stuck on 4/4 pods (2026-04-17)
```

**Regel:** Immer zuerst Stufe 1 prüfen. Wenn CUDA-/PyTorch-Version zu Stufe 1 passt, dieses Image verwenden.  
Eigene Images (Stufe 3) werden als Overlay auf einem Stufe-2-Basis-Image nach `ghcr.io` gepusht, nicht als nacktes `nvidia/cuda`.

## FlashBoot {#flashboot}

Kostenlose Optimierung des Cold Starts, standardmäßig aktiviert.

- 48 % der Cold Starts sind in <200 ms abgeschlossen
- Typisch: 1–2 Sek. Cold Start
- ComfyUI: 50–80 % schnellere Cold Starts mit FlashBoot
- Mechanismus: Häufigere Aufrufe → RunPod hält Worker auf dem Host „warm“

**Anzahl aktiver Worker ≥ 1** reduziert den Cold Start auf ca. 0 ms (zum Preis eines Dauerbetriebs).

## Network Volumes (Modellspeicher) {#network-volumes-model-storage}

```bash
# Create volume in RunPod Console → pick region closest to traffic source
# Mount volume in pod/worker:
# /opt/ComfyUI/models → Network Volume path

# Pre-load models via cheap CPU pod:
rsync -av ./models/ /workspace/models/
# Or: aws s3 sync s3://your-bucket/models /workspace/models/
```

**Preise:** 0,07 $/GB/Monat für das erste TB, 0,05 $/GB darüber.  
**Einsatz, wenn:** Modelle >10 GB groß sind, häufig aktualisiert werden und sich mehrere Pods teilen.  
**Eingebackene Modelle im Image:** Nur für stabile Modelle ≤10 GB, die sich selten ändern.

## worker-comfyui-Muster {#worker-comfyui-pattern}

Offizielles Serverless-Muster (`github.com/runpod-workers/worker-comfyui`).

### Request-Format {#request-format}

```json
{
  "input": {
    "workflow": {},
    "images": [{"name": "input.png", "image": "<base64>"}],
    "api_key_override": ""
  },
  "webhook": "https://your-endpoint/callback"
}
```

### Response-Format (v5.0.0+) {#response-format-v500}

```json
{
  "output": {
    "images": [
      {"filename": "out.png", "type": "base64", "data": "..."}
    ],
    "errors": []
  }
}
```

### Endpoints {#endpoints}
- `/run` — asynchron, Payload bis 10 MB
- `/runsync` — synchron, Payload bis 20 MB
- `/health` — Statusprüfung

### SSH-Zugriff zum Debugging {#ssh-debug-access}
```bash
# Set env var in pod template:
PUBLIC_KEY=<your-ssh-public-key>
# Opens port 22 for SSH access into worker
```

## Secrets-Management {#secrets-management}

```bash
# In RunPod Console → Account → Secrets → create named secret
# Reference in template env vars:
RUNPOD_SECRET_WASABI_ACCESS_KEY=my-wasabi-key-name
RUNPOD_SECRET_WASABI_SECRET_KEY=my-wasabi-secret-name
# Runtime substitutes encrypted value → plain env var inside container
```

**Scoped API-Keys (2026):** Keys pro Endpoint mit Nutzungsverfolgung anlegen. Prinzip der minimalen Berechtigung.

## GPU-Auswahlmatrix {#gpu-selection-matrix}

| GPU | Architektur | flash-attn2 | flash-attn3 | Hinweise |
|-----|-------------|-------------|-------------|----------|
| A100 | sm_80 | Ja | Nein | Standard, breit verfügbar |
| H100 | sm_90 | Ja | Ja (+30–50 % gegenüber FA2) | Am besten für HF/Training |
| H200 | sm_90 | Ja | Ja | Neueste Generation, knapp verfügbar |
| A40 | sm_86 | Ja | Nein | Budget-Training |
| RTX 4090 | sm_89 | Ja | Nein (sm_89 < sm_90) | Consumer, günstig |

**Auswahl der Flash-Attention-Laufzeit:**
```python
import torch
cap = torch.cuda.get_device_capability()
if cap[0] >= 9:
    # H100, H200 → FA3 via HF Kernels
    from kernels import get_kernel
    fa = get_kernel("kernels-community/vllm-flash-attn3",
                    arch=f"sm_{cap[0]}{cap[1]}")
else:
    # A100 → FA2
    fa = get_kernel("kernels-community/flash-attn2",
                    arch=f"sm_{cap[0]}{cap[1]}")
```

## CI/CD-Muster {#cicd-pattern}

```yaml
# .github/workflows/deploy.yml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ghcr.io/org/image:${{ github.sha }},ghcr.io/org/image:latest
    cache-from: type=registry,ref=ghcr.io/org/image:buildcache
    cache-to: type=registry,ref=ghcr.io/org/image:buildcache,mode=max
```

**Unveränderliche Tags:** `:sha` wird nie verändert. `:latest` ist nur ein wandernder Zeiger.

## 8 typische Fallstricke {#8-common-pitfalls}

| Symptom | Ursache | Behebung |
|---------|---------|----------|
| Image-Pull hängt dauerhaft | Stufe-3-Image nicht von RunPod gecacht, Docker-Hub-Rate-Limit | Stufe 1/2 verwenden; eigenes Image als Overlay nach ghcr.io pushen |
| CUDA-Mismatch zur Laufzeit | CUDA des Basis-Images ≠ CUDA der installierten PyTorch-Version | Exakt abgleichen: `cu130`-Wheels benötigen ein CUDA-13.0-Basis-Image |
| Null-GPU-Skalierung, bleibt bei 0 Workern | Health Check des Workers schlägt fehl | `PUBLIC_KEY` für SSH-Debugging prüfen; `/health`-Endpoint testen |
| OOM bei großen Modellen | Modell wird pro Request statt einmalig geladen | Modell in der Initialisierung von `handler.py` laden, nicht innerhalb der Funktion `handler()` |
| Kosten laufender Idle-Pods | Pod nach der Sitzung weiter aktiv | Für Produktion Serverless verwenden; für Dev-Pods Stop-bei-Leerlauf setzen |
| Secrets nicht zugänglich | Einfacher Umgebungsvariablenname statt `RUNPOD_SECRET_*` referenziert | Im Template das Präfix `RUNPOD_SECRET_<secret-name>` verwenden |
| Community-Cloud-Pods hängen | Image-Pull auf Community-Nodes unzuverlässig | Für Stufe-3-Images Secure Cloud verwenden |
| Blackwell-GPU inkompatibel | sm_100-Wheels noch nicht verfügbar | Wheel-Kompatibilität prüfen; bis zur Unterstützung A100/H100 nutzen |

## Gotchas {#gotchas}

- **Problem:** `nvidia/cuda:13.0.0-devel-ubuntu22.04` direkt als Pod-Image verwendet → hängt bei 4/4 aufeinanderfolgenden Pods auf A5000/A40/L40S. -> **Lösung:** `pytorch/pytorch:2.11.0-cuda13.0-cudnn9-devel` als Basis verwenden (gleiches CUDA 13, gleiches PyTorch 2.11, korrekt gecacht). Rohe `nvidia/cuda`-Images niemals direkt als RunPod-Ziele verwenden.
- **Problem:** Modell wird auf die lokale Festplatte des Containers geladen → geht verloren, wenn der Pod beendet wird. -> **Lösung:** Für Modelle >1 GB immer Network Volumes verwenden. Volume unter `/workspace/models` einbinden. Sentinel-Datei `.models_provisioned` nutzen, um beim Neustart das erneute Herunterladen zu überspringen.
- **Problem:** Serverless-Worker lädt ein schweres Modell innerhalb der Funktion `handler()` → 30 Sekunden Cold Start pro Request. -> **Lösung:** Modell auf Modulebene laden (außerhalb des Handlers): `model = load_model()`, einmalig bei der Worker-Initialisierung ausgeführt.
- **Problem:** Sitzungen mit `--resume` / `--continue`, deren Verlauf abrechnungsbezogene Zeichenketten enthält, lösen einen Fehler bei der Cache-Invalidierung aus (v2.1.100), wodurch sich die Token-Kosten um den Faktor 10–20 erhöhen. -> **Lösung:** `--resume` vermeiden, bis der Fehler nachweislich behoben ist; für lange Workflows neue Sitzungen starten.

## Siehe auch {#see-also}

- [[docker-for-ml]]
- [[container-registries]]
- [[dockerfile-and-image-building]]
- [[cicd-pipelines]]
