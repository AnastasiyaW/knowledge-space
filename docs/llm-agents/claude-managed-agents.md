---
title: "Organization-Managed Claude Code Subagents"
description: "Define organization-managed Claude Code subagents with explicit scope, precedence, tool limits, and verification rather than treating managed configuration as a cloud execution runtime."
tags: [claude-code, subagents, managed-settings, governance, permissions]
---

# Organization-Managed Claude Code Subagents

**Scope checked: 2026-09-04.** In current Claude Code documentation, a managed subagent is an organization-provided subagent definition distributed through managed settings. It is not a hosted “Brain/Hands/Session” runtime, a provider-priced sandbox product, or a guarantee of persistent cloud execution. Managed definitions use the same Markdown and YAML-frontmatter format as user and project subagents, and take precedence when an identically named definition exists at a lower scope. [Claude Code subagents](https://code.claude.com/docs/en/subagents)

## Definition Scopes and Precedence

| Scope | Intended use | Owner |
|---|---|---|
| user | personal reusable workflows | individual developer |
| project | repository-specific shared workflow | repository team |
| managed | organization policy and centrally maintained agents | organization administrator |
| plugin | distributable third-party or internal package | plugin publisher |

Choose the narrowest scope that has the required owner. A managed definition may override a project or user definition with the same name, so names should be treated as part of the organization policy surface. [Subagent configuration](https://code.claude.com/docs/en/configuration)

## Define a Bounded Agent

An agent definition contains frontmatter followed by the agent's Markdown instructions. The example below is deliberately read-only; adapt exact fields and permitted tools to the current Claude Code reference before rollout.

```markdown
---
name: policy-reviewer
description: "Read-only review of dependency and repository policy changes."
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
---

Inspect the requested revision. Return findings with file references,
severity, evidence, and the smallest corrective action. Do not modify files.
```

Keep the description specific enough that automatic delegation is predictable. The body should define what evidence matters, which tools are allowed, the stop condition, and the required response structure. A role title alone is not a safety boundary. [Create custom subagents](https://code.claude.com/docs/en/subagents)

## Separate Configuration from Execution

Managed settings can distribute a definition, but they do not prove that a task ran in a particular container, region, account, or retention model. Establish those facts at the execution layer:

1. record the client version, effective settings source, and workspace revision;
2. constrain tools and permissions before the task begins;
3. give the agent the smallest data and repository scope needed;
4. store external side-effect receipts and idempotency keys outside the chat;
5. run the task's deterministic validation;
6. require an independent review when the change is material.

Do not attach fixed latency, cost, session-persistence, or data-residency numbers to a configuration feature unless the vendor publishes a current contract for the exact runtime.

## Plugin Boundaries

Plugins can ship specialized agents, skills, hooks, MCP servers, and related components. Claude Code documents an important restriction: plugin-supplied subagents do not support hook, MCP-server, or permission-mode frontmatter fields; those fields are ignored. If a workflow needs such controls, use the appropriate user, project, or managed settings layer and review the effective policy. [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

This prevents a plugin agent declaration from quietly becoming a universal trust boundary. A plugin can still influence work through its instructions and declared components, so treat installation and updates as a supply-chain decision.

## Operational Pattern

Use a clear contract for each centrally managed agent:

| Contract field | Example |
|---|---|
| trigger | a repository policy review is requested |
| input boundary | checked-out revision and declared paths only |
| tool boundary | read/search/test commands, no writes |
| output | structured findings with source/test receipt |
| escalation | unknown authorization or production target |
| failure signal | nonzero check, missing evidence, or explicit blocked state |
| owner | organization team that maintains the definition |

Record which effective definition ran. A change to a managed policy can alter an agent's behavior without changing the repository, so a release receipt needs both the project revision and the applicable managed configuration version or identifier.

## Rollout and Change Control

1. review the agent definition like production configuration;
2. test it on a disposable or isolated worktree;
3. confirm that lower-scope duplicates do not shadow the intended definition;
4. run representative allowed and denied tool calls;
5. publish the expected findings/output contract;
6. keep a rollback version and a dated deployment record.

For a security or compliance agent, do not let the same agent author a change and certify it. Use a separately scoped reviewer or a deterministic gate.

## Gotchas

- **A project agent and a managed agent share a name.** The effective behavior may be the managed definition. **Fix:** use explicit names and verify the active source before release.
- **A plugin agent declares permissions in frontmatter.** Those fields are ignored for plugin-supplied agents. **Fix:** move required controls to a supported settings scope and verify them there.
- **An agent can read a secret but is told not to reveal it.** Text instructions alone are not a capability boundary. **Fix:** do not provide unnecessary secret access.
- **A review output says PASS without evidence.** A conclusion is not a release receipt. **Fix:** require command results, source references, or observed artifacts.
- **An organization update changes behavior silently.** Reproduction becomes difficult. **Fix:** record managed-configuration identity in the task receipt.

## Sources

- [Claude Code subagents](https://code.claude.com/docs/en/subagents)
- [Claude Code settings and subagent configuration](https://code.claude.com/docs/en/configuration)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code extension overview](https://code.claude.com/docs/en/features-overview)

## See Also

- [[claude-code-harness-patterns]]
- [[agent-orchestration]]
- [[agentic-security-2026]]
- [[multi-session-coordination]]
