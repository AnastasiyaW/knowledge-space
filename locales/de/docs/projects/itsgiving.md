---
title: "Itsgiving: itsgiving"
category: "projects"
date: 2026-09-12
tags: ["itsgiving", "project"]
aliases: ["Itsgiving: itsgiving"]
level: 2
source_sha256: 031cd37ad35acf3302daa068c72406eedb9557912a9c1cae2835a3bbe2c13a2f
translation: machine
translated_at: '2026-10-24'
---
# Itsgiving: itsgiving {#itsgiving-itsgiving}

**Entwicklungsstrang:** project:itsgiving · thread itsgiving  
**Letztes Ereignis:** 2026-09-12 · 2 datierte seit 2026-09-12 · **Recherchiert:** 2026-09-12 · Konfidenz: mittel

## Was es ist {#what-it-is}

ItsGiving ist ein Python-Webcam-Tool für Meeting-Teilnehmer. Es erkennt Gesichtsausdrücke sowie Hand- und Körperposen und blendet passende Bilder oder GIFs ein. Das Ergebnis wird als virtuelle Kamera bereitgestellt.

Es enthält 14 eingebaute Reaktionen, benutzerdefinierte Assets und Posen sowie einen kalibrierten v2-Detektor. Es benötigt Python 3.11 oder 3.12. Beim ersten Start werden drei MediaPipe-Modelle heruntergeladen, insgesamt etwa 15 MB.

Verwende das kalibrierte v2-Skript. Das Projekt dokumentiert v1 als Legacy-Verhalten mit festen Schwellenwerten.

## Entwicklungsstrang {#development-line}

- **2026-09-12 — ItsGiving - Face/Gesture-to-Meme Streaming Tool.** Ein Webcam-Tool, das Gesichts- und Gestenerkennung nutzt und passende Memes in einem Stream anzeigt. Es lässt sich mit Zoom, Meet, Discord und Teams integrieren.
  - Das Projekt dokumentiert 14 Reaktionen und eine Ausgabe als virtuelle Kamera für Zoom, Meet, Teams, Discord und OBS. Die empfohlene Implementierung ist \`its\_giving\_v2.py\`. Sie zeichnet eine siebensekündige Baseline mit neutralem Gesicht auf und bewertet Ausdrücke relativ dazu. (undatierte Re) — <https://github.com/gazijarin/itsgiving>
  - Das Projekt dokumentiert 14 Reaktionen und eine Ausgabe als virtuelle Kamera für Zoom, Meet, Teams, Discord und OBS. Die empfohlene Implementierung ist \`its\_giving\_v2.py\`. Sie zeichnet eine siebensekündige Baseline mit neutralem Gesicht auf und bewertet Ausdrücke relativ dazu. (undatierte Re) — <https://github.com/gazijarin/itsgiving>
- **2026-09-12 — ItsGiving Webcam Tool with Face/Gesture Tracking and Meme Integration.** Ein Webcam-Tool, das Gesichts- und Gestenerkennung nutzt und passende Memes in einem Stream anzeigt. Es lässt sich mit Zoom, Meets, Discord und Teams integrieren.
  - Das Projekt dokumentiert 14 Reaktionen und eine Ausgabe als virtuelle Kamera für Zoom, Meet, Teams, Discord und OBS. Die empfohlene Implementierung ist \`its\_giving\_v2.py\`. Sie zeichnet eine siebensekündige Baseline mit neutralem Gesicht auf und bewertet Ausdrücke relativ dazu. (undatierte Re) — <https://github.com/gazijarin/itsgiving>
  - Das Projekt dokumentiert 14 Reaktionen und eine Ausgabe als virtuelle Kamera für Zoom, Meet, Teams, Discord und OBS. Die empfohlene Implementierung ist \`its\_giving\_v2.py\`. Sie zeichnet eine siebensekündige Baseline mit neutralem Gesicht auf und bewertet Ausdrücke relativ dazu. (undatierte Re) — <https://github.com/gazijarin/itsgiving>

## Was sich geändert hat {#what-changed}

Das öffentliche Repository dokumentiert eine kalibrierte v2-Implementierung neben der v1-Implementierung mit festen Schwellenwerten. Ein separat datierter öffentlicher Entwicklungsschritt nach dem geprüften Datum wurde nicht verifiziert.

## So verwendest du es {#how-to-use-this}

1. Erstelle eine virtuelle Python-3.11- oder 3.12-Umgebung und installiere die fixierten Abhängigkeiten.
  — <https://github.com/gazijarin/itsgiving>
2. Führe \`python its\_giving\_v2.py --calibrate\` aus. Bleibe während der siebensekündigen Kalibrierung neutral und starte danach \`python its\_giving\_v2.py\`.
  — <https://github.com/gazijarin/itsgiving>
3. Installiere ein Backend für virtuelle Kameras für das Betriebssystem. Starte ItsGiving vor der Meeting-Anwendung und wähle anschließend die veröffentlichte virtuelle Kamera in den Video-Einstellungen dieser Anwendung aus.
  — <https://github.com/gazijarin/itsgiving>

## Best Practices {#best-practices}

- Belasse die Abhängigkeits-Fixierungen unverändert. Die dokumentierten Kompatibilitätsvorgaben für MediaPipe, NumPy und OpenCV hängen voneinander ab.
  — <https://github.com/gazijarin/itsgiving>
- Verwende v2 und kalibriere bei Bedarf neu. Die Schwellenwerte für Ausdrücke beruhen auf der Neutral-Gesicht-Baseline des Nutzers.
  — <https://github.com/gazijarin/itsgiving>
- Prüfe beim Hinzufügen einer Pose die Reihenfolge der Posen, bevor du Schwellenwerte senkst. Die erste passende Pose gewinnt. Nutze das HUD und eine Armzählung, um Fehlauslösungen zu justieren.
  — <https://github.com/gazijarin/itsgiving>
- Teste Reaktionen, bevor du sie in einem Meeting einsetzt. Die Ausgabe kann automatisch ausgelöst werden und ist für alle Teilnehmer des Anrufs sichtbar.
  — <https://github.com/gazijarin/itsgiving>

## Abgelöst durch dies {#superseded-by-this}

- Noch nichts als veraltet markiert.

## Noch unbekannt {#still-unknown}

- Die öffentliche Repository-Seite ist nicht datiert. Sie bestätigt die geprüften Einträge vom 2026-09-12, legt aber nicht den genauen Veröffentlichungszeitpunkt fest und zeigt nicht, welcher der beiden Einträge vom selben Tag einer eigenständigen Projektänderung entspricht.
- Die geprüfte VK-URL konnte während der Recherche nicht öffentlich abgerufen werden.
- Es wurde keine brauchbare chinesischsprachige (vereinfachtes Chinesisch) Quelle zu diesem konkreten Projekt gefunden.

## Quellen {#sources}

| source | title | read |
|---|---|---|
| https://github.com/gazijarin/itsgiving | gazijarin/itsgiving — It's giving... | 2026-09-13 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** project:itsgiving, Thread itsgiving, 2 datierte Ereignisse 2026-09-12 → 2026-09-12.
- **Praktischer Hinweis:** Siehe die belegten Abschnitte zu Nutzung und Praxis oben, einschließlich ihrer Grenzen.
- **Konfidenz:** mittel. Datierte Ablösungen oben sind maßgeblich dafür, was veraltet ist.
