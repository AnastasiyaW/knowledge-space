---
title: "Krea AI — Videogenerierung"
category: organizations
tags: [krea-ai, krea_ai, organization, video-generation]
aliases: ["Krea AI"]
level: 2
source_sha256: af9fbb456f5c8ef5ca6d2bcb02392b62b2f5843fd3d2b81581a8a1f580c6d183
translation: machine
translated_at: '2026-10-24'
---
# Krea AI — Videogenerierung {#krea-ai-video-generation}

**Entwicklungslinie:** `organization:krea-ai` · Strang `video-generation`  
**Ereignisse:** 3 datiert, 2025-04-16 → 2025-08-29 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Krea AI ist ein browserbasiertes Toolkit für Designer und Videoteams, das Bilder und Videos generiert, bearbeitet, verbessert und animiert sowie wiederverwendbare Stile trainiert.

- **Image und Video:** Wähle für die jeweilige Aufgabe das eigene Modell Krea 2 oder ein Drittanbietermodell.
- **Realtime:** Nutze ein Canvas mit Live-Generierung aus Text, Zeichnung, Webcam oder Bildschirm.
- **Edit, Enhancer und Train:** Nimm lokale Bearbeitungen vor, skaliere Bilder hoch und trainiere ein LoRA für einen Stil, eine Figur oder ein Produkt.

Die Dokumentation für ein gewöhnliches Videorendering nennt 5–12 Sekunden, 1–10 Minuten und ab 1 000 Rechen-Credits.

Krea ist ein Arbeitsbereich, um Modelle zu vergleichen und Visuals schnell zu iterieren. Prüfe vor einer konkreten Aufgabe die Modellauswahl, die Credit-Limits und den Status von Stage.

## Entwicklungslinie {#development-line}

- **2025-04-16 — Krea AI veröffentlichte eine Videoerfahrung mit einer OL-Flux-Kennung.** Am 2025-04-16 verwies ein datierter Krea-AI-Link auf deren Videoerfahrung, wobei URL-Parameter auf eine OL-Flux-Variante hinwiesen. Dies ist ein wesentlicher Schritt in der Entwicklungslinie der Videogenerierung bei Krea AI. Die Links belegen weder die Details der Fähigkeiten, die Verfügbarkeit noch den Launch-Wortlaut.
- **2025-04-18 — Krea AI verlinkte seine Produktoberfläche Stage.** Am 2025-04-18 verwies ein datierter Krea-AI-Link auf den Produktpfad Stage des Unternehmens. Dies ist ein wesentlicher Schritt in der Linie der Videogenerierung, weil er eine eigenständige Produktoberfläche kenntlich macht. Die Links belegen weder den Funktionsumfang oder die Verfügbarkeit von Stage noch, ob dieses Datum den Launch markierte.
- **2025-08-29 — Krea AI veröffentlichte eine Ankündigung für Realtime Video.** Am 2025-08-29 veröffentlichte Krea AI eine Blogseite, deren URL auf eine Ankündigung für Realtime Video hinweist. Dies ist eine wesentliche Entwicklung in der Linie der Videogenerierung des Unternehmens. Die Links belegen weder dessen Betriebsmodell, Einführungsbedingungen noch Funktionsdetails.

## Was sich geändert hat {#what-changed}

Krea AI ging von getrennten Oberflächen Video und Stage zu einem Toolkit mit eigenem Modell und einem steuerbaren Echtzeit-Workflow über.

