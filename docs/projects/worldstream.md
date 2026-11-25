---
title: "Worldstream: worldstream-3d-world-model — Worldstream 3D World Model"
category: "projects"
date: 2026-10-22
tags: ["project", "worldstream", "worldstream-3d-world-model"]
aliases: ["Worldstream: worldstream-3d-world-model"]
---

# Worldstream: worldstream-3d-world-model — Worldstream 3D World Model

**Development line:** project:worldstream · thread worldstream-3d-world-model  
**Last event:** 2026-10-22 · 2 dated since 2026-10-22 · **Researched:** 2026-10-23 · confidence: high

## What it is

WorldStream is an open-ended, interactive 3D world model architecture. It is meant for simulation researchers and developers of virtual environments.

Abilities:

- Terrain streaming: generates continuous 3D terrain past the boundaries of a predefined map.
- Hierarchical planning: a macro scale lays out ecology and transport, a micro scale compiles individual tiles.
- Procedural compilation: deterministic code turns structured decisions into terrain, roads, vegetation, settlements and entities.
- Language control: open-ended natural language instructions change the world and steer entities in it.
- Persistence: user edits, boundary commitments and stateful NPC records survive when tiles unload and reload.

Throughput and spatial consistency depend on two things: accurate prediction of the motion corridor, and bounded budgets for procedural compilation. WorldStream is a viable structured alternative to black-box video or voxel generation, because it pairs symbolic planning with deterministic graphics compilation.

## Development line

- **2026-10-22 — WorldStream: streaming interactive 3D world model with hierarchical planning.** Researchers announced WorldStream, an open-ended 3D world model. It extends playable terrain beyond pre-specified maps, acts on open-ended language in the running world, and restores visited places with their edits. A hierarchical planner (Macro and Micro stages) hands its plans to deterministic local code, which compiles them into terrain, roads, settlements, vegetation and entities. The streaming design plans ahead along the predicted movement corridor.
- **2026-10-22 — WorldStream introduced as an open-ended interactive 3D world model.** A preprint dated 2026-10-22 presents WorldStream. The model extends playable terrain beyond a predefined map, acts on open-ended language instructions, and restores visited regions with their edits. Its hierarchical planner emits structured decisions for terrain, settlements and entities. Streaming compiles only the regions needed soon. A persistent world record keeps edits and stateful NPCs.
- **2026-10-22 — other reporting on this date.**
  - The paper specifies that the hierarchical planner works over a typed decision model. Macro planning governs groups of spatial tiles and sets the global ecological, hydrological and transport topology. Micro planning specializes these contracts to the measured local terrain and to boundary commitments with neighbouring tiles. Geometry behind the player's predicted movement corridor is actively unloaded, so memory stays within a bounded budget. (2026-10-22) — <https://arxiv.org/abs/2610.28827>
  - The paper details that the persistent world record is kept per tile. It stores seeds, mutable entity identities and boundary commitments, along with user attribute modifications. A returning tile is recompiled from these structured records, not re-inferred and not stored as a heavy raw mesh. (2026-10-22) — <https://arxiv.org/abs/2610.28827>

## What changed

The initial research established the core WorldStream framework. It moves open-ended world generation from monolithic offline synthesis to decoupled streaming execution. The architecture introduced:

- two-tier hierarchical planning across tile clusters and local cells;
- deterministic procedural compilation, to reduce the memory footprint;
- per-tile persistent state, so edits hold when a region is revisited.

## How to use this

1. Set the global generation seeds and environmental priors. They initialize the Macro planning layer for regional ecology, hydrology and transit networks.
  — <https://arxiv.org/abs/2610.28827>
2. Supply the agent's position and heading vectors to project the movement corridor. This triggers Micro planning ahead of time for the tiles coming up next.
  — <https://arxiv.org/abs/2610.28827>
3. Run local deterministic procedural compilation. It turns approved Micro plan decisions into renderable 3D terrain, vegetation and settlement assets.
  — <https://arxiv.org/abs/2610.28827>
4. Issue natural language commands to update runtime entities or tile attributes. Modified states persist to the per-tile world record database.
  — <https://arxiv.org/abs/2610.28827>

## Best practices

- Keep planning horizons separate from geometry compilation along predicted corridors, so frame rates stay stable and compute does not spike.
  — <https://arxiv.org/abs/2610.28827>
- Enforce strict tile-to-tile boundary commitments in the Micro planner, so independently compiled cells do not show visual or topological seams.
  — <https://arxiv.org/abs/2610.28827>
- When the agent travels large distances, recompile from per-tile seed and mutation records instead of caching high-poly meshes in memory.
  — <https://arxiv.org/abs/2610.28827>

## Superseded by this

- Monolithic offline 3D world generation, which confines simulation to static pre-computed maps with no infinite dynamic streaming.
  — <https://arxiv.org/abs/2610.28827>
- Stateless streaming, which discards user terrain edits and NPC interaction history when a tile is evicted.
  — <https://arxiv.org/abs/2610.28827>

## Still unknown

- Independent external runtime benchmarks and the availability of open-source code are unverified until a public repository is released.
- Community evaluations and practitioner usage reports have not yet appeared; the preprint was released on October 22, 2026.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2610.28827 | WorldStream: Streaming Interactive 3D Worlds with Hierarchical Planning and Persistent State | 2026-10-23 |

## Agent brief {#agent-brief}

- **Subject:** project:worldstream, thread worldstream-3d-world-model, 2 dated events 2026-10-22 → 2026-10-22.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
