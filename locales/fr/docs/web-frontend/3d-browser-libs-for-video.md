---
title: "Bibliothèques 3D pour navigateur pour les vidéos produit"
description: "Comparatif de Three.js, React Three Fiber, Spline, Lottie et d'autres bibliothèques 3D et d'animation pour la génération de vidéos produit dans le navigateur avec Remotion."
level: 3
source_sha256: b57e40c058ba0eccf06443a7f1690c9b59d012ce9389b29c37db8a586deea029
translation: machine
translated_at: '2026-10-24'
---
# Bibliothèques 3D pour navigateur pour les vidéos produit {#3d-browser-libraries-for-product-video}

Comparatif de bibliothèques 3D et d'animation pour le rendu dans le navigateur, axé sur l'usage en vidéo programmatique (Remotion) et sur les présentations de produits.

## Guide de décision rapide {#quick-decision-guide}

| Objectif | Meilleur choix |
|----------|----------------|
| Vidéo produit 3D, contrôle total | React Three Fiber + `@remotion/three` |
| Scène 3D sans code + animation programmatique | Spline + Remotion |
| Animations After Effects préexistantes | Lottie + `@remotion/lottie` |
| 3D complexe avec keyframing visuel | Three.js + Theatre.js + R3F |
| Simples retournements de cartes 3D, sans dépendance | Transformations 3D CSS |
| Site web, défilement piloté | GSAP + Three.js |

## Statut d'intégration avec Remotion {#remotion-integration-status}

| Bibliothèque | Statut | Paquet |
|--------------|--------|--------|
| React Three Fiber | Officiel | `@remotion/three` |
| Lottie | Officiel | `@remotion/lottie` |
| Spline | Documenté | via `@remotion/three` |
| Transformations 3D CSS | Natif | CSS React standard |
| GSAP | Manuel | nécessite un adaptateur de frames |
| Rive | Aucun | - |
| Babylon.js | Aucun | - |
| tsParticles | Manuel | via capture de canvas |

## Moteurs 3D complets {#full-3d-engines}

### React Three Fiber (R3F) - 9/10 pour la vidéo produit {#react-three-fiber-r3f-910-for-product-video}

Renderer React pour Three.js. API de composants déclarative : les scènes sont des arbres JSX.

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

**Différence clé avec R3F autonome :** utiliser `useCurrentFrame()` à la place de `useFrame()`. Remotion contrôle l'horloge.

**Écosystème :**
- `@react-three/drei` - utilitaires (OrbitControls, Environment, Text, etc.)
- `@react-three/postprocessing` - bloom, profondeur de champ, aberration chromatique
- Leva - contrôles d'interface pour le développement

**Modèle officiel :** `remotion-template-three`

### Three.js - 8/10 pour la vidéo produit {#threejs-810-for-product-video}

Plus bas niveau que R3F. Plus de contrôle, plus de code répétitif. À utiliser lorsque les abstractions de R3F sont limitantes.

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

**Skills Claude Code pour Three.js :**
- `github.com/OpenAEC-Foundation/Three.js-Claude-Skill-Package` - 24 skills (WebGL, WebGPU, R3F, Drei, physique, IFC)
- `github.com/CloudAI-X/threejs-skills` - fondamentaux
- `github.com/dgreenheck/webgpu-claude-skill` - WebGPU + Three.js
- `github.com/Nice-Wolf-Studio/claude-skills-threejs-ecs-ts` - Three.js + ECS + TypeScript
- `github.com/freshtechbro/claudedesignskills` - plus de 20 skills, dont R3F

### Babylon.js - 5/10 pour la vidéo produit {#babylonjs-510-for-product-video}

Moteur de jeu complet : physique, audio, XR, éditeur visuel. Surdimensionné pour les vidéos produit. Aucune intégration Remotion.

Cas d'usage : expériences 3D interactives, configurateurs, jeux - pas le rendu vidéo.

## 3D sans code / visuelle {#no-code-visual-3d}

### Spline (spline.design) - 9/10 pour la vidéo produit {#spline-splinedesign-910-for-product-video}

Meilleur flux de travail designer-développeur : le designer construit la scène dans l'éditeur du navigateur, le développeur l'anime via Remotion.

**Fonctionnalités (2026) :** texte vers 3D, image vers 3D, aperçu Apple Vision Pro, collaboration en temps réel.

**Tarifs :** Gratuit / 12 $ Starter / 20 $ Pro / 36 $ Team

**Intégration Remotion :** documentée via `@remotion/three`. Importer les fichiers `.splinecode`.

```tsx
import Spline from '@splinetool/react-spline';

// Wrap in ThreeCanvas or use as React component
// Animate Spline object properties via frame-driven state
```

