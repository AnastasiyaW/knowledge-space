---
title: "InternVL"
category: projects
tags: [internvl, internvl-model-releases, project]
aliases: ["InternVL", "InternVL 3.5"]
level: 3
source_sha256: c55b2648454f66ea8b76ef412c2b2322d36f4952143f156edd5b20ebe18577e4
translation: machine
translated_at: '2026-10-24'
---
# InternVL {#internvl}

**Entwicklungslinie:** `project:internvl` · Thread `internvl-model-releases`  
**Ereignisse:** 2 datiert, 2024-12-11 → 2025-08-27 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

InternVL ist eine Familie von Vision-Language-Modellen mit offenen Gewichten für Teams, die Bilder, Dokumente, mehrere Bilder, Videos und GUI-Zustände in einem selbst gehosteten Workflow analysieren müssen.

- Fragebeantwortung zu Bildern, Dokumenten, Diagrammen und OCR
- Konversation über mehrere Bilder und Videos
- Visual Grounding, mehrsprachige Vision-Language-Aufgaben sowie GUI- und Embodied-Aufgaben in 3.5

Die aktuelle 3.5-Linie umfasst Modelle von 1,1 Mrd. bis 240,7 Mrd. Parameter insgesamt. Der offizielle Leitfaden ordnet Modelle bis 30B einer A100 zu, 38B zwei A100 und 241B acht A100. Für neue lokale Installationen sollte man einen vollständigen Checkpoint ohne Suffix der 3.5-Linie wählen; Flash ist dann sinnvoll, wenn die Kosten der visuellen Token der Engpass sind.

## Entwicklungslinie {#development-line}

- **2024-12-11 — InternVL2.5-78B-Modell und Collection veröffentlicht.** Am 2024-12-11 veröffentlichte das Projekt InternVL2.5-78B mit einer Modell-Collection, einem Repository, einer Projektseite und einer Demo. Die verlinkten Quellen belegen keine Benchmark-Ergebnisse oder Funktionsdetails.
- **2025-08-27 — InternVL3.5-Paper und Modell-Collection veröffentlicht.** Am 2025-08-27 veröffentlichte das Projekt das InternVL3.5-Paper, die offizielle Collection, ein Repository und den Chat. Die verlinkten Quellen belegen weder die detaillierten Aussagen des Papers noch die unterstützten Varianten oder Hinweise zum Deployment.

## Was sich geändert hat {#what-changed}

Am 2024-12-05 (erfasst am 2024-12-11) wurde InternVL2.5 zu einer Familie von 1B bis 78B. Die grundlegende Architektur blieb gegenüber dem Vorgänger erhalten, Training, Test-Time-Scaling und Datenqualität wurden jedoch überarbeitet. Der 78B-Checkpoint kombinierte einen 6B-Vision-Encoder mit Qwen2.5-72B.

Am 2025-08-26 (erfasst am 2025-08-27) ersetzte InternVL3.5 diese Kernlinie durch Checkpoints von 1B bis 241B, und zwar sowohl im projekteigenen als auch im Standardformat von Hugging Face. Eingeführt wurden CascadeRL, der Visual Resolution Router, eine entkoppelte Vision-Language-Bereitstellung, Sprachbackbones auf Basis von Qwen3 bzw. GPT-OSS sowie GUI- und Embodied-Fähigkeiten.

Am 2025-08-30 veröffentlichte das Projekt den Code und die Daten des CascadeRL-Trainings für seine GPT-OSS-20B-A4B-Variante. Nach dem 2025-08-27 wurde ein offizieller InternVL3.5-Flash-Checkpoint verfügbar. Seine Model Card beschreibt ViCO in Kombination mit einem visuellen Resolution-Routing, das die visuellen Token um 50 % reduziert; die geprüften Quellen belegen jedoch nicht das genaue Datum der ersten Veröffentlichung.

## So wird es verwendet {#how-to-use-this}

Am 2024-12-11 sollte man bei der Auswahl eines InternVL2.5-Release die offizielle Modellseite und Collection von InternVL2.5-78B prüfen. Ab dem 2025-08-27 sollte man vor der Wahl einer neueren InternVL-Linie das verlinkte InternVL3.5-Paper und die offizielle Collection durchsehen, statt davon auszugehen, dass die frühere Linie weiterhin der Standard ist.

1. Für normale Inferenz einen vollständigen InternVL3.5-Checkpoint ohne Suffix wählen; wenn es auf die Kosten der visuellen Token ankommt, die Flash-Variante nehmen.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Flash>
2. Das Format bewusst wählen: Der projekteigene Checkpoint wird über AutoModel mit Remote Code geladen, das HF-Format folgt den üblichen Transformers-Konventionen. transformers >=4.52.1 installieren; die 20B-A4B-Variante benötigt >=4.55.0.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
3. Für Bild-Chat die mitgelieferte dynamische Kachelung mit 448px anwenden, die Kacheln in bf16 umwandeln und den Prompt mit einem `<image>`-Platzhalter über model.chat senden.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
4. Für Video eine begrenzte Anzahl an Frames samplen, jedem Frame `FrameN: <image>` voranstellen und die passende num_patches_list an den Chat-Aufruf übergeben.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
5. Für einen Dienst über LMDeploy oder vLLM mit einem OpenAI-kompatiblen Endpunkt bereitstellen; für die GPT-OSS-20B-A4B-Variante vLLM verwenden.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>