- **2025-04-16:** Video war dokumentiert, doch die genaue Veröffentlichung lässt sich über die alte URL mit dem Parameter `ol_flux` nicht mehr rekonstruieren, da sie inzwischen auf eine sich ändernde Oberfläche führt.
- **2025-04-18:** Stage bot einen experimentellen Workflow für 3D-Szenen: eine Szene aus Text erzeugen, Objekte hinzufügen und verschieben sowie glTF exportieren. Die Bestätigung der Details ist nachrangig, da die historische Spezifikation unter der ursprünglichen URL nicht verfügbar ist.
- **2025-08-29:** Realtime Video ergänzte eine Generierung, die schneller als die Wiedergabe ist, mit Canvas, Text, Webcam und Bildschirmaufnahme. Die erste Ankündigung ist auf 2025-08-27 datiert.
- **2025-10-20:** Krea veröffentlichte Realtime 14B, ein autoregressives Modell für langes Echtzeitvideo. Das Unternehmen gab 11 fps auf einer B200 und erste Frames in etwa einer Sekunde an.
- **2026-05-12 und 2026-05-21:** Krea 2 wurde ein eigenes Foundation-Bildmodell, gefolgt von LoRA-Training in der Beta für Max und Business.
- **2026-09-04:** Die aktuelle Dokumentation beschreibt Krea als Toolkit aus Image, Video, Realtime, Edit, Enhancer und Train statt als einen einzelnen Generator.

## Wie man das anwendet {#how-to-use-this}

Ab 2025-08-29 sollten Praktiker, die Krea AI bewerten, die Oberfläche Realtime Video in Workflow-Vergleiche einbeziehen und aktuelle Zugänglichkeit, Verhalten und Fähigkeiten unabhängig prüfen.

