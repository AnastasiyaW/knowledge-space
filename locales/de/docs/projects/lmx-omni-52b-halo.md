---
title: "LMX-Omni-52B-Halo"
category: projects
date: 2026-06-12
tags: [lmx-omni-52b-halo, project]
aliases: ["LMX-Omni-52B-Halo"]
level: 2
source_sha256: 6eb3737b10406bb03330fd56b51fcb9ce8f013ff23bfd6e3a0b8caf4a92d980c
translation: machine
translated_at: '2026-10-24'
---
# LMX-Omni-52B-Halo {#lmx-omni-52b-halo}

**Entwicklungslinie:** `project:lmx-omni-52b-halo` · Thread `lmx-omni-52b-halo`  
**Letztes Ereignis:** 2026-06-12 · 1 datiertes Ereignis seit 2026-06-12 · **Recherchiert:** 2026-09-05 · Konfidenz: hoch

## Was es ist {#what-it-is}

LMX-Omni-52B-Halo ist ein Bündel aus Qwen3.6-35B-A3B-MTP, Flux-2-Klein-9B, Whisper-Large-v3-Turbo und kokoro-v1 für lokale multimodale Anwendungen. Funktionen: Chat und Bildanalyse; Bilderzeugung und Bildbearbeitung; Transkription; Sprachsynthese. Einschränkung: Das Laden der Komponenten belegt etwa 44,8 GB, und die Klasse Halo ist auf Geräte der Strix-Halo-Klasse ausgerichtet. Fazit: Wählen Sie das Modell für einen lokalen any-to-any-Prototyp oder eine entsprechende Anwendung, wenn der Umfang des Downloads und die Latenz der internen Tool-Calling-Schleife vertretbar sind.

## Entwicklungslinie {#development-line}

- **2026-06-12 — LMX-Omni-52B-Halo wurde mit seinem Hugging-Face-Modell-Repository verknüpft.** Am 2026-06-12 verzeichnete der Datensatz eine Verknüpfung mit dem Hugging-Face-Repository von LMX-Omni-52B-Halo. Dadurch gilt das Repository zu diesem Datum als Projektartefakt, es belegt jedoch weder den Veröffentlichungsstatus, die Fähigkeiten, die Lizenzierung noch den vorgesehenen Einsatzzweck.

## Was sich geändert hat {#what-changed}

2026-06-12 — Die Modellkarte beschrieb LMX-Omni-52B-Halo als einheitliches, OpenAI-kompatibles Omni-Bündel; das primäre Repository wurde am 2026-06-03 angelegt, und am 2026-06-04 wurde sein Manifest auf das unified format umgestellt und die alte collection.json entfernt. 2026-06-23 — Dem veröffentlichten Manifest wurde ein für die Collection konfigurierbarer System Prompt hinzugefügt. 2026-08-08 — Ein offener, ungelöster Bericht wurde eingereicht: Die Collection leitet das reasoning_content des Planners nicht in den Stream von Open WebUI weiter. Für eine Oberfläche, die einen sichtbaren Denkverlauf benötigt, bleibt dies eine Einschränkung.

## So verwenden Sie es {#how-to-use-this}

Ab dem 2026-06-12 sollten Praktiker das verknüpfte Hugging-Face-Repository als Ausgangspunkt nutzen, um die Artefakte und die Dokumentation von LMX-Omni-52B-Halo zu prüfen, bevor sie sich auf das Projekt verlassen.

1. Installieren Sie Lemonade und laden Sie anschließend alle Komponenten mit dem Befehl `lemonade pull LMX-Omni-52B-Halo` herunter; starten Sie das Modell mit dem Befehl `lemonade run LMX-Omni-52B-Halo`.
  — <https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo>
2. Wählen Sie in einem OpenAI-kompatiblen Client den Modellnamen für Anfragen an `/chat/completions`; der Server ruft die Komponenten selbst auf und gibt Bilder und Audio in der Antwortnachricht zurück.
  — <https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo>
3. Übergeben Sie in einem MCP-Client `model: "LMX-Omni-52B-Halo"` an `lemonade_omni`, wenn Sie einen einzelnen multimodalen Turn mit Bildern und Audio benötigen.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>

## Best Practices {#best-practices}

- Geben Sie Halo nur auf geeigneter Hardware ausdrücklich an; MCP verwendet standardmäßig das kleinere und schnellere LMX-Omni-5.5B-Lite.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>
- Legen Sie für MCP-Artefakte `output_dir` fest: Dadurch erhalten Dateien eindeutige Namen, und das ist für Clients geeignet, die keine audio content blocks anzeigen.
  — <https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md>
- Rechnen Sie nicht mit einer gestreamten Anzeige des Reasonings in Open WebUI: Das gemeldete Problem für Omni-Collections ist weiterhin offen.
  — <https://github.com/lemonade-sdk/lemonade/issues/2990>

## Hierdurch abgelöst {#superseded-by-this}

- 2026-05-21 — Die bisherige Anleitung zu den alten „Collections“ ist veraltet: Das Release Lemonade v10.6.0 hat sie durch die Modelle LMX-Omni-52B-Halo und LMX-Omni-5.5B-Lite ersetzt.
- 2026-06-04 — Das alte Manifest-Format `collection.json` für dieses Modell wurde durch die einheitliche Datei `LMX-Omni-52B-Halo.json` ersetzt.

## Weiterhin unbekannt {#still-unknown}

- Die Primärquelle datiert weder auf genau den 2026-06-12 eine Veröffentlichung noch eine Änderung; sie bestätigt den Zustand der Seite, enthält aber keinen eigenen Eintrag für ein Ereignis an diesem Tag.
- Das Antwortschema enthält die angefragten Felder event_findings und new_events nicht; deren tatsächliche Ergänzungen sind in what_changed und unknowns abgebildet.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo | Modellkarte LMX-Omni-52B-Halo | 2026-09-05 |
| https://huggingface.co/lemonade-sdk/LMX-Omni-52B-Halo/commits/main | Commit-Verlauf von LMX-Omni-52B-Halo | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/blob/main/docs/dev/lemonade-omni.md | Dokumentation zu Lemonade Omni Models | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/blob/main/docs/api/mcp.md | Dokumentation der Lemonade MCP API | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/releases/tag/v10.6.0 | Release Lemonade v10.6.0 | 2026-09-05 |
| https://github.com/lemonade-sdk/lemonade/issues/2990 | Omni-Collections streamen den reasoning_content des Planners nicht | 2026-09-05 |

## Agent-Kurzfassung {#agent-brief}

- **Gegenstand:** `project:lmx-omni-52b-halo`, Thread `lmx-omni-52b-halo`, 1 datiertes Ereignis vom 2026-06-12 bis 2026-06-12.
- **Praktischer Hinweis:** Ab dem 2026-06-12 sollten Praktiker das verknüpfte Hugging-Face-Repository als Ausgangspunkt nutzen, um die Artefakte und die Dokumentation von LMX-Omni-52B-Halo zu prüfen, bevor sie sich auf das Projekt verlassen.
- **Konfidenz:** hoch. Für die Frage, was veraltet ist, sind die datierten Ablösungen maßgeblich.
