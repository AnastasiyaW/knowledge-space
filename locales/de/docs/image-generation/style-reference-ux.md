---
title: "Style-Referenz-UX: Autorität, Stärke und Herkunft"
description: "Die Style-Referenz-UX muss temporären Einfluss von dauerhaft gespeichertem Training, Stil von Inhalt und Struktur sowie lokale Daten von der Verarbeitung durch Dritte trennen und dabei Stärke und Herkunft für die Nutzerin bzw. den Nutzer sichtbar machen."
category: systems
tags: [style-reference, ux, provenance, privacy, lora, content-reference, strength-control]
aliases: ["Style Reference UX", "Style Reference Workflow"]
level: 2
source_sha256: c6f9b17c7801c58b9e2ea2f57a9db8ea7ada3c31dc9ae5f1fbbe705a01fa415d
translation: machine
translated_at: '2026-10-24'
---
# Style-Referenz-UX: Autorität, Stärke und Herkunft {#style-reference-ux-authority-strength-and-provenance}

Eine Style-Referenz-Steuerung verändert die visuelle Ausgabe, doch Nutzerinnen und Nutzer müssen verstehen,
was sie übernehmen kann, was sie erhält, wohin ihre Referenz gesendet wird und
ob die Auswahl temporär ist oder ein wiederverwendbares trainiertes Asset erzeugt. Diese
Sachverhalte sind Produktanforderungen und keine optionalen Hilfetexte.

## Die Absichten der Nutzerin bzw. des Nutzers trennen {#separate-the-users-intents}

Stellen Sie eigene Steuerelemente bereit für:

- **Stil:** Farbpalette, Textur, Stimmung, Medium und visuelle Sprache;
- **Inhalt:** Motiv, Objektidentität, Produktgeometrie und Szenenfakten;
- **Struktur:** Pose, Layout, Kamera bzw. Bildausschnitt oder räumliche Vorgaben; und
- **Erhaltung:** Referenzmerkmale, die eine Bearbeitung unverändert lassen muss.

Präsentieren Sie diese nicht als einen einzigen, unscharfen Regler für die „Referenzstärke“. Wenn ein
Workflow sie technisch nicht trennen kann, sagen Sie das ausdrücklich und zeigen Sie den
zu erwartenden Konflikt, statt den Eindruck zu erwecken, dass alle Referenzeigenschaften erhalten bleiben.

## Temporäre gegenüber dauerhaften Entscheidungen {#temporary-versus-durable-choices}

Bieten Sie zwei klar beschriftete Wege an:

1. **Sitzungsreferenz:** wird nur auf den aktuellen Auftrag angewendet und zusammen mit dem Auftragsdatensatz entfernt.
2. **Gespeicherter Stil oder trainierter Adapter:** ein dauerhaftes Asset mit Name, Eigentümer, Quelle/Herkunft, Modellbindung, Aufbewahrungsrichtlinie und Löschpfad.

Ein gespeicherter Stil darf niemals implizit aus einem Upload entstehen. Training,
Weitergabe oder Wiederverwendung erfordern eine eigene, ausdrückliche Handlung sowie einen sichtbaren Hinweis darauf,
welche Daten aufbewahrt werden.

## Stärkeregler, die Risiken kommunizieren {#strength-controls-that-communicate-risk}

Verwenden Sie einen umkehrbaren Stärkeregler mit allgemeinverständlichen Wirkungsbeschreibungen und einer Vorschau,
die mit der Baseline ohne Referenz vergleicht. Die Oberfläche sollte anzeigen, wann eine stärkere Stileinwirkung
die Erhaltung von Inhalt und Struktur schwächt. Vermeiden Sie den Eindruck, numerische Gewichte seien
über verschiedene Modelle, Adapter oder Bildreferenzen hinweg vergleichbar.

Bei komplexen Anfragen stellen Sie vor der Generierung eine explizite Konfliktübersicht bereit:
welche Quelle die Farbe bestimmt, welche die Komposition, welche die Objektfakten und
welche Priorität gilt, wenn sie sich widersprechen.

## Daten- und Anbietergrenze {#data-and-provider-boundary}

Bevor eine Referenz akzeptiert wird, legen Sie offen, ob sie lokal bleibt oder an einen Anbieter
für Captioning, Embedding, Generierung oder Training gesendet wird. Halten Sie Anbieter, Modell bzw. Revision,
Aufbewahrungs- und Zugriffsbedingungen sowie die Nutzungsbefugnis im Auftragsbeleg fest. Sensible Porträts,
Produkte unter NDA und fremde Kunstwerke erfordern eine ausdrückliche Entscheidung über die zulässige Nutzung.

## Abnahme und Wiederverwendung {#acceptance-and-reuse}

Zeigen Sie ein Quellenpanel mit Vorschaubildern bzw. Digests, Modell- und Adapterbindung,
Referenzumfang, Prompt, Ergebnis und Feedback. Nutzerbewertungen sind nützliche Präferenzsignale,
belegen aber keine Rechte, keine sachliche Produktgenauigkeit und keine Identitätserhaltung. Ein
wiederverwendbarer Adapter muss dem Freigabevertrag in [[flux-klein-style-lora-system]] folgen.

## Verwandte Seiten {#related-pages}

- [[flux-klein-style-lora-system]]
- [[megastyle-flux-style-transfer]]
- [[flux-klein-jewelry-photography]]
- [[face-beautify-edit-lora]]
