---
title: KnowAct-GUIClaw
category: projects
date: 2026-07-18
tags: [knowact-guiclaw, project]
aliases: ["KnowAct-GUIClaw"]
---

# KnowAct-GUIClaw

**Development line:** `project:knowact-guiclaw` · thread `knowact-guiclaw`  
**Last event:** 2026-07-18 · 1 dated since 2026-07-18 · **Researched:** 2026-09-06 · confidence: medium

## What it is

KnowAct-GUIClaw is an OpenClaw-style host and GUI executor for developers automating long-horizon work across Android, iOS, HarmonyOS, and desktop.

- Routes tasks and carries typed values between apps.
- Retrieves experience memory.
- Validates reusable mobile shortcuts and skills.

## Development line

- **2026-07-18 — KnowAct-GUIClaw project site and source repository linked.** On July 18, 2026, a public message linked the KnowAct-GUIClaw project site and the KnowAct GitHub repository. This establishes a dated public association between the GUIClaw project and the KnowAct codebase, but does not evidence a particular release, feature, or implementation milestone.

## What changed

2026-07-18 — No first-party release, paper revision, or repository change is documented on this date; code had a public initial commit on 2026-07-14, and MobileWorld recorded its result on 2026-07-17.

## How to use this

As of 2026-07-18, practitioners should treat KnowAct-GUIClaw as a project with a public project page and an associated KnowAct source repository, and verify capabilities and setup directly from those resources before adoption.

1. Choose the bundled nanobot path for a WebUI, gateway, or agent host, or use standalone guiclaw when another host, script, or terminal should invoke the GUI layer.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
2. Install Python 3.11+, uv, a multimodal OpenAI-compatible provider, and only the backend extra needed for Android or HarmonyOS, desktop, or iOS; then create the YAML provider configuration.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
3. Run dry-run first; it exercises the model and agent loop without changing a real device. Then select the adb, ios, hdc, or local backend.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
4. For automation hosts, request JSON output and consume its success, error, and trace fields instead of assuming that a screen action succeeded.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>

## Best practices

- Start with dry-run and a test device or account: validation can launch intents and change application state.
  — <https://github.com/HITsz-TMG/KnowAct>
- Treat POLICY memory as advisory only; enforce mandatory restrictions with device or app permissions, backend allowlists, host approvals, or sandboxing.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
- Use the default profile for reliable native function calling; select another profile only when the model's action format matches it.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
- Validate Android shortcut candidates on an ADB device before promotion; a declared intent or deep link does not prove that the expected page opens.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>
- Do not plan on skills for macOS, Linux, or Windows: desktop skills do not retrieve, execute, extract, or evolve; memory extraction remains available.
  — <https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No primary release, commit, paper revision, or project announcement was found dated 2026-07-18, so this date cannot be treated as a distinct product release.
- The current site and repository documentation are mutable; the exact install path, package version, dependency pins, and license at the 18 July state are unverified.
- No official model checkpoint or semantic package release was identified.
- A demonstration detail conflicts across current first-party sources: the site reports a 43-minute walk for the host-recovery case, while arXiv v2 reports 13 minutes for the matching example.

## Sources

| source | title | read |
|---|---|---|
| https://shibosusu.github.io/KnowAct-GUIClaw/ | KnowAct-GUIClaw | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct | HITsz-TMG/KnowAct | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/commits/main | Commit history · HITsz-TMG/KnowAct | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/releases/tag/Result | Release GUIClaw-Result · HITsz-TMG/KnowAct | 2026-09-06 |
| https://arxiv.org/abs/2607.12625 | KnowAct-GUIClaw: Know Deeply, Act Perfectly, Personal GUI Assistant with Self-Evolving Memory and Skill | 2026-09-06 |
| https://arxiv.org/html/2607.12625v2 | KnowAct-GUIClaw technical report, arXiv v2 | 2026-09-06 |
| https://raw.githubusercontent.com/Tongyi-MAI/MobileWorld/main/site/leaderboard.json | MobileWorld leaderboard data | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/blob/main/GUIClaw/docs/guiclaw-cli.md | GUIClaw CLI and Configuration Reference | 2026-09-06 |
| https://github.com/HITsz-TMG/KnowAct/blob/main/README_CN.md | KnowAct Chinese README | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:knowact-guiclaw`, thread `knowact-guiclaw`, 1 dated events 2026-07-18 → 2026-07-18.
- **Practical note:** As of 2026-07-18, practitioners should treat KnowAct-GUIClaw as a project with a public project page and an associated KnowAct source repository, and verify capabilities and setup directly from those resources before adoption.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
