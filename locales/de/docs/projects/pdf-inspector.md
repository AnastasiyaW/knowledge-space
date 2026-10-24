---
title: "pdf-inspector"
category: projects
date: 2026-08-03
tags: [firecrawl, pdf-inspector, pdf-inspector-development, project]
aliases: ["pdf-inspector"]
level: 3
source_sha256: 1e48e5441065519fb29b77de8d0959d7ad85cc1dc5bb9341a260d7e684400e7f
translation: machine
translated_at: '2026-10-24'
---
# pdf-inspector {#pdf-inspector}

**Entwicklungslinie:** `project:pdf-inspector` · Thread `pdf-inspector-development`  
**Letztes Ereignis:** 2026-08-03 · 1 datiertes seit 2026-08-03 · **Recherchiert:** 2026-09-05 · Konfidenz: mittel

## Was es ist {#what-it-is}

pdf-inspector — eine lokale Rust-Bibliothek und CLI für Entwickler von PDF-Verarbeitung: Sie klassifiziert native Text-, gescannte, bildbasierte und gemischte PDFs und liefert anschließend strukturiertes Markdown und seitenbezogene Routing-Daten. — Einstiegspunkte für Rust, Python, Node.js, CLI und Browser-WebAssembly. — Positionsbewusster Text, Lesereihenfolge, Tabellenerkennung und optionale OCR mit Herkunftsangabe. Die Klassifizierung ist laut Dokumentation mit etwa 10–50 ms angegeben; geroutete OCR benötigt externes PDFium, ONNX Runtime und einen Modellsatz von etwa 31 MB. Nutzen Sie es als lokale Schicht für Klassifizierung und Extraktion, validieren Sie jedoch die Dokumentstrukturen, auf die es in Ihrem Workflow ankommt.

## Entwicklungslinie {#development-line}

- **2026-08-03 — pdf-inspector-Repository im Firecrawl-Thread verlinkt.** Am 2026-08-03 wurde das GitHub-Repository von pdf-inspector im Firecrawl-Thread verlinkt. Das ist ein wesentlicher historischer Verweis, weil er das Quell-Repository des Projekts zu diesem Datum identifiziert. Die verfügbaren Belege belegen weder ein Release, eine Funktionsänderung noch die Reife des Projekts.

## Was sich geändert hat {#what-changed}

2026-08-03 — Das Python-Paket von pdf-inspector war bereits als 0.2.6 öffentlich; am selben Tag wurden Fehler bei fehlerhaften xref-Tabellen und dünnen Tabellen gemeldet, daher ist das Datum kein verifizierter Launch. 2026-08-06 — pdf-inspector wurde als eigenständige Open-Source-PDF-Engine von Firecrawl und als Bestandteil gehosteter Dokument-Endpunkte dokumentiert. 2026-08-10 — pdf-inspector erhielt den verifizierten Tag packages-2026-08-10, der die Paketversionen über die Python-Linie 0.2.6 hinaus konsolidiert. 2026-08-13 — pdf-inspector v1.14.2 ergänzte Ressourcengrenzen für pathologische PDFs sowie Korrekturen für Form XObject und Layout. 2026-08-17 — pdf-inspector v1.15.0 ergänzte selektive OCR über PDFium, ONNX Runtime und PP-OCRv6 Small. 2026-08-21 — PyPI veröffentlichte pdf-inspector 1.17.0, die aktuelle öffentliche Python-Paketlinie. 2026-09-03 — Der main-Branch von pdf-inspector erhielt Änderungen an der Geometrie gedrehten Texts und an den Koordinaten der sichtbaren Seite; diese Quelländerungen sind weiterhin nicht veröffentlicht.

## So wird es verwendet {#how-to-use-this}

Stand 2026-08-03 können Praktiker das verlinkte pdf-inspector-Repository als datierte Quellenreferenz nutzen, wenn sie PDF-Inspektionsarbeiten im Zusammenhang mit Firecrawl bewerten.

1. Installieren Sie die Python-Bindung mit `pip install pdf-inspector` und rufen Sie anschließend für jede Eingabe `detect_pdf()` auf, bevor Sie einen Verarbeitungspfad festlegen.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
2. Für ein Ergebnis mit nativem Text rufen Sie `process_pdf()` auf, um Markdown sowie Typ, Konfidenz, Seitenzahl, Seiten mit OCR-Bedarf, Layoutsignale und Kennzeichen für Kodierungsprobleme zu erhalten.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
3. Für gescannte oder gemischte Dokumente rufen Sie `process_pdf_with_ocr()` im Automatikmodus auf und bewahren Sie für jede Seite die Herkunft als nativ, OCR oder fusioniert auf.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
4. Wenn OCR geroutet wird, installieren Sie die dokumentierten PDFium- und ONNX-Runtime-Builds, setzen Sie deren Bibliothekspfade und befüllen Sie ein Modellverzeichnis vorab, und aktivieren Sie den Offline-Modus, wenn Netzwerkzugriff nicht erlaubt ist.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/ocr-runtime.md>
5. Verwenden Sie in einem Node-Server die asynchrone Funktion `processPdfWithOcr()` und prüfen Sie `pagesRoutedToOcr` und `pagesRecommendingHosted`.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md>

## Bewährte Praktiken {#best-practices}

