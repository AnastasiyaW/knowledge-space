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

<!-- live-update:ff798f3ff58c9c5da779122c8b23a44d918d5a28e3dfeb1f8a636f5e6c8d9990 -->
## 2026-09-09 — Meta launches Muse personal AI agent

Meta introduced Muse, a personal AI agent powered by Muse Spark. It can plan work, use a cloud browser, and fill forms. The official launch described an initial US rollout.

## 2026-09-09 — Meta details Muse controls for browser tasks

Muse can handle browser and form tasks. Meta says users approve sensitive actions and choose the access granted to connected services.

### Usage and practices

- Confirm that Muse is available in your country, create or open the Muse experience, and state a bounded task or goal in chat. [Source](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)
- Connect only the services needed for that task and choose the permitted access level. Revoke a connection when it is no longer needed. [Source](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)
- Use the shared browser for research, appointments, forms or price monitoring. Take control when needed. [Source](https://www.meta.com/en-gb/help/superintelligence/2124746764949121/)
- Review approval prompts before purchases, email sending or other consequential actions. Inspect the activity trail afterward. [Source](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)
- Start with a public-web task. Take over at login or another sensitive interaction instead of granting broad account access immediately. [Source](https://www.techradar.com/ai-platforms-assistants/i-tried-metas-new-muse-ai-agent-its-incredibly-useful-but-handing-it-my-digital-life-felt-deeply-uncomfortable)
- Keep approval friction enabled for consequential actions. Grant each connected service only the scope required for the task. [Source](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)

### What practitioners say

- A hands-on reviewer found shopping delegation useful, but recommends beginning with public-web tasks and retaining human control at logins and sensitive steps. (2026-09-14) [Source](https://www.techradar.com/ai-platforms-assistants/i-tried-metas-new-muse-ai-agent-its-incredibly-useful-but-handing-it-my-digital-life-felt-deeply-uncomfortable)

### Additional evidence

- 2026-09-09: The public launch documentation identifies the underlying model family as Muse Spark. It describes a dedicated Muse Secure VM with its own browser, and says the initial rollout was in the US on iOS, Android and muse.ai; it does not substantiate a “Muse Spark 1.3” launch-model designation. [Source](https://about.fb.com/ja/news/2026/09/introducing-muse-personal-ai-agent/)
- 2026-09-09: Meta says sensitive actions require confirmation, credentials are stored separately from the agent, and users can select or revoke connected-service permissions. The English launch page is dated 2026-09-08, one day earlier than this recorded event date. [Source](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)

### Subsequent developments

- 2026-10-12: Meta introduced Muse Wonder and Muse Wonder Full for developers and Muse Code subscribers, and said Muse Wonder would soon power Muse experiences, first for subscribers. [Source](https://about.fb.com/news/2026/10/introducing-muse-wonder-models/)
- 2026-10-23: Muse became available in Japan on iOS, Android and muse.ai, which Meta described as its first availability outside North America. [Source](https://about.fb.com/ja/news/2026/10/muse-personal-ai-agent-launches-in-japan/)
- 2026-11-23: Muse became available to UK adults through iOS, Android, muse.ai and WhatsApp, with free use and optional subscription plans. [Source](https://about.fb.com/news/2026/11/muse-now-available-in-the-uk-muse-does-the-work-you-stay-in-control/)

### Superseded guidance (retained for history)

- 2026-10-23: The launch-era expectation that Muse would remain limited to its initial US rollout is obsolete: Meta subsequently announced availability in Japan and the UK. [Source](https://about.fb.com/ja/news/2026/10/muse-personal-ai-agent-launches-in-japan/)
- 2026-10-12: Treating Muse Spark as the only announced model path for Muse is outdated: Meta announced that Muse Wonder would begin powering Muse experiences for subscribers. [Source](https://about.fb.com/news/2026/10/introducing-muse-wonder-models/)

### Limits and open questions

- The accessible official launch announcement names Muse Spark, but does not identify the consumer agent’s launch model as “Muse Spark 1.3.”
- Current availability, quotas and subscription limits vary by country and may change after the dated regional announcements.

<!-- Retained base: fd92264f7cc8086bb18b1dce8dc62956ef6d5d27; article blob: 3d121dc407d12dcec20b31c85f036865077c5242 -->
