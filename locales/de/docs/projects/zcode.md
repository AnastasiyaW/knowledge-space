---
title: "ZCode 3.0 — ZCode IDE"
category: projects
date: 2026-06-15
tags: [project, zcode, zcode-ide, zcode_ide]
aliases: ["ZCode 3.0"]
level: 2
source_sha256: 68cb5ebe098b17cf0ad7c9fe0239f87dbcb8a984be97af6a96d32257698b0bba
translation: machine
translated_at: '2026-10-24'
---
# ZCode 3.0 — ZCode IDE {#zcode-30-zcode-ide}

**Entwicklungslinie:** `project:zcode` · Thread `zcode-ide`  
**Letztes Ereignis:** 2026-06-15 · 1 datiertes seit 2026-06-15 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ZCode 3.0 ist die Desktop-ADE von Z.ai. Es funktioniert als GUI-Harness für einen Agenten und nicht als reiner Terminal-Coding-Agent. Die Umgebung kombiniert ZCode Agent, Datei- und Workspace-Referenzen, Terminal-Befehle, Ausführungsberechtigungen, Git-Status, Review und Fernsteuerung. Aktuelle Downloads stellen v3.11.2 bereit. Die offizielle Dokumentation stellt das Produkt in den Mittelpunkt von GLM-5.3 und dem angegebenen Kontextfenster von 1M Token. Wir nutzen es wegen des integrierten Desktop-Workflows, nicht als Drop-in-Ersatz, der bestehende CLAUDE.md-Regeln rekursiv lädt.

## Entwicklungslinie {#development-line}

- **2026-06-15 — Installationsdokumentation für ZCode erschien.** Am 2026-06-15 veröffentlichte Z.ai englische Installationsdokumentation für ZCode. Die offizielle Installations-URL markiert einen Onboarding-Meilenstein der ZCode-3.0-Linie. Die verfügbaren Belege belegen keine Details zur Produktveröffentlichung, unterstützte Plattformen oder ob die Anleitung selbst an diesem Tag erstmals erschien.

## Was sich geändert hat {#what-changed}

- **2026-06-15** — Der Installationslink für ZCode 3.0 verwies auf den Desktop-Client. Die zugehörige Veröffentlichung vom 2026-06-13 wechselte auf den hauseigenen ZCode Agent, abgestimmt auf GLM-5.2. Sie ergänzte gruppierte Aufgaben-Workspaces, Zread-Projektwissen, einen Git-Branch-Graphen, Monitoring und Anhangseingabe.
- **2026-08-14** — ZCode v3.7.7 machte GLM-5.3 verfügbar.
- **2026-08-20** — ZCode v3.8.1 fügte globale und workspace-bezogene Steuerungen für Agentenfähigkeiten sowie Hooks auf Workspace-Ebene hinzu.
- **2026-08-26** — ZCode v3.9.2 ergänzte GLM-5.3 Flash und explizite Abfragen für Berechtigungen zur Computersteuerung.
- **2026-09-04** — ZCode v3.11.2 ergänzte PDF- und Medienvorschauen in Unterhaltungen sowie die workspace-spezifische Installation von Plugins.

## Verwendung {#how-to-use-this}

Ab dem 2026-06-15 die offizielle englische Installationsanleitung für die Einrichtung verwenden. Die verfügbaren Quellen bestätigen unterstützte Umgebungen und Funktionsumfang der Veröffentlichung nicht.

1. Den aktuellen Build für macOS, Windows oder Linux herunterladen und installieren.
  — <https://zcode.z.ai/en/docs/install>
2. Beim ersten Start das Projektverzeichnis als Workspace auswählen und eine kleine Anweisung senden, um zu prüfen, ob der Agent antwortet.
  — <https://zcode.z.ai/en/docs/install>
3. Ein Z.ai- oder BigModel-Konto verbinden oder einen kompatiblen Drittanbieter bzw. API-Key-Provider konfigurieren.
  — <https://zcode.z.ai/en/docs/configuration>
