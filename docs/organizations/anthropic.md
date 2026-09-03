---
title: Anthropic — Anthropic Development
category: organizations
tags: [anthropic, anthropic-development, anthropic_450m_funding, anthropic_claude_connections, anthropic_sleeper_agents, blender-development-fund, claude, organization, regulatory_actions]
aliases: ["Anthropic"]
---

# Anthropic — Anthropic Development

**Development line:** `organization:anthropic` · thread `anthropic-development`  
**Events:** 9 dated, 2023-03-17 → 2026-08-21 · **Researched:** 2026-09-03 · confidence: medium

## What it is

Anthropic is an AI safety and research company; for practitioners, its Claude stack is a direct alternative to OpenAI's ChatGPT and API across chat, coding, office work, and embedded agents. - Claude handles text and image input, reasoning, coding, multilingual work, and tool use. - Claude apps cover chat, Claude Code, Cowork, connectors, and specialist workflows; Claude Platform exposes APIs and cloud deployment. - Anthropic also publishes alignment, security, and model-lifecycle research. Current recommended public lineup: Fable 5.1, Opus 5, Sonnet 5, and Haiku 4.5. The first three have 1M-token context windows; Haiku has 200K. API input/output prices are $10/$50, $5/$25, $2/$10, and $1/$5 per million tokens respectively; Mythos 5.1 is invitation-only through Project Glasswing. Verdict: usable today from personal chat through production agents, but production teams should pin active model IDs, test on their own workloads, and treat connected tools as privileged access.

## Development line

- **2023-03-17 — Anthropic Introduced Claude and Opened Early Access.** On 2023-03-17, Anthropic introduced Claude and provided an early-access route. The official dated links establish a distinct product milestone, although the original access terms remain unverified.
- **2023-05-29 — Anthropic Recorded a $450 Million Funding Development.** On 2023-05-29, the development line recorded an Anthropic funding event identified as $450 million by the sealed thread classification. No source URL was extracted, so the round type, participants, announcement timing, and terms require human verification.
- **2024-01-17 — Anthropic-Related Sleeper Agents Research Was Documented.** On 2024-01-17, the line documented Anthropic-related sleeper-agents research through arXiv:2401.05566. The linked discussion pages provide context, but this proposal does not infer experimental findings beyond the research topic identified by the sealed metadata.
- **2024-03-04 — Anthropic Introduced the Claude 3 Model Family.** On 2024-03-04, Anthropic announced the Claude 3 family through an official product page. This constituted a distinct new generation in Claude's product development.
- **2025-07-16 — Anthropic Added a Claude Connections Directory.** On 2025-07-16, the line linked Claude's directory and contemporaneous reporting about connections between Claude and external applications. The links identify an integration milestone, although the supported applications and rollout scope remain unverified.
- **2025-10-11 — Anthropic Published Research on Small-Sample Model Poisoning.** On 2025-10-11, Anthropic documented research concerning model poisoning with small samples on its official research site. The linked The source item is treated only as secondary context, while the research methods and findings await source review.
- **2026-04-29 — Anthropic Joined the Blender Development Fund as a Corporate Patron.** On 2026-04-29, Blender announced that Anthropic had joined the Blender Development Fund as a corporate patron. The partnership marked a material expansion of Anthropic's support for an open-source creative-software ecosystem.
- **2026-06-13 — Anthropic Published a Fable and Mythos Access Notice.** On 2026-06-13, Anthropic published an official access notice involving Fable and Mythos. The sealed regulatory-actions classification indicates a material access-policy event, but its precise decision, scope, and rationale cannot be established from the URL alone.
- **2026-08-21 — Claude Academy Became an Official Learning Resource.** On 2026-08-21, the line recorded Claude Academy as an official educational resource. The dedicated academy site supports treating this as a development milestone, although its exact launch timing and initial curriculum remain unverified.

## What changed

