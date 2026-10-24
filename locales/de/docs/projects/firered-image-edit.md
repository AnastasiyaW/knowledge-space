---
title: "FireRed Image Edit — ComfyUI-Ressourcen"
category: projects
date: 2026-03-17
tags: [comfyui-resources, firered, firered-image-edit, project]
aliases: ["FireRed Image Edit"]
level: 3
source_sha256: 5f484c2ba722a5868b668a84372372a36fa4c3e43f6257297d1b59320f84c091
translation: machine
translated_at: '2026-10-24'
---
# FireRed Image Edit — ComfyUI-Ressourcen {#firered-image-edit-comfyui-resources}

**Entwicklungslinie:** `project:firered-image-edit` · Thread `comfyui-resources`  
**Letztes Ereignis:** 2026-03-17 · 1 datierter Eintrag seit 2026-03-17 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

FireRed Image Edit ist ein lokaler, anweisungsgesteuerter Bildeditor für ComfyUI und Diffusers.

- Bearbeitung von Quellbildern auf Basis von Textanweisungen.
- Referenzfusion mit 1 bis 3 Bildern für Porträts, Textstil, Make-up, Restaurierung und virtuelles Anprobieren.

Der BF16-Transformer allein benötigt 40,9 GB. Der separate optimierte Pfad gibt 30 GB und eine Laufzeit von etwa 4,5 Sekunden an.

## Entwicklungslinie {#development-line}

- **2026-03-17 — Eine ComfyUI-Ressource für FireRed Image Edit 1.1 wurde verlinkt.** Eine Nachricht im FireRed-Thread verlinkte am 2026-03-17 ein Hugging-Face-Repository für FireRed Image Edit 1.1 für ComfyUI. Die gleiche Nachricht enthielt 3 RunningHub-URLs. Zu den verlinkten Inhalten, einem Release, Fähigkeitsänderungen oder Workflow-Details liegen uns keine Belege vor. Wir erfassen nur die datierte Veröffentlichung dieser Ressourcenlinks.

## Was sich geändert hat {#what-changed}

- 2026-02-12 — Der technische Bericht zu v1 etablierte das Modell für anweisungsbasierte Bearbeitung.
- 2026-02-14 — Die Gewichte von FireRed-Image-Edit-1.0 wurden verfügbar.
- 2026-02-27 — Das Team ergänzte einen Agent-Pfad und einen ComfyUI-Workflow für 1.0.
- 2026-03-01 — Ein optimierter lokaler Inferenzpfad wurde dokumentiert.
- 2026-03-03 — FireRed-Image-Edit-1.1 wurde als Nachfolger von 1.0 veröffentlicht, mit Verbesserungen bei Porträtkonsistenz, Multi-Element-Fusion, gestyltem Text und Make-up.
- 2026-03-04 — Das offizielle ComfyUI-Paket für 1.1 erschien.
- 2026-03-08 — 3 unabhängig erstellte Vergleichsgraphen für Ein-, Zwei- und Mehrbildbearbeitung erschienen, ohne das offizielle Paket zu verändern.
- 2026-03-09 — REDEdit-Bench wurde veröffentlicht.
- 2026-03-13 — Ein 8-Schritt-Beschleuniger 1.0-Lightning v1.1 wurde dem ComfyUI-Paket 1.1 hinzugefügt.
- 2026-03-17 — Das offizielle JSON wechselte seinen optionalen Beschleuniger von 1.0-Lightning 8steps v1.0 auf v1.1; dies war nicht das Basis-Release 1.1.
- 2026-03-24 — Code für das LoRA-Training wurde eingeführt.
- 2026-03-25 — Unterstützung für LoRA-Training über ModelScope wurde angekündigt.
- 2026-03-26 — Die offizielle Sammlung markierte LoRA Zoo als aktualisiert.
- 2026-04-03 — Unterstützung für Recaptioning mit mehreren Anbietern wurde in den kanonischen Code übernommen.
- 2026-04-10 — Eine Datei 1.1-Lightning 8-step v1.1 wurde hinzugefügt.
- 2026-04-14 — Eine Datei 1.1-Lightning 8-step v1.2 wurde hinzugefügt.

## So wird es verwendet {#how-to-use-this}

1. Wählen Sie einen unterstützten Weg: Laden Sie FireRedTeam/FireRed-Image-Edit-1.1 mit Diffusers oder starten Sie vom offiziellen ComfyUI-Paket 1.1.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1>
2. Für den Standard-ComfyUI-Graphen legen Sie den Transformer 1.1 in models/diffusion_models, qwen2.5vl-7b-bf16 in models/text_encoders und qwen_image_vae in models/vae ab und importieren danach das offizielle JSON.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
3. Legen Sie das Quellbild in den primären Loader, fügen Sie optional bis zu 2 Referenzen hinzu und benennen Sie im Prompt die gewünschte Änderung sowie die Bildnummern.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
4. Führen Sie zuerst ein unverändertes Standardprofil aus: 40 Schritte und CFG 4 ohne die Beschleunigungs-LoRA oder 8 Schritte und CFG 1 mit dem mitgelieferten Lightning-Pfad.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
5. Bei mehr als 3 Eingaben verwenden Sie den separaten Agent-Preprocessor und prüfen Sie seine Abhängigkeit von der Gemini-ROI-Verarbeitung, bevor Sie Bilder senden.
  — <https://github.com/FireRedTeam/FireRed-Image-Edit>

## Bewährte Verfahren {#best-practices}

