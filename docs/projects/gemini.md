---
title: Gemini
category: projects
date: 2026-08-14
tags: [gemini, gemini-development, project]
aliases: ["Gemini", "Gemini 1.5", "Gemini 3.7 Flash"]
---

# Gemini

**Development line:** `project:gemini` · thread `gemini-development`  
**Last event:** 2026-08-14 · 6 dated since 2024-02-16 · **Researched:** 2026-09-04 · confidence: high

## What it is

Gemini is Google's model family for chat, text, code, images, audio, video, and API integrations.

- Gemini app: manual chat and everyday tasks.
- AI Studio: prompt prototyping and code generation.
- Gemini API: backend integration into applications.
- Live API: streaming voice and vision interfaces.

Access to the consumer app, API keys, pricing tiers, Live API, and macOS features is independent, and Live API remains in Preview. We prototype in AI Studio, pin a stable model ID in production, and check its pricing tier and lifecycle.

## Development line

- **2024-02-16 — Google publishes a Gemini model-development announcement.** On 2024-02-16, Google linked an official Technology & AI blog item about Gemini as a next-generation model. This is a first-party model-development announcement for Gemini. The supplied link alone does not establish its exact feature or availability scope.
- **2024-12-12 — Gemini-related Live interface appears in Google AI Studio.** On 2024-12-12, a Google AI Studio Live page was linked for the Gemini line. This indicates a Gemini-related live-interaction surface in the developer environment. The supplied URL does not establish the precise model, API, or launch status.
- **2026-03-03 — Gemini 3.1 Flash-Lite Preview appears with pricing documentation.** On 2026-03-03, Google AI Studio linked Gemini 3.1 Flash-Lite Preview alongside official pricing documentation for that named preview. This is a material availability-and-pricing step for the Gemini developer model line. The supplied links do not establish quotas, regions, or final-release status.
- **2026-04-10 — Gemini app announces 3D-model and chart capabilities.** On 2026-04-10, Google linked an official Gemini app announcement concerning 3D models and charts, together with the Gemini app. This records a product-capability step in the Gemini application surface. The URLs alone do not establish how the capability was implemented or which accounts received it.
- **2026-04-16 — Gemini gains a Mac-specific product surface.** On 2026-04-16, Google linked a Gemini page specifically for Mac. This records an expansion of the Gemini product's desktop-platform surface. The supplied URL does not establish the exact supported macOS versions, rollout scope, or feature set.
- **2026-08-14 — Google introduces Gemini 3.7 Flash for AI Studio.** On 2026-08-14, Google linked an official announcement introducing Gemini 3.7 Flash and an AI Studio prompt URL selecting that model. This is a material model-release and developer-availability step. The supplied links do not establish the model's final status, limits, or regional availability.

## What changed

- 2024-02-16: Gemini 1.5 Pro introduced MoE architecture, 128K standard context, and a limited preview up to 1M tokens through AI Studio and Vertex AI.
- 2024-12-12: Gemini 2.0 introduced the Multimodal Live API for real-time audio and video streaming; the historical AI Studio Live URL now requires sign-in, while the current Live API runs over stateful WebSocket and remains in Preview.
- 2026-03-03: Gemini 3.1 Flash-Lite entered preview for high-frequency tasks, translation, moderation, and data processing; Google later retired the preview endpoint.
- 2026-04-10: Gemini app added generation of interactive simulations and models directly in chat, with configurable visualization parameters.
- 2026-04-16: Gemini for macOS added desktop access with hotkeys and screen context; it requires an Apple Silicon machine running macOS 15+ in a supported country.
- 2026-08-14: Gemini 3.7 Flash, announced by Google on August 13, became the Flash model for coding and agent workflows.
- Found 2026-09-04: Gemini 3.8 Flash launched on September 2 and is the current stable Flash; Gemini 3.7 Flash remains fully supported, but the model list now marks it previous-generation.

## How to use this

Track Gemini by product surface as of 2026-08-14. Use AI Studio's Live interface for live workflows (2024-12-12). Price and evaluate Gemini 3.1 Flash-Lite Preview before adoption (2026-03-03). Select Gemini 3.7 Flash in AI Studio where available (2026-08-14), and treat Gemini app and Mac features as separate product surfaces.

