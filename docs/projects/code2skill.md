---
title: "Code2Skill: code2skill"
category: "projects"
date: 2026-09-22
tags: ["code2skill", "project"]
aliases: ["Code2Skill: code2skill"]
---

# Code2Skill: code2skill

**Development line:** project:code2skill · thread code2skill  
**Last event:** 2026-09-22 · 3 dated since 2026-09-04 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Code2Skill is a research implementation for developers building coding agents.

- Source selection: chooses source units from open repositories.
- Record creation: produces atomic operations, composite workflows, and repeating patterns.
- Behavior reconstruction: reconstructs behavior without source bodies and compares it with source code.
- Provenance storage: saves origin metadata for retrieval.

The paper reports 1,006,822 accepted records from 19,769 repositories; the repository states that model comparison does not prove program equivalence. Use it as a traceable research pipeline and inspect records, not as a formal correctness guarantee.

## Development line

- **2026-09-04 — Code2Skill: code2skill update.** The Code2Skill preprint, “Grounded Skill Synthesis from Code at Scale for Agentic Intelligence,” was submitted to arXiv.
- **2026-09-22 — Code2Skill: Converting Open Repository Code into Coding Agent Skills.** Transforms code from open repositories into coding agent skills. Source code is available before interaction and can be verified after abstraction, unlike agent-trace skills. Contains 1,006,822 verified skills from 19,769 repositories with 500+ stars, atomic operations, composite workflows, repeating patterns, behavior reconstruction verification, application conditions, anti-goals, failure cases, and provenance. Integrates into planning, primary generation, post-review, and coding RL. Planning improved all 8 pairs; post-generation verification is the most stable gain.
- **2026-09-22 — Code2Skill transforms open repository code into coding agent skills.** Converts code from open repositories into coding agent skills, with verified statistics and integration points for planning and post-generation review.
- **2026-09-22 — other reporting on this date.**
  - The preprint sets the evaluation scope at 72 protocol-matched evaluations across nine model settings and eight benchmarks; it reports improvement in 57 evaluations and describes the bank as 1,006,822 accepted records from 19,769 repositories. (2026-09-04) — <https://arxiv.org/abs/2609.05571>
  - The abstract states that CodeSkillBank contains accepted records with workflow, boundary, provenance, and source-evidence metadata, verified through source-body-blind reconstruction and source-aware comparison. (2026-09-04) — <https://searcharxiv.org/abs/2609.05571>

## What changed

Public materials now pair the research report with a runnable reference implementation. It produces accepted and rejected records, decision logs, retrieval records, prompt traces, and a purpose index. The implementation is marked pre-release and requires an intentionally configured model endpoint.

## How to use this

1. Create a virtual environment and install the implementation in editable mode.
  — <https://github.com/ant-intl/Code2Skill>
2. Configure an intentionally trusted OpenAI-compatible model endpoint, then run `code2skill run` against the target repository and an output directory.
  — <https://github.com/ant-intl/Code2Skill>
3. Review accepted and rejected records, decision logs, and traces; build a purpose index from accepted-record JSONL when retrieval is needed.
  — <https://github.com/ant-intl/Code2Skill>

## Best practices

- Use `show-prompts` to inspect model-visible prompts before making model calls, and enable public model URLs only when the endpoint is intentionally trusted.
  — <https://github.com/ant-intl/Code2Skill>
- Treat source-aware LLM comparison as a quality gate, not semantic-equivalence proof; retain provenance and inspect records before operational use.
  — <https://github.com/ant-intl/Code2Skill>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The public implementation labels itself pre-release; check its licensing and publication-gate text before production adoption.
- A separate project, leechen298/Code2Skill, uses the same name but is distinct from ant-intl/Code2Skill; search results can conflate the two.
- No public practitioner report describing first-hand deployment or operational outcomes for ant-intl/Code2Skill was located.

## Sources

| source | title | read |
|---|---|---|
| https://ant-international-research.github.io/developer-skill-hubs/ | DeveloperSkillHubs — Developer Skills from Real Code | 2026-11-25 |
| https://arxiv.org/abs/2609.05571 | Grounded Skill Synthesis from Code at Scale for Agentic Intelligence | 2026-11-25 |
| https://github.com/ant-intl/Code2Skill | ant-intl/Code2Skill | 2026-11-25 |
| https://www.alphaxiv.org/zh/abs/2609.05571 | 面向智能体智能的规模化代码驱动技能合成 | 2026-11-25 |
| https://github.com/leechen298/Code2Skill | leechen298/Code2Skill | 2026-11-25 |
| https://searcharxiv.org/abs/2609.05571 | Grounded Skill Synthesis from Code at Scale for Agentic Intelligence | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:code2skill, thread code2skill, 3 dated events 2026-09-04 → 2026-09-22.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
