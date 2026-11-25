---
title: "F⁴Splat"
category: projects
tags: [f4splat, f4splat-development, project]
aliases: ["F⁴Splat"]
level: 2
source_sha256: 3e67e3562f2422099d822c54795715b6bb2ca32836a1311db89e47d14402df9b
translation: machine
translated_at: '2026-10-24'
---
# F⁴Splat {#f4splat}

**Entwicklungslinie:** `project:f4splat` · Thread `f4splat-development`  
**Ereignisse:** 2 datiert, 2026-03-30 → 2026-07-24 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

F⁴Splat ist ein 3DGS-Forschungsframework für Entwickler, das aus wenigen, nicht kalibrierten Bildern neue Ansichten synthetisiert. Es ist eine Code-Alternative zu AnySplat für CUDA-Forschung und kein fertiger Cloud-Dienst oder universeller 3D-Scanner.

- Kamera- und Parametervorhersage: sagt Kameraposen, Gaussian-Parameter und Score-Karten für die Verdichtung (Densification) voraus.
- Primitivzuweisung: verteilt Gaussian-Primitive nach Szenenkomplexität und Überlappungen zwischen Ansichten.
- Budgetskalierung: ändert das Ziel-Gaussian-Budget zur Inferenzzeit, ohne neu trainieren zu müssen.

Die lokale Demo nimmt 2–16 Bilder entgegen; die veröffentlichten Gewichte decken ACID 2-View sowie RealEstate10K 2- und 24-View ab.

## Entwicklungslinie {#development-line}

- **2026-03-30 — Projektseite zu F⁴Splat veröffentlicht.** F⁴Splat erschien am 2026-03-30 auf der öffentlichen Projektseite. Ein Verweis auf Level-of-Detail-Grafik rahmte die Ankündigung im Kontext der Rendering-Entwicklung. Die Seite enthielt keine exakten technischen Aussagen und keinen Angaben zum Release-Status.
- **2026-07-24 — GitHub-Repository zu F⁴Splat verlinkt.** Die Entwicklungslinie verlinkte das F⁴Splat-GitHub-Repository am 2026-07-24 zusammen mit der Ankündigung vom März. Damit wurde öffentlicher Zugriff auf den Quellcode eröffnet. Der Beitrag nannte nicht, welcher Code, welche Version oder welche Implementierungsänderungen an diesem Datum erschienen.

## Was sich geändert hat {#what-changed}

- **2026-03-30:** Die Projektseite beschrieb die Methode. Statt einer gleichmäßigen Verteilung von Pixeln oder Voxeln auf Gaussians weist das Modell Primitive anhand der vorhergesagten Dichte zu.
- **2026-06-30:** Der offizielle Commit „Release public code“ (dt. etwa „Öffentlichen Code veröffentlichen“) fügte 181 Dateien mit Demo, Training, Evaluation und Quellcode hinzu. Die Methode wurde dadurch zu einem reproduzierbaren lokalen Workflow.
- **2026-07-24:** Der Link verwies auf das offizielle Repository, aber die Quelle verzeichnete an diesem Tag keine eigenständige technische Änderung. Die nächstgelegene bestätigte Code-Veröffentlichung bleibt der 30. Juni.
- **2026-09-03:** Das arXiv-Paper wurde auf v3 aktualisiert. Die Seite beschreibt die Unterschiede nicht, daher können wir für diese Revision keine neuen Funktionen oder geänderten Ergebnisse belegen.

## So nutzt man es {#how-to-use-this}

Stand 2026-07-24: Für Kontext die F⁴Splat-Projektseite konsultieren und für den Quellcode das verlinkte GitHub-Repository. Genaue Fähigkeiten und Versionsstände als ungeprüft behandeln, bis die Recherche sie bestätigt.

1. Repository klonen, eine Python-3.11-Umgebung anlegen, PyTorch 2.8.0 für CUDA 12.8 installieren und die Projektabhängigkeiten installieren.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
2. Den Hub-Checkpoint herunterladen, der zum Zieldatensatz und zur Anzahl der Kontextansichten passt: `acid-2view`, `re10k-2view` oder `re10k-24view`.
  — <https://huggingface.co/Knowing/F4Splat>
