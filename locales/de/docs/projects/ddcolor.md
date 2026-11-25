---
title: "DDColor"
category: projects
date: 2024-01-15
tags: [ddcolor, ddcolor-development, project]
aliases: ["DDColor"]
level: 3
source_sha256: ced4ea966cacc4b53f8d393c47057eaf4a8f7fc032baadb50f563500edfe5db2
translation: machine
translated_at: '2026-10-24'
---
# DDColor {#ddcolor}

**Entwicklungslinie:** `project:ddcolor` · Thread `ddcolor-development`  
**Letztes Ereignis:** 2024-01-15 · 1 datierter Eintrag seit 2024-01-15 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

DDColor ist ein PyTorch-Modell von ICCV 2023 zur automatischen Kolorierung von Fotos.

- Monochrome Fotos: werden automatisch koloriert.
- Graustufenkanäle: bestehende Farbbilder werden aus diesen neu eingefärbt.
- Deployment: läuft über lokale Skripte, Hugging Face, ModelScope, Gradio oder ONNX-Export.

## Entwicklungslinie {#development-line}

- **2024-01-15 — Quell-Repository von DDColor und Colab-Workflow wurden verknüpft.** Camenduru veröffentlichte Colab- und Gradio-Colab-Notebooks, die auf den kanonischen DDColor-Code verweisen. Dabei handelte es sich um einen Community-Wrapper, nicht um eine Veröffentlichung des Kernmodells.

## Was sich geändert hat {#what-changed}

Die beiden Wege vom Januar 2024 waren Wrapper um dasselbe Modell, gefolgt von offiziellen Inferenzoptionen.

- 2024-01-15: Camenduru veröffentlichte Colab- und Gradio-Colab-Notebooks, die auf den kanonischen DDColor-Code verweisen, als Community-Wrapper und nicht als Veröffentlichung des Kernmodells.
- 2024-01-22: Der Old Photo Restoration Space von ModelScope verwendete `iic/cv_ddcolor_image-colorization` hinter einer Oberfläche mit Upload und Schieberegler. Damit wurde eine DDColor-Integration bestätigt und kein eigenständiges Restaurierungsmodell.
- Offizielle Updates brachten am 2024-01-26 die Hugging-Face-Integration, am 2024-01-29 einen Fix, am 2024-10-25 Unterstützung für den ONNX-Export, am 2024-12-31 ein Refactoring der lokalen Inferenz ohne BasicSR und am 2026-01-17 ein gestrafftes Laden und Ausführen der Inferenz.

## Verwendung {#how-to-use-this}

Wir können seit 2024-01-15 mit DDColor über das Quell-Repository und seinen Colab-Workflow arbeiten. Prüfe den unterstützten Workflow in diesen Ressourcen, bevor du ihn ausführst.

1. Lege die dokumentierte Python-3.9-Umgebung an und installiere danach PyTorch 2.2.0 mit CUDA 11.8 sowie `requirements.txt`. Die lokale Inferenz benötigt kein BasicSR.
  — <https://github.com/piddnad/DDColor>
2. Beginne mit `ddcolor_modelscope` für gewöhnliche Bilder außerhalb von ImageNet. Verwende `ddcolor_paper` nur zur Reproduktion des Papers, `ddcolor_artistic` für ein alternatives Ergebnis oder `ddcolor_paper_tiny`, wenn der Ressourcenbedarf entscheidend ist.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
3. Führe `python scripts/infer.py --model_name ddcolor_modelscope --input ./assets/test_images` aus. Alternativ lädst du den ModelScope-Checkpoint herunter und übergibst seine `pytorch_model.pt` über `--model_path`.
  — <https://github.com/piddnad/DDColor>
4. Für die Python-Integration erstellst du eine ModelScope-Pipeline `Tasks.image_colorization` mit `iic/cv_ddcolor_image-colorization`, übergibst ein Bild und speicherst `OutputKeys.OUTPUT_IMG`.
  — <https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary>
5. Führe `python demo/gradio_app.py` lokal aus, wenn eine Upload-Oberfläche benötigt wird.
  — <https://github.com/piddnad/DDColor>

## Best Practices {#best-practices}

- Verwende standardmäßig `ddcolor_modelscope` für Bilder außerhalb von ImageNet. Das Paper-Modell sollte der Reproduktion vorbehalten bleiben und nicht für den allgemeinen Einsatz genutzt werden.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
- Vergleiche `ddcolor_artistic`, wenn Farbartefakte ein Problem sind, da beim Training auf einen Colorfulness-Verlust verzichtet wurde. Verwende `ddcolor_paper_tiny`, wenn der Ressourcenbedarf entscheidend ist.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
- Prüfe Comics, Eingaben mit niedriger Auflösung und verrauschte Bilder sorgfältig, denn das Modell wurde auf natürlichen Fotos trainiert.
  — <https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary>
- Verwende den gehosteten Old Photo Restoration Space nicht als aktuellen Einstiegspunkt. Er liefert einen Laufzeitfehler, der durch einen unvollständigen Download der Modellkonfiguration verursacht wird.
  — <https://huggingface.co/spaces/modelscope/old_photo_restoration>

## Dadurch abgelöst {#superseded-by-this}

- 2024-01-15 — Reine Colab-Anleitung zur Einrichtung: Die offiziellen Wege über lokale Skripte, Hugging Face, ModelScope, Gradio und ONNX lösen sie ab.
- 2024-01-22 — Gehostete Demo des Old Photo Restoration Space: veraltet, da sie einen Laufzeitfehler liefert.
- 2024-12-31 — Lokale Inferenz mit BasicSR-Abhängigkeit: Der aktuelle Weg über lokale Skripte benötigt kein BasicSR.

## Weiterhin unbekannt {#still-unknown}

- Der erfasste Linktext war nicht zugänglich, daher konnten seine redaktionelle Aussage und der beabsichtigte Vergleich nicht überprüft werden.
- Die Quellen geben nicht an, ob die historische ModelScope-ID `iic/cv_ddcolor_image-colorization` und die aktuelle Repository-ID `damo/cv_ddcolor_image-colorization` Aliase oder eine Migration darstellen. Nimm nicht an, dass sie austauschbar sind.
- Es wurde kein aktueller lokaler Inferenzlauf, keine Hardwaremessung und kein Benchmark gegen einen neueren Colorizer verifiziert.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/piddnad/DDColor | DDColor — offizielle PyTorch-Implementierung | 2026-09-04 |
| https://github.com/piddnad/DDColor/commits/master/ | DDColor-Commit-Verlauf | 2026-09-04 |
| https://github.com/camenduru/DDColor-colab | camenduru/DDColor-colab | 2026-09-04 |
| https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md | DDColor Model Zoo | 2026-09-04 |
| https://huggingface.co/spaces/modelscope/old_photo_restoration | Old Photo Restoration — ein Hugging-Face-Space von modelscope | 2026-09-04 |
| https://huggingface.co/spaces/modelscope/old_photo_restoration/blob/main/app.py | Old Photo Restoration app.py | 2026-09-04 |
| https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary | DDColor zur Bildkolorierung | 2026-09-04 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:ddcolor`, Thread `ddcolor-development`, 1 datiertes Ereignis 2024-01-15 → 2024-01-15.
- **Praktischer Hinweis:** Wir können die DDColor-Arbeit seit 2024-01-15 über das verlinkte Quell-Repository und den Colab-Workflow beginnen. Prüfe den genauen unterstützten Workflow anhand dieser Ressourcen, bevor du ihn verwendest.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
