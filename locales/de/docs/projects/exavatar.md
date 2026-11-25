---
title: "ExAvatar"
category: projects
date: 2024-09-26
tags: [exavatar, exavatar-development, project]
aliases: ["ExAvatar"]
level: 3
source_sha256: 240e0e756c9d7eee2296d025c679d5cea8769177ba81658b26007e521ee47891
translation: machine
translated_at: '2026-10-24'
---
# ExAvatar {#exavatar}

**Entwicklungslinie:** `project:exavatar` · Thread `exavatar-development`  
**Letztes Ereignis:** 2024-09-26 · 2 datierte Einträge seit 2024-08-01 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

ExAvatar ist eine Forschungspipeline für Grafik- und Avatar-Praktiker, die Körper-, Hand- und Gesichtsausdruckssteuerung aus einem monokularen Handyvideo einer einzelnen Person benötigen, anstelle der 3D-Scan-/RGB-D-Eingabe von X-Avatar.

- SMPL-X- und FLAME-Fitting: passt die Modelle an die Aufnahme an.
- 3D-Gaussian-Avatar: trainiert auf Basis der angepassten Aufnahme.
- View Synthesis: rendert neuartige Körper- und Handposen, Gesichtsausdrücke und Blickwinkel.

Das Projekt demonstriert einen etwa 10-sekündigen Handy-Scan in neutraler Pose. Nicht gesehene Mundinnenräume, Handflächen und dynamische Kleidung können fehlschlagen. Wir verwenden es für kontrollierte Offline-Avatar-Forschung, wenn der SMPL-X-Fitting-Stack akzeptabel ist. Wir verwenden es nicht dort, wo Kleidungsverformung oder nicht gesehene Anatomie zuverlässig abgebildet werden müssen.

## Entwicklungslinie {#development-line}

- **2024-08-01 — ExAvatar-Projektwebseite geteilt.** Am 2024-08-01 wurde ExAvatar über seine Projektwebseite als öffentliche Projektreferenz geteilt.
- **2024-09-26 — ExAvatar-Release-Repository geteilt.** Am 2024-09-26 veröffentlichte ExAvatar ein eigenes GitHub-Release-Repository, um eine releaseorientierte Quelle neben der früheren Projektwebseite bereitzustellen.

## Was sich geändert hat {#what-changed}

2024-08-01 — ExAvatar erschien als ECCV-2024-Methode, die SMPL-X mit 3D Gaussian Splatting kombiniert, um aus einem kurzen Handy-Scan einen steuerbaren Körper-, Hand- und Gesichtsavatar zu erzeugen.

2024-09-26 — ExAvatar_RELEASE stellte die offizielle PyTorch-Neuimplementierung mit öffentlichen Assets und dokumentierten Pfaden für Fitting, Training, Testing und Animation bereit.

2026-09-04 — Das offizielle Repository und die Dokumentation bleiben öffentlich, aber GitHub listet keine paketierten Releases oder Release Notes. Reproduzierbare Nutzung sollte einen gewählten Commit festhalten.

## Anwendung {#how-to-use-this}

Stand 2024-09-26 sollte man für releaseorientierte Projektmaterialien das ExAvatar-Release-Repository konsultieren, anstatt sich nur auf die am 2024-08-01 geteilte Projektwebseite zu verlassen.

1. Die Conda-Umgebung in einem ExAvatar_RELEASE-Checkout erstellen: `conda env create -f environment.yml`, danach `conda activate exavatar`.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/README.md>
2. Die Voraussetzungen für das Fitting installieren: SMPL-X 1.1, FLAME, DECA, Hand4Whole, MMPose, Segment Anything, Depth Anything V2 und COLMAP; die Anpassungen im Repository über `copy_code.py` ausführen.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
3. Das Video einer Person unter `data/Custom/data/$SUBJECT_ID/video.mp4` ablegen, Frames extrahieren, Listen für alle/Training/Test-Frames erstellen, `dataset = 'Custom'` setzen und dann SMPL-X mit dem dokumentierten Kameramodus anpassen.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
4. Vordergrundmasken erzeugen, eine Hintergrund-Punktwolke nur für einen statischen Hintergrund erstellen, mit `main/train.py` trainieren und die Rekonstruktionsausgabe mit `test.py` prüfen.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>
5. Für einen unter `output/model_dump/$SUBJECT_ID` exportierten Avatar SMPL-X-Ansteuerungsparameter bereitstellen und `animation.py` ausführen; für ein rotierendes Kamera-Rendering `animate_view_rot.py` verwenden.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>

## Best Practices {#best-practices}

- Im Freien oder anderweitig starke Beleuchtung und harte Schatten vermeiden; den Vorverarbeitungspfad für statischen oder dynamischen Hintergrund entsprechend wählen.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>
- Fitting-Frames verwenden, in denen die Person größtenteils sichtbar und nicht abgeschnitten ist; etwa 5 fps aus 30 fps abzutasten ist der dokumentierte, geschwindigkeitsorientierte Ausgangspunkt.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
- COLMAP für eine bewegte Kamera verwenden; den Pfad der virtuellen Kamera für eine statische Aufnahme oder SMPL-X-Parameterextraktion.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
- Wenn das Gesichts-Fitting sich verschlechtert, `flame_init/renders` prüfen und sicherstellen, dass DECA-Ergebnisse vorbereitet waren, bevor die Pipeline erneut ausgeführt wird.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
- Die Identitätsparameter für SMPL-X-Shape, Joint-Offset und Face-Offset zwischen Training und Evaluation identisch halten.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>

## Hierdurch ersetzt {#superseded-by-this}

- 2024-09-26 — Für die Implementierung ersetzen das öffentliche ExAvatar_RELEASE-Repository und seine READMEs zu Fitting und Avatar die Vorabversions- oder reine Projektseiten-Anleitung.

## Weiterhin unbekannt {#still-unknown}

- Das Repository hat kein GitHub-Release-Paket, und die geprüften Quellen nennen weder ein aktuelles VRAM-Ziel noch eine Erwartung an die Trainingszeit oder eine unterstützte CUDA-/Treiber-Matrix.
- Keine geprüfte Quelle aus erster Hand erklärt ExAvatar für veraltet oder benennt einen offiziellen Nachfolger.
- Es wurde kein reproduzierbarer chinesischsprachiger Betriebsbericht und kein unabhängiges Community-Hardware-Rezept gefunden; die aufgeführten Praktiken sind Leitlinien der Maintainer.
- Der Permalink der Quelle vom 2024-09-26 konnte nicht abgerufen werden und wurde nicht als Beleg verwendet.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://mks0601.github.io/ExAvatar/ | ExAvatar-Projektseite | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE | ExAvatar_RELEASE offizielles Repository | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/blob/main/README.md | ExAvatar_RELEASE README | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md | Fitting von SMPL-X an ein monokulares Video | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md | Erstellen eines Avatars aus einem Handy-Scan | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/releases | ExAvatar_RELEASE GitHub Releases | 2026-09-04 |
| https://arxiv.org/abs/2407.21686 | Expressive Whole-Body 3D Gaussian Avatar | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:exavatar`, Thread `exavatar-development`, 2 datierte Ereignisse 2024-08-01 → 2024-09-26.
- **Praktischer Hinweis:** Stand 2024-09-26 sollten Praktiker für releaseorientierte Projektmaterialien das ExAvatar-Release-Repository konsultieren, anstatt sich nur auf die am 2024-08-01 geteilte Projektwebseite zu verlassen.
- **Konfidenz:** mittel. Die datierten Hinweise zu Ersetzungen sind maßgeblich dafür, was veraltet ist.
