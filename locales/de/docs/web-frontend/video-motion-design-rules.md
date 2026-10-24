---
title: "Regeln für Video- und Motion-Design"
description: "Konkrete Werte für Timing, Easing, Audiopegel, Komposition und Storytelling in Produktvideos und Motion Graphics."
level: 4
source_sha256: 8f3ccfecf037945120c3f8a345b3a23698345fe3338df0e347e9fdc39c21649d
translation: machine
translated_at: '2026-10-24'
---
# Regeln für Video- und Motion-Design {#video-motion-design-rules}

Referenz für produktionsreife Motion Graphics, Produktvideos und animierte Präsentationen. Alle Werte sind konkret und umsetzbar.

## Animation-Timing {#animation-timing}

### Dauer nach Elementgewicht {#duration-by-element-weight}

| Element | Dauer | Frames @30fps | Beispiel |
|---------|-------|---------------|----------|
| Mikro (Icon, Punkt) | 150-200ms | 5-6 | Toggle, Checkbox |
| Klein (Button, Badge) | 200-300ms | 6-9 | Hover-Zustand, Tooltip |
| Mittel (Karte, Text) | 300-500ms | 9-15 | Panel-Slide, Dropdown |
| Groß (Panel, Bild) | 400-700ms | 12-21 | Modal öffnen |
| Hero (Produkt, Szene) | 600-1200ms | 18-36 | Produkt-Reveal |
| Cinematic (Hintergrund) | 800-1500ms | 24-45 | Ambient-Übergänge |

**Regel:** UI-Animationen bleiben unter 300ms. 180ms wirken reaktionsschneller als 400ms (empirisch).

### Material Design 3 Duration-Tokens {#material-design-3-duration-tokens}

| Token | Wert | Wann |
|-------|------|------|
| short1 | 50ms | Mikro-Feedback |
| short4 | 200ms | Standardinteraktionen |
| medium2 | 300ms | Standardübergänge |
| medium4 | 400ms | Komplexe Übergänge |
| long2 | 500ms | Navigationsübergänge |
| long4 | 600ms | Aufwendige Übergänge |
| extraLong1-4 | 700-1000ms | Dramatisch (selten) |

### Richtwerte für Szenendauer {#scene-duration-guidelines}

| Szenentyp | Dauer |
|-----------|-------|
| Hook/Opener | 3-5s |
| Hero-Statistik ("2x schneller") | 4-6s |
| Feature-Showcase | 5-8s |
| Produkt-Beauty-Shot | 3-5s |
| Testimonial/Zitat | 4-6s |
| CTA/Abschluss | 4-6s |
| Schnelle Montage | je 2-3s |

**Rhythmus eines 60-Sekunden-Videos:**
```text
[0-5s]   Hook: bold statement, dark bg        — FAST
[5-15s]  Problem: 2-3 quick cuts              — MEDIUM
[15-25s] Solution reveal: product appears     — SLOW
[25-40s] Features: 3-4 staggered              — MEDIUM
[40-50s] Social proof: stats/logos/quotes     — MEDIUM-FAST
[50-60s] CTA: logo + URL + action             — SLOW, decisive
```

**Atemregel:** Nach jedem schnellen Abschnitt (3+ schnelle Schnitte) folgt eine ruhige Einstellung (5-8s).

## Easing {#easing}

### Cubic-Bezier-Referenz {#cubic-bezier-reference}

