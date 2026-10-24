---
title: "FLOAT"
category: projects
date: 2025-07-21
tags: [float, float-public-releases, model_releases, project]
aliases: ["FLOAT"]
level: 3
source_sha256: ee43d90ef7842cc0e4a6c6f515bf382d58f3c6d058c5ba89b85f49163d4a9fcb
translation: machine
translated_at: '2026-10-24'
---
# FLOAT {#float}

**Entwicklungslinie:** `project:float` · Thread `float-public-releases`  
**Letztes Ereignis:** 2025-07-21 · 2 datierte Ereignisse seit 2024-12-05 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

FLOAT ist eine PyTorch-Forschungsimplementierung, die ein einzelnes, überwiegend frontales Porträt anhand von Sprachaudio animiert.

- Bewegungserzeugung in einem gelernten Bewegungs-Latent-Raum mit Flow Matching.
- Animation von Lippen-, Kopf- und ausdrucksstarker Bewegung aus Audio.
- Emotionsumlenkung und Bearbeitung der Kopfbewegung zur Testzeit.

Das veröffentlichte Paket ist nur für Inferenz gedacht, dient der Forschung und ist nicht kommerziell nutzbar. Getestet wurde unter Linux mit GPUs vom Typ A100 und V100.

Verwenden Sie es für reproduzierbare Forschungsdemos, nicht als kommerziell einsetzbaren Talking-Head-Stack.

## Entwicklungslinie {#development-line}

- **2024-12-05 — Projektseite von FLOAT wurde öffentlich.** FLOAT wurde als flow-matching-basierte, audiogesteuerte Erzeugung sprechender Porträts mit einem orthogonalen Bewegungs-Latent-Raum und sprachgesteuerter Emotion vorgestellt.
- **2025-07-21 — Repository von FLOAT und ergänzende Ressourcenlinks erschienen.** Das offizielle Repository und der Pfad zu den manuellen Checkpoints verwiesen auf diesen lauffähigen Inferenzpfad; eine neue benannte Modellversion haben wir nicht identifiziert.

## Was sich geändert hat {#what-changed}

FLOAT entwickelte sich von einer veröffentlichten Methode zu einem lauffähigen Inferenzpaket und danach zu einer überarbeiteten ICCV-Veröffentlichung, nicht zu einem versionierten Produkt-Release.

- 2024-12-05: FLOAT wurde als flow-matching-basierte, audiogesteuerte Erzeugung sprechender Porträts mit einem orthogonalen Bewegungs-Latent-Raum und sprachgesteuerter Emotion präsentiert.
- 2025-02-17: Das offizielle Repository veröffentlichte Inferenzcode und Checkpoints unter einer nicht-kommerziellen Lizenz, wodurch die Methode lauffähig wurde.
- 2025-06-26: Das Projekt meldete die Annahme bei der ICCV 2025.
- 2025-07-21: Das offizielle Repository und der Pfad zu den manuellen Checkpoints verwiesen auf diesen lauffähigen Inferenzpfad; wir identifizieren keine neue benannte Modellversion.
- 2025-09-19: arXiv v5 überarbeitete das Paper; es nennt kein neues Inferenz-Release.
- 2025-11-10: Die Historie des Main-Branches zeigt einen Update-Commit, dessen funktionale Änderung nicht dokumentiert ist; GitHub listet keine Releases.

Es gibt keine getaggte Modell-Release-Reihe und keinen veröffentlichten Trainingscode.

Behandeln Sie das Repository und seine Checkpoints als Forschungs-Code-Drop, nicht als gepflegten Release-Kanal.

## So verwenden Sie es {#how-to-use-this}

Stand 2025-07-21 sollten Sie das offizielle FLOAT-Repository, die verlinkte ergänzende Ressource und die Projektseite konsultieren, um FLOAT zu bewerten oder zu reproduzieren; überprüfen Sie den genauen Inhalt der Artefakte und die Nutzungsbedingungen separat.

1. Klonen Sie das offizielle Repository, erstellen Sie daraus die Conda-Umgebung mit Python 3.8.5 und installieren Sie anschließend den dokumentierten PyTorch-Build für CUDA 11.8 sowie die Requirements.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
2. Laden Sie die Checkpoints mit `sh download_checkpoints.sh` herunter und legen Sie die Checkpoint-Dateien für FLOAT, Wav2Vec2 und die Sprachemotions-Erkennung im dokumentierten Checkpoint-Verzeichnis ab.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
3. Bereiten Sie ein überwiegend frontales Einzelgesichts-Porträt und eine Sprachspur vor; beginnen Sie mit aktiviertem automatischem Gesichtszuschnitt.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
4. Führen Sie `generate.py` auf einem CUDA-Gerät mit `--ref_path`, `--aud_path`, `--seed 15`, `--a_cfg_scale 2`, `--e_cfg_scale 1` und `--ckpt_path ./checkpoints/float.pth` aus.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
5. Für einen expliziten Ausdruck fügen Sie `--emo` mit einem der Werte angry, disgust, fear, happy, neutral, sad oder surprise hinzu; passen Sie `--e_cfg_scale` erst nach einem Standardlauf an.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>

