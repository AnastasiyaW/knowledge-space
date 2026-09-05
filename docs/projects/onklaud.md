---
title: Onklaud 5
category: projects
date: 2026-07-02
tags: [onklaud, onklaud-5-development, project]
aliases: ["Onklaud 5"]
---

# Onklaud 5

**Development line:** `project:onklaud` · thread `onklaud-5-development`  
**Last event:** 2026-07-02 · 1 dated since 2026-07-02 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Onklaud 5: a Python orchestration tool for developers who want a code draft assessed by several language models rather than one model.

- finds known library or standard-library solutions before generation;
- runs Kimi and GLM review passes, then an arbitration loop and a local quality gate;
- accepts an OpenRouter key and can use an OpenAI-compatible local endpoint.

## Development line

- **2026-07-02 — On 2026-07-02, Onklaud 5 was linked to a public GitHub repository.** On 2026-07-02, the Onklaud 5 development line included a link to the GitHub repository KorroAi/onklaud-5. The dated link establishes a public repository reference for the project, but does not establish a release, feature set, or code change.

## What changed

2026-06-22 — current documentation says the project ran its internal benchmark suite, reporting 20 of 35 Ponytail hits and 29 of 30 pipeline checks. 2026-07-02 — Onklaud 5 was made available through the linked repository; the current checkout configures Kimi K2.7 Code and GLM 5.2, but no dated tag or commit proves that this exact state existed on the event date.

## How to use this

From 2026-07-02, practitioners should treat KorroAi/onklaud-5 as the identified public repository reference for Onklaud 5 and inspect its contents before relying on it.

1. Clone the repository, copy `.env.example` to `.env`, and set `OPENROUTER_API_KEY` for the Kimi and GLM calls.
  — <https://github.com/KorroAi/onklaud-5>
2. Run `python test_pipeline.py` as the bundled local smoke check before connecting it to a workflow.
  — <https://github.com/KorroAi/onklaud-5>
3. Check configuration with `python council.py status`, then submit a draft with `python council.py dual --type code --prompt "..." --draft-file file.py`; use `loop` for the longer pre-design, dual-review, gate, and arbitration path.
  — <https://github.com/KorroAi/onklaud-5>

## Best practices

- Treat `test_pipeline.py` as a structural smoke test, not hosted-model end-to-end proof: its default entry point runs local checks and never invokes an API test. Add a non-sensitive API canary and your own test suite before relying on a review result.
  — <https://github.com/KorroAi/onklaud-5/blob/master/test_pipeline.py>
- Do not accept a degraded council loop as a normal review: without `OPENROUTER_API_KEY`, the code explicitly warns that loop mode will run degraded; other API modes return an error.
  — <https://github.com/KorroAi/onklaud-5/blob/master/council.py>
- Confirm that your production use meets the revenue or headcount condition, or obtain a commercial licence; the BSL converts to MIT only on 2030-06-22.
  — <https://github.com/KorroAi/onklaud-5/blob/master/LICENSE>

## Superseded by this

- Guidance to treat the current repository as permissively open source is obsolete: the licence is BSL 1.1 with conditional production rights until its MIT change date (observed 2026-09-05).

## Still unknown

- A dated tag, release, or archived commit for 2026-07-02 was not available, so the current repository cannot prove its contents on that date.
- The current sources call the repository Onklaud 5 but the licence calls the licensed work v3.2; no documented mapping between those labels was found.
- The 57.1% task-resolution and quality claims are self-reported; no independent reproduction was found.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/KorroAi/onklaud-5 | KorroAi/onklaud-5 — Onklaud 5 repository and README | 2026-09-05 |
| https://github.com/KorroAi/onklaud-5/blob/master/council.py | Onklaud 5 council.py | 2026-09-05 |
| https://github.com/KorroAi/onklaud-5/blob/master/test_pipeline.py | Onklaud 5 test_pipeline.py | 2026-09-05 |
| https://github.com/KorroAi/onklaud-5/blob/master/LICENSE | Onklaud 5 Business Source License 1.1 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:onklaud`, thread `onklaud-5-development`, 1 dated events 2026-07-02 → 2026-07-02.
- **Practical note:** From 2026-07-02, practitioners should treat KorroAi/onklaud-5 as the identified public repository reference for Onklaud 5 and inspect its contents before relying on it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