| Name | Wert | Wann |
|------|------|------|
| ease (Browser-Standard) | `(0.25, 0.1, 0.25, 1.0)` | Generisch, akzeptabel |
| **Material Standard** | `(0.4, 0.0, 0.2, 1.0)` | Primäres UI-Easing |
| Material Decelerate (Eintritt) | `(0.0, 0.0, 0.2, 1.0)` | Element erscheint |
| Material Accelerate (Austritt) | `(0.4, 0.0, 1.0, 1.0)` | Element verlässt die Szene |
| Emphasized Enter | `(0.05, 0.7, 0.1, 1.0)` | Dramatisches Erscheinen |
| Emphasized Exit | `(0.3, 0.0, 0.8, 0.15)` | Dramatischer Abgang |
| Bounce/Overshoot | `(0.34, 1.56, 0.64, 1.0)` | Verspielte Buttons/Badges |
| Snappy | `(0.2, 0.0, 0.0, 1.0)` | Schnell, bestimmt |
| Apple-Ease | `(0.25, 0.1, 0.25, 1.0)` | Premium-/Apple-Stil |

### Federphysik {#spring-physics}

| Konfiguration | stiffness | damping | Wirkung |
|---------------|-----------|---------|---------|
| Responsive UI | 200 | 20 | Minimales Federn |
| Verspielt | 120 | 10 | Deutliches Federn |
| Sanft (große Elemente) | 50 | 200 | Langsam, kein Federn |

**NIEMALS linear für UI** – wirkt mechanisch. Linear ist nur für Fortschrittsbalken gedacht.

## Stagger-Muster {#stagger-patterns}

**Maximal gestaffelte Elemente: 8-10.** Darüber hinaus warten die letzten Elemente zu lange.

**Lineares Stagger:** 30-80ms Abstand zwischen Listenelementen.

**Kaskade (beschleunigend):** Jede Verzögerung ist kürzer als die vorherige – erzeugt den Effekt des "Hineinfließens".

**Grid-Diagonale:** Verzögerung = `(row + col) * baseDelay`. Oben links startet zuerst.

**Welle vom Zentrum:** Verzögerung proportional zum Abstand vom Mittelpunkt.

## Disneys 12 Prinzipien, angewendet auf Produktvideos {#disneys-12-principles-applied-to-product-video}

| Prinzip | Anwendung | DO / DON'T |
|---------|-----------|------------|
| **Squash & Stretch** | Buttons skalieren beim Drücken auf 0.95-0.97 | DO: weiche Elemente. DON'T: Text/Linien |
| **Antizipation** | 30-50ms Mikrobewegung entgegen der Hauptrichtung | DO: vor größeren Übergängen. DON'T: bei Hover |
| **Staging** | Ein Fokuspunkt pro Szene | DO: Hintergrundanimationen stoppen, wenn das Schlüsselelement gezeigt wird. DON'T: 3+ gleichzeitige Animationen |
| **Follow Through** | Elemente überschwingen um 2-5 % und pendeln sich ein | DO: Stagger in Listen/Grids. DON'T: gleicher Stagger bei 20+ Elementen |
| **Ease In/Out** | Nie linear für UI | Material Standard als Standard verwenden |
| **Bögen** | Natürliche gekrümmte Bahnen zwischen Positionen | DO: schwebende Elemente. DON'T: Dropdowns (erwarten eine gerade Linie) |
| **Sekundäre Aktion** | Hintergrundeffekte unterstützen, konkurrieren nicht | DO: Ambient-Partikel, Glow-Puls. DON'T: Drehen, Blinken |
| **Übertreibung** | Produkt um 5-15 % größer skalieren für Wirkung | DO: Hero-Animationen. DON'T: Utility-Animationen |
| **Tiefe** | 3-5 Parallax-Ebenen | Hintergrund 0.3x Geschwindigkeit, Vordergrund 1.0-1.3x |

## Typografie auf dem Bildschirm {#typography-on-screen}

### Größenskala für 1920x1080 {#size-scale-for-1920x1080}

| Rolle | Größe | Gewicht | Hinweise |
|-------|-------|---------|----------|
| Hero-Zahl | 120-200px | 800-900 | "10x schneller", Kernkennzahlen |
| Abschnittstitel | 64-80px | 600 | Feature-Namen |
| Untertitel | 36-48px | 500 | Unterstützende Überschriften |
| Fließtext | 24-32px | 400 | Beschreibungen |
| Bildunterschrift | 16-20px | 400 | Kleine Anmerkungen |
| **Minimum** | **16px** | beliebig | Darunter im Video unlesbar |