1. Open Gemini app, sign in with a Google Account, and start a chat with text or attached files for one-off tasks.
  — <https://gemini.google.com/app>
2. Install Gemini for macOS on Mac only if the device has Apple Silicon, runs macOS Sequoia 15.0+, and the country supports Gemini app.
  — <https://gemini.google/mac/>
3. Open Google AI Studio to prototype: pick a prompt interface, test the model, adjust parameters and safety settings, and add tools.
  — <https://ai.google.dev/gemini-api/docs/ai-studio-quickstart>
4. Use Get code after prototyping, create or import a Cloud project, and generate an API auth key for backend integration.
  — <https://ai.google.dev/gemini-api/docs/api-key>
5. Select a stable endpoint from the model list before deployment; evaluate gemini-3.8-flash for new coding and agent tasks instead of defaulting to the older 3.7 endpoint.
  — <https://ai.google.dev/gemini-api/docs/models>
6. Use the separate Live API path over WebSocket for real-time voice or vision dialogue; use ephemeral tokens for client-to-server setups.
  — <https://ai.google.dev/gemini-api/docs/live-api>

## Best practices

- Pin production workloads to a specific stable model ID instead of latest or experimental aliases: latest changes automatically, and experimental endpoints carry tighter limits without contract stability.
  — <https://ai.google.dev/gemini-api/docs/models>
- Write short, direct instructions for Gemini 3; do not carry over verbose prompt engineering techniques from older models.
  — <https://ai.google.dev/gemini-api/docs/gemini-3>
- Enable Structured Output for complex JSON Schema instead of relying on "reply in JSON"; add consistent examples for repeatable formatting.
  — <https://ai.google.dev/gemini-api/docs/prompting-strategies>
- Place the question after reference material in long-context calls, omit unneeded context, and cache reused files or data.
  — <https://ai.google.dev/gemini-api/docs/long-context>
- Keep the API key out of Git and client code; route web and mobile production calls through a backend and restrict the key.
  — <https://ai.google.dev/gemini-api/docs/api-key>
- Check the pricing table before estimating costs: free and paid tiers differ in limits, features, and content handling, so launch announcement pricing is not a valid estimate.
  — <https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview>

## Superseded by this

- 2024-02-16 — Early access for Gemini 1.5 Pro with 128K base context and limited 1M preview is historical background, not current model selection guidance.
- 2026-03-03 — The `gemini-3.1-flash-lite-preview` endpoint was shut down on 2026-05-25; its direct replacement was `gemini-3.1-flash-lite`. That replacement now lists a shutdown date of 2027-05-07 with `gemini-3.5-flash-lite` as the next recommended successor.
- Found 2026-09-04 — Describing Gemini 3.7 Flash as the newest Flash is obsolete: `gemini-3.8-flash` was released on 2026-09-02. `gemini-3.7-flash` remains fully supported, but it is now the previous-generation stable option.

## Still unknown

- Gemini spans separate product surfaces: consumer app, macOS app, AI Studio, Gemini API, and Live API. Access to one does not confirm quotas, pricing tiers, or features for another.
- The historical AI Studio Live URL redirects to a login prompt. We cannot verify the exact interface or settings from December 2024 without an active session; an official announcement on December 11, 2024, and current documentation confirm the launch separately.
- The Gemini for macOS product page lists requirements and limits but gives no launch date; it does not independently verify the 2026-04-16 date.

## Sources

