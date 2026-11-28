---
title: Claude
category: projects
date: 2023-11-22
tags: [claude, claude-product-development, project]
aliases: ["Claude", "Claude 2.1"]
---

# Claude

**Development line:** `project:claude` · thread `claude-product-development`  
**Last event:** 2023-11-22 · 2 dated since 2023-05-12 · **Researched:** 2026-09-04 · confidence: high

## What it is

Claude is Anthropic’s model family for chat users, application developers, and software teams.

- Text and images: takes text and images, and returns text.
- Capabilities: supports multilingual tasks, vision, tool use, and long-context workflows.
- Surfaces: runs through chat, the Messages API, and Claude Code for repository work.

## Development line

- **2023-05-12 — Claude expanded to 100K-token context windows.** Claude grew from 9K to 100K tokens in the 100K-context release so prompts could hold whole documents and full codebases. The official article is dated 2023-05-11.
- **2023-11-22 — Claude 2.1 introduced a 200K-token context window.** Claude 2.1 raised the limit to 200K tokens, added system prompts and beta tool use, and cut false statements. The official article is dated 2023-11-21.

## What changed

Claude — the dated development line:

- 2023-05-12: The 100K-context release expanded Claude from 9K to 100K tokens so prompts could hold whole documents and codebases. The official article is dated 2023-05-11.
- 2023-11-22: Claude 2.1 raised the limit to 200K tokens, added system prompts and beta tool use, and lowered false-statement rates. The official article is dated 2023-11-21.
- 2026-09-04 (found today): Current documentation describes a model family with text-and-image input, tool use, model-specific limits, and a 200K–1M-token context range.

## How to use this

From 2023-05-12, practitioners could consider Claude for workflows requiring up to 100K tokens of context. From 2023-11-22, Claude 2.1 extended that planning envelope to 200K tokens.

1. Choose the surface: use Claude.ai for chat, the Console and API for an application, or Claude Code for a repository task.
  — <https://docs.anthropic.com/en/docs/about-claude/models/overview>
2. For API integration, create a Claude Console account and API key, export it as ANTHROPIC_API_KEY, then install the supported SDK.
  — <https://docs.anthropic.com/en/docs/get-started>
3. Choose a current model against capability, latency, cost, effort, and your task evaluation before committing to production.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
4. Make a Messages API call with the selected model, a max_tokens limit, and the user message; add tools, files, or context-management features only when the task needs them.
  — <https://docs.anthropic.com/en/docs/get-started>
5. For codebase work, install Claude Code on a supported surface, start it in the project directory, and review the file and command actions it performs.
  — <https://code.claude.com/docs/en/overview>

## Best practices

- Define specific, measurable success criteria and an evaluation set before changing prompts or models.
  — <https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>
- State the task, context, constraints, output format, and ordered steps directly. Add relevant examples when output consistency matters.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- For inputs above 20K tokens, place long documents before the query, structure multiple documents clearly, and ask for supporting quotations before synthesis.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Treat model choice and effort as performance controls alongside prompting; use evaluations to trade capability against latency and cost.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
- Pin model IDs for reproducibility and monitor their lifecycle. Dateless IDs from the 4.6 generation onward are fixed snapshots, not moving aliases.
  — <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions>

## Superseded by this

- 2023-05-12: Treating 100K tokens as Claude’s operational context ceiling is obsolete; current models range from 200K to 1M input tokens.
- 2023-11-22: Deploying Claude 2.1 guidance is obsolete; API model claude-2.1 was retired on 2025-07-21.
- 2023-11-22: Treating tool use as a beta-only capability is obsolete; current-model documentation lists tool use as a supported capability.
- Pre-4.6 alias assumptions are obsolete for current dateless model IDs: each current ID identifies a fixed model snapshot.

## Still unknown

- The two dated events are not a complete release chronology between 2023 and today; the current documentation is used only as a live snapshot.
- The supplied event dates are one day later than the official article dates: 2023-05-12 versus 2023-05-11, and 2023-11-22 versus 2023-11-21.
- Plan availability, region, platform, and pricing can differ by account and change after this snapshot; verify them in the Console before rollout.

## Sources

| source | title | read |
|---|---|---|
| https://www.anthropic.com/index/100k-context-windows | Introducing 100K context windows | Anthropic | 2026-09-04 |
| https://www.anthropic.com/index/claude-2-1 | Introducing Claude 2.1 | Anthropic | 2026-09-04 |
| https://docs.anthropic.com/en/docs/about-claude/models/overview | Models overview | Claude Platform Docs | 2026-09-04 |
| https://docs.anthropic.com/en/docs/get-started | Get started with Claude | Claude Platform Docs | 2026-09-04 |
| https://code.claude.com/docs/en/overview | Overview | Claude Code Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/models/choosing-a-model | Choosing the right model | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Define success criteria and build evaluations | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Prompting best practices | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions | Model IDs and versioning | Claude Platform Docs | 2026-09-04 |
| https://platform.claude.com/docs/en/about-claude/model-deprecations | Model deprecations | Claude Platform Docs | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:claude`, thread `claude-product-development`, 2 dated events 2023-05-12 → 2023-11-22.
- **Practical note:** From 2023-05-12, practitioners could consider Claude for workflows requiring up to 100K tokens of context; from 2023-11-22, Claude 2.1 extended that planning envelope to 200K tokens.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:91d9b0daa139e136fe3860add9ae3f5f5dacab3f8de4cb3b973ecb69396e5c13 -->
## 2026-11-20 — Claude multi-agent setup applied to theoretical black hole physics

