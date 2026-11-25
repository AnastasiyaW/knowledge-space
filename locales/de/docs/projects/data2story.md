---
title: "Data2Story — Agentic Data Storytelling"
category: projects
date: 2026-06-16
tags: [agentic-data-storytelling, agentic_data_storytelling, data2story, project]
aliases: ["Data2Story"]
level: 2
source_sha256: 215eecd4d399fe72596b19705b057ab188bb3f21c4be64ce41dc2dd90a1a9308
translation: machine
translated_at: '2026-10-24'
---
# Data2Story — Agentic Data Storytelling {#data2story-agentic-data-storytelling}

**Entwicklungslinie:** `project:data2story` · Thread `agentic-data-storytelling`  
**Letztes Ereignis:** 2026-06-16 · 1 datiertes Ereignis seit 2026-06-16 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Data2Story wandelt eine CSV-Datei, einen Datenordner, ein Paper oder eine Idee in Pro in eine in sich geschlossene HTML-Story um. Dabei erzeugt es Diagramme und Medien zusammen mit einem Evidenz-Viewer.

- Sieben Newsroom-Rollen strukturieren die kanonische Entwurfspipeline.
- Claim-Tracing verknüpft jede Aussage und jede Visualisierung mit Daten, Code oder Zitaten.
- Pro ergänzt einen Workflow mit 14 Agenten und eine Neuberechnung direkt in der Seite.

Das Paper evaluierte 18 Artikel mit 53 Teilnehmenden.
Einsetzen sollte man es, wenn die Nachvollziehbarkeit von Evidenz eine Liefervoraussetzung ist, nicht um redaktionelles Urteilsvermögen zu ersetzen.

## Entwicklungslinie {#development-line}

- **2026-06-16 — Data2Story wurde öffentlich mit seiner Website und seinem GitHub-Repository verknüpft.** Am 2026-06-16 verbanden öffentliche Links Data2Story mit der Projektwebsite und dem GitHub-Repository data2story-skill. Dies setzt den Bezugspunkt für die Entwicklungslinie zu agentic Data Storytelling, ohne ungeprüfte Funktionen zu behaupten.

## Was sich geändert hat {#what-changed}

- 2026-05-11 — Data2Story wurde als Spotlight-Paper beim Workshop der ACM Conference on AI and Agentic Systems angenommen.
- 2026-06-09 — Paper und Repository wurden veröffentlicht. Die kanonische Implementierung etablierte eine sequenzielle Newsroom-Struktur mit sieben Rollen und evaluierte 18 Artikel mit 53 Teilnehmenden.
- 2026-06-16 — Data2Story wurde öffentlich als Workflow von Datensatz zu überprüfbarer Story vorgestellt. Der Inspector verfolgt jede Aussage und jede Visualisierung zurück zu Daten, Code oder Referenzen.
- 2026-06 — Version 0.1.0 optimierte visuelle Effekte. Das Repository kennzeichnet data2story-pro als die umfangreichere Implementierung neben dem paperreproduzierbaren Skill mit sieben Rollen.

## Anwendung {#how-to-use-this}

Stand 2026-06-16 dienen die Projektwebsite und das GitHub-Repository als Ausgangspunkte für agentic Data Storytelling.

1. Repository klonen oder öffnen und dann den kanonischen Skill `data2story` verwenden, wenn die siebenstufige Pipeline des Papers reproduziert werden soll.
  — <https://github.com/QinghongLin/data2story-skill>
2. Eine CSV-Datei, eine JSON-Datei, ein Datenverzeichnis, ein Paper oder – in Pro – eine Idee oder eine URL bereitstellen und den Orchestrator mit dieser Eingabe ausführen.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story-pro/README.md>
3. `index.html` für den Artikel öffnen und Aussagen über `viewer.html` im kanonischen Skill oder über den Inspector in der Seite in Pro prüfen.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story/SKILL.md>

## Best Practices {#best-practices}

- Die festen Stufen in der vorgegebenen Reihenfolge ausführen und erst fortfahren, wenn das vorherige Artefakt vollständig ist.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story/SKILL.md>
- Die exakt verwendeten Skills jedes Laufs archivieren, damit ein Ergebnis nachvollziehbar und erneut prüfbar bleibt.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story/SKILL.md>
- Den Idea-Modus von Pro nur verwenden, wenn er einen echten Datensatz beschaffen und validieren kann; er bricht ab, statt unterstützende Daten zu erfinden.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story-pro/README.md>
- Die veröffentlichte Laufzeit von Pro als Planungsschätzung behandeln: `--fast` wird mit etwa 15–25 Minuten angegeben, der Premium-Modus mit etwa 2 Stunden 40 bis 50 Minuten.
  — <https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story-pro/README.md>

## Abgelöst durch dies {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Die Update-Notizen des Repositorys nennen für Version 0.1.0 nur den Monat, der genaue Veröffentlichungstag ist daher nicht überprüft.
- Keine Quelle aus erster Hand belegt die laufenden Betriebskosten, modellspezifische Standardeinstellungen für die Medienerzeugung oder ein formelles Changelog für Data2Story Pro.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://data2story.github.io/ | Data Journalist Agent (Data2Story) | 2026-09-05 |
| https://github.com/QinghongLin/data2story-skill | Repository QinghongLin/data2story-skill | 2026-09-05 |
| https://arxiv.org/abs/2606.11176 | Data Journalist Agent: Transforming Data into Verifiable Multimodal Stories | 2026-09-05 |
| https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story/SKILL.md | Data2Story kanonischer Skill-Orchestrator | 2026-09-05 |
| https://raw.githubusercontent.com/QinghongLin/data2story-skill/main/skills/data2story-pro/README.md | Data2Story Pro README | 2026-09-05 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:data2story`, Thread `agentic-data-storytelling`, 1 datiertes Ereignis 2026-06-16 → 2026-06-16.
- **Praxishinweis:** Stand 2026-06-16 können Praktikerinnen und Praktiker die angegebene Projektwebsite und das GitHub-Repository als Ausgangspunkte nutzen, wenn sie Data2Story für Arbeiten an agentic Data Storytelling bewerten.
- **Konfidenz:** hoch. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
