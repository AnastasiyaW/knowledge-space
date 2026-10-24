---
title: "Realism_Engine_Ideogram_4 — Ideogram-LoRA"
category: projects
date: 2026-06-11
tags: [ideogram-lora, project, realism-engine-ideogram-4]
aliases: ["Realism_Engine_Ideogram_4"]
level: 2
source_sha256: f3947eb20d075f351d0ce57ac77d32e7a13927f47267f960c59db44286ce8802
translation: machine
translated_at: '2026-10-24'
---
# Realism_Engine_Ideogram_4 — Ideogram-LoRA {#realism_engine_ideogram_4-ideogram-lora}

**Entwicklungslinie:** `project:realism-engine-ideogram-4` · Thread `ideogram-lora`  
**Letztes Ereignis:** 2026-06-11 · 1 datiertes Ereignis seit 2026-06-11 · **Recherchiert:** 2026-09-07 · Konfidenz: mittel

## Was es ist {#what-it-is}

Realism_Engine_Ideogram_4 ist eine vom Nutzer gehostete Sammlung von LoRA-Gewichtsdateien und ComfyUI-Workflow-JSONs für die lokale Inferenz mit Ideogram 4.

- enthält safetensors-Dateien für V1, beta, V2, V3, V4 und V5;
- sein V2-Workflow wendet das V2-Gewicht über reine Model-LoRA-Loader auf die Ideogram-4-Zweige an.

Einschränkung: Das Repository umfasst 21,5 GB, hat eine leere README, eine unbekannte Adapter-Lizenz und keinen gehosteten Inferenzanbieter. Es ist als lokal getestetes Community-Asset zu behandeln, nicht als dokumentierte oder kommerziell freigegebene Ideogram-4-Veröffentlichung.

## Entwicklungslinie {#development-line}

- **2026-06-11 — Hugging-Face-Projektressource für Realism_Engine_Ideogram_4 erfasst.** Am 2026-06-11 enthielt diese Entwicklungslinie einen Link auf eine Hugging-Face-Ressource für Realism_Engine_Ideogram_4. Der datierte Link belegt, dass zu diesem Zeitpunkt eine identifizierbare, mit der Linie verbundene Projektressource existierte. Die verfügbaren Belege klären weder deren Veröffentlichungsstatus, Inhalte, Trainingsmethode noch Kompatibilität.

## Was sich geändert hat {#what-changed}

- 2026-06-09 — Das Repository wurde angelegt, frühe Assets und Workflows wurden hochgeladen.
- 2026-06-11 — Realism_Engine_Ideogram_V2.safetensors und rei4_v2_workflow.json wurden hinzugefügt.
- 2026-06-12 — Realism_Engine_Ideogram_V3.safetensors wurde hinzugefügt.
- 2026-06-14 — Realism_Engine_Ideogram_V4.safetensors wurde hinzugefügt.
- 2026-06-19 — Realism_Engine_Ideogram_V5.safetensors wurde hinzugefügt; es ist das neueste benannte Gewicht in der sichtbaren Historie.

## Anwendung {#how-to-use-this}

1. Vor dem Download die Adapter-Seite prüfen: Die README ist leer und die Lizenz unbekannt, daher ist die kommerzielle Nutzung durch die eigene Dokumentation nicht freigegeben.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4>
2. Die ComfyUI-Komponenten für Ideogram 4 in den dokumentierten Ordnern diffusion_models, text_encoders und vae installieren.
  — <https://huggingface.co/Comfy-Org/Ideogram-4>
3. Für den dokumentierten V2-Pfad Realism_Engine_Ideogram_V2.safetensors herunterladen, rei4_v2_workflow.json importieren und seine beiden ModelOnly-LoRA-Loader auf genau dieses Gewicht zeigen lassen.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/blob/main/rei4_v2_workflow.json>
4. Getestetes Gewicht und Workflow gemeinsam fixieren: V3–V5 sind spätere Uploads, aber das Repository dokumentiert weder ihre Änderungen noch die Workflow-Kompatibilität.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/commits/main>

