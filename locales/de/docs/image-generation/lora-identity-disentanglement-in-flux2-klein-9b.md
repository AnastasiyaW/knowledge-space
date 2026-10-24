---
title: "FLUX.2 [klein] 9B Identity-LoRA: Vertrag zur Disentanglement-Trennung"
description: "Ein FLUX.2 [klein] 9B Identity-LoRA ist ein an Version, Daten und Rechte gebundenes Adapter-Experiment; das offizielle Basismodell-Release und dessen Bedingungen, Adapter-/Runtime-Format, autorisierte Identitätsreferenzen, Label-/Caption- und Erhaltungsrichtlinie, quellenfremde Identitäts- und Nicht-Ziel-Evaluierung sowie eine Prüfung vor jeder Verwendung festlegen."
category: techniques
tags: [flux2-klein, lora, identity, disentanglement, provenance, evaluation]
aliases: ["LoRA Identity Disentanglement in FLUX.2 Klein 9B", "FLUX.2 Klein Identity LoRA"]
level: 2
source_sha256: ae1410d6e60e28c1f20df38252c724bacbbc83e05f4697d255873dd8959892d4
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 [klein] 9B Identity-LoRA: Vertrag zur Disentanglement-Trennung {#flux2-klein-9b-identity-lora-disentanglement-contract}

Ein Identity-LoRA lernt einen Adapter für eine bestimmte Basismodell-Version;
es isoliert eine Person standardmäßig nicht von allen umgebenden Attributen.
„Disentanglement“ ist eine Aussage über die Erhaltung von Merkmalen, die
Nachweise für die genannten Daten, den Adapter, die Runtime und den
Prompt-/Edit-Workflow erfordert.

Die offizielle [FLUX.2 [klein] Trainingsdokumentation](https://docs.bfl.ai/flux_2/flux2_klein_training)
beschreibt LoRA-Feinabstimmung für die Modellfamilie einschließlich
Anwendungsfällen zur Charakterkonsistenz. Sie unterscheidet außerdem das
9B-Basismodell und seine Bedingungen von anderen Varianten. Das stützt ein
Experiment mit genau dem kompatiblen Release, nicht aber die Annahme, dass
Block-Auswahl, Rang-Reduktion, Adapter-Arithmetik oder das Rezept einer
anderen Modellfamilie unverändert übertragbar sind.

## Adapter und dessen Berechtigung festlegen {#bind-the-adapter-and-its-authority}

Für jeden Lauf sind festzuhalten:

- offizielle Kennung des Basismodells/Checkpoints, Artefakt-Digest, Lizenz- und
  Zugangsbedingungen, Modell-Runtime sowie Serialisierung und Ladepfad des Adapters;
- autorisierte Referenzmaterialien, Einwilligung oder sonstige
  Nutzungsberechtigung, Zweck, Aufbewahrungs- und Löschregeln, Captions,
  Trigger-Vokabular sowie ausgeschlossene Attribute oder Bereiche;
- Trainingssplit, Gruppierung nach Quelle/Derivat, Vorverarbeitung,
  Zuschnitt/Ausrichtung, Caption-Richtlinie, Augmentierungsrichtlinie,
  Code-/Konfigurationsstand und Seeds;
- vorgeschlagene Adapterdatei, Merge- und Stärkesteuerung, Ausgabe-Digest sowie
  der exakte für die Evaluierung verwendete Workflow; und
- Entscheidung der prüfenden Person mit Nachweisen zur Identitätsübereinstimmung,
  Nachweisen zur Erhaltung der Nicht-Ziel-Merkmale, Fehlerbeispielen und einer
  Schlussfolgerung zur zulässigen Nutzung.

Ein 9B-Adapter muss mit dem Modell-Release und der Runtime gepaart werden, für
die er trainiert wurde. Kompatibilität darf nicht aus einer ähnlichen
FLUX-Variante, einer Dateiendung oder einer Bezeichnung in einer
Community-Oberfläche abgeleitet werden.

## Trennung messen statt voraussetzen {#measure-separation-rather-than-assume-it}

Festzulegen ist, welche gewünschten Identitätsmerkmale übertragen werden dürfen
und welche Nicht-Ziel-Merkmale kontrollierbar bleiben müssen: Pose, Ausdruck,
wirkendes Alter, Kleidung, Hintergrund, Beleuchtung, Stil, Körper und
geschützte Attribute. Die gewünschte Übertragung ist getrennt von der Erhaltung
an zurückgehaltenen, quellenfremden Prompts und Referenzen zu evaluieren.
Autorisierte Korrekturen der prüfenden Personen sowie Negativfälle sind
aufzubewahren, insbesondere wenn ein Adapter einen Hintergrund wiederholt, einen
geschützten Bereich verändert oder eine ungewollte Ähnlichkeit erzeugt.

Block-Targeting, Rang-Auswahl, Orthogonalitätsverluste, Subtraktion, Merging und
SVD-Trunkierung sind modell- und implementierungsspezifische Experimente. Sie
benötigen eine erklärte Hypothese, eine fixierte Implementierung, eine
Vergleichsbasis und dieselbe Identitäts- und Erhaltungsprüfung; keines davon ist
ein universeller Bereinigungsschritt.

## Grenzen bei Fehlern {#failure-boundary}

Wenn Basis-Release oder Bedingungen unbekannt sind, die Referenzberechtigung
unvollständig ist, das Adapter-/Runtime-Format abweicht, Quellgruppen in die
Evaluierung gelangen oder eine prüfende Person gewünschte Übertragung nicht von
einer Nicht-Ziel-Änderung unterscheiden kann, ist der Adapter nicht zu
verwenden. Er darf nicht stillschweigend auf einer anderen Variante geladen,
Nachweise dürfen nicht entfernt und eine generierte Ähnlichkeit nicht als
verifizierte Identität gekennzeichnet werden.

## Verwandte Seiten {#related-pages}

- [[flux-klein-character-lora]]
- [[diffusion-lora-training]]
- [[lora-auxiliary-losses]]
- [[face-beautify-edit-lora]]
