---
title: "Windows-Copilot-API"
category: projects
date: 2026-06-22
tags: [project, windows-copilot-api, windows-copilot-api-development]
aliases: ["Windows-Copilot-API"]
level: 2
source_sha256: 2e3b9ff587cb79dd9e98d7d55ea0c0d3f20eaec0db72e0164dc23a6a293a6f81
translation: machine
translated_at: '2026-10-24'
---
# Windows-Copilot-API {#windows-copilot-api}

**Entwicklungslinie:** `project:windows-copilot-api` · Thread `windows-copilot-api-development`  
**Letztes Ereignis:** 2026-06-22 · 1 datiertes Ereignis seit 2026-06-22 · **Recherchiert:** 2026-09-06 · Konfidenz: hoch

## Was es ist {#what-it-is}

Windows-Copilot-API ist eine inoffizielle plattformübergreifende Brücke. Sie wandelt eine angemeldete Sitzung von Copilot für Verbraucher in Python-Aufrufe oder einen lokalen, OpenAI-kompatiblen Chat-Endpunkt um.

- Python-Chat, Streaming und Konversations-IDs
- Lokale Endpunkte `/v1/chat/completions` und `/v1/models`
- Anmeldung im Browser und eine persistente lokale Sitzung

## Entwicklungslinie {#development-line}

- **2026-06-22 — Windows-Copilot-API-Repository und die Microsoft-Copilot-Website wurden verknüpft.** Am 2026-06-22 verbanden öffentliche Links das GitHub-Repository von Windows-Copilot-API mit der Website von Microsoft Copilot. Das schafft einen datierten öffentlichen Bezugspunkt für die Entwicklungslinie des Projekts, belegt aber weder ein Release, einen Funktionsumfang, eine Zuständigkeit noch einen Bereitstellungsstatus. Es wurden weder der ursprüngliche Quelltext noch unabhängige bestätigende Belege bereitgestellt.

## Was sich geändert hat {#what-changed}

- 2026-06-22 — Windows-Copilot-API ergänzte eine Docker-Bereitstellung, Ratenbegrenzung, Korrekturen bei der Behandlung von Host und Port, Fehlersuchmaterial und eine CLI-Korrektur. Die zentrale lokale, OpenAI-kompatible Brücke war bereits am 2026-06-19 eingeführt worden.
- 2026-06-23 — Ein Patch- und Diagnose-Update wurde eingespielt.
- 2026-06-24 — Die Anmeldung wurde um Google-Konten neben Microsoft-Konten erweitert, und die automatische Behandlung der Cloudflare-Clearance wurde eingeführt.

Das Repository listet keine GitHub-Releases auf; daher sind Commits, nicht Release-Versionen, die verlässlichen historischen Anker.

## Anwendung {#how-to-use-this}

1. Leiten Sie keine produktiven Arbeitslasten mit Copilot für Verbraucher über dieses Projekt. Die Nutzungsbedingungen für Verbraucher untersagen die Verwendung von Werkzeugen oder Computerprogrammen, etwa Bots oder Scrapern, für den Zugriff auf Copilot.
  — <https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/termsofuse>
2. Für eine unterstützte Microsoft-365-Integration verwenden Sie die separaten Microsoft-365-Copilot-APIs: Besorgen Sie die erforderliche Lizenzierung für Microsoft 365 Copilot und eine E3/E5-äquivalente Lizenz, registrieren Sie eine Entra-Anwendung, beziehen Sie ein Benutzer-Token und rufen Sie die Graph-Oberfläche `/copilot` auf.
  — <https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview>
3. Für die historische Codeanalyse fixieren Sie den Commit-Stand vom 2026-06-22; schreiben Sie das spätere Google-Login-Verhalten oder die automatische Clearance-Behandlung nicht diesem Datum zu.
  — <https://github.com/sums001/Windows-Copilot-API/commits/master/>

## Bewährte Vorgehensweisen {#best-practices}

- Behandeln Sie den Zugriff für Verbraucher als unzulässig und nicht als Ausweichlösung für den Produktivbetrieb. Microsoft untersagt ausdrücklich den programmatischen Zugriff auf Copilot durch Bots oder Scraper.
  — [Nutzungsbedingungen von Microsoft Copilot](https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/termsofuse)
