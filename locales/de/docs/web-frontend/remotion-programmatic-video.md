---
title: "Remotion: Programmatische Videos mit React"
description: "Produkt-Demos, Marketingvideos und Pitch-Decks als React-Komponenten erstellen – als MP4 rendern mit frame-genauer Animationssteuerung."
level: 4
source_sha256: 52ccdf5c7c0fdb190a6d6392ac894e68bf158327cad5850529699498aaad2739
translation: machine
translated_at: '2026-10-24'
---
# Remotion: Programmatische Videos mit React {#remotion-programmatic-video-with-react}

Remotion rendert React-Komponenten zu Videoframes. Jede Animation wird durch `useCurrentFrame()` gesteuert – keine CSS-Transitions, kein Laufzeitzustand. Die Ausgabe ist deterministisch und per Skript steuerbar.

## Kernkonzepte {#core-concepts}

**Frame = Zeit.** Bei 30 fps entspricht Frame 90 genau 3 Sekunden. Jede Animation ist eine Funktion der aktuellen Framenummer.

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion';

const MyScene: React.FC = () => {
  const frame = useCurrentFrame();           // current frame (0-based)
  const { fps, width, height } = useVideoConfig();

  return <div style={{ opacity: frame / 30 }}>Fades in over 1 second</div>;
};
```

**KRITISCH:** Niemals CSS-`transition`, `animation` oder `@keyframes` verwenden. Sie werden beim Headless-Rendering nicht ausgeführt – nur `interpolate()` und `spring()` funktionieren.

## Projektstruktur {#project-structure}

```typescript
src/
  Root.tsx              # registerRoot() entry point
  Composition.tsx       # all compositions registered here
  videos/ProductDemo/
    index.tsx           # main composition
    scenes/
      Hook.tsx
      Problem.tsx
      Solution.tsx
      Features.tsx
      CTA.tsx
    components/
      AnimatedText.tsx
      ProductImage.tsx
    constants.ts        # colors, fonts, timing - edit here only
    types.ts
  lib/
    animations.ts       # reusable spring/interpolate helpers
    fonts.ts            # font loading
  public/
    music/
    images/
    sounds/
```

**Constants-first-Muster** – alle anpassbaren Werte in einer Datei:

```tsx
// constants.ts
export const COLORS = {
  bg: '#000000',
  text: '#FFFFFF',
  accent: '#007AFF',
  secondary: '#8E8E93',
} as const;

export const TIMING = {
  fps: 30,
  sceneDuration: 150,  // 5s at 30fps
  fadeIn: 15,          // 0.5s
  stagger: 4,          // ~133ms between items
} as const;

export const FONTS = {
  heading: 'Inter',
  mono: 'JetBrains Mono',
} as const;
```

## Animationsprimitiven {#animation-primitives}

### `interpolate()` – Abbildung von Frame auf Wert {#interpolate-frame-to-value-mapping}

```tsx
import { interpolate, Easing, useCurrentFrame } from 'remotion';

const frame = useCurrentFrame();

// Fade in over 15 frames (0.5s @30fps)
const opacity = interpolate(frame, [0, 15], [0, 1], {
  easing: Easing.out(Easing.cubic),
  extrapolateRight: 'clamp',
});

// Slide up 40px over 20 frames
const translateY = interpolate(frame, [0, 20], [40, 0], {
  easing: Easing.out(Easing.cubic),
  extrapolateRight: 'clamp',
});

