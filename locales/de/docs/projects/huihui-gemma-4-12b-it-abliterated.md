---
title: "Huihui-gemma-4-12B-it-abliterated — Modellveröffentlichung"
category: projects
date: 2026-06-07
tags: [gemma, huihui-gemma-4-12b-it-abliterated, model-release, project]
aliases: ["Huihui-gemma-4-12B-it-abliterated"]
level: 2
source_sha256: 3703837ba61a043893ef50c980946abde70c07b9ef76ffe8d1d4e71cecf05b2b
translation: machine
translated_at: '2026-10-24'
---
# Huihui-gemma-4-12B-it-abliterated — Modellveröffentlichung {#huihui-gemma-4-12b-it-abliterated-model-release}

**Entwicklungslinie:** `project:huihui-gemma-4-12b-it-abliterated` · Thread `model-release`  
**Letztes Ereignis:** 2026-06-07 · 1 datiertes seit 2026-06-07 · **Recherchiert:** 2026-09-05 · Vertrauensgrad: hoch

## Was es ist {#what-it-is}

Huihui-gemma-4-12B-it-abliterated ist eine abliterierte Ableitung des Instruction-Modells Gemma 4 12B von Google für lokale Nutzer, die Text-, Bild- und Audioeingaben benötigen, ohne das übliche Ablehnungsverhalten des Basismodells. Es behält die einheitliche multimodale Architektur bei; das 24 GB große BF16-Repository und die reduzierte Sicherheitsfilterung machen es für unbeaufsichtigte öffentliche Nutzung ungeeignet. Fazit: Nur hinter anwendungsseitigen Richtlinienprüfungen und mit Ausgabeprüfung einsetzen.

## Entwicklungslinie {#development-line}

- **2026-06-07 — Verweis auf das Repository Huihui-gemma-4-12B-it-abliterated.** Am 2026-06-07 hat der Datensatz einen Link auf das Repository Huihui-gemma-4-12B-it-abliterated auf Hugging Face erfasst. Allein auf Grundlage der verfügbaren Belege lässt sich dies als wesentliches öffentliches Historienereignis behandeln, ohne dass Details zur Veröffentlichung oder zu den Fähigkeiten des Modells belegt wären.

## Was sich geändert hat {#what-changed}

2026-06-07 — Huihui AI hat Huihui-gemma-4-12B-it-abliterated veröffentlicht. Die Modellkarte beschreibt es als abliterierte Version von google/gemma-4-12B-it, wobei Denk- und Nicht-Denk-Modi behandelt und die Schichten 23–28 verändert wurden; die Commit-Historie des Repositorys vom selben Tag dokumentiert die Veröffentlichung. Befund zum Ereignis: Der Herausgeber hat später gewarnt, dass die frühesten Upstream-Gewichte von Gemma 4 12B-it fehlerhaft waren, das Modell erneut abliteriert und bestehende Downloader angewiesen, es erneut herunterzuladen. Neuer Kontext: Google hat das Upstream-Modell Gemma 4 12B am 2026-06-03 als einheitliches, encoderfreies multimodales 12B-Modell vorgestellt, das für den lokalen Betrieb mit 16 GB VRAM oder Unified Memory gedacht ist; diese Upstream-Veröffentlichung liegt vor dieser Ableitung und ersetzt sie nicht.

## So nutzt du es {#how-to-use-this}

Stand 2026-06-07 sollten Anwender das verlinkte Hugging-Face-Repository als Ausgangspunkt für die Bewertung dieses Modells betrachten und Modellkarte, Lizenz, Herkunft und vorgesehene Verwendung vor dem Einsatz unabhängig prüfen.

1. Eine aktuelle Ollama-Version installieren und anschließend `ollama run huihui_ai/gemma-4-abliterated:12b` ausführen.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>
2. Für Transformers das Modell mit `AutoProcessor` und `AutoModelForMultimodalLM` laden, mit `device_map="auto"`; Text-, Bild- und Audiopfade vor dem Deployment getrennt testen.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>
3. Wird ein kleineres lokales Artefakt benötigt, das spätere QAT-Q4_0-GGUF-Derivat mit llama.cpp oder Ollama verwenden, statt das 24 GB große BF16-Repository als leichten Download zu behandeln.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-qat-q4_0-unquantized-abliterated-GGUF>

## Bewährte Praktiken {#best-practices}

- Das Modell erneut herunterladen, statt eine frühe lokale Kopie zu behalten: Der Herausgeber gibt an, dass die frühesten Upstream-Gewichte Probleme hatten und die Ableitung erneut abliteriert wurde.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>
- Menschliche Prüfung und anwendungsseitige Schutzmaßnahmen für sensible, öffentliche, minderjährige oder hochsicherheitsrelevante Einsatzbereiche beibehalten; die reduzierte Filterung ist eine ausdrücklich genannte Einschränkung des Modells.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>
- Für den bereitgestellten Ollama-Modellnamen die neueste Ollama-Version verwenden.
  — <https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated>

## Dadurch ersetzt {#superseded-by-this}

- 2026-06-07 — jede lokal zwischengespeicherte Kopie, die aus den frühesten Upstream-Gewichten von Gemma 4 12B-it erstellt wurde, ist für diese Ableitung veraltet; durch den erneut abliterierten Upload ersetzen.

## Noch unbekannt {#still-unknown}

- Die Modellkarte liefert keine reproduzierbaren Vorher-/Nachher-Ergebnisse zu Ablehnungsverhalten, Fähigkeiten oder Sicherheit, daher sind die praktischen Qualitätseinbußen durch Abliteration nicht verifiziert.
- Der genaue Zeitstempel des erneut abliterierten Gewichtsuploads ist im zugänglichen Repository-Verlauf nicht ersichtlich; er wird deshalb dem Veröffentlichungsschritt vom 2026-06-07 zugeordnet und nicht als eigenes datiertes Ereignis behandelt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated | huihui-ai/Huihui-gemma-4-12B-it-abliterated | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-abliterated/commits/main | Commits · huihui-ai/Huihui-gemma-4-12B-it-abliterated | 2026-09-05 |
| https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/ | Introducing Gemma 4 12B | 2026-09-05 |
| https://huggingface.co/huihui-ai/Huihui-gemma-4-12B-it-qat-q4_0-unquantized-abliterated-GGUF | huihui-ai/Huihui-gemma-4-12B-it-qat-q4_0-unquantized-abliterated-GGUF | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:huihui-gemma-4-12b-it-abliterated`, Thread `model-release`, 1 datiertes Ereignis 2026-06-07 → 2026-06-07.
- **Praktischer Hinweis:** Stand 2026-06-07 sollten Anwender das verlinkte Hugging-Face-Repository als Ausgangspunkt für die Bewertung dieses Modells betrachten und Modellkarte, Lizenz, Herkunft und vorgesehene Verwendung vor dem Einsatz unabhängig prüfen.
- **Vertrauensgrad:** hoch. Datierte Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
