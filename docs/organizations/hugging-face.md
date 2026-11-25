---
title: Hugging Face
category: organizations
date: 2025-02-03
tags: [dreambooth-hackathon, hf-inference-providers, hugging-face, hugging-face-mcp, hugging-face-platform-evolution, huggingface-local-apps, organization]
aliases: ["Hugging Face"]
---

# Hugging Face

**Development line:** `organization:hugging-face` · thread `hugging-face-platform-evolution`  
**Last event:** 2025-02-03 · 4 dated since 2022-12-28 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Hugging Face is a GitHub-style ML platform for teams that publish, evaluate, run, or connect models, datasets, and AI apps.

- Hub repositories for models, datasets, and Spaces.
- Inference Providers for compatible serverless models through one API.
- MCP access to Hub search, documentation, selected Spaces, Jobs, and Sandboxes.

## Development line

- **2022-12-28 — Hugging Face published materials for a DreamBooth hackathon.** Hugging Face linked a DreamBooth Hackathon page and a Colab notebook for diffusion workflows.
- **2024-05-24 — Hugging Face added a Local Apps product path.** Hugging Face linked Local Apps task code and a settings page to support local application workflows.
- **2024-06-05 — Hugging Face published a Spaces secrets disclosure.** Hugging Face disclosed secrets in Spaces, making credential security in Spaces a public concern for maintainers and users.
- **2025-02-03 — Hugging Face announced Inference Providers.** Hugging Face announced Inference Providers as a platform route to access inference through integrated providers.

## What changed

Hugging Face expanded from hosted model collaboration into a platform with local, routed, and agent-facing execution paths.

- 2022-12-28 — DreamBooth Hackathon gave a notebook path to personalize Stable Diffusion from a handful of images and publish models to the Hub. The contest ended in January 2023.
- 2024-05-24 — Local Apps added runnable local-runtime snippets to model pages. The linked mutable source covers llama.cpp, vLLM, SGLang, and MLX, but the May 2024 implementation is not pinned.
- 2024-06-05 — Following the May 31 Space-secrets disclosure, Hugging Face rotated affected tokens, removed organization tokens from Spaces, added KMS-backed secrets, and moved users to fine-grained tokens.
- 2025-02-03 — Recorded shortly after the January 28 launch, Inference Providers shifted serverless use from a single Hub endpoint to a provider-routed API with compatible model pages, SDK support, personal provider keys, and Hugging Face-routed billing.
- 2025-06-07 — Aligned with the June 6 official MCP Server launch, MCP-compatible assistants could search Hub resources and call selected Gradio apps. It launched as experimental.
- 2026-07-22 (found today) — MCP added the hf_fs navigation tool for repositories, storage, documentation, and papers, plus Sandboxes attached to buckets and repositories.

## How to use this

Review and remediate secrets used in Hugging Face Spaces after the 2024-06-05 Spaces disclosure. Evaluate Hugging Face Inference Providers as a provider-mediated inference access path after 2025-02-03 when selecting deployment workflows.

1. Create a fine-grained access token scoped to the repository or inference task, then authenticate a development machine with hf auth login.
  — <https://huggingface.co/docs/hub/en/security-tokens>
2. Create a model, dataset, or Space repository; set owner, visibility, and license; then upload through hf upload or Git/Xet.
  — <https://huggingface.co/docs/hub/en/repositories-getting-started>
3. Publish a Model Card in the repository README with intended uses, limitations, training information, datasets, and evaluation results.
  — <https://huggingface.co/docs/hub/en/model-cards>
4. For hosted inference, select a compatible Hub model and call it through InferenceClient with an explicit model and provider when the workload needs predictable routing.
  — <https://huggingface.co/docs/huggingface_hub/guides/inference>
5. For an agent workflow, open MCP Settings while signed in, use the generated client configuration, restart the client, then add only the Hub or Space tools needed for the task.
  — <https://huggingface.co/docs/hub/en/agents-mcp>
6. For a Space, select public, protected, or private visibility deliberately and put credentials in Space Secrets rather than source code or public Variables.
  — <https://huggingface.co/docs/hub/en/spaces-overview>

## Best practices

- Use one fine-grained token per application or usage; use OIDC Trusted Publishers for CI where available instead of storing a long-lived token.
  — <https://huggingface.co/docs/hub/en/security-tokens>
