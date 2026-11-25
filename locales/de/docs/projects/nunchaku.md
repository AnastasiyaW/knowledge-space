---
title: "Nunchaku — Ausweitung der Modellintegration"
category: projects
date: 2026-01-23
tags: [model-integration-expansion, nunchaku, project]
aliases: ["Nunchaku"]
level: 3
source_sha256: 318b3f1f35208adc5ddc1eed09bf5a8121bd04e80cb1a16013c770b250f9c593
translation: machine
translated_at: '2026-10-24'
---
# Nunchaku — Ausweitung der Modellintegration {#nunchaku-model-integration-expansion}

**Entwicklungslinie:** `project:nunchaku` · Thread `model-integration-expansion`  
**Letztes Ereignis:** 2026-01-23 · 3 datierte Einträge seit 2025-08-03 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Nunchaku ist eine SVDQuant-4-Bit-Inference-Engine für Nutzer von Diffusers und ComfyUI, die Transformer für FLUX oder Qwen Image mit niedrigerer Präzision benötigen, nicht ein weiteres Basismodell.

- Transformer-Gewichte: Lädt INT4- oder FP4-SVDQuant-Gewichte über Diffusers-kompatible Klassen.
- Framework-Unterstützung: Stellt Python- und ComfyUI-Routen für FLUX, Qwen Image/Edit, ControlNets und Z-Image bereit.

Wir müssen das Wheel auf PyTorch, CUDA, Python und GPU abstimmen; die Dokumentation ist mit 1.3.0 gekennzeichnet, während GitHub v1.2.1 als neueste formale Version ausweist.
Wir verwenden einen offiziellen Nunchaku-Modell-Namespace und einen versionsgleichen Workflow und behandeln das QuantFunc-2511-Artefakt als separate Implementierung.

## Entwicklungslinie {#development-line}

- **2025-08-03 — Nunchaku veröffentlichte Integrationsressourcen für FLUX.1-Krea-dev.** Am 2025-08-03 ergänzte Nunchaku ein Hugging-Face-Repository und ein GitHub-Beispiel für FLUX.1-Krea-dev. Das Beispiel dokumentierte einen Implementierungsweg für dieses Modell.
- **2025-09-24 — Nunchaku dokumentierte die Integration von Qwen Image Edit 2509.** Am 2025-09-24 dokumentierte Nunchaku die Nutzung von Qwen Image Edit 2509 und verlinkte ein Modell-Repository und einen ComfyUI-Workflow. Diese Dateien bieten einen operativen Integrationsweg für diese Bildbearbeitungsvariante.
- **2026-01-23 — Ein Qwen-Image-Edit-2511-Modell-Repository mit Nunchaku-Namen erschien.** Am 2026-01-23 veröffentlichte QuantFunc das Repository Nunchaku-Qwen-Image-EDIT-2511 auf Hugging Face. Die Datei führte nach der 2509-Integration ein weiteres Qwen-Image-Edit-Modellartefakt ein.

## Was sich geändert hat {#what-changed}

- 2025-08-03 — Nunchaku ergänzte 4-Bit-Unterstützung für FLUX.1-Krea-dev mit SVDQuant-Transformer-Gewichten für den FLUX-kompatiblen Checkpoint.
- 2025-09-24 — Nunchaku veröffentlichte 4-Bit-Gewichte für Qwen-Image-Edit-2509 sowie die Diffusers- und ComfyUI-Integration mit INT4/NVFP4- und Rang-Optionen.
- 2026-01-23 — QuantFunc veröffentlichte den Qwen-Image-Edit-2511-Checkpoint mit Nunchaku-Namen als unabhängige Requantisierung und nicht als offizielle Nunchaku-Veröffentlichung.

## Anwendung {#how-to-use-this}

Stand 2026-01-23 wählen wir Nunchaku-Ressourcen anhand der exakt unterstützten Modellvariante aus und verwenden die bereitgestellte modellspezifische Dokumentation oder den entsprechenden Workflow. So vermeiden wir die Annahme, dass ein einziges Setup FLUX.1-Krea-dev und die Qwen-Image-Edit-Varianten gleichermaßen abdeckt.

1. Installiere ein vorgefertigtes Wheel erst, nachdem du es auf PyTorch 2.5 oder neuer, CUDA, Python und GPU-Architektur abgestimmt hast; baue aus dem Quellcode nur dann, wenn kein kompatibles Wheel existiert.
  — <https://nunchaku.tech/docs/nunchaku/installation/installation.html>
2. Für ComfyUI installiere das Plugin ComfyUI-nunchaku und danach das Nunchaku-Backend in dieselbe Python-Umgebung, in der ComfyUI läuft.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/installation.html>
3. Lade das passende quantisierte Nunchaku-Modell und die Basismodell-Assets herunter, importiere ein offizielles Beispiel-Workflow, starte ComfyUI und wähle dann diesen Workflow aus.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/usage.html>
4. Für Qwen-Image-Edit-2509 in Python lädst du den Nunchaku-Transformer über NunchakuQwenImageTransformer2DModel, verwendest QwenImageEditPlusPipeline mit dem vorgelagerten Basismodell und übergibst die RGB-Bildliste, wie im offiziellen Beispiel.
  — <https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509>
5. Im Wheel Installer von ComfyUI aktualisierst du die Versionsliste, wählst eine offizielle Version aus, installierst sie und startest ComfyUI anschließend vollständig neu; die separate Steuerung für Entwicklungsversionen verwendest du nur für Entwicklungsbuilds.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/workflows/tools.html>

## Best Practices {#best-practices}

