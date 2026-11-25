---
title: "ControlNet"
category: projects
date: 2023-04-13
tags: [controlnet, controlnet-development, controlnet_face_landmarks, controlnet_v1_1, open_source_release, project]
aliases: ["ControlNet"]
level: 3
source_sha256: 406dfbe74332beb300a643e28dc1f98b9b4451628e6d807ec4639bc76ae61f3a
translation: machine
translated_at: '2026-10-24'
---
# ControlNet {#controlnet}

**Entwicklungslinie:** `project:controlnet` · Thread `controlnet-development`  
**Letztes Ereignis:** 2023-04-13 · 3 datierte Einträge seit 2023-02-12 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

ControlNet ist ein räumlicher Konditionierungsadapter für Diffusionsmodelle. Wir setzen ihn ein, wenn ein Prompt einem Referenzbild folgen muss und nicht nur dem Text.

- Kanten- und Linienkarten, Tiefe, Segmentierung, Posen und Skizzen steuern die Generierung.
- Die eingefrorenen Gewichte des Basismodells bleiben unverändert, während Adapterzweige visuelle Struktur hinzufügen.

## Entwicklungslinie {#development-line}

- **2023-02-12 — ControlNet-Quellcode und lauffähige Einstiegspunkte wurden öffentlich verfügbar.** Am 2023-02-12 ermöglichten das verlinkte GitHub-Repository, der Hugging-Face-Space und das Colab-Notebook öffentlichen Zugriff auf Code und lauffähige Demos. Die Links nennen kein bestimmtes Release-Tag und keinen Funktionsumfang.
- **2023-03-20 — Ein ControlNet-Modell für Gesichtslandmarken wurde der Community vorgestellt.** Am 2023-03-20 veröffentlichte eine Community-Ressource ein ControlNet-Modell für Gesichtslandmarken. Es ergänzte das Ökosystem um Konditionierung auf Gesichtsstruktur. Zu seiner Verbreitung, Leistung oder Akzeptanz liegen uns keine Zahlen vor.
- **2023-04-13 — ControlNet v1.1 begann eine Nightly-Entwicklungslinie.** Am 2023-04-13 markierte ein GitHub-Repository den Beginn der v1.1-Nightly-Linie. Sie setzte die aktive Projektentwicklung fort. Das Repository nannte kein Datum für ein stabiles Release und listete keine Änderungen auf.

## Was sich geändert hat {#what-changed}

ControlNet entwickelte sich von einer Forschungsimplementierung für SD 1.x zu modellspezifischen Steuerungs-Workflows. 2023-02-12 - Das ursprüngliche Projekt dokumentierte die Übertragung von ControlNet auf SD-1.x-Modelle aus der Community. 2023-03-20 - Ein Community-Checkpoint für Gesichtslandmarken ergänzte einen Steuerungstyp, ohne die Kernarchitektur zu verändern. 2023-04-13 - ControlNet 1.1 behielt die 1.0-Architektur bei, vereinheitlichte die Namen und erweiterte den Katalog für SD 1.5 auf 14 Modelle: 11 produktionsreife und 3 experimentelle. 2023-05-31 - Die A1111-Erweiterung fügte in 1.1.202 einen kaskadierten Workflow für Inpainting in hoher Auflösung hinzu, ohne ControlNet selbst zu verändern. 2026-09-04 - Aktuelle Anleitungen dokumentieren ControlNet-Workflows für Flux, Hunyuan-DiT, Stable Diffusion 3 und SDXL über ComfyUI-Knoten und Diffusers-Pipelines.

## Wie man das nutzt {#how-to-use-this}

Die Arbeit begann am 2023-02-12 mit Quellcode und lauffähigen Einstiegspunkten. Ab 2023-04-13 die v1.1-Nightly-Linie direkt identifizieren, statt alle Ressourcen als ein einziges Release zu behandeln.

1. Wähle eine strukturelle Vorgabe und bereite das passende Referenzbild vor; verschiedene ControlNet-Typen erwarten unterschiedliche Referenzbilder.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
2. In ComfyUI legst du den Checkpoint unter `ComfyUI/models/controlnet` ab, lädst das Basis-Checkpoint und ControlNet und lädst dann das Referenzbild hoch.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
3. Verbinde ControlNet mit positiver und negativer Konditionierung, setze Stärke und optional Start- und Endprozente und starte dann die Generierung.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
4. Im Code lädst du ein Steuermodell in die Diffusers-Pipeline, übergibst Prompt und `control_image` und stimmst `controlnet_conditioning_scale` ab.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
5. In AUTOMATIC1111 installierst oder aktualisierst du `sd-webui-controlnet`, fügst Modelldateien hinzu, aktualisierst die Liste und wählst den Preprocessor in der UI aus.
  — <https://github.com/Mikubill/sd-webui-controlnet>