3. `python demo/app.py` ausführen, 2–16 Bilder hochladen und ein Gaussian-Budget auswählen, um Renderings zu vergleichen.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
4. Für Experimente den Datensatz im PyTorch-Chunk-Format mit `index.json` vorbereiten und anschließend die mitgelieferten Trainings- oder Evaluationsskripte mit GPU-ID und Checkpoint-Pfad ausführen.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>

## Bewährte Vorgehensweisen {#best-practices}

- Zuerst das PyTorch-Wheel an die installierte CUDA-Version anpassen. Falls CUDA nicht 12.8 ist, das passende PyTorch vor allen anderen Abhängigkeiten installieren.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
- Checkpoints nach Datensatz und Anzahl der Kontextansichten wählen. Veröffentlichte Gewichte nicht als universelles Modell für beliebige Szenen behandeln.
  — <https://huggingface.co/Knowing/F4Splat>
- Das Gaussian-Budget anhand der tatsächlichen Primitivanzahl bewerten. Die Demo rendert nur Interpolationsvideos und kennzeichnet Ergebnisse mit den tatsächlichen Gaussian-Anzahlen in Tausend.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>
- Beim Training die Lizenz- und Zugriffsbedingungen für RealEstate10K, DL3DV und ACID einhalten.
  — <https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md>

## Abgelöst durch diese Einträge {#superseded-by-this}

- 2026-06-30: F⁴Splat ausschließlich als Paper oder Projektseite zu behandeln, ist veraltet. Offizieller Quellcode mit Demo-, Trainings- und Evaluationsskripten ist verfügbar.
- 2026-09-03: Für aktuelle Forschungszitate arXiv v3 statt v1/v2 angeben. Diese Revision belegt keine Änderungen der Laufzeitfähigkeiten.

## Weiterhin unbekannt {#still-unknown}

- Der Primärquelltext war nicht lesbar, daher wurde eine eventuelle eigenständige Release-Aussage für 2026-07-24 nicht erfasst.
- Das arXiv-v3-Preprint vom 2026-09-03 enthält keine Änderungsnotiz, daher sind die Unterschiede zu v1/v2 nicht bestätigt.
- Offizielle Materialien enthalten keine unabhängige Qualitätsbewertung mit eigenen Aufnahmen, keine Laufzeitgeschwindigkeit und keinen GPU-Speicherverbrauch.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://mlvlab.github.io/F4Splat/ | F⁴Splat | 2026-09-04 |
| https://github.com/mlvlab/F4Splat | mlvlab/F4Splat | 2026-09-04 |
| https://github.com/mlvlab/F4Splat/commits/main | Commits · mlvlab/F4Splat | 2026-09-04 |
| https://github.com/mlvlab/F4Splat/commit/127ed096c1ab7c4aa65431dc659bc08592adbb22 | Öffentlichen Code veröffentlichen · mlvlab/F4Splat@127ed09 | 2026-09-04 |
| https://raw.githubusercontent.com/mlvlab/F4Splat/main/README.md | F4Splat-README | 2026-09-04 |
| https://huggingface.co/Knowing/F4Splat | Knowing/F4Splat | 2026-09-04 |
| https://arxiv.org/abs/2603.21304 | F4Splat: Feed-Forward Predictive Densification for Feed-Forward 3D Gaussian Splatting | 2026-09-04 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:f4splat`, Thread `f4splat-development`, 2 datierte Ereignisse 2026-03-30 → 2026-07-24.
- **Praktischer Hinweis:** Stand 2026-07-24 für Kontext die F⁴Splat-Projektseite und für den Quellcode das verlinkte GitHub-Repository konsultieren. Genaue Fähigkeiten und Versionsstände bleiben bis zur Recherche ungeprüft.
- **Konfidenz:** mittel. Die datierten Abl­ösungen oben sind maßgeblich dafür, was veraltet ist.
