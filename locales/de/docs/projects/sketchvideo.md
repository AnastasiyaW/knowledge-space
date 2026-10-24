---
title: "SketchVideo"
category: projects
date: 2025-04-07
tags: [project, sketchvideo, sketchvideo-development]
aliases: ["SketchVideo"]
level: 2
source_sha256: 749af09511f387c43fac44e37f26d65b42b9378a852adda5330e333e11f171b3
translation: machine
translated_at: '2026-10-24'
---
# SketchVideo {#sketchvideo}

**Entwicklungslinie:** `project:sketchvideo` · Thread `sketchvideo-development`  
**Letztes Ereignis:** 2025-04-07 · 2 datierte Einträge seit 2023-11-28 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

SketchVideo ist heute kein einzelnes Werkzeug, sondern eine Namenskollision. — Sketch Video Synthesis (2023): optimiert Bézier-Kurven über einem Eingabevideo und exportiert Vektor-SVGs zur Stilisierung, Nachzeichnung und Compositing. — Sketch-based Video Generation and Editing (2025): erzeugt oder bearbeitet ein Video anhand von Text und einer oder zwei Skizzen von Schlüsselbildern. Einschränkung des aktuellen Codes von 2025: bis zu 49 Bilder bei 720×480; für eine A100 geben die Autoren etwa 21 GB/95 s für SketchGen und 23 GB/230 s für SketchEdit an. Fazit: Die Wahl sollte anhand des Repositorys der Autoren getroffen werden, nicht anhand des Namens.

## Entwicklungslinie {#development-line}

- **2023-11-28 — Ressourcen des SketchVideo-Projekts wurden veröffentlicht.** Der veröffentlichte Code optimiert bildweise Bézier-Kurven mit CLIP-Semantik und bildübergreifender Konsistenz und wandelt das Ausgangsvideo in eine SVG-Skizze um.
- **2025-04-07 — Ein späterer SketchVideo-Ressourcensatz wurde verlinkt.** Ein anderes Projekt stellte Code und Gewichte zur Erzeugung und lokalen Bearbeitung von Videos anhand einer oder zweier Schlüsselbild-Skizzen auf Basis von CogVideo-2b bereit.

## Was sich geändert hat {#what-changed}

2023-11-28 — Sketch Video Synthesis: Der veröffentlichte Code optimiert bildweise Bézier-Kurven mit CLIP-Semantik und bildübergreifender Konsistenz und wandelt das Ausgangsvideo in eine SVG-Skizze um. 2025-04-07 — SketchVideo: Ein anderes Projekt stellte Code und Gewichte zur Erzeugung und lokalen Bearbeitung von Videos anhand einer oder zweier Schlüsselbild-Skizzen auf Basis von CogVideo-2b bereit.

Keiner dieser Schritte ist ein Update des anderen: Es handelt sich um zwei verschiedene Projekte mit demselben Namen.

## Wie man das nutzt {#how-to-use-this}

Stand 2025-04-07 sollten Praktiker die später verlinkten Ressourcen von geometrylearning.com und IGLICT mit den Projektressourcen von 2023 vergleichen, bevor sie eine SketchVideo-Implementierung auswählen.

1. Für das generative Projekt legen Sie eine Python-3.10-Umgebung an und installieren die Abhängigkeiten; das Repository setzt diffusers==0.30.1 voraus.
  — <https://github.com/IGLICT/SketchVideo>
2. Laden Sie die Gewichte von SketchGen oder SketchEdit sowie das Basismodell CogVideo-2b herunter und tragen Sie die Pfade dazu in den Skripten oder in config.py ein.
  — <https://github.com/IGLICT/SketchVideo>
3. Für die Generierung bereiten Sie eine Skizze mit 720×480 auf einem oder zwei Bildern vor und starten test_sketch_gen_single.sh oder test_sketch_gen_two.sh.
  — <https://github.com/IGLICT/SketchVideo>
4. Für die Bearbeitung bereiten Sie ein 49-Bild-Video mit 720×480, eine Skizze des Schlüsselbilds und Masken der zu bearbeitenden Bereiche vor und starten test_sketch_edit.sh.
  — <https://github.com/IGLICT/SketchVideo>
5. Für die Vektorisierung von Videos verwenden Sie das separate Repository von 2023: installieren Sie die Abhängigkeiten, bereiten Sie einen Clip mit weniger als 70 Bildern und Masken vor, erstellen Sie den Atlas und führen Sie operate_clipavideo.sh aus.
  — <https://github.com/yudianzheng/SketchVideo>