### Lesegeschwindigkeit {#reading-speed}

| Format | Wörter | Anzeigedauer |
|--------|--------|--------------|
| Kurze Zeile | 3-7 Wörter | 1.5-3s |
| Mittlere Zeile | 8-12 Wörter | 3-5s |
| Langer Satz | 13-20 Wörter | 5-8s |
| 30+ Wörter | auf 2-3 Bildschirme aufteilen | - |

Für gemischtes Publikum 150-180 WPM ansetzen. Regel: 2.5-3.0s pro kurze Zeile (7-9 Wörter).

### Wortlimits pro Element {#word-limits-per-element}

| Element | Limit |
|---------|-------|
| Headline | 3-6 Wörter |
| Untertitel/Bildunterschrift | max. 2 Zeilen, 32-42 Zeichen pro Zeile |
| Lower Third | max. 2 Zeilen (Name + Titel) |
| Bildschirm mit Voiceover | max. 10-15 Wörter |
| Bildschirm ohne Voiceover | max. 20-25 Wörter |
| Thumbnail | max. 3-5 Wörter |

### Textanimation {#typography-animation}

- DO: Einblenden + 20-40px von unten verschieben
- DO: Skalierung von 95 % auf 100 % mit Opazität 0→1
- DO: Wörter um 4-8 Frames versetzt einblenden
- DON'T: Text drehen
- DON'T: Text hüpfen lassen (außer bei verspielter Marke)
- DON'T: Text bewegen, während der Zuschauer ihn liest

**Text muss mindestens 2s nach Abschluss der Animation lesbar sein.** Niemals Text animieren und gleichzeitig Lesen erwarten.

## Farbe {#color}

### Palettenregeln {#palette-rules}

- Maximal 3 Farben pro Video (+ Schwarz/Weiß/Grau)
- 1 primäre Markenfarbe + 1 Akzent + 1 CTA-Farbe
- Kontrast Hintergrund:Text mindestens 7:1 (WCAG AAA)
- Verlaufsfarben: maximal 120° auseinander auf dem Farbkreis

### Verlaufsrichtlinien {#gradient-guidelines}

**Richtung:** oben links→unten rechts (natürliches Licht). DON'T: unten nach oben.

| Typ | Wann |
|-----|------|
| Linear | Hintergründe, Overlays |
| Radial | Spotlight, Glow, Fokus auf die Mitte |
| Mesh | Premium-Hero-Hintergründe, App-Screens |
| Konisch | Uhren, Tortendiagramme, Fortschritt |

**Noise-Verläufe (2025-2026):** Verlauf + 3-8 % Noise-Overlay = organisch-premium Anmutung.

### Dark vs. Light Mode {#dark-vs-light-mode}

**Dark Mode besser für:** Produktpräsentationen (das Produkt hebt sich ab), Premium-/Luxusanmutung, gedämpfte Betrachtungsumgebungen, Fotos/Portfolios.

**Light Mode besser für:** dichten Text, Corporate, Konferenzräume, druknahe Inhalte.

### Trendpaletten (2026) {#trending-palettes-2026}

**Tech/Dunkel:**
- Tiefes Navy `#0D1117` + elektrisches Blau `#58A6FF`
- Dunkles Petrol `#0F2027` + Cyan `#00C9FF` + Weiß mit leichtem Ton

**Tech/Hell:**
- Off-White `#F8F9FA` + warme Akzente
- Weiches Lavendel `#F3E8FF` + tiefes Violett `#7C3AED`

## Komposition {#composition}

### Safe Zones nach Plattform {#safe-zones-by-platform}

**16:9 YouTube (1920x1080):**
- Title-Safe: innere 80 % (10 % Rand auf jeder Seite)
- Action-Safe: innere 90 %
- Lower-Third-Zone: untere 20-25 %

