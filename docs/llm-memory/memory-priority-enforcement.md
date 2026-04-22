# Memory Priority Enforcement

Pattern for structuring agent memory into always-load (critical) and on-demand (reference) tiers, with mechanical enforcement for the most critical rules. Convergence of 8 independent domains onto the same principle.

## Core Principle

If forgetting a rule causes irreversible consequences → always-load.  
Everything else → on-demand.

This is not a performance optimization. It is a safety property: critical context must survive context compaction, long sessions, and attention degradation.

## Always vs On-Demand Criteria

**Always-load** (qualify for any one):
1. **Irreversible consequences** — forgetting causes data loss, financial damage, production downtime, security breach
2. **Cross-session invariants** — rules that must not be violated regardless of task ("never delete without confirmation", "never use production GPU without checking allocation")
3. **User profile / preferences** — communication style, expertise level, tool preferences

**On-demand** (load when topic becomes relevant):
- Active project details (loaded when working on that project)
- Reference materials and methodologies
- Historical information and past incidents
- Specific tool integrations not in daily use

## Boeing Rule — Keep Always-Load Short

Aviation "memory items" (emergency procedures done from memory, no checklist):
- Typical: 3-4 items per emergency procedure
- Maximum: ~10 items (considered high)
- Above 10: checklist fatigue → critical items forgotten under stress

**For agent memory:** Always-load section should be 10-15 entries maximum. Above this, important items fall into the "lost in the middle" zone.

**Lost in the Middle (Liu et al. 2023, arxiv 2307.03172):** LLM performance follows a U-shape based on context position. Items at the beginning or end receive highest attention. Items in the middle degrade significantly. With 36 always-load entries, critical rules rank 5-35 in a long context — exactly the degraded zone.

## IAEA Two-Layer Principle

From IAEA INSAG-10 defense-in-depth: critical safety barriers must be independent and redundant. Relying on a single layer (rule) to enforce critical behavior fails under common-cause failure (context pressure, compaction, distraction).

**Applied:**
- Rule in CLAUDE.md/memory (describes WHY and HOW)
- Hook/script mechanical enforcement (executes regardless of context state)

**Examples of working pairs:**
```text
Documentation integrity:
  Rule → "validate file references"
  Hook → SessionStart → validate_config.py (runs every session, blocks on drift)

Handoff reminder:
  Rule → "write handoff before ending long sessions"
  Hook → Stop → remind_handoff.py (blocks session end if no recent handoff)

Supply chain defense:
  Rule → "delay fresh packages"
  Enforcement → .npmrc min-release-age=7 (mechanically applied to every install)
```

**Check when adding a new critical rule:** "Can this rule be bypassed by forgetting to read memory?"  
If yes → it needs a hook, not just a rule.

## MemGPT Two-Tier Architecture

```text
Core memory    ← in-context, fixed-size, agent can read/write via tool calls
               ← User profile, current task state, active invariants

Archival memory ← searchable database, paged in on-demand
                ← Historical context, past projects, reference materials
```

**Key property:** Agent explicitly decides what to page in from archival to core. This keeps core small and focused while preserving full history.

**For file-based systems:**  
`MEMORY.md Always Load` section = core memory  
`MEMORY.md On Demand` section = archival index  
Actual on-demand files = archival storage

## Domain Convergence Table

| Domain | Critical / Always | Reference / On-demand | Enforcement mechanism |
|--------|------------------|-----------------------|----------------------|
| LLM context (Liu 2023) | Beginning / end of context | Middle (attention degrades) | Position in prompt |
| MemGPT | Core memory (fixed) | Archival (paged) | Tool calls for page-in |
| Aviation | Memory items (3-10) | Checklists (documented) | Training + repetition |
| Neuroscience | Procedural memory (striatum) | Episodic (hippocampus) | Neural architecture |
| Cognitive psych | Working memory (4±1 chunks) | Long-term (unlimited) | Attention / rehearsal |
| Nuclear safety (INSAG-10) | 5-layer defense barriers | Procedures / manuals | Physical redundancy |
| Linux syslog | EMERG/ALERT → console | DEBUG → ring buffer | `console_loglevel` |
| Kubernetes | Admission webhook policies | API server logs | Webhook interception |

All 8 domains converge on: **small critical set + large reference set + mechanical enforcement for the critical set.**

## Memory Staleness Management

Memory records should include a `created: YYYY-MM-DD` field. Staleness by type:

| Type | Stale after | Check on use |
|------|-------------|--------------|
| `project` | 30 days | Verify before use if older |
| `reference` (IPs, paths, ports) | 7 days | Always verify if infrastructure-related |
| `feedback` | Stable (user preferences rarely change) | Low priority |
| `user` | Very stable | Only check if major context shift suspected |

## Automatic Memory Extraction Pattern

After sessions, extract to memory:
1. **Capabilities** — new workflows, tools, integrations discovered
2. **Corrections** — user-corrected approaches (→ feedback memory)
3. **Permissions** — newly allowed commands (→ settings)
4. **Bug/fix pairs** — symptom → root cause → solution (→ gotchas)
5. **Decisions** — architectural choices with rationale (→ DECISIONS.md or memory)

Tagged for triage: `[DECISION]`, `[GOTCHA]`, `[REUSE]`, `[DEFER]`

## Gotchas

- **Issue:** Always-load section grows unbounded as new rules are added without removing old ones. -> **Fix:** Apply Boeing rule at review time: if section exceeds 15 entries, conduct a triage pass using irreversible-consequence criterion. Most "nice to remember" items belong in on-demand.
- **Issue:** Rule in memory prevents an action at session start but is forgotten after context compaction mid-session. -> **Fix:** For any rule that must hold for an entire session (e.g., "don't modify production"), create a hook that checks at every relevant tool call — not just at session start.
- **Issue:** On-demand memory becomes a flat unstructured dump, making retrieval unreliable. -> **Fix:** Use wiki-links `[[filename]]` to create a navigable graph. Memory about project X should link to the infrastructure it runs on, the tools it uses, and the methodology applied.
- **Issue:** Memory records created years ago reference file paths, server IPs, or ports that no longer exist. -> **Fix:** SessionStart hook (e.g., `validate_config.py`) scans memory for absolute paths and checks existence. Reports drift before the session acts on stale data.

## See Also

- [[context-window-management]]
- [[memory-architectures]]
- [[session-persistence]]
- [[knowledge-graph-memory]]
