---
title: "ACE++: Referenzgesteuerte Bilderstellung und Bildbearbeitung"
description: "ACE++ ermöglicht referenzgesteuerte Bilderstellung und Bildbearbeitung über aufgabenspezifische LoRA-Workflows und ein allgemeines FFT-Modell; verwenden Sie die veröffentlichte Basismodell-Kombination und prüfen Sie deren Bedingungen."
category: models
tags: [image-editing, alibaba, flux, reference-image, inpainting, lora, comfyui]
aliases: ["ACE Plus", "FuseAnyPart"]
level: 2
source_sha256: 17371554ba213dcd211e0d1d1c5ae9a42dec44badad0fd439e56000e468607e5
translation: machine
translated_at: '2026-10-24'
---
# ACE++: Referenzgesteuerte Bilderstellung und Bildbearbeitung {#ace-reference-driven-image-creation-and-editing}

**Stand der Prüfung: 2026-09-04.** ACE++ ist ein Post-Training-System des Alibaba Tongyi Lab für die Erzeugung und Bearbeitung von Bildern auf Basis von Referenzbildern. Es kombiniert Referenzbilder, bei Bedarf Bearbeitungsbilder oder Masken sowie eine Textanweisung. Das offizielle Repository stellt mehrere aufgabenspezialisierte LoRA-Routen und ein breiter angelegtes, vollständig feinabgestimmtes (FFT) Modell bereit, anstatt einen einzigen austauschbaren Checkpoint für alle Workflows.

## Veröffentlichte Modellroute auswählen {#select-the-published-model-route}

| Route | Vorgesehener Einsatzbereich | Betriebshinweis |
|---|---|---|
| Portrait-LoRA | Identitäts- und Porträt-Referenzgenerierung oder -bearbeitung | den mitgelieferten Referenz-Workflow verwenden |
| Subject-LoRA | Konsistenz von Objekten, Logos, Mustern und Motiven | den mitgelieferten Referenz-Workflow verwenden |
| Local-Editing-LoRA | masken- oder steuerungsgeführte lokale Änderungen | ggf. die dokumentierte Vorverarbeitung verwenden |
| FFT-Modell | breiter angelegte Referenz- und Bearbeitungsaufgaben | die Autoren merken an, dass die Ergebnisse weniger stabil sind als bei den spezialisierten LoRA-Routen |

Das Repository empfiehlt die LoRA-Workflows, sofern eine spezialisierte Route existiert. Ein allgemeines Modell kann praktisch sein, sollte aber nicht als Qualitätsmaßstab für eine Aufgabe gelten, für die ein eigener Adapter existiert.

## Basismodell und Grenzen des Workflows {#base-model-and-workflow-boundary}

Die veröffentlichten LoRA-Beispiele kombinieren ACE++ mit `FLUX.1-Fill-dev`; einige Workflows verwenden zusätzlich FLUX.1 Redux oder dokumentierte Vorverarbeitungskomponenten. Die FFT-Route hat eine eigene Konfiguration. Die folgenden Punkte sollten als eine versionierte Einheit behandelt werden:

- ACE++-Gewichte und ausgewählter Workflow;
- Revision des Basismodells und etwaige Begleitmodelle;
- Vorverarbeitungsmodell und Konvention für Masken bzw. Steuerung;
- Bildabmessungen, Einstellung der Sequenzlänge, Sampling-Parameter und Prompt;
- Ausgabeartefakt und Autorisierung der Referenzquelle.

Laden Sie keinen ACE++-Adapter in einen beliebigen FLUX-Checkpoint, nur weil die Dateinamen kompatibel wirken. Die Option `max_seq_length` des Repositorys ist ein Regler zwischen Speicherbedarf und Detailtreue für den mitgelieferten Workflow, keine allgemeingültige Qualitätseinstellung.

## Praktische Abnahmeprüfungen {#practical-acceptance-checks}

Testen Sie die genaue Bearbeitungsklasse, bevor Sie sich darauf verlassen:

1. Prüfen Sie, ob das Referenzmotiv bzw. Referenzobjekt dort erhalten bleibt, wo dies erforderlich ist.
2. Kontrollieren Sie in Auslieferungsgröße die Bearbeitungsgrenze, Maskenüberlauf, Hände, Typografie und kleine Logos.
3. Prüfen Sie, ob unbeteiligte Bereiche unverändert bleiben, sofern Erhaltung gefordert ist.
4. Bewahren Sie Eingabebild, Maske, Prompt, Seed, Modellrevisionen und Ausgabe für eine reproduzierbare Prüfung auf.
5. Weichen Sie auf einen kontrollierten manuellen oder kompositionsbasierten Weg aus, wenn das Ergebnis das falsche Objekt verändert.

Das Upstream-Projekt nennt Einschränkungen bei der Befolgung von Anweisungen für einige Hinzufüge- und Entfernungsoperationen und weist auf mögliche Artefakte hin. Ein visuell plausibles Ergebnis ist kein Nachweis dafür, dass die angeforderte lokale Bearbeitung korrekt durchgeführt wurde.

## Lizenzierung und Verbreitung {#licensing-and-distribution}

ACE++ basiert auf externen Basismodell-Artefakten. Prüfen Sie die aktuellen Lizenz- und Zugangsbedingungen für das gewählte Basismodell, die ACE++-Gewichte und jeden Begleit-Checkpoint, bevor Sie kommerziell einsetzen, weiterverbreiten oder einen gehosteten Dienst anbieten. Bezeichnen Sie einen Workflow nicht als kommerziell freigegeben, nur weil der Code auf GitHub einsehbar ist.

## Referenzen {#references}

- [ACE++ offizielles Repository](https://github.com/ali-vilab/ACE_plus)
- [ACE++-Paper](https://arxiv.org/abs/2501.02487)
- [ACE++ Hugging-Face-Collection](https://huggingface.co/ali-vilab/ACE_Plus)
