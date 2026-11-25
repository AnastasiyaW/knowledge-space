---
title: Vidu S1
category: projects

tags: [project, vidu-s1]
aliases: ["Vidu S1"]
---

# Vidu S1

**Development line:** `project:vidu-s1` · thread `vidu-s1`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-06 · confidence: medium

## What it is

Vidu S1 is ShengShu’s hosted real-time video model for creators and product teams building spoken, interactive digital characters. Vidu lists it separately from Q1/Q2/Q3 clip-generation models.

- Character creation: builds a character from a persona, an initial human/anime/pet image, and a selected or cloned voice.
- Dynamic control: changes character actions from spoken input during an audio or video session.
- Client access: offers Vidu Stream and a currently documented Vidu S1 API (Beta) using a control WebSocket plus AliRTC media.

The product page lists 540p at 25 fps, up to 42 fps. Session duration and billing must be read from the live-session response because vendor documentation conflicts. Use it for responsive avatar interactions, not for a local-model install or a conventional finished clip.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-10 — Vidu S1’s public GitHub presentation received three experience-GIF edits. The formal release was already dated 2026-07-03, so this was a demo and documentation refinement rather than a new model release.

## How to use this

1. For a no-code trial, open Vidu Stream, sign in and verify the account, then select a character or create one.
  — <https://www.vidu.com/vidu-stream>
2. Set the persona, upload an initial image, then select, upload, or clone a voice before starting the conversation.
  — <https://www.vidu.com/vidu-stream>
3. Use spoken instructions during the conversation to direct the character’s actions.
  — <https://www.vidu.com/vidu-stream>
4. For an application, obtain an API key and create a Live session with `POST /live/v1/lives`; retain `live.id` and the returned RTC credentials.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
5. Join Aliyun RTC and establish the authenticated control WebSocket, wait for `conn_init_ack.success=true`, then hang up, close the WebSocket, and leave the RTC channel.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>

## Best practices

- For browser clients, keep the raw Vidu API key on a trusted backend and proxy the authenticated WebSocket. Native browser WebSockets cannot set the required authorization header.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
- Treat the returned `live_duration` and final billed usage as authoritative. Do not hard-code an “unlimited” or fixed session cap.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/api-reference.md>
- In video mode, implement close–backoff–reconnect handling for `NOT_READY`. Create a fresh Live session for `LIVE_CONN_INIT_FAILED`.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
- Integrate Aliyun RTC as a separate media layer and subscribe once to the active remote stream. Ignore stale RTC or WebSocket events from a previous session.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md>
- Handle both server `type:6` hangups and abnormal WebSocket closure. After an active hangup, close the WebSocket before calling `leaveChannel()`.
  — <https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/websocket-protocol.md>

## Superseded by this

- 2026-07-03 — Treating Vidu S1 as a standard prompt-submit-then-wait video generator or a Vidu Q-series variant is obsolete. It launched as a separate real-time interactive digital-character line.
- 2026-07-03 — Calling 2026-07-10 the Vidu S1 launch is obsolete. ShengShu formally released it on 2026-07-03.

## Still unknown

- The public platform API says `live_duration` has a 600-second maximum, while the vendor-owned integration guide says to use a policy-specific returned value and shows 7200 seconds. No live account response was available to reconcile them.
- Current vendor sources also conflict on credit-unit and extra voice-clone pricing. Use an authenticated console or final billing response before approving a budget.
- The linked Vidu-S1 repository provides documentation and images, not public model weights or a runnable inference package; local deployment and model-license rights remain unverified.
- The 42-fps and long-duration figures are vendor and preprint claims, not an independent latency or quality guarantee for every deployment.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/shengshu-ai/Vidu-S1 | Vidu S1: A Real-Time Interactive Video Generation Model | 2026-09-06 |
| https://github.com/shengshu-ai/Vidu-S1/commits/main | Commits · shengshu-ai/Vidu-S1 · GitHub | 2026-09-06 |
| https://www.vidu.com/vidu-stream | Vidu S1 AI Video Model | Vidu AI | 2026-09-06 |
| https://platform.vidu.com/docs/vidu-s1 | Vidu S1 API (Beta) | Vidu API | 2026-09-06 |
| https://platform.vidu.com/docs/model-map | Model Map | Vidu API | 2026-09-06 |
| https://platform.vidu.com/docs/pricing | Pricing | Vidu API | 2026-09-06 |
| https://www.genspi.com/zh/news/vidu-s1-realtime-interactive-model/ | 生数科技发布 Vidu S1，推动视频生成迈向“实时交互”新时代 | 2026-09-06 |
| https://arxiv.org/html/2607.03118v1 | Vidu S1: A Real-Time Interactive Video Generation Model | 2026-09-06 |
| https://www.genspi.com/zh/news/vidu-s1-zhenhuan-digital-human/ | 技术赋能 IP 新体验，Vidu S1助力 360 打造《甄嬛传》数字人新玩法 | 2026-09-06 |
| https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/SKILL.md | Vidu S1 Live API Integration | 2026-09-06 |
| https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/api-reference.md | Vidu S1 Live API — HTTP Reference | 2026-09-06 |
| https://github.com/shengshu-ai/vidu-s1-api/blob/main/skills/vidu-s1-api/references/websocket-protocol.md | Vidu S1 Live API — WebSocket Control Protocol | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:vidu-s1`, thread `vidu-s1`, 0 dated events - → -.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
