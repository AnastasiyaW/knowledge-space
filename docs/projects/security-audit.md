---
title: "Security Audit: security-audit — Security Audit"
category: "projects"
date: 2026-09-17
tags: ["project", "security-audit"]
aliases: ["Security Audit: security-audit"]
---

# Security Audit: security-audit — Security Audit

**Development line:** project:security-audit · thread security-audit  
**Last event:** 2026-09-17 · 1 dated since 2026-09-17 · **Researched:** 2026-11-25 · confidence: high

## What it is

security-audit is a coding-agent skill from Cloudflare that turns an agent into a security auditor.

It orchestrates isolated agents through reconnaissance, coverage-led hunting, candidate validation, structured output, independent record verification and target-neutral reporting. The repository describes it as the single-repo starting point of Cloudflare's fleet-wide vulnerability discovery harness. It is published under the MIT license.

## Development line

- **2026-09-17 — Cloudflare Security Audit Skill.** Internal skill for searching and verifying vulnerabilities through six phases: architecture reconnaissance, zone coverage hunting, independent candidate verification, structured output, fact re-verification, and goal-independent reporting. Findings are verified by a separate agent under adversarial validation.
  - The six phases are: (1) reconnaissance, mapping architecture, trust boundaries, input surfaces, prior evidence and deterministic coverage into architecture.md and coverage-ledger.json; (2) coverage-led hunting with isolated hunters assigned from ledger units and coverage critics that find gaps; (3) candidate validation, where every unique candidate goes to a fresh verifier that tries to disprove it; (4) structured output, writing confirmed, needs_validation and rejected records to findings.json and validating them against report-schema.json; (5) independent record verification by fresh agents, with another independent verifier for material replacements; (6) target-neutral reporting that derives REPORT.md, FINDINGS-DETAIL.md and NEEDS-VALIDATION.md from the verified records and the coverage ledger. The repository says this skill seeded Cloudflare's vulnerability discovery harness, described in 'Build your own vulnerability harness'. The three verdict meanings are: confirmed has a complete source trace and a bounded observed result; needs_validation has an exact unresolved fact and no severity; rejected records a disproved candidate. (undated) — <https://github.com/cloudflare/security-audit-skill>

## What changed

The skill is published as an open repository (cloudflare/security-audit-skill). It documents the six-phase workflow, the three verdicts (confirmed, needs_validation, rejected), and validator scripts for the coverage ledger and the findings file.

## How to use this

1. Install the skill from the repository (skills/security-audit) into a coding agent and ask it to audit a repo. The parent agent orchestrates isolated hunter and verifier agents through the six phases.
  — <https://github.com/cloudflare/security-audit-skill>
2. Run validate-coverage-ledger.cjs after creating the coverage ledger and after each later ledger update.
  — <https://github.com/cloudflare/security-audit-skill>
3. Run validate-findings.cjs in Phase 4, and again after every Phase 5 replacement, to check findings.json against report-schema.json.
  — <https://github.com/cloudflare/security-audit-skill>

## Best practices

- Give every unique candidate finding to a fresh verifier that tries to disprove it, rather than letting the finding agent confirm its own result.
  — <https://github.com/cloudflare/security-audit-skill>
- Keep the three verdicts distinct: confirmed needs a full source trace and bounded observed result; needs_validation names the exact unresolved fact and carries no severity; rejected records the disproved candidate.
  — <https://github.com/cloudflare/security-audit-skill>
- Run repeated audits against the same repo. Runs are additive: prior ledgers and findings are used to target gaps and revalidate changed source, and stale or unresolved work is not counted as covered.
  — <https://github.com/cloudflare/security-audit-skill>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The repository page is undated, so the release date of the skill is not stated.
- The captured repository page is truncated, so the full file list, installation instructions and the contents of the later reference files were not seen.
- The page presents the skill as a public starting point for Cloudflare's harness; it does not say how the skill is used inside Cloudflare today.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/cloudflare/security-audit-skill | GitHub - cloudflare/security-audit-skill: A coding-agent skill for multi-phase security audits with independently verified, machine-readable findings | 2026-09-17 |

## Agent brief {#agent-brief}

- **Subject:** project:security-audit, thread security-audit, 1 dated events 2026-09-17 → 2026-09-17.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
