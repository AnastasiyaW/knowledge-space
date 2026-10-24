---
title: "MiniMax"
category: organizations
date: 2025-12-27
tags: [minimax, minimax-models-and-products, minimax_models, organization]
aliases: ["MiniMax"]
level: 3
source_sha256: fef8ae2b00f124b6f62e25f22198d5a3b6fbdecbb197aed2e13d683c6c1d8a32
translation: machine
translated_at: '2026-10-24'
---
# MiniMax {#minimax}

**Entwicklungslinie:** `organization:minimax` · Thread `minimax-models-and-products`  
**Letztes Ereignis:** 2025-12-27 · 3 datierte seit 2025-06-18 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

MiniMax stellt KI-Modelle und Dienste bereit. Entwickler erhalten eine Anthropic-SDK-kompatible API, daneben Video- und Sprachdienste; Kreative erhalten die separaten Produkte Hailuo und Audio.

- M3: Sprache, Tool-Nutzung, Bild- und Videoeingabe sowie ein Kontextfenster von 1 Mio. Token.
- H3: Videogenerierung aus Text, Bild, erstem/letztem Frame und multimodalen Referenzen.
- Speech 2.8: Sprachsynthese, Stimmklonen und Stimmgestaltung.

## Entwicklungslinie {#development-line}

- **2025-06-18 — MiniMax veröffentlichte Ressourcen zum Modell MiniMax-M1.** Am 2025-06-18 verlinkte MiniMax eine Hugging-Face-Collection für MiniMax-M1 sowie ein GitHub-Repository für das Modell. Der gleiche datierte Linksatz verwies auf Hailuo Create und MiniMax Agent und stellte das Modell neben Video- und Agent-Oberflächen.
- **2025-06-22 — MiniMax machte sein Audio-Produkt öffentlich sichtbar.** Sprache bleibt eine eigenständige API-Linie mit Synthese, Stimmklonen und Stimmgestaltung; der Zugang zu Musik hat sich wesentlich geändert.
- **2025-12-27 — MiniMax machte M2.1 über gehostete und lokale Zugangswege sichtbar.** Am 2025-12-27 verlinkte MiniMax seine Nachrichtenseite zu MiniMax-M2.1 und das Hugging-Face-Modell-Repository. Das datierte Ressourcenset verwies außerdem auf MiniMax Agent, eine Referenz zur Anthropic-kompatiblen Text-API, OpenRouter und Ollama und listete damit mehrere Zugangswege für M2.1 auf.

## Was sich geändert hat {#what-changed}

2024-10-10 — Für ein MiniMax-Ereignis liegen kein erhaltener Text und keine URL vor, daher gibt es keine quellengestützte historische Aussage. MiniMax' nächstliegende primäre Ausgangsbasis ist Video-01, veröffentlicht am 2024-08-31 mit Text-zu-Video und Bild-zu-Video in 720p/25 fps für bis zu sechs Sekunden. Dies ist Kontext, keine Bestätigung der Änderung vom 10. Oktober.

2025-06-18 — MiniMax M1 und Hailuo 02 wurden erfasst. M1 war ein Open-Weight-Reasoning-Modell mit hybrider Aufmerksamkeit, 456 Mrd. Parameter insgesamt, 45,9 Mrd. aktive Parameter und 1 Mio. Kontext. Hailuo 02 ergänzte native 1080p-Videooptionen.

2025-06-20 — Hailuo Video Agent ging als Beta mit vorgefertigten Videovorlagen als Stufe eins an den Start. Spätere autonome Stufen waren eine Roadmap, keine verifizierten Fähigkeiten.

2025-06-22 — Ein MiniMax-Audio-Endpunkt erschien, die Seite nennt jedoch keine datierten Angaben zur Veröffentlichung. Sprache bleibt eine separate API-Linie mit Synthese, Stimmklonen und Stimmgestaltung; der Zugang zu Musik hat sich wesentlich geändert.

2025-12-27 — M2.1 wurde als Open-Weight-Modell der M2-Reihe mit Agenten-Ausrichtung für mehrsprachiges Programmieren, Tool-Nutzung, Befolgen von Anweisungen und langfristige Aufgaben erfasst. Die Release-Notiz von MiniMax ist auf 2025-12-23 datiert, während die Modell-Release-Notes 2025-12-22 angeben.

Heute gefunden — M3 wurde am 2026-06-01 als aktuelles Sprachmodell mit 1 Mio. Kontext veröffentlicht. H3 wurde am 2026-08-03 als multimodale Videolinie quelloffen gemacht. Der Zugang zur Music-API hat sich am 2026-08-20 für neue Nutzer geändert.