| source | title | read |
|---|---|---|
| https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/#sundar-note | Our next-generation model: Gemini 1.5 | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/ | Google introduces Gemini 2.0: A new AI model for the agentic era | 2026-09-04 |
| https://aistudio.google.com/live | Sign in - Google Accounts | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/pricing?hl=ru#gemini-3.1-flash-lite-preview | Цены на API Gemini Developer | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/ | Gemini 3.1 Flash-Lite: Built for intelligence at scale | 2026-09-04 |
| https://blog.google/innovation-and-ai/products/gemini-app/3d-models-charts/ | The Gemini app can now generate interactive simulations and models. | 2026-09-04 |
| https://gemini.google.com/app | Google Gemini | 2026-09-04 |
| https://gemini.google/mac/ | Gemini for macOS – native AI assistant and Mac automation | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/ | Introducing Gemini 3.7 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/models | Models | Gemini API | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/deprecations?hl=en | Gemini deprecations | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/latest-model | What's new in Gemini 3.8 Flash | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/ai-studio-quickstart | Google AI Studio quickstart | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/api-key | Using Gemini API keys | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt design strategies | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/long-context | Long context | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/gemini-3 | Gemini 3 developer guide | 2026-09-04 |
| https://ai.google.dev/gemini-api/docs/live-api | Gemini Live API overview | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:gemini`, thread `gemini-development`, 6 dated events 2024-02-16 → 2026-08-14.
- **Practical note:** As of 2026-08-14, practitioners should track Gemini by product surface: use AI Studio's Live interface for live workflows (2024-12-12), evaluate and price Gemini 3.1 Flash-Lite Preview before adoption (2026-03-03), and select Gemini 3.7 Flash in AI Studio where available (2026-08-14), while treating Gemini app and Mac features as separate product surfaces.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:398dd2f32a452ed7eca648c3d1a5190ce4b2b3fbb900ced2b7568b314a146b3e -->
## 2026-11-19 — Google adds background computer use agent to Gemini macOS client

Gemini for macOS now has a computer use agent. It runs multi-step desktop and application workflows in an isolated background window, on Apple Silicon Macs only.

### Usage and practices

- Install the Gemini for macOS desktop client on an Apple Silicon Mac. Sign in with an account that has a paid Google AI subscription. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)
- Grant Accessibility and screen control permissions in macOS System Settings. Whitelist the target desktop applications in the Gemini settings. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)
- Describe the local file, form or application workflow as a multi-step prompt in the chat panel. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)
- Watch the run in the isolated live preview window. Confirm any sensitive login or transaction prompt. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)
- Grant access to specific applications one by one, not to the whole system. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)
- Keep the live preview panel open during complex tasks to follow how the agent navigates. Pause at once if it takes a wrong step. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)
- Leave manual approval on for authentication checkpoints, credential submission and financial transactions. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)

### Additional evidence

- 2026-11-19: The automation runs in an isolated background window with a live preview in the chat. The main desktop and the mouse cursor stay free to use. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)
- 2026-11-19: It needs Apple Silicon hardware with macOS and a paid Google AI Plus, Pro or Ultra subscription. Permissions are set per application, and sensitive transactions need manual approval. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)

### Superseded guidance (retained for history)

