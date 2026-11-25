---
title: "FLUX.2 [klein]-Architektur: Release-gebundene Schnittstelle"
description: "Aussagen zur FLUX.2 [klein]-Architektur müssen an das benannte offizielle Release und Artefakt gebunden sein. Die öffentliche Modellfamilie unterstützt Text-zu-Bild und Referenz-Bearbeitung, interne Block-Layouts, Encoder-Verdrahtung, Quantisierung und Adapter-Kompatibilität lassen sich jedoch nicht sicher über Varianten oder Laufzeitumgebungen hinweg ableiten."
category: reference
tags: [flux, klein, architecture, model-contract, adapters, inference, provenance]
aliases: ["Klein Architecture", "FLUX2 Klein Architecture"]
level: 2
source_sha256: dc36186cf6588c455a0d27e7ed5709515066920c70e24caef3adc1837e9d5e4a
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 [klein]-Architektur: Release-gebundene Schnittstelle {#flux2-klein-architecture-release-bound-interface}

FLUX.2 [klein] ist eine Modellfamilie und keine austauschbare Architekturdatei.
Für jede interne Aussage ist der benannte Checkpoint, die offizielle Model Card,
die Quellrevision und die Laufzeitumgebung maßgeblich. Parameteranzahl-Bezeichnungen,
ein Familienname oder ein Drittanbieter-Workflow belegen weder Blockanzahlen,
Text-Encoder-Verdrahtung, Latent-Layout, Quantisierungsunterstützung noch
Adapter-Kompatibilität.

## Was die offizielle Familiendeklaration belegt {#what-the-official-family-declaration-supports}

Das [offizielle FLUX.2-Repository](https://github.com/black-forest-labs/flux2)
listet die Varianten [klein] 4B, 9B, 9B KV, 4B Base und 9B Base auf und beschreibt
für die Familie Text-zu-Bild sowie Bildbearbeitung mit einer und mehreren Referenzen.
Es unterscheidet destillierte von Base-Varianten und empfiehlt Base-Modelle für
Fine-Tuning und LoRA-Arbeiten.

Das stützt eine Entscheidung zur Release-Auswahl. Es macht jedoch kein festes
internes Transformer-Diagramm, kein Qwen-Layer-Extraktionsrezept, keine VAE-Kanalanzahl,
keinen RoPE-Offset, keine Sequenzgrenze und keine Inferenzeinstellung für jedes
Artefakt wahr, das den Namen [klein] trägt.

## Die ausführbare Schnittstelle binden {#bind-the-executable-interface}

Für eine bestimmte Deployment- oder Trainingsaufgabe sind folgende Angaben festzuhalten:

- offizieller Modellbezeichner, Revision/Digest, Lizenzhinweis und alle erforderlichen
  Komponenten;
- Quelle und Version der Laufzeitumgebung, Tokenizer/Text-Encoder, VAE/Decoder,
  Scheduler sowie das Eingabeschema für Bilder und Referenzen;
- dtype, Quantisierung sowie Geräte- und Backend-Unterstützung, wie sie für genau
  dieses Release dokumentiert sind;
- der bereitgestellte Einstiegspunkt für Generierung bzw. Bearbeitung, erforderliche
  Vorverarbeitung und Ausgabe-Metadaten; und
- ein Basis-Nachweis (Baseline-Receipt), dass der gewählte Pfad für Text, eine
  einzelne Referenz oder mehrere Referenzen tatsächlich ausgeführt wird.

Referenzbilder sind Eingaben mit eigener Herkunft, Vorverarbeitung, Anzahl,
Reihenfolge und Fehlerbehandlung. Ein gemeinsames Latent-Sequenz-Layout oder
die Wiederverwendung von Zuständen aus einer anderen Variante darf nicht abgeleitet
werden, nur weil eine Oberfläche mehrere Bilder akzeptiert.

## Grenze zwischen Base, destilliert und Kompatibilität {#base-distilled-and-compatibility-boundary}

Base- und destillierte Releases haben unterschiedlich angegebene Zwecke. Der aktuelle
BFL-[klein-Trainingsleitfaden](https://docs.bfl.ai/flux_2/flux2_klein_training)
beschreibt Base-Modelle als nicht destillierte Ausgangspunkte für Fine-Tuning, während
die öffentliche Modellübersicht familienweite Unterschiede bei Laufzeit und Nutzung
auflistet. Den gewählten Artefakt festzuschreiben ist richtig; diese Hinweise
dürfen nicht als pauschale Konvertierungs- oder Inferenzzusage dargestellt werden.

Ein Adapter gilt erst dann als kompatibel, wenn Ziel-Basischeckpoint, Architektur,
Loader, Adapterkonfiguration und Ausgabeverhalten gemeinsam getestet wurden. Ein
FLUX.1-, 4B-, 9B-, Community- oder quantisierter Adapter darf niemals allein aufgrund
seines Dateinamens, seiner Parameteranzahl oder einer vermuteten verborgenen Form
geladen werden. Ein fehlgeschlagener oder ungeprüfter Adapter muss ein sichtbares
Inkompatibilitätsergebnis liefern und darf nicht stillschweigend teilweise zusammengeführt werden.

## Lizenz- und Ausgabegrenze {#license-and-output-boundary}

Die Lizenz für lokale Gewichte gilt für das benannte Artefakt und nicht für das
allgemeine Wort „FLUX“. Die [offizielle Modelltabelle](https://github.com/black-forest-labs/flux2)
nennt derzeit Apache-2.0 für [klein] 4B/4B Base und die FLUX Non-Commercial License
für 9B-Varianten. Vor jedem Deployment oder jeder Verbreitung sind die beigefügte
Lizenz und der aktuelle kommerzielle Weg zu prüfen. Ein feinabgestimmter Adapter
kann ein abgeleitetes Werk mit zusätzlichen Pflichten sein.

Auch generierte oder bearbeitete Ausgaben benötigen eigene Herkunfts-, Rechte- und
visuelle Prüfung. Eine Modellfähigkeit belegt nicht, dass eine bestimmte Bearbeitung
Fakten, Identität, Produktgeometrie, Text oder geschützte Bereiche erhalten hat.

## Verwandte Seiten {#related-pages}

- [[flux-klein-capability-map]]
- [[flux-klein-9b-inference]]
- [[diffusion-lora-training]]
- [[lora-fine-tuning-for-editing-models]]
