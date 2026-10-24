---
title: "DRIFT — Projektressourcen"
category: projects
date: 2026-06-04
tags: [drift, project, project-resources]
aliases: ["DRIFT"]
level: 2
source_sha256: c2824fae4f4cda62c846a3db71bbe7cdf94ba32257f6613a6592ce27003585a9
translation: machine
translated_at: '2026-10-24'
---
# DRIFT — Projektressourcen {#drift-project-resources}

**Entwicklungslinie:** `project:drift` · Thread `project-resources`  
**Letztes Ereignis:** 2026-06-04 · 1 datiertes seit 2026-06-04 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

DRIFT ist ein offenes, auf Behauptungen (Claims) zentriertes Framework für Trajektorien von Deep-Research-Agenten. Es lokalisiert Spans, in denen eine nicht verifizierte oder widersprüchliche Behauptung schädlich wird.

Es umfasst Claim Keeper, Support Seeker und Dependency Tracer. TELBench stellt 1 000 von Experten verifizierte Trajektorien-Aufgaben aus 2 790 erfassten Läufen bereit.

Dies ist ein reproduzierbares Werkzeug, um Trajektorienprüfungen zu vergleichen und Fehler zu untersuchen, keine fertige Überwachungsschicht für einen laufenden Agenten.

## Entwicklungslinie {#development-line}

- **2026-06-04 — Projektseite und Repository zu DRIFT wurden verlinkt.** Am 2026-06-04 verlinkte eine datierte Meldung die Projektseite zu DRIFT und das zugehörige GitHub-Repository. Diese Meldung ordnet beide Ressourcen der Entwicklungslinie zu. Sie belegt weder ein Release, eine Version, eine technische Änderung noch einen Projektstart.

## Was sich geändert hat {#what-changed}

2026-06-04 — DRIFT und TELBench wurden als offene Artefakte für die Fehlerlokalisierung auf Span-Ebene in Trajektorien von Deep-Research-Agenten vorgestellt.

## So wird es genutzt {#how-to-use-this}

Ab dem 2026-06-04 sollte DRIFT anhand der verlinkten Projektseite und des GitHub-Repositorys bewertet werden. Das Ereignis belegt weder eine Installation noch eine Änderung des Workflows.

1. Repository klonen und das Paket im Editable-Modus installieren.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
2. Verschlüsseltes TELBench von Hugging Face herunterladen und mit dem mitgelieferten Skript entschlüsseln; das Skript prüft den SHA-256-Hash.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
3. OpenAI-kompatible Chat-Completions- oder Responses-API über Argumente oder eine Env-Datei konfigurieren. Anschließend `drift --setting drift` auf JSONL-Trajektorien ausführen.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
4. `summary.json` an `drift-eval` übergeben. Der Bericht gibt Macro- und Micro-Precision, Recall, F1, First-Error-Accuracy sowie fehlende und zusätzliche Identifikatoren aus.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>

## Bewährte Vorgehensweisen {#best-practices}

- Zuerst `bare` mit denselben Eingaben und demselben Modell ausführen, danach `drift`. Dieser von den Autoren vorgesehene Vergleich trennt den Effekt der auf Behauptungen zentrierten Pipeline vom Basismodell.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
- Die Prüfsumme des entschlüsselten TELBench kontrollieren. Heruntergeladene Artefakte, den Schlüssel und entschlüsselte JSONL-Dateien nicht in Git committen.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
- Keine Gold-Labels, Annotationen, Metadaten, Judge-Ausgaben oder manuellen Notizen an das Modell übergeben. Die Auswertung akzeptiert nur die Frage und die geordneten rohen Span-Texte.
  — <https://huggingface.co/datasets/NJU-LINK/TELBench>
- `--reasoning-effort low` für die Responses API beibehalten, sofern kein gemessener Grund für eine Änderung besteht. Das ist der Projektstandard für reine JSON-Prompts.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>

## Hiermit ersetzt {#superseded-by-this}

- Bisher ist nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Öffentliche Primärquellen bestätigen die Einreichung des Papers am 1. Juni 2026 und seine Überarbeitung v2 am 2. Juni. Sie verzeichnen kein eigenes DRIFT-Release am 4. Juni. Das Datum 4. Juni bleibt das Ereignisdatum, kein bestätigtes Release-Datum.
- Es gibt kein primäres, datiertes Changelog nach dem 4. Juni 2026, mit dem spätere Code- oder Datensatzänderungen benannt werden könnten.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://nju-link.github.io/DRIFT/ | DRIFT — Claim-zentrierte Trajektorienprüfung | 2026-09-05 |
| https://github.com/NJU-LINK/DRIFT | NJU-LINK/DRIFT-Repository | 2026-09-05 |
| https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md | DRIFT-Nutzungsanleitung | 2026-09-05 |
| https://huggingface.co/datasets/NJU-LINK/TELBench | NJU-LINK/TELBench-Dataset-Card | 2026-09-05 |
| https://arxiv.org/abs/2606.02060 | Where Do Deep-Research Agents Go Wrong? Span-Level Error Localization in Agent Trajectories | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:drift`, Thread `project-resources`, 1 datiertes Ereignis 2026-06-04 → 2026-06-04.
- **Praktischer Hinweis:** Ab dem 2026-06-04 sollten Praktiker, die DRIFT evaluieren, die verlinkte Projektseite und das GitHub-Repository als verfügbare Primärressourcen verwenden; diese Belege belegen keine Installations- oder Workflow-Änderung.
- **Konfidenz:** hoch. Datierte Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.