- Behandeln Sie das veränderliche `master` nicht als Release-Artefakt. Fixieren Sie einen Commit-SHA, da das Repository keine GitHub-Releases hat.
  — [Releases von Windows-Copilot-API](https://github.com/sums001/Windows-Copilot-API/releases)
- Halten Sie bei der Prüfung historischer Mechanismen spätere OAuth- und Clearance-Änderungen getrennt vom Stand vom 2026-06-22.
  — [Commit-Verlauf von Windows-Copilot-API](https://github.com/sums001/Windows-Copilot-API/commits/master/)
- Wählen Sie die lizenzierten Microsoft-Graph-Copilot-APIs, wenn wir eine unterstützte Unternehmensintegration mit Microsoft-365-Daten und Governance benötigen.
  — [Überblick über die Microsoft-365-Copilot-APIs](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview)

## Hierdurch ersetzt {#superseded-by-this}

- 2026-06-12 — Die Empfehlung, diese Brücke gegen Copilot für Verbraucher einzusetzen, ist ersetzt. Die ausdrücklichen Nutzungsbedingungen für Verbraucher verbieten für den Zugriff auf Copilot Werkzeuge, Computerprogramme, Bots und Scraper.
- 2026-06-24 — Die Einrichtungsempfehlung, nur Microsoft-Konten zu verwenden, ist ersetzt. Das Repository hat die Anmeldung so aktualisiert, dass sowohl Microsoft- als auch Google-Konten unterstützt werden.
- 2026-06-24 — Die Empfehlung zur Cloudflare-Clearance vor der Automatisierung ist für interaktive Clients durch die automatische Clearance-Behandlung ersetzt. Der Dienstbetrieb ohne Oberfläche hängt nach wie vor davon ab, dass sich bei abgelaufener Clearance außerhalb des Systems über einen sichtbaren Browser erneut angemeldet wird.

## Weiterhin unbekannt {#still-unknown}

- Die Beschreibung („About“) des Repositorys behauptet Zugriff auf GPT-4 und GPT-5, die ausführliche README zeigt jedoch ein einziges generisches Modell `copilot` ohne Modellauswahl; das genaue Upstream-Modell lässt sich nicht überprüfen.
- Die aktuelle README ist veränderlich und das Repository hat keine GitHub-Releases. Das aktuelle Verhalten lässt sich daher ohne eine commitspezifische Prüfung nicht auf den 2026-06-22 zurückdatieren.
- Die Verlaufsansicht von GitHub liefert Kalenderdaten, aber nicht genug Zeitstempel- oder Zeitzonendetails, um die mehreren Commits vom 2026-06-22 genau zu ordnen.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/sums001/Windows-Copilot-API | Windows-Copilot-API-Repository | 2026-09-06 |
| https://copilot.microsoft.com/ | Microsoft Copilot | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/commits/master/ | Commit-Verlauf von Windows-Copilot-API | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/blob/master/README.md | README von Windows-Copilot-API | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/commit/dfbe3a91112640db7ff991511cf00d3176d80d53 | Commit OAuth für Google- und Microsoft-Konten | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/commit/878a2ff1ec5607b5c417a57a9ff0a7daa6e5b48e | Commit automatische CF-Clearance | 2026-09-06 |
| https://github.com/sums001/Windows-Copilot-API/releases | Releases von Windows-Copilot-API | 2026-09-06 |
| https://www.microsoft.com/en-us/microsoft-copilot/for-individuals/termsofuse | Nutzungsbedingungen von Microsoft Copilot | 2026-09-06 |
| https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview | Überblick über die Microsoft-365-Copilot-APIs | 2026-09-06 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:windows-copilot-api`, Thread `windows-copilot-api-development`, 1 datiertes Ereignis vom 2026-06-22 bis 2026-06-22.
- **Praxishinweis:** Siehe die belegten Abschnitte zu Anwendung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** hoch. Die datierten Ersetzungshinweise sind maßgeblich dafür, was veraltet ist.
