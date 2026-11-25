---
title: "Wan-Dancer"
category: projects
date: 2026-07-14
tags: [project, wan-dancer, wan-dancer-development, wan_dancer]
aliases: ["Wan-Dancer"]
level: 3
source_sha256: 08cddcd0a6b79356af28a9fa68215576bec9cd8d032ebfddf159bd794de40251
translation: machine
translated_at: '2026-10-24'
---
# Wan-Dancer {#wan-dancer}

**Entwicklungslinie:** `project:wan-dancer` · Thread `wan-dancer-development`  
**Letztes Ereignis:** 2026-07-14 · 1 datiertes Ereignis seit 2026-07-14 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

Wan-Dancer ist ein 14B-System zur Erzeugung von Tanzvideos aus Musik für Kreative, die einen langen, choreografierten Clip aus einem Porträt, einer Musikspur und einem Stil-Prompt benötigen, statt kurze Clips manuell zusammenzufügen.

- Globale Keyframe-Planung aus dem vollständigen Titel.
- Lokale Verfeinerung für zeitliche Kontinuität.
- Stil-Prompts für Chinese Classical, K-Pop, Street, Tap und Latin Dance.

Die angegebene Ausgabe läuft mit 720p und 30 fps für mehr als eine Minute. Die Autoren haben ihren Code auf 8 × NVIDIA A800 80GB GPUs getestet. Wir verwenden die Pipeline der Autoren für kontrollierte Langform-Arbeiten, nicht als validierten Einzel-GPU- oder reinen Demo-Workflow.

## Entwicklungslinie {#development-line}

- **2026-07-14 — Projektressourcen zu Wan-Dancer wurden öffentlich verlinkt.** Am 2026-07-14 erschienen öffentliche Links zur Projektwebsite von Wan-Dancer, zum Quell-Repository, zur Hugging-Face-Modellseite und zum ModelScope Studio. Das markierte einen Verteilungsmeilenstein des Projekts. Die Links belegen keine technischen Aussagen, Versionsdetails oder den ursprünglichen Ankündigungswortlaut.

## Was sich geändert hat {#what-changed}

Wan-Dancer — Entwicklungslinie.

- 2026-05-09 — ComfyUI hat die Kernunterstützung für WanDancer vor der öffentlichen Modellveröffentlichung zusammengeführt; dies spiegelt die Implementierungshistorie wider, nicht die Verfügbarkeit öffentlicher Artefakte.
- 2026-07-10 — arXiv v1 veröffentlichte die hierarchische Methode für Musik-zu-Tanz.
- 2026-07-13 — Wan-AI kündigte die Veröffentlichung der Wan-Dancer-14B-Gewichte und des Inferenzcodes an.
- 2026-07-14 — Das offizielle Repository hat einen Commit zur Aktualisierung der Links gepusht, und ein ModelScope-Community-Beitrag dokumentierte einen Studio-Ablauf für Porträt und Musik.
- 2026-07-17 — arXiv veröffentlichte v3, ohne in den Metadaten Verhaltens- oder Gewichtsänderungen zu beschreiben.

## Verwendung {#how-to-use-this}

Stand 2026-07-14: Prüfe die verlinkte Projektseite auf Quellcode und offizielle Modellverteilungen, und überprüfe dann Zugang, Lizenz und Anleitungen, bevor du das Projekt übernimmst.

1. Klone Wan-Video/Wan-Dancer, erstelle die virtuelle Umgebung und installiere den fixierten Abhängigkeitssatz aus der README. Die Referenzplattform ist Ubuntu 22.04, Python 3.10.14 und CUDA 12.4.
  — <https://github.com/Wan-Video/Wan-Dancer>
2. Lade Wan-AI/Wan-Dancer-14B mit huggingface-cli in ein kontrolliertes lokales Modellverzeichnis herunter.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
3. Bereite image_path, music_path und einen globalen prompt_path vor; die Prompt-Familien decken Chinese Classical, K-Pop, Street, Tap und Latin Dance ab.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
4. Führe gen_video_global.sh aus und speichere das erzeugte globale Video zusammen mit Seed und Einstellungen.
  — <https://github.com/Wan-Video/Wan-Dancer>
5. Übergib dieses Ergebnis als global_video_path an gen_video_local.sh mit dem passenden lokalen Prompt, damit die lokale Verfeinerung ihr Basisvideo hat.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
6. Für ComfyUI: Aktualisiere ComfyUI, öffne dessen Wan-Dancer-Vorlage und lege die globalen/lokalen Modelle, LoRA, Text-Encoder, CLIP-Vision-Modell und VAE in benannten Vorlagenordnern ab. Diese Vorlage wird upstream geändert und wurde hier nicht lokal verifiziert.
  — <https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_dancer.json>

