---
date: 2026-04-13
authors:
  - anastasiia
categories:
  - Engineering
description: "How a 582-line CLAUDE.md prevents AI agents from breaking production systems"
---

# My CLAUDE.md is 582 lines. Here's why.

Every new Claude Code chat starts from scratch. The agent doesn't know your project, doesn't remember what you discussed an hour ago in another window, has no idea that a specific port on your server is off-limits. You explain the same things for the fifth time, and on the sixth try the agent still goes in to "fix" a config that was working fine.

Every week on r/ClaudeAI there's a new story. An agent deleted a production database. An agent pushed secrets to a public repo. An agent "optimized" a billing service and charged customers zero. Each time you read it, you think: I really don't want to be that person in the headline.

CLAUDE.md is supposed to solve both problems - context between sessions and protection against catastrophes. A typical CLAUDE.md at 5-10 lines solves neither. I decided to approach this as an architecture problem, not a list of reminders.

<!-- more -->

My config is now 582 lines, 6 layers, and every rule has a specific incident behind it.

## Three incidents that changed everything

**The agent "fixed" a working system.** Sunday evening. The agent sees `127.0.0.1` in a config pointing at an external storage service. It decides the previous session left a bug - localhost instead of a real address. Logical, right? It swaps in the real IP. Uploads break. Thirty minutes of debugging later, you realize: that was an SNI proxy through a local tunnel. `127.0.0.1` was the correct value. Without context, the obvious fix was a catastrophe.

The rule that appeared: "don't change configs without understanding why the current values are what they are. If a value looks wrong, understand it first."

**fail2ban flagged the agent as a brute-forcer.** The agent was checking server health. For each check, it opened a new SSH connection. Ten connections in a minute - fail2ban interpreted this as a brute-force attack and blocked the IP for thirty minutes. A model was training on the server at the time, and I lost access to it.

The rule: "one SSH bridge for everything. One client per session. Don't write separate scripts for check, fix, verify - merge them into one."

**"Filter" meant "delete."** I asked the agent to filter a dataset - remove unsuitable images. The agent interpreted it literally: deleted the files. Not moved. Not flagged. Deleted. The data was gone.

The rule: "'filtering' = move or flag, not delete. Before any deletion, confirm the user explicitly asked to delete."

Writing "be careful" doesn't work. You need a system.

## Six layers: how it's structured

None of the layers were planned. Each one appeared after a specific problem.

**Layer 1: Rules** (9 files). A set of rules that load based on context. Agent writing an article? It doesn't need SSH rules. Debugging code? It doesn't need writing guidelines. Claude Code can activate relevant rules files depending on the task.

**Layer 2: Memory** (78 files). This appeared when the agent forgot server configuration for the third time. Between sessions it now remembers: infrastructure settings, project decisions, my preferences, past mistakes. Files are linked with `[[filename]]` references - 178 cross-links, creating a knowledge graph out of plain markdown. Some always load (core rules), others load on demand.

**Layer 3: Handoffs.** These appeared when a new chat repeated a dead-end from the previous one. When closing a chat, the agent writes a summary: what was done, what did NOT work (the most valuable part), one next action. Here's a real handoff:

```
## Session goal
Color checker: CNN sweep + diffusion, first visual results.

## Done
- CNN baseline: median 1.99 deg (11M params, 21 MB)
- Sweep on 5 GPUs: crop128(3.17), bs16(2.04), lr3e-4(NaN)
- Diffusion training started: epoch 5/50, loss 0.827

## Didn't work
- EfficientNet-B0: hash mismatch in Docker image
- lr=3e-4: NaN after epoch 10-13, no gradient clipping
- CNN visually: 3 numbers cause parasitic casts

## Next step
Inference script for diffusion + visual sheets with 24 patches
```

The next chat reads 1500 tokens instead of re-analyzing the whole project. Over 4 days I accumulated 27 handoffs - not one dead-end repeated. It also works across accounts: with multiple active Claude subscriptions, handoffs let you pick up in a different context without re-explaining everything.

**Layer 4: Chronicles.** These appeared after 20+ handoffs, when it became unclear why the project reached its current state in the first place. A handoff answers "what's next." A chronicle answers "how did we get here." Key decisions, pivots, dead-ends. 3-7 lines per milestone.

**Layer 5: Hooks.** These appeared when the rule "check links in CLAUDE.md" stopped working after 20 minutes of a session. More on this below.

**Layer 6: Skills** (16 of them). Ready-made knowledge sets for specific tasks. The description is written as a trigger for the model: "use when: GPU hanged, need server health check" - not "helps with servers."

## A rule is a wish. A hook is a guarantee.

This is the least obvious lesson from a month of this.

