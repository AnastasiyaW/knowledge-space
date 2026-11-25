---
title: "Gemini"
category: projects
date: 2026-07-22
tags: [gemini, gemini-app, gemini-gems, gemini-product-development, google-gemini, project]
aliases: ["Gemini", "Google Gemini"]
level: 3
source_sha256: ce252c4cf2fd525d123c2533549a65e9ac37ed8108c55429969039e487c48dc0
translation: machine
translated_at: '2026-10-24'
---
# Gemini {#gemini}

**Entwicklungslinie:** `project:google-gemini` · Thread `gemini-product-development`  
**Letztes Ereignis:** 2026-07-22 · 1 datiertes seit 2026-07-22 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Gemini ist Googles Produktfamilie für Chat, Dateien, Code und Modellintegration in Anwendungen.
- Gemini Apps: Konversation, Anhänge und Modellauswahl.
- Gems: gespeicherte Anweisungen für wiederkehrende Aufgaben.
- Gemini API und AI Studio: multimodale Aufrufe, strukturierte Ausgaben und Tools.

Verfügbare Modell-IDs und ihr Status ändern sich; der aktuelle Katalog enthält `gemini-3.8-flash`, während `gemini-3.6-flash` weiterhin gelistet ist. Für persönliche Routinen eignet sich ein Gem, für Produkte die API mit expliziter Modellwahl und Antwortprüfungen.

## Entwicklungslinie {#development-line}

- **2026-07-22 — Gemini 3.6 Flash wurde mit aktualisierten Flash-Modellvarianten verknüpft.** Eine verlinkte Google-Seite vom 2026-07-21 stellte Gemini 3.6 Flash, 3.5 Flash-Lite und einen begrenzten Pilotbetrieb von 3.5 Flash Cyber vor; 3.6 und 3.5 Flash-Lite wurden über Gemini API und AI Studio verfügbar.

## Was sich geändert hat {#what-changed}

- 2024-05-14 — Gemini Apps: Gemini Advanced erhielt Gemini 1.5 Pro mit einem Kontextfenster von 1 Million Token und Dateiuploads.
- 2024-05-14 — Gems: Google kündigte anpassbare Versionen von Gemini an, markiert mit „soon“ statt als bestätigter öffentlicher Start.
- 2024-05-14 — Gemini API: Google führte Gemini 1.5 Flash für hochfrequente Aufgaben ein, während Gemini 1.5 Pro in API und AI Studio Kontext bis zu 2 Millionen Token und Audioverarbeitung erhielt.
- 2024-12-20 — AI Studio: Eine neue Chat-URL tauchte auf, ohne Modell, Version oder Release anzugeben; die konkrete Änderung ist daher unbestätigt.
- 2026-07-22 — Flash-Reihe: Eine verlinkte Google-Seite vom 2026-07-21 stellte Gemini 3.6 Flash, 3.5 Flash-Lite und einen begrenzten Pilotbetrieb von 3.5 Flash Cyber vor; 3.6 und 3.5 Flash-Lite wurden über Gemini API und AI Studio verfügbar.
- 2026-09-04 — Aktueller Katalog: Die Gemini API listet `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.6-flash` und `gemini-3.5-flash-lite`; 3.6 ist nicht mehr die einzige aktuelle Wahl.

3.5 Flash Cyber wurde nicht als öffentliches API-Modell veröffentlicht; Google beschreibt einen Pilotbetrieb für Behörden und vertrauenswürdige Partner über CodeMender. Für neue Integrationen sollte eine Version aus dem aktuellen Katalog gewählt werden, nicht aus einem alten AI-Studio-Link.

## Anwendung {#how-to-use-this}

Ab 2026-07-22 sollte Gemini 3.6 Flash als Kandidat für ein Modell in AI Studio behandelt werden. Fähigkeiten, Rollout und Preise sind vor einer Übernahme im verlinkten offiziellen Modell-Update zu prüfen.

1. Für persönliche Aufgaben: Gemini Apps öffnen, anmelden, ein Modell auswählen, bei Bedarf eine Datei oder ein Bild anhängen und den Prompt senden.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
2. Für wiederkehrende Rollen: Explore Gems → New Gem öffnen. Name festlegen, Anweisungen zu Rolle, Aufgabe, Kontext und Format ergänzen, in der Vorschau testen und speichern.
  — <https://support.google.com/gemini/answer/15235603>
3. Für Integrationen: In AI Studio ein Projekt und einen API-Schlüssel anlegen. Den Schlüssel in einer Umgebungsvariablen speichern, das SDK installieren und den ersten Aufruf der Interactions API aus Python, JavaScript oder REST absetzen.
  — <https://ai.google.dev/gemini-api/docs/get-started>
