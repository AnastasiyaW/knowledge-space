---
title: "FLUX.2 [klein] 9B-Inferenz"
description: "Die Inferenz mit FLUX.2 [klein] 9B muss dem veröffentlichten Modellvariante, Checkpoint, Scheduler und der Lizenz folgen; benchmarken Sie den exakten Text- oder Edit-Workflow, statt generische Sampler-, VRAM- oder LoRA-Regeln zu übernehmen."
category: models
tags: [flux, flux2, klein, 9b, inference, editing, lora, reproducibility, licensing]
aliases: ["Klein 9B", "FLUX Klein 9B", "Klein Distilled"]
level: 3
source_sha256: 40feef373f1be8858fd4eb15f218296398c86c5f23f44735b2956251fc5e3f73
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 [klein] 9B-Inferenz {#flux2-klein-9b-inference}

FLUX.2 [klein] ist eine Modellfamilie. FLUX.2 [klein] 9B ist eine benannte destillierte Veröffentlichung, bildet ohne ihre Checkpoint-Revision und Laufzeit-Assets aber dennoch keine vollständige Inferenzkonfiguration. Das [offizielle FLUX.2-Repository](https://github.com/black-forest-labs/flux2) unterscheidet die Varianten 9B, 9B KV und 9B Base; die dortigen Hinweise empfehlen destillierte Varianten für interaktive Workflows und Base-Varianten für Fine-Tuning und maximale Flexibilität. Behandeln Sie den benannten Checkpoint und seine veröffentlichten Laufzeit-Assets als einen gemeinsamen Vertrag.

## Den exakten Vertrag festlegen {#identify-the-exact-contract}

Erfassen Sie vor jedem Inferenz- oder Edit-Lauf Folgendes:

- Modell und Checkpoint-Revision, einschließlich destillierter/Base- oder KV-Variante;
- Pipeline, Scheduler, Text-Encoder, Decoder/VAE, Adapter-Loader und Laufzeitumgebung;
- Prompt- oder Bildreferenz-Fixture, Seed, Abmessungen und Ausgabeformat;
- alle Adapter und deren Kompatibilität mit Quell- bzw. Basismodell; sowie
- die geltenden Bedingungen für Gewichte, API und abgeleitete Nutzung.

Das offizielle Projekt führt FLUX.2 [klein] 9B unter einer nicht-kommerziellen Lizenz. Das allein erlaubt keinen Produkt-Workflow: Prüfen Sie die aktuellen Bedingungen für die gewählten Gewichte und prüfen Sie separat die Bedingungen etwaiger gehosteter Dienste oder Drittkomponenten.

## Text-zu-Bild und Bearbeitung sind getrennte Tests {#text-to-image-and-editing-are-separate-tests}

Für Text-zu-Bild verwenden Sie eine kleine, versionierte Prompt-Suite mit Fixtures für Komposition, Material, Typografie und Negativ-Prompts. Für die Bildbearbeitung bewahren Sie das Quellbild auf und deklarieren vor der Generierung die gewünschten Änderungen sowie die zu schützenden Eigenschaften.

Die [FLUX.2-Dokumentation zur Bildbearbeitung](https://docs.bfl.ai/flux_2/flux2_image_editing) beschreibt textgesteuerte Bearbeitung mit einer oder mehreren Referenzen. Das bedeutet nicht, dass jeder lokale Wrapper, Checkpoint oder Adapter alle Details erhält. Prüfen Sie die konkrete Route anhand von Quell-/Ergebnis-Vergleichen und nicht anhand einer allgemeinen Aussage über die Modellfähigkeit.

## Durch Messung abstimmen, nicht nach Faustregeln {#tune-by-measurement-not-folklore}

Übernehmen Sie keine universelle Schrittzahl, keinen Guidance-Wert, keinen Sampler, keine Denoise-Stärke, keine VRAM-Angabe und keinen LoRA-Gewichtsbereich aus einem anderen Workflow. Stattdessen:

1. führen Sie die veröffentlichte Baseline für den gewählten Checkpoint aus;
2. variieren Sie jeweils eine unterstützte Einstellung auf denselben Fixtures;
3. messen Sie Kalt- und Warmstart-Latenz, Spitzenspeicherbedarf, Reproduzierbarkeit und visuelle Abnahme;
4. bewerten Sie die Erhaltung der Quelle für einen Edit-Workflow separat; und
5. veröffentlichen Sie das gewählte Versionstupel und bekannte Grenzen zusammen mit dem Job.

Quantisierung, Kompilierung und Memory-Offloading sind Laufzeit-Kompromisse. Den Nachweis, der vor einer Kombination mit einem Bild-Workflow erforderlich ist, finden Sie unter [[diffusion-inference-acceleration]].

## Adapter-Kompatibilität {#adapter-compatibility}

Ein Adapter muss den exakten Basis-Checkpoint und den Loader benennen, mit denen er trainiert wurde. Ähnliche Parameterzahlen oder ein gemeinsames Label „FLUX“ sind kein Nachweis der Kompatibilität. Testen Sie einen Adapter zuerst allein, bevor Sie eine Kombination testen, halten Sie Skalierung und Ladereihenfolge im Run-Receipt fest und verwerfen Sie eine Ausgabe, wenn deren geschützter Inhalt abweicht.

Beim Training eines neuen Adapters verwenden Sie die aktuelle modellspezifische Anleitung, etwa die [FLUX.2 [klein] Trainingsdokumentation](https://docs.bfl.ai/flux_2/flux2_klein_training), und validieren Sie das resultierende Artefakt anschließend in derselben Inferenz-Pipeline, die es später bedienen wird.

## Freigabedokumentation {#release-record}

Speichern Sie zu jedem freigegebenen Lauf das Modell-Manifest, das Prompt-/Referenz-Fixture, den Hash der Ausgabe, die Abnahmeprüfung, die Lizenzentscheidung und etwaige Metadaten zur Kennzeichnung der Ausgabe. So wird eine spätere Laufzeit- oder Modell-Aktualisierung nachvollziehbar, anstatt das Bildverhalten stillschweigend zu verändern.

## Verwandte Seiten {#related-pages}

- [[flux-klein-9b-architecture]]
- [[flux-klein-style-lora-system]]
- [[diffusion-inference-acceleration]]
- [[flow-matching]]
