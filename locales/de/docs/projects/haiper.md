---
title: "Haiper — Öffentlicher Start und iOS-Verfügbarkeit"
category: projects
date: 2024-03-16
tags: [haiper, project, public-launch-and-ios-availability]
aliases: ["Haiper"]
level: 3
source_sha256: 94cad6e91839178a766287f4845f16c5760f9b23ec3d6bb6134040d1995b225e
translation: machine
translated_at: '2026-10-24'
---
# Haiper — Öffentlicher Start und iOS-Verfügbarkeit {#haiper-public-launch-and-ios-availability}

**Entwicklungslinie:** `project:haiper` · Thread `public-launch-and-ios-availability`  
**Letztes Ereignis:** 2024-03-16 · 2 datierte Ereignisse seit 2024-03-13 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Haiper war eine Cloud-Videoplattform für Kreative und Integratoren, die im Bereich Text-zu-Video und Bild-zu-Video direkt mit Runway konkurrierte.

- Videoerzeugung: Text-zu-Video, Bild-zu-Video, Keyframe-Konditionierung, Video-zu-Video und Text-zu-Bild.
- Zugang: Web, iOS und HTTP-API (früher).

Die veröffentlichte Dokumentation der Version 2.x nennt Ausgaben in 540p und 720p zu 5–8 Credits pro Sekunde. Weder ein bezahlter Zugang noch ein abgeschlossener neuer Auftrag ist jedoch verifiziert. Haiper sollte nicht für einen neuen Produktionsworkflow gewählt werden, und die API ist als Legacy zu behandeln, bis ein autorisierter Testauftrag erfolgreich ist.

## Entwicklungslinie {#development-line}

- **2024-03-13 — Auf die offizielle Website von Haiper wurde öffentlich verwiesen.** Der Dienst bot kostenlose kurze Text-zu-Video-Erzeugung, Bildanimation und Repaint für 2 Sekunden in HD oder bis zu 4 Sekunden in geringerer Qualität.
- **2024-03-16 — Auf die iOS-App von Haiper wurde öffentlich verlinkt.** Öffentliche Links führten am 2024-03-16 zur Apple-App-Store-Seite von Haiper und zu früheren Haiper-Materialien. Dies dokumentiert die öffentliche iOS-Verfügbarkeit bzw. Bewerbung der App zu diesem Zeitpunkt. Die vorliegenden Belege belegen weder die Funktionen der App, ihren Veröffentlichungsstatus noch den begleitenden Ankündigungstext.

## Was sich geändert hat {#what-changed}

- 2024-03-13 — Die Webadresse von Haiper wurde zum Einstiegspunkt. Die öffentliche Beta bot kostenlose kurze Text-zu-Video-Erzeugung, Bildanimation und Repaint für 2 Sekunden in HD oder bis zu 4 Sekunden in geringerer Qualität.
- 2024-03-16 — Eine App-Store-URL kam zum Web-Zugang hinzu. Damit war ein iOS-Vertriebsweg in den Produktlinks bestätigt, nicht jedoch das Veröffentlichungsdatum der App.
- 2024-10-21 — Haiper 2.0 und Templates erweiterten das Produkt von der reinen Generierung auf Modellversionen und die Erstellung von Videos aus Vorlagen.
- 2024-12-18 — Haiper 2.5 wurde mit einer API-Integration bei VEED gestartet, wodurch der Fokus auf Partner- und API-Workflows rückte.
- 2025-03-20 — Microsoft stellte zwei Mitgründer von Haiper ein.
- 2025-06-23 — NetMind kaufte das Haiper-KI-Modell, wodurch die Technologie den Besitzer wechselte.
- 2026-09-04 — Die Domain und die API-Dokumentation sind weiterhin online, doch es gibt keinen verifizierten neuen Benutzerlogin, keine Zahlung und keine abgeschlossene Generierung.

## Wie man das verwendet {#how-to-use-this}

Ab dem 2024-03-16 ist Haiper als Dienst mit öffentlich erwähnter Webpräsenz und iOS-Vertriebsweg zu betrachten. Die aktuelle Verfügbarkeit und Funktionalität sollten jedoch direkt überprüft werden, bevor man sich auf eines davon verlässt.

1. Prüfen, ob der Anbieter nach dem Aufladen tatsächlich einen API-Schlüssel ausstellt. Kommt kein Schlüssel an, abbrechen: Der öffentliche Startpfad bleibt unverifiziert.
  — <https://docs.haiper.ai/api-reference/authentication>
2. Mit einem gültigen Schlüssel genau einen Text-zu-Video-Auftrag an den dokumentierten Endpunkt senden und die generation_id speichern.
  — <https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video>
3. Den Status über die generation_id abfragen. pending, processing, post_processing und failed als getrennte Zustände behandeln.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-status>
4. Ergebnisse erst nach succeed abrufen. Der Detail-Endpunkt liefert die Video-URL und die Ausgaben.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-detail>

## Bewährte Praktiken {#best-practices}

- Die einzige Kopie eines Videos oder Projekts nicht in der Cloud von Haiper speichern: Nutzerberichte von Anfang Februar 2025 dokumentieren Serverausfälle und verlorene Projekte nach der Einstellung.
  — <https://uk.trustpilot.com/review/haiper.ai>