**9:16 Hochformat (TikTok/Reels/Shorts, 1080x1920):**
- Untere 20 % werden von der Plattform-UI belegt
- Rechte 10 % werden von der Plattform-UI belegt
- Motiv/Gesicht: obere 20-30 % des Bildes
- Textsafe-Zone: 15-75 % der Höhe, mittig zentriert

**1:1 Quadrat (Instagram, 1080x1080):**
- Safe Zone: innere 900x900px
- Zentrierte Komposition funktioniert am besten

### Visuelle Hierarchie pro Szene {#visual-hierarchy-per-scene}

- Maximal 3 Hierarchieebenen pro Szene
- Primäres Element = 40-60 % des visuellen Gewichts
- Niemals zwei primäre Elemente, die in einer Szene konkurrieren
- Größe + Gewicht + Farbe + Position gemeinsam einsetzen (nicht nur eines davon)

### Parallax-Tiefe {#parallax-depth}

- Hintergrundebene: 0.2-0.4x Scroll-Geschwindigkeit
- Mittelgrund: 0.6-0.8x
- Vordergrund: 1.0-1.3x

## Szenenübergänge {#scene-transitions}

| Übergang | Wann | Dauer |
|----------|------|-------|
| **Harter Schnitt** | Gleiche Energie, schnelles Tempo (80 % der Schnitte) | sofort |
| Crossfade | Zeitsprung, weiche Verbindung | 0.5-2s |
| Ausblenden nach Schwarz | Ende eines Abschnitts, dramatische Pause | 1-2s |
| Wipe | Ortswechsel, stilistisch | 0.5-1.5s |
| Zoom-Durchgang | Energie, modern, dynamisch | 0.3-0.5s |
| Match Cut | Visuelle Ähnlichkeit (Form/Farbe/Bewegung) | sofort |
| L-Cut | Audio aus Szene 1 über Visuals von Szene 2 | Audioüberlappung |
| J-Cut | Audio aus Szene 2 beginnt vor dem Ende von Szene 1 | Audio führt |

**Standard = harter Schnitt.** 80 %+ der professionellen Videoübergänge sind Schnitte.

Maximal 2-3 Übergangstypen pro Video. DON'T: Sternwischer, Schachbrettmuster, Crossfade >2s.

**Audio-Crossfade:** 100-300ms Überlappung für saubere Audioübergänge.

## Audiopegel {#audio-levels}

### dB-Referenz {#db-reference}

| Element | Spitze | Lautheit (LUFS) |
|---------|--------|-----------------|
| Voiceover | -12 bis -10 dB | -16 bis -14 |
| Musik unter VO | -32 bis -24 dB | -24 bis -18 |
| Musik solo | -16 bis -12 dB | -16 bis -14 |
| Soundeffekte | -18 bis -10 dB | variabel |
| Gesamtmix | -14 Mittel, Spitzen < -6 dB | -16 bis -14 |
| True-Peak-Grenze | -1 bis -3 dB | - |

**Regel:** Das VO sollte etwa 20 dB lauter sein als die Hintergrundmusik.

### BPM nach Stimmung {#bpm-by-mood}

| BPM | Stimmung | Anwendungsfall |
|-----|----------|----------------|
| 60-80 | Ruhig/Ambient | Luxus, Meditation |
| 80-100 | Entspannt | Lifestyle, Interviews |
| 100-120 | Moderat | Corporate, Tech-Demos |
| 120-140 | Energetisch | Produktlaunches, Fitness |
| 140+ | Hohe Energie | Action, Gaming |

120 BPM = bevorzugtes menschliches Tempo (entspricht Gehtempo, DAW-Standard).

### Soundeffekt-Typen {#sound-effect-types}

