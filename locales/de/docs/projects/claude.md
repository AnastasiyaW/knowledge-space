---
title: "Claude"
category: projects
date: 2023-11-22
tags: [claude, claude-product-development, project]
aliases: ["Claude", "Claude 2.1"]
level: 3
source_sha256: a8a04f472bec5ade180774636412dabe07dbd67f03a8bc9e6c372eed999d5d8f
translation: machine
translated_at: '2026-10-24'
---
# Claude {#claude}

**Entwicklungslinie:** `project:claude` · Thread `claude-product-development`  
**Letztes Ereignis:** 2023-11-22 · 2 datierte seit 2023-05-12 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Claude ist Anthropics Modellfamilie für Chat-Nutzer, Anwendungsentwickler und Softwareteams.

- Text und Bilder: nimmt Text und Bilder entgegen und gibt Text zurück.
- Fähigkeiten: unterstützt mehrsprachige Aufgaben, Bildverarbeitung, Tool-Nutzung und Workflows mit langem Kontext.
- Oberflächen: läuft über Chat, die Messages API und Claude Code für Arbeit mit Repositories.

## Entwicklungslinie {#development-line}

- **2023-05-12 — Claude erweitert auf Kontextfenster mit 100K Token.** Claude wuchs in der 100K-Context-Version von 9K auf 100K Token, damit Prompts ganze Dokumente und vollständige Codebases aufnehmen können. Der offizielle Artikel ist auf 2023-05-11 datiert.
- **2023-11-22 — Claude 2.1 führte ein Kontextfenster mit 200K Token ein.** Claude 2.1 hob das Limit auf 200K Token an, ergänzte Systemprompts und Tool-Nutzung in der Beta und senkte falsche Aussagen. Der offizielle Artikel ist auf 2023-11-21 datiert.

## Was sich geändert hat {#what-changed}

Claude — die datierte Entwicklungslinie:

- 2023-05-12: Die 100K-Context-Version erweiterte Claude von 9K auf 100K Token, damit Prompts ganze Dokumente und Codebases aufnehmen können. Der offizielle Artikel ist auf 2023-05-11 datiert.
- 2023-11-22: Claude 2.1 hob das Limit auf 200K Token an, ergänzte Systemprompts und Tool-Nutzung in der Beta und senkte die Rate falscher Aussagen. Der offizielle Artikel ist auf 2023-11-21 datiert.
- 2026-09-04 (heute gefunden): Die aktuelle Dokumentation beschreibt eine Modellfamilie mit Text-und-Bild-Eingabe, Tool-Nutzung, modellspezifischen Limits und einem Kontextbereich von 200K bis 1M Token.

## So wird es eingesetzt {#how-to-use-this}

Ab 2023-05-12 konnten Praktiker Claude für Workflows in Betracht ziehen, die bis zu 100K Token Kontext benötigen. Ab 2023-11-22 erweiterte Claude 2.1 diesen Planungsrahmen auf 200K Token.

1. Wähle die Oberfläche: Verwende Claude.ai für den Chat, die Console und die API für eine Anwendung oder Claude Code für eine Repository-Aufgabe.
  — <https://docs.anthropic.com/en/docs/about-claude/models/overview>
2. Für die API-Integration lege ein Claude-Console-Konto und einen API-Schlüssel an, exportiere ihn als ANTHROPIC_API_KEY und installiere anschließend das unterstützte SDK.
  — <https://docs.anthropic.com/en/docs/get-started>
3. Wähle ein aktuelles Modell anhand von Leistungsfähigkeit, Latenz, Kosten, Effort und deiner eigenen Aufgabenevaluierung, bevor du dich für den Produktivbetrieb entscheidest.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
4. Führe einen Messages-API-Aufruf mit dem gewählten Modell, einem max_tokens-Limit und der Benutzernachricht durch; ergänze Tools, Dateien oder Funktionen zur Kontextverwaltung nur dann, wenn die Aufgabe sie braucht.
  — <https://docs.anthropic.com/en/docs/get-started>
