---
title: "Hedra — Hedra-Produktentwicklung"
category: organizations
tags: [hedra, hedra-product-development, hedra_release, organization, product_releases]
aliases: ["Hedra"]
level: 2
source_sha256: 344314acd4111229551acdc1aa2a8ba9594250ca30f2a41eddc33d4e5327ef2c
translation: machine
translated_at: '2026-10-24'
---
# Hedra — Hedra-Produktentwicklung {#hedra-hedra-product-development}

**Entwicklungslinie:** `organization:hedra` · Thread `hedra-product-development`  
**Ereignisse:** 3 datierte, 2025-04-02 → 2026-02-20 · **Recherchiert:** 2026-09-03 · Konfidenz: mittel

## Was es ist {#what-it-is}

Hedra — ein einheitlicher Workflow für Personen, die sonst einen Dienst für sprechende Avatare, einen Videogenerator, ein Sprachwerkzeug und eine Modell-API kombinieren müssten. — Agent und Studio für Bild, Video, Sprache, Bearbeitung, Referenzen und wiederverwendbare Anweisungen. — Eigene Charaktermodelle: Character 3, Avatar und Omnia; die API stellt außerdem Bild-, Video- und Audiomodelle bereit. Einschränkung: Character 3 akzeptiert Bild, Text und Audio für Videos von bis zu 10 Minuten; Omnia ist für kurze Clips von etwa acht Sekunden in 1080p vorgesehen. Fazit: Einsetzen, wenn die Darstellung von Charakteren und ein gemeinsamer Workflow für Erstellung und API wichtig sind; das Modell pro Auftrag auswählen und prüfen, statt alle Videomodi als austauschbar zu behandeln.

## Entwicklungslinie {#development-line}

- **2025-04-02 — Die öffentliche Video-Anwendungsroute von Hedra wurde zitiert.** Am 2025-04-02 zitierte ein datierter Hedra-Verweis die öffentliche Route `/app/video`. Dies verzeichnet einen öffentlichen Einstiegspunkt für Videoprodukte in der Entwicklungslinie; der Link allein belegt jedoch weder Einführungsdatum, Funktionen noch Zugangsbedingungen.
- **2025-07-24 — Die öffentliche Avatar-Anwendungsroute von Hedra wurde zitiert.** Am 2025-07-24 zitierte ein datierter Hedra-Verweis die öffentliche Route `/app/avatar`. Dies verzeichnet einen Einstiegspunkt für ein Avatar-Produkt in der Entwicklungslinie, ohne eine bestimmte Veröffentlichung, ein Modell, einen Workflow oder eine Änderung der Verfügbarkeit zu behaupten.
- **2026-02-20 — Hedra verknüpfte Entwickler-Quickstart-Dokumentation mit Anwendungseinstiegspunkten.** Am 2026-02-20 enthielt ein datierter Hedra-Verweis seine Startseiten-Route der Anwendung und die Entwickler-Quickstart-Dokumentation. Dies verzeichnet eine öffentliche Entwicklerdokumentation neben den Produkteinstiegspunkten, belegt aber weder Inhalte, Veröffentlichungsdatum noch Verfügbarkeit einer API oder Funktion.

## Was sich geändert hat {#what-changed}

2024-08-17 — Die Startseite von Hedra wurde erfasst, doch mit dem Ereignis ist kein Veröffentlichungstext erhalten; eine konkrete Produktänderung lässt sich nicht sicher rekonstruieren. 2025-03-07 — Character 3 ersetzte im März 2025 Character 2. Es änderte den Kern der Charakter-Videoerzeugung von Hedra so, dass Bild, Text und Audio gemeinsam für Lippensynchronisation und Charakteranimation genutzt werden. 2025-04-02 — Die erfasste Route `/app/video` ist jetzt ein Video-Arbeitsbereich mit manuellen Werkzeugen. Der verfügbare Nachweis belegt über diesen Einstiegspunkt zur Videoerstellung hinaus keine eigenständige Veröffentlichung. 2025-07-24 — Die erfasste Route `/app/avatar` leitet nun auf `/app/home` weiter, wo ein Agent-Arbeitsbereich beginnt. Dies ist ein Beleg für einen geänderten Einstiegsweg, nicht dafür, dass das aktuelle Hedra-Avatar-Modell im Juli 2025 eingeführt wurde. 2026-02-20 — Ein Entwickler-Quickstart wurde erfasst. Seine aktuelle Version setzt vor der Generierung ein kostenpflichtiges Konto, einen API-Schlüssel, Credits und eine Anfrage der Modellliste voraus; dies ist aktuelle Dokumentation, kein Beleg für den genauen Stand im Februar 2026. 2026-02-05 — Hedra veröffentlichte Omnia, das audiogesteuerten Charaktervideos Szenenbewegung, dynamische Umgebungen und gerichtete Kamerasteuerung hinzufügt. 2026-09-04 (heute gefunden) — Hedra ist nun um einen Agent-/Studio-Workflow und eine Entwickler-API herum organisiert, nicht mehr nur als Spielwiese für Charaktervideos.

## So wird es genutzt {#how-to-use-this}

Stand 2026-02-20 sollten Praktiker, die Hedra evaluieren, die öffentlichen Einstiegspunkte der Anwendung und den Entwickler-Quickstart konsultieren, bevor sie annehmen, welche Video-, Avatar- oder Entwickler-Workflows verfügbar sind.

1. Für Studio-Arbeit einen Space anlegen, Ziel, Zielgruppe, Ausgabeformat, Randbedingungen und Referenzmaterial angeben und danach Iterationen auf der Arbeitsfläche prüfen und steuern.
  — <https://www.hedra.com/docs/pages/app/getting-started/overview>
