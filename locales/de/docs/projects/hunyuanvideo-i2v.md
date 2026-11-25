---
title: "HunyuanVideo-I2V — Öffentliche Verfügbarkeit des Projekts"
category: projects
date: 2025-03-06
tags: [hunyuanvideo, hunyuanvideo-i2v, project, public-project-availability]
aliases: ["HunyuanVideo-I2V"]
level: 3
source_sha256: c42bc1ab2ea59f8357ef40f9d5875b4cc0f50918a2d75e02a86dd7aa3ab79e29
translation: machine
translated_at: '2026-10-24'
---
# HunyuanVideo-I2V — Öffentliche Verfügbarkeit des Projekts {#hunyuanvideo-i2v-public-project-availability}

**Entwicklungslinie:** `project:hunyuanvideo-i2v` · Thread `public-project-availability`  
**Letztes Ereignis:** 2025-03-06 · 1 datiertes Ereignis seit 2025-03-06 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

HunyuanVideo-I2V ist Tencents lokaler Image-to-Video-Stack aus dem Jahr 2025 für Teams, die eine erste-Frame-gesteuerte Generierung statt einer gehosteten API benötigen.

- Eingaben: Referenzbild und Textprompt als Konditionierung.
- Komponenten: offizieller PyTorch-Code, vortrainierte Gewichte, Sampling, LoRA-Training und xDiT-Multi-GPU-Inferenz.
- Ausgabe: Videogenerierung mit bis zu 720p und 129 Frames (etwa fünf Sekunden).

Die offizielle Anleitung für eine einzelne GPU gibt einen Spitzenbedarf von 60 GB VRAM an und wurde mit 80 GB getestet.

Der ursprüngliche Stack bleibt lauffähig, doch neue Deployments sollten die spätere I2V-Linie HunyuanVideo-1.5 vergleichen, bevor Hardware und Integrationsarbeit festgelegt werden.

## Entwicklungslinie {#development-line}

- **2025-03-06 — Öffentliche Projektveröffentlichung von HunyuanVideo-I2V.** Tencent veröffentlichte den Inferenzcode und die Modellgewichte.

## Was sich geändert hat {#what-changed}

HunyuanVideo-I2V startet mit einer lokalen 720p-Veröffentlichung, korrigiert die anfänglichen Gewichte und ergänzt Multi-GPU-Inferenz.

- 2025-03-06: Tencent veröffentlichte den Inferenzcode und die Modellgewichte.
- 2025-03-07: Tencent ersetzte den Veröffentlichungsstand nach der Behebung eines ID-Wechsel-Fehlers; die korrigierten Gewichte sind die maßgebliche Quelle für die Konsistenz des ersten Frames.
- 2025-03-09: Tencent veröffentlichte an diesem Tag keinen separaten offiziellen Code, keine Gewichte und keine Versionsänderung; eine Implementierungsänderung lässt sich nicht verifizieren.
- 2025-03-11: Tencent aktualisierte nach der Fehlerbehebung den Code für LoRA-Training und -Inferenz.
- 2025-03-13: Tencent veröffentlichte die xDiT-gestützte parallele Inferenz.
- 2025-11-21: Tencent veröffentlichte die separate Linie HunyuanVideo-1.5 T2V/I2V mit I2V-Checkpoints für 480p und 720p; sie ist nicht als direkte Fortsetzung dieses Repositorys dokumentiert.

## So nutzen Sie das {#how-to-use-this}

Ab dem 2025-03-06 sollten Praktiker die verlinkte offizielle Hugging-Face-Seite und das Tencent-GitHub-Repository als kanonische Ausgangspunkte für HunyuanVideo-I2V verwenden und mit Maßnahmen auf Basis späterer Ankündigungen warten, bis archivierte Update-Inhalte vorliegen.

1. Prüfen Sie, ob der ursprüngliche Stack auf die Maschine passt: Linux und eine NVIDIA-CUDA-GPU sind erforderlich; planen Sie 60 GB Spitzen-VRAM bei 720p ein, wobei 80 GB die getestete Konfiguration ist.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
2. Klonen Sie das offizielle Repository, legen Sie dessen Python-3.11.9-Umgebung an und installieren Sie die dokumentierten PyTorch/CUDA-Abhängigkeiten und Requirements; verwenden Sie den veröffentlichten CUDA-12-Container, falls dieser zum Deployment passt.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
3. Laden Sie die aktuellen offiziellen HunyuanVideo-I2V-Gewichte von der Modellkarte bei Tencent herunter und prüfen Sie vor der Nutzung die Tencent Hunyuan Community License.
  — <https://huggingface.co/tencent/HunyuanVideo-I2V>
