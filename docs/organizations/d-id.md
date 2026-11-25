---
title: D-ID — Public product surfaces
category: organizations
tags: [d-id, d_id_studio, organization, product_release, public-product-surfaces]
aliases: ["D-ID"]
---

# D-ID — Public product surfaces

**Development line:** `organization:d-id` · thread `public-product-surfaces`  
**Events:** 2 dated, 2022-08-01 → 2023-03-09 · **Researched:** 2026-09-03 · confidence: medium

## What it is

D-ID is a platform for teams that need either a generated presenter video or a live visual agent on a website. — Creates talking-avatar videos from image, text, or audio, plus video translation. — Creates WebRTC agents with an avatar, voice, LLM instructions, and an optional RAG knowledge base. — Offers Studio, API, a website embed, and a client SDK. Limit: video generation is asynchronous, while embedded agents require client keys restricted to approved domains. Verdict: choose the video or real-time path first; D-ID is no longer just a talking-photo demo.

## Development line

- **2022-08-01 — D-ID public demo surface recorded.** On 2022-08-01, the sealed record pointed to a D-ID demo hosted on its create subdomain. This establishes a public-facing demonstration surface in the company's development line, without establishing the demo's exact functionality or launch status.
- **2023-03-09 — D-ID chat product surface recorded.** On 2023-03-09, the sealed record pointed to a D-ID chat endpoint on its chat subdomain. This indicates a distinct public product surface after the earlier demo record, but does not establish its capabilities, release terms, or relationship to the demo.

## What changed

2022-08-01: `create.d-id.com/demo/` was the Studio-demo entry point. Its current title identifies Creative Reality Studio, but the original demo state is no longer inspectable. 2022-09-19 (found today): D-ID formally launched Creative Reality Studio as a self-service workflow for turning one image into a presenter-led video, moving the product beyond enterprise-only video reenactment. 2023-03-07 (found today): D-ID launched beta chat.D-ID, combining its streaming digital human with ChatGPT for face-to-face conversation. 2023-03-09: `chat.d-id.com/` was the recorded access route for that conversational product; it now redirects to D-ID’s AI Agents page. 2026-02-04 (found today): V4 Expressive Avatars reached Studio and the API, adding sentiment selection for generated video. Today: D-ID documents two distinct working paths—async Videos and real-time Agents with WebRTC, LLM configuration, and RAG knowledge bases. Verdict: the development line is from a self-service image-to-presenter tool to a platform with separate prerecorded-video and conversational-agent products.

## How to use this

From 2022-08-01, practitioners could evaluate D-ID through a public demo surface; from 2023-03-09, they should treat its chat endpoint as a separate product surface when assessing available workflows, pending primary-source research.

1. Choose the workflow first: use Videos for asynchronous avatar output, or Realtime for a conversational visual agent.
  — <https://docs.d-id.com/docs/quickstart>
2. For a V4 video, submit an avatar ID and required text or audio script to the Expressives endpoint; optionally set sentiment, background, result URL, or webhook.
  — <https://docs.d-id.com/reference/createv4video>
3. For an agent, create it with a presenter, voice, LLM provider/model, and instructions; retain the returned agent ID.
  — <https://docs.d-id.com/docs/agent-quickstart>
4. Fetch the agent until its status is `done`, create a domain-scoped client key, then use the Client SDK to connect, chat, and disconnect.
  — <https://docs.d-id.com/docs/agent-session-quickstart>
5. Use the single-script Agents Embed for a prebuilt website UI; use the SDK instead when the application needs programmatic layout and behavior control.
  — <https://docs.d-id.com/docs/embed-overview>

## Best practices

- Treat `status: done` and the returned idle-video URL as the readiness gate before opening real-time sessions.
  — <https://docs.d-id.com/docs/agent-quickstart>
- Restrict every frontend client key to the exact allowed domains; it is valid only from those origins.
  — <https://docs.d-id.com/docs/agent-session-quickstart>
- Choose the embed for minimal-code integration and the SDK only when the application needs fuller UI and lifecycle control.
  — <https://docs.d-id.com/docs/embed-overview>
- For a custom LLM in production, use streaming; D-ID documents non-streaming as a debugging option rather than a production mode.
  — <https://docs.d-id.com/docs/llms-overview>

## Superseded by this

- 2022-08-01 — Demo-only framing is obsolete for product selection: current D-ID documentation separates asynchronous Videos from real-time Agents.
- 2023-03-09 — `chat.d-id.com/` as a standalone Chat entry point is superseded operationally: the URL now redirects to the current AI Agents product page.
- 2022–2023 — Guidance that describes D-ID only as a single-image presenter-video tool is incomplete where a live, embedded visual agent is the actual requirement.

## Still unknown

- The 2022-08-01 demo date precedes D-ID’s dated 2022-09-19 Studio launch announcement, so it may represent an early or limited demo rather than the public launch; the exact state is unverified.
- The original page content at `create.d-id.com/demo/` is unavailable to inspect today; only its current title is recoverable.
- The Studio-demo and Chat entries are different product tracks—async video and real-time conversation—under D-ID rather than different companies. Their exact historical product relationship and deprecation timeline cannot be reconstructed from the two original URLs alone.
- Current pricing, regional availability, and consent-policy requirements were not assessed in this research.

## Sources

| source | title | read |
|---|---|---|
| https://create.d-id.com/demo/ | D-ID Creative Reality Studio | 2026-09-04 |
| https://chat.d-id.com/ | AI Agents: Create an Interactive Visual Agent | 2026-09-04 |
| https://www.d-id.com/news/d-id-launches-creative-reality-studio-self-service-video-creation-platform-with-hyper-real-ai-presenters/ | D-ID Launches Creative Reality Studio Self-Service Video Creation Platform with Hyper-Real AI Presenters | 2026-09-04 |
| https://www.d-id.com/news/press-release-chat-d-id-enables-anyone-to-talk-face-to-face-with-ai/ | Press Release: chat.D-ID enables anyone to talk face to face with AI | 2026-09-04 |
| https://docs.d-id.com/docs/quickstart | Quickstart | 2026-09-04 |
| https://docs.d-id.com/reference/createv4video | Create a Video | 2026-09-04 |
| https://docs.d-id.com/docs/agent-quickstart | Agents | 2026-09-04 |
| https://docs.d-id.com/docs/agent-session-quickstart | Agent Sessions | 2026-09-04 |
| https://docs.d-id.com/docs/embed-overview | Overview — Agents Embed | 2026-09-04 |
| https://docs.d-id.com/docs/llms-overview | Overview — LLMs | 2026-09-04 |
| https://www.d-id.com/resources/product-updates/expressive-avatars-are-live-in-d-id-studio/ | Expressive Avatars are live in D-ID Studio | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:d-id`, thread `public-product-surfaces`, 2 dated events 2022-08-01 → 2023-03-09.
- **Practical note:** From 2022-08-01, practitioners could evaluate D-ID through a public demo surface; from 2023-03-09, they should treat its chat endpoint as a separate product surface when assessing available workflows, pending primary-source research.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
