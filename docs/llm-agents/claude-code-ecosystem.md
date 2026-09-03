---
title: "Claude Code Extension and Governance Surfaces"
description: "Use Claude Code plugins, skills, hooks, project instructions, and subagents as explicit, versioned governance surfaces; verify their current schema and effective scope before rollout."
tags: [claude-code, plugins, skills, hooks, subagents, governance]
---

# Claude Code Extension and Governance Surfaces

**Scope checked: 2026-09-04.** Claude Code can extend a session through project instructions, plugins, skills, hooks, and subagents. These are separate control surfaces with different lifecycles and authority. Do not treat a convenient extension as proof that a task ran in a particular cloud environment, that a policy is enforced everywhere, or that a plugin is safe to install.

## Choose the Smallest Control Surface

| Need | Appropriate surface | Evidence to retain |
|---|---|---|
| stable repository guidance | project instruction file | reviewed source revision and effective instructions |
| reusable task playbook | skill | trigger, scope, and validation outcome |
| deterministic reaction to a lifecycle event | hook | event schema, handler source, exit/decision record |
| distributable bundle of related extensions | plugin | source, version, declared components, and install approval |
| bounded delegated investigation or implementation | subagent | tool boundary, input revision, output evidence, and verifier result |

A short instruction cannot reliably enforce a destructive-operation policy. A hook cannot decide a product requirement that needs human judgment. A subagent description is not an authorization grant. Put each control at the layer that can actually prove or enforce it.

## Project Instructions Are a Policy Layer

Keep repository guidance concise, task-relevant, and reviewable. It should name the normal validation command, important architecture boundaries, protected data, and escalation rules. It should not duplicate a linter or pretend that a natural-language instruction is a sandbox.

Claude Code documents its project-memory system and instruction-file loading separately from plugins and hooks. Inspect the current effective instruction sources in the target client before relying on precedence or automatic inclusion. [How Claude remembers your project](https://code.claude.com/docs/en/memory)

A useful instruction answers four questions:

1. what repository or path is in scope;
2. what the agent may read, change, or execute;
3. what evidence decides success;
4. when it must stop and ask an owner.

## Plugins Are Supply-Chain Inputs

A plugin can bundle capabilities such as commands, agents, skills, hooks, and MCP-related configuration. Its package shape and supported fields evolve, so use the current plugin reference instead of copying an old manifest from a blog or repository. [Create plugins](https://code.claude.com/docs/en/plugins)

Before installation or update, record:

- publisher and immutable source revision;
- declared components and their tool/network behavior;
- required secrets, data paths, and external endpoints;
- compatibility evidence for the target Claude Code version;
- rollback or disable procedure;
- validation result in a disposable or non-production workspace.

Do not approve a plugin merely because its command name sounds familiar. A bundled hook or MCP integration can affect a much wider trust boundary than a Markdown skill.

## Hooks Need a Deterministic Contract

Current Claude Code hooks can react to lifecycle events through command, HTTP, MCP, prompt, or agent handlers. The hook reference documents the event schema, matcher behavior, input/output formats, decision controls, and supported configuration locations. [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)

For each hook, declare:

| Field | Example |
|---|---|
| trigger | a named lifecycle event and narrow matcher |
| input | documented JSON fields used by the handler |
| side effect | read-only validation, local artifact write, or notification |
| decision | no decision, allow, deny, or defer where the current event supports it |
| failure policy | timeout/error is visible and cannot silently approve a protected action |
| receipt | handler version, exit result, and affected revision |

Use hooks for mechanical rules that can be evaluated from declared input. Avoid broad shell hooks that inspect every command, scrape undeclared environment variables, or make network calls without an explicit allowlist and timeout. A no-output successful exit is not the same thing as a security review.

## Delegate with Subagent Boundaries

A subagent is useful when its input, tools, and required evidence can be bounded. Claude Code subagent definitions can scope a role, its instructions, and allowed tools; consult the current reference for placement, fields, precedence, and product-specific limitations. [Create custom subagents](https://code.claude.com/docs/en/subagents)

Use a task brief that names:

```yaml
goal: verify the changed authentication paths
input: immutable revision and declared files
tools: read, search, and named test command only
writes: none
output: findings with file, evidence, and severity
stop_when: evidence is missing or the task exceeds the declared scope
```

The main workflow must still inspect referenced artifacts and run the release gate. A subagent's prose is a candidate assessment, not a replacement for the underlying test, source, or deployment receipt.

## Roll Out Extensions Safely

1. review the extension source and ownership;
2. test it in a disposable repository or isolated worktree;
3. record the effective configuration and permitted tools;
4. run a task with a deliberately small scope;
5. verify produced artifacts and any external effects;
6. promote only after a reviewer can reproduce the result;
7. retain a disable path for hooks, plugins, and policy changes.

Treat a schema mismatch, unavailable component, or missing receipt as a visible failure. Do not silently substitute another plugin, command, provider, or permission mode.

## Common Failure Modes

- **Version folklore:** static event counts, CLI flags, or manifest fields copied from an old release.
- **Policy by prose:** a critical safety rule exists only in a long instruction file.
- **Unscoped hook:** a command handler gains access to data or network targets unrelated to its trigger.
- **Plugin-name trust:** installation occurs without source, component, or permission review.
- **Delegation without proof:** a subagent says a change works, but no test or target receipt exists.
- **Hidden fallback:** an unavailable extension causes a different capability to run without operator visibility.

## References

- [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
- [Create plugins](https://code.claude.com/docs/en/plugins)
- [Create custom subagents](https://code.claude.com/docs/en/subagents)
- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
