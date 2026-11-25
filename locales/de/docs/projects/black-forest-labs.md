---
title: "FLUX.1-Kontext-dev-onnx — FLUX.1 Kontext ONNX und Bearbeitung"
category: projects
date: 2025-07-03
tags: [black-forest-labs, black_forest_labs, flux-kontext, flux_kontext, project]
aliases: ["FLUX.1-Kontext-dev-onnx", "Kontext Komposer"]
level: 3
source_sha256: ff1af75935176435b33e1c982a54a2bfc1ec65324d2659af4c6836937aedf54c
translation: machine
translated_at: '2026-10-24'
---
# FLUX.1-Kontext-dev-onnx — FLUX.1 Kontext ONNX und Bearbeitung {#flux1-kontext-dev-onnx-flux1-kontext-onnx-and-editing}

**Entwicklungslinie:** `project:black-forest-labs` · Thread `flux-kontext`  
**Letztes Ereignis:** 2025-07-03 · 1 datiertes seit 2025-07-03 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

FLUX.1-Kontext-dev-onnx ist der ONNX-Export von FLUX.1 Kontext [dev] für lokale Laufzeitumgebungen.

- Bildbearbeitung auf Basis von Textanweisungen.
- Lokale und globale Änderungen mit Erhalt von Figur oder Stil über iterative Arbeitsschritte hinweg.
- Modellexporte in BF16, FP8 und FP4 (SVDQuant).

## Entwicklungslinie {#development-line}

- **2025-07-03 — Black Forest Labs veröffentlichte das ONNX-Repository für FLUX.1 Kontext dev.** Die offizielle Veröffentlichung umfasst BF16-, FP8- und FP4-Exporte (SVDQuant) für das öffentliche Basismodell Kontext [dev]. Dabei handelt es sich um ein Paketierungsformat für bestehende Gewichte, nicht um eine neue Basismodell-Version.

## Was sich geändert hat {#what-changed}

2025-07-03 — FLUX.1-Kontext-dev-onnx: Black Forest Labs stellte BF16-, FP8- und FP4-Exporte (SVDQuant) für das öffentliche Modell Kontext [dev] bereit. Dies ist eine Option zur Paketierung für die Laufzeit und keine neue Basismodell-Version.

2025-07-11 — BFL Playground und Kontext-Komposer-Voreinstellungen: Der Web-Editor ergänzte textgesteuerte Bearbeitung ohne Code, und ein Community-Beitrag dokumentierte Prompt-Voreinstellungen. Keine der beiden Quellen führte ONNX-Gewichte, eine API oder eine Modellrevision ein.

Heute gefunden (2026-09-04) — BFL führt Kontext weiterhin als Werkzeug der vorherigen Generation. Ausgaben bleiben bei 1 MP. BFL empfiehlt für neue Arbeiten, die Ausgaben bis 4 MP, Bearbeitungen mit mehreren Referenzen oder eine genauere Steuerung erfordern, FLUX.2.

## So wird es verwendet {#how-to-use-this}

Ab 2025-07-03 beginnt die Evaluierung mit dem ONNX-Repository. Modellrevisionen und Laufzeitunterstützung sind vor der Integration zu prüfen.

1. Öffnen Sie das offizielle ONNX-Repository, melden Sie sich an und akzeptieren Sie die beschränkte FLUX.1 [dev] Non-Commercial License, bevor Sie Dateien herunterladen.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
2. Wählen Sie BF16, FP8 oder FP4 (SVDQuant) für eine unterstützte Laufzeitumgebung. Die Model Card enthält kein modellspezifisches Code-Beispiel; prüfen Sie die Unterstützung, bevor Sie einen allgemeinen Diffusion-Single-File-Workflow verwenden.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
3. Verwenden Sie die kanonischen Kontext-[dev]-Gewichte, wenn ONNX nicht erforderlich ist. Installieren Sie Diffusers, laden Sie die Pipeline und übergeben Sie anschließend ein Eingabebild und einen Bearbeitungs-Prompt.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/tree/main>
4. Für eine gehostete Evaluierung öffnen Sie die ursprüngliche Playground-Bearbeitungsroute und melden sich an. Bei der heutigen Prüfung wurde über die BFL-Authentifizierung zum Dashboard-Playground weitergeleitet.
  — <https://playground.bfl.ai/image/edit>
5. Wählen Sie FLUX.2 statt einer neuen Kontext-Integration, wenn ein Produktionsprojekt mehr als 1 MP Ausgabe oder mehrere Referenzen benötigt.
  — <https://help.bfl.ai/articles/5186006235-what-is-flux-1-kontext>

## Bewährte Praktiken {#best-practices}

- Formulieren Sie jeweils eine explizite visuelle Änderung, etwa „Change the car color to red“, und prüfen Sie das Ergebnis, bevor Sie die nächste Bearbeitung vornehmen.
  — <https://docs.bfl.ai/kontext/kontext_image_editing>
