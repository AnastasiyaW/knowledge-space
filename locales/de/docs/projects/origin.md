---
title: "Origin — Code-Hosting"
category: projects
date: 2026-08-19
tags: [code-hosting, cursor, origin, project]
aliases: ["Origin"]
level: 3
source_sha256: 97e865b7b96e512d7f0b1f143265e5d8cfd458c79dc705617459c7dc9792e70d
translation: machine
translated_at: '2026-10-24'
---
# Origin — Code-Hosting {#origin-code-hosting}

**Entwicklungslinie:** `project:origin` · Thread `code-hosting`  
**Letztes Ereignis:** 2026-08-19 · 1 datiert seit 2026-08-19 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Origin ist der frühe Beta-Git-Forge von Cursor für zahlende Cursor-Nutzer.

- Native Repositories: Code wird bei Origin als Source of Truth gehostet.
- GitHub-Spiegelung: Repositories werden gespiegelt, während GitHub die Source of Truth bleibt.
- Codesuche und Durchsuchen: Code im Repository suchen und prüfen.
- Pull-Request-Review: Diffs und Checks vor dem Mergen prüfen.
- Agent-Anbindungen: Cloud-Agents und Automatisierungen mit Repositories verbinden.

Nutzen Sie Origin für Cursor-native Code-Workflows oder einen GitHub-Spiegel, behandeln Sie aber die API und die Beta-Verträge als veränderlich.

## Entwicklungslinie {#development-line}

- **2026-08-19 — Origin hat einen Meilenstein im Code-Hosting erreicht.** Native Repositories, GitHub-Spiegelung, Code-Browsing, Pull Requests und Cursor-Agents; die Launch-Seite selbst ist auf 2026-08-17 datiert.

## Was sich geändert hat {#what-changed}

- 2026-08-19 — Origin ist in die frühe Beta-Einführung gegangen: native Repositories, GitHub-Spiegelung, Code-Browsing, Pull Requests und Cursor-Agents; die Launch-Seite selbst ist auf 2026-08-17 datiert.
- 2026-08-26 — Die öffentliche API hat Repository-Labels und Check-Run-Annotationen ergänzt; die Payloads der Reviewer-Webhooks haben ihre Struktur geändert.
- 2026-08-27 — Die API-Spezifikation wurde besser für Code-Generatoren geeignet und um optionale Deadlines für Check Runs erweitert.
- 2026-08-28 — Abgelaufene Deadlines beginnen, laufende Check Runs als timed out abzuschließen; die API hat Repository-Tarballs und das Auflisten von Vergleichsdateien ergänzt.
- 2026-08-29 — Die API-Unterstützung für angefragte Reviewer, auflösbare Review-Threads, Inline-Kommentare und atomare Review-Kommentare wurde erweitert.
- 2026-09-01 — Webhooks für das Löschen von Repositories und für Metadaten-Updates wurden hinzugefügt.
- 2026-09-02 — Die Listen-Endpunkte für Check Suites und Check Runs geben nur noch den neuesten Versuch zurück; überholte Wiederholungen werden in normalen Listen ausgeblendet.
- 2026-09-03 — Das Auflisten von Check Runs und Pull-Request-Kommentaren erhielt Filter für inkrementelles Polling.
- 2026-09-04 — Das App-`slug` wurde aus den Actor-Metadaten von API und Webhooks entfernt; Integrationen müssen die App-`id` und optional `displayName` verwenden.

## Anwendung {#how-to-use-this}

Ab 2026-08-19 sollten Praktiker, die Code-Hosting-Workflows evaluieren, Origin in ihre Recherche aufnehmen und dabei die genauen Fähigkeiten und die Verfügbarkeit anhand der Primärdokumentation prüfen.

1. Prüfen Sie, ob Ihr Konto Zugriff auf Origin hat, beanspruchen Sie einen Codebase-Namespace und wählen Sie ihn sorgfältig: Er kann während der Beta nicht umbenannt werden.
  — <https://cursor.com/docs/origin>
2. Erstellen Sie ein natives Repository über Codebase → New, wählen Sie die Sichtbarkeit Internal oder Private und kopieren Sie dann die Clone-URL.
  — <https://cursor.com/docs/origin/create-repository>
3. Authentifizieren Sie sich mit der Origin CLI und klonen Sie das Repository bzw. fügen Sie das Standard-Git-HTTPS-Remote hinzu; pushen Sie danach Ihren Branch.
  — <https://cursor.com/docs/origin/git>