## Best Practices {#best-practices}

- Für den Betrieb den Checkpoint ohne Suffix bevorzugen: Er ist die Version, die die vollständige Pipeline durchlaufen hat, anders als die Checkpoints der Stufen Pretrained, Instruct und MPO.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Flash>
- Die Modellgröße anhand der dokumentierten GPU-Vorgaben planen, bevor heruntergeladen wird: bis 30B eine A100, 38B zwei und 241B acht.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
- Die dokumentierte Mindestversion von Transformers verwenden; die Mindestabhängigkeit aus der 2.5-Zeit reicht für 3.5 nicht aus.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
- Für den Thinking-Modus do_sample=true und temperature=0.6 setzen; das Projekt empfiehlt dies, um Wiederholungen zu begrenzen.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>
- Bei Prompts mit mehreren Bildern das Kontextfenster vergrößern und die Bilder im Prompt nummerieren, damit das Modell sie unterscheiden kann.
  — <https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct>

## Abgelöst durch {#superseded-by-this}

- 2024-12-05 / 2024-12-11: InternVL2.5 ist nicht mehr der Standard für ein neues InternVL-Kernsystem-Deployment; einen vollständigen InternVL3.5-Checkpoint ohne Suffix verwenden, es sei denn, Abwärtskompatibilität ist die entscheidende Randbedingung.
- Die Anforderung transformers>=4.37.2 aus InternVL2.5 ist für InternVL3.5 veraltet: transformers>=4.52.1 verwenden, bzw. >=4.55.0 für 20B-A4B.
- 2025-08-26: Die Aussage in der 3.5-Model-Card, dass Flash noch bevorstehe, ist veraltet; ein offizieller InternVL3_5-8B-Flash-Checkpoint ist inzwischen verfügbar.

## Weiterhin unbekannt {#still-unknown}

- Das genaue erste Veröffentlichungsdatum von InternVL3.5-Flash wurde nicht ermittelt; die aktuelle Verfügbarkeit ist bestätigt, ein Aktualisierungsdatum der Modellseite muss jedoch nicht dem Starttermin entsprechen.
- Die angegebenen Verbesserungen beim logischen Schließen und die Reduktion der Token sind vom Projekt berichtete Benchmark-Ergebnisse, keine unabhängige Bewertung für einen bestimmten Workload.
- Das öffentliche Chat-Frontend war erreichbar, lieferte dem Abrufwerkzeug jedoch keine prüfbare Antwort, sodass das Verhalten der gehosteten Live-Demo nicht verifiziert wurde.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/OpenGVLab/InternVL | OpenGVLab/InternVL | 2026-09-04 |
| https://internvl.github.io/blog/2024-12-05-InternVL-2.5/ | InternVL2.5 | 2026-09-04 |
| https://huggingface.co/OpenGVLab/InternVL2_5-78B | OpenGVLab/InternVL2_5-78B | 2026-09-04 |
| https://internvl.github.io/blog/2025-08-26-InternVL-3.5/ | InternVL3.5 | 2026-09-04 |
| https://huggingface.co/papers/2508.18265 | InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency | 2026-09-04 |
| https://huggingface.co/collections/OpenGVLab/internvl35-68ac87bd52ebe953485927fb | InternVL3.5 — OpenGVLab Collection | 2026-09-04 |
| https://huggingface.co/OpenGVLab/InternVL3_5-8B-Instruct | OpenGVLab/InternVL3_5-8B-Instruct | 2026-09-04 |
| https://huggingface.co/OpenGVLab/InternVL3_5-8B-Flash | OpenGVLab/InternVL3_5-8B-Flash | 2026-09-04 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:internvl`, Thread `internvl-model-releases`, 2 datierte Ereignisse 2024-12-11 → 2025-08-27.
- **Praktischer Hinweis:** Am 2024-12-11 sollten Praktiker die offizielle Modellseite und Collection von InternVL2.5-78B prüfen, wenn sie eine InternVL2.5-Version auswählen. Ab dem 2025-08-27 sollten sie das verlinkte InternVL3.5-Paper und die offizielle Collection durchsehen, bevor sie eine neuere InternVL-Linie wählen, statt davon auszugehen, dass die frühere Modelllinie weiterhin der passende Standard ist.
- **Konfidenz:** hoch. Die datierten Ablöse-Hinweise oben sind maßgeblich dafür, was veraltet ist.