## Bewährte Vorgehensweisen {#best-practices}

- Mischen Sie Gewichte, Anleitungen und Ergebnisse der beiden Repositorys nicht: Autoren, Aufgaben und Pipelines sind verschieden.
  — <https://github.com/yudianzheng/SketchVideo>
- Für SketchVideo 2025 beginnen Sie mit einer oder zwei Schlüsselbild-Skizzen in exakt 720×480; für die Bearbeitung muss der Eingabeclip 49 Bilder enthalten.
  — <https://github.com/IGLICT/SketchVideo>
- Wenn das Ergebnis des generativen Projekts instabil ist, probieren Sie andere Seeds aus; die Autoren garantieren den Erfolg bei jedem Lauf ausdrücklich nicht. Weniger DDIM-Schritte verkürzen die Inferenzzeit.
  — <https://github.com/IGLICT/SketchVideo>
- Für das Projekt von 2023 beschränken Sie den Eingabeclip auf weniger als 70 Bilder und bereiten Masken des Vordergrundobjekts vor, bevor Sie den Atlas erstellen.
  — <https://github.com/yudianzheng/SketchVideo>

## Hiermit ersetzt {#superseded-by-this}

- 2025-04-07: Die Annahme, dass IGLICT/SketchVideo eine neue Version von yudianzheng/SketchVideo ist, ist falsch; es handelt sich um ein unabhängiges CVPR-2025-Projekt.
- 2025-04-01: Für die Aufgabe der Erzeugung oder Bearbeitung anhand einer Skizze ist IGLICT/SketchVideo mit den Gewichten einschlägig; es ersetzt jedoch nicht die SVG-Vektorisierung aus dem Projekt von 2023.

## Weiterhin unbekannt {#still-unknown}

- Die Seite http://geometrylearning.com/SketchVideo/ war bei der Prüfung nicht erreichbar, daher wurde ihr Inhalt nicht verwendet.
- Es gibt keine Belege für eine gemeinsame Codebasis, ein gemeinsames Team oder eine Nachfolge zwischen den Repositorys von 2023 und 2025; sie sind als zwei getrennte subject_key zu führen.
- event_findings: 2023-11-28 — Das arXiv-Primärdokument vom 2023-11-26 nennt die Autoren (Yudian Zheng, Xiaodong Cun, Menghan Xia, Chi-Man Pun) und präzisiert, dass die Methode Bézier-Kurven mit einem CLIP-semantischen Verlust und einem atlasbasierten Konsistenzverlust optimiert; Quelle https://arxiv.org/abs/2311.15306.
- event_findings: 2025-04-07 — Das Repository präzisiert die Namen der Gewichte von SketchGen und SketchEdit, die Basis CogVideo-2b und die Grenze von 49 Bildern bei 720×480; das README datiert die Veröffentlichung von Code und Gewichten auf 2025-04-01; Quelle https://github.com/IGLICT/SketchVideo.
- new_events: 2023-11-26 — arXiv-Preprint Sketch Video Synthesis veröffentlicht; Quelle https://arxiv.org/abs/2311.15306.
- new_events: 2025-03-30 — Für das unabhängige SketchVideo wurde eine Projektseite gestartet und der arXiv-Preprint aktualisiert; Quelle https://github.com/IGLICT/SketchVideo.
- new_events: 2025-04-01 — Für das unabhängige SketchVideo wurden Code und Gewichte veröffentlicht; Quelle https://github.com/IGLICT/SketchVideo.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/yudianzheng/SketchVideo | yudianzheng/SketchVideo — Sketch Video Synthesis | 2026-09-05 |
| https://sketchvideo.github.io/ | Sketch Video Synthesis project page | 2026-09-05 |
| https://arxiv.org/abs/2311.15306 | Sketch Video Synthesis | 2026-09-05 |
| https://github.com/IGLICT/SketchVideo | IGLICT/SketchVideo — Sketch-based Video Generation and Editing | 2026-09-05 |
| https://arxiv.org/abs/2503.23284 | SketchVideo: Sketch-based Video Generation and Editing | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Subjekt:** `project:sketchvideo`, Thread `sketchvideo-development`, 2 datierte Ereignisse 2023-11-28 → 2025-04-07.
- **Praktischer Hinweis:** Stand 2025-04-07 sollten Praktiker die später verlinkten Ressourcen von geometrylearning.com und IGLICT mit den Projektressourcen von 2023 vergleichen, bevor sie eine SketchVideo-Implementierung auswählen.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
