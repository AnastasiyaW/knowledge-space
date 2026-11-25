---
title: "OpenCut"
category: projects
date: 2026-07-18
tags: [opencut, opencut-development, project]
aliases: ["OpenCut"]
level: 3
source_sha256: e53112df81f1409a49e085135c8c55ae689ce12280a06186ab0f288f67b66298
translation: machine
translated_at: '2026-10-24'
---
# OpenCut {#opencut}

**Entwicklungslinie:** `project:opencut` · Thread `opencut-development`  
**Letztes Ereignis:** 2026-07-18 · 1 datiertes Ereignis seit 2026-07-18 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

OpenCut ist ein unter MIT-Lizenz stehender Videoeditor für Creator, die einen CapCut-Workflow wünschen.

- Web-Workspace: bietet einen öffentlichen Einstiegspunkt für die frühe Beta.
- Multiplattform-Neuentwicklung: nutzt einen Rust-Kern für Web, Desktop und Mobile.
- Release v0.3.0: dokumentiert Masken, Keyframe-Kurven, Geschwindigkeitsregler, Lautstärkeregler und den Import von Untertiteln aus Transkriptdateien.

## Entwicklungslinie {#development-line}

- **2026-07-18 — Website und Quellcode-Repository von OpenCut wurden öffentlich referenziert.** Am 2026-07-18 verlinkte ein Beitrag die Projektwebsite und das GitHub-Repository. Wir erfassen dies, weil es Leser auf die Website und den Quellcode verweist. Der Beitrag zeigt nicht, ob es sich um einen Launch, ein Release oder ein Feature-Update handelt.

## Was sich geändert hat {#what-changed}

2026-07-18 — OpenCut war unter opencut.app und dem Repository OpenCut-app/OpenCut erreichbar. Die verlinkten Seiten zeigen an diesem Datum kein versioniertes Release und keine Funktionsänderung.

## Verwendung {#how-to-use-this}

Stand 2026-07-18 sollten Sie für die Bewertung oder Einführung des Projekts von der offiziellen OpenCut-Website und dem GitHub-Repository ausgehen.

1. Öffnen Sie die offizielle Website und wählen Sie „Try early beta“, um in den Projekt-Workspace zu gelangen.
  — <https://opencut.app/>
2. Für die Entwicklung der Neuentwicklung klonen Sie das Hauptrepository, installieren Proto und führen `proto use` aus, um die in `.prototools` festgelegten Werkzeuge zu installieren.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>
3. Starten Sie das erforderliche lokale Ziel: `moon run web:dev`, `moon run api:dev` oder `moon run desktop:dev`.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>

## Best Practices {#best-practices}

- Fixieren Sie die Toolchain mit `proto use`, bevor Sie Moon-Tasks ausführen.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>
- Behandeln Sie Plugins, MCP, Headless-Modus und Scripting als geplante Arbeit, nicht als aktive Abhängigkeiten.
  — <https://github.com/OpenCut-app/OpenCut/issues/811>
- Prüfen Sie die Architekturplanung, bevor Sie Code einreichen: Das Projekt gibt an, dass während der Neugestaltung keine externen Beiträge angenommen werden.
  — <https://github.com/OpenCut-app/OpenCut/blob/main/README.md>

## Hierdurch überholt {#superseded-by-this}

- 2026-05-17 — Beitragsrichtlinien für opencut-classic sind veraltet: Der Eigentümer hat das Repository archiviert und die Pflege eingestellt.
- 2026-05-26 — Die Behandlung der Editor-API, plattformübergreifender Plugins, des MCP-Servers, des Headless-Renderings oder des In-Editor-Scriptings als ausgelieferte Funktionen ist veraltet: Sie bleiben Ziele der Neuentwicklung ohne Liefertermine.

## Weiterhin unbekannt {#still-unknown}

