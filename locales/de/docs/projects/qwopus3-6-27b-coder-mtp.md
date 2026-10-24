---
title: "Qwopus3.6-27B-Coder-MTP"
category: projects
date: 2026-06-18
tags: [project, qwopus3-6-27b-coder-mtp, qwopus3-6-27b-coder-mtp-development, qwopus3_6]
aliases: ["Qwopus3.6-27B-Coder-MTP"]
level: 2
source_sha256: 3f6827bcf35f8e199e73df98f4d7a43f3f129d097e2ac091380b1717c59aab20
translation: machine
translated_at: '2026-10-24'
---
# Qwopus3.6-27B-Coder-MTP {#qwopus36-27b-coder-mtp}

**Entwicklungslinie:** `project:qwopus3-6-27b-coder-mtp` · Thread `qwopus3-6-27b-coder-mtp-development`  
**Letztes Ereignis:** 2026-06-18 · 1 datiertes seit 2026-06-18 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Qwopus3.6-27B-Coder-MTP ist ein Coding-Fine-Tune von Qwopus3.6-27B-v2 mit MTP-Draft-Heads für die lokale Arbeit an Repositories.

- Codegenerierung für Repositories.
- Debugging und Patchen von Code.
- Strukturierte Tool-Aufrufe.

Die verfügbaren GGUF-Quantisierungen reichen von 13,5 GB Q3_K_M bis 29 GB Q8_0. Der von der Community gemeldete SWE-bench-Wert liegt bei 335/500 in einem Q5_K_M-Lauf mit deaktiviertem Thinking, weitere Suiten stehen noch aus. Wir verwenden das Modell als experimentelles lokales Coding-Modell, nicht als unabhängig validierte Produktionsinstanz.

## Entwicklungslinie {#development-line}

- **2026-06-18 — GGUF-Artefakt von Qwopus3.6-27B-Coder-MTP verlinkt.** Wir haben Qwopus3.6-27B-Coder-MTP-GGUF, dessen Basis Qwopus3.6-27B-v2 und den Konvertierungsworkflow Qwen MTP-zu-GGUF als einen lokalen Pfad für spekulatives Decodieren verlinkt.

## Was sich geändert hat {#what-changed}

2026-06-18: Qwopus3.6-27B-Coder-MTP-GGUF, dessen Basis Qwopus3.6-27B-v2 und der Konvertierungsworkflow Qwen MTP-zu-GGUF wurden als ein lokaler Pfad für spekulatives Decodieren verlinkt.

## Wie dies zu verwenden ist {#how-to-use-this}

Ab dem 2026-06-18 sollte das verlinkte GGUF-Artefakt als Kandidat für ein Coder-MTP-Deployment-Format behandelt werden. Vor der Verwendung Herkunft, Laufzeitkompatibilität, Lizenz und Leistung gegen das verlinkte v2-Modell prüfen.

1. Eine GGUF-Quantisierung wählen, die zu Speicherplatz und Arbeitsspeicher passt. Das Repository listet Builds von Q3_K_M bis Q8_0 auf.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/tree/main>
2. Das GGUF in einer llama.cpp-kompatiblen lokalen Anwendung ausführen. Die Model Card nennt llama.cpp, Ollama und LM Studio als kompatible Zielumgebungen.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF>
3. Tool-Definitionen und System-Prompt für Agenten am Trainingsformat ausrichten. Text innerhalb von <think>-Tags im Client behandeln.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md>

## Best Practices {#best-practices}

- Den gemeldeten SWE-bench-Wert von 67,0 % als Einzelkonfiguration behandeln, nicht als harness-übergreifendes Ranking. Die Model Card kennzeichnet das Release als experimentell und lässt weitere Suiten offen.
  — <https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md>
- Den Preflight vor dem Herunterladen der Gewichte ausführen, wenn ein MTP-GGUF erstellt oder neu verpackt wird. Eine Abweichung in der Quell-/Zielkonfiguration oder unzureichender Speicherplatz bricht den Build ab.
  — <https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md>
- Das GGUF vor Upload oder Deployment mit einem Smoke-Test prüfen. Ein passendes Quellmodell für die MTP-Heads verwenden, statt davon auszugehen, dass Heads zwischen Varianten übertragbar sind.
  — <https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md>

## Durch dieses ersetzt {#superseded-by-this}

- 2026-07-09: Ein Commit zur Bereinigung des GGUF per Super-Squash ersetzte die bisherige feingranulare Repository-Historie. Er zeigt keine neue Modellfähigkeit.

## Weiterhin ungeklärt {#still-unknown}

- Keine datierte Primärquelle belegt, dass die Benchmark-, Durchsatz- oder MTP-Geschwindigkeitsangaben am 2026-06-18 zutrafen. Wir ordnen diese Angaben diesem Ereignis nicht zu.
- Die Hugging-Face-Metadaten kennzeichnen das GGUF als image-text-to-text, Transformers und CLIP-Architektur mit 0,5B, die README beschreibt jedoch ein 27B-Coding-GGUF. Dieser Widerspruch macht die Transformers-, vLLM- und Bildbeispiele für das Deployment unverifiziert.
- Für den Release-Stand vom 2026-06-18 existiert kein unabhängiges Benchmark-Reproduktion, keine Kompatibilitätsmatrix und kein Changelog.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF | Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF Model Card | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/blob/main/README.md | Qwopus3.6-27B-Coder-MTP-GGUF README | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/tree/main | Qwopus3.6-27B-Coder-MTP-GGUF Dateibaum | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-v2 | Jackrong/Qwopus3.6-27B-v2 Model Card | 2026-09-05 |
| https://github.com/R6410418/Jackrong-llm-finetuning-guide/tree/main/qwen-mtp-gguf | Verzeichnis des Repositorys Qwen MTP GGUF Conversion Skill | 2026-09-05 |
| https://raw.githubusercontent.com/R6410418/Jackrong-llm-finetuning-guide/main/qwen-mtp-gguf/README.md | README der Qwen MTP GGUF Conversion Skill | 2026-09-05 |
| https://huggingface.co/Jackrong/Qwopus3.6-27B-Coder-MTP-GGUF/commits/main | Commit-Historie von Qwopus3.6-27B-Coder-MTP-GGUF | 2026-09-05 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:qwopus3-6-27b-coder-mtp`, Thread `qwopus3-6-27b-coder-mtp-development`, 1 datiertes Ereignis, 2026-06-18 → 2026-06-18.
- **Praktischer Hinweis:** Ab dem 2026-06-18 sollte das verlinkte GGUF-Artefakt als Kandidat für ein Coder-MTP-Deployment-Format behandelt werden. Vor der Verwendung Herkunft, Laufzeitkompatibilität, Lizenz und Leistung gegen das verlinkte v2-Modell prüfen.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
