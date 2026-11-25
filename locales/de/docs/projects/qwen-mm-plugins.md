---
title: "Qwen-MM-Plugins — Entwicklung"
category: projects
date: 2026-08-10
tags: [development, project, qwen, qwen-mm-plugins]
aliases: ["Qwen-MM-Plugins"]
level: 3
source_sha256: 545fc7adbc4f2498695184293619f99bd37edd7d6eb1ca84a783fa94300a8366
translation: machine
translated_at: '2026-10-24'
---
# Qwen-MM-Plugins — Entwicklung {#qwen-mm-plugins-development}

**Entwicklungslinie:** `project:qwen-mm-plugins` · Thread `development`  
**Letztes Ereignis:** 2026-08-10 · 1 datiertes seit 2026-08-10 · **Recherchiert:** 2026-09-08 · Konfidenz: mittel

## Was es ist {#what-it-is}

Qwen-MM-Plugins bündelt fähigkeitsspezifische Skills und optionale MCP-Server für Agent-Harnesses. Es verbindet einen bestehenden Agenten mit Aufgaben aus den Bereichen Bild, Audio, Dokumente, Suche und 3D/CAD.

- `core`: lokales Lesen und Visualisieren von Bildern, Videos, Dokumenten, Daten, 3D-Dateien und NIfTI.
- `api` und `search`: modell- und API-basierte Aufgaben für Vision, OCR, Grounding, Audio, Web und Reverse-Image-Suche.
- `video-memory`, `video-edit`, `blender`, `freecad`, `edu-agent` und `omni-memory`: Workflows für lange Videos, Medienbearbeitung, Anwendungssteuerung, Bildung und audiovisuelles Gedächtnis.

`core` benötigt im Standardmodus für native Bilder keinen API-Schlüssel. Cloud-, Such-, reine Text-Captioning- und Gedächtnispfade erfordern Zugangsdaten oder Systemabhängigkeiten. Natives Windows ist nicht validiert. Beginne mit `core` in einem multimodalen Harness. Ergänze Fähigkeiten erst, wenn Anforderungen an Datenabfluss und Laufzeit es verlangen.

## Entwicklungslinie {#development-line}

- **2026-08-10 — Qwen-MM-Plugins-Repository referenziert.** Am 2026-08-10 verwies der Qwen-Thread auf das GitHub-Repository Qwen-MM-Plugins. Die Quelle nennt nur das Datum und den Repository-Link und behauptet weder ein Release noch eine Funktions- oder Modelländerung.

## Was sich geändert hat {#what-changed}

- 2026-08-10 — Qwen-MM-Plugins wurde in einer datierten Quelle erwähnt; das erreichbare Repository des Herstellers belegt weder einen Start, eine Erstellung noch ein Datum des ersten Commits.
- 2026-08-11 — Ein optionaler Rohmodus für Base64-Audio bei OpenAI-kompatiblen Endpunkten wurde zusammengeführt; der DashScope-Standard blieb unverändert.
- 2026-08-18 — `video-memory` v1.0.2 normalisierte lokale Datei-URIs über alle Fähigkeiten hinweg im Rahmen plattformübergreifender Pfadkorrekturen.
- 2026-08-20 — Getaggte Fähigkeits-Updates ergänzten einen Textfallback für MCP-Bildergebnisse.
- 2026-08-24 — `core` v1.0.5 ergänzte die Visualisierung von NIfTI-Volumina und die Auswahl von 4D-Volumina.
- 2026-09-03 — `omni-memory` v1.0.0 ergänzte audiovisuelles Gedächtnis für die Arbeit mit langen Videos.

## So wird es verwendet {#how-to-use-this}

1. Wähle eine Fähigkeit für die Aufgabe und verwende dann den geführten Installer für das Zielharness. Unter Windows nutze Ubuntu WSL2 und lege den Checkout im Linux-Home-Verzeichnis ab.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
2. Konfiguriere nur die erforderlichen Zugangsdaten und Systemwerkzeuge. Führe die Aktion Verify des Installers aus oder teste den MCP-Eintrag mit `--check-system`.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
3. Verweise im Harness auf eine Datei und beschreibe die Aufgabe in einfacher Sprache. Der installierte Skill wählt das passende MCP-Tool aus.
  — <https://github.com/QwenLM/Qwen-MM-Plugins>
