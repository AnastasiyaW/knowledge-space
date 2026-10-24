---
title: "Diffusion-LoRA-Training: Nachweise und Kompatibilitätsvertrag"
description: "Diffusion-LoRA-Training ist ein versionsgebundenes Adapterexperiment. Binde den exakten Basis-Checkpoint, die Architektur, die Laufzeitumgebung, das Adapterformat, die autorisierten Daten und den Evaluationssplit, und wähle Rang, Zeitplan, Zielmodule und Optimierer ausschließlich anhand des gemessenen Verhaltens auf Held-out-Daten statt anhand kopierter Rezepte."
category: techniques
tags: [lora, fine-tuning, diffusion, adapters, provenance, evaluation, training]
aliases: ["LoRA Training Pipeline", "Diffusion Fine-Tuning"]
level: 3
source_sha256: c0f8dc0ed26661b590d7c58aa563339250d5b51ca0e3fff2f16ad50cd4dcc9e6
translation: machine
translated_at: '2026-10-24'
---
# Diffusion-LoRA-Training: Nachweise und Kompatibilitätsvertrag {#diffusion-lora-training-evidence-and-compatibility-contract}

Ein LoRA ist keine portable Stildatei und kein Rezept, das durch eine Anzahl an Bildern, einen Rang, eine Lernrate oder eine Schrittzahl definiert ist. Es ist ein Adapter, der für eine bestimmte Basisarchitektur und Laufzeitumgebung trainiert wurde. Trainingsparameter sind experimentelle Eingaben, deren Wert anhand des Verhaltens auf Held-out-Daten für die benannte Aufgabe beurteilt werden muss.

## Den Adaptervertrag festlegen {#pin-the-adapter-contract}

Vor dem Training ist Folgendes zu dokumentieren:

- Basismodell/Checkpoint und Komponenten-Digests, Architekturrevision, VAE bzw. Bild-Encoder, Tokenizer/Text-Encoder sowie der Pfad für die Bildkonditionierung;
- Trainer/Laufzeitumgebung, Abhängigkeitsversionen, Zielmodule, Adaptermethode, Präzision, Vorverarbeitung und Serialisierungsformat des Checkpoints;
- vorgesehene Inferenz-Laufzeitumgebung und Loader einschließlich des unterstützten Adapterformats und der Ladereihenfolge; sowie
- Lizenz, autorisierte Nutzung, Ausgabe-Richtlinie und Revision jedes vorgelagerten Artefakts.

