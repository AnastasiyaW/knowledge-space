---
title: "Krea2 TextFusion Refusal-Reduction LoRA"
category: projects
date: 2026-07-15
tags: [krea2-textfusion-refusal-reduction-lora, krea2_textfusion_refusal_reduction_lora, project]
aliases: ["Krea2 TextFusion Refusal-Reduction LoRA"]
level: 2
source_sha256: 55eb35f5579b272b07abbabde6fd01e5d42d12c808974d03255c0fa47b31e538
translation: machine
translated_at: '2026-10-24'
---
# Krea2 TextFusion Refusal-Reduction LoRA {#krea2-textfusion-refusal-reduction-lora}

**Entwicklungslinie:** `project:krea2-textfusion-refusal-reduction-lora` · Thread `krea2-textfusion-refusal-reduction-lora`  
**Letztes Ereignis:** 2026-07-15 · 1 datiert seit 2026-07-15 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Krea2 TextFusion Refusal-Reduction LoRA – ein Rank-64-LoRA für Krea 2, das die Unterdrückung von Konzepten, die dem Basismodell bereits bekannt sind, verringern soll. – verändert Attention und MLP in vier TextFusion-Blöcken; – fügt keine Stile, Figuren oder neuen visuellen Konzepte hinzu; – verändert weder den Image Transformer, txtmlp noch den 1×12-Tap-Projector. Die aktuell verfügbare Version ist v2.0; die öffentlich angegebene empfohlene Stärke liegt bei 0.75–1.00.

## Entwicklungslinie {#development-line}

- **2026-07-15 — Civitai-Referenz für Krea2 TextFusion Refusal-Reduction LoRA erfasst.** Rank-64-LoRA nur für TextFusion für Krea 2; eine unabhängige Kopie der Beschreibung bestätigt die vier Zielblöcke und die Stärke 1.00, nennt aber kein eigenes Veröffentlichungsdatum, weshalb dies keine datierte Ergänzung zum Ereignis ist.

## Was sich geändert hat {#what-changed}

2026-07-15 – Version v1.0 veröffentlicht: Rank-64-LoRA nur für TextFusion für Krea 2; eine unabhängige Kopie der Beschreibung bestätigt die vier Zielblöcke und die Stärke 1.00, nennt aber kein eigenes Veröffentlichungsdatum, weshalb dies keine datierte Ergänzung zum Ereignis ist. 2026-08-29 – v2.0: angegeben werden besseres Befolgen des Prompts und weniger geglättete Texturen; empfohlen wird der Bereich 0.75–1.00, 1.50 wird als funktionsfähig, aber nicht empfohlen gekennzeichnet.

## So wird es verwendet {#how-to-use-this}

Ab 2026-07-15 sollten Anwender die verlinkte Civitai-Seite als Ausgangsreferenz für dieses LoRA nutzen und dort vor dem Einsatz die aktuelle Version, Lizenz und Nutzungsdetails prüfen; die gesicherten Belege stützen keine stärkere operative Empfehlung.

1. Richten Sie einen lokalen Krea-2-Turbo-Workflow in ComfyUI ein und installieren Sie die Basisgewichte, den Qwen3VL-Text-Encoder und das VAE gemäß dem offiziellen Schema.
  — <https://docs.comfy.org/tutorials/image/krea/krea-2>
2. Laden Sie die LoRA-Datei herunter, legen Sie sie in `ComfyUI/models/loras/` ab, wählen Sie diese Datei im LoRA-Knoten für Krea 2 aus und aktivieren Sie das LoRA.
  — <https://docs.comfy.org/tutorials/image/krea/krea-2>
3. Für v2.0 beginnen Sie mit der Stärke 0.75–1.00; vergleichen Sie das Ergebnis mit demselben Seed ohne LoRA, bevor Sie Sampler oder Prompt ändern.
  — <https://tungsten.run/model/GJjkvTwp3m>

## Best Practices {#best-practices}

- Verwenden Sie diesen Adapter nicht als Style- oder Concept-LoRA: Er ist für den TextFusion-Pfad ausgewiesen, nicht zum Hinzufügen gelernter visueller Begriffe.
  — <https://huggingface.co/Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora>
- Halten Sie den Basis-Workflow von Krea 2 reproduzierbar: Verwenden Sie die offizielle Vorlage und schalten Sie das LoRA über einen separaten Schalter zu, damit Sie seinen Beitrag prüfen können.
  — <https://docs.comfy.org/tutorials/image/krea/krea-2>
- Erhöhen Sie v2.0 nicht direkt auf 1.50: Die Startseite kennzeichnet diesen Wert als nicht empfohlen.
  — <https://tungsten.run/model/GJjkvTwp3m>

## Dadurch überholt {#superseded-by-this}

- 2026-08-29: Für v2.0 wurde die frühere Empfehlung von v1.0 „strength 1.00“ durch den aktuellen Startbereich 0.75–1.00 ersetzt; dies betrifft die Einstellung und belegt nicht die Einstellung der Verfügbarkeit von v1.0.

## Noch unbekannt {#still-unknown}

- Die primäre Civitai-Seite war bei der Prüfung nicht abrufbar; daher sind ihr ursprüngliches Veröffentlichungsdatum und die Autorenbeschreibung von v1.0 nicht direkt bestätigt.
- Es wurde kein unabhängiges, datiertes Changelog gefunden, das v2.0 mit derselben Veröffentlichung des Autors verknüpft; Name und Civitai-Modell-ID stimmen auf der Seite von v2.0 im Link überein.
- Das Antwortschema enthält keine eigenen Felder event_findings und new_events: Datierte Angaben sind in what_changed enthalten.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://civitai.com/models/2775340/krea2-textfusion-refusal-reduction-lora | Krea2 TextFusion Refusal-Reduction LoRA | Civitai | 2026-09-05 |
| https://huggingface.co/Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora | Quiho/Krea2_TextFusion_Refusal-Reduction_LoRA_v1.0_lora | 2026-09-05 |
| https://tungsten.run/model/GJjkvTwp3m | Krea2 TextFusion Refusal-Reduction v2.0 | 2026-09-05 |
| https://docs.comfy.org/tutorials/image/krea/krea-2 | Krea 2 | ComfyUI Documentation | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:krea2-textfusion-refusal-reduction-lora`, Thread `krea2-textfusion-refusal-reduction-lora`, 1 datiertes Ereignis 2026-07-15 → 2026-07-15.
- **Praktischer Hinweis:** Ab 2026-07-15 sollten Anwender die verlinkte Civitai-Seite als Ausgangsreferenz für dieses LoRA nutzen und dort vor dem Einsatz die aktuelle Version, Lizenz und Nutzungsdetails prüfen; die gesicherten Belege stützen keine stärkere operative Empfehlung.
- **Konfidenz:** mittel. Die datierten Überholungsangaben oben sind maßgeblich dafür, was veraltet ist.
