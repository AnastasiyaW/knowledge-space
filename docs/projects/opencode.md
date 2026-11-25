---
title: "Opencode"
category: "projects"
date: 2026-11-19
tags: ["opencode", "project"]
aliases: ["Opencode"]
---

# Opencode

OpenCode is an open-source terminal AI coding agent for developers, an alternative to Claude Code or Cursor, with a mobile companion app.

**Development line:** project:opencode · thread opencode  
**Last event:** 2026-11-19 · 2 dated since 2026-11-19 · **Researched:** 2026-11-20 · confidence: high

## What it is

OpenCode is an open-source AI coding assistant and agent environment for software developers. It runs locally in the terminal, as an alternative to Claude Code or Cursor.

It does this:

- inspects local repository trees
- executes terminal commands
- edits source files across multi-file diffs
- answers user queries
- streams agent tool executions to paired client apps in real time

It needs a local machine daemon running Node.js, plus an active network tunnel or pairing mechanism for remote use. It stays bounded by host process permissions and user approval prompts.

## Development line

- **2026-11-19 — OpenCode mobile app launches as remote companion for desktop sessions.** The mobile app is available. Users can view and continue agent sessions running on their computer, answer permission requests, attach images and dictate voice messages. Pairing uses a QR code from `opencode pair --remote` through OpenTunnel. The Android listing lacks the voice-call feature, which is described only on the website.
- **2026-11-19 — OpenCode releases mobile companion app.** The mobile app is a remote companion for viewing and continuing agent sessions running on a user's computer. It supports real-time session viewing, tool activity monitoring, answers to permission and agent questions, image attachments and voice dictation. The Android version lacks the voice-call feature advertised on the website. Sessions are paired with `opencode pair --remote` over OpenTunnel.
- **2026-11-19 — other reporting on this date.**
  - Official documentation says the mobile companion links to active desktop OpenCode instances over OpenTunnel or local QR pairing. Users can inspect session progress, review file diffs, approve tool executions, upload photos and dictate messages. (2026-11-19) — <https://opencode.ai/mobile>
  - The Google Play listing for ai.opencode.mobilecode describes the Android build as a client companion for existing OpenCode workstation installations. It gives live tool activity feeds and lets users answer questions, without running a model locally on the phone. (2026-11-19) — <https://play.google.com/store/apps/details?id=ai.opencode.mobilecode>

## What changed

The project started as an open-source terminal AI coding assistant for local code editing. It grew from a local CLI into a client-server setup with web interfaces and remote connection handling. Mobile apps for iOS and Android followed. They let users watch sessions, confirm tool calls, send prompts, upload images and dictate audio over encrypted tunnels. Core agent compute stays on the user's workstation.

## How to use this

1. Install OpenCode locally and launch the CLI or background daemon on your development workstation.
  — <https://github.com/anomalyco/opencode>
2. Run `opencode pair --remote` in the terminal to generate an OpenTunnel pairing QR code and connection URL.
  — <https://opencode.ai/mobile>
3. Install the OpenCode companion app on Android from Google Play, or on iOS via TestFlight.
  — <https://opencode.ai/mobile>
4. Scan the pairing QR code in the mobile app to connect to the active desktop session. From there, review tool calls and approve permissions remotely.
  — <https://opencode.ai/mobile>

## Best practices

- Keep the host machine and the local OpenCode terminal session running in a persistent process or shell multiplexer, so the mobile client keeps its connection over OpenTunnel.
  — <https://opencode.ai/mobile>
- Check tool execution prompts and file diffs on the mobile client before you authorize bash commands or repository changes.
  — <https://play.google.com/store/apps/details?id=ai.opencode.mobilecode>
- Use voice dictation for conceptual follow-ups, prompt adjustments and status reviews, not for writing full code on a phone.
  — <https://opencode.ai/mobile>

## Superseded by this

- Supervising OpenCode agent runs used to require constant physical access to the local desktop terminal, to answer tool permission prompts and watch tool output.
  — <https://opencode.ai/mobile>

## Still unknown

- The website advertises real-time voice calls, but the first Android store release notes do not mention them. It is not verified whether this is an iOS-only feature or a staged backend rollout.
- No official first-party Simplified Chinese documentation or release mirrors were identified. Chinese search results were limited to secondary community discussion guides.

## Sources

| source | title | read |
|---|---|---|
| https://opencode.ai/mobile | OpenCode Mobile - Remote Companion App | 2026-11-20 |
| https://play.google.com/store/apps/details?id=ai.opencode.mobilecode | OpenCode - Apps on Google Play | 2026-11-20 |
| https://testflight.apple.com/join/M9eFEE1q | Join the OpenCode beta - Apple TestFlight | 2026-11-20 |
| https://github.com/anomalyco/opencode | GitHub - anomalyco/opencode: The open source AI coding agent | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:opencode, thread opencode, 2 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
