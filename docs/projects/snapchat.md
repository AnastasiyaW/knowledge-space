---
title: Snapchat
category: projects
date: 2022-06-06
tags: [project, snapchat, snapchat-lenses, snapchat-lenses-and-filters, snapchat_crying_filter]
aliases: ["Snapchat"]
---

# Snapchat

**Development line:** `project:snapchat` · thread `snapchat-lenses-and-filters`  
**Last event:** 2022-06-06 · 1 dated since 2022-06-06 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Snapchat is a camera app and the Lens Studio AR platform for users, creators, and developers: Face Lenses, World Lenses, templates, scripting, SnapML, and publishing to Snapchat, Camera Kit, and Spectacles.

Submitted lenses are capped at 8 MB, with up to 10 MB for a SnapML model. Lens Studio is a working route to build AR effects, not a tool to recreate a specific old viral filter.

## Development line

- **2022-06-06 — A Snapchat Lens link was recorded in the development line.** On 2022-06-06, a message linked a Snapchat Lens URL alongside a source reference. The dated links establish a lens-related Snapchat item in this development line, but do not establish its functionality, authorship, or release status.

## What changed

2022-05-12 — Crying Lens became a widely discussed Snapchat AR effect; a third-party report notes its debut on 6 May and over 1 billion uses by 12 May.

2022-06-06 — A standalone Snapchat Lens page was cited, but we could not independently read its name, author, or features; a link to Crying Lens remains unconfirmed.

2022-12-06 — Snap described the platform as a way to publish lenses not only to Snapchat, but also through Camera Kit and for Spectacles, and reported over 3 million created AR lenses.

## How to use this

As of 2022-06-06, practitioners tracking Snapchat work should include Lens URLs as a concrete implementation or distribution surface, while keeping unsupported claims about a lens's behavior or status out of the record.

1. Sign in to Lens Studio through Snapchat and choose a template for a simple lens or start from scratch; mobile and web tools serve casual creators, while desktop handles complex development.
  — <https://help.snapchat.com/hc/en-gb/articles/7012330991124-How-can-I-create-Lenses-for-Snapchat>
2. Set project name, platform, and size; for mobile lenses, target the 8 MB cap and check built-in validation checks.
  — <https://developers.snap.com/lens-studio/publishing/configuring/configuring-project-info?lang=en-US>
3. In Lens Studio click Publish, create or select an organization and Lens Folder, then submit the lens as new or update an existing project.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>
4. Choose Upload and Publish to publish in Snapchat, or Upload to Lens Folder if the lens is needed only for further distribution through Camera Kit or Business Manager.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>

## Best practices

- Check performance, device compatibility, and policy compliance before submission: publishing undergoes validation, automated testing, and content review.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>
- Do not copy ML models or viral lenses; use a clear preview, set Lens Hints, and compress assets. Documentation recommends aiming below 8 MB.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>
- Do not add irrelevant tags: they undergo moderation and do not improve lens reach.
  — <https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens>

## Superseded by this

- Before 2022-12-06: the view that lenses are only for Snapchat; Snap also documented using published AR effects in Camera Kit and on Spectacles.
- Before current Lens Studio 5: a desktop-only approach for all creators; current support separates desktop for complex AR projects from mobile and web tools for personal creation.

## Still unknown

- Crying Lens and the 2022-06-06 lens link may be separate topics under Snapchat: the standalone lens page was unavailable for independent inspection.
- No primary Snap source was found with a release date for Crying Lens; the 6 May debut and early usage metric are confirmed by a secondary source from 12 May 2022.
- We cannot confirm whether the specific lens at the 2022-06-06 link is available today.

## Sources

