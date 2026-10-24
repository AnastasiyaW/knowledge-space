---
title: "AuraFlow"
category: projects
date: 2024-08-15
tags: [auraflow, auraflow-model-releases, auraflow_release, project]
aliases: ["AuraFlow"]
level: 3
source_sha256: 6718fd27805d917914803d8496c28ed4ef426d2ce88b5be844d6a070dcd46640
translation: machine
translated_at: '2026-10-24'
---
# AuraFlow {#auraflow}

**Entwicklungslinie:** `project:auraflow` · Thread `auraflow-model-releases`  
**Letztes Ereignis:** 2024-08-15 · 3 datierte Einträge seit 2024-07-12 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Ein Flow-basiertes Text-zu-Bild-Modell für lokale Diffusers- und ComfyUI-Setups oder gehostete fal-Inferenz.

- Erzeugt Bilder aus Text über AuraFlowPipeline.
- Stellt einen gehosteten `fal-ai/aura-flow`-Endpunkt bereit.
- v0.3 unterstützt variable Seitenverhältnisse bis zu 1536 Pixel pro Dimension.

## Entwicklungslinie {#development-line}

- **2024-07-12 — Die ersten öffentlichen Projektreferenzen zu AuraFlow wurden erfasst.** V0.1 erschien als vollständig offenes Flow-basiertes Text-zu-Bild-Modell; fal dokumentierte native Unterstützung für Diffusers und ComfyUI sowie eine 6.8B-Architektur.
- **2024-07-29 — AuraFlow v0.2 wurde als neue Modellversion erfasst.** V0.2 wurde als Nachfolger von v0.1 dokumentiert, der mit mehr Rechenleistung trainiert wurde. Die offizielle Collection führt das Modell-Update auf 2024-07-27; möglicherweise wird damit zwischen Veröffentlichung des Modells und Ankündigung unterschieden.
- **2024-08-15 — AuraFlow v0.3 wurde als nachfolgende Modellversion erfasst.** V0.3 brachte mehr Rechenleistung, Feinabstimmung auf ästhetischen Daten und Seitenverhältnis-Unterstützung bis zu 1536 Pixel pro Dimension.

## Was sich geändert hat {#what-changed}

AuraFlow — Entwicklungslinie:

- 2024-07-12: v0.1 erschien als vollständig offenes Flow-basiertes Text-zu-Bild-Modell; fal dokumentierte native Unterstützung für Diffusers und ComfyUI sowie eine 6.8B-Architektur.
- 2024-07-29: v0.2 wurde als Nachfolger von v0.1 dokumentiert, der mit mehr Rechenleistung trainiert wurde. Die offizielle Collection führt das Modell-Update auf 2024-07-27; möglicherweise wird damit zwischen Veröffentlichung des Modells und Ankündigung unterschieden.
- 2024-08-15: v0.3 brachte mehr Rechenleistung, Feinabstimmung auf ästhetischen Daten und Seitenverhältnis-Unterstützung bis zu 1536 Pixel pro Dimension.
- Heute gefunden: fals offizielle Collection listet nur das unversionierte Modell, v0.2 und v0.3; der aktive fal-Endpunkt identifiziert AuraFlow als v0.3 und kennzeichnet es weiterhin als Beta.

## Anwendung {#how-to-use-this}

Stand 2024-08-15: Behandle AuraFlow als versionierte Modelllinie. Wähle für jeden Workflow die benötigte offizielle Referenz (AuraFlow, AuraFlow-v0.2 oder AuraFlow-v0.3) aus, statt anzunehmen, dass Releases austauschbar sind.

1. Fixiere `fal/AuraFlow-v0.3` für einen neuen lokalen Build; es ist der dokumentierte aktuelle Checkpoint in der offiziellen Collection.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
2. Installiere aktuelle `diffusers`, `transformers` und `accelerate` und lade anschließend `AuraFlowPipeline.from_pretrained("fal/AuraFlow-v0.3", torch_dtype=torch.float16, variant="fp16").to("cuda")`.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
3. Generiere mit expliziten Dimensionen, 50 Inferenzschritten, CFG 3.5 und einem festen Generator-Seed; speichere das resultierende Bild.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
4. Für gehostete Inferenz installiere `@fal-ai/client`, setze `FAL_KEY` in der Server-Umgebung, rufe `fal.subscribe("fal-ai/aura-flow", { input: { prompt } })` auf und speichere die zurückgegebene Request-ID.
  — <https://fal.ai/models/fal-ai/aura-flow/api>

## Best Practices {#best-practices}

- Setze Steps und CFG explizit. Starte mit dem v0.3-Rezept von 50 Steps und CFG 3.5, statt dich auf einen Bibliotheks-Default zu verlassen.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
- Wenn der lokale VRAM begrenzt ist, nutze die dokumentierte 8-Bit-Quantisierung und das ausbalancierte Device Mapping und vergleiche die Ausgaben, bevor du den Pfad mit niedrigerer Präzision übernimmst.
  — <https://huggingface.co/docs/diffusers/api/pipelines/aura_flow>
