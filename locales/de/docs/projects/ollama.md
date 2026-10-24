---
title: "Ollama — Produktentwicklung"
category: projects
date: 2026-01-22
tags: [ollama, product-development, project]
aliases: ["Ollama"]
level: 2
source_sha256: ea28751ddad14f28a58e16889bae3832622d517d7d31f7a3650ec259df555845
translation: machine
translated_at: '2026-10-24'
---
# Ollama — Produktentwicklung {#ollama-product-development}

**Entwicklungslinie:** `project:ollama` · Thread `product-development`  
**Letztes Ereignis:** 2026-01-22 · 2 datierte seit 2025-05-19 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Ollama ist eine lokale Laufzeitumgebung für Entwickler, die Sprach-, Vision- und Embedding-Modelle auf eigener Hardware oder über eine kompatible API betreiben.

- Modell-Runner: lädt Modelle herunter und stellt eine interaktive CLI, eine HTTP-API sowie Python- und JavaScript-Bibliotheken bereit.
- Bildverarbeitung: verarbeitet Bilder zusammen mit Textprompts.

Geschwindigkeit, Kontextgröße und Parallelität hängen vom verfügbaren RAM und VRAM ab.

Eine praktische Alternative zur Cloud-Inferenz für lokale Entwicklung und kontrollierte Datenhaltung.

## Entwicklungslinie {#development-line}

- **2025-05-19 — Ollama veröffentlichte ein Update zu multimodalen Modellen.** Am 2025-05-19 verlinkte Ollama auf seine offizielle Blogseite zu multimodalen Modellen und auf die Download-Seite, ohne Details zu bestimmten Modellen oder Hardwareanforderungen zu nennen.
- **2026-01-22 — Ollama teilte ein Software-Release-Update.** Am 2026-01-22 verwies Ollama Nutzer auf die GitHub-Releases-Seite, ohne Version oder Änderungsliste zu nennen.

## Was sich geändert hat {#what-changed}

- 2025-05-19 — Ollama verlagerte Vision-Modelle in eine neue multimodale Engine und ergänzte die Unterstützung für Llama 4, Gemma 3, Qwen 2.5 VL und Mistral Small 3.1.
- 2026-01-22 — Ein Link zu GitHub Releases bestätigt den Release-Kanal, doch die URL enthält kein Versions-Tag, sodass sich der Release-Inhalt nicht verlässlich rekonstruieren lässt.

## Verwendung {#how-to-use-this}

Stand 2025-05-19: Bei der Auswahl lokaler Modelle den offiziellen multimodalen Workflow prüfen. Stand 2026-01-22: Vor einem Upgrade die Release Notes des Projekts auf GitHub prüfen.

1. Ollama unter macOS, Windows oder Linux installieren.
  — <https://docs.ollama.com/quickstart>
2. Ein Modell im Terminal ausführen, etwa `ollama run gemma4`, um die erste Sitzung zu testen.
  — <https://docs.ollama.com/quickstart>
3. Anwendungen senden Anfragen an die lokale API unter `http://localhost:11434/api` oder nutzen die offiziellen Python- und JavaScript-Bibliotheken.
  — <https://docs.ollama.com/api/introduction>
4. Für Vision-Aufgaben ein Bild zusammen mit Text in der CLI übergeben oder im Feld `images` der API-Anfrage.
  — <https://docs.ollama.com/capabilities/vision>

## Best Practices {#best-practices}

- Modellplatzierung mit `ollama ps` prüfen, um festzustellen, ob das Modell auf GPU, CPU oder im Mischbetrieb läuft.
  — <https://docs.ollama.com/faq>
- `OLLAMA_CONTEXT_LENGTH` und Parallelität an den verfügbaren Speicher anpassen: Der Verbrauch wächst mit parallelen Anfragen multipliziert mit der Kontextgröße.
  — <https://docs.ollama.com/faq>
- Den Dienst auf dem Standard-Loopback-Interface belassen; `OLLAMA_HOST` nur bewusst ändern und beim Veröffentlichen einen Reverse-Proxy verwenden.
  — <https://docs.ollama.com/faq>
- Cloud-Funktionen mit `OLLAMA_NO_CLOUD=1` oder `disable_ollama_cloud` deaktivieren, für ein vollständig lokales Setup.
  — <https://docs.ollama.com/faq>

## Überholt durch dies {#superseded-by-this}

- 2025-05-15 — Die ältere Integration, die auf gemeinsamem multimodalem Code auf Basis von llama.cpp aufbaute, wurde durch isolierte Modellimplementierungen in der neuen Engine ersetzt.
- 2026-01-20 — Bildgenerierung, die auf macOS beschränkt war, wurde als experimentell markiert; Windows und Linux wurden noch nicht unterstützt.

## Noch unbekannt {#still-unknown}

- Der GitHub-Releases-Link im Ereignis vom 2026-01-22 verweist auf einen veränderlichen Release-Feed ohne Tag, daher können wir weder eine bestimmte Version noch ein Changelog diesem Datum zuordnen.
- Die aktuelle Dokumentation enthält Cloud-Modelle, doch die beiden datierten Links zeigen nicht, ob Cloud-Ausführung Teil der ursprünglichen Ankündigung war.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://ollama.com/blog/multimodal-models | Ollamas neue Engine für multimodale Modelle | 2026-09-05 |
| https://ollama.com/download | Ollama herunterladen | 2026-09-05 |
| https://github.com/ollama/ollama/releases | Releases · ollama/ollama | 2026-09-05 |
| https://github.com/ollama/ollama/releases/tag/v0.14.3 | Release v0.14.3 · ollama/ollama | 2026-09-05 |
| https://ollama.com/blog/image-generation | Bildgenerierung (experimentell) | 2026-09-05 |
| https://docs.ollama.com/quickstart | Schnellstart | 2026-09-05 |
| https://docs.ollama.com/api/introduction | Einführung - Ollama API | 2026-09-05 |
| https://docs.ollama.com/capabilities/vision | Vision | 2026-09-05 |
| https://docs.ollama.com/faq | FAQ | 2026-09-05 |

## Agenten-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:ollama`, Thread `product-development`, 2 datierte Ereignisse 2025-05-19 → 2026-01-22.
- **Praxishinweis:** Stand 2025-05-19 Ollamas offiziellen multimodalen Workflow bei der Auswahl lokaler Modelle bewerten; Stand 2026-01-22 die Release Notes des Projekts auf GitHub vor einem Upgrade prüfen.
- **Konfidenz:** mittel. Datierte Überholungen sind maßgeblich dafür, was veraltet ist.
