---
title: "Claude Adaptive Thinking & Effort Control"
description: "How Claude's adaptive thinking system works, the March 2026 effort regression, quantified metrics, and env vars to restore reasoning depth."
---

# Claude Adaptive Thinking & Effort Control

Adaptive thinking lets Claude decide per-turn how much reasoning to use. Shipped February 2026 with Opus 4.6. The March 2026 default effort downgrade caused a measurable regression documented across thousands of real sessions.

## How Adaptive Thinking Works

```text
thinking: {type: "adaptive"}  →  model decides reasoning depth per request
thinking: {type: "enabled", budget_tokens: N}  →  fixed budget (deprecated on 4.6)
```

Three layers of control:

| Layer | What it controls |
|-------|-----------------|
| `thinking.type` | `adaptive` or `enabled` (fixed, deprecated on 4.6) |
| `output_config.effort` | Guidance level: `max`, `high`, `medium`, `low` |
| `budget_tokens` | Exact token cap (legacy, deprecated on 4.6 models) |

**Effort behavior:**

| Level | Behavior |
|-------|---------|
| `max` | Always thinks, no constraints. Opus 4.6 / Sonnet 4.6 only |
| `high` | Always thinks, deep reasoning (default pre-March 3, 2026) |
| `medium` | Moderate thinking, may skip for "simple" queries (default post-March 3) |
| `low` | Minimal thinking |

The March 3, 2026 change: default silently lowered from `high` to `medium` (effort level 85). No changelog entry. Confirmed post-hoc by Boris Cherny (Anthropic).

## Quantified Regression (March 2026)

From 6,852 Claude Code session logs, 234,760 tool calls:

| Metric | Before (Jan 30 - Feb 12) | After (Mar 8+) | Delta |
|--------|--------------------------|----------------|-------|
| Median thinking depth | ~2,200 chars | ~600 chars | -73% |
| Reads per edit | 6.6 | 2.0 | -70% |
| Edits without prior Read | 6.2% | 33.7% | +5.4x |
| Stop-hook violations | 0 total | 173 | - |
| User interrupts per 1K tool calls | 0.9 | 11.4 | +12.7x |
| Reasoning loops per 1K tool calls | 8.2 | 21.0 | +2.6x |
| Estimated monthly API cost | $345 | $42,121 | +122x |

**Cache invalidation bugs (v2.1.100):** Two separate bugs also inflated token costs:
1. Billing-sentinel string-replacement breaks cache prefix → full context re-billed
2. Resume/continue tool-injection at wrong position → cache invalidated on every resume

Typical cost inflation from cache bugs: 10-20x per session with resume.

## Affected Models

| Model | Adaptive thinking | `enabled` + `budget_tokens` |
|-------|------------------|-----------------------------|
| Claude Opus 4.6 | Default mode | Deprecated (still works) |
| Claude Sonnet 4.6 | Supported | Deprecated |
| Claude Mythos Preview | Only mode - cannot disable | Not supported |
| Claude Opus 4.5 / Sonnet 4.5 | Not supported | Still works |

## Restoring Reasoning Depth

### Claude Code (interactive)

```bash
/effort max         # session-only
/effort             # check current level
```

### Environment variables (permanent)

```bash
# Linux/macOS
export CLAUDE_CODE_EFFORT_LEVEL=max
export CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1

# Windows PowerShell
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
$env:CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING="1"
```

### settings.json

```json
{
  "env": {
    "CLAUDE_CODE_EFFORT_LEVEL": "max",
    "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING": "1"
  }
}
```

### API (Opus 4.6 / Sonnet 4.6)

```json
{
  "model": "claude-opus-4-6",
  "thinking": {"type": "adaptive"},
  "output_config": {"effort": "max"},
  "max_tokens": 32000
}
```

Legacy path (deprecated, still functional):
```json
{
  "thinking": {"type": "enabled", "budget_tokens": 31999}
}
```

## Hybrid Model Stack (Cost Mitigation)

| Task | Tool | Rationale |
|------|------|-----------|
| Architecture, security review, complex debugging | Claude Opus 4.6 + effort=max | Quality gap still significant |
| Bulk generation, routine refactoring | DeepSeek V3.2 | ~20x cheaper, ~90% quality |
| Long context, terminal tasks | Qwen 3.6-Plus | 1M context, strong on terminal benchmarks |
| Batch dataset processing | DeepSeek V3.2 | Cost-effective at scale |

## Gotchas

- **`MAX_THINKING_TOKENS` makes every request a thinking request** (issue #5257). Even "what time is it" gets a thinking block. Check for this env var before troubleshooting unexplained costs.
- **`ultrathink` keyword conflicts with `MAX_THINKING_TOKENS`** (issue #18072): the keyword is ignored when the env var is set.
- **Raising `max_tokens` alone does nothing.** Adaptive mode won't use the extra space - the bottleneck is the effort level, not the output ceiling.
- **Downgrading Claude Code to v2.1.87** avoids the v2.1.100 cache invalidation bugs, but also loses features. Evaluate the trade-off.
- **`budget_tokens` is deprecated on 4.6 models** and will be removed in a future release. Migrate to `output_config: {effort: ...}` now.
- **`CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` increases cost 3-5x** vs medium default. Budget accordingly.

## See Also

- [[claude-code-ecosystem]]
- [[kv-cache-compression]]
- [[context-engineering]]
