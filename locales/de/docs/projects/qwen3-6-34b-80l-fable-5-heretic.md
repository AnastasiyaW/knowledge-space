---
title: "Qwen3.6-34B-80L-Fable-5-Heretic"
category: projects
date: 2026-06-29
tags: [project, qwen3-6-34b-80l-fable-5-heretic]
aliases: ["Qwen3.6-34B-80L-Fable-5-Heretic"]
level: 2
source_sha256: fd7289b5b7966a4a09c8b06db2662a70ccb669307e0dbc1cd4b1cd8e9f3988e0
translation: machine
translated_at: '2026-10-24'
---
# Qwen3.6-34B-80L-Fable-5-Heretic {#qwen36-34b-80l-fable-5-heretic}

**Entwicklungslinie:** `project:qwen3-6-34b-80l-fable-5-heretic` · Thread `qwen3-6-34b-80l-fable-5-heretic`  
**Letztes Ereignis:** 2026-06-29 · 1 datiertes seit 2026-06-29 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Qwen3.6-34B-80L-Fable-5-Heretic ist eine BF16-Ableitung von Qwen3.6-27B für den Selbsthostingbetrieb mit Transformers oder vLLM.

- 80 Layer, ~34B Parameter und ein laut Angabe bis zu 256K großer Kontext.
- QLoRA-Training auf 4 665 agentischen CoT-Traces von Fable-5.
- MTP-Gewichte im Repository für spekulatives Dekodieren.

## Entwicklungslinie {#development-line}

- **2026-06-29 — Modellseite Qwen3.6-34B-80L-Fable-5-Heretic auf Hugging Face erfasst.** Eine Ableitung von Qwen3.6-27B, erweitert von 64 auf 80 Layer, mit einer Angabe von ~34B Parametern, BF16-Gewichten, 4 665 QLoRA-Traces und 15 MTP-Gewichten. Wir haben keine unabhängige, datierte Bestätigung der Veröffentlichung am 2026-06-29 gefunden.

## Was sich geändert hat {#what-changed}

2026-06-29 — Wir haben den Link zu hiebo/Qwen3.6-34B-80L-Fable-5-Heretic erfasst. Die Model Card beschreibt diesen Schritt: Die Ableitung von Qwen3.6-27B wird von 64 auf 80 Layer erweitert, mit einer Angabe von ~34B Parametern, BF16-Gewichten, 4 665 QLoRA-Traces und 15 MTP-Gewichten. Wir haben keine unabhängige, datierte Bestätigung der Veröffentlichung am 2026-06-29 gefunden.

Nach 2026-06-29 — Wir haben keine verifizierten datierten Änderungen am Modell gefunden. Spiegel auf Hugging Face verteilen dieselben Artefakte, nicht eine neue Version.

## So wird es verwendet {#how-to-use-this}

Ab 2026-06-29 die Qwen3.6-34B-80L-Fable-5-Heretic-Seite auf Hugging Face suchen und Model Card, Dateien, Lizenzierung, Herkunft und Kompatibilität prüfen, bevor es eingesetzt wird.

1. Die exakte ID `hiebo/Qwen3.6-34B-80L-Fable-5-Heretic` über Transformers mit `device_map="auto"` laden und einen kurzen Prompt testen, bevor der volle Kontext geladen wird.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
2. Mit dem vLLM-Befehl aus der Model Card unter BF16 und mit explizitem `--max-model-len` bereitstellen. Mit einem niedrigeren Limit beginnen, bis KV-Cache und GPU-Speicher gemessen sind.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>

## Best Practices {#best-practices}

- Einstellungen des Basismodells nicht automatisch übernehmen: Die eigene Ableitung ändert die Layer-Anzahl und fügt MTP-Gewichte hinzu, daher zuerst mit einem lokalen Smoke-Test prüfen, ob Loader, Tokenizer und Generierungspipeline kompatibel sind.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
- Die angegebene Akzeptanzrate von 78 % und den Durchsatz von 2× als Hypothese der Model Card behandeln; Akzeptanz, Latenz und Qualität auf der eigenen Aufgabensuite messen.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
- Das Basismodell Qwen empfiehlt ein großes Generierungslimit für komplexe Aufgaben; dies als experimentelle Einstellung behandeln, nicht als Beleg für die Qualität der Ableitung.
  — <https://huggingface.co/Qwen/Qwen3.6-27B>

## Hierdurch abgelöst {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die Model Card ist eine Behauptung des Autors aus einem persönlichen Repository; wir haben keine unabhängigen Evaluierungen, reproduzierbaren Trainingsläufe oder verifizierten Beschleunigungen gefunden.
- Primärquellen nennen keine genauen Veröffentlichungs- und Aktualisierungsdaten, daher können wir nicht bestätigen, dass die Veröffentlichung am 2026-06-29 erfolgte.
- Das Schema enthält keine Felder `event_findings` und `new_events`; relevante Befunde haben wir in `what_changed` und `unknowns` erfasst.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic | hiebo/Qwen3.6-34B-80L-Fable-5-Heretic — model card | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.6-27B | Qwen/Qwen3.6-27B — official model card | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:qwen3-6-34b-80l-fable-5-heretic`, Thread `qwen3-6-34b-80l-fable-5-heretic`, 1 datiertes Ereignis 2026-06-29 → 2026-06-29.
- **Praktischer Hinweis:** Ab 2026-06-29 können Praktiker den Hugging-Face-Eintrag zu Qwen3.6-34B-80L-Fable-5-Heretic finden und sollten Model Card, Dateien, Lizenzierung, Herkunft und Kompatibilität prüfen, bevor sie ihn einsetzen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich für das, was veraltet ist.
