---
title: "James Webb Space Telescope — Veröffentlichung der ersten Bilder"
category: projects
tags: [first-images-release, james-webb-space-telescope, james_webb_space_telescope, project]
aliases: ["James Webb Space Telescope"]
level: 2
source_sha256: a6de2d602316d55dcb81c40d52d9406c0f6adb2f63e4ab380ff45755aeda1b8c
translation: machine
translated_at: '2026-10-24'
---
# James Webb Space Telescope — Veröffentlichung der ersten Bilder {#james-webb-space-telescope-first-images-release}

**Entwicklungslinie:** `project:james-webb-space-telescope` · Strang `first-images-release`  
**Ereignisse:** 1 datiert, 2022-07-12 → 2022-07-12 · **Recherchiert:** 2026-09-04 · Konfidenz: mittel

## Was es ist {#what-it-is}

James Webb Space Telescope ist ein aktives Infrarot-Observatorium der NASA, ESA und CSA für Astronomen, die öffentlich zugängliche Daten von Weltraumobservatorien auswerten.

- MAST stellt Rohdaten, kalibrierte Daten und hochverarbeitete Produkte bereit.
- Die Open-Source-Pipeline des JWST verarbeitet jedes Instrument und jeden Beobachtungsmodus mit CRDS-Referenzdateien.

## Entwicklungslinie {#development-line}

- **2022-07-12 — Die ersten öffentlichen Bilder des James Webb Space Telescope werden veröffentlicht.** Webb ging am 2022-07-12 vom Commissioning in die öffentliche wissenschaftliche Datenbereitstellung über. Die Veröffentlichung gab der Öffentlichkeit und der wissenschaftlichen Gemeinschaft erstmals einen breiten Eindruck von der Beobachtungsfähigkeit des Teleskops.

## Was sich geändert hat {#what-changed}

- **2022-07-12.** Der Vergleich SMACS 0723 Hubble/Webb machte das erste Tiefenfeld zu einem direkten Test der Leistungsfähigkeit. Dies war ein Meilenstein für die öffentliche Wissenschaft, keine Hardware-Änderung.
- **2022-07-13.** Ein Medienobjekt ergänzte das NIRISS-Transmissionsspektrum von WASP-96 b und erweiterte die erste Veröffentlichung von Bildern auf die Exoplanetenspektroskopie. Das Quellobjekt erschien am 2022-07-12, daher markiert der 2022-07-13 die Verbreitung und nicht einen neuen Beobachtungsmodus.
- **2026-09-04.** Webb ist weiterhin aktiv. MAST verarbeitet Datenprodukte nach jedem quartalsweisen Operations-Build neu, daher sind frühere Downloads nicht zwingend aktuelle kalibrierte Produkte.

## Anwendung {#how-to-use-this}

Wenn Sie den Projektstand hinsichtlich der operativen Reife beschreiben, betrachten Sie JWST-Erstbildveröffentlichungen ab dem 2022-07-12 als historische Grenze zwischen Commissioning und öffentlicher wissenschaftlicher Beobachtungsdatenbereitstellung.

1. Prüfen Sie, ob die benötigten Beobachtungen öffentlich sind. Rufen Sie öffentliche MAST-Daten anonym ab oder authentifizieren Sie sich mit MyST-Zugangsdaten und Programmfreigabe für Daten mit exklusivem Zugriff.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data>
2. Suchen Sie im MAST Portal nach Programm, Instrument, Modus, Koordinaten oder Ziel. Verwenden Sie die JWST Mission Search für JWST-spezifische Filter.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access>
3. Laden Sie zuerst die minimal empfohlenen Produkte herunter. Wählen Sie Rohdaten, Zwischenprodukte, Guide-Star- oder Referenzdateien nur dann aus, wenn die Analyse sie benötigt.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access>
4. Für die Neuverarbeitung installieren Sie ein veröffentlichtes jwst-Paket unter Linux oder macOS. Konfigurieren Sie CRDS, bevor Sie das Paket importieren, und führen Sie dann die für den Beobachtungsmodus geeigneten Stufen aus.
  — <https://jwst-docs.stsci.edu/jwst-science-calibration-pipeline>
5. Für eine Publikation dokumentieren Sie die Pipeline-Version und den CRDS-Kontext, zitieren Sie die Daten und nehmen Sie die vorgeschriebene Missionsdanksagung auf.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/citing-jwst-data>

## Bewährte Vorgehensweisen {#best-practices}

