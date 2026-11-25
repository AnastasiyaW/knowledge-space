---
title: "VideoLifter"
category: projects
date: 2025-01-22
tags: [project, videolifter]
aliases: ["VideoLifter"]
level: 2
source_sha256: 93d4713af674cbf8a7d8c97c8afb1e9b1ab58a828e5aa9e21309febe36bc1d5a
translation: machine
translated_at: '2026-10-24'
---
# VideoLifter {#videolifter}

**Entwicklungslinie:** `project:videolifter` · Thread `videolifter`  
**Letztes Ereignis:** 2025-01-22 · 2 datierte Einträge seit 2025-01-09 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

VideoLifter — ein SfM-freies Framework für Forscher im Bereich 3D-Rekonstruktion: Es nimmt unkalibrierte Bilder aus Videos entgegen, nutzt DUSt3R und MASt3R für die initiale Geometrie, optimiert anschließend eine 3D-Gaussian-Repräsentation und richtet Fragmente zu einer gemeinsamen Szene aus. Funktionen: Schätzung von Posen und Struktur, Rekonstruktion langer Videos über lokale Fenster, Novel-View-Synthese. Kennzahl: Die Autoren geben eine Reduktion der Trainingszeit um mehr als 82 % an. Fazit: Einsatz lohnt sich in einer CUDA-Umgebung mit vorbereiteten Tanks-and-Temples- bzw. CO3D-Daten, wobei man eine Forschungspipeline mit Training und Evaluation erwarten sollte.

## Entwicklungslinie {#development-line}

- **2025-01-09 — Projektwebseite von VideoLifter referenziert.** Die hierarchische Stereo-Ausrichtung ersetzt vorab berechnete Kameras und klassisches SfM beim Übergang von Video zu 3D.
- **2025-01-22 — GitHub-Repository von VideoLifter referenziert.** Am 2025-01-22 verknüpfte ein datierter Eintrag das GitHub-Repository VITA-Group/VideoLifter sowie einen früheren verwandten Link. Damit ist eine öffentliche Quell-Repository-Referenz in der Projekthistorie belegt, nicht jedoch Version, Release, Commit oder Funktionsstatus des Repositorys an diesem Datum.

## Was sich geändert hat {#what-changed}

2025-01-09 — Beschreibung der Methode veröffentlicht: Die hierarchische Stereo-Ausrichtung ersetzt vorab berechnete Kameras und klassisches SfM beim Übergang von Video zu 3D. 2025-01-22 — Ein offizielles Reproduktions-Repository erschien, mit Abhängigkeiten, einem vortrainierten MASt3R-Checkpoint und separaten Skripten für Tanks and Temples und CO3D.

## Anwendung {#how-to-use-this}

Ab 2025-01-22 sollten Praktiker, die Implementierungsmaterial zu VideoLifter suchen, mit dem verlinkten Repository VITA-Group/VideoLifter beginnen; die Webseite vom 2025-01-09 dient als öffentlicher Einstiegspunkt des Projekts. Version, Lizenz und Nutzungsdetails sind separat zu prüfen.

1. Klonen Sie das Repository mit Submodulen und laden Sie den Checkpoint MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth in submodules/mast3r/checkpoints herunter.
  — <https://github.com/VITA-Group/VideoLifter>
2. Erstellen Sie eine conda-Umgebung mit Python 3.10, PyTorch 2.1.0 und CUDA 11.8; installieren Sie anschließend die requirements und die zwei lokalen CUDA-Pakete.
  — <https://github.com/VITA-Group/VideoLifter>
3. Bereiten Sie die Daten vor: Tanks and Temples in data/Tanks bzw. das Preprocessing der Autoren für CO3D in data/co3d.
  — <https://github.com/VITA-Group/VideoLifter>
4. Starten Sie scripts/train_tt.sh für Tanks and Temples oder scripts/train_co3d.sh für CO3D; die Ergebnisse sind für Training und Evaluation der 3D-Rekonstruktion gedacht.
  — <https://github.com/VITA-Group/VideoLifter>

## Best Practices {#best-practices}

- Klonen Sie mit --recursive: DUSt3R und MASt3R sind als Submodule eingebunden, ohne sie lässt sich die Pipeline nicht reproduzieren.
  — <https://github.com/VITA-Group/VideoLifter>
- Verwenden Sie die von den Autoren festgelegten Versionen von Python, PyTorch und CUDA und keine beliebige aktuelle Umgebung.
  — <https://github.com/VITA-Group/VideoLifter>
- Kompilieren Sie die CUDA-Kernels für RoPE aus CroCo: Die Autoren kennzeichnen dies als optional, aber dringend empfohlene Beschleunigung.
  — <https://github.com/VITA-Group/VideoLifter>

## Abgelöst durch diesen Eintrag {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Nach dem ursprünglichen Repository wurde kein datierter Release-Tag, kein Paket und kein Modell von VideoLifter gefunden; die aktuelle Dokumentation beschreibt eine Forschungsreproduktion, bestätigt aber nicht die Unterstützung beliebiger eigener Videos als fertiges Produkt.
- Für das Ereignis vom 2025-01-22 ist das GitHub-README verfügbar, die Seite nennt jedoch kein eigenes Datum für die konkrete Änderung. Die Angaben zur Umgebung sind daher als aktueller Stand des offiziellen Repositorys zu lesen und nicht als Beleg dafür, dass jede einzelne davon genau am 22. Januar hinzugefügt wurde.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://videolifter.github.io/ | VideoLifter: Lifting Videos to 3D with Fast Hierarchical Stereo Alignment | 2026-09-05 |
| https://github.com/VITA-Group/VideoLifter | VITA-Group/VideoLifter — offizielle Implementierung | 2026-09-05 |
| https://arxiv.org/abs/2501.01949 | VideoLifter: Lifting Videos to 3D with Fast Hierarchical Stereo Alignment | 2026-09-05 |
| https://ece.utexas.edu/news/wenyan-cong-receives-best-paper-award-cvpr-workshop | Wenyan Cong Receives Best Paper Award at CVPR Workshop | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:videolifter`, Thread `videolifter`, 2 datierte Ereignisse 2025-01-09 → 2025-01-22.
- **Praxishinweis:** Ab 2025-01-22 sollten Praktiker, die Implementierungsmaterial zu VideoLifter suchen, mit dem verlinkten Repository VITA-Group/VideoLifter beginnen; die Webseite vom 2025-01-09 dient als öffentlicher Einstiegspunkt des Projekts. Version, Lizenz und Nutzungsdetails sind separat zu prüfen.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Einträge zu „Abgelöst durch“ als maßgeblich.
