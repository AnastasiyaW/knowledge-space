---
title: "Remotion: Programmatic Video with React"
description: "Build product demos, marketing videos, and pitch decks as React components — render to MP4 with frame-accurate animation control."
---

# Remotion: Programmatic Video with React

Remotion renders React components to video frames. Every animation is driven by `useCurrentFrame()` — no CSS transitions, no runtime state. Output is deterministic and scriptable.

## Core Concepts

**Frame = time.** At 30fps, frame 90 = 3 seconds. All animation is a function of the current frame number.

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion';

const MyScene: React.FC = () => {
  const frame = useCurrentFrame();           // current frame (0-based)
  const { fps, width, height } = useVideoConfig();

  return <div style={{ opacity: frame / 30 }}>Fades in over 1 second</div>;
};
```

**CRITICAL:** Never use CSS `transition`, `animation`, or `@keyframes`. They don't execute during headless rendering — only `interpolate()` and `spring()` work.

## Project Structure

```
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

**Constants-first pattern** - all tunable values in one file:

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

## Animation Primitives

### `interpolate()` - frame to value mapping

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

**Always use `extrapolateRight: 'clamp'`** to freeze at final value. Without it, values continue beyond keyframe range.

### `spring()` - physics-based animation

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

### Easing reference

| Easing | When | Remotion code |
|--------|------|---------------|
| ease-out | Element entering | `Easing.out(Easing.cubic)` |
| ease-in | Element leaving | `Easing.in(Easing.cubic)` |
| ease-in-out | Element moving on-screen | `Easing.inOut(Easing.cubic)` |
| spring smooth | Most elements | `spring({config: {damping: 200}})` |
| spring bouncy | Playful / badges | `spring({config: {damping: 8}})` |
| linear | Progress bars only | `Easing.linear` |

**Common bezier presets:**

```tsx
const EASING = {
  appleEase:       Easing.bezier(0.25, 0.1, 0.25, 1.0),
  materialStandard: Easing.bezier(0.4, 0.0, 0.2, 1.0),
  materialDecel:   Easing.bezier(0.0, 0.0, 0.2, 1.0),
  materialAccel:   Easing.bezier(0.4, 0.0, 1.0, 1.0),
  snappyIn:        Easing.bezier(0.0, 0.0, 0.15, 1.0),
};
```

## Scene Composition

### `Sequence` - non-overlapping scenes

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

Inside each Scene component, `useCurrentFrame()` resets to 0 at the sequence start.

### `TransitionSeries` - scenes with transitions

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

**Note:** TransitionSeries overlaps scenes during transition - total duration is shorter than sum of parts.

## Assets

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

Always use `staticFile()` for public/ assets - works in Studio, Lambda, and Cloud Run.

## Font Loading

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

`loadFont()` blocks render until font is ready - no FOUT in exported video.

## Stagger Patterns

**Linear stagger:**

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

**Grid stagger (diagonal):**

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

## Reusable Animation Helpers

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

## Logo Animation Patterns

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

## Parallax Depth Effect

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

## Render Performance

- Use `npx remotion benchmark` to find optimal `--concurrency` value
- `<OffthreadVideo>` over `<Video>` - renders outside main thread
- `useMemo` for expensive calculations (not for animation values - those change every frame)
- `staticFile()` for all assets - handles paths correctly across environments
- Keep composition tree shallow - deep nesting multiplies render cost
- Render controls as sibling to `<Player>`, not child - avoids unnecessary re-renders

## Ecosystem - Official Integrations

| Package | What it adds |
|---------|-------------|
| `@remotion/three` | React Three Fiber + `<ThreeCanvas>` |
| `@remotion/lottie` | After Effects animations via JSON |
| `@remotion/transitions` | `TransitionSeries` + built-in transitions |
| `@remotion/google-fonts` | Type-safe font loading |
| `@remotion/lambda` | AWS Lambda render farm |
| `@remotion/player` | In-browser preview component |

## Community Toolkits (Claude Code Skills)

- `remotion-dev/skills` - official first-party Claude Code skills (`npx skills add remotion-dev/skills`)
- `digitalsamba/claude-code-video-toolkit` - product demos with ElevenLabs voiceover, dark tech aesthetic
- `BayramAnnakov/remotion-video-director` - interactive deliberation: thinking → designing → building → reviewing
- `remotion-dev/apple-wow-tutorial` - reference implementation for Apple animation style

## Pre-Render Checklist

- [ ] All text on screen >= 32px (body), >= 64px (headings) at 1080p
- [ ] Every text block readable for minimum 2s after animation completes
- [ ] Contrast ratio >= 7:1 for text/background pairs
- [ ] Max 3 brand colors + black/white/gray
- [ ] No CSS transitions/animations - only `interpolate()` / `spring()`
- [ ] Consistent animation direction throughout
- [ ] Audio levels: music -12 to -18 dB relative to speech
- [ ] Logo has clear space (min 1x logo height on all sides)
- [ ] CTA is last thing on screen (3-5s dwell after animation)
- [ ] Duration matches target platform (15s social, 60s product, 90s pitch)

## Gotchas

- **CSS animations silently break on export.** The headless renderer doesn't run CSS keyframes. `transition: opacity 0.3s` looks fine in Studio preview but produces static output. Use `interpolate()` for all animation.
- **`useCurrentFrame()` is absolute inside Sequence.** Inside a `<Sequence from={150}>`, frame 0 = absolute frame 150. This is intentional - scenes are self-contained.
- **TransitionSeries shortens total duration.** Each transition overlaps adjacent scenes. A 30-frame transition between two 150-frame scenes gives total 270 frames, not 300. Account for this in `<Composition durationInFrames>`.
- **`spring()` never exactly reaches target.** It asymptotically approaches. For exact final values use `interpolate()` with `extrapolateRight: 'clamp'`. Springs are for feel, not precision.
- **Font FOUT doesn't appear in video.** `loadFont()` blocks rendering until ready. No need for fallback fonts.
- **Remote images require `allowFullScreen`.** Local assets via `staticFile()` are safer for reproducible renders.

## See Also

- [[css-animation-and-transforms]]
- [[react-components-and-jsx]]
- [[react-state-and-hooks]]
- [[3d-browser-libs-for-video]]
- [[video-motion-design-rules]]
