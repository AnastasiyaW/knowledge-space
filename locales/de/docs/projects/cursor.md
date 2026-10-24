---
title: "Cursor — Produktentwicklung"
category: projects
date: 2026-06-29
tags: [cursor, product-development, project]
aliases: ["Cursor"]
level: 3
source_sha256: 4fad5d2f7e14bb8085d66c3c9c4e58bab7a7220023caae1259e1520de59c30f3
translation: machine
translated_at: '2026-10-24'
---
# Cursor — Produktentwicklung {#cursor-product-development}

**Entwicklungslinie:** `project:cursor` · Thread `product-development`  
**Letztes Ereignis:** 2026-06-29 · 1 datiertes seit 2026-06-29 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Cursor ist ein Coding-Editor und Agent für Entwickler, die ein Repository verstehen, Änderungen delegieren und Änderungen zusammenführen müssen.

- Codebase-Indexierung zum Abbilden des Repositorys, zum Planen von Features, Schreiben von Code, Beheben von Bugs und Reviewen von Diffs.
- Plattformübergreifende Laufzeit über die Desktop-App, isolierte Cloud-VMs, Web und iOS, mit Session-Übergabe zwischen lokalen und Cloud-Läufen.
- Kontextinjektion über Rules, `AGENTS.md`, Skills und MCP für repositoryspezifische Vorgaben.

## Entwicklungslinie {#development-line}

- **2026-06-29 — Cursor kündigte eine iOS-App an.** Cursor kündigte seine iOS-App am 2026-06-29 in einem Blogbeitrag und einem App-Store-Eintrag an. Die Veröffentlichung erweitert den Editor auf iOS-Geräte. Die Links der Ankündigung bestätigen das Veröffentlichungsdatum, nennen aber keine konkreten Funktionen, keine regionale Verfügbarkeit und keinen endgültigen Veröffentlichungsstatus.

## Was sich geändert hat {#what-changed}

Cursor entwickelte sich von einem einzelnen Web-Einstiegspunkt zu einem Agent-Arbeitsbereich über mehrere Geräte hinweg.

- 2023-08-21 — `cursor.so` diente als ursprüngliche öffentliche Adresse. Die Seite leitet inzwischen weiter und enthält keine früheren Funktionsbeschreibungen mehr, sodass für dieses Datum keine überprüfbare Funktionsbasis existiert.
- 2026-04-02 (heute gefunden) — Cursor 3 ergänzte eine einheitliche Agent-Oberfläche für mehrere Workspaces mit parallelen lokalen und Cloud-Agents, Session-Übergaben, Diff- und PR-Workflows, einem integrierten Browser und Plugins.
- 2026-06-29 — Cursor veröffentlichte eine native iOS-App als öffentliche Beta, mit der Cloud-Agents gestartet, lokale Agents remote gesteuert, Benachrichtigungen verfolgt, Artefakte geprüft und PRs zusammengeführt werden können.
- 2026-09-04 (heute gefunden) — Die aktuelle Dokumentation verknüpft iOS mit dem gemeinsamen Agent-Backend für Desktop und Web. Sie listet Einstiegspunkte für Cloud Agents auf Desktop, Web, iOS, Slack, Kommentaren in der Quellcodeverwaltung, Linear und der API auf.

## Wie du das nutzt {#how-to-use-this}

Ab 2026-06-29 solltest du Cursors iOS-App neben den bestehenden Workflows testen, falls mobiler Zugriff benötigt wird. Die datierten Quellen bieten keine Grundlage für eine vollständige Migration oder weitergehende Feature-Empfehlungen.

1. Installiere die Desktop-Anwendung, melde dich an und öffne das Projektverzeichnis.
  — <https://cursor.com/docs/get-started/quickstart>
2. Bitte den Agent, Repository-Struktur, Einstiegspunkte und zentrale Module zu erklären, bevor du Änderungen vorschlagen lässt.
  — <https://cursor.com/docs/get-started/quickstart>
3. Beginne mit einer kleinen, risikoarmen Änderung und wechsle für Recherche, dateiübergreifende Aufgaben oder heikle Freigaben in den Plan Mode.
  — <https://cursor.com/docs/get-started/quickstart>
4. Lege Repository-Anweisungen unter `.cursor/rules/*.mdc` ab oder platziere eine `AGENTS.md` im Wurzelverzeichnis für projektweite Vorgaben.
  — <https://cursor.com/docs/rules>
5. Prüfe die erzeugten Diffs und führe dann vorhandene Testsuiten, Typprüfungen, Linter oder Builds aus, bevor du eine Änderung übernimmst.
  — <https://cursor.com/docs/get-started/quickstart>
6. Verbinde die Quellcodeverwaltung für Hintergrundaufgaben, konfiguriere die Cloud-Agent-Laufzeit in einer isolierten VM und prüfe die resultierenden Artefakte, Diffs und Pull Requests.
  — <https://cursor.com/docs/cloud-agent>
