---
title: "Snapchat"
category: projects
date: 2022-06-06
tags: [project, snapchat, snapchat-lenses, snapchat-lenses-and-filters, snapchat_crying_filter]
aliases: ["Snapchat"]
level: 2
source_sha256: 17efafda8744c864dc33894eae346c33db6e884e13c0d56cddc736f1c98cce0e
translation: machine
translated_at: '2026-10-24'
---
# Snapchat {#snapchat}

**Entwicklungslinie:** `project:snapchat` · Thread `snapchat-lenses-and-filters`  
**Letztes Ereignis:** 2022-06-06 · 1 datiertes Ereignis seit 2022-06-06 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

Snapchat ist eine Kamera-App und die Lens-Studio-AR-Plattform für Nutzer, Creator und Entwickler: Face Lenses, World Lenses, Vorlagen, Scripting, SnapML und Veröffentlichung auf Snapchat, Camera Kit und Spectacles.

Eingereichte Lenses sind auf 8 MB begrenzt, für ein SnapML-Modell sind bis zu 10 MB möglich. Lens Studio ist ein praktikabler Weg, AR-Effekte zu bauen, kein Werkzeug, um einen bestimmten alten viralen Filter nachzubauen.

## Entwicklungslinie {#development-line}

- **2022-06-06 — Ein Snapchat-Lens-Link wurde in der Entwicklungslinie erfasst.** Am 2022-06-06 verlinkte eine Nachricht eine Snapchat-Lens-URL zusammen mit einer Quellenangabe. Die datierten Links belegen ein lensbezogenes Snapchat-Element in dieser Entwicklungslinie, belegen aber weder dessen Funktionalität, Urheberschaft noch Veröffentlichungsstatus.

## Was sich geändert hat {#what-changed}

2022-05-12 — Crying Lens wurde zu einem viel diskutierten Snapchat-AR-Effekt; ein Drittanbieterbericht nennt das Debüt am 6. Mai und über 1 Milliarde Nutzungen bis zum 12. Mai.

2022-06-06 — Eine eigenständige Snapchat-Lens-Seite wurde zitiert, doch Name, Autor und Funktionen konnten wir nicht unabhängig prüfen; eine Verbindung zu Crying Lens bleibt unbestätigt.

2022-12-06 — Snap beschrieb die Plattform als Möglichkeit, Lenses nicht nur auf Snapchat, sondern auch über Camera Kit und für Spectacles zu veröffentlichen, und meldete über 3 Millionen erstellte AR-Lenses.

## Anwendung {#how-to-use-this}

Stand 2022-06-06 sollten Praktiker, die Snapchat-Arbeiten verfolgen, Lens-URLs als konkrete Implementierungs- oder Distributionsfläche erfassen. Nicht belegte Aussagen über Verhalten oder Status einer Lens gehören dagegen nicht in die Dokumentation.

1. Melde dich über Snapchat bei Lens Studio an und wähle entweder eine Vorlage für eine einfache Lens oder beginne von vorn; Mobil- und Web-Werkzeuge dienen Gelegenheits-Creators, während der Desktop für komplexe Entwicklung gedacht ist.
  — <https://help.snapchat.com/hc/en-gb/articles/7012330991124-How-can-I-create-Lenses-for-Snapchat>
2. Lege Projektname, Plattform und Größe fest; für mobile Lenses solltest du das 8-MB-Limit einhalten und die integrierten Validierungsprüfungen kontrollieren.
  — <https://developers.snap.com/lens-studio/publishing/configuring/configuring-project-info?lang=en-US>
3. Klicke in Lens Studio auf Publish, erstelle oder wähle eine Organisation und einen Lens Folder und reiche die Lens dann als neues Projekt ein oder aktualisiere ein bestehendes.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>
4. Wähle Upload and Publish, um in Snapchat zu veröffentlichen, oder Upload to Lens Folder, wenn die Lens nur für die weitere Distribution über Camera Kit oder Business Manager benötigt wird.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>

## Bewährte Praktiken {#best-practices}

- Prüfe vor der Einreichung Performance, Gerätekompatibilität und Richtlinienkonformität: Die Veröffentlichung durchläuft Validierung, automatisierte Tests und Inhaltsprüfung.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>
- Kopiere keine ML-Modelle oder viralen Lenses; verwende eine klare Vorschau, setze Lens Hints und komprimiere Assets. Die Dokumentation empfiehlt, unter 8 MB zu bleiben.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>
- Füge keine irrelevanten Tags hinzu: Sie werden moderiert und verbessern die Reichweite der Lens nicht.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>

## Dadurch überholt {#superseded-by-this}

- Vor 2022-12-06: die Auffassung, Lenses seien nur für Snapchat gedacht; Snap dokumentierte außerdem die Nutzung veröffentlichter AR-Effekte in Camera Kit und auf Spectacles.
- Vor dem aktuellen Lens Studio 5: ein reiner Desktop-Ansatz für alle Creator; die aktuelle Unterstützung trennt Desktop für komplexe AR-Projekte von Mobil- und Web-Werkzeugen für persönliche Creations.

## Weiterhin unbekannt {#still-unknown}

- Crying Lens und der Lens-Link vom 2022-06-06 könnten unter Snapchat getrennte Themen sein: Die eigenständige Lens-Seite war für eine unabhängige Prüfung nicht verfügbar.
- Es wurde keine primäre Snap-Quelle mit einem Veröffentlichungsdatum für Crying Lens gefunden; das Debüt am 6. Mai und die frühe Nutzungszahl sind durch eine Sekundärquelle vom 12. Mai 2022 belegt.
- Wir können nicht bestätigen, ob die konkrete Lens unter dem Link vom 2022-06-06 heute noch verfügbar ist.

## Quellen {#sources}

| Quelle | Titel | Gelesen am |
|---|---|---|
| https://www.bustle.com/life/how-to-use-crying-filter-snapchat-tiktok-instagram | How To Use The Crying Filter On Snapchat, TikTok, Instagram & More | 2026-09-05 |
| https://www.tmz.com/2022/05/12/snapchat-new-crying-face-filter-not-inspired-by-amber-heard/ | Snapchat's New Crying Face Filter NOT Inspired by Amber Heard | 2026-09-05 |
| https://help.snapchat.com/hc/en-gb/articles/7012330991124-How-can-I-create-Lenses-for-Snapchat | How can I create Lenses for Snapchat? | 2026-09-05 |
| https://developers.snap.com/lens-studio/home | Lens Studio | 2026-09-05 |
| https://developers.snap.com/lens-studio/publishing/configuring/configuring-project-info?lang=en-US | Configuring Project Settings | 2026-09-05 |
| https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens | Submitting Your Lens | 2026-09-05 |
| https://newsroom.snap.com/lens-fest-2022 | Lens Fest 2022: Celebrating Five Years of the Snap AR Community | 2026-09-05 |

## Agent-Kurzbeschreibung {#agent-brief}

- **Gegenstand:** `project:snapchat`, Thread `snapchat-lenses-and-filters`, 1 datiertes Ereignis 2022-06-06 → 2022-06-06.
- **Praxishinweis:** Stand 2022-06-06 sollten Praktiker, die Snapchat-Arbeiten verfolgen, Lens-URLs als konkrete Implementierungs- oder Distributionsfläche erfassen. Nicht belegte Aussagen über Verhalten oder Status einer Lens gehören dagegen nicht in die Dokumentation.
- **Konfidenz:** mittel. Die datierten Überholungsangaben oben sind maßgeblich dafür, was veraltet ist.
