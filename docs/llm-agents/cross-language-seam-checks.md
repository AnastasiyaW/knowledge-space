---
title: "Cross-Language Seam Checks for Coding Agents"
description: "Guard values that are hand-copied between languages and components (routes, versions, DTO fields, env vars) with a mechanical check, and tell the agent which file on the other side to fix. Worked through with Crossweft 0.4.0."
tags: [coding-agents, harness, hooks, verification, contracts, polyglot, crossweft]
---

# Cross-Language Seam Checks for Coding Agents

**Scope checked: 2026-11-05, Crossweft 0.4.0.** A *seam* is a place where two components must agree on something written by hand on both sides: a route, a header, an API version, the fields of a DTO, the env vars a service reads, the same rounding rule in Go and TypeScript. Types, unit tests and linters stay inside one language, so they miss a seam. A coding agent edits one side, its local tests pass, and it reports "done".

## When a Seam Needs a Guard

| How both sides are kept equal | Guard needed? |
|---|---|
| shared symbol in one language | no: the compiler checks it |
| generated from one schema (OpenAPI, `.proto`) | no, if the generator runs in CI; check the generated side is fresh |
| contract test covers it | no, if the test reads both real sides |
| written by hand on both sides | **yes**: nothing else fails when one side moves |

**Key rule:** every link between components declares its enforcement (`shared-code`, `generated`, `schema-tests`, `duplicated`, `convention`, `none`). A link marked `duplicated` must carry a mechanical guard that reads both sides.

## Guard Kinds

| Guard | Checks | Typical seam |
|---|---|---|
| join | a value extracted by regex from each file is identical | API version, header name, pipe name |
| set | the members extracted from each side match | DTO fields, enum values, env var names |
| pair | two marked regions of duplicated logic; editing one fails until someone re-reads the other and attests | the same rounding or price rule in two languages |
| ui_actions | every UI control reaches a handler, every handler has a control | hand-written dispatch tables |
| anchor | a literal exists in a file, so the map cannot claim code that is gone | any block or link end |

## Crossweft: One Implementation

