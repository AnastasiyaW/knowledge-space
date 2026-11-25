---
title: "Farbtheorie für Datenvisualisierung"
category: concepts
tags: [bi-analytics, color, visualization, accessibility, palette, colorbrewer]
level: 3
source_sha256: 1efdcd80899fa0afa92f67ad75627755778d3d60e25dfc715def7f2c2c85b6fd
translation: machine
translated_at: '2026-10-24'
---
# Farbtheorie für Datenvisualisierung {#color-theory-for-data-visualization}

Farbe ist eines der wirkungsvollsten und zugleich am häufigsten falsch eingesetzten Kodierungsattribute in der Datenvisualisierung. Eine sachgerechte Verwendung von Farbskalen, Barrierefreiheit und konsistente Farbsemantik über alle Dashboards hinweg wirken sich deutlich auf Lesbarkeit und Vertrauenswürdigkeit aus.

## Wichtige Fakten {#key-facts}

- Drei Farbskalentypen: kategorisch, sequenziell, divergierend
- Maximal 5–7 Farben pro Dashboard – mehr Farben bedeuten, dass sich Zuordnungen nicht mehr merken lassen
- Eine Farbe = eine Entität über alle Diagramme eines Dashboards hinweg
- Grau ist die Standard-Grundfarbe; Farbe nur dort hinzufügen, wo sie dem Nutzer hilft
- Sicherer Standard bei Unsicherheit: Blau, Grau und deren Abstufungen
- Gedeckte Töne statt grelle Farben: Sättigung und Helligkeit reduzieren
- Übliche Assoziationen: Grün = gut, Rot = schlecht

## Muster {#patterns}

### Farbskalentypen {#color-scale-types}

| Typ | Anwendungsfall | Regeln |
|------|----------|-------|
| **Kategorisch** | Gruppen/Kategorien unterscheiden | Keine Ordnungsbeziehung; maximal 5–7 Farben; alle mit gleichem visuellen Gewicht |
| **Sequenziell** | Numerische Werte kodieren | Eine Grundfarbe + Verlauf; hell = weniger, dunkel = mehr |
| **Divergierend** | Abweichungen von 0/Mittelwert zeigen | Zwei polare Farben; Verlauf über neutrales Grau; Rot-Grün für gut-schlecht, Blau-Orange für Abweichungen |

### Farbinterpolation {#color-interpolation}

Interpolation = Zuordnung von Farbabstufungen zu bestimmten numerischen Werten. Eine falsche Interpolation macht Diagramme irreführend. Heatmaps und Karten immer auf korrekte Interpolation in Tableau prüfen.

### Benutzerdefinierte Palette in Tableau {#custom-palette-in-tableau}

Hinzufügen zu: `My Tableau Repository/Preferences.tps`

Palettentypen:
- `regular` = kategorische Palette
- `sequential` = kontinuierlicher Verlauf
- `diverging` = Verlauf mit zwei Polen

### Farbenblindheitsfreundliche Ressourcen {#color-blind-safe-resources}

- **ColorBrewer** (colorbrewer2.org) – der Goldstandard für kartografische und Datenpaletten
- **DataColorPicker** – erzeugt Paletten mit wahrnehmungsgleichmäßigen Abständen
- **Coolors** – Palettengenerator mit Barrierefreiheitsprüfung
- **Paletton** – Palettengestaltung auf Basis des Farbkreises

### Farb-Checkliste {#color-checklist}

1. Vor Beginn eine Farbpalette festlegen
2. Eine Farbe = eine Entität, konsistent über alle Diagramme
3. Doppelte Kodierung (Farbe + Größe) ist zulässig, aber oft unnötig
4. Großflächige Diagramme → Pastellfarben verwenden (geringere Sättigung)
5. Grau als primäre Grundfarbe
6. Auf Farbenblindheit-Barrierefreiheit testen
7. Dunkler Text auf hellem Hintergrund (Kontrast prüfen)

### Farbe in Power BI {#color-in-power-bi}

Benutzerdefinierte Designs ermöglichen volle Farbkontrolle über JSON:
```json
{
  "name": "MyTheme",
  "dataColors": ["#118DFF", "#12239E", "..."],
  "background": "#FFFFFF",
  "foreground": "#252423",
  "tableAccent": "#118DFF"
}
```

Anwenden über: Ansicht -> Designs -> Designs durchsuchen.

### Bedingte Farbe in DAX {#conditional-color-in-dax}

```dax
KPI Color =
IF([Actual] >= [Target], "#28A745", "#DC3545")
```

Anwenden in: Visualisierungen -> Wertfeld -> Bedingte Formatierung -> Feldwert.

## Fallstricke {#gotchas}

- Die Kombination Rot-Grün ist für farbenblinde Nutzer am ungünstigsten (etwa 8 % der Männer) – stattdessen Blau-Orange oder Blau-Rot verwenden
- Sequenzielle Skalen mit zu ähnlichen Abstufungen werden im Druck unlesbar
- Grelle, gesättigte Farben erzeugen visuelle Ermüdung auf datenintensiven Dashboards
- Farben, die auf einem Monitor „herausstechen“, können bei Projektion verblassen – in der Präsentationsumgebung testen
- Dieselbe Farbe für verschiedene Entitäten über Diagramme hinweg zu verwenden, zerstört die visuelle Sprache des Dashboards

## Siehe auch {#see-also}

- [[dashboard-design-patterns]] – Layout und visuelle Hierarchie
- [[tableau-chart-types]] – Kodierungsattribute und Diagrammauswahl
- [[powerbi-advanced-features]] – Power-BI-Designs und bedingte Formatierung