## Bewährte Praktiken {#best-practices}

- Die V2-Feinabstimmung auf V2 beschränken: Der mitgelieferte Workflow nennt 0,50–0,90 als Optimalbereich und warnt davor, über 0,90 zu gehen.
  — <https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/blob/main/rei4_v2_workflow.json>
- Für den vorgesehenen Qualitätspfad sowohl die konditionalen als auch die unkonditionalen Ideogram-Gewichte verwenden: Der Maintainer von Comfy-Org erklärt, dass das Weglassen des unkonditionalen Zweigs meist Qualität kostet, während ein Unkonditional-Modell mit niedrigerer Präzision den Speicherbedarf senken kann.
  — <https://huggingface.co/Comfy-Org/Ideogram-4/discussions/1>
- Für kontrollierte Tests die strukturierten JSON-Captions von Ideogram 4 verwenden und den Seed für Reproduzierbarkeit beibehalten.
  — <https://huggingface.co/docs/diffusers/main/api/pipelines/ideogram4>
- Kommerzielle Nutzung zurückstellen, bis die Rechte geklärt sind: Das ComfyUI-Basispaket steht unter der Ideogram-Vereinbarung für nicht-kommerzielle Modelle.
  — <https://huggingface.co/Comfy-Org/Ideogram-4>

## Hierdurch ersetzt {#superseded-by-this}

- Bis 2026-09-07 ist keine Ablösung dokumentiert: Der V5-Upload vom 2026-06-19 erklärt nicht, dass er V1, beta, V2, V3 oder V4 ersetzt; diese bleiben verfügbar.

## Weiterhin unbekannt {#still-unknown}

- Trainingsdaten, Trainingsmethode, vorgesehene Verwendung und Lizenz des Adapters sind nicht dokumentiert.
- Es gibt keine Release Notes, Benchmarks oder Workflow-Zuordnungen, die belegen, welches von V3–V5 V2 ersetzen sollte.
- Es wurde keine chinesischsprachige Dokumentation vom Anbieter und keine verwertbaren unabhängigen Betriebsnachweise auf Chinesisch gefunden.
- Es wurde kein unabhängiger lokaler Lauf durchgeführt; die V2-Einstellungen sind Hinweise des Workflow-Autors und kein verifiziertes Rezept für spätere Gewichte.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4 | RazzzHF/Realism_Engine_Ideogram_4 — Modellseite | 2026-09-07 |
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/tree/main | RazzzHF/Realism_Engine_Ideogram_4 — aktuelle Dateistruktur | 2026-09-07 |
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/commits/main | RazzzHF/Realism_Engine_Ideogram_4 — Commit-Historie, Einträge vom 2026-06-09 bis 2026-06-19 | 2026-09-07 |
| https://huggingface.co/RazzzHF/Realism_Engine_Ideogram_4/blob/main/rei4_v2_workflow.json | rei4_v2_workflow.json — V2-Workflow, hochgeladen am 2026-06-11 | 2026-09-07 |
| https://huggingface.co/Comfy-Org/Ideogram-4 | Comfy-Org/Ideogram-4 — ComfyUI-Paket und Lizenz | 2026-09-07 |
| https://huggingface.co/Comfy-Org/Ideogram-4/discussions/1 | Comfy-Org Ideogram-4 Diskussion — Hinweise zu gepaarten Modellen und Sampler | 2026-09-07 |
| https://huggingface.co/docs/diffusers/main/api/pipelines/ideogram4 | Hugging Face Diffusers — Dokumentation der Ideogram-4-Pipeline | 2026-09-07 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:realism-engine-ideogram-4`, Thread `ideogram-lora`, 1 datiertes Ereignis 2026-06-11 → 2026-06-11.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Anwendung und Praktiken oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
