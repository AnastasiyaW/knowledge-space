---
title: "Figma-Design-Workflow"
category: concepts
tags: [web-frontend, figma, typography, color, prototyping, responsive]
level: 3
source_sha256: aef298d42b151b49fb52b9b2174e163bc5404cc8e871ef31f307750d127f6e77
translation: machine
translated_at: '2026-10-24'
---
# Figma-Design-Workflow {#figma-design-workflow}

Typografie, Farbtheorie, Effekte, Prototyping und Workflow für responsives Design in Figma.

## Typografie {#typography}

### Schriftklassifikation {#font-classification}
- **Serifenschrift** (Times, Playfair): klassisch, formell - Überschriften im Luxus-/Editorial-Bereich
- **Serifenlose Schrift** (Roboto, Inter, Open Sans): klar, modern - Standard für Fließtext im Web
- **Nichtproportionale Schrift** (Fira Code): ausschließlich für Codeblöcke
- **Display/Schreibschrift**: nur für Überschriften oder Akzente, niemals für Fließtext

### Typografische Skala {#typography-scale}

| Element | Größe | Gewicht | Zeilenhöhe |
|---------|-------|---------|------------|
| H1 | 48-64px | Bold 700 | 110-120% |
| H2 | 36-48px | Bold 700 | 120-130% |
| H3 | 24-32px | SemiBold 600 | 120-130% |
| Body | 16-18px | Regular 400 | 150-160% |
| Caption | 12-14px | Regular 400 | 140-150% |
| Button | 14-16px | Medium 500 | 100% |

### Regeln {#rules}
- Maximal 2 Schriftfamilien pro Projekt
- 45-75 Zeichen pro Zeile für gute Lesbarkeit
- Mindestens 14px im Web, 16px für Fließtext empfohlen
- Großbuchstaben: nur für kurze Labels, Buchstabenabstand um 2-5% erhöhen

## 8px-Abstandsraster {#8px-spacing-grid}

Alle Abstände sind Vielfache von 8: 8, 16, 24, 32, 40, 48, 64, 80px. Ein 4px-Subraster für feine Anpassungen.

| Kontext | Typische Werte |
|---------|---------------|
| Seitenränder (mobil) | 16-24px |
| Seitenränder (Desktop) | 80-120px |
| Abschnittsabstand (Padding) | 64-120px |
| Karten-Padding | 16-32px |
| Abstand zwischen Karten | 16-32px |
| Button-Padding | 12-16px vertikal, 24-32px horizontal |

## Farbe {#color}

### HSB-Modell {#hsb-model}
- **H** (Hue/Farbton): 0-360 Farbkreis
- **S** (Saturation/Sättigung): 0-100% (von Grau bis leuchtend)
- **B** (Brightness/Helligkeit): 0-100% (von Schwarz bis volle Helligkeit)

### Aufbau einer Palette {#building-a-palette}
1. **Primär**: Markenfarbe (CTAs, Links)
2. **Sekundär**: komplementär
3. **Neutraltöne**: 5-7 Graustufen
4. **Semantisch**: Erfolg/Fehler/Warnung/Info

### 60-30-10-Regel {#60-30-10-rule}
- 60% dominant (meist neutral/weiß)
- 30% sekundär (Abschnitte, Karten)
- 10% Akzent (CTAs, Hervorhebungen)

### Kontrast {#contrast}
Mindestens 4,5:1 für Fließtext, 3:1 für große Schrift (WCAG AA). Zur Überprüfung die Plugins Stark/Contrast verwenden.

## Effekte {#effects}

### Schlagschatten {#drop-shadow}
Üblich: `X:0 Y:4 Blur:12 Color:#000 at 10-15%`. Mehrere Schatten können übereinandergelegt werden.

### Hintergrundunschärfe (Glassmorphism) {#background-blur-glassmorphism}
Hintergrundunschärfe 10-20px + Füllung #FFF mit 30-60% Deckkraft.

### Füllmethoden (Blend Modes) {#blend-modes}
Multiply (abdunkeln), Screen (aufhellen), Overlay (Kontrast). Für die Tonung von Bildern verwenden.

### Masken {#masks}
Form über dem Bild platzieren -> beide auswählen -> "Use as mask" (Ctrl+Alt+M). Die Form definiert den sichtbaren Bereich.

## Prototyping {#prototyping}

### Verbindungen {#connections}
1. Auslösendes Element auswählen (Button, Karte)
2. Blauen Kreis zum Zielframe ziehen
3. Konfigurieren: Auslöser, Aktion, Animation, Dauer, Easing