## Bewährte Praktiken {#best-practices}

- Fixiere den Seed über alle Vergleiche hinweg, damit Läufe reproduzierbar bleiben.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
- Behandle globale und lokale Generierung als eine Pipeline und ersetze das erforderliche global_video_path niemals durch einen unzusammenhängenden Clip.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
- Erhöhe die Inferenzschritte bei längeren Videos; die Autoren empfehlen 48 Schritte, statt das lokale Beispiel mit 24 Schritten als allgemeingültig zu betrachten.
  — <https://huggingface.co/Wan-AI/Wan-Dancer-14B>
- Bewerte die Rohqualität nicht anhand der Projektgalerie, da die gezeigten Videos nachbearbeitet wurden.
  — <https://humanaigc.github.io/wan-dancer-project/>
- Beginne mit dem Standardwert von 5 Sekunden in der ComfyUI-Vorlage und überwache den VRAM, da das gleichzeitige Sampling von 149 Frames viel Speicher benötigt.
  — <https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_dancer.json>
- Betrachte das Testsystem der Autoren mit 8 × A800 80GB nicht als Mindestanforderung für eine einzelne GPU, da es als Referenzumgebung dient und nicht als Hardware-Untergrenze.
  — <https://github.com/Wan-Video/Wan-Dancer>

## Abgelöst durch {#superseded-by-this}

- Die Annahme, dass der 2026-07-14 das erste öffentliche Veröffentlichungsdatum der Wan-Dancer-Gewichte und des Inferenzcodes sei; die offizielle Modellkarte datiert diese Veröffentlichung auf den 2026-07-13.

## Noch unbekannt {#still-unknown}

- Die direkte ModelScope-Studio-Seite zeigte keine Live-Steuerelemente, weshalb ihre aktuellen Felder, Standardwerte, Zugriffsrichtlinien und Grenzen nicht verifiziert sind.
- Keine Quelle der Autoren veröffentlichte einen Mindest-VRAM-Bedarf für eine einzelne GPU, eine Laufzeit oder eine vollständige Reproduktion; das einzige berichtete Setup ist 8 × A800 80GB.
- Die gezeigten Videos wurden nachbearbeitet und sind nicht unabhängig reproduziert, daher sind die angegebene Dauer und Qualität keine Produktionsgarantien.
- Die Herkunft der Checkpoints und die Kompatibilität zwischen Wan-Dancer-14B und den wan2.2_dancer-Assets in der ComfyUI-Vorlage sind nicht verifiziert.
- Der Unterstützungsstatus für ComfyUI ist ungeklärt: Die offizielle Modellkarte kennzeichnet die Integration als unvollständig, während ComfyUI eine funktionierende Vorlage zusammengeführt hat.
- Die geprüften Quellen zeigen nach dem 2026-07-17 keine offizielle Funktions- oder Gewichtsaktualisierung von Wan-Dancer, wobei nicht indexierte Veröffentlichungen möglich sind.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://humanaigc.github.io/wan-dancer-project/ | Wan-Dancer-Projektseite | 2026-09-06 |
| https://github.com/Wan-Video/Wan-Dancer | Offizielles Repository Wan-Video/Wan-Dancer | 2026-09-06 |
| https://github.com/Wan-Video/Wan-Dancer/commits/main/ | Commit-Verlauf von Wan-Video/Wan-Dancer | 2026-09-06 |
| https://huggingface.co/Wan-AI/Wan-Dancer-14B | Modellkarte Wan-AI/Wan-Dancer-14B | 2026-09-06 |
| https://arxiv.org/abs/2607.09581 | Wan-Dancer: A Hierarchical Framework for Minute-scale Coherent Music-to-Dance Generation | 2026-09-06 |
| https://modelscope.csdn.net/6a55a9d210ee7a33f28d3bfc.html | ModelScope Community: Ankündigung der Open-Source-Veröffentlichung von Wan-Dancer | 2026-09-06 |
| https://github.com/Comfy-Org/ComfyUI/pull/13813 | ComfyUI Pull Request #13813: Support Wan-Dancer | 2026-09-06 |
| https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan_dancer.json | Comfy-Org Wan-Dancer-Workflow-Vorlage auf main | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:wan-dancer`, Thread `wan-dancer-development`, 1 datiertes Ereignis 2026-07-14 → 2026-07-14.
- **Praktischer Hinweis:** Stand 2026-07-14 können Praktiker über die verlinkte Projektseite Quellcode und offizielle Modellverteilungen von Wan-Dancer finden und sollten vor der Übernahme aktuellen Zugang, Lizenz und Nutzungsanleitungen prüfen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.