7. Melde dich auf iPhone oder iPad an, wähle Repository und Zielbranch, gib dem Agent Anweisungen und prüfe oder führe Pull Requests unterwegs zusammen.
  — <https://cursor.com/docs/cloud-agent/mobile>

## Best Practices {#best-practices}

- Halte Projekt-Rules eng gefasst und unter 500 Zeilen, damit sie handlungsrelevant bleiben. Teile übergroße Regelsätze auf, verweise auf kanonische Dateien, statt Text zu kopieren, und committe sie in Git.
  — <https://cursor.com/docs/rules>
- Stelle Repository-Kontext bereit, bevor du Arbeit delegierst. Teste eine kleine Änderung, bevor du umfangreiche Änderungen versuchst, und nutze den Plan Mode, wenn die Umsetzung Recherche oder Freigabe erfordert.
  — <https://cursor.com/docs/get-started/quickstart>
- Konfiguriere Cloud-Agent-Umgebungen, bevor du Aufgaben startest. Hinterlege Secrets über das Dashboard, verwende OIDC statt langlebiger Cloud-Schlüssel, erlaube nur benötigte ausgehende Netzwerkrouten und führe Tests ohne externe Abhängigkeiten aus.
  — <https://cursor.com/docs/cloud-agent/best-practices>
- Behandle jede Agent-Ausgabe als Entwurf. Prüfe den Diff und führe die Repository-Checks aus, bevor du dich für ein Zusammenführen entscheidest.
  — <https://cursor.com/docs/get-started/quickstart>
- Nutze Quick Agent Review für kurze Plausibilitätsprüfungen. Wende Deep Review bei komplexer Logik, sicherheitsrelevanten Änderungen oder großen Refactorings an.
  — <https://cursor.com/docs/agent/agent-review>

## Dadurch abgelöst {#superseded-by-this}

- 2023-08-21 — `cursor.com` ersetzt die alte Domain `cursor.so`. Die alte URL leitet auf die neue Seite weiter, und aktuelle Einrichtungsschritte stehen in der offiziellen Dokumentation.
- 2026-04-02 — Annahmen zu einem Desktop-Editor mit einem einzigen Fenster sind veraltet. Cursor 3 koordiniert lokale und Cloud-Agents über mehrere Workspaces und behält dabei die Inspektion auf IDE-Ebene bei.
- 2026-06-29 — Die Behandlung mobiler Apps als reine Benachrichtigungsfeeds ohne Schreibzugriff ist überholt. Der native iOS-Client startet und steuert Agents, prüft Ergebnisse und führt Pull Requests zusammen.

## Weiterhin unbekannt {#still-unknown}

- Die Quelle von 2023 leitet auf die Hauptseite weiter, ohne ursprüngliche Startnotizen, Versionsnummern oder Funktionsdetails zu erhalten.
- Der Beitrag von Juni 2026 beschreibt iOS als öffentliche Beta. Die aktuelle Dokumentation beschreibt die Funktionen, lässt aber offen, ob die App allgemein verfügbar ist.
- Die aktuelle Dokumentation klärt nicht, welche Modelle aktiv sind, welche Abonnementstufen es gibt, welche Preis- oder Nutzungslimits gelten oder wie die regionale Verfügbarkeit im App Store aussieht.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://www.cursor.so/ | KI-Coding-Agent für anspruchsvolle Software \| Cursor | 2026-09-04 |
| https://cursor.com/blog/cursor-3 | Die neue Cursor-Version im Überblick \| Cursor | 2026-09-04 |
| https://cursor.com/blog/ios-mobile-app | Von überall aus arbeiten mit Cursor für iOS \| Cursor | 2026-09-04 |
| https://apps.apple.com/app/cursor/id6767085653 | Cursor App | App Store | 2026-09-04 |
| https://cursor.com/docs/get-started/quickstart | Schnellstart | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/rules | Rules | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/cloud-agent | Cloud Agents | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/cloud-agent/best-practices | Best Practices für Cloud Agents | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/agent/agent-review | Agent Review | Cursor Docs | 2026-09-04 |
| https://cursor.com/docs/cloud-agent/mobile | Cursor für iOS | Cursor Docs | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:cursor`, Thread `product-development`, 1 datiertes Ereignis 2026-06-29 → 2026-06-29.
- **Praktischer Hinweis:** Ab 2026-06-29 sollten Teams, die mobile Unterstützung benötigen, Cursors iOS-Client neben aktuellen Tools evaluieren. Die geprüften Links stützen keine umfassendere Plattformmigration oder Feature-Einführung.
- **Konfidenz:** mittel. Die datierten Ablösungen oben bleiben die Grundlage für veraltete Workflows.
