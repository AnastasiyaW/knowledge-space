---
title: "Reve"
category: projects
date: 2026-02-25
tags: [project, reve, reve-product-development]
aliases: ["Reve"]
level: 3
source_sha256: 0b4d119fe5a42e557c2caa9d302156ff13d18f6bc1b33016397e2e80a2ecdb3e
translation: machine
translated_at: '2026-10-24'
---
# Reve {#reve}

**Entwicklungslinie:** `project:reve` · Thread `reve-product-development`  
**Letztes Ereignis:** 2026-02-25 · 2 datierte seit 2025-09-16 · **Recherchiert:** 2026-09-04 · Konfidenz: hoch

## Was es ist {#what-it-is}

Reve ist eine direkte Alternative zu Midjourney und Adobe Firefly für die Bildgenerierung und Bildbearbeitung im Browser.

- Konversationelle Erstellung, um Bilder im Chat zu generieren.
- Referenzsammlungen, um Stil und Figurenkonsistenz über alle Arbeiten hinweg zu steuern.
- Objektbearbeitung, um bestimmte Elemente zu verändern.
- Ebenen und Effekte, um die visuelle Komposition anzupassen.
- Reframe, um den Kamerausschnitt anzupassen.
- Videogenerierung über Veo aus Textprompts oder Einzelbildern.

Die native 4K-Ausgabe hat 16 Megapixel; Video ist weltweit für Pro-Abonnenten verfügbar. Es eignet sich für interaktive visuelle Arbeit in der Webanwendung, aber nicht für neue API-Integrationen.

## Entwicklungslinie {#development-line}

- **2025-09-16 — Produktupdate zu Reve dokumentiert.** Am 2025-09-16 verlinkte die Dokumentation einen eigenen Blogeintrag zu Reve zusammen mit der Anwendung. Wir betrachten dies als wesentliches Produktentwicklungsereignis, da die datierte kanonische Blog-URL ein eigenständiges Produktupdate kennzeichnet. Die bereitgestellten Links belegen keine Funktionsdetails des Updates.
- **2026-02-25 — Veröffentlichung von Reve 1.5 dokumentiert.** Am 2026-02-25 verlinkte die Dokumentation einen eigenen kanonischen Reve-Blogeintrag zu Version 1.5 zusammen mit der Anwendung. Wir betrachten dies als wesentliches versioniertes Produktentwicklungsereignis. Die bereitgestellten Links belegen keine Funktionsdetails oder betrieblichen Änderungen der Veröffentlichung.

## Was sich geändert hat {#what-changed}

- 2025-09-16 — Reve Image kombinierte Generierung und Remixing, einen Drag-and-Drop-Editor in der Beta, einen kreativen Assistenten und eine Beta-API; die primäre Quelle der Veröffentlichung ist auf 2025-09-15 datiert.
- 2026-02-25 — Frühes Reve v1.5 führte ein neues Text-zu-Bild-Modell mit nativem 4K ein; Bearbeitung und Referenzen wurden als kommende Funktionen angekündigt, während die Quelle der Veröffentlichung auf 2026-02-23 datiert ist.
- 2026-06-04 — Reve 2.0 ersetzte alle früheren Modelle: Eine Layoutrepräsentation machte Objekte und Text für die Bearbeitung adressierbar; die Veröffentlichung vom 2026-06-03 behauptete einen Zugewinn von +125 Elo gegenüber v1.5.
- 2026-07-11 — Reve 2.1 verbesserte Layoutplanung, lokalisierte Bearbeitung, komplexe Szenen und fremdsprachigen Schrifttext in nativem 4K; die Veröffentlichung vom 2026-07-09 nennt eine Ausgabe mit 16 Megapixeln.
- 2026-07-15 — Die Reve 2.1 API ging mit Standard-Endpunkten für Create und Edit sowie experimenteller Full Layout Control live; Reframe erhielt Reshoot und Relayout mit Skalierung bis 10×; die API wurde später, am 2026-08-14, geschlossen.

## So wird es verwendet {#how-to-use-this}

Stand 2026-02-25 sollten Annahmen zu Reve-Workflows anhand der aktuellen Versionsdokumentation überprüft werden, bevor man sich darauf verlässt. Dieses Update dokumentiert eine versionierte Veröffentlichung, keine betrieblichen Details.

1. Reve öffnen und den Arbeitsbereich für Erstellung, Bilder und Alben betreten.
  — <https://help.reve.com/hc/en-us/articles/46800570058772-Finding-your-way-around>