2. Für ein sprechendes Charaktervideo ein Porträt und saubere Audioaufnahmen vorbereiten; einen Avatar-Workflow verwenden, bei dem das Audio Lippensynchronisation und Bewegung steuert.
  — <https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video>
3. Für Omnia Bild und Audio bereitstellen und anschließend Motivbewegung, Kamera und Hintergrund im Prompt explizit vorgeben.
  — <https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model>
4. Für API-Arbeit ein kostenpflichtiges Konto verwenden, einen API-Schlüssel mit ausreichend Credits erstellen und den aktuellen Modellkatalog abrufen, bevor ein Modell ausgewählt wird.
  — <https://www.hedra.com/docs/pages/developer/getting_started/quickstart>
5. Erforderliche Assets hochladen, die Generierung absenden und deren Status abfragen, bis sie abgeschlossen ist und das Ausgabe-Asset zurückgibt.
  — <https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video>

## Bewährte Praktiken {#best-practices}

- Ein klares, gut ausgeleuchtetes Nahporträt und saubere Sprachaufnahmen verwenden; Vortrag und zurückhaltende Bewegung beschreiben, wenn die gewünschte Darstellung spezifisch ist.
  — <https://www.hedra.com/models/video/hedra/character-3>
- Für Omnia ein einziges Motiv, eine explizite Kameraführung, 16:9, klar getaktetes Audio verwenden und längere Arbeiten aus kurzen Clips von etwa acht Sekunden in 1080p zusammensetzen.
  — <https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model>
- Den Modellkatalog vor der Generierung abrufen und Slug, Eingabeanforderungen, Dauer, Auflösung und Preise prüfen; den stabilen Slug einer umgebungsspezifischen Modell-ID vorziehen.
  — <https://www.hedra.com/docs/api-reference/public/list-models>
- Die Generierung als asynchron behandeln: Status abfragen und das zurückgegebene Asset erst nach Abschluss verwenden.
  — <https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video>

## Hierdurch ersetzt {#superseded-by-this}

- März 2025 — Character 2 wurde durch Character 3 als Kernmodell für Charakter-Videos von Hedra ersetzt.
- 2025-07-24 — `/app/avatar` nicht als stabilen aktuellen Einstiegspfad verwenden: Bei der Beobachtung am 2026-09-04 leitet er auf `/app/home` weiter.
- Februar 2026 — Eine Empfehlung, die Hedra nur als Werkzeug für sprechende Avatare mit feststehender Kamera behandelt, ist unvollständig: Omnia ergänzt gerichtete Kamera- und Umgebungsbewegung, mit einer Begrenzung auf kurze Clips.
- 2026-09-04 — Eine Empfehlung, die Hedra nur als Web-Spielwiese für Videos behandelt, ist überholt: Die aktuelle Dokumentation stellt einen Agent-Arbeitsbereich, manuelle Medienwerkzeuge und eine Entwickler-API bereit.

## Weiterhin unbekannt {#still-unknown}

- Das Ereignis vom 2024-08-17 enthält nur eine Startseiten-URL; die konkrete Veröffentlichungsbehauptung ist nicht verfügbar.
- Das Ereignis vom 2025-03-07 hat keine extrahierte URL; die Zuordnung zu Character 3 stützt sich deshalb auf das Veröffentlichungsdatum März 2025 der offiziellen Modellseite und nicht auf erhaltenen Ereignistext.
- Die Routenverweise vom 2025-04-02 und 2025-07-24 enthalten nicht genug Text, um eine eigenständige Veröffentlichung oder Funktionseinführung zu identifizieren.
- Die verlinkte X-Status-URL konnte nicht abgerufen werden, und `http://hedra.com/app/home` lieferte keine lesbare Seite; beides wird nicht als sachlicher Beleg verwendet.

## Quellen {#sources}

| Quelle | Titel | Abgerufen |
|---|---|---|
| https://www.hedra.com/ | Hedra — Visual Inference Models and Infrastructure | 2026-09-04 |
| https://www.hedra.com/app/video | Hedra Video Playground | 2026-09-04 |
| https://www.hedra.com/app/avatar | Hedra Agent — General Visual Intelligence | 2026-09-04 |
| https://www.hedra.com/docs/pages/developer/getting_started/quickstart | Hedra API Quickstart Guide | 2026-09-04 |
| https://www.hedra.com/docs/pages/app/getting-started/overview | Meet Hedra Agent | 2026-09-04 |
| https://www.hedra.com/models/video/hedra/character-3 | Hedra Character 3: Omnimodal Character Video | 2026-09-04 |
| https://www.hedra.com/blog/hedra-omnia-frontier-ai-video-model | Hedra Omnia: Unified AI Video for Character-Driven Content | 2026-09-04 |
| https://www.hedra.com/docs/pages/developer/guides/generate-avatar-video | Generate an Avatar Video | 2026-09-04 |
| https://www.hedra.com/docs/api-reference/public/list-models | List Available AI Models | 2026-09-04 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `organization:hedra`, Thread `hedra-product-development`, 3 datierte Ereignisse 2025-04-02 → 2026-02-20.
- **Praktischer Hinweis:** Stand 2026-02-20 sollten Praktiker, die Hedra evaluieren, die öffentlichen Einstiegspunkte der Anwendung und den Entwickler-Quickstart konsultieren, bevor sie annehmen, welche Video-, Avatar- oder Entwickler-Workflows verfügbar sind.
- **Konfidenz:** mittel. Die datierten Ersetzungen oben sind maßgeblich für die Frage, was veraltet ist.
