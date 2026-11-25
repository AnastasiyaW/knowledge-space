---
title: "ControlVideo"
category: projects
date: 2023-07-09
tags: [controlvideo, project]
aliases: ["ControlVideo"]
level: 3
source_sha256: 68cdf0c098a5efcbda64b2b0bbc059823725f487d03aacbce98357588a5339ed
translation: machine
translated_at: '2026-10-24'
---
# ControlVideo {#controlvideo}

**Entwicklungslinie:** `project:controlvideo` · Thread `controlvideo`  
**Letztes Ereignis:** 2023-07-09 · 2 datierte Ereignisse seit 2023-05-23 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

ControlVideo erzeugt ein neues SD-1.5-Video, das auf einem Quellvideo und einem Text-Prompt konditioniert ist.

- Bildweise Konditionen: extrahiert ControlNet-Signale, darunter Tiefe, Kanten und Pose.
- Bildkonsistenz: fügt volle Cross-Frame-Attention und verschachtelte Glättung hinzu.
- Lange Sequenzen: enthält einen optionalen hierarchischen Video-Sampler.

## Entwicklungslinie {#development-line}

- **2023-05-23 — ControlVideo-GitHub-Repository taucht auf.** Am 2023-05-23 erfassen wir das GitHub-Repository als Einstiegspunkt für den Quellcode des Projekts. Das Datum markiert, wann wir das Repository gesehen haben, nicht seine bestätigte erste Veröffentlichung.
- **2023-07-09 — Hugging-Face-Space-Demo erscheint neben dem Repository.** Am 2023-07-09 nehmen wir die Hugging-Face-Space-Demo neben dem GitHub-Repository auf. Der Link bietet einen interaktiven Demo-Zugang, wobei das genaue Startdatum und die ursprünglichen Funktionen ungeprüft bleiben.

## Was sich geändert hat {#what-changed}

Die ControlVideo-Veröffentlichungen verliefen in Etappen:
- 2023-05-23: das Paper wurde veröffentlicht.
- 2023-05-25: der Quellcode wurde im offiziellen Repository veröffentlicht.
- 2023-05-28: eine Replicate-Demo wurde hinzugefügt.
- 2023-07-09: der fffiloni-Space erschien neben dem offiziellen Repository.
- 2023-07-11: Unterstützung für ControlNet 1.1 wurde hinzugefügt.
- 2023-07-16: der Autor verlinkte eine Hugging-Face-Demo.
- 2026-09-04: der fffiloni-Space ist pausiert, und der vom Autor verlinkte Yabo-Space scheitert mit einem Laufzeitfehler wegen des Speicherlimits. Keiner funktioniert als dokumentierte Browser-Demo.

## Verwendung {#how-to-use-this}

Ab dem 2023-07-09 ControlVideo anhand des Code-Repositorys oder des verlinkten Hugging-Face-Space bewerten und die Kompatibilität lokal prüfen.

1. Eine isolierte Python-3.10-Umgebung anlegen und die gepinnten Anforderungen installieren.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt>
2. Stable Diffusion v1.5, die benötigten ControlNet-Gewichte und die RIFE-FlowNet-Gewichte in die dokumentierten Checkpoint-Pfade herunterladen.
  — <https://github.com/YBYBZhang/ControlVideo>
3. Eine Kondition wählen, die von der Ziel-ControlNet-Version unterstützt wird; für v10 Schlüssel wie depth_midas, canny oder openpose mit passenden Checkpoints übergeben.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
4. Den Referenzbefehl inference.sh mit einem Quellvideo und Prompt ausführen, beginnend mit 15 Bildern und 512×512.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh>
5. --is_long_video erst nach erfolgreichem Kurzlauf ergänzen, um den hierarchischen Sampler für längere Sequenzen zu aktivieren.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>

## Bewährte Praktiken {#best-practices}