// Apple-style bezier easing
const smooth = interpolate(frame, [0, 30], [0, 100], {
  easing: Easing.bezier(0.25, 0.1, 0.25, 1.0),
  extrapolateRight: 'clamp',
});
```

**Immer `extrapolateRight: 'clamp'` verwenden**, um am Endwert zu verharren. Ohne diese Option laufen die Werte über den Keyframe-Bereich hinaus weiter.

### `spring()` – physikalisch basierte Animation {#spring-physics-based-animation}

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Spring presets
const SPRING_CONFIGS = {
  smooth:  { damping: 200 },                    // default - smooth settle
  snappy:  { damping: 20, stiffness: 200 },     // quick, minimal bounce
  bouncy:  { damping: 8, stiffness: 200 },      // noticeable bounce
  gentle:  { damping: 200, stiffness: 50 },     // slow settle for large elements
} as const;

const scale = spring({
  frame,
  fps,
  from: 0,
  to: 1,
  config: SPRING_CONFIGS.snappy,
});
```

### Easing-Referenz {#easing-reference}

| Easing | Einsatz | Remotion-Code |
|--------|---------|---------------|
| ease-out | Element erscheint | `Easing.out(Easing.cubic)` |
| ease-in | Element verschwindet | `Easing.in(Easing.cubic)` |
| ease-in-out | Element bewegt sich im Bild | `Easing.inOut(Easing.cubic)` |
| spring smooth | Die meisten Elemente | `spring({config: {damping: 200}})` |
| spring bouncy | Verspielt / Badges | `spring({config: {damping: 8}})` |
| linear | Nur Fortschrittsbalken | `Easing.linear` |

**Gängige Bezier-Voreinstellungen:**

```tsx
const EASING = {
  appleEase:       Easing.bezier(0.25, 0.1, 0.25, 1.0),
  materialStandard: Easing.bezier(0.4, 0.0, 0.2, 1.0),
  materialDecel:   Easing.bezier(0.0, 0.0, 0.2, 1.0),
  materialAccel:   Easing.bezier(0.4, 0.0, 1.0, 1.0),
  snappyIn:        Easing.bezier(0.0, 0.0, 0.15, 1.0),
};
```

## Szenenkomposition {#scene-composition}

### `Sequence` – nicht überlappende Szenen {#sequence-non-overlapping-scenes}

```tsx
import { AbsoluteFill, Sequence } from 'remotion';

export const ProductDemo: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#000' }}>
    <Sequence from={0}    durationInFrames={150}><HookScene /></Sequence>
    <Sequence from={150}  durationInFrames={300}><ProblemScene /></Sequence>
    <Sequence from={450}  durationInFrames={300}><SolutionScene /></Sequence>
    <Sequence from={750}  durationInFrames={450}><FeaturesScene /></Sequence>
    <Sequence from={1200} durationInFrames={150}><CTAScene /></Sequence>
  </AbsoluteFill>
);
```

Innerhalb jeder Scene-Komponente wird `useCurrentFrame()` beim Start der Sequence auf 0 zurückgesetzt.

### `TransitionSeries` – Szenen mit Übergängen {#transitionseries-scenes-with-transitions}

```tsx
import { TransitionSeries, springTiming, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';

export const ProductDemo: React.FC = () => (
  <TransitionSeries>
    <TransitionSeries.Sequence durationInFrames={150}>
      <HookScene />
    </TransitionSeries.Sequence>

    <TransitionSeries.Transition
      presentation={fade()}
      timing={springTiming({ config: { damping: 200 } })}
    />

    <TransitionSeries.Sequence durationInFrames={300}>
      <ProblemScene />
    </TransitionSeries.Sequence>

    <TransitionSeries.Transition
      presentation={slide({ direction: 'from-right' })}
      timing={linearTiming({ durationInFrames: 12 })}
    />

    <TransitionSeries.Sequence durationInFrames={300}>
      <SolutionScene />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);
```

**Hinweis:** TransitionSeries überlappt die Szenen während des Übergangs – die Gesamtdauer ist daher kürzer als die Summe der Teile.

## Assets {#assets}

