---
title: ResearchStudio
category: projects
date: 2026-07-07
tags: [project, researchstudio]
aliases: ["ResearchStudio"]
---

# ResearchStudio

**Development line:** `project:researchstudio` · thread `researchstudio`  
**Last event:** 2026-07-07 · 1 dated since 2026-07-07 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ResearchStudio is an MIT-licensed Claude Code and Codex skill suite for two research stages.

- Idea: searches literature, explores directions, and checks prior-art collisions to produce an idea card.
- Reel: turns one paper PDF into a poster, narrated video, bilingual blog, and interactive reel.

## Development line

- **2026-07-07 — ResearchStudio public project references recorded.** On 2026-07-07, public references appeared for the Microsoft ResearchStudio project site and its GitHub repository. They show the project exists publicly, but confirm no release version, feature set, or launch status.

## What changed

- 2026-07-03 — ResearchStudio-Idea released the pre-paper workflow: IdeaSpark, Paper-Search, and Scoop-Check.
- 2026-07-05 — Companion Idea and Reel papers documented the evidence-grounded ideation and shared-extraction dissemination designs.
- 2026-07-08 — ResearchStudio-Reel released the five-skill post-paper pipeline for poster, video, bilingual blog, and interactive reel outputs.
- 2026-08-13 — IdeaSpark began retaining the full query, resolving named papers, and recording whether selection followed or departed from a stated solution direction.
- 2026-08-25 — Trending Paper released as a Reels-based entry point for browsing research.
- 2026-09-03 — IdeaSpark added a warn-level Chinese word-order validator.

## How to use this

Check the official ResearchStudio site and source repository before adopting the project as of 2026-07-07. That reference alone does not confirm any specific workflow, capability, or release.

1. Create an isolated Python environment with conda (Python 3.10+) or uv, then install from a clone with install.sh or through the interactive npx installer.
  — <https://github.com/microsoft/ResearchStudio/blob/main/README.md>
2. For an early research direction, invoke IdeaSpark with the problem plus any constraints, seed papers, and compute budget; use Paper-Search and Scoop-Check when those parts are needed separately.
  — <https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea>
3. For a finished paper, run Paper2Assets once, then use its shared bundle for Paper2Poster, Paper2Video, Paper2Blog, and Paper2Reel.
  — <https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md>
4. Review an interactive reel through the supplied HTTP server rather than opening its HTML file directly, because video seeking needs HTTP Range support.
  — <https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md>

## Best practices

- Use the recommended capable-model floor and an isolated environment before installing the skills.
  — <https://github.com/microsoft/ResearchStudio/blob/main/README.md>
- Give IdeaSpark concrete constraints, seed papers, and compute limits; run the prior-art check before treating a novelty claim as actionable.
  — <https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea>
- Reuse one Paper2Assets bundle across poster, video, blog, and reel generation so the deliverables share the same extracted evidence.
  — <https://microsoft.github.io/ResearchStudio/reel-page/>
- Keep intermediate HTML during Reel runs and validate the final viewer through serve_reel.py.
  — <https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md>
- For Chinese Idea outputs, update to the version with the word-order validator and review its warnings instead of relying on a generic translation instruction.
  — <https://github.com/microsoft/ResearchStudio/commit/2540dde4be02dc841444f4ef7d81aa73aa6cf86e>

## Superseded by this

- 2026-07-07 — Describing ResearchStudio as a same-day complete-lifecycle release is unsupported: official history places Idea on 2026-07-03 and Reel on 2026-07-08.
- 2026-08-13 — Guidance that treats a bare topic as the whole IdeaSpark brief is superseded by query preservation, named-paper resolution, and explicit solution-direction disposition.
- 2026-09-03 — “Natural Chinese, not word-for-word” as the sole control is superseded by a documented warn-level word-order validator.

## Still unknown

- No first-party release entry identifies a distinct ResearchStudio change on 2026-07-07; without the original source text, that date can only be treated as a discovery point between the Idea and Reel releases.
- The repository does not expose a tagged-version compatibility matrix, so exact dependency and runtime reproducibility remain unverified.
- We did not independently reproduce the published benchmark claims.

## Sources

| source | title | read |
|---|---|---|
| https://microsoft.github.io/ResearchStudio/ | ResearchStudio — Your AI co-author, from research problem to publication | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio | GitHub — microsoft/ResearchStudio | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/blob/main/README.md | ResearchStudio README | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea | ResearchStudio-Idea | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md | ResearchStudio-Reel README | 2026-09-05 |
| https://microsoft.github.io/ResearchStudio/reel-page/ | ResearchStudio-Reel Gallery | 2026-09-05 |
| https://arxiv.org/abs/2607.04439 | ResearchStudio-Idea: An Evidence-Grounded Research-Ideation Skill Suite from ML Conference Outcomes | 2026-09-05 |
| https://arxiv.org/abs/2607.04438 | ResearchStudio-Reel: Automate the Last Mile of Research from Paper to Poster, Video, and Blog | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/commits/main | ResearchStudio commit history | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/commit/2540dde4be02dc841444f4ef7d81aa73aa6cf86e | feat(idea-spark): Chinese word order is a rule, not a request | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:researchstudio`, thread `researchstudio`, 1 dated events 2026-07-07 → 2026-07-07.
- **Practical note:** As of 2026-07-07, practitioners can consult the official ResearchStudio site and source repository before evaluating or adopting the project; this line alone does not establish any specific workflow, capability, or release.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.