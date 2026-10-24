---
title: "Nano Banana Pro"
category: projects
date: 2025-11-26
tags: [nano-banana-pro, nano_banana, nano_banana_pro, project]
aliases: ["Nano Banana Pro"]
level: 3
source_sha256: 7c2d1d95e155f2e69f13faaa901f3475c03c87082f25f8a4613ab822538263ad
translation: machine
translated_at: '2026-10-24'
---
# Nano Banana Pro {#nano-banana-pro}

**Entwicklungslinie:** `project:nano-banana-pro` · Thread `nano-banana-pro`  
**Letztes Ereignis:** 2025-11-26 · 2 datierte Ereignisse seit 2025-11-20 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Nano Banana Pro ist Googles Gemini-3-Pro-Image-Modell für Kreative und Entwickler, die komplexe visuelle Assets erstellen.

- Erzeugt und bearbeitet Bilder aus Text- und Bildeingaben.
- Unterstützt Google-Search-Grounding, Textdarstellung, Lokalisierung, Komposition mit mehreren Referenzen und Ausgabe in bis zu 4K.
- Die stabile API-ID lautet `gemini-3-pro-image`; sie akzeptiert 65.536 Eingabe-Tokens und liefert bis zu 32.768 Ausgabe-Tokens. Je nach Verwendung sind bis zu sechs hochauflösende Objektreferenzen, fünf Charakterreferenzen oder insgesamt 14 Referenzen möglich.

## Entwicklungslinie {#development-line}

- **2025-11-20 — Google stellte Nano Banana Pro vor.** Am 2025-11-20 veröffentlichte Google einen offiziellen KI-Blogbeitrag zu Nano Banana Pro und verlinkte das Modell in Google AI Studio. Dies ist in dieser Entwicklungslinie der öffentliche Einführungspunkt für Nano Banana Pro.
- **2025-11-26 — Google veröffentlichte Prompting-Hinweise für Nano Banana Pro.** Der verlinkte Prompting-Leitfaden ist auf 2025-11-20 datiert und vermittelt die Nutzung, kündigt aber keine Überarbeitung an.

## Was sich geändert hat {#what-changed}

- 2025-11-20 — Nano Banana Pro wurde als Gemini 3 Pro Image eingeführt; der Preview-Endpunkt der Gemini API lautete `gemini-3-pro-image-preview`.
- 2025-11-26 — Es ist keine separate Modellveröffentlichung belegt: Der verlinkte Prompting-Leitfaden ist auf 2025-11-20 datiert und vermittelt die Nutzung, kündigt aber keine Überarbeitung an.
- 2025-12-01 — Search AI Mode erweiterte Nano Banana Pro für Google-AI-Pro- und Ultra-Abonnenten auf weitere englischsprachige Länder.
- 2025-12-17 — Search erweiterte den Zugang zu Nano Banana Pro auf weitere Personen in den Vereinigten Staaten.
- 2025-12-23 — Google nannte die Verfügbarkeit in Gemini, Search AI Mode, NotebookLM, Workspace, Flow, Mixboard, AI Studio, Vertex AI und weiteren Entwickler-Oberflächen.
- 2026-04-20 — Google-AI-Pro- und Ultra-Abonnements erhielten höhere AI-Studio-Limits und Zugang zu Nano Banana Pro.
- 2026-05-28 — `gemini-3-pro-image` wurde zur GA-API-ID; die Preview-ID wurde mit einem Abschaltdatum am 25. Juni 2026 als veraltet markiert.

## Verwendung {#how-to-use-this}

Ab 2025-11-20 konnte Nano Banana Pro über Google AI Studio genutzt werden; ab 2025-11-26 sollte bei der Arbeit damit den modellspezifischen Prompting-Hinweisen von Google gefolgt werden.

1. In Gemini Apps: Mit einem Google-AI-Plan ein Bild mit Nano Banana 2 oder Nano Banana 2 Lite erstellen und anschließend More → Redo with Pro für den detaillierten Durchlauf wählen; das tägliche Kontingent kann das erneute Generieren blockieren.
  — <https://support.google.com/gemini/answer/14286560?hl=en-Documentation>
2. In Search AI Mode: Pro auswählen, Image und anschließend Create Images wählen; das Bild beschreiben oder zum Bearbeiten ein Bild hochladen. Die Verfügbarkeit ist nur auf Englisch gegeben und hängt von Konto, Alter, Plan und Land ab.
  — <https://support.google.com/websearch/answer/16649374?co=GENIE.Platform%3DDesktop&hl=en-EN>
3. In der Gemini API: Das stabile Modell `gemini-3-pro-image` mit Text- und/oder Bildeingaben aufrufen und anschließend dessen Bild- und Textausgabe verarbeiten.
  — <https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image?authuser=00>