## Best Practices {#best-practices}

- Passe Preprocessor und Referenzkarte an den Checkpoint an; verschiedene ControlNet-Typen erfordern unterschiedliche Referenzbilder.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
- Halte Checkpoints und Pipelines innerhalb einer Modellfamilie, statt SD 1.5, SDXL, Flux und andere als austauschbar zu behandeln.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- Stimme Control Strength oder `controlnet_conditioning_scale` direkt ab, damit die Referenz die Ausgabe weder dominiert noch zu schwach einschränkt.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- Bei Multi-ControlNet die Eingaben auf die erwarteten Abmessungen skalieren, Bedingungen maskieren, um Überlappungen zu vermeiden, und jede Konditionierungsskala separat abstimmen.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- Verwende in ComfyUI `Apply ControlNet`; `Apply ControlNet (Old)` ist veraltet.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
- Verwende für AUTOMATIC1111 `sd-webui-controlnet`; installiere das Forschungsrepository `ControlNet-v1-1-nightly` nicht als A1111-Erweiterung.
  — <https://github.com/lllyasviel/ControlNet-v1-1-nightly>

## Durch Folgendes überholt {#superseded-by-this}

- 2023-04-13 - Die Installation von `ControlNet-v1-1-nightly` in AUTOMATIC1111 ist ein fehlerhafter Altpfad; dessen eigene Anleitung verweist A1111-Nutzer auf `sd-webui-controlnet`.
- 2023-05-31 - A1111 v1.1.202 als aktuelle Integration zu betrachten, ist veraltet; die Erweiterung dokumentiert spätere Arbeiten in v1.1.454 vom 2024-07-09.
- 2023-Ära - ComfyUI-Graphen mit `Apply ControlNet (Old)` sind veraltet; verwende `Apply ControlNet`.

## Weiterhin unbekannt {#still-unknown}

- Der Eintrag zu Gesichtslandmarken beruht auf einem einzigen Community-Beitrag und einer Demo; wir haben weder die Modellkarte, die Lizenz, die Kompatibilität der Checkpoints noch das aktuelle Hosting überprüft.
- Die datierten Ereignisse vermischen Kernarchitektur, einen Community-Checkpoint und eine AUTOMATIC1111-Erweiterung zu einem Ökosystem statt zu einer einzigen gepflegten Distribution.
- Wir können den historischen Hugging-Face-Space und das Colab-Notebook nicht einsehen; die ursprünglichen Anleitungen und ihre Verfügbarkeit bleiben daher unbestätigt.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/lllyasviel/ControlNet | GitHub - lllyasviel/ControlNet: Let us control diffusion models! | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/11v3dgj/new_controlnet_model_trained_on_face_landmarks/ | New ControlNet Model Trained on Face Landmarks | 2026-09-04 |
| https://github.com/lllyasviel/ControlNet-v1-1-nightly | GitHub - lllyasviel/ControlNet-v1-1-nightly: Nightly release of ControlNet 1.1 | 2026-09-04 |
| https://github.com/Mikubill/sd-webui-controlnet/discussions/1464 | [1.1.202 Inpaint] Improvement: Everything Related to Adobe Firefly Generative Fill | 2026-09-04 |
| https://huggingface.co/docs/diffusers/using-diffusers/controlnet | ControlNet - Hugging Face Diffusers | 2026-09-04 |
| https://docs.comfy.org/tutorials/controlnet/controlnet | ComfyUI ControlNet Usage Example | 2026-09-04 |
| https://github.com/Mikubill/sd-webui-controlnet | GitHub - Mikubill/sd-webui-controlnet: WebUI extension for ControlNet | 2026-09-04 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:controlnet`, Thread `controlnet-development`, 3 datierte Ereignisse vom 2023-02-12 bis 2023-04-13.
- **Praktischer Hinweis:** Ab 2023-02-12 konnten Praktiker ControlNet über die verlinkten Quellcode- und Einstiegspunkte beziehen; ab 2023-04-13 sollten sie die v1.1-Nightly-Linie ausdrücklich identifizieren, statt alle ControlNet-Ressourcen als ein statisches Release zu behandeln.
- **Konfidenz:** mittel. Die datierten Überholungshinweise sind maßgeblich dafür, was veraltet ist.