```tsx
import { Img, staticFile, OffthreadVideo, Audio } from 'remotion';

// Image - blocks render until loaded (no broken frames)
<Img src={staticFile('product-hero.png')} style={{ width: '100%' }} />

// Video - renders offthread for better performance vs <Video>
<OffthreadVideo src={staticFile('demo.mp4')} />

// Background music
<Audio src={staticFile('music/ambient.mp3')} volume={0.3} />

// Volume fade out over last 30 frames
<Audio
  src={staticFile('music/bg.mp3')}
  volume={(f) =>
    interpolate(f, [totalFrames - 30, totalFrames], [0.3, 0], {
      extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    })
  }
/>

// Sound effect at frame 90
<Sequence from={90}>
  <Audio src={staticFile('sounds/whoosh.mp3')} volume={0.5} />
</Sequence>
```

Für Dateien im Ordner `public/` immer `staticFile()` verwenden – das funktioniert in Studio, Lambda und Cloud Run.

## Schriftladen {#font-loading}

```tsx
// fonts.ts
import { loadFont as loadInter } from '@remotion/google-fonts/Inter';
import { loadFont as loadJetBrainsMono } from '@remotion/google-fonts/JetBrainsMono';

const { fontFamily: interFamily } = loadInter('normal', {
  weights: ['400', '500', '600', '700', '800'],
  subsets: ['latin'],
});

export const FONT_FAMILIES = {
  heading: interFamily,
  mono: loadJetBrainsMono('normal', { weights: ['400', '700'] }).fontFamily,
};
```

`loadFont()` blockiert das Rendering, bis die Schrift bereit ist – im exportierten Video tritt daher kein FOUT auf.

## Stagger-Muster {#stagger-patterns}

**Lineares Stagger:**

```tsx
const STAGGER_DELAY = 8; // frames between items

{items.map((item, i) => {
  const delay = i * STAGGER_DELAY;
  return (
    <div key={i} style={{
      opacity: interpolate(frame, [delay, delay + 15], [0, 1],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
      transform: `translateY(${interpolate(frame, [delay, delay + 20], [30, 0], {
        easing: Easing.out(Easing.cubic),
        extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
      })}px)`,
    }}>
      {item}
    </div>
  );
})}
```

**Raster-Stagger (diagonal):**

```tsx
const COLS = 3;
const STAGGER = 4; // frames

{items.map((item, index) => {
  const row = Math.floor(index / COLS);
  const col = index % COLS;
  const delay = (row + col) * STAGGER;

  return (
    <div key={index} style={{
      opacity: interpolate(frame, [delay, delay + 15], [0, 1],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
    }}>
      {item}
    </div>
  );
})}
```

## Wiederverwendbare Animationshelfer {#reusable-animation-helpers}

```tsx
// lib/animations.ts
import { interpolate, Easing, spring } from 'remotion';

export const SPRING_CONFIGS = {
  smooth:  { damping: 200 },
  snappy:  { damping: 20, stiffness: 200 },
  bouncy:  { damping: 8, stiffness: 200 },
  gentle:  { damping: 200, stiffness: 50 },
} as const;

export const fadeIn = (frame: number, startFrame = 0, duration = 15) =>
  interpolate(frame, [startFrame, startFrame + duration], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

export const fadeOut = (frame: number, startFrame: number, duration = 12) =>
  interpolate(frame, [startFrame, startFrame + duration], [1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

export const slideInFromBottom = (frame: number, startFrame = 0, distance = 40, duration = 20) =>
  interpolate(frame, [startFrame, startFrame + duration], [distance, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

export const scalePop = (frame: number, fps: number, delay = 0, config = SPRING_CONFIGS.snappy) =>
  spring({ frame: frame - delay, fps, from: 0, to: 1, config });

export const staggerDelay = (index: number, delayPerItem = 4) => index * delayPerItem;

export const countTo = (frame: number, target: number, startFrame = 0, duration = 30) =>
  Math.round(interpolate(frame, [startFrame, startFrame + duration], [0, target], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  }));

export const typewriter = (text: string, frame: number, startFrame = 0, charsPerFrame = 0.5) => {
  const chars = Math.floor((frame - startFrame) * charsPerFrame);
  return text.slice(0, Math.max(0, Math.min(chars, text.length)));
};
```