- Beginnen Sie mit den von MAST minimal empfohlenen Produkten, statt standardmäßig Rohdaten herunterzuladen. Rufen Sie Produkte niedrigerer Stufe nur für einen klar definierten Reduktionsbedarf ab.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access>
- Verwenden Sie für allgemeine Analysen den Operations-Pipeline-Build und den kompatiblen Standard-CRDS-Kontext. Entwicklungs-Builds werden nicht als Standard empfohlen.
  — <https://jwst-docs.stsci.edu/jwst-science-calibration-pipeline>
- Dokumentieren Sie sowohl die jwst-Softwareversion als auch den CRDS-Kontext, wann immer Ergebnisse von einer Neuverarbeitung oder einer Kontextüberschreibung abhängen.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/citing-jwst-data>
- Prüfen Sie den aktuellen Kalibrierungsstatus und bekannte Probleme, bevor Sie ein heruntergeladenes Produkt als endgültig interpretieren, da sich Archivprodukte und Kalibrierungsversionen quartalsweise ändern.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data>

## Hiermit ersetzt {#superseded-by-this}

- Der Vergleich der ersten Bilder vom 2022-07-12 als Analysebasis wird durch die aktuelle MAST-Archivveröffentlichung ersetzt, da Produkte nach jedem quartalsweisen Operations-Build neu verarbeitet werden.
- Die Praxis vor Oktober 2024, veröffentlichte jwst-Software mit einem sich bewegenden CRDS-Kontext zu kombinieren, ist veraltet. Jede Pipeline-Version wählt nun einen kompatiblen, eingefrorenen Standardkontext, und Überschreibungen müssen dokumentiert werden.

## Weiterhin unbekannt {#still-unknown}

- Die ImgSli-Seite wurde während der Recherche nicht angezeigt. Daher sind ihre genaue Bildunterschrift, die Versionen der Quellbilder und die Verarbeitungseinstellungen nicht verifiziert.
- Das Objekt zu WASP-96 b ist auf den 2022-07-12 datiert; das Ereignisdatum 2022-07-13 kann daher keine eigenständige Änderung an Instrument oder Mission belegen.
- Die beiden datierten Einträge betreffen ein Teleskop, aber zwei verschiedene erste Bildergebnisse: einen Bildvergleich von SMACS 0723 und ein Transmissionsspektrum von WASP-96 b.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://imgsli.com/MTE2Mjc3 | ImgSli-Eintrag MTE2Mjc3 — Hubble/JWST-Vergleich von SMACS 0723; Seite wurde während der Recherche nicht angezeigt | 2026-09-04 |
| https://webbtelescope.org/contents/media/images/2022/032/01G72VSFW756JW5SXWV1HYMQK4?Collection=First+Images&news=true | Exoplanet WASP-96 b (NIRISS-Transmissionsspektrum) | 2026-09-04 |
| https://commons.wikimedia.org/wiki/File%3AExoplanet_WASP-96_b_%28NIRISS_Transmission_Spectrum%29_%282022-032-01G72VSFW756JW5SXWV1HYMQK4%29.png | Datei: Exoplanet WASP-96 b (NIRISS-Transmissionsspektrum) | 2026-09-04 |
| https://science.nasa.gov/mission/webb/webb-mission-timeline/ | Webb Mission Timeline | 2026-09-04 |
| https://science.nasa.gov/missions/webb/nasas-webb-delivers-deepest-infrared-image-of-universe-yet/ | NASA’s Webb Delivers Deepest Infrared Image of Universe Yet | 2026-09-04 |
| https://science.nasa.gov/mission/webb/ | James Webb Space Telescope | 2026-09-04 |
| https://jwst-docs.stsci.edu/accessing-jwst-data | Accessing JWST Data | 2026-09-04 |
| https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access | MAST Web Access | 2026-09-04 |
| https://jwst-docs.stsci.edu/jwst-science-calibration-pipeline | JWST Science Calibration Pipeline | 2026-09-04 |
| https://jwst-docs.stsci.edu/accessing-jwst-data/citing-jwst-data | Citing JWST Data | 2026-09-04 |

## Agent-Brief {#agent-brief}

- **Gegenstand:** `project:james-webb-space-telescope`, Strang `first-images-release`, 1 datiertes Ereignis 2022-07-12 → 2022-07-12.
- **Praktischer Hinweis:** Wenn Sie den Projektstand hinsichtlich der operativen Reife beschreiben, betrachten Sie JWST-Erstbildveröffentlichungen ab dem 2022-07-12 als historische Grenze zwischen Commissioning und öffentlicher wissenschaftlicher Beobachtungsdatenbereitstellung.
- **Konfidenz:** mittel. Die datierten Ersetzungshinweise sind maßgeblich dafür, was veraltet ist.