- Treat the Model Card as a release requirement: state intended use, known limits, training inputs and parameters, and evaluation evidence.
  — <https://huggingface.co/docs/hub/en/model-cards>
- Set an explicit Hub model ID and named provider in production; recommended models and automatic provider selection can change.
  — <https://huggingface.co/docs/huggingface_hub/guides/inference>
- Verify model-task-provider compatibility before deployment; a model hosted on the Hub is not automatically available from every inference provider.
  — <https://huggingface.co/docs/inference-providers/index>
- Keep Space secrets out of code and Variables; Secrets are private while Variables are publicly viewable and copied with duplicated Spaces.
  — <https://huggingface.co/docs/hub/en/spaces-overview>
- Use the MCP Settings-generated configuration and keep write-capable repository tools, Jobs, Sandboxes, and community Spaces opt-in.
  — <https://huggingface.co/docs/hub/en/agents-mcp>

## Superseded by this

- 2022-12-28 — DreamBooth Hackathon prize, certificate, and leaderboard-submission workflows are obsolete because the event ended in January 2023.
- 2024-06-05 — Guidance based on broad classic read/write tokens is superseded by per-application fine-grained tokens and short-lived OIDC-issued tokens for CI.
- 2025-02-03 — Assuming a single static hosted Inference API for every Hub model is superseded by provider compatibility and explicit provider selection.
- 2025-06-07 — Hand-written fixed MCP client configuration is superseded by the generated Settings configuration and hf_fs navigation.

## Still unknown

- Hugging Face combines a repository platform, local-runtime integration layer, inference gateway, Spaces platform, and MCP connector. These events reflect a platform chronology, not one single product migration.
- The 2025-06-07 post returned no readable content during research. Hugging Face's June 6 changelog independently confirms the MCP launch, but not the post's exact wording.
- The Local Apps reference points to mutable repository source rather than an immutable May 2024 revision, so its exact historical behaviour is unverified.
- Current prices, quotas, data-processing terms, and availability were not quoted because they vary by plan, model, and provider.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/dreambooth-hackathon | DreamBooth Hackathon | 2026-09-04 |
| https://github.com/huggingface/huggingface.js/blob/main/packages/tasks/src/local-apps.ts | local-apps.ts — huggingface.js | 2026-09-04 |
| https://raw.githubusercontent.com/huggingface/huggingface.js/main/packages/tasks/src/local-apps.ts | local-apps.ts raw source | 2026-09-04 |
| https://huggingface.co/blog/space-secrets-disclosure | Space secrets leak disclosure | 2026-09-04 |
| https://huggingface.co/blog/inference-providers | Welcome to Inference Providers on the Hub | 2026-09-04 |
| https://x.com/_akhaliq/status/1931013733406445702 | x.com status 1931013733406445702 | 2026-09-04 |
| https://huggingface.co/changelog/hf-mcp-server | Connect Your MCP Client to the Hugging Face Hub | 2026-09-04 |
| https://huggingface.co/changelog/mcp-improvements-jul-26 | MCP Server Enhancements | 2026-09-04 |
| https://huggingface.co/docs/hub/en/index | Hugging Face Hub documentation | 2026-09-04 |
| https://huggingface.co/docs/hub/en/repositories-getting-started | Getting Started with Repositories | 2026-09-04 |
| https://huggingface.co/docs/hub/en/model-cards | Model Cards | 2026-09-04 |
| https://huggingface.co/docs/hub/en/security-tokens | User access tokens | 2026-09-04 |
| https://huggingface.co/docs/inference-providers/index | Inference Providers | 2026-09-04 |
| https://huggingface.co/docs/huggingface_hub/guides/inference | Run Inference on servers | 2026-09-04 |
| https://huggingface.co/docs/hub/en/agents-mcp | Hugging Face MCP Server | 2026-09-04 |
| https://huggingface.co/docs/hub/en/spaces-overview | Spaces Overview | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:hugging-face`, thread `hugging-face-platform-evolution`, 4 dated events 2022-12-28 → 2025-02-03.
- **Practical note:** After the 2024-06-05 Spaces disclosure, review and remediate any secrets used in Hugging Face Spaces; from 2025-02-03, evaluate Hugging Face Inference Providers as a provider-mediated inference access path when selecting deployment workflows.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
