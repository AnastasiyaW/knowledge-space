---
title: "Amazon"
category: "organizations"
date: 2026-11-21
tags: ["amazon-generative-ai-platform-and-models", "amazon-nova", "amazon-web-services", "amazon_bedrock_codewhisperer", "organization"]
aliases: ["Amazon"]
---

# Amazon

Amazon runs AWS Quick, an agentic AI workspace for research and workflows, competing with Google Workspace AI and Microsoft Copilot Studio.

**Development line:** organization:amazon-web-services · thread amazon-generative-ai-platform-and-models  
**Last event:** 2026-11-21 · 3 dated since 2023-04-13 · **Researched:** 2026-11-22 · confidence: medium

## What it is

AWS Quick is an agentic AI workspace for individual practitioners and enterprise teams. It is built for automated research and multi-step operational workflows, and it competes with Google Workspace AI and Microsoft Copilot Studio.

Abilities:

- Quick Research runs multi-step research
- Quick Flows orchestrates autonomous workflows
- Quick Automate runs automated validation
- Fast, Balanced and Smart modes set the reasoning speed

Usage is metered in active agentic hours. Individual tiers include free access, and paid tiers add pooled background runtime allowances. It is a managed workflow orchestrator, not a developer interface for raw foundation model API access.

## Development line

- **2023-04-13 — Amazon introduces Bedrock and expands its generative AI offering.** On 2023-04-13, Amazon introduced Amazon Bedrock as its entry into the generative AI platform market. The linked materials also place Amazon CodeWhisperer in this developer-facing AI expansion. That makes the post a material step in Amazon's generative AI development.
- **2024-12-04 — Amazon announces Amazon Nova models for Bedrock.** On 2024-12-04, Amazon announced the Amazon Nova family of AI models for use through Amazon Bedrock. It was a material step: Amazon's generative AI line moved from a platform for model access toward named first-party models.
- **2026-11-21 — AWS Quick offers free tier and Claude model access.** AWS Quick reportedly has a permanent Free plan at $0 and a 30-day Plus trial for new users. Plus costs $25/month, or $20/month billed annually. Fast, Balanced and Smart reportedly map to Claude Haiku 5.5, Sonnet 5.5 and Opus 5.5, but that mapping was not independently verified. Usage limits are measured in agentic hours. This is not free Claude API access.
  - First-party pricing documentation confirms individual Plus at $25/month ($20/month billed annually) and a Max tier at $100-$125/month. Organization plans are Essentials ($3/user/month), Professional ($20/user/month) and Enterprise ($40/user/month). They carry a flat $250/account/month infrastructure fee, and overage hours cost $3 per agent hour. (2026-11-21) — <https://aws.amazon.com/quick/pricing/>
  - A community review says Fast, Balanced and Smart reportedly correlate to Claude Haiku 5.5, Sonnet 5.5 and Opus 5.5 reasoning levels. AWS has not confirmed the mapping, and the service does not grant raw model API token access. (2026-11-21) — <https://x.com/interjc/status/2124164577743261840>

## What changed

The service grew out of earlier internal suite prototypes into a standalone agentic productivity product. It now has self-serve consumer access and governed organization plans. Individual sign-ups get a permanent Free plan and trial access to paid Plus features. Consumption is no longer counted in prompt-response tokens but in active agentic runtime hours, with tiered reasoning modes.

## How to use this

1. Go to quick.aws.com and create an individual account. That gives the permanent Free plan or a 30-day Plus trial, with no AWS account linked.
  — <https://quick.aws.com/sn>
2. Pick Fast, Balanced or Smart for each background agent task, depending on how complex the reasoning is.
  — <https://quick.aws.com/sn>
3. For teams, link an AWS account to get the governed tiers. Then track consumed agentic hours against the monthly pool allowances.
  — <https://aws.amazon.com/quick/pricing/>

## Best practices

- Use Fast or Balanced for standard summarization and multi-step search, so the agentic runtime hours last. Keep Smart for deep multi-document reasoning.
  — <https://quick.aws.com/sn>
- Set spending and usage alerts on organization accounts, so long background workflows do not run into the $3 per agent hour overage charge.
  — <https://aws.amazon.com/quick/pricing/>

## What practitioners say

- Vendor documentation does not verify that the modes match specific Claude variants. Agentic hours meter workflow execution, not standard foundation model API tokens. (2026-11-21)
  — <https://x.com/interjc/status/2124164577743261840>

## Superseded by this

- AWS AI agent workflows used to need dedicated Bedrock API token provisioning and a custom orchestrator deployment.
  — <https://aws.amazon.com/quick/pricing/>

## Still unknown

- A 2026 physical attack or physical data loss at AWS: no evidence was found. The reviewed events and public material describe only the launch and pricing of AWS Quick.
- The foundation models behind Fast, Balanced and Smart. Third parties report Claude 5.5 Haiku, Sonnet and Opus, but official AWS technical documentation does not confirm it.
- The agentic-hour quotas for the individual Free and Plus tiers, beyond the trial duration. Public documentation does not quantify them.

## Sources

| source | title | read |
|---|---|---|
| https://quick.aws.com/sn | AWS Quick Console and Agent Workspace | 2026-11-22 |
| https://aws.amazon.com/quick/pricing/ | AWS Quick Pricing and Agentic Hours | 2026-11-22 |
| https://x.com/interjc/status/2124164577743261840 | Post on AWS Quick Tiering, Modes, and Agentic Hours | 2026-11-22 |

## Agent brief {#agent-brief}

- **Subject:** organization:amazon-web-services, thread amazon-generative-ai-platform-and-models, 3 dated events 2023-04-13 → 2026-11-21.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
