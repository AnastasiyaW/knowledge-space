---
level: 3
source_sha256: b7536e5cae66881006e79c82b36569f38381f5e876d2b186202eb5aa2c81041f
translation: machine
translated_at: '2026-10-24'
---
# Ökosystem für Video-Demo-Skills {#video-demo-skills-ecosystem}

Skill-Sammlungen und Bibliotheken für Claude Code zum programmatischen Erstellen von Video-Demos, Präsentationen und Marketinginhalten.

## Remotion-basierte Videoproduktion {#remotion-based-video-production}

### Offizielle Skills {#official-skills}

```bash
npx skills add remotion-dev/skills
```

Erste-Hand-Skills von Remotion. Deckt Standardmuster für Videokomposition, Komponenten-Lebenszyklus und die Render-Pipeline ab.

### Community-Toolkits {#community-toolkits}

| Toolkit | Schwerpunkt |
|---|---|
| `digitalsamba/claude-code-video-toolkit` | Produkt-Demos, Walkthroughs, Erklärvideos. ElevenLabs/Qwen3-TTS-Voiceover, ACE-Step-1.5-Musik, dunkle Tech-Ästhetik |
| `wilwaldon/Claude-Code-Video-Toolkit` | Remotion + Manim + Bildschirmaufnahme + YouTube-Clipping + FFmpeg |
| `BayramAnnakov/remotion-video-director` | Interaktive Abwägung: Denken → Gestalten → Bauen → Prüfen |
| `wshuyi/remotion-video-skill` | Eigenständiger Skill mit KI-TTS-Audio |
| `jhartquist/claude-remotion-kickstart` | Starter-Kit mit vorgefertigten Komponenten |
| `Ashad001/remotion-transitions` | Eigene Szenenübergänge mit Animationsmathematik |
| `jezweb/claude-skills (walkthrough-video)` | Erzeugt Walkthrough-Videos aus Screenshots oder Live-Websites |

### Referenz für Apple-Stil-Animationen {#apple-style-animation-reference}

- `remotion-dev/apple-wow-tutorial`: offizielles Tutorial, das Apples typischen Animationsstil nachbildet
- Remotion Showcase: remotion.dev/showcase
- Referenz für Produkt-Demo-Prompts: remotion.dev/prompts/product-demo-for-presscut

## Präsentationsdesign {#presentation-design}

```bash
# Web-based slides via Reveal.js
/presentation

# Frontend-slides command
/frontend-slides
```

| Skill | Ergebnis |
|---|---|
| `coleam00/second-brain-skills (pptx-generator)` | 16 Folienlayouts + 5 Karussell-Formate; zuerst Marke konfigurieren |
| `zarazhangrui/frontend-slides` | Webbasierte Folien |
| Reveal Presentations plugin | HTML-Decks über Reveal.js |
| `Rosetree-Solutions/google-slides-generator` | .pptx + Google Slides |
| `HungHsunHan/claude-code-ppt-generation-team` | Multi-Agenten-Pipeline: Fotos → PowerPoint |

## Skills für Marketinginhalte {#marketing-content-skills}

### Komplettes Marketing-Paket {#full-marketing-pack}

```bash
npx skillkit install coreyhaines31/marketingskills
```

Abdeckung: Copywriting, CRO, SEO, Analytics, Positionierung, Lead-Magnete, Direct Response. Fork verfügbar unter `mysticaltech/marketingskills`.

### Landingpages & Copywriting (MCPMarket.com) {#landing-page-copywriting-mcpmarketcom}

- Landing Page Builder, Designer, Launchpad, GTM Content Generator, CRO Expert
- Conversion Copywriter, Copywriter Agent, Marketing Copywriter

## Inhaltsextraktion & Markenstimme {#content-extraction-brand-voice}

- NLP- & Textanalyse-Skill (MCPMarket)
- YouTube-Kommentaranalyse (MCPMarket)
- `affaan-m/content-engine` + `brand-voice`-Skills
- `coleam00/brand` & Voice-Generator

## React-/HTML5-Komponenten-Skills {#react-html5-component-skills}

