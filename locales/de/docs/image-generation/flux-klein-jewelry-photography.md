---
title: "FLUX.2 [klein] Schmuck-Bildworkflow"
description: "Schmuckbilder sind ein quellenkontrollierter Produkt-Workflow: Bewahren Sie das freigegebene Asset, die Material- und Geometrienachweise, die Farbpipeline und die Rechtegrenze, und geben Sie erst nach visueller und sachlicher QA frei."
category: workflows
tags: [flux, flux2, klein, jewelry, product-photography, compositing, color-management, quality-control]
aliases: ["FLUX Klein Jewelry Photography", "Jewelry Product Imagery"]
level: 3
source_sha256: ef79a5d5e21a6fd9eba27db9b21441c44630a610b5941d637970df5858d5cd79
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 [klein] Schmuck-Bildworkflow {#flux2-klein-jewelry-imagery-workflow}

Schmuckbilder sind eine Aufgabe zur Produkttreue, nicht bloß eine Aufgabe zum
Fotorealismus. Ein Bild kann überzeugend wirken und dabei die Anzahl der Steine,
das Krappenlayout, die Metalloberfläche, eine Gravur, ein Logo oder die
Produktgeometrie verändern. Behandeln Sie das freigegebene Asset und den
Produktdatensatz im gesamten Workflow als maßgebliche Quelle.

## Quell- und Rechteprüfung {#source-and-rights-gate}

Erstellen Sie vor jeder Generierung oder Bearbeitung ein Quellpaket:

- freigegebenes Produktbild bzw. 3D-Asset und einen Inhalts-Digest;
- Produktkennung, freigegebene Ansichten, Material-, Stein- und Oberflächenangaben
  sowie untersagte Aussagen;
- Farbreferenz, Erfassungs- bzw. Renderraum und ggf. einen Nachweis über eine
  physische Farbkarte;
- Nutzungsrechte für die Quelle, Referenzen, Marken und abgeleitete Ausgaben; und
- einen festgelegten erlaubten Nutzungsumfang für das finale Bild.

Keine Modellausgabe kann fehlende Produktfakten oder Rechte belegen. Ist der
Produktdatensatz unvollständig, leiten Sie ihn zur Prüfung weiter, statt ein
generatives Modell die Lücke füllen zu lassen.

## Einen belegerhaltenden Weg wählen {#choose-an-evidence-preserving-route}

Verwenden Sie den am wenigsten generativen Weg, der das Briefing erfüllen kann:

1. **Quellerhaltende Bereinigung:** Entfernen Sie einen zulässigen Hintergrundfehler
   oder ein Präsentationsartefakt, während Sie die Produktmaske schützen.
2. **Kontrollierte Komposition:** Platzieren Sie ein freigegebenes Produkt-Asset in
   einer separat freigegebenen Szene mit deklarierten Geometrie-, Kontaktschatten-,
   Reflexions- und Farbvorgaben.
3. **Referenzgeführte Bearbeitung:** Wenn Sie die Bildbearbeitung von FLUX.2 nutzen,
   binden Sie genau die Modell-/API-Route und jede Eingabereferenz an den
   Job-Beleg. Der [offizielle Bearbeitungsleitfaden](https://docs.bfl.ai/flux_2/flux2_image_editing)
   beschreibt die referenzbasierte Bearbeitung, die Ausgabe erfordert jedoch
   weiterhin eine Prüfung der Produkttreue.
4. **Konzeptillustration:** Kennzeichnen Sie diese getrennt von Katalogbildern. Sie
   darf nicht verwendet werden, um ein bestehendes Produktmerkmal oder eine
   bestehende SKU zu suggerieren.

Halten Sie das Originalasset, die Maske, den Prompt bzw. die Bearbeitungsanweisung
und die Ausgabe im Job-Datensatz miteinander verknüpft. Machen Sie ein KI-bearbeitetes
Produkt niemals stillschweigend zu einer neuen Quelle der Wahrheit.

## Farb- und Materialkontrollen {#color-and-material-controls}

Wenden Sie vor der kreativen Gradation einen deklarierten Farbmanagement-Workflow an.
Bei einer physischen Aufnahme kann eine gemessene Farbkarte die Kalibrierung stützen;
eine gelernte oder generierte Farbschätzung kann diese Messung nicht ersetzen. Siehe
[[color-checker-and-white-balance]].

Prüfen Sie Metallton, Edelsteinfarbe, Kantenlichter, spiegelnde Reflexe,
Schattenrichtung und Kontaktauflage in der finalen Auslieferungsgröße. Verwerfen Sie
ein Bild, wenn seine Materialwirkung den freigegebenen Produktnachweisen widerspricht,
auch wenn es ästhetisch stärker ist.

## Produkttreue-QA {#product-fidelity-qa}

Jeder Kandidat benötigt einen menschlichen oder deterministischen Vergleich mit
freigegebenen Referenzen. Prüfen Sie mindestens:

- Silhouette, Proportionen, Ketten- bzw. Gliederanzahl, Steinanzahl, Fassungs- und
  Krappenform, Gravur sowie lesbare Kennzeichnungen;
- Metall- und Edelsteinwirkung unter der deklarierten Farbpipeline;
- physikalisch plausible Auflage, Reflexe, Verdeckung und Schattenrichtung;
- Hintergrund, Ausschnitt, Typografie und Aussagen, die durch das Briefing erlaubt sind; und
- Provenienz von Modell, Adapter, Prompt/Referenz und Ausgabe.

Dokumentieren Sie einen Grund für jede Ablehnung. Ein erneuter Lauf mit einem anderen
Seed ist keine Korrektur, solange die sachlichen Abnahmeprüfungen nicht bestanden sind.

## Modell- und Lizenzgrenze {#model-and-license-boundary}

Das [offizielle FLUX.2-Repository](https://github.com/black-forest-labs/flux2)
führt FLUX.2 [klein] 9B unter nicht-kommerziellen Bedingungen auf. Verwenden Sie
diese Gewichte nicht für kommerzielle Produktbilder ohne eine separate, aktuelle
Lizenzentscheidung. Hosted-API-Bedingungen, Adapter von Drittanbietern, Quell-Assets
und Produktmarken erfordern jeweils eine eigene Prüfung.

## Verwandte Seiten {#related-pages}

- [[flux-klein-9b-inference]]
- [[color-checker-and-white-balance]]
- [[perspective-calibration-for-compositing]]
- [[retouch-patch-harmonization]]
