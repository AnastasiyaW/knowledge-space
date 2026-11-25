---
title: "PAM — Öffentliche Veröffentlichung"
category: projects
date: 2026-03-26
tags: [pam, project, public-release]
aliases: ["PAM"]
level: 2
source_sha256: d9d5407255bb8648daa7ae9079cf1e45092923135a0671b060043777dfb36868
translation: machine
translated_at: '2026-10-24'
---
# PAM — Öffentliche Veröffentlichung {#pam-public-release}

**Entwicklungslinie:** `project:pam` · Strang `public-release`  
**Letztes Ereignis:** 2026-03-26 · 1 datiertes seit 2026-03-26 · **Recherchiert:** 2026-09-06 · Konfidenz: mittel

## Was es ist {#what-it-is}

PAM ist eine Forschungspipeline für Teams, die aus Simulationen Daten zu Hand-Objekt-Interaktionen erzeugen.

- Pose erstellt eine Trajektorie aus Start- und Ziel-MANO-Posen, der 6-DoF-Objektpose und dem Objektmesh.
- Appearance erzeugt das erste Frame aus Tiefenbild, Segmentierung und Handkeypoints.
- Motion wandelt die Bedingungen und das gewählte erste Frame in einen Videoclip um.

Die Autoren berichten 301,1 s für 40 Frames und einen Spitzenwert von 41,4 GB auf NVIDIA H20. Dies ist ein Offline-Generator für synthetische HOI-Daten und kein reiner Prompt-Videoendpunkt.

## Entwicklungslinie {#development-line}

- **2026-03-26 — Öffentliche Projektressourcen für PAM wurden bereitgestellt.** Die Projektwebseite, der Code und die Gewichtesammlung wurden miteinander verlinkt. Die Primärquelle bestätigt an diesem Tag keine neue Code- oder Gewichteveröffentlichung.

## Was sich geändert hat {#what-changed}

- 2025-12-04 — PAM: Hugging Face hat einen vierteiligen All-Condition-Motion-Checkpoint für OakInk2 hinzugefügt.
- 2026-03-23 — PAM: arXiv v1 stellte den dreistufigen Pose-Appearance-Motion-Ansatz vor.
- 2026-03-25 — PAM: arXiv v2 veröffentlichte Ergebnisse zu DexYCB und OAKINK2 vor dem Datum der Primärerwähnung.
- 2026-03-26 — PAM: Die Projektwebseite, der Code und die Gewichtesammlung wurden miteinander verlinkt, die Primärquelle bestätigt an diesem Tag jedoch keine neue Code- oder Gewichteveröffentlichung.
- 2026-04-02 — PAM: arXiv v3 aktualisierte den Eintrag; der Kommentar im Eintrag vermerkt die Annahme zur CVPR 2026.

## Wie man es verwendet {#how-to-use-this}

1. Prüfen Sie zuerst die Aufgabenpassung: PAM benötigt simulierte HOI-Geometrie und Posen, keinen einzelnen Text-Prompt.
  — <https://arxiv.org/html/2603.22193v2>
2. Wählen Sie ein datensatzspezifisches Artefakt, etwa `dexycb_all_cond` oder `oakink2_all_cond`, und fixieren Sie es, statt die Hub-Wurzel als einen einzelnen Checkpoint zu behandeln.
  — <https://huggingface.co/GasaiYU/PAM/tree/main>
3. Richten Sie die Umgebung aus `environment.yaml` ein, verwenden Sie CUDA 12.1 und installieren Sie `manopth`, wie es der offizielle Code verlangt.
  — <https://github.com/GasaiYU/PAM>
4. Bereiten Sie DexYCB oder OakInk2 vor: Video, vordergrundmaskierte Tiefe, Segmentierung, Handkeypoints, Beschriftungen und Dateilisten.
  — <https://github.com/GasaiYU/PAM>
5. Für Sim-to-Real übergeben Sie gerenderte GraspXL-RGB-, Normalen-, Tiefen-, Segmentierungs- und Keypoint-Daten, erzeugen und wählen das erste Frame aus und führen danach die Motion-Stufe über `testing/evaluation_sim.py` aus.
  — <https://github.com/GasaiYU/PAM>

## Best Practices {#best-practices}

- Behandeln Sie das automatisch erzeugte, rein promptbasierte Diffusers-Beispiel auf dem Hub nicht als verifiziertes Rezept: Verwenden Sie getrennte Artefakte und Eingangsbedingungen aus der Pipeline der Autoren.
  — <https://huggingface.co/GasaiYU/PAM/tree/main>
- Behalten Sie alle drei Bedingungen bei: Tiefe, Segmentierung und Handkeypoints. Die Ablationsstudie der Autoren zeigt das beste Ergebnis bei deren Kombination.
  — <https://arxiv.org/html/2603.22193v2>
- Prüfen Sie die Geometrie und filtern Sie das erste Frame, bevor die Motion-Stufe läuft: Kontaktfehler und ein schlechtes Referenzframe führen zu physikalisch unplausiblen Videos und zeitlichem Flackern.
  — <https://arxiv.org/html/2603.22193v3>
- Planen Sie den Lauf als rechenintensive Offline-Aufgabe ein: Ein vollständiger Durchlauf mit 40 Frames dauerte im Paper 301,1 s auf H20, und die Appearance-Stufe erreichte 41,4 GB.
  — <https://arxiv.org/html/2603.22193v3>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2026-04-02 — arXiv v1 (2026-03-23) und v2 (2026-03-25) sind für Zitation und Prüfung des Paper-Status durch die aktuelle Version v3 ersetzt.

## Weiterhin unbekannt {#still-unknown}

- Die Primärquelle liefert keinen überprüfbaren Zeitstempel für den Zustand der Projektwebseite, des GitHub-Repositorys und des vollständigen Hugging-Face-Baums am 2026-03-26; dieses Datum können wir nicht als Code- oder Gewichteveröffentlichung bezeichnen.
- Eine separate Gewichtelizenz und die Modellkarte der Autoren auf dem Hub sind nicht bestätigt; Apache-2.0 für den Quellcode belegt keine Bedingungen für einzelne Checkpoints.
- Es existiert keine unabhängige Replikation, die den aktuellen Code verifiziert; die berichteten Metriken und Ressourcenangaben bleiben Ergebnisse der Autoren.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://arxiv.org/html/2603.22193v2 | PAM: A Pose–Appearance–Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://arxiv.org/abs/2603.22193v2 | [2603.22193v2] PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://arxiv.org/html/2603.22193v3 | PAM: A Pose–Appearance–Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://arxiv.org/abs/2603.22193v3 | [2603.22193v3] PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://github.com/GasaiYU/PAM | GitHub - GasaiYU/PAM: PAM: A Pose–Appearance–Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://huggingface.co/GasaiYU/PAM/tree/main | GasaiYU/PAM at main | 2026-09-06 |
| https://huggingface.co/GasaiYU/PAM/commit/1253ebb77e4b9ad9506aed5a770bfa2b1ffbc1a9 | Upload folder using huggingface_hub · GasaiYU/PAM at 1253ebb | 2026-09-06 |

## Agenten-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:pam`, Strang `public-release`, 1 datiertes Ereignis vom 2026-03-26 → 2026-03-26.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Verwendung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.
