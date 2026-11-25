---
title: "LiveEdit"
category: projects
date: 2026-06-30
tags: [liveedit, project]
aliases: ["LiveEdit"]
level: 2
source_sha256: 3fb8c2dfe7bc5339018baee3e702091ac08c05660d3ed74953010d8d587b47d1
translation: machine
translated_at: '2026-10-24'
---
# LiveEdit {#liveedit}

**Entwicklungslinie:** `project:liveedit` · Thread `liveedit`  
**Letztes Ereignis:** 2026-06-30 · 1 datiertes seit 2026-06-30 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

LiveEdit ist ein textgesteuerter Video-zu-Video-Editor für Linux- und NVIDIA-Systeme. Er basiert auf Wan2.1-T2V-1.3B und läuft nicht als gehosteter Dienst.

- Video-zu-Video-Bearbeitung auf Grundlage von Textprompts für einen Eingabestream.
- Kausale Verarbeitung in Chunks, damit Hintergrund und unbearbeitete Abschnitte erhalten bleiben.
- Autoregressives Mask-Caching für kurze Clips und ein erweiterter Pfad für lange Videos.

## Entwicklungslinie {#development-line}

- **2026-06-30 — Die Projektressourcen von LiveEdit wurden öffentlich verlinkt.** Die offizielle Projektseite von LiveEdit, das Code-Repository und die Modell-Checkpoints waren bereits online. Die Zeitangaben der Autoren setzen Code und Hinweise zu den Checkpoints auf 2026-06-24 und das Preprint v1 auf 2026-06-25. Das Datum 2026-06-30 ist daher kein Veröffentlichungsdatum der Autoren.

## Was sich geändert hat {#what-changed}

- **2026-06-30:** Die offiziellen Projekt-, Quellcode- und Modell-Endpunkte von LiveEdit waren bereits öffentlich. Die Autoren haben Code- und Checkpoint-Anleitungen am 2026-06-24 und Preprint v1 am 2026-06-25 veröffentlicht, daher ist dies kein Veröffentlichungsdatum der Autoren.
- **2026-07-13:** arXiv hat das Paper auf v2 aktualisiert, ohne dass Code- oder Checkpoint-Veröffentlichungen hinzukamen.
- **2026-08-05:** Die Autoren dokumentierten Inferenz für lange Videos mit rollierenden Attention Sinks und fensterrelativem RoPE.

## So wird es verwendet {#how-to-use-this}

1. Unter Linux mit NVIDIA-GPU die dokumentierte Python-3.10-Umgebung anlegen. Die Requirements und FlashAttention installieren. Inferenz auf einer GPU funktioniert; Trainingsskripte erfordern Multi-GPU-torchrun.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
2. Wan-AI/Wan2.1-T2V-1.3B und den dokumentierten Checkpoint ar-forcing_002000.pt in die Pfade herunterladen, die das Repository erwartet.
  — <https://huggingface.co/cp-cp/LiveEdit>
3. Eine JSON-Datei mit instruction und source_path anlegen. Für den dokumentierten V2V-Pfad infer-local-ar-forcing.sh ausführen.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
4. infer-token-pruning.sh mit --save_mask ausführen, um den Cache zu untersuchen. Für längere Clips infer-local-ar-forcing-long.sh ausführen.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>

## Best Practices {#best-practices}

- Den dokumentierten Checkpoint ar-forcing_002000.pt mit 2.000 Schritten und das mitgelieferte Skript verwenden. Nicht jede Gewichtsdatei im Repository hat ein eigenständiges Rezept.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
- Im Modus für lange Videos SINK_SIZE kleiner als LOCAL_ATTN_SIZE halten und bei der Ziel-Clip-Länge testen. Die Autoren weisen darauf hin, dass die Ausgabe jenseits des Trainingshorizonts für kurze Sequenzen schlechter wird.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
- Masken-Visualisierungen beim Token-Pruning speichern, damit wir prüfen können, welche Regionen der Cache wiederverwendet.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>

## Hiermit abgelöst {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Der Eintrag vom 2026-06-30 liefert nur sein Datum und die offiziellen URLs; die zugrunde liegende Aussage ist nicht verfügbar.
- Keine unabhängige Ausführung hat die berichteten 12,66 FPS reproduziert oder eine VRAM-Untergrenze für LiveEdit festgelegt. Diese Geschwindigkeit ist eine von den Autoren angegebene Zahl.
- Der Name LiveEdit ist mehrfach belegt: qizhou000/LiveEdit ist ein separates Projekt zur Bearbeitung von Vision-Language-Modellen (CVPR 2025). Das cp-cp-Repository, der Hugging-Face-Checkpoint, die Projektseite und das arXiv-Preprint beziehen sich auf dieses Videobearbeitungsprojekt.
- Die Daten 2026-06-24 und 2026-08-05 stammen aus den Änderungsprotokollen im README der Autoren, nicht aus unabhängiger Verfolgung von Veröffentlichungen oder Qualitätstests Dritter.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://live-edit.github.io/ | LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing | ECCV 2026 | 2026-09-06 |
| https://github.com/cp-cp/LiveEdit | GitHub - cp-cp/LiveEdit: LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing | 2026-09-06 |
| https://github.com/cp-cp/LiveEdit/blob/main/README.md | README.md · cp-cp/LiveEdit at main | 2026-09-06 |
| https://huggingface.co/cp-cp/LiveEdit | cp-cp/LiveEdit · Hugging Face | 2026-09-06 |
| https://arxiv.org/abs/2606.26740 | LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing | 2026-09-06 |
| https://github.com/qizhou000/LiveEdit | qizhou000/LiveEdit: Lifelong Knowledge Editing for Vision Language Models with Low-Rank Mixture-of-Experts | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:liveedit`, Thread `liveedit`, 1 datiertes Ereignis 2026-06-30 → 2026-06-30.
- **Praktischer Hinweis:** Die belegten Abschnitte zu Nutzung und Praxis oben verwenden, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ablösungen entscheiden, was veraltet ist.
