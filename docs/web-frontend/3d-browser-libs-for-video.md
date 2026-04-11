---
title: "3D Browser Libraries for Product Video"
description: "Comparison of Three.js, React Three Fiber, Spline, Lottie, and other 3D/animation libraries for browser-based product video generation with Remotion."
---

# 3D Browser Libraries for Product Video

Comparison of 3D and animation libraries for browser rendering, focused on use in programmatic video (Remotion) and product showcases.

## Quick Decision Guide

| Goal | Best choice |
|------|-------------|
| 3D product video, full control | React Three Fiber + `@remotion/three` |
| No-code 3D scene + programmatic animation | Spline + Remotion |
| Pre-made After Effects animations | Lottie + `@remotion/lottie` |
| Complex 3D with visual keyframing | Three.js + Theatre.js + R3F |
| Simple 3D card flips, no dep | CSS 3D transforms |
| Browser website, scroll-driven | GSAP + Three.js |

## Remotion Integration Status

| Library | Status | Package |
|---------|--------|---------|
| React Three Fiber | Official | `@remotion/three` |
| Lottie | Official | `@remotion/lottie` |
| Spline | Documented | via `@remotion/three` |
| CSS 3D transforms | Native | standard React CSS |
| GSAP | Manual | needs frame adapter |
| Rive | None | - |
| Babylon.js | None | - |
| tsParticles | Manual | via canvas capture |

## Full 3D Engines

### React Three Fiber (R3F) - 9/10 for product video

React renderer for Three.js. Declarative component API - scenes are JSX trees.

```tsx
import { Canvas } from '@react-three/fiber';
import { useCurrentFrame } from 'remotion';
import { ThreeCanvas } from '@remotion/three';

// Use ThreeCanvas from @remotion/three instead of Canvas
// It syncs Remotion frame timing with R3F render loop

const ProductScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <ThreeCanvas width={1920} height={1080}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <mesh rotation={[0, (frame / 30) * Math.PI * 2, 0]}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="royalblue" />
      </mesh>
    </ThreeCanvas>
  );
};
```

**Key difference from standalone R3F:** use `useCurrentFrame()` instead of `useFrame()`. Remotion controls the clock.

**Ecosystem:**
- `@react-three/drei` - helpers (OrbitControls, Environment, Text, etc.)
- `@react-three/postprocessing` - bloom, depth of field, chromatic aberration
- Leva - UI controls for development

**Official template:** `remotion-template-three`

### Three.js - 8/10 for product video

Lower-level than R3F. More control, more boilerplate. Use when R3F abstractions are limiting.

```tsx
import { ThreeCanvas } from '@remotion/three';
import * as THREE from 'three';
import { useRef, useEffect } from 'react';
import { useCurrentFrame } from 'remotion';

const ThreeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const meshRef = useRef<THREE.Mesh>(null);

  // Access Three.js objects directly via refs
  return (
    <ThreeCanvas width={1920} height={1080}>
      {/* ... */}
    </ThreeCanvas>
  );
};
```

**Claude Code skills for Three.js:**
- `github.com/OpenAEC-Foundation/Three.js-Claude-Skill-Package` - 24 skills (WebGL, WebGPU, R3F, Drei, physics, IFC)
- `github.com/CloudAI-X/threejs-skills` - fundamentals
- `github.com/dgreenheck/webgpu-claude-skill` - WebGPU + Three.js
- `github.com/Nice-Wolf-Studio/claude-skills-threejs-ecs-ts` - Three.js + ECS + TypeScript
- `github.com/freshtechbro/claudedesignskills` - 20+ skills including R3F

### Babylon.js - 5/10 for product video

Full game engine: physics, audio, XR, visual editor. Overkill for product videos. No Remotion integration.

Use case: interactive 3D experiences, configurators, games - not video rendering.

## No-Code / Visual 3D

### Spline (spline.design) - 9/10 for product video

Best designer-developer workflow: designer builds scene in browser editor, developer animates via Remotion.

**Features (2026):** Text-to-3D, Image-to-3D, Apple Vision Pro preview, real-time collaboration.

**Pricing:** Free / $12 Starter / $20 Pro / $36 Team

**Remotion integration:** documented via `@remotion/three`. Import `.splinecode` files.

```tsx
import Spline from '@splinetool/react-spline';

// Wrap in ThreeCanvas or use as React component
// Animate Spline object properties via frame-driven state
```

**Workflow:** Spline editor → export scene → import in Remotion → drive animation with `useCurrentFrame()`.

**Claude Code skills:** `freshtechbro/claudedesignskills` includes `spline-interactive`.

### Theatre.js - 7/10 for product video

Visual timeline editor for Three.js/R3F animations. Keyframing, sequence editor, scene graph. v0.5: all prop types are sequenceable.

No direct Remotion integration - export animations then drive from frame data.

Best for: creating complex 3D animations visually, then baking to keyframe data for Remotion.

## Animation Libraries

### Lottie - 7/10 for product video

After Effects animations exported to JSON. Official Remotion package.

```tsx
import { Lottie } from '@remotion/lottie';
import { staticFile } from 'remotion';

<Lottie
  animationData={require('./animation.json')}
  // or
  src={staticFile('animations/loading.json')}
/>
```

**Library:** LottieFiles.com - thousands of free animations. Filter by category, download JSON.

**Performance vs Rive:** Lottie files are ~4x larger, ~4x slower to parse. For video rendering this matters less than for interactive web.

### Rive (rive.app) - 6/10 for product video

Interactive animations with state machines. 90% smaller files vs Lottie, 4x faster production. Used by Spotify, Duolingo, Disney.

No Remotion integration. Best for interactive UI animations, not video rendering.