## Anwendung {#how-to-use-this}

Stand 2025-12-27: Bewerten Sie MiniMax-Modelle anhand jedes aufgeführten Zugangswegs – MiniMax Agent, der Text-API, OpenRouter oder Ollama – statt davon auszugehen, dass eine einzige Oberfläche alle Produkte abdeckt.

1. Wählen Sie zuerst die aktuelle Oberfläche: M3 für Sprache, Programmierung, Tool-Nutzung oder multimodale API-Arbeit; H3 für Video; Speech 2.8 für Sprache. Gehen Sie nicht von historischen Bezeichnungen wie M2.1 oder Hailuo aus.
  — <https://platform.minimax.io/docs/guides/models-intro>
2. Erstellen Sie auf der MiniMax-Plattform einen API-Schlüssel mit Pay-as-you-go-Abrechnung, um auf Sprach-, Video-, Sprach- und Bildmodelle zuzugreifen.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
3. Für Sprachintegrationen setzen Sie `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic` im Anthropic SDK, verwenden den MiniMax-API-Schlüssel und rufen `MiniMax-M3` auf.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
4. Für Tool-Aufrufe fügen Sie die vollständige Assistentenantwort – Denkblöcke, Textblöcke und Tool-Use-Blöcke – dem Verlauf hinzu, bevor Sie Tool-Ergebnisse und den nächsten Zug senden.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
5. Für H3-Video erstellen Sie eine asynchrone Aufgabe, speichern die `task_id`, fragen den Status ab und holen die Ausgabe-URL nach erfolgreichem Abschluss. Wählen Sie Eingaben und Dauer innerhalb des Bereichs von 4 bis 15 Sekunden.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
6. Für Sprache verwenden Sie synchrones T2A für kurze interaktive Audioausgaben und asynchrone Synthese für lange Texte. Starten Sie keine neue Music-API-Integration; verwenden Sie stattdessen MiniMax Audio oder das offene Modell Music 3.
  — <https://platform.minimax.io/docs/api-reference/api-overview>

## Best Practices {#best-practices}

- Behandeln Sie die Anthropic-Kompatibilität als dokumentierte Teilmenge: Die API ignoriert `top_k`, Stop-Sequenzen, MCP-Server, Kontextverwaltung und Container, statt sie nachzubilden.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Nutzen Sie das adaptive Denken von M3 für komplexes Reasoning und deaktivieren Sie es für geringe Latenz; lassen Sie Denkblöcke über Tool-Use-Züge hinweg unverändert.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Verwenden Sie für Bild- oder Videoeingaben M3 – nicht M2.x – und schätzen Sie die Token-Anzahl ab, bevor Sie große multimodale Anfragen senden.
  — <https://platform.minimax.io/docs/api-reference/text-anthropic-api>
- Behandeln Sie M2.1, Hailuo 02/2.3 und ältere Sprachmodelle als Legacy, die eine explizite Kompatibilitäts- oder Migrationsentscheidung erfordern.
  — <https://platform.minimax.io/docs/guides/models-intro>
- Behandeln Sie Videogenerierung als Auftragsworkflow statt als synchronen Aufruf: Speichern Sie Task-IDs, fragen Sie den Status ab und behandeln Sie Abbruch oder Löschung sauber.
  — <https://platform.minimax.io/docs/api-reference/api-overview>
- Wenn ein Deployment lokale M2.1-Gewichte erfordert, stellen Sie sie über SGLang oder vLLM bereit und prüfen Sie die Modified-MIT-Lizenz vor der Auslieferung.
  — <https://huggingface.co/MiniMaxAI/MiniMax-M2.1>
- Prüfen Sie die Kontoberechtigung, bevor Sie Musik-Workflows aufbauen: Neue Nutzer können nicht auf kostenpflichtige Music-APIs zugreifen, und kostenlose Endpunkte wurden eingestellt.
  — <https://platform.minimax.io/docs/api-reference/api-overview>

## Hierdurch abgelöst {#superseded-by-this}

