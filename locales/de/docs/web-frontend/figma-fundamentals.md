---
title: "Figma-Grundlagen"
category: concepts
tags: [web-frontend, figma, design, ui-design]
level: 2
source_sha256: cf16b35e3bc6cef1cb41897029ededf62782b7b271569803f3cb494fc7ef9e8b
translation: machine
translated_at: '2026-10-24'
---
# Figma-Grundlagen {#figma-fundamentals}

Figma ist ein kollaboratives Design-Tool für UI/UX. Funktioniert im Browser oder als Desktop-App (identische Funktionalität). Die kostenlose Version reicht zum Lernen aus.

## Oberfläche {#interface}

- **Linkes Panel**: Ebenen-Baum (Hierarchie)
- **Mitte**: unendliche Arbeitsfläche (Canvas)
- **Rechtes Panel**: Eigenschaften (Abmessungen, Farben, Effekte)
- **Obere Werkzeugleiste**: Werkzeuge (Frame, Form, Stift, Text)

### Navigation {#navigation}
| Aktion | Tastenkürzel |
|--------|--------------|
| Zoomen | Strg+Scrollen |
| Verschieben | Leertaste+Ziehen |
| Alles anzeigen | Strg+1 |
| Zoom 100 % | Strg+0 |
| Auswahl zoomen | Umschalt+1 |
| Raster ein-/ausblenden | Strg+Umschalt+4 |

## Frames {#frames}

Primäre Container, die Bildschirmgrenzen definieren. Entsprechen Artboards in anderen Tools.

| Gerät | Breite |
|--------|-------|
| Desktop | 1440px |
| Laptop | 1280px |
| Tablet | 768px |
| Mobil | 375px |

- Frames können verschachtelt werden (Frame in Frame für Abschnitte)
- „Inhalt beschneiden“ steuert die Sichtbarkeit von Überläufen
- Beim Ziehen an den Frame-Kanten Strg gedrückt halten, um die Größe zu ändern, ohne die untergeordneten Elemente zu skalieren

## Rastersystem {#grid-system}

Frame auswählen -> Layout-Raster -> „+“ -> Spalten:
- **Anzahl**: 12 (Standard für Web, teilbar durch 2/3/4/6)
- **Typ**: Dehnen (skaliert mit dem Frame)
- **Rand**: 80–120px (Desktop)
- **Zwischenraum (Gutter)**: 20–30px

Mehrere Raster können übereinandergelegt werden (Spalten + Zeilen + Grundlinie).

## Ebenen und Auswahl {#layers-and-selection}

- Oben im Panel = vorne auf der Arbeitsfläche (Z-Reihenfolge)
- **Gruppe** (Strg+G): visuelle Gruppierung, kein Beschneiden, keine eigene Größe
- **Frame** (Strg+Alt+G): Container mit Beschneidung, eigenen Abmessungen, unterstützt AutoLayout
- Klick = oberste Ebene; Doppelklick = in die Gruppe hineinwechseln; Strg+Klick = Tiefenauswahl

## Formen und boolesche Operationen {#shapes-and-boolean-operations}

Integriert: Rechteck (R), Ellipse (O), Linie (L), Polygon, Stern.
- Umschalt halten = eingeschränkt (Quadrat/Kreis)
- Alt halten = vom Mittelpunkt aus zeichnen

**Boolesche Operationen** (2 oder mehr Formen auswählen): Vereinigen, Subtrahieren, Schnittmenge, Ausschließen. Standardmäßig nicht destruktiv; Reduzieren (Strg+E) macht sie dauerhaft.

## Stiftwerkzeug (P) {#pen-tool-p}

- Klick = gerader Ankerpunkt
- Klick+Ziehen = gekrümmt (Bézier-Griffe)
- Pfad schließen, indem der erste Punkt angeklickt wird
- Doppelklick auf den Pfad, um Punkte zu bearbeiten

## Text {#text}

- Taste T, Klick für automatische Breite, Klick+Ziehen für feste Breite
- Eigenschaften: Schriftart, Gewicht, Größe, Zeilenhöhe, Buchstabenabstand

## Export {#export}

- Element auswählen -> Abschnitt Export -> „+“
- **SVG**: Icons, Logos (Vektor, skaliert verlustfrei)
- **PNG**: Grafiken mit Transparenz
- **JPG**: Fotos
- Skalierungen: 1x, 2x, 3x für Retina

## Teilen {#sharing}

- Schaltfläche „Teilen“ -> Link kopieren
- Berechtigungen: „kann anzeigen“ oder „kann bearbeiten“
- „In deine Entwürfe duplizieren“ für eine bearbeitbare Kopie

## Frames vs. Gruppen {#frames-vs-groups}

| Merkmal | Frame | Gruppe |
|---------|-------|-------|
| Beschneidet Inhalt | Ja | Nein |
| Eigene Abmessungen | Ja | Nein |
| AutoLayout | Ja | Nein |
| Füllung/Kontur | Ja | Nein |
| CSS-Entsprechung | `<div>` | Visuelle Gruppierung |

**Regel**: Frames für Layout-Container (entsprechen HTML). Gruppen für temporäre visuelle Gruppierung.

## Fallstricke {#gotchas}

- **Raster ist nur visuell**: erzwingt kein Layout; Elemente müssen manuell positioniert werden
- **Verwechslung Gruppe vs. Frame**: Frame verwenden, wenn Beschneiden, Größenangaben oder AutoLayout nötig sind
- **Lokale Schriften im Browser**: erfordern das Plugin Figma Font Helper; die Desktop-App lädt lokale Schriften
- **Duplizieren in Entwürfe**: Der Eigentümer des Originallinks steuert den Zugriff; für bearbeitbare Arbeiten immer duplizieren

## Siehe auch {#see-also}

- [[figma-layout-and-components]] - AutoLayout, Constraints, Komponenten, Varianten
- [[figma-design-workflow]] - Typografie, Farbe, Prototyping
- [[css-grid]] - CSS-Umsetzung der Figma-Rasterkonzepte
