---
title: "X-Dub: Öffentliches maskenfreies Visual Dubbing"
description: "X-Dub ist eine öffentlich verfügbare Visual-Dubbing-Veröffentlichung auf Basis von Wan2.2-TI2V-5B; validieren Sie bei jedem Zielvideo Single-Person-Cropping, Identität, zeitliche Stabilität, Audiorechte und Modellbedingungen."
category: models
tags: [visual-dubbing, lip-sync, video-editing, wan2.2, audio-driven, generative-bootstrapping, synthetic-media]
aliases: ["X-Dub Wan-5B"]
level: 2
source_sha256: 2a5a84f96014f1d39f81709e61aa2c2e1fce870f70a5fb728e4111331768796d
translation: machine
translated_at: '2026-10-24'
---
# X-Dub: Öffentliches maskenfreies Visual Dubbing {#x-dub-public-mask-free-visual-dubbing}

**Stand der Prüfung: 2026-09-04.** X-Dub ist die öffentliche Implementierung eines Visual-Dubbing-Verfahrens, das ein Video mit ersetzendem Audio synchronisiert. Das ursprüngliche Verfahren behandelt die Aufgabe als maskenfreie Bearbeitung, die durch generative Bootstrapping-Verfahren trainiert wird. Es soll sprachbezogene Bewegungen verändern und den übrigen Teil des Videos beibehalten, wobei die Beibehaltung jedoch ein Abnahmeziel und keine Garantie ist.

## Öffentliche Veröffentlichung im Vergleich zum Paper-Modell {#public-release-versus-the-paper-model}

Die Maintainer unterscheiden ausdrücklich zwischen der veröffentlichten X-Dub-(Wan-5B)-Version und dem internen Modell, das im Paper evaluiert wurde. Die öffentliche Version nutzt einen Stack auf Basis von Wan2.2-TI2V-5B sowie mehrstufiges überwachtes Feintuning; das interne Modell und sein LoRA-Tuning sind nicht veröffentlicht.

Übertragen Sie keine quantitativen Aussagen, Qualitätserwartungen oder Einstellungen aus dem internen Paper-Modell auf den öffentlichen Checkpoint. Das öffentliche Repository selbst dokumentiert verbleibende Einschränkungen bei zeitlicher Konsistenz und Konsistenz des Subjekts und vermerkt, dass ein quantitativer Vergleich noch aussteht.

## Grenzen der aktuellen Laufzeit {#current-runtime-boundary}

Das offizielle Repository enthält eine Inferenz-Pipeline, ein Modellpaket, Audiokomponenten und Unterstützung für Gesichtszuschnitte. Der aktuelle Online-Zuschnittpfad ist für Videos mit **einer einzelnen Person** vorgesehen. Er schneidet das Gesicht aus, führt das Dubbing auf dem Ausschnitt aus und bildet das Ergebnis anschließend auf das ursprüngliche Video ab.

Dieser Komfortpfad ist kein Multi-Personen-Tracker. Schnelle Kopfbewegungen, Verdeckungen oder unzuverlässiges Crop-Tracking können Jitter, Identitätsdrift, Farbdrift oder fehlerhafte Frames verursachen. Behandeln Sie jede Ausgabe als Kandidatenclip, der einer Prüfung bedarf.

## Sicherer Produktions-Workflow {#safe-production-workflow}

1. Prüfen Sie Rechte und Einwilligung für das Quellvideo, das Ersatz-Audio und jede abgebildete Person oder Figur.
2. Frieren Sie die exakte Repository-Revision, Gewichte, Abhängigkeiten, Eingangsvideo, Eingangsaudio und Inferenzeinstellungen ein.
3. Führen Sie einen kurzen repräsentativen Abschnitt aus, bevor Sie ein vollständiges Asset verarbeiten.
4. Prüfen Sie die Ausgabe Frame für Frame um Sprachpassagen, Schnitte, Verdeckungen, schnelle Bewegungen und die Zuschnittgrenze.
5. Vergleichen Sie Identität, Beleuchtung, Farbe, Hintergrund und Bewegungen außerhalb des Mundbereichs mit der Quelle.
6. Bewahren Sie Quelle, Ausgabe, Konfiguration, Logs und, wo angebracht, eine eindeutige Kennzeichnung als synthetische Medien auf.

Verwenden Sie ein generiertes Dubbing-Ergebnis niemals als Beleg dafür, dass eine echte Person etwas gesagt hat. Bei öffentlichem, kommerziellem oder sensiblem Material fügen Sie eine menschliche Freigabestufe hinzu und befolgen Sie die jeweils geltenden Regeln zu Einwilligung, Offenlegung und Plattformen.

## Validierungsmatrix {#validation-matrix}

| Risiko | Erforderlicher Nachweis |
|---|---|
| Lippen-/Audio-Ausrichtung | mehrere Sprachsegmente mit dem vorgesehenen Audio prüfen |
| Identität und Erscheinungsbild | Vergleich Quelle/Ausgabe in der Auslieferungsauflösung |
| Zeitliche Stabilität | fortlaufende Prüfung über Schnitte, schnelle Wendungen und Verdeckungen |
| Korrektheit des Zuschnitts | prüfen, dass ausschließlich das vorgesehene Gesicht ausgewählt wurde |
| Reproduzierbarkeit | Digests von Quelle und Audio, Modellrevision, Einstellungen und Ausgabe-Beleg |

## Lizenzierung und Bedingungen für Artefakte {#licensing-and-artifact-terms}

Das Code-Repository, das Wan-Backbone, das Checkpoint-Paket, die Audiomodell-Komponenten und jede Community-Integration können jeweils eigene Bedingungen haben. Prüfen Sie die aktuellen Bedingungen und Weitergabebestimmungen für jedes heruntergeladene Artefakt; leiten Sie die Berechtigung zum Deployment nicht aus einer einzelnen Repository-Bezeichnung ab.

## Referenzen {#references}

- [X-Dub official repository](https://github.com/KlingAIResearch/X-Dub)
- [X-Dub project page](https://hjrphoebus.github.io/X-Dub/)
- [X-Dub paper](https://arxiv.org/abs/2512.25066)
- [X-Dub model collection](https://huggingface.co/KlingTeam/X-Dub)
