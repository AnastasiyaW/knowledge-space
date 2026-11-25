---
title: "ComfyUI Mobile Frontend"
category: projects
date: 2026-08-12
tags: [comfyui-mobile-frontend, comfyui_mobile_frontend, project]
aliases: ["ComfyUI Mobile Frontend"]
level: 2
source_sha256: 9dacca8e72a92a77e5539af874666fcd66b14cf2c8cbb157a31a3ce5335dd39b
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI Mobile Frontend {#comfyui-mobile-frontend}

**Entwicklungslinie:** `project:comfyui-mobile-frontend` · Thread `comfyui-mobile-frontend`  
**Letztes Ereignis:** 2026-08-12 · 1 datiertes seit 2026-08-12 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

ComfyUI Mobile Frontend ist ein Custom Node für Personen, die ComfyUI betreiben und Workflows bearbeiten, Warteschlangen überwachen und Ausgaben von einem Smartphone oder Tablet aus verwalten möchten.

- Browser-Oberfläche, bereitgestellt unter `/mobile`.
- Workflow-Editor für Touchgeräte.
- Überwachung von Warteschlange und Verlauf.
- Ausgaben- und Medienbetrachter.

Die Unterstützung für Custom Nodes ist unvollständig, und das Projekt bezeichnet sich selbst als experimentell. Die neueste gefundene veröffentlichte Version ist v3.2.5 vom 2026-08-25. Nutze sie auf einem vertrauenswürdigen persönlichen ComfyUI-Server, nachdem du die benötigten Workflows und Nodes getestet hast.

## Entwicklungslinie {#development-line}

- **2026-08-12 — Öffentliche Referenzen zum ComfyUI Mobile Frontend wurden geteilt.** Am 2026-08-12 wurde die Entwicklungslinie des ComfyUI Mobile Frontend mit seinem GitHub-Repository und der CueForge-Website verknüpft. Damit entsteht ein datierter öffentlicher Bezugspunkt für das Projekt, wobei die geteilten Links jedoch weder ein Release, einen Funktionsumfang noch einen anderen konkreten Meilenstein dokumentieren.

## Was sich geändert hat {#what-changed}

2026-08-12 — v3.1.3 verbesserte die Ausgabenansicht, die Workflow-Steuerung und die Behandlung von Wildcards.

## So verwendest du es {#how-to-use-this}

Ab dem 2026-08-12 konnten Praktiker das verlinkte GitHub-Repository und die CueForge-Website als Ausgangsreferenzen bei der Bewertung von ComfyUI Mobile Frontend nutzen; allein aus diesem Ereignis sollten jedoch keine konkreten Fähigkeiten, Versionen oder Release-Stände abgeleitet werden.

1. Installiere es über ComfyUI-Manager unter dem Autor `cosmicbuffalo` oder klone das Repository in das Verzeichnis `custom_nodes` von ComfyUI.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend>
2. Starte ComfyUI neu und öffne anschließend `http://<server-ip>:8188/mobile`; verwende die Option `--listen` von ComfyUI, wenn du von einem anderen Gerät im LAN darauf zugreifst.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend>
3. Lade einen Workflow; fehlen Nodes, öffne über den Dialog den Custom Nodes Manager, gefiltert auf die fehlenden Node-Typen.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/USER_GUIDE.md>

## Bewährte Vorgehensweisen {#best-practices}

- Teste genau die Custom-Node-Workflows, die du benötigst, bevor du dich auf die mobile Oberfläche verlässt, da eine automatische Unterstützung für alle Custom Nodes nicht verfügbar ist.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend>
- Stelle einen ComfyUI-Server nicht für nicht vertrauenswürdige Clients bereit; setze ihn hinter eine Authentifizierung, ein VPN oder einen Reverse Proxy. Deaktiviere das Pairing mit CueForge über `COMFYUI_MOBILE_APP_PUSH=0`, falls es nicht gewünscht ist.
  — <https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/CUEFORGE_PRIVACY.md>

## Durch dieses Ereignis ersetzt {#superseded-by-this}

- 2026-08-16 — v3.2.0 ersetzte die rein englischsprachige Oberflächenhinweise, indem Vereinfachtes Chinesisch, Traditionelles Chinesisch, Japanisch und Koreanisch hinzugefügt wurden.
- 2026-08-25 — v3.2.5 ersetzte v3.2.4 als neueste veröffentlichte Version und ergänzte Unterstützung für einen clientgesteuerten Progress-Socket sowie eine Korrektur für Subgraph-Combos.

## Weiterhin unbekannt {#still-unknown}

- CueForge ist ein separater iOS-Client und keine Version des Custom Nodes. Die abgerufene offizielle Seite kündigt an, dass er bald im App Store erscheint; ein datierter Erstveröffentlichungsnachweis des Herstellers wurde jedoch nicht gefunden.
- Der abgerufene Changelog des Main-Branches kennzeichnet v3.2.5 als „Unreleased“, während die offizielle Releases-Seite v3.2.5 als neueste veröffentlichte Version vom 2026-08-25 auflistet; für die Auswahl der veröffentlichten Version ist die Release-Seite maßgeblich.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend | ComfyUI Mobile Frontend repository | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/releases | ComfyUI Mobile Frontend releases | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/releases/tag/v3.0.0 | Release v3.0.0 | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/releases/tag/v3.1.0 | Release v3.1.0 — Another big UX release | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/USER_GUIDE.md | ComfyUI Mobile User Guide | 2026-09-05 |
| https://github.com/cosmicbuffalo/comfyui-mobile-frontend/blob/main/CUEFORGE_PRIVACY.md | What this custom node sends to CueForge | 2026-09-05 |
| https://cueforge.dev/ | CueForge — ComfyUI on iPhone | 2026-09-05 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:comfyui-mobile-frontend`, Thread `comfyui-mobile-frontend`, 1 datiertes Ereignis 2026-08-12 → 2026-08-12.
- **Praktischer Hinweis:** Ab dem 2026-08-12 konnten Praktiker das verlinkte GitHub-Repository und die Cueforge-Website als Ausgangsreferenzen bei der Bewertung von ComfyUI Mobile Frontend nutzen; allein aus diesem Ereignis sollten keine konkreten Fähigkeiten, Versionen oder Release-Stände abgeleitet werden.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise oben sind maßgeblich für die Frage, was veraltet ist.
