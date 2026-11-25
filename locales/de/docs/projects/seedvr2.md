---
title: "SeedVR2"
category: projects
date: 2026-07-30
tags: [project, seedvr, seedvr2, seedvr2-development-and-distribution]
aliases: ["SeedVR2"]
level: 3
source_sha256: 3da1feb253c4ca8b1a33799ddf3b980865c7f2a141e899527e2c4644b3b5d443
translation: machine
translated_at: '2026-10-24'
---
# SeedVR2 {#seedvr2}

**Entwicklungslinie:** `project:seedvr2` · Thread `seedvr2-development-and-distribution`  
**Letztes Ereignis:** 2026-07-30 · 3 datierte seit 2025-06-09 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

SeedVR2 ist der Nachfolger von SeedVR für die prompt-freie Wiederherstellung von Videos und Bildern: einstufiges Upscaling, adaptive Fenster-Aufmerksamkeit (adaptive windowed attention), Modelle mit 3B und 7B Parametern sowie eine Drittanbieter-Destillation mit 1.44B für weniger leistungsstarke Hardware. Einschränkung: Der offizielle Start ist auf ein Multi-Prozess-GPU-Inferenzschema ausgerichtet; die 1.4B-Variante unterstützt nur Bilder und benötigt eine separate Unterstützung im ComfyUI-Loader. Fazit: Für maximale Genauigkeit die offiziellen 3B/7B verwenden; die 1.4B ist ein bewusster Kompromiss zwischen Geschwindigkeit und Detailtreue.

## Entwicklungslinie {#development-line}

- **2025-06-09 — Projektseite von SeedVR2 wurde verlinkt.** Am 2025-06-09 wurde ein Link zur SeedVR2-Projektseite erfasst. Der datierte Link markiert einen öffentlichen Bezugspunkt für das Projekt, belegt aber selbst weder eine Veröffentlichung, die Verfügbarkeit von Modellen noch Implementierungsdetails.
- **2025-06-11 — Code- und Modell-Repositories von SeedVR wurden verlinkt.** Am 2025-06-11 wurden Links zum Quellcode-Repository ByteDance-Seed/SeedVR und zum SeedVR-Modell-Repository auf Hugging Face erfasst. Dies ist ein vorgelagertes Verteilungs- und Referenzereignis für die SeedVR2-Linie, wobei die vorliegenden Links allein weder das genaue Verhältnis zwischen SeedVR und SeedVR2 noch den Veröffentlichungsstand zu diesem Datum belegen.
- **2026-07-30 — ComfyUI-Paket für SeedVR2-1.4B wurde verlinkt.** Am 2026-07-30 wurden ein Hugging-Face-Repository namens SeedVR2-1.4B und dessen ComfyUI-Verzeichnis verlinkt. Dies dokumentiert einen praxisnahen, auf ComfyUI ausgerichteten Verteilungsweg für das genannte Modell, wobei die datierten Links allein weder Herkunft, Vollständigkeit noch Kompatibilität verifizieren.

## Was sich geändert hat {#what-changed}

2025-06-09 — SeedVR2 wurde als einstufige adversariale Diffusions-Wiederherstellung von Videos vorgestellt; Eingabegrößen müssen durch 32 teilbar sein. 2025-06-11 — Das offizielle Repository mit Startcode und Checkpoint-Modellen SeedVR2-3B/7B wurde angelegt. 2026-07-30 — Eine Drittanbieter-Destillation von SeedVR2-7B mit 1.44B und sechs Schichten wurde veröffentlicht, mit fertiger ComfyUI-Integration für das Upscaling statischer Bilder.

## Wie man das nutzt {#how-to-use-this}

Stand 2026-07-30 sollten Praktiker SeedVR2 als versionierten Bereitstellungspfad behandeln: Zuerst die offiziellen Projekt- und Repository-Referenzen konsultieren, danach das verlinkte 1.4B-ComfyUI-Paket unabhängig bewerten, bevor es in einem Workflow eingesetzt wird.

