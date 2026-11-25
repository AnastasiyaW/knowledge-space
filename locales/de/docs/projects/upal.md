---
title: "UPAL"
category: projects
date: 2026-08-24
tags: [project, upal, upal-development]
aliases: ["UPAL"]
level: 2
source_sha256: f3b3e8c50e66c233f25e57c02cb878ee8e7aa04a85e3a650c93565be30709856
translation: machine
translated_at: '2026-10-24'
---
# UPAL {#upal}

**Entwicklungslinie:** `project:upal` · Thread `upal-development`  
**Letztes Ereignis:** 2026-08-24 · 1 datiertes seit 2026-08-24 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

UPAL ist ein eigenständiger PyTorch-Feature-Extraktor für Praktiker in CV und SLAM. Er kombiniert Punkterkennung, Linienerkennung und lokale Deskriptoren in einem Netzwerk.

- Subpixel-Keypoints und Konfidenzwerte;
- 128-dimensionale, L2-normalisierte Deskriptoren;
- Keypoint-Heatmaps und Linien-Distanzfelder, mit mitgelieferter `points_lsd`-Nachbearbeitung für Segmente.

## Entwicklungslinie {#development-line}

- **2026-08-24 — UPAL-GitHub-Repository referenziert.** Das Repository war öffentlich erschienen, aber kein Commit, Tag oder Release aus erster Hand ist diesem Datum zugeordnet. Daher belegt es keine neue Version.

## Was sich geändert hat {#what-changed}

2026-08-20: arXiv v1 stellte UPAL als gemeinsam genutzten Backbone-Extraktor für Punkt- und Linienmerkmale mit öffentlichem Code vor. Berichtet wurden etwa 4× Beschleunigung und ein 10× kleinerer Speicherbedarf gegenüber ALIKED + DeepLSD. 2026-08-24: Das UPAL-Repository erschien öffentlich, aber kein Commit, Tag oder Release aus erster Hand ist diesem Datum zugeordnet, daher belegt es keine neue Version.

## So verwenden Sie es {#how-to-use-this}

Stand 2026-08-24 sollten Sie für Projektrecherchen vom UPAL-GitHub-Repository ausgehen, da die Belege keine engeren operativen Hinweise stützen.

1. Checken Sie das Repository aus, richten Sie eine Python-3.10+-Umgebung ein und installieren Sie das Paket mit `pip install -e .`.
  — <https://github.com/francois141/upal>
2. Initialisieren Sie rekursive Submodule und installieren Sie `third_party/points_lsd`. Für CUDA installieren Sie vor dem Bauen dieser Erweiterung den passenden PyTorch-Build.
  — <https://github.com/francois141/upal>
3. Führen Sie `demo_inference.py`, `demo_match_points.py` und `demo_match_lines.py` aus, um die unterstützten Pfade für Inferenz, Punkt-Matching und Linien-Matching zu testen.
  — <https://github.com/francois141/upal>
4. Um UPAL in einer Anwendung zu nutzen, laden Sie `weights/upal.tar`, übergeben Sie einen normalisierten Tensor im Bereich `[0,1]` mit der Form `B×1×H×W` oder `B×3×H×W` und lesen Sie Keypoints, Deskriptoren, Heatmaps und das Linien-Distanzfeld aus.
  — <https://github.com/francois141/upal>

## Bewährte Praktiken {#best-practices}

- Installieren Sie einen CUDA-kompatiblen PyTorch-Build, bevor Sie `points_lsd` kompilieren, da der Linienpfad von diesem nativen Submodul abhängt.
  — <https://github.com/francois141/upal>
- Testen Sie vor der Integration alle drei mitgelieferten Demos, da Inferenz, Punkt-Matching und Linien-Matching getrennte unterstützte Pfade sind.
  — <https://github.com/francois141/upal>
- Verallgemeinern Sie die Geschwindigkeitsangabe nicht auf andere Deployments: Das veröffentlichte Ergebnis von 70 ms wurde mit 500 sequenziellen 800×800-Bildern, Batchgröße eins und einer RTX 2080 Ti erzielt.
  — <https://arxiv.org/html/2608.19894v1>

## Abgelöst durch {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Weiterhin unbekannt {#still-unknown}

- Wir haben keinen Commit, Tag oder Release aus einer Primärquelle mit Datum 2026-08-24 gefunden, daher können wir dieses Datum nicht als Versionsveröffentlichung behandeln.
- Das Repository dokumentiert eigenständige Inferenz und Demos, nicht einen unterstützten Produktionsdienst, einen Trainings-Workflow oder eine Betriebssystem-Matrix.
- Wir haben keinen verifizierten Installationsbericht aus der Community gefunden, daher bleiben Builds in der Zielumgebung und die Leistung ungetestet.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://github.com/francois141/upal | GitHub - francois141/upal: Unified point and line detector | 2026-09-05 |
| https://arxiv.org/abs/2608.19894 | Unified and Efficient Point-Line Local Features | 2026-09-05 |
| https://arxiv.org/html/2608.19894v1 | Unified and Efficient Point-Line Local Features — arXiv HTML v1 | 2026-09-05 |
| https://www.x-techcon.com/article/178188.html | SLAM优化新方向：UPAL统一点线特征，提速4倍内存小10倍 | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:upal`, Thread `upal-development`, 1 datiertes Ereignis 2026-08-24 → 2026-08-24.
- **Praktischer Hinweis:** Stand 2026-08-24 sollten Sie für Projektrecherchen vom UPAL-GitHub-Repository ausgehen, da die Belege keine engeren operativen Hinweise stützen.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich für die Frage, was veraltet ist.