- Geben Sie bei Textbearbeitungen im Bild sowohl den Ausgangs- als auch den Ersatztext an. Verwenden Sie auffällige Annotationsrahmen, wenn eine Textbearbeitung eine gezielte Neupositionierung oder Größenanpassung erfordert.
  — <https://docs.bfl.ai/kontext/kontext_image_editing>
- Halten Sie Bearbeitungsketten kurz und speichern Sie gute Zwischenergebnisse. BFL dokumentiert sichtbare Qualitätsverluste nach sechs iterativen Bearbeitungen; starten Sie daher lieber mit einem sauberen Bild neu, statt eine Kette endlos fortzuführen.
  — <https://bfl.ai/blog/flux-1-kontext>
- Behandeln Sie dev-Gewichte standardmäßig als nicht kommerziell und nicht für den Produktivbetrieb bestimmt. Setzen Sie Filterung oder manuelle Prüfung ein und erfüllen Sie die geltenden Anforderungen an die Herkunftsnachweise.
  — <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx>
- Community-Praxis: Erstellen Sie Voreinstellungen als bearbeitbare Prompt-Vorlagen, die das Motiv beibehalten und dabei Kontext, Szene, Stil, Kleidung oder Hintergrund verändern. Dies sind keine offiziellen Modellsteuerungen.
  — <https://www.reddit.com/r/StableDiffusion/comments/1lx8lot/kontext_presets_all_system_prompts/>

## Hiermit abgelöst {#superseded-by-this}

- Der private Beta-Zugang per E-Mail vom 2025-05-29 endete mit der öffentlichen Veröffentlichung der offenen Gewichte am 2025-06-26. Der Zugang läuft nun über den beschränkten Lizenzablauf auf Hugging Face.
- Die Hinweise vom 2025-07-11, die die Playground-Bearbeitungs-URL als nicht authentifizierten Einstiegspunkt beschreiben, sind veraltet. Wie am 2026-09-04 beobachtet, leitet sie über die BFL-Authentifizierung zum Dashboard weiter.
- Die Empfehlung aus dem Jahr 2025, neue hochauflösende oder mehrfach referenzierte Bearbeitungen auf Kontext aufzubauen, wird durch die Empfehlung von BFL für FLUX.2 abgelöst. Kontext bleibt verfügbar; es wurde nicht entfernt.

## Weiterhin unbekannt {#still-unknown}

- Das ONNX-Artefakt vom 2025-07-03 sowie die Browser- und Voreinstellungsmaterialien vom 2025-07-11 teilen den Namen der Kontext-Familie, ihre Zusammengehörigkeit als ein Produkt ist jedoch nicht belegt. Das Erste ist eine lokale Distribution; das Zweite umfasst einen gehosteten Editor und eine Prompt-Schicht aus der Community.
- Kontext Komposer taucht in Community-Beiträgen als Bezeichnung einer Voreinstellung auf, etwa „Komposer: Teleport“. Keine Primärquelle belegt, dass es sich um ein offizielles BFL-Produkt, eine Version oder einen Bestandteil des ONNX-Repositorys handelt.
- Die offizielle ONNX-Model-Card enthält kein durchgängiges Laufzeitbeispiel. Wir müssen entweder eine kompatible, eigene ONNX-Pipeline bereitstellen oder den dokumentierten Diffusers-Weg nutzen.
- Der ursprüngliche datierte Quelltext ist nicht verfügbar, daher lassen sich seine genauen Aussagen, der Status einer BFL-Empfehlung oder die Exportrevisionen allein anhand der Links nicht rekonstruieren.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx | black-forest-labs/FLUX.1-Kontext-dev-onnx · Hugging Face | 2026-09-04 |
| https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/tree/main | black-forest-labs/FLUX.1-Kontext-dev at main · Hugging Face | 2026-09-04 |
| https://bfl.ai/blog/flux-1-kontext-dev | FLUX.1 Kontext [dev] - Open Weights for Image Editing | Black Forest Labs | 2026-09-04 |
| https://bfl.ai/blog/flux-1-kontext | Introducing FLUX.1 Kontext and the BFL Playground | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/kontext/kontext_image_editing | Image Editing | Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/5186006235-what-is-flux-1-kontext | What is FLUX.1 Kontext? | Black Forest Labs Knowledge Base | 2026-09-04 |
| https://playground.bfl.ai/image/edit | Black Forest Labs - Frontier AI Lab | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/1lx8lot/kontext_presets_all_system_prompts/ | Kontext Presets - All System Prompts : r/StableDiffusion | 2026-09-04 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:black-forest-labs`, Thread `flux-kontext`, 1 datiertes Ereignis 2025-07-03 → 2025-07-03.
- **Praktischer Hinweis:** Ab 2025-07-03 sollten Praktiker, die diese Linie evaluieren, mit dem verlinkten ONNX-Repository als Deployment-Artefakt beginnen und Modellrevision sowie Laufzeitunterstützung vor der Integration separat prüfen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich für die Frage, was veraltet ist.
