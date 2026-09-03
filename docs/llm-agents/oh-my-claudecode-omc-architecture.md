---
title: "Oh My ClaudeCode (OMC) Integration"
description: "How to adopt the fast-moving OMC plugin without mistaking third-party commands, model routing, or generated state for a stable security or release boundary."
tags: [claude-code, plugins, orchestration, omc, supply-chain, worktrees]
---

# Oh My ClaudeCode (OMC) Integration

**Scope checked: 2026-09-04.** Oh My ClaudeCode (OMC) is a third-party multi-agent orchestration layer for Claude Code. Its repository currently presents a Claude Code plugin installation path and a separately published terminal package, but its commands, compatibility behavior, and internal files evolve quickly. Treat the repository and installed revision as the authority for the version you are running; do not rely on fixed agent counts, model names, token prices, or historical command aliases. [OMC repository](https://github.com/Yeachan-Heo/oh-my-claudecode) [Claude Code plugins](https://code.claude.com/docs/en/plugins)

## Choose the Installation Surface

The OMC repository documents two different surfaces:

| Surface | Use for | Boundary |
|---|---|---|
| Claude Code plugin | in-session skills, hooks, agents, and slash commands | subject to Claude Code plugin policy |
| terminal package | setup, update, diagnostics, and documented CLI workflows | local executable with its own dependencies |

The documented plugin setup is:

```text
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
```

The repository also documents the separately named terminal package. Install only through its current documentation and inspect the resulting version before treating any CLI example as runnable. In particular, the project distinguishes in-session skills from terminal commands; do not invent an OMC CLI subcommand because a similarly named slash command exists. [OMC README](https://github.com/Yeachan-Heo/oh-my-claudecode)

## Treat OMC as an Integration, Not a Trust Boundary

OMC can coordinate planning, review, and multiple local provider CLIs, but it does not replace:

- repository instructions and deterministic validation;
- code review and release approval;
- tenant, credential, or production authorization;
- Git history, worktree isolation, and external idempotency;
- a supply-chain review of plugins and local dependencies.

Its generated artifacts are useful operational evidence only when they identify the input revision, command, output, and owner. A plan, consensus loop, or agent label does not prove that a build, migration, or external side effect succeeded.

## Safe Adoption Pattern

Before enabling the plugin in a work repository:

1. pin and record the repository or package revision being evaluated;
2. inspect the plugin manifest, declared agents, skills, hooks, MCP configuration, and setup script;
3. identify every external CLI or provider the workflow may invoke;
4. test in an isolated worktree with non-production credentials and data;
5. run the repository's own checks after the plugin changes files;
6. retain a rollback path and remove the integration through its supported mechanism if it fails review.

Claude Code plugins package skills, agents, hooks, MCP servers, and other components. The installation source therefore deserves the same scrutiny as any other executable dependency. [Plugins reference](https://code.claude.com/docs/en/plugins-reference)

## Team and Provider Routing

The current OMC repository describes Team as its canonical orchestration surface and documents migration away from legacy swarm terminology. That is a repository-version fact, not a general multi-agent standard. Verify the installed documentation before scripting a command or training an operator on a shortcut. [OMC README](https://github.com/Yeachan-Heo/oh-my-claudecode)

When a workflow routes a task to another local or remote provider:

1. classify the input before forwarding it;
2. keep credentials, customer content, private source, and secrets out of third-party prompts unless an approved data path exists;
3. record which provider, model, and CLI revision actually ran;
4. treat returned text as untrusted until the repository's checks and human or independent review validate it;
5. avoid automatic provider fallback for mutations unless the fallback contract is explicit.

The useful boundary is not “multi-model”; it is a reviewed transfer contract with an observable result.

## Worktrees and Durable State

Use Git worktrees or equivalent isolated checkouts for concurrent writers. A coordinator should maintain one task record containing ownership, target revision, expected checks, external reservation/idempotency key, and a terminal receipt. Never let two workers modify the same file set merely because an orchestration tool calls them a team.

Generated state may be an implementation detail of the installed OMC version. Keep project decisions, source changes, release evidence, and handoff records in repository-owned paths with reviewable formats rather than relying on a plugin cache as the only source of truth.

## Upgrade Procedure

1. read the upstream release notes and current installation instructions;
2. record the existing plugin/package revision and configuration;
3. update in a disposable or isolated repository first;
4. run the documented diagnostic command if the project provides one;
5. compare installed components and configuration changes;
6. run representative non-production tasks and the repository's validation;
7. promote only with a rollback revision and receipt.

This catches removed aliases, changed tool access, generated-state migrations, and behavior changes before they affect release work.

## Gotchas

- **A historical OMC command still appears in a blog post.** It may have been renamed or removed. **Fix:** use the current repository documentation for the installed revision.
- **A plugin is installed directly into a production repository.** Hooks or setup can alter behavior before review. **Fix:** inspect and test in an isolated worktree first.
- **A planner produces a detailed artifact.** Detail is not verification. **Fix:** bind each task to the repository's real tests, builds, and release receipts.
- **A routed provider receives private source by default.** That can violate the data boundary. **Fix:** classify and minimize input before any transfer.
- **Parallel workers edit the same files.** An orchestration label does not serialize writes. **Fix:** assign exclusive file ownership or use separate worktrees and integrate through review.

## Sources

- [Oh My ClaudeCode repository and current README](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code subagents](https://code.claude.com/docs/en/subagents)

## See Also

- [[claude-code-harness-patterns]]
- [[adaptive-patterns-for-autonomous-agents]]
- [[multi-session-coordination]]
- [[agent-orchestration]]
