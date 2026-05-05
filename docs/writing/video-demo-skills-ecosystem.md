# Video Demo Skills Ecosystem

Claude Code skill collections and libraries for building programmatic video demos, presentations, and marketing content.

## Remotion-Based Video Production

### Official Skills

```bash
npx skills add remotion-dev/skills
```

First-party Remotion skills. Covers standard video composition patterns, component lifecycle, and render pipeline.

### Community Toolkits

| Toolkit | Focus |
|---|---|
| `digitalsamba/claude-code-video-toolkit` | Product demos, walkthroughs, explainers. ElevenLabs/Qwen3-TTS voiceover, ACE-Step 1.5 music, dark tech aesthetic |
| `wilwaldon/Claude-Code-Video-Toolkit` | Remotion + Manim + screen recording + YouTube clipping + FFmpeg |
| `BayramAnnakov/remotion-video-director` | Interactive deliberation: thinking → designing → building → reviewing |
| `wshuyi/remotion-video-skill` | Standalone skill with AI TTS audio |
| `jhartquist/claude-remotion-kickstart` | Starter kit with pre-built components |
| `Ashad001/remotion-transitions` | Custom scene transitions with animation math |
| `jezweb/claude-skills (walkthrough-video)` | Generates walkthrough videos from screenshots or live sites |

### Apple-Style Animation Reference

- `remotion-dev/apple-wow-tutorial` — official tutorial recreating Apple's signature animation style
- Remotion Showcase: remotion.dev/showcase
- Product demo prompt reference: remotion.dev/prompts/product-demo-for-presscut

## Presentation Design

```bash
# Web-based slides via Reveal.js
/presentation

# Frontend-slides command
/frontend-slides
```

| Skill | Output |
|---|---|
| `coleam00/second-brain-skills (pptx-generator)` | 16 slide layouts + 5 carousel formats; configure brand first |
| `zarazhangrui/frontend-slides` | Web-based slides |
| Reveal Presentations plugin | HTML decks via Reveal.js |
| `Rosetree-Solutions/google-slides-generator` | .pptx + Google Slides |
| `HungHsunHan/claude-code-ppt-generation-team` | Multi-agent pipeline: photos → PowerPoint |

## Marketing Content Skills

### Full Marketing Pack

```bash
npx skillkit install coreyhaines31/marketingskills
```

Covers: copywriting, CRO, SEO, analytics, positioning, lead-magnet, direct-response. Fork available at `mysticaltech/marketingskills`.

### Landing Page & Copywriting (MCPMarket.com)

- Landing Page Builder, Designer, Launchpad, GTM Content Generator, CRO Expert
- Conversion Copywriter, Copywriter Agent, Marketing Copywriter

## Content Extraction & Brand Voice

- NLP & Text Analysis skill (MCPMarket)
- YouTube Comment Analysis (MCPMarket)
- `affaan-m/content-engine` + `brand-voice` skills
- `coleam00/brand` & voice generator

## React / HTML5 Component Skills

| Skill | Output |
|---|---|
| `bknddevelopment/claude-magic-ui` | Natural language → React components |
| React Component Generator (MCPMarket) | Functional React + TypeScript scaffolding |
| Magic UI Component Builder (MCPMarket) | Production-grade React/TS |
| `neonwatty/css-animation-skill` | Self-contained HTML/CSS animations; extracts design language from live app |
| Anthropic `frontend-design` skill | Design system philosophy (277K+ installs) |
| `nafiurrahmanniloy/figma-skill` | Figma-to-code for 7 frameworks |

## Mega-Collections

| Collection | Size |
|---|---|
| `affaan-m/everything-claude-code` | 156+ skills |
| `coleam00/second-brain-skills` | Video + PPTX + brand |
| `panaversity/claude-code-skills-lab` | Remotion for commercials, demos, social |
| `VoltAgent/awesome-agent-skills` | 1000+ agent skills, cross-tool compatible |
| `Mindrally/skills` | 240+ skills ported from Cursor rules |

## Foundational Library: pretext

[chenglou/pretext](https://github.com/chenglou/pretext) — pure JS text measurement and layout without DOM reflow.

Key capabilities:
- Precise text positioning
- Shrink-to-fit behavior
- Balanced line breaks
- 100+ language support

Particularly useful inside Remotion: avoids expensive DOM reflow per frame during rendering, making it reliable for programmatic typography at scale.

```js
// Example: measure text without touching the DOM
import { measureText } from 'pretext';
const { width, height } = measureText('Hello', { font: 'Inter', size: 32 });
```

## Recommended Stack for Product Demo Pipeline

1. `remotion-dev/skills` — foundation layer
2. `digitalsamba/claude-code-video-toolkit` — product demo templates with TTS/music
3. `remotion-dev/apple-wow-tutorial` — Apple aesthetic patterns as reference
4. `coleam00/second-brain-skills pptx-generator` — presentation output
5. `coreyhaines31/marketingskills` — value proposition extraction and copy

## Gotchas

- **Issue:** `coleam00/second-brain-skills pptx-generator` produces unstyled slides → **Fix:** run brand setup step first before generating any slides; the generator pulls brand config from a prior step
- **Issue:** Remotion renders hang or produce blank frames when using DOM-dependent text measurement → **Fix:** replace DOM-based measurement with `pretext` to avoid per-frame reflow inside the render pipeline
- **Issue:** `coreyhaines31/marketingskills` install fails silently if `skillkit` is not available → **Fix:** confirm `npx skillkit` resolves before install; fallback is cloning the repo and installing skills manually
- **Issue:** `BayramAnnakov/remotion-video-director` enters a loop on "reviewing" phase without producing output → **Fix:** provide explicit acceptance criteria in the initial prompt; the deliberation flow needs a termination condition

## See Also

- [[automated-video-production-and-post-production-toolkits]]
- [[video-narrative-design-and-scripting-pipelines]]
- [[4-layer-content-quality-framework]]
