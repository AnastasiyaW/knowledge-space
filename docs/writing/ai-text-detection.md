---
title: AI Text Detection
description: Distinguish corpus-level language research, individual detection, provenance, and editorial quality.
category: concepts
tags: [writing, ai-detection, nlp, research, evaluation]
---

# AI Text Detection

Text-origin detection, factual verification, and editorial quality answer
different questions. A clear, accurate article may be AI-assisted; a human-written
article may be false. Scope checked 2026-09-06 against the primary sources below.

Do not turn a word list, a rhythm heuristic, or an uncalibrated product score
into a confident claim about an individual author's process.

## Separate the Questions

| Question | Relevant evidence | What does not answer it |
|---|---|---|
| Did language usage change across a corpus? | Corpus design, time comparison, measured vocabulary shifts | One suspicious word in one document |
| Does a detector discriminate in a defined setting? | Labeled held-out samples, fixed threshold, error rates | A vendor ranking or an unversioned accuracy claim |
| How was this particular document produced? | Available source/draft history and trustworthy provenance | Regular grammar or absence of anecdotes |
| Is this document correct and useful? | Sources, runnable examples where relevant, reader task | A low “AI probability” score |

## What the Cited Research Establishes

[Delving into LLM-assisted writing in biomedical publications through excess vocabulary](https://arxiv.org/abs/2406.07016)
studies vocabulary changes across biomedical abstracts. Its corpus-level
estimates are not an individual-document classifier or an editorial blacklist.
Use the paper's stated population and revision when discussing its estimates;
do not transplant a percentage into another language, genre, or time period.

[GPT detectors are biased against non-native English writers](https://arxiv.org/abs/2304.02819)
reports false-positive and robustness problems for the detectors and samples it
evaluated. It supports caution about those measurements, not the claim that
every current detector is equally inaccurate.

The [NIST synthetic-content transparency report](https://doi.org/10.6028/NIST.AI.100-4)
covers provenance, labeling, detection and evaluation as different technical
approaches. Provenance can add information about origin and changes; it is not
a guarantee that a statement is true or presented in context.

Source versions: arXiv 2406.07016 v5 (2025-07-03), arXiv 2304.02819 v3
(2023-07-10), and NIST AI 100-4 (2024-11-20). These dates identify the evidence,
not a benchmark of every model or detector available in September 2026.

## Evaluate a Detector Before Using Its Score

For an actual detection task, define the intended population and decision cost.
Keep training or threshold-selection material separate from held-out evaluation.

Record at least the following in the evaluation you already use:

- Detector version, preprocessing, threshold, and available score definition.
- Human and generated source groups, language, genre and document length.
- Generator identity and settings when known; mark unknown provenance explicitly.
- Counts of false positives and false negatives, with their denominators.
- Behavior on permitted editing, translation and mixed-authorship cases relevant
  to the task.

Report results for the measured groups rather than only a pooled accuracy
number. Decide whether the observed errors are tolerable for the intended use.
An unexplained score must not become proof of misconduct.

## Keep Detection Out of the Editing Objective

Edit for supported meaning, useful structure and the requested voice.
Preserve dates, numbers, versions, uncertainty and attribution.

A fixed demand for opinions, personal failure stories, unusual words or uneven
paragraph lengths can damage a factual reference. Conversely, formal prose and
parallel list items may be appropriate for contracts and instructions.
These are editorial choices, not measured authorship verdicts.

If a style flag identifies a real problem, state it directly: an ambiguous
condition, a redundant paragraph, an unsupported guarantee, or a missing source.
Do not add intentional mistakes or invented testimony to lower a detector score.

## Decision Boundaries

Use detection only for the task it was evaluated to support. If the available
evidence cannot establish origin, keep that conclusion unresolved rather than
replacing it with stylistic confidence.

For a publication-quality task, a source check and a bounded editorial review
can finish the work without solving authorship detection. For an authorship
investigation, clean prose alone is not the terminal evidence.

## Gotchas

- **Corpus-to-document leap:** a population shift is treated as proof against
  one writer. Keep the population estimate and individual claim separate.
- **Unmeasured threshold:** “three warning signs” becomes high confidence.
  Use an evaluated decision rule or state that no calibrated rule is available.
- **Detector optimization harms facts:** dates, numbers or uncertainty are
  altered to sound less synthetic. Preserve the claim before changing style.
- **Provenance is confused with truth:** authentic history is used to endorse
  a false statement. Verify the statement and its context independently.

## See Also

- [[editing-checklist]]
- [[agent-evaluation]]