- Für Kundenmedien is_public=false explizit übergeben: Die veröffentlichte API setzt den Standardwert auf true.
  — <https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video>
- Ratenbegrenzungen in den Client einbauen: Die Dokumentation begrenzt den Datenverkehr auf 500 HTTP-Anfragen pro Minute und 40 gleichzeitige Generierungen. Bei 429 nicht blind wiederholen.
  — <https://docs.haiper.ai/api-reference/rate-limits>
- Details nicht abfragen, bevor der Status succeed zurückgibt: Zuerst den Status, danach die Details abfragen, um falsche Erfolgsmeldungen und leere Links zu vermeiden.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-detail>

## Hiermit überholt {#superseded-by-this}

- 2024-03-05 bis 2024-03-13: Die Empfehlung, sich für die kostenlose Verbraucher-Beta anzumelden und Videos in der Web-App zu erzeugen, ist für neue Nutzer veraltet. Der Verbraucherzugang ist nach den Ereignissen von 2025 nicht verifiziert.
- 2024-03-16: Die Empfehlung, die App über die ursprüngliche App-Store-URL zu installieren, ist als aktiver Onboarding-Weg veraltet. Die URL lieferte bei der Prüfung keine aktive Produktseite.
- 2024-12-18: Die Ankündigung der Haiper-2.5-API mit VEED ist eine historische Beschreibung der Integration und kein Beleg dafür, dass die API oder der Partnerweg heute neue Aufträge annimmt.
- Historische Preise aus der veröffentlichten Dokumentation sind kein aktuelles Angebot, solange Schlüsselbereitstellung und ein erfolgreicher Auftrag nicht bestätigt sind.

## Weiterhin unbekannt {#still-unknown}

- Haiper hat keine offizielle, datierte Erklärung zur Einstellung des Verbraucherprodukts veröffentlicht. Der Shutdown im Februar 2025 stützt sich auf Nutzerberichte und Sekundärquellen, nicht auf eine Mitteilung des Unternehmens.
- Es wurde kein autorisierter API-Auftrag ausgeführt und keine neue Schlüsselausstellung verifiziert. Die veröffentlichte Dokumentation könnte daher ein verlassenes Legacy-Artefakt sein.
- Die ursprüngliche App-Store-URL lieferte bei der Prüfung keinen aktiven Eintrag. Ihr regionaler Status, eine mögliche Entfernung und die Zugänglichkeit für bestehende Nutzer bleiben unbestätigt.
- NetMind hat den Kauf des Modells bestätigt, aber ob NetMind es heute neuen Nutzern anbietet, ist nicht verifiziert.

## Quellen {#sources}

| Quelle | Titel | Gelesen |
|---|---|---|
| https://haiper.ai/ | Haiper - AI Video Generator | 2026-09-04 |
| https://apps.apple.com/app/id6468952574 | Apple App Store URL, app id 6468952574 | 2026-09-04 |
| https://techcrunch.com/2024/03/05/competition-in-ai-video-generation-heats-up-as-deepmind-alums-unveil-haiper/ | Competition in AI video generation heats up as DeepMind alums unveil Haiper | 2026-09-04 |
| https://testapp.haiper.ai/home | Unlock Creativity with AI Content Generator Tools | Haiper | 2026-09-04 |
| https://testapp2.haiper.ai/blog/haiper-partners-with-veed | Haiper Launches Its 2.5 Model-Powered API with VEED | 2026-09-04 |
| https://sifted.eu/articles/microsoft-haiper-ai-hires-video-sora-inflection/ | Exclusive: Microsoft scoops up talent from AI video startup Haiper | 2026-09-04 |
| https://sifted.eu/articles/haiper-ai-sold-for-parts | Exclusive: Haiper AI sold for parts after Microsoft poaches cofounders | 2026-09-04 |
| https://uk.trustpilot.com/review/haiper.ai | Haiper Reviews | Read Customer Service Reviews of haiper.ai | 2026-09-04 |
| https://docs.haiper.ai/llms.txt | Haiper documentation index | 2026-09-04 |
| https://docs.haiper.ai/pricing | Pricing for Haiper Web App & iOS App - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/authentication | Authentication - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video | Text to Video - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/get-creation-status | Get Creation Status - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/get-creation-detail | Get Creation Detail - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/rate-limits | Rate Limits - Haiper | 2026-09-04 |

## Agenten-Briefing {#agent-brief}

- **Gegenstand:** `project:haiper`, Thread `public-launch-and-ios-availability`, 2 datierte Ereignisse vom 2024-03-13 bis 2024-03-16.
- **Praktischer Hinweis:** Ab dem 2024-03-16 sollten Praktiker Haiper als Dienst mit öffentlich erwähnter Webpräsenz und iOS-Vertriebsweg betrachten. Aktuelle Verfügbarkeit und Funktionalität sollten jedoch direkt überprüft werden, bevor man sich auf eines davon verlässt.
- **Konfidenz:** mittel. Die datierten Überholungshinweise sind maßgeblich dafür, was veraltet ist.
