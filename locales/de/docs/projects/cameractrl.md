---
title: "CameraCtrl"
category: projects
date: 2024-05-29
tags: [cameractrl, cameractrl-development, project]
aliases: ["CameraCtrl"]
level: 3
source_sha256: 9cddf8b85147979fffdcbfd74ca06f4babee9fb9d546c30da84c3cf51b8b6649
translation: machine
translated_at: '2026-10-24'
---
# CameraCtrl {#cameractrl}

**Entwicklungslinie:** `project:cameractrl` · Thread `cameractrl-development`  
**Letztes Ereignis:** 2024-05-29 · 2 datierte Einträge seit 2024-04-10 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

CameraCtrl ist eine Forschungscodebasis für die Videogenerierung mit vorgegebener Kamerabewegung in AnimateDiffV3 und Stable Video Diffusion.

- Konditionierung über die Kamerapose: steuert die Videogenerierung entlang einer exakten Kameratrajektorie.
- Modularer Aufbau: trennt das Basis-Diffusionsmodell von den Gewichten für die Kamerasteuerung.
- Backend-Implementierungen: stellt AnimateDiffV3 auf `main` und die SVD-Image-to-Video-Variante auf `svd` bereit.

## Entwicklungslinie {#development-line}

- **2024-04-10 — Projektseite und Quellcode-Repository von CameraCtrl wurden verlinkt.** Am 2024-04-10 verwiesen öffentliche Links auf die CameraCtrl-Projektseite und das GitHub-Repository. Die Links belegen die öffentliche Verfügbarkeit, nennen aber weder eine Release-Version noch den Inhalt der Veröffentlichung.
- **2024-05-29 — Ein CameraCtrl-svd-Hugging-Face-Space wurde verlinkt.** Am 2024-05-29 verlinkte die öffentliche Nachverfolgung den CameraCtrl-svd-Hugging-Face-Space und verwies auf den früheren CameraCtrl-Beitrag. Dies zeigte einen Demo-Schritt, doch allein die Links bestätigen weder Funktionsfähigkeit, Modellversion noch Live-Status an diesem Datum.

## Was sich geändert hat {#what-changed}

2024-04-10 — CameraCtrl erschien auf seiner Projektseite und im öffentlichen Repository. Die Release Notes datieren die Veröffentlichung von AnimateDiffV3-Code und Checkpoint auf 2024-04-03.
2024-05-29 — Der Pfad für Stable Video Diffusion erschien über die SVD-xt-Demo. Die Hinweise der Maintainer datieren Code, vortrainierte Modelle und die Gradio-Demo auf 2024-05-24. Damit kam eine eigenständige SVD-Image-to-Video-Implementierung hinzu.
2025-03-13 [heute gefunden] — CameraCtrl II wurde eingereicht, um die Forschung auf die iterative Erkundung dynamischer Szenen auszuweiten.
2026-09-04 [heute gefunden] — Das ursprüngliche Repository ordnet AnimateDiffV3 weiterhin `main` und SVD weiterhin `svd` zu. Der öffentliche CameraCtrl-svd-Space zeigt einen Fehler beim Import einer Abhängigkeit an.

## Verwendung {#how-to-use-this}

Wir hatten am 2024-04-10 öffentliche Projekt- und Quellcode-Links. Der CameraCtrl-svd-Hugging-Face-Space folgte am 2024-05-29 zum Testen. Die reinen Link-Belege stützen keine operativen Aussagen über diese Orte hinaus.

1. Wählen Sie zuerst das Backend: Verwenden Sie `main` für AnimateDiffV3 und checken Sie `svd` nur für die Stable-Video-Diffusion-Image-to-Video-Variante aus.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
2. Für den AnimateDiffV3-Pfad erstellen Sie die dokumentierte Python-3.10/CUDA-11.7-Umgebung und aktivieren `cameractrl`.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
3. Laden Sie SD1.5, den AnimateDiffV3-Adaptor, die Motion-Module-Checkpoints und den CameraCtrl-Checkpoint herunter. Führen Sie den ADV3-Adaptor vor der Inferenz mit dem SD1.5-UNet zusammen.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
4. Bereiten Sie eine Trajektorien-Textdatei und eine Prompt-JSON aus den bereitgestellten Assets vor und visualisieren Sie die Trajektorie vor dem Sampling.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
5. Führen Sie das dokumentierte `inference.py`-Rezept aus und geben Sie die Pfade zum Basismodell, zum Motion Module, zum CameraCtrl-Checkpoint, zum Prompt, zur Trajektorie und zur Ausgabe an. Der Referenzstart verwendet acht Prozesse.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
6. Für SVD verwenden Sie die Umgebung `svd`, einen kompatiblen SVD- oder SVD-xt-Checkpoint, Konditionierungsbilder, Prompt-JSON und Trajektorie. Die dokumentierten Frame-Anzahlen sind 14 für SVD und 25 für SVD-xt.
  — <https://github.com/hehao13/CameraCtrl/blob/svd/README.md>

