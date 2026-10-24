---
title: "3D-Browser-Bibliotheken für Produktvideos"
description: "Vergleich von Three.js, React Three Fiber, Spline, Lottie und weiteren 3D- und Animationsbibliotheken für die browserbasierte Produktvideo-Erstellung mit Remotion."
level: 3
source_sha256: b57e40c058ba0eccf06443a7f1690c9b59d012ce9389b29c37db8a586deea029
translation: machine
translated_at: '2026-10-24'
---
# 3D-Browser-Bibliotheken für Produktvideos {#3d-browser-libraries-for-product-video}

Vergleich von 3D- und Animationsbibliotheken für das Rendern im Browser, mit Fokus auf den Einsatz in programmatischen Videos (Remotion) und Produktpräsentationen.

## Schnelle Entscheidungshilfe {#quick-decision-guide}

| Ziel | Beste Wahl |
|------|-------------|
| 3D-Produktvideo, volle Kontrolle | React Three Fiber + `@remotion/three` |
| 3D-Szene ohne Code + programmatische Animation | Spline + Remotion |
| Vorgefertigte After-Effects-Animationen | Lottie + `@remotion/lottie` |
| Komplexes 3D mit visuellem Keyframing | Three.js + Theatre.js + R3F |
| Einfache 3D-Kartenwendungen, keine Abhängigkeit | CSS-3D-Transformationen |
| Browser-Website, scrollgesteuert | GSAP + Three.js |

## Status der Remotion-Integration {#remotion-integration-status}

| Bibliothek | Status | Paket |
|---------|--------|---------|
| React Three Fiber | Offiziell | `@remotion/three` |
| Lottie | Offiziell | `@remotion/lottie` |
| Spline | Dokumentiert | über `@remotion/three` |
| CSS-3D-Transformationen | Nativ | Standard-React-CSS |
| GSAP | Manuell | benötigt Frame-Adapter |
| Rive | Keine | - |
| Babylon.js | Keine | - |
| tsParticles | Manuell | über Canvas-Capture |

## Vollwertige 3D-Engines {#full-3d-engines}

### React Three Fiber (R3F) - 9/10 für Produktvideos {#react-three-fiber-r3f-910-for-product-video}

React-Renderer für Three.js. Deklarative Komponenten-API, Szenen sind JSX-Bäume.

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

**Wichtiger Unterschied zu eigenständigem R3F:** `useCurrentFrame()` statt `useFrame()` verwenden. Remotion steuert den Takt.

**Ökosystem:**
- `@react-three/drei` - Hilfsfunktionen (OrbitControls, Environment, Text usw.)
- `@react-three/postprocessing` - Bloom, Tiefenschärfe, chromatische Aberration
- Leva - UI-Steuerelemente für die Entwicklung

**Offizielle Vorlage:** `remotion-template-three`

### Three.js - 8/10 für Produktvideos {#threejs-810-for-product-video}

Niedrigere Abstraktionsebene als R3F. Mehr Kontrolle, mehr Boilerplate. Einsetzen, wenn die Abstraktionen von R3F einschränken.

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

**Claude-Code-Skills für Three.js:**
- `github.com/OpenAEC-Foundation/Three.js-Claude-Skill-Package` - 24 Skills (WebGL, WebGPU, R3F, Drei, Physik, IFC)
- `github.com/CloudAI-X/threejs-skills` - Grundlagen
- `github.com/dgreenheck/webgpu-claude-skill` - WebGPU + Three.js
- `github.com/Nice-Wolf-Studio/claude-skills-threejs-ecs-ts` - Three.js + ECS + TypeScript
- `github.com/freshtechbro/claudedesignskills` - über 20 Skills, darunter R3F

### Babylon.js - 5/10 für Produktvideos {#babylonjs-510-for-product-video}

Vollwertige Game-Engine: Physik, Audio, XR, visueller Editor. Für Produktvideos überdimensioniert. Keine Remotion-Integration.

Anwendungsfall: interaktive 3D-Erlebnisse, Konfiguratoren, Spiele - nicht das Rendern von Videos.

## Ohne Code / visuelles 3D {#no-code-visual-3d}

### Spline (spline.design) - 9/10 für Produktvideos {#spline-splinedesign-910-for-product-video}

Bester Workflow zwischen Designer und Entwickler: Der Designer baut die Szene im Browser-Editor, der Entwickler animiert sie über Remotion.

**Funktionen (2026):** Text-zu-3D, Bild-zu-3D, Vorschau für Apple Vision Pro, Echtzeit-Zusammenarbeit.

**Preise:** Kostenlos / 12 $ Starter / 20 $ Pro / 36 $ Team

**Remotion-Integration:** dokumentiert über `@remotion/three`. `.splinecode`-Dateien importieren.

```tsx
import Spline from '@splinetool/react-spline';

// Wrap in ThreeCanvas or use as React component
// Animate Spline object properties via frame-driven state
```