## Produktvideo-Design im Apple-Stil {#apple-style-product-video-design}

**Ein Element pro Szene.** Niemals zwei primäre Elemente, die miteinander konkurrieren. 60–70 % des Frames sind Negativraum. Langsame Enthüllungen erzeugen Vorfreude; der Rhythmus wechselt zwischen schnellen Schnitten (2–3 s) und Hero-Shots (5–8 s).

### Typografische Skala (1920x1080) {#typography-scale-1920x1080}

| Rolle | Größe | Gewicht |
|-------|-------|---------|
| Hero-Kennzahl ("2x schneller") | 120–200px | 800–900 |
| Abschnittstitel | 64–80px | 600 |
| Untertitel | 36–48px | 500 |
| Fließtext | 24–32px | 400 |
| Bildunterschrift | 16–20px | 400 |
| **Minimum** | **16px** | beliebig |

**Schrift:** `@remotion/google-fonts/Inter` (offene Alternative zu SF Pro).

### Farbpalette {#color-palette}

Maximal 3 Farben pro Video. Kontrast Hintergrund:Text mindestens 7:1 (WCAG AAA).

| Farbe | Hex | Einsatz |
|-------|-----|---------|
| Schwarz | `#000000` | Hintergrund für Premium-Tech |
| Apple-Blau | `#007AFF` | CTAs, Tech-Features |
| Grün | `#34C759` | Wachstum, Erfolgskennzahlen |
| Orange | `#FF9500` | Aufmerksamkeit, Dringlichkeit |
| Lila | `#AF52DE` | Premium, kreative Werkzeuge |

## Logo-Animationsmuster {#logo-animation-patterns}

```tsx
// Pattern 1: Fade + Scale (most professional)
const logoOpacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
const logoScale = interpolate(frame, [0, 25], [0.9, 1], {
  easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp',
});

// Pattern 2: Stroke draw reveal (for line logos)
const pathLength = 200; // measure from SVG
const drawProgress = interpolate(frame, [0, 40], [pathLength, 0], { extrapolateRight: 'clamp' });
// Apply: strokeDasharray={pathLength} strokeDashoffset={drawProgress}

// Pattern 3: Mask/wipe reveal
const clipX = interpolate(frame, [0, 30], [0, 100], {
  easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp',
});
// Apply: clipPath: `inset(0 ${100 - clipX}% 0 0)`
```

## Parallax-Tiefeneffekt {#parallax-depth-effect}

```tsx
const scrollProgress = interpolate(frame, [0, 90], [0, 100], { extrapolateRight: 'clamp' });

<div style={{ transform: `translateY(${-scrollProgress * 0.3}px)` }}>
  <BackgroundLayer />  {/* background: 0.2-0.4x speed */}
</div>
<div style={{ transform: `translateY(${-scrollProgress * 0.7}px)` }}>
  <ProductImage />     {/* midground: 0.6-0.8x */}
</div>
<div style={{ transform: `translateY(${-scrollProgress * 1.0}px)` }}>
  <FloatingElements /> {/* foreground: 1.0-1.3x */}
</div>
```

## Render-Performance {#render-performance}

- `npx remotion benchmark` verwenden, um den optimalen `--concurrency`-Wert zu finden
- `<OffthreadVideo>` statt `<Video>` – rendert außerhalb des Hauptthreads
- `useMemo` für aufwendige Berechnungen (nicht für Animationswerte – diese ändern sich in jedem Frame)
- `staticFile()` für alle Assets – behandelt Pfade in allen Umgebungen korrekt
- Komponentenbaum flach halten – tiefe Verschachtelung vervielfacht die Renderkosten
- Steuerelemente als Geschwister von `<Player>` rendern, nicht als Kind – vermeidet unnötige Neu-Renderings

## Ökosystem – offizielle Integrationen {#ecosystem-official-integrations}