[Crossweft](https://github.com/AnastasiyaW/crossweft) (Apache-2.0, Python 3.9+ stdlib only) keeps a map of components (*blocks*) and *links*, checks every guard, and plugs into Claude Code hooks and a Codex skill. Project page: [happyin.work/crossweft](https://happyin.work/crossweft/).

```bash
# local install by tag
python -m pip install "git+https://github.com/AnastasiyaW/crossweft.git@v0.4.0"
# in CI pin the release commit (a tag can be moved); v0.4.0 = 9880dfe
python -m pip install "git+https://github.com/AnastasiyaW/crossweft.git@9880dfe52c0f1cc1f35ecc5694cf315ebc6cbf02"
crossweft init --example
crossweft check            # RESULT: PASS
```

### A link and its guards

```json
{
  "id": "web-orders", "from": "web", "to": "api", "transport": "https",
  "contract": {"name": "Orders API", "enforcement": "duplicated"},
  "from_anchors": [{"path": "web/src/api.ts", "find": "export async function getOrder"}],
  "to_anchors": [{"path": "server/main.go", "find": "r.Route(\"/v1\""}],
  "signals": {"red": true}
}
```

```json
{
  "joins": [{
    "id": "api-version", "link": "web-orders",
    "points": [
      {"path": "web/src/api.ts", "side": "web", "regex": "API_VERSION = \"([^\"]+)\""},
      {"path": "server/main.go", "side": "api", "regex": "APIVersion = \"([^\"]+)\""}
    ]
  }],
  "sets": [{
    "id": "order-fields", "link": "web-orders", "mode": "equal",
    "left":  {"paths": ["web/src/api.ts"], "within": "interface Order \\{([^}]*)\\}", "regex": "^\\s*([a-z_]+)\\??:"},
    "right": {"paths": ["server/main.go"], "within": "type Order struct \\{([^}]*)\\}", "regex": "json:\"([a-z_]+)"}
  }]
}
```

### What the agent sees

After an edit to one side, the PostToolUse hook names the other side (demo output, shortened to the first of three links):

```text
crossweft: server/main.go is part of 3 cross-component seam(s). Keep both sides in agreement:
- link web-orders (web -> api, https; Orders API [duplicated]): you changed its to side.
  Re-read: web/src/api.ts. Guarded by: join:api-version, join:version-header,
  set:order-fields, set:web-statuses, pair:price-rounding.
...
Run `crossweft check` before you finish.
```

If the agent tries to stop with the sides out of agreement, the Stop hook runs the check and sends it back with the exact disagreement:

```text
- join:api-version disagrees: web@web/src/api.ts:3='2026-09-01'; api@server/main.go:14='2026-10-01'
```

## Commands Worth Knowing (0.4.0)

| Command | Use |
|---|---|
| `check [--incremental]` | verify map vs code; `--incremental` reruns only guards whose files changed since the last pass |
| `impact <file>` | which seams a change touches and where the other side lives |
| `attest` | record that both regions of a pair were read and agree |
| `baseline` | adopt in a repo with existing drift: record it as open findings, new drift still fails |
| `discover` / `import` | list unmapped seams; build guards from OpenAPI JSON or `.proto` |
| `report` | HTML map with what the check found on it |
| `signals` | JSON catalog of the alarm rules the map implies: health checks, heartbeats, HTTP requests/errors/latency, queue depth and dead letters, probes, a watchdog |
| `doctor` | which installed copy runs and whether another shadows it |
| `mcp` | read-only MCP server for agents |

Exit codes are three-state: `0` pass, `1` fail, `2` not verified (for example "scanned nothing"). Treat `2` as not green.

## Rolling It Out Across Repositories

1. `crossweft init` in each repo: it writes `crossweft.json`, an empty model, the hooks, the `AGENTS.md` block and the skill.
2. Map the blocks first, then links with `duplicated` enforcement; add a guard per such link.
3. `baseline` the existing drift, each finding with an owner and next step.
4. CI installs Crossweft pinned to a release **commit**; the same commit runs the local hook.
5. Upgrade one repo at a time: bump the pin and run `crossweft render` + `crossweft agents` in the same commit.

## Gotchas

- **Issue:** one shared Crossweft install checks many repos, each pinned to a different version in CI. Measured 2026-11-05 on four repos moving from 0.3.0 to 0.4.0: every failure was generated output (`viewer.html`, the `AGENTS.md` block, the skill file), no map had changed, yet all four went red at once. -> **Fix:** run each repo's own pinned version locally, and upgrade per repo with the re-render in the same commit.
- **Issue:** installing from a tag (`@v0.4.0`) in CI; a tag can be moved and silently changes what CI runs. -> **Fix:** pin the release commit, keep the tag in a comment.
- **Issue:** a join regex also matches a documented alternative value further down the file, so the check fails although the defaults agree. -> **Fix:** narrow the point with `within` (a capture region); every match inside it still counts.
- **Issue:** the Stop hook runs a full check on a large map (measured 385 s on 1,140 files). -> **Fix:** `check --incremental` (38 s after one edit on the same map).
- **Issue:** `crossweft validators` in CI for a repo that declares no validators exits `2` and fails the job. -> **Fix:** add that CI step only together with `validators.dir`; exit `2` means "no verdict", by design.
- **Issue:** more than one installed copy on a machine; the hook may run a different copy from the one you upgraded. -> **Fix:** `crossweft doctor` shows which copy runs and whether another shadows it.
- **Issue:** a `queue` signal on an HTTP link is rejected as a schema error. -> **Fix:** queue signals belong only on queue transports; use `red` for HTTP links.

## A Configuration Kit That Uses It

[codex-claude-code-config](https://github.com/AnastasiyaW/codex-claude-code-config) is a public configuration system for Claude Code and Codex: principles, enforcement hooks, skills, drop-in rules and templates. It runs Crossweft as a Stop gate alongside its own hooks.

## Sources

- [Crossweft repository](https://github.com/AnastasiyaW/crossweft)
- [Crossweft v0.4.0 release](https://github.com/AnastasiyaW/crossweft/releases/tag/v0.4.0)
- [Crossweft agent integration](https://github.com/AnastasiyaW/crossweft/blob/main/docs/agents.md)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)

## See Also

- [[claude-code-harness-patterns]]
- [[claude-code-ecosystem]]
- [[multi-session-coordination]]