**Workflow:** Spline-Editor → Szene exportieren → in Remotion importieren → Animation mit `useCurrentFrame()` steuern.

**Claude-Code-Skills:** `freshtechbro/claudedesignskills` enthält `spline-interactive`.

### Theatre.js - 7/10 für Produktvideos {#theatrejs-710-for-product-video}

Visueller Timeline-Editor für Three.js-/R3F-Animationen. Keyframing, Sequenz-Editor, Szenengraph. Version 0.5: alle Property-Typen sind sequenzierbar.

Keine direkte Remotion-Integration - Animationen exportieren und anschließend über Frame-Daten steuern.

Ideal für: komplexe 3D-Animationen visuell erstellen und anschließend als Keyframe-Daten für Remotion einbacken.

## Animationsbibliotheken {#animation-libraries}

### Lottie - 7/10 für Produktvideos {#lottie-710-for-product-video}

After-Effects-Animationen, exportiert als JSON. Offizielles Remotion-Paket.

```tsx
import { Lottie } from '@remotion/lottie';
import { staticFile } from 'remotion';

<Lottie
  animationData={require('./animation.json')}
  // or
  src={staticFile('animations/loading.json')}
/>
```

**Bibliothek:** LottieFiles.com - Tausende kostenlose Animationen. Nach Kategorie filtern, JSON herunterladen.

**Performance im Vergleich zu Rive:** Lottie-Dateien sind etwa 4x größer und werden etwa 4x langsamer geparst. Für das Rendern von Videos spielt das eine geringere Rolle als für interaktives Web.

### Rive (rive.app) - 6/10 für Produktvideos {#rive-riveapp-610-for-product-video}

Interaktive Animationen mit State Machines. 90 % kleinere Dateien als Lottie, 4x schnellere Produktion. Eingesetzt von Spotify, Duolingo, Disney.

Keine Remotion-Integration. Am besten für interaktive UI-Animationen geeignet, nicht für das Rendern von Videos.

### GSAP + ScrollTrigger - 5/10 für Produktvideos {#gsap-scrolltrigger-510-for-product-video}

Leistungsstärkste Animationsbibliothek für das Web. Hervorragend für scrollgesteuerte Websites. Nicht für frame-basiertes Videorendering konzipiert.

Keine direkte Remotion-Integration: GSAP arbeitet in Echtzeit, Remotion mit Frame-Nummern. Ein eigener Adapter ist nötig, der `useCurrentFrame()` in die Position der GSAP-Timeline übersetzt.

Außerhalb von Remotion einsetzen für: Landingpages, Portfolio-Seiten, Scroll-Animationen.

**Claude-Code-Skills:** `freshtechbro/claudedesignskills` enthält `gsap-scrolltrigger`.

### Anime.js - 4/10 für Produktvideos {#animejs-410-for-product-video}

Leichtgewichtige DOM-Animation (ca. 17 KB, Lite-Version 3 KB). Version 4.3.0 (Jan. 2026) ergänzt `createLayout()` für Animationen zwischen Layoutzuständen. Keine Remotion-Integration.

Einsatz für: Animationen in Web-Oberflächen, nicht für das Rendern von Videos.

### Motion Canvas - 6/10 für Produktvideos {#motion-canvas-610-for-product-video}

TypeScript-Bibliothek für programmatische Videoanimationen. Konkurrent zu Remotion mit Fokus auf Bildungs- und Erklärvideos. Fork: Revideo (Ziel für Produktionsmigration).

**Wann statt Remotion wählen:** mathelastige Erklärvideos, programmatische Diagrammanimationen. Nicht für Produktpräsentationen oder Marketing.

**Claude-Code-Skills:** `apoorvlathey/motion-canvas-skills` auf agentskills.so.

## Leichtgewichtige Effekte {#lightweight-effects}

### CSS-3D-Transformationen - 6/10 für Produktvideos {#css-3d-transforms-610-for-product-video}

Native Perspektiv-Transformationen. Keine Abhängigkeiten. Funktioniert in Remotion als Standard-React-CSS.

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

Geeignet für: Kartenwendungen, Buchseiten, einfache 3D-Transformationen. Nicht für komplexe 3D-Szenen.

### tsParticles - 6/10 als Akzentelement {#tsparticles-610-as-accent-element}

Partikeleffekte (Konfetti, Feuerwerk, schwebende Partikel). Integrationen für React, Vue, Svelte und Angular.

Keine offizielle Remotion-Integration. Kann über Canvas erfasst und als Videoebene eingefügt werden.

Als Akzent oder Hintergrund verwenden, nicht als Hauptinhalt.

### Vanta.js - 5/10 für Produktvideos {#vantajs-510-for-product-video}

Vorgefertigte animierte Hintergründe: Vögel, Wellen, Globus, Nebel, Wolken. Benötigt Three.js oder p5.js.

Ohne Canvas-Capture keine Remotion-Integration. Gut als Hintergrundtextur in Produktaufnahmen.