- Halte `FAL_KEY` serverseitig; nutze Queue-Status und Webhooks, statt bei langsamen Anfragen zu blockieren, und speichere den zurückgegebenen Seed und den erweiterten Prompt zur Reproduzierbarkeit.
  — <https://fal.ai/models/fal-ai/aura-flow/api>
- Importiere den veröffentlichten v0.3-ComfyUI-Workflow nicht unverändert: Er nennt derzeit `aura_flow_0.2.safetensors`; ersetze den Checkpoint bewusst und validiere eine Testgenerierung.
  — <https://huggingface.co/fal/AuraFlow-v0.3/blob/main/comfy_workflow.json>
- Für SimpleTuner-Feinabstimmung behandle den AuraFlow-spezifischen Lycoris-LoKr-Weg als Ausgangspunkt und nicht als beiläufiges Full-Rank-Tuning; die Anleitung setzt für vollständiges Tuning erheblichen VRAM bzw. DeepSpeed voraus und startet die Validierung bei 1024², 30–50 Steps und CFG 3.5–4.0.
  — <https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/AURAFLOW.md>

## Hierdurch ersetzt {#superseded-by-this}

- 2024-07-29: AuraFlow v0.2 ersetzt für die offizielle Hauptlinie den v0.1-Checkpoint, da er mit mehr Rechenleistung trainiert wurde; v0.1 nur für die Reproduktion von Altbeständen beibehalten.
- 2024-08-15: AuraFlow v0.3 ersetzt v0.2 als dokumentierten Ausgangs-Checkpoint und ergänzt ästhetische Feinabstimmung sowie variable Seitenverhältnisse bis zu 1536 Pixel pro Dimension.
- Aktuell: Das unversionierte `fal/AuraFlow` sowie Ladebeispiele für v0.2 gelten für neue Builds als veraltet; verwende stattdessen `fal/AuraFlow-v0.3`. Dies ist eine Nutzungsempfehlung, keine formelle Abkündigung.

## Noch unbekannt {#still-unknown}

- fals Collection listet drei v0.x-Checkpoints, doch dieses Fehlen beweist nicht, dass kein unveröffentlichter oder anders benannter Nachfolger existiert.
- Die öffentlichen Modell- und API-Seiten bezeichnen v0.3 weiterhin als Beta; es wurde weder eine aktuelle Matrix unterstützter GPUs noch ein eigener v0.3-Lauf gefunden, daher werden VRAM und Latenz nicht verallgemeinert.
- Die aktuelle Diffusers-Referenz ist intern widersprüchlich: Ihre Aufrufsignatur zeigt CFG 3.5, die Parameterbeschreibung nennt 5.0. Setze CFG explizit gemäß dem v0.3-Card-/API-Rezept.
- Die veröffentlichte `comfy_workflow.json` des v0.3-Repositorys nennt einen v0.2-Checkpoint; sie ist daher ohne lokalen Austausch und Testlauf nicht als v0.3-Workflow verifiziert.
- Der chinesischsprachige Strang fand eine SimpleTuner-Übersetzung und einen community-erstellten ComfyUI-Workflow, aber keine unabhängige, versionsfixierte Messung zu v0.3; dies ändert das dokumentierte Ausgangsrezept nicht.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://blog.fal.ai/auraflow/ | Introducing AuraFlow v0.1, an Open Exploration of Large Rectified Flow Models | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow | fal/AuraFlow · Hugging Face | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow-v0.2 | fal/AuraFlow-v0.2 · Hugging Face | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow-v0.3 | fal/AuraFlow-v0.3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/collections/fal/auraflow | AuraFlow — a fal Collection | 2026-09-04 |
| https://fal.ai/models/fal-ai/aura-flow/api | AuraFlow Text to Image API Docs | fal | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/aura_flow | AuraFlow — Hugging Face Diffusers | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow-v0.3/blob/main/comfy_workflow.json | comfy_workflow.json · fal/AuraFlow-v0.3 | 2026-09-04 |
| https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/AURAFLOW.md | Auraflow Quickstart — SimpleTuner | 2026-09-04 |
| https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/AURAFLOW.zh.md | Auraflow Quickstart, Simplified Chinese — SimpleTuner | 2026-09-04 |
| https://comfyui.nomadoor.net/zh/basic-workflows/auraflow/ | AuraFlow | Comfy with ComfyUI, Simplified Chinese | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:auraflow`, Thread `auraflow-model-releases`, 3 datierte Ereignisse 2024-07-12 → 2024-08-15.
- **Praktischer Hinweis:** Stand 2024-08-15 sollten Praktiker AuraFlow als versionierte Modelllinie behandeln und für ihren Workflow die benötigte offizielle Referenz (AuraFlow, AuraFlow-v0.2 oder AuraFlow-v0.3) auswählen, statt anzunehmen, dass Releases austauschbar sind.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
