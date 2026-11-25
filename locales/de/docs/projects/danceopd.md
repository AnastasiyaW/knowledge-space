---
title: "DanceOPD"
category: projects
date: 2026-06-26
tags: [danceopd, danceopd-development, project]
aliases: ["DanceOPD"]
level: 3
source_sha256: 4e76ddb15414128a47d49feb175dd5812017d99441a5964e6f481bb4ba024ceb
translation: machine
translated_at: '2026-10-24'
---
# DanceOPD {#danceopd}

**Entwicklungslinie:** `project:danceopd` · Thread `danceopd-development`  
**Letztes Ereignis:** 2026-06-26 · 1 datiertes Ereignis seit 2026-06-26 · **Recherchiert:** 2026-09-06 · Konfidenz: hoch

## Was es ist {#what-it-is}

DanceOPD ist ein Trainingsframework für Teams, die bereits kompatible Flow-Matching-Checkpoints oder LoRAs besitzen und einen einzelnen Student-Modell benötigen, das Text-zu-Bild- und Bildbearbeitungsverhalten kombiniert.

- Leitet jedes Sample hart an ein eingefrorenes Capability-Field weiter.
- Fragt einen Low-Noise-Zustand aus dem aktuellen Student-Rollout ab und gleicht die Velocity per MSE an.
- Dokumentiert SD3.5/Diffusers- und Z-Image/DiffSynth-Backends.

## Entwicklungslinie {#development-line}

- **2026-06-26 — Projektwebsite zu DanceOPD verlinkt.** Am 2026-06-26 ging die GitHub-Pages-Seite zu DanceOPD online. Die Seite verschaffte dem Projekt eine öffentliche Präsenz, der zugrunde liegende Quelltext war jedoch nicht verfügbar.

## Was sich geändert hat {#what-changed}

- 2026-06-25 — arXiv v1 wurde um 17:59:58 UTC eingereicht und erzeugte den kanonischen Preprint-Eintrag.
- 2026-06-26 — Das v1-Manuskript ist auf den 26. Juni datiert, und das öffentliche Repository wurde mit dem initialen Commit `init` geöffnet.
- 2026-06-30 — `Sync public release contents` fügte 59 Dateien mit 3.208 Ergänzungen und 76 Löschungen hinzu, darunter Code, Konfigurationen, Datenaufbereitung, Smoke-Skripte und Dokumentation.
- 2026-07-07 — arXiv v2 wurde ohne Revisionshinweis eingereicht, sodass die inhaltlichen Änderungen unbekannt bleiben.
- 2026-08-15 — arXiv v3 wurde eingereicht. DanceOPD 0.2.0 brachte aufgabengebundenes Teacher-Routing, drei Modi über SD3.5-M und Z-Image, lauffähige öffentliche Konfigurationen, Paper-Templates, Resume-Unterstützung, Dual-LoRA-Unterstützung und CFG-Field-Optionen.

## So wird es verwendet {#how-to-use-this}

1. Klone `worldbench/DanceOPD`, installiere das benötigte Extra-Set und führe `pip install -e ".[smoke]"` sowie `bash scripts/bootstrap_smoke.sh` aus.
  — <https://github.com/worldbench/DanceOPD>
2. Führe den Trockenlauf der SD3.5- oder Z-Image-Konfiguration aus, bevor echte Gewichte geladen werden. Installiere DiffSynth-Studio vor dem vollständigen Z-Image-Training.
  — <https://github.com/worldbench/DanceOPD>
3. Bereite einen gerouteten Prompt oder eine OmniEdit-CSV vor. Bearbeitungsrouten erfordern `source_image`, und Aufgaben zu Stil, Hintergrund oder Umgebung werden auf `global_edit` abgebildet, sofern nicht überschrieben.
  — <https://github.com/worldbench/DanceOPD>
