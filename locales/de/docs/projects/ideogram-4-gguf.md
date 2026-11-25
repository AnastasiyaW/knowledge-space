---
title: "ideogram-4-GGUF — Ideogram 4"
category: projects
date: 2026-06-11
tags: [ideogram-4, ideogram-4-gguf, project]
aliases: ["ideogram-4-GGUF"]
level: 2
source_sha256: bb11827f1097ee02f691c05eedb135802aaf53f658c6da835d2ebc4a70ac44a7
translation: machine
translated_at: '2026-10-24'
---
# ideogram-4-GGUF — Ideogram 4 {#ideogram-4-gguf-ideogram-4}

**Entwicklungslinie:** `project:ideogram-4-gguf` · Thread `ideogram-4`  
**Letztes Ereignis:** 2026-06-11 · 1 datiert seit 2026-06-11 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ideogram-4-GGUF ist ein Paar aus Q4_0-GGUF-Gewichten für die Haupt- und die unkonditionierte Diffusionskomponente von Ideogram 4.0, gedacht für lokale Ausführung statt über die API.

- Basismodell: Ideogram 4.0, 9,3B DiT.
- Laufzeitumgebung: stable-diffusion.cpp.
- Abhängigkeiten: Qwen3-VL-8B-Instruct im GGUF-Format und Flux2 AE VAE.

Die Haupt-Datei im Format Q4_0 belegt 5,64 GB. Dies ist weder ein offizieller Ideogram-Checkpoint noch ein fertiges ComfyUI-Setup.

Für ein CLI-Experiment mit stable-diffusion.cpp ist das geeignet. Für reproduzierbaren Produktivbetrieb sollten die genauen Versionen aller vier Komponenten sowie die Lizenz des Basismodells geprüft werden.

## Entwicklungslinie {#development-line}

- **2026-06-11 — Ideogram-4-GGUF-Repository auf Hugging Face verlinkt.** Q4_0-GGUF-Konvertierungen zweier Diffusionskomponenten von Ideogram 4.0 für stable-diffusion.cpp.

## Was sich geändert hat {#what-changed}

2026-06-11 — Der Link belegt die Verfügbarkeit von leejet/ideogram-4-GGUF: Q4_0-GGUF-Konvertierungen zweier Diffusionskomponenten von Ideogram 4.0 für stable-diffusion.cpp.

## Anwendung {#how-to-use-this}

Stand 2026-06-11 können Praktiker das verlinkte Hugging-Face-Repository als Kandidatenquelle für Ideogram-4-GGUF-Artefakte nutzen. Dabei sollten Dateien, Lizenz, Herkunft und Laufzeitkompatibilität vor dem Einsatz unabhängig überprüft werden.

1. Beide verlinkten Q4_0-Dateien herunterladen: die konditionierte `ideogram4-Q4_0.gguf` und die unkonditionierte `ideogram4_uncond-Q4_0.gguf`.
  — <https://huggingface.co/leejet/ideogram-4-GGUF>
2. Kompatibles `sd-cli` aus stable-diffusion.cpp bauen oder herunterladen; das Projekt beansprucht Unterstützung für Ideogram4 und das GGUF-Format.
  — <https://github.com/leejet/stable-diffusion.cpp>
3. Beide Diffusionsdateien, die GGUF-Version von Qwen3-VL-8B-Instruct und `flux2_ae.safetensors` an `sd-cli` übergeben; der Prompt muss gültiges JSON gemäß dem Beispiel der Model Card sein.
  — <https://huggingface.co/leejet/ideogram-4-GGUF>

## Best Practices {#best-practices}

- Strukturierte JSON-Prompts statt einfacher Zeichenketten verwenden, da die Quell-Pipeline auf dieses Schema trainiert wurde und es validiert.
  — <https://ideogram.ai/blog/ideogram-4.0/>
- Laufzeitversionen und alle abhängigen Gewichte festschreiben, da stable-diffusion.cpp ausdrücklich warnt, dass sich CLI-Optionen und APIs häufig ändern.
  — <https://github.com/leejet/stable-diffusion.cpp>
- Die Originallizenz von Ideogram 4.0 vor kommerzieller Nutzung prüfen, da die GGUF-Karte diese übernimmt und keine eigene festlegt.
  — <https://huggingface.co/leejet/ideogram-4-GGUF>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- 2026-06-03 — Vor Ideogram 4.0 gab es keine lokale GGUF-Variante; die offizielle Basisveröffentlichung stellte offene FP8- und NF4-Gewichte bereit, aber nicht dieses Drittanbieter-GGUF-Paket.
- 2026-06-04 — Die Annahme, Ideogram 4 lasse sich nicht in stable-diffusion.cpp ausführen, ist überholt; die Laufzeitumgebung kündigte Unterstützung für Ideogram4 an.

## Weiterhin unbekannt {#still-unknown}

- Keine unabhängige, datierte Primärquelle bestätigt das Veröffentlichungsdatum der GGUF-Konvertierung für das Ereignis vom 2026-06-11: Die öffentliche Model Card gibt den Repository-Stand wieder, während das Hugging-Face-Profil ein Update vom 2026-06-07 zeigt.
- Exakte Hashes, die aktuelle Kompatibilität von stable-diffusion.cpp mit diesen Dateien sowie die Ausgabequalität im Vergleich zu den originalen FP8- und NF4-Gewichten sind nicht verifiziert.
- Die offizielle Veröffentlichung von Ideogram 4.0 vom 2026-06-03 und das Drittanbieter-GGUF-Paket sind getrennte Einheiten: Erstere veröffentlichte das Basismodell, Letzteres konvertierte es für eine bestimmte Laufzeitumgebung.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/leejet/ideogram-4-GGUF | leejet/ideogram-4-GGUF | 2026-09-05 |
| https://github.com/leejet/stable-diffusion.cpp | leejet/stable-diffusion.cpp | 2026-09-05 |
| https://ideogram.ai/blog/ideogram-4.0/ | Ideogram 4.0 Technical Details: Open model at the forefront of design | 2026-09-05 |
| https://ideogram.ai/news/ideogram-4.0/ | Ideogram releases 4.0, a frontier image model with open weights, and a new brand for the company | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:ideogram-4-gguf`, Thread `ideogram-4`, 1 datiertes Ereignis 2026-06-11 → 2026-06-11.
- **Praktischer Hinweis:** Stand 2026-06-11 können Praktiker das verlinkte Hugging-Face-Repository als Kandidatenquelle für Ideogram-4-GGUF-Artefakte nutzen. Dabei sollten Dateien, Lizenz, Herkunft und Laufzeitkompatibilität vor dem Einsatz unabhängig überprüft werden.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.
