---
title: "Wiederherstellung sichtbarer Wasserzeichen: Vertrag für autorisierte Assets"
description: "Die Wiederherstellung sichtbarer Wasserzeichen ist nur für Assets zulässig, die der Betreiber modifizieren darf. Eigentumsnachweis oder schriftliche Genehmigung, Quell-Asset und Overlay-Typ, Freigaben für Erkennung/Maske und Wiederherstellung, geschützte Bereiche und Provenienzbehandlung, Offenlegung der Ausgabe sowie menschliche Prüfung sind verbindlich festzulegen. Eine plausible Rekonstruktion darf niemals als wiederhergestelltes Originalinhalt behandelt werden."
category: techniques
tags: [watermark, restoration, authorized-assets, provenance, inpainting, review]
aliases: ["Visible Watermark Detection and Removal", "Authorized Watermark Restoration"]
level: 3
source_sha256: 3ab557ba07e42ed814eedd06888d0c8a84af36ef787f5f22385c412c11269ea3
translation: machine
translated_at: '2026-10-24'
---
# Wiederherstellung sichtbarer Wasserzeichen: Vertrag für autorisierte Assets {#visible-watermark-restoration-authorized-asset-contract}

Diese Seite betrifft die Wiederherstellung eines sichtbaren Overlays nur dann,
wenn der Betreiber das Asset besitzt oder ausdrücklich befugt ist, es zu
verändern, etwa bei der Korrektur eines versehentlichen Overlays auf einem
hauseigenen Export oder bei der Erstellung einer autorisierten Ableitung. Die
[AAAI-Forschung zu sichtbaren Wasserzeichen](https://ojs.aaai.org/index.php/AAAI/article/view/28080)
beschreibt die Trennung von Overlay-Lokalisierung und Hintergrundrekonstruktion.
Ein wiederhergestellter Bereich bleibt eine Rekonstruktion und kein
nachgewiesener Beleg dessen, was ursprünglich verdeckt war.

Dieser Workflow darf nicht verwendet werden, um Markierungen von Vorschauen
Dritter, lizenziertem Stock-Material, über Plattformen ausgelieferten Medien
oder jedem Asset zu entfernen, dessen Nutzungsbedingungen Veränderungen
untersagen. Er erstreckt sich auch nicht auf das Umgehen unsichtbarer
Wasserzeichen oder das Löschen von Provenienzkontrollen. [C2PA Content Credentials](https://spec.c2pa.org/specifications/)
sind ein eigenständiges Provenienzsystem und erfordern eine eigene,
richtlinienkonforme Behandlung.

## Autorisierung und Geltungsbereich festlegen {#establish-authorization-and-scope}

Vor der Verarbeitung sind folgende Angaben zu dokumentieren:

- Digest des Quell-Assets, Eigentümer, Lizenz-/Vertragsnachweis oder schriftliche
  Genehmigung, autorisierter Zweck, Ziel, Aufbewahrungs- und Löschrichtlinie
  sowie Prüfer;
- Klassifizierung des Overlays und Dokumentation seiner Platzierung: eigenes
  Export-Wasserzeichen, genehmigtes Herausgeberzeichen, versehentlicher
  Compositing-Artefakt oder ein anderer ausdrücklich zulässiger Fall;
- eine explizite Liste geschützter Bereiche für Personen, Identität, Text,
  Produkte, Sicherheitskennzeichnungen, sachliche Aufzeichnungen, rechtliche
  Hinweise und Inhalte, die nicht rekonstruiert oder verändert werden dürfen; und
- ein Ablehnungsprotokoll für Assets unbekannter Herkunft, Vorschauen Dritter
  oder Anfragen, die ohne Berechtigung Eigentums- oder Provenienznachweise
  entfernen würden.

Die Berechtigung, eine Kopie anzusehen, herunterzuladen oder zu bearbeiten,
ist keine Berechtigung, ein sichtbares Eigentumszeichen zu entfernen. Ist die
Befugnis unklar, ist sie einzuholen, oder stattdessen das saubere Originalasset
zu verwenden.

## Wiederherstellung und Offenlegung dokumentieren {#bind-restoration-and-disclosure}

Für jeden autorisierten Durchlauf sind die Quelle von Detektor und Maske sowie
deren Revision, das Koordinatensystem der Maske und die Korrekturen des Prüfers,
die Freigabe des Wiederherstellungsmodells oder Werkzeugs, die
Eingabevorverarbeitung, der Digest des Ausgabeartefakts und jeder veränderte
Bereich zu protokollieren. Original-Asset und Maske sind zusammen mit dem
Ergebnis aufzubewahren. Eine generierte Auffüllung darf nicht als
rekonstruierte Pixel, als authentischer Produktnachweis oder als unverändertes
Original dargestellt werden.

Die Abdeckung der Maske ist getrennt von der Qualität der Wiederherstellung zu
bewerten. Zu prüfen sind Ränder, halbtransparente Overlay-Kanten, Text,
wiederkehrende Muster, feine sachliche Details, Beleuchtung, Spiegelungen und
die umgebende Geometrie. Wird Training eingesetzt, sind Quell-Assets und
Ableitungen gruppenweise disjunkt auf Trainings-, Validierungs- und
Prüfmengen zu verteilen; die Evaluation erfolgt auf autorisierten
Held-out-Daten.

Eine Veröffentlichung erfolgt erst, nachdem ein Prüfer Autorisierung,
Behandlung geschützter Bereiche, Offenlegung der Ausgabe und vorgesehene
Verwendung bestätigt hat. Festzuhalten ist außerdem, ob Provenienzmetadaten
oder Content Credentials gemäß der anwendbaren Asset-Richtlinie erhalten,
neu erzeugt oder als ungültig markiert werden müssen. Dies ist keine
allgemeine Bereinigung von Metadaten.

## Fallstricke {#gotchas}

- **Problem:** Eine lizenzierte Vorschau wird als bearbeitbare Quelle behandelt,
  weil sie öffentlich sichtbar ist. -> **Lösung:** Vor jedem Wiederherstellungsversuch
  das Originalasset oder eine ausdrückliche schriftliche Berechtigung verlangen.
- **Problem:** Eine plausible Auffüllung wird als wiederhergestellter Originalinhalt
  dargestellt. -> **Lösung:** Als Wiederherstellung bzw. Rekonstruktion kennzeichnen,
  Quelle und Maske aufbewahren und sachliche oder beweisrelevante Verwendung ohne
  unabhängige Belege untersagen.
- **Problem:** Die Entfernung des Overlays verändert Provenienzerwartungen, während nur
  Pixel geprüft werden. -> **Lösung:** Die anwendbare Richtlinie zu
  Provenienz bzw. Content Credentials prüfen und ein sichtbares Protokoll der
  Veränderung erhalten.

## Abbruchgrenze {#failure-boundary}

Fehlen Eigentums- oder Autorisierungsnachweis, Quellprovenienz, zulässiger
Overlay-Geltungsbereich, Prüfung geschützter Bereiche, Freigabe der
Wiederherstellung oder die abschließende Offenlegung, wird das Ergebnis weder
verarbeitet noch veröffentlicht. Die Angelegenheit ist an den Asset-Eigentümer
zu eskalieren oder eine saubere, autorisierte Quelle anzufordern. Das Wasserzeichen
darf nicht stillschweigend gelöscht, zugeschnitten oder umgangen werden.

## Verwandte Seiten {#related-pages}

- [[object-removal-inpainting]]
- [[LaMa]]
- [[in-context-segmentation]]
- [[paired-training-for-restoration]]
- [[segmentation-dataset-preparation]]
