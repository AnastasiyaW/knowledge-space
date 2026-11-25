---
level: 3
source_sha256: b7536e5cae66881006e79c82b36569f38381f5e876d2b186202eb5aa2c81041f
translation: machine
translated_at: '2026-10-24'
---
# Écosystème des skills de vidéo de démonstration {#video-demo-skills-ecosystem}

Collections de skills et bibliothèques pour Claude Code, destinées à la création programmatique de vidéos de démonstration, de présentations et de contenus marketing.

## Production vidéo basée sur Remotion {#remotion-based-video-production}

### Skills officiels {#official-skills}

```bash
npx skills add remotion-dev/skills
```

Skills officiels de Remotion. Couvre les patterns standard de composition vidéo, le cycle de vie des composants et le pipeline de rendu.

### Boîtes à outils communautaires {#community-toolkits}

| Boîte à outils | Axe principal |
|---|---|
| `digitalsamba/claude-code-video-toolkit` | Démos produit, parcours guidés, vidéos explicatives. Voix off ElevenLabs/Qwen3-TTS, musique ACE-Step 1.5, esthétique tech sombre |
| `wilwaldon/Claude-Code-Video-Toolkit` | Remotion + Manim + capture d'écran + découpage YouTube + FFmpeg |
| `BayramAnnakov/remotion-video-director` | Délibération interactive : réflexion → conception → construction → revue |
| `wshuyi/remotion-video-skill` | Skill autonome avec audio généré par TTS |
| `jhartquist/claude-remotion-kickstart` | Kit de démarrage avec composants préconstruits |
| `Ashad001/remotion-transitions` | Transitions de scène personnalisées avec calculs d'animation |
| `jezweb/claude-skills (walkthrough-video)` | Génère des vidéos de parcours à partir de captures d'écran ou de sites en ligne |

### Référence d'animation de style Apple {#apple-style-animation-reference}

- `remotion-dev/apple-wow-tutorial` : tutoriel officiel reproduisant la signature d'animation d'Apple
- Vitrine Remotion : remotion.dev/showcase
- Référence de prompts pour démos produit : remotion.dev/prompts/product-demo-for-presscut

## Conception de présentations {#presentation-design}

```bash
# Web-based slides via Reveal.js
/presentation

# Frontend-slides command
/frontend-slides
```

| Skill | Sortie |
|---|---|
| `coleam00/second-brain-skills (pptx-generator)` | 16 mises en page de diapositives + 5 formats de carrousel ; configurer la marque en premier |
| `zarazhangrui/frontend-slides` | Diapositives pour le web |
| Plugin Reveal Presentations | Présentations HTML via Reveal.js |
| `Rosetree-Solutions/google-slides-generator` | .pptx + Google Slides |
| `HungHsunHan/claude-code-ppt-generation-team` | Pipeline multi-agents : photos → PowerPoint |

## Skills de contenu marketing {#marketing-content-skills}

### Pack marketing complet {#full-marketing-pack}

```bash
npx skillkit install coreyhaines31/marketingskills
```

Couvre : rédaction, CRO, SEO, analytics, positionnement, lead magnets et marketing à réponse directe. Un fork est disponible sur `mysticaltech/marketingskills`.

### Pages de destination et rédaction (MCPMarket.com) {#landing-page-copywriting-mcpmarketcom}

- Landing Page Builder, Designer, Launchpad, GTM Content Generator, CRO Expert
- Conversion Copywriter, Copywriter Agent, Marketing Copywriter

## Extraction de contenu et voix de marque {#content-extraction-brand-voice}

- Skill NLP et analyse de texte (MCPMarket)
- Analyse des commentaires YouTube (MCPMarket)
- `affaan-m/content-engine` + skills `brand-voice`
- `coleam00/brand` et générateur de voix

## Composants React / HTML5 {#react-html5-component-skills}

| Skill | Sortie |
|---|---|
| `bknddevelopment/claude-magic-ui` | Langage naturel → composants React |
| React Component Generator (MCPMarket) | Squelettes React fonctionnels + TypeScript |
| Magic UI Component Builder (MCPMarket) | React/TS de qualité production |
| `neonwatty/css-animation-skill` | Animations HTML/CSS autonomes ; extrait le langage visuel d'une application en ligne |
| Skill `frontend-design` d'Anthropic | Philosophie de système de design (plus de 277 000 installations) |
| `nafiurrahmanniloy/figma-skill` | Figma vers code pour 7 frameworks |

## Collections majeures {#mega-collections}

| Collection | Taille |
|---|---|
| `affaan-m/everything-claude-code` | Plus de 156 skills |
| `coleam00/second-brain-skills` | Vidéo + PPTX + marque |
| `panaversity/claude-code-skills-lab` | Remotion pour publicités, démos et réseaux sociaux |
| `VoltAgent/awesome-agent-skills` | Plus de 1 000 skills d'agents, compatibles entre outils |
| `Mindrally/skills` | Plus de 240 skills portés depuis les règles Cursor |

## Bibliothèque de référence : pretext {#foundational-library-pretext}

[chenglou/pretext](https://github.com/chenglou/pretext) : mesure et mise en page de texte en JS pur, sans reflow du DOM.

Fonctionnalités clés :
- Positionnement précis du texte
- Réduction automatique pour tenir dans l'espace disponible
- Coupures de lignes équilibrées
- Prise en charge de plus de 100 langues

Particulièrement utile dans Remotion : il évite un reflow DOM coûteux à chaque image pendant le rendu, ce qui le rend fiable pour une typographie programmatique à grande échelle.

```js
// Example: measure text without touching the DOM
import { measureText } from 'pretext';
const { width, height } = measureText('Hello', { font: 'Inter', size: 32 });
```

## Pile recommandée pour un pipeline de démo produit {#recommended-stack-for-product-demo-pipeline}

1. `remotion-dev/skills` : couche de fondation
2. `digitalsamba/claude-code-video-toolkit` : modèles de démo produit avec TTS/musique
3. `remotion-dev/apple-wow-tutorial` : patterns esthétiques Apple comme référence
4. `coleam00/second-brain-skills pptx-generator` : sortie de présentation
5. `coreyhaines31/marketingskills` : extraction de la proposition de valeur et rédaction

## Pièges courants {#gotchas}

- **Problème :** `coleam00/second-brain-skills pptx-generator` produit des diapositives sans style → **Solution :** exécuter l'étape de configuration de la marque avant de générer les diapositives ; le générateur récupère la configuration de marque d'une étape précédente
- **Problème :** les rendus Remotion se bloquent ou produisent des images vides lorsque la mesure du texte dépend du DOM → **Solution :** remplacer la mesure basée sur le DOM par `pretext` pour éviter un reflow à chaque image dans le pipeline de rendu
- **Problème :** l'installation de `coreyhaines31/marketingskills` échoue silencieusement si `skillkit` n'est pas disponible → **Solution :** vérifier que `npx skillkit` se résout avant l'installation ; en repli, cloner le dépôt et installer les skills manuellement
- **Problème :** `BayramAnnakov/remotion-video-director` boucle indéfiniment en phase de « revue » sans produire de sortie → **Solution :** fournir des critères d'acceptation explicites dans le prompt initial ; le flux de délibération a besoin d'une condition d'arrêt

## Voir aussi {#see-also}

- [[automated-video-production-and-post-production-toolkits]]
- [[video-narrative-design-and-scripting-pipelines]]
- [[4-layer-content-quality-framework]]
