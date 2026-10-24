---
title: "Remotion : vidéo programmatique avec React"
description: "Créez des démos produit, des vidéos marketing et des pitch decks sous forme de composants React, et exportez-les en MP4 avec un contrôle de l'animation image par image."
level: 4
source_sha256: 52ccdf5c7c0fdb190a6d6392ac894e68bf158327cad5850529699498aaad2739
translation: machine
translated_at: '2026-10-24'
---
# Remotion : vidéo programmatique avec React {#remotion-programmatic-video-with-react}

Remotion rend des composants React sous forme d'images vidéo. Chaque animation est pilotée par `useCurrentFrame()` : pas de transitions CSS, pas d'état à l'exécution. Le résultat est déterministe et scriptable.

## Concepts fondamentaux {#core-concepts}

**Image = temps.** À 30 ips, l'image 90 correspond à 3 secondes. Toute animation est une fonction du numéro de l'image courante.

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion';

const MyScene: React.FC = () => {
  const frame = useCurrentFrame();           // current frame (0-based)
  const { fps, width, height } = useVideoConfig();

  return <div style={{ opacity: frame / 30 }}>Fades in over 1 second</div>;
};
```

**CRITIQUE :** n'utilisez jamais `transition`, `animation` ou `@keyframes` en CSS. Ils ne s'exécutent pas pendant le rendu headless : seuls `interpolate()` et `spring()` fonctionnent.

## Structure du projet {#project-structure}

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

**Principe des constantes en premier** : toutes les valeurs ajustables sont regroupées dans un seul fichier :

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

## Primitives d'animation {#animation-primitives}

### `interpolate()` : correspondance image vers valeur {#interpolate-frame-to-value-mapping}

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

**Utilisez toujours `extrapolateRight: 'clamp'`** pour figer la valeur finale. Sans cette option, les valeurs continuent au-delà de la plage des keyframes.

### `spring()` : animation basée sur la physique {#spring-physics-based-animation}

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

### Référence des courbes d'accélération (easing) {#easing-reference}

| Easing | Quand | Code Remotion |
|--------|-------|---------------|
| ease-out | Élément qui entre | `Easing.out(Easing.cubic)` |
| ease-in | Élément qui sort | `Easing.in(Easing.cubic)` |
| ease-in-out | Élément qui se déplace à l'écran | `Easing.inOut(Easing.cubic)` |
| spring smooth | La plupart des éléments | `spring({config: {damping: 200}})` |
| spring bouncy | Ludique / badges | `spring({config: {damping: 8}})` |
| linear | Barres de progression uniquement | `Easing.linear` |

**Préréglages de courbes de Bézier courants :**

```tsx
const EASING = {
  appleEase:       Easing.bezier(0.25, 0.1, 0.25, 1.0),
  materialStandard: Easing.bezier(0.4, 0.0, 0.2, 1.0),
  materialDecel:   Easing.bezier(0.0, 0.0, 0.2, 1.0),
  materialAccel:   Easing.bezier(0.4, 0.0, 1.0, 1.0),
  snappyIn:        Easing.bezier(0.0, 0.0, 0.15, 1.0),
};
```

## Composition de scènes {#scene-composition}

### `Sequence` : scènes sans chevauchement {#sequence-non-overlapping-scenes}

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

Dans chaque composant de scène, `useCurrentFrame()` repart de 0 au début de la séquence.

### `TransitionSeries` : scènes avec transitions {#transitionseries-scenes-with-transitions}

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

**Remarque :** `TransitionSeries` fait chevaucher les scènes pendant la transition. La durée totale est donc inférieure à la somme des parties.

## Ressources {#assets}

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

Utilisez toujours `staticFile()` pour les ressources du dossier public/. Cela fonctionne dans Studio, Lambda et Cloud Run.

## Chargement des polices {#font-loading}

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

`loadFont()` bloque le rendu jusqu'à ce que la police soit prête : aucun FOUT dans la vidéo exportée.

## Motifs de décalage (stagger) {#stagger-patterns}

**Décalage linéaire :**

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

**Décalage en grille (diagonal) :**

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

## Fonctions utilitaires d'animation réutilisables {#reusable-animation-helpers}

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

## Design de vidéo produit à la manière d'Apple {#apple-style-product-video-design}

**Une seule chose par scène.** Ne faites jamais concurrencer deux éléments principaux. 60 à 70 % de l'image doivent rester en espace négatif. Les révélations lentes créent de l'anticipation ; le rythme alterne des coupes rapides (2 à 3 s) avec des plans héros (5 à 8 s).

### Échelle typographique (1920x1080) {#typography-scale-1920x1080}

| Rôle | Taille | Graisse |
|------|--------|---------|
| Statistique héros (« 2x plus rapide ») | 120 à 200 px | 800 à 900 |
| Titre de section | 64 à 80 px | 600 |
| Sous-titre | 36 à 48 px | 500 |
| Corps de texte | 24 à 32 px | 400 |
| Légende | 16 à 20 px | 400 |
| **Minimum** | **16 px** | indifférent |

**Police :** `@remotion/google-fonts/Inter` (alternative libre à SF Pro).

### Palette de couleurs {#color-palette}

Maximum 3 couleurs par vidéo. Contraste fond/texte minimum de 7:1 (WCAG AAA).

| Couleur | Hex | Usage |
|---------|-----|-------|
| Noir | `#000000` | Fond tech premium |
| Bleu Apple | `#007AFF` | CTA, fonctionnalités tech |
| Vert | `#34C759` | Croissance, indicateurs de succès |
| Orange | `#FF9500` | Attention, urgence |
| Violet | `#AF52DE` | Premium, outils créatifs |