### Übergangstypen {#transition-types}
- **Instant**: keine Animation
- **Dissolve**: Überblendung
- **Smart Animate**: interpoliert übereinstimmende Ebenen (gleicher Name erforderlich)
- **Move/Push/Slide**: gerichtete Übergänge

### Smart Animate {#smart-animate}
1. Frame A erstellen (Startzustand)
2. Duplizieren -> in Frame B ändern (Position, Größe, Farbe, Deckkraft)
3. A->B mit Smart Animate verbinden
4. Ebenen MÜSSEN identische Namen haben, um zugeordnet zu werden

Interpoliert werden: Position, Größe, Rotation, Deckkraft, Füllung, Eckradius, Kontur.

### Overlays {#overlays}
Auslöser -> "Open overlay" verbinden -> Overlay-Frame auswählen. Position, Hintergrundabdunklung und Schließen bei Klick konfigurieren.

### Interaktive Komponenten {#interactive-components}
Interaktionen INNERHALB der Komponentenvarianten definieren (Hover, Press). Jede Instanz übernimmt sie automatisch.

### Dauer-Richtwerte {#duration-guidelines}
| Animation | Dauer |
|-----------|-------|
| Button-Zustand | 100-200ms |
| Tooltip | 150-200ms |
| Modal | 200-300ms |
| Seitenübergang | 300-500ms |

### Easing {#easing}
- **Ease out**: einblendende Elemente (am häufigsten)
- **Ease in**: ausblendende Elemente
- **Ease in-out**: Elemente, die sich innerhalb des sichtbaren Bereichs bewegen
- Material Design: `cubic-bezier(0.4, 0.0, 0.2, 1.0)`

## Workflow für responsives Design {#responsive-design-workflow}

### Breakpoints {#breakpoints}
Mindestens 3 Größen gestalten: Mobil (375px), Tablet (768px), Desktop (1440px).

### Anpassungsmuster {#adaptation-patterns}
1. **Umfluss (Reflow)**: horizontal -> vertikaler Stapel
2. **Ausblenden (Hide)**: unwesentliche Elemente auf kleinen Bildschirmen entfernen
3. **Skalieren (Resize)**: Schriften und Abstände proportional verkleinern
4. **Ersetzen (Replace)**: Hamburger-Menü ersetzt horizontale Navigation

### Vorgehen {#process}
1. Zuerst Desktop (mehr Platz für die Planung des Layouts)
2. Duplizieren -> auf Tablet skalieren -> anpassen
3. Duplizieren -> auf Mobil skalieren -> anpassen
4. Komponenten über alle Breakpoints hinweg konsistent halten

### Export für Retina {#export-for-retina}
- 1x (Standard), 2x (Retina), 3x (iPhone Plus/Max)
- SVG benötigt keine mehrfachen Exporte (Vektor)

## Gestaltungsprinzipien {#design-principles}

- **Weißraum**: mehr = hochwertige Wirkung; weniger = informationsdicht
- **Nähe**: zusammengehörige Elemente eng, unzusammenhängende weit auseinander
- **Wiederholung**: konsistente Stile für Elemente derselben Ebene
- **Kontrast**: Unterschiede in Größe, Gewicht, Farbe und Abstand erzeugen Hierarchie
- **Ausrichtung**: gemeinsame Achsen schaffen Ordnung

## Wireframes {#wireframes}

Strukturplanung in niedriger Detailtiefe: Graustufen, einfache Rechtecke, grundlegender Text. Vor dem Investieren in hohe Detailtiefe mit Stakeholdern testen.

## Wesentliche Plugins {#essential-plugins}

| Plugin | Zweck |
|--------|-------|
| Iconify | 100k+ Icons |
| Unsplash | Stockfotos |
| Contrast/Stark | Prüfung der Barrierefreiheit |
| Content Reel | Platzhalterdaten |

## Stolperfallen {#gotchas}

- **Smart-Animate-Namensabweichung**: Ebenen mit unterschiedlichen Namen werden überblendet statt interpoliert
- **Overlay ohne Schließen**: Nutzer bleiben hängen; immer Schließen bei Klick außerhalb aktivieren
- **Zu viele Schriften**: mehr als 2 Familien erzeugen visuelles Chaos
- **Kontrast ignorieren**: schön, aber unlesbarer Text scheitert an der Barrierefreiheit
- **Denken in statischen Mockups**: wer das Größenverhalten nicht früh testet, erhält nicht responsive Designs

## Siehe auch {#see-also}

- [[figma-fundamentals]] - Oberfläche, Frames, Export
- [[figma-layout-and-components]] - AutoLayout, Komponenten, Varianten
- [[css-animation-and-transforms]] - Umsetzung der gestalteten Animationen
- [[css-responsive-design]] - CSS-Media-Queries für Breakpoints
