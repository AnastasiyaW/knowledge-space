# Claude Code Harness Patterns — Skills, Commands, CLI Detectors

Three-layer harness architecture for enforcing design quality and development discipline in Claude Code. The pattern separates knowledge (skill files), triggers (slash commands), and deterministic verification (CLI tool) into independent layers.

## Three-Layer Architecture

```text
┌─────────────────────────────────────────────────────┐
│ Layer 3: Deterministic CLI Detector                 │
│  • Mechanical checks, no LLM needed                 │
│  • Anti-pattern regex + headless browser checks     │
│  • JSON output for piping into CI                   │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│ Layer 2: Slash Commands                              │
│  • Named triggers: /audit /polish /critique         │
│  • Composable: /audit /normalize /polish blog       │
│  • Discoverable names → agent picks correct command │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│ Layer 1: Skill (SKILL.md + reference files)         │
│  • Domain knowledge: typography, color, spacing     │
│  • Always-loaded context for the agent              │
│  • Reference files per sub-domain                  │
└─────────────────────────────────────────────────────┘
```

**Shell Bypass Principle:** Mechanical checks (linting, pattern detection) must NOT go through LLM. They are deterministic — run via CLI, feed results as structured input to the next step.

## TDD-First Methodology (RED-GREEN-REFACTOR)

Enforced workflow:
```text
brainstorming → writing-plans → using-git-worktrees →
subagent-driven-development → test-driven-development →
requesting-code-review → finishing-a-development-branch
```

**Key constraint:** Agent checks which skills apply BEFORE starting a task. Skills are not optional hints — they are mandatory workflows the agent self-enforces.

**Measured impact (community benchmarks):**
- Visual brainstorming with HTML mockups reduced style-related retries: 4/feature → 0
- Token cost reduction: ~14% with better upfront planning
- Parallel agent dispatch via git worktrees: 3-5x speedup on multi-file tasks

## Visual Context Pattern (HTML Fragment Server)

When a decision is better understood visually than in text, use a local HTTP server with HTML fragments:

```bash
scripts/start-server.sh --project-dir /path/to/project
```

**How it works:**
1. Agent writes HTML fragments to `screen_dir` (not full documents — server wraps in template)
2. User opens URL, clicks options
3. Clicks stored as JSON events in `$STATE_DIR/events`
4. Agent reads events next turn, iterates

**CSS contract classes:** `.options`, `.option`, `.cards`, `.mockup`, `.split`, `.mock-nav`, `.mock-sidebar`, `.mock-button`, `.mock-input`

**Decision rule:** "Would the user understand this better by seeing it than reading it?" → yes: HTML fragment; no: terminal output.

## Design CLI Anti-Pattern Detection

Run deterministic pattern checks before invoking LLM review:

```bash
npx impeccable detect src/          # directory scan
npx impeccable detect index.html    # single file
npx impeccable detect https://url   # URL via headless browser
npx impeccable detect --fast --json # regex-only, JSON for CI
```

**Anti-pattern manifest (24 checkers, categories):**

| Category | Patterns blocked |
|----------|-----------------|
| AI-slop fonts | Inter, Roboto, Arial as default (without overrides) |
| AI-slop colors | Pure black/gray (need tinted neutrals), purple gradients |
| AI-slop layout | Nested cards ("Cardocalypse"), thick border accent cards |
| AI-slop motion | Bounce/elastic easing, dark outer glows |
| Quality | Line length >75ch, cramped padding, skipped heading levels, small touch targets (<44px) |
| Text | Gray text on colored backgrounds |

**Integration in CI:**
```yaml
# .github/workflows/design-check.yml
- name: Design anti-pattern check
  run: npx impeccable detect src/ --fast --json > design-report.json
- name: Fail on P0 issues
  run: jq '.issues[] | select(.severity == "P0")' design-report.json | grep -q . && exit 1 || true
```

## Anti-Pattern as Config

Both positive ("use tinted neutrals") and negative ("never Inter as default") instructions are needed. Negative list is often more actionable:

```markdown
# DESIGN.md pattern — anti-attractor procedure
Before choosing any design element, enumerate your reflex defaults and reject them:
- Font: NOT Inter/Roboto/Arial → choose from [your brand fonts]
- Card background: NOT pure white (#fff) → use [your surface color]
- Primary action: NOT purple gradient → use [your brand primary]
- Animation: NOT bounce/elastic → use ease-out or spring (tension 200, friction 26)
```

## DESIGN.md — Visual CLAUDE.md

Drop a `DESIGN.md` in project root. Agents read it as a visual runtime config:

```markdown
---
brand: your-brand-name
version: 1.0.0
---

## Typography
- Heading: [font-name], weights 600/700
- Body: [font-name], weight 400, line-height 1.6
- Scale: 12/14/16/18/24/32/48px

## Color Tokens
- surface-0: hsl(220, 15%, 97%)   # not pure white
- text-primary: hsl(220, 15%, 15%) # not pure black (#000)
- brand-primary: hsl(230, 80%, 55%)

## Spacing
- Unit: 8px base grid
- Component padding: 16/24/32px

## Avoid
- Generic card-in-card patterns
- Centered single-column content wider than 720px
- Decorative elements with no semantic function
```

## Command Composition Examples

```bash
# Full frontend workflow
/audit /normalize /polish blog

# UX review with error hardening
/critique /harden checkout

# Extract design system from existing codebase
/create-design-system

# Visual verification after changes
/verify-artifact   # screenshot + vision check vs anti-pattern list
```

## Gotchas

- **Issue:** Layer 3 CLI runs synchronously and can't catch dynamic rendering issues. -> **Fix:** Use headless browser mode (`--no-fast`) for SPAs; use `--fast` for static HTML in CI.
- **Issue:** `/verify-artifact` requires MCP browser tool to be connected. -> **Fix:** Check for `mcp__Claude_Preview__preview_screenshot` availability before invoking; fall back to `--fast` CLI scan if unavailable.
- **Issue:** DESIGN.md conflicts with CLAUDE.md if both define tone/style. -> **Fix:** DESIGN.md covers visual/brand only; CLAUDE.md covers behavior/workflow. No overlap by design.

## See Also

- [[claude-code-ecosystem]]
- [[agent-design-patterns]]
- [[context-engineering]]
- [[production-patterns]]
