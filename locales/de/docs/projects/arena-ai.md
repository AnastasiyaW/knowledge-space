---
title: "Arena.ai — Agent Mode"
category: projects
date: 2026-06-04
tags: [agent-mode, arena-ai, arena_ai, project]
aliases: ["Arena.ai"]
level: 3
source_sha256: 2be68514e30a62d82567888e1529a44a3351d43125f96a6f78927e8a2f3f413f
translation: machine
translated_at: '2026-10-24'
---
_placeholder_check: The input contains no @@CODE_n@@ placeholders, so none need preserving.

---
title: Arena.ai — Agent Mode
category: projects
date: 2026-06-04
tags: [agent-mode, arena-ai, arena_ai, project]
aliases: ["Arena.ai"]
---

# Arena.ai — Agent Mode {#arenaai-agent-mode}

**Entwicklungslinie:** `project:arena-ai` · Thread `agent-mode`  
**Letztes Ereignis:** 2026-06-04 · 1 datiertes Ereignis seit 2026-06-04 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Arena.ai Agent Mode ist ein Browser-Arbeitsbereich für mehrstufige Aufgaben und nicht nur für isolierte Chat-Antworten.

- Plant Aufgaben und führt sie mit Websuche, Bildgenerierung, Uploads, Code-Unterstützung und einer sandboxed Bash aus.
- Verbindet ein GitHub-Repository, das in eine Sandbox geklont wird, zeigt Diffs an und erstellt Pull Requests.
- Leitet jede Sitzung zufällig an ein nicht offengelegtes Orchestrator-Modell weiter.

Eine Repository-Sitzung erstellt nur einen einzigen Pull Request und kann nach dem Mergen oder Schließen keine weiteren Arbeiten mehr pushen.
Verwenden Sie sie für abgegrenzte Ergebnisse, die wir prüfen können; das Leaderboard spiegelt die Umgebung von Arena wider und ist keine allgemeingültige Garantie.

## Entwicklungslinie {#development-line}

- **2026-06-04 — Arena.ai dokumentierte ein Entwicklungsupdate zu Agent Mode.** Arena.ai startete Agent Mode mit werkzeuggestützten, mehrstufigen Workflows und einem Agent-Arena-Leaderboard, das auf echten Sitzungstraces basiert.

## Was sich geändert hat {#what-changed}

- 2026-06-04: Arena.ai startete Agent Mode mit einem werkzeuggestützten, mehrstufigen Workflow und dem Agent-Arena-Leaderboard, abgeleitet aus echten Sitzungstraces.
- 2026-06-29: Arena meldete mehr als 5 Mio. Agent-Mode-Turns pro Monat und 10 % Wachstum gegenüber der Vorwoche.
- 2026-08-14: Agent Arena erhielt Filter für Code, Chat und Work sowie Ansichten für Kosten pro Aufgabe und Pareto.
- 2026-08-24: Agent Mode erhielt GitHub-gestütztes Programmieren mit Sandbox-Klonen, Live-Diffs, Commits, Pushes und Pull Requests.

## So wird es genutzt {#how-to-use-this}

Ab 2026-06-04 sollten Praktiker, die Arena.ai evaluieren, den Agent-Mode-Workflow und die Agent-Produktoberfläche als Teil ihrer Tool-Bewertung prüfen; die Fähigkeiten sollten sie jedoch direkt verifizieren, da diese Entwicklungslinie keine recherchierten Funktionsnachweise enthält.

1. Öffnen Sie Agent Mode direkt.
  — <https://arena.ai/agent>
2. Beschreiben Sie das gewünschte mehrstufige Ergebnis, hängen Sie relevante Dateien an und starten Sie den Workflow über die Chat-Leiste.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>
3. Verwenden Sie Workspace, um Ergebnisse abzurufen: Laden Sie ein ZIP ohne Repository herunter oder prüfen Sie den Diff und den Pull Request, wenn ein Repository verbunden ist.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>
4. Für Repository-Arbeit verbinden Sie GitHub, wählen die Organisationen und Repositories aus, auf die Arena zugreifen darf, und aktivieren GitHub in Agent Mode.
  — <https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode>