### GSAP + ScrollTrigger - 5/10 for product video

Most powerful web animation library. Excellent for scroll-driven websites. Not designed for frame-based video rendering.

No direct Remotion integration: GSAP uses real-time, Remotion uses frame numbers. Requires a custom adapter to translate `useCurrentFrame()` to GSAP timeline position.

Use outside Remotion for: landing pages, portfolio sites, scroll animations.

**Claude Code skills:** `freshtechbro/claudedesignskills` includes `gsap-scrolltrigger`.

### Anime.js - 4/10 for product video

Lightweight DOM animation (~17KB, lite 3KB). v4.3.0 (Jan 2026) adds `createLayout()` for animating between layout states. No Remotion integration.

Use for: web UI animations, not video rendering.

### Motion Canvas - 6/10 for product video

TypeScript library for programmatic video animations. Remotion competitor focused on educational/explainer content. Fork: Revideo (production migration target).

**When to choose over Remotion:** math-heavy explainer videos, programmatic diagram animations. Not for product showcase/marketing.

**Claude Code skills:** `apoorvlathey/motion-canvas-skills` on agentskills.so.

## Lightweight Effects

### CSS 3D Transforms - 6/10 for product video

Native perspective transforms. Zero dependencies. Works in Remotion as standard React CSS.

```tsx
// 3D card flip
<div style={{
  perspective: '1000px',
  transformStyle: 'preserve-3d',
}}>
  <div style={{
    transform: `rotateY(${interpolate(frame, [0, 30], [0, 180], {
      extrapolateRight: 'clamp'
    })}deg)`,
  }}>
    Card content
  </div>
</div>
```

Good for: card flips, book pages, simple 3D transforms. Not for complex 3D scenes.

### tsParticles - 6/10 as accent element

Particle effects (confetti, fireworks, floating particles). React, Vue, Svelte, Angular integrations.

No Remotion official integration. Can capture via canvas and inject as video layer.

Use as accent/background, not primary content.

### Vanta.js - 5/10 for product video

Pre-built animated backgrounds: birds, waves, globe, fog, clouds. Requires Three.js or p5.js.

No Remotion integration without canvas capture. Good as background texture in product shots.

## 2D Rendering

### Pixi.js - 4/10 for product video

Fastest 2D WebGL/WebGPU renderer. Excellent for games and interactive 2D. No Remotion integration.

### p5.js - 3/10 for product video

Creative coding (Processing for JavaScript). Generative art, visualizations. No Remotion integration without canvas capture.

## Performance Comparison

| Library | Bundle Size | Parse Time | GPU Usage | Render in Remotion |
|---------|-------------|-----------|-----------|-------------------|
| CSS 3D | 0KB | 0ms | Low | Native |
| Lottie | ~40KB | Fast | Low | Official |
| Three.js | ~600KB | Medium | High | Via `@remotion/three` |
| R3F | ~800KB | Medium | High | Official |
| Babylon.js | ~2MB | Slow | High | None |
| GSAP | ~100KB | Fast | Low | Manual adapter |

## Claude Code Skills Ecosystem

### Primary collections

**freshtechbro/claudedesignskills** (main collection)
- 20+ skills in one plugin: Three.js, R3F, GSAP, Babylon.js, PlayCanvas, Pixi.js, Lottie, Rive, Spline, Anime.js, A-Frame
- `github.com/freshtechbro/claudedesignskills`

**OpenAEC-Foundation/Three.js-Claude-Skill-Package**
- 24 deterministic Three.js skills: WebGL, WebGPU, R3F, Drei, physics, IFC
- `github.com/OpenAEC-Foundation/Three.js-Claude-Skill-Package`

### Specialized

- `github.com/CloudAI-X/threejs-skills` - Three.js fundamentals
- `github.com/dgreenheck/webgpu-claude-skill` - WebGPU + Three.js
- `github.com/Nice-Wolf-Studio/claude-skills-threejs-ecs-ts` - Three.js + ECS + TypeScript (game dev)

## TOP-5 for Product Videos

1. **R3F + `@remotion/three`** - 9/10 - full 3D in video, official support, React-native
2. **Spline + Remotion** - 9/10 - no-code 3D design + programmatic video
3. **Three.js + `@remotion/three`** - 8/10 - maximum control
4. **Lottie + `@remotion/lottie`** - 7/10 - ready-made animations, fast
5. **Theatre.js + R3F** - 7/10 - visual timeline for complex 3D animations

## Gotchas

- **`useFrame()` from R3F doesn't work in Remotion.** Replace with `useCurrentFrame()` from Remotion. The Remotion frame clock drives all animation - R3F's internal clock is bypassed.
- **Canvas capture for non-integrated libraries produces inconsistent frames.** When capturing libraries like GSAP or Vanta.js through canvas, frame timing depends on real-time execution. During fast headless rendering, frames can be skipped or duplicated. Prefer official integrations.
- **Spline scenes load async.** In Remotion, the scene must be fully loaded before frames render. Wrap Spline components in a loading gate or use `delayRender()` / `continueRender()`.
- **Three.js geometry is expensive per-frame if re-created.** Create geometry in component body (runs once), not inside render logic. Use `useMemo` for materials and geometries.
- **Babylon.js 2MB bundle impacts Lambda cold starts.** For video pipelines using AWS Lambda, heavy bundles increase cold start time. Prefer Three.js or R3F.
- **GSAP timeline position ≠ Remotion frame number.** GSAP `seek(time)` uses seconds, Remotion uses frames. The adapter: `timeline.seek(frame / fps)` before render.

## See Also

- [[remotion-programmatic-video]]
- [[css-animation-and-transforms]]
- [[react-components-and-jsx]]
- [[video-motion-design-rules]]
