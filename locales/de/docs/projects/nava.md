---
title: "NAVA"
category: projects
date: 2026-06-03
tags: [nava, nava-development, project]
aliases: ["NAVA"]
level: 3
source_sha256: e5c145d7400bd1fc03b2eb4689a3d60ca4fb21710c94665cfa83435c84311ca9
translation: machine
translated_at: '2026-10-24'
---
# NAVA {#nava}

**Entwicklungslinie:** `project:nava` · Thread `nava-development`  
**Letztes Ereignis:** 2026-06-03 · 1 datiertes Ereignis seit 2026-06-03 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

NAVA ist ein lokales gemeinsames Audio-Video-Modell für Text-zu-Audio-Video, Fortsetzung ab dem ersten Frame eines Bildes, reine Audiogenerierung und Sprachsynthese mit Referenzklangfarbe.

- Erzeugt Video und Stereo-Szenen- sowie Sprachaudio gemeinsam, statt Audio nach der Videogenerierung anzuhängen.
- Verwendet einen Align-then-Fuse-MMDiT; Referenz-WAVs werden auf geordnete `<S>…<E>`-Sprachspannen abgebildet.
- 1280×704 bei 37 Frames/24 fps läuft etwa sechs Sekunden lang; vollständig residente Inferenz ist mit 80 GB VRAM dokumentiert, der FP8-Pfad benötigt etwa 18 GB.
- Den gepflegten lokalen Code oder den ComfyUI-Pfad verwenden; die offizielle gehostete Space war zum Zeitpunkt der Prüfung pausiert.

## Entwicklungslinie {#development-line}

- **2026-06-03 — NAVA-Projektressourcen wurden verlinkt.** Am 2026-06-03 verlinkte NAVA seine Projektseite, das GitHub-Repository und die Hugging-Face-Seite, um Leser direkt zu Dokumentation, Quellcode und Modellressourcen zu führen.

## Was sich geändert hat {#what-changed}

- 2026-05-28 — NAVA-Paper v1 beschrieb einen 6,3B Align-then-Fuse-MMDiT für gemeinsame Audio-Video-Generierung.
- 2026-05-29 — NAVA erreichte seine offizielle initiale Modellveröffentlichung.
- 2026-05-30 — NAVA lud `NAVA.safetensors` hoch und entfernte die Hub-Kopie der veralteten `NAVA.ckpt`.
- 2026-06-01 — NAVA ergänzte den `NAVA_fp8.safetensors`-Checkpoint für geringeren VRAM-Bedarf.
- 2026-06-03 — NAVA lud englische und vereinfacht-chinesische Model-Card-Dokumentation hoch; GitHub aktualisierte außerdem das README und die optimierte Inferenz.
- 2026-06-05 — NAVA ergänzte FP8-Unterstützung für ComfyUI.
- 2026-06-08 — NAVA optimierte und bereinigte seine ComfyUI-Implementierung.
- 2026-06-15 — NAVA behob die Desynchronisation des FP8-Prompt-Rewriters und ergänzte einen Vision-Language-Rewrite-Workflow.
- 2026-06-23 — NAVA aktualisierte seine Hugging-Face-Space- und Gradio-Implementierung.
- 2026-06-30 — NAVA aktualisierte die VerseBench-Inferenzskripte.

## Verwendung {#how-to-use-this}

1. Die offizielle gehostete Demo derzeit als nicht verfügbar betrachten: Ihre Space war zum Zeitpunkt der Prüfung pausiert; stattdessen einen lokalen Workflow verwenden.
  — <https://huggingface.co/spaces/baidu/NAVA>
2. Den offiziellen Code klonen, zuerst das CUDA-passende PyTorch installieren und danach NAVA und FlashAttention in der dokumentierten Reihenfolge installieren.
  — <https://github.com/ernie-research/NAVA>
3. Die gepflegten Gewichte von der aktuellen Modellseite `baidu/NAVA` herunterladen; `NAVA.safetensors` für bf16 oder `NAVA_fp8.safetensors` für den Pfad mit geringerem VRAM-Bedarf verwenden.
  — <https://huggingface.co/baidu/NAVA>
4. Jeden Auftrag als JSONL vorbereiten: `prompt` für Text-zu-Audio-Video verwenden, `image_path` für die Konditionierung auf den ersten Frame hinzufügen und bis zu zwei `spk_wavs` für klangfarbengesteuerte Sprache ergänzen; danach das passende Inferenzskript wählen.
  — <https://github.com/ernie-research/NAVA>
5. Für einen Node-Workflow die offiziellen ComfyUI-Nodes installieren, `NAVA_fp8.safetensors` auswählen und eines der mitgelieferten Beispielgraphen laden.
  — <https://github.com/ernie-research/NAVA/blob/main/comfyui_nava/README.md>

## Bewährte Vorgehensweisen {#best-practices}

- Die CUDA-passende PyTorch-Installation, die editierbare NAVA-Installation und `flash-attn --no-build-isolation` als getrennte Schritte durchführen; die Requirements-Datei nicht mit Force-Reinstall installieren.
  — <https://github.com/ernie-research/NAVA>
