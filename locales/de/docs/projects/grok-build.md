---
title: "Grok Build"
category: projects
date: 2026-07-16
tags: [grok-build, project]
aliases: ["Grok Build"]
level: 3
source_sha256: 7d47e7eab16496bcd07f680490f0b0cb022963feb557b4f0736c5695ed7e18e0
translation: machine
translated_at: '2026-10-24'
---
# Grok Build {#grok-build}

**Entwicklungslinie:** `project:grok-build` · Thread `grok-build`  
**Letztes Ereignis:** 2026-07-16 · 1 datiertes Ereignis seit 2026-07-16 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Grok Build ist ein terminalbasierter KI-Coding-Agent für Softwarearbeit.

- Codebase-Bearbeitung: liest und bearbeitet Projektdateien.
- Shell-Ausführung: führt Shell-Befehle aus.
- Websuche: sucht im Web nach technischen Informationen.
- Aufgabenverwaltung: bearbeitet lange Aufgaben über eine Vollbild-TUI, eine Headless-CLI oder ACP.

Die Dokumentation nennt grok-4.6 als zugrunde liegendes Modell und erlaubt die Konfiguration eigener Modelle. Das veröffentlichte Binary ist der praktische Einstiegspunkt. Der unter Apache-2.0 stehende Quellcode ist zur Einsicht und für lokale Builds offen, xAI nimmt jedoch keine externen Beiträge an.

## Entwicklungslinie {#development-line}

- **2026-07-16 — Öffentliche Repository-Referenz für Grok Build.** Am 2026-07-16 verwies der Grok-Build-Thread auf das öffentliche GitHub-Repository von xAI für Grok Build. Damit entsteht eine datierte öffentliche Quellenreferenz für das Projekt. Den Inhalt des Repositorys bzw. den genauen Kontext der Nachricht haben wir jedoch nicht untersucht.

## Was sich geändert hat {#what-changed}

- **2026-05-25** — Grok Build erschien in einer frühen Beta als Terminal-Coding-Agent mit Plan-Review, Hooks, Skills, MCP-Unterstützung, Subagents, Headless-Modus und ACP.
- **2026-06-11** — Grok Build erhielt einen integrierten Plugin-Marketplace mit remote installierten Plugins, die auf einen bestimmten Commit fixiert werden.
- **2026-07-15** — Die Rust-CLI/TUI und die Agent-Runtime von Grok Build wurden als Open Source veröffentlicht. Lokal ausgeführte, benutzerdefinierte Inferenz ist dokumentiert.
- **2026-07-16** — Grok Build v0.2.102 ergänzte sitzungsbezogene Flags für minimal/fullscreen, `/jump`, eine Timeline-Seitenleiste, die Konfiguration von Remote-Berechtigungen sowie verbessertes Login- und Sitzungsverhalten.
- **2026-07-23** — Grok Build ergänzte generierte, wiederverwendbare Workflows für die Orchestrierung mehrerer Agents im Hintergrund.
- **2026-08-19** — Grok Build weitete eine separate Oberfläche zum Erstellen von Web- und Mobile-Apps auf alle Tarife aus, einschließlich Veröffentlichung, Teilen, GitHub-Export, Secrets und Connectors.

## Verwendung {#how-to-use-this}

Ab 2026-07-16 sollten Sie das verlinkte GitHub-Repository von xAI als öffentlichen Ausgangspunkt für Grok Build betrachten. Prüfen Sie dessen Inhalte, bevor Sie sich auf Implementierungsdetails verlassen.

1. Installieren Sie das veröffentlichte Binary für Ihre Plattform und führen Sie anschließend `grok --version` aus.
  — <https://github.com/xai-org/grok-build>
2. Wechseln Sie in das Ziel-Repository und führen Sie `grok` aus. Authentifizieren Sie sich im Browser oder hinterlegen Sie in einer Umgebung ohne Browser einen API-Schlüssel.
  — <https://docs.x.ai/build/overview>
3. Beginnen Sie komplexe Aufgaben im Plan-Modus. Prüfen oder bearbeiten Sie den Plan, genehmigen Sie die Ausführung und kontrollieren Sie die resultierenden Diffs.
  — <https://x.ai/news/grok-build-cli>
4. Automatisieren Sie einen begrenzten Prompt mit `grok -p`. Verwenden Sie streamendes JSON, wenn ein anderes Programm das Ergebnis weiterverarbeitet.
  — <https://docs.x.ai/build/overview>
5. Konfigurieren Sie Modell, Projektberechtigungen, Plugins und MCP-Quellen bewusst. Führen Sie `grok inspect` aus, um zu prüfen, ob die Konfiguration tatsächlich geladen wurde.
  — <https://docs.x.ai/build/settings>

## Best Practices {#best-practices}

