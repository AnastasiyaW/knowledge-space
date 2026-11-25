---
title: "Figma-Layout und Komponenten"
category: concepts
tags: [web-frontend, figma, autolayout, components, variants, design-system]
level: 3
source_sha256: ecb01c0f84a704918373d8ae62767efb5711365fa82b21df9a54b5ebaa892d34
translation: machine
translated_at: '2026-10-24'
---
# Figma-Layout und Komponenten {#figma-layout-and-components}

AutoLayout (Figmas Entsprechung zu Flexbox), Constraints für die Positionierung und Komponenten für wiederverwendbare Designelemente.

## AutoLayout {#autolayout}

Lässt Frames sich wie Flex-Container verhalten: Kindelemente ordnen sich an, verteilen sich und passen ihre Größe automatisch an.

**Erstellen**: Elemente auswählen -> Shift+A (oder im rechten Panel „+“ neben Auto Layout).

### Eigenschaften {#properties}
- **Richtung**: Horizontal (Zeile), Vertikal (Spalte), Umbruch
- **Gap**: Abstand zwischen den Kindelementen
- **Padding**: Innenabstand (einzeln oder einheitlich)
- **Ausrichtung**: 9-Punkte-Raster (oben links bis unten rechts)

### Größenverhalten {#resizing-behavior}

| Modus | Verhalten | CSS-Entsprechung |
|------|----------|----------------|
| Fixed | Feste Größe | `width: 200px` |
| Hug contents | Schrumpft auf den Inhalt | `width: fit-content` |
| Fill container | Füllt den Container aus | `flex: 1` / `width: 100%` |

### Abstandsmodi {#spacing-modes}
- **Packed**: Elemente gruppieren sich mit definiertem Gap (wie CSS `gap`)
- **Space between**: Elemente werden verteilt (wie `justify-content: space-between`)

### Verschachteltes AutoLayout (echte Layouts) {#nested-autolayout-real-layouts}
```text
Page (vertical)
  ├── Header (horizontal)
  │     ├── Logo (fixed)
  │     ├── Nav (horizontal, gap: 24)
  │     └── CTA (fixed)
  ├── Hero (vertical, fill)
  └── Cards (horizontal, wrap)
        ├── Card 1 (vertical, fill)
        └── Card 2 (vertical, fill)
```

Spiegelt die HTML/CSS-Struktur wider und erleichtert so die Übergabe an Entwickler.

### Min/Max-Constraints {#minmax-constraints}
Elementeigenschaften -> „...“ unter W/H für Min-/Max-Breite bzw. -Höhe. Entscheidend für das responsive Verhalten.

### Absolute Positionierung {#absolute-positioning}
„Absolute position“ beim Kindelement aktivieren, um es vom AutoLayout-Fluss auszunehmen. Vergleichbar mit `position: absolute` innerhalb von `position: relative`.

### Tipps {#tips}
1. Von innen nach außen aufbauen: zuerst die kleinsten Elemente, dann in größere AutoLayouts einpacken
2. Fill für flexible Bereiche, Hug für natürliche Größen (Buttons, Tags)
3. 8px-Raster: Abstände von 8, 16, 24, 32, 40, 48px
4. Frames aussagekräftig benennen (Entwickler lesen die Namen)

## Constraints {#constraints}

Für Elemente mit fester Position innerhalb von Frames ohne AutoLayout. Steuern das Größenverhalten.

| Horizontal | Verhalten |
|-----------|----------|
| Left | Von links fixiert |
| Right | Von rechts fixiert |
| Left and Right | Dehnt sich |
| Center | Zentriert |
| Scale | Proportional |

Vertikal gelten dieselben Optionen (Top, Bottom usw.).

**Constraints vs. AutoLayout**: AutoLayout für 90 % der Layouts (flussbasiert). Constraints für Sonderfälle (schwebende, überlappende Elemente).

## Komponenten {#components}

Wiederverwendbare Elemente. Ändert man die Hauptkomponente, aktualisieren sich alle Instanzen.

### Erstellen {#creating}
1. Element(e) auswählen
2. Ctrl+Alt+K -> Komponente wird erstellt (lila Raute)
3. Mit Schrägstrich benennen: `button/primary`, `button/secondary`

### Hauptkomponente vs. Instanz {#main-vs-instance}
- **Hauptkomponente** (lila Raute): Quelldefinition
- **Instanz** (nicht ausgefüllte Raute): verknüpfte Kopie
- Instanzen können überschrieben werden: Text, Füllung, Sichtbarkeit von Kindelementen
- Instanz lösen (Rechtsklick), um die Verknüpfung aufzuheben

## Varianten {#variants}

Zusammengehörige Komponentenzustände in einem Komponentenset gruppieren.

### Eigenschaften {#properties_1}
| Eigenschaft | Werte | Verwendung |
|----------|--------|-----|
| State | default, hover, pressed, disabled | Interaktion |
| Size | sm, md, lg | Responsiv |
| Type | primary, secondary, ghost | Visuell |
| Icon | true, false | Mit/ohne |

Benennung: `Button/Size=md, Type=primary, State=default`

### Komponenteneigenschaften {#component-properties}
- **Boolean**: Kindelement ein-/ausblenden
- **Instance swap**: verschachtelte Komponente ersetzen
- **Text**: editierbaren Text freigeben

## Design-System-Seite {#design-system-page}

Eigene Seite, die alle Designentscheidungen dokumentiert:
1. Farbpalette (Farbfelder mit Hex-Werten)
2. Typografie-Skala (alle Überschriften- und Fließtextgrößen)
3. Abstandsskala (8px-Raster)
4. Komponentenbibliothek (Buttons, Eingabefelder, Karten)
5. Icon-Set
6. Rastervorgaben

### Styles-System {#styles-system}
```text
Color styles:  primary/500, neutral/100, accent/success
Text styles:   heading/h1, heading/h2, body/regular
Effect styles: shadow/sm, shadow/md, blur/glass
Grid styles:   reusable grid configurations
```

Der Schrägstrich erzeugt eine Ordnerhierarchie. Ändert man die Style-Definition, aktualisieren sich alle Instanzen.

## Dateiorganisation {#file-organization}

| Seite | Inhalt |
|------|----------|
| Cover | Projektvorschaubild (1920x960) |
| Design System | Styles, Farben, Typografie, Komponenten |
| Wireframes | Layouts mit niedriger Detailtreue |
| Desktop | Desktop-Ansicht mit hoher Detailtreue |
| Mobile | Mobile-Ansicht mit hoher Detailtreue |
| Prototype | Verbundene Bildschirme |

## Stolpersteine {#gotchas}

- **Constraints werden im AutoLayout ignoriert**: AutoLayout steuert die Positionierung aller Kindelemente
- **Benennung von Varianten**: muss exakt im Format `Property=Value` mit Kommas erfolgen
- **Fill container nur im AutoLayout**: kann nicht bei Kindelementen von Frames ohne AutoLayout verwendet werden
- **Komponentenhierarchie**: keine Element-von-Element-Benennung; flach halten
- **Gelöste Instanzen**: verlieren jede Verbindung zur Hauptkomponente; können nicht wieder angebunden werden

## Siehe auch {#see-also}

- [[figma-fundamentals]] - Oberfläche, Frames, Export
- [[figma-design-workflow]] - Typografie, Prototyping, Responsive Design
- [[css-flexbox]] - CSS-Umsetzung der AutoLayout-Konzepte
- [[css-responsive-design]] - Breakpoints und adaptives Design