- Kurze oder englische Prompts vor der Inferenz umschreiben und jede `<S>…<E>`-Sprachspanne unverändert belassen.
  — <https://github.com/ernie-research/NAVA>
- Die Reihenfolge der Referenz-WAVs an die Reihenfolge der Sprachspannen anpassen; für ComfyUI zuerst T5-Offload aktivieren und bei weniger als 48 GB VRAM Group-Offload verwenden.
  — <https://github.com/ernie-research/NAVA/blob/main/comfyui_nava/README.md>
- FP8 zur Reduzierung des VRAM-Bedarfs einsetzen, nicht in der Erwartung schnellerer Matrixberechnungen; zur Rechenzeit wird nach bf16 dequantisiert.
  — <https://github.com/ernie-research/NAVA>
- Nur Gesichts- und Stimmreferenzen verwenden, für die eine Einwilligung vorliegt, generiertes Material als synthetisch kennzeichnen und vor einer Weitergabe Herkunftsnachweise oder Wasserzeichen anbringen.
  — <https://huggingface.co/baidu/NAVA>
- Standardmäßig die aktuellen safetensors-Checkpoints verwenden; der Hub hat `NAVA.ckpt` gelöscht, obwohl der lokale Code die Checkpoint-Kompatibilität beibehält.
  — <https://huggingface.co/baidu/NAVA/commits/main>

## Hierdurch überholt {#superseded-by-this}

- 2026-05-30 — Die Hub-Download-Anleitung, die `NAVA.ckpt` voraussetzt, ist veraltet: Der offizielle Hub hat dieses Artefakt entfernt und stellt safetensors-Checkpoints bereit; lokale `.ckpt`-Kompatibilität bleibt erhalten.
- 2026-06-05 — Die Behandlung von NAVA als reinen Skript-Workflow für 8 GPUs ist veraltet: Das offizielle Projekt hat einen FP8-ComfyUI-Pfad ergänzt.
- 2026-06-15 — Die FP8-Prompt-Rewrite-Anleitung vor der Korrektur ist für bildkonditionierte Arbeiten veraltet: Der offizielle Code hat die Desynchronisation des Rewriters behoben und VL-Rewrite ergänzt.

## Weiterhin unbekannt {#still-unknown}

- Der genaue Begleittext des Eintrags vom 2026-06-03 ist nicht verfügbar; deshalb behandeln wir dieses Datum als Meilenstein für Dokumentations- und Inferenzaktualisierung am selben Tag, nicht als abgeleitete Startankündigung.
- Keine semantischen Release-Tags oder GitHub-Releases ordnen Commit-Änderungen versionierten NAVA-Releases zu.
- Die offizielle Space war zum Zeitpunkt der Prüfung pausiert, daher wurde ein erfolgreicher aktueller gehosteter Inferenzlauf nicht verifiziert.
- Die offizielle Dokumentation ist intern inkonsistent: Der aktuelle Code verwendet standardmäßig safetensors, während Teile der Model Card noch gelöschte `NAVA.ckpt`-Pfade zeigen.
- Nach dem 2026-06-30 wurde kein späterer Eintrag der Erstanbieter zu Code oder Modellverlauf gefunden; dies beweist nicht, dass außerhalb der geprüften offiziellen Verläufe kein Update existiert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://arxiv.org/abs/2605.30073 | Native Audio-Visual Alignment for Generation — arXiv:2605.30073 | 2026-09-06 |
| https://ernie-research.github.io/NAVA/ | NAVA · Native Audio-Visual Alignment for Generation | 2026-09-06 |
| https://github.com/ernie-research/NAVA | ernie-research/NAVA — Offizieller Code von NAVA | 2026-09-06 |
| https://github.com/ernie-research/NAVA/commits/main | Commits · ernie-research/NAVA | 2026-09-06 |
| https://huggingface.co/ernie-research/NAVA | ernie-research/NAVA-Weiterleitung auf baidu/NAVA | 2026-09-06 |
| https://huggingface.co/baidu/NAVA | baidu/NAVA · Hugging Face | 2026-09-06 |
| https://huggingface.co/baidu/NAVA/commits/main | Commits · baidu/NAVA | 2026-09-06 |
| https://huggingface.co/baidu/NAVA/blob/main/README_zh.md | README_zh.md · baidu/NAVA | 2026-09-06 |
| https://github.com/ernie-research/NAVA/blob/main/comfyui_nava/README.md | NAVA ComfyUI Nodes | 2026-09-06 |
| https://huggingface.co/spaces/baidu/NAVA | NAVA Audio-Video Generator — Hugging Face Space | 2026-09-06 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:nava`, Thread `nava-development`, 1 datiertes Ereignis vom 2026-06-03 bis 2026-06-03.
- **Praktische Anmerkung:** Siehe die belegten Abschnitte zu Verwendung und bewährten Vorgehensweisen oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Die datierten Einträge unter „Hierdurch überholt" sind maßgeblich dafür, was veraltet ist.