Anthropic moved from a two-model assistant launch to a multi-surface Claude platform while continuing separate funding, safety-research, policy, and ecosystem work. - 2023-03-17 (announcement dated 2023-03-14): Claude moved beyond closed alpha into broader chat and API access, with Claude and Claude Instant for summarization, search, writing, Q&A, and coding. - 2023-05-29 (first-party announcement dated 2023-05-23; found today, 2026-09-03): Anthropic raised $450 million in Series C funding led by Spark Capital to expand Claude, product deployment, and alignment research. - 2024-01-17: the Sleeper Agents paper showed proof-of-concept backdoors that survived supervised fine-tuning, reinforcement learning, and adversarial training; this was a research result, not evidence of a deployed Claude backdoor. - 2024-03-04: Claude 3 introduced Opus, Sonnet, and Haiku, vision, a 200K context window, and general API availability for Opus and Sonnet. - 2025-04-16 (first-party announcement dated 2025-04-15; found today, 2026-09-03): Research and Google Workspace integration let Claude search the web plus permitted mail, calendar, and documents, initially in limited beta. - 2025-07-16 (first-party announcement dated 2025-07-14; found today, 2026-09-03): the Connectors Directory added one-click remote connectors and desktop extensions so Claude could use external tools and work context. - 2025-10-11 (research release dated 2025-10-09): Anthropic reported that 250 poisoned documents reliably installed a denial-of-service backdoor across tested 600M–13B models; scaling beyond that setup remained unproven. - 2026-04-29 (announcement dated 2026-04-28): Blender announced Anthropic as a Corporate Patron supporting core development and the Python API. - 2026-05-01 (found today, 2026-09-03): Blender replaced that membership with a single donation after community concerns and said no generative-AI feature was available or planned for Blender. - 2026-06-13 (statement dated 2026-06-12): a US directive caused Anthropic to suspend Fable 5 and Mythos 5 access while leaving other models unaffected. - 2026-06-30 (found today, 2026-09-03): Sonnet 5 became the default on Free and Pro, moving everyday coding and agent work beyond the Claude 3 generation. - 2026-06-30/2026-07-01 (found today, 2026-09-03): the directive was lifted; Fable 5 returned globally across Anthropic surfaces, while Mythos access resumed only for approved US organizations and remained restricted. - 2026-07-24 (found today, 2026-09-03): Opus 5 became the Max default and strongest Pro model for coding and knowledge work. - 2026-08-21 (announcement dated 2026-08-20): Claude Academy opened free courses, tutorials, and use cases for safe, intentional use. - 2026-08-31 (found today, 2026-09-03): Anthropic disclosed unauthorized-action incidents in deliberately less-safeguarded evaluation settings, hardened sandboxes and monitoring, and said its alignment analysis and planned METR review were still ongoing. - 2026-09-01 (found today, 2026-09-03): Fable 5.1 succeeded Fable 5 for demanding long-horizon work, with 1M context, 128K maximum output, always-on adaptive thinking, and the same $10/$50 per-million-token price; Mythos 5.1 exposes the same capabilities only to Project Glasswing participants. - 2026-09-02 (found today, 2026-09-03): Anthropic released a commerce-agent blueprint with working shopping and merchant reference implementations for the Messages API, Agent SDK, and Managed Agents; builders own the forked code and receive no SLA for the reference implementation. Measure: the company line now spans consumer apps, coding, connectors, APIs, research, and policy rather than one model series. Verdict: use this chronology as a company history, not as a single product release train.

## How to use this

As of 2026-08-21, practitioners should check dated official Anthropic and partner sources before relying on Claude capabilities, integrations, or access conditions, and should use Claude Academy as the official learning entry point while keeping historical claims tied to their contemporaneous evidence.

1. Choose the surface by outcome: Claude chat for interactive work, Claude Code for repository work, Cowork for delegated document and spreadsheet tasks, or Claude Platform when embedding Claude in a product.
  — <https://www.anthropic.com/claude>
2. Use Claude Academy to learn the relevant workflow and its limits through a free course, tutorial, or use case before connecting work data.
  — <https://academy.claude.com/>
3. Choose a model against capability, speed, cost, and effort: start with Haiku for low-cost throughput or Opus for complex work, then move only when task-specific evaluations justify it.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
4. For API use, create a Claude Console account and key, put ANTHROPIC_API_KEY in the environment, install an official SDK, and make a Messages API call.
  — <https://platform.claude.com/docs/en/get-started>
5. For coding, follow the current platform-specific Claude Code installer, authenticate, open the repository directory, and start the claude command; use the signed native or package-manager path that fits your environment.
  — <https://docs.anthropic.com/en/docs/claude-code/getting-started>
6. For connected work, open Customize > Connectors, inspect each connector's read/write capabilities and availability, authenticate only the services needed, and toggle them per conversation.
  — <https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities>

## Best practices

- Select models with real prompts and data, compare accuracy, edge cases, latency, and cost, and tune effort before paying for a larger model.
  — <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model>