1. Für den offiziellen Start das Repository klonen, eine Python-3.10-Umgebung anlegen und requirements, FlashAttention sowie ein kompatibles Apex installieren.
  — <https://github.com/ByteDance-Seed/SeedVR>
2. Den offiziellen Checkpoint, z. B. ByteDance-Seed/SeedVR2-3B, per snapshot_download in den lokalen Ordner ckpts/ herunterladen.
  — <https://github.com/ByteDance-Seed/SeedVR>
3. projects/inference_seedvr2_3b.py mit torchrun starten und dabei Eingabeordner, Ausgabeauflösung, Seed und sequence-parallel degree angeben; die Eingabegrößen müssen durch 32 teilbar sein.
  — <https://github.com/ByteDance-Seed/SeedVR>
4. Für die 1.4B-Variante in ComfyUI den ComfyUI-Checkpoint in models/diffusion_models und das VAE in models/vae legen, den Support-Ordner nach custom_nodes kopieren und ComfyUI neu starten.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B>
5. Den fertigen Workflow laden und mit 4× beginnen; einen Schritt, CFG 1, Euler/simple und denoise 1 verwenden.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B/blob/main/comfyui/seedvr2_1.4b_upscale_image.json>

## Bewährte Vorgehensweisen {#best-practices}

- Den 1.4B-Checkpoint nicht im Standard-SeedVR2-Loader verwenden: Die sechs Blöcke erfordern einen ergänzten Zweig zur Architekturerkennung.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B>
- Für ComfyUI den Checkpoint aus dem Unterverzeichnis comfyui/ nehmen, nicht den aus dem Wurzelverzeichnis: Nur dort liegen die Conditioning-Tensoren, die der Loader benötigt.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B>
- Mit 4× beginnen; 8× verschlechtert die Qualität. VAE tile_size nicht über 512 erhöhen; bei Speichermangel auf 256 reduzieren.
  — <https://huggingface.co/lvladikov/SeedVR2-1.4B/blob/main/comfyui/seedvr2_1.4b_upscale_image.json>
- Ergebnisse an leichten Degradationen und kleinen Auflösungen prüfen: Das offizielle Projekt warnt vor überbetonten Details sowie vor geringer Robustheit gegenüber starken Degradationen und großen Bewegungen.
  — <https://github.com/ByteDance-Seed/SeedVR>

## Hierdurch abgelöst {#superseded-by-this}

- Nicht bestätigt: SeedVR (CVPR 2025) wurde nicht als veraltet erklärt; das offizielle Repository führt SeedVR und SeedVR2 weiterhin als getrennte Modelle.
- 2026-07-30: Die 1.4B-Destillation ersetzt die offiziellen 3B/7B hinsichtlich der Treue (Fidelity) nicht; sie ist für Speicher- und Latenzbeschränkungen gedacht.

## Noch unbekannt {#still-unknown}

