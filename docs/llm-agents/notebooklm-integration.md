---
title: "NotebookLM Integration for AI Coding Agents"
description: "Using Google NotebookLM as a free research backend for Claude Code - token-saving workflows, cross-session memory, skill-based orchestration."
---

# NotebookLM Integration for AI Coding Agents

Bridge between Claude Code and Google NotebookLM via reverse-engineered CLI (`notebooklm-py`). Heavy analytics (30+ documents, web research, cross-references) runs free on Google's Gemini RAG infrastructure. Claude spends tokens only on orchestration and final editing.

## Architecture

```text
User request
    |
    v
Claude Code (orchestrator, token-metered)
    |
    v  CLI calls
notebooklm-py (bridge, reverse-engineered API)
    |
    v
Google NotebookLM (Gemini RAG, free tier: 50 sources/notebook)
    |
    v  results
Claude Code (final polish, minimal tokens)
```

## Setup

```bash
# Install CLI bridge
# Repo: https://github.com/teng-lin/notebooklm-py
# Follow README for installation + Google auth

# Install Claude Code skill
notebooklm skill install
notebooklm skill status    # verify
```

Skill installs to `~/.claude/skills/notebooklm/SKILL.md` (personal) and `~/.agents/skills/notebooklm/` (cross-agent compatible with Codex, Gemini CLI).

## Four Workflows

### A. Research Without Token Spend

Offload document analysis to NotebookLM. Claude orchestrates, Google processes.

```bash
# 1. Create notebook
notebooklm create "My Research Project"

# 2. Add sources (up to 50 free, 300 Pro)
notebooklm source add \
    "./transcript-1.md" \
    "https://example.com/article" \
    "./report.pdf"

# 3. Query across all sources (free, Gemini RAG)
notebooklm ask "what are the three most important themes across all sources?"

# 4. Generate artifacts
notebooklm generate slide-deck
notebooklm generate flashcards --quantity more
notebooklm generate mind-map
notebooklm generate data-table "compare key concepts"
notebooklm generate audio "make it engaging" --wait
```

**Token math**: analytical work on Google infrastructure. Claude tokens reserved for orchestration + final editing only. $20/month plan stretches to $200/month capability.

### B. Expert Agent from Web Research (DBS Framework)

Use NotebookLM Deep Research for autonomous web crawling, then structure into a Claude Code skill.

1. Run Deep Research in NotebookLM browser (source type: "web", specific query)
2. Structure results using **DBS framework**:
   - **Direction** - step-by-step logic, decision trees, error handling -> becomes SKILL.md core
   - **Blueprints** - static references: templates, tone guidelines, classification rules -> companion files
   - **Solutions** - deterministic code tasks: API calls, formatting, calculations -> scripts
3. Feed to `/skill-creator` in Claude Code -> auto-generates full skill package
4. Test and iterate

### C. Cross-Session Memory via Master Brain

```bash
# End of session: extract insights
# /wrap-up skill extracts: corrections, successful patterns, open questions, decisions

# Push to dedicated NotebookLM notebook
notebooklm use master-brain-notebook-id \
    "./session-summary-2026-04-06.md"

# Add to CLAUDE.md:
# "Before answering architecture questions, query Master Brain via NotebookLM CLI"
```

Over weeks, Master Brain accumulates hundreds of session summaries. NotebookLM indexes everything with semantic connections. Claude retrieves exactly the context needed without loading hundreds of documents into its context window.

### D. Visual Knowledge via Obsidian

Run Claude Code from Obsidian vault root. All generated files appear in Obsidian's graph view.

```bash
cd ~/Documents/MyVault
claude
```

CLAUDE.md in vault root specifies: folder structure, mandatory metadata (dates, tags, source links), cross-reference rules (`[[double brackets]]`), formatting standards.

Custom skills: `/research <topic>`, `/daily` (daily summary with cross-refs), `/wrap-up` (session memory to vault).

## CLI Reference

| Command | Description |
|---------|-------------|
| `notebooklm create "Name"` | Create notebook |
| `notebooklm source add file url ...` | Add sources |
| `notebooklm ask "question"` | Query notebook |
| `notebooklm generate slide-deck` | Generate slides |
| `notebooklm generate flashcards` | Generate flashcards |
| `notebooklm generate mind-map` | Generate mind map |
| `notebooklm generate audio` | Generate audio |
| `notebooklm generate data-table "..."` | Generate table |
| `notebooklm skill install` | Install Claude Code skill |
| `notebooklm login` | Re-authenticate (cookies expire) |

## Gotchas

- **Unofficial API - no stability guarantee.** `notebooklm-py` reverse-engineers Google's internal protocols. Google can break it at any time by changing their backend. No SLA, maintained by one developer (Teng Ling). Treat as power-user tool, not production infrastructure
- **`storage_state.json` contains live Google session cookies.** Anyone with this file gets full access to your NotebookLM data. Never commit to git. Treat as a password. Add to `.gitignore` immediately
- **Cookies expire periodically.** When commands fail with auth errors, run `notebooklm login` (30 seconds). No way to get permanent tokens
- **GDPR implications.** User-tier Claude and NotebookLM process/store data in the US. If you work with regulated data (EU/UK), corporate API offers regional processing but consumer tier does not
- **Anthropic ToS compliance.** Do not use this to circumvent token limits through unofficial wrappers. Ensure usage matches your plan

## See Also

- [[context-engineering]] - context management strategies
- [[agent-memory]] - memory patterns for AI agents
- [[rag-pipeline]] - RAG architecture that NotebookLM uses internally
- [[token-optimization]] - reducing token consumption
- [[managed-agents]] - Anthropic's official hosted agent platform