- Verwende FP4 mit RTX-50-Serie-Blackwell-GPUs und INT4 auf den anderen aufgeführten GPU-Architekturen; Blackwell erfordert außerdem PyTorch 2.7 oder neuer mit CUDA 12.8 oder neuer.
  — <https://nunchaku.tech/docs/nunchaku/installation/installation.html>
- Wähle für Qwen-Image-Edit-2509 r32, wenn Geschwindigkeit zählt, und r128, wenn die Ausgabequalität wichtiger ist; vergleiche deren Durchsatz nicht, als wären es gleichwertige Konfigurationen.
  — <https://huggingface.co/nunchaku-tech/nunchaku-qwen-image-edit-2509>
- Bei wenig VRAM verwende das asynchrone Offloading von Nunchaku; wenn du das sequentielle CPU-Offloading von Diffusers ergänzt, schließe den Nunchaku-Transformer davon aus, da sein Offloading-Pfad anders funktioniert. Die dokumentierte Konfiguration kann den Verbrauch auf etwa 3 GB senken.
  — <https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509>
- Fixiere Qwen-Image-Edit-2509 auf diffusers 0.36.0 oder neuer und plane keine offizielle Unterstützung für eigene LoRAs dafür ein, bis sich die Dokumentation ändert.
  — <https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509>
- Bevorzuge für Produktivbetrieb den offiziellen Versionsauswahlschalter des Wheel Installers gegenüber dem Auswahlschalter für Entwicklungsversionen und starte ComfyUI nach jeder Paketänderung neu.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/workflows/tools.html>
- Halte die Qwen-Image-Edit-2511-Gewichte von QuantFunc außerhalb des offiziellen Nunchaku-Kompatibilitätspfads; sie zielen auf die eigene Engine von QuantFunc und sind ausdrücklich unabhängig von Nunchaku.
  — <https://www.modelscope.cn/models/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511>

## Hiermit ersetzt {#superseded-by-this}

- Die Aussage vom 2025-09-24, dass Lightning-Modelle für Qwen-Image-Edit-2509 später erscheinen würden — seit 2025-09-25 überholt.
- Die Annahme, dass jeder Checkpoint mit dem Wort Nunchaku ein offizielles Nunchaku-Projektrelease ist — seit der späteren Klarstellung durch QuantFunc im Jahr 2026-07 überholt.

## Weiterhin unbekannt {#still-unknown}

- Die aktuelle Dokumentation ist mit 1.3.0 gekennzeichnet, aber GitHub weist v1.2.1 als neueste formale Version aus und listet nur v1.3.0dev-Vorabversionen; wir haben keine Release-Notiz zu einer stabilen Version v1.3.0 gefunden.
- Wir haben keine aktuelle offizielle Nunchaku-Supportseite für Qwen-Image-Edit-2511 gefunden. Der QuantFunc-Checkpoint vom 2026-01-23 ist eine unabhängige Requantisierung und daher kein Beleg für offizielle Nunchaku-Kompatibilität.
- Die ursprünglichen nunchaku-tech-Links leiten auf nunchux-ai bei GitHub und nunchaku-ai bei Hugging Face weiter. Eine gesonderte offizielle Ankündigung der Umbenennung haben wir nicht gefunden; reproduziere Workflows daher vom aufgelösten Ziel aus und fixiere die exakte Version oder Modelldatei.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/nunchaku-tech/nunchaku | Nunchaku repository README | 2026-09-04 |
| https://github.com/nunchux-ai/nunchaku/releases | Nunchaku GitHub releases | 2026-09-04 |
| https://www.krea.ai/blog/flux-krea-open-source-release | Releasing Open Weights for FLUX.1 Krea | 2026-09-04 |
| https://huggingface.co/nunchaku-tech/nunchaku-flux.1-krea-dev/tree/main | nunchaku-flux.1-krea-dev model files | 2026-09-04 |
| https://huggingface.co/nunchaku-tech/nunchaku-qwen-image-edit-2509 | Nunchaku Qwen-Image-Edit-2509 model card | 2026-09-04 |
| https://huggingface.co/Qwen/Qwen-Image-Edit-2509 | Qwen-Image-Edit-2509 model card | 2026-09-04 |
| https://huggingface.co/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511 | QuantFunc Nunchaku-Qwen-Image-EDIT-2511 model card | 2026-09-04 |
| https://www.modelscope.cn/models/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511 | QuantFunc Nunchaku-Qwen-Image-EDIT-2511 on ModelScope | 2026-09-04 |
| https://nunchaku.tech/docs/nunchaku/ | Nunchaku documentation 1.3.0 | 2026-09-04 |
| https://nunchaku.tech/docs/nunchaku/installation/installation.html | Nunchaku installation guide | 2026-09-04 |
| https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509 | Nunchaku Qwen-Image-Edit usage guide | 2026-09-04 |
| https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/installation.html | ComfyUI-nunchaku installation guide | 2026-09-04 |
| https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/usage.html | ComfyUI-nunchaku usage guide | 2026-09-04 |
| https://nunchaku.tech/docs/ComfyUI-nunchaku/workflows/tools.html | ComfyUI-nunchaku wheel-installer workflow | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:nunchaku`, Thread `model-integration-expansion`, 3 datierte Ereignisse 2025-08-03 → 2026-01-23.
- **Praxishinweis:** Stand 2026-01-23 wählen wir Nunchaku-Ressourcen anhand der exakt unterstützten Modellvariante aus und verwenden die bereitgestellte modellspezifische Dokumentation oder den entsprechenden Workflow. So vermeiden wir die Annahme, dass ein einziges Setup FLUX.1-Krea-dev und die Qwen-Image-Edit-Varianten gleichermaßen abdeckt.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was überholt ist.