4. Auf einem Host ohne Multimodalität setze `QWEN_MM_NATIVE_MODE=0` erst, nachdem ein VL-Endpunkt konfiguriert und das Hochladen von Bildern freigegeben wurde.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md>
5. Für einen Videoworkflow mit `omni-memory` frage zuerst `get_memory_status` ab. Erstelle oder setze das Gedächtnis nur fort, wenn Clip-Dauer und Status es rechtfertigen.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/cookbooks/omni-memory/usage.md>

## Best Practices {#best-practices}

- Fixiere dauerhafte Installationen auf unveränderliche Tags je Fähigkeit. Verwende `main` und den lokalen Checkout-Modus nur für die Entwicklung.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
- Aktualisiere Skill und MCP-Registrierung einer Fähigkeit gemeinsam und lade das Harness danach neu oder starte es neu.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md>
- Behalte die native Bildausgabe für einen multimodalen Host bei. Der Textfallback sendet zurückgegebene Bilder und Screenshots an den konfigurierten VL-Endpunkt.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md>
- Fixiere `QWEN_MM_SEARCH_BACKEND`, wenn die Auswahl des Anbieters reproduzierbar bleiben muss. Der Auto-Modus wählt das erste konfigurierte Backend.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md>
- Aktiviere `QWEN_MM_AUDIO_RAW_B64` nur für OpenAI-spezifikationskonforme Omni-Endpunkte, die rohes Base64 erfordern. Belasse DashScope beim Standardformat.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/pull/9>
- Prüse nach einem unterbrochenen omni-memory-Build die Clip-Abdeckung mit `get_memory_status`. Setze fort, statt einem unvollständigen Gedächtnis zu vertrauen.
  — <https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/cookbooks/omni-memory/usage.md>

## Durch diesen Eintrag ersetzt {#superseded-by-this}

- 2026-08-11 — Die Annahme, dass jeder OpenAI-kompatible Endpunkt Audio als DashScope-Data-URL akzeptiert. Der optionale Pfad mit rohem Base64 deckt Endpunkte wie vLLM ab, während DashScope den Standard behält.
- 2026-08-18 — Nicht normalisierte lokale Datei-URIs über alle Fähigkeiten hinweg. `video-memory` v1.0.2 normalisierte URIs und behob plattformübergreifende Pfade.
- 2026-08-20 — Native MCP-Bildblöcke als einziges dokumentiertes Format für Hosts ohne Multimodalität. Updates ergänzten einen Textfallback.
- 2026-08-24 — `core` ohne NIfTI-Visualisierung oder 4D-Volumenauswahl. `core` v1.0.5 ergänzte beides.

## Noch ungeklärt {#still-unknown}

- Der offizielle Qwen-Beitrag vom 10. August gab bei der Recherche HTTP 403 zurück. Die Angaben zum Ereignis stützen sich auf sekundäre Archive statt auf einen Beleg aus dem offiziellen Repository.
- Die Seiten des GitHub-Repositorys und der Releases belegen weder ein Erstellungsdatum noch einen ersten Commit oder ein GitHub-Release am 2026-08-10.
- Die breitere Qwen-Entwicklungslinie umfasst separate Projekte. Wir haben keine technischen Zusammenhänge, Kompatibilitäten oder Zuständigkeiten zu Qwen-MM-Plugins gefunden.
- Wir haben keine primäre Kompatibilitätsmatrix für OpenAI-kompatible Anbieter gefunden. Teste den gewählten Endpunkt und die Fähigkeit, bevor du dich darauf verlässt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/QwenLM/Qwen-MM-Plugins | QwenLM/Qwen-MM-Plugins repository README | 2026-09-08 |
| https://easyvibecoding.app/curated/2887-alibaba-qwen-shares-qwen-mm-plugins-native-multimodal-agent | EasyVibeCoding-Archiv des Qwen-MM-Plugins-Beitrags von Qwen | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/pull/9 | PR #9: optionales rohes Base64-Eingabeaudio für OpenAI-spezifizierte Server | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/tags | Qwen-MM-Plugins-Tags der Fähigkeiten | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/installation.md | Qwen-MM-Plugins installation guide | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/docs/en/configuration.md | Qwen-MM-Plugins configuration reference | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/blob/main/cookbooks/omni-memory/usage.md | Qwen-MM-Plugins omni-memory usage cookbook | 2026-09-08 |
| https://github.com/QwenLM/Qwen-MM-Plugins/releases | Qwen-MM-Plugins GitHub-Releases-Seite | 2026-09-08 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:qwen-mm-plugins`, Thread `development`, 1 datiertes Ereignis 2026-08-10 → 2026-08-10.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich für das, was veraltet ist.