- SeedVR2-1.4B ist eine Drittanbieter-Destillation von lvladikov, kein offizieller Checkpoint von ByteDance Seed; ihre numerischen Messungen und Vergleiche sind keine unabhängige Validierung.
- Beim historischen Link auf ByteDance-Seed/SeedVR-Models leitet die aktuelle URL auf SeedVR2-3B weiter; daher lässt sich der genaue Stand des ursprünglichen Modellbaums vom 2025-06-11 aus dieser Seite nicht rekonstruieren.
- Die offizielle Dokumentation beschreibt den Multi-GPU-Start; praktische Unterstützung für Single-GPU, Offloading und ComfyUI entwickelt sich in separaten Community-Implementierungen und ist durch diese offizielle Anleitung nicht bestätigt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://iceclear.github.io/projects/seedvr2/ | SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training | 2026-09-05 |
| https://arxiv.org/abs/2506.05301 | SeedVR2: One-Step Video Restoration via Diffusion Adversarial Post-Training | 2026-09-05 |
| https://github.com/ByteDance-Seed/SeedVR | ByteDance-Seed/SeedVR — Repository für SeedVR2 und SeedVR | 2026-09-05 |
| https://huggingface.co/ByteDance-Seed/SeedVR-Models/tree/main | Modellbaum ByteDance-Seed/SeedVR2-3B | 2026-09-05 |
| https://huggingface.co/lvladikov/SeedVR2-1.4B | lvladikov/SeedVR2-1.4B | 2026-09-05 |
| https://huggingface.co/lvladikov/SeedVR2-1.4B/tree/main/comfyui | SeedVR2-1.4B ComfyUI-Dateien | 2026-09-05 |
| https://huggingface.co/lvladikov/SeedVR2-1.4B/blob/main/comfyui/seedvr2_1.4b_upscale_image.json | SeedVR2-1.4B ComfyUI-Upscale-Workflow | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1va0dxy/seedvr214b_a_6layer_distillation_of_seedvr27b/ | SeedVR2-1.4B — eine 6-Schichten-Destillation von SeedVR2-7B | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:seedvr2`, Thread `seedvr2-development-and-distribution`, 3 datierte Ereignisse 2025-06-09 → 2026-07-30.
- **Praxishinweis:** Stand 2026-07-30 sollten Praktiker SeedVR2 als versionierten Bereitstellungspfad behandeln: Zuerst die offiziellen Projekt- und Repository-Referenzen konsultieren, danach das verlinkte 1.4B-ComfyUI-Paket unabhängig bewerten, bevor es in einem Workflow eingesetzt wird.
- **Konfidenz:** hoch. Die oben aufgeführten datierten Ersetzungen sind maßgeblich dafür, was veraltet ist.

<!-- authored-live-update:8c58cec247991662f3b16a987bbace4205f20ba435517274aa6d2da0aaa171bb -->
# SeedVR2 TensorRT Studio {#seedvr2-tensorrt-studio}

VRGDG SeedVR2 TensorRT Studio ist eine Windows-Anwendung rund um SeedVR2, kein offizielles ByteDance-Release. Ihre öffentliche Heimat ist das [Creator-Repository](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio). Die GitHub-Releases-Seite enthielt bei der Prüfung kein Release, daher kommen Installation und Updates aus dem Pfad `main` des Repositorys. [Releases](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/releases)

Das Studio nutzt eine kompatible SeedVR2-Integration, die von NumZs ComfyUI-Projekt abgeleitet ist. Der Creator gibt an, seine eigenen Ergänzungen umfassten die TensorRT-Encoder-Übergabe, die Latent-Erfassung und einen schnellen Pfad, der vor der VAE-Dekodierung stoppt. Dies ist eine Wrapper- und Integrationsschicht. [Drittanbieter-Hinweise](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/THIRD_PARTY_NOTICES.md)

## Was der Workflow hinzufügt {#what-the-workflow-adds}

- Eine kurze Vorschau vor dem vollständigen Render.
- Original-, wiederhergestellte, Wipe-Vergleichs- und Side-by-Side-Ansichten.
- Lokale TensorRT-VAE-Dekodierung auf unterstützter NVIDIA-RTX-Hardware.
- Ausgabeordner pro Job mit Medien, Manifesten und Logs.
- Wiederaufnehmbare Abschnitte für ein langes Video.

Die vorgesehene Reihenfolge ist einfach: einen Clip laden, das Ziel wählen, eine repräsentative Vorschau rendern, die Wipe- oder Side-by-Side-Ansicht nutzen und Gesichter, Sommersprossen, Muttermale und andere dauerhafte Merkmale prüfen, bevor der vollständige Render startet. [Workflow](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/README.md)

Der TensorRT-Pfad bietet die temporalen Batches 5 und 21. Dabei handelt es sich um Bildgruppen-Optionen innerhalb eines Renders. Sie belegen nicht, dass das Studio eine Warteschlange für mehrere Dateien hat. Ein offenes Issue vom 2. September forderte die Verarbeitung mehrerer Dateien nacheinander; daher gilt Batching über mehrere Dateien derzeit als nicht verifiziert. [Issues](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/issues)

## Grenzen der Installation {#installation-boundary}