## Motifs d'animation de logo {#logo-animation-patterns}

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

## Effet de profondeur parallaxe {#parallax-depth-effect}

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

## Performance du rendu {#render-performance}

- Utilisez `npx remotion benchmark` pour trouver la valeur optimale de `--concurrency`
- Préférez `<OffthreadVideo>` à `<Video>` : le rendu se fait hors du thread principal
- Utilisez `useMemo` pour les calculs coûteux (pas pour les valeurs d'animation, qui changent à chaque image)
- Utilisez `staticFile()` pour toutes les ressources : les chemins sont gérés correctement selon les environnements
- Gardez l'arbre de composition peu profond : une imbrication profonde multiplie le coût du rendu
- Placez les contrôles de rendu en frères de `<Player>`, et non en enfants : cela évite des re-rendus inutiles

## Écosystème : intégrations officielles {#ecosystem-official-integrations}

| Paquet | Ce qu'il apporte |
|--------|------------------|
| `@remotion/three` | React Three Fiber + `<ThreeCanvas>` |
| `@remotion/lottie` | Animations After Effects via JSON |
| `@remotion/transitions` | `TransitionSeries` + transitions intégrées |
| `@remotion/google-fonts` | Chargement de polices typé |
| `@remotion/lambda` | Ferme de rendu AWS Lambda |
| `@remotion/player` | Composant de prévisualisation dans le navigateur |

## Boîtes à outils communautaires (Skills Claude Code) {#community-toolkits-claude-code-skills}

- `remotion-dev/skills` : skills Claude Code officiels de l'éditeur (`npx skills add remotion-dev/skills`)
- `digitalsamba/claude-code-video-toolkit` : démos produit avec voix off ElevenLabs, esthétique tech sombre
- `BayramAnnakov/remotion-video-director` : délibération interactive : réflexion → conception → construction → relecture
- `remotion-dev/apple-wow-tutorial` : implémentation de référence du style d'animation Apple

## Checklist avant rendu {#pre-render-checklist}

- [ ] Tout texte à l'écran >= 32 px (corps), >= 64 px (titres) en 1080p
- [ ] Chaque bloc de texte reste lisible pendant au moins 2 s après la fin de l'animation
- [ ] Ratio de contraste >= 7:1 pour les paires texte/fond
- [ ] Au maximum 3 couleurs de marque + noir/blanc/gris
- [ ] Aucune transition ni animation CSS : uniquement `interpolate()` / `spring()`
- [ ] Direction d'animation cohérente sur toute la vidéo
- [ ] Niveaux audio : musique entre -12 et -18 dB par rapport à la voix
- [ ] Le logo dispose d'un espace libre (au moins 1x la hauteur du logo de chaque côté)
- [ ] Le CTA est le dernier élément à l'écran (3 à 5 s de présence après l'animation)
- [ ] La durée correspond à la plateforme cible (15 s pour les réseaux sociaux, 60 s pour un produit, 90 s pour un pitch)

## Pièges courants {#gotchas}

- **Les animations CSS échouent silencieusement à l'export.** Le moteur de rendu headless n'exécute pas les keyframes CSS. `transition: opacity 0.3s` paraît correct dans l'aperçu Studio, mais produit une sortie statique. Utilisez `interpolate()` pour toutes les animations.
- **`useCurrentFrame()` est absolu à l'intérieur d'une Sequence.** Dans un `<Sequence from={150}>`, l'image 0 correspond à l'image absolue 150. C'est voulu : les scènes sont autonomes.
- **`TransitionSeries` raccourcit la durée totale.** Chaque transition chevauche les scènes adjacentes. Une transition de 30 images entre deux scènes de 150 images donne un total de 270 images, et non 300. Tenez-en compte dans `<Composition durationInFrames>`.
- **`spring()` n'atteint jamais exactement la cible.** Il s'en approche de façon asymptotique. Pour des valeurs finales exactes, utilisez `interpolate()` avec `extrapolateRight: 'clamp'`. Les springs servent à la sensation, pas à la précision.
- **Le FOUT des polices n'apparaît pas dans la vidéo.** `loadFont()` bloque le rendu jusqu'à ce que la police soit prête. Inutile de prévoir des polices de secours.
- **Les images distantes nécessitent `allowFullScreen`.** Les ressources locales via `staticFile()` sont plus sûres pour des rendus reproductibles.

## Voir aussi {#see-also}

- [[css-animation-and-transforms]]
- [[react-components-and-jsx]]
- [[react-state-and-hooks]]
- [[3d-browser-libs-for-video]]
- [[video-motion-design-rules]]
