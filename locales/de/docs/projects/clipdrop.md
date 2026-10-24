---
title: "Clipdrop"
category: projects
tags: [clipdrop, clipdrop-image-editing, project]
aliases: ["Clipdrop", "Clipdrop Relight"]
level: 3
source_sha256: 87589727ded8a35926419f0bef798e16270f97cd9f6b06e28f75bd591f6d5b65
translation: machine
translated_at: '2026-10-24'
---
# Clipdrop {#clipdrop}

**Entwicklungslinie:** `project:clipdrop` · Thread `clipdrop-image-editing`  
**Ereignisse:** 2 datiert, 2022-09-09 → 2023-04-08 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

Clipdrop ist ein browserbasiertes Bildwerkzeug für Kreative, das Photoshop-Retusche mit separaten Web-Generatoren kombiniert.

- Hintergrund- und Objektentfernung: Hintergründe, Objekte, Personen und Text entfernen oder ersetzen
- Relighting: Beleuchtung bestehender Bilder mit virtuellen Lichtquellen anpassen
- Bildverbesserung: hochskalieren, entrauschen, erweitern (uncrop), in der Größe ändern und aus Text generieren
- Reimagine: Variationsgenerierung im Jasper Document Editor mit einem Business-Tarif ausführen

Clipdrop listet neun Browser-Tools; das kostenlose Relight-Kontingent beträgt 20 Nutzungen pro 24 Stunden.

Wir nutzen die direkten Web-Tools für einmalige Bearbeitungen und Jasper für den verbliebenen Reimagine-Workflow.

## Entwicklungslinie {#development-line}

- **2022-09-09 — Clipdrop veröffentlicht Relight.** Bild hochladen, virtuelle Lichtquellen positionieren, anschließend das Ergebnis herunterladen.
- **2023-04-08 — Clipdrop veröffentlicht Stable Diffusion Reimagine.** Aus einem Ausgangsbild mehrere neue Variationen erzeugen, statt es exakt zu reproduzieren.

## Was sich geändert hat {#what-changed}

Clipdrop hat die Bildbearbeitung von eigenständigen Webseiten in eine Aufteilung zwischen den Clipdrop-Webwerkzeugen und dem Editor von Jasper verlagert.

- 2022-09-09 — Relight war die erfasste Funktion: Bild hochladen, virtuelle Lichtquellen positionieren, anschließend das Ergebnis herunterladen.
- 2023-04-08 — Stable Diffusion Reimagine war die erfasste Funktion: aus einem Ausgangsbild mehrere neue Variationen erzeugen, statt es exakt zu reproduzieren.
- 2026-09-04 — Die eigenständige Reimagine-URL leitet auf die Clipdrop-Startseite weiter, und Reimagine fehlt im Web-Katalog mit neun Tools; Jasper dokumentiert es im Document Editor, eingeschränkt auf Business-Nutzer.
- 2026-09-04 — Die Clipdrop-Website nennt die Übernahme von InitML durch Stability im Februar 2023 und den Verkauf an Jasper im Februar 2024.

Der aktuelle direkte Katalog enthält Relight, aber nicht Reimagine.

Alte Reimagine-Links sind veraltete Einstiegspunkte und kein Beleg dafür, dass die Funktion verschwunden ist.

## So verwenden Sie das {#how-to-use-this}

Stand 2023-04-08 verfolgen wir Clipdrop für Relighting und Workflows mit Stable Diffusion Reimagination, prüfen jedoch Verfügbarkeit und Verhalten, bevor wir eines der beiden Werkzeuge auswählen.

1. Den direkten Clipdrop-Katalog öffnen und das Einzweck-Tool wählen, das zur Bearbeitung passt.
  — <https://clipdrop.co/tools>
2. Für Relight das Ausgangsbild auf der Relight-Seite hochladen.
  — <https://clipdrop.co/relight>
3. Die virtuellen Lichtquellen verschieben, das Ergebnis beurteilen und die gewählte Version herunterladen.
  — <https://clipdrop.co/relight>
4. Für Reimagine ein Bild im Jasper Document Editor hinzufügen oder hochladen, darüberfahren, Edit wählen und anschließend Reimagine auswählen; Jasper dokumentiert dies als Tool für Business-Tarife.
  — <https://help.jasper.ai/hc/en-us/articles/25074326466971-How-to-Add-Images-to-Your-Jasper-Content>