| Skill | Ergebnis |
|---|---|
| `bknddevelopment/claude-magic-ui` | Natürliche Sprache → React-Komponenten |
| React Component Generator (MCPMarket) | Funktionales React + TypeScript-Gerüst |
| Magic UI Component Builder (MCPMarket) | Produktionsreifes React/TS |
| `neonwatty/css-animation-skill` | In sich geschlossene HTML/CSS-Animationen; extrahiert die Designsprache aus einer laufenden App |
| Anthropic `frontend-design`-Skill | Designsystem-Philosophie (über 277.000 Installationen) |
| `nafiurrahmanniloy/figma-skill` | Figma-zu-Code für 7 Frameworks |

## Mega-Sammlungen {#mega-collections}

| Sammlung | Umfang |
|---|---|
| `affaan-m/everything-claude-code` | 156+ Skills |
| `coleam00/second-brain-skills` | Video + PPTX + Marke |
| `panaversity/claude-code-skills-lab` | Remotion für Werbespots, Demos, Social Media |
| `VoltAgent/awesome-agent-skills` | 1000+ Agent-Skills, toolübergreifend kompatibel |
| `Mindrally/skills` | 240+ Skills, portiert aus Cursor-Regeln |

## Grundlegende Bibliothek: pretext {#foundational-library-pretext}

[chenglou/pretext](https://github.com/chenglou/pretext) — reine JS-Textmessung und Layout ohne DOM-Reflow.

Zentrale Fähigkeiten:
- Präzise Textpositionierung
- Anpassung an die Breite (Shrink-to-fit)
- Ausgewogene Zeilenumbrüche
- Unterstützung für über 100 Sprachen

Besonders nützlich innerhalb von Remotion: Es vermeidet teuren DOM-Reflow pro Frame während des Renderns und ist dadurch für programmatische Typografie in großem Maßstab zuverlässig.

```js
// Example: measure text without touching the DOM
import { measureText } from 'pretext';
const { width, height } = measureText('Hello', { font: 'Inter', size: 32 });
```

## Empfohlener Stack für eine Produkt-Demo-Pipeline {#recommended-stack-for-product-demo-pipeline}

1. `remotion-dev/skills`: Basisschicht
2. `digitalsamba/claude-code-video-toolkit`: Produkt-Demo-Vorlagen mit TTS/Musik
3. `remotion-dev/apple-wow-tutorial`: Apple-Gestaltungsmuster als Referenz
4. `coleam00/second-brain-skills pptx-generator`: Präsentationsausgabe
5. `coreyhaines31/marketingskills`: Extraktion des Nutzenversprechens und Copy

## Stolpersteine {#gotchas}

- **Problem:** `coleam00/second-brain-skills pptx-generator` erzeugt unformatierte Folien → **Lösung:** Den Schritt zur Markeneinrichtung zuerst ausführen, bevor Folien generiert werden; der Generator bezieht die Markenkonfiguration aus einem vorherigen Schritt
- **Problem:** Remotion-Renderings hängen oder erzeugen leere Frames, wenn DOM-abhängige Textmessung verwendet wird → **Lösung:** DOM-basierte Messung durch `pretext` ersetzen, um DOM-Reflow pro Frame in der Render-Pipeline zu vermeiden
- **Problem:** Die Installation von `coreyhaines31/marketingskills` schlägt stillschweigend fehl, wenn `skillkit` nicht verfügbar ist → **Lösung:** Vor der Installation prüfen, dass `npx skillkit` aufgelöst wird; als Alternative das Repository klonen und die Skills manuell installieren
- **Problem:** `BayramAnnakov/remotion-video-director` gerät in der Phase „Prüfen“ in eine Schleife, ohne Ergebnis zu liefern → **Lösung:** Im initialen Prompt explizite Abnahmekriterien angeben; der Abwägungsablauf braucht eine Abbruchbedingung

## Siehe auch {#see-also}

- [[automated-video-production-and-post-production-toolkits]]
- [[video-narrative-design-and-scripting-pipelines]]
- [[4-layer-content-quality-framework]]