4. Bearbeiten: Ein Bild mit einer direkten Änderungsanweisung bereitstellen und für Folgebearbeitungen dieselbe Konversation fortsetzen.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>
5. Ausgabe: `response_format.type` auf `image` setzen und `aspect_ratio` sowie `image_size` anfordern, wenn Bildausschnitt oder Ausgabeauflösung relevant sind.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>

## Bewährte Praktiken {#best-practices}

- Modellauswahl: Nano Banana Pro für komplexe professionelle Assets und anspruchsvolle Anweisungen einsetzen; Nano Banana 2 verwenden, wenn das allgemeine Verhältnis von Kosten und Latenz wichtiger ist.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>
- Prompts: Motiv, Komposition, Handlung, Ort, Stil und eine direkte Bearbeitungsanweisung angeben.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Komposition: Seitenverhältnis, Kamera, Beleuchtung, Textplatzierung und sachliche Vorgaben explizit nennen.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Referenzen: Die Rolle jedes hochgeladenen Bildes benennen, etwa Pose, Stil oder Hintergrund.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Bearbeitungen: In einer mehrstufigen Konversation iterieren, statt jede Überarbeitung neu zu starten.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>
- Ergebnisse: Vor der Verwendung kleinen Text, Rechtschreibung, Fakten in Diagrammen, Übersetzungen, komplexe Überblendungen und die Konsistenz von Charakteren unabhängig prüfen.
  — <https://blog.google/products/gemini/prompting-tips-nano-banana-pro/>
- Eingaben: Nur Bilder hochladen, für die die erforderlichen Rechte vorliegen.
  — <https://ai.google.dev/gemini-api/docs/image-generation?authuser=00>

## Hiermit ersetzt {#superseded-by-this}

- 2026-05-28 — Für eine neue Nano-Banana-Pro-API-Integration `gemini-3-pro-image-preview` verwenden. Ersetzt durch den GA-Endpunkt `gemini-3-pro-image`; der Preview-Endpunkt sollte am 2026-06-25 abgeschaltet werden.

## Weiterhin unbekannt {#still-unknown}

- Der historische AI-Studio-Deep-Link `https://aistudio.google.com/prompts/new_chat?model=nano-banana-pro` erfordert eine Anmeldung; seine aktuelle Modellvorauswahl und sein Kontingent konnten daher nicht unabhängig über eine öffentliche Seite verifiziert werden.
- Der Zugang für Verbraucher variiert nach Konto, Google-AI-Plan, Sprache, Alter, Land und sich ändernden täglichen Kontingenten; daraus lässt sich nicht ableiten, ob ein bestimmtes Konto berechtigt ist.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://blog.google/technology/ai/nano-banana-pro/ | Introducing Nano Banana Pro | 2026-09-04 |
| https://blog.google/products/gemini/prompting-tips-nano-banana-pro/ | 7 tips to get the most out of Nano Banana Pro | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/changelog | Release notes | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image?authuser=00 | Gemini 3 Pro image | Gemini API | Google AI for Developers | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/image-generation?authuser=00 | Image generation | Gemini API | Google AI for Developers | 2026-09-04 |
| https://blog.google/products-and-platforms/products/search/gemini-3-ai-mode-more-countries/ | Gemini 3 and Nano Banana Pro in Search are coming to more countries around the world. | 2026-09-04 |
| https://blog.google/products-and-platforms/products/search/google-ai-mode-update-gemini-3-flash/ | Gemini 3 Flash is rolling out globally in Google Search | 2026-09-04 |
| https://blog.google/products-and-platforms/products/gemini/where-to-use-nano-banana-pro/ | Here’s where you can use Nano Banana Pro | 2026-09-04 |
| https://blog.google/innovation-and-ai/technology/developers-tools/google-one-ai-studio/ | Start vibe coding in AI Studio with your Google AI subscription. | 2026-09-04 |
| https://support.google.com/gemini/answer/14286560?hl=en-Documentation | Generate & edit images with Gemini Apps - Computer - Gemini Apps Help | 2026-09-04 |
| https://support.google.com/websearch/answer/16649374?co=GENIE.Platform%3DDesktop&hl=en-EN | Create and edit images in Google Search - Computer - Google Search Help | 2026-09-04 |

## Agent-Kurzbriefing {#agent-brief}

- **Gegenstand:** `project:nano-banana-pro`, Thread `nano-banana-pro`, 2 datierte Ereignisse vom 2025-11-20 bis 2025-11-26.
- **Praktischer Hinweis:** Ab 2025-11-20 konnten Anwender Nano Banana Pro über Google AI Studio nutzen; ab 2025-11-26 sollten sie bei der Arbeit damit den modellspezifischen Prompting-Hinweisen von Google folgen.
- **Konfidenz:** hoch. Für die Frage, was veraltet ist, gelten die datierten Ersetzungshinweise als maßgeblich.