- Die gepinnten Abhängigkeiten vor einem Upgrade isolieren. Torch 1.13.1+cu116, Diffusers 0.14.0, Transformers 4.26.1 und xFormers 0.0.16 bilden einen veralteten Stack für Reproduzierbarkeit.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt>
- --condition, --version und Checkpoint-Pfade aufeinander abstimmen. Der Code ordnet v10 und v11 unterschiedlichen Konditionsschlüsseln zu.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- depth_midas statt der generischen depth-Option aus der README angeben. Das Skript inference.sh und die v10-Zuordnung erfordern depth_midas.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh>
- Bildbreite und -höhe durch 32 teilbar halten. Tests mit 15 Bildern und 512×512 beginnen und den Seed festlegen, um Iterationen zu vergleichen.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Die erzeugten Dateien source_video.mp4 und das Konditionsvideo prüfen, bevor die Ausgabequalität bewertet wird. Die Pipeline schreibt beide Dateien vor dem Sampling der Bilder.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Für aktive Arbeit die vom Autor verlinkte Browser-Demo meiden. Der gehostete Space bricht mit einem Laufzeitfehler wegen des Speicherlimits ab.
  — <https://huggingface.co/spaces/Yabo/ControlVideo>

## Dadurch überholt {#superseded-by-this}

- 2023-07-09: Der Betrieb des fffiloni-Hugging-Face-Space ist überholt, da er seit 2026-09-04 pausiert ist.
- 2023-07-16: Der Betrieb des vom Autor verlinkten Yabo-Hugging-Face-Space ist überholt, da er mit einem Laufzeitfehler wegen des Speicherlimits scheitert.
- Das README-Argument --condition depth von 2023 ist auf master überholt. Einen zugeordneten Schlüssel wie depth_midas zusammen mit der passenden --version übergeben.

## Weiterhin unbekannt {#still-unknown}

- Die Kompatibilität jenseits des gepinnten Stacks von 2023 bleibt ungeprüft, da wir keine Tests in einer sauberen CUDA- und Python-Umgebung von 2026 durchgeführt haben.
- Einrichtungsanleitungen auf Vereinfachtem Chinesisch bleiben ungeprüft, da die Recherche keine Dokumentation des Herstellers fand.
- Der ursprüngliche Nachrichtentext vom 2023-07-09 ist nicht verfügbar, daher prüfen wir die erfassten Links statt der ursprünglichen Aussage.
- Das THU-ControlVideo-Projekt unter arXiv:2305.17098 ist eine eigenständige One-Shot-Methode zur Text-zu-Video-Bearbeitung und nicht das hier erfasste trainingsfreie Generierungsprojekt.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://github.com/YBYBZhang/ControlVideo | ControlVideo — offizielle PyTorch-Implementierung | 2026-09-04 |
| https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt | ControlVideo requirements.txt — master | 2026-09-04 |
| https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py | ControlVideo inference.py — master | 2026-09-04 |
| https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh | ControlVideo inference.sh — master | 2026-09-04 |
| https://arxiv.org/abs/2305.13077 | ControlVideo: Training-free Controllable Text-to-Video Generation | 2026-09-04 |
| https://huggingface.co/spaces/fffiloni/ControlVideo | ControlVideo — Hugging-Face-Space von fffiloni | 2026-09-04 |
| https://huggingface.co/spaces/Yabo/ControlVideo | ControlVideo — Hugging-Face-Space von Yabo | 2026-09-04 |
| https://ml.cs.tsinghua.edu.cn/controlvideo/ | ControlVideo: Adding Conditional Control for One Shot Text-to-Video Editing | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:controlvideo`, Thread `controlvideo`, 2 datierte Ereignisse vom 2023-05-23 bis 2023-07-09.
- **Praxishinweis:** Ab dem 2023-07-09 ControlVideo anhand des Code-Repositorys und des Hugging-Face-Space bewerten, lokale Abhängigkeiten aber separat testen.
- **Konfidenz:** mittel. Die oben aufgeführten überholten Punkte kennzeichnen veraltete Wege.
