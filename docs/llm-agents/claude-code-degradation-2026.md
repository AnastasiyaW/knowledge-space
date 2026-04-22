# Claude Code Degradation 2026

Timeline, root causes, and workarounds for the March 2026 Claude Code quality regression and token cost inflation event.

## What Happened — Timeline

| Date | Event |
|------|-------|
| Early Feb 2026 | Opus 4.6 released with Adaptive Thinking (model decides per-turn reasoning budget) |
| 2026-02-12 | `redact-thinking-2026-02-12` header rolled out — hides thinking traces from UI |
| 2026-03-03 | Default `effort` silently lowered from `high` to `medium` (effort=85). No changelog entry. |
| 2026-03-08 | Quality cliff in longitudinal session data (stop-hook violations spike, reads-per-edit collapses) |
| 2026-03-23+ | Cache invalidation bugs in v2.1.100 deployed. Token costs inflate 10-20x silently. |
| 2026-03-26 | Anthropic confirms peak-hour throttling (5-11am PT weekdays) |
| 2026-03-31 | Anthropic public statement: "hitting limits way faster than expected" |
| 2026-04-02 | 6,852-session longitudinal analysis published. Median thinking depth: 2,200 → 600 chars (-67%). Reads-per-edit: 6.6 → 2.0. Team monthly Bedrock-equivalent cost: $345 → $42,121 (~122x). |
| 2026-04-09 | Community workaround guides for `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` published |

## Root Causes (Confirmed)

### 1. Effort Default Lowered (effort=85)

Anthropic lowered the default `effort` level from `high` to `medium` (internal value 85) on 2026-03-03. Confirmed by Anthropic engineering. Motivation: users "consuming too many tokens per task."

Effect: model allocates less thinking budget per turn. For simple tasks: negligible. For complex multi-step engineering: 67% reduction in thinking depth.

Adaptive thinking can allocate zero tokens on easy-seeming turns, producing fabricated commit SHAs, non-existent packages, and hallucinated API versions.

### 2. Cache Invalidation Bugs in v2.1.100

Two separate bugs reverse-engineered from Claude Code v2.1.100 binary:

**Bug 1 — Billing sentinel string replacement:**  
When conversation history contains billing-related terms, a regex replacement hits the wrong byte position → breaks cache prefix → entire context re-billed as uncached. Effect: 10-20x token inflation.

**Bug 2 — Resume/continue tool injection position:**  
Tool definitions injected at a different position than in fresh sessions → cache invalidated → full re-processing of all prior context on every `--resume`/`--continue`.

Combined effect: ~20,000 invisible tokens added to every request in affected sessions. Sessions drain quota ~40% faster.

## Measured Impact

| Metric | Pre-cliff (Feb) | Post-cliff (March) |
|--------|----------------|-------------------|
| Median thinking block length | 2,200 chars | 600 chars (-67%) |
| Reads-per-edit ratio | 6.6 | 2.0 |
| Stop-hook violations/day | ~0 | ~10 |
| API request count for equivalent task | baseline | ~80x higher |
| Monthly cost (team, Bedrock-equivalent) | $345 | $42,121 (~122x) |

## Workarounds

### Tier 1 — Officially Supported

```bash
# Force maximum reasoning effort persistently
export CLAUDE_CODE_EFFORT_LEVEL=max

# Disable adaptive thinking — force fixed reasoning budget per turn
export CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1
```

In-session: `/effort max` or `/effort high`. Per-turn trigger: `ultrathink` keyword.

**settings.json:**
```json
{
  "effort": "max",
  "disableAdaptiveThinking": true
}
```

**API users — explicit thinking budget (not adaptive):**
```python
{"thinking": {"type": "enabled", "budget_tokens": 32000}}
# NOT {"type": "adaptive"} — adaptive silently nullifies maxThinkingTokens
```

### Tier 2 — Community Workarounds

**Cache hygiene (Bug 2 mitigation):**
- Avoid `--resume` / `--continue` until v2.1.100 cache bugs are confirmed fixed
- Start fresh sessions for long workflows
- Avoid billing-related strings in conversation history (Bug 1 trigger): "billing", "usage limit", "quota"

**CLAUDE.md prefix stability (Bug 1 mitigation):**
- No timestamps near the top of CLAUDE.md (breaks cache on every session)
- No dynamic content in system prompt prefix
- Define all tools once; use state machines instead of swapping tool definitions
- Preserve error messages in context (reduces retry cycles ~40%)

**Token monitoring:**
- Track `cache_read_input_tokens` vs `cache_creation_input_tokens` in API responses
- Target: >80% cache hit rate on long sessions
- Below 80% → something is breaking the prefix

**Version rollback:**
```bash
# Rollback to v2.1.87 (pre-regression):
curl -fsSL https://claude.ai/install.sh | bash
# Use native installer, NOT npm
```

### Tier 3 — Alternative Models

| Model | SWE-bench | Cost vs Opus 4.6 | Notes |
|-------|-----------|-----------------|-------|
| DeepSeek V3.2 | ~90% of GPT-5.4 | ~20x cheaper | Strong agentic coding |
| Gemini 3.1 Pro | 80.6% | ~50% cheaper | Comparable on coding |
| Qwen3.6-Plus | Beats Opus 4.5 on terminal | Via Tongyi subscription | 1M context |
| GLM-5.1 | Agentic-tuned | Free (self-host) | Open weights |

**Pragmatic 2026 stance:** Start with open-weight (DeepSeek/Qwen/GLM) for routine tasks; use Opus 4.6 only for subtasks where the gap matters.

## What Anthropic Has Not Addressed (as of 2026-04-14)

- Whether v2.1.100 cache bugs are fixed
- Exact mapping of `effort=85` / `medium` / `high` / `max` to thinking-token budgets
- Why the effort-default change was not in any release note
- Whether model weights changed between Opus 4.5 and 4.6 (denied, not independently verifiable)

## KV-Cache Best Practices (Permanent)

Regardless of Anthropic changes, cache-friendly CLAUDE.md structure reduces costs:

```text
CLAUDE.md structure (cache-friendly):
  1. Static invariant rules (never changes between sessions)
  2. Project structure (changes rarely)
  3. Per-session context (if any, goes at END)

Never at the top:
  - Current timestamps
  - Dynamic project status
  - Session-specific context
```

See [[context-window-management]] for full KV-cache optimization guide.

## Gotchas

- **Issue:** `/effort max` in-session resets after compaction or new session without persisted settings. -> **Fix:** Set `"effort": "max"` in `settings.json` AND export `CLAUDE_CODE_EFFORT_LEVEL=max` in shell profile.
- **Issue:** Adaptive thinking allocated zero tokens on a turn → model produces confident but fabricated output (commit SHAs, package names, API versions). -> **Fix:** `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` forces a minimum thinking budget per turn. Verify critical outputs against actual filesystem/APIs.
- **Issue:** Cache hit rate monitoring shows low hits even with stable prefix → legacy v2.1.100 tool injection bug. -> **Fix:** Upgrade to latest Claude Code via native installer (not npm). Check `cache_creation_input_tokens` vs `cache_read_input_tokens` in API response to confirm.

## See Also

- [[context-window-management]]
- [[agentic-security-2026]]
- [[claude-code-harness-patterns]]