5. Vor einem Stapel das aktuelle Kontingent und die Auflösungsstufe prüfen; kostenloses Relight ist mit 20 Nutzungen pro 24 Stunden angegeben, Pro-Relight in hoher Auflösung mit 1.000 pro 24 Stunden.
  — <https://clipdrop.co/pricing>

## Bewährte Vorgehensweisen {#best-practices}

- Reimagine für Variationen verwenden, nicht für Erhalt: Es erzeugt vom Eingabebild inspirierte Bilder und reproduziert dessen Pixel nicht.
  — <https://stability.ai/news-updates/stable-diffusion-reimagine>
- Für Cleanup etwas über das unerwünschte Objekt hinaus malen und dessen Schatten einbeziehen; Clipdrop merkt an, dass die größere Maske die Rekonstruktion verbessert.
  — <https://clipdrop.co/cleanup>
- Die alte eigenständige Reimagine-URL als Weiterleitung behandeln und stattdessen den Jasper Document Editor nutzen, statt einen Workflow auf der veralteten Seite aufzubauen.
  — <https://help.jasper.ai/hc/en-us/articles/25074326466971-How-to-Add-Images-to-Your-Jasper-Content>
- Das Volumen vor der Produktion planen: Das öffentliche kostenlose Kontingent für Relight, Cleanup und x2 Upscale beträgt 20 Nutzungen pro 24 Stunden.
  — <https://clipdrop.co/pricing>

## Hiermit ersetzt {#superseded-by-this}

- 2023-04-08 — Der eigenständige Stable-Diffusion-Reimagine-Workflow über die Webseite ist veraltet: Seine Clipdrop-URL leitet nun auf die Startseite weiter; der aktuell dokumentierte Zugang ist Jasper Document Editor > Edit > Reimagine für Business-Nutzer.
- 2022-09-09 — Clipdrop als eigenständiges InitML-Produkt zu behandeln ist veraltet: Die aktuelle Clipdrop-Website besagt, dass InitML 2023 von Stability übernommen und 2024 an Jasper verkauft wurde.

## Weiterhin unbekannt {#still-unknown}

- Die Quelle lieferte keine unabhängig überprüfbaren Inhalte, daher stützt sie keine Aussage.
- Keine aktuelle Seite des Anbieters belegt eine öffentliche eigenständige Reimagine-Oberfläche oder nennt deren aktuelles Kontingent; verifizierter aktueller Zugang ist der Jasper Document Editor für Business-Nutzer.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://clipdrop.co/ | Create stunning visuals in seconds with AI. | 2026-09-04 |
| https://clipdrop.co/tools | Tools — Clipdrop | 2026-09-04 |
| https://clipdrop.co/relight | Clipdrop - Relight | 2026-09-04 |
| https://clipdrop.co/stable-diffusion-reimagine | Create stunning visuals in seconds with AI. (redirected from Stable Diffusion Reimagine) | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-reimagine | Stable Diffusion Reimagine — Stability AI | 2026-09-04 |
| https://help.jasper.ai/hc/en-us/articles/25074326466971-How-to-Add-Images-to-Your-Jasper-Content | How to Add Images to Your Jasper Content — Jasper Help Center | 2026-09-04 |
| https://clipdrop.co/cleanup | Clipdrop - Cleanup | 2026-09-04 |
| https://clipdrop.co/pricing | Clipdrop - pricing | 2026-09-04 |

## Agent-Briefing {#agent-brief}

- **Gegenstand:** `project:clipdrop`, Thread `clipdrop-image-editing`, 2 datierte Ereignisse 2022-09-09 → 2023-04-08.
- **Praxishinweis:** Stand 2023-04-08 sollten Praktiker Clipdrop als Produkt mit datierten öffentlichen Referenzen für Relighting- und Stable-Diffusion-Reimagination-Workflows behandeln und vor der Auswahl eines der beiden Werkzeuge Verfügbarkeit und Verhalten prüfen.
- **Konfidenz:** mittel. Die datierten „Hiermit ersetzt“-Einträge sind maßgeblich dafür, was veraltet ist.