4. Für ein bestehendes GitHub-Repository verwenden Sie Sync from GitHub; Origin wird dann zum Spiegel, während GitHub für Pushes maßgeblich bleibt.
  — <https://cursor.com/docs/origin/mirror-github>
5. Öffnen Sie einen Pull Request nach dem Pushen eines Branches, prüfen Sie Checks und Diffs, fordern Sie Reviewer an und mergen Sie erst nach bestandenem Review und CI.
  — <https://cursor.com/docs/origin/pull-requests>
6. Hängen Sie Cloud-Agents oder Automatisierungen von Cursor an, wenn Agents das Repository klonen, Branches anlegen, committen, pushen oder Pull Requests dafür öffnen sollen.
  — <https://cursor.com/docs/origin/integrations>

## Best Practices {#best-practices}

- Behandeln Sie ein per GitHub synchronisiertes Repository als Spiegel: GitHub Issues, die Actions-Konfiguration und Secrets werden nicht nach Origin kopiert, und GitHub bleibt die Source of Truth.
  — <https://cursor.com/docs/origin/mirror-github>
- Wählen Sie den Namespace, bevor Sie Origin aktivieren; Beta-Namespaces lassen sich nach der Beanspruchung nicht mehr ändern oder aktualisieren.
  — <https://cursor.com/docs/origin>
- Generieren Sie für Integrationen den Code aus der aktuellen OpenAPI-Spezifikation neu und migrieren Sie die App-Identitätsbehandlung von `slug` auf `id` plus optional `displayName`.
  — <https://cursor.com/docs/api/origin/changelog>
- Fragen Sie neue Pull-Request-Kommentare mit den Filtern `since` oder `until` ab, statt wiederholt die gesamte Kommentarhistorie zu durchblättern.
  — <https://cursor.com/docs/api/origin/changelog>

## Durch dies ersetzt {#superseded-by-this}

- 2026-08-27 — Die Anleitung, dass ein abgelaufenes `deadlineAt` den Status eines Check Runs nicht ändert, wurde am 2026-08-28 ersetzt: abgelaufene laufende Runs werden nun als `timed_out` abgeschlossen.
- 2026-09-02 — Integrationen, die sich darauf verlassen, dass Listen-Endpunkte jeden Check-Versuch zeigen, sind veraltet: normale Listen-Antworten enthalten nur noch den neuesten Versuch; für überholte Versuche rufen Sie eine bestimmte ID ab.
- 2026-09-04 — Integrationen, die das App-`slug` als Actor-Kennung verwenden, sind veraltet; verwenden Sie App-`id` und optional `displayName`.

## Weiterhin unbekannt {#still-unknown}

- Das angegebene Ereignisdatum ist 2026-08-19, die primäre Launch-Seite von Cursor ist jedoch auf 2026-08-17 datiert; wir behalten 2026-08-19 als Ereignisdatum bei.
- Es wurden keine unabhängigen Belege für den produktiven Einsatz von Origin gefunden; die Verfügbarkeit der Funktionen ist als gestaffelte frühe Beta dokumentiert. Die meisten gefundenen Änderungen nach dem Launch betrafen die API und nicht eine datierte Erzählung von Produktveröffentlichungen.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://cursor.com/changelog/origin-code-hosting | Origin Code Hosting · Cursor | 2026-09-05 |
| https://cursor.com/docs/origin | Origin | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/create-repository | Ein Origin-Repository erstellen | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/git | Clone, Push & Pull | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/mirror-github | Ein GitHub-Repository spiegeln | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/pull-requests | Pull Requests | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/origin/integrations | Origin-Integrationen | Cursor Docs | 2026-09-05 |
| https://cursor.com/docs/api/origin/changelog | Origin-API-Changelog | Cursor Docs | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:origin`, Thread `code-hosting`, 1 datiertes Ereignis 2026-08-19 → 2026-08-19.
- **Praktischer Hinweis:** Ab 2026-08-19 sollten Praktiker, die Code-Hosting-Workflows evaluieren, Origin in ihre Recherche aufnehmen und dabei die genauen Fähigkeiten und die Verfügbarkeit anhand der Primärdokumentation prüfen.
- **Konfidenz:** hoch. Die datierten „Durch dies ersetzt“-Einträge sind maßgeblich dafür, was veraltet ist.
