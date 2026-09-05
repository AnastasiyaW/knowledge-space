---
title: Claude Mythos
category: projects

tags: [claude-mythos, claude-mythos-security-findings, claude_mythos_security_findings, project]
aliases: ["Claude Mythos"]
---

# Claude Mythos

**Development line:** `project:claude-mythos` · thread `claude-mythos-security-findings`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: medium

## What it is

Anthropic’s invite-only model line for approved cyber defenders and critical-software teams.

- Scans owned codebases for contextual vulnerability findings and proposed fixes.
- Direct access for approved Project Glasswing partners only.
- Powers Claude Security scans without exposing direct model access.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-04-07 — Anthropic announced Claude Mythos Preview and Project Glasswing. Preview went to launch partners and more than 40 critical-infrastructure organizations for defensive work rather than general release.
- 2026-04-10 — Anthropic’s dated guidance identifies the model as Claude Mythos Preview and frames this step as operational guidance after launch, not a second model release. AI compresses vulnerability-discovery and exploit timelines; Anthropic recommends closing the patch gap and remediating KEV entries urgently.
- 2026-06-09 — Claude Mythos 5 (`claude-mythos-5`) replaced Preview for eligible Glasswing participants. It shares Fable 5’s base model while removing cyber safeguards for approved users; documented limits were 1M context, 128K output, and $10/$50 per million input/output tokens.
- 2026-08-21 — Claude Security public beta for Enterprise began running repository scans on Mythos 5, returning findings and suggested fixes without direct Mythos prompting.
- 2026-08-31 — Claude Mythos 5.1 was designated a limited-availability Covered Model for approved partners.
- 2026-09-01 — Claude Mythos 5.1 became the current direct-access Mythos model, still invitation-only through Project Glasswing.

## How to use this

As of 2026-04-10, make no operational change from this line until we retrieve and review the underlying post or source evidence.

1. Enable Claude Security in organization settings under Claude Enterprise.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
2. Connect an authorized GitHub account, then select an owned GitHub.com or GitHub Enterprise Server repository in Claude Security.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
3. Run the scan, then inspect the CWE category, severity, confidence, reproduction path, and suggested fix for each finding.
  — <https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders>
4. Open a proposed fix in Claude Code, then have a human review, test, and approve it before implementation.
  — <https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders>
5. For direct Mythos 5.1 use, obtain Project Glasswing approval through an Anthropic, AWS, or Google Cloud account team; use model ID `claude-mythos-5-1` only after access is granted.
  — <https://platform.claude.com/docs/en/models/mythos-5-1/overview>

## Best practices

- Scan only code the organization owns or has rights to scan.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
- Treat scans as stochastic evidence, not a replacement for validation; severity settings are not configurable.
  — <https://support.claude.com/en/articles/14661296-use-claude-security>
- Patch internet-facing systems within 24 hours of an available exploit; remediate KEV entries first and prioritize the remaining queue with EPSS.
  — <https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense>
- Send a vulnerability report only after human verification; include the vulnerable code path, a runnable reproduction, a proposed patch, and disclose AI involvement.
  — <https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense>
- Start AI alert triage with read-only access and measure agreement with a human reviewer before expanding automation.
  — <https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense>

## Superseded by this

- 2026-06-09 — Claude Mythos Preview is deprecated; eligible users were moved to Claude Mythos 5.
- 2026-09-01 — Claude Mythos 5 is no longer the current direct-access target; eligible partners should migrate to Claude Mythos 5.1.
- 2026-08-21 — Direct prompting is no longer required for Mythos: Claude Security returns bounded defensive findings without exposing the model.

## Still unknown

- The 2026-04-10 entry has no URL or text, so its exact claim cannot be matched conclusively to the dated Anthropic guidance.
- Current documentation names Mythos 5 for Claude Security scans and Mythos 5.1 for direct partner access; it does not confirm that Claude Security has moved to 5.1.
- No public self-service path to direct Mythos 5.1 access is documented.

## Sources

| source | title | read |
|---|---|---|
| https://www.anthropic.com/research/mythos-preview | Assessing Claude Mythos Preview’s cybersecurity capabilities | 2026-09-05 |
| https://www.anthropic.com/glasswing | Project Glasswing: Securing critical software for the AI era | 2026-09-05 |
| https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense | Preparing your security program for AI-accelerated offense | 2026-09-05 |
| https://www.anthropic.com/news/claude-fable-5-mythos-5 | Claude Fable 5 and Claude Mythos 5 | 2026-09-05 |
| https://platform.claude.com/docs/en/models/mythos-5/overview | Claude Mythos 5 - Claude Platform Docs | 2026-09-05 |
| https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders | Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders | 2026-09-05 |
| https://platform.claude.com/docs/en/models/mythos-5-1/overview | Claude Mythos 5.1 - Claude Platform Docs | 2026-09-05 |
| https://support.claude.com/en/articles/14661296-use-claude-security | Use Claude Security | 2026-09-05 |
| https://support.claude.com/en/articles/15425695-covered-models | Covered Models | 2026-09-05 |
| https://platform.claude.com/docs/en/about-claude/model-deprecations | Model deprecations - Claude Platform Docs | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:claude-mythos`, thread `claude-mythos-security-findings`, 0 dated events - → -.
- **Practical note:** As of 2026-04-10, make no operational change from this line until the underlying post or source evidence can be retrieved and reviewed.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.