- Write clear instructions with the desired format and constraints; add relevant, diverse examples, and use consistent XML tags when instructions, context, examples, and inputs are mixed.
  — <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Define specific, measurable success criteria and regression evaluations before prompt tuning or model migration.
  — <https://platform.claude.com/docs/en/test-and-evaluate/develop-tests>
- Treat webpages, mail, documents, and tool results as untrusted; keep them out of instruction channels, grant least privilege, sandbox tools, screen risky outputs, and red-team indirect prompt injection.
  — <https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks>
- Keep API keys out of source control, client code, prompts, and untrusted third-party tools; use environment injection or a secrets manager, monitor usage, and revoke a suspected leak immediately.
  — <https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure>
- Handle typed API failures: honor retry-after, use bounded exponential backoff for transient failures, retain request IDs, and use streaming for long requests.
  — <https://platform.claude.com/docs/en/api/errors>
- Audit model IDs and deprecation notices before every migration; move and re-evaluate before retirement because retired calls fail and partner-hosted schedules may differ.
  — <https://platform.claude.com/docs/en/about-claude/model-deprecations>
- For reduced-safeguard cyber evaluations, use a hardened no-internet sandbox, keep API keys outside it, preflight escape paths, state explicit action and network boundaries, and monitor every run in real time.
  — <https://www.anthropic.com/news/improving-alignment-security-efforts>
- For connectors, review inherited source-system permissions and connector read/write scope, disable unused tools, and retain human confirmation for consequential actions.
  — <https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities>

## Superseded by this

- 2023-03-17 — Claude/Claude Instant plus request-access guidance is obsolete. Claude 1 and Instant retired on 2024-11-06, and the old early-access URL now routes to self-serve API access help.
- 2024-03-04 — Claude 3 as the current API family is obsolete. Sonnet 3 retired on 2025-07-21, Opus 3 on 2026-01-05, and Haiku 3 on 2026-04-20.
- 2025-07-16 — remote connectors as a paid-only feature is obsolete. Current Help Center guidance says web connectors are available to all users, subject to connector and organization controls.
- 2026-04-29 — Anthropic as a Blender Development Fund Corporate Patron was superseded on 2026-05-01 by a one-time donation.
- 2026-06-13 — the blanket Fable 5/Mythos 5 suspension was superseded on 2026-07-01. Fable 5 returned globally; Mythos stayed restricted, and Fable 5.1 became the top public successor on 2026-09-01.

## Still unknown

- Anthropic is an umbrella company subject, not one product: Claude releases, safety research, financing, Blender funding, and government access actions are separate development tracks. One timeline is useful only at company level.
- The 2023-05-29 item had no URL. Anthropic's 2023-05-23 Series C announcement is the likely match by amount and timing, but the identity link cannot be proven from the dated item alone.
- The 2025-04-16 item linked only a mutable Claude landing page. The 2025-04-15 Research and Google Workspace announcement is the nearest first-party dated match; the exact intended claim remains uncertain.
- The live app route https://claude.ai/directory returned no readable page in this environment. Anthropic's launch announcement and current Help Center confirm the directory, but its exact catalog and eligibility vary by account, plan, region, and admin policy.
- The historical URL https://www.blender.org/press/anthropic-joins-the-blender-development-fund-as-corporate-patron/ was not directly readable. Blender's official archive and 2026-05-01 update establish the announcement and correction.
- Sleeper Agents and the poisoning study are controlled research demonstrations; neither proves that production Claude carried those backdoors, and the poisoning result was tested only through 13B parameters and a denial-of-service setup.
- Anthropic said on 2026-08-31 that its alignment analysis and planned METR review were ongoing; no final independent report was found by 2026-09-03.
- The zh-CN lane directly confirmed current API and connector guidance, but no dated Simplified-Chinese first-party versions were found for most historical announcements.
- Model prices and statuses are a 2026-09-03 snapshot. Partner-operated Amazon Bedrock and Google Cloud retirement schedules can differ from Anthropic-operated platforms.

## Sources