4. Führen Sie sample_image2video.py mit HYVideo-T/2, --i2v-mode, einem Pfad zum Referenzbild, einem knappen Prompt, 720p-Auflösung, Sampling-Schritten, Videolänge und einem Ausgabepfad aus; aktivieren Sie bei Bedarf CPU-Offload für hochauflösende Generierung.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
5. Wählen Sie bewusst zwischen stabiler und dynamischer Bewegung: Der stabile Modus verwendet --i2v-stability mit --flow-shift 7.0; dynamische Ausgabe erfolgt mit deaktivierter Stabilität und --flow-shift 17.0. Setzen Sie einen Seed, wenn das Ergebnis reproduzierbar sein muss.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
6. Für einen individuellen Effekt bereiten Sie Trainingsdaten aus Videos und Captions vor, führen das mitgelieferte LoRA-Trainingsskript aus und laden anschließend die erzeugte safetensors-Datei bei der Inferenz über --use-lora und --lora-path.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>

## Best Practices {#best-practices}

- Verwenden Sie nicht die Startgewichte vom 6. März: Nutzen Sie die korrigierten Gewichte, die nach der Behebung des Identitätswechsels angekündigt wurden.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Halten Sie den Prompt kurz und konkret: Nennen Sie Subjekt und Aktion und ergänzen Sie Hintergrund oder Kamera nur bei Bedarf; zu detaillierte Prompts können unerwünschte Übergänge erzeugen.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Verwenden Sie Flow Shift 7 mit aktiviertem stabilen Modus für ruhigere Bewegung, und Flow Shift 17 mit deaktiviertem stabilen Modus, wenn Bewegung wichtiger ist als Stabilität.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Planen Sie die Hardware anhand des dokumentierten Minimums von 60 GB und gehen Sie nicht davon aus, dass CPU-Offload den 720p-Workflow zu einem Low-VRAM-Workflow macht; die offiziell getestete Konfiguration sind 80 GB.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Für LoRA-Effekte setzen Sie einen Phrasen- oder Kurzsatz als Trigger direkt in jede Video-Caption; trainieren Sie mit 360p und verwenden Sie das resultierende LoRA anschließend für die Inferenz bei 720p.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>

## Abgelöst durch {#superseded-by-this}

- Die ursprünglichen HunyuanVideo-I2V-Gewichte vom 2025-03-06 sind durch die korrigierten Gewichte vom 2025-03-07 abgelöst, weil die ursprüngliche Open-Source-Veröffentlichung die Identität verändern konnte.
- Die Deployment-Entscheidung vom 2025-03-06 ist datiert, aber nicht formell abgekündigt: HunyuanVideo-1.5 wurde am 2025-11-21 als separate spätere T2V/I2V-Linie von Tencent mit I2V-Checkpoints für 480p und 720p veröffentlicht. Bewerten Sie sie für neue Deployments, gehen Sie aber nicht von Kompatibilität bei Checkpoints oder Workflows aus.

## Weiterhin unbekannt {#still-unknown}

- Das Ereignis vom 9. März lässt sich anhand von Primärquellen keinem eindeutigen vorgelagerten Release zuordnen; die verlinkte Quellseite war nicht abrufbar.
- Tencent dokumentiert HunyuanVideo-1.5 nicht als direktes Upgrade oder formellen Ersatz für HunyuanVideo-I2V.
- Die Quellen nennen für den ursprünglichen HunyuanVideo-I2V-Stack keine aktuelle Wartungszusage, kein Supportfenster und keine Verfügbarkeit einer gehosteten API.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news | HunyuanVideo-I2V-README und Neuigkeiten — Tencent-Hunyuan auf GitHub | 2026-09-04 |
| https://huggingface.co/tencent/HunyuanVideo-I2V | Modellkarte tencent/HunyuanVideo-I2V — Hugging Face | 2026-09-04 |
| https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5 | HunyuanVideo-1.5-README — Tencent-Hunyuan auf GitHub | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:hunyuanvideo-i2v`, Thread `public-project-availability`, 1 datiertes Ereignis 2025-03-06 → 2025-03-06.
- **Praxishinweis:** Ab dem 2025-03-06 sollten Praktiker die verlinkte offizielle Hugging-Face-Seite und das Tencent-GitHub-Repository als kanonische Ausgangspunkte für HunyuanVideo-I2V verwenden und mit Maßnahmen auf Basis späterer Ankündigungen warten, bis archivierte Update-Inhalte vorliegen.
- **Konfidenz:** mittel. Die datierten Ablösungshinweise oben sind maßgeblich für die Frage, was veraltet ist.