2. Die Aufgabe im Chat in einfacher Sprache beschreiben und den Prompt absenden.
  — <https://help.reve.com/hc/en-us/articles/46776083658132-Creating-images-in-chat>
3. Ein gutes Ergebnis auswählen, wieder in den Chat übernehmen und Beleuchtung, Komposition oder Inhalt verfeinern, während das Original erhalten bleibt.
  — <https://help.reve.com/hc/en-us/articles/46776083658132-Creating-images-in-chat>
4. Bilder und gespeicherte Referenzsammlungen für einen konsistenten Stil hinzufügen; für gezielte Änderungen den Editor und die Objektoperationen verwenden.
  — <https://app.reve.com/>
5. Für Video im Chat das Videowerkzeug auswählen und anschließend einen Textprompt oder Start- und Endbilder bereitstellen.
  — <https://help.reve.com/hc/en-us/articles/46799418938900-Video-creation>

## Bewährte Vorgehensweisen {#best-practices}

- In einem einzigen Chat iterieren: Eine ausgewählte Generierung verfeinern, statt jedes Mal von vorne zu beginnen, damit das Ausgangsbild erhalten bleibt.
  — <https://help.reve.com/hc/en-us/articles/46776083658132-Creating-images-in-chat>
- Referenzen projektübergreifend speichern, um Stil, Figur oder Stimmung beizubehalten.
  — <https://help.reve.com/hc/en-us/articles/46776083658132-Creating-images-in-chat>
- Nur dauerhafte Anforderungen wie eine Farbpalette in die Custom instructions aufnehmen; Anforderungen für eine einzelne Generierung im Prompt belassen.
  — <https://help.reve.com/hc/en-us/articles/46798449634452-Custom-instructions>
- Keine neuen Integrationen auf der Reve API aufbauen: Der Dienst bestätigt, dass die API geschlossen ist.
  — <https://help.reve.com/hc/en-us/articles/46837930295316-Reve-API>

## Abgelöst durch {#superseded-by-this}

- 2026-06-03 — Reve 2.0 ersetzte jedes vorherige Modell.
- 2026-08-14 — Die Reve 2.1 API ist geschlossen und nicht verfügbar, daher können wir keine neuen Integrationen darauf aufbauen.

## Noch unbekannt {#still-unknown}

- Die Veröffentlichungsdaten der primären Quellen liegen ein bis zwei Tage vor den dokumentierten Ereignisdaten; ihre verifizierten Details sind in der obigen Chronologie festgehalten.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://blog.reve.com/posts/the-new-reve/ | Introducing the New Reve | 2026-09-05 |
| https://blog.reve.com/posts/reve-1.5-is-here/ | Reve v1.5 Is Here | 2026-09-05 |
| https://blog.reve.com/posts/announcing-reve-2.0/ | Introducing Reve 2.0 | 2026-09-05 |
| https://blog.reve.com/posts/launching-reve-2.1/ | Launching Reve 2.1 | 2026-09-05 |
| https://blog.reve.com/posts/the-reve-api/ | The Reve API | 2026-09-05 |
| https://blog.reve.com/posts/introducing-reframe/ | Introducing Reframe | 2026-09-05 |
| https://app.reve.com/ | Reve Image | 2026-09-05 |
| https://help.reve.com/hc/en-us/articles/46800570058772-Finding-your-way-around | Finding your way around | 2026-09-05 |
| https://help.reve.com/hc/en-us/articles/46776083658132-Creating-images-in-chat | Creating images in chat | 2026-09-05 |
| https://help.reve.com/hc/en-us/articles/46798449634452-Custom-instructions | Custom instructions | 2026-09-05 |
| https://help.reve.com/hc/en-us/articles/46799418938900-Video-creation | Video creation | 2026-09-05 |
| https://help.reve.com/hc/en-us/articles/46837930295316-Reve-API | Reve API | 2026-09-05 |

## Agenten-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:reve`, Thread `reve-product-development`, 2 datierte Ereignisse 2025-09-16 → 2026-02-25.
- **Praktischer Hinweis:** Stand 2026-02-25 sollten Annahmen zu Reve-Workflows anhand der aktuellen Versionsdokumentation überprüft werden, bevor man sich darauf verlässt. Dieses Update dokumentiert eine versionierte Veröffentlichung, keine betrieblichen Details.
- **Konfidenz:** hoch. Die datierten Ablösungen oben sind maßgeblich dafür, was veraltet ist.
