---
title: "X-Dub — Projektentwicklung"
category: projects
date: 2026-03-28
tags: [project, project-development, x-dub]
aliases: ["X-Dub"]
level: 2
source_sha256: be448c0db046accdf5235432e68e73671ae54d790f4d54d18664c4b5168389d6
translation: machine
translated_at: '2026-10-24'
---
# X-Dub — Projektentwicklung {#x-dub-project-development}

**Entwicklungslinie:** `project:x-dub` · Thread `project-development`  
**Letztes Ereignis:** 2026-03-28 · 1 datiertes Ereignis seit 2026-03-28 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

X-Dub ist eine Veröffentlichung unter Apache-2.0 mit Code und Gewichten für die Lippensynchronisation von Video auf Audio. Das öffentliche Modell X-Dub (Wan-5B) basiert auf Wan2.2-TI2V-5B und nicht auf dem internen X-Dub (internal-1B) aus dem Paper.

- Bearbeitung der Mundbewegung: synchronisiert die Mundbewegung im Video mit dem bereitgestellten Audio.
- Unterstützung von Figuren: verarbeitet menschliche und nicht-menschliche Gesichter.
- Gesichtszuschnitt: schneidet den Kopfbereich automatisch zu.

Die typische Inferenz benötigt etwa 21 GB VRAM und unterstützt derzeit eine Person pro Video. Einsetzbar ist es für lokales Nachvertonen mit einem einzelnen Subjekt, wenn der GPU-Speicher ausreicht und gelegentliches Flackern oder Identitätsdrift akzeptabel sind.

## Entwicklungslinie {#development-line}

- **2026-03-28 — Öffentliche Projektressourcen von X-Dub wurden verlinkt.** Am 2026-03-28 verlinkte ein datierter X-Dub-Eintrag die Projektwebsite, das GitHub-Repository und die Hugging-Face-Seite. Die Links bestätigen öffentlich verfügbaren Code und Gewichte, führen aber weder eine neue Veröffentlichung, Version noch eine technische Änderung ein.

## Was sich geändert hat {#what-changed}

- 2025-12-31 — Das Paper und die Projektseite stellten ContextDubBench und die selbstbootstrappende, maskenfreie Methode für visuelles Dubbing vor.
- 2026-03-19 — Inferenzcode und vortrainierte Gewichte für die öffentliche, auf Wan basierende X-Dub-Veröffentlichung wurden veröffentlicht.
- 2026-03-28 — X-Dub wurde über die Projektseite, das GitHub-Repository und die Hugging-Face-Gewichte verfügbar.
- 2026-05-15 — Das Projekt meldete die Annahme bei der ICML 2026.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-03-28 sollten Sie bei der Bewertung öffentlicher Ressourcen die Projektseite von X-Dub, das GitHub-Repository und die Hugging-Face-Seite heranziehen. Der verlinkte Eintrag stellt Code und Gewichte bereit, aber kein eigenständiges Einrichtungsverfahren.

1. Klonen Sie das offizielle Repository, legen Sie eine Conda-Umgebung mit Python 3.10 an und installieren Sie die aufgelisteten Abhängigkeiten für Python, OpenMMLab und das editierbare Projekt.
  — <https://github.com/KlingAIResearch/X-Dub>
2. Laden Sie `KlingTeam/X-Dub` nach `checkpoints/` herunter und verschieben Sie anschließend die mitgelieferten DWPose-Modelle nach `dwpose_tools/models/`.
  — <https://github.com/KlingAIResearch/X-Dub>
3. Führen Sie `infer_lip_sync_pipeline.py` aus, mit einem Video, dem Ersatz-Audio, `X-Dub_model.safetensors`, dem Ausgabeverzeichnis sowie den Anfangseinstellungen `ref_cfg_scale=2.5`, `audio_cfg_scale=10.0` und 30 Inferenzschritten.
  — <https://github.com/KlingAIResearch/X-Dub>
4. Prüfen Sie die Ausgabe auf Zittern des Zuschnitts, Flackern, Farbdrift und verrauschte Frames, bevor Sie bearbeitete Medien veröffentlichen.
  — <https://github.com/KlingAIResearch/X-Dub>

## Bewährte Vorgehensweisen {#best-practices}

- Verwenden Sie Aufnahmen mit einer einzelnen Person und einem Gesicht, das nachverfolgbar bleibt. Online-DWPose verliert schnell bewegte Köpfe und versagt bei Szenen mit mehreren Personen.
  — <https://github.com/KlingAIResearch/X-Dub>
- Beginnen Sie mit 25–50 Inferenzschritten. Mehr Schritte kosten Laufzeit und sind nicht umfassend evaluiert.
  — <https://github.com/KlingAIResearch/X-Dub>
- Passen Sie `ref_cfg_scale` und `audio_cfg_scale` für jeden Clip an, um die Treue zum Referenzerscheinungsbild gegen die audiogesteuerte Mundbewegung abzuwägen.
  — <https://github.com/KlingAIResearch/X-Dub>
- Kennzeichnen Sie generierte oder bearbeitete Medien eindeutig. Verwenden Sie das System nicht für täuschende Identitätsimitation.
  — <https://github.com/KlingAIResearch/X-Dub>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-03-19 — Das interne X-Dub (internal-1B) aus dem Paper ist nicht die herunterladbare Implementierung. Die öffentliche Veröffentlichung ist X-Dub (Wan-5B), die das Backbone austauscht und statt LoRA-Tuning mehrstufiges SFT verwendet.
- 2026-03-19 — Gehen Sie im Produktivbetrieb nicht von Parität mit dem Modell aus dem Paper aus. Die öffentliche Veröffentlichung läuft etwa doppelt so langsam, kann flackern oder driften und meldet in etwa 2 % der Fälle schwer verrauschte Frames.

## Weiterhin unbekannt {#still-unknown}

- Keine Primärquelle ordnet dem 2026-03-28 eine bestimmte Produktänderung zu. Das offizielle Repository datiert die öffentliche Veröffentlichung auf 2026-03-19. Wir werten den 2026-03-28 als Bestätigung der Verfügbarkeit, nicht als eigene Modellversion.
- Das öffentliche Repository kündigt quantitative Vergleiche mit dem internen Modell aus dem Paper für ein späteres Update an; ein solcher Vergleich wurde hier nicht überprüft.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://hjrphoebus.github.io/X-Dub/ | X-Dub: From Inpainting to Editing: A Self-Bootstrapping Framework for Context-Rich Visual Dubbing | 2026-09-05 |
| https://github.com/KlingAIResearch/X-Dub | KlingAIResearch/X-Dub — offizielles Repository | 2026-09-05 |
| https://huggingface.co/KlingTeam/X-Dub | KlingTeam/X-Dub — Modellkarte und Gewichte | 2026-09-05 |
| https://arxiv.org/abs/2512.25066 | From Inpainting to Editing: A Self-Bootstrapping Framework for Context-Rich Visual Dubbing | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:x-dub`, Thread `project-development`, 1 datiertes Ereignis 2026-03-28 → 2026-03-28.
- **Praktischer Hinweis:** Stand 2026-03-28 sollten Praktiker bei der Bewertung des Projekts oder beim Auffinden seiner öffentlichen Ressourcen die Projektseite von X-Dub, das GitHub-Repository und die Hugging-Face-Seite heranziehen; diese Belege begründen keine bestimmte Einrichtungs- oder Nutzungsanleitung.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich für die Frage, was veraltet ist.