- Wir wissen nicht, ob der 2026-07-18 ein Release, eine Änderung der Verfügbarkeit oder einen Verweis auf bestehende Einstiegspunkte markierte.
- Die Website bezeichnet ihren Einstiegspunkt als frühe Beta, die README besagt jedoch, dass opencut.app weiterhin den klassischen Editor betreibt.
- Wir haben keine offizielle Dokumentation oder Ankündigungen auf Vereinfachtem Chinesisch gefunden.
- Das Projekt nennt kein Veröffentlichungsdatum für die Neuentwicklung, Plugins, MCP, den Headless-Modus, Scripting sowie Desktop- oder Mobile-Builds.
- Die GitHub-Release-Linie endet mit v0.3.0 am 2026-04-15; offizielle Quellen sagen nicht, welches Release die frühe Beta trägt.
- Nicht verwandte Forks und Spiegel verwenden den Namen OpenCut; diese Seite behandelt nur OpenCut-app/OpenCut und opencut.app.
- Wir haben keinen verifizierten aktuellen Vertriebskanal für Desktop- oder Mobile-Versionen gefunden.
- Das klassische Repository und das Neuentwicklungs-Repository folgen unterschiedlichen Verträgen; eine dokumentierte Funktionsparität besteht nicht.
- Die frühe Beta wird per JavaScript gerendert, daher ist der Bearbeitungsworkflow nicht textuell dokumentiert.
- Wir haben nach der Ankündigung der Neuentwicklung keinen offiziellen Changelog-Eintrag gefunden.
- Speicherung, Export und Datenschutz der frühen Beta entsprechen nur dem, was das Projekt selbst angibt.
- Nicht-Entwickler haben heute keinen bestätigten Zugang zu den geplanten Automatisierungswerkzeugen.
- Offizielle Quellen nennen keine unterstützten Browser, Betriebssysteme, GPUs oder Videocodecs für die Beta.
- Die Release-Notes zu v0.3.0 beschreiben die Desktop-App als früh und schlicht, seitdem gibt es keine datierte Änderung.
- Wir wissen nicht, ob in der frühen Beta erstellte Projekte im archivierten klassischen Editor geöffnet werden können.
- Wir haben keinen offiziellen Paketmanager, Installer oder signierte Desktop-Version gefunden.
- Die Schaltfläche „Try early beta“ öffnet einen Workspace, aber die Dokumente beschreiben weder Kontoregeln noch Projektspeicherung.
- Der geplante MCP-Server, der Plugin-Host und der Scripting-Tab haben keine Release-Notes.
- Das Repository lehnt externe Pull Requests ab, solange die Architekturdokumentation vorbereitet wird; ein Enddatum ist nicht angegeben.
- Für die frühe Beta gibt es keine veröffentlichte Service-Level-Zusage und keine Support-Richtlinie.
- Ein Rust-Kern ist eine erklärte Richtung der Neuentwicklung, kein Nachweis, dass aktuelle Editor-Funktionen ihn nutzen.
- Wir haben keine offizielle chinesischsprachige Quelle gefunden, um Bedingungen, Support oder regionale Verfügbarkeit zu prüfen.
- Die alte Release-Funktionsliste belegt keine Funktionsparität mit dem Web-Workspace.
- Die verlinkten Seiten belegen die Identität, nicht aber den privaten Kontext des Beitrags vom 2026-07-18.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://opencut.app/ | OpenCut | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut | Repository OpenCut-app/OpenCut | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut/blob/main/README.md | OpenCut-README | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut/releases | OpenCut-Releases | 2026-09-05 |
| https://github.com/OpenCut-app/OpenCut/issues/811 | Tracking: OpenCut-Neuentwicklung | 2026-09-05 |
| https://github.com/OpenCut-app/opencut-classic | OpenCut-Legacy-Repository | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:opencut`, Thread `opencut-development`, 1 datiertes Ereignis 2026-07-18 → 2026-07-18.
- **Praxishinweis:** Stand 2026-07-18 sollten Praktiker die offizielle OpenCut-Website und das GitHub-Repository als Ausgangspunkte für die Bewertung oder Einführung des Projekts nutzen, vorbehaltlich der Prüfung der verlinkten Inhalte.
- **Konfidenz:** mittel. Datierte Überholungen sind maßgeblich dafür, was veraltet ist.
