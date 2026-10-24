---
level: 3
source_sha256: 52390eba927f492b92d335caa98d1c1ff9e48220c2d2cb1af8220f50a52e6e1d
translation: machine
translated_at: '2026-10-24'
---
Let me produce the translation. The YAML front matter: the input begins with a YAML block between --- lines? Looking at the input: it starts with "# RunPod Flash GPU Serverless" — no YAML block. So no front matter to handle. Just translate the body.

Need to keep @@CODE_n@@ lines as is. Headings translated. Keep "Endpoint", "Dockerfile", "Flash" as is. Translate prose.

Note "Pattern 3" in gotchas: "Custom Docker" pattern — keep the English term in backticks? "`Custom Docker`" is a pattern name, not inline code in the source; it's in backticks in source, so keep. Pattern 3 translate "Muster 3"? The pattern list heading is "Deployment Patterns" -> "Deployment-Muster" maybe. I'll use "Deployment-Muster".

Wiki links: keep byte-identical.


# RunPod Flash GPU Serverless {#runpod-flash-gpu-serverless}

RunPod Flash ist ein Open-Source-Python-SDK (MIT-Lizenz, v1.16.0), das die Bereitstellung GPU-beschleunigter Serverless-Funktionen über eine decorator-basierte Schnittstelle ermöglicht. Es automatisiert die Bereitstellung von Workern, die Einrichtung der Umgebung und die Verwaltung von Abhängigkeiten und macht manuelle Dockerfile-Erstellung sowie die Pflege einer Container-Registry überflüssig.

## Kernarchitektur und Implementierung {#core-architecture-and-implementation}
Flash-Funktionen werden mit dem `@Endpoint`-Decorator definiert, der Hardwareanforderungen und Software-Abhängigkeiten festlegt. Das SDK übernimmt den plattformübergreifenden Build-Prozess, sodass Entwickler auf macOS (M-Serie) oder Linux Remote-x86_64-GPU-Umgebungen als Ziel angeben können.

### Definition einer Serverless-Funktion {#serverless-function-definition}
```python
from runpod_flash import Endpoint, GpuType

@Endpoint(
    name="tensor-processor",
    gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,
    workers=(0, 10), # scale-to-zero to 10 max workers
    dependencies=["torch>=2.4.0", "numpy", "pillow"]
)
async def process_data(payload):
    # Logic executes on remote RunPod Serverless infrastructure
    import torch
    return {"device": str(torch.cuda.get_device_name(0))}
```

### Bereitstellungs-Workflow {#deployment-workflow}
Die CLI verwaltet die Authentifizierung und den Lebenszyklus der Endpoints:
```bash
pip install runpod-flash
flash login   # OAuth browser flow
flash deploy  # Provisions infrastructure and uploads code
```

## Ressourcenverwaltung und Hardwareauswahl {#resource-management-and-hardware-selection}
Das SDK verwendet typisierte Enums für eine präzise Hardware-Auswahl sowie flexible Skalierungskonfigurationen.

- **GPU-Typen:** Auswahl spezifischer Modelle über `GpuType` (z. B. `NVIDIA_A100_80GB_PCIe`, `NVIDIA_GEFORCE_RTX_4090`).
- **GPU-Gruppen:** Verwendung von `GpuGroup` (z. B. `GpuGroup.AMPERE_80`, `GpuGroup.ANY`), damit der Provisioner den ersten verfügbaren kompatiblen Knoten auswählen kann.
- **Worker-Skalierung:** Der Parameter `workers=(min, max)` aktiviert die Logik für Scale-to-Zero, um Leerlaufkosten zu vermeiden.
- **Speicher:** Die Integration von `NetworkVolume` bietet persistenten, rechenzentrumsübergreifenden Speicher für Modellgewichte oder Datensätze.
- **Umgebungsvariablen:** Flash schließt die Werte von Umgebungsvariablen aus dem Konfigurations-Hash aus. Dadurch lösen eine Rotation von Secrets oder Konfigurationsänderungen keinen Neubau des Images aus.

## Bereitstellungsmuster {#deployment-patterns}
1. **Queue-basiert (asynchron):** Standardmuster für Batch-Verarbeitungsjobs, die über die async API des SDK ausgelöst werden.
2. **Load-balanced API:** HTTP-erreichbare Routen, die sich einen gemeinsamen Pool skalierender Worker teilen.
3. **Custom Docker Orchestration:** Integration bestehender, vorgefertigter Images (z. B. vLLM, TensorRT-LLM, ComfyUI) in die Flash-Orchestrierungsschicht.
4. **Entwicklungsmodus:** Ephemere Worker-Bereitstellung über `flash dev --auto-provision` für lokales Debugging gegen Remote-GPU-Ressourcen.

## Betriebliche Einschränkungen {#operational-constraints}
- **Paketlimits:** Die Gesamtgröße der Bereitstellung (Code + lokale Abhängigkeiten) ist auf 500 MB begrenzt.
- **Laufzeitunterstützung:** Beschränkt auf Python 3.10, 3.11 und 3.12.
- **Cold Starts:** Umfangreiche Abhängigkeitsstapel (z. B. `torch` + `diffusers`) können Cold Starts von mehreren Minuten verursachen.
- **Host-Anforderungen:** Die lokale Entwickler-CLI erfordert macOS oder Linux; Windows-Umgebungen werden nur über WSL2 unterstützt.

## Stolperfallen {#gotchas}
- **Problem:** Hoher Abhängigkeitsaufwand führt zum Überschreiten des 500-MB-Limits der Bereitstellung oder zu langsamen Cold Starts. → **Lösung:** Große statische Assets und Modellgewichte in ein `NetworkVolume` verschieben und dieses im Worker einhängen, statt sie im Bereitstellungspaket zu bündeln.
- **Problem:** Standardmäßige pip-Installationen im Decorator schlagen bei privaten oder komplexen Paketen fehl. → **Lösung:** Das Muster `Custom Docker` (Muster 3) verwenden, um eine vorgefertigte Umgebung bereitzustellen und Flash weiterhin zur Orchestrierung zu nutzen.
- **Problem:** Die lokale Ausführung unter Windows kann die Flash-CLI nicht initialisieren. → **Lösung:** Einen Linux-basierten Entwicklungscontainer oder WSL2 verwenden, da die native Windows-Shell für lokale Builds nicht unterstützt wird.

## Siehe auch {#see-also}
- [[runpod-production]]
- [[docker-for-ml]]
- [[deployment-strategies]]
- [[kubernetes-resource-management]]
