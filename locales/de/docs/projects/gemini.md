---
title: "Gemini"
category: projects
date: 2026-08-14
tags: [gemini, gemini-development, project]
aliases: ["Gemini", "Gemini 1.5", "Gemini 3.7 Flash"]
level: 3
source_sha256: e5d207f43ce4282113d7bb6283d6dbfba5cab00c756546d63f12c491955a40bb
translation: machine
translated_at: '2026-10-24'
---
# Gemini {#gemini}

**Entwicklungslinie:** `project:gemini` · Thread `gemini-development`  
**Letztes Ereignis:** 2026-08-14 · 6 datierte Einträge seit 2024-02-16 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Gemini ist Googles Modellfamilie für Chat, Text, Code, Bilder, Audio, Video und API-Integrationen.

- Gemini-App: manueller Chat und alltägliche Aufgaben.
- AI Studio: Prompt-Prototyping und Codegenerierung.
- Gemini API: Backend-Integration in Anwendungen.
- Live API: Streaming-Schnittstellen für Sprache und Bildverarbeitung.

Der Zugang zur Verbraucher-App, API-Schlüssel, Preisstufen, Live API und macOS-Funktionen sind voneinander unabhängig, und die Live API befindet sich weiterhin in der Preview-Phase. Wir prototypen in AI Studio, fixieren in der Produktion eine stabile Modell-ID und prüfen Preisstufe und Lebenszyklus.

## Entwicklungslinie {#development-line}

- **2024-02-16 — Google veröffentlicht eine Ankündigung zur Modellentwicklung von Gemini.** Am 2024-02-16 verlinkte Google einen offiziellen Beitrag des Technology-&-AI-Blogs über Gemini als Modell der nächsten Generation. Dies ist eine Ankündigung der Modellentwicklung von Gemini durch den Anbieter selbst. Der angegebene Link allein belegt nicht den genauen Funktions- oder Verfügbarkeitsumfang.
- **2024-12-12 — Gemini-bezogene Live-Oberfläche erscheint in Google AI Studio.** Am 2024-12-12 wurde eine Live-Seite von Google AI Studio für die Gemini-Linie verlinkt. Dies deutet auf eine Gemini-bezogene Oberfläche für Live-Interaktionen in der Entwicklungsumgebung hin. Die angegebene URL belegt nicht das genaue Modell, die API oder den Launch-Status.
- **2026-03-03 — Gemini 3.1 Flash-Lite Preview erscheint zusammen mit Preisdokumentation.** Am 2026-03-03 verlinkte Google AI Studio Gemini 3.1 Flash-Lite Preview zusammen mit der offiziellen Preisdokumentation für diese benannte Preview-Version. Dies ist ein wesentlicher Schritt bei Verfügbarkeit und Preisgestaltung für die Modellreihe für Entwickler. Die angegebenen Links belegen keine Kontingente, Regionen oder den Status einer finalen Veröffentlichung.
- **2026-04-10 — Die Gemini-App kündigt Fähigkeiten für 3D-Modelle und Diagramme an.** Am 2026-04-10 verlinkte Google eine offizielle Ankündigung der Gemini-App zu 3D-Modellen und Diagrammen zusammen mit der Gemini-App. Dies dokumentiert einen Schritt bei den Produktfähigkeiten der Gemini-Anwendung. Die URLs allein belegen nicht, wie die Fähigkeit umgesetzt wurde oder welche Konten sie erhalten haben.
- **2026-04-16 — Gemini erhält eine macOS-spezifische Produktoberfläche.** Am 2026-04-16 verlinkte Google eine Gemini-Seite speziell für Mac. Dies dokumentiert eine Erweiterung der Desktop-Plattformoberfläche des Gemini-Produkts. Die angegebene URL belegt nicht die genau unterstützten macOS-Versionen, den Ausrollumfang oder den Funktionsumfang.
- **2026-08-14 — Google führt Gemini 3.7 Flash für AI Studio ein.** Am 2026-08-14 verlinkte Google eine offizielle Ankündigung zur Einführung von Gemini 3.7 Flash sowie eine AI-Studio-Prompt-URL, die dieses Modell auswählt. Dies ist ein wesentlicher Schritt bei der Modellveröffentlichung und der Verfügbarkeit für Entwickler. Die angegebenen Links belegen weder den endgültigen Status des Modells noch seine Limits oder regionale Verfügbarkeit.

## Was sich geändert hat {#what-changed}