- Behalten Sie Ask als initialen Berechtigungsmodus bei und verwenden Sie den Plan-Modus für nachvollziehbar zu prüfende Änderungen. Verwechseln Sie Auto oder Always-approve nicht mit einem Ersatz für die Plan-Prüfung.
  — <https://docs.x.ai/build/features/permissions>
- Führen Sie nicht vertrauenswürdige Repositorys nur mit einer strikten Sandbox und eng gefassten Berechtigungsregeln aus. Ergänzen Sie explizite Verbote für `.env`, private Schlüssel und andere Pfade mit Zugangsdaten, da die integrierten Profile diese nicht dauerhaft schützen.
  — <https://docs.x.ai/build/features/sandbox>
- Verwenden Sie `grok inspect` nach jeder Konfigurationsänderung, damit aktive Quellen für Instruktionen, Skills, Plugins, Hooks, MCP und Modelle sichtbar bleiben.
  — <https://docs.x.ai/build/settings>
- Behandeln Sie Plugins von Drittanbietern als ausführbaren Code und installieren Sie nur Quellen, die Sie geprüft haben. Das Pinning im Marketplace verifiziert eine ausgewählte Revision, macht Code von Drittanbietern jedoch weder empfohlen noch sicher.
  — <https://github.com/xai-org/plugin-marketplace>

## Ersetzt durch dieses Dokument {#superseded-by-this}

- 2026-07-15 — Die Annahme, dass der Grok-Build-Harness für die Quellcodeprüfung oder lokale Kompilierung nicht verfügbar sei, ist veraltet. xAI hat den Quellcode von CLI/TUI und Agent-Runtime veröffentlicht.
- 2026-08-19 — Die Zugangsbeschränkung der Early Beta für die Oberfläche zum Erstellen von Web- und Mobile-Apps ist veraltet. xAI gibt an, dass diese Oberfläche in allen Tarifen verfügbar ist. Daraus folgt jedoch nicht, dass für die Terminal-CLI dieselben Zugangsbedingungen gelten.

## Weiterhin unbekannt {#still-unknown}

- Die angeforderten Felder event_findings und new_events sind im bereitgestellten Antwortschema nicht verfügbar. Die Ergänzungen des datierten Ereignisses sind in „Was sich geändert hat“ abgebildet: die Open-Source-Ankündigung vom 15. Juli und der Changelog-Eintrag zu v0.2.102 vom 16. Juli.
- Grok Build bezeichnet zwei verbundene, operativ aber unterschiedliche Oberflächen: Das GitHub-Repository deckt den terminalbasierten Coding-Agenten ab, während die August-Ankündigung einen Web- und Mobile-App-Builder beschreibt, der Projekte nach GitHub exportieren und im Terminal weiterführen kann. xAI dokumentiert ihre genaue gemeinsame Implementierungslinie nicht.
- Die August-Ankündigung beschreibt die Early Beta für Web und Mobile als auf SuperGrok Heavy beschränkt. Der Terminal-CLI-Start im Mai beschrieb dagegen einen Early-Beta-Zugang für SuperGrok und X Premium Plus. Wir sollten die Zugangsregeln nicht als eine einheitliche historische Berechtigung behandeln.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/xai-org/grok-build | xai-org/grok-build | 2026-09-05 |
| https://x.ai/news/grok-build-cli | Introducing Grok Build | 2026-09-05 |
| https://x.ai/news/grok-plugin-marketplace | Grok Build Plugin Marketplace | 2026-09-05 |
| https://x.ai/news/grok-build-open-source | Grok Build is Now Open Source | 2026-09-05 |
| https://x.ai/build/changelog | Grok Build Changelog | 2026-09-05 |
| https://x.ai/news/workflows | Workflows in Grok Build | 2026-09-05 |
| https://x.ai/news/grok-build-for-everyone | Grok Build on web and mobile | 2026-09-05 |
| https://docs.x.ai/build/overview | Grok Build: SpaceXAI's Coding Agent | 2026-09-05 |
| https://docs.x.ai/build/settings | Grok Build Settings | 2026-09-05 |
| https://docs.x.ai/build/features/permissions | Grok Build Permissions | 2026-09-05 |
| https://docs.x.ai/build/features/sandbox | Grok Build Sandbox | 2026-09-05 |
| https://github.com/xai-org/plugin-marketplace | xai-org/plugin-marketplace | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:grok-build`, Thread `grok-build`, 1 datiertes Ereignis vom 2026-07-16 → 2026-07-16.
- **Praktischer Hinweis:** Ab dem 2026-07-16 sollten Praktiker das verlinkte GitHub-Repository von xAI als öffentlichen Ausgangspunkt für Grok Build betrachten und dessen Inhalte prüfen, bevor sie sich auf Implementierungsdetails verlassen.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich dafür, was veraltet ist.