1. Öffne Krea und wähle für ein Standardrendering Image oder Video. Nutze Realtime, wenn die Komposition Live-Steuerung braucht.  
   — [Krea-Leitfaden](https://www.krea.ai/docs/user-guide/get-started/what-is-krea)
2. Wähle in Video ein Modell, lege Prompt, Seitenverhältnis, Dauer und Auflösung fest und füge bei Bedarf Start- und End-Frames hinzu.  
   — [Video-Modelle](https://www.krea.ai/docs/user-guide/features/video)
3. Gib in Realtime einen Prompt ein und zeichne, verschiebe Figuren, lade eine Referenz hoch oder stelle einen Webcam- oder Bildschirm-Feed bereit. Wähle Image oder Video als Ausgabe.  
   — [Realtime](https://www.krea.ai/docs/user-guide/features/realtime)
4. Für einen wiederholbaren Stil, eine Figur oder ein Produkt öffne Train. Lade mindestens drei Bilder hoch, wähle Krea 2 Medium oder Large, prüfe die Captions und binde das fertige LoRA in Image ein.  
   — [Krea 2 LoRA-Training](https://www.krea.ai/blog/krea-2-lora-training)
5. Um einen Bereich zu ändern, öffne Edit. Wähle ihn mit Rechteck, Pinsel oder automatischer Auswahl aus und beschreibe die Ersetzung. Setze den Bearbeitungsverlauf Schritt für Schritt fort.  
   — [Krea Edit](https://www.krea.ai/blog/krea-edit)

## Bewährte Vorgehensweisen {#best-practices}

- Vergleiche mehrere Modelle mit demselben Prompt. Wähle nach der benötigten Bewegung, Steuerung und Figurenerhaltung, nicht nach dem Modellnamen.  
  — [Video-Modelle](https://www.krea.ai/docs/user-guide/features/video)
- Beginne mit kostengünstigen Tests von 5–10 Sekunden; erhöhe Dauer und Auflösung erst, nachdem eine Richtung feststeht.  
  — [Video-Modelle](https://www.krea.ai/docs/user-guide/features/video)
- Beschreibe Aktion und Kamerabewegung explizit. Nutze Start- und End-Frames und setze komplexe Szenen zuerst aus einzelnen Frames zusammen.  
  — [Video-Modelle](https://www.krea.ai/docs/user-guide/features/video)
- Nutze Realtime für Komposition und schnelle Tests. Nutze gewöhnliches Image, wenn du ein bewusst prompt-basiertes Rendering ohne Zeichnen brauchst.  
  — [Realtime](https://www.krea.ai/docs/user-guide/features/realtime)
- Halte bei LoRA den ersten Datensatz eng, aber vielfältig in Blickwinkeln, Licht und Hintergrund. Prüfe Captions von Hand und erhöhe die Schrittzahl nicht ohne Grund.  
  — [Krea 2 LoRA-Training](https://www.krea.ai/blog/krea-2-lora-training)

## Durch dies ersetzt {#superseded-by-this}

- **2025-04-16** — Die Schlussfolgerung, aus dem alten Parameter `ol_flux` ein Videomodell zu empfehlen, ist veraltet. Wähle das Modell im aktuellen Auswahlmenü und prüfe es mit demselben Test.
- **2025-04-18** — Die Anweisung, Stage als dokumentierten eigenständigen Einstiegspunkt zu behandeln, ist veraltet. Ihre historische Spezifikation ist unter der ursprünglichen URL nicht mehr verfügbar, daher muss der alte Workflow neu geprüft werden.
- **2025-08-29** — Die Behandlung der Realtime-Video-Ankündigung als endgültiger Zustand der Funktion ist veraltet. Sie entwickelte sich am 2025-10-20 zu Realtime 14B und dem heutigen Canvas-basierten Realtime-Workflow.

## Weiterhin unbekannt {#still-unknown}

- Die genaue Produktveröffentlichung vom 2025-04-16 ist nicht bestätigt. Die Video-URL existiert noch, aber ihr historischer Inhalt und die Bedeutung des Parameters `ol_flux` sind nicht verfügbar.
- Stage ist im April 2025 als eigenes experimentelles 3D-Werkzeug belegt, doch ist unklar, ob es später umbenannt, verschoben oder eingestellt wurde. Die aktuelle Seite `/stage` enthält keine lesbare Spezifikation.
- Die drei Daten gehören zu einem Unternehmen, aber zu verschiedenen Produktoberflächen — Video, Stage und Realtime. Es handelt sich nicht um drei unabhängige Unternehmen, doch das Schicksal von Stage bleibt unklar.
- Die aktuellen Primärquellen widersprechen sich: Die Übersichtsseite nennt noch Krea 1 als Hauptmodell, während die Veröffentlichungen von 2026 Krea 2 als eigenes Foundation-Modell positionieren.
- Der Zugang zu Modellen, Tarifen, Credits und regionalen Beschränkungen wurde nicht für ein bestimmtes Konto geprüft. Die Angaben in der Dokumentation sind ein Richtwert, keine Garantie für den jeweils geltenden Tarif.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://www.krea.ai/video?kr_v=ol&krex=ol_flux | Krea Video | 2026-09-04 |
| https://www.krea.ai/stage | Krea Stage | 2026-09-04 |
| https://cgworld.jp/flashnews/01-202504-KreaStage.html | KREAに3Dシーン生成機能「Krea Stage」が追加 | 2026-09-04 |
| https://www.krea.ai/blog/announcing-realtime-video | Ankündigung: Realtime Video | 2026-09-04 |
| https://www.krea.ai/blog/krea-realtime-14b | Krea Realtime 14B: Echtzeit-Videogenerierung in großer Länge mit KI | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-image-model | Einführung von Krea 2 | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-lora-training | Krea 2 LoRA-Training ist jetzt verfügbar | 2026-09-04 |
| https://www.krea.ai/docs/user-guide/get-started/what-is-krea | Was ist Krea? | 2026-09-04 |
| https://www.krea.ai/docs/user-guide/features/video | Video-Modelle | Krea-Dokumentation | 2026-09-04 |
| https://www.krea.ai/docs/user-guide/features/realtime | Realtime | Krea-Dokumentation | 2026-09-04 |
| https://www.krea.ai/blog/krea-edit | Ein neues, leistungsstärkeres Krea Edit | 2026-09-04 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `organization:krea-ai`, Strang `video-generation`, 3 datierte Ereignisse 2025-04-16 → 2025-08-29.
- **Praktischer Hinweis:** Ab 2025-08-29 sollten Praktiker, die Krea AI bewerten, die Oberfläche Realtime Video in Workflow-Vergleiche einbeziehen und dabei aktuelle Zugänglichkeit, Verhalten und Fähigkeiten unabhängig prüfen.
- **Konfidenz:** mittel. Die datierten, ersetzten Einträgen oben bestimmen, was veraltet ist.
