# Handoff Rollup Pattern

Technique for compressing accumulated session handoffs in long-running projects into a single rollup document with a forward pointer, preventing linear growth of context load for new sessions.

## Problem

In projects with 20+ sequential sessions, each session produces a handoff file. A new session resuming work must either read all prior handoffs (token-expensive, O(n) growth) or read only the latest one (loses earlier context). Neither is acceptable for projects spanning weeks.

## Rollup Structure

```markdown
# Handoff Rollup — {project-slug}

**covers:** [list of handoff IDs or date ranges]
**through:** YYYY-MM-DD HH:MM
**status:** ACTIVE

## What was built (cumulative)
[Dense summary of all decisions and artifacts from covered period]

## What was abandoned and why
[Approaches tried and rejected, with reasons]

## Current state as of {through}
[Working: X, Y. Broken: Z. Blocked: W]

## Next step
[Single action to resume]
```

**Filename convention:** `.claude/handoffs/YYYY-MM-DD_rollup_{slug}.md`

## Covered-Until Pointer

Rollup frontmatter marks `through:` — the timestamp or message ID up to which the rollup is accurate. New sessions combine the rollup with only handoffs dated **after** the rollup's `through` timestamp:

```text
Read: rollup (covers months 1-3)
  +  handoff_2026-04-18.md (after rollup)
  +  handoff_2026-04-20.md (after rollup)
= complete picture with O(log n) load
```

Covered handoffs get a back-reference added to their frontmatter:
```yaml
rolled_up_into: 2026-04-20_rollup_color-checker.md
```

This preserves original files for audit while making them skippable.

## Dual Attribution in Handoffs

When a session delegates to sub-agents (via `Task()` spawns), standard handoffs lose the distinction between who claimed ownership and who did actual work:

```yaml
invoked_by: main-session-ani       # session that accepted the task
worked_by: [main-session-ani, explorer-sub-1, fixer-sub-3]  # all sessions that contributed
```

**Why this matters:** Without dual attribution, post-hoc analysis of agent performance can't separate delegation patterns from execution patterns. A session that delegates everything looks identical to one that does nothing.

## When to Create a Rollup

Trigger conditions:
- More than 15 handoffs accumulated for a project
- New session startup time is dominated by reading prior handoffs
- Project enters a new phase (phase transition = natural rollup boundary)
- After a major milestone (major feature shipped, architecture changed)

**Do not rollup:** actively-branching projects where parallel sessions are running (risk of losing concurrent context). Wait until all branches are merged.

## Gotchas

- **Issue:** Rollup created while parallel sessions are active → concurrent handoffs missing from rollup coverage. -> **Fix:** Only rollup when all sessions for the project are CLOSED. Check INDEX.md for ACTIVE entries before rolling up.
- **Issue:** `through:` timestamp set to "now" but last handoff was hours ago → gap between rollup coverage and reality. -> **Fix:** Set `through:` to the timestamp of the last handoff being rolled up, not current time. Future handoffs start from that exact timestamp.
- **Issue:** Back-references added to covered handoffs make them appear "ACTIVE" to naive INDEX.md readers. -> **Fix:** Mark covered handoffs as `ROLLED_UP` status in INDEX.md, not `CLOSED` — these are different states.
- **Issue:** Rollup grows stale as project evolves. -> **Fix:** Rollup is a snapshot, not a living document. Create a new rollup at next phase boundary rather than updating the old one.

## Relationship to Project Chronicles

Rollup handoffs are tactical: "resume work from here." Project chronicles are strategic: "understand how we got here." They complement each other:

| Artifact | Purpose | Audience | Update frequency |
|----------|---------|----------|-----------------|
| Individual handoff | Resume next session | Next session | Per session |
| Rollup handoff | Resume after long gap | Any future session | Per phase boundary |
| Chronicle | Historical understanding | Anyone | Per milestone |

## See Also

- [[multi-session-coordination]]
- [[session-persistence]]
- [[agent-memory]]
