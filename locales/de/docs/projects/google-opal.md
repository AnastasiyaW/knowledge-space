---
title: "Google Opal"
category: projects
date: 2025-07-25
tags: [google-opal, opal, project]
aliases: ["Google Opal"]
level: 2
source_sha256: c2b9f1afd4c006f20c7cde4782bea3e7ed4b029485134ad606c6e20e8a10ce5f
translation: machine
translated_at: '2026-10-24'
---
# Google Opal {#google-opal}

**Entwicklungslinie:** `project:google-opal` · Thread `google-opal`  
**Letztes Ereignis:** 2025-07-25 · 1 datiert seit 2025-07-25 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Google Opal ist eine No-Code-Alternative zu kleinen individuellen Web-Apps, entwickelt für Personen, die teilbare KI-Workflows ohne eigenen Server betreiben möchten.

- Workflow-Editor: erstellt und bearbeitet knotenbasierte Pipelines aus natürlicher Sprache.
- Visuelle Arbeitsfläche: verknüpft Eingaben, Prompts, Modellaufrufe, Tools und Ausgaben.
- Agent Mode: wählt Tools aus, nutzt Speicher, steuert die Ausführung und führt Folgedialoge im Chat.

## Entwicklungslinie {#development-line}

- **2025-07-25 — Google stellt Opal vor.** Am 2025-07-25 veröffentlichte Google eine Einführung in Opal und teilte den zugehörigen Web-Einstiegspunkt. Die Ankündigung bestätigte das Projekt, legte aber weder den vollen Funktionsumfang noch die regionale Verfügbarkeit oder Kontobeschränkungen fest.

## Was sich geändert hat {#what-changed}

- **2025-07-25** (ursprüngliche Ankündigung datiert auf 2025-07-24) — Opal startete als öffentliche Beta, nur in den USA verfügbar, als visueller Baukasten und Builder per natürlicher Sprache für mehrstufige Apps, die Prompts, Modellaufrufe und Tools verketten.
- **2026-02-25** (offizielle Ankündigung datiert auf 2026-02-24) — Der Schritt Generate erhielt den Agent Mode, um Tools und Modelle anhand eines Ziels auszuwählen, Speicher zu behalten, dynamisch zu routen und Rückfragen zu stellen.
- **2026-03-24** — Die Dokumentation des Anbieters zeigt, dass Agent Mode standardmäßig aktiviert ist und Search/Maps, Code Exec, Memory und Medienerzeugung bereitstellt. Feste Workflows bleiben für starre oder präzisionskritische Logik verfügbar.

## Wie man das nutzt {#how-to-use-this}

Wir bewerten Google Opal anhand der offiziellen Einführung und des Web-Einstiegspunkts vom 2025-07-25. Die offizielle Dokumentation zeigt keine späteren Änderungen an Workflows oder Funktionen.

1. Melden Sie sich bei Opal an, öffnen Sie eine Demo aus der Gallery und wählen Sie Remix, um eine bearbeitbare Kopie zu erstellen. Wählen Sie Create New, um eine App von Grund auf zu erstellen.
  — <https://developers.google.com/opal/quickstart>
2. Fügen Sie für offene Workflows einen Generate-Schritt hinzu, aktivieren Sie bei Bedarf Agent und definieren Sie das Zielergebnis.
  — <https://developers.google.com/opal/Agent_Mode>
3. Verweisen Sie auf benötigte Fähigkeiten über das @-Menü, etwa @Search oder @Memory, und verknüpfen Sie anschließend Eingaben, Generierungsschritte und Ausgaben im visuellen Editor.
  — <https://developers.google.com/opal/Agent_Mode>
4. Testen Sie die App mit repräsentativen Eingaben, prüfen Sie den resultierenden Graphen und verfeinern Sie Prompts oder Knoten, bevor Sie die App teilen.
  — <https://developers.google.com/opal/quickstart>
5. Halten Sie Opal-Apps standardmäßig privat. Beim Teilen beschränken Sie Nutzer entweder auf die Ansicht der App oder gewähren vollen Editor- und Remix-Zugriff.
  — <https://developers.google.com/opal/faq>

## Bewährte Vorgehensweisen {#best-practices}

- Remixen Sie eine bestehende Gallery-App, statt den ersten Workflow auf einer leeren Arbeitsfläche zu entwerfen.
  — <https://developers.google.com/opal/quickstart>
- Bei Agent Mode geben Sie das Ziel und das erforderliche Ergebnis vor, statt jeden Zwischenschritt festzulegen.
  — <https://developers.google.com/opal/Agent_Mode>
- Rufen Sie Tools explizit mit @ auf, wenn Sie eine bestimmte Fähigkeit benötigen. Laut offizieller Dokumentation ist das präziser.
  — <https://developers.google.com/opal/Agent_Mode>
- Testen Sie Prompts und den gesamten Workflow, bevor Sie sich darauf verlassen, da Opal Fehler machen kann.
  — <https://developers.google.com/opal/faq>
- Behandeln Sie Remix- und Editor-Freigaben als Offenlegung von Prompts: Beim Teilen werden Prompts, der Workflow-Graph und die zugrunde liegende Drive-Datei sichtbar.
  — <https://developers.google.com/opal/faq>

## Dadurch abgelöst {#superseded-by-this}

- **2025-07-25** — Die ursprüngliche Regel für die öffentliche Beta, nur in den USA verfügbar, ist veraltet: Die aktuelle FAQ listet unterstützte Länder auf, statt den Zugang auf die USA zu beschränken.
- **Vor 2026-02-25** — Jede Opal-App rein als statische Prompt-Kette zu betrachten, ist für offene Aufgaben veraltet. Agent Mode ergänzt Toolauswahl, Speicher, Routing und interaktiven Chat. Feste Workflows bleiben für starre oder präzisionskritische Logik angemessen.

## Weiterhin unbekannt {#still-unknown}

- Wir haben keine Tests mit angemeldetem Konto durchgeführt. Kontingente, Abrechnung, Veröffentlichungsobergrenzen und kontospezifische Funktionsverfügbarkeit sind daher ungeprüft.
- Suchen auf Chinesisch ergaben keine offizielle vereinfachte chinesische Opal-Dokumentation. Die Empfehlungen stützen sich daher ausschließlich auf offizielle englischsprachige Quellen.
- Die Verfügbarkeit ist länderabhängig. Prüfen Sie die aktuelle offizielle FAQ, bevor Sie einen Workflow auf Opal festlegen.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://developers.googleblog.com/en/introducing-opal/ | Introducing Opal: describe, create, and share your AI mini-apps | 2026-09-04 |
| https://opal.google/landing/ | Opal [Experiment] | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-labs/opal-agent/ | Build dynamic agentic workflows in Opal | 2026-09-04 |
| https://developers.google.com/opal/ | Opal | Google for Developers | 2026-09-04 |
| https://developers.google.com/opal/quickstart | Quickstart | Opal | Google for Developers | 2026-09-04 |
| https://developers.google.com/opal/Agent_Mode | Agent Mode in Opal | Google for Developers | 2026-09-04 |
| https://developers.google.com/opal/faq | Frequently asked questions and best practices | Opal | Google for Developers | 2026-09-04 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:google-opal`, Thread `google-opal`, 1 datiertes Ereignis vom 2025-07-25 → 2025-07-25.
- **Praxishinweis:** Ab dem 2025-07-25 konnten Praktiker Google Opal anhand der offiziellen Projekteinführung von Google und des verlinkten Web-Einstiegspunkts bewerten. Die vorliegenden Belege belegen jedoch keine spätere Änderung von Workflows oder Funktionen.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