| source | title | read |
|---|---|---|
| https://www.bustle.com/life/how-to-use-crying-filter-snapchat-tiktok-instagram | How To Use The Crying Filter On Snapchat, TikTok, Instagram & More | 2026-09-05 |
| https://www.tmz.com/2022/05/12/snapchat-new-crying-face-filter-not-inspired-by-amber-heard/ | Snapchat's New Crying Face Filter NOT Inspired by Amber Heard | 2026-09-05 |
| https://help.snapchat.com/hc/en-gb/articles/7012330991124-How-can-I-create-Lenses-for-Snapchat | How can I create Lenses for Snapchat? | 2026-09-05 |
| https://developers.snap.com/lens-studio/home | Lens Studio | 2026-09-05 |
| https://developers.snap.com/lens-studio/publishing/configuring/configuring-project-info?lang=en-US | Configuring Project Settings | 2026-09-05 |
| https://developers.snap.com/lens-studio/publishing/submitting/submitting-your-lens | Submitting Your Lens | 2026-09-05 |
| https://newsroom.snap.com/lens-fest-2022 | Lens Fest 2022: Celebrating Five Years of the Snap AR Community | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:snapchat`, thread `snapchat-lenses-and-filters`, 1 dated events 2022-06-06 → 2022-06-06.
- **Practical note:** As of 2022-06-06, practitioners tracking Snapchat work should include Lens URLs as a concrete implementation or distribution surface, while keeping unsupported claims about a lens's behavior or status out of the record.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:1b873a14e8c26df11b6fa6ab8aade31bec1840b3201edf682a8ba3693e8f9990 -->
## 2026-11-18 — Snapchat launches Easy Lens CLI and Lens Studio MCP for AI coding assistants

Snap launched the Easy Lens CLI and a Model Context Protocol integration for Lens Studio. Developers can build, debug, preview and publish AR Lenses and Web Lens games from natural-language prompts in Claude Code, Cursor or Codex.

### Usage and practices

- Install the cross-platform Easy Lens CLI and sign in with a Snapchat developer account. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)
- Connect an AI coding assistant such as Claude Code, Cursor or Codex to the workspace through the Lens Studio Model Context Protocol (MCP) server. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)
- Describe the AR effect, face filter or Web Lens game mechanics in plain language. The agent assembles components from AR building blocks and AI asset generators. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)
- Stream live preview builds to a paired mobile phone to test camera tracking and debug at runtime. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)
- Publish the finished Lens through the automated CLI or the Lens Studio flow. It goes to platform moderation review, and monetization is set up there. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)
- Write structured prompts that name the tracking targets, the interaction physics and the leaderboard states, so the agent has less room to drift. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)
- Check generated 3D assets and scripts against mobile performance budgets on paired physical devices before platform review. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)
- Build complex scenes from the existing modular AR building blocks. Do not prompt custom shader code from scratch. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)

### Additional evidence

- 2026-11-18: The release adds the Easy Lens CLI, available on macOS, Windows and Linux, and native MCP server support in Lens Studio. Agents such as Claude Code, Cursor and Codex can inspect scenes, manage project assets and write TypeScript/JavaScript scripts directly. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)
- 2026-11-18: Agents connect to more than 100 AR building blocks and over 50 AI asset generators. They cover the work end to end: asset synthesis, error correction, on-device streaming previews and enrollment in the Lens+ Payouts program for monetization. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)

### Superseded guidance (retained for history)

- 2026-11-18: Before this, AR Lens creation meant assembling the project by hand in the IDE and writing scripts in Lens Studio. There was no terminal agent automation and no MCP workspace control. [Source](https://techcrunch.com/2026/11/18/snapchat-now-lets-developers-build-ar-lenses-with-ai-coding-assistants-like-claude-code-and-cursor/)

### Limits and open questions

- Direct links to the Chinese tech coverage (Sohu and TechNews Taiwan) could not be resolved, so they are not listed.
- Direct documentation links on lensstudio.com and snap.com for Easy Lens CLI configuration could not be resolved either, so they are not cited.


<!-- Retained base: 0fd8999e9214ce9f42a7aa048a739e9c9ddc5cc0; article blob: 0cacd2d104185d274aa4f2a3e628741fd1e26c19 -->