A rule in CLAUDE.md is an instruction in a prompt. The agent can forget it, reinterpret it, ignore it mid-session when the context is full of other things. The rule "check links before working" worked for the first ten minutes. Then the agent got absorbed in the task and forgot.

A hook is a Python script that Claude Code runs automatically on specific events: `SessionStart`, `Stop`, `PreToolUse`. The script doesn't forget, doesn't reinterpret. It executes mechanically, every time.

Example - a hook that reminds you to write a handoff before closing a long session:

```python
# remind_handoff.py (Stop hook, simplified)
age = session_age_minutes()
if age < 15:
    return  # short session, skip

if fresh_handoff_exists():
    return  # already written

# Block exit and ask for handoff
print(json.dumps({
    "decision": "block",
    "reason": f"Session {int(age)} min, handoff not written. "
              f"Write to .claude/handoffs/ before closing."
}))
```

The model itself knows when it's time - when the task is done or context is filling up. The hook catches the cases where it forgot.

If something must happen reliably - it's a hook, not a rule.

## One config line that blocked a supply chain attack

On March 31, 2026, the Sapphire Sleet group (DPRK) [compromised](https://security.elastic.co/blog/dprk-supply-chain-attack-axios) the official axios npm package (~100M downloads/week). They published version 1.14.1 with malicious code. Exposure window: 3 hours, 00:21 to 03:29 UTC.

My `.npmrc` had one line:

```ini
min-release-age=7
```

Packages published less than 7 days ago don't install. Most malicious packages are caught within 1-3 days; 7 days is a comfortable buffer.

I wasn't affected. One line in a config.

The same for Python - in `uv.toml`:

```toml
exclude-newer = "7 days"
```

## 37 papers behind the config

Many of the rules came not from personal experience but from academic research. [37 arxiv papers](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/README.md), processed into engineering principles. Here are the ones that changed my workflow the most:

**[Proof Loop](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/02-proof-loop.md).** The agent says "tests passed" - you check, tests didn't pass. Proof Loop prohibits the agent from signing off its own work. You need artifact evidence: test output, a verdict from a verifier running in a fresh session that didn't see the build process. [Source](https://arxiv.org/abs/2603.10165).

**[Structured Reasoning](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/05-structured-reasoning.md).** Instead of free-form "well, maybe it's this, or maybe that" - a format: what we know for certain from code and logs → step-by-step trace → what follows → which hypotheses were tested and discarded. On real patches, accuracy went from 78% to 93%. [Source](https://arxiv.org/abs/2603.01896).

**[Deterministic Orchestration](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/04-deterministic-orchestration.md).** If a task is deterministic - tests, linters, formatters - it goes through a shell script. Models are bad at counting, lose loop counters, mix up conditions in branches. Scripts don't.

**[Red Lines](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/15-red-lines.md).** Normal rules the agent can interpret "creatively." Red Lines are absolute prohibitions without exceptions. "No deletion without confirmation." "No changing production configs without understanding them." Each one is tied to an incident. Pattern from Chinese engineering culture (红线).

The other principles - [generator-evaluator](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/01-harness-design.md), [autoresearch](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/03-autoresearch.md), [multi-agent decomposition](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/06-multi-agent-decomposition.md), [codified context](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/07-codified-context.md), [agent security](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/10-agent-security.md), [documentation integrity](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/11-documentation-integrity.md), and 7 more - are documented in the [repo](https://github.com/AnastasiyaW/claude-code-config/blob/main/principles/README.md).

## The numbers

78 memory files. 178 cross-references. 27 handoffs over 4 days. 96.9% KV-cache hit rate across 83 sessions in a week.

The config file updates itself: after any change, the agent checks whether links have gone stale. The SessionStart hook validates automatically.

Does it work perfectly? No. An audit found 4 memory files that had dropped out of the index. Documentation drift happened in the system designed to prevent it. But it would have been worse without the system.

## What I don't know

I'm not sure all these principles are needed for everyone. For most projects, five are probably enough: Deterministic Orchestration, Structured Reasoning, Supply Chain Defense, Codified Context, Handoffs.

I'm not sure 6 layers is the minimum. Maybe I overengineered. But over a month, not once did context get lost, and not one dead-end repeated.

One of the principles (Assumption Testing) states it directly: every component encodes an assumption about what the model can't do on its own. Models improve. Remove components and measure - maybe some layers are no longer needed.

## Try it

Paste into Claude Code:

```
https://github.com/AnastasiyaW/claude-code-config - look through everything, choose what fits my project, set it up
```

Start small: Supply Chain Defense (one line in `.npmrc`) + Deterministic Orchestration (tests through scripts) + Structured Reasoning (debug format). Add more as needed.

All MIT licensed. [github.com/AnastasiyaW/claude-code-config](https://github.com/AnastasiyaW/claude-code-config)