4. Konfiguriere jeden eingefrorenen Teacher als Basis-Checkpoint, vollständigen Checkpoint, PEFT-LoRA oder Checkpoint-plus-LoRA. Halte die trainierbare Student-LoRA getrennt.
  — <https://github.com/worldbench/DanceOPD>
5. Verwende `configs/public`, um Code oder Paper-Templates mit kompatiblen Assets zu testen, und starte anschließend mit Accelerate; bei Bedarf wird ab einem gespeicherten Schritt fortgesetzt.
  — <https://github.com/worldbench/DanceOPD>

## Best Practices {#best-practices}

- Behandle den Smoke-Pfad als Prüfung der Codegesundheit, nicht als Beleg dafür, dass Paper-Metriken reproduziert werden.
  — <https://github.com/worldbench/DanceOPD>
- Behalte für DanceOPD selbst den dokumentierten Standard bei: ein hart geroutetes Teacher-Modell, eine Low-Noise-Abfrage (`K=1`) und direkte Velocity-MSE.
  — <https://github.com/worldbench/DanceOPD>
- Staple keine Teacher-LoRAs auf den trainierbaren Student-Adapter. Füge stattdessen jeden Teacher in ein sauberes, eingefrorenes Teacher-Modul zusammen.
  — <https://github.com/worldbench/DanceOPD>
- Belasse `student_cfg_scale=1.0`, wenn CFG absorbiert wird, passe die Teacher-Skalierung an und stimme die CFG bei der Inferenz separat ab, damit sich Effekte nicht verstärken.
  — <https://github.com/worldbench/DanceOPD>
- Halte herunterladbare öffentliche Ersatzressourcen getrennt von paper-konformen Templates; die Paper-Checkpoints bleiben nicht verfügbar.
  — <https://github.com/worldbench/DanceOPD>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-06-26 — Ein Verständnis, das nur auf der Projektseite beruhte, wurde durch die Code-Synchronisation am 2026-06-30 und das Toolkit 0.2.0 am 2026-08-15 abgelöst.
- 2026-08-15 — Ein undifferenzierter Reproduktionspfad ist veraltet: öffentliche Ersatz-Assets und paper-konforme Templates sind getrennt, und die Paper-Checkpoints bleiben unveröffentlicht.

## Weiterhin unbekannt {#still-unknown}

- Die Projektseite selbst hat keinen Veröffentlichungszeitstempel. Das Ereignis vom 26. Juni stützt sich auf das angezeigte Datum im Manuskript und die Repository-Historie, während arXiv v1 am 25. Juni (UTC) eingereicht wurde.
- arXiv liefert für v2 und v3 keine Änderungshinweise, daher bleiben Änderungen am Manuskript ungeprüft.
- Es wurde kein begutachteter Konferenz- oder Journal-Veröffentlichungsort verifiziert; arXiv führt die Arbeit als Technical Report.
- Es wurden keine offiziellen Hardwareanforderungen, Schätzungen der Trainingsdauer, deterministischen Seeds, gehosteten Inferenz-Endpunkte oder unabhängigen Reproduktionsnachweise verifiziert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://danceopd.github.io/ | DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://arxiv.org/html/2606.27377v1 | DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://arxiv.org/abs/2606.27377 | [2606.27377] DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://github.com/worldbench/DanceOPD | GitHub - worldbench/DanceOPD: DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://github.com/worldbench/DanceOPD/commits/main/ | Commits · worldbench/DanceOPD · GitHub | 2026-09-06 |
| https://github.com/worldbench/DanceOPD/commit/08f1230c013bf8fe21295cc95bd01e36e5c2a45b | Sync public release contents · worldbench/DanceOPD@08f1230 · GitHub | 2026-09-06 |
| https://raw.githubusercontent.com/worldbench/DanceOPD/main/CHANGELOG.md | DanceOPD CHANGELOG.md | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:danceopd`, Thread `danceopd-development`, 1 datiertes Ereignis vom 2026-06-26 bis 2026-06-26.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