- 2024-02-16: Gemini 1.5 Pro führte MoE-Architektur, einen standardmäßigen 128K-Kontext und eine eingeschränkte Preview mit bis zu 1M Tokens über AI Studio und Vertex AI ein.
- 2024-12-12: Gemini 2.0 führte die Multimodal Live API für Audio- und Video-Streaming in Echtzeit ein; die historische AI-Studio-Live-URL erfordert nun eine Anmeldung, während die aktuelle Live API über einen zustandsbehafteten WebSocket läuft und sich weiterhin in der Preview-Phase befindet.
- 2026-03-03: Gemini 3.1 Flash-Lite wurde als Preview für hochfrequente Aufgaben, Übersetzung, Moderation und Datenverarbeitung veröffentlicht; Google hat den Preview-Endpunkt später abgeschaltet.
- 2026-04-10: Die Gemini-App ergänzte die Erzeugung interaktiver Simulationen und Modelle direkt im Chat, mit konfigurierbaren Visualisierungsparametern.
- 2026-04-16: Gemini für macOS ergänzte den Desktop-Zugriff mit Hotkeys und Bildschirmkontext; dafür ist ein Mac mit Apple Silicon unter macOS 15+ in einem unterstützten Land erforderlich.
- 2026-08-14: Gemini 3.7 Flash, von Google am 13. August angekündigt, wurde das Flash-Modell für Coding- und Agent-Workflows.
- Gefunden 2026-09-04: Gemini 3.8 Flash wurde am 2. September veröffentlicht und ist das aktuelle stabile Flash-Modell; Gemini 3.7 Flash bleibt vollständig unterstützt, wird in der Modellliste aber nun als Vorgängergeneration gekennzeichnet.

## So verwenden Sie dies {#how-to-use-this}

Verfolgen Sie Gemini nach Produktoberfläche, Stand 2026-08-14. Nutzen Sie die Live-Oberfläche von AI Studio für Live-Workflows (2024-12-12). Bepreisen und evaluieren Sie Gemini 3.1 Flash-Lite Preview vor einer Einführung (2026-03-03). Wählen Sie Gemini 3.7 Flash in AI Studio aus, wo verfügbar (2026-08-14), und behandeln Sie Gemini-App und Mac-Funktionen als getrennte Produktoberflächen.

1. Öffnen Sie die Gemini-App, melden Sie sich mit einem Google-Konto an und starten Sie einen Chat mit Text oder angehängten Dateien für einmalige Aufgaben.
  — <https://gemini.google.com/app>
2. Installieren Sie Gemini für macOS nur auf dem Mac, wenn das Gerät Apple Silicon hat, macOS Sequoia 15.0+ ausführt und das Land die Gemini-App unterstützt.
  — <https://gemini.google/mac/>
3. Öffnen Sie Google AI Studio, um Prototypen zu erstellen: Wählen Sie eine Prompt-Oberfläche, testen Sie das Modell, passen Sie Parameter und Sicherheitseinstellungen an und fügen Sie Tools hinzu.
  — <https://ai.google.dev/gemini-api/docs/ai-studio-quickstart>
4. Verwenden Sie nach dem Prototyping „Get code“, erstellen oder importieren Sie ein Cloud-Projekt und generieren Sie einen API-Auth-Schlüssel für die Backend-Integration.
  — <https://ai.google.dev/gemini-api/docs/api-key>
5. Wählen Sie vor dem Deployment einen stabilen Endpunkt aus der Modellliste; evaluieren Sie gemini-3.8-flash für neue Coding- und Agent-Aufgaben, statt standardmäßig den älteren 3.7-Endpunkt zu verwenden.
  — <https://ai.google.dev/gemini-api/docs/models>
6. Nutzen Sie den separaten Live-API-Pfad über WebSocket für Sprach- oder Bilddialoge in Echtzeit; verwenden Sie ephemere Tokens für Client-Server-Setups.
  — <https://ai.google.dev/gemini-api/docs/live-api>

## Bewährte Verfahren {#best-practices}

- Fixieren Sie Produktions-Workloads auf eine bestimmte stabile Modell-ID statt auf `latest`- oder experimentelle Aliase: `latest` ändert sich automatisch, und experimentelle Endpunkte haben engere Limits ohne vertragliche Stabilität.
  — <https://ai.google.dev/gemini-api/docs/models>
- Formulieren Sie kurze, direkte Anweisungen für Gemini 3; übernehmen Sie keine ausführlichen Prompt-Engineering-Techniken aus älteren Modellen.
  — <https://ai.google.dev/gemini-api/docs/gemini-3>
- Aktivieren Sie Structured Output für komplexe JSON-Schemata, statt sich auf „antworte in JSON“ zu verlassen; ergänzen Sie konsistente Beispiele für ein wiederholbar einheitliches Format.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Platzieren Sie bei langen Kontext-Aufrufen die Frage nach dem Referenzmaterial, lassen Sie nicht benötigten Kontext weg und cachen Sie wiederverwendete Dateien oder Daten.
  — <https://ai.google.dev/gemini-api/docs/long-context>
