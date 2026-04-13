---
title: "Knowledge Graph Memory for AI Agents"
description: "Persistent knowledge graph patterns for AI agents: entity resolution, pipeline stages, agent notes, and inline executable tasks in Markdown vaults."
---

# Knowledge Graph Memory for AI Agents

Structured knowledge graphs as persistent agent memory - beyond flat note files. The agent continuously extracts entities from incoming data (email, meetings, transcripts), resolves them to canonical records, and maintains a bidirectionally linked Obsidian-compatible vault.

Reference implementation: [Rowboat](https://github.com/rowboatlabs/rowboat) (YC S24, Apache 2.0).

## Architecture: Two-Layer Storage

```
raw/           - Append-only sources (email, transcripts, voice memos)
               - Never modified by agent, only read
knowledge/
  People/      - Person entities with roles, orgs, emails
  Organizations/
  Projects/    - Status, stakeholders, timeline
  Topics/      - Keywords, related notes
  Meetings/    - Attendees, decisions, action items
  Agent Notes/ - User model (identity, preferences, style)
  Today.md     - Auto-generated daily brief (inline task)
```

**Core invariant:** raw data is immutable source of truth; knowledge/ is the agent's processed, cross-linked world model.

## Three-Stage Pipeline

### Stage 1: Signal Filtering (for email/feeds)

Before building the graph, filter noise. LLM applies YAML frontmatter to each source item:

```yaml
---
labels:
  relationship: [investor, customer, team]
  topics: [fundraising, hiring, legal]
  type: "intro" | "followup" | ""
  filter: [cold-outreach, newsletter, spam]
  action: "action-required" | "urgent" | "waiting" | ""
processed: true
labeled_at: "2026-04-11T10:00:00Z"
---
```

**Noise-first principle:** identify what to SKIP before deciding what to keep. If `filter` array is non-empty, the item is excluded from graph building regardless of other tags.

```
"Founder Signal Test": would a busy domain expert want this in their knowledge system?
```

Strictness levels control how aggressively notes are created:
- `high` - only explicit interactions create notes; emails only update existing contacts
- `medium` - personalized business emails create notes; filters consumer services
- `low` - most human senders, minimal filtering

### Stage 2: Graph Building

Processes filtered sources into entity notes. Before each batch:

1. **Rebuild knowledge index** - scan all `knowledge/` .md files, extract entities
2. **Inject index into prompt** - agent receives structured table of known entities
3. **Process batch** - agent writes/updates notes, resolves to canonical names

Change detection uses hybrid approach:
```
mtime check (fast) → if changed, SHA-256 hash → if hash differs → process
```
Eliminates false positives from timestamp-only changes.

### Stage 3: Tagging

Applies categorical tags to generated knowledge notes. Tag categories: relationship (12), topic (11), email-type (2), noise (13), action (3), status (5), source (6).

## Entity Resolution

**Critical pattern:** before processing each batch, rebuild an in-memory index of all known entities:

```typescript
interface KnowledgeIndex {
  people: { file, name, email?, aliases[], organization?, role? }[]
  organizations: { file, name, domain?, aliases[] }[]
  projects: { file, name, status?, aliases[] }[]
  topics: { file, name, keywords[], aliases[] }[]
}
```

The agent receives this as a formatted markdown table. When it encounters "John Smith" in source data, it resolves to the existing `[[People/John Smith]]` rather than creating a duplicate.

**Without this:** agents create `John Smith.md`, `J. Smith.md`, `Smith, John.md` for the same person.

## Note Templates

### People Note
```markdown
# Person Name

## Info
- **Role:** 
- **Organization:** [[Organizations/OrgName]]
- **Email:** 

## Summary

## Connected to

## Activity

## Key facts

## Open items
```

### Wiki-Link Conventions

- Syntax: `[[Folder/Canonical Name]]` (absolute path within knowledge/)
- Always bidirectional: if Person links to Org, Org must link back to Person
- Agent resolves name variants to canonical names via the knowledge index before writing links

## Agent Notes - Structured User Model

Separate `knowledge/Agent Notes/` directory for the AI's understanding of the user:

```
Agent Notes/
  user.md          - identity facts only (roles, companies, location)
  preferences.md   - explicit rules ("no meetings before 11am")
  style/
    email.md       - writing patterns by recipient type
```

**Data sources:** user's sent messages, inbox items (manual notes), conversation logs.

**Processing:** deduplicates aggressively, timestamps facts for staleness detection.

This is distinct from the main knowledge graph - it's the agent's model of WHO it works for, not WHAT it knows about the world.

## Inline Tasks (Live Notes)

Executable JSON blocks embedded in Markdown. Notes with `live_note: true` frontmatter are polled on a schedule:

```markdown
---
live_note: true
---

# Today

```task
{
  "instruction": "Create a daily brief for me",
  "schedule": { "type": "cron", "expression": "*/15 * * * *" },
  "lastRunAt": "2026-04-11T10:30:00Z",
  "targetId": "dailybrief"
}
```

<!--task-target:dailybrief-->
Results written here automatically
<!--/task-target-->
```

Schedule types: `cron`, `window` (time-constrained execution), `one-shot`.

**Effect:** static knowledge files become active agents. The graph is not just a store - it runs.

## Version History

Git-track the knowledge vault using isomorphic-git:
- Only `.md` files are tracked
- Commit after each processing batch
- Full restoration from any commit
- Audit trail of knowledge evolution

```typescript
// After each batch completes
await git.commit({
  dir: knowledgeDir,
  message: `Processed batch: ${files.join(', ')}`,
  author: { name: 'agent', email: 'agent@local' }
});
```

## Scaling Patterns

| Scale | Retrieval Strategy |
|-------|--------------------|
| <200 notes | Index file navigation only |
| 200-1000 | Domain-specific indexes + grep search |
| 1000-5000 | BM25 with LLM reranking |
| 5000+ | Full [[rag-pipeline]] + [[vector-databases]] |

For moderate scale (the common case), a structured index + Unix tools (grep, find) outperforms vector search in latency and cost.

## Applying These Patterns Without the Full Stack

### Entity Resolution for File-Based Memory

Before creating new memory entries, scan existing files for the same entity:

```python
def resolve_entity(name: str, memory_dir: Path) -> Optional[Path]:
    """Find existing file for entity before creating duplicate."""
    for f in memory_dir.rglob("*.md"):
        content = f.read_text()
        if name.lower() in content.lower():
            # Check aliases in frontmatter or body
            return f
    return None
```

### Noise-First Filtering for Any Ingestion

Define explicit skip rules before extract rules:

```python
SKIP_PATTERNS = ["newsletter", "no-reply", "unsubscribe", "automated"]

def should_skip(source: dict) -> bool:
    """Noise-first: skip known noise categories first."""
    return any(p in str(source).lower() for p in SKIP_PATTERNS)
```

### Two-Layer Raw/Processed Separation

```
sessions/raw/     - immutable session transcripts, never modified
memory/           - extracted, consolidated knowledge
                  - derived from raw but not tied to it
```

Allows re-processing raw data with improved extraction logic without data loss.

## Gotchas

- **Entity resolution must run BEFORE each batch, not once at startup.** The knowledge graph grows during processing; a batch at step 5 may need entities created in step 2. Rebuild the index before every batch, not just on initialization
- **Skip tags must be hard filters.** If noise filtering is advisory (weighted), spam leaks into the graph over time. Make skip/filter tags override all create signals - a cold-outreach email never creates a person note, regardless of relationship tags
- **Wiki-links without bidirectional enforcement diverge.** One-way links create orphaned nodes that the agent can't navigate to. Enforce bidirectionality at write time: when agent writes `[[People/Alice]]` in an org note, check that Alice's note links back to that org
- **Inline tasks in live notes require polling, not file watchers.** File system events don't carry schedule context. A polling loop (every 15s) reading `live_note: true` frontmatter is more reliable across OS platforms than inotify/FSEvents

## LLM Wiki Pattern (Karpathy)

A simpler alternative to full knowledge graph systems: **structured markdown collections with cross-references**. No RAG, no vector DB - just text files navigated by the LLM.

### Three-Layer Architecture

```
raw/          - immutable source materials (PDFs, clipped articles, notes)
              - LLM reads but NEVER modifies
wiki/         - LLM-generated structured markdown
              - encyclopedia articles for concepts and entities
              - summaries, comparisons, cross-references via backlinks
              - index.md: catalog updated on every ingest
              - log.md: append-only chronological operation log
schema/       - CLAUDE.md: structure conventions, workflows
```

### Three Operations

```
Ingest:  user drops source file
         LLM reads → discusses takeaways → writes summary pages
         updates index.md → revises entity/concept pages → appends to log
         one source → ~10-15 wiki pages touched

Query:   user asks question
         LLM navigates via index → synthesizes answer with citations
         valuable answers → new wiki pages

Lint:    periodic health-check passes
         find: contradictions, stale claims, orphan pages, missing cross-refs
```

### Why Plain Markdown Beats RAG (at moderate scale)

At ~100 articles / ~400K words, LLM navigates via summaries and index without vector search. Wiki = "persistent, compounding artifact" - knowledge compiled once and maintained, not re-derived on every query as in RAG. LLM handles bookkeeping: doesn't forget to update cross-references, can touch 15 files in one pass.

At larger scale: add optional BM25/vector search with LLM re-ranking.

### Comparison

| Approach | Scale | Query Speed | Setup | Best for |
|----------|-------|-------------|-------|---------|
| LLM Wiki (plain markdown) | <500 articles | Full LLM navigation | Minimal | Personal knowledge base |
| Knowledge Graph (Rowboat) | 500-5000 entities | Index lookup + LLM | Medium | Work context from email/meetings |
| RAG + vector DB | 5000+ articles | Sub-100ms retrieval | Significant | Large corpus Q&A |

### Session-to-Wiki Pipeline

Connect session work to persistent wiki:

```python
# After each session, extract learnings
session_summary = extract_session_insights(conversation_log)

# Ingest into wiki
wiki.ingest(session_summary)
# → LLM reads, updates relevant concept pages, appends to log

# At session start, query wiki for context
context = wiki.query("current project architecture decisions")
```

## See Also

- [[knowledge-base-as-memory]]
- [[memory-architectures]]
- [[memory-retrieval-patterns]]
- [[session-persistence]]
- [[temporal-memory]]
- [[rag-pipeline]]