| SFX | Dauer | Wann |
|-----|-------|------|
| Whoosh | 50-200ms | Slide-in-Übergänge |
| Klick/Pop | 20-50ms | Button-Druck, Auswahl |
| Ding/Chime | - | Erfolgsmeldungen, Benachrichtigungen |
| Swoosh | - | Seitenübergänge, Enthüllungen |

SFX sollten 6-12 dB leiser sein als das VO.

### Freie Soundbibliotheken {#free-sound-libraries}

- **Mixkit** (mixkit.co) – lizenzfrei, keine Namensnennung, kommerziell erlaubt
- **Pixabay** (pixabay.com/sound-effects) – lizenzfrei, keine Anmeldung
- **Freesound** (freesound.org) – CC-lizenziert
- **SFX Engine** (sfxengine.com) – KI-generierte UI-Sounds

## Storytelling-Frameworks {#storytelling-frameworks}

### PAS (Problem-Agitation-Solution) – höchste Conversion {#pas-problem-agitation-solution-highest-converting}

```yaml
Problem:    3s — one clear pain point
Agitation:  5s — vivid consequence
Solution:   4s — your product/answer
CTA:        3s — direct call to action
Total: ~15s. Scale proportionally for 30-60s.
```

### Hook-Value-CTA {#hook-value-cta}

```yaml
Hook:  2-5s  — pain point or question
Value: rest  — concise solution
CTA:   3-5s
```

### Hook-Problem-Solution-Proof-CTA (für Kurzvideos optimiert) {#hook-problem-solution-proof-cta-short-video-optimized}

| Abschnitt | Dauer | Beispiel |
|-----------|-------|----------|
| Hook | 3-5s | "Was, wenn du Produktvideos in 5 Minuten erstellen könntest?" |
| Problem | 5-10s | "Ein Videoteam zu beauftragen kostet 5000 $+. DIY-Tools wirken amateurhaft." |
| Lösung | 10-20s | Produkt-Reveal + 1 zentrale Demo |
| Beleg | 5-10s | Kennzahlen, Logos, Testimonials |
| CTA | 3-5s | "Kostenlos starten unter product.com" |

### Regel für die ersten Sekunden {#first-seconds-rule}

- Die ersten 3 Sekunden entscheiden über die Verweildauer (Scroll-Stopp-Moment)
- Die ersten 8 Sekunden sind bei Short-Form alles
- DON'T: Logo/Intro am Anfang (niemanden interessiert dein Logo)
- DO: mit Hook, Problem oder visueller Überraschung beginnen

## Plattform-Spezifikationen (2026) {#platform-specs-2026}

| Plattform | Seitenverhältnis | Auflösung | Max. Dauer | Format |
|-----------|------------------|-----------|------------|--------|
| YouTube | 16:9 | 1920x1080 (bis 4K) | 12 Stunden | MP4 H.264+AAC |
| YouTube Shorts | 9:16 | 1080x1920 | 3 Min | MP4 |
| Instagram Reels | 9:16 | 1080x1920 | 20 Min | MP4/MOV |
| Instagram Feed | 1:1 oder 4:5 | 1080x1080 oder 1080x1350 | 60s | MP4/MOV |
| TikTok | 9:16 | 1080x1920 | 10 Min in der App | MP4/MOV |
| TikTok-Ads | 9:16 | 1080x1920 | 9-60s | MP4/MOV <500MB |
| LinkedIn | 16:9 oder 1:1 | 1920x1080 | 10 Min | MP4 |

**Engagement-Optimum:** TikTok 21-34s, YouTube Shorts 30-60s, Instagram Reels 15-30s.

## Copywriting für Video {#copywriting-for-video}

- Zahlen > Adjektive: "5x schneller" statt "viel schneller"
- Nutzen > Feature: "Spare 10 Stunden pro Woche" statt "Hat Batch-Verarbeitung"
- Du > Wir: "Du wirst lieben…" statt "Wir haben gebaut…"
- Maximal 8-10 Wörter pro Bildschirmzeile
- Streichen: sehr, wirklich, eigentlich, tatsächlich, einfach

