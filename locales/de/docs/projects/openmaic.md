---
title: "OpenMAIC"
category: projects
date: 2026-03-16
tags: [openmaic, openmaic-development, project]
aliases: ["OpenMAIC"]
level: 2
source_sha256: edbb7f1400bb32e90646085c9d869842f0a52fea0779f44eec33abc390395d5b
translation: machine
translated_at: '2026-10-24'
---
# OpenMAIC {#openmaic}

**Entwicklungslinie:** `project:openmaic` · Thread `openmaic-development`  
**Letztes Ereignis:** 2026-03-16 · 1 datiertes seit 2026-03-16 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

OpenMAIC ist ein Open-Source-Generator für Unterrichtseinheiten für Lehrende und Lernende: Folien, Quizze, interaktive HTML-Szenen, projektbasiertes Lernen, KI-Diskussion mit Lehrenden und Peers, Whiteboard, TTS und Exporte. Der Self-Hosting-Betrieb erfordert derzeit Node.js 22.19+ und pnpm 10+. Fazit: Einsetzen, wenn eine generierte Lektion ein spielbares Klassenzimmer statt einer Chatbot-Antwort benötigt.

## Entwicklungslinie {#development-line}

- **2026-03-16 — Ressourcen des OpenMAIC-Projekts referenziert.** Am 2026-03-16 verwies eine datierte OpenMAIC-Meldung auf das GitHub-Repository des Projekts und die öffentliche Website. Die vorliegenden Belege belegen weder ein Release, ein Feature, einen Launch noch einen anderen technischen Meilenstein; dieses Ereignis hält daher nur die Verfügbarkeit dieser Projektressourcen fest.

## Was sich geändert hat {#what-changed}

2026-03-16 — OpenMAIC wurde als Projekt für interaktive Klassenzimmer mit mehreren Agenten gegründet und als Open Source veröffentlicht; das erste getaggte Release folgte am 2026-03-26.

## So wird es eingesetzt {#how-to-use-this}

Stand 2026-03-16 können Praktiker das referenzierte GitHub-Repository und die Projektwebsite als die identifizierten OpenMAIC-Ressourcen nutzen; die vorliegenden Belege etablieren keine konkreten Fähigkeiten, Releases oder Nutzungshinweise.

1. Repository klonen und Abhängigkeiten mit pnpm installieren.
  — <https://github.com/THU-MAIC/OpenMAIC>
2. `.env.example` nach `.env.local` kopieren und mindestens einen LLM-Anbieter konfigurieren.
  — <https://github.com/THU-MAIC/OpenMAIC>
3. `pnpm dev` ausführen und anschließend http://localhost:3000 öffnen; für einen Produktionsbuild `pnpm build && pnpm start` verwenden.
  — <https://github.com/THU-MAIC/OpenMAIC>
4. Für einen gemeinsam genutzten Betrieb `ACCESS_CODE` setzen, damit UI und API-Routen das Site-Passwort verlangen.
  — <https://github.com/THU-MAIC/OpenMAIC>

## Best Practices {#best-practices}

- Interaktive Widgets vor Version 0.3 als Kandidaten für Kompatibilitätsprüfungen behandeln: v0.3.0 hat den Same-Origin-Zugriff aus der iframe-Sandbox entfernt.
  — <https://raw.githubusercontent.com/THU-MAIC/OpenMAIC/main/CHANGELOG.md>
- Keine Zugangsdaten in Docker-Build-Argumenten ablegen; Image-Metadaten oder Build-Provenance können sie speichern.
  — <https://github.com/THU-MAIC/OpenMAIC>
- Für eine gemeinsam genutzte Instanz `ACCESS_CODE` verwenden, statt die generierten Klassenzimmer und API-Routen offen zu lassen.
  — <https://github.com/THU-MAIC/OpenMAIC>

## Hierdurch ersetzt {#superseded-by-this}

- 2026-06-28 — Die Hinweise zur kommerziellen Lizenzierung unter AGPL-3.0 sind veraltet: v0.3.0 hat OpenMAIC auf MIT umgestellt.
- 2026-06-28 — Hinweise, die davon ausgehen, dass interaktive Widgets Same-Origin-Zugriff per iframe nutzen dürfen, sind veraltet; diese Sandbox-Berechtigung wurde entfernt.

## Weiterhin unbekannt {#still-unknown}

- Der genaue Funktionsumfang und der Commit zum Launch am 2026-03-16 lassen sich aus keiner Launch-Tag-Quelle rekonstruieren: Das erste getaggte Release ist v0.1.0 vom 2026-03-26.
- Der gehostete Dienst wurde nicht als Beleg herangezogen, da seine Seite bei der Prüfung keine lesbaren Inhalte bereitstellte.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/THU-MAIC/OpenMAIC | THU-MAIC/OpenMAIC-Repository und aktuelle Einrichtungsanleitung | 2026-09-05 |
| https://raw.githubusercontent.com/THU-MAIC/OpenMAIC/main/CHANGELOG.md | OpenMAIC-Changelog | 2026-09-05 |
| https://shangqingtu.github.io/ | Shangqing Tu — News | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:openmaic`, Thread `openmaic-development`, 1 datiertes Ereignis 2026-03-16 → 2026-03-16.
- **Praktischer Hinweis:** Stand 2026-03-16 können Praktiker das referenzierte GitHub-Repository und die Projektwebsite als die identifizierten OpenMAIC-Ressourcen nutzen; die vorliegenden Belege etablieren keine konkreten Fähigkeiten, Releases oder Nutzungshinweise.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