## Best Practices {#best-practices}

- Halten Sie `main` und `svd` getrennt: Sie zielen auf unterschiedliche Backends, Umgebungen und Eingabemodi, daher sollten Sie ihre Setup-Anleitungen oder Checkpoints nicht vermischen.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
- Behandeln Sie die Kameratrajektorie als erstklassige Eingabe: Beginnen Sie mit den mitgelieferten Pose-Dateien, visualisieren Sie den Pfad und halten Sie Prompts und Seeds fest, wenn Sie Trajektorien vergleichen.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
- Verwenden Sie das passende Asset-Set: main benötigt SD1.5 sowie zusammengeführte ADV3- und CameraCtrl-Gewichte, während `svd` SVD/SVD-xt und den dazu passenden CameraCtrl-Checkpoint benötigt.
  — <https://github.com/hehao13/CameraCtrl/blob/svd/README.md>
- Reproduzieren Sie Ergebnisse mit der vom Projekt festgelegten Umgebung, bevor Sie Bibliotheken aktualisieren. Die main-Umgebung fixiert Python 3.10, PyTorch 1.13.1, CUDA 11.7, diffusers 0.24.0 und xformers 0.0.16.
  — <https://github.com/hehao13/CameraCtrl/blob/main/environment.yaml>
- Betreiben Sie SVD lokal, statt sich auf den öffentlichen Space zu verlassen, bis dieser repariert ist: Der Fehler im Space ist ein Importfehler für `cached_download`.
  — <https://huggingface.co/spaces/hehao13/CameraCtrl-svd>

## Durch Folgendes ersetzt {#superseded-by-this}

- Einrichtungshinweise vom 2024-04-10, die nur `main` betrafen — für SVD-Nutzer durch das Release `svd` vom 2024-05-24 ersetzt. Dies ist eine eigenständige Image-to-Video-Implementierung und kein Upgrade von `main`.
- Workflow mit der gehosteten Demo vom 2024-05-29 — seit 2026-09-04 durch den beobachteten Laufzeitfehler des CameraCtrl-svd-Space ersetzt. Führen Sie den lokalen Pfad `svd` aus, um Ergebnisse zu reproduzieren.

## Weiterhin unbekannt {#still-unknown}

- Die Fehlerseite des CameraCtrl-svd stammt aus einem Crawl, der als zwei Wochen alt gekennzeichnet ist. Eine aktuelle interaktive Prüfung war nicht möglich. Prüfen Sie den Laufzeitstatus, bevor Sie sich darauf verlassen.
- CameraCtrl II ist ein späteres Forschungsprojekt ohne offizielle Migrationsanleitung, kompatibles Release oder Drop-in-Zusicherung. Wir betrachten es nicht als Ersatz für das Repository von 2024.
- Die Autorenseite nennt CameraCtrl II++, doch Tests haben weder ein nutzbares Release noch die Kompatibilität mit dem ursprünglichen CameraCtrl-Workflow bestätigt.
- Es gibt kein offizielles Referenzrezept für eine einzelne GPU. Beide dokumentierten Inferenzbeispiele verwenden acht Prozesse.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://hehao13.github.io/projects-CameraCtrl/ | CameraCtrl: Enabling Camera Control for Video Diffusion Models | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl | hehao13/CameraCtrl | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl/blob/main/README.md | CameraCtrl README — main branch | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl/blob/main/environment.yaml | CameraCtrl environment.yaml — main branch | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl/blob/svd/README.md | CameraCtrl README — svd branch | 2026-09-04 |
| https://huggingface.co/spaces/hehao13/CameraCtrl-svd | CameraCtrl Svd Xt — Hugging Face Space | 2026-09-04 |
| https://arxiv.org/abs/2404.02101 | CameraCtrl: Enabling Camera Control for Text-to-Video Generation | 2026-09-04 |
| https://arxiv.org/abs/2503.10592 | CameraCtrl II: Dynamic Scene Exploration via Camera-controlled Video Diffusion Models | 2026-09-04 |
| https://hehao13.github.io/ | Hao He — projects | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:cameractrl`, Thread `cameractrl-development`, 2 datierte Ereignisse vom 2024-04-10 bis 2024-05-29.
- **Praktischer Hinweis:** Öffentliche Projekt- und Quellcode-Links waren am 2024-04-10 erreichbar. Der CameraCtrl-svd-Hugging-Face-Space stand am 2024-05-29 zur Evaluation bereit. Die reinen Link-Belege rechtfertigen keine operativen Aussagen über diese Orte hinaus.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise sind maßgeblich dafür, was veraltet ist.