- Halten Sie den API-Schlüssel aus Git und Client-Code heraus; leiten Sie Produktionsaufrufe aus Web- und Mobil-Apps über ein Backend und beschränken Sie den Schlüssel.
  — <https://ai.google.dev/gemini-api/docs/api-key>
- Prüfen Sie die Preistabelle, bevor Sie Kosten abschätzen: Kostenlose und kostenpflichtige Stufen unterscheiden sich bei Limits, Funktionen und Inhaltsverarbeitung, daher ist der Preis aus der Launch-Ankündigung keine gültige Schätzung.
  — <https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview>

## Hiermit überholt {#superseded-by-this}

- 2024-02-16 — Early Access für Gemini 1.5 Pro mit 128K-Basiskontext und eingeschränkter 1M-Preview ist historischer Hintergrund und keine aktuelle Empfehlung zur Modellauswahl.
- 2026-03-03 — Der Endpunkt `gemini-3.1-flash-lite-preview` wurde am 2026-05-25 abgeschaltet; sein direkter Nachfolger war `gemini-3.1-flash-lite`. Dieser Nachfolger führt nun ein Abschaltdatum von 2027-05-07, wobei `gemini-3.5-flash-lite` als nächster empfohlener Nachfolger gilt.
- Gefunden 2026-09-04 — Die Beschreibung von Gemini 3.7 Flash als neuestes Flash-Modell ist veraltet: `gemini-3.8-flash` wurde am 2026-09-02 veröffentlicht. `gemini-3.7-flash` bleibt vollständig unterstützt, ist nun aber die stabile Option der Vorgängergeneration.

## Noch unbekannt {#still-unknown}

- Gemini umfasst getrennte Produktoberflächen: Verbraucher-App, macOS-App, AI Studio, Gemini API und Live API. Der Zugang zu einer davon bestätigt keine Kontingente, Preisstufen oder Funktionen einer anderen.
- Die historische AI-Studio-Live-URL leitet auf eine Anmeldeaufforderung weiter. Ohne aktive Sitzung lassen sich die genaue Oberfläche bzw. die Einstellungen vom Dezember 2024 nicht überprüfen; eine offizielle Ankündigung vom 11. Dezember 2024 und die aktuelle Dokumentation bestätigen den Launch getrennt voneinander.
- Die Produktseite von Gemini für macOS listet Anforderungen und Limits, nennt aber kein Veröffentlichungsdatum; sie bestätigt das Datum 2026-04-16 nicht unabhängig.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/#sundar-note | Unser Modell der nächsten Generation: Gemini 1.5 | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/ | Google stellt Gemini 2.0 vor: Ein neues KI-Modell für das Zeitalter der Agenten | 2026-09-04 |
| https://aistudio.google.com/live | Anmelden – Google-Konten | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview | Цены на API Gemini Developer | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/ | Gemini 3.1 Flash-Lite: Entwickelt für Intelligenz im großen Maßstab | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/gemini-app/3d-models-charts/ | Die Gemini-App kann jetzt interaktive Simulationen und Modelle erzeugen. | 2026-09-04 |
| https://gemini.google.com/app | Google Gemini | 2026-09-04 |
| https://gemini.google/mac/ | Gemini für macOS – nativer KI-Assistent und Mac-Automatisierung | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/ | Einführung von Gemini 3.7 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models | Models | Gemini API | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/deprecations?hl=en | Gemini deprecations | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/latest-model | What's new in Gemini 3.8 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/ai-studio-quickstart | Google AI Studio quickstart | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/api-key | Using Gemini API keys | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt design strategies | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/long-context | Long context | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/gemini-3 | Gemini 3 developer guide | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/live-api | Gemini Live API overview | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:gemini`, Thread `gemini-development`, 6 datierte Ereignisse 2024-02-16 → 2026-08-14.
- **Praxishinweis:** Stand 2026-08-14 sollten Praktiker Gemini nach Produktoberfläche verfolgen: die Live-Oberfläche von AI Studio für Live-Workflows nutzen (2024-12-12), Gemini 3.1 Flash-Lite Preview vor einer Einführung evaluieren und bepreisen (2026-03-03) und Gemini 3.7 Flash in AI Studio auswählen, wo verfügbar (2026-08-14); Gemini-App und Mac-Funktionen sind dabei als getrennte Produktoberflächen zu behandeln.
- **Konfidenz:** hoch. Die datierten Überholungshinweise oben sind maßgeblich dafür, was veraltet ist.