Das paketierte Setup zielt auf Windows 11, einen aktuellen NVIDIA-RTX-Treiber und mindestens 35 GB freien Speicher. Es erzeugt TensorRT-Engine-Pläne lokal für die installierte GPU und Laufzeitumgebung von TensorRT. TensorRT-Plan-Dateien von einer anderen GPU oder Laufzeitumgebung nicht kopieren. [Installationsanleitung](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/docs/INSTALLATION.md)

Schlägt die TensorRT-Dekodierung nach dem Restaurierungsdurchlauf fehl, sagt das Studio, es könne die gespeicherten Latents mit seinem Stable-Decoder erneut versuchen. Das vermeidet eine Wiederholung der Restaurierung, ist aber ein Ausweichpfad und kein Beleg für dieselbe Geschwindigkeit oder Ausgabe wie bei der beschleunigten Dekodierung. [Workflow](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/README.md)

## Chunking erfordert eine Ausgabeprüfung {#chunking-needs-an-output-check}

Die Dokumentation bietet eine automatische Chunk-Wahl oder manuelle Chunks von 30 Sekunden bis 30 Minuten. Abgeschlossene Chunks sollen eine Unterbrechung überstehen, und ein Retry setzt beim ersten unfertigen Abschnitt fort.

Dieses Wiederherstellungsverhalten belegt nicht, dass die zusammengesetzte Datei brauchbar ist. Ein offenes Issue beschreibt eine 60-Sekunden-Eingabe, die in zwei Chunks geteilt wurde: Beide Chunk-Dateien ließen sich abspielen, das zusammengesetzte Video fror jedoch zur Hälfte ein. Der Melder sagt, dies sei vor den Korrekturen der Dateigröße geschehen, und er wisse nicht, ob die Korrektur damit zusammenhängt. Den Fehler für das aktuelle `main` als ungelöst behandeln. Unsere Vorsicht bei der Auslieferung: die finale Dauer, die Audiodauer, jede Verbindungsstelle und eine vollständige Dekodierung prüfen. [Issue #30](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/issues/30)

## Das RTX-5090-Beispiel {#the-rtx-5090-example}

Der Creator berichtet von einem Lauf: ein 8-Sekunden-Clip von 360p auf 2K in etwa 8 Minuten auf einer RTX 5090 mit 7B Sharp FP16. Das ist ein einzelnes veröffentlichtes Szenario, kein Benchmark. Die Quelle nennt nicht genug Details zu Bildrate, temporalem Batch, Treiber, TensorRT-Version, Ausgangsdegradation oder Ausgabeprüfung, um einen anderen Auftrag vorherzusagen. [README](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/blob/main/README.md)

Auch frühe Einrichtungsrisiken gibt es. Ein Issue dokumentiert einen CUDA-ONNX-Export-OOM beim Allokieren von 38050725888 Bytes auf einer GPU mit insgesamt 25756696576 Bytes Speicher, danach einen CPU-Export als Fallback. Ein Reddit-Kommentator berichtet außerdem von Flackern nach dem Hinzufügen zusätzlicher Filter. Beides sind Berichte aus benannten Konfigurationen oder von einzelnen Nutzern, keine allgemeingültige Grenze oder Voreinstellung. [Issue #26](https://github.com/vrgamegirl19/VRGDG-SeedVR2-TensorRT-Studio/issues/26) · [Community-Bericht](https://www.reddit.com/r/comfyui_elite/comments/1w6muu7/seedvr2_video_upscaler_suite_github_linked_in_post/)

## Noch unbekannt {#still-unknown_1}

Kein paketiertes Studio-Release gefunden. Kein unabhängiger Studio-Benchmark und keine verifizierte Warteschlange für mehrere Dateien gefunden. Die vereinfacht-chinesische Evidenzlage ist weiterhin unvollständig: Die begrenzte Recherche fand nur Verzeichnis- und Aggregationsseiten, kein vom Creator gepflegtes chinesisches Dokument und keinen reproduzierbaren chinesischen Betriebsbericht.

<!-- Retained base: 10a1a74b58eb65fd5b18c6a04e3d1b0dcadb09ea; article blob: 19e5cf206339f2bebe4cc872fb877cca05957b85 -->