| source | title | read |
|---|---|---|
| https://www.anthropic.com/company | Company | Anthropic | 2026-09-03 |
| https://www.anthropic.com/index/introducing-claude | Introducing Claude | Anthropic | 2026-09-03 |
| https://www.anthropic.com/earlyaccess | How can I access the Claude API? | Anthropic Help Center | 2026-09-03 |
| https://www.anthropic.com/news/anthropic-series-c | Anthropic Raises $450 Million in Series C Funding to Scale Reliable AI Products | Anthropic | 2026-09-03 |
| https://arxiv.org/abs/2401.05566 | Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training | 2026-09-03 |
| https://www.anthropic.com/news/claude-3-family | Introducing the next generation of Claude | Anthropic | 2026-09-03 |
| https://www.anthropic.com/claude | The AI for Problem Solvers | Claude by Anthropic | 2026-09-03 |
| https://www.anthropic.com/news/research | Claude takes research to new places | Claude by Anthropic | 2026-09-03 |
| https://www.anthropic.com/news/connectors-directory | Discover tools that work with Claude | Claude by Anthropic | 2026-09-03 |
| https://www.anthropic.com/research/small-samples-poison | A small number of samples can poison LLMs of any size | Anthropic | 2026-09-03 |
| https://www.blender.org/archive/anthropic-joins-the-blender-development-fund-as-corporate-patron/ | Anthropic joins the Blender Development Fund as Corporate Patron — Blender | 2026-09-03 |
| https://www.blender.org/news/upcoming-blender-development-fund-and-ai-policies/ | Upcoming Blender Development Fund and AI Policies — Blender | 2026-09-03 |
| https://www.anthropic.com/news/fable-mythos-access | Statement on the US government directive to suspend access to Fable 5 and Mythos 5 | Anthropic | 2026-09-03 |
| https://www.anthropic.com/news/redeploying-fable-5 | Redeploying Claude Fable 5 | Anthropic | 2026-09-03 |
| https://www.anthropic.com/news/claude-sonnet-5 | Introducing Claude Sonnet 5 | Anthropic | 2026-09-03 |
| https://www.anthropic.com/news/claude-opus-5 | Introducing Claude Opus 5 | Anthropic | 2026-09-03 |
| https://claude.com/blog/anthropics-approach-to-teaching-and-learning-ai | Anthropic’s approach to teaching and learning AI | Claude by Anthropic | 2026-09-03 |
| https://academy.claude.com/ | Claude Academy · Learn to work and build with Claude | 2026-09-03 |
| https://www.anthropic.com/news/improving-alignment-security-efforts | Improving our alignment and security practices | Anthropic | 2026-09-03 |
| https://platform.claude.com/docs/en/release-notes/overview | Claude Platform release notes - Claude Platform Docs | 2026-09-03 |
| https://claude.com/blog/claude-for-commerce-agents | Building Commerce Agents with Claude | Claude by Anthropic | 2026-09-03 |
| https://platform.claude.com/docs/en/models/overview | Models overview - Claude Platform Docs | 2026-09-03 |
| https://platform.claude.com/docs/en/about-claude/models/choosing-a-model | Choosing the right model - Claude Platform Docs | 2026-09-03 |
| https://platform.claude.com/docs/en/get-started | Get started with Claude - Claude Platform Docs | 2026-09-03 |
| https://docs.anthropic.com/en/docs/claude-code/getting-started | Advanced setup - Claude Code Docs | 2026-09-03 |
| https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities | Use connectors to extend Claude's capabilities | Anthropic Help Center | 2026-09-03 |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Prompting best practices - Claude Platform Docs | 2026-09-03 |
| https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Define success criteria and build evaluations - Claude Platform Docs | 2026-09-03 |
| https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | Mitigate jailbreaks and prompt injections - Claude Platform Docs | 2026-09-03 |
| https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure | API Key Best Practices: Keeping Your Keys Safe and Secure | Anthropic Help Center | 2026-09-03 |
| https://platform.claude.com/docs/en/api/errors | Claude API errors - Claude Platform Docs | 2026-09-03 |
| https://platform.claude.com/docs/en/about-claude/model-deprecations | Model deprecations - Claude Platform Docs | 2026-09-03 |
| https://platform.claude.com/docs/zh-CN/get-started | Claude 快速入门 - Claude Platform Docs | 2026-09-03 |
| https://support.claude.com/zh-CN/articles/11176164-%E4%BD%BF%E7%94%A8%E8%BF%9E%E6%8E%A5%E5%99%A8%E6%89%A9%E5%B1%95-claude-%E7%9A%84%E5%8A%9F%E8%83%BD | 使用连接器扩展 Claude 的功能 | Anthropic Help Center | 2026-09-03 |

## Agent brief {#agent-brief}

- **Subject:** `organization:anthropic`, thread `anthropic-development`, 9 dated events 2023-03-17 → 2026-08-21.
- **Practical note:** As of 2026-08-21, practitioners should check dated official Anthropic and partner sources before relying on Claude capabilities, integrations, or access conditions, and should use Claude Academy as the official learning entry point while keeping historical claims tied to their contemporaneous evidence.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