5. Prüfen Sie den Diff und die automatisierten Checks vor dem Mergen; halten Sie die Aufgabe innerhalb des aktuellen Limits von einem Pull Request pro Chat.
  — <https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode>

## Best Practices {#best-practices}

- Verwenden Sie Agent Mode für verbundene Recherche, Programmierung, Analyse oder Iteration; verwenden Sie Battle, Side-by-Side oder Direct für eine einfache Einzelschritt-Anfrage.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>
- Wählen Sie ein Agentenmodell in der passenden Ansicht Code, Chat oder Work und vergleichen Sie die Aufgabenkosten, anstatt einen einzelnen Gesamtrang als allgemeingültig zu behandeln.
  — <https://arena.ai/blog/agent-categories-and-cost>
- Beschränken Sie bei GitHub-Arbeiten eine Sitzung auf einen überprüfbaren Pull Request und prüfen Sie sowohl den Diff als auch die Checks vor dem Merge.
  — <https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode>
- Pushen oder laden Sie Arbeiten herunter, bevor Sie einen Pull Request mergen oder schließen, da die Sitzung nach diesem abgeschlossenen Workflow keine weiteren Dateien mehr liefern kann.
  — <https://help.arena.ai/articles/5432423882-how-to-use-agent-mode>

## Abgelöst durch diese Entwicklung {#superseded-by-this}

- Seit 2026-08-14 ist die Auswahl eines Agent-Arena-Modells allein anhand des einzelnen Gesamtrankings unvollständig; verwenden Sie die Kategorie- und Kostenansichten.
- Seit 2026-08-24 ist die Beschreibung von Agent Mode als Sandbox ohne Repository-Auslieferungs-Workflow veraltet; es kann GitHub-Repositories verbinden und Pull Requests erstellen.

## Noch unbekannt {#still-unknown}

- Arena legt das Orchestrator-Modell nach Feedback nicht offen, daher lässt sich eine abgeschlossene Sitzung über die hier beschriebene öffentliche Oberfläche nicht einem benannten Modell zuordnen.
- Die geprüften Quellen belegen weder Preise, Ratenlimits, Aufbewahrungsdauer noch eine Service-Level-Zusage für Agent Mode.
- Repository-Berechtigungen und das Live-Auslieferungsverhalten wurden nicht direkt in einer angemeldeten Sitzung getestet.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| http://arena.ai/blog/agent-mode/ | Empowering Users to Get More Done With Agent Mode | 2026-09-05 |
| https://arena.ai/agent | Agent Mode | Autonomous AI Agents for Real-World Tasks | 2026-09-05 |
| https://arena.ai/blog/agent-arena-methodology | Agent Arena: Causal Evaluation of Agents in the Real World | 2026-09-05 |
| https://help.arena.ai/articles/5432423882-how-to-use-agent-mode | How to use Agent Mode on Arena | 2026-09-05 |
| https://arena.ai/blog/arena-100m-revenue | Arena Reaches $100M in 8 Months | 2026-09-05 |
| https://arena.ai/blog/agent-categories-and-cost | Agent Leaderboard Improvements: Categories & Task Cost | 2026-09-05 |
| https://arena.ai/blog/coding-in-agent-mode | Coding in Agent Mode: From Idea to Shipping with GitHub | 2026-09-05 |
| https://help.arena.ai/articles/1655691990-how-to-use-coding-in-agent-mode | How to use coding in Agent Mode | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:arena-ai`, Thread `agent-mode`, 1 datiertes Ereignis 2026-06-04 → 2026-06-04.
- **Praktischer Hinweis:** Ab 2026-06-04 sollten Praktiker, die Arena.ai evaluieren, den Agent-Mode-Workflow und die Agent-Produktoberfläche als Teil ihrer Tool-Bewertung prüfen; die Fähigkeiten sollten sie jedoch direkt verifizieren, da diese Entwicklungslinie keine recherchierten Funktionsnachweise enthält.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
