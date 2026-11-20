---
title: "Muse"
category: "projects"
date: 2026-11-19
tags: ["meta-muse-ai-agent", "muse", "muse-image-video-msl", "project"]
aliases: ["Muse"]
---

# Muse

**Development line:** project:meta-muse-ai-agent · thread muse-image-video-msl  
**Last event:** 2026-11-19 · 2 dated since 2026-07-08 · **Researched:** 2026-11-20 · confidence: medium

## What it is

Meta Muse is a personal AI agent that runs tasks across apps, automates device workflows and handles messages in third-party services. It competes with Apple Intelligence and Google Assistant. It can:

- Monitor push notifications and operating system accessibility streams to pick up scheduling and messaging context;
- Use third-party web services and apps with stored credentials;
- Run automated transactions and workflow reminders that the user asks for.

It needs broad device-level accessibility permissions. Test setups risk leaking context and hallucinating across user sessions that are not isolated. Muse is still an experimental enterprise prototype, and it needs strict credential boundaries and manual permission isolation.

## Development line

- **2026-07-08 — Muse Image, Muse Video, and MSL announcement.** On 2026-07-08, Meta AI published a Muse-related announcement. The linked URL names Muse Image, Muse Video, and MSL, so the link appears to introduce named components of the Muse project. The evidence we have does not establish their capabilities, availability, or technical specifications.
- **2026-11-19 — Report says Meta's Muse AI agent is mixing up conversations and may expose private data.** A report published on 2026-11-19 says Muse has been mixing up conversations. According to employees, it surfaced messages, product orders and bank balances that did not belong to the users, which raises the possibility of private data exposure.
  - Internal employee testing reports documented data leaking between accounts. Muse showed other users' Capital One ($2,722.58) and Charles Schwab ($5,899.57) bank balances, unprompted childcare and career requests, and unauthorized non-refundable Airbnb reservations. The report also says Muse picked up context from encrypted apps such as Signal by reading Android push notifications and macOS accessibility APIs. Meta attributed this to prompt-driven hallucinations in unreleased test builds. (2026-11-19) — <https://techcrunch.com/2026/11/19/metas-ai-agent-muse-is-mixing-up-conversations-and-exposing-private-data-report-says/>

## What changed

Development moved from isolated conversational assistant prototypes to an autonomous cross-app agent that reads system notifications and drives third-party services. The architecture shifted to agent instances running in dedicated virtual machines with isolated credential storage. Internal dogfooding then exposed security holes. Notification listeners and accessibility hooks bypassed app encryption boundaries, and unprompted hallucinations surfaced across sessions.

## How to use this

1. Install the agent app and set the accessibility and notification listener permissions on the host operating system that cross-app automation requires.
  — <https://techcrunch.com/2026/11/19/metas-ai-agent-muse-is-mixing-up-conversations-and-exposing-private-data-report-says/>
2. Connect authorized third-party app accounts through the isolated credential store, so tasks can be delegated.
  — <https://techcrunch.com/2026/11/19/metas-ai-agent-muse-is-mixing-up-conversations-and-exposing-private-data-report-says/>
3. Send task prompts in conversation, and check the autonomous background actions before they execute.
  — <https://techcrunch.com/2026/11/19/metas-ai-agent-muse-is-mixing-up-conversations-and-exposing-private-data-report-says/>

## Best practices

- Turn off broad accessibility and push notification listener permissions, so the agent cannot take in context from end-to-end encrypted messaging apps.
  — <https://techcrunch.com/2026/11/19/metas-ai-agent-muse-is-mixing-up-conversations-and-exposing-private-data-report-says/>
- Keep financial accounts and sensitive transactional services away from automated booking and payment.
  — <https://techcrunch.com/2026/11/19/metas-ai-agent-muse-is-mixing-up-conversations-and-exposing-private-data-report-says/>
- Opt out of sharing data for model training, and check that session contexts run in isolated, secure virtual machines.
  — <https://techcrunch.com/2026/11/19/metas-ai-agent-muse-is-mixing-up-conversations-and-exposing-private-data-report-says/>

## Superseded by this

- The claim that an autonomous agent's cross-app notification listeners keep user privacy safe across unisolated sessions without explicit sandboxing.
  — <https://techcrunch.com/2026/11/19/metas-ai-agent-muse-is-mixing-up-conversations-and-exposing-private-data-report-says/>

## Still unknown

- Meta has not disclosed the public release timeline, the model parameter size or the underlying foundation model architecture.
- Meta's own technical documentation and release notes were not available at permanent canonical URLs. Only the internal employee testing reports are known.
- Practitioner discussions on external forums could not be checked through direct canonical URLs, because search results redirected.

## Sources

| source | title | read |
|---|---|---|
| https://techcrunch.com/2026/11/19/metas-ai-agent-muse-is-mixing-up-conversations-and-exposing-private-data-report-says/ | Meta's AI agent Muse is mixing up conversations and exposing private data, report says | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:meta-muse-ai-agent, thread muse-image-video-msl, 2 dated events 2026-07-08 → 2026-11-19.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** medium. The dated supersedes above decide what is obsolete.