| Paket | Funktion |
|-------|----------|
| `@remotion/three` | React Three Fiber + `<ThreeCanvas>` |
| `@remotion/lottie` | After-Effects-Animationen über JSON |
| `@remotion/transitions` | `TransitionSeries` + eingebaute Übergänge |
| `@remotion/google-fonts` | Typsicheres Laden von Schriften |
| `@remotion/lambda` | AWS-Lambda-Render-Farm |
| `@remotion/player` | Vorschau-Komponente im Browser |

## Community-Toolkits (Claude-Code-Skills) {#community-toolkits-claude-code-skills}

- `remotion-dev/skills` – offizielle Claude-Code-Skills vom Remotion-Team (`npx skills add remotion-dev/skills`)
- `digitalsamba/claude-code-video-toolkit` – Produkt-Demos mit ElevenLabs-Voiceover, dunkle Tech-Ästhetik
- `BayramAnnakov/remotion-video-director` – interaktive Abstimmung: Denken → Gestalten → Bauen → Prüfen
- `remotion-dev/apple-wow-tutorial` – Referenzimplementierung für den Apple-Animationsstil

## Checkliste vor dem Rendern {#pre-render-checklist}

- [ ] Gesamter Text auf dem Bildschirm >= 32px (Fließtext), >= 64px (Überschriften) bei 1080p
- [ ] Jeder Textblock ist mindestens 2 s lesbar, nachdem die Animation abgeschlossen ist
- [ ] Kontrastverhältnis >= 7:1 für Text-/Hintergrund-Paare
- [ ] Maximal 3 Markenfarben + Schwarz/Weiß/Grau
- [ ] Keine CSS-Transitions/-Animationen – nur `interpolate()` / `spring()`
- [ ] Durchgehend einheitliche Animationsrichtung
- [ ] Audiopegel: Musik -12 bis -18 dB relativ zur Sprache
- [ ] Logo hat Freiraum (mindestens 1x Logohöhe auf allen Seiten)
- [ ] Der CTA ist das Letzte auf dem Bildschirm (3–5 s Verweildauer nach der Animation)
- [ ] Dauer passt zur Zielplattform (15 s Social, 60 s Produkt, 90 s Pitch)

## Stolperfallen {#gotchas}

- **CSS-Animationen brechen beim Export stillschweigend.** Der Headless-Renderer führt keine CSS-Keyframes aus. `transition: opacity 0.3s` sieht in der Studio-Vorschau korrekt aus, erzeugt aber statische Ausgabe. Für alle Animationen `interpolate()` verwenden.
- **`useCurrentFrame()` ist innerhalb von Sequence absolut.** Innerhalb von `<Sequence from={150}>` entspricht Frame 0 dem absoluten Frame 150. Das ist beabsichtigt – Szenen sind in sich abgeschlossen.
- **TransitionSeries verkürzt die Gesamtdauer.** Jeder Übergang überlappt die angrenzenden Szenen. Ein 30-Frame-Übergang zwischen zwei 150-Frame-Szenen ergibt insgesamt 270 Frames, nicht 300. Dies muss bei `<Composition durationInFrames>` berücksichtigt werden.
- **`spring()` erreicht den Zielwert nie exakt.** Es nähert sich ihm asymptotisch an. Für exakte Endwerte `interpolate()` mit `extrapolateRight: 'clamp'` verwenden. Springs dienen dem Gefühl, nicht der Präzision.
- **FOUT tritt im Video nicht auf.** `loadFont()` blockiert das Rendering, bis die Schrift bereit ist. Fallback-Schriften sind nicht nötig.
- **Remote-Bilder erfordern `allowFullScreen`.** Lokale Assets über `staticFile()` sind für reproduzierbare Renderings sicherer.

## Siehe auch {#see-also}

- [[css-animation-and-transforms]]
- [[react-components-and-jsx]]
- [[react-state-and-hooks]]
- [[3d-browser-libs-for-video]]
- [[video-motion-design-rules]]
