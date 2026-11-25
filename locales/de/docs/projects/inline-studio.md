---
title: "Inline Studio"
category: projects
date: 2026-08-16
tags: [inline-studio, inline-studio-development, inlineresearch/inline-studio, project]
aliases: ["Inline Studio"]
level: 3
source_sha256: 08c66da8fd26412d9bb0402095ad90f6ebfd9e179fa1069c8fa1f01387034ff2
translation: machine
translated_at: '2026-10-24'
---
# Inline Studio {#inline-studio}

**Entwicklungslinie:** `project:inline-studio` · Thread `inline-studio-development`  
**Letztes Ereignis:** 2026-08-16 · 1 datiertes seit 2026-08-16 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

Inline Studio ist ein Open-Source-Workspace für charakterzentrierte Bild- und Videogenerierung. Er kombiniert einen Node-Canvas, portable `.char`-Dateien, lokales LoRA-Training, Modell-Nodes und Take-Historie.

- Konsistente Charaktergenerierung über Modell-Nodes hinweg.
- Lokale GPU- und API-Node-Generierung.
- LoRA-Training auf lokaler Hardware.
- Wiederverwendbare Workflows auf einem Node-Canvas.
- Take-Historie mit versionierten Render-Takes.

Die dokumentierte lokale Trainingsspitze liegt bei 8,6 GB bis 13,4 GB VRAM für mehrere 512-px-Modellpfade; LTX-2.5 benötigt 48 GB.

Einsetzen sollte man es, wenn Charakterkontinuität und ein lokaler Graph-Workflow wichtiger sind als ein One-Shot-Bildgenerator.

## Entwicklungslinie {#development-line}

- **2026-08-16 — Inline Studio veröffentlichte das Release v1.2.71.** Am 2026-08-16 veröffentlichte Inline Studio das GitHub-Release v1.2.71. Das Release verlinkte die Characters-Seite als Versions-Checkpoint, ohne konkrete Release-Inhalte zu beschreiben.

## Was sich geändert hat {#what-changed}

2026-08-16 — Release v1.2.71 erlaubt es FLUX.2-Generierungs-Nodes, portable `.char`-Dateien auszuwählen, ohne LoRA-Training oder Adapter.

2026-08-21 — Release v1.3.0 führte Training und Generierung zusammen und refaktorierte den Node-Graphen. Eine `.char`-Datei enthält nun Modell-Payloads für FLUX.2 und Krea 2.

2026-08-25 — Release v1.3.11 ergänzte `.char`-Unterstützung für die MiniMax-H3-Nodes für Text-zu-Video, Bild-zu-Video und Referenz-zu-Video.

2026-08-30 — Release v1.3.13 ergänzte Körper- und Kleidungsreferenzen für Charaktere und schützte die Take-Historie vor veralteten Browser-Schreibvorgängen.

2026-09-03 — Release v1.3.15 erweiterte die Charakterunterstützung auf API-Nodes, darunter MiniMax, Seedance und Nano Banana.

## So verwendest du es {#how-to-use-this}

Behandle Inline Studio v1.2.71 als Versions-Checkpoint vom 2026-08-16. Prüfe die Characters-Seite auf Charakterfunktionen, da die Links keine Migrationshinweise enthalten.

1. Installiere Python 3.11+ und klone das Repository. Führe `webui.bat --install --extra all` unter Windows bzw. `./webui.sh --install --extra all` unter macOS/Linux aus und starte anschließend die lokale UI.
  — <https://github.com/inlineresearch/Inline-Studio/blob/main/README.md>
2. Erstelle im Characters-Panel einen Charakter aus einem Foto oder einem bestehenden Take. Inline Studio speichert eine portable `.char`-Datei unter `models/characters`.
  — <https://inlinestudio.art/characters>
3. Wähle diesen Charakter in einem kompatiblen Generierungs-Node aus. Führe den Graphen aus und prüfe den Kontinuitätswert, der für jeden Take erfasst wird.
  — <https://inlinestudio.art/characters>

## Best Practices {#best-practices}

- Verwende abwechslungsreiche Referenzwinkel statt vieler Frontalbilder. Referenzen werden unabhängig voneinander abgeglichen, und jede verursacht zusätzliche Inferenz-Tokens.
  — <https://inlinestudio.art/characters>
- Beschränke Charakter-Workflows auf Einstellungen mit einer zentrierten Person. Bei Szenen mit mehreren Personen kann sich die Identität auf andere Gesichter ausbreiten, während der Wert trotzdem eine Übereinstimmung meldet.
  — <https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71>
- Behandle den Kontinuitätswert als Diagnosewerkzeug, nicht als Beleg für eine korrekte Menschenmenge im Bild. Der Wert setzt sich zu 0,8 aus Gesichtsähnlichkeit und zu 0,2 aus Subjektähnlichkeit zusammen. Ist kein Gesicht sichtbar, greift er auf die reine Subjektähnlichkeit zurück.
  — <https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71>

## Abgelöst durch {#superseded-by-this}

- 2026-08-21 — Release v1.3.0 ersetzte das reine FLUX.2-Format von v1.2.71 durch ein einheitliches `.char`-Format für FLUX.2 und Krea 2.
- 2026-08-25 — Release v1.3.11 löste den reinen Bildmodell-Charakter-Workflow für MiniMax-H3-Nodes ab.
- 2026-09-03 — Release v1.3.15 löste die auf lokale Modell-Nodes beschränkte Charakterunterstützung ab, indem sie auf unterstützte API-Nodes erweitert wurde.

## Weiterhin unbekannt {#still-unknown}

- GitHub datiert das Release v1.2.71 auf den 2026-08-15, unser Ereignisdatum ist jedoch der 2026-08-16. Wir behalten den 2026-08-16 als Ereignisdatum bei und halten den 2026-08-15 zu Kontextzwecken fest.
- Die Characters-Seite behandelt FLUX.2 und Krea 2, während die Release-Notes MiniMax H3 und ausgewählte API-Nodes ergänzen. Die Parität über andere Modelle hinweg ist nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://github.com/inlineresearch/Inline-Studio/releases/tag/v1.2.71 | Release v1.2.71 - Konsistente Charaktere, ohne LoRA-Training (nur Flux) | 2026-09-05 |
| https://inlinestudio.art/characters | Portable Charaktere: eine Datei für FLUX.2 und Krea 2 | 2026-09-05 |
| https://github.com/inlineresearch/Inline-Studio/releases | Inline-Studio-Releases | 2026-09-05 |
| https://github.com/inlineresearch/Inline-Studio/blob/main/README.md | Inline-Studio-README | 2026-09-05 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:inline-studio`, Thread `inline-studio-development`, 1 datiertes Ereignis 2026-08-16 → 2026-08-16.
- **Praktischer Hinweis:** Behandle Inline Studio v1.2.71 als Versions-Checkpoint vom 2026-08-16. Konsultiere die Characters-Seite für Charakterfunktionen; die Links enthalten keine Migrationshinweise.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich für die Frage, was veraltet ist.