4. Vor der Veröffentlichung eine exakte Modell-ID aus dem aktuellen Katalog in der Konfiguration festschreiben. Die aktuelle Dokumentation beginnt mit `gemini-3.8-flash`.
  — <https://ai.google.dev/gemini-api/docs/models?hl=en>
5. Wenn Antworten aktuelle Daten erfordern, Google Search anbinden. Beim Aufruf interner Systeme eine Funktion deklarieren, sie in der Anwendung ausführen und das Ergebnis an das Modell zurückgeben.
  — <https://ai.google.dev/gemini-api/docs/tools>

## Best Practices {#best-practices}

- Ziel, Randbedingungen, Format und Kontext explizit angeben; bei Stil oder Klassifikation mehrere konsistente Beispiele verwenden.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Bei Gemini 3.x zunächst Temperature, Top-p und Top-k auf den Standardwerten belassen; jede Änderung dokumentieren und testen, da Feinabstimmung komplexes Schlussfolgern verschlechtern oder Schleifen auslösen kann.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Structured Outputs für feste Endformate und Function Calling für Aktionen verwenden; das Schema-JSON auf Semantik und Geschäftsregeln prüfen.
  — <https://ai.google.dev/gemini-api/docs/structured-output>
- Antworten von Gemini Apps vor beruflichen Entscheidungen überprüfen; die Hilfedokumentation warnt ausdrücklich, dass die App Fehler machen kann.
  — <https://support.google.com/gemini/answer/13275745?hl=en>
- Vor dem Senden von Arbeitsdaten einen Tarif wählen; Google gibt an, dass Inhalte im Free-Tarif zum Training der Produkte verwendet werden, im Paid-Tarif jedoch nicht. Team- und Vertragsbedingungen sind daher zu prüfen.
  — <https://ai.google.dev/gemini-api/docs/pricing>

## Durch Folgendes ersetzt {#superseded-by-this}

- 2024-05-14: „Gems coming soon“ ist veraltet; die aktuelle Hilfedokumentation erklärt, wie Gems erstellt, getestet und gespeichert werden.
- 2024-05-14: Eine neue API-Integration mit Gemini 1.5 Flash oder 1.5 Pro zu beginnen, ist veraltet; der aktuelle Gemini-API-Katalog konzentriert sich auf 3.x und listet Gemini 3.8 Flash.
- 2026-07-22: Gemini 3.6 Flash und 3.5 Flash-Lite bleiben verfügbar, aber 3.6 Flash ist nicht mehr das neueste Flash-Modell; der Katalog enthält zusätzlich 3.7 und 3.8 Flash.
- 2024-12-20: Die neue AI-Studio-Chat-URL ist ein Einstiegspunkt, keine stabile Empfehlung für eine Modellversion.

## Weiterhin unbekannt {#still-unknown}

- Der genaue Wortlaut für die beiden Einträge vom 2024-05-14 ist nicht verfügbar; die offiziellen Ankündigungen dieses Tages bestätigen die Richtung, nicht den vollständigen Text.
- Der Eintrag vom 2024-12-20 nennt nur eine neue AI-Studio-Chat-URL, ohne Modell, Version oder Release anzugeben.
- Gemini Apps, Gems und Gemini API sind verschiedene Oberflächen einer Familie, keine getrennten Projekte; die Verfügbarkeit hängt von Konto, Tarif, Region und Modell ab.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://blog.google/products-and-platforms/products/gemini/google-gemini-update-may-2024/ | Mehr erledigen mit Gemini: 1.5 Pro und weitere intelligente Funktionen ausprobieren | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/google-gemini-update-flash-ai-assistant-io-2024/ | Gemini bricht mit einem schnelleren Modell, längerem Kontext, KI-Agenten und mehr neue Wege ein | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ | Vorstellung von Gemini 3.6 Flash, 3.5 Flash-Lite und 3.5 Flash Cyber | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models?hl=en | Models | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/get-started | Getting started | Gemini API | Google AI for Developers | 2026-09-04 |
| https://support.google.com/gemini/answer/13275745?hl=en | Gemini Apps verwenden | 2026-09-04 |
| https://support.google.com/gemini/answer/15235603 | Tipps zum Erstellen benutzerdefinierter Gems | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt design strategies | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/tools | Using tools with Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/structured-output | Structured outputs | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/pricing | Gemini Developer API pricing | Gemini API | Google AI for Developers | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Thema:** `project:google-gemini`, Thread `gemini-product-development`, 1 datiertes Ereignis 2026-07-22 → 2026-07-22.
- **Praxishinweis:** Ab 2026-07-22 sollten Praktiker Gemini 3.6 Flash als Kandidat für die Modellauswahl in AI Studio behandeln und Fähigkeiten, Rollout und Preise im verlinkten offiziellen Modell-Update prüfen, bevor sie es übernehmen.
- **Konfidenz:** mittel. Datierte Ersetzungen oben sind maßgeblich dafür, was veraltet ist.