- 2024-08-31 / 2024-10-10 — Die Limits von Video-01 (720p, 25 fps, bis zu sechs Sekunden) sind Legacy. H3 deckt multimodale Eingaben, Ausgaben von 4 bis 15 Sekunden, 24 fps und bis zu 2K ab.
- 2025-06-18 — M1 als standardmäßig gehostetes Modell mit 1 Mio. Kontext ist historisch. MiniMax dokumentiert M3 als aktuelles Sprachmodell mit 1 Mio. Kontext; M1 ist Archiv oder selbst gehostetes Open-Weight-Modell.
- 2025-06-20 — Die Beta von Hailuo Video Agent Stufe eins sowie die Roadmap für Stufe zwei und drei sind historisch. Prüfen Sie aktuelle Funktionen anhand von H3 und der API-Dokumentation, statt anzunehmen, dass die Roadmap ausgeliefert wurde.
- 2025-12-27 — M2.1 als Flaggschiff-Modell zu wählen, ist veraltet. Es bleibt API-kompatibel und herunterladbar, doch MiniMax ordnet es den Legacy-Modellen zu.
- 2025-06-22 — Einen Music-API-Workflow auf Basis älterer MiniMax-Audio-Anleitungen zu beginnen, ist veraltet: Ab 2026-08-20 sind kostenpflichtige Music-APIs für neue Nutzer geschlossen und kostenlose Endpunkte eingestellt.

## Weiterhin unbekannt {#still-unknown}

- Zum Ereignis vom 2024-10-10 existiert kein erhaltener Link und kein Text. Die Video-01-Seite vom 2024-08-31 ist Kontext, kein Beleg für die Oktoberänderung.
- Die Links `https://hailuoai.video/create`, `https://agent.minimax.io/` und `https://www.minimax.io/audio` lieferten bei der Abfrage JavaScript-Hüllen zurück; aktuelle Consumer-UX und Verfügbarkeit sind daher nicht verifiziert.
- Der X-Beitrag vom 2025-06-20 war nicht lesbar. Eine gleichtägige Ankündigung von Hailuo Video Agent aus erster Hand existiert, die genaue Übereinstimmung ist jedoch nicht verifiziert.
- Das Veröffentlichungsdatum von M2.1 variiert in den Quellen: 2025-12-27 im datierten Ereignis, 2025-12-23 im Release-Artikel und 2025-12-22 in den API-Release-Notes.
- `minimax` und `minimax_models` vermischen Unternehmensgeschichte mit Modell-Linien. Sie hängen zusammen, bilden aber keinen einheitlichen Produktlebenszyklus.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://www.minimax.io/news/video-01 | MiniMax officially releases the Video-01 video generation model | 2026-09-04 |
| https://huggingface.co/collections/MiniMaxAI/minimax-m1-68502ad9634ec0eeac8cf094 | MiniMax-M1 - a MiniMaxAI Collection | 2026-09-04 |
| https://github.com/MiniMax-AI/MiniMax-M1 | MiniMax-AI/MiniMax-M1 | 2026-09-04 |
| https://www.minimax.io/news/minimax-hailuo-02 | MiniMax Hailuo 02, World-Class Quality, Record-Breaking Cost Efficiency | 2026-09-04 |
| https://www.minimax.io/news/video-agent | Introducing Hailuo Video Agent in Beta, Vibe Videoing with Zero-touch | 2026-09-04 |
| https://www.minimax.io/news/minimax-m21 | MiniMax M2.1: Significantly Enhanced Multi-Language Programming, Built for Real-World Complex Tasks | 2026-09-04 |
| https://platform.minimax.io/docs/release-notes/models | Models - MiniMax API Docs release notes | 2026-09-04 |
| https://huggingface.co/MiniMaxAI/MiniMax-M2.1 | MiniMaxAI/MiniMax-M2.1 | 2026-09-04 |
| https://platform.minimax.io/docs/guides/models-intro | Models - MiniMax API Docs | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/api-overview | API Overview - MiniMax API Docs | 2026-09-04 |
| https://platform.minimax.io/docs/api-reference/text-anthropic-api | Anthropic SDK - MiniMax API Docs | 2026-09-04 |
| https://www.minimax.io/models/text/m3 | MiniMax M3 - Coding & Agentic Frontier, 1M Context, Multimodal | 2026-09-04 |
| https://www.minimax.io/news/minimax-h3-open-source | Open General Intelligence: MiniMax H3 Is Now Open Source | 2026-09-04 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `organization:minimax`, Thread `minimax-models-and-products`, 3 datierte Ereignisse 2025-06-18 → 2025-12-27.
- **Praxishinweis:** Stand 2025-12-27 sollten Praktiker die Nutzung von MiniMax-Modellen anhand des ausdrücklich aufgeführten Zugangswegs bewerten – MiniMax Agent, der Text-API, OpenRouter oder Ollama – statt davon auszugehen, dass eine einzige Oberfläche alle MiniMax-Produkte abdeckt.
- **Konfidenz:** mittel. Die datierten Ablösungen oben sind maßgeblich für das, was veraltet ist.