- Behandeln Sie die Klassifizierung als Routing und nicht als pauschale OCR-Entscheidung: Bewahren Sie Typ, Konfidenz, Gründe pro Seite und Seitenherkunft zusammen mit dem extrahierten Inhalt auf.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md>
- Fixieren Sie PDFium 153.0.7988.0, ONNX Runtime 1.27.0 und die Revision des PP-OCRv6-Small-Artefakts für reproduzierbare OCR; befüllen Sie Modelle vorab und nutzen Sie den Offline-Modus für abgeschottete Deployments.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/ocr-runtime.md>
- Benchmarken Sie repräsentative PDFs, statt aus dem veröffentlichten Vergleich mit 200 Dokumenten auf einem Apple M4 Pro ohne OCR zu verallgemeinern.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>
- Halten Sie PDFs mit fehlerhaftem startxref im Regressionsprotokoll fest; ein Bericht vom 3. August zeigte, dass Klassifizierung und Extraktion bei ihnen in 0.2.6 beide fehlschlagen konnten.
  — <https://github.com/firecrawl/pdf-inspector/issues/228>
- Validieren Sie dünn besetzte und gruppierte Tabellen gegen die Quellseiten, denn ein Bericht vom 3. August zeigte in 0.2.6 wohlgeformtes, aber strukturell falsches Markdown mit zusammengefallenen Zeilen.
  — <https://github.com/firecrawl/pdf-inspector/issues/229>
- Normalisieren Sie Seitenzahl-Konventionen an Ihrer Schnittstelle: Klassifizierung und Bereichsextraktion verwenden 0-basierte Seitenlisten, während OCR-Selektoren und mehrere Ergebnistypen 1-basierte Seitenzahlen verwenden.
  — <https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md>

## Durch diesen Eintrag überholt {#superseded-by-this}

- 2026-08-03 — das Repository-Link als Beleg dafür zu behandeln, dass pdf-inspector an diesem Tag gestartet wurde.
- Vor 2026-08-17 — jede gescannte oder gemischte Seite manuell an ein anderes OCR-System zu übergeben, als einzig unterstützter Weg.

## Weiterhin unbekannt {#still-unknown}

- Das genaue Release bzw. die Absicht zum 2026-08-03 ist nicht verifiziert: Der Repository-Link enthält weder Version noch Release-Notiz, während Issue-Berichte vom selben Tag ein bereits öffentliches Paket 0.2.6 belegen.
- GitHub Releases markiert weiterhin 1.15.0 als neueste Version, während das aktuelle Quell-Manifest und PyPI 1.17.0 zeigen; eine GitHub-Release-Seite für 1.16.0 oder 1.17.0 wurde nicht gefunden.
- Die Koordinaten- und Änderungen an gedrehtem Text vom 2026-09-03 stehen im aktuellen Quellcode und im Abschnitt „Unreleased“ des Changelogs; ihre erste paketierte Version ist daher nicht verifiziert.
- Firecrawl gibt an, dass die gehosteten Endpunkte /parse und /scrape pdf-inspector verwenden; diese Recherche hat keinen der beiden Endpunkte selbst ausgeführt.

## Quellen {#sources}

| Quelle | Titel | gelesen |
|---|---|---|
| https://github.com/firecrawl/pdf-inspector | firecrawl/pdf-inspector | 2026-09-05 |
| https://raw.githubusercontent.com/firecrawl/pdf-inspector/main/README.md | pdf-inspector README | 2026-09-05 |
| https://raw.githubusercontent.com/firecrawl/pdf-inspector/main/Cargo.toml | pdf-inspector Cargo.toml | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/issues/228 | Issue #228: Keine xref-Wiederherstellung | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/issues/229 | Issue #229: Zeilen in dünn besetzten/gruppierten Tabellen fallen zusammen | 2026-09-05 |
| https://www.firecrawl.dev/blog/anydoc-and-pdf-inspector | Einführung von AnyDoc und pdf-inspector | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/tags | pdf-inspector-Tags | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/releases/tag/v1.14.2 | Release 1.14.2 — Gehärtetes Parsing für pathologische PDFs | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/releases/tag/v1.15.0 | Release 1.15.0 — Selektive OCR für gescannte und gemischte PDFs | 2026-09-05 |
| https://pypi.org/project/pdf-inspector/ | pdf-inspector auf PyPI | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/commit/636ca1a58bdc1af4cd3fc20b8c1f549a1121cca7 | Commit 636ca1a: Geometrie gedrehten Texts | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/CHANGELOG.md | pdf-inspector-Changelog | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md | pdf-inspector Python-API | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md | pdf-inspector Node.js-API | 2026-09-05 |
| https://github.com/firecrawl/pdf-inspector/blob/main/docs/ocr-runtime.md | Einrichtung der pdf-inspector-OCR-Laufzeitumgebung | 2026-09-05 |

## Agent-Kurzbrief {#agent-brief}

- **Gegenstand:** `project:pdf-inspector`, Thread `pdf-inspector-development`, 1 datiertes Ereignis 2026-08-03 → 2026-08-03.
- **Praktischer Hinweis:** Stand 2026-08-03 können Praktiker das verlinkte pdf-inspector-Repository als datierte Quellenreferenz nutzen, wenn sie PDF-Inspektionsarbeiten im Zusammenhang mit Firecrawl bewerten.
- **Konfidenz:** mittel. Die datierten Überholungsvermerke oben sind maßgeblich dafür, was veraltet ist.
