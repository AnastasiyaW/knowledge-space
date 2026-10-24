---
title: "Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF — GGUF-Verteilung"
category: projects
date: 2026-03-25
tags: [gguf-distribution, project, qwen3-5-40b-claude-4-6-opus-deckard-heretic-uncensored-thinking-gguf, qwen3_5_40b_claude_4_6_opus_deckard_heretic_uncensored_thinking_gguf]
aliases: ["Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF"]
level: 2
source_sha256: b571ae47d2533c74f3dfc4f434367508b1bd9957486ee309ee173d9ed16eb543
translation: machine
translated_at: '2026-10-24'
---
# Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF — GGUF-Verteilung {#qwen35-40b-claude-46-opus-deckard-heretic-uncensored-thinking-gguf-gguf-distribution}

**Entwicklungslinie:** `project:qwen3-5-40b-claude-4-6-opus-deckard-heretic-uncensored-thinking-gguf` · Thread `gguf-distribution`  
**Letztes Ereignis:** 2026-03-25 · 1 datiertes Ereignis seit 2026-03-25 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Worum es sich handelt {#what-it-is}

Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF ist eine Sammlung statischer GGUF-Quantisierungen eines multimodalen 39B-Modells mit Fine-Tuning für llama.cpp, Ollama und lokale OpenAI-kompatible Server.

- Text- und Bildverarbeitung in Kombination mit einer mmproj-Datei.
- Ausführung über die lokale CLI und einen lokalen Server.
- Auswahl der Quantisierung anhand des verfügbaren Speichers und der gewünschten Qualität.

Q4_K_M benötigt 24,0 GB, Q8_0 benötigt 41,6 GB, und eigenständige mmproj-Dateien benötigen 0,7–1,0 GB.

Wir erhalten eine praxistaugliche lokale Veröffentlichung, doch die Angaben zur Zensurfreiheit und die Qualität des Fine-Tunings müssen separat anhand Ihrer eigenen Aufgaben und Risiken getestet werden.

## Entwicklungslinie {#development-line}

- **2026-03-25 — Hugging-Face-Referenz für die GGUF-Modelllinie erfasst.** Die Dateien reichen von Q2_K (14,5 GB) bis Q8_0 (41,6 GB), dazu kommen zwei multimodale Projektor-Dateien. Die Modellkarte verlinkt direkt auf das vorgelagerte DavidAU-Repository und auf eine separate i1/imatrix-Variante.

## Was sich geändert hat {#what-changed}

2026-03-25 — Statische GGUF-Quantisierungen des 39B-Basismodells sind verfügbar: von Q2_K (14,5 GB) bis Q8_0 (41,6 GB), dazu zwei multimodale Projektor-Dateien. Die Karte verweist direkt auf das vorgelagerte DavidAU-Repository und auf eine separate i1/imatrix-Variante.

2026-03-25 — Der Quantisierungsindex führt außerdem eine separate i1-GGUF-Veröffentlichung von mradermacher auf. Dabei handelt es sich um einen parallelen, gewichteten imatrix-Build desselben Checkpoints und nicht um ein Update der statischen GGUF-Linie.

## So wird es verwendet {#how-to-use-this}

Stand 2026-03-25 können Praktiker die verlinkte Hugging-Face-Seite als Ausgangspunkt für diese GGUF-Modelllinie nutzen. Vor dem Einsatz sollten Dateien, Herkunft, Lizenz und Laufzeitkompatibilität jedoch unabhängig überprüft werden.

1. Wählen Sie eine Quantisierung anhand des verfügbaren Speichers; die Karte empfiehlt Q4_K_M für einen ersten lokalen Lauf und kennzeichnet Q4_K_S als schnelle empfohlene Option.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
2. Führen Sie das Modell über llama.cpp aus: `llama serve -hf mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF:Q4_K_M`. Der Server stellt einen lokalen, OpenAI-kompatiblen Endpunkt bereit.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
3. Für Ollama führen Sie `ollama run hf.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF:Q4_K_M` aus; für die Bildverarbeitung laden Sie eine passende mmproj-Datei aus dem statischen Repository herunter.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>

## Bewährte Vorgehensweisen {#best-practices}

- Wählen Sie eine Quantisierung nicht allein nach Dateigröße: Der Autor weist darauf hin, dass die Liste nach Größe sortiert ist und IQ-Quantisierungen häufig besser abschneiden als Nicht-IQ-Varianten ähnlicher Größe.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF>
- Beziehen Sie mmproj für Bildaufgaben aus dem statischen GGUF-Repository; das i1/imatrix-Repository vermerkt, dass seine mmproj-Datei dort liegt.
  — <https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF>
- Testen Sie das Modell vor dem Einsatz anhand Ihrer eigenen Aufgaben und Sicherheitsanforderungen: Die Karte beschreibt Herkunft und behauptete Eigenschaften, liefert jedoch weder unabhängige Benchmarks noch eine Garantie für das Verhalten.
  — <https://huggingface.co/DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking>

## Hiermit ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Die angeforderten Felder event_findings und new_events fehlen im Antwortschema; Fakten zum 2026-03-25 erscheinen unter what_changed.
- Das genaue Veröffentlichungsdatum des vorgelagerten DavidAU-Modells und unabhängige Qualitätsmetriken sind durch die angegebenen Quellen nicht bestätigt.
- Die Modellkarte bezeichnet das Modell als Vision-Modell und stellt eine mmproj-Datei bereit. Ob die Laufzeitumgebung Bilder verarbeiten kann, hängt jedoch von Version und Konfiguration ab.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF | mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-GGUF | 2026-09-05 |
| https://huggingface.co/DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking | DavidAU/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking | 2026-09-05 |
| https://huggingface.co/mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF | mradermacher/Qwen3.5-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking-i1-GGUF | 2026-09-05 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:qwen3-5-40b-claude-4-6-opus-deckard-heretic-uncensored-thinking-gguf`, Thread `gguf-distribution`, 1 datiertes Ereignis, 2026-03-25 → 2026-03-25.
- **Praktischer Hinweis:** Stand 2026-03-25 können Praktiker die verlinkte Hugging-Face-Seite als Ausgangspunkt für diese GGUF-Modelllinie nutzen. Vor dem Einsatz sollten Dateien, Herkunft, Lizenz und Laufzeitkompatibilität unabhängig überprüft werden.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten allein die datierten Ersetzungsangaben weiter oben.
