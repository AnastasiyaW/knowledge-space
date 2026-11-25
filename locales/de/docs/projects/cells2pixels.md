---
title: "Cells2Pixels"
category: projects

tags: [cells2pixels, cells2pixels-development, project]
aliases: ["Cells2Pixels"]
level: 2
source_sha256: feaebfd250a4132359d5cfe06dbfadee738fce14323d5c2ab9f88a51885acbe3
translation: machine
translated_at: '2026-10-24'
---
# Cells2Pixels {#cells2pixels}

**Entwicklungslinie:** `project:cells2pixels` · Thread `cells2pixels-development`  
**Letztes Ereignis:** - · 0 datierte seitdem · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Cells2Pixels ist der Code und die interaktive Demo zu Neural Cellular Automata: From Cells to Pixels für Forschende im Bereich generativer Grafik.

- NCA und Local Pattern Producing Network (LPPN) werden gemeinsam trainiert.
- Die Kernmodi umfassen 2D-Morphogenese, PBR-Texturen, Texturen auf Meshes und 3D-Texturen.
- Die experimentellen Modi umfassen dynamische Texturen, Radiance Field und Voxel-Wachstum.

Das Repository ist für das Training gedacht, es gibt kein paketiertes Release und kein fertiges Colab. Das README führt Colab und Tests noch als TODO-Punkte auf. Es eignet sich für reproduzierbare NCA-Experimente, nicht für die Produktion von Bildern.

## Entwicklungslinie {#development-line}

- Die datierte Linie ist noch nicht ausgearbeitet; das Bekannte steht in den Abschnitten unten.

## Was sich geändert hat {#what-changed}

2026-07-11 — Cells2Pixels erschien als Implementierung zur SIGGRAPH 2026. Ein grobes zelluläres Gitter entwickelt sich durch lokale Updates. Das LPPN dekodiert interpolierte Zellzustände und lokale Koordinaten in Bilder oder Oberflächeneigenschaften beliebiger Auflösung.

## Wie man das verwendet {#how-to-use-this}

Stand 2026-07-11 ist Cells2Pixels als Projekt zu behandeln, das eine Prüfung der Quellen über die Website und das Repository erfordert; allein aus den datierten Links ergibt sich keine Änderung des Arbeitsablaufs für Praktiker.

1. Abhängigkeiten mit `pip install -r requirements.txt` installieren. Kaolin ist für Läufe ohne Meshes optional.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
2. Datensätze und Eingabeverzeichnisstrukturen mit `python scripts/download_data.py` herunterladen.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
3. Training mit `python train.py --config <path>` starten. Für 2D-Wachstum mit `configs/nca2d/growing.yaml` beginnen, für PBR mit `configs/nca2d/pbr_texture.yaml`, für Meshes mit `configs/meshnca/texture.yaml` oder für 3D mit `configs/nca3d/3d_texture.yaml`.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
4. Nach dem Training `--test` übergeben, um den Checkpoint zu laden und Bilder sowie Rollout-Videos im konfigurierten Ausgabeverzeichnis zu speichern.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
5. Das Modellverhalten in der interaktiven Zeichenfläche testen, indem man einen Modus wählt, die LPPN-Skalierung anpasst und auf das NCA klickt oder es berührt.
  — <https://cells2pixels.github.io/>

## Bewährte Vorgehensweisen {#best-practices}

- PyTorch- und Kaolin-Versionen an die requirements anpassen. Kaolin wird nur für Mesh-Rendering und Rasterisierung benötigt.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
- Dynamische Textur, Wachstum im Radiance Field oder Voxel-Wachstum nicht als Ergebnisse aus dem Paper darstellen. Das README trennt diese experimentellen Modi von den vier Trainingsmodi aus dem Paper.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
- Modelle anhand eines gespeicherten Checkpoints und eines expliziten Test-Rollouts bewerten, statt sich allein auf den Trainingslauf zu verlassen.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>

## Durch dies ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Die Projektseite und das README enthalten kein datiertes Repository-Changelog, daher lassen sich Veröffentlichungsdaten für Code, Demos und einzelne Konfigurationen nicht verifizieren.
- Es gibt kein bestätigtes paketiertes Release, keinen Katalog von Checkpoints und keinen unterstützten Produktionsworkflow.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://cells2pixels.github.io/ | Neural Cellular Automata: From Cells to Pixels | 2026-09-05 |
| https://github.com/TheDevilWillBeBee/Cells2Pixels | TheDevilWillBeBee/Cells2Pixels — offizielle Implementierung | 2026-09-05 |
| https://arxiv.org/abs/2506.22899 | Neural Cellular Automata: From Cells to Pixels | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:cells2pixels`, Thread `cells2pixels-development`, 0 datierte Ereignisse - → -.
- **Praktischer Hinweis:** Stand 2026-07-11 ist Cells2Pixels als Projekt zu behandeln, das eine Prüfung der Quellen über die Website und das Repository erfordert; allein aus den datierten Links ergibt sich keine Änderung des Arbeitsablaufs für Praktiker.
- **Konfidenz:** hoch. Datierte Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.