- 2026-11-19: Gemini on macOS was limited to text and code generation in the chat window. It could not interact with native desktop applications or run filesystem workflows. [Source](https://techcrunch.com/2026/11/19/google-gives-gemini-the-ability-to-use-your-mac-for-you/)

### Limits and open questions

- Permalinks to the official Google blog post and to secondary technical reports are not available yet.
- No community benchmarks compare the isolated background window with foreground desktop agents across third-party Mac applications.


<!-- Retained base: af7458929f9dfaf6c693e5f0a3138b1fc52eda69; article blob: 39fcc5b32b83f09a151039b030917bf294dd3917 -->

<!-- live-update:a8a80a7efc6106eeceac6cd761607b1dea80f0272c00a7f934a11ea7aeebb7b7 -->
## 2026-11-20 — Google adds background Computer Use to Gemini for Mac

The Gemini app on macOS now has Computer Use. It runs multi-step desktop tasks in an isolated background window, so it does not take over the user's cursor.

### Usage and practices

- Install and open the Gemini desktop app on an Apple Silicon Mac running macOS, with an active Google AI subscription. [Source](https://the-decoder.com/googles-gemini-can-now-run-mac-apps-and-finish-desktop-chores-in-the-background-while-you-keep-working/)
- Start a task by typing @Computer use, then the multi-step request, in the Gemini chat input. [Source](https://the-decoder.com/googles-gemini-can-now-run-mac-apps-and-finish-desktop-chores-in-the-background-while-you-keep-working/)
- Grant permissions per application, for the local software and directories the task needs. [Source](https://the-decoder.com/googles-gemini-can-now-run-mac-apps-and-finish-desktop-chores-in-the-background-while-you-keep-working/)
- Watch the run in the background window's preview stream, and confirm the prompts for sensitive actions when they appear. [Source](https://the-decoder.com/googles-gemini-can-now-run-mac-apps-and-finish-desktop-chores-in-the-background-while-you-keep-working/)
- Give access to desktop apps selectively, so sensitive local files and unrelated software stay out of reach. [Source](https://the-decoder.com/googles-gemini-can-now-run-mac-apps-and-finish-desktop-chores-in-the-background-while-you-keep-working/)
- Keep the live preview in view during automation you do not know well, so you can catch anomalies before a critical step asks for approval. [Source](https://the-decoder.com/googles-gemini-can-now-run-mac-apps-and-finish-desktop-chores-in-the-background-while-you-keep-working/)

### Additional evidence

- 2026-11-20: Google added Computer Use to the Gemini desktop app for Mac through the @Computer use command. Actions run in an isolated background window with a live stream preview, not on the user's cursor. It needs Apple Silicon and a paid Google AI Plus, Pro, or Ultra subscription. [Source](https://the-decoder.com/googles-gemini-can-now-run-mac-apps-and-finish-desktop-chores-in-the-background-while-you-keep-working/)

### Superseded guidance (retained for history)

- 2026-11-20: Before this, Gemini on desktop handled text and multimodal chat queries only. It had no direct control over native macOS apps or local file workflows. [Source](https://the-decoder.com/googles-gemini-can-now-run-mac-apps-and-finish-desktop-chores-in-the-background-while-you-keep-working/)

### Limits and open questions

- Latency and error rates across different macOS software setups have not been measured.


<!-- Retained base: ba59150ff6af8d3245658020d86e3463aab13771; article blob: 72c9f27b214614f42e7c88afed3791669ce09c95 -->

<!-- live-update:6b3b632666e141a3bab9c9d772a080bf0676bb3b1ee674f8666476e5d7d268d8 -->
## 2026-07-07 — Managed Agents adds asynchronous execution and remote MCP support

Managed Agents in the Gemini API runs agent work inside a remote sandbox. It adds background execution, remote MCP integration, custom functions, and credential refresh.

## 2026-07-17 — Gemini 3.5 Flash Cyber is limited to CodeMender pilot access

Gemini 3.5 Flash Cyber is a cybersecurity model built on 3.5 Flash. It finds, validates, and patches vulnerabilities. Access is restricted to governments and trusted partners through CodeMender.

## 2026-07-21 — Gemini adds 3.6 Flash, 3.5 Flash-Lite, and Flash Cyber

Gemini introduces separate Flash-family options for specific workloads: general agent work, high-throughput lower-latency workflows, and CodeMender security remediation.

## 2026-07-28 — Gemini Robotics 2 separates motor control, reasoning, and local deployment

Gemini Robotics 2 is a vision-language-action model for whole-body robot control. It runs alongside ER 2 for high-level reasoning and On-Device 2 for local use.

## 2026-07-28 — Managed Agents adds 3.6 Flash defaults and sandbox hooks

Managed Agents defaults to Gemini 3.6 Flash. The update adds model selection, environment hooks, budget controls, scheduled triggers, and free-tier access.

## 2026-07-30 — Gemini Robotics ER 2 adds video-based task tracking

Gemini Robotics ER 2 plans multi-step robot tasks. It tracks progress and recovery through continuous video, and coordinates multiple robots.

### Usage and practices

- Create a Managed Agent interaction for remote-sandbox work. Set background: true so work continues after the initial request. Keep the returned interaction ID to poll, stream, or reconnect. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api/)
- Attach only the remote MCP servers and built-in tools required for the task. Use custom functions when local business logic must run on the client. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api/)
- Pin the Managed Agent model explicitly when reproducibility, latency, or cost matters. The July default is Gemini 3.6 Flash, while Flash-Lite is the lower-cost option. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/)
- For robots, pair a lower-level VLA for motor control with Gemini Robotics ER 2. ER 2 handles instruction understanding, task planning, video-based progress tracking, and tool use. [Source](https://deepmind.google/blog/gemini-robotics-er-2-powering-robotics-with-video-understanding-task-orchestration-and-multi-robot-collaboration/)
- Use background execution for long-running interactions instead of holding an HTTP connection open. Retain the interaction ID and handle terminal statuses explicitly. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api/)
- Use environment hooks to enforce controls before or after sandbox tool calls. They can block, lint, or audit actions. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/)
- Treat Flash Cyber as a restricted security workflow through CodeMender, not a general patching endpoint. Initial deployment is limited to governments and trusted partners. [Source](https://deepmind.google/blog/introducing-gemini-3-5-flash-cyber/)
- Use Flash-Lite for throughput-sensitive tasks. Compare its pricing against prior Flash-Lite versions rather than assuming the Lite name makes it cheaper. [Source](https://www.reddit.com/r/Bard/comments/1v2lk1l/introducing_gemini_36_flash_35_flashlite_and_35/)

### What practitioners say

- One practitioner argued that 3.5 Flash-Lite's higher listed price undermines the Lite label. Check actual input and output pricing instead of trusting the name. (2026-07-21) [Source](https://www.reddit.com/r/Bard/comments/1v2lk1l/introducing_gemini_36_flash_35_flashlite_and_35/)

### Additional evidence

- 2026-07-07: Managed Agents run in an isolated cloud sandbox. Background interactions return an ID to poll, stream, or reconnect. Remote MCP servers work alongside built-in tools. Custom functions shift execution to the client via a requires\_action state. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api/)
- 2026-07-17: The linked first-party announcement is dated 2026-07-21, not 2026-07-17. It describes Gemini 3.5 Flash Cyber as built on 3.5 Flash for finding, validating, and patching vulnerabilities. Initial access is limited to governments and trusted partners via CodeMender. [Source](https://deepmind.google/blog/introducing-gemini-3-5-flash-cyber/)
- 2026-07-21: Gemini 3.6 Flash costs $1.50 per million input tokens and $7.50 per million output tokens. Gemini 3.5 Flash-Lite targets high-throughput workloads at $0.30 per million input tokens and $2.50 per million output tokens. Cyber pairs with CodeMender rather than serving as a general API model. [Source](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/)
- 2026-07-28: The linked Robotics 2 announcement is dated 2026-07-30, not 2026-07-28. It lists Robotics 2 as the vision-language-action model for humanoids and bi-arm robots. Robotics ER 2 handles high-level reasoning, and Robotics On-Device 2 runs locally on device. [Source](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)
- 2026-07-28: Managed Agents defaults to Gemini 3.6 Flash. Developers can pin a model via agent\_config.model. Environment hooks run before or after sandbox tool calls to block, lint, or audit them. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/)
- 2026-07-30: Gemini Robotics ER 2 handles high-level embodied reasoning, handing motor execution to a lower-level VLA. It adds continuous-video progress tracking, failure recovery, native tool and user-function calling, and multi-robot collaboration in shared spaces. [Source](https://deepmind.google/blog/gemini-robotics-er-2-powering-robotics-with-video-understanding-task-orchestration-and-multi-robot-collaboration/)

### Subsequent developments

- 2026-11-10: Gemini Robotics 2.5 introduced a later vision-language-action model. It focuses on broader robot skills and faster skill acquisition in unstructured real-world environments. [Source](https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/)

### Superseded guidance (retained for history)

- 2026-07-28: For Managed Agents on antigravity-preview-05-2026, Gemini 3.6 Flash supersedes the earlier default model. Developers can still pin 3.5 Flash or 3.5 Flash-Lite explicitly. [Source](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/)
- 2026-07-30: Gemini Robotics ER 2 supersedes Gemini Robotics ER 1.6 for embodied reasoning. The new generation adds continuous-video progress tracking and multi-robot collaboration. [Source](https://deepmind.google/blog/gemini-robotics-er-2-powering-robotics-with-video-understanding-task-orchestration-and-multi-robot-collaboration/)

### Limits and open questions

- The reviewed 2026-07-17 Cyber event points to a first-party page dated 2026-07-21.
- The reviewed 2026-07-28 Robotics 2 event points to a first-party page dated 2026-07-30.
- The subject combines distinct products: Managed Agents, general Flash models, a restricted cyber model, and robotics models. Their availability and operating assumptions are not interchangeable.

<!-- Retained base: 4ed654b1b2077d990cd62c178eaaaa33977aa715; article blob: ef7f6dae0339f7e6e2d2948b037932df2afc569f -->