- Fixieren Sie Workflow-JSON, Transformer und Lightning-LoRA gemeinsam: Der Graph vom 17. März verwendete absichtlich einen Transformer 1.1 mit dem Adapter 1.0-Lightning v1.1.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/179def9bfaad5170a00b7760d7d1526ca53de019>
- Behandeln Sie die spätere Datei 1.1-Lightning v1.2 nicht als dokumentierten Drop-in-Ersatz für den Graphen vom 17. März; testen Sie sie als eigenen versionierten Lauf.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/tree/main>
- Beginnen Sie mit dem mitgelieferten Sampler und den mitgelieferten Einstellungen statt den Graphen umzuverdrahten; die gespeicherten Profile sind 40 Schritte/CFG 4 oder 8 Schritte/CFG 1.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
- Übertragen Sie die Angabe des Projekts zu 30 GB und etwa 4,5 Sekunden für das optimierte Skript nicht in eine Kapazitäts- oder Geschwindigkeitsgarantie für ComfyUI.
  — <https://github.com/FireRedTeam/FireRed-Image-Edit>
- Bei Aufträgen mit mehr als 3 Bildern behandeln Sie das Agent-Preprocessing als Grenze zu einem externen Dienst: Die ROI-Erkennung nutzt weiterhin Gemini, auch wenn das Recaptioning einen anderen Anbieter verwendet.
  — <https://github.com/FireRedTeam/FireRed-Image-Edit>
- Behandeln Sie unabhängig zusammengestellte Vergleichsgraphen als benutzerdefinierte Workflows, bis Checkpoint, Einstellungen und Herkunft der Knoten geprüft sind.
  — <https://www.runninghub.ai/post/2030612111793065986>

## Hiermit ersetzt {#superseded-by-this}

- 2026-03-03 — Die Annahme, dass das Ereignis vom 2026-03-17 die Veröffentlichung von FireRed-Image-Edit-1.1 ist, ist veraltet; 1.1 wurde am 2026-03-03 angekündigt.
- 2026-03-08 — Die Annahme, dass der verlinkte Mehrbild-Vergleichsgraph das offizielle ComfyUI-Paket 1.1 von FireRedTeam ist, ist veraltet.
- 2026-04-14 — Die Bezeichnung FireRed-Image-Edit-1.1-Lightning-8steps-v1.1 als neuestes offizielles 1.1-Lightning-Artefakt ist veraltet.

## Weiterhin unbekannt {#still-unknown}

- Keine gelesene offizielle Quelle kündigt eine Basismodellversion nach 1.1 an; dies beweist jedoch nicht, dass keine nicht indizierte regionale Veröffentlichung existiert.
- Das offizielle Paket nennt keine explizite Mindestversion von ComfyUI, keine Matrix getesteter GPUs und keinen ComfyUI-spezifischen Leistungs-Benchmark.
- Der Workflow vom 17. März dokumentiert nicht die Kompatibilität seiner Paarung 1.0-Lightning v1.1 mit der späteren Datei 1.1-Lightning v1.2.
- GGUF-Gewichte sind veröffentlicht, aber das Standard-JSON wählt Safetensors aus und belegt keinen GGUF-Loader-Graphen.
- ControlNet- und OpenPose-Kompatibilität wurde durch keine primäre FireRed-Quelle bestätigt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://arxiv.org/abs/2602.13344 | FireRed-Image-Edit-1.0 Technical Report | 2026-09-06 |
| https://github.com/FireRedTeam/FireRed-Image-Edit | FireRedTeam/FireRed-Image-Edit README | 2026-09-06 |
| https://github.com/FireRedTeam/FireRed-Image-Edit/commits/main/ | Commits · FireRedTeam/FireRed-Image-Edit | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1 | FireRedTeam/FireRed-Image-Edit-1.1 | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commits/main | Commit-Verlauf · FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/179def9bfaad5170a00b7760d7d1526ca53de019 | Upload firered-image-edit-1.1.json · Commit 179def9 | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true | firered-image-edit-1.1.json | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/tree/main | FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI Dateibaum | 2026-09-06 |
| https://huggingface.co/collections/FireRedTeam/firered-image-edit | FireRed-Image-Edit · FireRedTeam Collection | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/02dd2dc5586fcf7a60451506e7dee8dd31021455 | Upload FireRed-Image-Edit-1.1-Lightning-8steps-v1.1 · Commit 02dd2dc | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/8625b60ec52d4fa0d128d8a6ebc8adba296f8592 | Upload FireRed-Image-Edit-1.1-Lightning-8steps-v1.2 · Commit 8625b60 | 2026-09-06 |
| https://www.runninghub.ai/post/2030611704802971649 | Xiaohongshu FireRed Image edit 1.1 Einzelbildbearbeitung vs. qwen | 2026-09-06 |
| https://www.runninghub.ai/post/2030612012606169089 | Xiaohongshu FireRed Image edit 1.1 Doppelbildbearbeitung vs. qwen | 2026-09-06 |
| https://www.runninghub.ai/post/2030612111793065986 | Xiaohongshu FireRed Image edit 1.1 Mehrbildbearbeitung vs. qwen | 2026-09-06 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:firered-image-edit`, Thread `comfyui-resources`, 1 datierter Eintrag 2026-03-17 → 2026-03-17.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Verwendung und bewährten Verfahren oben, einschließlich deren Grenzen.
- **Konfidenz:** mittel. Die datierten Einträge unter „Hiermit ersetzt“ sind maßgeblich dafür, was veraltet ist.
