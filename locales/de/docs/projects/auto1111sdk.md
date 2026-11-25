---
title: "Auto1111SDK"
category: projects
date: 2024-03-05
tags: [auto1111sdk, auto1111sdk-development, project]
aliases: ["Auto1111SDK"]
level: 2
source_sha256: 0e20f3f6ea5b1e109eecf120ee1313705d78f164c87a8c1b598648ab417efc3d
translation: machine
translated_at: '2026-10-24'
---
# Auto1111SDK {#auto1111sdk}

**Entwicklungslinie:** `project:auto1111sdk` · Thread `auto1111sdk-development`  
**Letztes Ereignis:** 2024-03-05 · 2 datierte Ereignisse seit 2024-02-06 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Auto1111SDK ist eine Python-Bibliothek für Entwickler, die lokale Stable-Diffusion-Workflows aus Code heraus steuern, statt über die Automatic1111 WebUI.

- Text-zu-Bild, Bild-zu-Bild, Inpainting, Outpainting und Stable-Diffusion-Upscaling.
- ESRGAN-/Real-ESRGAN-Upscaling, CivitAI-Downloads, benutzerdefinierte VAE-/SDXL-Unterstützung und eine ControlNet-Schnittstelle.

## Entwicklungslinie {#development-line}

- **2024-02-06 — Auto1111SDK-Projektrepository und Colab-Notebook erschienen.** Das Projekt nutzte den persönlichen Repository-Pfad `saketh12/Auto1111SDK` und eine Colab-Demo.
- **2024-03-05 — Auto1111SDK-Organisationsrepository mit dem Colab-Notebook erschienen.** Am 2024-03-05 wurde das Repository unter die GitHub-Organisation Auto1111SDK verschoben, zusammen mit dem verknüpften Colab-Notebook. Die Änderung markiert einen öffentlichen Einstiegspunkt, doch die Verweise zeigen nicht, ob es sich um eine Repository-Migration, ein Release oder eine erneute Veröffentlichung handelte.

## Was sich geändert hat {#what-changed}

Auto1111SDK wurde Anfang 2024 eingestellt; danach gab es kein weiteres PyPI-Release. Am 2024-02-06 startete das Projekt unter dem persönlichen Repository-Pfad `saketh12/Auto1111SDK` mit einer Colab-Demo. Am 2024-02-16 veröffentlichte PyPI Version 0.0.95, die in der Historie weiterhin das neueste Release ist. Am 2024-03-05 wechselte der Repository-Pfad zu `Auto1111SDK/Auto1111SDK`, wobei dieselbe Colab-Datei beibehalten wurde; dies zeigt eine Änderung des Veröffentlichungspfads und nicht neuen Code. Am 2026-09-04 dokumentiert das GitHub-README weiterhin nur die Installation über virtualenv, den alten persönlichen Git-Installationspfad und ControlNet nur mit FP32. Das Paket ist nun eine Legacy-Abhängigkeit mit ungeprüfter Kompatibilität zur aktuellen Laufzeitumgebung.

## So verwenden Sie es {#how-to-use-this}

Ab dem 2024-03-05 betrachten Sie das Auto1111SDK-Organisationsrepository als historischen Projekteinstiegspunkt und prüfen das aktuelle Setup separat.

1. Legen Sie eine saubere Python-Virtual-Environment an; das Projekt empfiehlt ausdrücklich ein virtualenv und erklärt Conda für nicht unterstützt.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
2. Installieren Sie das reproduzierbare letzte Paket-Release mit `pip install auto1111sdk==0.0.95` und prüfen Sie anschließend Version und Dateien gegen PyPI.
  — <https://pypi.org/project/auto1111sdk/>