## 2D-Rendering {#2d-rendering}

### Pixi.js - 4/10 für Produktvideos {#pixijs-410-for-product-video}

Schnellster 2D-WebGL/WebGPU-Renderer. Hervorragend für Spiele und interaktive 2D-Inhalte. Keine Remotion-Integration.

### p5.js - 3/10 für Produktvideos {#p5js-310-for-product-video}

Creative Coding (Processing für JavaScript). Generative Kunst, Visualisierungen. Ohne Canvas-Capture keine Remotion-Integration.

## Performance-Vergleich {#performance-comparison}

| Bibliothek | Bundle-Größe | Parse-Zeit | GPU-Last | Rendering in Remotion |
|---------|-------------|-----------|-----------|-------------------|
| CSS 3D | 0 KB | 0 ms | Niedrig | Nativ |
| Lottie | ~40 KB | Schnell | Niedrig | Offiziell |
| Three.js | ~600 KB | Mittel | Hoch | Über `@remotion/three` |
| R3F | ~800 KB | Mittel | Hoch | Offiziell |
| Babylon.js | ~2 MB | Langsam | Hoch | Keine |
| GSAP | ~100 KB | Schnell | Niedrig | Manueller Adapter |

## Ökosystem der Claude-Code-Skills {#claude-code-skills-ecosystem}

### Wichtigste Sammlungen {#primary-collections}

**freshtechbro/claudedesignskills** (Hauptsammlung)
- Über 20 Skills in einem Plugin: Three.js, R3F, GSAP, Babylon.js, PlayCanvas, Pixi.js, Lottie, Rive, Spline, Anime.js, A-Frame
- `github.com/freshtechbro/claudedesignskills`

**OpenAEC-Foundation/Three.js-Claude-Skill-Package**
- 24 deterministische Three.js-Skills: WebGL, WebGPU, R3F, Drei, Physik, IFC
- `github.com/OpenAEC-Foundation/Three.js-Claude-Skill-Package`

### Spezialisierte Sammlungen {#specialized}

- `github.com/CloudAI-X/threejs-skills` - Three.js-Grundlagen
- `github.com/dgreenheck/webgpu-claude-skill` - WebGPU + Three.js
- `github.com/Nice-Wolf-Studio/claude-skills-threejs-ecs-ts` - Three.js + ECS + TypeScript (Spieleentwicklung)

## TOP 5 für Produktvideos {#top-5-for-product-videos}

1. **R3F + `@remotion/three`** - 9/10 - vollständiges 3D im Video, offizielle Unterstützung, React-nativ
2. **Spline + Remotion** - 9/10 - 3D-Design ohne Code + programmatisches Video
3. **Three.js + `@remotion/three`** - 8/10 - maximale Kontrolle
4. **Lottie + `@remotion/lottie`** - 7/10 - fertige Animationen, schnell
5. **Theatre.js + R3F** - 7/10 - visuelle Timeline für komplexe 3D-Animationen

## Stolperfallen {#gotchas}

- **`useFrame()` von R3F funktioniert nicht in Remotion.** Durch `useCurrentFrame()` aus Remotion ersetzen. Der Frame-Takt von Remotion steuert sämtliche Animationen - der interne Takt von R3F wird umgangen.
- **Canvas-Capture bei nicht integrierten Bibliotheken erzeugt inkonsistente Frames.** Beim Erfassen von Bibliotheken wie GSAP oder Vanta.js über Canvas hängt das Frame-Timing von der Ausführung in Echtzeit ab. Bei schnellem Headless-Rendering können Frames übersprungen oder doppelt erzeugt werden. Offizielle Integrationen bevorzugen.
- **Spline-Szenen werden asynchron geladen.** In Remotion muss die Szene vollständig geladen sein, bevor Frames gerendert werden. Spline-Komponenten in ein Ladegate einhüllen oder `delayRender()` / `continueRender()` verwenden.
- **Die Neuerstellung von Three.js-Geometrien pro Frame ist teuer.** Geometrien im Komponentenkörper erstellen (wird einmal ausgeführt), nicht innerhalb der Render-Logik. Für Materialien und Geometrien `useMemo` verwenden.
- **Das 2-MB-Bundle von Babylon.js verlängert Lambda-Cold-Starts.** Bei Video-Pipelines auf AWS Lambda vergrößern schwere Bundles die Cold-Start-Zeit. Three.js oder R3F bevorzugen.
- **Die GSAP-Timeline-Position entspricht nicht der Remotion-Frame-Nummer.** `seek(time)` von GSAP arbeitet in Sekunden, Remotion in Frames. Der Adapter: `timeline.seek(frame / fps)` vor dem Rendern.

## Siehe auch {#see-also}

- [[remotion-programmatic-video]]
- [[css-animation-and-transforms]]
- [[react-components-and-jsx]]
- [[video-motion-design-rules]]