Anthropic detailed a workflow in which several copies of Claude investigated holographic duality and anti-de Sitter space. Calculations were validated by two separate methods. Components of the proof were encoded in Lean.

## 2026-11-20 — Levent Alpöge announces Claude-assisted Riemann Hypothesis formalization claim

Mathematician Levent Alpöge announced a Claude-assisted formalization claim for the Riemann Hypothesis and the Generalized Riemann Hypothesis. It is written in Lean 4 and spread across 14 code archives. The community is reviewing it now.

## 2026-11-20 — Unverified Claude-assisted Riemann Hypothesis proof claim circulating

Reports of a Claude-assisted proof of the Riemann Hypothesis are still under formal evaluation by mathematicians. To confirm it, the Lean 4 kernel must compile the code independently.

### Usage and practices

- Formulate mathematical conjectures or theoretical physics questions, then translate the problems into formal specifications such as Lean 4. [Source](https://simonwillison.net/2026/Nov/20/levent-alpoge/)
- Run multi-copy or agentic Claude workflows to explore proof trees, expand expressions symbolically and generate formal code modules. [Source](https://habr.com/ru/articles/1110482/)
- Audit AI-generated arguments with independent verification: a formal theorem prover kernel such as Lean 4, and alternative cross-checked derivations. [Source](https://alpo.ge/remark.pdf)
- Verify AI-generated mathematical claims mechanically in an interactive theorem prover such as Lean 4, not from natural-language prose. [Source](https://alpo.ge/remark.pdf)
- Use multi-agent verification, where separate model copies compute intermediate mathematical and physical derivations independently and cross-check each other. [Source](https://habr.com/ru/articles/1110482/)

### What practitioners say

- Machine-checked proofs spare humans the fatigue of reading them. Even so, a huge AI-generated Lean archive needs independent kernel compilation and auditing before a historic claim is accepted. (2026-11-20) [Source](https://simonwillison.net/2026/Nov/20/levent-alpoge/)
- Commentators are skeptical of unreviewed AI proof claims. An extraordinary mathematical claim must be confirmed by the maintainers of the formal system and by the mathematical community before it counts as valid. (2026-11-20) [Source](https://habr.com/ru/articles/1110558/)

### Additional evidence

- 2026-11-20: Anthropic detailed a workflow in which several copies of Claude investigated holographic duality and anti-de Sitter space. Calculations were validated by two separate methods, and components of the proof were encoded in Lean. [Source](https://habr.com/ru/articles/1110482/)
- 2026-11-20: Alpöge and Claude formalized the claimed proof of the Riemann Hypothesis and the Generalized Riemann Hypothesis in Lean 4. There is no accompanying narrative paper. The result is roughly 175,000 modules across 14 archive segments, for machine verification. [Source](https://simonwillison.net/2026/Nov/20/levent-alpoge/)
- 2026-11-20: External researchers and formal mathematics communities began auditing the 175,000 Lean modules. Full validation depends on complete compilation through the Lean 4 kernel. [Source](https://habr.com/ru/articles/1110558/)

### Superseded guidance (retained for history)

- 2026-11-20: Complex AI-derived proofs were handed over as traditional human-written preprints, with no formalization in an interactive theorem prover. [Source](https://alpo.ge/remark.pdf)

### Limits and open questions

- Whether the Lean 4 formalization of the Riemann Hypothesis proof passes full independent kernel verification, with no hidden axiomatic inconsistencies.
- The exact internal multi-agent architecture and prompting pipeline Anthropic used for the black hole physics and Riemann Hypothesis workflows.
- Permanent URLs for the intermediate research checkpoints before November 2026 are missing. The search results linked through search-engine redirect wrappers.

<!-- Retained base: 1ff9770000fb565deaf10f760149bceea1a08343; article blob: 59c3f03ee16daa0d1a0a66a66ef4cfc0793233eb -->

<!-- live-update:bb4bf5ca2f86fa1a916e73890ba80258803faf7a89c73c2bee51a6bdcb88ce3a -->
## 2026-11-27 — Claude Anti-Distillation Safeguard Triggers False Positive on Set Theory Queries

Anthropic's automated anti-distillation filter cut off a corporate user's session during research on set theory and programming. It shows how sensitive the heuristic filter is on commercial accounts.

### Usage and practices

- Use an enterprise account or the Anthropic Console for programming and formal reasoning. [Source](https://habr.com/ru/companies/speshu_ai/articles/1113148/)
- Send targeted math and logic prompts interactively. Avoid high-volume repetitive formatting that looks like dataset extraction. [Source](https://habr.com/ru/companies/speshu_ai/articles/1113148/)
- Describe the problem around each intensive set theory or math query, so interactive exploration is not mistaken for distillation. [Source](https://habr.com/ru/companies/speshu_ai/articles/1113148/)
- Keep automated pipeline tests and interactive research in separate development environments on commercial tiers. [Source](https://habr.com/ru/companies/speshu_ai/articles/1113148/)

### What practitioners say

- Practitioners report false positives and session terminations from the automated anti-distillation heuristics. These hit legitimate complex tasks in mathematics and logic programming. (2026-11-27) [Source](https://habr.com/ru/companies/speshu_ai/articles/1113148/)

### Additional evidence

- 2026-11-27: The safeguard triggered during set theory and programming research on a corporate account used one to two hours daily. It flagged the task as an attempt to extract model capabilities for training a competitor. The account owner called the filter counterproductive for legitimate customer research. He still holds that Claude frontier models perform well overall. [Source](https://habr.com/ru/companies/speshu_ai/articles/1113148/)

### Superseded guidance (retained for history)

- 2026-11-27: Corporate and paid subscription tiers run without automated heuristic terminations during intensive algorithmic and mathematical workloads. [Source](https://habr.com/ru/companies/speshu_ai/articles/1113148/)

### Limits and open questions

- Anthropic has not disclosed the exact classification criteria or thresholds of the anti-distillation filter. They remain proprietary heuristics.
- English and Chinese secondary reports could not be cited. The search results from external tech media led only to opaque redirects, with no direct URLs that can be checked.

<!-- Retained base: 0087738ff12f312118dba38382b3529e33c51018; article blob: 23639ca6bbed76ac1477e411f4d409d035d0d955 -->

<!-- live-update:3eaf634df2e81989f8fc352f0f21cc3d6d5170582c3e103fecf5392e2d295bc9 -->
## 2026-11-27 — Study Evaluates Reasoning Effort in Claude 5.5 Models on Plausible-but-Wrong Django Patches

The study ran Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 at low, medium and high reasoning effort on ninety AI-generated Django patches. Higher effort cut false success rates from 67% to 45% on Opus 5.5, from 65% to 49% on Sonnet 5.5, and from 78% to 51% on Haiku 5.5.

### Usage and practices

- Set the reasoning effort by how critical the code is. Use higher effort on non-trivial patches. [Source](https://arxiv.org/abs/2611.33639)
- Run automated patch reviews in an isolated environment, against the repository-level test suites. [Source](https://arxiv.org/abs/2611.33639)
- Before merging, cross-check AI approvals with an independent hardened test suite such as SWE-ABS. [Source](https://arxiv.org/abs/2611.33639)
- For code review with Haiku or Sonnet, set maximum reasoning effort. Defect detection dropped sharply at low effort. [Source](https://arxiv.org/abs/2611.33639)
- Treat model approvals as a first filter, not as the merge gate. Keep the hardened regression suites and human review. [Source](https://arxiv.org/abs/2611.33639)

### Additional evidence

- 2026-11-27: Zax Shen, Hanling Zhang and Zixu Wang ran Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 at low, medium and high reasoning effort on ninety AI-generated Django patches from SWE-bench Verified. Against the SWE-ABS hardened test suite, fifty-five patches were plausible but wrong. Higher effort cut false success rates from 67% to 45% on Opus 5.5, from 65% to 49% on Sonnet 5.5, and from 78% to 51% on Haiku 5.5. Even at peak effort, all models approved at least 45% of the broken patches. [Source](https://arxiv.org/abs/2611.33639)
- 2026-11-27: On ninety AI-generated Django patches, higher reasoning effort cut false success rates from 67% to 45% on Claude Opus 5.5, from 65% to 49% on Sonnet 5.5, and from 78% to 51% on Haiku 5.5. [Source](https://arxiv.org/abs/2611.33639)
- 2026-11-27: The study tested Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5 on ninety AI-generated Django patches. Higher reasoning effort cut false success rates from 67% to 45% on Opus 5.5, from 65% to 49% on Sonnet 5.5, and from 78% to 51% on Haiku 5.5. [Source](https://arxiv.org/abs/2611.33639)

### Superseded guidance (retained for history)

- 2026-11-27: Assumed that low reasoning effort or a single-pass LLM review reliably finds regression bugs in AI-generated pull requests. [Source](https://arxiv.org/abs/2611.33639)
- 2026-11-27: Treated a pass on standard SWE-bench Verified tests as enough to certify a patch, without hardened test coverage. [Source](https://arxiv.org/abs/2611.33639)

### Limits and open questions

- Community forum threads and practitioner blog posts could not be cited. The search redirects carried no verified direct URLs.
- Searches returned no Simplified-Chinese technical publications or discussions that evaluate arXiv:2611.33639.


<!-- Retained base: 3622a7af3e107e3ac36acf1afac8396af5242178; article blob: 1a7e6f66c104a97afe3417f638498a8f3a9f229f -->
