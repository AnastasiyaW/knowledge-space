---
title: "Yumina: yumina-open-source-engine-releases — Yumina Open Source Engine Releases"
category: "projects"
date: 2026-11-26
tags: ["project", "yumina", "yumina-open-source-engine-releases"]
aliases: ["Yumina: yumina-open-source-engine-releases"]
---

# Yumina: yumina-open-source-engine-releases — Yumina Open Source Engine Releases

Yumina is an open-source world engine and web player for interactive fiction, visual novels and roleplay, for authors who have outgrown SillyTavern.

**Development line:** project:yumina · thread yumina-open-source-engine-releases  
**Last event:** 2026-11-26 · 2 dated since 2026-11-26 · **Researched:** 2026-11-27 · confidence: high

## What it is

Yumina is an open-source world engine and web runtime for authors of interactive fiction, visual novels and roleplay simulations. It suits those who need LLM-driven story state, which pure text chat tools like SillyTavern do not give. It combines an editor, a story player and an execution engine.

What it does:

- Character animation: turns a single 2D character portrait into a reactive multi-layer figure with idle motion, cursor tracking and VTube Studio input.
- State-machine orchestration: runs across OpenAI, Anthropic, Google, OpenRouter and Ollama endpoints.
- Persistence: Drizzle ORM on embedded PGlite or PostgreSQL.
- Media: web-based playback.

It needs Node.js 22 and pnpm. Python 3 with Pillow and FFmpeg is optional, for processing animated graphics. The engine is the open-source, self-hosted baseline next to the commercial hosted platform at yumina.io.

## Development line

- **2026-11-26 — Yumina open-source engine adds single-image 2D character animation and VTube Studio support.** Yumina is an open-source engine for AI-driven visual novels, RPGs and interactive worlds. It is presented as turning a single image into an animated 2D character that blinks, breathes, tracks the cursor and reacts to webcam input and VTube Studio. It is described as having grown from a SillyTavern fork with Godot integration. It runs locally via GitHub, or in the cloud at yumina.io.
- **2026-11-26 — Yumina open-source engine adds single-image 2D character animation and VTube Studio support.** The open-source Yumina engine is described as a base for AI-driven games and interactive characters. A single uploaded image can become a multilayer 2D character with blinking, breathing, cursor tracking, webcam and VTube Studio support. It is described as a local service (engine, editor and player), deployed locally from GitHub or hosted in the cloud at yumina.io.
- **2026-11-26 — other reporting on this date.**
  - The open-source repository documents a full-stack engine, a visual editor and a web player. They are written in framework-free TypeScript, with Hono API routing, Drizzle ORM on PGlite or PostgreSQL, and a React 19 frontend using TanStack Router and Zustand. (2026-11-26) — <https://github.com/lovetimo0421/yumina-oss>
  - It connects natively to OpenRouter, Anthropic, OpenAI, Google and local Ollama endpoints. It links self-hosted GitHub deployments with cloud-hosted player spaces on yumina.io. (2026-11-26) — <https://github.com/lovetimo0421/yumina-oss>

## What changed

The project moved from a SillyTavern fork to an independent AI-native world engine. It now combines full game state management with visual novel mechanics.

The core is modular:

- a framework-free TypeScript engine
- a Hono API server
- Drizzle ORM persistence with embedded PGlite
- a React 19 interface

Characters are no longer only static 2D portraits. They are animated multi-layer rigs with idle breathing, eye blinking, cursor tracking, webcam control and VTube Studio integration.

## How to use this

1. Clone the repository with git clone https://github.com/lovetimo0421/yumina-oss.git and enter the directory.
  — <https://github.com/lovetimo0421/yumina-oss>
2. Install dependencies with pnpm install, on Node.js 22 or higher.
  — <https://github.com/lovetimo0421/yumina-oss>
3. Start the local engine and editor with pnpm start. Then add your model API credentials, or point it at a local Ollama instance.
  — <https://github.com/lovetimo0421/yumina-oss>

## Best practices

- Install Python 3 with Pillow and FFmpeg before uploading animated covers or generating multi-frame character assets, so asset conversion does not fail.
  — <https://github.com/lovetimo0421/yumina-oss>
- Use embedded PGlite for quick desktop work with no configuration. Move to dedicated PostgreSQL for persistent multi-user setups.
  — <https://github.com/lovetimo0421/yumina-oss>

## Superseded by this

- In standard roleplay interfaces like SillyTavern, animated sprites, screen transitions and game variables needed external visual novel plugins or separate frontend scripts.
  — <https://github.com/lovetimo0421/yumina-oss>

## Still unknown

- Exact version tags and Git commit hashes for the single-image 2D character rigging release are not given in the top-level project documentation.
- Community discussion threads could not be resolved to public thread URLs, so none are included.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/lovetimo0421/yumina-oss | lovetimo0421/yumina-oss: AI-native world engine and platform for interactive fiction, text adventures, and visual novels | 2026-11-27 |
| https://yumina.io/ | Yumina - AI-native interactive storytelling platform | 2026-11-27 |

## Agent brief {#agent-brief}

- **Subject:** project:yumina, thread yumina-open-source-engine-releases, 2 dated events 2026-11-26 → 2026-11-26.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** high. The dated entries under "Superseded by this" decide what is obsolete.