Die [PEFT-Hinweise zu Checkpoints](https://huggingface.co/docs/peft/developer_guides/checkpoint) verlangen bei der Konvertierung in das eigene Format sowohl die Adaptergewichte als auch die Adapterkonfiguration. Das zeigt, warum eine Adapterdatei allein keine Kompatibilitätsaussage darstellt. Vor der Interpretation eines Trainingsergebnisses ist das Laden sowie eine bekannte Baseline-Ausgabe mit der exakten Produktionslaufzeit zu testen.

## Die Datenhoheit definieren {#define-the-data-authority}

Für jedes Sample sind Nutzungsrechte, Einwilligung bei abgebildeten Personen, die Herkunft der Captions bzw. Annotationen und die vorgesehene Aufgabe festzuhalten. Eine Stil-/Domänen-Sammlung, ein Quelle-Ziel-Bearbeitungspaar und eine referenzkonditionierte Aufgabe liefern unterschiedliche Supervision. Eine dieser Formen darf nicht umetikettiert werden, um ein Experiment als gepaart erscheinen zu lassen.

Die Daten sind nach Originalasset, Aufnahmesitzung, Motiv/Produkt und Ableitungskette zu splitten. Near-Duplicate-Zuschnitte, mehrere Bearbeitungen eines Quellbildes und generierte Ableitungen gehören in denselben Split. Unsicherheits- und Ausschlussmarkierungen sind beizubehalten, statt sämtliche Internetbilder oder synthetischen Bilder als autorisierte Ground Truth zu behandeln.

## Parameter anhand von Messungen auswählen {#select-parameters-by-measurement}

Rang, Zielschichten, Lernrate, Optimierer, Batch-/Akkumulationsgröße, Auflösung, Caption-Richtlinie und Stoppunkt hängen vom festgelegten Modell und der Aufgabe ab. Ausgangspunkt ist die benannte Dokumentation von Trainer bzw. Modell. Anschließend ist eine reproduzierbare Baseline zu etablieren und eine begrenzte Konfiguration mit einem aufbewahrten Experiment-Receipt zu variieren.

Die [Diffusers-Trainingsdokumentation](https://huggingface.co/docs/diffusers/training/overview) stellt Beispielskripte bereit, von denen jedes eigene Anforderungen hat. Sie etabliert kein universelles Parameterrezept für jede Diffusionsarchitektur. Ähnlich dokumentiert BFL [klein Base models](https://docs.bfl.ai/flux_2/flux2_klein_training) als geeignete Ausgangspunkte für Fine-Tuning. Das zertifiziert jedoch weder einen Community-Trainer, noch einen Rang, Optimierer oder Adapter als kompatibel, ohne einen Test auf Artefaktebene.

## Präzision und Datenladen getrennt binden {#bind-precision-and-data-loading-separately}

Die PyTorch-2.14-Dokumentation unterscheidet zwischen Autocast und Gradient-Scaling. Scaling adressiert den Gradient-Underflow bei FP16. Es ist kein generischer Schalter für jeden Lauf mit reduzierter Präzision. Für den unterstützten CUDA-Pfad eines Trainers ist der Scaler für FP16 zu aktivieren, nicht automatisch für BF16. Ein Fallback auf volle Präzision auf der CPU darf nicht in einen CUDA-Autocast-Kontext gelangen. CPU-BF16 ist eine eigene Entscheidung für unterstützte Operationen und keine Annahme, die man trifft, wenn CUDA fehlt. [AMP-Referenz](https://docs.pytorch.org/docs/2.14/amp.html).

Eine nicht verifizierte iterierbare Eingabe-Pipeline ist mit `num_workers=0` zu starten. Vor dem Hinzufügen von Workern ist nachzuweisen, dass die Replikate die vorgesehenen Samples partitionieren und dass sich der Durchsatz ohne inakzeptables Wachstum des Host-Speichers verbessert. Neben den Batches sind Sample-IDs und -Anzahlen zu protokollieren. Ein schnellerer Stream mit Duplikaten ist keine Verbesserung des Trainings. Wo sinnvoll, ist worker-bewusste Partitionierung über `get_worker_info()` oder `worker_init_fn` zu verwenden. Prefetching und persistente Worker sind nur für einen Multi-Prozess-Loader zu konfigurieren. [DataLoader-Referenz](https://docs.pytorch.org/docs/2.14/data.html).

## Die gewünschte Änderung und die Erhaltung bewerten {#evaluate-the-requested-change-and-preservation}

Verwende quellendisjunkte Prompts und Bilder, die nicht zur Auswahl der Parameter dienten. Folgende Aspekte sind getrennt zu prüfen:

| Frage | Nachweis |
|---|---|
| Tritt das gewünschte Konzept oder die gewünschte Bearbeitung auf? | aufgabenspezifische Held-out-Evaluation und freigegebene visuelle Prüfung |
| Was soll unverändert bleiben? | Identität, Produktgeometrie, Text, Masken, Hintergrund, Farbe oder andere deklarierte geschützte Bereiche |
| Lädt der Adapter korrekt? | exaktes Lade-Receipt für Basis und Laufzeitumgebung sowie deterministische oder geprüfte Smoke-Beispiele |
| Ist das Ergebnis stabil? | wiederholte Seeds/Eingaben, Erfassung von Fehlern und Vergleich mit der festgelegten Baseline des Basismodells |

Eine hohe scheinbare Stärke des Stils ist kein Nachweis für korrektes Bearbeiten, faktische Wiederherstellung, Identitätserhalt oder Lizenzkonformität.

## Grenze der Veröffentlichung {#release-boundary}

Ein Adapter darf nur zusammen mit seinem Basis-/Laufzeitvertrag, der Datenhoheit, den Adapter- und Konfigurationsdateien, dem Evaluations-Receipt, bekannten Fehlermodi und den Nachweisen zu Lizenz und Verbreitung veröffentlicht werden. Lassen sich Kompatibilität, Rechte oder Erhaltung nicht belegen, bleibt er für die Evaluation privat oder wird als geprüftes visuelles Experiment gekennzeichnet und nicht als wiederverwendbarer Produktionsadapter.

## Stolperfallen {#gotchas}

- **Ein grüner CPU-Smoke-Test wird als GPU-Trainingsergebnis bezeichnet:** Die CPU-only-Grenze ist beizubehalten. Vor dieser Aussage sind Beschleuniger, Dtype und Optimiererpfad im tatsächlichen Trainingslauf zu verifizieren.
- **Mehr Loader-Worker wiederholen Beispiele:** Vor der Interpretation von Durchsatz oder Epochenzählern ist die Zuordnung der Samples pro Worker zu prüfen.
- **BF16 hat eine FP16-Scaler-Einstellung übernommen:** Binde den Scaler an den tatsächlichen Dtype-Vertrag des Trainers, statt ein Mixed-Precision-Rezept zu kopieren.

## Verwandte Seiten {#related-pages}

- [[lora-fine-tuning-for-editing-models]]
- [[flux-klein-9b-architecture]]
- [[flux-klein-character-lora]]
- [[paired-training-for-restoration]]
