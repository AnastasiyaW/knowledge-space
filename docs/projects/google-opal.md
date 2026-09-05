---
title: Google Opal
category: projects
date: 2025-07-25
tags: [google-opal, opal, project]
aliases: ["Google Opal"]
---

# Google Opal

**Development line:** `project:google-opal` · thread `google-opal`  
**Last event:** 2025-07-25 · 1 dated since 2025-07-25 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Google Opal is a no-code alternative to small custom web apps, built for people who want shareable AI workflows without running a server.

- Workflow editor: builds and edits node-based pipelines from natural language.
- Visual canvas: chains inputs, prompts, model calls, tools, and outputs.
- Agent Mode: selects tools, uses memory, routes execution, and conducts follow-up chat.

## Development line

- **2025-07-25 — Google introduced Opal.** On 2025-07-25, Google published an introduction to Opal and shared its web entry point. The launch confirmed the project, but did not establish its full feature set, regional availability, or account limits.

## What changed

- **2025-07-25** (original announcement dated 2025-07-24) — Opal launched in U.S.-only public beta as a visual and natural-language builder for multi-step apps chaining prompts, model calls, and tools.
- **2026-02-25** (official announcement dated 2026-02-24) — The Generate step gained Agent Mode to pick tools and models against a goal, retain memory, route dynamically, and ask follow-up questions.
- **2026-03-24** — First-party documentation shows Agent Mode enabled by default, exposing Search/Maps, Code Exec, Memory, and media generation. Fixed workflows remain available for rigid or high-precision logic.

## How to use this

We evaluate Google Opal through its official introduction and web entry point from 2025-07-25. Official documentation shows no later workflow or capability changes.

1. Sign in to Opal, open a Gallery demo, and select Remix to create an editable copy. Select Create New to build an app from scratch.
  — <https://developers.google.com/opal/quickstart>
2. For open-ended workflows, add a Generate step, turn on Agent if needed, and define the target outcome.
  — <https://developers.google.com/opal/Agent_Mode>
3. Reference needed capabilities with the @ menu, such as @Search or @Memory, then link inputs, generation steps, and outputs in the visual editor.
  — <https://developers.google.com/opal/Agent_Mode>
4. Preview the app with representative inputs, inspect the resulting graph, and refine prompts or nodes before sharing.
  — <https://developers.google.com/opal/quickstart>
5. Keep an Opal private by default. When sharing, restrict users to the app view or grant full editor and remix access.
  — <https://developers.google.com/opal/faq>

## Best practices

- Remix an existing Gallery app rather than designing the first workflow on an empty canvas.
  — <https://developers.google.com/opal/quickstart>
- For Agent Mode, specify the goal and required output rather than prescribing every intermediate step.
  — <https://developers.google.com/opal/Agent_Mode>
- Call tools explicitly with @ when you need a particular capability, which official documentation describes as more precise.
  — <https://developers.google.com/opal/Agent_Mode>
- Test prompts and the full workflow before relying on it, because Opal can make mistakes.
  — <https://developers.google.com/opal/faq>
- Treat remix and editor sharing as prompt disclosure: sharing exposes prompts, the workflow graph, and the underlying Drive file.
  — <https://developers.google.com/opal/faq>

## Superseded by this

- **2025-07-25** — The original U.S.-only public beta access rule is obsolete: the current FAQ lists supported countries instead of restricting access to the U.S.
- **Before 2026-02-25** — Treating every Opal purely as a static prompt chain is obsolete for open-ended tasks; Agent Mode adds tool selection, memory, routing, and interactive chat. Fixed workflows remain appropriate for rigid or high-precision logic.

## Still unknown

- We ran no signed-in tests, leaving quotas, billing, publication caps, and account-specific feature availability unverified.
- Chinese-language searches found no first-party Simplified-Chinese Opal documentation, so guidance relies entirely on official English sources.
- Availability remains country-specific; check the current official FAQ before committing a workflow to Opal.

## Sources

| source | title | read |
|---|---|---|
| https://developers.googleblog.com/en/introducing-opal/ | Introducing Opal: describe, create, and share your AI mini-apps | 2026-09-04 |
| https://opal.google/landing/ | Opal [Experiment] | 2026-09-04 |
| https://blog.google/innovation-and-ai/models-and-research/google-labs/opal-agent/ | Build dynamic agentic workflows in Opal | 2026-09-04 |
| https://developers.google.com/opal/ | Opal | Google for Developers | 2026-09-04 |
| https://developers.google.com/opal/quickstart | Quickstart | Opal | Google for Developers | 2026-09-04 |
| https://developers.google.com/opal/Agent_Mode | Agent Mode in Opal | Google for Developers | 2026-09-04 |
| https://developers.google.com/opal/faq | Frequently asked questions and best practices | Opal | Google for Developers | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:google-opal`, thread `google-opal`, 1 dated events 2025-07-25 → 2025-07-25.
- **Practical note:** From 2025-07-25, practitioners could evaluate Google Opal through Google's official project introduction and linked web entry point; the supplied evidence does not establish a later workflow or capability change.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.