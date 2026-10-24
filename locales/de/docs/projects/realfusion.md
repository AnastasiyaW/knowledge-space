---
title: "RealFusion"
category: projects
date: 2023-03-03
tags: [code_release, project, realfusion, realfusion-development]
aliases: ["RealFusion"]
level: 2
source_sha256: 0ce5d87fa10dbce7431800b2a42b955434b705c345eda904d599aeea75515881
translation: machine
translated_at: '2026-10-24'
---
# RealFusion {#realfusion}

**Entwicklungslinie:** `project:realfusion` · Thread `realfusion-development`  
**Letztes Ereignis:** 2023-03-03 · 1 datiertes Ereignis seit 2023-03-03 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

RealFusion rekonstruiert aus einem maskierten Bild ein plausibles 360-Grad-Objekt, indem es Single-Image-Textual-Inversion, Score Distillation mit Stable Diffusion und ein NeRF im Stil von Instant-NGP kombiniert.

- Token-Inversion: lernt ein bildspezifisches Token
- Strahlungsfeld (Radiance Field): optimiert gegen das Eingabebild und den Diffusions-Prior
- Mesh-Export: exportiert optional ein texturiertes Mesh

Nicht gesehene Geometrie wird geschätzt, nicht rekonstruiert; fehlgeschlagene Konvergenz und Janus-artige, doppelt dargestellte Gesichter bleiben dokumentierte Fehlerbilder.

Verwenden Sie es als Reproduzierbarkeits-Baseline oder als abstimmbaren Forschungsworkflow, nicht als aktuelles schlüsselfertiges Bild-zu-3D-Produkt.

## Entwicklungslinie {#development-line}

- **2023-03-03 — RealFusion-Code und Projektressourcen verlinkt.** Am 2023-03-03 hat die RealFusion-Entwicklungslinie einen Code-Release-Eintrag mit Links zur öffentlichen Projektseite und zum GitHub-Repository erfasst. Damit ist ein datierter öffentlicher Referenzpunkt festgelegt; eine Version, ein Commit oder eine konkrete technische Änderung wird jedoch nicht genannt.

## Was sich geändert hat {#what-changed}

2023-03-03 — Die öffentliche Projektseite und das Code-Release von RealFusion machten den Workflow aus Single-Image-Textual-Inversion und NeRF außerhalb der Paper-Implementierung lauffähig. 2023-04-08 — Die spätere Referenz verweist auf das Release vom 2023-03-03; aus diesem Link ergibt sich kein eigenständiges RealFusion-Code-, Modell- oder Methoden-Update.

## So verwenden Sie es {#how-to-use-this}

Ab dem 2023-03-03 konnten Praktiker die datierten Links zur RealFusion-Projektseite und zum Repository als Ausgangspunkt nutzen, um die öffentlich referenzierten Code-Release-Ressourcen zu finden.

1. Installieren Sie die Python-Abhängigkeiten, PyTorch separat und die CUDA-Erweiterungen; installieren Sie nvdiffrast nur, wenn Sie ein texturiertes Mesh exportieren.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
2. Bereiten Sie ein quadratisches RGBA-Bild mit dem Objekt und der Maske vor; verwenden Sie das mitgelieferte Skript zur Maskenextraktion, wenn Sie von einem unmaskierten Bild ausgehen.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
3. Führen Sie Single-Image-Textual-Inversion mit Stable Diffusion v1.5 aus, um das gelernte Objekt-Embedding zu erzeugen.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
4. Starten Sie die Rekonstruktion mit `python main.py --O`, dem RGBA-Bild, dem gelernten Embedding und dem passenden Stable-Diffusion-Checkpoint.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
5. Prüfen Sie neue Ansichten und passen Sie Kamerapose, Kamera-Radien, Verlustfunktionen und Zufallsseeds für das jeweilige Bild an, bevor Sie ein Ergebnis übernehmen.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>

## Bewährte Verfahren {#best-practices}

- Beginnen Sie mit einem sauber maskierten Objektbild; der dokumentierte Eingabevertrag ist ein quadratisches RGBA-Bild.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Verwenden Sie `--O`: Das Repository gibt an, dass sein CUDA-Raymarching-Pfad mit diesem Optimierungspaket entwickelt und getestet wurde.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Stimmen Sie `pose_angle` auf den Kamerablickwinkel ab und setzen Sie `radius_rot` leicht über das Maximum des Trainingsradius.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Führen Sie mehrere Seeds aus und wählen Sie die Ergebnisse nach Prüfung aus; die Standardparameter sind ausdrücklich nicht für jedes Beispiel gleich gut geeignet.
  — <https://github.com/lukemelas/realfusion/blob/main/README.md>
- Behandeln Sie Rückseiten als plausible Extrapolationen und verwerfen Sie transparente Felder, Floater, falsche Geometrie oder doppelt dargestellte Flächen, statt sie als rekonstruierte Geometrie darzustellen.
  — <https://arxiv.org/abs/2302.10663>

## Hierdurch ersetzt {#superseded-by-this}

- 2023-03-03 — Das überarbeitete Release des öffentlichen Repositorys ersetzte die Abhängigkeit von den ursprünglichen Implementierungsdetails des Papers; der Maintainer erklärt, dass sich Teile vom Paper-Code unterscheiden.
- 2023-04-08 — Die Behandlung der späteren Referenz als eigenständiges Release ist überholt: Sie verweist auf den früheren Eintrag vom 2023-03-03, statt ein neues Release zu dokumentieren.

## Weiterhin unbekannt {#still-unknown}

- Für die Referenz vom 2023-04-08 wurde keine datierte Ankündigung des Erstanbieters zu einem Release, Checkpoint, Kompatibilitätstest oder Nachfolgemethode gefunden; sie wirkt wie ein nachträglicher Verweis auf den früheren Eintrag und nicht wie ein eigener Entwicklungsschritt.
- Das aktuelle Repository beschreibt einen CUDA-abhängigen Forschungsworkflow, belegt aber nicht die Kompatibilität mit aktuellen Versionen von PyTorch, CUDA, Diffusers oder dem Stable-Diffusion-Ökosystem.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://lukemelas.github.io/realfusion/ | RealFusion-Projektseite | 2026-09-05 |
| https://github.com/lukemelas/realfusion | lukemelas/realfusion | 2026-09-05 |
| https://github.com/lukemelas/realfusion/blob/main/README.md | RealFusion-README | 2026-09-05 |
| https://arxiv.org/abs/2302.10663 | RealFusion: 360° Reconstruction of Any Object from a Single Image | 2026-09-05 |
| https://cvpr.thecvf.com/virtual/2023/poster/21294 | CVPR 2023 poster: RealFusion: 360° Reconstruction of Any Object From a Single Image | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:realfusion`, Thread `realfusion-development`, 1 datiertes Ereignis vom 2023-03-03 bis 2023-03-03.
- **Praktischer Hinweis:** Ab dem 2023-03-03 konnten Praktiker die datierten Links zur RealFusion-Projektseite und zum Repository als Ausgangspunkt nutzen, um die öffentlich referenzierten Code-Release-Ressourcen zu finden.
- **Konfidenz:** hoch. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
