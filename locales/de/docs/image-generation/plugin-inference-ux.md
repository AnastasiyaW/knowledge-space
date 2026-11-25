---
title: "ML-Plugin-Inferenz-UX: Vertrag zum Host-Zustand"
description: "ML-Plugin-Inferenz-UX ist ein explizites Vertragsmodell für Host- und Job-Zustand: Host-API festlegen, Snapshot- und Modellversionen dokumentieren, Abbruch- und Fortschrittsverhalten, Cache- und Invalidierungsschlüssel, Herkunft der Vorschau, nicht-destruktives Commit und gemessene Latenz statt eines Versprechens universeller Reaktionsfähigkeit."
category: techniques
tags: [plugin, inference, ux, caching, progress, cancellation, non-destructive, evidence]
aliases: ["ML Plugin Inference UX Patterns", "Inference UX"]
level: 3
source_sha256: e25834384a052289dec26ba5e95a898ceaf29446e54616c1076d05fbf71f8900
translation: machine
translated_at: '2026-10-24'
---
# ML-Plugin-Inferenz-UX: Vertrag zum Host-Zustand {#ml-plugin-inference-ux-host-state-contract}

Eine ML-Operation in einem kreativen Host ist ein Job mit Dokument-, Modell- und Host-Zustand. Ein Spinner, ein gecachtes Ergebnis oder eine Vorschau ist nur dann vertrauenswürdig, wenn der Nutzer erkennen kann, welchen Quell-Snapshot sie repräsentiert, ob sie abgebrochen werden kann und was beim Commit geändert wird. Versprechen Sie keinen universellen Latenzwert. Messen Sie stattdessen das konkrete Modell, Gerät, die Dokumentklasse, den Kalt-/Warmzustand und die Host-Version.

## Beobachtbare Job-Zustände definieren {#define-observable-job-states}

Verwenden Sie ein Zustandsmodell, dessen Übergänge sichtbar und nachvollziehbar sind:

`Draft → queued → snapshot verified → preprocessing → inference → preview ready
→ user accepts → atomic non-destructive commit`

Alternative Endzustände sind `cancelled`, `invalidated`, `failed` und `review required`. Eine Dokumentbearbeitung, eine Parameteränderung, eine Modelländerung, eine Berechtigungsänderung oder eine Quellabweichung muss abhängige Vorschauen invalidieren, statt sie später stillschweigend anzuwenden.

Speichern Sie für jeden Job die Quelldigest- bzw. Composite-Richtlinie, die Dokument- und Ebenenversion, den Farb-, Orientierungs- und Auswahlzustand, Modell-, Checkpoint- und Runtime-Version, die Parameter, die Hardware- bzw. Provider-Grenze, Zeitstempel, den Ergebnis-Digest und den Endzustand.

## Die Host-Grenze respektieren {#respect-the-host-boundary}

Host-APIs bestimmen, wie Dokumentmutation, Verlauf, Abbruch und Fortschritt funktionieren. In Photoshop UXP erfordern dokumentverändernde Befehle [`executeAsModal`](https://developer.adobe.com/photoshop/uxp/ps_reference). Die [Modal-Ausführungs-API](https://developer.adobe.com/photoshop/uxp/2022/ps-reference/media/executeasmodal) stellt Abbruch und Fortschrittsmeldungen bereit. Diese Eigenschaften berechtigen ein Plugin jedoch nicht, während einer Remote-Inferenz einen Modal-Bereich zu halten, und nicht, ein Ergebnis anzuwenden, nachdem sich die Quelle geändert hat.

Führen Sie sichere Vorbereitungsschritte aus, bevor Sie exklusiven Mutationszugriff anfordern, sofern der Host dies erlaubt. Verwenden Sie die engste dokumentierte Host-Transaktion erst für das geprüfte, explizite Commit. Erhalten Sie die Undo-/Verlaufssemantik und lassen Sie die Originaldaten unverändert.

## Nur nachvollziehbare Zwischenergebnisse cachen {#cache-only-attributable-intermediates}

Ein Cache-Schlüssel sollte jede Eingabe enthalten, die das Ergebnis ändern kann: Quellpixel oder unveränderlicher Composite-Digest, Abmessungen, Zuschnitt und Orientierung, Farbraum, ausgewählter Bereich bzw. Maske, Version der Vorverarbeitung, Modell/Checkpoint/Runtime, Parameter und Provider-Richtlinie. Speichern Sie die Ausgabeherkunft zusammen mit dem Cache-Eintrag. Ein Dateiname, eine ID des aktiven Dokuments oder eine partielle Pixelstichprobe reicht nicht aus.

Legen Sie Eigentümerschaft, Verschlüsselung und Aufbewahrung, Größenbudget, Verdrängung und Invalidierung fest. Verwenden Sie ein Zwischenergebnis niemals dokumentübergreifend oder nutzerübergreifend, nur weil es ähnlich aussieht. Prefetching ist optionale Arbeit: Geben Sie ihm ein Budget, einen Abbruchpfad und eine explizite lokale/remote Richtlinie. Es darf keine Quellinhalte hochladen und kein Remote-Kontingent ohne Autorisierung verbrauchen.

## Vorschauen ehrlich gestalten {#make-previews-honest}

Kennzeichnen Sie eine Vorschau, die entwurfsartig, gekachelt, heruntergerechnet, überblendet, veraltet oder approximativ ist, mit der Eigenschaft, die ihr fehlt. Ein Schieberegler, der Quelle und Ausgabe überblendet, ist eine Darstellungsnäherung, sofern das Modell nicht tatsächlich bei dieser Einstellung ausgewertet wurde. Zeigen Sie die Zuordnung von Quelle und Ergebnis an und bieten Sie eine explizite Aktualisierung an, wenn sich Parameter oder Quellzustand unterscheiden.

Vergleichen Sie vor dem Commit die übernommene Ausgabe mit dem aufgezeichneten Snapshot und prüfen Sie Ausgabeabmessungen, Alpha-/Maskenrichtlinie, Farbkonvertierung, geschützte Bereiche und die Modellherkunft. Schlägt eine Bedingung fehl, behalten Sie die Vorschau als nicht übernommen bei und melden Sie den Grund.

## Die behauptete Nutzererfahrung messen {#measure-the-claimed-experience}

Berichten Sie für das tatsächliche Release Latenzverteilungen für Kalt- und Warmstart, Warteschlangenverzögerung, Reaktionszeit beim Abbruch, Abweichung zwischen Vorschau und finalem Ergebnis, Cache-Trefferquote, Speicherdruck, Fehlerrate und das Wiederherstellungsverhalten des Hosts. Testen Sie große Dokumente, schnelle Parameteränderungen, Undo/Redo, Quellbearbeitungen während der Warteschlange, Umordnung der Warteschlange, Offline- bzw. Provider-Ausfälle und gleichzeitige Host-Aktionen.

Ersetzen Sie einen Fehler nicht durch ein anderes Modell, einen anderen Cache-Eintrag, einen Cloud-Dienst oder ein veraltetes Ergebnis. Der Fallback muss explizit benannt, für die angeforderte Operation gleichwertig und für den Nutzer sichtbar sein.

## Verwandte Seiten {#related-pages}

- [[tiled-inference]]
- [[low-vram-inference-strategies]]
- [[frequency-decomposition-editing]]
- [[diffusion-lora-training]]