**Flux de travail :** éditeur Spline → export de la scène → import dans Remotion → piloter l'animation avec `useCurrentFrame()`.

**Skills Claude Code :** `freshtechbro/claudedesignskills` inclut `spline-interactive`.

### Theatre.js - 7/10 pour la vidéo produit {#theatrejs-710-for-product-video}

Éditeur de timeline visuel pour les animations Three.js/R3F. Keyframing, éditeur de séquences, graphe de scène. v0.5 : tous les types de propriétés sont séquençables.

Pas d'intégration directe avec Remotion : exporter les animations puis les piloter à partir des données de frames.

Idéal pour : créer visuellement des animations 3D complexes, puis les figer en données de keyframes pour Remotion.

## Bibliothèques d'animation {#animation-libraries}

### Lottie - 7/10 pour la vidéo produit {#lottie-710-for-product-video}

Animations After Effects exportées en JSON. Paquet officiel Remotion.

```tsx
import { Lottie } from '@remotion/lottie';
import { staticFile } from 'remotion';

<Lottie
  animationData={require('./animation.json')}
  // or
  src={staticFile('animations/loading.json')}
/>
```

**Bibliothèque :** LottieFiles.com - des milliers d'animations gratuites. Filtrer par catégorie, télécharger le JSON.

**Performances par rapport à Rive :** les fichiers Lottie sont environ 4 fois plus volumineux et environ 4 fois plus lents à analyser. Pour le rendu vidéo, cela compte moins que pour le web interactif.

### Rive (rive.app) - 6/10 pour la vidéo produit {#rive-riveapp-610-for-product-video}

Animations interactives avec machines à états. Fichiers inférieurs de 90 % à Lottie, production 4 fois plus rapide. Utilisé par Spotify, Duolingo, Disney.

Aucune intégration Remotion. Idéal pour les animations d'interface interactives, pas pour le rendu vidéo.

### GSAP + ScrollTrigger - 5/10 pour la vidéo produit {#gsap-scrolltrigger-510-for-product-video}

Bibliothèque d'animation web la plus puissante. Excellente pour les sites à défilement piloté. Non conçue pour le rendu vidéo image par image.

Aucune intégration directe avec Remotion : GSAP fonctionne en temps réel, Remotion en numéros de frames. Nécessite un adaptateur personnalisé pour convertir `useCurrentFrame()` en position de timeline GSAP.

À utiliser hors de Remotion pour : pages d'accueil, sites portfolio, animations de défilement.

**Skills Claude Code :** `freshtechbro/claudedesignskills` inclut `gsap-scrolltrigger`.

### Anime.js - 4/10 pour la vidéo produit {#animejs-410-for-product-video}

Animation DOM légère (~17 Ko, version lite 3 Ko). La v4.3.0 (janv. 2026) ajoute `createLayout()` pour animer entre des états de mise en page. Aucune intégration Remotion.

À utiliser pour : animations d'interface web, pas pour le rendu vidéo.

### Motion Canvas - 6/10 pour la vidéo produit {#motion-canvas-610-for-product-video}

Bibliothèque TypeScript pour les animations vidéo programmatiques. Concurrent de Remotion orienté contenus pédagogiques et explicatifs. Fork : Revideo (cible de migration en production).

**Quand le choisir plutôt que Remotion :** vidéos explicatives riches en mathématiques, animations de diagrammes programmatiques. Pas pour les présentations produit ou le marketing.

**Skills Claude Code :** `apoorvlathey/motion-canvas-skills` sur agentskills.so.

## Effets légers {#lightweight-effects}

### Transformations 3D CSS - 6/10 pour la vidéo produit {#css-3d-transforms-610-for-product-video}

Transformations de perspective natives. Aucune dépendance. Fonctionne dans Remotion comme du CSS React standard.

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

Adapté à : retournements de cartes, pages de livre, transformations 3D simples. Pas pour les scènes 3D complexes.

### tsParticles - 6/10 comme élément d'accent {#tsparticles-610-as-accent-element}

