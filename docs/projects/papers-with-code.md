---
title: Papers with Code
category: projects

tags: [papers-with-code, papers-with-code-development, project]
aliases: ["Papers with Code"]
---

# Papers with Code

**Development line:** `project:papers-with-code` · thread `papers-with-code-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: medium

## What it is

Papers with Code is a Hugging Face–hosted revival of the former research index for practitioners who need to find papers, implementations, tasks, datasets, and evaluation results.

- Paper discovery to find publications and linked implementations.
- Task and benchmark pages to navigate datasets and metrics.
- Multi-metric leaderboards to compare model performance.
- Code links to inspect reference implementations.
- Result submissions to add papers and code to the index.

The catalog expands continuously, with automated enrichment for parts of the index. A leaderboard rank narrows the candidate set, but does not prove a result will reproduce in a target environment.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-05-19: Papers with Code became available at the new paperswithcode.co domain shortly after its relaunch. A May 24 maintainer update places the launch one week earlier. The dated link alone does not preserve the original claim, but available evidence points to the revived service rather than a legacy .com update.
- 2026-05-24: Added multi-metric benchmark tables, external-paper submission, paper lineage, method pages, leaderboard image export, and about 3,000 evaluations.
- 2026-06-22: Added SOTA badges for top-three benchmark scores, third-party evaluation results, and additional tasks and benchmarks. The trend score now also uses activity on linked Hugging Face artifacts.

## How to use this

As of 2026-05-19, no practice change can be established from the dated Papers with Code homepage link alone.

1. Open the homepage, search or browse by research task, then open candidate paper pages and their linked implementations.
  — <https://paperswithcode.co/>
2. Compare models on the relevant task or benchmark; read every metric rather than relying on a single rank.
  — <https://huggingface.co/blog/nielsr/paperswithcode-launch>
3. Submit an arXiv paper, repository, blog post, or other supported external paper through the submission page when adding work to the index.
  — <https://paperswithcode.co/submit>
4. Use the task catalog to discover benchmarks and check whether a paper's reported result is first-party or an external evaluation.
  — <https://huggingface.co/blog/nielsr/updates-to-pwc>

## Best practices

- Compare accuracy with the accompanying efficiency metric where the benchmark exposes more than one metric; for example, WER with RTFx or mAP with FPS.
  — <https://huggingface.co/blog/nielsr/paperswithcode-launch>
- Treat the trending feed as discovery, not a quality ranking: its score incorporates GitHub star velocity and activity on linked Hugging Face artifacts.
  — <https://huggingface.co/blog/nielsr/updates-to-pwc>
- Separate paper-authored results from third-party evaluations before using a leaderboard number for a technical decision.
  — <https://huggingface.co/blog/nielsr/updates-to-pwc>

## Superseded by this

- Before 2026-05-24: guidance treating the legacy Papers with Code catalog as the only current interface is obsolete; the active service is paperswithcode.co and supports submissions beyond arXiv.
- Before 2026-06-22: guidance expecting only paper-introduced evaluations is incomplete because the revived service also displays external evaluations.

## Still unknown

- The text of the 2026-05-19 item is unavailable, so we cannot reconstruct the exact assertion made on that date from its URL alone.
- The maintained site confirms the relaunch happened roughly a week before 2026-05-24, while a first-person launch post is dated 2026-05-18; the available first-party update does not establish one exact launch timestamp.
- No primary source reviewed here states a formal verification policy or coverage guarantee for every automatically enriched record.

## Sources

| source | title | read |
|---|---|---|
| https://paperswithcode.co/ | Papers with Code — Trending research and open source | 2026-09-05 |
| https://huggingface.co/blog/nielsr/paperswithcode-launch | Relaunching PapersWithCode with new features | 2026-09-05 |
| https://huggingface.co/blog/nielsr/updates-to-pwc | New updates to Papers with Code | 2026-09-05 |
| https://paperswithcode.co/submit | Papers with Code submission page | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:papers-with-code`, thread `papers-with-code-development`, 0 dated events - → -.
- **Practical note:** As of 2026-05-19, no practice change can be established from the dated Papers with Code homepage link alone.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