4. Dauerhafte Teamregeln, Validierungsbefehle und Hinweise zu risikoreichen Dateien in der AGENTS.md im Workspace-Root ablegen.
  — <https://zcode.z.ai/en/docs/agents>
5. Ein konkretes Ziel formulieren, relevante Dateien mit @ anhängen und dann einen Ausführungsmodus wählen, der zum Risiko der Aufgabe passt.
  — <https://zcode.z.ai/en/docs/agents>

## Best Practices {#best-practices}

- Plan-Modus oder Ask vor Änderungen für kritische Dateien, Shell-Befehle und umfassende Änderungen verwenden. Full access für klar umrissene Arbeiten mit geringerem Risiko vorbehalten.
  — <https://zcode.z.ai/en/docs/agents>
- Wichtige Projektregeln in der AGENTS.md des aktuellen Workspaces halten. ZCode führt verschachtelte Dateien nicht zusammen und löst keine Importe auf.
  — <https://zcode.z.ai/en/docs/agents>
- Für einen API-Key des Coding Plan den coding-spezifischen Endpunkt statt des allgemeinen API-Endpunkts verwenden.
  — <https://zcode.z.ai/en/docs/configuration>
- Für einen einfachen, wiederverwendbaren Prompt Commands verwenden. Skills einsetzen, wenn der Workflow zusätzlich Skripte, Vorlagen oder Beispiele benötigt.
  — <https://zcode.z.ai/en/docs/commands>
- Einen erforderlichen Proxy innerhalb von ZCode konfigurieren. Ein leeres Proxy-Feld verbindet direkt und übernimmt HTTP_PROXY nicht.
  — <https://zcode.z.ai/en/docs/install>

## Durch dieses ersetzt {#superseded-by-this}

- 2026-08-14 — Die Standardauswahl des Modells stützt sich nicht mehr auf GLM-5.2 aus der Veröffentlichung von ZCode 3.0. Release v3.7.7 machte GLM-5.3 verfügbar, und die aktuelle Dokumentation zum ZCode Agent stellt die GLM-5.3-Familie in den Mittelpunkt.
- 2026-09-04 — Der Download von ZCode 3.0 ist für neue Installationen veraltet. Der aktuelle offizielle Download ist v3.11.2.

## Weiterhin unbekannt {#still-unknown}

- Wir fanden in der indexierten offiziellen Historie keine datierte Release-Notiz von ZCode 3.0 aus erster Hand und keinen unveränderlichen Hash des v3.0-Installers. Ein datierter Sekundärbericht stützt die Details zur Veröffentlichung vom 2026-06-13, ersetzt aber keine archivierte primäre Release-Notiz.
- Wir haben den angegebenen In-App-Quota-Vorteil von 150 % sowie Behauptungen zu einer besseren Aufgabenerledigung gegenüber Drittanbieter-Agenten nicht unabhängig gemessen. Wir empfehlen sie nicht.
- Aktuelle Tarif-Quotas, Verfügbarkeit der Provider und Desktop-Versionen sind veränderlich. Wir geben keine Preis- oder Quota-Empfehlung.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://zcode.z.ai/en/docs/install | Install | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/docs/agents | ZCode Agent | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/docs/configuration | Connect Models | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/docs/commands | Command | ZCode Docs | 2026-09-05 |
| https://zcode.z.ai/en/changelog | ZCode Releases & Updates | GLM-5.3 Coding Agent | 2026-09-05 |
| https://zcode.z.ai/cn/docs/install | 安装 | ZCode Docs | 2026-09-05 |
| https://www.ithome.com/0/963/985.htm | 智谱 AI 编程工具 ZCode 3.0 版本发布：切换自研 ZCode Agent 内核，深度适配 GLM-5.2 | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:zcode`, Thread `zcode-ide`, 1 datiertes Ereignis 2026-06-15 → 2026-06-15.
- **Praxishinweis:** Ab dem 2026-06-15 sollten Praktiker, die ZCode evaluieren, die offizielle englische Installationsanleitung als Einstiegspunkt nutzen. Die verfügbaren Quellen bestätigen unterstützte Umgebungen und Funktionsumfang der Veröffentlichung nicht.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