**Hook-Formeln:**
- "Was, wenn du [gewünschtes Ergebnis] könntest?"
- "[Zahl] [Substantiv], die [unerwarteter Nutzen]"
- "Hör auf, [häufiger Fehler]. Fang an mit [bessere Vorgehensweise]."

## Thumbnail-Design {#thumbnail-design}

Spezifikation: 1280x720px, 72dpi, PNG/JPG <2MB.

**60-30-10-Farbregel:** 60 % Hintergrund, 30 % Motiv, 10 % Akzent/Text.

- Maximal 3-5 Wörter, auf Mobilgröße lesbar
- Gesichter mit Emotion = +20-30 % CTR
- Maximal 1-2 Hauptelemente, keine Unordnung

## Stolperfallen {#gotchas}

- **Lineares Easing wirkt mechanisch.** Immer eine Kurve verwenden. Die einzige berechtigte Verwendung von Linear sind Fortschrittsbalken und Spinner, bei denen eine konstante Rate erwartet wird.
- **Stagger bei 20+ Elementen bricht die UX.** Das letzte Element wartet zu lange, die Aufmerksamkeit des Betrachters schweift ab. Maximal 8-10 gestaffelte Elemente; bei längeren Listen gruppieren und die Gruppen staffeln.
- **Nicht mit einem Logo beginnen.** Zuschauer überspringen Intros. Der Hook muss Aufmerksamkeit gewinnen, bevor das Branding erscheint.
- **BPM ≠ Stimmung.** Zwei Tracks mit 120 BPM können sich völlig unterschiedlich anfühlen. Das BPM legt das Energieniveau fest, nicht den emotionalen Charakter.
- **Die unteren 20 % eines Hochformatvideos werden von der Plattform-UI verdeckt** (TikTok-Buttons für Like/Kommentar/Teilen). Dort niemals Text oder CTAs platzieren.
- **Ein Crossfade länger als 2 Sekunden wirkt wie ein Fehler.** Der Crossfade dient dem Zeitsprung, nicht dem Stil. Auf maximal 0.5-2s begrenzen.

## Produktions-Checklisten {#production-checklists}

### Vorproduktion {#pre-production}

- [ ] Storytelling-Framework: PAS / 3-Akt / Hook-Value
- [ ] Plattform und Seitenverhältnis festgelegt
- [ ] Farbpalette: maximal 3-4 Farben + Neutraltöne
- [ ] Schriften: maximal 2 (Überschrift + Fließtext)
- [ ] Musik: BPM passend zur Stimmung
- [ ] Soundeffekt-Bibliothek bereit

### Animation {#animation}

- [ ] Konsistentes Easing: maximal 1-2 Kurventypen
- [ ] Timing innerhalb der Grenzen (Mikro <100ms, Standard 200-350ms, komplex 350-500ms)
- [ ] Stagger 30-80ms zwischen gruppierten Elementen
- [ ] Maximal 2 gleichzeitig animierte Elemente
- [ ] Follow-Through bei Stopps (Überschwingen + Einpendeln)
- [ ] Antizipation vor größeren Übergängen

### Postproduktion {#post-production}

- [ ] Audiopegel: VO -12 bis -10 dB, Musik -32 bis -24 dB unter dem VO
- [ ] Text auf der Zielgerätegröße lesbar
- [ ] Safe Zones für die Zielplattform eingehalten
- [ ] Übergänge konsistent (maximal 2-3 Typen)
- [ ] Hook in den ersten 3 Sekunden
- [ ] CTA klar und sichtbar
- [ ] Thumbnail: 60-30-10-Regel, maximal 5 Wörter
- [ ] Untertitel/Captions hinzugefügt
- [ ] Im korrekten Plattformformat exportiert

## Siehe auch {#see-also}

- [[css-animation-and-transforms]]
- [[remotion-programmatic-video]]
- [[3d-browser-libs-for-video]]