## Best Practices {#best-practices}

- Verwenden Sie zuerst ein frontales Porträt. Das Modell wurde auf Verteilungen frontaler Kopfhaltungen trainiert, und nicht-frontale Eingaben können die Qualität verringern.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Lassen Sie den automatischen Zuschnitt aktiviert, sofern kein gemessener Vergleich `--no_crop` rechtfertigt; ein Deaktivieren kann die Leistung verschlechtern, während der Standardzuschnitt schwarze Ränder hinzufügen kann.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Extrahieren Sie die Stimme vor der Inferenz, wenn das Audio viel Hintergrundmusik enthält; die Autoren verweisen dafür auf ClearVoice.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Beginnen Sie die Emotionssteuerung mit dem dokumentierten Standardwert 1; die Autoren schlagen 5–10 nur vor, wenn ein stärkerer Ausdruck erforderlich ist.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Beschränken Sie die Arbeit auf Forschungszwecke und planen Sie kein Fine-Tuning auf Basis des offiziellen Releases: Die Lizenz ist nicht-kommerziell, und die Autoren erklären, dass der Trainingscode nicht veröffentlicht wird.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>

## Hierdurch ersetzt {#superseded-by-this}

- Vor 2025-02-17: Hinweis, dass FLOAT nur eine Methode aus dem Paper bzw. von der Projektseite war und auf offiziellen Inferenzcode und Gewichte gewartet werden musste. Ersetzt durch das offizielle Release von Inferenzcode und Checkpoints.
- 2024-12-05: Eine reine Methodenbeschreibung ist als Einrichtungsanleitung nicht mehr ausreichend. Ersetzt durch die Anleitung im offiziellen README zu Umgebung, Checkpoints, Vorverarbeitung und CLI; der Checkpoint-Link vom 2025-07-21 ist ein Weg zu diesem lauffähigen Paket und kein Beleg für eine neu versionierte Modellversion.

## Weiterhin unbekannt {#still-unknown}

- Die bereitgestellte Google-Drive-URL des Checkpoints konnte nicht unabhängig gelesen werden; Dateiinhalte, Prüfsumme und die Frage, ob sie sich nach dem 2025-07-21 geändert hat, bleiben daher unverifiziert.
- Es existiert keine Dokumentation zu FLOAT in vereinfachtem Chinesisch von den Entwicklern; Ergebnisse Dritter auf Chinesisch wurden nicht als Beleg verwendet.
- Der jüngste sichtbare Commit vom 2025-11-10 trägt nur die Bezeichnung „update“; kein offizielles Changelog erklärt seine funktionale Wirkung.
- Das offizielle Material nennt weder die unterstützte Eingabedauer, die Ausgabeauflösung, den VRAM-Bedarf noch die Kompatibilität über das getestete Linux-Setup mit A100/V100 hinaus.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://deepbrainai-research.github.io/float/ | FLOAT project page | 2026-09-04 |
| https://github.com/deepbrainai-research/float | FLOAT official GitHub repository | 2026-09-04 |
| https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md | FLOAT README on the main branch | 2026-09-04 |
| https://arxiv.org/abs/2412.01064 | FLOAT: Generative Motion Latent Flow Matching for Audio-driven Talking Portrait | 2026-09-04 |
| https://github.com/deepbrainai-research/float/commits/main/ | FLOAT main-branch commit history | 2026-09-04 |
| https://github.com/deepbrainai-research/float/releases | FLOAT GitHub releases | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:float`, Thread `float-public-releases`, 2 datierte Ereignisse 2024-12-05 → 2025-07-21.
- **Praktischer Hinweis:** Stand 2025-07-21 sollten Praktiker bei der Bewertung oder Reproduktion von FLOAT neben der Projektseite auch das offizielle FLOAT-Repository und die verlinkte ergänzende Ressource konsultieren; überprüfen Sie den genauen Inhalt der Artefakte und die Nutzungsbedingungen separat.
- **Konfidenz:** mittel. Für die Frage, was veraltet ist, gelten die datierten Ersetzungshinweise oben als maßgeblich.