5. Für Arbeit an Codebases installiere Claude Code auf einer unterstützten Oberfläche, starte es im Projektverzeichnis und prüfe die Datei- und Befehlsaktionen, die es ausführt.
  — <https://code.claude.com/docs/en/overview>

## Best Practices {#best-practices}

- Definiere spezifische, messbare Erfolgskriterien und einen Evaluierungssatz, bevor du Prompts oder Modelle änderst.
  — <https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>
- Formuliere Aufgabe, Kontext, Randbedingungen, Ausgabeformat und geordnete Schritte direkt. Ergänze relevante Beispiele, wenn die Konsistenz der Ausgabe wichtig ist.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Setze bei Eingaben über 20K Token lange Dokumente vor die Anfrage, strukturiere mehrere Dokumente klar und bitte vor der Synthese um belegende Zitate.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Behandle Modellwahl und Effort als Leistungsstellgrößen neben dem Prompting; nutze Evaluierungen, um Leistungsfähigkeit gegen Latenz und Kosten abzuwägen.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
- Fixiere Modell-IDs für Reproduzierbarkeit und überwache ihren Lebenszyklus. Ohne Datum angegebene IDs ab der Generation 4.6 sind feste Snapshots und keine wandernden Aliase.
  — <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions>

## Hierdurch abgelöst {#superseded-by-this}

- 2023-05-12: Die Annahme, 100K Token seien die betriebliche Kontextobergrenze von Claude, ist veraltet; aktuelle Modelle reichen von 200K bis 1M Eingabe-Token.
- 2023-11-22: Die Ausrichtung auf die Anleitung zu Claude 2.1 ist veraltet; das API-Modell claude-2.1 wurde am 2025-07-21 eingestellt.
- 2023-11-22: Die Annahme, Tool-Nutzung sei nur eine Beta-Fähigkeit, ist veraltet; die Dokumentation aktueller Modelle führt Tool-Nutzung als unterstützte Fähigkeit auf.
- Annahmen über Aliase vor 4.6 sind für aktuelle Modell-IDs ohne Datum veraltet: Jede aktuelle ID bezeichnet einen festen Modell-Snapshot.

## Weiterhin unbekannt {#still-unknown}

- Die beiden datierten Ereignisse ergeben keine vollständige Versionschronologie zwischen 2023 und heute; die aktuelle Dokumentation wird nur als Momentaufnahme herangezogen.
- Die angegebenen Ereignisdaten liegen einen Tag nach den Daten der offiziellen Artikel: 2023-05-12 statt 2023-05-11 und 2023-11-22 statt 2023-11-21.
- Verfügbarkeit nach Tarif, Region, Plattform und Preise können je nach Konto abweichen und sich nach dieser Momentaufnahme ändern; prüfe sie vor dem Rollout in der Console.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.anthropic.com/index/100k-context-windows | Einführung von 100K-Kontextfenstern | Anthropic | 2026-09-04 |
| https://www.anthropic.com/index/claude-2-1 | Einführung von Claude 2.1 | Anthropic | 2026-09-04 |
| https://docs.anthropic.com/en/docs/about-claude/models/overview | Modellübersicht | Claude Platform Docs | 2026-09-04 |
| https://docs.anthropic.com/en/docs/get-started | Erste Schritte mit Claude | Claude Platform Docs | 2026-09-04 |
| https://code.claude.com/docs/en/overview | Übersicht | Claude Code Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/models/choosing-a-model | Das richtige Modell auswählen | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Erfolgskriterien definieren und Evaluierungen erstellen | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Best Practices für Prompting | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions | Modell-IDs und Versionierung | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/model-deprecations | Einstellung von Modellen | Claude Platform Docs | 2026-09-04 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:claude`, Thread `claude-product-development`, 2 datierte Ereignisse 2023-05-12 → 2023-11-22.
- **Praxishinweis:** Ab 2023-05-12 konnten Praktiker Claude für Workflows in Betracht ziehen, die bis zu 100K Token Kontext benötigen; ab 2023-11-22 erweiterte Claude 2.1 diesen Planungsrahmen auf 200K Token.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
