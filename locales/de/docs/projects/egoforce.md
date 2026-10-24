---
title: "EgoForce"
category: projects
date: 2026-07-14
tags: [egoforce, egoforce-development, project]
aliases: ["EgoForce"]
level: 2
source_sha256: 9c9c0b83bb8195bd78cff838c25c2e07c7b29b799ffffc774cf81c4e86be5e49
translation: machine
translated_at: '2026-10-24'
---
# EgoForce {#egoforce}

**Entwicklungslinie:** `project:egoforce` · Thread `egoforce-development`  
**Letztes Ereignis:** 2026-07-14 · 1 datiertes Ereignis seit 2026-07-14 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

EgoForce schätzt die absolute 3D-Handpose und das Handmesh im Kamerakoordinatensystem aus einer einzelnen egozentrischen RGB-Kamera.

- Kameraunterstützung: funktioniert mit Fisheye-, Perspektiv- und verzerrten Weitwinkelkameras.
- Mitgelieferte Assets: enthält Gewichte, Datensätze und eine Gradio/Project-Aria-Demo.
- Benchmark: meldet bis zu 28 % niedrigeren kamerabezogenen MPJPE auf HOT3D.

Es handelt sich um Forschungscode für kalibrierte egozentrische Aufnahmen, nicht um ein allgemeines kommerzielles Hand-Tracking-SDK.

## Entwicklungslinie {#development-line}

- **2026-07-14 — Öffentliche Projektressourcen zu EgoForce wurden verlinkt.** Am 2026-07-14 verlinkte die EgoForce-Entwicklungslinie eine Projektseite, ein Quellcode-Repository, eine Hugging-Face-Modellseite und einen Hugging-Face-Space. Zusammen etablieren die datierten Links einen öffentlichen Einstiegspunkt für Projektinformationen, Code, Modellartefakte und eine interaktive Oberfläche. Sie enthalten keine Aussagen zu einer bestimmten Version, Fähigkeiten, Benchmarks oder Veröffentlichungsstatus.

## Was sich geändert hat {#what-changed}

- **2026-05-12** — Das Paper von DFKI/MPII stellte den unterarmgeführten Ansatz im Ray-Space vor.
- **2026-07-14** — Der Projektcode, die Modellassets, der Datensatz und die Browser-Demo waren gemeinsam verfügbar.
- **2026-08-09** — Ein offener Bericht dokumentierte einen Fehler beim Tracking der linken Hand auf einer benannten HOT3D-Sequenz; eine verifizierte Korrektur wurde nicht gefunden.

## Anwendung {#how-to-use-this}

Stand 2026-07-14 dienen die verlinkte Projektseite, das Repository, die Modellseite und der Space als Ausgangspunkte, um EgoForce zu evaluieren oder zu reproduzieren. Vor einer Verwendung sollten jedoch deren aktuelle Inhalte und Bedingungen geprüft werden.

1. Erstelle die dokumentierte Python-3.10-Conda-Umgebung und führe den Installer des Repositories aus.
  — <https://github.com/dfki-av/EgoForce/tree/main>
2. Lade die Modellgewichte und benötigten Assets herunter und setze dann das Dataset-Root-Verzeichnis in settings.py.
  — <https://github.com/dfki-av/EgoForce/tree/main>
3. Führe experiments/save_predictions.py für einen unterstützten Datensatz aus und evaluiere anschließend die gespeicherte Vorhersagedatei mit den passenden Flags.
  — <https://github.com/dfki-av/EgoForce/tree/main>
4. Für einen schnellen visuellen Test lädst du ein Video in die gehostete Demo hoch oder führst die Gradio-App des Repositories lokal aus.
  — <https://huggingface.co/spaces/chris10/EgoForce>

## Best Practices {#best-practices}

- Behandle es als nicht-kommerzielle Forschungssoftware: Code und Gewichte stehen unter CC-BY-NC 4.0, während die mitgelieferten WiLoR- und MANO-Assets eigene Lizenzen haben.
  — <https://huggingface.co/chris10/EgoForce>
- Validiere die Kamera-Intrinsics und verwende die passenden Flags für Vorhersage und Evaluation; die Autoren dokumentieren eine Sweep-Analyse zum Rauschen der Intrinsics sowie variantenspezifische Suffixe für Ausgabedateien.
  — <https://github.com/dfki-av/EgoForce/tree/main>
- Teste beide Hände auf den Zielsequenzen, bevor du dich auf das System verlässt: Ein Fehler bei der linken Hand auf HOT3D ist im öffentlichen Issue-Tracker weiterhin offen.
  — <https://github.com/dfki-av/EgoForce/issues>

## Abgelöst durch dies {#superseded-by-this}

- Bisher nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Ein anderes Paper aus dem Mai 2026 trägt ebenfalls den Namen EgoForce, ist aber ein separates, diffusionsbasiertes Projekt zur Rekonstruktion der Ganzkörperbewegung von anderen Autoren; die angegebenen URLs beziehen sich auf das DFKI-Handpose-Projekt.
- Es wurde keine datierte Release-Notiz gefunden, die unabhängig bestätigt, warum die Links zu Code, Modell, Daten und Demo am 2026-07-14 gebündelt wurden.
- Das offene Issue zur linken Hand auf HOT3D belegt einen gemeldeten Fehler, nicht dessen Häufigkeit oder eine bestätigte Korrektur.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://dfki-av.github.io/EgoForce/ | EgoForce-Projektseite | 2026-09-05 |
| https://github.com/dfki-av/EgoForce/tree/main | dfki-av/EgoForce, offizielle Implementierung | 2026-09-05 |
| https://huggingface.co/chris10/EgoForce | chris10/EgoForce, Modell-Repository | 2026-09-05 |
| https://huggingface.co/spaces/chris10/EgoForce | chris10/EgoForce, Demo | 2026-09-05 |
| https://arxiv.org/abs/2605.12498 | EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera | 2026-09-05 |
| https://github.com/dfki-av/EgoForce/issues | EgoForce-Issue-Tracker | 2026-09-05 |
| https://arxiv.org/abs/2605.13041 | EgoForce: Robust Online Egocentric Motion Reconstruction via Diffusion Forcing | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:egoforce`, Thread `egoforce-development`, 1 datiertes Ereignis 2026-07-14 → 2026-07-14.
- **Praktischer Hinweis:** Stand 2026-07-14 sollten Praktiker die verlinkte Projektseite, das Repository, die Modellseite und den Space als Ausgangspunkte nutzen, um EgoForce zu evaluieren oder zu reproduzieren, und vor einer Verwendung deren aktuelle Inhalte und Bedingungen prüfen.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
