---
title: "Session Handoff Rollups"
description: "How to create a bounded, auditable rollup of long-running agent work without pretending that a summary is lossless."
tags: [handoff, continuity, context-management, agent-operations, documentation]
---

# Session Handoff Rollups

**Scope checked: 2026-09-03.** A rollup is a dated snapshot that helps the next operator resume a project. It is not a replacement for source history, a guarantee of lossless compression, or a reason to erase the receipts that supported earlier decisions.

The safe resume set is a verified rollup plus the bounded tail of entries recorded after its cut point.

## Why a Rollup Exists

Long-running work accumulates small handoffs: completed actions, active constraints, failed attempts, and pending approvals. Reading only the most recent handoff can lose a still-valid decision. Reading every historical note is slow and can elevate stale context.

A rollup answers four questions:

1. What exact source records does it cover?
2. What is verified, reported, blocked, or unknown at the cut point?
3. Which artifacts, revisions, and receipts remain authoritative?
4. Which entries must a new session read after the cut point?

## The Snapshot Contract

Use explicit frontmatter and stable source references:

```yaml
---
project: example-project
status: ACTIVE
as_of: 2026-09-03T20:15:00Z
covered_sources:
  - handoff-2026-08-30-a
  - handoff-2026-09-01-b
source_index_ref: handoffs/INDEX.md
verification_ref: receipts/rollup-2026-09-03.json
---
```

`as_of` is the latest included source event, not the time someone happened to write the summary. A reader loads:

```text
current rollup
  + source index
  + every entry after as_of
  + artifacts named by the current task
```

The tail must stay bounded. Create a new rollup at a phase boundary or when the index shows that normal resumption again requires too many source records.

## Preserve Attribution and Confidence

Every important statement should be traceable:

| Field | Meaning |
|---|---|
| claim | concise statement of current state |
| confidence | `VERIFIED`, `REPORTED`, `UNKNOWN`, or `BLOCKED` |
| evidence reference | test output, commit, issue, runtime receipt, or user report |
| owner | who may act on the next step |
| recheck | event or command that can change the statement |

This prevents a summary from turning a tentative diagnosis into a fact. When a source is missing or a claim cannot be reproduced, label it `UNKNOWN`; do not fill in the gap from conversational memory.

## Safe Rollup Procedure

1. inventory the handoff IDs, commits, receipts, and active branches to be covered;
2. choose an immutable cut point and record it;
3. extract only decisions, constraints, verified outcomes, failures, and open authorities;
4. attach a source reference to each material conclusion;
5. compare the rollup with the source index and test the stated resume path;
6. publish the rollup as a new append-only artifact;
7. leave later handoffs in the tail for the next rollup.

Do not overwrite original handoffs to make the rollup look cleaner. If an index needs a relationship, add an index row or back-reference after checking that concurrent writers cannot lose it.

## Parallel Work Requires a Cut Boundary

Do not roll up a live, branching project as if it were serial. At the cut point:

- record every active branch and worktree;
- identify resource leases and their owners;
- treat unmerged changes as `RUNNING`, not completed;
- record messages or receipts that are still in flight;
- keep new writes after the cut in the tail.

If the snapshot cannot name its writers and artifacts, postpone it rather than manufacture a complete picture.

## Rollup Structure

```text
purpose and scope
covered source IDs and cut point
verified current state
active work and owners
decisions and rejected paths
known failures and evidence
release or publication gates
next safe action and recheck
tail-reading rule
```

The next safe action is a continuation aid, not a command to bypass approval, re-run an irreversible effect, or change an unrelated project.

## Validate Before Reuse

Before a new session acts on a rollup:

1. confirm the cited repository revision or runtime state still exists;
2. check whether the recheck event has occurred;
3. read all tail entries after `as_of`;
4. verify any resource lease externally before taking ownership;
5. create a new snapshot when the current one is stale.

This makes the handoff useful even when a previous session ended unexpectedly.

## Gotchas

- **A rollup has no explicit cut point.** Readers cannot know what to add. **Fix:** record `as_of` and covered source identifiers.
- **A summary labels all state as done.** It hides failed checks and pending authority. **Fix:** use confidence and terminal-state labels with receipts.
- **Concurrent agents edit the same index.** A last writer can drop another relation. **Fix:** prefer append-only records or serialize the mutable index update.
- **The tail becomes as large as the original history.** The rollup no longer improves retrieval. **Fix:** create a new dated snapshot after the next verified phase boundary.
- **An old rollup is treated as live policy.** It can reintroduce stale decisions. **Fix:** check its `as_of`, evidence, and recheck rules before acting.

## See Also

- [[multi-session-coordination]]
- [[session-persistence]]
- [[agent-memory]]
- [[claude-code-harness-patterns]]
