---
title: GLM-5.2 — Model availability
category: projects
date: 2026-06-14
tags: [glm-5-2, glm_models, model-availability, project]
aliases: ["GLM-5.2"]
---

# GLM-5.2 — Model availability

**Development line:** `project:glm-5-2` · thread `model-availability`  
**Last event:** 2026-06-14 · 1 dated since 2026-06-14 · **Researched:** 2026-09-05 · confidence: medium

## What it is

GLM-5.2 is a still-listed Z.ai model for software-engineering agents.

- Reasoning
- Streaming
- Function calls
- Context caching
- Structured JSON
- MCP

1M context and 128K output.

Retain GLM-5.2 for compatibility or a controlled comparison, but use GLM-5.3 for new coding work.

## Development line

- **2026-06-14 — Z.ai documentation identified GLM-5.2 as its latest model.** On 2026-06-14, Z.ai linked DevPack documentation for the latest model under the GLM-5.2 project line. This marks an availability milestone, but we did not research the post or documentation. We assert no release details, capabilities, or access terms.

## What changed

- 2026-06-14 — The linked “latest model” URL points to a GLM-5.3 switching guide, so it does not prove a GLM-5.2 launch.
- 2026-06-16 — Z.ai released GLM-5.2 and open-sourced it under MIT, adding a 1M lossless context model for long-horizon coding tasks.
- 2026-07-08 — An independent CAISI assessment added a safety caveat: deployment safeguards did not prevent agentic exploit-development assistance, and operators can remove safeguards from self-hosted open weights.
- 2026-08-18 — GLM-5.3 superseded GLM-5.2 as Z.ai’s latest flagship, with a vendor-reported 50% coding gain on Z.ai Code Bench.

## How to use this

As of 2026-06-14, check Z.ai’s DevPack latest-model documentation when selecting GLM-5.2. Do not assume an earlier GLM model remains the current documented option.

1. Create a Z.ai API client and send a Bearer-authenticated request to `https://api.z.ai/api/paas/v4/chat/completions` with `model: "glm-5.2"` and at least one user message.
  — <https://docs.z.ai/guides/llm/glm-5.2>
2. For a difficult coding task, enable thinking and set `reasoning_effort` to `max`. Cap `max_tokens` to the output actually required.
  — <https://docs.z.ai/guides/llm/glm-5.2>
3. Use `stream: true` when the caller can consume Server-Sent Event chunks. Omit it or set it to false for a synchronous response.
  — <https://docs.z.ai/api-reference/llm/chat-completion>
4. Treat returned function-call arguments as untrusted input. Validate them against the declared schema before execution.
  — <https://docs.z.ai/api-reference/llm/chat-completion>

## Best practices

- Give a refactoring task explicit business-logic, API, runtime, dependency, and verification boundaries. Require a plan and relevant test results before accepting the change.
  — <https://docs.z.ai/guides/llm/glm-5.2>
- Keep `thinking.clear_thinking` enabled for ordinary chat. Preserve prior reasoning only when the complete, unmodified, correctly ordered history is available.
  — <https://docs.z.ai/api-reference/llm/chat-completion>
- Evaluate GLM-5.3 first for new coding deployments. Keep GLM-5.2 only where its model ID is an intentional compatibility constraint.
  — <https://docs.z.ai/guides/llm/glm-5.3>

## Superseded by this

- :

## Still unknown

- The 2026-06-14 item predates Z.ai’s confirmed 2026-06-16 release. Available first-party material confirms advance Coding Plan access before release but does not date that preview to June 14.
- Z.ai’s official pages disagree on GLM-5.3 timing. The research index shows 2026-08-14, while release notes show 2026-08-18; we use the latter for the supersession date.
- We made no authenticated API request. Account-specific availability, quota, and regional access remain unverified.

## Sources

| source | title | read |
|---|---|---|
| https://docs.z.ai/devpack/latest-model | How to Switch Models - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://docs.z.ai/release-notes/new-released | New Released - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://www.zhipuai.cn/zh/research/161 | GLM-5.2上线并开源：专注Coding与长程任务 | 2026-09-05 |
| https://docs.z.ai/guides/llm/glm-5.2 | GLM-5.2 - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://docs.z.ai/api-reference/llm/chat-completion | Chat Completion - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://www.nist.gov/document/caisi-assessment-zais-glm-52 | Assessment of Z.ai’s GLM-5.2 | 2026-09-05 |
| https://docs.z.ai/guides/llm/glm-5.3 | GLM-5.3 - Overview - Z.AI DEVELOPER DOCUMENT | 2026-09-05 |
| https://www.zhipuai.cn/en/research | Research - Z.ai | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:glm-5-2`, thread `model-availability`, 1 dated events 2026-06-14 → 2026-06-14.
- **Practical note:** As of 2026-06-14, check Z.ai’s DevPack latest-model documentation when selecting GLM-5.2. Do not assume an earlier GLM model remains the current documented option.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