Effets de particules (confettis, feux d'artifice, particules flottantes). Intégrations React, Vue, Svelte, Angular.

Pas d'intégration officielle avec Remotion. Peut être capturé via canvas puis injecté comme calque vidéo.

À utiliser comme accent ou arrière-plan, pas comme contenu principal.

### Vanta.js - 5/10 pour la vidéo produit {#vantajs-510-for-product-video}

Arrière-plans animés préconçus : oiseaux, vagues, globe, brouillard, nuages. Nécessite Three.js ou p5.js.

Pas d'intégration Remotion sans capture de canvas. Convient comme texture d'arrière-plan dans les prises de vue produit.

## Rendu 2D {#2d-rendering}

### Pixi.js - 4/10 pour la vidéo produit {#pixijs-410-for-product-video}

Moteur de rendu 2D WebGL/WebGPU le plus rapide. Excellent pour les jeux et la 2D interactive. Aucune intégration Remotion.

### p5.js - 3/10 pour la vidéo produit {#p5js-310-for-product-video}

Programmation créative (Processing pour JavaScript). Art génératif, visualisations. Aucune intégration Remotion sans capture de canvas.

## Comparatif de performances {#performance-comparison}

| Bibliothèque | Taille du bundle | Temps d'analyse | Usage GPU | Rendu dans Remotion |
|--------------|------------------|-----------------|-----------|---------------------|
| CSS 3D | 0 Ko | 0 ms | Faible | Natif |
| Lottie | ~40 Ko | Rapide | Faible | Officiel |
| Three.js | ~600 Ko | Moyen | Élevé | Via `@remotion/three` |
| R3F | ~800 Ko | Moyen | Élevé | Officiel |
| Babylon.js | ~2 Mo | Lent | Élevé | Aucun |
| GSAP | ~100 Ko | Rapide | Faible | Adaptateur manuel |

## Écosystème de skills Claude Code {#claude-code-skills-ecosystem}

### Collections principales {#primary-collections}

**freshtechbro/claudedesignskills** (collection principale)
- Plus de 20 skills dans un seul plugin : Three.js, R3F, GSAP, Babylon.js, PlayCanvas, Pixi.js, Lottie, Rive, Spline, Anime.js, A-Frame
- `github.com/freshtechbro/claudedesignskills`

**OpenAEC-Foundation/Three.js-Claude-Skill-Package**
- 24 skills Three.js déterministes : WebGL, WebGPU, R3F, Drei, physique, IFC
- `github.com/OpenAEC-Foundation/Three.js-Claude-Skill-Package`

### Spécialisées {#specialized}

- `github.com/CloudAI-X/threejs-skills` - fondamentaux Three.js
- `github.com/dgreenheck/webgpu-claude-skill` - WebGPU + Three.js
- `github.com/Nice-Wolf-Studio/claude-skills-threejs-ecs-ts` - Three.js + ECS + TypeScript (développement de jeux)

## TOP 5 pour les vidéos produit {#top-5-for-product-videos}

1. **R3F + `@remotion/three`** - 9/10 - 3D complète dans la vidéo, support officiel, natif React
2. **Spline + Remotion** - 9/10 - conception 3D sans code + vidéo programmatique
3. **Three.js + `@remotion/three`** - 8/10 - contrôle maximal
4. **Lottie + `@remotion/lottie`** - 7/10 - animations prêtes à l'emploi, rapide
5. **Theatre.js + R3F** - 7/10 - timeline visuelle pour animations 3D complexes

## Pièges à éviter {#gotchas}

- **`useFrame()` de R3F ne fonctionne pas dans Remotion.** Le remplacer par `useCurrentFrame()` de Remotion. L'horloge de frames de Remotion pilote toutes les animations : l'horloge interne de R3F est contournée.
- **La capture de canvas pour les bibliothèques non intégrées produit des frames incohérentes.** Lors de la capture de bibliothèques comme GSAP ou Vanta.js via canvas, le timing des frames dépend de l'exécution en temps réel. Pendant un rendu headless rapide, des frames peuvent être sautées ou dupliquées. Privilégier les intégrations officielles.
- **Les scènes Spline se chargent de manière asynchrone.** Dans Remotion, la scène doit être entièrement chargée avant que les frames ne soient rendues. Encapsuler les composants Spline dans un garde de chargement, ou utiliser `delayRender()` / `continueRender()`.
- **La géométrie Three.js coûte cher à chaque frame si elle est recréée.** Créer la géométrie dans le corps du composant (exécuté une seule fois), et non dans la logique de rendu. Utiliser `useMemo` pour les matériaux et les géométries.
- **Un bundle Babylon.js de 2 Mo alourdit les démarrages à froid de Lambda.** Pour les pipelines vidéo sur AWS Lambda, les bundles lourds augmentent le temps de démarrage à froid. Privilégier Three.js ou R3F.
- **La position dans une timeline GSAP n'est pas un numéro de frame Remotion.** `seek(time)` de GSAP utilise des secondes, Remotion utilise des frames. L'adaptateur : `timeline.seek(frame / fps)` avant le rendu.

## Voir aussi {#see-also}

- [[remotion-programmatic-video]]
- [[css-animation-and-transforms]]
- [[react-components-and-jsx]]
- [[video-motion-design-rules]]