3. Legen Sie einen kompatiblen lokalen Checkpoint oder eine `.safetensors`-Datei auf der Festplatte ab, erstellen Sie `StableDiffusionPipeline(path)` und rufen Sie `generate_txt2img` mit Prompt, Abmessungen und Schritten auf.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
4. Speichern Sie das erste erzeugte Bild mit `output[0].save(...)`; verwenden Sie diesen minimalen Ablauf als Smoke-Test der Umgebung, bevor Sie einen größeren Workflow hinzufügen.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
5. Für ControlNet erstellen Sie `ControlNetModel` mit dem Modellnamen ohne Dateiendung und einem Eingabebild, übergeben es an die Pipeline und stellen FP32-VRAM bereit.
  — <https://github.com/Auto1111SDK/Auto1111SDK>

## Bewährte Vorgehensweisen {#best-practices}

- Verwenden Sie eine isolierte Virtual Environment statt Conda; dies ist die einzige vom Projekt angegebene Grenze für die Umgebungsunterstützung.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
- Fixieren Sie die Versionen von Auto1111SDK, Python, PyTorch, CUDA und Modellgewichten in einer Lock-Datei oder einem Image: Das neueste veröffentlichte Paket ist die Pre-Alpha 0.0.95 vom 2024-02-16.
  — <https://pypi.org/project/auto1111sdk/>
- Verwenden Sie für einen reproduzierbaren Workflow nicht die ungepinnte Installation `pip install git+https://github.com/saketh12/Auto1111SDK.git` aus dem README; falls eine Installation aus dem Quellcode nötig ist, verwenden Sie eine geprüfte, unveränderliche Quellrevision.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
- Behandeln Sie ControlNet als reines FP32 und messen Sie den GPU-Speicherbedarf, bevor Sie sich darauf festlegen; gehen Sie nicht davon aus, dass die im README geplante FP16-Unterstützung ausgeliefert wurde.
  — <https://github.com/Auto1111SDK/Auto1111SDK>

## Hierdurch ersetzt {#superseded-by-this}

- 2024-02-06 — Der persönliche Link `saketh12/Auto1111SDK` wird als kanonische Referenz durch den am 2024-03-05 erfassten Organisationspfad ersetzt; beide führen heute zum selben benannten Projekt.
- 2024-02-16 — „Installiere die neueste Version“ darf nicht als aktuelle Diffusionsunterstützung der neuesten Generation verstanden werden: Sie ergibt die Pre-Alpha 0.0.95, veröffentlicht am 2024-02-16.
- 2024-03-05 — Die Annahme, dass die Installation aus der Git-Quelle auf neuere ControlNet-Unterstützung hinweist, ist überholt; das aktuelle README dokumentiert ControlNet weiterhin nur als FP32.

## Weiterhin unbekannt {#still-unknown}

- Das Colab-Notebook unter `https://colab.research.google.com/drive/1SekiJ-mdB2V8ogWbyRyF_yDnoMuDGWTl` konnte ohne gültige Google-Sitzung nicht gelesen werden; daher sind seine aktuelle Laufzeitumgebung, Paketversionen, Hardware und der Ausführungszustand ungeprüft.
- Die datierten Verweise belegen einen Wechsel des GitHub-Pfads von persönlich zu Organisation am 2024-03-05, belegen aber nicht, ob es sich um eine Repository-Übertragung, einen Spiegel oder eine Code-Veröffentlichung handelte; für den 2024-03-05 war weder eine Release-Notiz noch ein Commit-Diff verfügbar.
- Die aktuelle Kompatibilität mit Python, PyTorch, CUDA und Modellformaten des Jahres 2026 ist durch die gelesenen Quellen nicht belegt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/Auto1111SDK/Auto1111SDK | Auto1111SDK/Auto1111SDK repository README | 2026-09-04 |
| https://pypi.org/project/auto1111sdk/ | auto1111sdk PyPI project and release history | 2026-09-04 |
| https://github.com/saketh12/Auto1111SDK | Auto1111SDK repository at the original personal path | 2026-09-04 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:auto1111sdk`, Thread `auto1111sdk-development`, 2 datierte Ereignisse 2024-02-06 → 2024-03-05.
- **Praktischer Hinweis:** Ab dem 2024-03-05 betrachten Sie das Auto1111SDK-Organisationsrepository als erfassten historischen Projekteinstiegspunkt und validieren aktuelle Setup-Anleitungen separat.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was überholt ist.
